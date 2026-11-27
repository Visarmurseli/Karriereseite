# -*- coding: utf-8 -*-
"""Obsidian Career OS Extraction & Synchronization Pipeline V2.

Walks all 5 workspace pillars (00_Aktuelle_Bewerbungsunterlagen through 04_DC1),
deduplicates source documents by SHA-256 bytes, extracts each unique document via
extractors_v2 into a single unsplit Markdown note under 05_Archiv/Volltexte_Quellen/,
preserves 100% of curated Layer-1 notes and module overviews, strips redundant raw
dumps/monoliths, fixes broken links, and guarantees 0 duplicate notes.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
import re
import shutil
import sys
import time
import zipfile
from collections import defaultdict
from datetime import datetime
from typing import Any

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from extractors_v2 import clean_text, extract_document_v2, finalize_markdown_body  # noqa: E402

VAULT_DIR = r"C:\Users\SHQIPTAR634\Documents\Obsidian Vault"
QUELLEN_REL = os.path.join("05_Archiv", "Volltexte_Quellen")
QUELLEN_DIR = os.path.join(VAULT_DIR, QUELLEN_REL)
LEGACY_DATALAKE_DIR = os.path.join(VAULT_DIR, "05_Archiv", "Volltexte_DataLake")
REGISTRY_V2_PATH = os.path.join(BASE_DIR, "config", "ingestion_v2_registry.json")

PILLARS = [
    "00_Aktuelle_Bewerbungsunterlagen",
    "01_SSB",
    "02_Master",
    "03_Bachelor",
    "04_DC1",
    "05_Fachliteratur_Bibliothek",
]

ALLOWED_EXTENSIONS = {
    ".pdf", ".epub", ".docx", ".doc", ".odt", ".pptx", ".xlsx", ".xlsm",
    ".csv", ".msg", ".vsdx", ".mpp", ".html", ".htm", ".md", ".txt", ".ps1",
}

SKIP_DIR_NAMES = {
    "node_modules", ".git", ".obsidian", "__pycache__", ".specify", ".venv", "venv",
    "03_HR_Vertraege_und_Administration", "04_Lohnabrechnungen",
    "05_HR_Werkstudent_Administration", "06_Original_Backups_OneNote",
    "00_Knowledge_Mining_NotebookLM", "SAP-Credentials",
    "99_Off_Topic_Nicht_Fuer_RAG",
    "target", "build", "dist", ".gradle", ".idea", ".settings", "bin",
    "PS_Module", "jlGui - Music Player - JavaDoc",
}

SKIP_REL_SUBSTRINGS = (
    os.path.join("Programmentwicklung", "01_Programmentwicklung_WS20", "PE2", "Vorlesungsfolien", "Git-Tutorial"),
    os.path.join("Programmentwicklung", "01_Programmentwicklung_WS20", "PE2", "Vorlesungsfolien", "example-web-app"),
)

# Maps Master & Bachelor top-level directory names -> canonical Layer-1 Modul_*.md basename
ACADEMIC_FOLDER_TO_MODUL: dict[tuple[str, str], str] = {
    ("02_Master", "AI4IoT – Artificial Intelligence for the Internet of Things"): "Modul_AI4IoT",
    ("02_Master", "Advanced Software Engineering"): "Modul_Advanced_Software_Engineering",
    ("02_Master", "Applied AI and Upcoming Technologies in Industries"): "Modul_Applied_AI",
    ("02_Master", "Datenbanken und Informationssysteme"): "Modul_Datenbanken",
    ("02_Master", "Digitale Nachhaltigkeit"): "Modul_Digitale_Nachhaltigkeit",
    ("02_Master", "Forschungsmethoden in der Wirtschaftsinformatik"): "Modul_Forschungsmethoden",
    ("02_Master", "Forschungsprojekte in der Wirtschaftsinformatik"): "Modul_FPWI",
    ("02_Master", "Innovationsmanagement"): "Modul_Innovationsmanagement",
    ("02_Master", "Innovationsmethoden für software- und datenintensive Geschäftsmodelle"): "Modul_ISG",
    ("02_Master", "Management von IT-Unternehmen"): "Modul_Management_IT_Unternehmen",
    ("02_Master", "Masterarbeit Wirtschaftsinformatik"): "Modul_Masterarbeit",
    ("02_Master", "Seminar Wirtschaftsinformatik 2"): "Modul_Seminar_WI2",
    ("02_Master", "Service Management and Cloud Computing, and Evaluation"): "Modul_Cloud_Computing",
    ("02_Master", "Service Operations Management"): "Modul_SOM",
    ("02_Master", "Software-Architektur"): "Modul_Software_Architektur",
    ("02_Master", "Theorie und Empirie internationaler Unternehmenstätigkeit"): "Modul_TEUI",
    ("02_Master", "xZusatz_Advanced Information Management (AIM)"): "Modul_AIM",
    ("02_Master", "xZusatz_nice2have-Grundlagen der Quanteninformatik"): "Modul_Quanteninformatik",
    ("02_Master", "xZusatz_nice2have-Smart Cities and Internet of Things"): "Modul_SmartCities",
    ("02_Master", "xZusatz_Schwedisch A1"): "Modul_Übersicht",
    ("02_Master", "xZusatz_Studienorganisation & Nachweise"): "Modul_Übersicht",
    ("02_Master", "xZusatz_nice2have-AI Prototyping 101"): "Modul_Übersicht",
    ("03_Bachelor", "Automaten und Formale Sprachen"): "Modul_AFS",
    ("03_Bachelor", "BWL 1 - Organisation, Personalführung, Strategisches Management"): "Modul_BWL1",
    ("03_Bachelor", "Bachelorarbeit Wirtschaftsinformatik"): "Modul_Bachelorarbeit",
    ("03_Bachelor", "Datenstrukturen und Algorithmen"): "Modul_DSA",
    ("03_Bachelor", "Einführung in die Softwaretechnik"): "Modul_EST",
    ("03_Bachelor", "Einführung in die Wirtschaftsinformatik"): "Modul_EWI",
    ("03_Bachelor", "GBWL 1 - Strukturen der Betriebswirtschaftslehre"): "Modul_GBWL1",
    ("03_Bachelor", "GBWL 4 - Finanzprozess"): "Modul_GBWL4",
    ("03_Bachelor", "GVWL 1 - Märkte & wirtschaftliche Entscheidungen"): "Modul_GVWL1",
    ("03_Bachelor", "Informatikrecht"): "Modul_Informatikrecht",
    ("03_Bachelor", "Informationsmanagement"): "Modul_Informationsmanagement_Bachelor",
    ("03_Bachelor", "Informationsverarbeitungspraktikum"): "Modul_Informationsverarbeitungspraktikum",
    ("03_Bachelor", "Management von Dienstleistungsunternehmen"): "Modul_Dienstleistungsmanagement",
    ("03_Bachelor", "Marketing Management"): "Modul_Marketing_Management",
    ("03_Bachelor", "Mathematik für Wirtschaftswissenschaftler"): "Modul_Mathematik",
    ("03_Bachelor", "Mensch-Computer-Interaktion"): "Modul_MCI",
    ("03_Bachelor", "Modellierung"): "Modul_Modellierung",
    ("03_Bachelor", "Profilseminar zum Human Resource Management"): "Modul_Profilseminar_HRM",
    ("03_Bachelor", "Programmentwicklung"): "Modul_Programmentwicklung",
    ("03_Bachelor", "Programmierung und Software-Entwicklung"): "Modul_PSE",
    ("03_Bachelor", "Schreibwerkstatt - Vom studentischen zum beruflichen Schreiben"): "Modul_Schreibwerkstatt",
    ("03_Bachelor", "Seminar interdisziplinäre Themen"): "Modul_Seminar_Interdisziplinaer",
    ("03_Bachelor", "Softwarepraktikum"): "Modul_Softwarepraktikum",
    ("03_Bachelor", "Statistik I"): "Modul_Statistik1",
    ("03_Bachelor", "Statistik II"): "Modul_Statistik2",
    ("03_Bachelor", "Wissensverarbeitung"): "Modul_Wissensverarbeitung",
    ("03_Bachelor", "xZusatz_Studienorganisation & Nachweise"): "Modul_Übersicht",
}


def compute_sha256(file_path: str) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(1048576), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_slug(text: str, max_len: int = 85) -> str:
    s = clean_text(text)
    s = re.sub(r'[\\/:*?"<>|\[\]#^|,&()+]+', "_", s)
    s = re.sub(r"\s+", "_", s)
    s = re.sub(r"_+", "_", s).strip("._ ")
    if len(s) > max_len:
        s = s[:max_len].rstrip("_")
    return s or "Dokument"


def resolve_modul_for_relpath(rel_path: str) -> str | None:
    parts = rel_path.replace("\\", "/").split("/")
    if len(parts) < 2:
        return None
    pillar, top_dir = parts[0], parts[1]
    if pillar == "03_Bachelor" and top_dir == "Betriebliche Informationssysteme (WI 1)":
        sub = parts[2] if len(parts) > 2 else ""
        if "E-Business" in sub:
            return "Modul_EBusiness"
        if "Management" in sub:
            return "Modul_MBIS"
        return "Modul_EBusiness"
    return ACADEMIC_FOLDER_TO_MODUL.get((pillar, top_dir))


def _peek_book_title(abs_path: str) -> str:
    """Fast metadata title peek for ISBN-named library .epub/.pdf files."""
    ext = os.path.splitext(abs_path)[1].lower()
    try:
        if ext == ".epub":
            import xml.etree.ElementTree as ET
            with zipfile.ZipFile(abs_path, "r") as zf:
                names = zf.namelist()
                nlow = {n.lower(): n for n in names}
                opf = ""
                c_key = "META-INF/container.xml" if "META-INF/container.xml" in names else nlow.get("meta-inf/container.xml", "")
                if c_key:
                    for rf in ET.fromstring(zf.read(c_key)).iter():
                        if rf.tag.endswith("rootfile") and rf.attrib.get("full-path"):
                            opf = rf.attrib["full-path"]
                            break
                if opf and opf in names:
                    for elem in ET.fromstring(zf.read(opf)).iter():
                        if elem.tag.split("}")[-1].lower() == "title" and (elem.text or "").strip():
                            return clean_text(elem.text)
        elif ext == ".pdf":
            import pymupdf
            with pymupdf.open(abs_path) as doc:
                t = (doc.metadata or {}).get("title") or ""
                if t.strip():
                    return clean_text(t)
    except Exception:
        pass
    return ""


LIBRARY_AREA_LABELS = {
    "01_SAP_S4HANA_BTP_CleanCore": "Fachbibliothek – SAP S/4HANA, BTP & ERP",
    "02_IT_Audit_Governance_Compliance": "Fachbibliothek – IT-Audit, Governance & Compliance",
    "03_Enterprise_Architecture_Cloud": "Fachbibliothek – Enterprise Architecture, BPM & Transformation",
    "04_AI_Engineering_Data_Automation": "Fachbibliothek – AI Engineering & Business AI",
    "05_Consulting_BWL_VISMUV": "Fachbibliothek – Consulting, BWL & Management",
    "06_Open_Access_Standards": "Fachbibliothek – Open-Access-Standards & Normen",
    "07_Wirtschaftsinformatik_IT_Grundlagen": "Fachbibliothek – Wirtschaftsinformatik & Software Engineering",
    "08_Unternehmertum_Marketing_VISMUV": "Fachbibliothek – Unternehmertum, Marketing & VISMUV",
}


def _classify_library_category(title: str, rel_path: str) -> tuple[str, str]:
    """Routes library files placed in pillar root to topic subfolders by title keywords."""
    parts = rel_path.replace("\\", "/").split("/")
    if len(parts) > 2:
        slug = safe_slug(parts[1], max_len=38)
        return slug, LIBRARY_AREA_LABELS.get(parts[1], f"Fachbibliothek – {parts[1]}")
    low = title.lower()
    if any(k in low for k in ("artificial intelligence", "künstliche intelligenz", "machine learning", "llm", "business ai", "rag")):
        return "04_AI_Engineering_Data_Automation", "Fachbibliothek – AI Engineering & Business AI"
    if any(k in low for k in ("audit", "iks", "compliance", "governance", "cobit", "dsgvo")):
        return "02_IT_Audit_Governance_Compliance", "Fachbibliothek – IT-Audit, Governance & Compliance"
    if any(k in low for k in ("enterprise architecture", "geschäftsprozess", "process management", "digitale transformation", "digital transformation", "enterprise design")):
        return "03_Enterprise_Architecture_Cloud", "Fachbibliothek – Enterprise Architecture, BPM & Transformation"
    if any(k in low for k in ("sap", "s/4", "s4hana", "abap", "erp", "controlling", "migration", "asset management", "analytics", "business warehouse", "integration suite", "e-learning")):
        return "01_SAP_S4HANA_BTP_CleanCore", "Fachbibliothek – SAP S/4HANA, BTP & ERP"
    return "05_Consulting_BWL_VISMUV", "Fachbibliothek – Consulting, BWL & Management"


def resolve_vault_subfolder_and_hub(rel_path: str, book_title: str = "") -> tuple[str, str, str, str]:
    """Returns (target_subdir_rel, domain, hub_wikilink, area_label) for a workspace rel_path."""
    parts = rel_path.replace("\\", "/").split("/")
    pillar = parts[0]

    if pillar == "00_Aktuelle_Bewerbungsunterlagen":
        return (
            os.path.join(QUELLEN_REL, "00_Aktuelle_Bewerbungsunterlagen"),
            "career-pmo",
            "00_Bewerbungsunterlagen_Master_Volltext",
            "Bewerbungsunterlagen & Zeugnisse",
        )

    if pillar == "04_DC1":
        sub = parts[1] if len(parts) > 1 else ""
        if "ITIL4" in sub:
            return (
                os.path.join(QUELLEN_REL, "04_DC1", "01_ITIL4_INOC"),
                "datacenter-operations",
                "DC1_ITIL4_Service_Operations",
                "Datacenter One – ITIL 4 & INOC",
            )
        return (
            os.path.join(QUELLEN_REL, "04_DC1", "02_Projekte_HLM_Carrier"),
            "datacenter-operations",
            "DC1_Hardware_Lifecycle_Management",
            "Datacenter One – HLM & Carriermanagement",
        )

    if pillar == "01_SSB":
        sub1 = parts[1] if len(parts) > 1 else ""
        sub2 = parts[2] if len(parts) > 2 else ""
        if "01_Gesamtprojekt" in sub1:
            return (
                os.path.join(QUELLEN_REL, "01_SSB", "01_PMO_Governance"),
                "sap-transformation",
                "SSB_Grossprojekt_SAP4SSB",
                "SSB PMO & Gesamtprojekt-Governance",
            )
        if "02_Teilprojekte" in sub1:
            tp_map = {
                "TP1": ("02_TP1_Change", "TP1_Change_Management_People_Plan", "SSB TP1 Change Management"),
                "TP2": ("03_TP2_Kaufmaennisch", "TP2_Kaufmaennische_Prozesse_Plan", "SSB TP2 Kaufmännische Prozesse"),
                "TP3": ("04_TP3_Instandhaltung", "TP3_Technische_Prozesse_Instandhaltung_Plan", "SSB TP3 Instandhaltung"),
                "TP4": ("05_TP4_IT_Basis", "TP4_IT_Unterstuetzung_Integration_Plan", "SSB TP4 IT & Basis"),
                "TP5": ("06_TP5_Gesamtsteuerung", "TP5_Gesamtsteuerung_PMO_Betriebsvereinbarung_Plan", "SSB TP5 Gesamtsteuerung"),
            }
            for prefix, (folder, hub, label) in tp_map.items():
                if sub2.startswith(prefix):
                    return (os.path.join(QUELLEN_REL, "01_SSB", folder), "sap-transformation", hub, label)
            return (
                os.path.join(QUELLEN_REL, "01_SSB", "02_Teilprojekte"),
                "sap-transformation",
                "SSB_Grossprojekt_SAP4SSB",
                "SSB Teilprojekte",
            )
        if "03_Fachstreams" in sub1:
            stream_slug = safe_slug(sub2 or "Allgemein", max_len=35)
            return (
                os.path.join(QUELLEN_REL, "01_SSB", "07_Fachstreams", stream_slug),
                "sap-transformation",
                "MOC_Kaufmaennische_Prozesse",
                f"SSB Fachstream – {sub2 or 'Allgemein'}",
            )
        return (
            os.path.join(QUELLEN_REL, "01_SSB", "08_Architektur_Tools"),
            "sap-transformation",
            "Toolkette_Signavio_CALM_EnableNow",
            "SSB Architektur, Methoden & Tools",
        )

    if pillar == "05_Fachliteratur_Bibliothek":
        cat_slug, area_label = _classify_library_category(book_title or os.path.basename(rel_path), rel_path)
        return (
            os.path.join(QUELLEN_REL, "05_Bibliothek", cat_slug),
            "reference-library",
            "05_Bibliothek_Quellen_Index",
            area_label,
        )

    # Academic pillars: 02_Master / 03_Bachelor
    modul_note = resolve_modul_for_relpath(rel_path) or "Modul_Übersicht"
    top_dir = parts[1] if len(parts) > 1 else "Allgemein"
    if pillar == "03_Bachelor" and top_dir == "Betriebliche Informationssysteme (WI 1)" and len(parts) > 2:
        folder_slug = safe_slug(parts[2], max_len=38)
    else:
        folder_slug = safe_slug(top_dir, max_len=38)

    return (
        os.path.join(QUELLEN_REL, pillar, folder_slug),
        "academic-curriculum",
        modul_note,
        f"{pillar.replace('_', ' ')} – {top_dir}",
    )


def _canonical_path_priority(rel_path: str) -> tuple[int, int, str]:
    """Lower tuple score wins as the canonical file inside a SHA-256 duplicate group."""
    norm = rel_path.replace("\\", "/")
    pillar = norm.split("/")[0]
    pillar_rank = {
        "04_DC1": 0,
        "01_SSB": 1,
        "02_Master": 2,
        "03_Bachelor": 3,
        "00_Aktuelle_Bewerbungsunterlagen": 4,
        "05_Fachliteratur_Bibliothek": 5,
    }.get(pillar, 9)

    fname = os.path.basename(norm).lower()
    if pillar == "00_Aktuelle_Bewerbungsunterlagen" and any(
        k in fname for k in ("lebenslauf", "zeugnis", "bewerbungsverlauf")
    ):
        pillar_rank = 0

    penalty = 0
    low = norm.lower()
    for bad in ("backup", "upload-ordner", "erstversuch", "_alt", " (1)", " (2)", "copy"):
        if bad in low:
            penalty += 2
    if "01_erfolgreiche" in low or "02_schmalz_praxisprojekt" in low or "abgabe_" in low:
        penalty -= 1
    return (pillar_rank, penalty, len(norm), norm.lower())


_NOTE_HEADER_END_MARKER = "\n> - **Kanonische Verknüpfung:**"


def _split_v2_note_header_body(note_text: str) -> tuple[str, str] | None:
    """Splits a rendered V2 note into (header_including_hr, raw_body)."""
    idx = note_text.find(_NOTE_HEADER_END_MARKER)
    if idx == -1:
        return None
    sep = note_text.find("\n---\n\n", idx)
    if sep == -1:
        return None
    split_pos = sep + len("\n---\n\n")
    return note_text[:split_pos], note_text[split_pos:]


def _compute_body_norm_hash(body_text: str) -> str:
    """Computes a canonical normalized-prose SHA-256 ignoring page break headings and whitespace."""
    if not body_text:
        return ""
    stripped = re.sub(r"^### Seite \d+(?: \*\(OCR\)\*)?$", "", body_text, flags=re.MULTILINE)
    norm = re.sub(r"\s+", " ", stripped).strip().lower()
    if not norm:
        return ""
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()


def _pptx_has_diagrams(file_path: str) -> bool:
    """Checks quickly whether a PPTX ZIP archive contains SmartArt diagram XML files."""
    try:
        with zipfile.ZipFile(file_path) as zf:
            return any(n.startswith("ppt/diagrams/data") and n.endswith(".xml") for n in zf.namelist())
    except Exception:
        return False


def _sampled_shingle_set(body_text: str, shingle_size: int = 5, max_samples: int = 450) -> set[tuple[str, ...]]:
    """Extracts evenly-spaced 5-word shingles across the full length of large documents."""
    words = re.findall(r"[a-z0-9äöüß]+", body_text.lower())
    n = len(words)
    if n < shingle_size + 20:
        return set()
    total = n - shingle_size + 1
    step = max(1, total // max_samples)
    return {tuple(words[i : i + shingle_size]) for i in range(0, total, step)}


def _canonical_content_priority(item: dict[str, Any]) -> tuple[int, int, int, str]:
    """Ranks candidate canonical files inside an identical/cloned content group (lower wins)."""
    base_rank = _canonical_path_priority(item["primary_rel"])
    stem = os.path.splitext(os.path.basename(item["primary_rel"]))[0].lower()
    name_penalty = 0
    for noisy in ("kopie", "copy", " (1)", " (2)", " (3)", " (4)", "_v0", "backup", "_alt", "mask"):
        if noisy in stem:
            name_penalty += 3
    if re.fullmatch(r"[a-z]+_?\d{1,2}", stem) or len(stem) <= 10:
        name_penalty += 2
    if re.search(r"et[ _]al|20\d{2}|schoormann|dietvorst|readiness|servicebeschreibung", stem):
        name_penalty -= 1
    return (base_rank[0], base_rank[1] + name_penalty, base_rank[2], base_rank[3])


def _merge_loser_into_winner(winner: dict[str, Any], loser: dict[str, Any]) -> None:
    merged_dups = list(dict.fromkeys(winner["duplicate_rels"] + [loser["primary_rel"]] + loser["duplicate_rels"]))
    winner["duplicate_rels"] = [d for d in merged_dups if d != winner["primary_rel"]]
    winner["all_rels"] = list(dict.fromkeys([winner["primary_rel"]] + winner["duplicate_rels"]))
    winner["ref_modules"] = sorted(set(winner["ref_modules"]) | set(loser["ref_modules"]))
    for rel_p in loser.get("all_rels", []):
        mod = resolve_modul_for_relpath(rel_p)
        if mod and mod not in winner["ref_modules"]:
            winner["ref_modules"] = sorted(set(winner["ref_modules"]) | {mod})


def _sync_winner_note_metadata(winner: dict[str, Any]) -> None:
    """Updates frontmatter duplicate_paths and canonical hub links in winner note after merge."""
    target_abs = os.path.join(VAULT_DIR, winner["vault_rel"])
    if not os.path.exists(target_abs):
        return
    with open(target_abs, "r", encoding="utf-8", errors="ignore") as f:
        raw = f.read()
    split = _split_v2_note_header_body(raw)
    if split is None:
        return
    header, body = split

    # Rebuild duplicate_paths in YAML cleanly
    header_clean = re.sub(r"\nduplicate_paths:\n(?:  - .*\n?)+", "\n", header)
    if winner["duplicate_rels"]:
        dup_lines = "\n".join(f'  - "{_yaml_escape(d)}"' for d in winner["duplicate_rels"])
        header_clean = header_clean.replace('\nstatus: extracted-v2', f'\nstatus: extracted-v2\nduplicate_paths:\n{dup_lines}', 1)

    related_hubs = [f"[[{winner['hub_link']}]]"] + [
        f"[[{m}]]" for m in winner["ref_modules"] if m != winner["hub_link"]
    ]
    related_str = " • ".join(related_hubs)
    dup_note = ""
    if winner["duplicate_rels"]:
        shown = ", ".join(f"`{d}`" for d in winner["duplicate_rels"][:8])
        extra = f" (+{len(winner['duplicate_rels']) - 8} weitere)" if len(winner["duplicate_rels"]) > 8 else ""
        dup_note = f"\n> - **SHA-256 / Inhalts-Dedupliziert:** Identische Kopien in {shown}{extra} verweisen auf diese eine kanonische Datei."

    idx_k = header_clean.find("\n> - **Kanonische Verknüpfung:**")
    if idx_k == -1:
        return
    new_header = (
        header_clean[:idx_k]
        + f"\n> - **Kanonische Verknüpfung:** {related_str} • [[00_Quellen_Index|🗄️ Quellen-Index]]{dup_note}"
        + "\n\n---\n\n"
    )
    _write_if_changed(target_abs, new_header + body)


def deduplicate_by_normalized_content(
    canonical_items: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]], int, int]:
    """Collapses exact normalized-text duplicates and verified mega near-clones (>=10k words)."""
    # 1. Exact normalized prose hash grouping (words >= 10)
    by_norm_hash: dict[str, list[dict[str, Any]]] = defaultdict(list)
    unique_pass1: list[dict[str, Any]] = []
    exact_collapsed = 0

    for it in canonical_items:
        h = it.get("_v2_body_norm_sha", "")
        if h and it.get("_v2_words", 0) >= 10:
            by_norm_hash[h].append(it)
        else:
            unique_pass1.append(it)

    for h, grp in by_norm_hash.items():
        if len(grp) == 1:
            unique_pass1.append(grp[0])
            continue
        grp_sorted = sorted(grp, key=_canonical_content_priority)
        winner = grp_sorted[0]
        for loser in grp_sorted[1:]:
            _merge_loser_into_winner(winner, loser)
            exact_collapsed += 1
        winner["_meta_dirty"] = True
        unique_pass1.append(winner)

    # 2. Conservative mega near-clone pass for untouched annotated textbooks/backups (>=10,000 words)
    mega_items = [it for it in unique_pass1 if it.get("_v2_words", 0) >= 10000]
    mega_items.sort(key=lambda x: -x.get("_v2_words", 0))
    shingles_by_sha: dict[str, set[tuple[str, ...]]] = {}
    absorbed_shas: set[str] = set()
    clone_collapsed = 0

    def _get_shingles(it: dict[str, Any]) -> set[tuple[str, ...]]:
        sha = it["sha256"]
        if sha not in shingles_by_sha:
            target_abs = os.path.join(VAULT_DIR, it["vault_rel"])
            txt = ""
            if os.path.exists(target_abs):
                with open(target_abs, "r", encoding="utf-8", errors="ignore") as f:
                    split = _split_v2_note_header_body(f.read())
                    txt = split[1] if split else ""
            shingles_by_sha[sha] = _sampled_shingle_set(txt)
        return shingles_by_sha[sha]

    def _date_and_version_sig(rel_p: str) -> tuple[tuple[str, ...], str]:
        fn = os.path.splitext(os.path.basename(rel_p))[0].lower()
        years = tuple(re.findall(r"20\d{2}(?:\d{4})?", fn))
        # Distinguish student-named or distinct metric reports cleanly
        ver = "".join(re.findall(r"v\d+(?:\.\d+)?", fn))
        return years, ver

    # Compare only pairs within 1.5% word-count tolerance
    for i in range(len(mega_items)):
        a = mega_items[i]
        if a["sha256"] in absorbed_shas:
            continue
        wa = a.get("_v2_words", 0)
        sig_a = _date_and_version_sig(a["primary_rel"])
        cluster = [a]
        for j in range(i + 1, len(mega_items)):
            b = mega_items[j]
            if b["sha256"] in absorbed_shas:
                continue
            wb = b.get("_v2_words", 0)
            if wb < wa * 0.985:
                break
            sig_b = _date_and_version_sig(b["primary_rel"])
            if sig_a != sig_b:
                continue
            sa = _get_shingles(a)
            sb = _get_shingles(b)
            if not sa or not sb:
                continue
            jac = len(sa & sb) / max(1, len(sa | sb))
            stem_a = re.sub(r"[^a-z0-9]+", " ", os.path.splitext(os.path.basename(a["primary_rel"]))[0].lower()).strip()
            stem_b = re.sub(r"[^a-z0-9]+", " ", os.path.splitext(os.path.basename(b["primary_rel"]))[0].lower()).strip()
            same_base_stem = bool(stem_a and stem_a == stem_b)
            if jac >= 0.965 or (same_base_stem and jac >= 0.92 and wb >= wa * 0.99):
                cluster.append(b)
        if len(cluster) > 1:
            cluster_sorted = sorted(cluster, key=_canonical_content_priority)
            winner = cluster_sorted[0]
            for other in cluster_sorted:
                if other["sha256"] != winner["sha256"]:
                    absorbed_shas.add(other["sha256"])
                    _merge_loser_into_winner(winner, other)
                    clone_collapsed += 1
            winner["_meta_dirty"] = True

    final_items = [it for it in unique_pass1 if it["sha256"] not in absorbed_shas]
    final_items.sort(key=lambda x: (-x["size_bytes"], x["primary_rel"].lower()))

    for it in final_items:
        if it.pop("_meta_dirty", False):
            _sync_winner_note_metadata(it)

    new_modul_links: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for it in final_items:
        for mod in it["ref_modules"]:
            new_modul_links[mod].append(it)

    return final_items, new_modul_links, exact_collapsed, clone_collapsed


def discover_unique_documents() -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]], dict[str, Any]]:
    """Walks all 5 pillars, filters junk/secrets, and deduplicates identically hashed files."""
    sha_groups: dict[str, list[str]] = defaultdict(list)
    total_raw_docs = 0
    skipped_empty = 0

    for pillar in PILLARS:
        root_dir = os.path.join(BASE_DIR, pillar)
        if not os.path.exists(root_dir):
            continue
        for root, dirs, files in os.walk(root_dir):
            dirs[:] = sorted(
                d for d in dirs if d not in SKIP_DIR_NAMES and not d.startswith(".")
            )
            rel_root = os.path.relpath(root, BASE_DIR)
            if any(sub in rel_root for sub in SKIP_REL_SUBSTRINGS):
                continue

            file_set = set(files)
            for fname in sorted(files):
                if fname.startswith(("~$", "._")) or fname in ("Thumbs.db", ".DS_Store", "00_UB_Stuttgart_Literatur_Checkliste.md"):
                    continue
                ext = os.path.splitext(fname)[1].lower()
                if ext not in ALLOWED_EXTENSIONS:
                    continue
                if pillar == "05_Fachliteratur_Bibliothek" and ext == ".pdf":
                    epub_sibling = os.path.splitext(fname)[0] + ".epub"
                    if epub_sibling in file_set:
                        continue
                fpath = os.path.join(root, fname)
                if not os.path.isfile(fpath):
                    continue
                if os.path.getsize(fpath) == 0:
                    skipped_empty += 1
                    continue

                total_raw_docs += 1
                sha = compute_sha256(fpath)
                sha_groups[sha].append(os.path.relpath(fpath, BASE_DIR))

    canonical_items: list[dict[str, Any]] = []
    modul_links_index: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for sha, rel_list in sha_groups.items():
        ordered = sorted(rel_list, key=_canonical_path_priority)
        primary_rel = ordered[0]
        dup_rels = ordered[1:]
        primary_abs = os.path.join(BASE_DIR, primary_rel)
        book_title = ""
        if primary_rel.startswith("05_Fachliteratur_Bibliothek"):
            book_title = _peek_book_title(primary_abs)
        target_subdir, domain, hub_link, area_label = resolve_vault_subfolder_and_hub(primary_rel, book_title=book_title)

        ref_modules: set[str] = set()
        for rel_p in ordered:
            m_note = resolve_modul_for_relpath(rel_p)
            if m_note:
                ref_modules.add(m_note)

        item = {
            "sha256": sha,
            "primary_rel": primary_rel,
            "primary_abs": primary_abs,
            "duplicate_rels": dup_rels,
            "all_rels": ordered,
            "size_bytes": os.path.getsize(primary_abs),
            "target_subdir": target_subdir,
            "domain": domain,
            "hub_link": hub_link,
            "area_label": area_label,
            "book_title": book_title,
            "ref_modules": sorted(ref_modules),
        }
        canonical_items.append(item)

    # Seed globally unique basenames excluding all existing Layer-1 notes
    used_basenames: set[str] = {
        "00_quellen_index",
        "01_ssb_quellen_index",
        "02_master_quellen_index",
        "03_bachelor_quellen_index",
        "04_dc1_quellen_index",
        "05_bibliothek_quellen_index",
    }
    for root, dirs, files in os.walk(VAULT_DIR):
        dirs[:] = [d for d in dirs if d not in (".obsidian", ".trash", "05_Archiv")]
        for fn in files:
            if fn.endswith(".md"):
                used_basenames.add(os.path.splitext(fn)[0].lower())

    canonical_items.sort(key=lambda x: (-x["size_bytes"], x["primary_rel"].lower()))

    # Deterministic unique basenames in primary_rel alphabetical pass for stability
    for item in sorted(canonical_items, key=lambda x: x["primary_rel"].lower()):
        stem = os.path.splitext(os.path.basename(item["primary_rel"]))[0]
        ext_tag = os.path.splitext(item["primary_rel"])[1].lstrip(".").lower()
        if item.get("book_title") and re.match(r"^[\d\-Xx]{8,}$", stem):
            isbn_tail = re.sub(r"[^0-9Xx]", "", stem)[-6:]
            title_slug = safe_slug(item["book_title"], max_len=50)
            base = f"{title_slug}_{isbn_tail}" if isbn_tail else title_slug
        else:
            base = safe_slug(stem, max_len=62)
        cand = base
        if cand.lower() in used_basenames:
            cand = f"{base[:56]}_{ext_tag}"
        if cand.lower() in used_basenames:
            cand = f"{base[:49]}_{ext_tag}_{item['sha256'][:6]}"
        used_basenames.add(cand.lower())
        item["note_basename"] = cand
        item["vault_rel"] = os.path.join(item["target_subdir"], f"{cand}.md")

        for mod in item["ref_modules"]:
            modul_links_index[mod].append(item)

    # Re-sort largest files first for optimal multiprocessing LPT load balancing
    canonical_items.sort(key=lambda x: (-x["size_bytes"], x["primary_rel"].lower()))

    stats = {
        "total_eligible_files": total_raw_docs,
        "unique_sha256_docs": len(canonical_items),
        "duplicates_collapsed": total_raw_docs - len(canonical_items),
        "empty_files_skipped": skipped_empty,
    }
    return canonical_items, modul_links_index, stats


def _extract_worker(args: tuple[dict[str, Any], bool]) -> dict[str, Any]:
    """Multiprocess worker extracting one source document with optional OCR."""
    task, enable_ocr = args
    res = extract_document_v2(task["primary_abs"], enable_ocr=enable_ocr)
    return {"sha256": task["sha256"], "res": res}


def _yaml_escape(val: str) -> str:
    return val.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ").strip()


def render_source_note(item: dict[str, Any], res: dict[str, Any], today: str) -> str:
    """Formats an extracted source document as a single clean YAML-compliant Obsidian note."""
    fname = os.path.basename(item["primary_rel"])
    stem = os.path.splitext(fname)[0]
    title_clean = clean_text(res.get("meta", {}).get("title") or stem.replace("_", " "))
    if len(title_clean) < 3 or len(title_clean) > 130:
        title_clean = clean_text(stem.replace("_", " "))[:120]

    file_url = "file:///" + item["primary_abs"].replace("\\", "/").replace(" ", "%20")
    dup_lines = "\n".join(f'  - "{_yaml_escape(d)}"' for d in item["duplicate_rels"])
    dup_yaml = f"\nduplicate_paths:\n{dup_lines}" if item["duplicate_rels"] else ""

    related_hubs = [f"[[{item['hub_link']}]]"]
    for m in item["ref_modules"]:
        if m != item["hub_link"]:
            related_hubs.append(f"[[{m}]]")
    related_str = " • ".join(related_hubs)

    pillar = item["primary_rel"].split(os.sep)[0]
    doc_type_val = "reference-book" if pillar == "05_Fachliteratur_Bibliothek" else "source-fulltext"
    summary_txt = f"Kanonischer V2-Volltext von {fname} ({res['format'].upper()}, {res['words']:,} Wörter, {res['pages_or_units']} Einheiten) aus {item['area_label']}."
    fm = f"""---
