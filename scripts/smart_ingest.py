# -*- coding: utf-8 -*-
"""
Karpathy LLM-Wiki Smart Ingestion & Entity-Extractor Engine
Author: Visar Murseli, M.Sc. | Enterprise Knowledge Hub & Career OS

Funktionen:
1. Automatische Erkennung & Extraktion von Rohdokumenten:
   - Unterstützt Markdown (.md), Text (.txt), PDF (.pdf via pypdf) und Word (.docx via docx).
2. Semantische Klassifikation & Domänen-Routing:
   - Identifiziert Unternehmen, Fachbegriffe, SAP-Module, akademische Theorien und Rollen.
   - Sortiert Dokumente zielsicher in den richtigen Ordner des Obsidian Vaults ein:
     * 01_Karriere_Bewerbungen/ (Interview-Dossiers, Job-Profile)
     * 02_Wirtschaftsinformatik_300ECTS/ (Studium, Forschung, Mayring)
     * 03_SAP_EnterpriseArchitecture/ (S/4HANA, BTP, Clean Core, FI/CO/MM/SD, ITIL 4)
     * 04_Second_Brain_Zettelkasten/ (Synergien, Personal OS)
3. Standardisierte Frontmatter- & Abstract-Generierung:
   - Erzeugt valides YAML-Frontmatter (id, title, type, domain, status, summary, tags, last_updated).
   - Injiziert den obligatorischen `> [!ABSTRACT] 60-Sekunden-Essenz` Block.
4. Automatische Wikilink-Quervernetzung (Auto-Linker):
   - Wendet das Zettelkasten-Fachlexikon direkt an und verlinkt Kernkonzepte als [[TargetNote|Label]].
   - Injiziert Navigations-Backlinks zu den zuständigen MOCs und zum Master Index [[00_INDEX]].
5. Local RAG Synchronisation & Archivierung:
   - Indexiert neue Zettel sofort in der SQLite/RRF Vektordatenbank (rag_upsert).
   - Verschiebt verarbeitete Rohdateien nach inbox/processed/.
"""

import os
import re
import sys
import shutil
import argparse
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INBOX_DIR = os.path.join(BASE_DIR, "inbox")
PROCESSED_DIR = os.path.join(INBOX_DIR, "processed")
VAULT_DIR = r"C:\Users\SHQIPTAR634\Documents\Obsidian Vault"
VAULT_INBOX_DIR = os.path.join(VAULT_DIR, "00_Inbox")

# Import synthesizer for instant safe auto-linking
try:
    from zettelkasten_synthesizer import (
        ZettelkastenSynthesizer,
        tokenize_markdown,
        CANONICAL_CONCEPT_LEXICON
    )
    SYNTHESIZER_AVAILABLE = True
except Exception:
    try:
        from scripts.zettelkasten_synthesizer import (
            ZettelkastenSynthesizer,
            tokenize_markdown,
            CANONICAL_CONCEPT_LEXICON
        )
        SYNTHESIZER_AVAILABLE = True
    except Exception:
        SYNTHESIZER_AVAILABLE = False

# Import local RAG upsert
try:
    from local_rag_engine import upsert_note as rag_upsert
    RAG_AVAILABLE = True
except Exception:
    try:
        from scripts.local_rag_engine import upsert_note as rag_upsert
        RAG_AVAILABLE = True
    except Exception:
        RAG_AVAILABLE = False


# Known companies & targeted routing keywords
COMPANIES_MAP = {
    "schwarz": "Schwarz_Digits",
    "schwarz digits": "Schwarz_Digits",
    "kpmg": "KPMG",
    "trumpf": "TRUMPF",
    "computacenter": "Computacenter",
    "ey": "Ernst_Young",
    "ernst & young": "Ernst_Young",
    "msg": "msg_systems",
    "msg systems": "msg_systems",
    "porsche": "Porsche",
    "mercedes": "Mercedes_Benz",
    "ssb": "SSB_AG",
    "datacenter one": "Datacenter_One",
    "dc1": "Datacenter_One",
}

