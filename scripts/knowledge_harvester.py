# -*- coding: utf-8 -*-
"""
Enterprise Knowledge Harvester & Ingestion Engine (EKHIE)
Piecewise, batch-oriented, persistent ingestion of all workspace documents into Obsidian.
Author: Visar Murseli, M.Sc. | Data Science & Enterprise AI Architect
"""

import os
import sys
import json
import hashlib
import re
from datetime import datetime
import argparse

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
VAULT_DIR = r"C:\Users\SHQIPTAR634\Documents\Obsidian Vault"
REGISTRY_PATH = os.path.join(BASE_DIR, "config", "ingestion_registry.json")

# Add scripts directory to sys.path
if os.path.dirname(__file__) not in sys.path:
    sys.path.insert(0, os.path.dirname(__file__))

from knowledge_extractors import extract_document, clean_text

EXTRACTABLE_EXTENSIONS = {'.pdf', '.docx', '.pptx', '.xlsx', '.xlsm', '.txt', '.md', '.html'}

# Sensitive folders to skip (contracts, paystubs, raw binaries)
SKIP_FOLDERS = {
    '03_HR_Vertraege_und_Administration',
    '04_Lohnabrechnungen',
    '05_HR_Werkstudent_Administration',
    '06_Original_Backups_OneNote',
    '.git', '.obsidian', '__pycache__', '.specify'
}

def get_file_hash(path):
    """Computes quick MD5 hash of first 64KB + file size for fast change detection."""
    try:
        h = hashlib.md5()
        size = os.path.getsize(path)
        h.update(str(size).encode())
        with open(path, "rb") as f:
            chunk = f.read(65536)
            h.update(chunk)
        return h.hexdigest()
    except Exception:
        return ""

def load_registry():
    if os.path.exists(REGISTRY_PATH):
        try:
            with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[!] Warning: Could not read registry ({e}). Starting fresh.")
    return {
        "version": "1.0",
        "created_at": datetime.now().isoformat(),
        "last_updated": datetime.now().isoformat(),
        "total_files": 0,
        "processed_files": 0,
        "total_chars_extracted": 0,
        "files": {}
    }

def save_registry(registry):
    registry["last_updated"] = datetime.now().isoformat()
    registry["total_files"] = len(registry["files"])
    registry["processed_files"] = sum(1 for f in registry["files"].values() if f.get("status") == "processed")
    registry["total_chars_extracted"] = sum(f.get("extracted_chars", 0) for f in registry["files"].values())
    os.makedirs(os.path.dirname(REGISTRY_PATH), exist_ok=True)
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)

def scan_workspace():
    print("=" * 70)
    print("🔍 SCANNING WORKSPACE FOR KNOWLEDGE DOCUMENTS...")
    print("=" * 70)
    
    registry = load_registry()
    existing_files = registry.get("files", {})
    
    pillars = ["01_SSB", "04_DC1", "02_Master", "03_Bachelor", "00_Aktuelle_Bewerbungsunterlagen"]
    found_count = 0
    new_count = 0
    
    for pillar in pillars:
        pillar_dir = os.path.join(BASE_DIR, pillar)
        if not os.path.exists(pillar_dir):
            continue
            
        for root, dirs, files in os.walk(pillar_dir):
            # Prune skipped directories
            dirs[:] = [d for d in dirs if d not in SKIP_FOLDERS and not d.startswith(".")]
            
            rel_folder = os.path.relpath(root, BASE_DIR)
            
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext not in EXTRACTABLE_EXTENSIONS:
                    continue
                    
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, BASE_DIR)
                found_count += 1
                
                if rel_path not in existing_files:
                    size = os.path.getsize(full_path)
                    fhash = get_file_hash(full_path)
                    existing_files[rel_path] = {
                        "rel_path": rel_path,
                        "filename": f,
                        "ext": ext,
                        "size_bytes": size,
                        "pillar": pillar,
                        "sub_folder": rel_folder,
                        "hash": fhash,
                        "status": "pending",
                        "extracted_chars": 0,
                        "target_note": "",
                        "discovered_at": datetime.now().isoformat(),
                        "processed_at": ""
                    }
                    new_count += 1
                    
    registry["files"] = existing_files
    save_registry(registry)
    
    print(f"\n[OK] Scan completed successfully!")
    print(f"     Total Extractable Documents in Registry: {len(existing_files)}")
    print(f"     New Documents Added: {new_count}")
    print(f"     Processed: {registry['processed_files']}")
    print(f"     Pending: {len(existing_files) - registry['processed_files']}")

def print_status():
    registry = load_registry()
    files = registry.get("files", {})
    total = len(files)
    processed = sum(1 for f in files.values() if f.get("status") == "processed")
    chars = sum(f.get("extracted_chars", 0) for f in files.values())
    
    print("=" * 70)
    print("📊 KNOWLEDGE INGESTION REGISTRY STATUS REPORT")
    print("=" * 70)
    print(f"Total Tracked Documents:   {total}")
    print(f"Fully Processed / Ingested: {processed} ({processed/total*100:.1f}%)" if total else "No files")
    print(f"Pending Extraction:        {total - processed}")
    print(f"Total Characters Extracted:{chars:,} chars (~{int(chars/4):,} tokens)")
    
    # Pillar breakdown
    pillar_stats = {}
    for f in files.values():
        p = f.get("pillar", "Other")
        stat = pillar_stats.setdefault(p, {"total": 0, "processed": 0, "chars": 0})
        stat["total"] += 1
        if f.get("status") == "processed":
            stat["processed"] += 1
            stat["chars"] += f.get("extracted_chars", 0)
            
    print("\nStatus by Knowledge Pillar:")
    for p, s in sorted(pillar_stats.items()):
        pct = (s["processed"] / s["total"] * 100) if s["total"] else 0
        print(f"  {p:<32}: {s['processed']:>4} / {s['total']:>4} ({pct:>5.1f}%) | {s['chars']:>10,} chars")
    print("=" * 70)

# ==============================================================================
# BATCH 1: PILLAR 04 (DATACENTER ONE / ITIL 4 SERVICE OPERATIONS)
# ==============================================================================

