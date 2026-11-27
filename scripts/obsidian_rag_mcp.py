# -*- coding: utf-8 -*-
"""
Zero-Dependency MCP (Model Context Protocol) Stdio Server für Visar Murselis
Obsidian V2.1 Hybrid-RAG & Bewerbungspipeline.

Kompatibel mit jedem Standard-MCP-Client (Antigravity, Claude Desktop, Cursor)
via JSON-RPC 2.0 über stdin/stdout (ohne externe Python-Abhängigkeiten).
"""

import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import local_rag_engine as rag  # noqa: E402

SERVER_INFO = {"name": "obsidian-career-rag", "version": "2.1.0"}
PROTOCOL_VERSION = "2024-11-05"

TOOLS = [
    {
        "name": "search_obsidian_rag",
        "description": "Hybrid RRF (FTS5 BM25 + 1024d bge-m3 Vektor + Cross-Signal-Reranker) Suche über den gesamten Obsidian V2.1 Knowledge Vault inkl. 454 Fachbüchern.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Suchbegriff oder Fachfrage"},
                "domain": {"type": "string", "description": "Optional: work, study, synergies, curated, empirie, library"},
                "top_k": {"type": "integer", "default": 6, "description": "Anzahl Ergebnisse (1-15)"},
            },
            "required": ["query"],
        },
    },
    {
        "name": "read_obsidian_note",
        "description": "Liest den vollständigen Markdown-Inhalt einer Notiz anhand ihres relativen Vault-Pfads (file_rel).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file_rel": {"type": "string", "description": "Relativer Pfad im Obsidian Vault aus Suchergebnissen"},
                "max_chars": {"type": "integer", "default": 12000, "description": "Maximale Zeichenanzahl"},
            },
            "required": ["file_rel"],
        },
    },
    {
        "name": "ask_career_rag",
        "description": "Beantwortet Fragen mit verifizierter Obsidian-Evidenz und Grounding-Prüfung (60s-kompakt oder tiefgehend).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Fach- oder Interviewfrage"},
                "domain": {"type": "string", "description": "Optional: work, study, synergies, curated, empirie, library"},
                "style": {"type": "string", "enum": ["compact", "deep"], "default": "deep"},
            },
            "required": ["query"],
        },
    },
    {
        "name": "match_job_description",
        "description": "Stellenanzeige x Vault Matcher: Mappt Anforderungen gegen SSB/DC1-Praxis, Uni-Module und Primärquellen.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "job_text": {"type": "string", "description": "Text der Stellenanzeige"},
                "company": {"type": "string", "description": "Unternehmen"},
                "role": {"type": "string", "description": "Zielrolle"},
            },
            "required": ["job_text"],
        },
    },
    {
        "name": "get_rag_and_pipeline_status",
        "description": "Liefert aktuelle Index-Statistiken von career_os_rag.db und die Live-Bewerbungs-Pipeline.",
        "inputSchema": {"type": "object", "properties": {}},
    },
]


def _safe_note_read(file_rel, max_chars=12000):
    rel_clean = (file_rel or "").replace("/", os.sep).lstrip("\\/")
    base = os.path.abspath(rag.VAULT_DIR)
    target = os.path.abspath(os.path.join(base, rel_clean))
    if not target.startswith(base + os.sep) or not os.path.isfile(target):
        return {"ok": False, "error": f"Ungültiger oder fehlender Pfad: {file_rel}"}
    with open(target, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read(int(max_chars) + 1)
    truncated = len(text) > int(max_chars)
    return {"ok": True, "file": file_rel, "truncated": truncated, "content": text[:int(max_chars)]}


def _dispatch_tool(name, args):
    args = args or {}
    if name == "search_obsidian_rag":
        top_k = max(1, min(int(args.get("top_k", 6)), 15))
        hits = rag.search(args.get("query", ""), top_k=top_k, domain=args.get("domain") or None)
        return [
            {
                "file": h["file"],
                "title": h["title"],
                "domain": h["domain"],
                "type": h["type"],
                "section": h["section"],
                "score": h["score"],
                "vec_sim": h.get("vec_sim", 0.0),
                "rerank_boost": h.get("rerank_boost", 1.0),
                "snippet": h["snippet"],
            }
            for h in hits
        ]
    if name == "read_obsidian_note":
        return _safe_note_read(args.get("file_rel", ""), args.get("max_chars", 12000))
    if name == "ask_career_rag":
        return rag.synthesize_answer(
            args.get("query", ""),
            domain=args.get("domain") or None,
            style=args.get("style", "deep"),
        )
    if name == "match_job_description":
        return rag.match_job_profile(
            args.get("job_text", ""),
            company=args.get("company", ""),
            role=args.get("role", ""),
        )
    if name == "get_rag_and_pipeline_status":
        return {"rag": rag.get_stats(), "pipeline": rag.get_pipeline_data()}
    raise ValueError(f"Unbekanntes Tool: {name}")


def _write_msg(obj):
    sys.stdout.write(json.dumps(obj, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def handle_message(msg):
    req_id = msg.get("id")
    method = msg.get("method", "")
    params = msg.get("params") or {}

    if method == "notifications/initialized" or req_id is None:
        return None
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {}},
                "serverInfo": SERVER_INFO,
            },
        }
    if method == "ping":
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": TOOLS}}
    if method == "tools/call":
        try:
            payload = _dispatch_tool(params.get("name"), params.get("arguments"))
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False, indent=2)}],
                    "isError": False,
                },
            }
        except Exception as exc:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": f"Fehler: {exc}"}],
                    "isError": True,
                },
            }
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"Method not found: {method}"},
    }


def main():
    for raw in sys.stdin:
        line = raw.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError as exc:
            _write_msg({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(exc)}})
            continue
        resp = handle_message(msg)
        if resp is not None:
            _write_msg(resp)


if __name__ == "__main__":
    main()
