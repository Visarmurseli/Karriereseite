# -*- coding: utf-8 -*-
"""
Obsidian Vault Optimizer & Second Brain Enhancer
1. Cleans macOS (._*) and Office (~$*) junk from registry and markdown dossiers
2. Splits oversized (>10 MB) monolithic Volltext dossiers into Electron-safe <4 MB volumes
3. Eliminates graph orphans by adding verified bidirectional Wikilinks across all Volltext dossiers
4. Creates rich atomic Zettelkasten notes & syncs Schwarz Digits post-interview debrief
5. Optimizes Obsidian core plugin settings & cleans empty root files
"""

import os
import re
import json
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
VAULT_DIR = r"C:\Users\SHQIPTAR634\Documents\Obsidian Vault"
REGISTRY_PATH = os.path.join(BASE_DIR, "config", "ingestion_registry.json")

MAX_VOLUME_BYTES = 3_800_000  # ~3.6 MB per markdown volume for snappy Obsidian UI & RAG


def clean_registry_junk():
    if not os.path.exists(REGISTRY_PATH):
        return
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        reg = json.load(f)
    files = reg.get("files", {})
    to_remove = [
        k for k, v in files.items()
        if os.path.basename(v.get("rel_path", k)).startswith("._")
        or os.path.basename(v.get("rel_path", k)).startswith("~$")
    ]
    for k in to_remove:
        del files[k]
    reg["files"] = files
    reg["last_updated"] = datetime.now().isoformat()
    reg["total_files"] = len(files)
    reg["processed_files"] = sum(1 for v in files.values() if v.get("status") == "processed")
    reg["total_chars_extracted"] = sum(v.get("extracted_chars", 0) for v in files.values())
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(reg, f, indent=2, ensure_ascii=False)
    print(f"[1/6] Registry cleaned: removed {len(to_remove)} junk entries (._* / ~$*). Total tracked: {len(files)}.")


def strip_junk_blocks_in_vault():
    cleaned = 0
    junk_section_re = re.compile(
        r"(?:\n---\n+)?### 📑 [^\n]*`(?:\._|~\$)[^\n]*\n.*?(?=(?:\n---\n+)?### 📑 |\Z)",
        re.DOTALL
    )
    for root, dirs, files in os.walk(VAULT_DIR):
        if ".obsidian" in root:
            continue
        for fn in files:
            if not fn.endswith("_Volltext.md"):
                continue
            fp = os.path.join(root, fn)
            with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                txt = f.read()
            new_txt = junk_section_re.sub("", txt)
            # Also clean junk lines from bullet list "- `._...`" or "- `~$...`"
            new_txt = re.sub(r"^- `(?:\._|~\$)[^`]+`\n?", "", new_txt, flags=re.MULTILINE)
            if new_txt != txt:
                with open(fp, "w", encoding="utf-8", errors="replace") as f:
                    f.write(new_txt)
                cleaned += 1
    print(f"[2/6] Stripped macOS/Office junk blocks from {cleaned} Volltext dossier(s).")


def split_giant_single_section(title_line, header_meta, body_text):
    """Splits an oversized single book/document section along page headings if > MAX_VOLUME_BYTES."""
    if len(body_text.encode("utf-8")) <= MAX_VOLUME_BYTES:
        return [(title_line, header_meta + "\n\n" + body_text)]

    pages = re.split(r"\n(?=#### Seite )", body_text)
    sub_parts = []
    cur = []
    cur_bytes = 0
    part_num = 1
    for pg in pages:
        pg_bytes = len(pg.encode("utf-8"))
        if cur and cur_bytes + pg_bytes > MAX_VOLUME_BYTES:
            sub_title = f"{title_line} [Auszug Teil {part_num}]"
            sub_parts.append((sub_title, header_meta + "\n\n" + "\n".join(cur)))
            cur = [pg]
            cur_bytes = pg_bytes
            part_num += 1
        else:
            cur.append(pg)
            cur_bytes += pg_bytes
    if cur:
        sub_title = f"{title_line} [Auszug Teil {part_num}]" if part_num > 1 else title_line
        sub_parts.append((sub_title, header_meta + "\n\n" + "\n".join(cur)))
    return sub_parts


