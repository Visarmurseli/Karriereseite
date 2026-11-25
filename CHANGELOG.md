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

## [1.22.0] - 2026-11-25 (Eigenständige Modern Dynamic UI, Entfernung von Drittanbieter-Branding, Suchfunktion & internen Dateinamen)

### 🎯 Kontext & Leitmotiv
Umfassende Weiterentwicklung zu einem **eigenständigen, modernen und dynamischen Enterprise Knowledge Hub** (inspiriert von zeitgemäßen Dokumentations-Workspaces, aber vollständig frei von Drittanbieter-/Clone-Referenzen), vollständige Entfernung der globalen Suchfunktion sowie Bereinigung sämtlicher lokaler Dateinamen und Pfade (z. B. `Interview_IP*_*.docx`, `HLM_v2.vsdx`, `Studium_Dokumente/`) aus dem Frontend.

### ✨ Neue UI/UX & Architekturanpassungen
- **Vollständige Entfernung aller Confluence/Jira/Atlassian-UI-Hinweise:**
  - App-Switcher, `CONFLUENCE OS`-Badge, `Atlassian Design System`-Tags und `Spaces`-Breadcrumbs in `header.py`, `dashboard.py`, `vue_app.py`, `synergies.py`, `enterprise_arch.py` und `cv_defense.py` vollständig entfernt bzw. in neutrale ITSM/SOP-Fachbegriffe überführt (**0** Treffer in `index.html` & `public_index.html`).
- **Komplette Entfernung der Suchfunktion:**
  - Globale Suchleiste, `Ctrl+K` Command-Palette-Modal, `Schnellsuche`-Buttons und Suchfilter-Banner rückstandslos aus App-Shell, Dashboard, Footer und `vue_app.py` entfernt.
- **Bereinigung interner Dateireferenzen (`thesis.py`, `synergies.py`, `vue_app.py`):**
  - Alle `Interview_IP1_Gesamt_PL.docx` – `Interview_IP4_Cloud_Basis.docx`-Namen, `Studium_Dokumente/Interviews_Masterarbeit`-Pfade sowie `HLM_v2.vsdx` entfernt; durch saubere fachliche Schwerpunkt-Tags ersetzt.
- **Modernes, dynamisches UI & UX (`portal_builder/header.py`, `vue_app.py`):**
  - **Scroll-Progress-Indikator** (`2px` Royal-Blue/Indigo-Verlaufslinie am oberen Viewport-Rand).
  - **Sanfte Tab-Reveal-Animationen (`tabReveal`)** & interaktive Card-Hover-Elevation.
  - **Kapitel-Stepper (`← Vorheriges Thema` / `Kapitel X / Y` / `Nächstes Kapitel →`)** mit automatischem Smooth-Scroll-to-Top (`selectTab`).
  - **Sticky Fix (`min-h-full` + `overflow-x: clip`):** Top-Navigation (`y = 0`) und linke Sidebar (`y = 56`) bleiben beim Scrollen durchgängig gepinnt (im Browser bei `1440×900` verifiziert).
- **Spec-Kit Quality Gates (`scripts/test_portal.py`):**
  - Erweitert um strikte Negativ-Checks gegen Suchfunktion, Clone-Branding und interne Dateinamen (100 % PASS).

---

## [1.21.0] - 2026-11-25 (Atlassian Design System Reverse Engineering: Confluence Cloud & Jira Hybrid UI Shell)

### 🎯 Kontext & Leitmotiv
Vollständiges UI/UX-Redesign der gesamten Dual-Mode-Webapp (`index.html` & `public_index.html`) nach dem **Atlassian Design System (`@atlaskit/tokens` – Confluence Cloud & Jira Cloud)**. Beseitigt jegliche Template-Reste, etabliert einen sauberen Confluence Light Mode als Standard mit nahtlosem Atlassian Dark Mode (`#1D2125`) und einer professionellen Enterprise-Dokumentationsstruktur.