# Domain routing rules
DOMAIN_RULES = [
    {
        "domain": "career-pmo",
        "keywords": [
            "interview", "vorstellungsgespräch", "bewerbung", "gehalt", "recruiting",
            "ansprechpartner", "talent acquisition", "stellenanzeige", "job description",
            "karriere", "probetag", "case study", "trainee"
        ],
        "default_folder": os.path.join(VAULT_DIR, "01_Karriere_Bewerbungen"),
        "interview_folder": os.path.join(VAULT_DIR, "01_Karriere_Bewerbungen", "Interview_Vorbereitungen"),
        "moc": "00_Bewerbungsmanagement_Cockpit"
    },
    {
        "domain": "sap-transformation",
        "keywords": [
            "s/4hana", "sap", "btp", "clean core", "solution design", "ltmc", "cvi",
            "signavio", "cloud alm", "enable now", "activate", "acdoca", "trennungsrechnung",
            "wricefa", "universal journal", "abap", "fiori", "fit-to-standard"
        ],
        "default_folder": os.path.join(VAULT_DIR, "03_SAP_EnterpriseArchitecture", "01_Architektur_Technik"),
        "finance_folder": os.path.join(VAULT_DIR, "03_SAP_EnterpriseArchitecture", "02_Kaufmaennische_Prozesse"),
        "governance_folder": os.path.join(VAULT_DIR, "03_SAP_EnterpriseArchitecture", "03_Governance_Vergabe"),
        "enablement_folder": os.path.join(VAULT_DIR, "03_SAP_EnterpriseArchitecture", "04_Change_Enablement"),
        "moc": "MOC_SSB_Transformation"
    },
    {
        "domain": "academic-curriculum",
        "keywords": [
            "vorlesung", "modul", "seminar", "ects", "prüfung", "lehrstuhl", "herzwurm",
            "becker", "masterarbeit", "bachelorarbeit", "mayring", "qualitative inhaltsanalyse",
            "boundary resources", "forschungsmethode"
        ],
        "default_folder": os.path.join(VAULT_DIR, "02_Wirtschaftsinformatik_300ECTS"),
        "moc": "Modul_Übersicht"
    },
    {
        "domain": "datacenter-operations",
        "keywords": [
            "datacenter one", "dc1", "inoc", "itil", "itil 4", "prtg", "usv", "klimatechnik",
            "core-netzwerk", "hardware-lifecycle", "hlm", "monitoring 24/7"
        ],
        "default_folder": os.path.join(VAULT_DIR, "03_SAP_EnterpriseArchitecture"),
        "moc": "DC1_ITIL4_Service_Operations"
    },
    {
        "domain": "synergy-architecture",
        "keywords": [
            "synergie", "arbeit x uni", "theorie und praxis", "transfer", "alleinstellung"
        ],
        "default_folder": os.path.join(VAULT_DIR, "04_Second_Brain_Zettelkasten", "Synergien"),
        "moc": "Persoenliches_Staerkenprofil"
    }
]


def slugify(text: str) -> str:
    """Wandelt einen String in einen sauberen Dateinamen-Slug um."""
    text = text.lower().strip()
    text = text.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    text = re.sub(r"[^a-z0-9\s_-]", "", text)
    text = re.sub(r"[\s_]+", "_", text)
    return text.strip("_")


