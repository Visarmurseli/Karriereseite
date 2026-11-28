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
import threading
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
    "profile": 1.52,
    "synergy": 1.50,
    "zettel": 1.45,
    "interview-prep": 1.42,
    "moc": 1.25,
    "hub": 1.25,
    "module": 1.15,
    "concept": 1.00,
    "source-fulltext": 0.72,
    "reference-book": 0.62,
    "log": 0.45,
}

LOGICAL_DOMAIN_GROUPS = {
    "work": ("sap-transformation", "datacenter-operations", "enterprise-architecture"),
    "arbeit": ("sap-transformation", "datacenter-operations", "enterprise-architecture"),
    "study": ("academic-curriculum",),
    "studium": ("academic-curriculum",),
    "synergies": ("synergy-architecture", "career-pmo"),
    "synergien": ("synergy-architecture", "career-pmo"),
    "library": ("reference-library",),
    "bibliothek": ("reference-library",),
    "literatur": ("reference-library",),
}

EMPIRIE_PATTERNS = (
    "Masterarbeit", "Bachelorarbeit", "Interview_IP", "Codebuch",
    "Mayring", "FPWI", "Seminararbeit", "DigitaleNachhaltigkeit",
    "01_Empirie", "02_Forschung", "Plattformisierung", "Boundary_Resources",
)

CORE_PRIORITY_PATTERNS = (
    "Masterarbeit", "Bachelorarbeit", "Interview_IP", "Codebuch",
    "Loesungsdesign", "Lösungsdesign", "SolutionDesign", "CustomCode",
    "Berechtigung", "UMT", "P_ORGIN", "SAP_Cloud_ALM", "Migration_nach_SAP",
    "SAP_HANA", "Enterprise_Architecture", "BPI_mit_SAP", "Enable_Now",
    "Zeugnis", "Arbeitszeugnis", "CM_ins_INOC", "HLM", "DigitaleNachhaltigkeit",
    "FPWI", "CloudComputing", "PatentRadar", "Trennungsrechnung", "Fördermittel",
    "Geschäftspartner", "Kontengruppen", "Datenströme", "Discover Phase",
    "Steering", "Lenkungsausschuss", "TOGAF",
)


SAP_PRESS_IN_SSB_BOOKS = (
    "Berechtigungen_in_S4HANA_und_Fiori",
    "BPI_mit_SAP",
    "Migration_nach_SAP_S4HANA",
    "SAP_Cloud_ALM",
    "SAP_HANA_Cloud",
)


def _domain_sql_clause(domain, alias="c"):
    """Maps intuitive UI domain group names or exact YAML domains to uniform SQL WHERE predicates."""
    if not domain:
        return "", []
    low = domain.strip().lower()
    if low in ("all", "alle"):
        return "", []
    if low in ("curated", "layer1", "schicht1"):
        return f" AND {alias}.file_rel NOT LIKE '05_Archiv%'", []
    if low in ("empirie", "forschung", "research"):
        likes = " OR ".join(f"{alias}.file_rel LIKE ?" for _ in EMPIRIE_PATTERNS)
        return f" AND {alias}.doc_type != 'log' AND ({likes})", [f"%{p}%" for p in EMPIRIE_PATTERNS]
    if low in ("synergies", "synergien"):
        return f" AND ({alias}.domain IN ('synergy-architecture', 'career-pmo') OR {alias}.doc_type IN ('synergy', 'profile', 'zettel'))", []
    if low in ("library", "bibliothek", "literatur"):
        sap_likes = " OR ".join(f"{alias}.file_rel LIKE ?" for _ in SAP_PRESS_IN_SSB_BOOKS)
        return f" AND ({alias}.domain = 'reference-library' OR {sap_likes})", [f"%{p}%" for p in SAP_PRESS_IN_SSB_BOOKS]
    if low in LOGICAL_DOMAIN_GROUPS:
        vals = LOGICAL_DOMAIN_GROUPS[low]
        ph = ",".join("?" for _ in vals)
        return f" AND {alias}.domain IN ({ph})", list(vals)
    return f" AND {alias}.domain = ?", [domain.strip()]


def _matches_domain_py(file_rel, doc_domain, doc_type, domain):
    """Python-side counterpart to _domain_sql_clause for vector & subword caches."""
    if not domain:
        return True
    low = domain.strip().lower()
    if low in ("all", "alle"):
        return True
    frel = str(file_rel or "")
    if low in ("curated", "layer1", "schicht1"):
        return not frel.startswith("05_Archiv")
    if low in ("empirie", "forschung", "research"):
        if doc_type == "log":
            return False
        return any(p.lower() in frel.lower() for p in EMPIRIE_PATTERNS)
    if low in ("synergies", "synergien"):
        return (doc_domain in ("synergy-architecture", "career-pmo")) or (doc_type in ("synergy", "profile", "zettel"))
    if low in ("library", "bibliothek", "literatur"):
        return doc_domain == "reference-library" or any(p.lower() in frel.lower() for p in SAP_PRESS_IN_SSB_BOOKS)
    if low in LOGICAL_DOMAIN_GROUPS:
        return doc_domain in LOGICAL_DOMAIN_GROUPS[low]
    return doc_domain == domain.strip()

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
    "iam": ["berechtigung", "pfcg", "p_orgin", "sod", "umt", "provisioning", "hcm"],
    "sod": ["segregation", "duties", "iks", "pfcg", "compliance", "audit"],
    "iks": ["kontrolle", "audit", "sod", "compliance", "gobd", "acdoca"],
    "prüfung": ["iks", "audit", "sod", "cvi", "acdoca", "übernahmekonto"],
    "audit": ["iks", "sod", "cvi", "acdoca", "übernahmekonto", "gobd"],
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
    "kpmg": ["transformation", "audit", "iks", "sdd", "acdoca", "sod", "trennungsrechnung"],
    "schwarz": ["hcm", "iam", "umt", "p_orgin", "third", "pfcg", "su53", "stauthtrace"],
    "trumpf": ["governance", "eam", "signavio", "calm", "togaf", "clean"],
    "empirie": ["interview", "mayring", "codebuch", "csf", "erfolgsfaktoren", "masterarbeit"],
    "erfolgsfaktoren": ["csf", "plattformisierung", "mayring", "masterarbeit", "change"],
    "eam": ["togaf", "adm", "architektur", "btp", "leanix", "schnittstellen"],
    "togaf": ["eam", "adm", "architektur", "datacenter", "dc1"],
    "calm": ["cloud", "alm", "signavio", "enable", "testmanagement", "quality"],
    "signavio": ["bpmn", "prozess", "calm", "fit", "standard"],
}