### 🎨 Atlassian UI Architektur (`portal_builder/header.py`, `dashboard.py`, `synergies.py`, `vue_app.py`)
- **Confluence App Shell:**
  - Kompakte 56px Global Navigation Bar mit 9-Dot App Switcher (`:::`), Brand Badge (`VM` / `Visar Murseli` / `CONFLUENCE OS`), zentrierter Global Search (`Ctrl + K`), Live-Telemetrie-Lozenges (`149 Dossiers`, `1.064 bidirektionale Links`, `21 Deliverables`, `300 ECTS`), PDF-Export und Light/Dark Theme Toggle.
  - Linke, permanent sichtbare und einklappbare (`«`/`»`) **Confluence Seitenbaum-Sidebar** (`navSpaces`), strukturiert in Spaces (*Übersicht & Fundament*, *Praxis & S/4HANA*, *Akademie 300 ECTS*, *Karriere & Einstieg*, lokal zusätzlich *Interview & Second Brain*).
  - Mobile-kompatible Quick-Nav-Leiste und Slide-Over Page-Tree Drawer für `< lg` Viewports.
- **Atlassian Design Tokens (`:root` + `html.dark`):**
  - Semantisches CSS-Token-System (`--ds-surface`, `--ds-surface-sunken`, `--ds-surface-raised`, `--ds-brand-bold: #1868DB`, `--ds-text: #172B4D`, Dark `#1D2125` / `#161A1D` / `#22272B`) über alle 14 Inhaltsmodule hinweg.
  - Authentic **Jira Status-Lozenges** (`.atl-lozenge`), **ADF Info Callout Banners** (`.atl-callout`) und Confluence-Tabellen.
- **Bugfixes & Browser-Verifikation:**
  - Mustache-Escaping (`{{ syn.* }}` & `{{ cat }}`) in `synergies.py` vollständig korrigiert (**0** unaufgelöste Template-Braces in der gesamten HTML).
  - Header-Flex-Layout (`shrink-0`) gegen Abschneiden auf `1440px` Viewports abgesichert und `overflow-x: clip` für echtes `position: sticky` der Seitenbaum-Sidebar gesetzt.
  - Role-Fit-Matcher entfernt und `scripts/test_portal.py` synchronisiert.

---

## [1.20.0] - 2026-11-25 (Webapp UX-Upgrade: Sticky Quick-Nav, Role-Fit Matcher, Timeline, Light Mode & PDF-Export)

### 🎯 Kontext & Leitmotiv
Umfassendes UX- und Recruiter-Readiness-Upgrade der Webapp (`portal_builder/`) sowohl für das lokale Cockpit (`s4hana-prep-portal/index.html`) als auch für die öffentliche GitHub-Pages-Karriereseite (`s4hana-prep-portal/public_index.html`).

### 🚀 Neue Features & UI-Optimierungen
- **Sticky Horizontal Quick-Nav Bar (`portal_builder/header.py`):**
  - Direkte 1-Klick-Navigation für alle sichtbaren Module direkt unter dem Header (adaptiert automatisch zwischen 10 Public-Modulen und 14 Local-Modulen).
- **Interaktiver Role-Fit Matcher (`portal_builder/dashboard.py`, `portal_builder/vue_app.py`):**
  - Recruiter-Umschalter für *SAP Consultant*, *IT-PMO / PM*, *Enterprise Architect* und *ITIL 4 / Operations* mit jeweils 3 verifizierten Belegen und Direkt-Links.
- **Akademischer & Beruflicher Werdegang-Timeline (2019–2026):**
  - Chronologische 5-Stationen-Leiste auf dem Dashboard (B.Sc. → TOGAF 9 ADM → Datacenter One → SSB AG S/4HANA → M.Sc. 1,6).
- **Live Knowledge-Graph-Metriken & Spec-Kit Sync (`scripts/test_portal.py`):**
  - Telemetrie auf aktuelle Karpathy-Wiki-Werte aktualisiert (**149 Dossiers**, **1.064 bidirektionale Links**, 100 % Vernetzung).
- **Light-Mode Fix, PDF-Druckansicht & Footer-Actions (`portal_builder/header.py`, `portal_builder/vue_app.py`):**
  - Vollständige `html:not(.dark)` CSS-Unterstützung mit WCAG-Kontrasten, `@media print`-Stylesheet (`🖨️ PDF`-Button) und interaktivem Footer.

---