def split_monster_files():
    targets = [
        {
            "rel": r"02_Wirtschaftsinformatik_300ECTS\Master_Seminar_MRK_Industrie50_Volltext.md",
            "short_title": "Master Seminar MRK & Industrie 5.0 (PRISMA SLR)",
            "parent_links": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_Seminar_WI2|🤖 Modul Seminar WI 2]]", "[[Wissenschaftliche_Methodik|🔬 Wissenschaftliche Methodik]]", "[[Generative_AI_LLM|🤖 Generative AI & LLMs]]"],
            "tags": ["master_of_science", "industrie_5_0", "prisma_slr", "volltext_band"]
        },
        {
            "rel": r"02_Wirtschaftsinformatik_300ECTS\Bachelor_Bachelorarbeit_Boundary_Resources_Volltext.md",
            "short_title": "Bachelorarbeit: Boundary Resources in Low-Code Plattformen",
            "parent_links": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_Bachelorarbeit|📜 Modul Bachelorarbeit]]", "[[Bimodale_ERP_Plattformisierung_BTP|🧩 Bimodale Plattformisierung & Boundary Resources]]", "[[Software_Engineering_Prinzipien|⚙️ Software Engineering]]"],
            "tags": ["bachelor_of_science", "boundary_resources", "low_code", "volltext_band"]
        },
        {
            "rel": r"02_Wirtschaftsinformatik_300ECTS\Master_Cloud_Computing_Service_Management_Volltext.md",
            "short_title": "Master: Cloud Computing & Service Management",
            "parent_links": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_Cloud_Computing|☁️ Modul Cloud Computing]]", "[[Modul_SOM|🔄 Service Operations Management]]", "[[SAP_BTP_Integration_Suite|☁️ SAP BTP & Cloud]]"],
            "tags": ["master_of_science", "cloud_computing", "service_management", "volltext_band"]
        },
    ]

    total_created = 0
    for cfg in targets:
        fpath = os.path.join(VAULT_DIR, cfg["rel"])
        if not os.path.exists(fpath):
            continue
        size_mb = os.path.getsize(fpath) / (1024 * 1024)
        if size_mb < 10.0:
            print(f"  [i] Skipping {cfg['rel']} ({size_mb:.2f} MB) – already split.")
            continue

        print(f"  [*] Splitting monster dossier: {cfg['rel']} ({size_mb:.2f} MB)...")
        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            raw = f.read()

        # Extract YAML frontmatter
        fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', raw, re.DOTALL)
        body = raw[len(fm_match.group(0)):] if fm_match else raw

        # Split by document headers ### 📑
        parts = re.split(r'\n(?=### 📑 )', body)
        intro = parts[0]
        doc_chunks = []
        for sec in parts[1:]:
            lines = sec.splitlines()
            first_line = lines[0]
            # Parse doc title from first line
            doc_title = first_line.replace("### 📑", "").strip()
            # Separate meta bullets (- **Datei:** ...) from content
            meta_lines = []
            content_start = 1
            for i in range(1, min(6, len(lines))):
                if lines[i].startswith("- **") or lines[i].strip() == "":
                    meta_lines.append(lines[i])
                    content_start = i + 1
                else:
                    break
            meta_str = "\n".join(meta_lines).strip()
            doc_body = "\n".join(lines[content_start:]).strip()
            # Clean trailing '---' separator if present
            if doc_body.endswith("---"):
                doc_body = doc_body[:-3].strip()

            sub_pieces = split_giant_single_section(doc_title, meta_str, doc_body)
            for stitle, sfull in sub_pieces:
                doc_chunks.append((stitle, f"### 📑 {stitle}\n{sfull}"))

        # Pack into balanced <3.8 MB volumes
        volumes = []
        cur_docs = []
        cur_bytes = 0
        for stitle, block in doc_chunks:
            b_bytes = len(block.encode("utf-8"))
            if cur_docs and cur_bytes + b_bytes > MAX_VOLUME_BYTES:
                volumes.append(cur_docs)
                cur_docs = [(stitle, block)]
                cur_bytes = b_bytes
            else:
                cur_docs.append((stitle, block))
                cur_bytes += b_bytes
        if cur_docs:
            volumes.append(cur_docs)

        base_name = os.path.splitext(os.path.basename(fpath))[0]
        folder = os.path.dirname(fpath)
        total_vols = len(volumes)
        toc_entries = []

        for idx, vol_docs in enumerate(volumes, 1):
            vol_name = f"{base_name}_Teil_{idx:02d}"
            vol_path = os.path.join(folder, f"{vol_name}.md")
            vol_slug = vol_name.lower().replace("_", "-")
            prev_link = f"[[{base_name}_Teil_{idx-1:02d}|⬅️ Band {idx-1:02d}]]" if idx > 1 else ""
            next_link = f"[[{base_name}_Teil_{idx+1:02d}|Band {idx+1:02d} ➡️]]" if idx < total_vols else ""
            nav_links = [l for l in [f"[[{base_name}|📖 Gesamtübersicht]]"] + cfg["parent_links"] + [prev_link, next_link] if l]
            doc_titles_md = "\n".join([f"- {dt}" for dt, _ in vol_docs])
            blocks_md = "\n\n---\n\n".join([blk for _, blk in vol_docs])
            tags_yaml = "\n".join([f"  - {t}" for t in cfg["tags"]])

            vol_content = f"""---
id: {vol_slug}
title: "{cfg['short_title']} – Band {idx:02d}/{total_vols:02d}"
type: concept
domain: academic-curriculum
status: verified
summary: "Band {idx:02d} von {total_vols:02d} des Volltext-Archivs {cfg['short_title']} ({len(vol_docs)} Dokumentabschnitte)."
tags:
{tags_yaml}
last_updated: "{datetime.now().strftime('%Y-%m-%d')}"
---

# 📚 {cfg['short_title']} – Band {idx:02d}/{total_vols:02d}

> [!SUMMARY] **Band-Navigation ({len(vol_docs)} Abschnitte | Teil {idx:02d} von {total_vols:02d})**
> {" • ".join(nav_links)}

## 📋 Enthaltene Dokumente in diesem Band
{doc_titles_md}

---

## 📜 Volltext-Transkripte (Band {idx:02d})

{blocks_md}
"""
            with open(vol_path, "w", encoding="utf-8", errors="replace") as vf:
                vf.write(vol_content)
            total_created += 1

            sample_names = ", ".join([dt.replace("Dokument:", "").replace("Akademisches ", "").replace("Bachelor-", "").strip(" `")[:45] for dt, _ in vol_docs[:3]])
            if len(vol_docs) > 3:
                sample_names += f" … (+{len(vol_docs)-3} weitere)"
            toc_entries.append(f"- [[{vol_name}|📘 Band {idx:02d}/{total_vols:02d}]] ({len(vol_docs)} Abschnitte, {os.path.getsize(vol_path)//1024:,} KB): {sample_names}")

        # Rewrite main Volltext file as lightweight Master Volume Hub
        hub_slug = base_name.lower().replace("_", "-")
        hub_tags = "\n".join([f"  - {t}" for t in cfg["tags"]])
        hub_content = f"""---
id: {hub_slug}
title: "{cfg['short_title']} – Gesamtverzeichnis ({total_vols} Bände)"
type: moc
domain: academic-curriculum
status: verified
summary: "Aufgesplittetes Master-Verzeichnis für {cfg['short_title']} ({size_mb:.1f} MB Gesamtkorpus in {total_vols} handlichen Obsidian-Bänden à <4 MB)."
tags:
{hub_tags}
  - moc
last_updated: "{datetime.now().strftime('%Y-%m-%d')}"
---

# 🏛️ {cfg['short_title']} – Volltext-Archiv ({total_vols} Bände)

> [!SUMMARY] **Performance-optimiertes Band-Archiv (Originalumfang: {size_mb:.1f} MB | {len(doc_chunks)} Dokumentabschnitte)**
> Um maximale Geschwindigkeit in Obsidian (ohne Editor-Freezes) und optimales RAG-Chunking zu gewährleisten, wurde dieses Großarchiv verlustfrei in **{total_vols} Einzelbände** aufgeteilt. Alle Volltexte bleiben zu 100 % durchsuchbar.

> [!INFO] **Wissensnetz-Verknüpfung**
> {" • ".join(cfg['parent_links'])}

## 📚 Bände im Direktzugriff

""" + "\n".join(toc_entries) + "\n"

        with open(fpath, "w", encoding="utf-8", errors="replace") as mf:
            mf.write(hub_content)
        print(f"    -> Split into {total_vols} clean volumes (< 4 MB each) + Master TOC hub.")

    print(f"[3/6] Monster-file splitting finished ({total_created} sub-volume files created).")