id: "src-{item['sha256'][:12]}"
title: "{_yaml_escape(title_clean)}"
type: {doc_type_val}
domain: {item['domain']}
summary: "{_yaml_escape(summary_txt)}"
pillar: "{_yaml_escape(pillar)}"
area: "{_yaml_escape(item['area_label'])}"
source_file: "{_yaml_escape(item['primary_rel'])}"
source_format: "{res['format']}"
sha256: "{item['sha256']}"
pages_or_units: {res['pages_or_units']}
ocr_pages: {res['ocr_pages']}
word_count: {res['words']}
status: extracted-v2
last_updated: "{today}"{dup_yaml}
tags:
  - quelle_volltext
  - "{safe_slug(pillar, 40).lower()}"
  - "{res['format']}"
---"""

    dup_note = ""
    if item["duplicate_rels"]:
        dup_list_md = ", ".join(f"`{d}`" for d in item["duplicate_rels"])
        dup_note = f"\n> - **SHA-256 Dedupliziert:** Identische Kopien in {dup_list_md} verweisen auf diese eine kanonische Datei."

    body_txt = res["text"] if res.get("success") else f"*(Extraktion ohne lesbaren Text: {res.get('error') or 'Leeres visuelles Artefakt'})*"
    # Guard AST Single-H1 invariant: neutralize any bare "# comment" lines outside fenced code blocks
    if body_txt and "\n#" in f"\n{body_txt}":
        parts = re.split(r"(```.*?```)", body_txt, flags=re.DOTALL)
        for i in range(0, len(parts), 2):
            parts[i] = re.sub(r"^#[ \t]+(\S)", r"    # \1", parts[i], flags=re.MULTILINE)
        body_txt = "".join(parts)

    return f"""{fm}

