# -*- coding: utf-8 -*-
"""
Systematic Full-Text Knowledge Extractor for Obsidian Vault
Pillars: 00 (Bewerbung), 01 (SSB), 02 (Master), 03 (Bachelor), 04 (DC1)
Target: C:\\Users\\SHQIPTAR634\\Documents\\Obsidian Vault
"""
import os
import re
import json
import datetime
import pypdf
import docx
import openpyxl

WS_DIR = r"c:\Users\SHQIPTAR634\Desktop\SSB Dateien"
VAULT_DIR = r"C:\Users\SHQIPTAR634\Documents\Obsidian Vault"

def extract_pdf_text(filepath, max_pages=None):
    if not os.path.exists(filepath):
        return ""
    try:
        reader = pypdf.PdfReader(filepath)
        num_pages = len(reader.pages) if max_pages is None else min(max_pages, len(reader.pages))
        pages_text = []
        for i in range(num_pages):
            txt = reader.pages[i].extract_text() or ""
            if txt.strip():
                pages_text.append(f"<!-- Page {i+1} -->\n" + txt.strip())
        return "\n\n".join(pages_text)
    except Exception as e:
        print(f"Error reading PDF {filepath}: {e}")
        return ""

def extract_docx_text(filepath):
    if not os.path.exists(filepath):
        return ""
    try:
        doc = docx.Document(filepath)
        paras = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        return "\n\n".join(paras)
    except Exception as e:
        print(f"Error reading DOCX {filepath}: {e}")
        return ""

def write_vault_note(relative_path, content):
    full_path = os.path.join(VAULT_DIR, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"[OK] Wrote note: {relative_path} ({len(content)} chars)")