class SmartIngestionEngine:
    def __init__(self, workspace_inbox: str = INBOX_DIR, vault_dir: str = VAULT_DIR):
        self.workspace_inbox = workspace_inbox
        self.vault_dir = vault_dir
        self.vault_inbox = os.path.join(vault_dir, "00_Inbox")
        self.processed_dir = PROCESSED_DIR
        os.makedirs(self.workspace_inbox, exist_ok=True)
        os.makedirs(self.vault_inbox, exist_ok=True)
        os.makedirs(self.processed_dir, exist_ok=True)

    def extract_text_from_file(self, file_path: str) -> tuple[str, str]:
        """Extrahiert Rohinhalt und Dokumenttitel aus verschiedenen Dateiformaten."""
        ext = os.path.splitext(file_path)[1].lower()
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        text = ""

        if ext in [".md", ".txt"]:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
            except UnicodeDecodeError:
                with open(file_path, "r", encoding="latin-1", errors="replace") as f:
                    text = f.read()

        elif ext == ".pdf":
            try:
                import pypdf
                reader = pypdf.PdfReader(file_path)
                pages_text = []
                for p in reader.pages:
                    t = p.extract_text()
                    if t:
                        pages_text.append(t)
                text = "\n\n".join(pages_text)
            except Exception as e:
                text = f"[!] PDF Extraktionsfehler: {e}"

        elif ext == ".docx":
            try:
                import docx
                doc = docx.Document(file_path)
                paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
                text = "\n\n".join(paragraphs)
            except Exception as e:
                text = f"[!] DOCX Extraktionsfehler: {e}"

        else:
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
            except Exception:
                text = ""

        # Title extraction from first markdown heading or clean filename
        title = base_name.replace("_", " ").title()
        for line in text.splitlines():
            line_s = line.strip()
            if line_s.startswith("# "):
                title = line_s[2:].strip()
                break

        return text.strip(), title

    def classify_and_route(self, text: str, title: str, source_filename: str = "") -> dict:
        """Bestimmt Domäne, Dokumententyp, Zielordner und Frontmatter-Tags."""
        text_lower = text.lower() + " " + title.lower() + " " + source_filename.lower()

        # 1. Company Detection
        detected_company = None
        for comp_key, canonical_name in COMPANIES_MAP.items():
            if re.search(r'\b' + re.escape(comp_key) + r'\b', text_lower):
                detected_company = canonical_name
                break

        # 2. Domain Scoring with Priority Gates
        best_domain = "second-brain"
        target_folder = os.path.join(self.vault_dir, "04_Second_Brain_Zettelkasten")
        target_moc = "00_INDEX"
        doc_type = "concept"
        max_score = 0

        is_academic_research = any(a in text_lower for a in [
            "experteninterview", "mayring", "qualitative inhaltsanalyse", "lehrstuhl",
            "masterarbeit", "bachelorarbeit", "forschungsmethode", "vorlesung", "ects"
        ])
        is_job_interview = (
            any(k in text_lower for k in ["vorstellungsgespräch", "job interview", "interview vorbereit", "bewerbungsgespräch", "recruiting interview"])
            or ("interview" in text_lower and not is_academic_research)
        )
        is_career = is_job_interview or any(k in text_lower for k in ["bewerbung", "recruiting", "stellenanzeige", "job description", "karriere"])

        if is_academic_research and not any(c in text_lower for c in ["bewerb", "recruiting", "gehaltsvorstellung"]):
            best_domain = "academic-curriculum"
            target_folder = os.path.join(self.vault_dir, "02_Wirtschaftsinformatik_300ECTS")
            target_moc = "Modul_Übersicht"
        elif is_job_interview or (is_career and detected_company and detected_company not in ["SSB_AG", "Datacenter_One"]):
            best_domain = "career-pmo"
            target_folder = os.path.join(self.vault_dir, "01_Karriere_Bewerbungen")
            target_moc = "00_Bewerbungsmanagement_Cockpit"
        else:
            for rule in DOMAIN_RULES:
                score = 0
                for kw in rule["keywords"]:
                    if re.search(r'\b' + re.escape(kw) + r'\b', text_lower):
                        score += 1
                if score > max_score:
                    max_score = score
                    best_domain = rule["domain"]
                    target_folder = rule["default_folder"]
                    target_moc = rule.get("moc", "00_INDEX")

        # Refined routing based on document type
        today_iso = datetime.now().strftime("%Y-%m-%d")

        if best_domain == "career-pmo":
            is_interview = any(k in text_lower for k in ["interview", "vorstellungsgespräch", "gesprächsnotiz", "debriefing"])
            if is_interview:
                doc_type = "interview-prep"
                target_folder = os.path.join(self.vault_dir, "01_Karriere_Bewerbungen", "Interview_Vorbereitungen")
                comp_tag = detected_company or "Unternehmen"
                target_filename = f"{today_iso}_{comp_tag}_{slugify(title)[:36]}.md"
            else:
                doc_type = "job-dossier" if any(k in text_lower for k in ["stelle", "job", "gehalt", "recruiting"]) else "concept"
                target_filename = f"{slugify(title)[:48]}.md"

        elif best_domain == "sap-transformation":
            doc_type = "concept"
            if any(k in text_lower for k in ["fi", "co", "finance", "controlling", "acdoca", "trennungsrechnung"]):
                target_folder = os.path.join(self.vault_dir, "03_SAP_EnterpriseArchitecture", "02_Kaufmaennische_Prozesse")
                target_moc = "MOC_Kaufmaennische_Prozesse"
            elif any(k in text_lower for k in ["signavio", "cloud alm", "enable now", "schulung", "change"]):
                target_folder = os.path.join(self.vault_dir, "03_SAP_EnterpriseArchitecture", "04_Change_Enablement")
                target_moc = "MOC_Change_Management"
            elif any(k in text_lower for k in ["pmo", "steuerung", "vergabe", "sektvo", "ms project"]):
                target_folder = os.path.join(self.vault_dir, "03_SAP_EnterpriseArchitecture", "03_Governance_Vergabe")
                target_moc = "MOC_Projektgovernance_Vergabe"
            else:
                target_folder = os.path.join(self.vault_dir, "03_SAP_EnterpriseArchitecture", "01_Architektur_Technik")
                target_moc = "MOC_Enterprise_Architecture"
            target_filename = f"{slugify(title)[:48]}.md"

        elif best_domain == "academic-curriculum":
            doc_type = "module" if "modul" in text_lower else "concept"
            target_folder = os.path.join(self.vault_dir, "02_Wirtschaftsinformatik_300ECTS")
            target_moc = "Modul_Übersicht"
            target_filename = f"Modul_{slugify(title)[:40]}.md" if doc_type == "module" else f"{slugify(title)[:48]}.md"

        elif best_domain == "synergy-architecture":
            doc_type = "synergy"
            target_folder = os.path.join(self.vault_dir, "04_Second_Brain_Zettelkasten", "Synergien")
            target_moc = "Persoenliches_Staerkenprofil"
            target_filename = f"Synergie_{slugify(title)[:40]}.md"

        else:
            target_folder = os.path.join(self.vault_dir, "04_Second_Brain_Zettelkasten")
            target_moc = "00_INDEX"
            target_filename = f"{slugify(title)[:48]}.md"

        # Generate tags
        tags = [best_domain.replace("-", "_")]
        if doc_type != "concept":
            tags.append(doc_type.replace("-", "_"))
        if detected_company:
            tags.append(detected_company.lower())

        return {
            "domain": best_domain,
            "type": doc_type,
            "target_folder": target_folder,
            "target_filename": target_filename,
            "target_moc": target_moc,
            "detected_company": detected_company,
            "tags": tags,
            "title": title
        }

    def assemble_structured_note(self, text: str, routing: dict) -> str:
        """Formatiert den Inhalt nach dem einheitlichen Karpathy LLM-Wiki Schema."""
        today_iso = datetime.now().strftime("%Y-%m-%d")
        title = routing["title"]
        slug_id = slugify(title)

        # Generate crisp 1-2 sentence summary
        summary = ""
        clean_lines = [l.strip() for l in text.splitlines() if l.strip() and not l.strip().startswith("#")]
        if clean_lines:
            first_p = clean_lines[0]
            summary = first_p[:180] + ("..." if len(first_p) > 180 else "")
        if not summary:
            summary = f"Wissenszettel zu {title} ({routing['domain']})."

        tags_str = "\n".join(f"  - {t}" for t in routing["tags"])

        # Header with frontmatter & 60s abstract
        header = f"""---
id: {slug_id}
title: "{title}"
type: {routing['type']}
domain: {routing['domain']}
status: active
summary: "{summary}"
tags:
{tags_str}
last_updated: "{today_iso}"
---

# 📝 {title}

> [!ABSTRACT] **60-Sekunden-Essenz**
> - **Fokus:** {summary}
> - **Kontext:** Zugeordnet zu Domäne `{routing['domain']}` ({routing['type']}).
> - **Navigation:** Verknüpft mit [[{routing['target_moc']}|🧭 {routing['target_moc']}]] • [[00_INDEX|🧠 Master Index]].

---

"""
        # Strip existing leading title heading if present in text to avoid duplication
        body = text.strip()
        body_lines = body.splitlines()
        if body_lines and body_lines[0].strip().startswith("# "):
            body = "\n".join(body_lines[1:]).strip()

        # Standard Backlinks & MOC Footer
        footer = f"""

---

## 🔗 Verknüpfte Zettel & MOCs
- [[{routing['target_moc']}|🧭 {routing['target_moc']}]]
- [[00_INDEX|🧠 Master Index]]
"""
        note_content = header + body + footer

        # Auto-Link plain text concepts using the Synthesizer lexicon if available
        if SYNTHESIZER_AVAILABLE:
            try:
                tokens = tokenize_markdown(body)
                sorted_lexicon = sorted(CANONICAL_CONCEPT_LEXICON.items(), key=lambda x: len(x[0]), reverse=True)
                new_tokens = []
                linked_targets = set()

                for kind, val in tokens:
                    if kind == "TEXT":
                        curr_val = val
                        for concept, target in sorted_lexicon:
                            if target in linked_targets or target.lower() == slug_id:
                                continue
                            if concept.lower() not in curr_val.lower():
                                continue
                            c_re = re.compile(r'\b(' + re.escape(concept) + r')\b', re.IGNORECASE)
                            if c_re.search(curr_val):
                                curr_val = c_re.sub(f"[[{target}|\\1]]", curr_val, count=1)
                                linked_targets.add(target)
                        new_tokens.append(("TEXT", curr_val))
                    else:
                        new_tokens.append((kind, val))

                linked_body = "".join(v for _, v in new_tokens)
                note_content = header + linked_body + footer
            except Exception:
                pass

        return note_content

    def ingest_file(self, file_path: str, dry_run: bool = False) -> dict:
        """Verarbeitet eine einzelne Datei aus inbox/ oder 00_Inbox."""
        filename = os.path.basename(file_path)
        text, title = self.extract_text_from_file(file_path)
        if not text:
            return {"ok": False, "error": f"Kein lesbarer Text in {filename}"}

        routing = self.classify_and_route(text, title, source_filename=filename)
        dest_folder = routing["target_folder"]
        dest_filename = routing["target_filename"]
        dest_path = os.path.join(dest_folder, dest_filename)

        final_note = self.assemble_structured_note(text, routing)

        if not dry_run:
            os.makedirs(dest_folder, exist_ok=True)
            with open(dest_path, "w", encoding="utf-8") as f:
                f.write(final_note)

            # RAG Upsert
            if RAG_AVAILABLE:
                try:
                    rag_upsert(dest_path)
                except Exception:
                    pass

            # Archive source file to processed/
            today_str = datetime.now().strftime("%Y-%m-%d")
            today_archive_dir = os.path.join(self.processed_dir, today_str)
            os.makedirs(today_archive_dir, exist_ok=True)
            archive_dest = os.path.join(today_archive_dir, filename)

            # If inside workspace inbox, move it. If inside vault inbox, move to archive
            try:
                shutil.move(file_path, archive_dest)
            except Exception:
                pass

        return {
            "ok": True,
            "source": file_path,
            "filename": filename,
            "title": title,
            "domain": routing["domain"],
            "type": routing["type"],
            "destination": dest_path,
            "target_moc": routing["target_moc"]
        }

    def ingest_raw_text(self, raw_text: str, title: str = "", dry_run: bool = False) -> dict:
        """Nimmt unstrukturierten Freitext (z.B. aus Telegram /notiz) auf und archiviert ihn zielsicher."""
        if not title:
            # derive title from first line
            first_line = raw_text.strip().splitlines()[0] if raw_text.strip() else "Neue Notiz"
            title = first_line[:40].replace("#", "").strip()

        routing = self.classify_and_route(raw_text, title)
        dest_folder = routing["target_folder"]
        dest_filename = routing["target_filename"]
        dest_path = os.path.join(dest_folder, dest_filename)

        final_note = self.assemble_structured_note(raw_text, routing)

        if not dry_run:
            os.makedirs(dest_folder, exist_ok=True)
            with open(dest_path, "w", encoding="utf-8") as f:
                f.write(final_note)

            if RAG_AVAILABLE:
                try:
                    rag_upsert(dest_path)
                except Exception:
                    pass

        return {
            "ok": True,
            "title": title,
            "domain": routing["domain"],
            "type": routing["type"],
            "destination": dest_path,
            "target_moc": routing["target_moc"]
        }

    def scan_and_ingest_all(self, dry_run: bool = False) -> list[dict]:
        """Durchsucht workspace inbox/ und vault 00_Inbox/ nach allen anstehenden Dokumenten."""
        results = []

        # 1. Scan workspace inbox/
        for f in os.listdir(self.workspace_inbox):
            if f in ["README.md", "processed", ".git", ".gitignore"] or f.startswith("."):
                continue
            full_p = os.path.join(self.workspace_inbox, f)
            if os.path.isfile(full_p):
                res = self.ingest_file(full_p, dry_run=dry_run)
                results.append(res)

        # 2. Scan vault 00_Inbox/ (files that are not Mobile_Notizen / Webapp_Notizen logs)
        if os.path.exists(self.vault_inbox):
            for f in os.listdir(self.vault_inbox):
                if f in ["Mobile_Notizen.md", "Webapp_Notizen.md"] or f.startswith("."):
                    continue
                full_p = os.path.join(self.vault_inbox, f)
                if os.path.isfile(full_p):
                    res = self.ingest_file(full_p, dry_run=dry_run)
                    results.append(res)

        return results


