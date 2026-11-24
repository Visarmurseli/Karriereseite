# 📜 CHANGELOG & SYSTEM RELEASE PROTOCOL
# Visar Murseli | Personal Career OS & Enterprise Knowledge Hub

Alle signifikanten Änderungen, Pipeline-Updates, architektonischen Erweiterungen und Git-Commits auf den Branch `main` werden in diesem Dokument lückenlos nach dem Standard [Keep a Changelog](https://keepachangelog.com/de/1.0.0/) und [Conventional Commits](https://www.conventionalcommits.org/de/v1.0.0/) protokolliert.

---

## [Unreleased] - 2026-11-24

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