def ingest_batch_dc1():
    print("=" * 70)
    print("🚀 STARTING PILLAR 04 (DATACENTER ONE) FULLTEXT HARVESTING")
    print("=" * 70)
    
    registry = load_registry()
    files = registry.get("files", {})
    
    # 1. Colocation & Network Incident Reports
    dc1_incidents = [f for f in files.values() if f["pillar"] == "04_DC1" and "01_Incident_Management_Reports" in f["rel_path"]]
    print(f"\n[1/3] Processing {len(dc1_incidents)} DC1 Incident Management Reports & Post-Mortems...")
    
    incident_blocks = []
    processed_incident_files = []
    
    for item in sorted(dc1_incidents, key=lambda x: x["filename"]):
        fpath = os.path.join(BASE_DIR, item["rel_path"])
        res = extract_document(fpath)
        if res["success"] and res["text"]:
            fname = item["filename"]
            incident_blocks.append(f"""### 📑 Incident Report: `{fname}`
- **Datei:** `{item["rel_path"]}`
- **Umfang:** {res.get("num_pages", 1)} Seiten | {res["chars"]:,} Zeichen

{res["text"]}
""")
            item["status"] = "processed"
            item["extracted_chars"] = res["chars"]
            item["target_note"] = "DC1_ITIL4_Incident_Reports_PostMortems_Volltext.md"
            item["processed_at"] = datetime.now().isoformat()
            processed_incident_files.append(fname)
            print(f"  [+] Extracted: {fname} ({res['chars']:,} chars)")

    if incident_blocks:
        note_target = os.path.join(VAULT_DIR, "03_SAP_EnterpriseArchitecture", "DC1_ITIL4_Incident_Reports_PostMortems_Volltext.md")
        full_content = f"""---
id: dc1-itil4-incident-reports-postmortems
title: "DC1 ITIL 4 Incident Reports & Root-Cause-Analysen (Volltext-Archiv)"
type: concept
domain: datacenter-operations
status: verified
summary: "Volltext-Dokumentation aller authentischen Datacenter One Incident Reports (Colocation, USV/Klimatechnik, Colo Connect Glasfaser-Links, BGP-Routing, MTTR & Post-Mortems)."
tags:
  - datacenter_one
  - itil4
  - incident_management
  - root_cause_analysis
  - network_operations
  - prtg_monitoring
aliases:
  - DC1 Incident Reports
  - ITIL 4 Post-Mortems
  - Colocation Störungsberichte
last_updated: "{datetime.now().strftime('%Y-%m-%d')}"
---

# 🏢 Datacenter One | ITIL 4 Incident Reports & Root-Cause-Analysen (Volltext)

> [!SUMMARY] **ITIL 4 Service Operations Archiv (Datacenter One INOC)**
> Authentische Dokumentation realer Rechenzentrums- und Netzwerkstörungen im 24/7 INOC-Leitstand unter Helmut Schmidpeter.
> Behandelt Ursachenanalysen (USV-Umschaltungen, Klimaanlagen-Kompressorausfälle, Carrier-Glasfaser-Trassenschäden, BGP-Flapping), Sofortmaßnahmen, Ticket-Workflows (Jira Service Desk) und präventive Problem-Management-Korrekturen.

## 📋 Übersicht der erfassten Störungsberichte ({len(processed_incident_files)} Dokumente)
| Incident-ID / Datei | Kategorie | Format | Extrahierte Zeichen |
|---|---|:---:|:---:|
""" + "\n".join([f"| `{f}` | ITIL Incident Management | PDF/DOCX | Dokumentiert |" for f in processed_incident_files]) + """

---

## 📜 Volltext-Transkripte der Incident Reports

""" + "\n\n---\n\n".join(incident_blocks)

        with open(note_target, "w", encoding="utf-8") as f:
            f.write(full_content)
        print(f"  [OK] Saved Master Dossier: {note_target}")

    # 2. Hardware Lifecycle Management & Rollout
    dc1_hlm = [f for f in files.values() if f["pillar"] == "04_DC1" and "01_Hardware_Lifecycle_Management" in f["rel_path"]]
    print(f"\n[2/3] Processing {len(dc1_hlm)} DC1 Hardware Lifecycle Management & Rollout-Pläne...")
    
    hlm_blocks = []
    processed_hlm_files = []
    
    for item in sorted(dc1_hlm, key=lambda x: x["filename"]):
        fpath = os.path.join(BASE_DIR, item["rel_path"])
        res = extract_document(fpath)
        if res["success"] and res["text"]:
            fname = item["filename"]
            hlm_blocks.append(f"""### 💻 HLM-Dokument: `{fname}`
- **Datei:** `{item["rel_path"]}`
- **Extrahierte Zeichen:** {res["chars"]:,} Zeichen

{res["text"]}
""")
            item["status"] = "processed"
            item["extracted_chars"] = res["chars"]
            item["target_note"] = "DC1_Hardware_Lifecycle_Management_Fahrplan_Volltext.md"
            item["processed_at"] = datetime.now().isoformat()
            processed_hlm_files.append(fname)
            print(f"  [+] Extracted: {fname} ({res['chars']:,} chars)")

    if hlm_blocks:
        hlm_target = os.path.join(VAULT_DIR, "03_SAP_EnterpriseArchitecture", "DC1_Hardware_Lifecycle_Management_Fahrplan_Volltext.md")
        hlm_content = f"""---
id: dc1-hardware-lifecycle-management-fahrplan
title: "DC1 Hardware Lifecycle Management & Rollout-Fahrplan (Volltext)"
type: concept
domain: datacenter-operations
status: verified
summary: "Volltext-Dokumentation des Hardware Lifecycle Managements (HLM) bei Datacenter One: Dell PoC, Fahrplan Notebookaustausch, Asset-Tracking und Visio-Prozesse."
tags:
  - datacenter_one
  - hardware_lifecycle
  - rollout
  - asset_management
  - process_design
aliases:
  - DC1 HLM Volltext
  - Hardware Lifecycle Fahrplan
  - Dell Notebookaustausch
last_updated: "{datetime.now().strftime('%Y-%m-%d')}"
---

# 💻 Datacenter One | Hardware Lifecycle Management & Rollout-Fahrplan

> [!SUMMARY] **Hardware-Rollout & Lifecycle-Steuerung**
> Volltext-Dokumentation der Modernisierung und des Austauschs der IT-Arbeitsplatzinfrastruktur bei Datacenter One.
> Beinhaltet die Gesamtvorgehensweise, Proof-of-Concept (Dell PoC), Inventarisierung, Benutzerübergabe und Asset-Entsorgung.

## 📋 Enthaltene Dokumente ({len(processed_hlm_files)} Artefakte)
""" + "\n".join([f"- `{f}`" for f in processed_hlm_files]) + """

---

## 📜 Volltext-Transkripte der HLM-Konzepte

""" + "\n\n---\n\n".join(hlm_blocks)

        with open(hlm_target, "w", encoding="utf-8") as f:
            f.write(hlm_content)
        print(f"  [OK] Saved Master Dossier: {hlm_target}")

    # 3. Carriermanagement & TOGAF
    dc1_carrier = [f for f in files.values() if f["pillar"] == "04_DC1" and ("02_Carriermanagement" in f["rel_path"] or "TOGAF" in f["rel_path"] or "Monitoring" in f["rel_path"])]
    print(f"\n[3/3] Processing {len(dc1_carrier)} DC1 Carrier Management, SOPs & TOGAF Decks...")
    
    carrier_blocks = []
    processed_carrier_files = []
    
    for item in sorted(dc1_carrier, key=lambda x: x["filename"]):
        fpath = os.path.join(BASE_DIR, item["rel_path"])
        res = extract_document(fpath)
        if res["success"] and res["text"]:
            fname = item["filename"]
            carrier_blocks.append(f"""### 🌐 Dokument: `{fname}`
- **Datei:** `{item["rel_path"]}`
- **Extrahierte Zeichen:** {res["chars"]:,} Zeichen

{res["text"]}
""")
            item["status"] = "processed"
            item["extracted_chars"] = res["chars"]
            item["target_note"] = "DC1_Carriermanagement_SOPs_TOGAF_Volltext.md"
            item["processed_at"] = datetime.now().isoformat()
            processed_carrier_files.append(fname)
            print(f"  [+] Extracted: {fname} ({res['chars']:,} chars)")

    if carrier_blocks:
        carrier_target = os.path.join(VAULT_DIR, "03_SAP_EnterpriseArchitecture", "DC1_Carriermanagement_SOPs_TOGAF_Volltext.md")
        carrier_content = f"""---
id: dc1-carriermanagement-sops-togaf
title: "DC1 Carrier Management, SOPs & TOGAF Architektur (Volltext)"
type: concept
domain: datacenter-operations
status: verified
summary: "Volltext-Dokumentation des Carrier-Managements im INOC (SLA-Tracking, Dark Fiber, Leitungsanbindung), Monitoring-SOPs und TOGAF Enterprise Architecture Decks."
tags:
  - datacenter_one
  - carrier_management
  - togf9
  - sops
  - network_architecture
aliases:
  - DC1 Carrier Management
  - INOC SOPs
  - TOGAF DC1
last_updated: "{datetime.now().strftime('%Y-%m-%d')}"
---

# 🌐 Datacenter One | Carrier Management, SOPs & TOGAF Architektur

> [!SUMMARY] **Carrier-Steuerung & Architektur-Modellierung**
> Volltext-Konzepte zur Carrier-Anbindung, SLA-Überwachung, Confluence-SOPs und Anwendung des TOGAF Architecture Development Method (ADM) Frameworks auf Colocation-Rechenzentren.

## 📋 Enthaltene Dokumente ({len(processed_carrier_files)} Artefakte)
""" + "\n".join([f"- `{f}`" for f in processed_carrier_files]) + """

---

## 📜 Volltext-Transkripte

""" + "\n\n---\n\n".join(carrier_blocks)

        with open(carrier_target, "w", encoding="utf-8") as f:
            f.write(carrier_content)
        print(f"  [OK] Saved Master Dossier: {carrier_target}")

    save_registry(registry)
    print("\n[OK] PILLAR 04 (DC1) HARVESTING COMPLETE!")

# ==============================================================================
# BATCH 2: PILLAR 01 SSB TP5 STEERING BOARD & PMO GOVERNANCE
# ==============================================================================