_DOT = getattr(math, "sumprod", lambda a, b: sum(map(operator.mul, a, b)))
_CACHE_LOCK = threading.Lock()
_VECTOR_CACHE = None
_OLLAMA_VECTOR_CACHE = None
_OLLAMA_ALIVE_CACHE = (0.0, False)
_QUERY_VEC_CACHE = OrderedDict()
OLLAMA_URL = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")
OLLAMA_DEFAULT_EMBED_MODEL = "nomic-embed-text"
OLLAMA_DEFAULT_CHAT_MODEL = os.environ.get("OLLAMA_CHAT_MODEL", "qwen2.5-7b-16k:latest")


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
    batch_size = 50
    for start in range(0, len(items), batch_size):
        batch = items[start:start + batch_size]
        reqs = [
            {
                "model": f"models/{EMBED_MODEL}",
                "content": {"parts": [{"text": txt[:1500]}]},
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
                err_body = ""
                try:
                    err_body = e.read().decode("utf-8", errors="ignore")
                except Exception:
                    pass
                if e.code == 429 and ("PerDay" in err_body or "RequestsPerDay" in err_body):
                    print(f"[!] Tages-Quota (Free Tier 1.000 Req/Tag) erreicht nach {total_saved} neuen Vektoren. Bisherige Batches gespeichert.", flush=True)
                    return total_saved
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
            time.sleep(0.25)
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
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ollama_vectors (
            chunk_id INTEGER PRIMARY KEY,
            dim INTEGER NOT NULL,
            model TEXT NOT NULL,
            vec BLOB NOT NULL
        )
    """)


def _refresh_metadata(cur):
    global _VECTOR_CACHE, _OLLAMA_VECTOR_CACHE
    _VECTOR_CACHE = None
    _OLLAMA_VECTOR_CACHE = None
    row = cur.execute("SELECT COUNT(DISTINCT file_rel), COUNT(*), COALESCE(SUM(char_len), 0) FROM chunks").fetchone()
    total_files, total_chunks, total_chars = row[0], row[1], row[2]
    _ensure_vector_table(cur)
    total_vectors = cur.execute("SELECT COUNT(*) FROM chunk_vectors").fetchone()[0]
    ollama_row = cur.execute("SELECT COUNT(*), COALESCE(MAX(model), '') FROM ollama_vectors").fetchone()
    ollama_vectors, ollama_model = ollama_row[0], ollama_row[1]
    cur.execute("INSERT OR REPLACE INTO metadata VALUES ('built_at', ?)", (datetime.now().isoformat(),))
    cur.execute("INSERT OR REPLACE INTO metadata VALUES ('total_files', ?)", (str(total_files),))
    cur.execute("INSERT OR REPLACE INTO metadata VALUES ('total_chunks', ?)", (str(total_chunks),))
    cur.execute("INSERT OR REPLACE INTO metadata VALUES ('total_chars', ?)", (str(total_chars),))
    cur.execute("INSERT OR REPLACE INTO metadata VALUES ('total_vectors', ?)", (str(total_vectors),))
    cur.execute("INSERT OR REPLACE INTO metadata VALUES ('ollama_vectors', ?)", (str(ollama_vectors),))
    cur.execute("INSERT OR REPLACE INTO metadata VALUES ('ollama_model', ?)", (str(ollama_model),))
    return total_files, total_chunks, total_chars, total_vectors


def _is_ollama_alive():
    """Fast cached socket check (~150ms max) for local Ollama daemon on port 11434."""
    global _OLLAMA_ALIVE_CACHE
    now = time.time()
    if now - _OLLAMA_ALIVE_CACHE[0] < 15.0:
        return _OLLAMA_ALIVE_CACHE[1]
    import socket
    alive = False
    try:
        parsed = urllib.request.urlparse(OLLAMA_URL)
        host = parsed.hostname or "127.0.0.1"
        port = parsed.port or 11434
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.15)
            alive = (s.connect_ex((host, port)) == 0)
    except Exception:
        alive = False
    _OLLAMA_ALIVE_CACHE = (now, alive)
    return alive


def _ollama_embed_texts(texts, model=OLLAMA_DEFAULT_EMBED_MODEL, timeout=90.0):
    """Calls local Ollama /api/embed (batch) with graceful fallback to /api/embeddings."""
    clean_inputs = [t[:2000] for t in texts]
    url = f"{OLLAMA_URL}/api/embed"
    payload = {"model": model, "input": clean_inputs}
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            embs = json.loads(resp.read().decode("utf-8")).get("embeddings", [])
        return [_normalize_vec(e) for e in embs]
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise
    out = []
    url_legacy = f"{OLLAMA_URL}/api/embeddings"
    for item in clean_inputs:
        req2 = urllib.request.Request(
            url_legacy,
            data=json.dumps({"model": model, "prompt": item}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req2, timeout=timeout) as resp2:
            vals = json.loads(resp2.read().decode("utf-8")).get("embedding", [])
        out.append(_normalize_vec(vals))
    return out


def embed_ollama_anchors(model=OLLAMA_DEFAULT_EMBED_MODEL, force=False, max_chunks=4000, include_library=True):
    """Builds unlimited local GPU/CPU vectors via Ollama (e.g. nomic-embed-text or bge-m3)."""
    if not os.path.exists(DB_PATH):
        return {"ok": False, "error": "DB not built yet"}
    if not _is_ollama_alive():
        return {
            "ok": False,
            "error": f"Ollama nicht aktiv unter {OLLAMA_URL}. Starte Ollama und führe 'ollama pull {model}' aus.",
        }

    conn = sqlite3.connect(DB_PATH, timeout=15.0)
    cur = conn.cursor()
    _ensure_vector_table(cur)
    if force:
        cur.execute("DELETE FROM ollama_vectors")
        conn.commit()
    else:
        existing_models = {r[0] for r in cur.execute("SELECT DISTINCT model FROM ollama_vectors").fetchall()}
        if existing_models and model not in existing_models:
            conn.close()
            return {
                "ok": False,
                "error": f"ollama_vectors nutzt bereits {existing_models}. Mit --force neu aufbauen beim Modellwechsel auf {model}.",
            }

    prio_likes = "(" + " OR ".join(f"file_rel LIKE '%{p}%'" for p in CORE_PRIORITY_PATTERNS) + ")"
    sap_book_likes = "(" + " OR ".join(f"file_rel LIKE '%{p}%'" for p in SAP_PRESS_IN_SSB_BOOKS) + ")"
    lib_sql = f"OR ((doc_type = 'reference-book' OR {sap_book_likes}) AND rn <= 30)" if include_library else ""
    rows = cur.execute(f"""
        WITH ranked AS (
            SELECT id, file_rel, doc_type, domain, title, section, content,
                   ROW_NUMBER() OVER (PARTITION BY file_rel ORDER BY id) AS rn
            FROM chunks
            WHERE doc_type != 'log'
        )
        SELECT id, title, section, file_rel, content, doc_type, domain, rn
        FROM ranked
        WHERE file_rel NOT LIKE '05_Archiv%'
           OR ({prio_likes} AND rn <= 8)
           {lib_sql}
           OR rn = 1
    """).fetchall()

    def _sort_key(r):
        _, _, _, frel, _, dtype, _, rn = r
        frel_low = str(frel).lower()
        is_prio = any(p.lower() in frel_low for p in CORE_PRIORITY_PATTERNS)
        is_sap_book = any(p.lower() in frel_low for p in SAP_PRESS_IN_SSB_BOOKS)
        tier = 0 if not str(frel).startswith("05_Archiv") else (1 if (is_prio and dtype != "reference-book" and not is_sap_book) else (2 if (dtype == "reference-book" or is_sap_book) else 3))
        return (tier, rn, r[0])

    rows.sort(key=_sort_key)
    existing = {r[0] for r in cur.execute("SELECT chunk_id FROM ollama_vectors").fetchall()}
    todo = [
        (cid, f"{title} | {sec} | {frel}\n{cont[:1600]}")
        for cid, title, sec, frel, cont, _, _, _ in rows
        if cid not in existing
    ]
    if max_chunks:
        todo = todo[:int(max_chunks)]

    if not todo:
        _refresh_metadata(cur)
        conn.commit()
        total_ol = cur.execute("SELECT COUNT(*) FROM ollama_vectors").fetchone()[0]
        conn.close()
        return {"ok": True, "provider": "ollama", "model": model, "embedded_new": 0, "ollama_vectors": total_ol}

    print(f"[*] Embedding {len(todo)} chunks locally via Ollama '{model}' ({OLLAMA_URL})...", flush=True)
    saved_count = 0
    batch_size = 32
    t_start = time.time()
    for start in range(0, len(todo), batch_size):
        batch = todo[start:start + batch_size]
        try:
            vecs = _ollama_embed_texts([txt for _, txt in batch], model=model, timeout=90.0)
            cur.executemany(
                "INSERT OR REPLACE INTO ollama_vectors (chunk_id, dim, model, vec) VALUES (?, ?, ?, ?)",
                [(cid, len(vec), model, vec.tobytes()) for (cid, _), vec in zip(batch, vecs)],
            )
            conn.commit()
            saved_count += len(vecs)
            if saved_count == len(vecs) or saved_count % 256 == 0 or start + batch_size >= len(todo):
                elapsed = max(0.1, time.time() - t_start)
                rate = saved_count / elapsed
                eta_min = max(0.0, (len(todo) - saved_count) / rate / 60.0) if rate > 0 else 0.0
                pct = (saved_count / len(todo)) * 100.0
                print(f"  [Ollama {saved_count}/{len(todo)} ({pct:.1f}%)] {rate:.1f} chunks/s | ETA ~{eta_min:.1f} min", flush=True)
        except Exception as exc:
            print(f"[!] Ollama Embedding gestoppt bei {saved_count} Vektoren ({exc})", flush=True)
            break

    _refresh_metadata(cur)
    total_ol = cur.execute("SELECT COUNT(*) FROM ollama_vectors").fetchone()[0]
    conn.commit()
    conn.close()
    print(f"[OK] Ollama vector index updated: +{saved_count} | {total_ol} total vectors ({model})")
    return {"ok": True, "provider": "ollama", "model": model, "embedded_new": saved_count, "ollama_vectors": total_ol}


def embed_anchors(force=False, max_chunks=2500):
    """Builds 768-dim Gemini embeddings over all Layer-1 notes plus prioritized Layer-2 core sources."""
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

    prio_likes = "(" + " OR ".join(f"file_rel LIKE '%{p}%'" for p in CORE_PRIORITY_PATTERNS) + ")"
    rows = cur.execute(f"""
        WITH ranked AS (
            SELECT id, file_rel, doc_type, domain, title, section, content,
                   ROW_NUMBER() OVER (PARTITION BY file_rel ORDER BY id) AS rn
            FROM chunks
            WHERE doc_type != 'log'
        )
        SELECT id, title, section, file_rel, content, doc_type, domain, rn
        FROM ranked
        WHERE file_rel NOT LIKE '05_Archiv%'
           OR ({prio_likes} AND rn <= 6)
           OR rn = 1
    """).fetchall()

    prio_map = {"profile": 0, "synergy": 0, "zettel": 1, "interview-prep": 1, "moc": 2, "hub": 3, "module": 4, "concept": 5, "source-fulltext": 7}

    def _sort_key(r):
        _, _, _, frel, _, dtype, _, rn = r
        is_layer1 = not str(frel).startswith("05_Archiv")
        is_core_l2 = any(p.lower() in str(frel).lower() for p in CORE_PRIORITY_PATTERNS)
        tier = 0 if is_layer1 else (1 if is_core_l2 else 2)
        return (tier, prio_map.get(dtype, 8), rn, r[0])

    rows.sort(key=_sort_key)

    existing = {r[0] for r in cur.execute("SELECT chunk_id FROM chunk_vectors").fetchall()}
    todo = [
        (cid, f"{title} | {sec} | {frel}\n{cont[:1300]}")
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

    print(f"[*] Embedding {len(todo)} prioritized semantic chunks (Layer 1 + Core Layer 2) via {EMBED_MODEL} ({EMBED_DIM}d)...")

    def save_batch(batch_rows):
        cur.executemany("INSERT OR REPLACE INTO chunk_vectors (chunk_id, vec) VALUES (?, ?)", batch_rows)
        conn.commit()

    saved_count = _batch_embed_texts_resilient(todo, key, on_batch=save_batch)
    _, _, _, total_vectors = _refresh_metadata(cur)
    conn.commit()
    conn.close()
    print(f"[OK] Vector index updated: {saved_count} new | {total_vectors} total vectors")
    return {"ok": True, "embedded_new": saved_count, "total_vectors": total_vectors}


def _migrate_existing_vectors(old_db_path, new_cur):
    """Carries over unchanged Gemini and Ollama vectors from the prior SQLite DB to avoid re-embedding."""
    if not os.path.exists(old_db_path):
        return 0, 0
    try:
        old_conn = sqlite3.connect(old_db_path, timeout=5.0)
        old_cur = old_conn.cursor()
        new_lookup = {
            (r[1], r[2], r[3]): r[0]
            for r in new_cur.execute("SELECT id, file_rel, section, char_len FROM chunks").fetchall()
        }
        g_rows = []
        try:
            for frel, sec, clen, vec in old_cur.execute(
                "SELECT c.file_rel, c.section, c.char_len, v.vec FROM chunk_vectors v JOIN chunks c ON c.id = v.chunk_id"
            ).fetchall():
                nid = new_lookup.get((frel, sec, clen))
                if nid is not None:
                    g_rows.append((nid, vec))
        except sqlite3.OperationalError:
            pass
        if g_rows:
            new_cur.executemany("INSERT OR REPLACE INTO chunk_vectors (chunk_id, vec) VALUES (?, ?)", g_rows)

        o_rows = []
        try:
            for frel, sec, clen, dim, model, vec in old_cur.execute(
                "SELECT c.file_rel, c.section, c.char_len, o.dim, o.model, o.vec FROM ollama_vectors o JOIN chunks c ON c.id = o.chunk_id"
            ).fetchall():
                nid = new_lookup.get((frel, sec, clen))
                if nid is not None:
                    o_rows.append((nid, dim, model, vec))
        except sqlite3.OperationalError:
            pass
        if o_rows:
            new_cur.executemany("INSERT OR REPLACE INTO ollama_vectors (chunk_id, dim, model, vec) VALUES (?, ?, ?, ?)", o_rows)

        old_conn.close()
        return len(g_rows), len(o_rows)
    except Exception:
        return 0, 0


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
        dirs[:] = [d for d in dirs if d not in (".obsidian", ".trash")]
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
    g_kept, o_kept = _migrate_existing_vectors(DB_PATH, cur)
    if g_kept or o_kept:
        print(f"[*] Preserved existing vectors during rebuild: {g_kept} Gemini + {o_kept} Ollama")
    total_files, total_chunks, total_chars, total_vectors = _refresh_metadata(cur)
    conn.commit()
    conn.close()

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    os.replace(tmp_db, DB_PATH)

    if with_vectors:
        try:
            vec_res = embed_anchors(force=False)
            total_vectors = vec_res.get("total_vectors", total_vectors)
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
    dom_sql, dom_params = _domain_sql_clause(domain, alias="c")
    sql += dom_sql
    params.extend(dom_params)
    sql += " ORDER BY raw_bm25 LIMIT ?"
    params.append(int(limit))
    try:
        return cur.execute(sql, params).fetchall()
    except sqlite3.OperationalError:
        return []


_ANCHOR_NGRAM_CACHE = None
_CACHE_DB_MTIME = 0.0


def _ensure_cache_fresh():
    """Invalidates in-process caches automatically whenever career_os_rag.db changes on disk."""
    global _CACHE_DB_MTIME, _ANCHOR_NGRAM_CACHE, _VECTOR_CACHE, _OLLAMA_VECTOR_CACHE
    try:
        mt = os.path.getmtime(DB_PATH)
    except OSError:
        return
    if mt != _CACHE_DB_MTIME:
        _ANCHOR_NGRAM_CACHE = None
        _VECTOR_CACHE = None
        _OLLAMA_VECTOR_CACHE = None
        _CACHE_DB_MTIME = mt


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
    core_likes = " OR ".join(f"file_rel LIKE '%{p}%'" for p in CORE_PRIORITY_PATTERNS)
    rows = cur.execute(f"""
        WITH ranked AS (
            SELECT id, file_rel, doc_type, domain, title, section, content,
                   ROW_NUMBER() OVER (PARTITION BY file_rel ORDER BY id) AS rn
            FROM chunks
            WHERE doc_type != 'log'
        )
        SELECT id, file_rel, title, domain, doc_type, section, content
        FROM ranked
        WHERE file_rel NOT LIKE '05_Archiv%'
           OR ({core_likes} AND rn <= 6)
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
        rows = cur.execute(
            "SELECT v.chunk_id, v.vec, c.file_rel, c.domain, c.doc_type "
            "FROM chunk_vectors v JOIN chunks c ON c.id = v.chunk_id"
        ).fetchall()
    except sqlite3.OperationalError:
        return []
    loaded = []
    for cid, blob, frel, dom, dtype in rows:
        arr = array.array("f")
        arr.frombytes(blob)
        loaded.append((cid, arr, frel, dom, dtype))
    _VECTOR_CACHE = loaded
    return loaded


def _load_ollama_vector_cache(cur):
    global _OLLAMA_VECTOR_CACHE
    if _OLLAMA_VECTOR_CACHE is not None:
        return _OLLAMA_VECTOR_CACHE
    try:
        rows = cur.execute(
            "SELECT v.chunk_id, v.vec, v.dim, v.model, c.file_rel, c.domain, c.doc_type "
            "FROM ollama_vectors v JOIN chunks c ON c.id = v.chunk_id"
        ).fetchall()
    except sqlite3.OperationalError:
        return []
    loaded = []
    for cid, blob, dim, model, frel, dom, dtype in rows:
        arr = array.array("f")
        arr.frombytes(blob)
        loaded.append((cid, arr, frel, dom, dtype, dim, model))
    _OLLAMA_VECTOR_CACHE = loaded
    return loaded


def _score_dense_anchors(q_vec, anchors, domain, cur, bm25_entries, pool_limit):
    """Computes domain-filtered cosine similarity over cached dense vectors and hydrates missing rows."""
    q_dim = len(q_vec)
    sims = [
        (entry[0], _DOT(q_vec, entry[1]))
        for entry in anchors
        if len(entry[1]) == q_dim and _matches_domain_py(entry[2], entry[3], entry[4], domain)
    ]
    sims.sort(key=lambda x: x[1], reverse=True)
    top_vec = sims[:max(pool_limit, 55)]
    missing_ids = [cid for cid, _ in top_vec if cid not in bm25_entries]
    if missing_ids:
        placeholders = ",".join("?" for _ in missing_ids)
        sql_m = f"SELECT id, file_rel, title, domain, doc_type, section, content FROM chunks WHERE id IN ({placeholders})"
        for r in cur.execute(sql_m, missing_ids).fetchall():
            d = dict(r)
            d["raw_bm25"] = 0.0
            bm25_entries[r["id"]] = (d, 0.55)
    rank_map, sim_map = {}, {}
    for v_rank, (cid, sim) in enumerate(top_vec, 1):
        rank_map[cid] = v_rank
        sim_map[cid] = round(float(sim), 4)
    return rank_map, sim_map


def _rerank_hits(query, base_terms, scored):
    """Stage-2 deterministic cross-signal reranker emphasizing phrase precision, term coverage, and entity richness."""
    lower_base = [t.lower() for t in base_terms if len(t) >= 2]
    q_clean = re.sub(r"\s+", " ", query.lower()).strip()
    phrases = []
    if len(lower_base) >= 2:
        phrases = [f"{lower_base[i]} {lower_base[i + 1]}" for i in range(len(lower_base) - 1)]

    entity_tokens = (
        "acdoca", "ltmc", "pfcg", "p_orgin", "su53", "stauthtrace", "umt",
        "1370/2007", "45a", "87", "itil", "togaf", "calm", "signavio", "btp",
        "cvi", "0,00", "mayring", "boundary", "tp5", "tp2", "1,0", "1,6", "1,7",
    )

    for item in scored:
        title_sec = f"{item['title']} {item['section']}".lower()
        body_low = item["content"][:3200].lower()
        boost = 1.0

        # Distinct base-query term coverage ratio
        if lower_base:
            base_cov = sum(1 for t in lower_base if t in body_low or t in title_sec) / len(lower_base)
            boost += 0.28 * base_cov

        # Adjacent phrase cohesion bonus
        phrase_hits = sum(1 for p in phrases if p in body_low or p in title_sec)
        if phrase_hits:
            boost += min(0.24, 0.08 * phrase_hits)
        if len(q_clean) >= 10 and q_clean in body_low:
            boost += 0.18

        # Technical / regulatory / academic entity specificity
        ent_hits = sum(1 for e in entity_tokens if e in body_low and e in q_clean)
        if ent_hits:
            boost += min(0.20, 0.07 * ent_hits)

        item["rerank_boost"] = round(boost, 3)
        item["score"] = round(item["score"] * boost, 3)

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored


def search(query, top_k=8, domain=None, max_per_file=2, use_vectors=True, rerank=True):
    if not os.path.exists(DB_PATH):
        return []
    _ensure_cache_fresh()
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
        pool_limit = max(int(top_k) * 5, 36)
        # 1. Stage 1 FTS5: Exact multi-term AND
        if 2 <= len(base_terms) <= 5:
            and_expr = " AND ".join(f'"{t}"*' for t in base_terms[:5])
            for r in _run_fts_stage(cur, and_expr, domain, pool_limit):
                bm25_entries[r["id"]] = (dict(r), 1.30)

        # 2. Stage 2 FTS5: Exact terms OR
        if base_terms:
            or_expr = " OR ".join(f'"{t}"*' for t in base_terms)
            for r in _run_fts_stage(cur, or_expr, domain, max(pool_limit, 55)):
                if r["id"] not in bm25_entries:
                    bm25_entries[r["id"]] = (dict(r), 1.00)

        # 3. Stage 3 FTS5: Synonym-expanded OR
        if exp_terms:
            syn_expr = " OR ".join(f'"{t}"*' for t in exp_terms)
            for r in _run_fts_stage(cur, syn_expr, domain, pool_limit):
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
                if not _matches_domain_py(d.get("file_rel"), d.get("domain"), d.get("doc_type"), domain):
                    continue
                sim = _sparse_cos(q_sub_g, q_sub_n, dg, dn)
                if sim > 0.08:
                    sub_sims.append((cid, d, sim))
            sub_sims.sort(key=lambda x: x[2], reverse=True)
            for s_rank, (cid, d, sim) in enumerate(sub_sims[:max(pool_limit, 45)], 1):
                if cid not in bm25_entries:
                    dc = dict(d)
                    dc["raw_bm25"] = 0.0
                    bm25_entries[cid] = (dc, 0.55)
                sub_rank_map[cid] = s_rank
                sub_sim_map[cid] = round(float(sim), 4)

        # 5. Dense Vector Search (Gemini 768d + optional Local Ollama) + Reciprocal Rank Fusion (RRF)
        vec_rank_map = {}
        vec_sim_map = {}
        ollama_rank_map = {}
        ollama_sim_map = {}
        if use_vectors:
            anchors = _load_vector_cache(cur)
            key = load_api_key()
            if anchors and key:
                try:
                    q_vec = _embed_single_query(query, key)
                    vec_rank_map, vec_sim_map = _score_dense_anchors(q_vec, anchors, domain, cur, bm25_entries, pool_limit)
                except Exception:
                    pass

            ol_anchors = _load_ollama_vector_cache(cur)
            if ol_anchors and _is_ollama_alive():
                try:
                    ol_model = ol_anchors[0][6]
                    ol_q_vecs = _ollama_embed_texts([query], model=ol_model, timeout=20.0)
                    if ol_q_vecs:
                        ollama_rank_map, ollama_sim_map = _score_dense_anchors(ol_q_vecs[0], ol_anchors, domain, cur, bm25_entries, pool_limit)
                except Exception:
                    pass

            bm25_entries = {
                cid: val for cid, val in bm25_entries.items()
                if _matches_domain_py(val[0].get("file_rel"), val[0].get("domain"), val[0].get("doc_type"), domain)
            }
            vec_rank_map = {cid: r for cid, r in vec_rank_map.items() if cid in bm25_entries}
            ollama_rank_map = {cid: r for cid, r in ollama_rank_map.items() if cid in bm25_entries}
            if vec_rank_map or ollama_rank_map:
                retrieval_mode = "hybrid_rrf_rerank" if rerank else "hybrid_rrf"
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
        if "05_archiv" in file_rel.lower() or "_Volltext" in file_rel or "_Teil_" in file_rel:
            auth_w *= 0.85
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
        if cid in ollama_rank_map:
            ol_sim = max(ollama_sim_map.get(cid, 0.0), 0.0)
            rrf += (1.20 * (0.6 + ol_sim)) / (40.0 + ollama_rank_map[cid])
        final_score = round(rrf * 1000.0 * auth_w * coverage_w, 3)

        best_sem = max(vec_sim_map.get(cid, 0.0), ollama_sim_map.get(cid, 0.0), sub_sim_map.get(cid, 0.0) * 0.9)
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
            "rerank_boost": 1.0,
            "retrieval_mode": retrieval_mode,
            "matched_terms": matched,
            "expanded_terms": exp_terms,
            "snippet": _smart_snippet(r["content"], all_terms, max_len=900),
            "content": r["content"]
        })

    if rerank:
        scored = _rerank_hits(query, base_terms, scored)
    else:
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