## [1.19.0] - 2026-11-25 (Purge veralteter Personal_OS-Tracking-Dokumente & Schärfung des Enterprise Career OS Fokus)

### 🎯 Kontext & Leitmotiv
Auf expliziten Nutzerwunsch wurden alle veralteten, rein privaten Tracking-Dokumente aus früheren Semestern (`Gewohnheiten.md`, `NoFap.md`, `Retrospektive_Wintersemester_23_24.md`, `Trainingsplan_Visar.md`) mitsamt dem Unterordner `04_Second_Brain_Zettelkasten/Personal_OS/` vollständig und rückstandslos aus dem Obsidian Second Brain entfernt. Dadurch wird das Wissensnetzwerk noch klarer auf den professionellen Kern ausgerichtet: SAP S/4HANA Transformation (SSB AG), Enterprise Architecture, Wirtschaftsinformatik (300 ECTS Master/Bachelor) und ITIL 4 Service Operations (Datacenter One).

### 🧹 Bereinigung & Re-Indizierung
- **Dateisystem & Obsidian Vault:**
  - Ordner `04_Second_Brain_Zettelkasten/Personal_OS/` und die 4 Tracking-Notizen physisch gelöscht.
  - Sämtliche Verweise in `00_INDEX.md` (Zeile 41 und 122) restlos entfernt.
- **Smart Ingestion Engine (`scripts/smart_ingest.py`):**
  - Domänen-Regel `personal-growth` entfernt; die Klassifikation konzentriert sich nun strikt auf die 5 Enterprise-Domänen (`career-pmo`, `sap-transformation`, `academic-curriculum`, `datacenter-operations`, `synergy-architecture`). Unspezifische Reflexionen fallen direkt in die Second Brain Wurzel zurück.
- **Graph-Synthese & Netzwerk-Metriken (`scripts/zettelkasten_synthesizer.py`):**
  - Re-Synthese erfolgreich durchgeführt: 149 Notizen (Layer 1), 1.064 Wissenskanten (Ø 7,14 Links/Zettel), 4,825% Netzwerk-Dichte, 100,0% Vernetzungsgrad, 0 verwaiste Notizen (Pure Orphans = 0).
- **Contradiction Checker Audit (`scripts/contradiction_checker.py`):**
  - Re-Audit über alle 293 Dokumente des Vaults: 0 kritische Widersprüche (FATAL), 0 Warnungen (WARNING), 100% konsistente Referenzen.
- **Operations Log (`log.md`):**
  - Revisionssicherer Eintrag `[2026-11-25] lint | Purge veralteter Personal_OS-Tracking-Dokumente` nach Karpathy LLM-Wiki Standard hinterlegt.

---

## [1.18.0] - 2026-11-25 (Smart Ingestion & Entity-Extractor Engine: Karpathy LLM-Wiki Ingestion Pipeline & Telegram /ingest Command)

### 🎯 Kontext & Leitmotiv
Implementierung von **Feature 3 aus der Andrej Karpathy LLM-Wiki Architektur** („Smart Ingestion & Entity-Extractor“): Vollautomatisches Ingestieren, Klassifizieren, Strukturieren und semantisches Einsortieren von Rohdokumenten und Freitext-Notizen aus `inbox/` und `00_Inbox/`. Beseitigt manuellen Ablage- und Formatierungsaufwand durch deterministisches Domänen-Routing, automatische YAML-Frontmatter-Generierung, `60-Sekunden-Essenz`-Abstracts, integriertes Wikilink-Auto-Linking und Echtzeit-RAG-Synchronisation.

### 📥 Smart Ingestion & Entity-Extractor (`scripts/smart_ingest.py`)
- **Multi-Format Dokumentenextraktion:**
  - Unterstützt `.md`, `.txt`, `.pdf` (via `pypdf`) und `.docx` (via `docx`).