def ingest_batch_ssb_steering():
    print("=" * 70)
    print("🚀 STARTING PILLAR 01 (SSB) STEERING BOARD & PMO HARVESTING")
    print("=" * 70)
    
    registry = load_registry()
    files = registry.get("files", {})
    
    sb_files = [f for f in files.values() if f["pillar"] == "01_SSB" and "02_Steering_Board_Lenkungsausschuss" in f["rel_path"]]
    print(f"\nProcessing {len(sb_files)} Steering Board (Lenkungskreis) Presentations & Protocols...")
    
    sb_blocks = []
    processed_sb = []
    
    for item in sorted(sb_files, key=lambda x: x["filename"]):
        fpath = os.path.join(BASE_DIR, item["rel_path"])
        res = extract_document(fpath)
        if res["success"] and res["text"]:
            fname = item["filename"]
            sb_blocks.append(f"""### 🏛️ Steering Board: `{fname}`
- **Datei:** `{item["rel_path"]}`
- **Extrahierte Zeichen:** {res["chars"]:,} Zeichen

{res["text"]}
""")
            item["status"] = "processed"
            item["extracted_chars"] = res["chars"]
            item["target_note"] = "SSB_TP5_Steering_Board_Lenkungsausschuss_Volltext.md"
            item["processed_at"] = datetime.now().isoformat()
            processed_sb.append(fname)
            print(f"  [+] Extracted: {fname} ({res['chars']:,} chars)")

    if sb_blocks:
        sb_target = os.path.join(VAULT_DIR, "03_SAP_EnterpriseArchitecture", "SSB_TP5_Steering_Board_Lenkungsausschuss_Volltext.md")
        sb_content = f"""---
id: ssb-tp5-steering-board-lenkungsausschuss
title: "SSB TP5 Steering Board & Lenkungsausschuss (Volltext-Archiv)"
type: hub
domain: sap-transformation
status: verified
summary: "Volltext-Archiv aller 26 Lenkungsausschuss-Präsentationen und C-Level Beschlussvorlagen von Gesamtprojektleiter Roland Nowak und IT-Leiter Dietmar Fillinger."
tags:
  - ssb
  - steering_board
  - c_level_governance
  - sap4ssb
  - pmo
  - roland_nowak
aliases:
  - SSB Steering Board Volltext
  - Lenkungsausschuss SAP4SSB
  - C-Level Reporting Volltext
last_updated: "{datetime.now().strftime('%Y-%m-%d')}"
---

# 🏛️ SSB TP5 | Steering Board & Lenkungsausschuss (Volltext-Archiv)

> [!SUMMARY] **C-Level Multiprojekt-Governance (SSB AG)**
> Vollständige Sammlung aller strategischen Lenkungskreis-Präsentationen, Meilenstein-Freigaben, Ampelberichte (Status Rot/Gelb/Grün), Budget-Trackings und Eskalationsentscheidungen im Großprojekt SAP4SSB.
> Beinhaltet die Entscheidungen zu Cutover, Cut-off, Parallelläufen, S/4HANA Private Cloud Sizing und Betriebsvereinbarungen.

## 📋 Enthaltene Lenkungskreis-Sitzungen ({len(processed_sb)} Decks)
| Sitzung / Präsentationsdatei | Status | Extrahierter Volltext |
|---|:---:|:---:|
""" + "\n".join([f"| `{f}` | Genehmigt / Archiviert | Vorhanden |" for f in processed_sb]) + """

---

## 📜 Volltext-Transkripte der Steering Board Sitzungen

""" + "\n\n---\n\n".join(sb_blocks)

        with open(sb_target, "w", encoding="utf-8") as f:
            f.write(sb_content)
        print(f"  [OK] Saved Master Dossier: {sb_target}")

    save_registry(registry)
    print("\n[OK] SSB STEERING BOARD HARVESTING COMPLETE!")

# ==============================================================================
# BATCH 3: PILLAR 01 SSB FACHSTREAMS (SD, CO, FI, GRANTS, EHS, MM)
# ==============================================================================

