# AGENTS.md – Leitlinien für den CareerOS-Curator Agenten
# Workspace: Visar Murseli | Enterprise Knowledge Hub & Career OS

Dieses Dokument definiert das Profil, die wissenschaftlichen Fakten und die architektonischen Richtlinien für alle Agenten und Automatisierungen in diesem Workspace.

---

## 1. Profil & Akademisches Fundament von Visar Murseli

* **Akademischer Grad:** Master of Science (M.Sc.) Wirtschaftsinformatik, Universität Stuttgart
* **Amtliches Zeugnis:** Ausgestellt am 17. September 2026 (Prüfungsausschussvorsitzender Prof. Dr. Christian Becker)
* **Gesamtnote Master:** **1,6 („gut“)** | 120 ECTS (100% abgeschlossen)
* **Bachelor of Science (B.Sc.):** Wirtschaftsinformatik, Universität Stuttgart (180 ECTS, Gesamtnote 2,3)

### Offizieller Titel & Fokus der Masterarbeit (Note 1,0 – Sehr Gut)
* **Offizieller Titel:**
  > **„Kritische Erfolgsfaktoren in der Transformation großer ERP-Systeme: Eine Untersuchung am Beispiel der Plattformisierung von SAP S/4HANA“**
* **Erstprüfer:** Prof. Dr. Georg Herzwurm | Lehrstuhl für ABWL und Wirtschaftsinformatik II
* **Umfang & Methodik:** 126 Seiten, 12 leitfadengestützte Experteninterviews im Großprojekt SAP4SSB (Gesamtprojektleiter Roland Nowak, TPLs, Lead-Architekten Axians & Nagarro), qualitative Inhaltsanalyse nach Mayring mit eigenem Codebuch.
* **Kernschwerpunkte (WICHTIG):**
  - **Transformation großer ERP-Systeme** in komplexen Organisationen
  - **Plattformisierung (Platformization) & Plattform-Governance**
  - **Kritische Erfolgsfaktoren (CSF)** im Spannungsfeld von Organisation, Technik, Mensch und PMO
  - **Boundary Resources Theory & Entkopplung (Bimodale IT)**
  - **Absorptive Capacity & Change Management**
* **Leitlinie für Agenten:** Die Masterarbeit darf **niemals** auf ein einzelnes Schlagwort (wie z.B. "Clean Core") reduziert werden! Der inhaltliche und strategische Fokus liegt stets auf der **ganzheitlichen ERP-Transformation, Plattformisierung und den empirisch fundierten Kritischen Erfolgsfaktoren**.

### Offizieller Titel der Bachelorarbeit (Note 1,7 – Gut)
* **Offizieller Titel:**
  > **„Die Bedeutung von Boundary Resources in Low-Code Entwicklungsplattformen: Eine qualitative Untersuchung am Beispiel von OutSystems und Mendix“**
* **Theoretische Fundierung:** Boundary Resource Theory (Ghazawneh & Henfridsson) – 14 Boundary-Resource-Klassen (ABR, DBR, SBR).

---

## 2. Praxis- und Berufsstationen

1. **Stuttgarter Straßenbahnen AG (SSB AG) – 24 Monate (01.05.2024 – 30.04.2026):**
   - Rolle: Werkstudent im IT-PMO (Teilprojekt 5: Gesamtsteuerung & Architektur) unter Gesamtprojektleiter Roland Nowak und IT-Leiter Dietmar Fillinger.
   - Aufgaben: Multiprojektkoordination (TP1–TP5), Lenkungsausschuss-Vorbereitung, Tool-Governance (SAP Cloud ALM, SAP Signavio, SAP Enable Now Übergabe), Schnittstellen-Tracking mit Axians, Migrationskataloge.
2. **Datacenter One GmbH – 12 Monate:**
   - Rolle: Werkstudent im Integrated Network Operation Center (INOC) unter Helmut Schmidpeter.
   - Aufgaben: 24/7 Monitoring von Core-Netzwerken, USV, Klimatechnik, Incident- & Problem-Management nach ITIL 4, Ticketbearbeitung in Jira/Confluence.
3. **Enterprise Architecture Zertifizierung:**
   - TOGAF 9 ADM-Intensivkurs bei Scape Consulting (Dr. Daniel Simon).

---

## 3. Architektur der Webapplikation (`s4hana-prep-portal`)

Das Webportal ist strikt modular, objektorientiert und wartungsfreundlich aufgebaut:

* **Quellcode-Module:** Liegen im Ordner `portal_builder/`:
  - `header.py` -> Meta-Tags, CDN-Imports (Tailwind, Vue 3), Navigation & Quick Jump
  - `dashboard.py` -> Executive Summary, The Strategic Triangle, KPI-Metriken
  - `cv_defense.py` -> CV De-Risking, Gefahrenstufen (Rot/Gelb/Grün), Pivot-Brücken
  - `project.py` -> Großprojekt SSB AG, TP1–TP5, Meilensteine, C-Level Governance
  - `solution_design.py` -> Lösungsdesign kaufmännische Prozesse (FI/CO/MM), Trennungsrechnung
  - `migration.py` -> Datenmigration (LTMC), Staging-Tabellen, CVI, 0,00 € Übernahmekonto
  - `tools.py` -> SAP Cloud ALM, SAP Signavio, SAP Enable Now, TOGAF ADM
  - `thesis.py` -> Forschung, 16 Master-Module (120 ECTS, Gesamtnote 1,6), 12 Interviews
  - `enterprise_arch.py` -> EAM, ITIL 4 Service Operations, BPMN 2.0 Modellierung
  - `cheatsheet.py` -> Tech Cheatsheet (BTP, SQL, CDS, Integration Patterns)
  - `career.py` -> 90-Tage Onboarding-Roadmap, Gehaltskalkulation (65–75k €)
  - `interview.py` -> Interview Masterclass, 60-Sekunden & Deep-Dive Pitches
  - `files_tab.py` -> Dokumenten-Vault (50+ Originaldateien)
  - `notebook.py` -> Interaktives Second Brain (Autosave in LocalStorage)
  - `vue_app.py` -> Vue 3 Setup, reaktive Daten (allQA, starStories, filesData)
* **Kompilierung:** Das Skript `build_ultimate_portal.py` assembliert alle Module zu `s4hana-prep-portal/index.html`.
* **Server:** `s4hana-prep-portal/run_portal.py` (Multi-Threaded HTTP-Server auf Port 8085).

---

## 4. Aufgaben & Arbeitsweise des CareerOS-Curator Agenten

1. **Eingangsprüfung (Inbox):** Überwacht den Ordner `inbox/` auf neue Dokumente (z.B. Bachelor-Notenbescheide, neue Seminararbeiten, Interview-Notizen, Jobprofile).
2. **Qualitätssicherung:**
   - Fakten müssen mit amtlichen Dokumenten (Zeugnisse, Zertifikate) übereinstimmen.
   - Keine einseitigen Schlagworte; der wissenschaftliche rote Faden (Plattformisierung, ERP-Transformation, EAM) steht im Mittelpunkt.
3. **Modulares Patchen:** Änderungen erfolgen **nur** in den betroffenen Modulen in `portal_builder/`.
4. **Automatischer Rebuild:** Nach jeder Code-Änderung führt der Agent sofort `python build_ultimate_portal.py` aus und prüft den erfolgreichen Build.