def run_cli():
    parser = argparse.ArgumentParser(description="Karpathy LLM-Wiki Smart Ingestion & Entity-Extractor Engine")
    parser.add_argument("--scan", action="store_true", default=True, help="Scan and ingest all files in inbox/")
    parser.add_argument("--file", help="Ingest a specific file path")
    parser.add_argument("--text", help="Ingest raw text string")
    parser.add_argument("--title", default="", help="Optional title for text ingestion")
    parser.add_argument("--dry-run", action="store_true", help="Simulate ingestion without moving files")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    engine = SmartIngestionEngine()

    print("=" * 72)
    print("📥 KARPATHY LLM-WIKI SMART INGESTION & ENTITY-EXTRACTOR")
    print("=" * 72)

    if args.text:
        res = engine.ingest_raw_text(args.text, title=args.title, dry_run=args.dry_run)
        if args.json:
            import json
            print(json.dumps(res, indent=2, ensure_ascii=False))
            return
        prefix = "[DRY-RUN] " if args.dry_run else "[✓] "
        print(f"{prefix}Freitext erfolgreich archiviert:")
        print(f"   • Titel: {res['title']}")
        print(f"   • Domäne: {res['domain']} ({res['type']})")
        print(f"   • Zielort: {res['destination']}")
        print(f"   • MOC: [[{res['target_moc']}]]")
        print("=" * 72)
        return

    if args.file:
        res = engine.ingest_file(args.file, dry_run=args.dry_run)
        if args.json:
            import json
            print(json.dumps(res, indent=2, ensure_ascii=False))
            return
        prefix = "[DRY-RUN] " if args.dry_run else "[✓] "
        if res.get("ok"):
            print(f"{prefix}Datei erfolgreich verarbeitet:")
            print(f"   • Quelle: {res['filename']}")
            print(f"   • Titel: {res['title']}")
            print(f"   • Domäne: {res['domain']} ({res['type']})")
            print(f"   • Zielort: {res['destination']}")
            print(f"   • MOC: [[{res['target_moc']}]]")
        else:
            print(f"[!] Fehler: {res.get('error')}")
        print("=" * 72)
        return

    # Default: scan all
    mode_str = "[DRY-RUN] " if args.dry_run else ""
    print(f"[*] {mode_str}Scanne inbox/ und 00_Inbox/ nach neuen Dokumenten...")
    results = engine.scan_and_ingest_all(dry_run=args.dry_run)

    if args.json:
        import json
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return

    if not results:
        print("\n[✓] Inbox ist aufgeräumt. Keine ausstehenden Rohdateien gefunden.")
    else:
        print(f"\n[+] {len(results)} Dokument(e) erfolgreich strukturiert und einsortiert:")
        for idx, r in enumerate(results, 1):
            if r.get("ok"):
                print(f"    {idx}. {r['filename']} -> [{r['domain']}] {r['destination']}")
            else:
                print(f"    {idx}. [!] Fehler bei {r.get('source')}: {r.get('error')}")

    print("=" * 72)


if __name__ == "__main__":
    run_cli()
