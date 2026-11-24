---
id: changelog-system-releases
title: "Changelog & System Release Protocol"
type: log
domain: system-governance
status: evergreen
summary: "Revisionssicheres Änderungsprotokoll nach Keep a Changelog und Conventional Commits für alle Systemupdates und Git-Releases auf main."
tags:
  - changelog
  - governance
  - releases
  - system_history
aliases:
  - Release Notes
  - Changelog
  - System History
last_updated: "2026-11-24"
---

# 📜 CHANGELOG & SYSTEM RELEASE PROTOCOL (Visar Murseli | Personal Career OS)

Alle signifikanten Änderungen, Pipeline-Updates, architektonischen Erweiterungen und Git-Commits auf den Branch `main` werden in diesem Dokument lückenlos nach dem Standard [Keep a Changelog](https://keepachangelog.com/de/1.0.0/) und [Conventional Commits](https://www.conventionalcommits.org/de/v1.0.0/) protokolliert.

---

## [Unreleased] - 2026-11-24

---

## [1.13.0] - 2026-11-24 (Interview-Dossiers, Live GMX IMAP /sync, Datenbereinigung & Windows-Autostart)

### 🎯 Kontext & Leitmotiv
Abschluss der Ausbaustufen (B) & (C): Alle laufenden Top-Interviewprozesse verfügen über dedizierte Obsidian-Dossiers, der Excel- und Obsidian-Bewerbungstracker ist von E-Mail-Parser-Artefakten bereinigt, und beide GMX-Postfächer lassen sich über `/sync` per Telegram live abgleichen — ergänzt durch einen lautlosen Windows-Autostart für Portal & Bot.

### 🚀 Neu hinzugefügt & Erweitert (Added & Enhanced)
- **4 neue Interview-Dossiers (`01_Karriere_Bewerbungen/Interview_Vorbereitungen/`):**
  - `2026-11-23_TRUMPF_Trainee_IT_Governance.md` (`Ref: R00042850`, 2. Gespräch Tanja Preissner & Martin Hartmann)
  - `2026-10-19_EY_Technology_Consulting_SAP_Transformation.md` (`Ref: 13743137`)
  - `2026-10-08_msg_systems_Technical_SAP_Consultant.md` (2. Gespräch Matthaeus Glueck & Sandra Ulber)
  - `2026-06-11_Computacenter_IT_Service_Architecture.md` (ITIL 4 / Datacenter One INOC Brücke)
- **Graph-Verdichtung & Dossier-Updates:** `00_INDEX.md`, `00_Bewerbungsmanagement_Cockpit.md`, `Target_Roles.md`, `Aktuelle_Bewerbungsunterlagen.md`, `Stream_Grants_Management_Drittmittel_LGVFG.md` und `SSB_S4HANA_12_Strategische_Domaenen_Notebook.md` stärker vernetzt.
- **Datenbereinigung (`scripts/gmx_imap_service.py --clean-excel`):**
  - `Terminerinnerung` aus beiden Excel-Sheets, Cockpit & CSV entfernt; `Berivan Mutlutürk` → **Stadtwerke Pforzheim**, `Özlem Sevinç` / `Webmailer Amadeus Fire` → **Amadeus FiRe AG**, `marie-sophie.grootens@bkb.ch` → **Basler Kantonalbank (BKB)** bereinigt und Mehrfachleerzeichen geglättet.
- **ATS-bewusster Live GMX IMAP Sync & Telegram `/sync` (`scripts/gmx_imap_service.py`, `telegram_career_agent.py` V3.2):**
  - Behebt ASCII-IMAP-Umlaute, ATS-Subdomains (`msg.join.com`) sowie Multi-Role-Kollisionen über Chronologie- & Fachrolle-Guards (`DISTINCTIVE_ROLE_WORDS`); aktualisiert `Bewerbungsverlauf.xlsx` (`HORBACH`, `LTI-Metalltechnik`, `Manß & Partner`, `mindsquare` → `1. Gespräch`, `msg systems Public Sector`), Cockpit-Matrix & FTS5 via `upsert_note()`.
- **Headless Portal & Windows-Autostart (`s4hana-prep-portal/run_portal.py`, `scripts/start_career_os.pyw`, `scripts/setup_autostart.py`):**
  - `--no-browser`-Modus im Server, silent `pythonw.exe`-Launcher mit Logs in `logs/` sowie Startup-Skript `CareerOS_Autostart.vbs` installiert.
  - 5 veraltete Scratch-Skripte nach `scripts/archive/` verschoben.

### ✅ Verifikation & Compliance-Nachweise
- **Obsidian Audit (`validate_obsidian_rag.py`):** **286 / 286** Dokumente mit validem YAML-Frontmatter (**100,0 %**), **1.662 Wikilinks (5,8 Ø/Note | 0 Broken Links)**, **0 Multiple H1**, **0 Dateien > 10 MB**, **0 Graph-Orphans**, **60.578.154 Wörter (~81,78 Mio. Tokens)** -> *PASSED WITH DISTINCTION*.
- **GMX IMAP & RAG:** Beide Konten (`visar.murseli@gmx.de`, `visarmurseli@gmx.de`) live synchronisiert (`2/2` OK, `56` Mails geprüft, anschließender Re-Run 100 % idempotent); Hybrid RAG Index umfasst `286` Notes, `137.349` Chunks, `240` 768d-Vektoren (`787,63 MB`).

---

## [1.12.0] - 2026-11-24 (Hybrid RAG V3: 768d Gemini Vektor-Suche + Subword-RRF + Synonym-Expansion & Markdown-Synthesizer | Commit d193a82)

### 🎯 Kontext & Leitmotiv
Upgrade der Retrieval-Architektur auf ein echtes **3-Signal Hybrid RAG V3 (Reciprocal Rank Fusion)** mit Gemini Dense Embeddings (`gemini-embedding-001` @ 768d Matryoshka), lokaler Character-4-Gram-Cosine-Ähnlichkeit, deutscher/englischer Domain-Synonym-Expansion (`DOMAIN_SYNONYMS`) sowie XSS-sicherem Markdown-Synthese-Renderer im lokalen Second-Brain-Portal.

### 🚀 Neu hinzugefügt & Erweitert (Added & Enhanced)
- **3-Signal Hybrid RAG V3 (`scripts/local_rag_engine.py`):**
  - **Dense Vector Index (`chunk_vectors`):** Priorisierte `768d`-Vektorisierung der 240 wichtigsten semantischen Anker-Chunks (`zettel`, `interview-prep`, `moc`, `hub`, Karriere & Core-SAP) via rate-limit-resilientem, batch-checkpointed `batchEmbedContents` (`EMBED_DIM=768`, Query-LRU-Cache).
  - **Lokaler Subword-4-Gram-Cosine-Scorer (`_subword_profile`):** Reines Python-Morphologie-/Komposita-Matching (`_sparse_cos`) über alle semantischen Anker als permanenter Offline-/Fallback-Verstärker.
  - **Domain-Synonym-Expansion (`DOMAIN_SYNONYMS`) & Reciprocal Rank Fusion (`RRF`):** Verknüpft konzeptuelle Umschreibungen (z. B. *„technische Schulden“* → `clean`, `core`, `btp`, `modifikation`; *„Berechtigungen“* → `iam`, `pfcg`, `p_orgin`, `stauthtrace`, `sod`, `umt`) und fusioniert BM25-Rang + Subword-Rang + 768d-Vektor-Rang (`hybrid_rrf`).
  - **Incremental Vector + FTS5 Upsert:** `upsert_note()` erneuert bei `/api/save-note` und `/notiz` neben FTS5 auch die 768d-Embeddings des gespeicherten Dokuments in Echtzeit.
- **Webportal UI & API V3 (`portal_builder/notebook.py`, `portal_builder/vue_app.py`, `s4hana-prep-portal/run_portal.py`):**
  - `/api/rag` liefert `mode` (`hybrid_rrf` vs. `hybrid_subword_bm25`), `vec_sim` (`%`) und `matched_terms` aus.
  - XSS-sicherer Markdown-Renderer (`formattedRagAnswer` mit Überschriften, Fett, Inline-Code, Listen & `[Quelle: ...]`-Pills) sowie 4 1-Klick-Schnellabfragen — strikt im privaten Cockpit (`index.html`, `396,79 KB`) gekapselt (`public_index.html` `231,27 KB`, `0` Leaks).

### ✅ Verifikation & Compliance-Nachweise
- **Vektor- & Retrieval-Audit:** `240 / 240` priorisierte 768d-Anker in `career_os_rag.db` (`787,59 MB | 282 Notizen | 137.342 Chunks`); Paraphrasen-Test (*„Wie verhindere ich technische Schulden bei S/4HANA-Erweiterungen?“*) liefert `MODE: hybrid_rrf` mit `MOC_Enterprise_Architecture.md` (`Sim=65.5%`, `RRF=180.977`) und `Bimodale_ERP_Plattformisierung_BTP.md` (`Sim=64.1%`) auf Platz 1–2.
- **Portal Spec-Kit & Syntax:** Alle 6 Checks in `test_portal.py` bestanden (`411,601 bytes`), JS-Lexer (`JS_CLEAN` auf `index.html` & `public_index.html`) sowie `py_compile` ohne Warnungen.

---

## [1.11.0] - 2026-11-24 (Hybrid RAG v2, KI-Synthese-API, Live-Pipeline-Cockpit, KPMG Interview-Prep & Obsidian Graph-Farben | Commit 184e002)

### 🎯 Kontext & Leitmotiv
Weiterentwicklung des gesamten Career OS vom reinen Dokumenten-Index zu einer **aktiven, zweistufig gewichteten Retrieval-&-Synthese-Plattform** inklusive gezielter Vorbereitung auf das bevorstehende **KPMG-Interview am 27.11.2026**, drei neuer tiefgehender Architektur-Zettel, Echtzeit-RAG-Inkrementalindexierung sowie farbcodierter Obsidian-Graph-Topologie.

### 🚀 Neu hinzugefügt & Erweitert (Added & Enhanced)
- **Hybrid RAG Engine V2 (`scripts/local_rag_engine.py`):**
  - **2-Stage FTS5 Query Strategy:** Kombiniert präzise Multi-Term-`AND`-Treffer (`1.28x`) mit Broad-Recall-`OR`-BM25, gekoppelt mit **Document-Type Authority Weighting** (`zettel` `1.45x`, `interview-prep` `1.42x`, `moc/hub` `1.25x`, `module` `1.15x`, `log` `0.45x`), Term-Coverage-Multiplikator, **Per-File Diversity Cap (`max_per_file=2`)** und Keyword-zentrierten Snippets.
  - **Real-Time Incremental Upsert (`upsert_note`):** Einzelne Markdown-Notizen aus Webportal (`/api/save-note`) und Telegram (`/notiz`) werden per FTS5 External-Content-Delete/Insert in `< 20 ms` nachindexiert, ohne die komplette 773-MB-DB neu zu bauen.
  - **Gemeinsamer Pipeline-Reader (`get_pipeline_data`):** Zentrale Auswertung von `00_Aktuelle_Bewerbungsunterlagen/Bewerbungsverlauf.xlsx` für Webportal und Telegram (Deduplizierung früherer Excel-Logik).
- **Webportal V2 & Telegram V3.1 (`s4hana-prep-portal/run_portal.py`, `portal_builder/notebook.py`, `portal_builder/vue_app.py`, `telegram_career_agent.py`):**
  - Neue lokale API-Endpoints `/api/ask` (Gemini-3-Synthese mit Quellenbelegen) und `/api/pipeline` (Live-Interview-Radar mit 1-Klick-„Prep via RAG + KI laden“) — strikt auf `localhost:8085` gekapselt (0 Leaks in `public_index.html`).
  - Telegram Career Agent V3.1 um `/stats` und Real-Time-`upsert_note()` bei `/notiz` sowie Upload-Analysen erweitert.
- **Obsidian Vault Knowledge & Visualisierung:**
  - Neues Interview-Dossier für **KPMG (`27.11.2026`)**: `01_Karriere_Bewerbungen/Interview_Vorbereitungen/2026-11-27_KPMG_IT_Transformation_ERP_Audit.md`.
  - **3 neue atomare Zettel:** `Data_Migration_CVI_LTMC_Selective_Transition.md`, `Solution_Design_Signavio_CloudALM_Governance.md`, `TOGAF_9_ADM_Enterprise_Architecture_ERP.md`.
  - `.obsidian/graph.json` mit 5 semantischen Farbgruppen (Zettelkasten Gold, Karriere Smaragd, SAP-Architektur Blau, 300 ECTS Violett, MOCs Crimson) und optimierter Physik konfiguriert; `00_INDEX.md` und `00_Bewerbungsmanagement_Cockpit.md` verlinkt.
- **Notion CRM:** `Porsche AG`, `MHP (Porsche Company)`, `Bosch Group (JMP)` und `Mercedes-Benz` ergänzt (17 Einträge live im Notion CRM; restliche 50 deduplizierte Zeilen in `config/notion_crm_remaining.csv`).

### ✅ Verifikation & Compliance-Nachweise
- **Obsidian Audit (`validate_obsidian_rag.py`):** **282 / 282** Dokumente mit validem YAML-Frontmatter (**100,0 %**), **1.612 Wikilinks (0 Broken Links)**, **0 Multiple H1**, **0 übergroße Dateien (> 10 MB)**, **0 Graph-Orphans**, **60.576.455 Wörter (~81,78 Mio. Tokens)** -> *PASSED WITH DISTINCTION*.
- **Dual-Mode Privacy Gate & Syntax (`test_portal.py` & JS/Py Checks):** `index.html` (`392,33 KB`) & `public_index.html` (`231,06 KB` | `0` Leaks inkl. `/api/pipeline`, `/api/ask`, `/api/save-note`), alle 6 Spec-Kit-Checks bestanden.

---

## [1.10.0] - 2026-11-24 (Obsidian RAG Optimization, Hybrid SQLite FTS5 Engine, Dual-Mode Portal & CRM Integration | Commit f7deb31)

### 🎯 Kontext & Leitmotiv
Umfassende Härtung und Veredelung des gesamten Career OS Stacks (Obsidian Second Brain, Notion CRM, Webapp-Cockpit, GitHub Showcase und Telegram Career Agent). Der Wissensgraph von 60,57 Mio. Wörtern wurde durch verlustfreies Splitting übergroßer Monolithen, Bereinigung von macOS/Office-Artefakten, Behebung des Graph-Manifest-ID-Mismatches und neue atomare Zettel-Karten auf 100 % Graph- & Electron-Kompatibilität gebracht. Gleichzeitig schlägt eine lokale SQLite-FTS5-Hybrid-RAG-Engine (137.332 Chunks) die Brücke zwischen Obsidian, Webportal und Telegram, während ein strenges Dual-Mode-Build-Gate private Interview-Taktiken konsequent aus dem öffentlichen GitHub-Pages-Showcase fernhält.

### 🚀 Neu hinzugefügt & Erweitert (Added & Enhanced)
- **Obsidian Vault Architektur & Graph-Vollendung (`scripts/optimize_obsidian_vault.py`, `scripts/harmonize_obsidian_vault.py`, `scripts/validate_obsidian_rag.py`):**
  - **22** macOS/Office-Junk-Einträge (`16 ._*`, `6 ~$*`) aus `config/ingestion_registry.json` (`4.980` verbleibende Quelldateien) sowie aus 5 Volltext-Dossiers entfernt; `scripts/knowledge_harvester.py` filtert diese Dateien nun bereits im Scanner.
  - **3 Monolith-Dossiers (> 25 MB)** verlustfrei in **85 Electron-sichere Teilbände (< 4 MB)** inkl. TOC-Hubs gesplittet (`Master_Seminar_MRK_Industrie50_Volltext`, `Bachelor_Bachelorarbeit_Boundary_Resources_Volltext`, `Master_Cloud_Computing_Service_Management_Volltext`).
  - **Graph-Reparatur & Zettelkasten:** `nodes[].id` vs. `edges[].target`-Mismatch in `harmonize_obsidian_vault.py` behoben, bidirektionale `[[Wikilinks]]` in 59 Dossiers ergänzt und **4 atomare Zettel** (`SAP_HCM_Berechtigungsarchitektur_IAM.md`, `Bimodale_ERP_Plattformisierung_BTP.md`, `Third_Level_Support_Incident_Root_Cause.md`, `SAP_Trennungsrechnung_Public_Sector_EU1370.md`) sowie den Live-Debrief **Schwarz Digits (24.11.2026)** angelegt (`01_Karriere_Bewerbungen/Interview_Vorbereitungen/2026-11-24_Schwarz_Digits_SAP_HCM_IAM.md`).
  - Core-Plugins `properties` und `slash-command` aktiviert; leere `Unbenannt*.base`-Dateien entfernt.
- **Lokale Hybrid-RAG Engine & Live-APIs (`scripts/local_rag_engine.py`, `s4hana-prep-portal/run_portal.py`, `telegram_career_agent.py`):**
  - Lokaler SQLite FTS5 BM25 Chunk-Index (`config/career_os_rag.db`: **773,42 MB**, **278 Notizen**, **137.332 Chunks**, **392.615.574 Zeichen**).
  - Multi-Threaded Portal-Server (Port `8085`) um `/api/health`, `/api/rag` und `/api/save-note` (`Obsidian Vault/00_Inbox/Webapp_Notizen.md`) erweitert.
  - **Telegram Career OS Agent V3:** Mit `local_rag_engine`, Live-Excel-Pipeline (`/pipeline`), `/rag`, Obsidian Inbox (`/notiz`), Windows-UTF-8-Console-Reconfigure, aktiv verifizierten Gemini-Modellen (`gemini-3-flash-preview`, `gemini-3.1-flash-lite`) und sicherem Public-Deploy (`/deploy`).
- **Dual-Mode Portal & Public Security (`build_ultimate_portal.py`, `portal_builder/*`):**
  - Striktes Privacy-Gate trennt internes Cockpit (`s4hana-prep-portal/index.html`, `386,98 KB` mit `cv_defense`, `interview`, `files`, `notebook`, Local RAG & Gehaltsstrategie) von der öffentlichen GitHub-Pages-Edition (`s4hana-prep-portal/public_index.html`, `232,19 KB`, `0` geleakte vertrauliche Begriffe).
  - `.gitignore` im Repository um `config/career_os_rag.db*`, `*.db` und `*.sqlite*` erweitert.
- **Notion CRM Synchronisation (`Bewerbungs-Pipeline & CRM`):**
  - Top-Interviews & Tier-1-Bewerbungen direkt nach Notion synchronisiert (`Schwarz Digits – AI PO`, `HORBACH`, `Manß & Partner`, `KPMG`, `TRUMPF`, `EY`, `msg systems`, `Computacenter`, `Schwarz Digits – SAP ALM`); komplette deduplizierte Restliste aus `Bewerbungsverlauf.xlsx` als `config/notion_crm_remaining.csv` (UTF-8 BOM) bereitgestellt.

### ✅ Verifikation & Compliance-Nachweise
- **Obsidian RAG Readiness Audit (`validate_obsidian_rag.py`):** 278 / 278 Dokumente mit validem YAML-Frontmatter (**100,0 %**), **1.588 semantische Kanten (0 Broken Links)**, **0 Multiple H1**, **0 übergroße Dateien (> 10 MB)**, **0 Graph-Orphans**, **60.575.055 Wörter (~81,78 Mio. Tokens)** -> *PASSED WITH DISTINCTION*.
- **Portal- & Script-Checks (`test_portal.py` & API-Tests):** Alle 6 Privacy-/Integritäts-Assertions bestanden; `py_compile`, JS-Syntaxbalance sowie Live-RAG-Synthese über `gemini-3-flash-preview` (`HTTP 200 OK`) erfolgreich verifiziert.

---

## [1.9.0] - 2026-11-24 (100% Omni-Corpus Ingestion & Total LLM Knowledge Lake Release | Commit fa4e6ee)

### 🎯 Kontext & Leitmotiv
Vollendung der vollständigen, verlustfreien Volltext-Ingestion aller 5.002 Originaldokumente des gesamten Workspaces in das Obsidian Second Brain. Mit dem planmäßigen Durchlauf der finalen Batches `master_courses`, `bachelor_cs_se` und `bachelor_business_career` erreicht das System eine **100,0 % Ingestion-Abdeckung (5.002 von 5.002 Dokumenten)**. Insgesamt wurden **373.485.771 Zeichen (~93,37 Millionen Tokens)** extrahiert. Der Obsidian Knowledge Graph umfasst nun **189 harmonisierte Markdown-Dossiers mit 60.558.006 Wörtern (~81,75 Millionen Tokens)** bei makelloser **100 % LLM- & RAG-Readiness (189/189 valides YAML-Frontmatter, 675 semantische Kanten bei 0 Broken Links, 100 % Single-H1 AST-Hierarchie)**.

### 🚀 Neu hinzugefügt & Erweitert (Added & Enhanced)
- **100,0 % Gesamtkorpus-Abdeckung (5.002 / 5.002 Dokumente):**
  - `00_Aktuelle_Bewerbungsunterlagen`: **8 / 8 (100,0 %)** | 316.272 Zeichen
  - `01_SSB` (SAP Großprojekt): **1.245 / 1.245 (100,0 %)** | 38.417.038 Zeichen
  - `02_Master` (120 ECTS): **1.756 / 1.756 (100,0 %)** | 216.549.033 Zeichen
  - `03_Bachelor` (180 ECTS): **1.961 / 1.961 (100,0 %)** | 117.974.064 Zeichen
  - `04_DC1` (ITIL 4 Service Operations): **32 / 32 (100,0 %)** | 229.364 Zeichen
- **28 neue Master-Dossiers im Obsidian Knowledge Graph:**
  - *Säule 02 (Masterstudium 120 ECTS):*
    - `Master_Cloud_Computing_Service_Management_Volltext.md` (224 Dokumente): Cloud-Architekturen, SLA-Management, IaaS/PaaS/SaaS und Cloud Governance.
    - `Master_FPWI_Smart_Service_Blueprinting_Volltext.md` (92 Dokumente): Smart Service Blueprinting, Design Science Research (DSRM) und IoT-Servicearchitekturen.
    - `Master_AIM_Advanced_Information_Management_Volltext.md` (69 Dokumente): Enterprise Content Management, Information Retrieval und Semantic Web.
    - `Master_Advanced_Software_Engineering_Volltext.md` (68 Dokumente): Domain-Driven Design (DDD), CI/CD-Pipelines, Microservices und Clean Code.
    - `Master_AI4IoT_Sensor_Edge_AI_Volltext.md` (66 Dokumente): Zeitreihenanalyse, Sensorfusion, Edge AI und Smart Connected Systems.
    - `Master_Software_Architektur_Microservices_Volltext.md` (37 Dokumente): Architekturmuster, Schnittstellendesign (APIs) und Qualitätsattribute.
    - `Master_Applied_AI_Generative_AI_Industrie_Volltext.md` (34 Dokumente): Generative KI, Large Language Models und industrielle KI-Anwendungen.
    - `Master_TEUI_Internationale_Unternehmenstaetigkeit_Volltext.md` (32 Dokumente): OLI-Paradigma, Multichannel-Strategien und internationale Markterschließung.
    - `Master_Datenbanken_Informationssysteme_Volltext.md` (28 Dokumente): Relationale Modelle, NoSQL, ACID-Transaktionsmanagement und Query-Optimierung.
    - `Master_Management_IT_Unternehmen_ITIL_COBIT_Volltext.md` (23 Dokumente): ITIL 4, COBIT, strategische IT-Ausrichtung und IT-Controlling.
    - `Master_SOM_Service_Operations_Management_Volltext.md` (17 Dokumente): Warteschlangentheorie, quantitative Kapazitätsplanung und stochastische Prozesse.
    - `Master_Innovationsmanagement_Plattformen_Volltext.md` (15 Dokumente): Stage-Gate, Lead-User-Methodik, Open Innovation und Ökosysteme.
    - `Master_Zusatzmodule_Quantum_SmartCities_AIProto_Volltext.md` (102 Dokumente): Quantencomputing, Smart Cities (FIWARE), Rapid AI Prototyping und Nachweise.
  - *Säule 03 (Bachelorstudium 180 ECTS):*
    - `Bachelor_AFS_Automaten_Formale_Sprachen_Theorie_Volltext.md` (338 Dokumente): Endliche Automaten (DFA/NFA), Turingmaschinen, Chomsky-Hierarchie und Berechenbarkeit.
    - `Bachelor_PSE_Programmierung_Java_OOP_Volltext.md` (152 Dokumente): Objektorientierte Softwareentwicklung in Java, Entwurfsmuster und Testing.
    - `Bachelor_Programmentwicklung_Funktional_Logisch_Volltext.md` (135 Dokumente): Haskell, Prolog, Lambda-Kalkül und formale Programmspezifikation.
    - `Bachelor_Modellierung_BPMN_UML_Petrinetze_Volltext.md` (82 Dokumente): BPMN 2.0, UML, Petrinetze, Entity-Relationship-Modelle und Normalisierung.
    - `Bachelor_EST_Softwaretechnik_VModell_Scrum_Volltext.md` (78 Dokumente): V-Modell XT, Scrum, Anforderungsanalyse und Qualitätssicherung.
    - `Bachelor_MCI_Mensch_Computer_Interaktion_UX_Volltext.md` (77 Dokumente): UI/UX-Design, Usability Engineering und Heuristische Evaluationen.
    - `Bachelor_DSA_Datenstrukturen_Algorithmen_Volltext.md` (73 Dokumente): Asymptotische Komplexität (O-Notation), Such-/Sortieralgorithmen und Graphentheorie.
    - `Bachelor_SOPRA_Softwarepraktikum_Java_taskMasterPro_Volltext.md` (52 Dokumente): Agile Teamentwicklung taskMasterPro in Java/Spring Boot.
    - `Bachelor_Mathematik_Statistik_Methoden_Volltext.md` (138 Dokumente): Lineare Algebra, Analysis, Wahrscheinlichkeitsräume und Inferenzstatistik.
    - `Bachelor_GVWL1_Mikrooekonomik_Maerkte_Volltext.md` (77 Dokumente): Mikroökonomik, Marktformen, Preiselastizitäten und Spieltheorie.
    - `Bachelor_BWL1_Organisation_Management_Volltext.md` (49 Dokumente): Aufbau-/Ablauforganisation, Führungstheorien und strategisches Management.
    - `Bachelor_GBWL1_Strukturen_BWL_Rechnungswesen_Volltext.md` (28 Dokumente): HGB-Bilanzierung, doppelte Buchführung und GuV-Rechnung.
    - `Bachelor_GBWL4_Finanzprozess_Investition_Volltext.md` (27 Dokumente): Investitionsrechnung, Kapitalwertmethode, CAPM und Unternehmensfinanzierung.
    - `Bachelor_Interdisziplinaer_Recht_Management_Volltext.md` (172 Dokumente): IT-Recht, DSGVO, Urheberrecht, Dienstleistungsmanagement und HRM.
  - *Säule 01 (SSB) & Säule 00 (Karriere):*
    - `SSB_Gesamtprojekt_S4HANA_Ergaenzungen_Volltext.md` (68 Dokumente): Ergänzende Projektdokumente, Governance, Vergabeanträge und Fachstream-Protokolle.
    - `00_Bewerbungsunterlagen_Master_Volltext.md` (9 Dokumente): Offizielle Master-Bewerbungsunterlagen, Lebenslauf-Versionen, Zeugnisse und Bewerbungstracker.
- **Master Knowledge Graph Navigation (`00_INDEX.md`):**
  - Vollständige Aktualisierung des Index auf 189 Notizen mit direkten Wikilinks auf alle 62 Volltext-Dossiers.
- **Graph-Manifest (`graph_manifest.json`):**
  - Aktualisiert für Vektordatenbanken und LLM-Tools auf **189 Knoten und 675 verifizierte Kanten** (100 % Graph-Konnektivität, 0 Broken Links).

### 🔧 Performance & Data Science Fixes (Changed & Fixed)
- **Minified JS Array Wikilink Guard:**
  - Schwellenwert-Filter (>200 Zeichen) in `canonicalize_wikilinks` implementiert, um eingebettete Plotly-/JavaScript-Array-Literale in HTML-Folien vor falscher Wikilink-Interpretation zu schützen. Broken Links sanken von 1 auf **0**.
- **Robuster Harvester-Kernel mit dynamischem Heading-Demoting:**
  - Automatische Demotierung interner Markdown-Überschriften (`#` zu `####`) bei der Dokumentextraktion, um 100 % saubere Single-H1 AST-Hierarchien bei der Dossier-Erstellung zu garantieren.
- **Surrogate Character Sanitization:**
  - Standardmäßige Filterung isolierter UTF-16 Surrogates aus fehlerhaften PDF-Font-Tabellen in allen Extraktoren.

---

## [1.8.0] - 2026-11-24 (Omni-Corpus Academic & Enterprise Knowledge Explosion Release)

### 🎯 Kontext & Leitmotiv
Monumentaler Ausbau der Volltext-Ingestion über alle akademischen und operativen Säulen des Workspaces. Systematischer Durchlauf der Groß-Batches `ssb_pmo`, `master` und `bachelor`. Erhöhung der verarbeiteten Dokumente von 723 auf **2.677 Originaldokumente (53,5 % des Gesamtbestands)** und Vervierzehnfachung der extrahierten Zeichen auf **292.550.377 Zeichen (~73,14 Millionen Tokens)**. Der Obsidian Knowledge Graph Data Lake wächst auf **161 Dokumente mit 49.265.681 Wörtern (~66,51 Millionen Tokens)** bei makelloser **100 % RAG- & LLM-Readiness (161/161 valides Frontmatter, 0 Broken Links bei 647 Kanten, 0 Multi-H1s)**.

### 🚀 Neu hinzugefügt & Erweitert (Added & Enhanced)
- **Pillar 01 (SSB Großprojekt SAP4SSB | 94,5 % abgeschlossen | 1.177 Dokumente, 38,2 Mio. Zeichen):**
  - `SSB_PMO_Projektleitung_Masterplan_Volltext.md` (7,6 MB): Gesamtsteuerung, Projektsteckbriefe, WBS-Strukturen, Grundlagenschulungen, Ressourcenplanung und operative PMO-Governance (306 Artefakte).
  - `SSB_SektVO_Ausschreibung_Vergabe_Volltext.md` (1,5 MB): EU-Bekanntmachungen (2025-OJS075), Vergabeunterlagen, Bewertungsmatrizen Axians/Nagarro, Bieterfragen und Vergabeentscheidungen (118 Artefakte).
  - `SSB_Architektur_Methoden_Tools_Volltext.md` (8,7 MB): Datenmigration LTMC, SAP Cloud ALM Migration Tracker, Signavio Prozesshierarchien, Readiness Check Clean Core und Enable Now Übergabedokumentation (118 Artefakte).
- **Pillar 02 (Masterstudium | 54,0 % abgeschlossen | 949 Dokumente, 157,7 Mio. Zeichen):**
  - `Master_Seminar_MRK_Industrie50_Volltext.md` (151,3 MB): Volltext von 439 internationalen Forschungsarbeiten zu Mensch-Roboter-Kollaboration in Industrie 5.0 (PRISMA Systematic Literature Review, IEEE, ScienceDirect, Springer, Tagungsbände).
  - `Master_Masterarbeit_Literatur_Fundierung_Volltext.md` (8,8 MB): Wissenschaftliche Kernliteratur, theoretische Grundlagen (Boundary Resources, Absorptive Capacity, Bimodale IT) und qualitative Inhaltsanalyse nach Mayring (115 Artefakte, Note 1,0).
  - `Master_Forschungsmethoden_Algorithm_Aversion_Volltext.md` (4,8 MB): Empirische Studie zu Algorithm Aversion, quantitatives Forschungsdesign, Hypothesenmodelle und statistische Erhebungen (108 Artefakte, Note 1,7).
  - `Master_Digitale_Nachhaltigkeit_Schmalz_Volltext.md` (4,0 MB): CSRD-Abfallbilanz und Prozessmodellierung für die J. Schmalz GmbH inklusive PowerShell-Automatisierungskonzepten (135 Artefakte, Note 1,0).
  - `Master_ISG_PatentRadar_Klingele_Volltext.md` (2,3 MB): Digital Venture PatentRadar für Klingele Paper & Packaging (Hybrides SaaS- & Consulting-Geschäftsmodell, BPMN-Prozesse; 164 Artefakte, Note 2,0).
- **Pillar 03 (Bachelorstudium | 26,5 % abgeschlossen | 520 Dokumente, 96,4 Mio. Zeichen):**
  - `Bachelor_Bachelorarbeit_Boundary_Resources_Volltext.md` (87,6 MB): Volltext der 103-seitigen Bachelorarbeit bei Prof. Herzwurm, Boundary Resource Theory (Ghazawneh & Henfridsson), 14 Boundary Resource Klassen (ABR, DBR, SBR), Experteninterviews mit Lead-Entwicklern von OutSystems/Mendix und Standardwerke der Informatik (360 Artefakte, Note 1,7).
  - `Bachelor_IVP_0x539_Wear_Unternehmensanalyse_Volltext.md` (7,6 MB): Quantitative Unternehmensanalyse 0x539-Wear GmbH, mehrstufige Deckungsbeitragsrechnung, Make-or-Buy Analysen und Controlling-Fallstudien (56 Artefakte, Note 2,3).
  - `Bachelor_WI1_Betriebliche_Informationssysteme_Volltext.md` (834 KB): Betriebliche Informationssysteme WI 1: ERP-Architekturen, ARIS-Modellierung, SAP R/3 & S/4HANA Vorläufer, EPK-Prozesse (54 Artefakte).
  - `Bachelor_Informationsmanagement_Architektur_Volltext.md` (530 KB): Strategisches Informationsmanagement, IT-Governance, Informationslogistik, EAM-Grundlagen und ITIL-Services (64 Artefakte).
  - `Bachelor_EBusiness_Bestnote_1_0_Volltext.md` (206 KB): Informationssysteme im E-Business (Bestnote 1,0 bei Prof. Dr. Georg Herzwurm), B2B-Plattformen, EDIFACT, XML-Standards und elektronische Marktplätze (15 Artefakte).
- **Master Knowledge Graph Navigation (`00_INDEX.md`):**
  - Vollständige Integration aller 13 neuen Masterdossiers in die Säulen 01, 02 und 03.
- **Graph-Manifest (`graph_manifest.json`):**
  - Aktualisiert für Vektordatenbanken und LLM-Tools auf **161 Knoten und 644 verifizierte Kanten**.

### 🔧 Performance & Data Science Fixes (Changed & Fixed)
- **XML-Streaming & Row Bounding in `extract_xlsx`:**
  - Behebung eines Hängers bei Tabellen mit Datenvalidierung bis Zeile 1.048.576 durch `max_row`-Bounding und Schwellenwert für leere Zeilen (`consecutive_empty >= 10`). Lesezeit sank von Minuten auf 16 Millisekunden.
- **UTF-8 Lone Surrogate Sanitizer:**
  - Behebung von `UnicodeEncodeError` beim Speichern von Großdossiers durch Bereinigung unvollständiger Unicode-Surrogates (`\ud800`–`\udfff`) in `clean_text` und `errors="replace"` beim Schreiben.
- **2D-Matrix & Code-Bracket Healing:**
  - Behebung von 145 fälschlicherweise als Wikilinks interpretierten 2D-Python-Arrays und mathematischen Intervallen (`[[1, 2, 3]]`, `[[i]]`, `[[·]]`) durch automatische Konvertierung in semantische Code-Klammern `⟦...⟧`.
- **AST Heading Hierarchy:**
  - Bereinigung von 4 nicht-alphanumerischen Steuerzeichen-Überschriften in `Master_Masterarbeit_Literatur_Fundierung_Volltext.md` -> **0 Multi-H1 Notizen im gesamten Vault**.

---

## [1.7.0] - 2026-11-24 (Enterprise Fulltext Ingestion & Knowledge Harvester Release)

### 🎯 Kontext & Leitmotiv
Aufbau und Etablierung des automatisierten, modularen und stückweisen Volltext-Ingestion-Frameworks (**Enterprise Knowledge Harvester & Ingestion Engine - EKHIE**). Systematischer Scan über alle 5.002 Dokumente des Workspace, Erfassung im Ingestion-Ledger (`config/ingestion_registry.json`) und initiale Extraktion von 723 Originaldokumenten (über 21,25 Millionen Zeichen). Verdopplung des Obsidian-Wissensvolumens auf 8,31 Millionen Wörter (~11,22 Millionen Tokens) bei 100% Graph-Integrität.

### 🚀 Neu hinzugefügt (Added)
- **Multi-Format Extractor Protocol (`scripts/knowledge_extractors.py`):**
  - Universelle Extraktion für `.pdf` (pypdf, paginiert), `.docx` (Überschriften & Tabellen), `.pptx` (Folien, Notizen & Tabellen), `.xlsx` (Tabellenblätter & Daten) und Textformate.
- **Enterprise Knowledge Harvester (`scripts/knowledge_harvester.py`):**
  - Resiliente CLI-Engine mit State-Registry (`--scan`, `--status`, `--batch <name>`) zur stückweisen, verlustfreien und deduplizierten Ingestion aller Dokumente.
- **Ingestion State Ledger (`config/ingestion_registry.json`):**
  - Tracking-Register über alle 5.002 Workspace-Dokumente mit Dateigröße, Hash, Status, extrahierter Zeichenanzahl und Ziel-Obsidian-Dossiers.
- **Volltext-Masterdossiers in Obsidian (15 neue Groß-Dossiers):**
  - **Pillar 04 (Datacenter One | 31 Dokumente, 225.514 Zeichen):**
    - `DC1_ITIL4_Incident_Reports_PostMortems_Volltext.md`: Alle Colocation- & Colo-Connect-Störungsberichte, Ursachenanalysen (USV, Klima, Glasfaser).
    - `DC1_Hardware_Lifecycle_Management_Fahrplan_Volltext.md`: Dell PoC, Fahrplan Notebookaustausch und Asset-Tracking.
    - `DC1_Carriermanagement_SOPs_TOGAF_Volltext.md`: Carrier-Anbindung, SLA-Monitoring und TOGAF-Rechenzentrumsarchitektur.
  - **Pillar 01 (SSB Großprojekt SAP4SSB | 692 Dokumente, 21.034.238 Zeichen):**
    - `SSB_TP5_Steering_Board_Lenkungsausschuss_Volltext.md`: Alle 26 Lenkungsausschuss-Präsentationen (Nowak/Fillinger).
    - `SSB_TP1_Change_Management_People_Plan_Volltext.md`: 5,2 MB Change Story, Erklärvideos, Key-User-Schulungen, Pulse Checks.
    - `SSB_TP2_Kaufmaennische_Prozesse_Workshops_Volltext.md`: 2,5 MB Fit-to-Standard Protokolle, Scope-Analysen, Custom Code.
    - `SSB_TP3_Technische_Instandhaltung_EAM_Volltext.md`: 317 KB Instandhaltung, Evora-Angebote, Mobile Instandhaltung SSAM.
    - `SSB_TP4_IT_Infrastruktur_RISE_Basis_Volltext.md`: 1,45 MB RISE with SAP, Cloud ALM, Signavio, Azure, SSO.
    - `SSB_TP5_Gesamtsteuerung_Architektur_PMO_Volltext.md`: 567 KB Masterplan, CVI, Betriebsvereinbarungen, MS Project.
    - `SSB_Fachstream_FI_Finanzwesen_Volltext.md`: 7,5 MB Hauptbuch, Anlagenbuchhaltung, GoBD, Umsatzsteuerrichtlinie.
    - `SSB_Fachstream_CO_Controlling_Volltext.md`: 227 KB Kostenstellen, PSP-Elemente, Innenaufträge, SaC.
    - `SSB_Fachstream_Grants_Management_Volltext.md`: 1,0 MB Öffentliche Zuschüsse, LGVFG/GVFG, Drittmittelabrechnung.
    - `SSB_Fachstream_SD_Vertrieb_PATRIS_Volltext.md`: 570 KB Ticketvertrieb, Tarifwesen, PATRIS-Schnittstelle.
    - `SSB_Fachstream_Sustainability_CSRD_EHS_Volltext.md`: 677 KB Gefahrstoffkataster, CSRD, Unfallmanagement.
    - `SSB_Fachstream_MM_Materialwirtschaft_Volltext.md`: 17 KB Ariba-Anbindung, Bestellwesen, apsolut-Workshops.

### 🔄 Geändert & Harmonisiert (Changed)
- **Obsidian Master Router (`00_INDEX.md`):**
  - Vollständige semantische Verlinkung aller 15 neuen Groß-Dossiers.
- **Knowledge Graph Integrität:**
  - 148 Dokumente, 629 verifizierte Kanten, 0 Broken Links, Single-H1 AST-Hierarchie across all notes.

### 🛡️ Governance & Quality Gate
- **Audit-Ergebnis:** 100% LLM & RAG READINESS - PASSED WITH DISTINCTION (148/148 Frontmatter, 0 Broken Links, 0 Multi-H1s).

---

## [1.6.0] - 2026-11-24 (Data Science & Knowledge Graph Release)

### 🎯 Kontext & Leitmotiv
Vollständige data-science-basierte Transformation und Harmonisierung des gesamten Obsidian Second Brains (133 Notizen | 4,4+ Mio. Wörter | ~5,99 Mio. Tokens) für den optimalen Einsatz mit LLMs, Agenten, Vektor-Datenbanken und semantischem Graph-RAG. 100% Schema-Compliance, 0 Broken Links und Single-H1 AST-Hierarchie.

### 🚀 Neu hinzugefügt (Added)
- **Data Science Vault Harmonizer (`scripts/harmonize_obsidian_vault.py`):**
  - Automatisierter Pipeline-Prozessor zur Normalisierung von Frontmatter, Wikilinks, mathematischen Semantik-Klammern und Heading-Hierarchien.
- **RAG & Knowledge Graph Quality Validator (`scripts/validate_obsidian_rag.py`):**
  - Standalone-Audit-Suite zur Verifikation von Metadaten-Compliance, Graph-Kanten-Konnektivität (Adjazenzmatrix), Outgoing Link Density und AST-Sanity.
- **Wissensgraph-Manifest (`graph_manifest.json`):**
  - Vollständiger maschinenlesbarer JSON-Graph-Export mit 133 Knoten (ID, Label, Typ, Domain, Summary, Word Count) und 614 verifizierten Kanten zur direkten Ingestion in GraphRAG (Neo4j, NetworkX, LlamaIndex PropertyGraph).
- **Semantischer Vector Router in `00_INDEX.md`:**
  - Strukturierte Navigationsprotokolle für KI-Agenten, Indexierung der 6 Wissenssäulen und direkte Verknüpfung aller Second-Brain-Artefakte.

### 🔄 Geändert & Harmonisiert (Changed)
- **100% YAML-Frontmatter Schema Compliance:**
  - Alle 133 Dokumente (zuvor 19 unvollständig) besitzen nun standardisierte Metadaten (`id`, `title`, `type`, `domain`, `status`, `summary`, `tags`, `aliases`, `last_updated`).
- **Graph-Kanten-Heilung (0 Broken Links):**
  - Eliminierung aller 665 defekten Wikilink-Referenzen durch kanonische Pfadbereinigung (`⟦target⟧` statt relativer Pfadfragmente) und Mapping konzeptioneller Lücken (`BPMN_Signavio` -> `SSB_Tool_Governance_Signavio_CALM`, `SAP_FI` -> `SSB_Solution_Design_FI_CO`, etc.).
  - Bereinigung von tabellarisch fehlerhaft maskierten Wikilinks (`⟦target | alias⟧`) in `Modul_Übersicht.md`.
- **Mathematisch-logische Semantik-Klammern:**
  - Ersetzung von OCR-bedingten Doppelklammern in Prädikatenlogik-Vorlesungsfolien (`⟦F⟧`, `⟦G⟧`, `⟦Hund(x)⟧`, `⟦n,k⟧`) durch echte mathematische Unicode-Klammern, wodurch Falsch-Positiv-Wikilinks vollständig beseitigt wurden.
- **AST Heading Hierarchy & Chunking-Sanity:**
  - Bereinigung mehrfacher H1-Tags in 17 Dokumenten. Jedes Dokument besitzt nun exakt ein einziges `# H1` am Dokumenten-Kopf, wodurch hierarchische Text-Splitter (LangChain MarkdownHeaderTextSplitter, LlamaIndex MarkdownNodeParser) optimal arbeiten können.
- **Root-Bereinigung:**
  - Verlagerung persönlicher Tracker (`Gewohnheiten.md` und `NoFap.md`) in `04_Second_Brain_Zettelkasten/` mit vollwertigem YAML-Frontmatter und Verknüpfung im Index.

### 🛡️ Governance & Quality Gate
- **Audit-Ergebnis:** 100% LLM & RAG READINESS - PASSED WITH DISTINCTION (133/133 Frontmatter, 0 Broken Links, 0 Multi-H1s).

---

## [1.5.0] - 2026-11-24 (Nacht-Release)

### 🎯 Kontext & Leitmotiv
Vollständige Orchestrierung des Multi-Kanal Bewerbungsmanagements: Automatisierte Synchronisation dualer GMX-Postfächer, Tiefenanalyse von Stellenprofilen und Interview-Einladungen, nahtlose Notion-Live-Integration für anstehende Vorstellungsgespräche und 100% Spec-Kit konformer Rebuild des Webportals mit GitHub-Push.

### 🚀 Neu hinzugefügt (Added)
- **GMX IMAP Multi-Account Career Harvester (`scripts/gmx_imap_service.py`):**
  - Parallele Unterstützung für `visar.murseli@gmx.de` und `visarmurseli@gmx.de`.
  - Resiliente SSL-Verbindung (`imap.gmx.net:993`) mit automatischer UTF-8 MIME-Header-Dekodierung.
  - Multi-Keyword Filterung zur Klassifikation von Bestätigungen, Einladungen, Zwischenständen und Absagen.
- **Deep Email Extraction Engine (`scripts/dump_deep_emails.py`):**
  - Volltext-Extraktion von E-Mail-Bodies, HTML-Bereinigung, Zeitstempeln und Absenderangaben in `00_Aktuelle_Bewerbungsunterlagen/deep_emails_dump.json`.
- **Master Excel & Pipeline Reconciler (`scripts/update_bewerbungsverlauf_excel.py`):**
  - **Sheet 1 (`Bewerbungsverlauf`):** 68 chronologisch sortierte, deduplizierte Bewerbungsvorgänge mit Status, Einreichungsdatum und Gesprächsrunden.
  - **Sheet 2 (`Stellenprofile_Details`):** Detaillierte Rollendossiers mit Standort, Aufgaben, Qualifikationsanforderungen, Interviewern und vertraulichen Notizen.
  - Automatische JSON-Pipeline-Generierung (`00_Aktuelle_Bewerbungsunterlagen/bewerbungen_pipeline.json`).
- **Live Notion Workspace Integration (MCP Server `notion_notion`):**
  - Direkte Kopplung mit Visars Notion-Datenbank *Bewerbungs-Pipeline & CRM*.
  - Anreicherung der Seite **Schwarz Digits** (`421272de-cb1d-8111-b712-e9bf27e6a337`) für das heutige Interview am **24.11.2026 um 11:00 Uhr**:
    - ⚠️ Warnhinweis zur zwingenden Personalausweis-/Reisepass-Prüfung.
    - 🔗 Direkter Google Meet Button (`meet.google.com/srb-rmtx-znh`).
    - ✍️ Strukturierte Live-Notizen-Vorlage für das laufende Gespräch.
    - 🎙️ Transkript- und Audio-Dropzone zur Nachbereitung und automatischen Analyse.
    - 💡 Fach-Spickzettel zu SAP HCM Berechtigungen (`SU01`, `SU10`, `PFCG`, `P_ORGIN`, `P_PERNR`, `OOSP`, Least Privilege, SoD, JML).
    - 🗣️ Maßgeschneiderter 60-Sekunden Elevator Pitch und verhaltensbezogene STAR-Antworten.
- **Obsidian Cockpit & Vault Synchronisation:**
  - Automatische Aktualisierung von `00_Bewerbungsmanagement_Cockpit.md` mit Tabellen-Matrix und visuellen Callout-Dossiers.
  - Erstellung des eigenständigen Vorbereitungsdokuments `2026-11-24_Schwarz_Digits_SAP_HCM_IAM.md`.

### 🔄 Geändert (Changed)
- **Konsolidierung Schlüsselprozesse TRUMPF & Schwarz Digits:**
  - TRUMPF: Zusammenführung des 1. HR-Screenings (06.11.2026 mit Jil Wachter) und des 2. einstündigen Fachinterviews (23.11.2026 um 09:30 Uhr mit Tanja Preissner, Head of IT Governance & Martin Hartmann, Head of IT Infrastructure).
  - Schwarz Digits: Exakte Verankerung der Rolle *Junior SAP HCM User Maintenance & Access Management Specialist [Ref: 4972]* mit Ansprechpartnern Cosmin Serbanescu & Stefanie Link.
- **Portalerstellung (`build_ultimate_portal.py`):**
  - Automatischer Sync zwischen `s4hana-prep-portal/index.html` und Root `index.html` im GitHub-Repository für verzögerungsfreie GitHub Pages Deployments.
- **Root-Path Auflösung in Skripten:**
  - Alle Skripte nutzen nun dynamische `BASE_DIR`-Auflösung statt statischer Pfade, wodurch sie im Workspace und im Git-Klon gleichermaßen portabel sind.

### 🛡️ Sicherheit & Governance (Security)
- **Vertraulichkeits-Gate & Gitignore-Härtung:**
  - `config/gmx_config.json` wird strikt ignoriert; im Repository existiert ausschließlich `config/gmx_config.template.json`.
  - Ausschluss aller Original-Zeugnisse, Masterarbeit-PDFs, Excel-Dateien und temporären Daten aus dem Git-Tracking.
  - Keine Klartext-Passwörter in Skripten oder Logs.
- **Git Push auf `main`:**
  - Saubere Synchronisation mit Remote `https://github.com/Visarmurseli/Karriereseite.git` (Commit `22130f4`).

---

## [1.4.0] - 2026-11-23

### 🎯 Kontext & Leitmotiv
Strategische Bereinigung des Webportals, Ausbau der theoretischen Fundierung (Master 1,6, Masterarbeit 1,0 bei Prof. Herzwurm), 43 Q&A Interview-Katalog, interaktive Hamburger-Navigation und Einführung automatisierter Spec-Kit Quality Gates.

### 🚀 Neu hinzugefügt (Added)
- **Automatisierte Spec-Kit Quality Gates (`scripts/test_portal.py`):**
  - Integriert in `build_ultimate_portal.py`.
  - Verifiziert: 0 verbotene Arbeitgeberzuschreibungen (z.B. keine Bosch-Praktika), 100% akademische Notengenauigkeit (Master 1,6, MA 1,0, BA 3,0), 8 WBS-Milestones und reaktive Vue-3-Telemetrie.
- **Interaktiver 43 Q&A Frage-Antwort-Katalog (`portal_builder/interview.py`):**
  - Strukturierte Vorbereitung auf Fach- und Verhaltensfragen zu SAP S/4HANA, Enterprise Architecture, BTP, Solution Design und ITIL 4.
- **One-Click Startup & Service Skripte:**
  - `run_gmx_sync.bat`: Startet E-Mail-Abruf und Excel-Abgleich per Doppelklick.
  - `run_portal.py`: Multi-Threaded HTTP-Server auf Port 8085 mit automatischem Browseraufruf.

### 🔄 Geändert (Changed)
- **UI/UX Refactoring des Portals:**
  - Minimalistische Hamburger-Navigation auf mobilen und Desktop-Endgeräten.
  - Entfall von Dateidownload-Buttons zugunsten direkter visueller Inspektion.
  - Klar strukturierte 5-Hub-Architektur mit Fokus auf Trainee- und Junior-Positionierung.
- **Curriculum & Ausbildungsdaten:**
  - Detaillierte Darstellung der Station bei der SSB AG (24 Monate) und Datacenter One GmbH (12 Monate ITIL 4 Service Operations).

### 🛡️ Sicherheit & Governance (Security)
- **Historischer Git-Purge (Commit `801fdcf`):**
  - Bereinigung von 29 vertraulichen Originaldokumenten der Universität Stuttgart und Arbeitgebern aus der Git-Historie.
  - Etablierung verbindlicher Compliance-Richtlinien in `AGENTS.md`.

---

## 📌 Standard-Richtlinie für zukünftige Commits & Branches auf `main`

Ab sofort gilt für jeden Agenten und jede manuelle Änderung:
1. **Commit-Nachricht:** Präfixe nach Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`, `security:`, `chore:`).
2. **Changelog-Pflege:** Vor dem Push auf `main` ist die vorliegende Datei `CHANGELOG.md` um den neuen Commit-Eintrag mit Datum, Beschreibung der betroffenen Module und Testresultaten zu ergänzen.
3. **Qualitätsprüfung:** Ausführung von `python build_ultimate_portal.py` zur Bestätigung von 100% bestandenen Spec-Kit Quality Gates.
4. **Vertraulichkeitskontrolle:** Keine `.pdf`, `.docx`, `.xlsx` oder Zugangsdaten im Staging-Bereich.