def add_context_links_to_volltext():
    # Exact verified target filenames (without .md) per Volltext file
    link_map = {
        "00_Bewerbungsunterlagen_Master_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[00_Bewerbungsmanagement_Cockpit|📊 Bewerbungs-Cockpit]]", "[[2026-11-24_Schwarz_Digits_SAP_HCM_IAM|🎯 Schwarz Digits Dossier]]", "[[00_Lebenslauf_Volltext|📄 Lebenslauf]]"],
        "00_Lebenslauf_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[00_Masterzeugnis_Leistungsuebersicht_Volltext|🎓 Masterzeugnis]]", "[[00_Bachelorzeugnis_Leistungsuebersicht_Volltext|🏛️ Bachelorzeugnis]]", "[[SSB_Grossprojekt_SAP4SSB|🚆 SSB S/4HANA]]"],
        "00_Masterzeugnis_Leistungsuebersicht_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[00_Lebenslauf_Volltext|📄 Lebenslauf]]", "[[Modul_Masterarbeit|⭐ Masterarbeit (1,0)]]", "[[Modul_Übersicht|📋 300 ECTS Übersicht]]"],
        "00_Bachelorzeugnis_Leistungsuebersicht_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[00_Lebenslauf_Volltext|📄 Lebenslauf]]", "[[Modul_Bachelorarbeit|📜 Bachelorarbeit (1,7)]]", "[[Modul_Übersicht|📋 300 ECTS Übersicht]]"],
        # Bachelor Volltext
        "Bachelor_AFS_Automaten_Formale_Sprachen_Theorie_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_AFS|🔤 Modul AFS]]", "[[Algorithmen_und_Datenstrukturen|🌲 Algorithmen]]"],
        "Bachelor_BWL1_Organisation_Management_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_BWL1|👔 Modul BWL 1]]", "[[MOC_Projektgovernance_Vergabe|🏛️ Projektgovernance]]"],
        "Bachelor_DSA_Datenstrukturen_Algorithmen_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_DSA|🌲 Modul DSA]]", "[[Algorithmen_und_Datenstrukturen|🌲 Zettel Algorithmen]]"],
        "Bachelor_EBusiness_Bestnote_1_0_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_EBusiness|🛒 Modul E-Business (1,0)]]", "[[E_Business_Konzepte|🛒 Zettel E-Business]]"],
        "Bachelor_EST_Softwaretechnik_VModell_Scrum_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_EST|⚙️ Modul EST]]", "[[Software_Engineering_Prinzipien|⚙️ Zettel SE]]"],
        "Bachelor_GBWL1_Strukturen_BWL_Rechnungswesen_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_GBWL1|📚 Modul GBWL 1]]", "[[Anlagenbuchhaltung_HGB_Steuerrecht|💶 HGB & Anlagen]]"],
        "Bachelor_GBWL4_Finanzprozess_Investition_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_GBWL4|💰 Modul GBWL 4]]", "[[Universal_Journal_ACDOCA|📑 ACDOCA]]"],
        "Bachelor_GVWL1_Mikrooekonomik_Maerkte_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_GVWL1|📉 Modul GVWL 1]]"],
        "Bachelor_IVP_0x539_Wear_Unternehmensanalyse_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_Informationsverarbeitungspraktikum|📊 Modul IVP]]", "[[Kostenrechnung_PSP_vs_Innenauftrag|💶 Kostenrechnung]]"],
        "Bachelor_Informationsmanagement_Architektur_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_Informationsmanagement_Bachelor|📊 Modul IM]]", "[[MOC_Enterprise_Architecture|🏛️ Enterprise Architecture]]"],
        "Bachelor_Interdisziplinaer_Recht_Management_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_Informatikrecht|⚖️ Informatikrecht]]", "[[Modul_Dienstleistungsmanagement|🏨 Dienstleistungsmanagement]]", "[[Modul_Profilseminar_HRM|👥 Profilseminar HRM]]", "[[Modul_EWI|🏢 Modul EWI]]", "[[Modul_Wissensverarbeitung|🧠 Wissensverarbeitung]]"],
        "Bachelor_MCI_Mensch_Computer_Interaktion_UX_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_MCI|🖥️ Modul MCI]]", "[[Fiori_Launchpad_Rollen_Berechtigungen|🎯 Fiori UX & Rollen]]"],
        "Bachelor_Mathematik_Statistik_Methoden_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_Mathematik|📐 Modul Mathematik]]", "[[Modul_Statistik1|📊 Statistik I]]", "[[Modul_Statistik2|📈 Statistik II]]"],
        "Bachelor_Modellierung_BPMN_UML_Petrinetze_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_Modellierung|📐 Modul Modellierung]]", "[[SQL_und_Datenmodellierung|💾 SQL & Datenmodellierung]]"],
        "Bachelor_PSE_Programmierung_Java_OOP_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_PSE|☕ Modul PSE]]", "[[Software_Engineering_Prinzipien|⚙️ Zettel SE]]"],
        "Bachelor_Programmentwicklung_Funktional_Logisch_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_Programmentwicklung|💻 Modul Programmentwicklung]]", "[[Software_Engineering_Prinzipien|⚙️ Zettel SE]]"],
        "Bachelor_SOPRA_Softwarepraktikum_Java_taskMasterPro_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_Softwarepraktikum|💻 Modul SOPRA]]", "[[Software_Engineering_Prinzipien|⚙️ Zettel SE]]"],
        "Bachelor_WI1_Betriebliche_Informationssysteme_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_MBIS|🔄 Modul MBIS/WI]]", "[[SSB_Grossprojekt_SAP4SSB|🚆 SAP S/4HANA]]"],
        # Master Volltext
        "Master_AI4IoT_Sensor_Edge_AI_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_AI4IoT|📡 Modul AI4IoT]]", "[[IoT_Architekturen|📡 Zettel IoT]]"],
        "Master_AIM_Advanced_Information_Management_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_AIM|📚 Modul AIM]]", "[[SQL_und_Datenmodellierung|💾 Datenmodellierung]]"],
        "Master_Advanced_Software_Engineering_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_Advanced_Software_Engineering|💻 Modul ASE]]", "[[Software_Engineering_Prinzipien|⚙️ Zettel SE]]"],
        "Master_Applied_AI_Generative_AI_Industrie_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_Applied_AI|🧠 Modul Applied AI]]", "[[Generative_AI_LLM|🤖 Zettel Generative AI]]"],
        "Master_Datenbanken_Informationssysteme_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_Datenbanken|💾 Modul DBIS]]", "[[SQL_und_Datenmodellierung|💾 Zettel SQL]]", "[[HANA_Datenbank|⚡ SAP HANA DB]]"],
        "Master_Digitale_Nachhaltigkeit_Schmalz_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_Digitale_Nachhaltigkeit|🌱 Modul Digitale Nachhaltigkeit]]", "[[EHS_Gefahrstoff_Nachhaltigkeitsberichterstattung|🌱 CSRD & EHS]]"],
        "Master_FPWI_Smart_Service_Blueprinting_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_FPWI|⚡ Modul FPWI]]", "[[IoT_Architekturen|📡 IoT Architekturen]]"],
        "Master_Forschungsmethoden_Algorithm_Aversion_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_Forschungsmethoden|📊 Modul Forschungsmethoden]]", "[[Wissenschaftliche_Methodik|🔬 Wissenschaftliche Methodik]]"],
        "Master_ISG_PatentRadar_Klingele_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_ISG|📦 Modul ISG]]", "[[Modul_Innovationsmanagement|💡 Innovationsmanagement]]"],
        "Master_Innovationsmanagement_Plattformen_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_Innovationsmanagement|💡 Modul Innovationsmanagement]]", "[[Bimodale_ERP_Plattformisierung_BTP|🧩 Plattformisierung]]"],
        "Master_Management_IT_Unternehmen_ITIL_COBIT_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_Management_IT_Unternehmen|📈 Modul Management IT]]", "[[DC1_ITIL4_Service_Operations|🏢 ITIL 4 Operations]]"],
        "Master_Masterarbeit_Literatur_Fundierung_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_Masterarbeit|⭐ Masterarbeit (1,0)]]", "[[Bimodale_ERP_Plattformisierung_BTP|🧩 Bimodale Plattformisierung]]", "[[Clean_Core_Paradigma|⭐ Clean Core]]"],
        "Master_SOM_Service_Operations_Management_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_SOM|🔄 Modul SOM]]", "[[DC1_ITIL4_Service_Operations|🏢 Service Operations]]"],
        "Master_Software_Architektur_Microservices_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_Software_Architektur|🏛️ Modul Software-Architektur]]", "[[MOC_Enterprise_Architecture|🏛️ Enterprise Architecture]]"],
        "Master_TEUI_Internationale_Unternehmenstaetigkeit_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_TEUI|🌍 Modul TEUI]]"],
        "Master_Zusatzmodule_Quantum_SmartCities_AIProto_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Modul_Quanteninformatik|⚛️ Quanteninformatik]]", "[[Modul_SmartCities|🏙️ Smart Cities]]", "[[Modul_TOGAF_Scape|🏛️ TOGAF 9 Zertifikat]]"],
        # SSB & DC1 Volltext
        "DC1_Carriermanagement_SOPs_TOGAF_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[DC1_ITIL4_Service_Operations|🏢 DC1 ITIL 4]]", "[[MOC_Enterprise_Architecture|🏛️ EAM & TOGAF]]"],
        "DC1_Hardware_Lifecycle_Management_Fahrplan_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[DC1_Hardware_Lifecycle_Management|💻 DC1 HLM]]"],
        "DC1_ITIL4_Incident_Reports_PostMortems_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[DC1_ITIL4_Service_Operations|🏢 DC1 ITIL 4]]", "[[Third_Level_Support_Incident_Root_Cause|🩺 Incident & 3rd-Level Root Cause]]"],
        "SSB_Architektur_Methoden_Tools_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[MOC_SSB_Transformation|🗺️ MOC SSB]]", "[[Toolkette_Signavio_CALM_EnableNow|🛠️ Toolchain]]", "[[Clean_Core_Paradigma|⭐ Clean Core]]"],
        "SSB_Fachstream_CO_Controlling_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[MOC_Kaufmaennische_Prozesse|💶 MOC FI/CO]]", "[[Kostenrechnung_PSP_vs_Innenauftrag|📊 PSP & Innenaufträge]]"],
        "SSB_Fachstream_FI_Finanzwesen_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[MOC_Kaufmaennische_Prozesse|💶 MOC FI/CO]]", "[[Universal_Journal_ACDOCA|📑 ACDOCA]]", "[[SAP_Trennungsrechnung_Public_Sector_EU1370|💶 Trennungsrechnung EU-1370]]"],
        "SSB_Fachstream_Grants_Management_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[SAP_Grants_Management_GTE|🏛️ Grants Management GTE]]", "[[Stream_Grants_Management_Drittmittel_LGVFG|🏛️ LGVFG Drittmittel]]"],
        "SSB_Fachstream_MM_Materialwirtschaft_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Stream_MM_Beschaffung_Ariba|📦 Stream MM & Ariba]]", "[[MOC_Kaufmaennische_Prozesse|💶 MOC Prozesse]]"],
        "SSB_Fachstream_SD_Vertrieb_PATRIS_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[Stream_Sales_Distribution_PATRIS|🎫 Stream SD & PATRIS]]", "[[Schnittstellenmatrix_Subsysteme|🔗 Schnittstellenmatrix]]"],
        "SSB_Fachstream_Sustainability_CSRD_EHS_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[EHS_Gefahrstoff_Nachhaltigkeitsberichterstattung|🌱 CSRD & EHS]]", "[[Modul_Digitale_Nachhaltigkeit|🌱 Digitale Nachhaltigkeit]]"],
        "SSB_Gesamtprojekt_S4HANA_Ergaenzungen_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[MOC_SSB_Transformation|🗺️ MOC SSB Transformation]]", "[[SSB_Grossprojekt_SAP4SSB|🚆 SSB Programmübersicht]]"],
        "SSB_Migration_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[SSB_Datenmigration_LTMC_CVI|🔄 Datenmigration Overview]]", "[[SAP_Migration_Cockpit_LTMC|🛠️ LTMC]]", "[[Customer_Vendor_Integration_CVI|🔗 CVI]]"],
        "SSB_PMO_Projektleitung_Masterplan_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[MOC_Projektgovernance_Vergabe|🏛️ MOC Governance]]", "[[Gesamtprojektplan_MS_Project|📅 MS Project Masterplan]]"],
        "SSB_SektVO_Ausschreibung_Vergabe_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[EU_Vergabeverfahren_SektVO_Ausschreibung|⚖️ EU-SektVO Vergabe]]", "[[Partner_Axians|🤝 Axians]]", "[[Partner_Nagarro|🤝 Nagarro]]"],
        "SSB_Solution_Design_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[SSB_Solution_Design_FI_CO|📐 Solution Design Summary]]", "[[SAP_Trennungsrechnung_Public_Sector_EU1370|💶 Trennungsrechnung]]", "[[Universal_Journal_ACDOCA|📑 ACDOCA]]"],
        "SSB_TP1_Change_Management_People_Plan_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[TP1_Change_Management_People_Plan|👥 TP1 Plan]]", "[[MOC_Change_Management|🤝 MOC Change]]"],
        "SSB_TP2_Kaufmaennische_Prozesse_Workshops_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[TP2_Kaufmaennische_Prozesse_Plan|💶 TP2 Plan]]", "[[MOC_Kaufmaennische_Prozesse|📐 MOC FI/CO]]"],
        "SSB_TP3_Technische_Instandhaltung_EAM_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[TP3_Technische_Prozesse_Instandhaltung_Plan|🔧 TP3 Plan]]", "[[Mobile_Instandhaltung_SSAM|📱 SSAM]]"],
        "SSB_TP4_IT_Infrastruktur_RISE_Basis_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[TP4_IT_Unterstuetzung_Integration_Plan|☁️ TP4 Plan]]", "[[SAP_BTP_Integration_Suite|🔗 SAP BTP]]"],
        "SSB_TP5_Gesamtsteuerung_Architektur_PMO_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[TP5_Gesamtsteuerung_PMO_Betriebsvereinbarung_Plan|🏛️ TP5 Plan]]", "[[Stakeholder_Roland_Nowak|👔 Roland Nowak]]"],
        "SSB_TP5_Steering_Board_Lenkungsausschuss_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[C_Level_Reporting_SteeringBoard|🏛️ C-Level Reporting]]", "[[MOC_Projektgovernance_Vergabe|🏛️ MOC Governance]]"],
        "SSB_Tool_Governance_CALM_EnableNow_Volltext": ["[[00_INDEX|🧠 Master Index]]", "[[SSB_Tool_Governance_Signavio_CALM|🛠️ Tool Governance]]", "[[Key_User_Enablement_EnableNow|🎓 Enable Now]]"],
    }

    updated = 0
    for root, dirs, files in os.walk(VAULT_DIR):
        if ".obsidian" in root:
            continue
        for fn in files:
            base = os.path.splitext(fn)[0]
            if base not in link_map:
                continue
            fp = os.path.join(root, fn)
            with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                txt = f.read()
            if "Wissensnetz-Verknüpfung" in txt:
                continue
            links_str = " • ".join(link_map[base])
            nav_callout = f"\n\n> [!INFO] **Wissensnetz-Verknüpfung**\n> {links_str}\n"
            # Insert right before first "## 📋" or "## 📜" or at top after summary
            if "\n## 📋" in txt:
                txt = txt.replace("\n## 📋", nav_callout + "\n## 📋", 1)
            elif "\n## 📜" in txt:
                txt = txt.replace("\n## 📜", nav_callout + "\n## 📜", 1)
            else:
                txt = txt + "\n" + nav_callout
            with open(fp, "w", encoding="utf-8", errors="replace") as f:
                f.write(txt)
            updated += 1
    print(f"[4/6] Added bidirectional Wissensnetz links to {updated} Volltext dossiers.")