# 📄 {title_clean}

> [!INFO] **Quellen-Metadaten (Obsidian V2 Volltext-Extraktion)**
> - **Originaldatei:** [{fname}]({file_url}) (`{res['format'].upper()}`)
> - **Workspace-Pfad:** `{item['primary_rel']}`
> - **Umfang:** **{res['words']:,} Wörter** | **{res['pages_or_units']} Einheiten/Seiten** | **OCR-Seiten:** `{res['ocr_pages']}` | **Tabellen:** `{res['tables_count']}`
> - **Kanonische Verknüpfung:** {related_str} • [[00_Quellen_Index|🗄️ Quellen-Index]]{dup_note}

---

{body_txt}
"""


def _write_if_changed(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            if f.read() == content:
                return
    with open(path, "w", encoding="utf-8", errors="replace") as f:
        f.write(content)


def build_v2_indexes(canonical_items: list[dict[str, Any]], stats: dict[str, Any], today: str) -> None:
    """Creates master and pillar-level navigation hubs inside 05_Archiv/Volltexte_Quellen/."""
    by_pillar: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for it in canonical_items:
        by_pillar[it["primary_rel"].split(os.sep)[0]].append(it)

    pillar_specs = [
        ("01_SSB_Quellen_Index", "🚆 SSB AG S/4HANA Transformation (Volltext-Quellen)", "sap-transformation", ["01_SSB"], "[[SSB_Grossprojekt_SAP4SSB]]"),
        ("02_Master_Quellen_Index", "🎓 M.Sc. Wirtschaftsinformatik (Volltext-Quellen)", "academic-curriculum", ["02_Master"], "[[Modul_Übersicht]]"),
        ("03_Bachelor_Quellen_Index", "🏛️ B.Sc. Wirtschaftsinformatik (Volltext-Quellen)", "academic-curriculum", ["03_Bachelor"], "[[Modul_Übersicht]]"),
        ("04_DC1_Quellen_Index", "🏢 Datacenter One & Bewerbungsunterlagen (Volltext-Quellen)", "datacenter-operations", ["04_DC1", "00_Aktuelle_Bewerbungsunterlagen"], "[[DC1_ITIL4_Service_Operations]]"),
        ("05_Bibliothek_Quellen_Index", "📚 Wissenschaftliche Fachliteratur & Standards (Bibliothek)", "reference-library", ["05_Fachliteratur_Bibliothek"], "[[00_INDEX]]"),
    ]

    for idx_name, idx_title, dom, pil_keys, parent_hub in pillar_specs:
        items = []
        for k in pil_keys:
            items.extend(by_pillar.get(k, []))
        by_area: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for it in items:
            by_area[it["area_label"]].append(it)

        sec_blocks: list[str] = []
        for area in sorted(by_area):
            area_items = sorted(by_area[area], key=lambda x: (x.get("book_title") or os.path.basename(x["primary_rel"])).lower())
            lines = [f"## {area} ({len(area_items)} Dokumente)\n"]
            for it in area_items:
                fn = os.path.basename(it["primary_rel"])
                disp = it.get("book_title") or fn
                fn_note = f"`{fn}` • " if it.get("book_title") else ""
                lines.append(f"- [[{it['note_basename']}|{disp}]] ({fn_note}`{it.get('_v2_fmt', '').upper()}` • {it.get('_v2_words', 0):,} Wörter)")
            sec_blocks.append("\n".join(lines))

        idx_md = f"""---
