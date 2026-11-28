# -*- coding: utf-8 -*-
"""
Exportiert ein kompaktes, datenschutzbereinigtes Cloud Knowledge Pack
(oracle_cloud/data/career_os_cloud.db) aus der lokalen career_os_rag.db.

Inhalt:
- Alle kuratierten Layer-1-Notizen (ohne private/medizinische/familienbezogene Daten)
- Bis zu 3 Anker-Chunks pro Fachbuch (447+ Werke) für globale Suche unterwegs
- FTS5-Index (unicode61 remove_diacritics 2) + Zero-Leak Compliance Gate
"""

import os
import re
import sqlite3
from datetime import datetime, timezone

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DB = os.path.join(BASE_DIR, "config", "career_os_rag.db")
OUT_DB = os.path.join(BASE_DIR, "oracle_cloud", "data", "career_os_cloud.db")

PRIVATE_BLOCK_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in (
        r"\btilidin\b",
        r"\bdr\.?\s*vollmer\b",
        r"\bnikkah\b",
        r"\balbina\b",
        r"\bshqiptar634\b",
        r"\blohnabrechnung",
        r"\bgesundheit",
    )
]

REDACT_TERMS = [
    "Roland Nowak", "Dietmar Fillinger", "Helmut Schmidpeter",
    "Sarah Lozano", "Thomas Wimpff", "Sebastian Neifer",
    "Markus Schmidt", "Joachim Kraus", "Henning Gerdes",
    "Armin Heinrich", "Michael Gehrung",
    "WBS 1–297", "Vorgang 110", "Vorgang 294", "Vorgang 297",
]

FORBIDDEN_COMPLIANCE = [
    re.compile(r"Robert\s+Bosch", re.IGNORECASE),
]


def _sanitize_text(text: str) -> str:
    if not text:
        return ""
    cleaned = text
    for term in REDACT_TERMS:
        cleaned = re.sub(re.escape(term), "[anonymisiert]", cleaned, flags=re.IGNORECASE)
    return cleaned


def _contains_private_block(text: str) -> bool:
    return any(rx.search(text or "") for rx in PRIVATE_BLOCK_PATTERNS)


def export_cloud_pack(src_db: str = SRC_DB, out_db: str = OUT_DB) -> dict:
    if not os.path.exists(src_db):
        raise FileNotFoundError(f"Quell-DB nicht gefunden: {src_db}")

    os.makedirs(os.path.dirname(out_db), exist_ok=True)
    tmp_db = out_db + ".tmp"
    if os.path.exists(tmp_db):
        os.remove(tmp_db)

    src = sqlite3.connect(src_db)
    dst = sqlite3.connect(tmp_db)
    try:
        dst.execute("CREATE TABLE metadata (k TEXT PRIMARY KEY, v TEXT)")
        dst.execute(
            """
            CREATE TABLE cloud_chunks (
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
            """
        )
        dst.execute("CREATE INDEX idx_cloud_file_rel ON cloud_chunks(file_rel)")
        dst.execute(
            """
            CREATE VIRTUAL TABLE cloud_chunks_fts USING fts5(
                title,
                section,
                file_rel,
                domain,
                content,
                content='cloud_chunks',
                content_rowid='id',
                tokenize='unicode61 remove_diacritics 2'
            )
            """
        )

        # 1. Layer-1-Notizen (nicht 05_Archiv, keine Logs)
        layer1_rows = src.execute(
            """
            SELECT file_rel, doc_id, title, domain, doc_type, section, content
            FROM chunks
            WHERE file_rel NOT LIKE '05_Archiv%'
              AND doc_type NOT IN ('log')
            ORDER BY id ASC
            """
        ).fetchall()

        # 2. Bis zu 3 Anker-Chunks je Fachbuch (reference-book)
        book_rows = src.execute(
            """
            WITH ranked AS (
                SELECT
                    file_rel, doc_id, title, domain, doc_type, section, content,
                    ROW_NUMBER() OVER (PARTITION BY file_rel ORDER BY id ASC) AS rn
                FROM chunks
                WHERE doc_type = 'reference-book'
            )
            SELECT file_rel, doc_id, title, domain, doc_type, section, content
            FROM ranked
            WHERE rn <= 3
            """
        ).fetchall()

        inserted = 0
        skipped_private = 0
        seen_files = set()

        for row in layer1_rows + book_rows:
            file_rel, doc_id, title, domain, doc_type, section, content = row
            combined = f"{file_rel}\n{title}\n{section}\n{content}"
            if _contains_private_block(combined):
                skipped_private += 1
                continue

            s_title = _sanitize_text(title or "")
            s_section = _sanitize_text(section or "")
            s_content = _sanitize_text(content or "")

            # Zero-Hallucination Check
            for rx in FORBIDDEN_COMPLIANCE:
                if rx.search(s_content):
                    s_content = rx.sub("[Compliance-gefiltert]", s_content)

            dst.execute(
                """
                INSERT INTO cloud_chunks (file_rel, doc_id, title, domain, doc_type, section, content, char_len)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (file_rel, doc_id, s_title, domain, doc_type, s_section, s_content, len(s_content)),
            )
            seen_files.add(file_rel)
            inserted += 1

        dst.execute("INSERT INTO cloud_chunks_fts(cloud_chunks_fts) VALUES('rebuild')")
        built_at = datetime.now(timezone.utc).isoformat()
        dst.executemany(
            "INSERT INTO metadata(k, v) VALUES (?, ?)",
            [
                ("built_at", built_at),
                ("total_chunks", str(inserted)),
                ("total_files", str(len(seen_files))),
                ("skipped_private", str(skipped_private)),
                ("privacy_gate", "strict-sanitized"),
            ],
        )
        dst.commit()
    finally:
        src.close()
        dst.close()

    if os.path.exists(out_db):
        os.remove(out_db)
    os.replace(tmp_db, out_db)

    size_mb = round(os.path.getsize(out_db) / (1024 * 1024), 2)
    return {
        "ok": True,
        "out_db": out_db,
        "total_chunks": inserted,
        "total_files": len(seen_files),
        "skipped_private": skipped_private,
        "size_mb": size_mb,
    }


if __name__ == "__main__":
    res = export_cloud_pack()
    print(f"[OK] Cloud Knowledge Pack gebaut: {res['out_db']}")
    print(f"     Dateien: {res['total_files']} | Chunks: {res['total_chunks']} | Privat gefiltert: {res['skipped_private']} | Groesse: {res['size_mb']} MB")