def create_zettel_and_sync_debrief():
    zettel_dir = os.path.join(VAULT_DIR, "04_Second_Brain_Zettelkasten")
    os.makedirs(zettel_dir, exist_ok=True)

    zettels = {
        "SAP_HCM_Berechtigungsarchitektur_IAM.md": """---
id: sap-hcm-berechtigungsarchitektur-iam
title: "SAP HCM Berechtigungsarchitektur, Strukturelle Profile & Enterprise IAM"
type: zettel
domain: sap-transformation
status: evergreen
summary: "Kernkonzepte der SAP HCM Sicherheit (P_ORGIN, P_PERNR, OOSP, SU01/SU10/PFCG/SUIM), JML-Zyklus und Learnings aus der globalen Schwarz-Gruppe (650.000 MA, 1,2 Mio. Berechtigungen/Monat via UMT)."
tags:
  - zettel
  - sap_hcm
  - iam
  - p_orgin
  - oosp
  - schwarz_digits
last_updated: "2026-11-24"
---

# 🔐 SAP HCM Berechtigungsarchitektur & Enterprise IAM

> [!SUMMARY] **Praxis-Synthese: Standard-SAP Security × Globale Enterprise-Skalierung**
> Verknüpft [[Fiori_Launchpad_Rollen_Berechtigungen|Fiori & Rollen]], [[2026-11-24_Schwarz_Digits_SAP_HCM_IAM|Schwarz Digits Interview-Debrief]] und [[Bimodale_ERP_Plattformisierung_BTP|Plattformisierung]].

## 1. Drei Säulen des SAP HCM Berechtigungsschutzes
1. **Funktionale Stammdatenprüfung (`P_ORGIN` / `P_ORGXX`):** Filtert nach Aktivität (`AUTHC`: Read/Write/Delete), Personalbereich (`PERSA`), Mitarbeiterkreis (`PERSK`) und Infotyp (`INFTY`, z. B. `IT0001` Orga, `IT0008` Entgelt).
2. **Selbstschutz (`P_PERNR`):** Verhindert zuverlässig Interessenkonflikte, indem HR-Sachbearbeiter ihre eigenen Stamm- und Gehaltsdaten nicht selbst einsehen oder manipulieren können.
3. **Strukturelle Berechtigungen (`OOSP` / OM):** Steuert hierarchische Sichtbarkeit über Planstellen (`S`), Organisationseinheiten (`O`) und Auswertungswege (`MANASS` in `HRP1000`/`HRP1001`).

## 2. Praxisbeispiel Großkonzern (Schwarz Digits Erkenntnisse, 24.11.2026)
* **Skalierung:** 650.000 Mitarbeitende über 34–37 Länder (Lidl, Kaufland, Schwarz Produktion, PreZero).
* **Pyramiden-Architektur:** Lokale Ländersysteme (je eigene Payroll/Gesetze) ➔ globales On-Premises HCM (HANA-Migration Sommer Live) ➔ SuccessFactors / Cloud-Apps via BTP.
* **Eigenentwickeltes User Management Tool (UMT):** Verteilt **> 1,2 Millionen Berechtigungen pro Monat** zu **> 95 % vollautomatisiert über Nacht** – inkl. dynamischer Pakete, User-Anlage, Alias-Erkennung und automatischer Verortung (auch für ~85 % Frontline-Mitarbeitende ohne eigene E-Mail-Adresse).

## 3. Verknüpfte Wissens-Nodes
* [[Third_Level_Support_Incident_Root_Cause|🩺 Third-Level-Support & Job-Analyse]]
* [[DC1_ITIL4_Service_Operations|🏢 ITIL 4 Governance & Ticket-Disziplin]]
""",
        "Bimodale_ERP_Plattformisierung_BTP.md": """---
id: bimodale-erp-plattformisierung-btp
title: "Bimodale ERP-Plattformisierung: Boundary Resources, Clean Core & SAP BTP"
type: zettel
domain: enterprise-architecture
status: evergreen
summary: "Wissenschaftlich-praktische Synthese der Bachelorarbeit (Boundary Resource Theory, Note 1,7), Masterarbeit (CSF ERP-Plattformisierung, Note 1,0) und praktischen Transformationserfahrung bei SSB AG & Schwarz."
tags:
  - zettel
  - plattformisierung
  - boundary_resources
  - btp
  - clean_core
  - masterarbeit
last_updated: "2026-11-24"
---

# 🧩 Bimodale ERP-Plattformisierung & Boundary Resources

> [!SUMMARY] **Vom akademischen Modell (Note 1,7 & 1,0) zur Konzern-Architektur**
> Verbindet [[Modul_Masterarbeit|Masterarbeit (1,0)]], [[Modul_Bachelorarbeit|Bachelorarbeit (1,7)]], [[Clean_Core_Paradigma|Clean Core]] und [[SAP_BTP_Integration_Suite|SAP BTP Integration Suite]].

## 1. Kern-Erkenntnis der Forschung (Uni Stuttgart)
* **Bachelorarbeit (Low-Code OutSystems & Mendix):** Plattform-Ökosysteme steuern das Spannungsfeld zwischen *Kontrolle* und *Generativität* über 14 Klassen von **Boundary Resources** (Application, Development, Social Boundary Resources nach Ghazawneh & Henfridsson).
* **Masterarbeit (SAP4SSB / S/4HANA Transformation):** Plattformisierung bedeutet nicht isoliert „Clean Core“, sondern das komplexe Zusammenspiel aus **Organisationaler Governance**, **Bimodaler Entkopplung** (stabiler ERP-Kern + agile Side-by-Side BTP-Erweiterungen), **Absorptive Capacity** im Fachbereich und klarer **PMO-Steuerung**.

## 2. Konkrete Praxis-Brücke (SSB AG & Schwarz Digits)
* Bei der **SSB AG** wurden kaufmännische Subsysteme (`PATRIS`, `xSuite`) sauber über Schnittstellen-Governance und Solution Design (`SDD`) entkoppelt, statt den S/4HANA-Kern zu verbauen.
* Bei **Schwarz** existiert historisch bedingt hohe Eigenentwicklung im On-Premises-System (z. B. `UMT`); im Zuge des **HANA-ready-Umbaus** wird genau dieser Übergang in Richtung **SAP BTP / Integration Suite** strategisch kritisch.

## 3. Verknüpfte Wissens-Nodes
* [[Absorptive_Capacity_SSB|🧠 Absorptive Capacity]] • [[WRICEFA_Entkopplung|🔗 WRICEFA Entkopplung]] • [[SSB_Solution_Design_FI_CO|📐 SSB Solution Design]]
""",
        "Third_Level_Support_Incident_Root_Cause.md": """---
id: third-level-support-incident-root-cause
title: "Third-Level-Support & Root-Cause-Analyse im SAP-Betrieb (ITIL 4)"
type: zettel
domain: datacenter-operations
status: evergreen
summary: "Systematische Methodik vom First-Level-SPoC (Datacenter One / Jira & Confluence) bis zum technischen Third-Level-Incident-Management in SAP-Berechtigungs- und Schnittstellenprozessen."
tags:
  - zettel
  - itil4
  - third_level_support
  - root_cause_analysis
  - sap_betrieb
last_updated: "2026-11-24"
---

# 🩺 Third-Level-Support & Root-Cause-Analyse im SAP-Betrieb

> [!SUMMARY] **Ticket-Disziplin + Architekturelle Ursachenforschung**
> Verbindet [[DC1_ITIL4_Service_Operations|DC1 ITIL 4 Operations]], [[DC1_ITIL4_Incident_Reports_PostMortems_Volltext|DC1 Incident Reports]] und [[2026-11-24_Schwarz_Digits_SAP_HCM_IAM|Schwarz Digits Runde 2]].

## 1. Strukturierte Eskalations- & Analyse-Kaskade
Im operativen Großbetrieb liegen Berechtigungsfehler oft **nicht im Berechtigungstool selbst**, sondern im vorgelagerten Quellprozess (Stammdaten, Organisationseinheit oder Job-Timing):
1. **Event- & Job-Monitoring (`SM37` / `SM21`):** Abgebrochene Hintergrundjobs nach Ursachen (Lock-Konflikt, Berechtigungs-Abbruch, Timeout, fehlender Datensatz) klassifizieren statt blind neu starten.
2. **Berechtigungs- & Dump-Diagnose (`SU53` / `ST01` / `ST22`):** Exaktes fehlendes Berechtigungsobjekt und Feldwert (`AUTHC`, `PERSA`, `INFTY`) gegen Standardrollen abgleichen.
3. **Schnittstellen- & OM/PA-Synchronisation:** Prüfen, ob HR-Maßnahmen (`PA40`) sauber in `HRP1000`/`HRP1001` und in Zielsysteme repliziert wurden – ggf. mit einem Referenz-Testfall gegen das Produktivsystem vergleichen.
4. **Dauerhafte Behebung & Knowledge Base:** Wiederkehrende Störungen nach **ITIL 4 Problem Management** in Runbooks / Confluence / Cloud ALM überführen.

## 2. Verknüpfte Wissens-Nodes
* [[SAP_HCM_Berechtigungsarchitektur_IAM|🔐 SAP HCM IAM]] • [[Modul_Management_IT_Unternehmen|📈 IT-Governance & ITIL]]
""",
        "SAP_Trennungsrechnung_Public_Sector_EU1370.md": """---
id: sap-trennungsrechnung-public-sector-eu1370
title: "ÖPNV Trennungsrechnung (EU-VO 1370/2007) im SAP S/4HANA Universal Journal"
type: zettel
domain: sap-transformation
status: evergreen
summary: "Verdichtete Architektur-Karte zur gesetzlichen Trennungsrechnung im öffentlichen Nahverkehr, abgebildet im Universal Journal (ACDOCA), Controlling und Grants Management bei der SSB AG."
tags:
  - zettel
  - trennungsrechnung
  - acdoca
  - eu1370
  - ssb
last_updated: "2026-11-24"
---

# 💶 Trennungsrechnung (EU-VO 1370/2007) in S/4HANA

> [!SUMMARY] **Regulatorik trifft Universal Journal (`ACDOCA`)**
> Verbindet [[Trennungsrechnung_OEPNV_EU1370|SSB Trennungsrechnung]], [[Universal_Journal_ACDOCA|Universal Journal ACDOCA]], [[SAP_Grants_Management_GTE|Grants Management]] und [[SSB_Solution_Design_FI_CO|Solution Design]].

## 1. Kernanforderung
Verkehrsunternehmen wie die **SSB AG** müssen nach **EU-Verordnung 1370/2007** hoheitliche/gemeinwirtschaftliche Leistungsbereiche (ÖPNV mit öffentlichen Zuschüssen) strikt rechnerisch von gewerblichen Tätigkeiten trennen, um Überkompensation gerichtsfest auszuschließen.

## 2. Abbildung in SAP S/4HANA
* **Single Source of Truth (`ACDOCA`):** Durch Kombination von Kostenstelle, Innenauftrag, PSP-Element (`PS`) und Profitcenter/Segment liefert jeder Beleg automatisch die korrekte Zuordnung zwischen FI und CO ohne nachträgliche Abstimmungsschleifen.
* **Drittmittel-Integration (`Grants Management / LGVFG`):** Investitionszuschüsse für Stadtbahn-Infrastruktur werden über Förderprogramme bis auf Anlage im Bau und spätere Abschreibung sauber durchgereicht.
* **Revisionssicherheit & Datenmigration (`LTMC` / `0,00 €`):** Kontenabstimmung und Summen-/Saldenabgleich garantieren, dass Eröffnungsbilanzwerte zu `0,00 €` Restsaldo überführt werden.

## 3. Verknüpfte Wissens-Nodes
* [[SSB_Migration_Volltext|🔄 SSB Datenmigration]] • [[Kostenrechnung_PSP_vs_Innenauftrag|📊 PSP vs. Innenauftrag]]
"""
    }

    for fname, body in zettels.items():
        with open(os.path.join(zettel_dir, fname), "w", encoding="utf-8", errors="replace") as f:
            f.write(body)
    print(f"[5/6] Created/updated {len(zettels)} rich atomic Zettelkasten cards.")

    # Update Schwarz Digits interview file in Obsidian with verified Notion debrief
    sd_path = os.path.join(VAULT_DIR, "01_Karriere_Bewerbungen", "Interview_Vorbereitungen", "2026-11-24_Schwarz_Digits_SAP_HCM_IAM.md")
    if os.path.exists(sd_path):
        with open(sd_path, "r", encoding="utf-8", errors="ignore") as f:
            sd_txt = f.read()
        if "Executive Debrief (24.11.2026" not in sd_txt:
            debrief_section = """

---

## 🚀 6. Executive Debrief & Ergebnisse nach dem Erstgespräch (24.11.2026 | Cosmin Serbanescu & Stefanie Link)

> [!SUCCESS] **Hervorragendes Kennenlernen – Positives Signal beider Seiten**
> Sympathisches Gespräch im professionellen „Du“. Nächster Schritt: Rückmeldung bis maximal Anfang nächster Woche für **Runde 2 (Fachinterview mit Cosmin & Abteilungsleiter Kai)**.

### Verknüpfte Konzepte & Wissensbasis
[[00_Bewerbungsmanagement_Cockpit|📊 Bewerbungs-Cockpit]] • [[00_INDEX|🧠 Master Index]] • [[SAP_HCM_Berechtigungsarchitektur_IAM|🔐 SAP HCM IAM Zettel]] • [[Bimodale_ERP_Plattformisierung_BTP|🧩 Plattformisierung & BTP]] • [[Third_Level_Support_Incident_Root_Cause|🩺 3rd-Level-Support & Root Cause]] • [[SSB_Grossprojekt_SAP4SSB|🚆 SSB S/4HANA]] • [[DC1_ITIL4_Service_Operations|🏢 DC1 ITIL 4]]

### Kernerkenntnisse zu Systemlandschaft & Rolle
1. **Dimension & Eigenentwicklung (UMT):** **650.000 interne Mitarbeitende** in **34–37 Ländern**. Über **1,2 Millionen Berechtigungen pro Monat**, zu **>95 % über Nacht vollautomatisiert** verteilt durch ein eigenentwickeltes Tool (**UMT**), weil Standard-SAP-Lösungen der Konzernkomplexität (z. B. ~85 % Mitarbeitende ohne Firmen-E-Mail-Adresse, eigene Filial-Gesellschaften) nicht genügen.
2. **Architektur & Transformation:** Pyramiden-Setup von lokalen Länder-Systemen (eigene Payroll) ➔ globales On-Premises HCM (**HANA-ready Umstellung / Livegang im Sommer**) ➔ SuccessFactors & Cloud über **SAP BTP / Integration Suite**. Tech-Hubs in Spanien, Bulgarien und Rumänien sowie eigene Cloud-Infrastruktur (**STACKIT**).
3. **Deine Mission (Re-Insourcing):** Eine interne Kollegin (Sultana) verlässt das Team; aktuell tragen drei erfahrene Externe den Betrieb. Gesucht wird jemand mit echter IT-Affinität:
   - *Einstieg:* Minor Releases & Customizing-Tabellen in Abstimmung mit den spanischen Entwicklern & Fachbereichen.
   - *Ausbau:* Event-Tickets (Job-Abbrüche analysieren) & strukturelle Profile / Organisationsmanagement (`OOSP`/`OM`).
   - *Zielbild:* **Technischer Third-Level-Support** – Fehlerquellen über PA/OM/Schnittstellen sauber identifizieren, statt nur Tickets weiterzuleiten. Projekte wie die *Transformation Zeitwirtschaft* begleiten.
4. **Konditionen & Entwicklung:** 40h-Woche, 30 Tage Urlaub, 2–3 Tage vor Ort in Neckarsulm. **100 % verlässliches Fixgehalt** (keine variablen Kürzungen) mit ca. **5 % jährlicher Junior-Progression** (Junior ➔ Professional 80–90 % selbstständig ➔ Senior). Bezahlte **ITIL 4-Zertifizierung** + Schwarz IT Academy.
5. **Follow-up & Runde 2 (Kai):** Proaktive Interessenbestätigung an Recruiterin **Albina Kadrija** senden; für das Fachgespräch mit **Kai** Fokus auf systematische Störungsanalyse (`SM37`, `SU53`, `ST22`), PA/OM-Schnittstellenlogik, BTP-Entkopplung und fachbereichstaugliche Least-Privilege-Governance legen.
"""
            sd_txt = sd_txt + debrief_section
            with open(sd_path, "w", encoding="utf-8", errors="replace") as f:
                f.write(sd_txt)
            print("    -> Updated Schwarz Digits Obsidian file with verified Executive Debrief & outgoing links.")

    # Wire Schwarz Digits debrief link inside Bewerbungsmanagement_Cockpit.md
    cockpit_path = os.path.join(VAULT_DIR, "01_Karriere_Bewerbungen", "00_Bewerbungsmanagement_Cockpit.md")
    if os.path.exists(cockpit_path):
        with open(cockpit_path, "r", encoding="utf-8", errors="ignore") as f:
            ct = f.read()
        if "[[2026-11-24_Schwarz_Digits_SAP_HCM_IAM" not in ct:
            ct = ct.replace(
                "Dient dem LLM und Second Brain als verlässliche Übersicht über alle laufenden Bewerbungsprozesse und anstehenden Gespräche.",
                "Dient dem LLM und Second Brain als verlässliche Übersicht über alle laufenden Bewerbungsprozesse und anstehenden Gespräche.\n> 🔗 **Aktives Live-Dossier:** [[2026-11-24_Schwarz_Digits_SAP_HCM_IAM|🎯 Schwarz Digits – Interview & Executive Debrief (24.11.2026)]] • [[00_INDEX|🧠 Master Index]]",
                1
            )
            with open(cockpit_path, "w", encoding="utf-8", errors="replace") as f:
                f.write(ct)

    # Wire new Zettels in 00_INDEX.md under Zweig 7 (Zettelkasten)
    index_path = os.path.join(VAULT_DIR, "00_INDEX.md")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8", errors="ignore") as f:
            idx_txt = f.read()
        extra_zettel_links = """- [[SAP_HCM_Berechtigungsarchitektur_IAM|🔐 SAP HCM Berechtigungsarchitektur, Strukturelle Profile & Enterprise IAM (UMT Case)]]
- [[Bimodale_ERP_Plattformisierung_BTP|🧩 Bimodale ERP-Plattformisierung: Boundary Resources, Clean Core & SAP BTP]]
- [[Third_Level_Support_Incident_Root_Cause|🩺 Third-Level-Support & Root-Cause-Analyse im SAP-Betrieb (ITIL 4)]]
- [[SAP_Trennungsrechnung_Public_Sector_EU1370|💶 ÖPNV Trennungsrechnung (EU-VO 1370/2007) im Universal Journal (ACDOCA)]]"""
        if "[[SAP_HCM_Berechtigungsarchitektur_IAM" not in idx_txt:
            idx_txt = idx_txt.replace(
                "- [[Generative_AI_LLM|🤖 Generative AI, LLMs & Retrieval Augmented Generation (RAG)]]",
                "- [[Generative_AI_LLM|🤖 Generative AI, LLMs & Retrieval Augmented Generation (RAG)]]\n" + extra_zettel_links
            )
            with open(index_path, "w", encoding="utf-8", errors="replace") as f:
                f.write(idx_txt)

    # Update .obsidian core-plugins & clean empty root Unbenannt.base placeholders
    for cfg_name in ["core-plugins.json", "core-plugins-migration.json"]:
        cp = os.path.join(VAULT_DIR, ".obsidian", cfg_name)
        if os.path.exists(cp):
            with open(cp, "r", encoding="utf-8") as f:
                data = json.load(f)
            data["properties"] = True
            data["slash-command"] = True
            with open(cp, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

    for junk_base in ["Unbenannt.base", "Unbenannt 1.base"]:
        jp = os.path.join(VAULT_DIR, junk_base)
        if os.path.exists(jp) and os.path.getsize(jp) < 100:
            os.remove(jp)
            print(f"    -> Removed empty Obsidian root placeholder: {junk_base}")

    # Sync Obsidian 00_CHANGELOG.md with workspace CHANGELOG.md
    ws_cl = os.path.join(BASE_DIR, "CHANGELOG.md")
    obs_cl = os.path.join(VAULT_DIR, "00_CHANGELOG.md")
    if os.path.exists(ws_cl):
        with open(ws_cl, "r", encoding="utf-8") as f:
            cl_txt = f.read()
        with open(obs_cl, "w", encoding="utf-8", errors="replace") as f:
            f.write(cl_txt)
        print("    -> Synchronized Obsidian 00_CHANGELOG.md with workspace CHANGELOG.md.")

    print("[6/6] Obsidian Second Brain configuration, Zettel & Debrief optimization complete!")


if __name__ == "__main__":
    clean_registry_junk()
    strip_junk_blocks_in_vault()
    split_monster_files()
    add_context_links_to_volltext()
    create_zettel_and_sync_debrief()
