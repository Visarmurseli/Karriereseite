# -*- coding: utf-8 -*-
"""
Knowledge & Profile OS 2.0 Restructurer (Phase 1: T101–T103)
1. Separates raw Volltext dumps & 85 split volumes cleanly into 05_Archiv/Volltexte_DataLake/
2. Builds 00_DataLake_Index.md so all graph edges & RAG chunks remain 100% connected
3. Isolates personal habits/fitness/retrospective notes into 04_Second_Brain_Zettelkasten/Personal_OS/
4. Restructures 00_INDEX.md into Layer 1 (Curated Foreground) vs Layer 2 (Data Lake)
5. Adds unified > [!ABSTRACT] **60-Sekunden-Essenz** callouts to core work stations & top modules
"""

import os
import re
import json
import shutil
from datetime import datetime

VAULT_DIR = r"C:\Users\SHQIPTAR634\Documents\Obsidian Vault"
DATALAKE_ROOT = os.path.join(VAULT_DIR, "05_Archiv", "Volltexte_DataLake")
TODAY = datetime.now().strftime("%Y-%m-%d")


def _safe_move(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.exists(src) and os.path.abspath(src) != os.path.abspath(dst):
        if os.path.exists(dst):
            os.remove(dst)
        shutil.move(src, dst)
        return True
    return False


def archive_volltext_datalake():
    """T101: Moves _Teil_XX splits and Pillar 02/03/DC1 _Volltext dumps to 05_Archiv/Volltexte_DataLake/."""
    moved = {"02_Wirtschaftsinformatik_300ECTS": [], "03_SAP_EnterpriseArchitecture": [], "04_DC1": []}

    # Pillar 02 (Academic): *_Volltext*.md and *_Teil_*.md
    p2_dir = os.path.join(VAULT_DIR, "02_Wirtschaftsinformatik_300ECTS")
    p2_dst_dir = os.path.join(DATALAKE_ROOT, "02_Wirtschaftsinformatik_300ECTS")
    if os.path.exists(p2_dir):
        for fn in sorted(os.listdir(p2_dir)):
            if not fn.endswith(".md"):
                continue
            if "_Volltext" in fn or "_Teil_" in fn:
                if _safe_move(os.path.join(p2_dir, fn), os.path.join(p2_dst_dir, fn)):
                    moved["02_Wirtschaftsinformatik_300ECTS"].append(fn)

    # Pillar 03/04 (SSB + DC1): SSB_*_Volltext.md and DC1_*_Volltext.md
    p3_dir = os.path.join(VAULT_DIR, "03_SAP_EnterpriseArchitecture")
    p3_dst_dir = os.path.join(DATALAKE_ROOT, "03_SAP_EnterpriseArchitecture")
    p4_dst_dir = os.path.join(DATALAKE_ROOT, "04_DC1")
    if os.path.exists(p3_dir):
        for fn in sorted(os.listdir(p3_dir)):
            if not fn.endswith(".md"):
                continue
            if fn.startswith("DC1_") and "_Volltext" in fn:
                if _safe_move(os.path.join(p3_dir, fn), os.path.join(p4_dst_dir, fn)):
                    moved["04_DC1"].append(fn)
            elif "_Volltext" in fn or "_Teil_" in fn:
                if _safe_move(os.path.join(p3_dir, fn), os.path.join(p3_dst_dir, fn)):
                    moved["03_SAP_EnterpriseArchitecture"].append(fn)

    # Collect all Data Lake main hubs (non-_Teil_) for 00_DataLake_Index.md
    lake_hubs = {"02_Wirtschaftsinformatik_300ECTS": [], "03_SAP_EnterpriseArchitecture": [], "04_DC1": []}
    for pillar_key in lake_hubs:
        pdir = os.path.join(DATALAKE_ROOT, pillar_key)
        if not os.path.exists(pdir):
            continue
        for fn in sorted(os.listdir(pdir)):
            if fn.endswith(".md") and "_Teil_" not in fn:
                lake_hubs[pillar_key].append(os.path.splitext(fn)[0])

    total_archived = sum(len(os.listdir(os.path.join(DATALAKE_ROOT, k))) for k in lake_hubs if os.path.exists(os.path.join(DATALAKE_ROOT, k)))

    ssb_links = "\n".join([f"- [[{b}]]" for b in lake_hubs["03_SAP_EnterpriseArchitecture"]])
    dc1_links = "\n".join([f"- [[{b}]]" for b in lake_hubs["04_DC1"]])
    uni_links = "\n".join([f"- [[{b}]]" for b in lake_hubs["02_Wirtschaftsinformatik_300ECTS"]])

    datalake_index = f"""---
id: volltext-data-lake-index
title: "Volltext Data Lake Archiv-Index (Layer 2 | Hybrid RAG Corpus)"
type: moc
domain: system-governance
status: evergreen
summary: "Archiv-Index für alle ausgelagerten Roh-Volltexte und 85 Split-Bände unter 05_Archiv/Volltexte_DataLake/ (durchsuchbar über Hybrid RAG & Wikilinks ohne Ordner-Ballast im Vordergrund)."
tags:
  - data_lake
  - archive
  - rag_corpus
  - moc
last_updated: "{TODAY}"
---

# 🗄️ Volltext Data Lake & Archiv-Index (Schicht 2)

> [!ABSTRACT] **60-Sekunden-Essenz**
> - **Zweck:** Trennt umfangreiche Roh-Extrakte, Vorlesungsfolien-Dumps und `85` `<4 MB` Split-Bände sauber von deinen alltäglichen Wissens-, Modul- und Profil-Karten (**Schicht 1**).
> - **Suchbarkeit:** Alle **{total_archived} Archiv-Dateien** hier sind vollständig im **Local Hybrid RAG V3 (`career_os_rag.db`)** indexiert und über `[[Wikilinks]]` direkt verknüpft.
> - **Zurück:** [[00_INDEX|🧠 Master Knowledge Hub (Schicht 1 Vordergrund)]]

---

## 🚆 SSB AG S/4HANA Transformation (Volltext-Dossiers)
{ssb_links}

---

## 🏢 Datacenter One GmbH (ITIL 4 / HLM / Carrier Volltexte)
{dc1_links}

---

## 🎓 Universität Stuttgart 300 ECTS (Vorlesungen, Übungen & Literatur-Bände)
{uni_links}
"""
    with open(os.path.join(DATALAKE_ROOT, "00_DataLake_Index.md"), "w", encoding="utf-8") as f:
        f.write(datalake_index)

    print(f"[T101] Moved {sum(len(v) for v in moved.values())} files to Data Lake ({total_archived} total archived files + 00_DataLake_Index.md).")
    return moved


def isolate_personal_os_and_rebuild_index():
    """T102: Isolates Personal_OS notes and rebuilds 00_INDEX.md into Layer 1 (Curated) vs Layer 2 (Data Lake)."""
    personal_dir = os.path.join(VAULT_DIR, "04_Second_Brain_Zettelkasten", "Personal_OS")
    os.makedirs(personal_dir, exist_ok=True)
    personal_files = ["Gewohnheiten.md", "NoFap.md", "Trainingsplan_Visar.md", "Retrospektive_Wintersemester_23_24.md"]
    moved_personal = 0
    for fn in personal_files:
        for cand in [os.path.join(VAULT_DIR, "04_Second_Brain_Zettelkasten", fn), os.path.join(VAULT_DIR, fn)]:
            if os.path.exists(cand):
                if _safe_move(cand, os.path.join(personal_dir, fn)):
                    moved_personal += 1
                break

    # Update Obsidian graph colors so Synergies pop and Archiv/Personal_OS stay visually distinct
    graph_cfg = {
        "collapse-filter": False,
        "search": "",
        "showTags": False,
        "showAttachments": False,
        "hideUnresolved": True,
        "showOrphans": False,
        "collapse-color-groups": False,
        "colorGroups": [
            {"query": "path:04_Second_Brain_Zettelkasten/Synergien", "color": {"a": 1, "rgb": 16106015}},
            {"query": "path:01_Karriere_Bewerbungen", "color": {"a": 1, "rgb": 1070020}},
            {"query": "path:03_SAP_EnterpriseArchitecture", "color": {"a": 1, "rgb": 2457067}},
            {"query": "path:02_Wirtschaftsinformatik_300ECTS", "color": {"a": 1, "rgb": 9130222}},
            {"query": "path:04_Second_Brain_Zettelkasten", "color": {"a": 1, "rgb": 16096779}},
            {"query": "path:00_MOCs OR file:00_INDEX", "color": {"a": 1, "rgb": 12527150}},
            {"query": "path:05_Archiv", "color": {"a": 1, "rgb": 5263440}},
        ],
        "collapse-display": True,
        "showArrow": True,
        "textFadeMultiplier": -0.2,
        "nodeSizeMultiplier": 1.1,
        "lineSizeMultiplier": 1,
        "collapse-forces": True,
        "centerStrength": 0.45,
        "repelStrength": 14,
        "linkStrength": 1,
        "linkDistance": 220,
        "scale": 0.35,
        "close": True,
    }
    graph_path = os.path.join(VAULT_DIR, ".obsidian", "graph.json")
    os.makedirs(os.path.dirname(graph_path), exist_ok=True)
    with open(graph_path, "w", encoding="utf-8") as gf:
        json.dump(graph_cfg, gf, indent=2)

    index_md = f"""---
id: master-knowledge-graph-index
title: "Master Knowledge Graph & Wissensnetz Index"
type: moc
domain: system-governance
status: evergreen
summary: "Zentraler Master Knowledge Hub (Knowledge & Profile OS 2.0): Trennt Schicht 1 (Kuratiertes Profil, Synergien, Stationen & Module) sauber von Schicht 2 (05_Archiv Volltext Data Lake für Hybrid RAG)."
author: "Visar Murseli, M.Sc."
degree: "Master of Science Wirtschaftsinformatik (Note 1,6 | Masterarbeit 1,0)"
experience: "36 Monate Berufserfahrung (24 Mo. SSB AG + 12 Mo. Datacenter One)"
last_updated: "{TODAY}"
tags:
  - moc
  - index
  - master_knowledge_graph
  - second_brain
  - knowledge_profile_os
aliases:
  - Master Index
  - Knowledge Hub Index
  - Vector Router
---
# 🧠 Visar Murseli | Knowledge & Profile OS (Master Index)

> [!ABSTRACT] **60-Sekunden-Essenz: Die zwei Schichten deines Wissens-OS**
> - **Schicht 1 (Vordergrund — Arbeit im Alltag):** Schlanke, kuratierte Dossiers zu Profil/Karriere, **Arbeit × Uni Synergien**, Praxisstationen (24M SSB AG, 12M Datacenter One) und den 300 ECTS Studienmodulen (Uni Stuttgart).
> - **Schicht 2 (Data Lake Archiv — Durchsuchbar im Hintergrund):** Über **140 Volltext-Bände & Split-Dateien** liegen sauber in [[00_DataLake_Index|05_Archiv/Volltexte_DataLake/]], ohne Ordner zu überfluten — vollständig abrufbar über das lokale **Hybrid RAG (`career_os_rag.db`)** & `[[Wikilinks]]`.

---

## 🧭 Architektur-Überblick (Schicht 1 & Schicht 2)

```mermaid
graph TD
    ROOT["🧠 Knowledge & Profile OS (Visar Murseli)"]
    ROOT --> L1["✨ Schicht 1: Kuratiertes Wissen & Profil"]
    ROOT --> L2["🗄️ Schicht 2: Volltext Data Lake (05_Archiv)"]
    L1 --> P0["01_Karriere_Bewerbungen (Profil, Stärken, Cockpit)"]
    L1 --> P1["03_SAP_EnterpriseArchitecture (24M SSB + 12M DC1)"]
    L1 --> P2["02_Wirtschaftsinformatik_300ECTS (47 Module & Arbeiten)"]
    L1 --> P3["04_Second_Brain_Zettelkasten (Konzepte, Synergien, Personal OS)"]
```

---

## 📂 1. Profil, Stärken & Aktive Bewerbungen (`01_Karriere_Bewerbungen/`)
- [[00_Lebenslauf_Volltext|📄 Master-Lebenslauf & Stationen (verifiziert)]]
- [[Target_Roles|🎯 Zielrollen & Positioning-Matrix]]
- [[Aktuelle_Bewerbungsunterlagen|📂 Dokumenten-Hub & Nachweise]]
- [[00_Masterzeugnis_Leistungsuebersicht_Volltext|🎓 Amtliches Masterzeugnis (M.Sc. 1,6 | 120 ECTS | Thesis 1,0)]]
- [[00_Bachelorzeugnis_Leistungsuebersicht_Volltext|🏛️ Amtliche Bachelor-Leistungsübersicht (B.Sc. 3,0 | 180 ECTS | Thesis 1,7)]]
- [[00_Bewerbungsunterlagen_Master_Volltext|📑 Verbindliches Master-Bewerbungsdossier & Profil-Audit]]
- [[00_Bewerbungsmanagement_Cockpit|📊 Bewerbungsmanagement Cockpit (Live Pipeline)]]
- [[2026-11-27_KPMG_IT_Transformation_ERP_Audit|🎯 Interview-Dossier: KPMG IT-Transformation & IKS/Audit (27.11.2026)]]
- [[2026-11-24_Schwarz_Digits_SAP_HCM_IAM|🎯 Live Interview-Dossier: Schwarz Digits (Junior SAP HCM IAM | Debrief)]]
- [[2026-11-23_TRUMPF_Trainee_IT_Governance|🎯 Interview-Dossier: TRUMPF Trainee IT Governance & Infra]]
- [[2026-10-19_EY_Technology_Consulting_SAP_Transformation|🎯 Interview-Dossier: EY Technology Consulting / SAP Transformation]]
- [[2026-10-08_msg_systems_Technical_SAP_Consultant|🎯 Interview-Dossier: msg systems Technical SAP Consultant]]
- [[2026-06-11_Computacenter_IT_Service_Architecture|🎯 Interview-Dossier: Computacenter IT Service Architecture]]

---

## 🚄 2. Berufliche Praxis: SSB S/4HANA (24M) & Datacenter One (12M)
- [[SSB_Grossprojekt_SAP4SSB|🚆 Großprojekt SAP4SSB: Übersicht TP1–TP5 & Governance (24 Monate)]]
- [[MOC_SSB_Transformation|🗺️ MOC SSB Transformation Gesamtatlas]] • [[MOC_SSB_Dokumentenatlas|📚 Dokumentenatlas (1.890 Dateien)]]
- **Teilprojekt-Pläne (WBS):** [[TP1_Change_Management_People_Plan|👥 TP1 Change]] • [[TP2_Kaufmaennische_Prozesse_Plan|💶 TP2 Kaufmännisch]] • [[TP3_Technische_Prozesse_Instandhaltung_Plan|🔧 TP3 Instandhaltung]] • [[TP4_IT_Unterstuetzung_Integration_Plan|☁️ TP4 IT & Basis]] • [[TP5_Gesamtsteuerung_PMO_Betriebsvereinbarung_Plan|🏛️ TP5 PMO & Gesamtsteuerung]]
- **Solution Design & Migration:** [[SSB_Solution_Design_FI_CO|📐 FI/CO & Trennungsrechnung]] • [[Trennungsrechnung_OEPNV_EU1370|⚖️ EU-VO 1370/2007]] • [[Universal_Journal_ACDOCA|📑 ACDOCA]] • [[SSB_Datenmigration_LTMC_CVI|🔄 Datenmigration LTMC & CVI]] • [[SSB_Foerdermittel_Grants_Management|🏛️ Grants Management]]
- **Architektur & Tooling:** [[S4HANA_Plattformisierung|🧩 S/4HANA Plattformisierung]] • [[Clean_Core_Paradigma|⭐ Clean Core]] • [[SSB_Tool_Governance_Signavio_CALM|🛠️ Signavio, Cloud ALM & Enable Now]] • [[SSB_Interviews_Experten_Transkripte|🎙️ Experteninterviews]] • [[SSB_Mitbestimmung_Betriebsrat_Dossier|🏛️ Betriebsrat § 87]] • [[SSB_Interview_Stories_STAR|🌟 5 STAR-Stories]] • [[SSB_S4HANA_12_Strategische_Domaenen_Notebook|🧠 12 Strategische Domänen]]
- **Datacenter One (12M INOC):** [[DC1_ITIL4_Service_Operations|🏢 DC1 24/7 INOC & ITIL 4 Operations]] • [[DC1_Hardware_Lifecycle_Management|💻 DC1 Hardware Lifecycle Management (Visio BPMN)]]

---

## 🎓 3. Akademische Exzellenz: 300 ECTS Studium (Universität Stuttgart)
> *Hinweis: Sauber kuratierte Modul- & Abschlussarbeiten-Karten. Die dazugehörigen Vorlesungsfolien- & Übungsvolltexte liegen durchsuchbar in Schicht 2 (`[[00_DataLake_Index]]`).*

### Abschlussarbeiten, Zertifikate & Spitzenleistungen
- [[Modul_Masterarbeit|⭐ Masterarbeit: Kritische Erfolgsfaktoren der ERP-Plattformisierung von SAP S/4HANA (Note 1,0 | 30 ECTS | 126 S.)]]
- [[Modul_Bachelorarbeit|📜 Bachelorarbeit: Boundary Resources in Low-Code Plattformen OutSystems & Mendix (Note 1,7 | 12 ECTS | 103 S.)]]
- [[Modul_TOGAF_Scape|🏛️ TOGAF 9 ADM Zertifizierung (Scape Consulting, 16.01.2020)]]
- [[Modul_Übersicht|📋 Gesamtübersicht aller 300 ECTS Bachelor- & Mastermodule]]

### Master of Science (120 ECTS | Gesamtnote 1,6)
- [[Modul_Digitale_Nachhaltigkeit|🌱 Digitale Nachhaltigkeit: CSRD-Abfallbilanz J. Schmalz GmbH (Note 1,0 | 6 ECTS)]]
- [[Modul_FPWI|⚡ FPWI: Smart Service Blueprinting für IoT-Plattformen (Note 1,3 | 6 ECTS | SUS 85/100)]]
- [[Modul_Advanced_Software_Engineering|💻 Advanced Software Engineering: DDD & CI/CD (Note 1,6 | 6 ECTS)]]
- [[Modul_Software_Architektur|🏛️ Software-Architektur: Microservices, Event-Driven & QASD (Note 1,7 | 6 ECTS)]]
- [[Modul_Innovationsmanagement|💡 Innovationsmanagement & Plattform-Ökosysteme (Note 1,7 | 6 ECTS)]]
- [[Modul_Applied_AI|🧠 Applied AI & Upcoming Technologies in Industries (Note 1,7 | 6 ECTS)]]
- [[Modul_Forschungsmethoden|📊 Forschungsmethoden in der WI: Algorithm Aversion (Note 1,7 | 6 ECTS)]]
- [[Modul_Seminar_WI2|🤖 Seminar WI 2: MRK Industrie 5.0 PRISMA SLR (Note 1,7 | 6 ECTS)]]
- [[Modul_TEUI|🌍 Theorie & Empirie internationaler Unternehmenstätigkeit (Note 1,7 | 6 ECTS)]]
- [[Modul_AI4IoT|📡 AI4IoT: Sensor-Datenströme & Edge AI (Note 2,0 | 6 ECTS)]]
- [[Modul_Cloud_Computing|☁️ Cloud Computing: AWS Serverless & Well-Architected (Note 2,0 | 6 ECTS)]]
- [[Modul_ISG|📦 Innovationsmethoden (ISG): PatentRadar für Verpackungsindustrie (Note 2,0 | 6 ECTS)]]
- [[Modul_Datenbanken|💾 Datenbanken & Informationssysteme (Note 2,7 | 6 ECTS)]]
- [[Modul_Management_IT_Unternehmen|📈 Management von IT-Unternehmen: ITIL & COBIT (Note 3,0 | 6 ECTS)]]
- [[Modul_SOM|🔄 Service Operations Management (Note 3,0 | 6 ECTS)]]
- **Zusatzmodule:** [[Modul_AIM|📚 AIM]] • [[Modul_Quanteninformatik|⚛️ Quanteninformatik]] • [[Modul_SmartCities|🏙️ Smart Cities & IoT]]

### Bachelor of Science (180 ECTS | Gesamtnote 3,0)
- **Top-Module:** [[Modul_EBusiness|🛒 Informationssysteme im E-Business (Bestnote 1,0)]] • [[Modul_Informationsverarbeitungspraktikum|📊 IVP Unternehmensanalyse 0x539-Wear (2,3)]] • [[Modul_Modellierung|📐 Modellierung BPMN/UML (2,3)]] • [[Modul_Seminar_Interdisziplinaer|🤖 Seminar ML & Big Data (2,3)]]
- **Wirtschaftsinformatik & Informatik:** [[Modul_EWI|🏢 EWI (2,7)]] • [[Modul_MBIS|🔄 MBIS / ERP (2,7)]] • [[Modul_Informationsmanagement_Bachelor|📊 IM & BI (3,0)]] • [[Modul_DSA|🌲 DSA (3,0)]] • [[Modul_Programmentwicklung|💻 PE (3,0)]] • [[Modul_Softwarepraktikum|💻 SOPRA (3,0)]] • [[Modul_MCI|🖥️ MCI/UX (3,3)]] • [[Modul_EST|⚙️ EST (3,7)]] • [[Modul_AFS|🔤 AFS (3,7)]] • [[Modul_Wissensverarbeitung|🧠 Wissensverarbeitung (3,7)]] • [[Modul_PSE|☕ PSE Java (4,0)]] • [[Modul_Informatikrecht|⚖️ Informatikrecht (4,0)]]
- **BWL / VWL / Quantitativ:** [[Modul_Statistik2|📈 Statistik II (2,7)]] • [[Modul_GBWL1|📚 GBWL 1 (2,7)]] • [[Modul_GBWL4|💰 GBWL 4 (2,7)]] • [[Modul_GVWL1|📉 GVWL 1 (2,7)]] • [[Modul_Profilseminar_HRM|👥 Profilseminar HRM (3,0)]] • [[Modul_BWL1|👔 BWL 1 (3,3)]] • [[Modul_Statistik1|📊 Statistik I (4,0)]] • [[Modul_Mathematik|📐 Mathematik (4,0)]] • [[Modul_Dienstleistungsmanagement|🏨 Dienstleistungsmanagement (4,0)]] • [[Modul_Schreibwerkstatt|✍️ Schreibwerkstatt (BE)]]

---

## ⚡ 4. Second Brain Zettelkasten & Konzepte (`04_Second_Brain_Zettelkasten/`)
- **Architektur & ERP-Synthese:** [[Bimodale_ERP_Plattformisierung_BTP|🧩 Bimodale ERP-Plattformisierung & Boundary Resources]] • [[TOGAF_9_ADM_Enterprise_Architecture_ERP|🏛️ TOGAF 9 ADM in ERP-Transformationen]] • [[Solution_Design_Signavio_CloudALM_Governance|📐 Solution Design Governance (Signavio / CALM / Enable Now)]] • [[Data_Migration_CVI_LTMC_Selective_Transition|🔄 Datenmigration: LTMC, CVI & Saldo 0,00 €]] • [[SAP_Trennungsrechnung_Public_Sector_EU1370|💶 ÖPNV Trennungsrechnung EU-1370 im ACDOCA]]
- **IT-Security, Operations & AI:** [[SAP_HCM_Berechtigungsarchitektur_IAM|🔐 SAP HCM IAM & UMT Case]] • [[Third_Level_Support_Incident_Root_Cause|🩺 3rd-Level-Support & Root-Cause (ITIL 4)]] • [[Generative_AI_LLM|🤖 Generative AI & RAG]] • [[IoT_Architekturen|📡 IoT-Architekturen]]
- **Informatik & Methoden:** [[Algorithmen_und_Datenstrukturen|🌲 Algorithmen]] • [[SQL_und_Datenmodellierung|💾 SQL & Datenmodellierung]] • [[Software_Engineering_Prinzipien|💻 Software Engineering]] • [[E_Business_Konzepte|🛒 E-Business]] • [[Wissenschaftliche_Methodik|🔬 Wissenschaftliche Methodik]]
- **Personal OS (isoliert):** [[Gewohnheiten|⚡ Gewohnheiten]] • [[Trainingsplan_Visar|💪 Trainingsplan]] • [[NoFap|🧠 Dopamin Reset]] • [[Retrospektive_Wintersemester_23_24|📝 WS 23/24 Retrospektive]]

---

## 🗄️ 5. Schicht 2: Volltext Data Lake & System (`05_Archiv/`)
- [[00_DataLake_Index|🗄️ Volltext Data Lake Master-Index (alle Vorlesungs- & SSB/DC1-Volltexte + 85 Split-Bände)]]
- [[00_CHANGELOG|📜 System Release-Historie (CHANGELOG)]] • [`graph_manifest.json`](file:///C:/Users/SHQIPTAR634/Documents/Obsidian%20Vault/graph_manifest.json)
"""
    with open(os.path.join(VAULT_DIR, "00_INDEX.md"), "w", encoding="utf-8") as f:
        f.write(index_md)

    print(f"[T102] Moved {moved_personal} Personal_OS file(s), updated graph.json & rebuilt 00_INDEX.md (Layer 1 vs Layer 2).")


ESSENCES = {
    r"03_SAP_EnterpriseArchitecture\SSB_Grossprojekt_SAP4SSB.md": """\n> [!ABSTRACT] **60-Sekunden-Essenz: Großprojekt SAP4SSB (24 Monate IT-PMO & TP5)**
> - **Umfang & Zeitraum:** `05/2024 – 04/2026` bei der **Stuttgarter Straßenbahnen AG** (`3.700+` Mitarbeitende); Transition von ECC 6.0 nach **SAP S/4HANA Private Cloud (RISE with SAP, Greenfield)**.
> - **Meine Rolle (TP5 / Gesamtsteuerung):** Operative PMO-Unterstützung direkt unter Gesamtprojektleiter **Roland Nowak** und IT-Leiter **Dietmar Fillinger** — MS-Project-Masterplan, Teilprojekt-Status (`TP1–TP5`), Steuerung externer Partner (**Nagarro, Axians, Evora, apsolut**) und Tool-Governance (**Signavio, Cloud ALM, Enable Now**).
> - **Projektstand bei Austritt (`04/2026`):** **Explore-Phase abgeschlossen**, Solution Design Document (`SDD`) vollständig abgenommen, Datenmigrations-Vorschlag (`LTMC`/`CVI`) erstellt und Pilot-Betriebsvereinbarung verabschiedet.""",

    r"03_SAP_EnterpriseArchitecture\03_Governance_Vergabe\TP1_Change_Management_People_Plan.md": """\n> [!ABSTRACT] **60-Sekunden-Essenz: Teilprojekt 1 – Change Management & People (WBS 16–63)**
> - **Fokus:** Akzeptanz, Stakeholder-Kommunikation (*„Zukunft auf Schiene“*, Coffee Corners), Multiplikatoren-Netzwerk über alle Unternehmensbereiche (`UB K, T, W, Z`) und Qualifizierung.
> - **Mein Beitrag:** Ausarbeitung des strategischen Übergabekonzepts für **SAP Enable Now** an die Personalentwicklung (`UB AC`) im Single-Source-Prinzip (1 Aufnahme → Handbuch, Simulation, Quiz, In-App-Hilfe).""",

    r"03_SAP_EnterpriseArchitecture\03_Governance_Vergabe\TP2_Kaufmaennische_Prozesse_Plan.md": """\n> [!ABSTRACT] **60-Sekunden-Essenz: Teilprojekt 2 – Kaufmännische Prozesse (WBS 64–112)**
> - **Fokus:** Fit-to-Standard mit Partner **Nagarro** für Finance & Controlling (`FI/CO`, Universal Journal `ACDOCA`), **Trennungsrechnung nach EU-VO 1370/2007**, **Grants Management (`LGVFG/GVFG`)**, Beschaffung (**MM/Ariba**) und Vertrieb (**PATRIS-Subsystem**).
> - **Mein Beitrag:** Dokumentation kaufmännischer Geschäftsprozesse für das **Solution Design Document (SDD)** sowie Analyse/Vorschlag von Migrationsobjekten und Staging-Tabellen im **SAP Migration Cockpit (`LTMC`)**.""",

    r"03_SAP_EnterpriseArchitecture\03_Governance_Vergabe\TP3_Technische_Prozesse_Instandhaltung_Plan.md": """\n> [!ABSTRACT] **60-Sekunden-Essenz: Teilprojekt 3 – Technische Instandhaltung / EAM (WBS 173–196)**
> - **Fokus:** Stadtbahn-, Bus- und Fahrleitungs-Instandhaltung (`SAP EAM/PM`) mit Implementierungspartner **Evora** inklusive mobiler Werkstattausführung über **SAP Service and Asset Manager (`SSAM`)**.
> - **Governance-Bezug:** Synchronisation der Material-/Anlagenstammdaten mit `TP2` (`FI-AA` / `MM`), Berechtigungsklärung (`Betriebsrat`) und Einbindung in den Gesamtterminplan `TP5`.""",

    r"03_SAP_EnterpriseArchitecture\03_Governance_Vergabe\TP4_IT_Unterstuetzung_Integration_Plan.md": """\n> [!ABSTRACT] **60-Sekunden-Essenz: Teilprojekt 4 – IT-Infrastruktur, Basis & Integration (WBS 197–202)**
> - **Fokus:** **RISE with SAP Private Cloud**, Mandantenaufbau (`ES4` `M300`/`M100`), Partner **Axians**, **SAP BTP Integration Suite** und Entkopplung geschäftskritischer Subsysteme (`xSuite`, `d.velop`, `PATRIS`, `ADS`, `SSO`).
> - **Mein Beitrag:** Tracking und T-Shirt-Sizing (`S/M/L`) offener IT-GAPs in **SAP Cloud ALM** mit Armin Heinrich & Axians, damit End-to-End-Tests termingerecht starten konnten.""",

    r"03_SAP_EnterpriseArchitecture\03_Governance_Vergabe\TP5_Gesamtsteuerung_PMO_Betriebsvereinbarung_Plan.md": """\n> [!ABSTRACT] **60-Sekunden-Essenz: Teilprojekt 5 – Gesamtsteuerung, PMO & Betriebsrat (WBS 203–297)**
> - **Fokus:** Lenkungsausschuss-Reporting (`Steering Board`), Ressourcenplanung in **MS Project**, Risikomanagement, Integration der 4 Partner und Begleitung der **Betriebsvereinbarungen (`§ 87 BetrVG`)**.
> - **Meilensteine:** Explore-Abschluss (`29.08.2025`), Pilot-Betriebsvereinbarung (`01.04.2026`), geplantes Ziel-Go-Live (`01.01.2027` nach meinem Studienende/`04/2026`).""",

    r"03_SAP_EnterpriseArchitecture\DC1_ITIL4_Service_Operations.md": """\n> [!ABSTRACT] **60-Sekunden-Essenz: Datacenter One GmbH (12 Monate | INOC & ITIL 4)**
> - **Zeitraum & Rolle:** `05/2023 – 04/2024` als Werkstudent im **24/7 Information Network Operation Center (INOC)** unter **Helmut Schmidpeter**.
> - **Kernleistung:** Single Point of Contact (**SPoC**) in **Jira Service Management**, Echtzeit-Überwachung von Core-Netzwerken, Dark Fiber, USV & HVAC via **PRTG**, SLA-Carrier-Koordination sowie Konzeption einer **Confluence-Wissensdatenbank** für SOPs und Post-Mortems.""",

    r"03_SAP_EnterpriseArchitecture\DC1_Hardware_Lifecycle_Management.md": """\n> [!ABSTRACT] **60-Sekunden-Essenz: Hardware Lifecycle Management (HLM | Datacenter One)**
> - **Projektziel:** Standardisierung des gesamten Arbeitsplatz- und Leitstand-Lifecycles für über `100` hochkritische Arbeitsplatzsysteme (**Dell PoC**, Staging, Rollout, DSGVO-konformes Decommissioning).
> - **Deliverable:** Vollständige **BPMN 2.0-Prozessmodellierung in Microsoft Visio (`HLM_v2.vsdx`)** zur Vermeidung von Stillstandszeiten im 24/7 Leitstandbetrieb.""",

    r"03_SAP_EnterpriseArchitecture\SSB_Solution_Design_FI_CO.md": """\n> [!ABSTRACT] **60-Sekunden-Essenz: SSB Solution Design FI/CO & Public Sector**
> - **Kernarchitektur:** Zusammenführung von Hauptbuch und Controlling im **Universal Journal (`ACDOCA`)** als Single Source of Truth inklusive paralleler Rechnungslegung (`HGB`, Steuerrecht).
> - **ÖPNV-Spezialität:** Gerichtsfeste **Trennungsrechnung nach EU-VO 1370/2007 & PBefG** über Profitcenter/Segment/PSP sowie Integration von **Grants Management (`LGVFG`)** bis in die Anlagenbuchhaltung (`FI-AA`).""",

    r"03_SAP_EnterpriseArchitecture\SSB_Datenmigration_LTMC_CVI.md": """\n> [!ABSTRACT] **60-Sekunden-Essenz: Datenmigration & CVI (`SAP4SSB`)**
> - **Werkzeug & Ansatz:** **SAP S/4HANA Migration Cockpit (`LTMC` / Staging-Tabellen)** für kontrollierte Greenfield-Datenübernahme aus dem stark modifizierten ECC 6.0.
> - **Revisionssicherheit:** Bereinigung von Debitoren/Kreditoren über **Customer-Vendor-Integration (`CVI`)** zu Business Partnern sowie Abstimmung des Migrations-Übernahmekontos auf exakt **`0,00 €` Restsaldo**.""",

    r"03_SAP_EnterpriseArchitecture\SSB_Tool_Governance_Signavio_CALM.md": """\n> [!ABSTRACT] **60-Sekunden-Essenz: Enterprise Toolchain Governance (`SAP4SSB`)**
> - **Dreiklang:** **SAP Signavio** (Prozessmodellierung `BPMN 2.0` End-to-End) → **SAP Cloud ALM** (`How2Handle` Quickguide, Requirements, Tasks & Testmanagement) → **SAP Enable Now** (Key-User-Befähigung & Single-Source-Lerninhalte).
> - **Wirkung:** Vermeidung von Tool-Silos zwischen internen Fachbereichen und den Implementierungspartnern Nagarro & Evora.""",

    r"03_SAP_EnterpriseArchitecture\S4HANA_Plattformisierung.md": """\n> [!ABSTRACT] **60-Sekunden-Essenz: Ganzheitliche ERP-Plattformisierung (Masterarbeit 1,0)**
> - **Kernaussage:** S/4HANA-Transformation darf nicht auf „Clean Core“ verengt werden — Plattformisierung umfasst das organisatorisch-technische Zusammenspiel aus **Bimodaler IT-Entkopplung (`BTP`)**, **Plattform-Governance**, **Boundary Resources** und **Absorptive Capacity**.
> - **Empirische Basis:** `126 Seiten`, **`12` Experteninterviews** bei `SSB AG`, `Axians` & `Nagarro`, qualitative Inhaltsanalyse nach **Mayring** (Prof. Dr. Georg Herzwurm, **Note `1,0`**).""",

    r"03_SAP_EnterpriseArchitecture\01_Architektur_Technik\Clean_Core_Paradigma.md": """\n> [!ABSTRACT] **60-Sekunden-Essenz: Clean Core & Bimodale Entkopplung (`SAP BTP`)**
> - **Prinzip:** Keine Core-Modifikationen (`Z-Tabellen`, klassische User-Exits) im S/4HANA-Standard; Differenzierung konsequent als **Tier-1 (ABAP Cloud/RAP)** oder **Side-by-Side auf SAP BTP**.
> - **Schnittstellen:** Entkopplung von Subsystemen (`PATRIS`, `xSuite`, `d.velop`) über freigegebene APIs und Event-Driven Architecture zur Sicherung der **Upgrade- und Cloud-Fähigkeit**.""",

    r"03_SAP_EnterpriseArchitecture\02_Kaufmaennische_Prozesse\Trennungsrechnung_OEPNV_EU1370.md": """\n> [!ABSTRACT] **60-Sekunden-Essenz: Trennungsrechnung im ÖPNV (`EU-VO 1370/2007`)**
> - **Regulatorischer Zwang:** Verbot von Quersubventionierung bzw. Überkompensation zwischen gemeinwirtschaftlichem ÖPNV und gewerblichen Geschäftsfeldern.
> - **SAP-Umsetzung:** Automatische Kontierung auf Profitcenter/Segment/Funktionsbereich je Buchungszeile im **`ACDOCA`**, ergänzt um **Grants Management** für Investitionszuschüsse.""",

    r"03_SAP_EnterpriseArchitecture\02_Kaufmaennische_Prozesse\Universal_Journal_ACDOCA.md": """\n> [!ABSTRACT] **60-Sekunden-Essenz: Universal Journal (`ACDOCA`) als Single Source of Truth**
> - **Technologiewandel:** Ersetzt getrennte Summen- und Indextabellen aus ECC (`GLT0`, `BSEG`/`COEP`-Redundanzen) durch eine einzige **HANA Column-Store-Einzelpostentabelle**.
> - **Geschäftsnutzen:** Keine langwierige Abstimmung zwischen `FI` und `CO` zum Monatsabschluss (**Fast Close**), direkte Drilldowns bis auf Belegebene.""",

    r"02_Wirtschaftsinformatik_300ECTS\Modul_Masterarbeit.md": """\n> [!ABSTRACT] **60-Sekunden-Essenz: Masterarbeit (Note 1,0 | 30 ECTS | Prof. Herzwurm)**
> - **Offizieller Titel:** *„Kritische Erfolgsfaktoren in der Transformation großer ERP-Systeme: Eine Untersuchung am Beispiel der Plattformisierung von SAP S/4HANA“* (`126 Seiten`).
> - **Design & Beitrag:** `12` leitfadengestützte Experteninterviews (`SAP4SSB`, Gesamt-PL Nowak, TPLs, Lead-Architekten Axians/Nagarro), qualitatives Codebuch nach **Mayring** → **4×3 CSF-Framework** über Organisation, Mensch/Absorptive Capacity, Plattform-Technik und PMO-Governance.""",

    r"02_Wirtschaftsinformatik_300ECTS\Modul_Bachelorarbeit.md": """\n> [!ABSTRACT] **60-Sekunden-Essenz: Bachelorarbeit (Note 1,7 | 12 ECTS | Prof. Herzwurm)**
> - **Offizieller Titel:** *„Die Bedeutung von Boundary Resources in Low-Code Entwicklungsplattformen: Eine qualitative Untersuchung am Beispiel von OutSystems und Mendix“* (`103 Seiten`).
> - **Brücke zur Karriere:** Legt mittels **Boundary Resource Theory (Ghazawneh & Henfridsson, 14 Klassen ABR/DBR/SBR)** exakt die theoretische Basis dafür, wie später in S/4HANA & BTP zwischen Kontrolle und Erweiterbarkeit balanciert wird.""",

    r"02_Wirtschaftsinformatik_300ECTS\Modul_EBusiness.md": """\n> [!ABSTRACT] **60-Sekunden-Essenz: Informationssysteme im E-Business (Bestnote 1,0)**
> - **Kerninhalt:** Architekturen elektronischer Marktplätze, B2B-Integration (`EDIFACT`/`XML`), E-Procurement, Plattformökonomie und digitale Geschäftsmodelle bei **Prof. Dr. Georg Herzwurm**.
> - **Praxisbrücke:** Direkter Transfer in die moderne **E-Procurement-/Ariba-Welt** und Plattformökosysteme in S/4HANA.""",

    r"02_Wirtschaftsinformatik_300ECTS\Modul_Digitale_Nachhaltigkeit.md": """\n> [!ABSTRACT] **60-Sekunden-Essenz: Digitale Nachhaltigkeit – J. Schmalz GmbH (Note 1,0 | 6 ECTS)**
> - **Reales Industrieprojekt:** Automatisierung der CSRD-konformen Abfallbilanz-Berichterstattung für Weltmarktführer **J. Schmalz GmbH** (Betreuung: Dr. Dimitri Petrik).
> - **Ergebnis:** **BPMN 2.0 Ist-Prozessmodellierung** + **PowerShell-Automatisierungsskripte** zur fehlerfreien Datenextraktion aus Entsorgungsbelegen — direkt übertragbar auf `SAP EHS/CSRD`.""",

    r"02_Wirtschaftsinformatik_300ECTS\Modul_FPWI.md": """\n> [!ABSTRACT] **60-Sekunden-Essenz: Forschungsprojekt WI – Smart Service Blueprinting (Note 1,3 | 6 ECTS)**
> - **Forschungsartefakt:** Weiterentwicklung des klassischen Service Blueprintings um physische Sensorik-/Aktorik-Ebenen und Cloud-Event-Streams für **IoT/CPS-Systeme**.
> - **Validierung:** Rigoroses **Design Science Research (DSRM nach Peffers)** mit **Thinking-Aloud Usability-Tests** und exzellentem **SUS-Score `85/100`**.""",

    r"02_Wirtschaftsinformatik_300ECTS\Modul_Advanced_Software_Engineering.md": """\n> [!ABSTRACT] **60-Sekunden-Essenz: Advanced Software Engineering (Note 1,6 | 6 ECTS)**
> - **Schwerpunkt (Prof. Dr. Steffen Becker):** **Domain-Driven Design (DDD)**, Architektur-Erosion vermeiden, Teststrategien, **CI/CD** und DevOps-Qualitätssicherung.
> - **Relevanz:** Liefert das saubere Architektur- und Bounded-Context-Fundament für **SAP CAP/RAP**, Side-by-Side-Extensions und professionelle IT-Umgebungen.""",

    r"02_Wirtschaftsinformatik_300ECTS\Modul_Software_Architektur.md": """\n> [!ABSTRACT] **60-Sekunden-Essenz: Software-Architektur / QASD (Note 1,7 | 6 ECTS)**
> - **Schwerpunkt (Prof. Dr. Steffen Becker):** Qualitätsgetriebener Architekturentwurf (**QASD**), Microservices vs. Monolithen, Event-Driven Systems, ATAM-Bewertung und Markov-Zuverlässigkeitsanalyse.
> - **Transfer:** Fundierte Bewertung von S/4HANA Integrationsmustern (`Sync vs. Async`, `Event Mesh`, `Entkopplung`).""",

    r"02_Wirtschaftsinformatik_300ECTS\Modul_Innovationsmanagement.md": """\n> [!ABSTRACT] **60-Sekunden-Essenz: Innovationsmanagement (Note 1,7 | 6 ECTS)**
> - **Kerninhalte:** Stage-Gate-Prozesse, Open Innovation, Plattform-Ökosysteme, Technologiediffusion und Management von Geschäftsmodellinnovationen.
> - **Synergie:** Erklärt die organisatorischen Adoptionsbarrieren hinter der **SAP-S/4HANA-Transformation** und beim Change-Enablement.""",

    r"02_Wirtschaftsinformatik_300ECTS\Modul_Applied_AI.md": """\n> [!ABSTRACT] **60-Sekunden-Essenz: Applied AI & Upcoming Technologies (Note 1,7 | 6 ECTS)**
> - **Kerninhalte:** Industrieller Einsatz von Machine Learning, **LLMs**, Generative AI Pipelines, RAG-Architekturen und Bewertung von KI-Use-Cases entlang von Compliance und Business Value.
> - **Eigener Proof:** Architektur dieses **Local Hybrid RAG V3 (`career_os_rag.db`)** mit BM25 + 768d Vektor-Fusion.""",

    r"02_Wirtschaftsinformatik_300ECTS\Modul_Forschungsmethoden.md": """\n> [!ABSTRACT] **60-Sekunden-Essenz: Forschungsmethoden in der WI (Note 1,7 | 6 ECTS)**
> - **Kerninhalte:** Quantitative und qualitative Erhebungsdesigns, Hypothesentests, Gütekriterien (Reliabilität/Validität) sowie eigene empirische Studie zu **Algorithm Aversion**.
> - **Transfer:** Methodische Vorbereitung für empirisches Arbeiten in der Masterarbeit (`Mayring`, `12` Experteninterviews) und datengetriebene Stakeholder-Analysen.""",

    r"02_Wirtschaftsinformatik_300ECTS\Modul_Seminar_WI2.md": """\n> [!ABSTRACT] **60-Sekunden-Essenz: Seminar WI 2 – Industrie 5.0 & MRK (Note 1,7 | 6 ECTS)**
> - **Forschungsdesign:** Systematische Literaturanalyse nach **PRISMA 2020** (`570` gesichtete / `439` tief analysierte Studien) zu **Mensch-Roboter-Kollaboration (MRK)** und Technologieakzeptanz.
> - **Ergebnis:** Synthese aus menschzentrierter Automatisierung (Industrie 5.0), Vertrauen in KI/Robotik und Change-Anforderungen.""",

    r"02_Wirtschaftsinformatik_300ECTS\Modul_TEUI.md": """\n> [!ABSTRACT] **60-Sekunden-Essenz: Internationale Unternehmenstätigkeit / TEUI (Note 1,7 | 6 ECTS)**
> - **Schwerpunkt (Prof. Oesterle):** Markteintrittsstrategien, globale Konzernsteuerung (Zentrale vs. Landesgesellschaften), Kultur- und Governance-Modelle.
> - **Praxisbrücke:** Direkter Mehrwert für internationale Rollouts und Konzernarchitekturen (z. B. globale **Schwarz-Pyramide** in `34–37` Ländern vs. lokale Payroll/Rechtsräume).""",

    r"02_Wirtschaftsinformatik_300ECTS\Modul_AI4IoT.md": """\n> [!ABSTRACT] **60-Sekunden-Essenz: AI4IoT – Sensor-Datenströme & Edge AI (Note 2,0 | 6 ECTS)**
> - **Schwerpunkt (Prof. Lachenmaier / Prof. Herzwurm):** Telemetrie, Zeitreihendaten, Edge-vs-Cloud-Inferenz und vorausschauende Wartung (**Predictive Maintenance**) im industriellen Umfeld.
> - **Verbindung:** Verknüpft IoT-Architektur mit **SAP EAM / SSAM** (`TP3` Instandhaltung) sowie **Smart Service Blueprinting (`FPWI`)**.""",

    r"02_Wirtschaftsinformatik_300ECTS\Modul_Cloud_Computing.md": """\n> [!ABSTRACT] **60-Sekunden-Essenz: Cloud Computing & AWS Well-Architected (Note 2,0 | 6 ECTS)**
> - **Architekturfokus:** Serverless Cloud Patterns (**AWS Lambda, EventBridge, Step Functions, DynamoDB**), Skalierbarkeit, Resilienz (`Well-Architected Framework`) und SaaS-Betrieb.
> - **Brücke:** Direkt übertragbar auf **RISE with SAP Private Cloud**, **SAP BTP Event Mesh** und verteilte Cloud-Betriebsmodelle (**DC1 / STACKIT**).""",

    r"02_Wirtschaftsinformatik_300ECTS\Modul_ISG.md": """\n> [!ABSTRACT] **60-Sekunden-Essenz: Innovationsmethoden (ISG) – PatentRadar Klingele (Note 2,0 | 6 ECTS)**
> - **Projektinhalt:** Konzeption eines hybriden **SaaS- & Beratungs-Geschäftsmodells (*PatentRadar*)** zur KI-gestützten Patentrecherche für ein führendes Verpackungsunternehmen (**Klingele Paper & Packaging**).
> - **Deliverable:** End-to-End **BPMN-Prozessmodellierung** für RPA-Automatisierung (**UiPath**-Potenzialanalyse) sowie fundierte **Business-Case-Kalkulation**.""",

    r"02_Wirtschaftsinformatik_300ECTS\Modul_Informationsverarbeitungspraktikum.md": """\n> [!ABSTRACT] **60-Sekunden-Essenz: IVP Unternehmensanalyse 0x539-Wear (Note 2,3 | 6 ECTS)**
> - **Analytik & Controlling:** Mehrstufige **Deckungsbeitragsrechnung (`DB I–IV`)**, ABC-Analysen, Make-or-Buy-Entscheidungen und Plan-Ist-Abweichungsanalysen im ERP-Kontext.
> - **Praxisbezug:** Schafft das betriebswirtschaftliche Fundament für **SAP CO (Ergebnisrechnung/PSP)** und datenbasierte Profitabilitätssteuerung.""",

    r"02_Wirtschaftsinformatik_300ECTS\Modul_Modellierung.md": """\n> [!ABSTRACT] **60-Sekunden-Essenz: Modellierung – BPMN 2.0, UML & Petrinetze (Note 2,3 | 6 ECTS)**
> - **Methodik (Prof. Mitschang):** Formale Unternehmens- und Softwaremodellierung (**BPMN 2.0, UML, Petrinetze, ERM, Normalformen `1NF–BCNF`**, Relationale Algebra).
> - **Praxistransfer:** Eins-zu-eins angewandt in **SAP Signavio** (`SSB AG`), **MS Visio HLM** (`Datacenter One`) und **Solution Design Document (`SDD`)**.""",

    r"02_Wirtschaftsinformatik_300ECTS\Modul_TOGAF_Scape.md": """\n> [!ABSTRACT] **60-Sekunden-Essenz: TOGAF 9 ADM Zertifizierung (Scape Consulting, 16.01.2020)**
> - **Kompetenz:** Strukturierte Unternehmensarchitektur entlang der **8 ADM-Phasen** (Preliminary, Architecture Vision, Business/IS/Tech Architecture, Opportunities & Solutions, Migration Planning).
> - **Anwendung:** Verbindet IT-Strategie und **Architecture Repository** direkt mit **SAP Activate (`Explore`/`Realize`)**, Schnittstellenlandkarten und **Carrier-/RZ-SOPs (`DC1`)**.""",
}


def inject_60s_compact_blocks():
    """T103: Injects unified > [!ABSTRACT] 60-Sekunden-Essenz callouts right after first H1 heading."""
    updated = 0
    for rel, block in ESSENCES.items():
        fp = os.path.join(VAULT_DIR, rel)
        if not os.path.exists(fp):
            print(f"  [!] Skip missing note: {rel}")
            continue
        with open(fp, "r", encoding="utf-8", errors="ignore") as f:
            txt = f.read()
        if "60-Sekunden-Essenz" in txt:
            continue
        lines = txt.splitlines()
        out = []
        inserted = False
        in_fm = False
        fm_done = False
        for idx, line in enumerate(lines):
            out.append(line)
            if idx == 0 and line.strip() == "---":
                in_fm = True
                continue
            if in_fm and not fm_done and line.strip() == "---":
                fm_done = True
                continue
            if (fm_done or not in_fm) and not inserted and line.startswith("# "):
                out.append(block.lstrip("\n"))
                inserted = True
        if not inserted:
            continue
        with open(fp, "w", encoding="utf-8", errors="replace") as f:
            f.write("\n".join(out) + ("\n" if txt.endswith("\n") else ""))
        updated += 1
    print(f"[T103] Added 60-Sekunden-Essenz blocks to {updated} curated station/module note(s).")
    return updated


if __name__ == "__main__":
    print("=" * 70)
    print("🚀 EXECUTING PHASE 1: KNOWLEDGE & PROFILE OS 2.0 (T101–T103)")
    print("=" * 70)
    archive_volltext_datalake()
    isolate_personal_os_and_rebuild_index()
    inject_60s_compact_blocks()
    print("[OK] Phase 1 migration script completed cleanly!")
