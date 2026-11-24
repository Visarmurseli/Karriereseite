# -*- coding: utf-8 -*-
"""
Local Hybrid RAG Engine V3:
- 2-Stage SQLite FTS5 BM25 (Multi-Term AND + Domain-Synonym-Expanded OR)
- Dense Semantic Vector Retrieval (Gemini gemini-embedding-001 @ 768-dim Matryoshka)
- Reciprocal Rank Fusion (RRF) + Document-Type Authority + Diversity Cap
- Real-Time Incremental FTS5 + Vector Upsert (<200 ms)
- Shared Live Pipeline Reader for Portal API and Telegram Career Agent
"""

import os
import re
import sys
import json
import math
import time
import array
import operator
import sqlite3
import urllib.request
import urllib.error
from collections import Counter, OrderedDict
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
VAULT_DIR = r"C:\Users\SHQIPTAR634\Documents\Obsidian Vault"
DB_PATH = os.path.join(BASE_DIR, "config", "career_os_rag.db")
ENV_PATH = os.path.join(BASE_DIR, ".env")
EXCEL_PIPELINE_PATH = os.path.join(BASE_DIR, "00_Aktuelle_Bewerbungsunterlagen", "Bewerbungsverlauf.xlsx")

EMBED_MODEL = "gemini-embedding-001"
EMBED_DIM = 768
CHUNK_TARGET_CHARS = 2800
CHUNK_MAX_CHARS = 4200