- **Semantische Klassifikation & Domänen-Routing:**
  - *Career & Interviews (`career-pmo`):* Job-Interviews, Vorstellungsgespräche und Recruiting-Dossiers werden zielgenau nach `01_Karriere_Bewerbungen/Interview_Vorbereitungen/` geroutet.
  - *SAP S/4HANA & Transformation (`sap-transformation`):* Finanz-/Controlling-Konzepte nach `02_Kaufmaennische_Prozesse/`, Tool-/Enablement-Notizen nach `04_Change_Enablement/`, PMO nach `03_Governance_Vergabe/` und Architektur nach `01_Architektur_Technik/`.
  - *Akademische Forschung & Lehre (`academic-curriculum`):* Wissenschaftliche Notizen (Lehrstuhl Herzwurm/Becker, Mayring-Inhaltsanalyse, Modulkonzepte) nach `02_Wirtschaftsinformatik_300ECTS/`.
  - *Datacenter Operations (`datacenter-operations`):* ITIL 4, INOC, PRTG und HLM nach `03_SAP_EnterpriseArchitecture/`.
  - *Synergien & Personal OS (`synergy-architecture`, `personal-growth`):* Nach `04_Second_Brain_Zettelkasten/Synergien/` bzw. `Personal_OS/`.
- **Standardisiertes Schema & 60s-Abstracts:**
  - Jede Zieldatei erhält valides YAML-Frontmatter (`id`, `title`, `type`, `domain`, `status`, `summary`, `tags`, `last_updated`) und einen `> [!ABSTRACT] 60-Sekunden-Essenz` Block.
- **Sofortige Quervernetzung (Auto-Linker) & RAG:**
  - Neue Dokumente werden unmittelbar mit dem kanonischen Fachbegriffs-Lexikon abgeglichen (`[[Clean_Core_Paradigma]]`, `[[Modul_TOGAF_Scape]]`, etc.) und mit Master-MOCs verlinkt.
  - Automatischer RRF/SQLite Upsert (`rag_upsert`) sorgt für sofortige Auffindbarkeit im Second Brain.
  - Quelldokumente werden revisionssicher nach `inbox/processed/YYYY-MM-DD/` archiviert.

### 📱 Telegram Career Agent V3.5 Integration (`telegram_career_agent.py`)
- **Neuer Befehl `/ingest`:** Scannt `inbox/` und `00_Inbox/`, verarbeitet alle anstehenden Dateien und liefert einen strukturierten Ablagebericht auf das Smartphone.
- **Automatisches Vault-Filing bei Dokument-Upload:** Hochgeladene PDFs oder Dokumente in Telegram werden jetzt nicht nur im Chat analysiert, sondern automatisch nach Karpathy-Standard strukturiert und permanent im richtigen Obsidian-Ordner abgelegt.

---

## [1.17.0] - 2026-11-25 (Second Brain Knowledge Graph Synthesizer & Auto-Linker: Karpathy LLM-Wiki Engine & Telegram /graph & /synthesize Commands)

### 🎯 Kontext & Leitmotiv
Vollständige Implementierung von **Feature 2 aus der Andrej Karpathy LLM-Wiki Architektur** („Zettelkasten-Synthesizer & Auto-Linker“): Beseitigung isolierter Notizen (Orphans) und unvollständiger Sackgassen (Dead Ends) durch einen hochperformanten topologischen Graph-Parser, ein deterministisches Fachbegriffs-Lexikon und einen syntaxsicheren Wikilink-Auto-Linker. Das Wissensnetzwerk erreicht **100,0% Vernetzungsgrad** und **0 verwaiste Notizen** über 152 kuratierte Dokumente hinweg.

### 🧠 Topologische Graph-Engine & Auto-Linker (`scripts/zettelkasten_synthesizer.py`)
- **Topologische Netzwerkanalyse (Layer 1):**
  - Indiziert alle 152 kuratierten Dokumente und berechnet In-Degree (Backlinks), Out-Degree (Zitate), Graphdichte und Hub-Zentralität.
  - Wissenskanten stiegen von 790 auf **1.062 aktive bidirektionale Verlinkungen** (Ø 6.99 Links/Zettel bei 4.63% Netzwerk-Dichte).
  - Identifiziert die Top 10 Autoritäts-Hubs (`Modul_Übersicht` [45], `Modul_Masterarbeit` [33], `SSB_Tool_Governance_Signavio_CALM` [30], `Universal_Journal_ACDOCA` [30], `Clean_Core_Paradigma` [28]) und Top-Sammler-Karten (`00_INDEX` [110], `MOC_SSB_Transformation` [35], `Persoenliches_Staerkenprofil` [24]).
