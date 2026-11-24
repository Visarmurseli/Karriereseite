# 📜 CHANGELOG & SYSTEM RELEASE PROTOCOL
# Visar Murseli | Personal Career OS & Enterprise Knowledge Hub

Alle signifikanten Änderungen, Pipeline-Updates, architektonischen Erweiterungen und Git-Commits auf den Branch `main` werden in diesem Dokument lückenlos nach dem Standard [Keep a Changelog](https://keepachangelog.com/de/1.0.0/) und [Conventional Commits](https://www.conventionalcommits.org/de/v1.0.0/) protokolliert.

---

## [Unreleased] - 2026-11-24

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
  - Eliminierung aller 665 defekten Wikilink-Referenzen durch kanonische Pfadbereinigung (`[[target]]` statt relativer Pfadfragmente) und Mapping konzeptioneller Lücken (`BPMN_Signavio` -> `SSB_Tool_Governance_Signavio_CALM`, `SAP_FI` -> `SSB_Solution_Design_FI_CO`, etc.).
  - Bereinigung von tabellarisch fehlerhaft maskierten Wikilinks (`[[target\|alias]]` -> `[[target|alias]]`) in `Modul_Übersicht.md`.
- **Mathematisch-logische Semantik-Klammern:**
  - Ersetzung von OCR-bedingten Doppelklammern in Prädikatenlogik-Vorlesungsfolien (`[[F]]`, `[[G]]`, `[[Hund(x)]]`, `[[n,k]]`) durch echte mathematische Unicode-Klammern (`⟦F⟧`, `⟦G⟧`, `⟦n,k⟧`), wodurch Falsch-Positiv-Wikilinks vollständig beseitigt wurden.
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