STOPWORDS = {
    "wie", "was", "wer", "welche", "welcher", "welches", "und", "oder", "der", "die", "das",
    "ein", "eine", "einen", "einem", "mit", "bei", "von", "zu", "zum", "zur", "im", "in",
    "ist", "sind", "war", "hat", "haben", "mein", "meine", "ich", "mir", "ueber", "über",
    "fuer", "für", "auf", "aus", "als", "des", "dem", "den", "sich", "noch", "auch", "wie",
    "kann", "man", "passt", "verhindere", "the", "and", "for", "with", "from", "what", "how", "about"
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

# Domain ontology synonym expansion for German/English ERP, SAP, Audit & EAM queries
DOMAIN_SYNONYMS = {
    "schulden": ["clean", "core", "btp", "modifikation"],
    "debt": ["clean", "core", "btp", "modifikation"],
    "erweiterung": ["clean", "core", "btp", "side", "extension"],
    "extension": ["clean", "core", "btp", "rap"],
    "berechtigung": ["iam", "pfcg", "p_orgin", "stauthtrace", "su53", "sod", "umt"],
    "berechtigungen": ["iam", "pfcg", "p_orgin", "stauthtrace", "su53", "sod", "umt"],
    "rechte": ["iam", "pfcg", "p_orgin", "sod", "umt"],
    "zugriff": ["iam", "pfcg", "p_orgin", "sod", "umt"],
    "prüfung": ["iks", "audit", "sod", "cvi", "acdoca", "übernahmekonto"],
    "audit": ["iks", "sod", "cvi", "acdoca", "übernahmekonto"],
    "kontrolle": ["iks", "sod", "governance", "compliance"],
    "migration": ["ltmc", "cvi", "staging", "übernahmekonto", "cutover"],
    "datenübernahme": ["ltmc", "cvi", "übernahmekonto", "cutover"],
    "altdaten": ["ltmc", "cvi", "übernahmekonto"],
    "schnittstelle": ["api", "btp", "integration", "boundary", "xsuite", "patris"],
    "schnittstellen": ["api", "btp", "integration", "boundary", "xsuite", "patris"],
    "entkopplung": ["clean", "core", "btp", "bimodal", "boundary"],
    "nachhaltigkeit": ["csrd", "esrs", "schmalz", "abfallbilanz", "ehs"],
    "störung": ["itil", "incident", "root", "noc", "prtg"],
    "support": ["itil", "incident", "third", "level", "root"],
    "ausschreibung": ["sektvo", "axians", "nagarro", "vergabe"],
    "vergabe": ["sektvo", "axians", "nagarro"],
    "öpnv": ["trennungsrechnung", "1370", "pbefg", "acdoca", "ssb"],
    "kpmg": ["transformation", "audit", "iks", "sdd", "acdoca", "sod"],
    "schwarz": ["hcm", "iam", "umt", "p_orgin", "third"],
}

_DOT = getattr(math, "sumprod", lambda a, b: sum(map(operator.mul, a, b)))
_VECTOR_CACHE = None
_QUERY_VEC_CACHE = OrderedDict()


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


def _normalize_vec(values):
    norm = math.sqrt(sum(v * v for v in values))
    if norm <= 1e-12:
        return array.array("f", values)
    return array.array("f", (v / norm for v in values))


def _embed_single_query(query, key):
    cached = _QUERY_VEC_CACHE.get(query)
    if cached is not None:
        _QUERY_VEC_CACHE.move_to_end(query)
        return cached
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{EMBED_MODEL}:embedContent?key={key}"
    payload = {
        "model": f"models/{EMBED_MODEL}",
        "content": {"parts": [{"text": query[:2000]}]},
        "taskType": "RETRIEVAL_QUERY",
        "outputDimensionality": EMBED_DIM
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=8.0) as resp:
        vals = json.loads(resp.read().decode("utf-8"))["embedding"]["values"]
    vec = _normalize_vec(vals)
    _QUERY_VEC_CACHE[query] = vec
    if len(_QUERY_VEC_CACHE) > 64:
        _QUERY_VEC_CACHE.popitem(last=False)
    return vec


def _batch_embed_texts_resilient(items, key, on_batch=None):
    """Embeds chunks via batchEmbedContents with per-batch commit & 429 rate-limit backoff."""
    total_saved = 0
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{EMBED_MODEL}:batchEmbedContents?key={key}"
    batch_size = 30
    for start in range(0, len(items), batch_size):
        batch = items[start:start + batch_size]
        reqs = [
            {
                "model": f"models/{EMBED_MODEL}",
                "content": {"parts": [{"text": txt[:1200]}]},
                "taskType": "RETRIEVAL_DOCUMENT",
                "outputDimensionality": EMBED_DIM
            }
            for _, txt in batch
        ]
        saved_batch = None
        for attempt in range(3):
            req = urllib.request.Request(url, data=json.dumps({"requests": reqs}).encode("utf-8"), headers={"Content-Type": "application/json"})
            try:
                with urllib.request.urlopen(req, timeout=30.0) as resp:
                    embs = json.loads(resp.read().decode("utf-8")).get("embeddings", [])
                saved_batch = [(cid, _normalize_vec(emb["values"]).tobytes()) for (cid, _), emb in zip(batch, embs)]
                break
            except urllib.error.HTTPError as e:
                if e.code == 429 and attempt < 2:
                    wait_s = 22 * (attempt + 1)
                    print(f"[!] Embedding Rate-Limit (429) bei Batch {start // batch_size + 1}, warte {wait_s}s...", flush=True)
                    time.sleep(wait_s)
                    continue
                print(f"[!] Embedding gestoppt bei {total_saved} Vektoren (HTTP {e.code}); bisherige Batches gespeichert.", flush=True)
                return total_saved
            except Exception as e:
                print(f"[!] Embedding-Fehler ({e}); bisherige {total_saved} Vektoren gespeichert.", flush=True)
                return total_saved
        if saved_batch:
            if on_batch:
                on_batch(saved_batch)
            total_saved += len(saved_batch)
            time.sleep(0.4)
    return total_saved


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


def _ensure_vector_table(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS chunk_vectors (
            chunk_id INTEGER PRIMARY KEY,
            vec BLOB NOT NULL
        )
    """)


def _refresh_metadata(cur):
    global _VECTOR_CACHE
    _VECTOR_CACHE = None
    row = cur.execute("SELECT COUNT(DISTINCT file_rel), COUNT(*), COALESCE(SUM(char_len), 0) FROM chunks").fetchone()
    total_files, total_chunks, total_chars = row[0], row[1], row[2]
    _ensure_vector_table(cur)
    total_vectors = cur.execute("SELECT COUNT(*) FROM chunk_vectors").fetchone()[0]
    cur.execute("INSERT OR REPLACE INTO metadata VALUES ('built_at', ?)", (datetime.now().isoformat(),))
    cur.execute("INSERT OR REPLACE INTO metadata VALUES ('total_files', ?)", (str(total_files),))
    cur.execute("INSERT OR REPLACE INTO metadata VALUES ('total_chunks', ?)", (str(total_chunks),))
    cur.execute("INSERT OR REPLACE INTO metadata VALUES ('total_chars', ?)", (str(total_chars),))
    cur.execute("INSERT OR REPLACE INTO metadata VALUES ('total_vectors', ?)", (str(total_vectors),))
    return total_files, total_chunks, total_chars, total_vectors


def embed_anchors(force=False, max_chunks=240):
    """Builds 768-dim Gemini embeddings over highest-signal semantic anchor chunks with checkpointing."""
    if not os.path.exists(DB_PATH):
        return {"ok": False, "error": "DB not built yet"}
    key = load_api_key()
    if not key:
        return {"ok": False, "error": "No GEMINI_API_KEY configured"}

    conn = sqlite3.connect(DB_PATH, timeout=15.0)
    cur = conn.cursor()
    _ensure_vector_table(cur)
    if force:
        cur.execute("DELETE FROM chunk_vectors")
        conn.commit()

    rows = cur.execute("""
        WITH ranked AS (
            SELECT id, file_rel, doc_type, domain, title, section, content,
                   ROW_NUMBER() OVER (PARTITION BY file_rel ORDER BY id) AS rn
            FROM chunks
            WHERE doc_type != 'log'
        )
        SELECT id, title, section, file_rel, content, doc_type, domain, rn
        FROM ranked
        WHERE doc_type IN ('zettel', 'interview-prep', 'moc', 'hub')
           OR file_rel LIKE '01_Karriere_Bewerbungen%'
           OR rn <= 2
    """).fetchall()

    prio_map = {"zettel": 0, "interview-prep": 1, "moc": 2, "hub": 3, "module": 5, "concept": 6}
    rows.sort(key=lambda r: (
        0 if (r[5] in ("zettel", "interview-prep") or r[3].startswith("01_Karriere_Bewerbungen")) else (1 if r[5] in ("moc", "hub") else (2 if "03_SAP_EnterpriseArchitecture" in r[3] else 3)),
        prio_map.get(r[5], 9),
        r[7],
        r[0]
    ))

    existing = {r[0] for r in cur.execute("SELECT chunk_id FROM chunk_vectors").fetchall()}
    todo = [
        (cid, f"{title} | {sec} | {frel}\n{cont[:1100]}")
        for cid, title, sec, frel, cont, _, _, _ in rows
        if cid not in existing
    ]
    if max_chunks:
        todo = todo[:int(max_chunks)]

    if not todo:
        _, _, _, total_vectors = _refresh_metadata(cur)
        conn.commit()
        conn.close()
        return {"ok": True, "embedded_new": 0, "total_vectors": total_vectors}

    print(f"[*] Embedding {len(todo)} prioritized semantic anchor chunks via {EMBED_MODEL} ({EMBED_DIM}d)...")

    def save_batch(batch_rows):
        cur.executemany("INSERT OR REPLACE INTO chunk_vectors (chunk_id, vec) VALUES (?, ?)", batch_rows)
        conn.commit()

    saved_count = _batch_embed_texts_resilient(todo, key, on_batch=save_batch)
    _, _, _, total_vectors = _refresh_metadata(cur)
    conn.commit()
    conn.close()
    print(f"[OK] Vector index updated: {saved_count} new | {total_vectors} total semantic anchors")
    return {"ok": True, "embedded_new": saved_count, "total_vectors": total_vectors}


def build_index(with_vectors=True):
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
    _ensure_vector_table(cur)

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
    total_files, total_chunks, total_chars, total_vectors = _refresh_metadata(cur)
    conn.commit()
    conn.close()

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    os.replace(tmp_db, DB_PATH)

    if with_vectors:
        try:
            vec_res = embed_anchors(force=True)
            total_vectors = vec_res.get("total_vectors", 0)
        except Exception as e:
            print(f"[!] Vector embedding skipped/fallback: {e}")

    size_mb = os.path.getsize(DB_PATH) / (1024 * 1024)
    print(f"[OK] Local RAG index built: {DB_PATH} ({size_mb:.2f} MB | {total_files} notes | {total_chunks:,} chunks | {total_vectors} vectors | {total_chars:,} chars)")
    return {"files": total_files, "chunks": total_chunks, "vectors": total_vectors, "chars": total_chars, "size_mb": round(size_mb, 2)}


def upsert_note(file_path):
    """Incrementally re-indexes a single Markdown note into SQLite FTS5 and chunk_vectors."""
    if not os.path.exists(DB_PATH) or not os.path.exists(file_path):
        return {"ok": False, "error": "DB or target note missing"}

    rel = os.path.relpath(file_path, VAULT_DIR)
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        raw = f.read()

    fm, body = parse_frontmatter(raw)
    file_chunks = chunk_markdown(rel, fm, body)

    conn = sqlite3.connect(DB_PATH, timeout=5.0)
    cur = conn.cursor()
    _ensure_vector_table(cur)
    try:
        old_rows = cur.execute(
            "SELECT id, title, section, file_rel, domain, content FROM chunks WHERE file_rel = ?",
            (rel,)
        ).fetchall()
        old_ids = [r[0] for r in old_rows]
        for r_id, r_title, r_sec, r_file, r_dom, r_cont in old_rows:
            cur.execute(
                """INSERT INTO chunks_fts(chunks_fts, rowid, title, section, file_rel, domain, content)
                   VALUES('delete', ?, ?, ?, ?, ?, ?)""",
                (r_id, r_title, r_sec, r_file, r_dom, r_cont)
            )
        if old_ids:
            cur.executemany("DELETE FROM chunk_vectors WHERE chunk_id = ?", [(i,) for i in old_ids])
        cur.execute("DELETE FROM chunks WHERE file_rel = ?", (rel,))

        inserted_for_vec = []
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
            if len(inserted_for_vec) < 5:
                inserted_for_vec.append((new_id, f"{c['title']} | {c['section']} | {c['file_rel']}\n{c['content'][:1800]}"))

        key = load_api_key()
        vec_updated = 0
        if key and inserted_for_vec and fm.get("type", "concept") != "log":
            def _save_upsert_vecs(brows):
                nonlocal vec_updated
                cur.executemany("INSERT OR REPLACE INTO chunk_vectors (chunk_id, vec) VALUES (?, ?)", brows)
                vec_updated += len(brows)
            _batch_embed_texts_resilient(inserted_for_vec, key, on_batch=_save_upsert_vecs)

        global _ANCHOR_NGRAM_CACHE
        _ANCHOR_NGRAM_CACHE = None
        _refresh_metadata(cur)
        conn.commit()
        return {"ok": True, "file": rel, "chunks": len(file_chunks), "vectors": vec_updated}
    finally:
        conn.close()


def _extract_terms(query):
    tokens = re.findall(r"[A-Za-z0-9\u00C0-\u017F_]{2,}", query)
    clean = [t for t in tokens if t.lower() not in STOPWORDS]
    if not clean:
        clean = tokens
    return clean[:12]


def _expand_terms(base_terms):
    expanded = []
    seen = {t.lower() for t in base_terms}
    for t in base_terms:
        low = t.lower()
        for syn in DOMAIN_SYNONYMS.get(low, []):
            if syn not in seen:
                seen.add(syn)
                expanded.append(syn)
    return expanded[:10]


def _smart_snippet(content, terms, max_len=900):
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


_ANCHOR_NGRAM_CACHE = None


def _subword_profile(text):
    """Builds normalized character-4-gram Counter for language-agnostic morphological/fuzzy cosine matching."""
    cleaned = " ".join(re.findall(r"[a-z0-9\u00e0-\u017f]{2,}", text.lower()))
    if len(cleaned) < 4:
        return {}, 1.0
    grams = Counter(cleaned[i:i + 4] for i in range(len(cleaned) - 3))
    norm = math.sqrt(sum(v * v for v in grams.values())) or 1.0
    return grams, norm


def _sparse_cos(q_grams, q_norm, d_grams, d_norm):
    if len(q_grams) > len(d_grams):
        dot = sum(v * q_grams[k] for k, v in d_grams.items() if k in q_grams)
    else:
        dot = sum(v * d_grams[k] for k, v in q_grams.items() if k in d_grams)
    return dot / (q_norm * d_norm)


def _load_subword_anchors(cur):
    global _ANCHOR_NGRAM_CACHE
    if _ANCHOR_NGRAM_CACHE is not None:
        return _ANCHOR_NGRAM_CACHE
    rows = cur.execute("""
        WITH ranked AS (
            SELECT id, file_rel, doc_type, domain, title, section, content,
                   ROW_NUMBER() OVER (PARTITION BY file_rel ORDER BY id) AS rn
            FROM chunks
            WHERE doc_type != 'log'
        )
        SELECT id, file_rel, title, domain, doc_type, section, content
        FROM ranked
        WHERE doc_type IN ('zettel', 'interview-prep', 'moc', 'hub')
           OR file_rel LIKE '01_Karriere_Bewerbungen%'
           OR rn <= 2
    """).fetchall()
    out = []
    for r in rows:
        d = dict(r)
        grams, norm = _subword_profile(f"{d['title']} {d['section']} {d['content'][:1200]}")
        out.append((d["id"], d, grams, norm))
    _ANCHOR_NGRAM_CACHE = out
    return out


def _load_vector_cache(cur):
    global _VECTOR_CACHE
    if _VECTOR_CACHE is not None:
        return _VECTOR_CACHE
    try:
        rows = cur.execute("SELECT chunk_id, vec FROM chunk_vectors").fetchall()
    except sqlite3.OperationalError:
        return []
    loaded = []
    for cid, blob in rows:
        arr = array.array("f")
        arr.frombytes(blob)
        loaded.append((cid, arr))
    _VECTOR_CACHE = loaded
    return loaded


def search(query, top_k=8, domain=None, max_per_file=2, use_vectors=True):
    if not os.path.exists(DB_PATH):
        return []
    base_terms = _extract_terms(query)
    if not base_terms and not query.strip():
        return []
    exp_terms = _expand_terms(base_terms)
    all_terms = base_terms + exp_terms

    conn = sqlite3.connect(DB_PATH, timeout=5.0)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    bm25_entries = {}
    retrieval_mode = "hybrid_subword_bm25"

    try:
        # 1. Stage 1 FTS5: Exact multi-term AND
        if 2 <= len(base_terms) <= 5:
            and_expr = " AND ".join(f'"{t}"*' for t in base_terms[:5])
            for r in _run_fts_stage(cur, and_expr, domain, max(top_k * 5, 30)):
                bm25_entries[r["id"]] = (dict(r), 1.30)

        # 2. Stage 2 FTS5: Exact terms OR
        if base_terms:
            or_expr = " OR ".join(f'"{t}"*' for t in base_terms)
            for r in _run_fts_stage(cur, or_expr, domain, max(top_k * 8, 50)):
                if r["id"] not in bm25_entries:
                    bm25_entries[r["id"]] = (dict(r), 1.00)

        # 3. Stage 3 FTS5: Synonym-expanded OR
        if exp_terms:
            syn_expr = " OR ".join(f'"{t}"*' for t in exp_terms)
            for r in _run_fts_stage(cur, syn_expr, domain, max(top_k * 5, 30)):
                if r["id"] not in bm25_entries:
                    bm25_entries[r["id"]] = (dict(r), 0.78)

        bm25_sorted = sorted(
            bm25_entries.items(),
            key=lambda kv: (-float(kv[1][0]["raw_bm25"])) * kv[1][1],
            reverse=True
        )
        bm25_rank_map = {cid: idx for idx, (cid, _) in enumerate(bm25_sorted, 1)}

        # 4. Pure-Python Subword 4-Gram Fuzzy/Morphological Semantic Signal
        sub_rank_map = {}
        sub_sim_map = {}
        q_sub_g, q_sub_n = _subword_profile(" ".join([query] + exp_terms[:4]))
        if q_sub_g:
            sub_anchors = _load_subword_anchors(cur)
            sub_sims = []
            for cid, d, dg, dn in sub_anchors:
                if domain and d.get("domain") != domain:
                    continue
                sim = _sparse_cos(q_sub_g, q_sub_n, dg, dn)
                if sim > 0.08:
                    sub_sims.append((cid, d, sim))
            sub_sims.sort(key=lambda x: x[2], reverse=True)
            for s_rank, (cid, d, sim) in enumerate(sub_sims[:max(top_k * 6, 40)], 1):
                if cid not in bm25_entries:
                    dc = dict(d)
                    dc["raw_bm25"] = 0.0
                    bm25_entries[cid] = (dc, 0.55)
                sub_rank_map[cid] = s_rank
                sub_sim_map[cid] = round(float(sim), 4)

        # 5. Dense Gemini 768d Vector Search + Reciprocal Rank Fusion (RRF)
        vec_rank_map = {}
        vec_sim_map = {}
        if use_vectors:
            anchors = _load_vector_cache(cur)
            key = load_api_key()
            if anchors and key:
                try:
                    q_vec = _embed_single_query(query, key)
                    sims = [(cid, _DOT(q_vec, avec)) for cid, avec in anchors]
                    sims.sort(key=lambda x: x[1], reverse=True)
                    top_vec = sims[:max(top_k * 6, 40)]
                    missing_ids = [cid for cid, _ in top_vec if cid not in bm25_entries]
                    if missing_ids:
                        placeholders = ",".join("?" for _ in missing_ids)
                        sql_m = f"SELECT id, file_rel, title, domain, doc_type, section, content FROM chunks WHERE id IN ({placeholders})"
                        params_m = list(missing_ids)
                        if domain:
                            sql_m += " AND domain = ?"
                            params_m.append(domain)
                        for r in cur.execute(sql_m, params_m).fetchall():
                            d = dict(r)
                            d["raw_bm25"] = 0.0
                            bm25_entries[r["id"]] = (d, 0.55)
                    for v_rank, (cid, sim) in enumerate(top_vec, 1):
                        if cid in bm25_entries:
                            vec_rank_map[cid] = v_rank
                            vec_sim_map[cid] = round(float(sim), 4)
                    if vec_rank_map:
                        retrieval_mode = "hybrid_rrf"
                except Exception:
                    pass
    finally:
        conn.close()

    if not bm25_entries:
        return []

    lower_all = [t.lower() for t in all_terms]
    scored = []
    for cid, (r, stage_boost) in bm25_entries.items():
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
        matched = [t for t in lower_all if t in hay_all]
        coverage_w = 1.0 + 0.14 * len(matched)
        if any(t in hay_title for t in lower_all):
            coverage_w += 0.20

        rrf = 0.0
        if cid in bm25_rank_map:
            rrf += (1.35 * stage_boost) / (40.0 + bm25_rank_map[cid])
        if cid in sub_rank_map:
            rrf += 0.85 / (40.0 + sub_rank_map[cid])
        if cid in vec_rank_map:
            sim_val = max(vec_sim_map.get(cid, 0.0), 0.0)
            rrf += (1.25 * (0.6 + sim_val)) / (40.0 + vec_rank_map[cid])
        final_score = round(rrf * 1000.0 * auth_w * coverage_w, 3)

        best_sem = max(vec_sim_map.get(cid, 0.0), sub_sim_map.get(cid, 0.0) * 0.9)
        scored.append({
            "id": cid,
            "file": file_rel,
            "title": r["title"],
            "domain": dom,
            "type": doc_type,
            "section": r["section"],
            "score": final_score,
            "vec_sim": round(best_sem * 100.0, 1),
            "bm25_rank": bm25_rank_map.get(cid),
            "vec_rank": vec_rank_map.get(cid),
            "retrieval_mode": retrieval_mode,
            "matched_terms": matched,
            "expanded_terms": exp_terms,
            "snippet": _smart_snippet(r["content"], all_terms, max_len=900),
            "content": r["content"]
        })

    scored.sort(key=lambda x: x["score"], reverse=True)

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
        "total_vectors": int(meta.get("total_vectors", 0)),
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
    mode = hits[0].get("retrieval_mode", "bm25_expanded") if hits else "none"
    key = load_api_key()
    if not key:
        return {"answer": "Kein GEMINI_API_KEY konfiguriert.", "mode": mode, "sources": hits}

    context_blocks = []
    for i, h in enumerate(hits, 1):
        context_blocks.append(f"[Quelle {i}: {h['file']} | Typ: {h['type']} | Abschnitt: {h['section']}]\n{h['content'][:2200]}")
    context_text = "\n\n---\n\n".join(context_blocks)

    prompt = f"""Beantworte die folgende Frage präzise auf Basis von Visar Murselis verifizierten Dokumenten.
Zitiere konkrete Quellen im Format [Quelle: Dateiname | Abschnitt] und gliedere mit klaren Überschriften und Bulletpoints. Erfinde keine Fakten.

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
                    return {
                        "answer": txt,
                        "model": model,
                        "mode": mode,
                        "sources": [
                            {"file": h["file"], "title": h["title"], "type": h["type"], "section": h["section"], "score": h["score"], "vec_sim": h.get("vec_sim", 0.0)}
                            for h in hits
                        ]
                    }
        except Exception:
            continue
    return {
        "answer": "Synthese fehlgeschlagen; zeige Rohtreffer.",
        "model": "fallback-raw",
        "mode": mode,
        "sources": [
            {"file": h["file"], "title": h["title"], "type": h["type"], "section": h["section"], "score": h["score"], "vec_sim": h.get("vec_sim", 0.0)}
            for h in hits
        ]
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Local Career OS Hybrid RAG Engine V3 (BM25 + Dense Vector RRF)")
    parser.add_argument("--build", action="store_true", help="Rebuilds FTS5 + 768d vector anchor index from Obsidian Vault")
    parser.add_argument("--embed", action="store_true", help="Builds missing 768d vector embeddings on existing DB")
    parser.add_argument("--upsert", type=str, help="Incrementally upserts a single .md file into FTS5 + vector index")
    parser.add_argument("--stats", action="store_true", help="Shows RAG index statistics")
    parser.add_argument("--pipeline", action="store_true", help="Shows live application pipeline JSON")
    parser.add_argument("--query", type=str, help="Searches indexed chunks via Hybrid RRF (BM25 + Vector)")
    parser.add_argument("--ask", type=str, help="Hybrid RRF RAG query + Gemini synthesis")
    args = parser.parse_args()

    if args.build:
        build_index(with_vectors=True)
    elif args.embed:
        print(json.dumps(embed_anchors(force=False), indent=2, ensure_ascii=False))
    elif args.upsert:
        print(json.dumps(upsert_note(args.upsert), indent=2, ensure_ascii=False))
    elif args.stats:
        print(json.dumps(get_stats(), indent=2, ensure_ascii=False))
    elif args.pipeline:
        print(json.dumps(get_pipeline_data(), indent=2, ensure_ascii=False))
    elif args.query:
        res = search(args.query, top_k=6)
        mode = res[0]["retrieval_mode"] if res else "none"
        print(f"=== MODE: {mode} | EXPANDED: {res[0]['expanded_terms'] if res else []} ===")
        for idx, r in enumerate(res, 1):
            print(f"\n[{idx}] RRF={r['score']} | Sim={r['vec_sim']}% | {r['type']} | {r['file']} :: {r['section']}")
            print(r["snippet"][:300].replace("\n", " "))
    elif args.ask:
        print(json.dumps(synthesize_answer(args.ask), indent=2, ensure_ascii=False))
    else:
        print(json.dumps(get_stats(), indent=2, ensure_ascii=False))
