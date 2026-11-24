# -*- coding: utf-8 -*-
"""
Local Hybrid RAG Engine V2 (SQLite FTS5 BM25 + 2-Stage AND/OR Retrieval +
Authority & Coverage Re-Ranking + Real-Time Incremental Upsert + Pipeline Reader)
Indexes the entire Obsidian Second Brain Vault (~100% of 4,980 workspace documents)
into a fast local SQLite FTS5 database (config/career_os_rag.db).
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
EXCEL_PIPELINE_PATH = os.path.join(BASE_DIR, "00_Aktuelle_Bewerbungsunterlagen", "Bewerbungsverlauf.xlsx")

CHUNK_TARGET_CHARS = 2800
CHUNK_MAX_CHARS = 4200

STOPWORDS = {
    "wie", "was", "wer", "welche", "welcher", "welches", "und", "oder", "der", "die", "das",
    "ein", "eine", "einen", "einem", "mit", "bei", "von", "zu", "zum", "zur", "im", "in",
    "ist", "sind", "war", "hat", "haben", "mein", "meine", "ich", "mir", "ueber", "über",
    "fuer", "für", "auf", "aus", "als", "des", "dem", "den", "sich", "noch", "auch",
    "the", "and", "for", "with", "from", "what", "how", "about"
}

TYPE_AUTHORITY = {
    "zettel": 1.45,
    "interview-prep": 1.42,
    "moc": 1.25,
    "hub": 1.25,
    "module": 1.15,
    "concept": 1.00,
    "log": 0.45,
}


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


def _refresh_metadata(cur):
    row = cur.execute("SELECT COUNT(DISTINCT file_rel), COUNT(*), COALESCE(SUM(char_len), 0) FROM chunks").fetchone()
    total_files, total_chunks, total_chars = row[0], row[1], row[2]
    cur.execute("INSERT OR REPLACE INTO metadata VALUES ('built_at', ?)", (datetime.now().isoformat(),))
    cur.execute("INSERT OR REPLACE INTO metadata VALUES ('total_files', ?)", (str(total_files),))
    cur.execute("INSERT OR REPLACE INTO metadata VALUES ('total_chunks', ?)", (str(total_chunks),))
    cur.execute("INSERT OR REPLACE INTO metadata VALUES ('total_chars', ?)", (str(total_chars),))
    return total_files, total_chunks, total_chars


def build_index():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    tmp_db = DB_PATH + ".tmp"
    if os.path.exists(tmp_db):
        os.remove(tmp_db)

    conn = sqlite3.connect(tmp_db)
    cur = conn.cursor()
    cur.execute("PRAGMA journal_mode=OFF;")
    cur.execute("PRAGMA synchronous=OFF;")

    cur.execute("CREATE TABLE metadata (k TEXT PRIMARY KEY, v TEXT)")
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
    cur.execute("CREATE INDEX idx_chunks_file_rel ON chunks(file_rel)")
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

    print("[*] Rebuilding FTS5 inverted BM25 index...")
    cur.execute("INSERT INTO chunks_fts(chunks_fts) VALUES('rebuild')")
    total_files, total_chunks, total_chars = _refresh_metadata(cur)
    conn.commit()
    conn.close()

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    os.replace(tmp_db, DB_PATH)
    size_mb = os.path.getsize(DB_PATH) / (1024 * 1024)
    print(f"[OK] Local RAG index built: {DB_PATH} ({size_mb:.2f} MB | {total_files} notes | {total_chunks:,} chunks | {total_chars:,} chars)")
    return {"files": total_files, "chunks": total_chunks, "chars": total_chars, "size_mb": round(size_mb, 2)}


def upsert_note(file_path):
    """Incrementally re-indexes a single Markdown note into SQLite FTS5 in <20 ms."""
    if not os.path.exists(DB_PATH) or not os.path.exists(file_path):
        return {"ok": False, "error": "DB or target note missing"}

    rel = os.path.relpath(file_path, VAULT_DIR)
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        raw = f.read()

    fm, body = parse_frontmatter(raw)
    file_chunks = chunk_markdown(rel, fm, body)

    conn = sqlite3.connect(DB_PATH, timeout=5.0)
    cur = conn.cursor()
    try:
        old_rows = cur.execute(
            "SELECT id, title, section, file_rel, domain, content FROM chunks WHERE file_rel = ?",
            (rel,)
        ).fetchall()
        for r_id, r_title, r_sec, r_file, r_dom, r_cont in old_rows:
            cur.execute(
                """INSERT INTO chunks_fts(chunks_fts, rowid, title, section, file_rel, domain, content)
                   VALUES('delete', ?, ?, ?, ?, ?, ?)""",
                (r_id, r_title, r_sec, r_file, r_dom, r_cont)
            )
        cur.execute("DELETE FROM chunks WHERE file_rel = ?", (rel,))

        for c in file_chunks:
            cur.execute(
                """INSERT INTO chunks (file_rel, doc_id, title, domain, doc_type, section, content, char_len)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (c["file_rel"], c["doc_id"], c["title"], c["domain"], c["doc_type"], c["section"], c["content"], c["char_len"])
            )
            new_id = cur.lastrowid
            cur.execute(
                """INSERT INTO chunks_fts(rowid, title, section, file_rel, domain, content)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (new_id, c["title"], c["section"], c["file_rel"], c["domain"], c["content"])
            )

        _refresh_metadata(cur)
        conn.commit()
        return {"ok": True, "file": rel, "chunks": len(file_chunks)}
    finally:
        conn.close()


def _extract_terms(query):
    tokens = re.findall(r"[A-Za-z0-9\u00C0-\u017F_]{2,}", query)
    clean = [t for t in tokens if t.lower() not in STOPWORDS]
    if not clean:
        clean = tokens
    return clean[:12]


def _smart_snippet(content, terms, max_len=900):
    """Centers snippet cleanly around the best term match in long chunks."""
    if len(content) <= max_len:
        return content
    lower = content.lower()
    best_pos = None
    for t in terms:
        idx = lower.find(t.lower())
        if idx != -1 and (best_pos is None or idx < best_pos):
            best_pos = idx
    if best_pos is None or best_pos < 250:
        return content[:max_len]
    start = max(0, best_pos - 180)
    end = min(len(content), start + max_len)
    prefix = "..." if start > 0 else ""
    suffix = "..." if end < len(content) else ""
    return prefix + content[start:end].strip() + suffix


def _run_fts_stage(cur, expr, domain, limit):
    sql = """
        SELECT
            c.id,
            c.file_rel,
            c.title,
            c.domain,
            c.doc_type,
            c.section,
            c.content,
            bm25(chunks_fts, 4.5, 3.2, 2.0, 1.5, 1.0) AS raw_bm25
        FROM chunks_fts
        JOIN chunks c ON chunks_fts.rowid = c.id
        WHERE chunks_fts MATCH ?
    """
    params = [expr]
    if domain:
        sql += " AND c.domain = ?"
        params.append(domain)
    sql += " ORDER BY raw_bm25 LIMIT ?"
    params.append(int(limit))
    try:
        return cur.execute(sql, params).fetchall()
    except sqlite3.OperationalError:
        return []


def search(query, top_k=8, domain=None, max_per_file=2):
    if not os.path.exists(DB_PATH):
        return []
    terms = _extract_terms(query)
    if not terms:
        return []

    conn = sqlite3.connect(DB_PATH, timeout=5.0)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    candidates = {}
    try:
        # Stage 1: Multi-term AND precision pass
        if 2 <= len(terms) <= 5:
            and_expr = " AND ".join(f'"{t}"*' for t in terms[:5])
            for r in _run_fts_stage(cur, and_expr, domain, max(top_k * 5, 30)):
                candidates[r["id"]] = (r, 1.28)

        # Stage 2: High-recall OR fallback pass
        or_expr = " OR ".join(f'"{t}"*' for t in terms)
        for r in _run_fts_stage(cur, or_expr, domain, max(top_k * 8, 50)):
            if r["id"] not in candidates:
                candidates[r["id"]] = (r, 1.0)
    finally:
        conn.close()

    if not candidates:
        return []

    lower_terms = [t.lower() for t in terms]
    scored = []
    for r, stage_boost in candidates.values():
        base_bm25 = max(-float(r["raw_bm25"]), 0.01)
        doc_type = r["doc_type"] or "concept"
        file_rel = r["file_rel"]
        dom = r["domain"] or "general"

        auth_w = TYPE_AUTHORITY.get(doc_type, 1.0)
        if doc_type == "concept" and ("_Volltext" in file_rel or "_Band_" in file_rel):
            auth_w *= 0.88
        if dom == "system-governance" and "changelog" in file_rel.lower():
            auth_w *= 0.45

        hay_title = f"{r['title']} {r['section']}".lower()
        hay_all = f"{hay_title} {r['content'][:2500].lower()}"
        matched = [t for t in lower_terms if t in hay_all]
        coverage_w = 1.0 + 0.16 * len(matched)
        if any(t in hay_title for t in lower_terms):
            coverage_w += 0.22

        final_score = round(base_bm25 * stage_boost * auth_w * coverage_w, 3)
        scored.append({
            "id": r["id"],
            "file": file_rel,
            "title": r["title"],
            "domain": dom,
            "type": doc_type,
            "section": r["section"],
            "score": final_score,
            "matched_terms": matched,
            "snippet": _smart_snippet(r["content"], terms, max_len=900),
            "content": r["content"]
        })

    scored.sort(key=lambda x: x["score"], reverse=True)

    # Diversity cap: avoid single large dossier monopolizing top results
    diverse = []
    overflow = []
    file_counts = {}
    for item in scored:
        cnt = file_counts.get(item["file"], 0)
        if cnt < max_per_file:
            diverse.append(item)
            file_counts[item["file"]] = cnt + 1
        else:
            overflow.append(item)
        if len(diverse) >= int(top_k):
            break

    while len(diverse) < int(top_k) and overflow:
        diverse.append(overflow.pop(0))
    return diverse[:int(top_k)]


def get_stats():
    if not os.path.exists(DB_PATH):
        return {"exists": False}
    conn = sqlite3.connect(DB_PATH, timeout=5.0)
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


def get_pipeline_data(excel_path=None, max_active=15):
    """Shared parser for Bewerbungsverlauf.xlsx used by both Portal API and Telegram Agent."""
    path = excel_path or EXCEL_PIPELINE_PATH
    if not os.path.exists(path):
        return {"ok": False, "error": "Bewerbungsverlauf.xlsx nicht gefunden", "interviews": [], "open_tier1": [], "open_count": 0, "closed_count": 0, "total_rows": 0}
    try:
        import openpyxl
        wb = openpyxl.load_workbook(path, data_only=True)
        ws = wb["Bewerbungsverlauf"]
        interviews = []
        active = []
        closed = 0
        for r in range(2, ws.max_row + 1):
            comp = str(ws.cell(r, 1).value or "").strip()
            role = str(ws.cell(r, 2).value or "").strip()
            date_sent = str(ws.cell(r, 3).value or "-").strip()
            g1 = str(ws.cell(r, 5).value or "-").strip()
            g2 = str(ws.cell(r, 6).value or "-").strip()
            status = str(ws.cell(r, 7).value or "").strip()
            if not comp or comp == "Terminerinnerung":
                continue
            item = {
                "company": comp,
                "role": role,
                "submitted": date_sent,
                "g1": g1,
                "g2": g2,
                "status": status
            }
            if "Absage" in status:
                closed += 1
            elif any(k in status for k in ["⭐", "🚀", "Gespräch", "Interview", "Einladung"]):
                interviews.append(item)
            else:
                active.append(item)
        return {
            "ok": True,
            "interviews": interviews,
            "open_tier1": active[:max_active],
            "open_count": len(active),
            "closed_count": closed,
            "total_rows": len(interviews) + len(active) + closed
        }
    except Exception as e:
        return {"ok": False, "error": str(e), "interviews": [], "open_tier1": [], "open_count": 0, "closed_count": 0, "total_rows": 0}


def synthesize_answer(query, top_k=6):
    hits = search(query, top_k=top_k)
    key = load_api_key()
    if not key:
        return {"answer": "Kein GEMINI_API_KEY konfiguriert.", "sources": hits}

    context_blocks = []
    for i, h in enumerate(hits, 1):
        context_blocks.append(f"[Quelle {i}: {h['file']} | Typ: {h['type']} | Abschnitt: {h['section']}]\n{h['content'][:2200]}")
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
            with urllib.request.urlopen(req, timeout=22.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                txt = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                if txt:
                    return {"answer": txt, "model": model, "sources": [{"file": h["file"], "title": h["title"], "type": h["type"], "section": h["section"], "score": h["score"]} for h in hits]}
        except Exception:
            continue
    return {"answer": "Synthese fehlgeschlagen; zeige Rohtreffer.", "model": "fallback-raw", "sources": [{"file": h["file"], "title": h["title"], "type": h["type"], "section": h["section"], "score": h["score"]} for h in hits]}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Local Career OS Hybrid RAG Engine V2")
    parser.add_argument("--build", action="store_true", help="Rebuilds FTS5 chunk index from Obsidian Vault")
    parser.add_argument("--upsert", type=str, help="Incrementally upserts a single .md file into FTS5 index")
    parser.add_argument("--stats", action="store_true", help="Shows RAG index statistics")
    parser.add_argument("--pipeline", action="store_true", help="Shows live application pipeline JSON")
    parser.add_argument("--query", type=str, help="Searches indexed chunks via Hybrid BM25")
    parser.add_argument("--ask", type=str, help="RAG query + Gemini synthesis")
    args = parser.parse_args()

    if args.build:
        build_index()
    elif args.upsert:
        print(json.dumps(upsert_note(args.upsert), indent=2, ensure_ascii=False))
    elif args.stats:
        print(json.dumps(get_stats(), indent=2, ensure_ascii=False))
    elif args.pipeline:
        print(json.dumps(get_pipeline_data(), indent=2, ensure_ascii=False))
    elif args.query:
        res = search(args.query, top_k=6)
        for idx, r in enumerate(res, 1):
            print(f"\n[{idx}] Score={r['score']} | {r['type']} | {r['file']} :: {r['section']}")
            print(r["snippet"][:320].replace("\n", " "))
    elif args.ask:
        print(json.dumps(synthesize_answer(args.ask), indent=2, ensure_ascii=False))
    else:
        print(json.dumps(get_stats(), indent=2, ensure_ascii=False))
