# -*- coding: utf-8 -*-
"""
Full-Text Extractor for Pillar 02 (Master) and Pillar 03 (Bachelor)
Target: C:\\Users\\SHQIPTAR634\\Documents\\Obsidian Vault\\02_Wirtschaftsinformatik_300ECTS
"""
import os
import pypdf
import docx
import datetime

WS_DIR = r"c:\Users\SHQIPTAR634\Desktop\SSB Dateien"
VAULT_DIR = r"C:\Users\SHQIPTAR634\Documents\Obsidian Vault"

def write_vault_note(relative_path, content):
    full_path = os.path.join(VAULT_DIR, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"[OK] Wrote note: {relative_path} ({len(content)} chars)")

def extract_pdf_all(filepath):
    if not os.path.exists(filepath):
        return ""
    try:
        reader = pypdf.PdfReader(filepath)
        pages_text = []
        for i, page in enumerate(reader.pages):
            txt = page.extract_text() or ""
            if txt.strip():
                pages_text.append(f"### Seite {i+1}\n" + txt.strip())
        return "\n\n".join(pages_text)
    except Exception as e:
        print(f"Error reading PDF {filepath}: {e}")
        return ""

def extract_docx_all(filepath):
    if not os.path.exists(filepath):
        return ""
    try:
        doc = docx.Document(filepath)
        paras = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        return "\n\n".join(paras)
    except Exception as e:
        print(f"Error reading DOCX {filepath}: {e}")
        return ""