def warm_caches():
    """Pre-loads SQLite subword, Gemini, and Ollama vector caches in a background thread."""
    if not os.path.exists(DB_PATH):
        return {"ok": False, "reason": "db_missing"}
    with _CACHE_LOCK:
        _ensure_cache_fresh()
        conn = sqlite3.connect(DB_PATH, timeout=15.0)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        try:
            anchors = _load_subword_anchors(cur)
            g_vecs = _load_vector_cache(cur)
            o_vecs = _load_ollama_vector_cache(cur)
            return {
                "ok": True,
                "anchors": len(anchors),
                "gemini_vectors": len(g_vecs),
                "ollama_vectors": len(o_vecs),
            }
        finally:
            conn.close()


_LIBRARY_CATEGORY_LABELS = {
    "00_Layer1_Synthese_Hubs": "Layer-1 Synthese-Hubs",
    "01_SAP_S4HANA_BTP_CleanCore": "SAP S/4HANA, BTP & Clean Core",
    "02_IT_Audit_Governance_Compliance": "IT-Audit, Governance & Compliance",
    "03_Enterprise_Architecture_Cloud": "Enterprise Architecture & Cloud",
    "04_AI_Engineering_Data_Automation": "AI Engineering, RAG & Automation",
    "05_Consulting_BWL_VISMUV": "Consulting, Strategy & BWL",
    "07_Wirtschaftsinformatik_IT_Grundlagen": "WI, Software & Grundlagen",
    "08_Unternehmertum_Marketing_VISMUV": "Entrepreneurship & Marketing",
}


