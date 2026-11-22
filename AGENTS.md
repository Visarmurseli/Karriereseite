# AGENTS.md – Leitlinien für den CareerOS-Curator Agenten
# Workspace: Visar Murseli | Enterprise Knowledge Hub & Career OS

Dieses Dokument definiert das Profil, die wissenschaftlichen Fakten und die architektonischen Richtlinien für alle Agenten und Automatisierungen in diesem Workspace.

---

## 1. Profil & Akademisches Fundament von Visar Murseli

* **Akademischer Grad:** Master of Science (M.Sc.) Wirtschaftsinformatik, Universität Stuttgart
* **Amtliches Zeugnis:** Ausgestellt am 17. September 2026 (Prüfungsausschussvorsitzender Prof. Dr. Christian Becker)
* **Gesamtnote Master:** **1,6 („gut“)** | 120 ECTS (100% abgeschlossen)
* **Bachelor of Science (B.Sc.):** Wirtschaftsinformatik, Universität Stuttgart (180 ECTS, Gesamtnote 3,0, Bachelorarbeit Note 1,7 bei Prof. Dr. Georg Herzwurm, Bestnote 1,0 in Informationssysteme im E-Business)

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

## 2. Praxis- und Berufsstationen & Projekte (Authentischer Lebenslauf-Standard)

### Berufserfahrung
1. **Stuttgarter Straßenbahnen AG (SSB AG) – 24 Monate (05/2024 – 04/2026):**
   - Rolle: Werkstudent SAP S/4HANA Transformation (IT-PMO & Teilprojekt 5: Gesamtsteuerung & Architektur unter Gesamtprojektleiter Roland Nowak und IT-Leiter Dietmar Fillinger).
   - Aufgaben & Deliverables: Analyse und Dokumentation von Geschäftsprozessen im SAP S/4HANA-Umfeld zur Erstellung des Solution Design Documents; Erstellung und Pflege des Projektplans in MS Project sowie interne Ressourcenplanung; Statusverfolgung und Fortschrittsanalyse diverser Teilprojekte; Strukturierung von Teams-Kanälen inklusive Kanban-Boards, Abwesenheitskalendern und FAQ-Seiten; Tool-Governance (SAP Cloud ALM, SAP Signavio, SAP Enable Now).
2. **Datacenter One GmbH – 12 Monate (05/2023 – 04/2024):**
   - Rolle: Werkstudent Information Network Operation Center (INOC unter Helmut Schmidpeter).
   - Aufgaben: Prozessorientiertes IT-Service-Management als Single Point of Contact (Jira); Konzeption und Aufbau einer Wissensdatenbank zur Prozessstandardisierung (Confluence); 24/7 Monitoring von Core-Netzwerken, USV und Klimatechnik nach ITIL 4.

### Projekte & Außerschulische Aktivitäten (WICHTIG: Keine Fehlatzuschreibung als Praktika!)
3. **Innovationsprojekt: Plattform für Patentmanagement und -recherche (02/2024):**
   - Kontext: Konzeption für ein führendes Unternehmen der Verpackungsindustrie (Klingele Paper & Packaging / ISG).
   - Aufgaben: Entwicklung und wirtschaftliche Konzeption eines hybriden Geschäftsmodells (SaaS & Beratung) zur Stärkung der Innovationskraft durch KI-gestützte Patentrecherche, inklusive BPMN-Modellierung der RPA-basierten Kernprozesse.
   - *Wichtige Leitlinie:* Dies war ein praxisbezogenes Innovationsprojekt für die Verpackungsindustrie – Visar hat **kein** Praktikum bei der Robert Bosch GmbH absolviert!
4. **Automatisierungsprojekt: Optimierung der Abfallbilanz und Nachhaltigkeitsberichterstattung (07/2024):**
   - Kontext: Abfallmanagement eines Industrieunternehmens.
   - Aufgaben: Modellierung von Ist-Prozessen und Identifikation von Automatisierungspotenzialen; Entwicklung von PowerShell-Skripts zur automatisierten Datenextraktion zur Eliminierung von Eingabefehlern und Reduzierung des Zeitaufwands.
5. **Privatprojekt: Persönliche Portfolio-Website (2023–):**
   - Konzeption und Entwicklung einer responsiven Single-Page-Application (via GitHub Pages) zur digitalen Präsentation des Qualifikationsprofils mit Fokus auf SAP-Expertise, akademische Arbeiten und technische Skills.
6. **Enterprise Architecture & Zertifizierungen:**
   - TOGAF 9 ADM-Intensivkurs bei Scape Consulting (Dr. Daniel Simon, Universität Stuttgart, 16.01.2020).
7. **Ehrenamt & Gesellschaftliches Engagement:**
   - Ehrenamtliche Geflüchtetenhilfe (Refugees Welcome, HVF) und Hausaufgabenbetreuung.

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
