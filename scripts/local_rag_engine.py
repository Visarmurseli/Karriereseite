# -*- coding: utf-8 -*-
"""
Local Hybrid RAG Engine (SQLite FTS5 BM25 + Heading-Aware Chunking + Gemini Synthesis)
Indexes the entire Obsidian Second Brain Vault (~100% of 5,002 workspace documents)
into a fast local SQLite FTS5 database (config/career_os_rag.db) for sub-second retrieval
via CLI, Telegram Career Agent, and the local Career Portal API.
"""

import os
import re
import sys
import json
import sqlite3
import urllib.request
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
VAULT_DIR = r"C:\Users\SHQIPTAR634\Documents\Obsidian Vault"
DB_PATH = os.path.join(BASE_DIR, "config", "career_os_rag.db")
ENV_PATH = os.path.join(BASE_DIR, ".env")

CHUNK_TARGET_CHARS = 2800
CHUNK_MAX_CHARS = 4200


def load_api_key():
    key = os.environ.get("GEMINI_API_KEY", "")
    if not key and os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if line.startswith("GEMINI_API_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    return key


def parse_frontmatter(text):
    fm = {}
    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', text, re.DOTALL)
    body = text
    if fm_match:
        body = text[len(fm_match.group(0)):]
        for line in fm_match.group(1).splitlines():
            if ":" in line and not line.strip().startswith("-"):
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, body


def chunk_markdown(rel_path, fm, body):
    """Splits markdown body cleanly along heading boundaries (H1-H4) into RAG-optimal chunks."""
    title = fm.get("title", os.path.splitext(os.path.basename(rel_path))[0])
    domain = fm.get("domain", "general")
    doc_type = fm.get("type", "concept")

    sections = re.split(r'\n(?=#{1,4}\s+)', body)
    chunks = []
    cur_section = title
    cur_buf = []
    cur_len = 0

    def flush():
        nonlocal cur_buf, cur_len
        if not cur_buf:
            return
        text_out = "\n".join(cur_buf).strip()
        if len(text_out) >= 40:
            chunks.append({
                "file_rel": rel_path,
                "doc_id": fm.get("id", rel_path),
                "title": title,
                "domain": domain,
                "doc_type": doc_type,
                "section": cur_section[:180],
                "content": text_out,
                "char_len": len(text_out)
            })
        cur_buf = []
        cur_len = 0

    for sec in sections:
        sec_clean = sec.strip()
        if not sec_clean:
            continue
        lines = sec_clean.splitlines()
        heading_line = lines[0].lstrip("#").strip() if lines[0].startswith("#") else cur_section

        # If single heading block is massive (> CHUNK_MAX_CHARS), split by paragraphs
        if len(sec_clean) > CHUNK_MAX_CHARS:
            flush()
            cur_section = heading_line
            paras = re.split(r'\n{2,}', sec_clean)
            pbuf = []
            plen = 0
            for p in paras:
                if pbuf and plen + len(p) > CHUNK_TARGET_CHARS:
                    cur_buf = pbuf
                    cur_len = plen
                    flush()
                    pbuf = [p[:CHUNK_MAX_CHARS]]
                    plen = len(pbuf[0])
                else:
                    pbuf.append(p)
                    plen += len(p) + 2
            if pbuf:
                cur_buf = pbuf
                cur_len = plen
                flush()
            continue

        if cur_buf and cur_len + len(sec_clean) > CHUNK_TARGET_CHARS:
            flush()
            cur_section = heading_line

        if not cur_buf:
            cur_section = heading_line
        cur_buf.append(sec_clean)
        cur_len += len(sec_clean) + 2

    flush()
    return chunks


def build_index():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    tmp_db = DB_PATH + ".tmp"
    if os.path.exists(tmp_db):
        os.remove(tmp_db)

    conn = sqlite3.connect(tmp_db)
    cur = conn.cursor()
    cur.execute("PRAGMA journal_mode=OFF;")
    cur.execute("PRAGMA synchronous=OFF;")

    cur.execute("""
        CREATE TABLE metadata (
            k TEXT PRIMARY KEY,
            v TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_rel TEXT NOT NULL,
            doc_id TEXT,
            title TEXT,
            domain TEXT,
            doc_type TEXT,
            section TEXT,
            content TEXT NOT NULL,
            char_len INTEGER
        )
    """)
    cur.execute("""
        CREATE VIRTUAL TABLE chunks_fts USING fts5(
            title,
            section,
            file_rel,
            domain,
            content,
            content='chunks',
            content_rowid='id',
            tokenize='unicode61 remove_diacritics 2'
        )
    """)

    total_files = 0
    total_chunks = 0
    total_chars = 0

    for root, dirs, files in os.walk(VAULT_DIR):
        if ".obsidian" in root:
            continue
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            fp = os.path.join(root, fn)
            rel = os.path.relpath(fp, VAULT_DIR)
            with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                raw = f.read()

            fm, body = parse_frontmatter(raw)
            file_chunks = chunk_markdown(rel, fm, body)
            if not file_chunks:
                continue

            cur.executemany(
                """INSERT INTO chunks (file_rel, doc_id, title, domain, doc_type, section, content, char_len)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                [(c["file_rel"], c["doc_id"], c["title"], c["domain"], c["doc_type"], c["section"], c["content"], c["char_len"]) for c in file_chunks]
            )
            total_files += 1
            total_chunks += len(file_chunks)
            total_chars += sum(c["char_len"] for c in file_chunks)

    print(f"[*] Building FTS5 inverted BM25 index across {total_chunks:,} chunks from {total_files} notes...")
    cur.execute("INSERT INTO chunks_fts(chunks_fts) VALUES('rebuild')")
    cur.execute("INSERT INTO metadata VALUES ('built_at', ?)", (datetime.now().isoformat(),))
    cur.execute("INSERT INTO metadata VALUES ('total_files', ?)", (str(total_files),))
    cur.execute("INSERT INTO metadata VALUES ('total_chunks', ?)", (str(total_chunks),))
    cur.execute("INSERT INTO metadata VALUES ('total_chars', ?)", (str(total_chars),))
    conn.commit()
    conn.close()

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    os.replace(tmp_db, DB_PATH)
    size_mb = os.path.getsize(DB_PATH) / (1024 * 1024)
    print(f"[OK] Local RAG index built: {DB_PATH} ({size_mb:.2f} MB | {total_files} notes | {total_chunks:,} chunks | {total_chars:,} chars)")
    return {"files": total_files, "chunks": total_chunks, "chars": total_chars, "size_mb": round(size_mb, 2)}


def _sanitize_fts_query(query):
    """Turns arbitrary German/English user query into safe FTS5 OR/AND match expression."""
    tokens = re.findall(r"[A-Za-z0-9\u00C0-\u017F_]{2,}", query)
    stopwords = {
        "wie", "was", "wer", "welche", "welcher", "welches", "und", "oder", "der", "die", "das",
        "ein", "eine", "einen", "einem", "mit", "bei", "von", "zu", "zum", "zur", "im", "in",
        "ist", "sind", "war", "hat", "haben", "mein", "meine", "ich", "mir", "ueber", "über",
        "the", "and", "for", "with", "from", "what", "how", "about"
    }
    clean = [t for t in tokens if t.lower() not in stopwords]
    if not clean:
        clean = tokens
    if not clean:
        return None
    # Prefix-OR matching gives high recall while BM25 ranks multi-term matches highest
    escaped = [f'"{t}"*' for t in clean[:12]]
    return " OR ".join(escaped)


def search(query, top_k=8, domain=None):
    if not os.path.exists(DB_PATH):
        return []
    fts_expr = _sanitize_fts_query(query)
    if not fts_expr:
        return []

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    sql = """
        SELECT
            c.id,
            c.file_rel,
            c.title,
            c.domain,
            c.doc_type,
            c.section,
            c.content,
            bm25(chunks_fts, 4.0, 3.0, 2.0, 1.5, 1.0) AS score
        FROM chunks_fts
        JOIN chunks c ON chunks_fts.rowid = c.id
        WHERE chunks_fts MATCH ?
    """
    params = [fts_expr]
    if domain:
        sql += " AND c.domain = ?"
        params.append(domain)
    sql += " ORDER BY score LIMIT ?"
    params.append(int(top_k))

    try:
        rows = cur.execute(sql, params).fetchall()
    except sqlite3.OperationalError:
        rows = []
    finally:
        conn.close()

    results = []
    for r in rows:
        results.append({
            "id": r["id"],
            "file": r["file_rel"],
            "title": r["title"],
            "domain": r["domain"],
            "type": r["doc_type"],
            "section": r["section"],
            "score": round(-float(r["score"]), 3),
            "snippet": r["content"][:900],
            "content": r["content"]
        })
    return results


def get_stats():
    if not os.path.exists(DB_PATH):
        return {"exists": False}
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    meta = dict(cur.execute("SELECT k, v FROM metadata").fetchall())
    conn.close()
    return {
        "exists": True,
        "built_at": meta.get("built_at"),
        "total_files": int(meta.get("total_files", 0)),
        "total_chunks": int(meta.get("total_chunks", 0)),
        "total_chars": int(meta.get("total_chars", 0)),
        "size_mb": round(os.path.getsize(DB_PATH) / (1024 * 1024), 2)
    }


def synthesize_answer(query, top_k=6):
    hits = search(query, top_k=top_k)
    key = load_api_key()
    if not key:
        return {"answer": "Kein GEMINI_API_KEY konfiguriert.", "sources": hits}

    context_blocks = []
    for i, h in enumerate(hits, 1):
        context_blocks.append(f"[Quelle {i}: {h['file']} | Abschnitt: {h['section']}]\n{h['content'][:2200]}")
    context_text = "\n\n---\n\n".join(context_blocks)

    prompt = f"""Beantworte die folgende Frage präzise auf Basis von Visar Murselis verifizierten Dokumenten.
Zitiere konkrete Quellen im Format [Quelle: Dateiname | Abschnitt]. Erfinde keine Fakten.

KONTEXT AUS DEM SECOND BRAIN:
{context_text}

FRAGE:
{query}
"""
    for model in ["gemini-3-flash-preview", "gemini-3.1-flash-lite", "gemini-3.1-pro-preview"]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2, "maxOutputTokens": 1500}
        }
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=20.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                txt = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                if txt:
                    return {"answer": txt, "model": model, "sources": [{"file": h["file"], "section": h["section"], "score": h["score"]} for h in hits]}
        except Exception:
            continue
    return {"answer": "Synthese fehlgeschlagen; zeige Rohtreffer.", "sources": hits}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Local Career OS Hybrid RAG Engine")
    parser.add_argument("--build", action="store_true", help="Rebuilds FTS5 chunk index from Obsidian Vault")
    parser.add_argument("--stats", action="store_true", help="Shows RAG index statistics")
    parser.add_argument("--query", type=str, help="Searches indexed chunks via BM25")
    parser.add_argument("--ask", type=str, help="RAG query + Gemini synthesis")
    args = parser.parse_args()

    if args.build:
        build_index()
    elif args.stats:
        print(json.dumps(get_stats(), indent=2, ensure_ascii=False))
    elif args.query:
        res = search(args.query, top_k=6)
        for idx, r in enumerate(res, 1):
            print(f"\n[{idx}] Score={r['score']} | {r['file']} :: {r['section']}")
            print(r["snippet"][:350].replace("\n", " "))
    elif args.ask:
        print(json.dumps(synthesize_answer(args.ask), indent=2, ensure_ascii=False))
    else:
        print(json.dumps(get_stats(), indent=2, ensure_ascii=False))