def _classify_library_category(file_rel):
    p = str(file_rel or "").replace("\\", "/")
    parts = p.split("/")
    if "05_Bibliothek" in parts:
        idx = parts.index("05_Bibliothek")
        if idx + 1 < len(parts):
            return parts[idx + 1]
    if "05_Fachbibliothek_Synthese" in parts:
        return "00_Layer1_Synthese_Hubs"
    return "01_SAP_S4HANA_BTP_CleanCore"


def get_library_catalog(domain_filter=None, query=None, limit=120):
    """Returns deduplicated Fachbibliothek works from SQLite grouped by 7 domain pillars + synthesis hubs."""
    if not os.path.exists(DB_PATH):
        return {"ok": False, "total": 0, "filtered": 0, "categories": [], "books": []}
    conn = sqlite3.connect(DB_PATH, timeout=5.0)
    cur = conn.cursor()
    try:
        sap_likes = " OR ".join("file_rel LIKE ?" for _ in SAP_PRESS_IN_SSB_BOOKS)
        params = [f"%{p}%" for p in SAP_PRESS_IN_SSB_BOOKS]
        rows = cur.execute(
            f"""
            SELECT file_rel, MAX(title), MAX(domain), MAX(doc_type), COUNT(*), SUM(char_len)
            FROM chunks
            WHERE doc_type = 'reference-book'
               OR file_rel LIKE '%05_Fachbibliothek_Synthese%'
               OR {sap_likes}
            GROUP BY file_rel
            ORDER BY file_rel ASC
            """,
            params,
        ).fetchall()
    finally:
        conn.close()

    cat_counts = Counter()
    all_items = []
    q_low = (query or "").strip().lower()
    dom_clean = (domain_filter or "").strip()

    for frel, title, dom, dtype, chunk_cnt, total_chars in rows:
        cat = _classify_library_category(frel)
        cat_counts[cat] += 1
        fname = os.path.basename(frel.replace("\\", "/"))
        disp_title = (title or os.path.splitext(fname)[0]).strip()
        if dom_clean and dom_clean.lower() not in ("all", "alle") and cat.lower() != dom_clean.lower():
            continue
        if q_low:
            hay = f"{disp_title} {fname} {cat} {_LIBRARY_CATEGORY_LABELS.get(cat, '')}".lower()
            if not all(tok in hay for tok in q_low.split() if tok):
                continue
        all_items.append({
            "file": frel.replace("\\", "/"),
            "filename": fname,
            "title": disp_title,
            "category": cat,
            "category_label": _LIBRARY_CATEGORY_LABELS.get(cat, cat),
            "doc_type": dtype or "reference-book",
            "chunks": int(chunk_cnt or 0),
            "chars": int(total_chars or 0),
        })

    categories = [
        {"id": k, "label": _LIBRARY_CATEGORY_LABELS.get(k, k), "count": int(cat_counts[k])}
        for k in sorted(cat_counts.keys())
    ]
    all_items.sort(key=lambda b: (0 if b["category"] == "00_Layer1_Synthese_Hubs" else 1, b["category"], b["title"].lower()))
    lim = max(1, min(int(limit or 120), 600))
    return {
        "ok": True,
        "total": sum(cat_counts.values()),
        "filtered": len(all_items),
        "categories": categories,
        "books": all_items[:lim],
    }