id: "{idx_name.lower()}"
title: "{idx_title}"
type: moc
domain: {dom}
status: evergreen
summary: "Kanonischer V2 Volltext-Index ohne Duplikate ({len(items)} einzigartige Originaldokumente)."
last_updated: "{today}"
tags:
  - quellen_index
  - moc
  - data_lake
---

# {idx_title}

> [!ABSTRACT] **60-Sekunden-Essenz**
> - **Bestand:** **{len(items)} kanonische Originaldokumente** (1 Datei = 1 vollständige Markdown-Notiz, SHA-256 dedupliziert).
> - **Navigation:** [[00_Quellen_Index|🗄️ Gesamt-Index]] • {parent_hub} • [[00_INDEX|🧠 Master Hub]]

---

""" + "\n\n".join(sec_blocks) + "\n"
        _write_if_changed(os.path.join(QUELLEN_DIR, f"{idx_name}.md"), idx_md)

    master_idx = f"""---
id: quellen-index-v2
title: "Volltext Quellen-Archiv Index V2 (Layer 2 | Dedupliziert)"
type: moc
domain: system-governance
status: evergreen
summary: "Gesamtindex für {stats['unique_sha256_docs']} einzigartige extrahierte Originaldokumente in 05_Archiv/Volltexte_Quellen/ (0 Splits, {stats['duplicates_collapsed']} Duplikate bereinigt)."
last_updated: "{today}"
tags:
  - data_lake
  - archive
  - rag_corpus
  - moc