- **Sicherer Prose Auto-Linker:**
  - Tokenisiert Markdown hierarchisch und schützt Frontmatter, Fenced Code, Inline-Code, HTML und bestehende Links vollständig vor Korruption.
  - Generierte **378 neue, kontextgenaue Wikilinks** über 85 Dokumente hinweg.
- **Orphan- & Dead-End-Healing:**
  - Beseitigung aller isolierten Notizen (`Audit_Konsistenzbericht.md` fest in `00_INDEX` verankert und mit Navigations-Backlinks ausgestattet).
  - Sackgassen wie `SSB_Interview_Stories_STAR.md` und `Stream_Sales_Distribution_PATRIS.md` mit den zugehörigen Master-MOCs verknüpft -> **0 Pure Orphans** im Vault.
- **Interaktiver Synthese-Bericht:**
  - Revisionssicherer Markdown-Bericht mit Mermaid-Netzwerkgraph unter `04_Second_Brain_Zettelkasten/Graph_Synthese_Bericht.md`.

### 📱 Telegram Career Agent V3.4 Integration (`telegram_career_agent.py`)
- **Neuer Befehl `/graph`:** Liefert Graph-Metriken, Dichte, Vernetzungs-Score und Top-Hubs direkt auf das Smartphone.
- **Neuer Befehl `/synthesize`:** Führt auf Knopfdruck die Zettelkasten-Synthese, Auto-Verlinkung und Dead-End-Heilung mobil aus.
- **Erweitertes Menü:** Aktualisierte Begrüßung in `/start` und `/hilfe`.

---

## [1.16.0] - 2026-11-25 (Second Brain Contradiction & Sanity Checker: Andrej Karpathy LLM-Wiki Audit & Telegram /audit Command)

### 🎯 Kontext & Leitmotiv
Implementierung von **Feature 1 aus der Karpathy LLM-Wiki / Second Brain Architektur** („Contradiction & Sanity Checker“): Ein vollautomatischer, deterministischer Prüfscanner über alle 295 Notizen im Obsidian Vault zur Erkennung von Faktenwidersprüchen, veralteten Statusangaben und architektonischem Reduktionismus. Das Feature ist sowohl als CLI-Tool (`python scripts/contradiction_checker.py`) als auch direkt mobil über den Telegram Career Agenten (`/audit`) abrufbar.

### 🛡️ Contradiction & Sanity Engine (`scripts/contradiction_checker.py`)
- **Zwei-Schichten-Scanning (Layer 1 vs. Layer 2):**
  - *Layer 1 (151 kuratierte Notizen):* Vollständige semantische Tiefenprüfung über alle vier Regelkategorien (<1 Sekunde).
  - *Layer 2 (144 Data Lake Volltext-Dateien):* Schnelle, ressourcenschonende Prüfung auf kritische Verfassungskonformität.
- **Regelsatz 1: Verfassung & Amtliche Fakten (Zero Tolerance - CRITICAL):**
  - Keine unerlaubte Assoziation mit der Robert Bosch GmbH (Klarstellung: Patentmanagement für Klingele Paper & Packaging / ISG).
  - Amtliche Gesamtnote Master 1,6 („gut“) und Masterarbeit Bestnote 1,0 („sehr gut“).
  - Amtliche Gesamtnote Bachelor 3,0 und Bachelorarbeit Note 1,7 („gut“).
  - ECTS-Integrität: 120 ECTS Master, 180 ECTS Bachelor, 300 ECTS Gesamtstudium.
  - Verifizierte Verweildauern: 24 Monate SSB AG (05/2024–04/2026) und 12 Monate Datacenter One (05/2023–04/2024).
- **Regelsatz 2: Thesen-Fokus & Anti-Reduktionismus (WARNING):**
  - Verhindert das unzulässige Verkürzen der Masterarbeit auf ein reines Schlagwort wie „Clean Core“ und fordert stets den ganzheitlichen Kontext: ERP-Transformation, Plattformisierung von SAP S/4HANA und empirische Kritische Erfolgsfaktoren (12 Interviews, Mayring).