def ingest_batch_ssb_fachstreams():
    print("=" * 70)
    print("🚀 STARTING PILLAR 01 (SSB) FACHSTREAMS HARVESTING")
    print("=" * 70)
    
    registry = load_registry()
    files = registry.get("files", {})
    
    streams = [
        ("Stream_CO_Controlling", "SSB_Fachstream_CO_Controlling_Volltext.md", "sap-transformation", "Kostenstellen, Profit Center & Innenaufträge"),
        ("Stream_FI_Finanzwesen", "SSB_Fachstream_FI_Finanzwesen_Volltext.md", "sap-transformation", "Hauptbuch, Debitoren/Kreditoren & Anlagenbuchhaltung"),
        ("Stream_Grants_Management_GM", "SSB_Fachstream_Grants_Management_Volltext.md", "sap-transformation", "Öffentliche Zuschüsse, LGVFG & Drittmittel"),
        ("Stream_SD_Vertrieb_PATRIS", "SSB_Fachstream_SD_Vertrieb_PATRIS_Volltext.md", "sap-transformation", "Ticketvertrieb, PATRIS-Subsystem & Erlösaufteilung"),
        ("Stream_Sustainability_EHS", "SSB_Fachstream_Sustainability_CSRD_EHS_Volltext.md", "sap-transformation", "Gefahrstoffe, CSRD & Nachhaltigkeitsberichterstattung"),
        ("Stream_MM_Materialwirtschaft", "SSB_Fachstream_MM_Materialwirtschaft_Volltext.md", "sap-transformation", "Bestellwesen, Lagerverwaltung & Ariba-Anbindung")
    ]
    
    for stream_folder, target_note_name, domain, desc in streams:
        stream_files = [f for f in files.values() if f["pillar"] == "01_SSB" and stream_folder in f["rel_path"]]
        print(f"\nProcessing {len(stream_files)} files in {stream_folder} ({desc})...")
        
        blocks = []
        processed_files = []
        
        for item in sorted(stream_files, key=lambda x: x["filename"]):
            fpath = os.path.join(BASE_DIR, item["rel_path"])
            res = extract_document(fpath)
            if res["success"] and res["text"]:
                fname = item["filename"]
                blocks.append(f"""### 📑 Dokument: `{fname}`
- **Datei:** `{item["rel_path"]}`
- **Extrahierte Zeichen:** {res["chars"]:,} Zeichen

{res["text"]}
""")
                item["status"] = "processed"
                item["extracted_chars"] = res["chars"]
                item["target_note"] = target_note_name
                item["processed_at"] = datetime.now().isoformat()
                processed_files.append(fname)
                print(f"  [+] Extracted: {fname} ({res['chars']:,} chars)")
                
        if blocks:
            note_target = os.path.join(VAULT_DIR, "03_SAP_EnterpriseArchitecture", target_note_name)
            slug = target_note_name.replace(".md", "").lower().replace("_", "-")
            title_clean = target_note_name.replace(".md", "").replace("_", " ")
            
            content = f"""---
id: {slug}
title: "{title_clean}"
type: concept
domain: {domain}
status: verified
summary: "Volltext-Archiv des Fachstreams {stream_folder} ({desc}): Original-Konzepte, Workshop-Dokumente und Schnittstellenspezifikationen im Großprojekt SAP4SSB."
tags:
  - ssb
  - sap4ssb
  - {stream_folder.lower()}
  - s4hana
  - solution_design
aliases:
  - {title_clean}
  - {stream_folder}
last_updated: "{datetime.now().strftime('%Y-%m-%d')}"
---

# 🚆 SSB | {title_clean}

> [!SUMMARY] **Fachstream-Archiv: {desc}**
> Umfassende Volltext-Dokumentation aus den Fit-to-Standard Workshops, Fachkonzepten, Customizing-Notizen und Schnittstellenanbindungen für den Stream {stream_folder}.

## 📋 Enthaltene Fachdokumente ({len(processed_files)} Artefakte)
""" + "\n".join([f"- `{f}`" for f in processed_files]) + """

---

## 📜 Volltext-Transkripte der Fachdokumente

""" + "\n\n---\n\n".join(blocks)

            with open(note_target, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  [OK] Saved Master Dossier: {note_target}")

    save_registry(registry)
    print("\n[OK] SSB FACHSTREAMS HARVESTING COMPLETE!")

# ==============================================================================
# BATCH 4: PILLAR 01 SSB TEILPROJEKTE TP1 BIS TP5
# ==============================================================================

def ingest_batch_ssb_teilprojekte():
    print("=" * 70)
    print("🚀 STARTING PILLAR 01 (SSB) TEILPROJEKTE TP1–TP5 HARVESTING")
    print("=" * 70)
    
    registry = load_registry()
    files = registry.get("files", {})
    
    tps = [
        ("TP3_Technische_Prozesse_Instandhaltung", "SSB_TP3_Technische_Instandhaltung_EAM_Volltext.md", "Instandhaltung, EAM, Werkstatt & Mobile Instandhaltung SSAM"),
        ("TP4_IT_Infrastruktur_RISE_Basis", "SSB_TP4_IT_Infrastruktur_RISE_Basis_Volltext.md", "RISE with SAP, Cloud ALM, Schnittstellen, Integration & Basis"),
        ("TP5_Gesamtsteuerung_Architektur", "SSB_TP5_Gesamtsteuerung_Architektur_PMO_Volltext.md", "Multiprojekt-Governance, MS Project Terminplan, CVI & Betriebsrat"),
        ("TP2_Kaufmaennische_Prozesse", "SSB_TP2_Kaufmaennische_Prozesse_Workshops_Volltext.md", "Fit-to-Standard Workshops Kaufmännische Prozesse FI/CO"),
        ("TP1_Change_Management_People", "SSB_TP1_Change_Management_People_Plan_Volltext.md", "Change Enablement, Stakeholder-Dialoge, Enable Now & Schulung")
    ]
    
    for tp_folder, target_note_name, desc in tps:
        tp_files = [f for f in files.values() if f["pillar"] == "01_SSB" and tp_folder in f["rel_path"]]
        print(f"\nProcessing {len(tp_files)} files in {tp_folder} ({desc})...")
        
        blocks = []
        processed_files = []
        
        # Sort by filename
        for item in sorted(tp_files, key=lambda x: x["filename"]):
            fpath = os.path.join(BASE_DIR, item["rel_path"])
            res = extract_document(fpath)
            if res["success"] and res["text"]:
                fname = item["filename"]
                blocks.append(f"""### 📑 Dokument: `{fname}`
- **Datei:** `{item["rel_path"]}`
- **Extrahierte Zeichen:** {res["chars"]:,} Zeichen

{res["text"]}
""")
                item["status"] = "processed"
                item["extracted_chars"] = res["chars"]
                item["target_note"] = target_note_name
                item["processed_at"] = datetime.now().isoformat()
                processed_files.append(fname)
                print(f"  [+] Extracted: {fname} ({res['chars']:,} chars)")
                
        if blocks:
            note_target = os.path.join(VAULT_DIR, "03_SAP_EnterpriseArchitecture", target_note_name)
            slug = target_note_name.replace(".md", "").lower().replace("_", "-")
            title_clean = target_note_name.replace(".md", "").replace("_", " ")
            
            content = f"""---
id: {slug}
title: "{title_clean}"
type: concept
domain: sap-transformation
status: verified
summary: "Volltext-Archiv des Teilprojekts {tp_folder} ({desc}): Original-Dokumente, Workshop-Unterlagen und PMO-Pläne im Großprojekt SAP4SSB."
tags:
  - ssb
  - sap4ssb
  - {tp_folder.lower()}
  - s4hana
  - transformation
aliases:
  - {title_clean}
  - {tp_folder}
last_updated: "{datetime.now().strftime('%Y-%m-%d')}"
---

# 🚆 SSB | {title_clean}

> [!SUMMARY] **Teilprojekt-Archiv: {desc}**
> Umfassende Volltext-Dokumentation aus den Teilprojekt-Deliverables, Abstimmungsrunden und Konzepten für {tp_folder}.

## 📋 Enthaltene Dokumente ({len(processed_files)} Artefakte)
""" + "\n".join([f"- `{f}`" for f in processed_files]) + """

---

## 📜 Volltext-Transkripte der Dokumente

""" + "\n\n---\n\n".join(blocks)

            with open(note_target, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  [OK] Saved Master Dossier: {note_target}")

    save_registry(registry)
    print("\n[OK] SSB TEILPROJEKTE HARVESTING COMPLETE!")

# ==============================================================================
# BATCH 5: PILLAR 01 SSB PMO GOVERNANCE, SEKTVO & ARCHITEKTUR-TOOLS
# ==============================================================================

def ingest_batch_ssb_pmo_governance():
    print("=" * 70)
    print("🚀 STARTING PILLAR 01 (SSB) PMO GOVERNANCE, SEKTVO & TOOLS HARVESTING")
    print("=" * 70)
    
    registry = load_registry()
    files = registry.get("files", {})
    
    batches = [
        (
            "04_Ausschreibung_Vergabe_SektVO",
            "SSB_SektVO_Ausschreibung_Vergabe_Volltext.md",
            "sap-transformation",
            "EU-SektVO Ausschreibung & Vergabe",
            "EU-Bekanntmachungen (2025-OJS075), Vergabeunterlagen, Bewertungsmatrizen Axians/Nagarro, Bieterfragen und Vergabeentscheidungen"
        ),
        (
            "04_Architektur_Methoden_Tools",
            "SSB_Architektur_Methoden_Tools_Volltext.md",
            "sap-transformation",
            "Architektur-Methoden & Tool-Katalog",
            "Datenmigration LTMC, SAP Cloud ALM Migration Tracker, Signavio Prozesshierarchien, Readiness Check Clean Core und Enable Now"
        ),
        (
            "01_Projektleitung_PMO_Masterplan",
            "SSB_PMO_Projektleitung_Masterplan_Volltext.md",
            "sap-transformation",
            "PMO Gesamtsteuerung & Masterplan",
            "Projektsteckbriefe, WBS-Strukturen, Grundlagenschulungen, Ressourcenplanung und operative PMO-Governance"
        )
    ]
    
    for folder_keyword, target_note_name, domain, title_clean, desc in batches:
        match_files = [f for f in files.values() if f["pillar"] == "01_SSB" and folder_keyword in f["rel_path"]]
        print(f"\nProcessing {len(match_files)} files in {folder_keyword} ({title_clean})...")
        
        blocks = []
        processed_files = []
        
        for item in sorted(match_files, key=lambda x: x["filename"]):
            fpath = os.path.join(BASE_DIR, item["rel_path"])
            res = extract_document(fpath)
            if res["success"] and res["text"]:
                fname = item["filename"]
                blocks.append(f"""### 📑 Dokument: `{fname}`
- **Datei:** `{item["rel_path"]}`
- **Extrahierte Zeichen:** {res["chars"]:,} Zeichen

{res["text"]}
""")
                item["status"] = "processed"
                item["extracted_chars"] = res["chars"]
                item["target_note"] = target_note_name
                item["processed_at"] = datetime.now().isoformat()
                processed_files.append(fname)
                print(f"  [+] Extracted: {fname} ({res['chars']:,} chars)")
                
        if blocks:
            note_target = os.path.join(VAULT_DIR, "03_SAP_EnterpriseArchitecture", target_note_name)
            slug = target_note_name.replace(".md", "").lower().replace("_", "-")
            
            content = f"""---
id: {slug}
title: "{title_clean}"
type: concept
domain: {domain}
status: verified
summary: "Volltext-Archiv für {title_clean} ({desc}) im Großprojekt SAP4SSB."
tags:
  - ssb
  - sap4ssb
  - {folder_keyword.lower()}
  - s4hana
  - governance
aliases:
  - {title_clean}
  - {folder_keyword}
last_updated: "{datetime.now().strftime('%Y-%m-%d')}"
---

# 🚆 SSB | {title_clean}

> [!SUMMARY] **Governance-Archiv: {desc}**
> Umfassende Volltext-Dokumentation aus den Originalakten und Arbeitsdokumenten für {folder_keyword}.

## 📋 Enthaltene Dokumente ({len(processed_files)} Artefakte)
""" + "\n".join([f"- `{f}`" for f in processed_files]) + """

---

## 📜 Volltext-Transkripte der Dokumente

""" + "\n\n---\n\n".join(blocks)

            with open(note_target, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  [OK] Saved Master Dossier: {note_target}")

    save_registry(registry)
    print("\n[OK] SSB PMO GOVERNANCE, SEKTVO & TOOLS HARVESTING COMPLETE!")

# ==============================================================================
# BATCH 6: PILLAR 02 MASTERSTUDIUM (AKADEMISCHE DEEP-DIVE PROJEKTE)
# ==============================================================================

def ingest_batch_master_academic():
    print("=" * 70)
    print("🚀 STARTING PILLAR 02 (MASTER) ACADEMIC DEEP-DIVE HARVESTING")
    print("=" * 70)
    
    registry = load_registry()
    files = registry.get("files", {})
    
    master_targets = [
        (
            "Masterarbeit Wirtschaftsinformatik",
            "Master_Masterarbeit_Literatur_Fundierung_Volltext.md",
            "Masterarbeit: Wissenschaftliche Literatur, Codebuch & Forschungsdokumente (Note 1,0)",
            "Volltext der Kern-Literatur, theoretischen Grundlagen (Boundary Resources, Absorptive Capacity, Bimodale IT) und qualitative Inhaltsanalyse nach Mayring"
        ),
        (
            "Seminar Wirtschaftsinformatik 2",
            "Master_Seminar_MRK_Industrie50_Volltext.md",
            "Seminararbeit: Mensch-Roboter-Kollaboration in Industrie 5.0 (Note 1,7)",
            "Systematic Literature Review nach PRISMA-Richtlinien, qualitative Kodierung, Akzeptanzmodelle und Forschungsagenda für Mensch-Roboter-Kollaboration"
        ),
        (
            "Digitale Nachhaltigkeit",
            "Master_Digitale_Nachhaltigkeit_Schmalz_Volltext.md",
            "Fallstudie Digitale Nachhaltigkeit: CSRD-Abfallbilanz J. Schmalz GmbH (Note 1,0)",
            "Volltext der Nachhaltigkeitsberichterstattung, Prozessmodellierung der Ist-Abfallbilanz und PowerShell-basierte Automatisierungskonzepte"
        ),
        (
            "Innovationsmethoden für software- und datenintensive Geschäftsmodelle",
            "Master_ISG_PatentRadar_Klingele_Volltext.md",
            "Praxisprojekt ISG: Digital Venture PatentRadar für Klingele (Note 2,0)",
            "Hybrides Geschäftsmodell (SaaS & Consulting) für KI-gestützte Patentrecherche und BPMN-Prozessmodellierung für die Verpackungsindustrie"
        ),
        (
            "Forschungsmethoden in der Wirtschaftsinformatik",
            "Master_Forschungsmethoden_Algorithm_Aversion_Volltext.md",
            "Forschungsmethoden: Empirische Studie zu Algorithm Aversion (Note 1,7)",
            "Hypothesenentwicklung, empirische Erhebungsdesigns, statistische Auswertungsverfahren und quantitatives Forschungsdesign"
        )
    ]
    
    for folder_keyword, target_note_name, title_clean, desc in master_targets:
        match_files = [f for f in files.values() if f["pillar"] == "02_Master" and folder_keyword in f["rel_path"]]
        note_target = os.path.join(VAULT_DIR, "02_Wirtschaftsinformatik_300ECTS", target_note_name)
        
        if os.path.exists(note_target) and os.path.getsize(note_target) > 10000:
            print(f"\n[i] Note {target_note_name} already exists ({os.path.getsize(note_target):,} bytes). Updating registry and continuing...")
            for item in match_files:
                item["status"] = "processed"
                item["target_note"] = target_note_name
                item["processed_at"] = datetime.now().isoformat()
            save_registry(registry)
            continue

        print(f"\nProcessing {len(match_files)} files in {folder_keyword} ({title_clean})...")
        
        blocks = []
        processed_files = []
        
        for item in sorted(match_files, key=lambda x: x["filename"]):
            fpath = os.path.join(BASE_DIR, item["rel_path"])
            res = extract_document(fpath)
            if res["success"] and res["text"]:
                fname = item["filename"]
                blocks.append(f"""### 📑 Akademisches Dokument: `{fname}`
- **Datei:** `{item["rel_path"]}`
- **Extrahierte Zeichen:** {res["chars"]:,} Zeichen

{res["text"]}
""")
                item["status"] = "processed"
                item["extracted_chars"] = res["chars"]
                item["target_note"] = target_note_name
                item["processed_at"] = datetime.now().isoformat()
                processed_files.append(fname)
                print(f"  [+] Extracted: {fname} ({res['chars']:,} chars)")
                
        if blocks:
            slug = target_note_name.replace(".md", "").lower().replace("_", "-")
            
            content = f"""---
id: {slug}
title: "{title_clean}"
type: concept
domain: academic-curriculum
status: verified
summary: "Volltext-Archiv für {title_clean}: {desc}."
tags:
  - master_of_science
  - academic_research
  - universitaet_stuttgart
  - wirtschaftsinformatik
aliases:
  - {title_clean}
  - {folder_keyword}
last_updated: "{datetime.now().strftime('%Y-%m-%d')}"
---

# 🎓 Master of Science | {title_clean}

> [!SUMMARY] **Akademisches Forschungs- & Projektdossier**
> {desc} an der Universität Stuttgart (M.Sc. Wirtschaftsinformatik | Gesamtnote 1,6).

## 📋 Enthaltene Forschungsartefakte ({len(processed_files)} Dokumente)
""" + "\n".join([f"- `{f}`" for f in processed_files]) + """

---

## 📜 Volltext-Transkripte der wissenschaftlichen Ausarbeitungen

""" + "\n\n---\n\n".join(blocks)

            with open(note_target, "w", encoding="utf-8", errors="replace") as f:
                f.write(content)
            print(f"  [OK] Saved Master Dossier: {note_target}")
            save_registry(registry)

    save_registry(registry)
    print("\n[OK] MASTER ACADEMIC HARVESTING COMPLETE!")

# ==============================================================================
# BATCH 7: PILLAR 03 BACHELORSTUDIUM (BOUNDARY RESOURCES & PRAXISPROJEKTE)
# ==============================================================================

def ingest_batch_bachelor_academic():
    print("=" * 70)
    print("🚀 STARTING PILLAR 03 (BACHELOR) ACADEMIC DEEP-DIVE HARVESTING")
    print("=" * 70)
    
    registry = load_registry()
    files = registry.get("files", {})
    
    bachelor_targets = [
        (
            "Bachelorarbeit Wirtschaftsinformatik",
            "Bachelor_Bachelorarbeit_Boundary_Resources_Volltext.md",
            "Bachelorarbeit: Boundary Resources in Low-Code Plattformen OutSystems & Mendix (Note 1,7)",
            "Volltext der 103-seitigen Bachelorarbeit bei Prof. Herzwurm, Boundary Resource Theory (Ghazawneh & Henfridsson), 14 Boundary Resource Klassen (ABR, DBR, SBR) und Experteninterviews"
        ),
        (
            "Informationssysteme_im_E-Business",
            "Bachelor_EBusiness_Bestnote_1_0_Volltext.md",
            "Informationssysteme im E-Business (Bestnote 1,0 | Prof. Dr. Georg Herzwurm)",
            "Volltext aller Fallstudien, E-Procurement-Konzepte, B2B-Plattformen, EDIFACT, XML-Standards und elektronische Marktplätze"
        ),
        (
            "Informationsverarbeitungspraktikum",
            "Bachelor_IVP_0x539_Wear_Unternehmensanalyse_Volltext.md",
            "IVP: Quantitative Unternehmensanalyse 0x539-Wear GmbH (Note 2,3)",
            "Deckungsbeitragsrechnung, Make-or-Buy Analysen, mehrstufige Divisionskalkulation und Controlling-Fallstudie"
        ),
        (
            "Betriebliche Informationssysteme (WI 1)",
            "Bachelor_WI1_Betriebliche_Informationssysteme_Volltext.md",
            "Betriebliche Informationssysteme WI 1: ERP, SAP-Grundlagen & EPK-Prozessmodellierung",
            "Volltext aller Vorlesungen und Übungen zu ERP-Architekturen, ARIS-Modellierung, SAP R/3 und S/4HANA Vorläufern und Workflow-Management"
        ),
        (
            "Informationsmanagement",
            "Bachelor_Informationsmanagement_Architektur_Volltext.md",
            "Informationsmanagement: Strategisches IM, IT-Governance & Informationsarchitekturen",
            "Volltext der Module zu Informationslogistik, EAM-Grundlagen, ITIL-Services und strategischem IT-Management"
        )
    ]
    
    for folder_keyword, target_note_name, title_clean, desc in bachelor_targets:
        match_files = [f for f in files.values() if f["pillar"] == "03_Bachelor" and folder_keyword in f["rel_path"]]
        note_target = os.path.join(VAULT_DIR, "02_Wirtschaftsinformatik_300ECTS", target_note_name)
        
        if os.path.exists(note_target) and os.path.getsize(note_target) > 10000:
            print(f"\n[i] Note {target_note_name} already exists ({os.path.getsize(note_target):,} bytes). Updating registry and continuing...")
            for item in match_files:
                item["status"] = "processed"
                item["target_note"] = target_note_name
                item["processed_at"] = datetime.now().isoformat()
            save_registry(registry)
            continue

        print(f"\nProcessing {len(match_files)} files in {folder_keyword} ({title_clean})...")
        
        blocks = []
        processed_files = []
        
        for item in sorted(match_files, key=lambda x: x["filename"]):
            fpath = os.path.join(BASE_DIR, item["rel_path"])
            res = extract_document(fpath)
            if res["success"] and res["text"]:
                fname = item["filename"]
                blocks.append(f"""### 📑 Bachelor-Dokument: `{fname}`
- **Datei:** `{item["rel_path"]}`
- **Extrahierte Zeichen:** {res["chars"]:,} Zeichen

{res["text"]}
""")
                item["status"] = "processed"
                item["extracted_chars"] = res["chars"]
                item["target_note"] = target_note_name
                item["processed_at"] = datetime.now().isoformat()
                processed_files.append(fname)
                print(f"  [+] Extracted: {fname} ({res['chars']:,} chars)")
                
        if blocks:
            slug = target_note_name.replace(".md", "").lower().replace("_", "-")
            
            content = f"""---
id: {slug}
title: "{title_clean}"
type: concept
domain: academic-curriculum
status: verified
summary: "Volltext-Archiv für {title_clean}: {desc}."
tags:
  - bachelor_of_science
  - academic_research
  - universitaet_stuttgart
  - wirtschaftsinformatik
aliases:
  - {title_clean}
  - {folder_keyword}
last_updated: "{datetime.now().strftime('%Y-%m-%d')}"
---

# 🏛️ Bachelor of Science | {title_clean}

> [!SUMMARY] **Bachelor Forschungs- & Fallstudiendossier**
> {desc} an der Universität Stuttgart (B.Sc. Wirtschaftsinformatik).

## 📋 Enthaltene Dokumente ({len(processed_files)} Artefakte)
""" + "\n".join([f"- `{f}`" for f in processed_files]) + """

---

## 📜 Volltext-Transkripte der wissenschaftlichen Arbeiten

""" + "\n\n---\n\n".join(blocks)

            with open(note_target, "w", encoding="utf-8", errors="replace") as f:
                f.write(content)
            print(f"  [OK] Saved Master Dossier: {note_target}")
            save_registry(registry)

    save_registry(registry)
    print("\n[OK] BACHELOR ACADEMIC HARVESTING COMPLETE!")

# ==============================================================================
# GENERIC TARGET INGESTION ENGINE
# ==============================================================================

def ingest_generic_targets(targets, batch_title):
    print("=" * 70)
    print(f"🚀 STARTING BATCH: {batch_title}")
    print("=" * 70)
    
    registry = load_registry()
    files = registry.get("files", {})
    
    for target in targets:
        pillar = target["pillar"]
        target_note_name = target["target_note_name"]
        title_clean = target["title_clean"]
        desc = target["desc"]
        subfolder = target.get("subfolder", "02_Wirtschaftsinformatik_300ECTS")
        folder_keywords = target.get("folder_keywords", [])
        is_catchall = target.get("is_catchall", False)
        
        note_target = os.path.join(VAULT_DIR, subfolder, target_note_name)
        
        # Match pending files
        match_files = []
        for item in files.values():
            if item.get("pillar") != pillar:
                continue
            if item.get("status") != "pending":
                continue
            
            if is_catchall:
                match_files.append(item)
            elif isinstance(folder_keywords, str):
                if folder_keywords.lower() in item["rel_path"].lower():
                    match_files.append(item)
            elif isinstance(folder_keywords, list):
                if any(kw.lower() in item["rel_path"].lower() for kw in folder_keywords):
                    match_files.append(item)
        
        if not match_files:
            print(f"\n[i] No pending files for {title_clean} ({target_note_name}).")
            continue

        print(f"\nProcessing {len(match_files)} pending files for {title_clean} ({target_note_name})...")
        
        blocks = []
        processed_files = []
        
        existing_header = ""
        existing_blocks_text = ""
        if os.path.exists(note_target):
            try:
                with open(note_target, "r", encoding="utf-8", errors="replace") as ef:
                    existing_content = ef.read()
                    if "## 📜 Volltext-Transkripte" in existing_content:
                        parts = existing_content.split("## 📜 Volltext-Transkripte")
                        existing_header = parts[0]
                        existing_blocks_text = ("## 📜 Volltext-Transkripte" + parts[1]).strip()
            except Exception:
                pass

        for idx, item in enumerate(sorted(match_files, key=lambda x: x["filename"]), 1):
            fpath = os.path.join(BASE_DIR, item["rel_path"])
            fname = item["filename"]
            
            if not os.path.exists(fpath):
                item["status"] = "processed"
                item["extracted_chars"] = 0
                item["processed_at"] = datetime.now().isoformat()
                item["target_note"] = target_note_name
                print(f"  [-] File not found on disk, marked processed: {item['rel_path']}")
                continue

            res = extract_document(fpath)
            
            if res.get("success") and res.get("text"):
                raw_text = res["text"]
                clean_res_text = re.sub(r'^#\s+', '#### ', raw_text, flags=re.MULTILINE)
                clean_res_text = re.sub(r'^##\s+', '#### ', clean_res_text, flags=re.MULTILINE)
                clean_res_text = clean_res_text.encode('utf-8', 'replace').decode('utf-8')
                
                blocks.append(f"""### 📑 Dokument: `{fname}`
- **Datei:** `{item["rel_path"]}`
- **Extrahierte Zeichen:** {res["chars"]:,} Zeichen

{clean_res_text}
""")
                item["status"] = "processed"
                item["extracted_chars"] = res["chars"]
                item["target_note"] = target_note_name
                item["processed_at"] = datetime.now().isoformat()
                processed_files.append(fname)
                print(f"  [{idx}/{len(match_files)}] Extracted: {fname} ({res['chars']:,} chars)")
            else:
                item["status"] = "processed"
                item["extracted_chars"] = 0
                item["target_note"] = target_note_name
                item["processed_at"] = datetime.now().isoformat()
                processed_files.append(fname)
                print(f"  [{idx}/{len(match_files)}] Extracted 0 chars (empty/skipped): {fname}")
                
            if idx % 20 == 0:
                save_registry(registry)

        if blocks:
            slug = target_note_name.replace(".md", "").lower().replace("_", "-")
            domain_tag = "academic-curriculum"
            h1_icon = "🏛️"
            if pillar == "01_SSB":
                domain_tag = "sap-transformation"
                h1_icon = "🚆"
            elif pillar in ["00_Aktuelle_Bewerbungsunterlagen", "04_DC1"]:
                domain_tag = "career-pmo"
                h1_icon = "💼"

            if existing_blocks_text:
                updated_content = existing_blocks_text + "\n\n---\n\n" + "\n\n---\n\n".join(blocks)
                if existing_header:
                    content = existing_header + "\n\n" + updated_content
                else:
                    content = updated_content
            else:
                content = f"""---
id: {slug}
title: "{title_clean}"
type: concept
domain: {domain_tag}
status: verified
summary: "Volltext-Archiv für {title_clean}: {desc}."
tags:
  - {domain_tag.replace('-', '_')}
  - academic_research
  - universitaet_stuttgart
  - wirtschaftsinformatik
aliases:
  - {title_clean}
last_updated: "{datetime.now().strftime('%Y-%m-%d')}"
---

# {h1_icon} {title_clean}

> [!SUMMARY] **Forschungs- & Dokumentendossier**
> {desc}.

## 📋 Enthaltene Dokumente ({len(processed_files)} Artefakte)
""" + "\n".join([f"- `{f}`" for f in processed_files]) + """

---

## 📜 Volltext-Transkripte der Dokumente

""" + "\n\n---\n\n".join(blocks)

            os.makedirs(os.path.dirname(note_target), exist_ok=True)
            with open(note_target, "w", encoding="utf-8", errors="replace") as f:
                f.write(content)
            print(f"  [OK] Saved Master Dossier: {note_target} ({len(blocks)} blocks, {os.path.getsize(note_target):,} bytes)")
            save_registry(registry)

    save_registry(registry)
    print(f"\n[OK] BATCH '{batch_title}' COMPLETE!")

# ==============================================================================
# BATCH 8: PILLAR 02 MASTER COURSES (ALLE VERBLEIBENDEN 807 DATEIEN)
# ==============================================================================

def ingest_batch_master_courses():
    targets = [
        {
            "pillar": "02_Master",
            "subfolder": "02_Wirtschaftsinformatik_300ECTS",
            "target_note_name": "Master_Cloud_Computing_Service_Management_Volltext.md",
            "title_clean": "Master: Cloud Computing, Service Management & Cloud Architecture",
            "desc": "Volltext aller Vorlesungen, Übungen und Fallstudien zu Cloud-Architekturen, SLA-Management, IaaS/PaaS/SaaS und Cloud Governance",
            "folder_keywords": ["Service Management and Cloud Computing, and Evaluation"]
        },
        {
            "pillar": "02_Master",
            "subfolder": "02_Wirtschaftsinformatik_300ECTS",
            "target_note_name": "Master_FPWI_Smart_Service_Blueprinting_Volltext.md",
            "title_clean": "Master: Forschungsprojekte Wirtschaftsinformatik (FPWI) & Smart Services",
            "desc": "Volltext aller Forschungsarbeiten, Projektberichte und Smart Service Blueprints im FPWI-Projekt",
            "folder_keywords": ["Forschungsprojekte in der Wirtschaftsinformatik"]
        },
        {
            "pillar": "02_Master",
            "subfolder": "02_Wirtschaftsinformatik_300ECTS",
            "target_note_name": "Master_AIM_Advanced_Information_Management_Volltext.md",
            "title_clean": "Master: Advanced Information Management (AIM) & Enterprise Information Systems",
            "desc": "Volltext zu Enterprise Content Management, Information Retrieval, Wissensmanagement und Semantic Web",
            "folder_keywords": ["Advanced Information Management"]
        },
        {
            "pillar": "02_Master",
            "subfolder": "02_Wirtschaftsinformatik_300ECTS",
            "target_note_name": "Master_Advanced_Software_Engineering_Volltext.md",
            "title_clean": "Master: Advanced Software Engineering (ASE) & DevOps",
            "desc": "Volltext zu fortgeschrittenen Software-Architekturen, Continuous Integration/Deployment, Microservices und Clean Code",
            "folder_keywords": ["Advanced Software Engineering"]
        },
        {
            "pillar": "02_Master",
            "subfolder": "02_Wirtschaftsinformatik_300ECTS",
            "target_note_name": "Master_AI4IoT_Sensor_Edge_AI_Volltext.md",
            "title_clean": "Master: AI4IoT – Künstliche Intelligenz für das Internet der Dinge & Edge Computing",
            "desc": "Volltext zu IoT-Architekturen, Sensordatenverarbeitung, Edge AI, Time-Series Analytics und Smart Connected Systems",
            "folder_keywords": ["AI4IoT"]
        },
        {
            "pillar": "02_Master",
            "subfolder": "02_Wirtschaftsinformatik_300ECTS",
            "target_note_name": "Master_Software_Architektur_Microservices_Volltext.md",
            "title_clean": "Master: Software-Architektur, Microservices & Entwurfsmuster",
            "desc": "Volltext zu Architekturmustern, Domain-Driven Design (DDD), Modularisierung, API-Design und Qualitätsattributen",
            "folder_keywords": ["Software-Architektur"]
        },
        {
            "pillar": "02_Master",
            "subfolder": "02_Wirtschaftsinformatik_300ECTS",
            "target_note_name": "Master_Applied_AI_Generative_AI_Industrie_Volltext.md",
            "title_clean": "Master: Applied AI & Upcoming Technologies in Enterprise Industries",
            "desc": "Volltext zu industrieller KI-Anwendung, Large Language Models, Generativer KI und industriellen Transformationsprojekten",
            "folder_keywords": ["Applied AI and Upcoming Technologies in Industries"]
        },
        {
            "pillar": "02_Master",
            "subfolder": "02_Wirtschaftsinformatik_300ECTS",
            "target_note_name": "Master_TEUI_Internationale_Unternehmenstaetigkeit_Volltext.md",
            "title_clean": "Master: Theorie und Empirie internationaler Unternehmenstätigkeit (TEUI)",
            "desc": "Volltext zu internationaler Markterschließung, Multichannel-Strategien, OLI-Paradigma und globalen Supply Chains",
            "folder_keywords": ["Theorie und Empirie internationaler Unternehmenstätigkeit"]
        },
        {
            "pillar": "02_Master",
            "subfolder": "02_Wirtschaftsinformatik_300ECTS",
            "target_note_name": "Master_Datenbanken_Informationssysteme_Volltext.md",
            "title_clean": "Master: Datenbanken und Informationssysteme (DBIS) & Data Engineering",
            "desc": "Volltext zu relationalen Datenbanken, NoSQL, Transaktionsmanagement (ACID), Indexierung und Query-Optimierung",
            "folder_keywords": ["Datenbanken und Informationssysteme"]
        },
        {
            "pillar": "02_Master",
            "subfolder": "02_Wirtschaftsinformatik_300ECTS",
            "target_note_name": "Master_Management_IT_Unternehmen_ITIL_COBIT_Volltext.md",
            "title_clean": "Master: Management von IT-Unternehmen, IT-Governance & IT-Strategie",
            "desc": "Volltext zu ITIL 4, COBIT, strategischer IT-Ausrichtung, IT-Servicemanagement und Kennzahlensystemen",
            "folder_keywords": ["Management von IT-Unternehmen"]
        },
        {
            "pillar": "02_Master",
            "subfolder": "02_Wirtschaftsinformatik_300ECTS",
            "target_note_name": "Master_SOM_Service_Operations_Management_Volltext.md",
            "title_clean": "Master: Service Operations Management (SOM) & Warteschlangentheorie",
            "desc": "Volltext zu quantitativer Kapazitätsplanung, stochastischen Prozessen, Warteschlangenmodellen und Service Level Agreements",
            "folder_keywords": ["Service Operations Management"]
        },
        {
            "pillar": "02_Master",
            "subfolder": "02_Wirtschaftsinformatik_300ECTS",
            "target_note_name": "Master_Innovationsmanagement_Plattformen_Volltext.md",
            "title_clean": "Master: Innovationsmanagement, Open Innovation & Digitale Ökosysteme",
            "desc": "Volltext zu Diffusionsmodellen, Lead-User-Methodik, Stage-Gate-Prozessen und Geschäftsmodellinnovationen",
            "folder_keywords": ["Innovationsmanagement"]
        },
        {
            "pillar": "02_Master",
            "subfolder": "02_Wirtschaftsinformatik_300ECTS",
            "target_note_name": "Master_Zusatzmodule_Quantum_SmartCities_AIProto_Volltext.md",
            "title_clean": "Master: Zusatzmodule – Quanteninformatik, Smart Cities, AI Prototyping & Studienorganisation",
            "desc": "Volltext aller interdisziplinären Master-Zusatzmodule zu Quantenalgorithmen, Smart Cities, Rapid Prototyping und Studiennachweisen",
            "folder_keywords": [],
            "is_catchall": True
        }
    ]
    ingest_generic_targets(targets, "PILLAR 02 (MASTER) CURRICULUM COURSES")

# ==============================================================================
# BATCH 9: PILLAR 03 BACHELOR COMPUTER SCIENCE & SOFTWARE ENGINEERING
# ==============================================================================

def ingest_batch_bachelor_cs_se():
    targets = [
        {
            "pillar": "03_Bachelor",
            "subfolder": "02_Wirtschaftsinformatik_300ECTS",
            "target_note_name": "Bachelor_AFS_Automaten_Formale_Sprachen_Theorie_Volltext.md",
            "title_clean": "Bachelor: Automaten und Formale Sprachen, Berechenbarkeit & Komplexität",
            "desc": "Volltext zu regulären Sprachen, Chomsky-Hierarchie, endlichen Automaten, Turing-Maschinen und P-NP-Theorie",
            "folder_keywords": ["Automaten und Formale Sprachen"]
        },
        {
            "pillar": "03_Bachelor",
            "subfolder": "02_Wirtschaftsinformatik_300ECTS",
            "target_note_name": "Bachelor_PSE_Programmierung_Java_OOP_Volltext.md",
            "title_clean": "Bachelor: Programmierung und Softwareentwicklung (PSE) – Java & OOP",
            "desc": "Volltext aller Vorlesungen und Übungen zu objektorientierter Programmierung in Java, Design Patterns und sauberem Code",
            "folder_keywords": ["Programmierung und Software-Entwicklung"]
        },
        {
            "pillar": "03_Bachelor",
            "subfolder": "02_Wirtschaftsinformatik_300ECTS",
            "target_note_name": "Bachelor_Programmentwicklung_Funktional_Logisch_Volltext.md",
            "title_clean": "Bachelor: Programmentwicklung – Funktionale & Logische Programmierung",
            "desc": "Volltext zu Haskell, Prolog, Lambda-Kalkül, Typsystemen, Rekursion und formaler Programmspezifikation",
            "folder_keywords": ["Programmentwicklung"]
        },
        {
            "pillar": "03_Bachelor",
            "subfolder": "02_Wirtschaftsinformatik_300ECTS",
            "target_note_name": "Bachelor_Modellierung_BPMN_UML_Petrinetze_Volltext.md",
            "title_clean": "Bachelor: Modellierung – BPMN, UML, Petrinetze & Geschäftsprozesse",
            "desc": "Volltext zu Prozessmodellierung, BPMN 2.0, ERM, UML-Klassendiagrammen, Petrinetzen und semantischen Datenmodellen",
            "folder_keywords": ["Modellierung"]
        },
        {
            "pillar": "03_Bachelor",
            "subfolder": "02_Wirtschaftsinformatik_300ECTS",
            "target_note_name": "Bachelor_EST_Softwaretechnik_VModell_Scrum_Volltext.md",
            "title_clean": "Bachelor: Einführung in die Softwaretechnik (EST) – V-Modell, Agile & Testing",
            "desc": "Volltext zu V-Modell XT, Scrum, Anforderungsanalyse, Software-Architektur und Software-Qualitätssicherung",
            "folder_keywords": ["Einführung in die Softwaretechnik"]
        },
        {
            "pillar": "03_Bachelor",
            "subfolder": "02_Wirtschaftsinformatik_300ECTS",
            "target_note_name": "Bachelor_MCI_Mensch_Computer_Interaktion_UX_Volltext.md",
            "title_clean": "Bachelor: Mensch-Computer-Interaktion (MCI) – UI/UX, Ergonomie & Usability",
            "desc": "Volltext zu Wahrnehmungspsychologie, Usability Engineering, Heuristischen Evaluationen und User Interface Design",
            "folder_keywords": ["Mensch-Computer-Interaktion"]
        },
        {
            "pillar": "03_Bachelor",
            "subfolder": "02_Wirtschaftsinformatik_300ECTS",
            "target_note_name": "Bachelor_DSA_Datenstrukturen_Algorithmen_Volltext.md",
            "title_clean": "Bachelor: Datenstrukturen und Algorithmen (DSA) – Bäume, Graphen & Sortierung",
            "desc": "Volltext zu asymptotischer Laufzeitanalyse (O-Notation), Such- und Sortieralgorithmen, AVL-Bäumen und Graphentheorie",
            "folder_keywords": ["Datenstrukturen und Algorithmen"]
        },
        {
            "pillar": "03_Bachelor",
            "subfolder": "02_Wirtschaftsinformatik_300ECTS",
            "target_note_name": "Bachelor_SOPRA_Softwarepraktikum_Java_taskMasterPro_Volltext.md",
            "title_clean": "Bachelor: Softwarepraktikum (SOPRA) – Agile Teamentwicklung Java / taskMasterPro",
            "desc": "Volltext zu Scrum-Sprint-Dokumentationen, Architekturspezifikationen und Implementierungsberichten des Teamprojekts taskMasterPro",
            "folder_keywords": ["Softwarepraktikum"]
        }
    ]
    ingest_generic_targets(targets, "PILLAR 03 (BACHELOR) CS & SOFTWARE ENGINEERING")

# ==============================================================================
# BATCH 10: PILLAR 03 BUSINESS, SSB REST & BEWERBUNGSUNTERLAGEN
# ==============================================================================

def ingest_batch_bachelor_business_career():
    targets = [
        {
            "pillar": "03_Bachelor",
            "subfolder": "02_Wirtschaftsinformatik_300ECTS",
            "target_note_name": "Bachelor_Mathematik_Statistik_Methoden_Volltext.md",
            "title_clean": "Bachelor: Mathematik & Statistik für Wirtschaftswissenschaftler – Lineare Algebra, Analysis & Inferenz",
            "desc": "Volltext zu Matrizenrechnung, Optimierung, Wahrscheinlichkeitsräumen, Regressionsanalysen und Hypothesentests",
            "folder_keywords": ["Mathematik für Wirtschaftswissenschaftler", "Statistik I", "Statistik II"]
        },
        {
            "pillar": "03_Bachelor",
            "subfolder": "02_Wirtschaftsinformatik_300ECTS",
            "target_note_name": "Bachelor_GVWL1_Mikrooekonomik_Maerkte_Volltext.md",
            "title_clean": "Bachelor: GVWL 1 – Mikroökonomik, Märkte & Wirtschaftliche Entscheidungen",
            "desc": "Volltext zu Haushalts- und Unternehmenstheorie, Marktformen (Monopol, Oligopol, Polypol) und Spieltheorie",
            "folder_keywords": ["GVWL 1"]
        },
        {
            "pillar": "03_Bachelor",
            "subfolder": "02_Wirtschaftsinformatik_300ECTS",
            "target_note_name": "Bachelor_BWL1_Organisation_Management_Volltext.md",
            "title_clean": "Bachelor: BWL 1 – Organisation, Personalführung & Strategisches Management",
            "desc": "Volltext zu Aufbau- und Ablauforganisation, Führungstheorien, Motivationskonzepten und strategischem Management",
            "folder_keywords": ["BWL 1"]
        },
        {
            "pillar": "03_Bachelor",
            "subfolder": "02_Wirtschaftsinformatik_300ECTS",
            "target_note_name": "Bachelor_GBWL1_Strukturen_BWL_Rechnungswesen_Volltext.md",
            "title_clean": "Bachelor: GBWL 1 – Strukturen der Betriebswirtschaftslehre & Externes Rechnungswesen",
            "desc": "Volltext zu Bilanzierung nach HGB, Buchführung, GuV-Rechnung und betriebswirtschaftlichen Grundfunktionen",
            "folder_keywords": ["GBWL 1"]
        },
        {
            "pillar": "03_Bachelor",
            "subfolder": "02_Wirtschaftsinformatik_300ECTS",
            "target_note_name": "Bachelor_GBWL4_Finanzprozess_Investition_Volltext.md",
            "title_clean": "Bachelor: GBWL 4 – Finanzprozess, Investition, Finanzierung & Unternehmensbewertung",
            "desc": "Volltext zu Kapitalwertmethode, Internem Zinsfuß, Portfolio-Theorie, CAPM und Finanzierungsarten",
            "folder_keywords": ["GBWL 4"]
        },
        {
            "pillar": "03_Bachelor",
            "subfolder": "02_Wirtschaftsinformatik_300ECTS",
            "target_note_name": "Bachelor_Interdisziplinaer_Recht_Management_Volltext.md",
            "title_clean": "Bachelor: Interdisziplinäre Module – Recht, Management, HRM & Studienorganisation",
            "desc": "Volltext zu IT-Recht, Urheberrecht, DSGVO, Dienstleistungscontrolling, Personalmanagement und wissenschaftlichem Arbeiten",
            "folder_keywords": [],
            "is_catchall": True
        },
        {
            "pillar": "01_SSB",
            "subfolder": "03_SAP_EnterpriseArchitecture",
            "target_note_name": "SSB_Gesamtprojekt_S4HANA_Ergaenzungen_Volltext.md",
            "title_clean": "SSB S/4HANA Gesamtprojekt: Ergänzende Projektdokumente, Governance & Fachstreams",
            "desc": "Volltext aller verbleibenden Detaildokumente des Großprojekts SAP4SSB, Vergabeanträge, Prozessprotokolle und Steuerungsinstrumente",
            "folder_keywords": [],
            "is_catchall": True
        },
        {
            "pillar": "00_Aktuelle_Bewerbungsunterlagen",
            "subfolder": "01_Karriere_Bewerbungen",
            "target_note_name": "00_Bewerbungsunterlagen_Master_Volltext.md",
            "title_clean": "Verbindliche Bewerbungsunterlagen, Lebenslauf, Zeugnisse & Profil-Audit",
            "desc": "Volltext aller offiziellen Bewerbungsunterlagen, CV-Versionen, Zeugnisse, Bewerbungstracker und Interviewvorbereitungen",
            "folder_keywords": [],
            "is_catchall": True
        },
        {
            "pillar": "04_DC1",
            "subfolder": "01_Karriere_Bewerbungen",
            "target_note_name": "00_Bewerbungsunterlagen_Master_Volltext.md",
            "title_clean": "Verbindliche Bewerbungsunterlagen, Lebenslauf, Zeugnisse & Profil-Audit",
            "desc": "Volltext aller offiziellen Bewerbungsunterlagen, CV-Versionen, Zeugnisse, Bewerbungstracker und Interviewvorbereitungen",
            "folder_keywords": [],
            "is_catchall": True
        }
    ]
    ingest_generic_targets(targets, "PILLAR 03 BUSINESS, SSB REST & BEWERBUNGSUNTERLAGEN")

# ==============================================================================
# MAIN CLI
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(description="Enterprise Knowledge Harvester & Ingestion Engine")
    parser.add_argument("--scan", action="store_true", help="Scans workspace and builds/updates ingestion registry")
    parser.add_argument("--status", action="store_true", help="Displays current registry ingestion status report")
    parser.add_argument("--batch", type=str, choices=["dc1", "ssb_steering", "ssb_streams", "ssb_tp", "ssb_pmo", "master", "bachelor", "master_courses", "bachelor_cs_se", "bachelor_business_career", "all"], help="Executes a specific ingestion batch")
    
    args = parser.parse_args()
    
    if args.scan:
        scan_workspace()
    elif args.status:
        print_status()
    elif args.batch == "dc1":
        ingest_batch_dc1()
    elif args.batch == "ssb_steering":
        ingest_batch_ssb_steering()
    elif args.batch == "ssb_streams":
        ingest_batch_ssb_fachstreams()
    elif args.batch == "ssb_tp":
        ingest_batch_ssb_teilprojekte()
    elif args.batch == "ssb_pmo":
        ingest_batch_ssb_pmo_governance()
    elif args.batch == "master":
        ingest_batch_master_academic()
    elif args.batch == "bachelor":
        ingest_batch_bachelor_academic()
    elif args.batch == "master_courses":
        ingest_batch_master_courses()
    elif args.batch == "bachelor_cs_se":
        ingest_batch_bachelor_cs_se()
    elif args.batch == "bachelor_business_career":
        ingest_batch_bachelor_business_career()
    elif args.batch == "all":
        scan_workspace()
        ingest_batch_dc1()
        ingest_batch_ssb_steering()
        ingest_batch_ssb_fachstreams()
        ingest_batch_ssb_teilprojekte()
        ingest_batch_ssb_pmo_governance()
        ingest_batch_master_academic()
        ingest_batch_bachelor_academic()
        ingest_batch_master_courses()
        ingest_batch_bachelor_cs_se()
        ingest_batch_bachelor_business_career()
        print_status()
    else:
        # Default behavior: scan and show status
        scan_workspace()
        print_status()

if __name__ == "__main__":
    main()