---

# 🗄️ Volltext Quellen-Archiv V2 (Schicht 2 – Single Source of Truth)

> [!ABSTRACT] **60-Sekunden-Essenz: Verifizierte V2-Extraktion ohne Redundanzen**
> - **Originaldateien gescannt:** `{stats['total_eligible_files']:,}` zulässige Dokumente
> - **Kanonische Volltext-Notizen (SHA-256 unique):** **`{stats['unique_sha256_docs']:,}` Markdown-Dateien** (1 Quelldokument = 1 vollständige Markdown-Notiz, ohne `Teil_01`-Zerstückelung)
> - **Automatisch bereinigte Duplikate:** `{stats['duplicates_collapsed']:,}` identische Datei-Kopien
> - **Zurück:** [[00_INDEX|🧠 Master Knowledge Hub (Schicht 1 Vordergrund)]]

---

## 🧭 Teil-Indizes nach Wissenssäulen
- [[01_SSB_Quellen_Index|🚆 Säule 01: SSB AG S/4HANA Transformation ({len(by_pillar.get('01_SSB', [])):,} Dokumente)]]
- [[02_Master_Quellen_Index|🎓 Säule 02: M.Sc. Wirtschaftsinformatik ({len(by_pillar.get('02_Master', [])):,} Dokumente)]]
- [[03_Bachelor_Quellen_Index|🏛️ Säule 03: B.Sc. Wirtschaftsinformatik ({len(by_pillar.get('03_Bachelor', [])):,} Dokumente)]]
- [[04_DC1_Quellen_Index|🏢 Säule 04 & 00: Datacenter One & Bewerbungsunterlagen ({len(by_pillar.get('04_DC1', [])) + len(by_pillar.get('00_Aktuelle_Bewerbungsunterlagen', [])):,} Dokumente)]]
- [[05_Bibliothek_Quellen_Index|📚 Säule 05: Fachliteratur-Bibliothek & E-Books ({len(by_pillar.get('05_Fachliteratur_Bibliothek', [])):,} Werke)]]
"""
    _write_if_changed(os.path.join(QUELLEN_DIR, "00_Quellen_Index.md"), master_idx)


def _clean_layer1_text_glitches(text: str, link_replacements: dict[str, str]) -> str:
    """Fixes nested wikilinks, stale Desktop/Wissensdatenbank paths, and retired DataLake links."""
    out = text.replace("Desktop/Wissensdatenbank", "Desktop/SSB Dateien").replace(
        "Desktop\\Wissensdatenbank", "Desktop\\SSB Dateien"
    )
    out = out.replace("Desktop/SSB%20Dateien", "Desktop/SSB%20Dateien")

    # Fix doubly-nested wikilinks like [[Target|Prefix [[Target|Inner]] Suffix]]
    for _ in range(3):
        m_exist = re.search(r"\[\[([^\|\]]+)\|([^\[\]]*?)\[\[[^\|\]]+\|([^\]]+)\]\]([^\]]*?)\]\]", out)
        if not m_exist:
            break
        out = re.sub(
            r"\[\[([^\|\]]+)\|([^\[\]]*?)\[\[[^\|\]]+\|([^\]]+)\]\]([^\]]*?)\]\]",
            r"[[\1|\2\3\4]]",
            out,
        )

    # Fix broken double-nested markdown file URL [name.pptx](file:///.../[name.pptx](file:///...))
    out = re.sub(
        r"\[([^\]]+)\]\(file:///[^()\s]*?\[\1\]\((file:///[^)]+)\)\)",
        r"[\1](\2)",
        out,
    )

    def _replace_wikilink(match: re.Match[str]) -> str:
        raw = match.group(1).strip()
        if "|" in raw:
            tgt, alias = raw.split("|", 1)
        else:
            tgt, alias = raw, None
        anchor = ""
        if "#" in tgt:
            tgt, anchor = tgt.split("#", 1)
            anchor = "#" + anchor.strip()
        base = os.path.splitext(os.path.basename(tgt.strip()))[0].lower()
        if base in link_replacements:
            new_base = link_replacements[base]
            return f"[[{new_base}{anchor}|{alias}]]" if alias else f"[[{new_base}{anchor}]]"
        return match.group(0)

    return re.sub(r"\[\[(.*?)\]\]", _replace_wikilink, out)


_MODUL_BUCKET_META: list[tuple[str, str]] = [
    ("vorlesung", "### 🖥️ Vorlesungsfolien & Skripte"),
    ("uebung", "### 📝 Übungen, Tutorien & Aufgaben"),
    ("projekt", "### 📄 Ausarbeitungen, Projekte & Vorträge"),
    ("literatur", "### 📚 Wissenschaftliche Literatur & Quellen"),
    ("pruefung", "### 🎓 Prüfungsvorbereitung & Organisation"),
    ("sonstiges", "### 📁 Weitere Modulunterlagen"),
]


def _classify_modul_source(rel_path: str) -> str:
    """Categorizes a module source document using filename cues first, then unambiguous folder names."""
    norm = rel_path.replace("\\", "/").lower()
    fname = os.path.basename(norm)
    parent = os.path.dirname(norm)

    if re.search(r"\b(altklausur\w*|klausur\w*|pr[uü]fung\w*|exam\w*|zusammenfassung\w*|zsmf|cheatsheet|cheat[_ -]?sheet|notenspiegel|modulhandbuch|syllabus)\b", fname) or re.search(r"/(?:[^/]*(?:altklausur|klausur|pr[uü]fungs|exam|studienorganisation|nachweise)[^/]*)(?:/|$)", parent):
        return "pruefung"
    if re.search(r"(vorlesung|folien|slides?|lecture|skript|script|kapitel|chapter|\bvl[_-]?\d+|ds_vl\d+|\blec[_-]?\d+)", fname):
        return "vorlesung"
    if re.search(r"([uü]bung|tutori|exercise|assignment|aufgabe|l[oö]sung|solution|praktikum|workshop|\btask\b|\blab\b|ds_ue\d+|musterl[oö]sung|\bue[_-]?\d+)", fname) or re.search(r"/(?:[^/]*(?:uebung|[uü]bung|tutori|assignment|exercise|praktikum)[^/]*)(?:/|$)", parent) and "vorlesung" not in parent:
        return "uebung"
    if re.search(r"(ausarbeitung|seminararbeit|bachelorarbeit|masterarbeit|thesis|praxisprojekt|projekt|project|pitch|abgabe|vortrag|pr[aä]sentation|poster|kickoff|followup|schmalz|bilanzpflege)", fname) or fname.endswith(".ps1") or re.search(r"/(?:[^/]*(?:praxisprojekt|ausarbeitung|seminararbeit|prototyp|abgabe|projekt)[^/]*)(?:/|$)", parent):
        return "projekt"
    if re.search(r"/(?:[^/]*(?:literatur|paper|journal|quellen)[^/]*)(?:/|$)", parent) or re.search(r"(et[_ ]al|springer|arxiv|ieee| - (?:19|20)\d{2} - )", fname) or fname.endswith(".bib"):
        return "literatur"
    if "vorlesung" in parent:
        return "vorlesung"
    if "uebung" in parent or "übung" in parent:
        return "uebung"
    return "sonstiges"


def migrate_layer1_and_cleanup(
    canonical_items: list[dict[str, Any]],
    modul_links_index: dict[str, list[dict[str, Any]]],
    stats: dict[str, Any],
    today: str,
) -> None:
    """Preserves all Layer-1 curation, builds categorized Modul V2 links, and trims truncated dumps."""
    # Look up canonical V2 basenames for specific documents formerly referenced as DataLake monoliths
    by_filename_lower = {
        os.path.basename(it["primary_rel"]).lower(): it["note_basename"]
        for it in canonical_items
    }
    cm_v2_note = by_filename_lower.get("cm_ins_inoc_projekt_vim.docx", "04_DC1_Quellen_Index")
    link_replacements = {
        "00_datalake_index": "00_Quellen_Index",
        "ssb_solution_design_volltext": by_filename_lower.get("ssb lösungsdesign dokument.docx", "SSB_Solution_Design_FI_CO"),
        "ssb_migration_volltext": by_filename_lower.get("migrationskonzept v0 1 2025_04_28.docx", "SSB_Datenmigration_LTMC_CVI"),
        "ssb_tool_governance_calm_enablenow_volltext": by_filename_lower.get("20251107_sap_calm_how2handle_quickguide.docx", "SSB_Tool_Governance_Signavio_CALM"),
        "ssb_tp5_gesamtsteuerung_architektur_pmo_volltext": "TP5_Gesamtsteuerung_PMO_Betriebsvereinbarung_Plan",
        "ssb_fachstream_grants_management_volltext": "Stream_Grants_Management_Drittmittel_LGVFG",
        "dc1_carriermanagement_sops_togaf_volltext": cm_v2_note,
        "dc1_itil4_incident_reports_postmortems_volltext": "04_DC1_Quellen_Index",
        "master_cloud_computing_service_management_volltext": "Modul_Cloud_Computing",
    }

    # 1. Clean 47 Modul_*.md files (preserve curated top, strip raw Folien/Übungen dumps, add grouped V2 links)
    p2_dir = os.path.join(VAULT_DIR, "02_Wirtschaftsinformatik_300ECTS")
    split_markers = (
        "\n## 🖥️ Vorlesungsfolien & Lehrinhalte (Volltext-Transkript)",
        "\n## 📝 Übungen, Fallstudien & Aufgabenblätter (Volltext-Transkript)",
        "\n## 📚 Originaldokumente & Volltexte (V2 Quellen-Index)",
    )
    for fn in sorted(os.listdir(p2_dir)):
        if not fn.endswith(".md"):
            continue
        fp = os.path.join(p2_dir, fn)
        with open(fp, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        if fn.startswith("Modul_") and fn != "Modul_Übersicht.md":
            cut_pos = len(content)
            for mk in split_markers:
                idx = content.find(mk)
                if idx != -1 and idx < cut_pos:
                    cut_pos = idx
            preserved = content[:cut_pos].rstrip()
            preserved = re.sub(r"\n---\s*$", "", preserved).rstrip()

            modul_key = os.path.splitext(fn)[0]
            linked_docs = sorted(
                modul_links_index.get(modul_key, []),
                key=lambda x: x["primary_rel"].lower(),
            )
            if linked_docs:
                grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
                for it in linked_docs:
                    grouped[_classify_modul_source(it["primary_rel"])].append(it)

                bucket_sections: list[str] = []
                # If a module has <= 8 docs total, render a crisp flat list; otherwise group by topic bucket
                if len(linked_docs) <= 8:
                    doc_lines = [
                        f"- [[{it['note_basename']}|{os.path.basename(it['primary_rel'])}]] (`{it.get('_v2_fmt', '').upper()}` • {it.get('_v2_words', 0):,} Wörter)"
                        for it in linked_docs
                    ]
                    bucket_sections.append("\n".join(doc_lines))
                else:
                    for bkey, bheading in _MODUL_BUCKET_META:
                        b_items = grouped.get(bkey, [])
                        if not b_items:
                            continue
                        b_lines = [f"{bheading} ({len(b_items)})\n"]
                        for it in sorted(b_items, key=lambda x: os.path.basename(x["primary_rel"]).lower()):
                            src_fn = os.path.basename(it["primary_rel"])
                            b_lines.append(
                                f"- [[{it['note_basename']}|{src_fn}]] (`{it.get('_v2_fmt', '').upper()}` • {it.get('_v2_words', 0):,} Wörter)"
                            )
                        bucket_sections.append("\n".join(b_lines))

                sources_sec = (
                    "\n\n---\n\n"
                    "## 📚 Originaldokumente & Volltexte (V2 Quellen-Index)\n\n"
                    f"> [!NOTE] **Vollständige Quelldokumente ({len(linked_docs)} kanonische Dateien)**\n"
                    "> Alle Vorlesungsfolien, Übungen, Skripte, Ausarbeitungen und Fallstudien dieses Moduls sind SHA-256 & inhaltlich dedupliziert und vollständig extrahiert verlinkt.\n\n"
                    + "\n\n".join(bucket_sections)
                    + "\n"
                )
            else:
                sources_sec = "\n"
            content = preserved + sources_sec

        content = _clean_layer1_text_glitches(content, link_replacements)
        _write_if_changed(fp, content)

    # 2b. Replace old truncated 15,000-char inline CM_ins_INOC dump in DC1_ITIL4_Service_Operations.md
    dc1_itil_path = os.path.join(VAULT_DIR, "03_SAP_EnterpriseArchitecture", "DC1_ITIL4_Service_Operations.md")
    if os.path.exists(dc1_itil_path):
        with open(dc1_itil_path, "r", encoding="utf-8", errors="ignore") as f:
            dc1_txt = f.read()
        cm_start_marker = "\n## 📡 Carriermanagement-Integration ins INOC (Projektkonzeption)"
        cm_end_marker = "\n## 🔗 Verknüpfungen im Wissensnetz"
        if cm_start_marker in dc1_txt and cm_end_marker in dc1_txt:
            pre_cm = re.sub(r"\n---\s*$", "", dc1_txt.split(cm_start_marker)[0].rstrip()).rstrip()
            post_cm = dc1_txt.split(cm_end_marker, 1)[1]
            curated_cm_section = (
                "\n\n---\n\n"
                "## 📡 Carriermanagement-Integration ins INOC (Projektkonzeption)\n\n"
                "Überführung von Carrier-Management- und Netzanbindungsprozessen in den 24/7 INOC-Leitstand (Entlastung durch standardisierte Jira-Ticket-Triage):\n\n"
                "- **Phase 1 (Aufgaben-Identifikation & Triage):** Trennung zwischen vertriebsnahen Netzwerkinfrastruktur-Anfragen (`VNI-*` Streckenverläufe, Preisabfragen) und operativen Produktrealisierungen (`CM-*` Leitungsbestellungen, Kündigungen, IP-Transit/Dark Fiber).\n"
                "- **Phase 2 (Leistungsabgrenzung):** Übernahme wiederkehrender INOC-fähiger Routinetickets (Vertragsrecherche, Kündigungsschreiben, Angebotsanfrage inkl. Abstimmung mit Einkauf/Recht für AGB & SLA).\n"
                "- **Phase 3 (Wissensdatenbank & Standardisierung):** Confluence-SOPs für Dark-Fiber-Beschaffung, Dual-Stack-IPv6/IPv4 10G IP-Transit (95%-Perzentil) und Eskalationspfade.\n"
                f"- **Vollständiges Originalkonzept (V2 Volltext):** [[{cm_v2_note}|CM_ins_INOC_Projekt_VIM.docx – Vollständige Projektkonzeption]]\n\n"
                "---"
            )
            dc1_txt = pre_cm + curated_cm_section + cm_end_marker + post_cm
            _write_if_changed(dc1_itil_path, _clean_layer1_text_glitches(dc1_txt, link_replacements))

    # 2. Slim 01_Karriere_Bewerbungen/00_Bewerbungsunterlagen_Master_Volltext.md (preserve summary, drop raw duplicate body)
    career_hub = os.path.join(VAULT_DIR, "01_Karriere_Bewerbungen", "00_Bewerbungsunterlagen_Master_Volltext.md")
    if os.path.exists(career_hub):
        with open(career_hub, "r", encoding="utf-8", errors="ignore") as f:
            c_txt = f.read()
        marker = "\n## 📜 Volltext-Transkripte der Dokumente"
        if marker in c_txt:
            head_part = re.sub(r"\n---\s*$", "", c_txt.split(marker)[0].rstrip()).rstrip()
            career_items = [
                it for it in canonical_items if it["primary_rel"].startswith("00_Aktuelle_Bewerbungsunterlagen")
            ]
            c_links = "\n".join(
                f"- [[{it['note_basename']}|{os.path.basename(it['primary_rel'])}]] (`{it.get('_v2_fmt', '').upper()}` • {it.get('_v2_words', 0):,} Wörter)"
                for it in sorted(career_items, key=lambda x: x["primary_rel"].lower())
            )
            c_txt = (
                head_part
                + "\n\n---\n\n## 📚 Kanonische Volltext-Quellen (V2 Extraktion)\n\n"
                + "- **Kuratierte Kern-Dossiers (Schicht 1):** [[00_Lebenslauf_Volltext]] • [[00_Masterzeugnis_Leistungsuebersicht_Volltext]] • [[00_Bachelorzeugnis_Leistungsuebersicht_Volltext]] • [[00_Bewerbungsmanagement_Cockpit]] • [[Modul_Masterarbeit]]\n\n"
                + c_links
                + "\n"
            )
        c_txt = _clean_layer1_text_glitches(c_txt, link_replacements)
        _write_if_changed(career_hub, c_txt)

    # 3. Link V2 Quellen-Indizes neatly into key Layer-1 hubs if not already linked
    hub_backlinks = {
        os.path.join(VAULT_DIR, "03_SAP_EnterpriseArchitecture", "SSB_Grossprojekt_SAP4SSB.md"): "[[01_SSB_Quellen_Index|🗄️ Alle SSB S/4HANA Volltext-Quellen (V2)]]",
        os.path.join(VAULT_DIR, "03_SAP_EnterpriseArchitecture", "DC1_ITIL4_Service_Operations.md"): "[[04_DC1_Quellen_Index|🗄️ Alle Datacenter One Volltext-Quellen (V2)]]",
        os.path.join(VAULT_DIR, "03_SAP_EnterpriseArchitecture", "DC1_Hardware_Lifecycle_Management.md"): f"[[{by_filename_lower.get('hlm_v2.vsdx', '04_DC1_Quellen_Index')}|💻 Visio BPMN HLM_v2.vsdx Volltext]]",
    }
    for h_path, link_line in hub_backlinks.items():
        if os.path.exists(h_path):
            with open(h_path, "r", encoding="utf-8", errors="ignore") as f:
                htxt = f.read()
            target_bname = re.search(r"\[\[([^\|\]]+)", link_line).group(1)
            if target_bname not in htxt:
                htxt = htxt.rstrip() + f"\n\n- **V2 Quellen-Archiv:** {link_line}\n"
            _write_if_changed(h_path, _clean_layer1_text_glitches(htxt, link_replacements))

    # 4. Update 00_INDEX.md Data Lake note reference & clean all remaining Layer-1 files
    idx_path = os.path.join(VAULT_DIR, "00_INDEX.md")
    if os.path.exists(idx_path):
        with open(idx_path, "r", encoding="utf-8", errors="ignore") as f:
            itxt = f.read()
        itxt = itxt.replace(
            "05_Archiv/Volltexte_DataLake/",
            "05_Archiv/Volltexte_Quellen/",
        ).replace(
            "Über **140 Volltext-Bände & Split-Dateien**",
            f"**{stats['unique_sha256_docs']:,} kanonische, SHA-256-deduplizierte Volltext-Dokumente** (0 Splits)",
        )
        _write_if_changed(idx_path, _clean_layer1_text_glitches(itxt, link_replacements))

    for root, dirs, files in os.walk(VAULT_DIR):
        dirs[:] = [d for d in dirs if d not in (".obsidian", ".trash", "05_Archiv")]
        for fn in files:
            if not fn.endswith(".md"):
                continue
            fp = os.path.join(root, fn)
            with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                raw = f.read()
            cleaned = _clean_layer1_text_glitches(raw, link_replacements)
            if cleaned != raw:
                with open(fp, "w", encoding="utf-8", errors="replace") as f:
                    f.write(cleaned)

    # 5. Cleanly retire legacy monolithic & split Volltexte_DataLake directory
    if os.path.exists(LEGACY_DATALAKE_DIR):
        shutil.rmtree(LEGACY_DATALAKE_DIR)
        print(f"[CLEANUP] Removed legacy Volltexte_DataLake monolith/split directory.")


def load_v2_registry() -> dict[str, Any]:
    if os.path.exists(REGISTRY_V2_PATH):
        try:
            with open(REGISTRY_V2_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"version": "2.0", "by_sha256": {}}


def save_v2_registry(reg: dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(REGISTRY_V2_PATH), exist_ok=True)
    with open(REGISTRY_V2_PATH, "w", encoding="utf-8") as f:
        json.dump(reg, f, indent=2, ensure_ascii=False)


def _needs_targeted_ocr(cached_entry: dict[str, Any]) -> bool:
    """Identifies genuinely scanned/image-heavy PDFs that need RapidOCR recovery."""
    if cached_entry.get("format") != "pdf" or cached_entry.get("ocr_checked"):
        return False
    low_vis = int(cached_entry.get("low_visual_pages", 0))
    if low_vis <= 0:
        return False
    pages = max(1, int(cached_entry.get("pages_or_units", 1)))
    chars = int(cached_entry.get("chars", 0))
    if chars < 200 * min(pages, 5):
        return True
    return pages <= 60 and low_vis >= max(1, int(pages * 0.45))


def _execute_extraction_pass(
    tasks: list[dict[str, Any]],
    workers: int,
    enable_ocr: bool,
    pass_label: str,
    cache: dict[str, Any],
    reg: dict[str, Any],
    stats: dict[str, Any],
    today: str,
    t0: float,
    ckpt_every: int = 50,
) -> tuple[int, int, int, int, int]:
    """Runs a parallel ProcessPool extraction pass with frequent registry checkpoints."""
    extracted_ok = 0
    extracted_err = 0
    total_ocr_pages = 0
    total_tables = 0
    total_words = 0

    if not tasks:
        return extracted_ok, extracted_err, total_ocr_pages, total_tables, total_words

    os.makedirs(QUELLEN_DIR, exist_ok=True)
    item_by_sha = {it["sha256"]: it for it in tasks}
    done_cnt = 0

    print(f"[{pass_label}] Starting {len(tasks):,} documents (workers={workers}, ocr={enable_ocr})...", flush=True)
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(_extract_worker, (it, enable_ocr)): it["sha256"] for it in tasks}
        for fut in concurrent.futures.as_completed(futures):
            done_cnt += 1
            try:
                out = fut.result()
                sha = out["sha256"]
                res = out["res"]
            except Exception as exc:
                sha = futures[fut]
                res = {
                    "success": False,
                    "format": "err",
                    "text": "",
                    "chars": 0,
                    "words": 0,
                    "pages_or_units": 0,
                    "ocr_pages": 0,
                    "toc_entries": 0,
                    "tables_count": 0,
                    "meta": {},
                    "error": str(exc),
                }
            it = item_by_sha[sha]

            note_md = render_source_note(it, res, today)
            target_abs = os.path.join(VAULT_DIR, it["vault_rel"])
            _write_if_changed(target_abs, note_md)

            body_norm_sha = _compute_body_norm_hash(res.get("text", ""))
            it["_v2_fmt"] = res["format"]
            it["_v2_words"] = res["words"]
            it["_v2_body_norm_sha"] = body_norm_sha
            total_ocr_pages += res.get("ocr_pages", 0)
            total_tables += res.get("tables_count", 0)
            total_words += res.get("words", 0)

            if res.get("success"):
                extracted_ok += 1
            else:
                extracted_err += 1

            cache[sha] = {
                "version": "2.1",
                "primary_rel": it["primary_rel"],
                "vault_rel": it["vault_rel"],
                "format": res["format"],
                "words": res["words"],
                "chars": res["chars"],
                "pages_or_units": res["pages_or_units"],
                "ocr_pages": res["ocr_pages"],
                "low_visual_pages": res.get("meta", {}).get("low_visual_pages", 0),
                "ocr_checked": enable_ocr or (res.get("meta", {}).get("low_visual_pages", 0) == 0),
                "tables_count": res["tables_count"],
                "body_norm_sha256": body_norm_sha,
                "error": res.get("error"),
                "updated_at": datetime.now().isoformat(),
            }

            if done_cnt % ckpt_every == 0 or done_cnt == len(tasks):
                reg["by_sha256"] = cache
                reg["stats"] = stats
                save_v2_registry(reg)
                print(
                    f"  [{pass_label} {done_cnt:,}/{len(tasks):,}] elapsed={time.time()-t0:.1f}s | "
                    f"ok={extracted_ok:,} err={extracted_err} ocr_pages={total_ocr_pages} words={total_words:,}",
                    flush=True,
                )

    return extracted_ok, extracted_err, total_ocr_pages, total_tables, total_words


def rebuild_graph_manifest() -> dict[str, Any]:
    """Rebuilds VAULT_DIR/graph_manifest.json across all curated + V2 source notes."""
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, str]] = []
    bname_to_id: dict[str, str] = {}
    cached_contents: list[tuple[str, str]] = []

    for root, dirs, files in os.walk(VAULT_DIR):
        dirs[:] = sorted(d for d in dirs if d not in (".obsidian", ".trash"))
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, VAULT_DIR)
            bname = os.path.splitext(fn)[0].lower()
            with open(full, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            fm_dict: dict[str, str] = {}
            fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
            if fm_match:
                for ln in fm_match.group(1).splitlines():
                    if ":" in ln and not ln.strip().startswith("-"):
                        k, v = ln.split(":", 1)
                        fm_dict[k.strip()] = v.strip().strip('"').strip("'")

            node_id = fm_dict.get("id", bname).strip() or bname
            bname_to_id[bname] = node_id
            cached_contents.append((node_id, content))
            nodes.append({
                "id": node_id,
                "label": fm_dict.get("title", fn),
                "file": rel,
                "type": fm_dict.get("type", "concept"),
                "domain": fm_dict.get("domain", "general"),
                "summary": fm_dict.get("summary", ""),
                "words": len(content.split()),
            })

    seen_edges: set[tuple[str, str]] = set()
    for node_id, content in cached_contents:
        for raw in re.findall(r"\[\[(.*?)\]\]", content):
            target = os.path.splitext(os.path.basename(raw.split("|")[0].split("#")[0].strip()))[0].lower()
            tgt_id = bname_to_id.get(target)
            if tgt_id and tgt_id != node_id and (node_id, tgt_id) not in seen_edges:
                seen_edges.add((node_id, tgt_id))
                edges.append({"source": node_id, "target": tgt_id, "relation": "references"})

    connected = {e["source"] for e in edges} | {e["target"] for e in edges}
    orphans = sum(1 for n in nodes if n["id"] not in connected)
    manifest = {
        "vault_name": "Visar Murseli | Enterprise Knowledge Hub & Second Brain (V2)",
        "generated_at": datetime.now().isoformat(),
        "total_nodes": len(nodes),
        "total_edges": len(edges),
        "orphan_nodes": orphans,
        "nodes": nodes,
        "edges": edges,
    }
    manifest_path = os.path.join(VAULT_DIR, "graph_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"[GRAPH] Manifest rebuilt: {len(nodes):,} nodes | {len(edges):,} edges | {orphans} orphans", flush=True)
    return manifest


def _apply_inplace_hygiene_upgrade(
    it: dict[str, Any], cached: dict[str, Any], target_abs: str, today: str
) -> bool:
    """Upgrades a V2.0 clean note in-place to V2.1 (expanding ligatures, fixing soft hyphens, hashing body)."""
    try:
        with open(target_abs, "r", encoding="utf-8", errors="ignore") as f:
            raw = f.read()
        split = _split_v2_note_header_body(raw)
        if split is None:
            return False
        header, body = split
        cleaned_body = finalize_markdown_body(body)
        new_words = len(cleaned_body.split()) if cleaned_body else 0
        new_chars = len(cleaned_body)
        norm_sha = _compute_body_norm_hash(cleaned_body)

        if cleaned_body != body.strip():
            # Refresh word_count & Umfang in header cleanly
            fmt_upper = str(cached.get("format", "")).upper()
            old_wc = cached.get("words", 0)
            header = re.sub(r"^word_count:\s*\d+", f"word_count: {new_words}", header, flags=re.MULTILINE)
            header = header.replace(f"({fmt_upper}, {old_wc:,} Wörter,", f"({fmt_upper}, {new_words:,} Wörter,")
            header = header.replace(f"**{old_wc:,} Wörter**", f"**{new_words:,} Wörter**")
            header = re.sub(r'^last_updated:\s*".*"', f'last_updated: "{today}"', header, flags=re.MULTILINE)
            _write_if_changed(target_abs, header + cleaned_body + "\n")

        cached["version"] = "2.1"
        cached["words"] = new_words
        cached["chars"] = new_chars
        cached["body_norm_sha256"] = norm_sha
        cached["updated_at"] = datetime.now().isoformat()
        it["_v2_fmt"] = cached.get("format", "")
        it["_v2_words"] = new_words
        it["_v2_body_norm_sha"] = norm_sha
        return True
    except Exception:
        return False


def _needs_v21_reextract(it: dict[str, Any], cached: dict[str, Any]) -> bool:
    """Identifies cached V2.0 items that gain material content from Pass-2 extractors (WinRT OCR / SmartArt)."""
    fmt = cached.get("format", "")
    if fmt == "pdf" and (int(cached.get("ocr_pages", 0)) > 0 or int(cached.get("low_visual_pages", 0)) > 0):
        # Reset ocr_checked flag on scan PDFs so WinRT OCR upgrades RapidOCR text!
        if int(cached.get("ocr_pages", 0)) > 0 or int(cached.get("words", 0)) < 30:
            cached["ocr_checked"] = False
            return True
    if fmt == "pptx" and (int(cached.get("words", 0)) < 30 or _pptx_has_diagrams(it["primary_abs"])):
        return True
    return False


def run_v2_sync(workers: int = 6, force: bool = False, dry_run: bool = False) -> None:
    t0 = time.time()
    today = datetime.now().strftime("%Y-%m-%d")

    print("=" * 72)
    print("OBSIDIAN CAREER OS PIPELINE V2.1 (WINRT OCR + SMARTART + CONTENT DEDUP)")
    print("=" * 72)

    canonical_items, modul_links_index, stats = discover_unique_documents()
    print(
        f"[SCAN] Eligible files: {stats['total_eligible_files']:,} | "
        f"Unique SHA-256: {stats['unique_sha256_docs']:,} | "
        f"SHA-Duplicates collapsed: {stats['duplicates_collapsed']:,} | "
        f"Empty skipped: {stats['empty_files_skipped']}"
    )

    if dry_run:
        return

    reg = load_v2_registry()
    cache = reg.get("by_sha256", {})

    pending_fast: list[dict[str, Any]] = []
    reextract_ocr: list[dict[str, Any]] = []
    reused_count = 0
    hygiene_upgraded = 0

    for it in canonical_items:
        target_abs = os.path.join(VAULT_DIR, it["vault_rel"])
        cached = cache.get(it["sha256"])
        file_fresh = (
            not force
            and cached
            and not cached.get("error")
            and cached.get("vault_rel") == it["vault_rel"]
            and os.path.exists(target_abs)
            and os.path.getmtime(target_abs) >= os.path.getmtime(it["primary_abs"])
        )
        if file_fresh and cached.get("version") == "2.1":
            norm_sha = cached.get("body_norm_sha256", "")
            if not norm_sha:
                with open(target_abs, "r", encoding="utf-8", errors="ignore") as f:
                    split = _split_v2_note_header_body(f.read())
                    norm_sha = _compute_body_norm_hash(split[1] if split else "")
                cached["body_norm_sha256"] = norm_sha
            it["_v2_fmt"] = cached.get("format", "")
            it["_v2_words"] = cached.get("words", 0)
            it["_v2_body_norm_sha"] = norm_sha
            reused_count += 1
        elif file_fresh and cached.get("version") == "2.0":
            if _needs_v21_reextract(it, cached):
                reextract_ocr.append(it)
            elif _apply_inplace_hygiene_upgrade(it, cached, target_abs, today):
                hygiene_upgraded += 1
            else:
                pending_fast.append(it)
        else:
            pending_fast.append(it)

    print(
        f"[PLAN] Reused V2.1: {reused_count:,} | In-place typography upgraded: {hygiene_upgraded:,} | "
        f"Re-extract WinRT/SmartArt: {len(reextract_ocr):,} | New/repair extract: {len(pending_fast):,} (workers={workers})",
        flush=True,
    )

    # Phase 1: High-speed extraction for new/changed/broken documents
    _, _, _, t1_tables, _ = _execute_extraction_pass(
        pending_fast, workers=workers, enable_ocr=False, pass_label="PHASE1-FAST",
        cache=cache, reg=reg, stats=stats, today=today, t0=t0, ckpt_every=50,
    )

    # Phase 2: Dedicated WinRT OCR + SmartArt PPTX pass
    # Include both Pass-2 upgraded targets AND any newly extracted scan PDFs
    seen_ocr_shas = {it["sha256"] for it in reextract_ocr}
    for it in canonical_items:
        if it["sha256"] not in seen_ocr_shas and _needs_targeted_ocr(cache.get(it["sha256"], {})):
            reextract_ocr.append(it)
            seen_ocr_shas.add(it["sha256"])

    pillar_prio = {"00_Aktuelle_Bewerbungsunterlagen": 0, "01_SSB": 1, "04_DC1": 2, "02_Master": 3, "03_Bachelor": 4}
    reextract_ocr.sort(
        key=lambda it: (
            pillar_prio.get(it["primary_rel"].split(os.sep)[0], 9),
            cache.get(it["sha256"], {}).get("pages_or_units", 0),
            it["primary_rel"].lower(),
        )
    )
    _, _, total_ocr_pages, t2_tables, _ = _execute_extraction_pass(
        reextract_ocr, workers=min(3, workers), enable_ocr=True, pass_label="PHASE2-WINOCR",
        cache=cache, reg=reg, stats=stats, today=today, t0=t0, ckpt_every=10,
    )
    total_tables = t1_tables + t2_tables

    # Pass-2 Normalized-Content + Mega Near-Clone Deduplication
    canonical_items, modul_links_index, exact_dup_collapsed, clone_dup_collapsed = deduplicate_by_normalized_content(
        canonical_items
    )
    stats["content_exact_collapsed"] = exact_dup_collapsed
    stats["content_clone_collapsed"] = clone_dup_collapsed
    stats["canonical_notes_final"] = len(canonical_items)
    stats["duplicates_collapsed"] += exact_dup_collapsed + clone_dup_collapsed
    stats["unique_sha256_docs"] = len(canonical_items)
    print(
        f"[DEDUP] Content-identical collapsed: {exact_dup_collapsed:,} | "
        f"Mega near-clones collapsed: {clone_dup_collapsed:,} | Final canonical notes: {len(canonical_items):,}",
        flush=True,
    )

    reg["by_sha256"] = cache
    reg["stats"] = stats
    reg["last_run"] = datetime.now().isoformat()
    save_v2_registry(reg)

    # Remove any orphaned/stale .md files under 05_Archiv/Volltexte_Quellen not part of current canonical set
    expected_rels = {os.path.normpath(it["vault_rel"]) for it in canonical_items}
    index_names = {
        "00_Quellen_Index.md",
        "01_SSB_Quellen_Index.md",
        "02_Master_Quellen_Index.md",
        "03_Bachelor_Quellen_Index.md",
        "04_DC1_Quellen_Index.md",
        "05_Bibliothek_Quellen_Index.md",
    }
    for it_idx in index_names:
        expected_rels.add(os.path.normpath(os.path.join(QUELLEN_REL, it_idx)))

    removed_stale = 0
    if os.path.exists(QUELLEN_DIR):
        for root, _, files in os.walk(QUELLEN_DIR):
            for fn in files:
                if fn.endswith(".md"):
                    full = os.path.join(root, fn)
                    rel = os.path.normpath(os.path.relpath(full, VAULT_DIR))
                    if rel not in expected_rels:
                        os.remove(full)
                        removed_stale += 1

    build_v2_indexes(canonical_items, stats, today)
    migrate_layer1_and_cleanup(canonical_items, modul_links_index, stats, today)
    rebuild_graph_manifest()

    elapsed = time.time() - t0
    print("\n" + "=" * 72)
    print(
        f"[DONE V2] {stats['unique_sha256_docs']:,} unique source notes synchronized | "
        f"OCR pages: {total_ocr_pages} | Tables: {total_tables:,} | "
        f"Stale removed: {removed_stale} | Elapsed: {elapsed:.1f}s"
    )
    print("=" * 72)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Obsidian Career OS Extraction & Sync V2")
    parser.add_argument("--workers", type=int, default=6, help="Multiprocessing workers for extraction")
    parser.add_argument("--force", action="store_true", help="Force re-extraction ignoring V2 cache")
    parser.add_argument("--dry-run", action="store_true", help="Scan & count without modifying vault")
    parser.add_argument("--manifest-only", action="store_true", help="Rebuild graph_manifest.json only")
    args = parser.parse_args()
    if args.manifest_only:
        rebuild_graph_manifest()
    else:
        run_v2_sync(workers=args.workers, force=args.force, dry_run=args.dry_run)