- **Regelsatz 3: Architektur-Konsistenz (WARNING):**
  - Validiert Greenfield vs. Brownfield bei der SSB S/4HANA Transformation (Ausschluss historischer Z-Altlasten).
- **Regelsatz 4: Zeitliche & Status-Inkonsistenzen (NOTICE):**
  - Erkennt veraltete Bearbeitungsstatus („in Bearbeitung“ bei abgeschlossener Masterarbeit).
  - Erkennt zurückliegende Vorstellungsgespräche in `Interview_Vorbereitungen/` ohne dokumentiertes Debriefing/Ergebnis und mahnt die Pflege an.
- **Audit-Report:** Speichert revisionssichere Markdown-Berichte mit Frontmatter und Handlungsempfehlungen unter `01_Karriere_Bewerbungen/Audit_Konsistenzbericht.md`.

### 📱 Telegram Career Agent V3.3 Integration (`telegram_career_agent.py`)
- **Neuer Befehl `/audit`:** Führt den gesamten Scan auf Knopfdruck per Telegram aus und sendet eine übersichtliche Zusammenfassung (Geprüfte Notizen, Kritisch: 0, Warnungen: 0, Pendenzen: 4, Konsistenz-Score: 98.6%) direkt auf das Smartphone.
- **Erweitertes Menü:** Aktualisierte Begrüßung in `/start` und `/hilfe`.

---

## [1.15.0] - 2026-11-25 (Privacy & Methodology Gate: DSGVO-Anonymisierung der Webapp, SAP Activate Phasen-Cockpit & NDA-Schutz | Local Build PASSED)

### 🎯 Kontext & Leitmotiv
Vollständige Anonymisierung aller personenbezogenen Daten von Vorgesetzten, Kollegen, Betriebsratsmitgliedern und Beratern auf der Webapplikation (`s4hana-prep-portal`, `index.html` und `public_index.html`) zur lückenlosen Wahrung von Datenschutz (DSGVO) und vertraglichen Geheimhaltungsvereinbarungen (NDA). Gleichzeitig erfolgte die strukturelle Neuausrichtung des Projekt-Radars von internen Firmen-WBS-Vorgangsnummern auf das offizielle **SAP Activate Phasen-Cockpit (Discover, Prepare, Explore ⭐, Realize, Deploy, Run)** mit klarem Fokus auf Visars 24-monatigen Kern-Wirkungsbereich bis zur erfolgreichen SDD-Lenkungsausschuss-Freigabe. Das persönliche Obsidian Second Brain behält zur authentischen Eigenrecherche alle internen Klarnamen und Realdaten unverändert bei.

### 🛡️ Datenschutz & Anonymisierung (Privacy & Anonymization)
- **Funktionen statt Klarnamen:** Alle Vorgesetzten und Kollegen in `project.py`, `vue_app.py`, `thesis.py`, `cv_defense.py`, `synergies.py`, `tools.py`, `migration.py` und `solution_design.py` wurden konsequent durch professionelle Funktionsbezeichnungen ersetzt (`Gesamtprojektleiter ERP-Transformation`, `Bereichsleiter IT`, `TPL Change Management & Academy`, `TPL Finance & Controlling`, `TPL Instandhaltung & Logistik`, `Lead-Architekten Basis & Cloud-Infrastruktur`, `Betriebsrats-Verhandlungskommission`, `INOC-Leitung`).
- **Wissenschaftliche Interview-Codierung (Mayring):** Die 12 Experteninterviews der Masterarbeit wurden nach qualitativem Forschungsstandard anonymisiert (`Experte 1 (IP1): Gesamtprojektleiter ERP-Transformation`, `Experte 2 (IP2): TPL Finance`, etc.).
- **NDA-Schutz & Bereinigung firmeninterner Metriken:** Eliminierung aller internen MS-Project-Vorgangsnummern (`WBS 1–297`, `Vorgang 110`, `Vorgang 294`, `Vorgang 297`), kundeninterner Reifegrade (`CO 90%, RE-FX 86%`) und firmeninterner Zieldaten.