def read_source_chunks(file_rel, max_chunks=14, offset=0):
    """Reads ordered RAG chunks for any indexed Obsidian file (used by the portal Slide-Over Reader Drawer)."""
    if not os.path.exists(DB_PATH):
        return {"ok": False, "error": "RAG DB nicht gefunden."}
    raw = (file_rel or "").strip()
    if not raw:
        return {"ok": False, "error": "Dateipfad fehlt."}
    win_rel = raw.replace("/", "\\")
    posix_rel = raw.replace("\\", "/")
    lim = max(1, min(int(max_chunks or 14), 30))
    off = max(0, int(offset or 0))

    conn = sqlite3.connect(DB_PATH, timeout=5.0)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    try:
        meta_row = cur.execute(
            """
            SELECT file_rel, MAX(title) AS title, MAX(domain) AS domain, MAX(doc_type) AS doc_type,
                   COUNT(*) AS total_chunks, SUM(char_len) AS total_chars
            FROM chunks
            WHERE file_rel = ? OR file_rel = ?
            GROUP BY file_rel
            """,
            (win_rel, posix_rel),
        ).fetchone()
        if not meta_row:
            return {"ok": False, "error": f"Quelle '{posix_rel}' nicht im RAG-Index gefunden."}
        rows = cur.execute(
            """
            SELECT id, section, content, char_len
            FROM chunks
            WHERE file_rel = ?
            ORDER BY id ASC
            LIMIT ? OFFSET ?
            """,
            (meta_row["file_rel"], lim, off),
        ).fetchall()
    finally:
        conn.close()

    return {
        "ok": True,
        "file": str(meta_row["file_rel"]).replace("\\", "/"),
        "title": meta_row["title"],
        "domain": meta_row["domain"],
        "doc_type": meta_row["doc_type"],
        "total_chunks": int(meta_row["total_chunks"] or 0),
        "total_chars": int(meta_row["total_chars"] or 0),
        "offset": off,
        "chunks": [
            {
                "id": int(r["id"]),
                "index": off + i + 1,
                "section": r["section"] or "Abschnitt",
                "char_len": int(r["char_len"] or 0),
                "content": r["content"],
            }
            for i, r in enumerate(rows)
        ],
    }


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
        "ollama_vectors": int(meta.get("ollama_vectors", 0)),
        "ollama_model": meta.get("ollama_model", ""),
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


_PRIVACY_AND_FACT_RULES = (
    "VERBINDLICHE REGELN:\n"
    "- Antwortstil für Visar Murseli: Im ersten Satz direkt zum Punkt, KEINE Einleitungsfloskeln und KEINE Zusammenfassungen am Ende; gliedere klar mit Stichpunkten oder Tabellen auf Master-/Expertenniveau.\n"
    "- Erfinde NIEMALS Noten, Zahlen, Projektdauern, Transaktionscodes oder Fakten außerhalb des Kontexts.\n"
    "- Zitiere jede belegte Aussage mit dem echten Dateinamen (NICHT 'Dok 1' / 'Dokument 1') exakt im Format [Quelle: Dateiname.md | Abschnitt] (ausschließlich gelieferte Quelldateien verwenden).\n"
    "- Datenschutz/Compliance: Nenne niemals reale Namen ehemaliger Vorgesetzter/Ansprechpartner und keine internen WBS-/Vorgangsnummern (verwende Funktionsrollen wie 'Gesamtprojektleiter', 'IT-Leiter', 'INOC-Leitung').\n"
    "- Visar Murseli hatte KEIN Praktikum bei Robert Bosch GmbH."
)


def _format_sources_compact(hits):
    return [
        {
            "file": h["file"],
            "title": h["title"],
            "type": h["type"],
            "section": h["section"],
            "score": h["score"],
            "vec_sim": h.get("vec_sim", 0.0),
            "rerank_boost": h.get("rerank_boost", 1.0),
        }
        for h in hits
    ]


def _build_context_blocks(hits, max_chars_per_hit=2200):
    blocks = []
    for i, h in enumerate(hits, 1):
        fname = os.path.basename(h["file"])
        blocks.append(
            f"=== DOKUMENT {i}: {fname} | Pfad: {h['file']} | Typ: {h['type']} | Abschnitt: {h['section']} ===\n"
            f"{h['content'][:max_chars_per_hit]}"
        )
    return "\n\n---\n\n".join(blocks)


def _call_gemini_text(prompt, key, max_tokens=2048, temp=0.2):
    """Calls Gemini generateContent across prioritized models with thinking-budget control."""
    if not key:
        return "", "none"
    effective_tokens = max(int(max_tokens), 2048)
    for model in ["gemini-3-flash-preview", "gemini-3.1-flash-lite", "gemini-3.1-pro-preview"]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
        gen_cfg = {"temperature": temp, "maxOutputTokens": effective_tokens}
        if "gemini-3" in model and "flash" in model:
            gen_cfg["thinkingConfig"] = {"thinkingBudget": 128}
        payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": gen_cfg}
        for use_thinking in (True, False):
            if not use_thinking and "thinkingConfig" in gen_cfg:
                gen_cfg = {"temperature": temp, "maxOutputTokens": effective_tokens}
                payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": gen_cfg}
            elif not use_thinking:
                break
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
            try:
                with urllib.request.urlopen(req, timeout=28.0) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
                    txt = "".join(p.get("text", "") for p in parts if not p.get("thought"))
                    if txt:
                        return txt, model
                    break
            except urllib.error.HTTPError as e:
                if e.code == 400 and "thinkingConfig" in gen_cfg and use_thinking:
                    continue
                break
            except Exception:
                break
    return "", "fallback-raw"