def run_academic_extraction():
    print("\n=== STARTING PILLARS 02 & 03 (MASTER & BACHELOR) EXTRACTION ===")

    # 1. Masterarbeit Wirtschaftsinformatik (Note 1,0 | 30 ECTS | 126 Seiten)
    ma_pdf = os.path.join(WS_DIR, "00_Aktuelle_Bewerbungsunterlagen", "Masterarbeit_Visar_Murseli.pdf")
    reader_ma = pypdf.PdfReader(ma_pdf)
    
    # Extract key chapters: Abstract (p2), Intro (p8-14), Table 1 CSF (p22-23), Table 2 IPs (p28), Table 4 Framework (p50-55), Conclusion (p56-60)
    abstract_text = reader_ma.pages[1].extract_text()
    toc_text = "\n".join([reader_ma.pages[i].extract_text() for i in range(2, 7)])
    
    # Extract empirical findings and conclusion
    findings_pages = []
    for p_idx in range(40, 56): # Key framework and discussion pages
        if p_idx < len(reader_ma.pages):
            txt = reader_ma.pages[p_idx].extract_text() or ""
            findings_pages.append(f"<!-- Thesis Page {p_idx+1} -->\n" + txt.strip())
    findings_text = "\n\n".join(findings_pages)

    note_ma = f"""---
title: "Masterarbeit Wirtschaftsinformatik – Volltext-Dossier & CSF-Framework"
author: "Visar Murseli, M.Sc."
institution: "Universität Stuttgart"
examiner: "Prof. Dr. Georg Herzwurm (Lehrstuhl für ABWL und Wirtschaftsinformatik II)"
degree: "Master of Science (M.Sc.) Wirtschaftsinformatik"
grade: "1,0 (sehr gut)"
ects: 30
pages: 126
interviews: 12
methodology: "Qualitative Inhaltsanalyse nach Mayring (mit Codebuch) & SLR nach PRISMA"
source_file: "file:///{ma_pdf.replace('\\', '/')}"
tags:
  - masterarbeit
  - s4hana
  - erp_transformation
  - plattformisierung
  - clean_core
  - csf_framework
  - mayring
  - herzwurm
---

# 🎓 Masterarbeit: Kritische Erfolgsfaktoren in der Transformation großer ERP-Systeme

> [!INFO] **Offizieller Titel & Auszeichnung**
> **„Kritische Erfolgsfaktoren in der Transformation großer ERP-Systeme: Eine Untersuchung am Beispiel der Plattformisierung von SAP S/4HANA“**  
> Erstprüfer: **Prof. Dr. Georg Herzwurm** | Universität Stuttgart  
> Umfang: **126 Seiten** | **12 Experteninterviews** im Großprojekt SAP4SSB | **Note 1,0 (Sehr Gut)**

---

## 📌 Abstract der Masterarbeit
{abstract_text}

---

## 📑 Inhalts- und Abbildungsverzeichnis
{toc_text}

---

## 🔬 Forschungsfragen (Research Questions)
1. **FF1:** Welche kritischen Erfolgsfaktoren (CSFs) sind für die Transformation großer ERP-Systeme in komplexen Organisationen relevant?
2. **FF2:** Inwiefern verändern sich diese Erfolgsfaktoren durch die Plattformisierung von ERP-Landschaften (SAP S/4HANA & SAP BTP)?
3. **FF3:** Wie können diese Faktoren in ein phasen- und kategorienbasiertes Implementierungs-Framework überführt werden, um praxistaugliche Handlungsempfehlungen für das Transformationsmanagement abzuleiten?

---

## 📊 Das 4x3 CSF-Framework der Plattformisierung (Mayring-Dimensionen)

Die Analyse der 12 Experteninterviews identifizierte 4 fundamentale Dimensionen:

### 1. Dimension Organisation (Governance, Kultur & Sourcing)
- **Top-Management-Support & Mandat:** Nicht nur Bereitstellung von Budgets, sondern aktives Durchsetzen der Standardorientierung gegen funktionale Silo-Wünsche.
- **Plattform-Governance & Architecture Review Boards (ARB):** Etablierung verbindlicher Entscheidungsgremien zur Freigabe von On-Stack vs. Side-by-Side-Erweiterungen.
- **Sourcing- & Partner-Ökosystem:** Multiprojekt-Steuerung spezialisierter Implementierungspartner (Nagarro für kaufmännische Prozesse, Evora für mobile Instandhaltung, Axians für Cloud-Infrastruktur).

### 2. Dimension Technik (Clean Core & Integrationsarchitektur)
- **Strikter Clean-Core-Ansatz:** Kernsystem modifikationsfrei halten; Erweiterungen ausschließlich über freigegebene Schnittstellen (APIs und CDS Views).
- **Entkopplung via SAP BTP:** Side-by-Side Extensibility, Event-Driven Architecture und zentrale API-Verwaltung verhindern Vendor Lock-in und technische Verschuldung.
- **Datenqualität & Revisionssichere Migration:** Harmonisierung heterogener Stammdaten (CVI Business Partner) und bilanzielle Abstimmung des Datenübernahmekontos auf exakt 0,00 €.

### 3. Dimension Mensch (Absorptive Capacity & Mitbestimmung)
- **Institutionalisierte Mitbestimmung (Betriebsrat):** Frühzeitige Einbindung nach § 87 Abs. 1 Nr. 6 BetrVG über Meilensteine (Pilot-BV vor UAT-Testbetrieb, Finale BV vor Go-Live).
- **Absorptive Capacity (Cohen & Levinthal):** Kontinuierlicher Aufbau von Vorwissen in den Fachbereichen durch Single-Source-Lernplattformen (SAP Enable Now).
- **Mindset-Shift:** Übergang von der "Wir customizen alles"-Mentalität zur "Fit-to-Standard"-Kultur.

### 4. Dimension Projektmanagement (Methodik & Tooling)
- **SAP Activate & Fit-to-Standard:** Iterative Prozessvalidierung direkt am laufenden System statt mehrjähriger isolierter Pflichtenhefterstellung.
- **Tool-Traceability:** Lückenlose Traceability durch Kopplung von SAP Signavio (BPMN 2.0 Geschäftsprozess) und SAP Cloud ALM (Testskripte, User Stories, Quality Gates).

---

## 🎙️ Übersicht der 12 empirischen Experteninterviews (Tabelle 2 der Masterarbeit)

| ID | Position / Funktion | Kontext / Organisation | Datum | Dauer |
| :---: | :--- | :--- | :---: | :---: |
| **IP1** | Teilprojektleiter Kaufmännische Prozesse (UB Steuerung) | Kommunales Verkehrsunternehmen (SSB AG) | 28.11.2025 | 28 Min. |
| **IP2** | Gesamtprojektleiter S/4HANA Transformation (Leiter PL-Pool) | Kommunales Verkehrsunternehmen (SSB AG) | 18.12.2025 | 54 Min. |
| **IP3** | SAP Inhouse Consultant | Kommunales Verkehrsunternehmen (SSB AG) | 05.12.2025 | 45 Min. |
| **IP4** | Projektleiter S/4HANA-HR-Projekt | Internationaler Handelskonzern | 05.12.2025 | 30 Min. |
| **IP5** | SAP Solution Architekt | Führendes SAP-Beratungshaus (Partner) | 08.12.2025 | 35 Min. |
| **IP6** | Teamleiter SAP Betrieb & Infrastruktur | Kommunales Verkehrsunternehmen (SSB AG) | 16.12.2025 | 37 Min. |
| **IP7** | Cloud- & Basis-Architekt | Kommunales Verkehrsunternehmen (SSB AG) | 05.12.2025 | 38 Min. |
| **IP8** | SAP HCM Projektleiter | SAP-Beratungshaus | 12.12.2025 | 25 Min. |
| **IP9** | Enterprise Basisarchitekt | Kommunales Verkehrsunternehmen (SSB AG) | 02.12.2025 | 57 Min. |
| **IP10** | SAP Inhouse Consultant | Kommunales Verkehrsunternehmen (SSB AG) | 15.12.2025 | 30 Min. |
| **IP11** | Teamleiter SAP-Team | Kommunales Verkehrsunternehmen (SSB AG) | 10.12.2025 | 27 Min. |
| **IP12** | SAP Inhouse Consultant | Kommunales Verkehrsunternehmen (SSB AG) | 27.11.2025 | 33 Min. |

---

## 📜 Auszug empirische Synthese & Framework (Seiten 41–55 der Arbeit)

{findings_text}

---

## 🔗 Verknüpfungen im Wissensnetz
- Vollständige Interview-Transkripte: [[03_SAP_EnterpriseArchitecture/SSB_Interviews_Experten_Transkripte]]
- Lösungsdesign Großprojekt: [[03_SAP_EnterpriseArchitecture/SSB_Solution_Design_Volltext]]
- Clean Core Dossier: [[03_SAP_EnterpriseArchitecture/01_Architektur_Technik/Clean_Core_Paradigma]]
- Bachelorarbeit-Fundament: [[02_Wirtschaftsinformatik_300ECTS/Modul_Bachelorarbeit]]
"""
    write_vault_note("02_Wirtschaftsinformatik_300ECTS/Modul_Masterarbeit.md", note_ma)

    # 2. Digitale Nachhaltigkeit (Schmalz GmbH Fallstudie | Note 1,0)
    schmalz_pdf = os.path.join(WS_DIR, "02_Master", "Digitale Nachhaltigkeit", "01_Vorlesung_und_Uebungen", "Upload-Ordner fuer schriftliche Ausarbeitungen - zum 01.07.2024", "Ausarbeitung_Degraf_Mirzaie_Murseli_Vischer", "Schriftliche Ausarbeitung", "Schriftliche_Ausarbeitung_Degraf_Mirzaie_Murseli_Vischer.pdf")
    schmalz_text = extract_pdf_all(schmalz_pdf)

    note_schmalz = f"""---
title: "Digitale Nachhaltigkeit: Fallstudie J. Schmalz GmbH (CSRD-Abfallbilanz)"
author: "Visar Murseli, Vitalij Degraf, Arwin Mirzaie, Tobias Vischer"
supervisor: "Dr. Dimitri Petrik"
institution: "Universität Stuttgart"
grade: "1,0 (sehr gut)"
ects: 6
methods: "BPMN 2.0, PowerShell Automatisierung, Life Cycle Assessment (LCA), CSRD/ESG Reporting"
source_file: "file:///{schmalz_pdf.replace('\\', '/')}"
tags:
  - digitale_nachhaltigkeit
  - schmalz
  - csrd
  - powershell
  - bpmn
  - green_it
---

# 🌱 Digitale Nachhaltigkeit: Fallstudie J. Schmalz GmbH (Note 1,0)

> [!SUMMARY] **Projektsteckbrief**
> - **Thema:** Nachhaltigkeit durch Automatisierung: Eine Fallstudie zur Optimierung der Abfallbilanz bei der J. Schmalz GmbH
> - **Dozent:** Dr. Dimitri Petrik (Universität Stuttgart)
> - **Note:** **1,0 (sehr gut)** | **6 ECTS**
> - **Industriepartner:** J. Schmalz GmbH (Glattener Vakuum-Technologie-Weltmarktführer)

---

## 📌 Executive Summary
Die J. Schmalz GmbH stand vor der Herausforderung, für ihre jährliche CSRD-konforme Nachhaltigkeitsberichterstattung hunderte Entsorgungsbelege, Wiegescheine und Gefahrgutnachweise manuell aus E-Mails und PDF-Anhängen in Excel-Tabellen zu übertragen. Dies führte zu hohem Zeitaufwand und manuellen Übertragungsfehlern.

Im Projekt wurde:
1. Der **Ist-Prozess in BPMN 2.0** lückenlos modelliert und Schwachstellen identifiziert.
2. Ein **Soll-Prozess mit automatisiertem Workflow** konzipiert.
3. Ein voll funktionsfähiger **PowerShell-Automatisierungs-Prototyp** entwickelt, der Entsorgungs-Nachweise automatisiert aus Postfächern extrahiert, validiert und in ein harmonisiertes Reporting-Schema einspeist.
4. Eine **ökologische und ökonomische Bewertung** nach LCA-Standards durchgeführt.

---

## 📜 Volltext der wissenschaftlichen Ausarbeitung (15 Seiten)

{schmalz_text}

---

## 🔗 Verknüpfungen
- [[03_SAP_EnterpriseArchitecture/02_Kaufmaennische_Prozesse/EHS_Gefahrstoff_Nachhaltigkeitsberichterstattung]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_Übersicht]]
"""
    write_vault_note("02_Wirtschaftsinformatik_300ECTS/Modul_Digitale_Nachhaltigkeit.md", note_schmalz)

    # 3. FPWI: Smart Service Blueprinting (Note 1,3 | 6 ECTS)
    fpwi_pdf = os.path.join(WS_DIR, "02_Master", "Forschungsprojekte in der Wirtschaftsinformatik", "01_Finale_Abgabe_und_Praesentation", "RiP_Anders_Murseli_Tumar.pdf")
    fpwi_text = extract_pdf_all(fpwi_pdf)

    note_fpwi = f"""---
title: "FPWI: Smart Service Blueprinting Framework (DSRM & IoT Services)"
author: "Visar Murseli, David Anders, Umut Eren Tumar"
institution: "Universität Stuttgart"
grade: "1,3 (sehr gut)"
ects: 6
methods: "Design Science Research (DSRM nach Peffers), Thinking-Aloud Evaluation, System Usability Scale (SUS)"
source_file: "file:///{fpwi_pdf.replace('\\', '/')}"
tags:
  - fpwi
  - smart_services
  - iot
  - dsrm
  - thinking_aloud
  - sus_score_85
---

# ⚡ Forschungsprojekt WI: Smart Service Blueprinting (Note 1,3)

> [!SUMMARY] **Wissenschaftlicher Beitrag**
> - **Titel:** Integration physischer und digitaler Welten: Ein Framework für Smart Service Blueprinting
> - **Note:** **1,3 (sehr gut)** | **6 ECTS**
> - **Methodik:** Design Science Research Methodology (DSRM nach Peffers et al.)
> - **Empirische Evaluation:** Thinking-Aloud Usability-Tests mit Software-Ingenieuren & **SUS-Score 85/100 (Grade A / Excellent)**.

---

## 📌 Problemstellung & Forschungslücke
Klassisches Service Blueprinting (nach Shostack / Bitner) modelliert Kundeninteraktionen, Onstage- und Backstage-Aktivitäten rein linear. Bei cyber-physischen Systemen (CPS) und vernetzten IoT-Produkten interagieren physische Sensoren, Cloud-Dienste und automatisierte Algorithmen jedoch autonom im Hintergrund. 

Das entwickelte Framework erweitert das Blueprinting um:
1. **Physische Sensorik & Aktorik-Ebene** (Hardware-Touchpoints, Telemetriedaten)
2. **Digitale Service- & Cloud-Ebene** (Schnittstellen, Event-Streams, Datenanalyse)
3. **Kollaborative Interaktionsebenen** zwischen Mensch und smartem Produkt.

---

## 📜 Volltext des Research-in-Progress Papers (12 Seiten)

{fpwi_text}

---

## 🔗 Verknüpfungen
- [[02_Wirtschaftsinformatik_300ECTS/Modul_AI4IoT]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_Cloud_Computing]]
"""
    write_vault_note("02_Wirtschaftsinformatik_300ECTS/Modul_FPWI.md", note_fpwi)

    # 4. Bachelorarbeit: Boundary Resources in Low-Code Plattformen (Note 1,7 | 12 ECTS)
    ba_pdf = os.path.join(WS_DIR, "03_Bachelor", "Bachelorarbeit Wirtschaftsinformatik", "01_Erfolgreiche_Bachelorarbeit_Boundary_Resources_Note_1_7", "Abgabe_Bachelorarbeit_Murseli", "Bachelorarbeit_Murseli.pdf")
    reader_ba = pypdf.PdfReader(ba_pdf)
    ba_abstract = reader_ba.pages[1].extract_text()
    
    # Extract sample chapters
    ba_pages = []
    for idx in [0, 1, 7, 8, 9, 20, 21, 45, 46, 70, 71]:
        if idx < len(reader_ba.pages):
            ba_pages.append(f"<!-- Page {idx+1} -->\n" + (reader_ba.pages[idx].extract_text() or "").strip())
    ba_sample = "\n\n".join(ba_pages)

    note_ba = f"""---
title: "Bachelorarbeit: Boundary Resources in Low-Code Entwicklungsplattformen"
author: "Visar Murseli, B.Sc."
examiner: "Prof. Dr. Georg Herzwurm (Lehrstuhl für ABWL und Wirtschaftsinformatik II)"
institution: "Universität Stuttgart"
degree: "Bachelor of Science (B.Sc.) Wirtschaftsinformatik"
grade: "1,7 (gut)"
ects: 12
pages: 103
cases: "OutSystems & Mendix"
theory: "Boundary Resource Theory (Ghazawneh & Henfridsson)"
source_file: "file:///{ba_pdf.replace('\\', '/')}"
tags:
  - bachelorarbeit
  - boundary_resources
  - low_code
  - outsystems
  - mendix
  - herzwurm
---

# 🏛️ Bachelorarbeit: Boundary Resources in Low-Code Plattformen (Note 1,7)

> [!INFO] **Offizieller Titel & Lehrstuhl**
> **„Die Bedeutung von Boundary Resources in Low-Code Entwicklungsplattformen: Eine qualitative Untersuchung am Beispiel von OutSystems und Mendix“**  
> Erstprüfer: **Prof. Dr. Georg Herzwurm** | Universität Stuttgart  
> Umfang: **103 Seiten** | **Note 1,7 (Gut)** | **12 ECTS**

---

## 📌 Abstract
{ba_abstract}

---

## 🎯 Die 14 Boundary-Resource-Klassen (ABR, DBR, SBR)
Die Bachelorarbeit klassifizierte die Grenzressourcen von Low-Code Plattformen in 3 Hauptgruppen:

### 1. Application Boundary Resources (ABR)
- **REST & SOAP Schnittstellen:** Standardisierte APIs zur Integration bestehender Enterprise-Systeme.
- **Datenkonnektoren:** Vorkonfigurierte Adapter für SQL, SAP, Salesforce und NoSQL.
- **Webhooks & Event-Handler:** Asynchrone Trigger für externe Systembenachrichtigungen.

### 2. Development Boundary Resources (DBR)
- **Visuelle IDE (Integrated Development Environment):** Drag-and-Drop Editoren für UI, Geschäftslogik und Datenmodelle.
- **Software Development Kits (SDKs):** Erweiterungsmöglichkeiten für professionelle Entwickler (Custom Code in Java/C#).
- **Test- & Debugging-Harnesses:** Integrierte Testautomatisierung und Breakpoint-Debugging.
- **Komponenten-Bibliotheken:** Wiederverwendbare UI-Widgets und Microflows.

### 3. Social Boundary Resources (SBR)
- **App-Marktplätze & Ökosysteme:** OutSystems Forge bzw. Mendix Marketplace für Community-Erweiterungen.
- **Entwickler-Communities & Foren:** Peer-to-Peer Wissensaustausch und Support.
- **Architektur-Richtlinien & Styleguides:** Leitfäden für saubere Modularisierung und Performance.
- **Zertifizierungsprogramme:** Qualifizierungsstufen für Associate, Professional und Expert Developer.

---

## 📜 Auszug aus der Original-Bachelorarbeit (103 Seiten)

{ba_sample}

---

## 🔗 Verknüpfungen
- Weiterführung im Master: [[02_Wirtschaftsinformatik_300ECTS/Modul_Masterarbeit]]
- E-Business Grundlagen: [[02_Wirtschaftsinformatik_300ECTS/Modul_EBusiness]]
"""
    write_vault_note("02_Wirtschaftsinformatik_300ECTS/Modul_Bachelorarbeit.md", note_ba)

    # 5. IVP Unternehmensanalyse 0x539-Wear GmbH (Note 2,3 | 6 ECTS)
    ivp_docx = os.path.join(WS_DIR, "03_Bachelor", "Informationsverarbeitungspraktikum", "01_Praktikum_IVP_SS19", "ABGABE", "Ausarbeitung_KablanMurseliStreich.docx")
    ivp_text = extract_docx_all(ivp_docx)

    note_ivp = f"""---
title: "Informationsverarbeitungspraktikum (IVP): Unternehmensanalyse 0x539-Wear GmbH"
author: "Visar Murseli, Kablan, Streich"
institution: "Universität Stuttgart (Lehrstuhl Abteilung VII - WI)"
grade: "2,3 (gut)"
ects: 6
methods: "Mehrstufige Deckungsbeitragsrechnung (DB I-IV), BI-Datenanalyse, ABC-Analyse, Plan-Ist-Vergleich"
source_file: "file:///{ivp_docx.replace('\\', '/')}"
tags:
  - ivp
  - controlling
  - deckungsbeitragsrechnung
  - datenanalyse
  - business_intelligence
---

# 📊 IVP: Quantitative Unternehmensanalyse 0x539-Wear GmbH (Note 2,3)

> [!SUMMARY] **Praktikumsschwerpunkt**
> - **Projekt:** Detaillierte datengestützte Analyse der betrieblichen Prozesse der 0x539-Wear GmbH
> - **Note:** **2,3 (gut)** | **6 ECTS**
> - **Kernkompetenz:** Beherrschung des internen Rechnungswesens, Deckungsbeitragsrechnung und SQL/Excel-basierte Auswertung von Massendaten.

---

## 📌 Analyseschwerpunkte
1. **Bestellungs- und Auftragsanalyse:** Identifikation von Saisonalitäten, Durchlaufzeiten und Retourenquoten.
2. **Mehrstufige Deckungsbeitragsrechnung:**
   - **DB I:** Umsatzerlöse abzüglich proportionaler variabler Produktkosten.
   - **DB II:** DB I abzüglich erzeugnisfixer Kosten (direkte Maschinen- und Rüstkosten).
   - **DB III:** DB II abzüglich Erzeugnisgruppen-Fixkosten (Spartenmarketing).
   - **DB IV:** Betriebsergebnis nach Abzug der Unternehmens-Gemeinkosten.
3. **Kunden- und Lieferanten-Rentabilität:** Aufdeckung unrentabler Kleinaufträge und Abhängigkeiten von Schlüssellieferanten.
4. **Bestandsoptimierung:** Reduzierung von Kapitalbindungskosten bei Ladenhütern.

---

## 📜 Volltext der Unternehmensanalyse (Ausarbeitung)

{ivp_text}

---

## 🔗 Verknüpfungen
- Controlling-Praxis bei SSB: [[03_SAP_EnterpriseArchitecture/02_Kaufmaennische_Prozesse/Kostenrechnung_PSP_vs_Innenauftrag]]
- Trennungsrechnung: [[03_SAP_EnterpriseArchitecture/02_Kaufmaennische_Prozesse/Trennungsrechnung_OEPNV_EU1370]]
"""
    write_vault_note("02_Wirtschaftsinformatik_300ECTS/Modul_Informationsverarbeitungspraktikum.md", note_ivp)

    # 6. Seminar WI 2: Human-Robot Collaboration (Note 1,7 | 6 ECTS)
    sem2_docx = os.path.join(WS_DIR, "02_Master", "Seminar Wirtschaftsinformatik 2", "01_Erfolgreiche_Seminararbeit_MRK_SS25", "01_Finale_Abgabe_und_Praesentation", "FINAL_Seminararbeit_Murseli.docx")
    sem2_text = extract_docx_all(sem2_docx)

    note_sem2 = f"""---
title: "Seminar WI 2: Mensch-Roboter-Kollaboration in der Produktion (PRISMA 2020 SLR)"
author: "Visar Murseli"
institution: "Universität Stuttgart"
grade: "1,7 (gut)"
ects: 6
methods: "Systematische Literaturanalyse (SLR nach PRISMA 2020), Konzeptmatrix, 570 Studien analysiert"
source_file: "file:///{sem2_docx.replace('\\', '/')}"
tags:
  - seminar_wi2
  - prisma_2020
  - slr
  - mrk
  - industrie_5_0
  - human_ai_collaboration
---

# 🤖 Seminararbeit WI 2: Mensch-Roboter-Kollaboration in Industrie 5.0 (Note 1,7)

> [!SUMMARY] **Wissenschaftliche Methodik**
> - **Thema:** Die Transformation menschlicher Arbeitsrollen durch KI-gestützte Mensch-Roboter-Kollaboration in der Produktion
> - **Note:** **1,7 (gut)** | **6 ECTS**
> - **Methodischer Standard:** PRISMA 2020 (Preferred Reporting Items for Systematic Reviews and Meta-Analyses)
> - **Umfang der Recherche:** 5 Fachdatenbanken (SpringerLink, AISeL, IEEE Xplore, ScienceDirect, ACM) mit 570 Treffern, verdichtet auf 26 Kernstudien.

---

## 📜 Volltext der Seminararbeit (31.000 Zeichen)

{sem2_text}

---

## 🔗 Verknüpfungen
- [[02_Wirtschaftsinformatik_300ECTS/Modul_Masterarbeit]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_AI4IoT]]
"""
    write_vault_note("02_Wirtschaftsinformatik_300ECTS/Modul_Seminar_WI2.md", note_sem2)

    # 7. Cloud Computing Kurzpaper (Note 2,0 | 6 ECTS)
    cloud_pdf = os.path.join(WS_DIR, "02_Master", "Service Management and Cloud Computing, and Evaluation", "03_Exam_Paper_Hausarbeit", "Kurzpaper_Murseli.pdf")
    cloud_text = extract_pdf_all(cloud_pdf)

    note_cloud = f"""---
title: "Cloud Computing: Cloud-basierte Plattformarchitektur (AWS Well-Architected)"
author: "Visar Murseli"
institution: "Universität Stuttgart"
grade: "2,0 (gut)"
ects: 6
methods: "AWS Well-Architected Framework, Serverless, DynamoDB, EventBridge, Step Functions"
source_file: "file:///{cloud_pdf.replace('\\', '/')}"
tags:
  - cloud_computing
  - aws
  - serverless
  - microservices
  - event_driven
---

# ☁️ Cloud Computing: Plattformarchitektur für E-Commerce (Note 2,0)

> [!SUMMARY] **Projektsteckbrief**
> - **Thema:** Entwicklung einer Cloud-basierten Plattformarchitektur für einen wachsenden Onlineshop
> - **Note:** **2,0 (gut)** | **6 ECTS**
> - **Architekturmodell:** AWS Serverless Architecture (DynamoDB NoSQL, Amazon EventBridge, AWS Step Functions, Lambda Microservices, Amazon QuickSight).

---

## 📜 Volltext des wissenschaftlichen Kurzpapers (12 Seiten)

{cloud_text}

---

## 🔗 Verknüpfungen
- [[03_SAP_EnterpriseArchitecture/01_Architektur_Technik/SAP_BTP_Integration_Suite]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_Advanced_Software_Engineering]]
"""
    write_vault_note("02_Wirtschaftsinformatik_300ECTS/Modul_Cloud_Computing.md", note_cloud)

if __name__ == "__main__":
    run_academic_extraction()