### 🚀 SAP Activate Phasen-Cockpit
- **End-to-End Activate Lifecycle:** Ersetzung der internen WBS-Karten durch die 6 Phasen nach SAP-Best-Practice:
  1. *Discover* (Strategie, Business Case, Clean Core, RISE with SAP)
  2. *Prepare* (Projektcharta, Tool-Governance mit Cloud ALM & Signavio, Template-Standards)
  3. *Explore (⭐ Visars 24M Hauptwirkungsfeld)* (Fit-to-Standard Workshops, BPMN 2.0 Modellierung, kaufmännisches Solution Design Document SDD abgenommen)
  4. *Realize* (Modifikationsfreies Customizing, ABAP Cloud / RAP On-Stack vs. BTP Side-by-Side, LTMC Staging-Tabellen, SIT/UAT Testfall-Kataloge)
  5. *Deploy* (Revisionssicherer Cutover, 0,00 € Saldo Übernahmekonto-Abstimmung, Mitbestimmungs-Governance)
  6. *Run* (Hypercare, Enable Now Key-User Transfer, ITIL 4 Service Operations)
- **Aktualisierter Filter & Banner:** Umschalten zwischen `Alle (6 Phasen)`, `Explore (Visars Fokus ⭐)` und `Ausblick (Realize / Deploy / Run)`.

### 🔬 Test-Suite & Quality Gates
- **Automatisierter Privacy Gate Test:** `scripts/test_portal.py` wurde um `test_supervisor_and_colleague_anonymization(content)` und die Prüfung von `public_index.html` erweitert. Bei jeglichem Klarnamen-Leak schlägt der Build sofort mit `AssertionError: PRIVACY & NDA VIOLATION` fehl.
- **Activate Radar Check:** Verifikation aller 9 Activate-Phasen und Qualitäts-Checkpoints im Portal-HTML.
- **Spec-Kit Gate:** 100% Bestanden für `index.html` (430 KB) und `public_index.html` (261 KB).

## [1.14.0] - 2026-11-24 (Knowledge & Profile OS 2.0: Data Lake Trennung, 6 Arbeit×Uni Synergie-Karten, Persönliches Stärkenprofil & 60s-Kompakt-Briefing | Commit b568a6f)

### 🎯 Kontext & Leitmotiv
Strategische Schärfung auf Visar Murselis Kernvision (**Knowledge & Profile OS 2.0**): Entschlackung des Obsidian-Vordergrunds in zwei klare Schichten (Kuratiertes Wissen vs. durchsuchbarer Volltext-Data-Lake), explizite Verzahnung von **Arbeit × Studium × Eigenprojekten** über sechs tiefgehende Synergie-Karten, ein evidenzbasiertes **`Persoenliches_Staerkenprofil.md`**, einheitliche **`> [!ABSTRACT] 60-Sekunden-Essenz`**-Blöcke sowie das neue **Stärken- & Synergie-Cockpit** inkl. **60s-Kompakt- vs. Tiefenanalyse-Modus** und **Domänenfiltern** im lokalen Webportal und auf GitHub Pages.

### 🚀 Neu hinzugefügt & Erweitert (Added & Enhanced)
- **Phase 1 — Obsidian Schicht-Trennung & Kompaktheit (`scripts/restructure_knowledge_hub.py`, `00_INDEX.md`, `.obsidian/graph.json`):**
  - `143` massive Volltext-Extrakt-Dumps und `< 4 MB` Split-Bände (`85` `_Teil_XX` + `58` `_Volltext`-Hubs aus Säule `02`/`03`/`DC1`) nach `05_Archiv/Volltexte_DataLake/` verlagert und über [[00_DataLake_Index]] vollständig mit `0 Broken Links` & `0 Orphans` angebunden.
  - Persönliche Habit-/Trainingsnotizen nach `04_Second_Brain_Zettelkasten/Personal_OS/` isoliert und `00_INDEX.md` in **Schicht 1 (Kuratiertes Wissen)** vs. **Schicht 2 (Data Lake)** gegliedert.
  - `33` zentrale Praxisstationen (`SSB TP1–TP5`, `DC1 INOC/HLM`, `SDD`, `LTMC/CVI`, `Plattformisierung`) und Top-Studienmodule (`Masterarbeit 1,0`, `Bachelorarbeit 1,7`, `E-Business 1,0`, `Schmalz 1,0`, `FPWI 1,3`, `ASE 1,6`, `TOGAF 9 ADM` u. v. m.) mit einheitlichem `> [!ABSTRACT] 60-Sekunden-Essenz`-Block angereichert.
  - `harmonize_obsidian_vault.py`, `knowledge_harvester.py`, `optimize_obsidian_vault.py`, `validate_obsidian_rag.py` und `local_rag_engine.py` pfadsicher auf die Zwei-Schichten-Struktur umgestellt.