# ==============================================================================
# BATCH 1: PILLAR 00 (Aktuelle Bewerbungsunterlagen)
# ==============================================================================
def process_pillar_00():
    print("\n--- Processing Pillar 00: Aktuelle Bewerbungsunterlagen ---")
    p00 = os.path.join(WS_DIR, "00_Aktuelle_Bewerbungsunterlagen")

    # 1. Lebenslauf Volltext
    cv_pdf = os.path.join(p00, "Lebenslauf_Murseli_Vsar.pdf")
    cv_text = extract_pdf_text(cv_pdf)
    
    note_cv = f"""---
title: "Lebenslauf Volltext & Werdegang"
author: "Visar Murseli, M.Sc."
category: "Bewerbungsunterlagen"
status: "aktiv_verifiziert"
source_file: "file:///{cv_pdf.replace('\\', '/')}"
last_updated: "{datetime.date.today().isoformat()}"
tags:
  - karriere
  - lebenslauf
  - single_source_of_truth
  - profil
---

# 📄 Lebenslauf – Visar Murseli, M.Sc. Wirtschaftsinformatik

> [!INFO] **Persönliche Kontaktdaten & Status**
> - **Name:** Visar Murseli
> - **E-Mail:** Visar.murseli@gmx.de | **Mobil:** 015788225884
> - **Wohnort:** Karl-Massa-Str. 5, 71634 Ludwigsburg
> - **Akademischer Grad:** Master of Science (M.Sc.) Wirtschaftsinformatik, Universität Stuttgart
> - **Zielpositionen:** Junior SAP Consultant, Junior Enterprise Architect, IT-/Management-Traineeprogramm
> - **Gehaltsziel:** 55.000 € – 65.000 € p.a.

---

## 🎯 Executive Summary & Kernkompetenzen
Wirtschaftsinformatiker (M.Sc., Note 1,6) mit starkem ingenieurwissenschaftlichem Fundament und 36 Monaten relevanter Berufserfahrung im ERP-Großprojektumfeld und Rechenzentrumsbetrieb.
- **24 Monate SSB AG:** Werkstudent im IT-PMO (Teilprojekt 5) beim Transformationsprogramm SAP4SSB (Greenfield S/4HANA Private Cloud, Tool-Governance mit SAP Cloud ALM, Signavio und Enable Now).
- **12 Monate Datacenter One (DC1):** Werkstudent im 24/7 Leitstand (INOC) nach ITIL 4 Service Operations (PRTG-Monitoring, Single Point of Contact, Hardware Lifecycle Management).
- **Masterarbeit (Note 1,0):** Empirische Untersuchung Kritischer Erfolgsfaktoren bei der S/4HANA-Plattformisierung mit 12 Experteninterviews bei Prof. Herzwurm.

---

## 🎓 Akademische Ausbildung

### Master of Science (M.Sc.) Wirtschaftsinformatik
- **Institution:** Universität Stuttgart (Fakultät für Wirtschafts- und Sozialwissenschaften)
- **Zeitraum:** 2023 – 2026 | **Gesamtnote:** **1,6 („gut“)** | **120 ECTS** (100% abgeschlossen)
- **Masterarbeit (Note 1,0):** *„Kritische Erfolgsfaktoren in der Transformation großer ERP-Systeme: Eine Untersuchung am Beispiel der Plattformisierung von SAP S/4HANA“* (Erstprüfer: Prof. Dr. Georg Herzwurm).
- **Schwerpunkte:** Software-Architektur (1,7), Advanced Software Engineering (1,6), Digitale Nachhaltigkeit (1,0), Forschungsprojekte FPWI (1,3), Cloud Computing (2,0), Applied AI (1,7).

### Bachelor of Science (B.Sc.) Wirtschaftsinformatik
- **Institution:** Universität Stuttgart
- **Zeitraum:** 2018 – 2023 | **Gesamtnote:** **3,0** | **180 ECTS** (100% abgeschlossen)
- **Bachelorarbeit (Note 1,7):** *„Die Bedeutung von Boundary Resources in Low-Code Entwicklungsplattformen: Eine qualitative Untersuchung am Beispiel von OutSystems und Mendix“* (Prof. Herzwurm).
- **Spitzenleistung:** Bestnote **1,0 in Informationssysteme im E-Business**.

---

## 💼 Berufliche Stationen

### 1. Stuttgarter Straßenbahnen AG (SSB AG) | 05/2024 – 04/2026 (24 Monate)
**Rolle:** Werkstudent SAP S/4HANA Transformation (IT-PMO & Teilprojekt 5: Gesamtsteuerung & Architektur)
- **Solution Design & Fachstreams:** Analyse und Dokumentation von Geschäftsprozessen im SAP S/4HANA-Umfeld zur Finalisierung des Solution Design Documents (SDD) für die kaufmännischen und technischen Streams (FI, CO, MM, RE-FX, Grants Management, Instandhaltung).
- **Projektsteuerung & Ressourcenplanung:** Erstellung und kontinuierliche Pflege des Gesamtprojektplans in MS Project (WBS 1–297); Status- und Meilenstein-Tracking für das C-Level Steering Board.
- **Tool-Governance:** Verfasser des offiziellen Handbuchs *SAP Cloud ALM How2Handle*; Prozess-Synchronisation von BPMN 2.0 Modellen in SAP Signavio mit Testfällen in CALM; strategisches Übergabekonzept von SAP Enable Now an die Personalentwicklung.
- **Datenmigration:** Analyse der Migrationsobjekte im SAP Migration Cockpit (LTMC Staging-Tabellen, CVI Business Partner Konsolidierung, Eröffnungsbilanz-Abgleich auf 0,00 € Übernahmekonto).

### 2. Datacenter One GmbH | 05/2023 – 04/2024 (12 Monate)
**Rolle:** Werkstudent Information Network Operation Center (INOC)
- **24/7 Leitstand & SPoC:** First-Point-of-Contact für Enterprise-Kunden und Carrier bei Störungen; Ticket-Bearbeitung nach ITIL 4 Service Operations im Jira Service Management.
- **Monitoring & Infrastruktur:** 24/7 Überwachung von Core-Netzwerken, Serverracks, USV-Anlagen und Rechenzentrums-Klimatechnik via PRTG Network Monitor.
- **Wissensmanagement:** Aufbau und Standardisierung der Confluence-Wissensdatenbank durch Erstellung von Standard Operating Procedures (SOPs) zur Steigerung der Erstlösungsquote.
- **Hardware Lifecycle Management (HLM):** BPMN-Modellierung in MS Visio und Begleitung des Rollouts von über 100 Arbeitsplatzsystemen inklusive datenschutzkonformem Decommissioning.

---

## 🛠️ Praxis- & Innovationsprojekte
- **Digital Venture PatentRadar (02/2024):** Konzeption eines hybriden Geschäftsmodells (SaaS & Consulting) für Klingele Paper & Packaging zur KI-gestützten Patentrecherche mit UiPath-RPA-Kernprozessen.
- **CSRD-Abfallbilanzierung (07/2024):** Prozessoptimierung und PowerShell-Automatisierung für die J. Schmalz GmbH zur automatisierten Extraktion von Entsorgungsnachweisen.
- **TOGAF 9 ADM Intensivkurs (01/2020):** Scape Consulting GmbH (Dr. Daniel Simon, Universität Stuttgart) – Enterprise Architecture Management, Metamodell und Gap-Analyse.
- **Ehrenamtliches Engagement:** Mitarbeit im Referat IT und Support der stuvus (Studierendenvertretung Universität Stuttgart) sowie ehrenamtliche Geflüchtetenhilfe und Hausaufgabenbetreuung.

---

## 🧠 Extrahierter Volltext aus Master-Lebenslauf
```text
{cv_text}
```

---

## 🔗 Verknüpfungen im Wissensnetz
- Masterarbeit: [[02_Wirtschaftsinformatik_300ECTS/Modul_Masterarbeit]]
- Großprojekt SSB: [[03_SAP_EnterpriseArchitecture/SSB_Grossprojekt_SAP4SSB]]
- Datacenter One: [[03_SAP_EnterpriseArchitecture/DC1_ITIL4_Service_Operations]]
- Notenübersicht: [[01_Karriere_Bewerbungen/00_Masterzeugnis_Leistungsuebersicht_Volltext]]
"""
    write_vault_note("01_Karriere_Bewerbungen/00_Lebenslauf_Volltext.md", note_cv)

    # 2. Bewerbungsmanagement Cockpit aus Bewerbungsverlauf.xlsx
    bv_xlsx = os.path.join(p00, "Bewerbungsverlauf.xlsx")
    wb = openpyxl.load_workbook(bv_xlsx, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    
    table_lines = ["| Arbeitgeber | Stellenbezeichnung | Datum | Bewerbungseingang | 1. Gespräch | 2. Gespräch | Status / Feedback |",
                   "| :--- | :--- | :---: | :---: | :---: | :---: | :--- |"]
    for r in rows[1:]:
        if any(r):
            ag = str(r[0] or '-').strip()
            title = str(r[1] or '-').strip()
            d1 = r[2].strftime('%d.%m.%Y') if isinstance(r[2], datetime.date) else str(r[2] or '-')
            d2 = r[3].strftime('%d.%m.%Y') if isinstance(r[3], datetime.date) else str(r[3] or '-')
            d3 = r[4].strftime('%d.%m.%Y') if isinstance(r[4], datetime.date) else str(r[4] or '-')
            d4 = r[5].strftime('%d.%m.%Y') if isinstance(r[5], datetime.date) else str(r[5] or '-')
            res = str(r[6] or '-').strip()
            table_lines.append(f"| **{ag}** | {title} | {d1} | {d2} | {d3} | {d4} | {res} |")

    note_bv = f"""---
title: "Bewerbungsverlauf & Tracking Cockpit"
author: "Visar Murseli"
category: "Karriere & Pipeline"
source_file: "file:///{bv_xlsx.replace('\\', '/')}"
last_updated: "{datetime.date.today().isoformat()}"
tags:
  - karriere
  - bewerbungsmanagement
  - pipeline
  - tracking
---

# 📊 Bewerbungsmanagement Cockpit & Pipeline-Historie

> [!NOTE] **Zweck dieses Dossiers**
> Revisionssichere Dokumentation aller Bewerbungskontakte, Interviewstufen, Reaktionszeiten und Feedbacks aus der Master-Tabelle `Bewerbungsverlauf.xlsx`.
> Dient dem LLM als Orientierung, welche Unternehmensprofile, Beratungsansätze und Gehaltsbänder bereits angefragt wurden.

---

## 📋 Status-Matrix der Bewerbungen

{chr(10).join(table_lines)}

---

## 🎯 Strategische Learnings für anstehende Gespräche
1. **Targeting Junior & Trainee:** Absagen auf Senior-/Associate-Stellen (wie bei Schwarz Digits oder Deloitte) bestätigen deine Entscheidung, den gezielten Einstieg als **Junior Consultant oder im Traineeprogramm** anzustreben.
2. **Branchenausrichtung:** Öffentliche Auftraggeber, Stadtwerke, ÖPNV, Mobilität und produzierendes Gewerbe (Axians, SSB-Ökosystem, All for One) schätzen deine 24 Monate SSB-Großprojekterfahrung und Clean Core Kompetenz am höchsten.
3. **Pitches & STAR-Stories nutzen:** Siehe [[03_SAP_EnterpriseArchitecture/SSB_Interview_Stories_STAR]].
"""
    write_vault_note("01_Karriere_Bewerbungen/00_Bewerbungsmanagement_Cockpit.md", note_bv)

    # 3. Masterzeugnis Volltext
    note_mz = f"""---
title: "Amtliches Masterzeugnis (120 ECTS | Gesamtnote 1,6)"
degree: "Master of Science"
university: "Universität Stuttgart"
graduation_date: "17.09.2026"
committee_chair: "Prof. Dr. Christian Becker"
first_examiner_thesis: "Prof. Dr. Georg Herzwurm"
grade_total: "1,6"
grade_thesis: "1,0"
ects: 120
status: "abgeschlossen_beglaubigt"
tags:
  - universitaet_stuttgart
  - masterzeugnis
  - master_of_science
  - 120_ects
---

# 🎓 Amtliches Zeugnis über die Masterprüfung (M.Sc. Wirtschaftsinformatik)

> [!SUMMARY] **Offizielle Eckdaten**
> - **Absolvent:** Visar Murseli (geboren 18.09.1997)
> - **Hochschule:** Universität Stuttgart | Fakultät für Wirtschafts- und Sozialwissenschaften
> - **Akademischer Grad:** Master of Science (M.Sc.) Wirtschaftsinformatik
> - **Ausstellungsdatum:** 17. September 2026
> - **Prüfungsausschussvorsitzender:** Prof. Dr. Christian Becker
> - **Gesamtnote:** **1,6 („gut“)** | **120 Leistungspunkte (ECTS)**

---

## 📜 Vollständige Leistungsübersicht aller 16 Master-Module

| Modulbezeichnung | Katalog | ECTS | Note | Dozent / Prüfer | Kernkompetenz & Praxisrelevanz |
| :--- | :--- | :---: | :---: | :--- | :--- |
| **⭐ Masterarbeit Wirtschaftsinformatik** | Masterarbeit | **30** | **1,0** | Prof. Dr. Georg Herzwurm | Kritische Erfolgsfaktoren (CSF) der S/4HANA Plattformisierung, 12 Experteninterviews im Großprojekt SSB, Mayring Inhaltsanalyse. |
| **Digitale Nachhaltigkeit** | Ergänzung WI | **6** | **1,0** | Dr. Dimitri Petrik | Fallstudie J. Schmalz GmbH: BPMN 2.0 Prozessmodellierung & PowerShell CSRD-Abfallbilanz. |
| **Forschungsprojekte in der WI (FPWI)** | Katalog WI | **6** | **1,3** | Lehrstuhl WI | Smart Service Blueprinting für IoT & cyber-physische Systeme, DSRM nach Peffers, SUS-Score 85/100 (Grade A). |
| **Advanced Software Engineering (ASE)** | Software Eng. | **6** | **1,6** | Prof. Dr. Steffen Becker | Fortgeschrittene Software-Architekturen, Domain-Driven Design (DDD), CI/CD, Enterprise Refactoring. |
| **Software-Architektur** | MINF Informatik | **6** | **1,7** | Prof. Dr. Steffen Becker | Microservices, Event-Driven Architecture, Schnittstellendesign (REST, gRPC), Entkopplungsstrategien. |
| **Forschungsmethoden in der WI** | Pflichtmodul | **6** | **1,7** | Lehrstuhl WI | DSRM, qualitative Inhaltsanalyse nach Mayring, quantitative Hypothesenprüfung. |
| **Seminar Wirtschaftsinformatik 2** | Seminar WI | **6** | **1,7** | Lehrstuhl WI | Systematische Literaturanalyse (SLR nach PRISMA 2020) über 5 Fachdatenbanken (570 Studien) zu Human-Robot Collaboration. |
| **Innovationsmanagement** | BWL | **6** | **1,7** | Lehrstuhl BWL | Disruptive Innovationen, Plattform-Ökosysteme, Technologie-Lebenszyklen und Go-to-Market Planung. |
| **Theorie und Empirie internat. Tätigkeit (INUT)** | BWL | **6** | **1,7** | Prof. Dr. Oesterle | Globale Wertschöpfungsketten, MNEs, internationales Sourcing und Standortentscheidungen. |
| **Applied AI and Upcoming Technologies** | Ergänzung WI | **6** | **1,7** | Lehrstuhl WI | Machine Learning im industriellen Einsatz, NLP, LLM-Architekturen und ERP-Integration. |
| **AI4IoT – Artificial Intelligence for IoT** | Katalog WI | **6** | **2,0** | Lehrstuhl WI | Sensor-Datenströme, Edge Computing, Predictive Maintenance im industriellen Maschinenbau. |
| **Cloud Computing and Service Management** | MINF Informatik | **6** | **2,0** | Lehrstuhl MINF | AWS Well-Architected Framework, Serverless (DynamoDB, EventBridge, Step Functions, Lambda), Cloud SLAs. |
| **Innovationsmethoden (ISG)** | Ergänzung WI | **6** | **2,0** | Prof. Dr. Herzwurm | Digital Venture PatentRadar für Klingele Paper & Packaging (UiPath RPA & SaaS). |
| **Datenbanken und Informationssysteme** | MINF Informatik | **6** | **2,7** | Prof. Dr. Mitschang | Relationale Datenmodelle, SQL, ACID-Transaktionsprinzipien, Indexierungsstrategien (Fundament für SAP HANA). |
| **Management von IT-Unternehmen** | Katalog WI | **6** | **3,0** | Lehrstuhl WI | IT-Governance, COBIT, ITIL Service Lifecycle, IT-Kostenrechnung und Budgetierung. |
| **Service Operations Management (SOM)** | Ergänzung BWL | **6** | **3,0** | Lehrstuhl BWL | Operations Management, Warteschlangentheorie, Kapazitäts- und Durchsatzoptimierung. |

---

## 🔗 Verknüpfungen zu den Fachdossiers
- [[02_Wirtschaftsinformatik_300ECTS/Modul_Masterarbeit]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_Digitale_Nachhaltigkeit]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_FPWI]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_Cloud_Computing]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_Advanced_Software_Engineering]]
"""
    write_vault_note("01_Karriere_Bewerbungen/00_Masterzeugnis_Leistungsuebersicht_Volltext.md", note_mz)

    # 4. Bachelorzeugnis Volltext
    note_bz = f"""---
title: "Amtliche Bachelor-Leistungsübersicht (180 ECTS | Gesamtnote 3,0)"
degree: "Bachelor of Science"
university: "Universität Stuttgart"
graduation_date: "18.09.2023"
ects: 180
grade_total: "3,0"
grade_thesis: "1,7"
status: "abgeschlossen_beglaubigt"
tags:
  - universitaet_stuttgart
  - bachelorzeugnis
  - bachelor_of_science
  - 180_ects
---

# 🏛️ Amtliche Leistungsübersicht Bachelor of Science (B.Sc. Wirtschaftsinformatik)

> [!SUMMARY] **Offizielle Eckdaten**
> - **Absolvent:** Visar Murseli (geboren 18.09.1997)
> - **Hochschule:** Universität Stuttgart | Dezernat 3 - Studium
> - **Akademischer Grad:** Bachelor of Science (B.Sc.) Wirtschaftsinformatik
> - **Abschlussdatum:** 18. September 2023
> - **Gesamtnote:** **3,0** | **180 Leistungspunkte (ECTS)**
> - **Bachelorarbeit:** **Note 1,7 (gut)** bei Prof. Dr. Georg Herzwurm (12 ECTS)
> - **Herausragende Einzelleistung:** **Bestnote 1,0 in Informationssysteme im E-Business**

---

## 📊 Aufteilung nach den 5 Säulen des Bachelorcurriculums

### 1. Bereich D: Bachelorarbeit (12 ECTS | Note 1,7)
- **Titel:** *„Die Bedeutung von Boundary Resources in Low-Code Entwicklungsplattformen: Eine qualitative Untersuchung am Beispiel von OutSystems und Mendix“*
- **Erstprüfer:** Prof. Dr. Georg Herzwurm (Lehrstuhl für ABWL und Wirtschaftsinformatik II)
- **Theoretischer Kern:** Boundary Resource Theory (Ghazawneh & Henfridsson) – Identifikation von 14 Grenzressourcen-Klassen (ABR, DBR, SBR).

### 2. Säule B2: Wirtschaftsinformatik (45 ECTS | Schnitt 2,8)
- **Informationssysteme im E-Business:** **Note 1,0 (Bestnote)** | 4,5 ECTS (Elektronische Marktplätze, EDI, E-Procurement, Function-Point-Analyse)
- **Management betrieblicher Informationssysteme (MBIS):** Note 2,7 | 4,5 ECTS (ERP, SCM, CRM Architekturen)
- **Informationsverarbeitungspraktikum (IVP):** **Note 2,3** | 6 ECTS (Unternehmensanalyse 0x539-Wear GmbH, mehrstufige Deckungsbeitragsrechnung)
- **Einführung in die Wirtschaftsinformatik:** Note 2,7 | 6 ECTS (Prof. Herzwurm)
- **Business Intelligence (BI):** Note 2,7 | 4,5 ECTS (Data Warehousing, ETL, Star-Schema, OLAP-Cubes)
- **Softwarepraktikum (SOPRA):** Note 3,0 | 6 ECTS (Agiles Team-Projekt, taskMasterPro 3 in Java)
- **Grundlagen des Informationsmanagements:** Note 3,3 | 4,5 ECTS
- **Wissensverarbeitung:** Note 3,7 | 6 ECTS (Ontologien, semantische Netze, Inferenz)
- **Informatikrecht:** Note 4,0 | 3 ECTS (DSGVO, Urheberrecht, Softwarevertragsrecht)

### 3. Säule B1: Informatik & Softwaretechnik (48 ECTS | Schnitt 3,3)
- **Modellierung:** **Note 2,3** | 6 ECTS (Prof. Mitschang: BPMN 2.0, UML, Petrinetze, ERM, Relationale Algebra, Normalisierung)
- **Datenstrukturen und Algorithmen (DSA):** Note 3,0 | 9 ECTS (Bäume, Graphen, Sortieralgorithmen, O-Notation)
- **Programmentwicklung:** Note 3,0 | 6 ECTS (Funktionale/logische Programmierung, Clean Code)
- **Mensch-Computer-Interaktion (MCI):** Note 3,3 | 6 ECTS (Usability Engineering, UX, Fiori Design Principles)
- **Einführung in die Softwaretechnik (EST):** Note 3,7 | 6 ECTS (V-Modell, Testing, Design Patterns)
- **Automaten und Formale Sprachen:** Note 3,7 | 6 ECTS (Endliche Automaten, reguläre Sprachen, Turing-Maschinen)
- **Programmierung und Software-Entwicklung (PSE):** Note 4,0 | 9 ECTS (Java OOP, Vererbung, Polymorphie, Collections)

### 4. Säule B3 & Bereich C: BWL, VWL & Management (45 ECTS)
- **GBWL 1: Strukturen der BWL:** Note 2,7 | 6 ECTS (Einführung BWL & Rechnungswesen/Buchführung)
- **GBWL 4: Finanzprozess:** Note 2,7 | 6 ECTS (Investition & Finanzierung, Kapitalwertmethode, Liquiditätssteuerung)
- **GVWL 1: Märkte & Entscheidungen:** Note 2,7 | 6 ECTS (Mikroökonomik, Marktformen, Preisbildung)
- **Profilseminar HRM (Prof. Büttgen):** Note 3,0 | 6 ECTS (Mensch-Roboter-Interaktion & Servicequalität, ECM)
- **BWL 1: Organisation & Führung:** Note 3,3 | 9 ECTS (Strategisches Management, Porter Five Forces, Change Management)
- **Marketing Management:** Note 3,3 | 6 ECTS (Marketing-Mix 4P, Marktforschung)
- **Management von Dienstleistungsunternehmen:** Note 4,0 | 6 ECTS (SERVQUAL, Kapazitätssteuerung, ÖPNV Service Delivery)

### 5. Bereich A & SQ: Mathematisch-Methodische Grundlagen (30 ECTS)
- **Seminar interdisziplinäre Themen:** Note 2,3 | 6 ECTS (Maschinelles Lernen & Big Data)
- **Statistik II (Induktiv):** Note 2,7 | 6 ECTS (Hypothesentests, Konfidenzintervalle, lineare Regression)
- **Statistik I (Deskriptiv):** Note 4,0 | 6 ECTS (Lage- und Streuungsmaße, Korrelationen)
- **Mathematik für Wirtschaftswissenschaftler:** Note 4,0 | 9 ECTS (Lineare Algebra, Differentialrechnung mehrerer Variablen)
- **Schreibwerkstatt:** Bestanden | 3 ECTS (Berufliches & wissenschaftliches Schreiben)

---

## 🔗 Verknüpfungen
- [[02_Wirtschaftsinformatik_300ECTS/Modul_Bachelorarbeit]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_EBusiness]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_Informationsverarbeitungspraktikum]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_Modellierung]]
"""
    write_vault_note("01_Karriere_Bewerbungen/00_Bachelorzeugnis_Leistungsuebersicht_Volltext.md", note_bz)

if __name__ == "__main__":
    process_pillar_00()