def _call_ollama_text(prompt, model=None, max_tokens=1600, temp=0.2):
    """Calls local Ollama `/api/chat` as zero-cost offline LLM fallback when Gemini API is unavailable."""
    use_model = (model or OLLAMA_DEFAULT_CHAT_MODEL or "qwen2.5-7b-16k:latest").strip()
    if not _is_ollama_alive():
        return "", "fallback-raw"
    url = f"{OLLAMA_URL}/api/chat"
    payload = {
        "model": use_model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Du bist der deutschsprachige Career-OS-Assistent von Visar Murseli. "
                    "Antworte AUSSCHLIESSLICH auf einwandfreiem Deutsch (verwende niemals chinesische, "
                    "japanische oder koreanische Schriftzeichen) und stütze dich strikt auf die Fakten im Kontext."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "stream": False,
        "options": {"temperature": temp, "num_predict": min(int(max_tokens), 1800), "repeat_penalty": 1.08},
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=80.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            txt = ((data.get("message") or {}).get("content") or "").strip()
            if txt:
                return txt, f"ollama/{use_model}"
    except Exception:
        pass
    return "", "fallback-raw"


def _call_llm_text(prompt, key="", max_tokens=2048, temp=0.2):
    """Routes text synthesis to Gemini API first, seamlessly falling back to local Ollama chat model."""
    if key:
        txt, model = _call_gemini_text(prompt, key, max_tokens=max_tokens, temp=temp)
        if txt:
            return txt, model
    return _call_ollama_text(prompt, max_tokens=min(int(max_tokens), 1600), temp=temp)


def _verify_grounding(answer_text, sources):
    """Cross-checks `[Quelle: ...]` references in synthesized output against retrieved source files."""
    if not answer_text:
        return {"citation_count": 0, "verified_citations": 0, "verified_files": []}
    matches = re.findall(
        r"\[Quelle(?:\s+\d+)?:\s*([^\]]+)\]|\(Quelle(?:\s+\d+)?:\s*([^\)]+)\)",
        answer_text,
        flags=re.IGNORECASE,
    )
    cited_raw = [(m[0] or m[1]).strip() for m in matches if (m[0] or m[1]).strip()]
    source_tokens = []
    for s in sources:
        f_full = str(s.get("file", "")).lower()
        f_base = os.path.basename(f_full).lower()
        f_stem = os.path.splitext(f_base)[0].lower()
        t_low = str(s.get("title", "")).lower()
        source_tokens.append((s.get("file", ""), [f_full, f_base, f_stem, t_low]))

    verified_count = 0
    verified_files = []
    for cite_grp in cited_raw:
        sub_cites = [sc.strip() for sc in cite_grp.split(";") if sc.strip()] or [cite_grp]
        grp_matched = False
        for cite in sub_cites:
            cite_clean = re.sub(r"[`\"'*]", "", cite)
            cite_head = cite_clean.split("|")[0].strip().lower()
            matched_file = None
            dok_m = re.match(r"^(?:dok(?:ument)?|doc)\s*(\d+)$", cite_head)
            if dok_m:
                idx_1 = int(dok_m.group(1)) - 1
                if 0 <= idx_1 < len(sources):
                    matched_file = sources[idx_1].get("file", "")
            if not matched_file:
                for orig_file, toks in source_tokens:
                    if any(tok and (tok in cite_head or (len(cite_head) >= 5 and cite_head in tok)) for tok in toks):
                        matched_file = orig_file
                        break
            if matched_file:
                grp_matched = True
                if matched_file not in verified_files:
                    verified_files.append(matched_file)
        if grp_matched:
            verified_count += 1

    return {
        "citation_count": len(cited_raw),
        "verified_citations": verified_count,
        "verified_files": verified_files,
    }


def synthesize_answer(query, top_k=8, domain=None, style="deep"):
    hits = search(query, top_k=min(max(int(top_k), 8), 10), domain=domain, rerank=True)
    mode = hits[0].get("retrieval_mode", "bm25_expanded") if hits else "none"
    style_norm = "compact" if str(style).strip().lower() == "compact" else "deep"
    key = load_api_key()
    compact_sources = _format_sources_compact(hits)
    context_text = _build_context_blocks(hits, max_chars_per_hit=2200)
    if style_norm == "compact":
        style_rules = f"""ANTWORT-MODUS: ⚡ 60-SEKUNDEN KOMPAKT-BRIEFING
- Maximal 160–190 Wörter insgesamt!
- Format:
  ## ⚡ 60s-Essenz
  - Kernaussage 1 (mit [Quelle: Dateiname | Abschnitt])
  - Kernaussage 2 (konkreter Arbeit/Uni-Beleg mit [Quelle: Dateiname | Abschnitt])
  - Kernaussage 3 (Synergie / Mehrwert)
  - Kernaussage 4 (Konkreter Kennwert/Note/T-Code/Paragraf)
{_PRIVACY_AND_FACT_RULES}"""
        max_tokens = 800
        temp = 0.15
    else:
        style_rules = f"""ANTWORT-MODUS: 🔬 STRUKTURIERTE TIEFENANALYSE
- Beantworte präzise, fundiert und mehrperspektivisch (Arbeit × Studium × Architektur) auf Basis von Visar Murselis verifizierten Dokumenten.
- Gliedere mit klaren Überschriften (## / ###) und prägnanten Bulletpoints.
{_PRIVACY_AND_FACT_RULES}"""
        max_tokens = 1650
        temp = 0.2

    prompt = f"""{style_rules}

KONTEXT AUS DEM SECOND BRAIN:
{context_text}

FRAGE:
{query}
"""
    txt, model = _call_llm_text(prompt, key, max_tokens=max_tokens, temp=temp)
    if txt:
        grounding = _verify_grounding(txt, compact_sources)
        return {
            "answer": txt,
            "model": model,
            "mode": mode,
            "style": style_norm,
            "domain": domain,
            "grounding": grounding,
            "sources": compact_sources,
        }
    return {
        "answer": "Synthese fehlgeschlagen; zeige verifizierte Rohtreffer.",
        "model": "fallback-raw",
        "mode": mode,
        "style": style_norm,
        "domain": domain,
        "grounding": {"citation_count": 0, "verified_citations": 0, "verified_files": []},
        "sources": compact_sources,
    }


def _gather_multi_domain_hits(query, buckets):
    """Collects deduplicated high-signal evidence across specified `(domain, top_k)` buckets."""
    by_id = {}
    ordered = []
    for dom, k in buckets:
        for h in search(query, top_k=k, domain=dom, max_per_file=2, rerank=True):
            if h["id"] not in by_id:
                by_id[h["id"]] = h
                ordered.append(h)
    return ordered


def match_job_profile(job_text, company="", role=""):
    """Matches a job posting against Visar Murseli's Obsidian Knowledge Hub across Work, Study, and Primary Sources."""
    raw_job = (job_text or "").strip()
    if not raw_job:
        return {"ok": False, "error": "Keine Stellenbeschreibung übermittelt."}

    comp_clean = (company or "").strip()
    role_clean = (role or "").strip()
    req_lines = [
        re.sub(r"^[\-\*\u2022\d\.\)\s]+", "", ln).strip()
        for ln in raw_job.splitlines()
        if len(ln.strip()) >= 12
    ][:12]

    query_seed = " ".join(x for x in [comp_clean, role_clean, raw_job[:900]] if x)
    hits = _gather_multi_domain_hits(
        query_seed,
        buckets=[
            (None, 5),
            ("work", 4),
            ("study", 3),
            ("synergies", 3),
            ("curated", 4),
            ("library", 3),
        ],
    )[:14]
    mode = hits[0].get("retrieval_mode", "hybrid_rrf_rerank") if hits else "none"
    compact_sources = _format_sources_compact(hits)
    context_text = _build_context_blocks(hits, max_chars_per_hit=1800)

    key = load_api_key()
    prompt = f"""AUFGABE: STELLENANZEIGE × VAULT MATCHER (3-Säulen-Evidenz-Synthese für Visar Murseli)
UNTERNEHMEN: {comp_clean or 'Zielunternehmen'}
ZIELROLLE: {role_clean or 'Junior / Trainee ERP, SAP & IT-Governance'}

STELLENANFORDERUNGEN / TEXT:
{raw_job[:4500]}

VERIFIZIERTER KONTEXT AUS OBSIDIAN V2.1 (Schicht 1 + Primärquellen Schicht 2):
{context_text}

ERSTELLE GENAU DIESE 5 SEKTIONEN IN SAUBEREM MARKDOWN:
## 📊 Gesamt-Fit & Positionierung
- Realistische Fit-Einschätzung & roter Faden (M.Sc. Wirtschaftsinformatik 1,6, Masterarbeit 1,0 zu ERP-Transformation & Plattformisierung, 24M SSB S/4HANA IT-PMO, 12M Datacenter One ITIL 4 INOC).

## ✅ Anforderungs-Match-Matrix (Praxis × Studium × Primärbeleg)
- Für die wichtigsten 5–6 Anforderungen aus dem Inserat jeweils:
  - **Anforderung:** ...
  - **Praxisbeleg (SSB/DC1):** ... [Quelle: ...]
  - **Studium / Wissenschaft:** ... [Quelle: ...]
  - **Konkreter Nutzen ab Tag 1:** ...

## 🌟 3 maßgeschneiderte STAR-Hooks & Anschreiben-Argumente
- 3 kompakte, sofort sprechfertige Pitches inkl. Zahlen & [Quelle: ...].

## ⚠️ Mögliche kritische Rückfragen & souveräner Pivot
- 2 ehrliche Potenzial-/Lücken-Punkte aus der Anzeige (z. B. fehlende ABAP-Coding-Routine o. ä.) + konstruktive Architektur-/Lern-Brücke.

## ❓ 3 clevere Rückfragen an das Fach- & HR-Team
- 3 prägnante Fragen, die direkt aus Visars SSB-/Masterarbeits-Tiefe heraus gestellt werden.

{_PRIVACY_AND_FACT_RULES}"""

    txt, model = _call_llm_text(prompt, key, max_tokens=2000, temp=0.2)
    if txt:
        return {
            "ok": True,
            "company": comp_clean,
            "role": role_clean,
            "extracted_requirements": req_lines[:8],
            "answer": txt,
            "model": model,
            "mode": mode,
            "grounding": _verify_grounding(txt, compact_sources),
            "sources": compact_sources,
        }

    fallback_lines = ["## 📊 Offline-Match (Top-Belege aus Obsidian V2.1)", ""]
    for i, h in enumerate(hits[:8], 1):
        fallback_lines.append(f"- **[{i}] {h['title']}** ({h['domain']} | {h['type']}) — `{h['file']}` › {h['section']}: {h['snippet'][:220]}")
    return {
        "ok": True,
        "company": comp_clean,
        "role": role_clean,
        "extracted_requirements": req_lines[:8],
        "answer": "\n".join(fallback_lines),
        "model": "fallback-raw",
        "mode": mode,
        "grounding": {"citation_count": 0, "verified_citations": 0, "verified_files": []},
        "sources": compact_sources,
    }


_SPARRING_PERSONAS = {
    "kpmg": {
        "company": "KPMG",
        "persona": "KPMG Senior Manager IT-Transformation & Wirtschaftsprüfung",
        "focus": "IT-Audit, IKS, Segregation of Duties (SoD), Berechtigungskonzepte, Trennungsrechnung EU 1370/2007, ACDOCA, LTMC/CVI 0,00 € Übernahmekonto, SAP Cloud ALM Quality Gates",
    },
    "schwarz": {
        "company": "Schwarz Digits",
        "persona": "Schwarz Digits Lead Identity & Access Management / SAP HCM Security",
        "focus": "SAP IAM, PFCG, HR-Berechtigungsobjekt P_ORGIN, Structural Authorizations, UMT/Third-Level-Prozesse, SU53 & STAUTHTRACE, SoD-Governance, Betriebsrat § 87 Abs. 1 Nr. 6 BetrVG",
    },
    "trumpf": {
        "company": "TRUMPF",
        "persona": "TRUMPF Leitung IT-Governance & Enterprise Architecture",
        "focus": "Bimodale IT, Clean Core / BTP-Plattformisierung, TOGAF 9 ADM, Signavio BPMN-Standards, SAP Cloud ALM Governance, Industrie-IT-Steuerung",
    },
    "cto": {
        "company": "Enterprise CTO / Tech-Lead",
        "persona": "Kritischer CTO & Lebenslauf-Stresstester (Devil's Advocate)",
        "focus": "Tiefe vs. Breite im Lebenslauf, Java/SQL/RPA-Realismus, Übergang Werkstudent zu Junior/Trainee, Notensprung B.Sc. 3,0 zu M.Sc. 1,6 & Masterarbeit 1,0",
    },
}


def interview_sparring(action="ask", persona="kpmg", company="", question="", user_answer="", topic=""):
    """Devil's Advocate Interview Simulator grounded strictly in Visar's Obsidian Knowledge Hub."""
    act = (action or "ask").strip().lower()
    p_key = (persona or "kpmg").strip().lower()
    cfg = _SPARRING_PERSONAS.get(p_key, {})
    comp_name = (company or cfg.get("company") or "Zielunternehmen").strip()
    persona_label = cfg.get("persona") or f"Kritischer Fach-Interviewer ({comp_name})"
    focus_str = f"{cfg.get('focus', '')} {topic}".strip()

    key = load_api_key()
    if act == "evaluate":
        q_clean = (question or "").strip()
        ans_clean = (user_answer or "").strip()
        if not ans_clean:
            return {"ok": False, "error": "Bitte gib zuerst eine Antwort zum Bewerten ein."}
        search_q = f"{comp_name} {focus_str} {q_clean} {ans_clean[:400]}".strip()
        hits = _gather_multi_domain_hits(search_q, buckets=[(None, 6), ("curated", 4), ("empirie", 2)])[:10]
        mode = hits[0].get("retrieval_mode", "hybrid_rrf_rerank") if hits else "none"
        compact_sources = _format_sources_compact(hits)
        context_text = _build_context_blocks(hits, max_chars_per_hit=1800)

        eval_prompt = f"""ROLLE: {persona_label} (streng, fair, analytisch – Devil's Advocate)
INTERVIEW-FRAGE AN VISAR:
{q_clean or 'Fachliche Rückfrage zum Profil'}

ANTWORT VON VISAR:
{ans_clean}

VERIFIZIERTE FAKTEN AUS VISARS OBSIDIAN V2.1 SECOND BRAIN:
{context_text}

BEWERTE VISARS ANTWORT IN GENAU DIESEN 4 SEKTIONEN:
## 📊 Score & Fakten-Audit (`X/10`)
- Bewertung nach Klarheit, Tiefe, Junior-/Trainee-Haltung und Faktentreue gegen Obsidian V2.1 (inkl. [Quelle: ...]).

## ✅ Was bereits stark überzeugt
- Konkrete Pluspunkte der Antwort.

## ⚠️ Lücken & Devil's-Advocate-Nachhaken
- Was fehlt? Wo hätte ein Senior-Interviewer kritisch nachgebohrt (z. B. fehlender T-Code, fehlendes Praxisbeispiel, fehlende Maßzahl)?

## 🚀 Perfektionierte 60-Sekunden-STAR-Antwort
- Formuliere eine druckreife, authentische Verbesserungsfassung in der Ich-Form mit verifizierten Belegen und [Quelle: ...].

{_PRIVACY_AND_FACT_RULES}"""
        txt, model = _call_llm_text(eval_prompt, key, max_tokens=1700, temp=0.2)
        if txt:
            return {
                "ok": True,
                "action": "evaluate",
                "company": comp_name,
                "persona": persona_label,
                "feedback": txt,
                "model": model,
                "mode": mode,
                "grounding": _verify_grounding(txt, compact_sources),
                "sources": compact_sources,
            }
        return {
            "ok": True,
            "action": "evaluate",
            "company": comp_name,
            "persona": persona_label,
            "feedback": "## ⚠️ Offline-Faktenabgleich\n\n" + "\n".join(f"- **{h['title']}** (`{h['file']}`): {h['snippet'][:220]}" for h in hits[:5]),
            "model": "fallback-raw",
            "mode": mode,
            "grounding": {"citation_count": 0, "verified_citations": 0, "verified_files": []},
            "sources": compact_sources,
        }

    # Default action: "ask" -> formulate one sharp, grounded critical question
    search_q = f"{comp_name} {focus_str} {topic}".strip()
    hits = _gather_multi_domain_hits(search_q, buckets=[(None, 4), ("curated", 4), ("empirie", 2), ("library", 3)])[:10]
    mode = hits[0].get("retrieval_mode", "hybrid_rrf_rerank") if hits else "none"
    compact_sources = _format_sources_compact(hits)
    context_text = _build_context_blocks(hits, max_chars_per_hit=1600)
    prev_note = f"\nBISHERIGE FRAGE (stelle jetzt eine ANDERE, tiefergehende Frage): {question.strip()}" if (question or "").strip() else ""

    ask_prompt = f"""ROLLE: {persona_label}
FOKUSTHEMA: {focus_str}{prev_note}

VERIFIZIERTER KONTEXT ÜBER VISAR MURSELI:
{context_text}

AUFGABE:
Stelle EINE einzige, realistische, anspruchsvolle Interviewfrage (als direkten Dialogbeitrag des Interviewers, 2–4 Sätze), die auf Visars echtem Lebenslauf/Kontext aufsetzt und Transferdenken verlangt (keine triviale Definitionsfrage).
Gib darunter GENAU EINEN kurzen Orientierungspunkt im Format:
**Prüf-Fokus:** <Stichworte welche Obsidian-Fakten/T-Codes/Methoden eine Top-Antwort abdecken sollte> [Quelle: Dateiname | Abschnitt]

{_PRIVACY_AND_FACT_RULES}"""
    txt, model = _call_llm_text(ask_prompt, key, max_tokens=550, temp=0.35)
    if txt:
        return {
            "ok": True,
            "action": "ask",
            "company": comp_name,
            "persona": persona_label,
            "question": txt.strip(),
            "model": model,
            "mode": mode,
            "grounding": _verify_grounding(txt, compact_sources),
            "sources": compact_sources,
        }
    return {
        "ok": True,
        "action": "ask",
        "company": comp_name,
        "persona": persona_label,
        "question": f"Wie stellen Sie bei {comp_name} konkret sicher, dass S/4HANA-Erweiterungen und Berechtigungsprozesse (z. B. PFCG/SoD bzw. Clean Core) revisionssicher und ohne technische Schulden funktionieren? Belegen Sie Ihre Antwort an einem konkreten Beispiel aus Ihrer SSB-/Masterarbeitspraxis.",
        "model": "fallback-raw",
        "mode": mode,
        "grounding": {"citation_count": 0, "verified_citations": 0, "verified_files": []},
        "sources": compact_sources,
    }


def tailor_cv_profile(job_text="", company="", role="", current_cv=None):
    """Tailors Visar's de-risked CV against a target job description using verified Obsidian evidence."""
    from cv_generator import get_default_cv_presets

    presets = get_default_cv_presets()
    base = presets["universal"]
    comp_clean = (company or "").strip()
    role_clean = (role or "").strip()
    job_clean = (job_text or "").strip()

    seed = " ".join(x for x in (comp_clean, role_clean, job_clean[:700]) if x).strip()
    if not seed:
        return {"ok": False, "error": "Bitte gib zuerst eine Stellenbeschreibung, Zielrolle oder Firma ein."}

    hits = _gather_multi_domain_hits(
        seed,
        buckets=[(None, 4), ("work", 4), ("study", 3), ("synergies", 2), ("curated", 3)],
    )[:12]
    mode = hits[0].get("retrieval_mode", "hybrid_rrf_rerank") if hits else "none"
    compact_sources = _format_sources_compact(hits)
    context_text = _build_context_blocks(hits, max_chars_per_hit=1400)
    key = load_api_key()

    cur_sub = ((current_cv or {}).get("header") or {}).get("subtitle") or base["header"]["subtitle"]
    prompt = f"""DU BIST EIN EXECUTIVE-KARRIEREBERATER & CV-ARCHITEKT FÜR VISAR MURSELI (M.Sc. Wirtschaftsinformatik, Note 1,6; Masterarbeit 1,0).

ZIELUNTERNEHMEN: {comp_clean or 'Zielunternehmen'}
ZIELROLLE: {role_clean or cur_sub}
STELLENANFORDERUNGEN:
{job_clean[:2200]}

VERIFIZIERTE OBSIDIAN-FAKTEN:
{context_text}

STRIKTE CV DE-RISKING & WAHRHEITSREGELN:
1. NIEMALS rohe Entwickler-Skills (Java, Python, SQL, HTML, CSS, UiPath Scripting) als Entwicklerkompetenz auflisten — IMMER als „Architektur- & Datenverständnis (Relationale Datenmodelle / SQL-Validierung)“ bzw. „Business Process Automation & Machbarkeitsanalyse (BPMN 2.0, PDD)“ framen!
2. SSB AG (05/2024–04/2026, 24 Monate) IMMER auf IT-PMO-/Architektur-Niveau framen (TP1–TP5 Steuerung, SDD, SAP Cloud ALM How2Handle, Signavio BPMN 2.0, Enable Now Übergabe, LTMC/CVI).
3. Keine erfundenen Stationen, keine Vorgesetztennamen, keine internen WBS-Nummern, NIEMALS „Robert Bosch“.
4. Output AUSSCHLIESSLICH als valides JSON-Objekt ohne einleitenden Text oder Markdown-Prosa:
{{
  "subtitle": "Prägnante 1-zeilige Ziel-Headline passend zur Stelle",
  "summary": "2 bis maximal 3 druckreife Sätze für das Kurzprofil (mit verifizierten Kennzahlen M.Sc. 1,6, Thesis 1,0, 36M Praxis)",
  "ssb_bullets": ["4 präzise, auf diese Stelle gewichtete Bulletpoints für SSB AG"],
  "dc1_bullets": ["3 präzise Bulletpoints für Datacenter One GmbH (ITIL 4, 24/7 INOC, SLA, SOPs, HLM)"],
  "skills_erp": "Kompakt priorisierte ERP-, Cloud- & Governance-Keywords für ATS-Match",
  "skills_data": "De-riskte Formulierung für Daten-, Analyse- & Automatisierungskompetenz",
  "highlights": ["3 stichpunktartige Erklärungen, welche Stellenanforderungen durch welche CV-Anpassung abgedeckt wurden"]
}}"""

    txt, model = _call_llm_text(prompt, key, max_tokens=1500, temp=0.18)
    parsed = None
    if txt:
        raw_json = txt.strip()
        fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_json, flags=re.DOTALL | re.IGNORECASE)
        if fence:
            raw_json = fence.group(1)
        else:
            brace = re.search(r"\{.*\}", raw_json, flags=re.DOTALL)
            if brace:
                raw_json = brace.group(0)
        try:
            cand = json.loads(raw_json)
            if isinstance(cand, dict) and cand.get("summary") and cand.get("ssb_bullets"):
                parsed = cand
        except Exception:
            parsed = None

    if not parsed:
        # Deterministic role-smart fallback without LLM
        parsed = {
            "subtitle": f"{role_clean or 'SAP Transformation & IT-PMO Consultant'} • M.Sc. Wirtschaftsinformatik (1,6)",
            "summary": base["summary"],
            "ssb_bullets": base["experience"][0]["bullets"],
            "dc1_bullets": base["experience"][1]["bullets"],
            "skills_erp": base["skills"]["erp_governance"],
            "skills_data": base["skills"]["data_analysis"],
            "highlights": [
                "De-Risking angewandt: Keine Coding-Fangfragen, voller Fokus auf S/4HANA Governance & Architektur",
                "Akademische Spitzenwerte integriert: M.Sc. 1,6 (120 ECTS) + Masterarbeit 1,0 + B.Sc. 180 ECTS (1,7 Thesis)",
                "ATS-Schlüsselbegriffe anhand deiner Obsidian-Quellen nachgerichtet",
            ],
        }
        model = "deterministic-fallback"

    # Privacy & hallucination sanitizer
    banned = ["Robert Bosch", "Roland Nowak", "Dietmar Fillinger", "Helmut Schmidpeter", "WBS 1–297"]
    def _clean_text(s):
        out = str(s or "")
        for bad in banned:
            out = re.sub(re.escape(bad), "", out, flags=re.IGNORECASE)
        return out.strip()

    safe = {
        "subtitle": _clean_text(parsed.get("subtitle") or cur_sub),
        "summary": _clean_text(parsed.get("summary") or base["summary"]),
        "ssb_bullets": [_clean_text(x) for x in (parsed.get("ssb_bullets") or base["experience"][0]["bullets"])[:4] if _clean_text(x)],
        "dc1_bullets": [_clean_text(x) for x in (parsed.get("dc1_bullets") or base["experience"][1]["bullets"])[:3] if _clean_text(x)],
        "skills_erp": _clean_text(parsed.get("skills_erp") or base["skills"]["erp_governance"]),
        "skills_data": _clean_text(parsed.get("skills_data") or base["skills"]["data_analysis"]),
        "highlights": [_clean_text(x) for x in (parsed.get("highlights") or [])[:4] if _clean_text(x)],
    }

    return {
        "ok": True,
        "model": model,
        "mode": mode,
        "tailored": safe,
        "sources": compact_sources,
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Local Career OS Hybrid RAG Engine V3 (BM25 + Dense Vector RRF + Rerank)")
    parser.add_argument("--build", action="store_true", help="Rebuilds FTS5 + 768d vector anchor index from Obsidian Vault")
    parser.add_argument("--no-vectors", action="store_true", help="Skip Gemini vector embedding during --build (keep offline/fast)")
    parser.add_argument("--embed", action="store_true", help="Builds missing vector embeddings on existing DB")
    parser.add_argument("--provider", type=str, default="gemini", choices=["gemini", "ollama"], help="Vector provider for --embed")
    parser.add_argument("--embed-model", type=str, default=OLLAMA_DEFAULT_EMBED_MODEL, help="Ollama embedding model (e.g. nomic-embed-text, bge-m3)")
    parser.add_argument("--max-chunks", type=int, default=900, help="Max vector chunks to embed with --embed (default: 900, Free-Tier safe)")
    parser.add_argument("--upsert", type=str, help="Incrementally upserts a single .md file into FTS5 + vector index")
    parser.add_argument("--stats", action="store_true", help="Shows RAG index statistics")
    parser.add_argument("--pipeline", action="store_true", help="Shows live application pipeline JSON")
    parser.add_argument("--query", type=str, help="Searches indexed chunks via Hybrid RRF (BM25 + Vector + Rerank)")
    parser.add_argument("--ask", type=str, help="Hybrid RRF RAG query + Gemini synthesis")
    parser.add_argument("--job-match", type=str, help="Matches a job description text against Obsidian Vault")
    parser.add_argument("--sparring-ask", type=str, help="Generates a Devil's Advocate interview question for persona (kpmg, schwarz, trumpf, cto)")
    parser.add_argument("--domain", type=str, default=None, help="Optional filter: work, study, synergies, curated, empirie, library, or exact YAML domain")
    parser.add_argument("--style", type=str, default="deep", choices=["compact", "deep"], help="Synthesis style: compact (60s briefing) or deep")
    args = parser.parse_args()

    if args.build:
        build_index(with_vectors=not args.no_vectors)
    elif args.embed:
        if args.provider == "ollama":
            print(json.dumps(embed_ollama_anchors(model=args.embed_model, force=False, max_chunks=args.max_chunks), indent=2, ensure_ascii=False))
        else:
            print(json.dumps(embed_anchors(force=False, max_chunks=args.max_chunks), indent=2, ensure_ascii=False))
    elif args.upsert:
        print(json.dumps(upsert_note(args.upsert), indent=2, ensure_ascii=False))
    elif args.stats:
        print(json.dumps(get_stats(), indent=2, ensure_ascii=False))
    elif args.pipeline:
        print(json.dumps(get_pipeline_data(), indent=2, ensure_ascii=False))
    elif args.query:
        res = search(args.query, top_k=6, domain=args.domain)
        mode = res[0]["retrieval_mode"] if res else "none"
        print(f"=== MODE: {mode} | DOMAIN: {args.domain or 'all'} | EXPANDED: {res[0]['expanded_terms'] if res else []} ===")
        for idx, r in enumerate(res, 1):
            print(f"\n[{idx}] RRF={r['score']} | Sim={r['vec_sim']}% | Boost={r.get('rerank_boost', 1.0)} | {r['type']} | {r['file']} :: {r['section']}")
            print(r["snippet"][:300].replace("\n", " "))
    elif args.ask:
        print(json.dumps(synthesize_answer(args.ask, domain=args.domain, style=args.style), indent=2, ensure_ascii=False))
    elif args.job_match:
        print(json.dumps(match_job_profile(args.job_match), indent=2, ensure_ascii=False))
    elif args.sparring_ask:
        print(json.dumps(interview_sparring(action="ask", persona=args.sparring_ask), indent=2, ensure_ascii=False))
    else:
        print(json.dumps(get_stats(), indent=2, ensure_ascii=False))