- **Phase 2 — Synergie-Atlas & Persönliches Stärkenprofil:**
  - **6 vernetzte Synergie-Karten (`04_Second_Brain_Zettelkasten/Synergien/`):** `01_Synergie_Plattformisierung_Boundary_Resources_ERP`, `02_Synergie_Cloud_ServiceOps_ITIL4`, `03_Synergie_Governance_Audit_IKS_Mitbestimmung`, `04_Synergie_Daten_Prozesse_Solution_Design`, `05_Synergie_Nachhaltigkeit_Prozessautomatisierung`, `06_Synergie_AI_IoT_Smart_Industry`.
  - **Master-Dossier `01_Karriere_Bewerbungen/Persoenliches_Staerkenprofil.md`:** 5 evidenzbasierte Stärken-Cluster, roter Faden `2019–2026` (`+1,4` Notenpunkte-Entwicklung B.Sc. `3,0` → M.Sc. `1,6`), kompakte Erfahrungs-Pitches und transparenter Wachstums-Radar.
- **Phase 3 — Webportal Showcase & Domänen-/Kompakt-RAG (`portal_builder/synergies.py`, `header.py`, `dashboard.py`, `notebook.py`, `vue_app.py`, `local_rag_engine.py`, `run_portal.py`):**
  - Neues Dual-Mode Modul `portal_builder/synergies.py` (Stärken-Cluster, interaktive `Arbeit × Uni × Projekte`-Matrix, `60s-Kompakt` vs. `Tiefenprofil`-Toggle) sowohl im privaten Cockpit (`index.html`, `429.06 KB`) als auch in der öffentlichen Showcase-Seite (`public_index.html` / `Karriereseite/index.html`, `259.57 KB`, `0` Privacy-Leaks).
  - `scripts/local_rag_engine.py` & `/api/ask` + `/api/rag`: Domänenfilter (`Alle`, `work`, `study`, `synergies`, `curated`), Priorisierung von `profile`/`synergy`-Vektorankern (`1.52`/`1.50`), Layer-1-Vorrang vor Data Lake und neuer Modus `style=compact` (*⚡ 60s-Kompakt-Briefing*) vs. `style=deep` (*🔬 Tiefenanalyse*).

### ✅ Verifikation & Compliance-Nachweise
- **Obsidian Audit (`validate_obsidian_rag.py`):** **294 / 294** Dokumente mit validem YAML-Frontmatter (**100,0 %**), **1.772 Wikilinks (6,0 Ø/Note | 0 Broken Links)**, **0 Multiple H1**, **0 Dateien > 10 MB**, **0 Graph-Orphans** (**Layer 1:** `150` Notizen | **Layer 2:** `144` Archiv-Bände), **60.583.583 Wörter (~81,79 Mio. Tokens)** -> *PASSED WITH DISTINCTION*.
- **Hybrid RAG V3 (`career_os_rag.db`):** Vollständig neu aufgebaut mit **`294` Notizen**, **`137.371` Chunks**, **`240 / 240` priorisierten Gemini 768d-Vektorankern**, **`392.689.572` Zeichen (`797,77 MB`)**.
- **Portal Build & Spec-Kit Tests (`test_portal.py` + `py_compile` + JS-Check):** Alle 7 Spec-Kit Compliance-Gates inkl. neuem Public-Showcase Privacy-Gate (`0` Leaks, `parens/braces delta: 0`) **100 % bestanden**.
- **Windows Autostart:** Unverändert aktiv (`CareerOS_Autostart.vbs` im Benutzer-Autostart).

---

## [1.13.0] - 2026-11-24 (Interview-Dossiers, Live GMX IMAP /sync, Datenbereinigung & Windows-Autostart | Commit 78114e9)

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
