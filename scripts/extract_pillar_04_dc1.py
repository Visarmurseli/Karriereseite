# -*- coding: utf-8 -*-
"""
Full-Text Extractor for Pillar 04 (Datacenter One) & Master Graph Synthesis
Target: C:\\Users\\SHQIPTAR634\\Documents\\Obsidian Vault
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
                pages_text.append(f"<!-- Page {i+1} -->\n" + txt.strip())
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

def run_dc1_and_index_extraction():
    print("\n=== STARTING PILLAR 04 (DC1) & MASTER GRAPH SYNTHESIS ===")

    # 1. Carriermanagement Volltext
    cm_docx = os.path.join(WS_DIR, "04_DC1", "02_Projekte_und_Architektur", "02_Carriermanagement_INOC", "CM_ins_INOC_Projekt_VIM.docx")
    cm_text = extract_docx_all(cm_docx)

    # 2. HLM Bericht Volltext
    hlm_pdf = os.path.join(WS_DIR, "04_DC1", "02_Projekte_und_Architektur", "01_Hardware_Lifecycle_Management", "Bericht_Notebookaustausch.pdf")
    hlm_text = extract_pdf_all(hlm_pdf)

    # Note 1: DC1 ITIL 4 Service Operations (Comprehensive enriched dossier)
    note_dc1_ops = f"""---
title: "Datacenter One (DC1): ITIL 4 Service Operations & INOC Leitstand"
company: "Datacenter One GmbH (Stuttgart)"
role: "Werkstudent Information Network Operation Center (INOC)"
supervisor: "Helmut Schmidpeter"
period: "05/2023 – 04/2024 (12 Monate)"
methods: "ITIL 4 Service Operations, PRTG Network Monitor, Jira Service Management, Confluence SOPs"
tags:
  - datacenter_one
  - dc1
  - itil4
  - inoc
  - monitoring
  - prtg
  - jira_service_management
  - sla_management
---

# 🏢 Datacenter One (DC1) – 12 Monate ITIL 4 Service Operations im INOC

> [!INFO] **Rahmendaten der Station**
> - **Unternehmen:** Datacenter One GmbH (führender Rechenzentrumsbetreiber für Colocation und Connectivity in Deutschland)
> - **Abteilung:** Information Network Operation Center (INOC) unter Helmut Schmidpeter
> - **Zeitraum:** Mai 2023 – April 2024 (**12 Monate**)
> - **Verantwortung:** 24/7 Leitstand, Single Point of Contact (SPoC) für Enterprise-Kunden und Tier-1 Carrier.

---

## 🎯 Kernaufgaben & operative Verantwortung

### 1. 24/7 Monitoring von Core-Netzwerken & RZ-Infrastruktur
- Kontinuierliche Überwachung hochverfügbarer Rechenzentrumsstandorte (DUS1, STR1 etc.) über den **PRTG Network Monitor**.
- Überwachung von Core-Switchen, Routern, Glasfaser-Trassen (Colo Connect), unterbrechungsfreien Stromversorgungen (USV), Diesel-Notstromaggregaten und Klimatechnik (HVAC).
- Latenz-, Packet-Loss- und Jitter-Messungen auf Kunden-Uplinks zur Einhaltung vertraglicher **Service Level Agreements (SLAs bis 99,99%)**.

### 2. ITIL 4 Incident & Problem Management als SPoC
- Zentraler **Single Point of Contact (SPoC)** für Großkunden, Internet Service Provider (ISPs) und Tier-1 Carrier (Telekom, Vodafone, Colt, GasLINE).
- Qualifizierte Ticketerfassung, Priorisierung (Severity 1–4) und lückenlose Bearbeitung im **Jira Service Management**.
- Koordination von Notfall-Einsätzen mit Field Service Technikern vor Ort im Rechenzentrum und Begleitung von Schaltungsterminen in Meet-Me-Rooms (MMR).

### 3. Wissensmanagement & Standard Operating Procedures (SOPs)
- Konzeption und Aufbau einer zentralen Wissensdatenbank in **Atlassian Confluence**.
- Erstellung und Pflege standardisierter Betriebsleitfäden (SOPs) für wiederkehrende Incident-Muster (z.B. Faserbruch auf Carrier-Strecken, USV-Alarme, Notfall-Eskalationspfade).
- Nachweisbare Steigerung der Erstlösungsquote (**First Contact Resolution, FCR**) und signifikante Reduzierung der Onboarding-Zeit neuer Leitstands-Mitarbeiter.

---

## 💡 Die 3 wichtigsten Learnings für Enterprise-Architektur & SAP

1. **Absolute SLA-Disziplin (99,99% Verfügbarkeit):**
   Im Rechenzentrumsbetrieb bedeutet ein Ausfall von wenigen Minuten massive Vertragsstrafen und Reputationsschäden. Man verinnerlicht höchste Sorgfalt bei Konfigurationsänderungen (Change-Management).
2. **Dokumentationsqualität als Lebensversicherung:**
   Im 24/7 Schichtbetrieb muss die nachfolgende Schicht ein Ticket in 30 Sekunden vollständig verstehen, ohne telefonische Rückfragen stellen zu müssen.
3. **Deeskalierende Krisenkommunikation:**
   Wenn bei einem Enterprise-Kunden die Primärverbindung ausfällt, zählt sachliche, ruhige und transparente Kommunikation mit klaren Zeithorizonten.

---

## 📡 Carriermanagement-Integration ins INOC (Projektkonzeption)
Auszug aus der Konzeption von Visar Murseli zur Übernahme von Carrier-Management- und Netzanbindungsprozessen in den INOC-Leitstand:

{cm_text[:15000]}

---

## 🔗 Verknüpfungen im Wissensnetz
- Hardware Lifecycle Management: [[03_SAP_EnterpriseArchitecture/DC1_Hardware_Lifecycle_Management]]
- S/4HANA Brücke (Cloud Basis): [[03_SAP_EnterpriseArchitecture/01_Architektur_Technik/SAP_BTP_Integration_Suite]]
- TOGAF Adaption: [[02_Wirtschaftsinformatik_300ECTS/Modul_TOGAF_Scape]]
"""
    write_vault_note("03_SAP_EnterpriseArchitecture/DC1_ITIL4_Service_Operations.md", note_dc1_ops)

    # Note 2: DC1 Hardware Lifecycle Management
    note_dc1_hlm = f"""---
title: "Datacenter One: Hardware Lifecycle Management (HLM) – Prozessdesign & Rollout"
company: "Datacenter One GmbH"
methods: "BPMN 2.0 (MS Visio), IT-Asset-Management, Dell PoC Rollout-Planung, DSGVO-Decommissioning"
tags:
  - dc1
  - hlm
  - hardware_lifecycle
  - bpmn
  - rollout
  - asset_management
---

# 💻 Datacenter One: Hardware Lifecycle Management (HLM)

> [!SUMMARY] **Projektsteckbrief**
> - **Thema:** Konzeption und Begleitung des Hardware-Lifecycle-Management-Prozesses für über 100 Arbeitsplatz- und Leitstandssysteme
> - **Modellierung:** Formale BPMN-Modellierung in Microsoft Visio (`HLM_v2.vsdx`)
> - **Ziel:** Vermeidung von Ausfallzeiten im 24/7 Leitstandbetrieb und lückenlose Revisionssicherheit bei Beschaffung, Rollout und Entsorgung.

---

## 🔄 Die 4 Lebenszyklus-Phasen des HLM-Prozesses

```mermaid
flowchart LR
    A["1. Bedarfsanalyse & Beschaffung"] --> B["2. Staging & Betankung"]
    B --> C["3. Rollout im 24/7 Betrieb"]
    C --> D["4. Decommissioning & Löschung"]
```

1. **Bedarfsanalyse & Beschaffung:**
   - Standardisierte Spezifikationen für Leitstands-Workstations (High-Performance Multi-Screen) und mobile Precisions für Techniker.
   - Pufferung von Reservegeräten und Test-Hardware zur Vermeidung von Lieferengpässen.
2. **Staging & Betankung:**
   - Automatisierte OS-Betankung, Treiber-Integration und Installation standardisierter Sicherheitssoftware (VPN, MFA, Monitoring-Agents).
3. **Rollout im 24/7 laufenden Betrieb:**
   - Schicht-synchrone Austauschplanung, um Arbeitsplätze ohne Unterbrechung der Leitstandsüberwachung umzustellen.
4. **Decommissioning & Zertifizierte Datenlöschung:**
   - Sichere Löschung nach BSI-Standards, Entinventarisierung in der Asset-Datenbank und umweltgerechte Verwertung.

---

## 📜 Volltext des Projektberichts Notebookaustausch

{hlm_text}

---

## 🔗 Verknüpfungen
- Leitstandsbetrieb: [[03_SAP_EnterpriseArchitecture/DC1_ITIL4_Service_Operations]]
- Prozessmodellierung: [[02_Wirtschaftsinformatik_300ECTS/Modul_Modellierung]]
"""
    write_vault_note("03_SAP_EnterpriseArchitecture/DC1_Hardware_Lifecycle_Management.md", note_dc1_hlm)

    # Note 3: TOGAF Scape Consulting Dossier in Bachelor/Master
    note_togaf = f"""---
title: "TOGAF 9 ADM – Enterprise Architecture Management (EAM) Zertifizierung"
institution: "Universität Stuttgart & Scape Consulting GmbH"
instructor: "Dr. Daniel Simon"
date: "16.01.2020"
methods: "TOGAF 9 Architecture Development Method (ADM), Architecture Metamodel, Gap Analysis"
tags:
  - togaf
  - eam
  - enterprise_architecture
  - scape_consulting
  - adm
---

# 🏛️ TOGAF 9 ADM – Enterprise Architecture Management (EAM)

> [!INFO] **Offizielle Zertifizierung**
> - **Lehrgang:** TOGAF 9 ADM-Intensivkurs an der Universität Stuttgart
> - **Dozent:** Dr. Daniel Simon (Senior Architekt & Geschäftsführer Scape Consulting GmbH)
> - **Abschlussdatum:** 16. Januar 2020 (Teilnahmebescheinigung amtlich verifiziert)
> - **Kernkompetenz:** Beherrschung des weltweiten De-facto-Standards für Enterprise Architecture Management (The Open Group).

---

## 🔄 Der TOGAF ADM Zyklus (Phasen A bis H)

```mermaid
flowchart TD
    PRE["Preliminary Phase: Framework & Principles"] --> A["Phase A: Architecture Vision"]
    A --> B["Phase B: Business Architecture"]
    B --> C["Phase C: Information Systems Architecture (Data & App)"]
    C --> D["Phase D: Technology Architecture"]
    D --> E["Phase E: Opportunities & Solutions"]
    E --> F["Phase F: Migration Planning"]
    F --> G["Phase G: Implementation Governance"]
    G --> H["Phase H: Architecture Change Management"]
    H --> A
```

---

## 🧩 Das TOGAF Architecture Metamodel

Das Metamodell verknüpft vier Architekturebenen:
1. **Business Architecture:** Business Capabilities, Geschäftsprozesse, Organisationseinheiten, Rollen und Geschäftsziele.
2. **Data Architecture:** Data Entities, logische Datenmodelle, Datenflüsse und Eigentümerschaften.
3. **Application Architecture:** Anwendungs-Komponenten, Schnittstellen (APIs) und Schnittstellenverträge.
4. **Technology Architecture:** Server, Cloud-Plattformen, Netzwerkknoten und physische Rechenzentren.

---

## 🛠️ Praxisanwendung im Großprojekt SAP4SSB
- **Baseline Architecture:** Gewachsenes SAP ECC 6.0 On-Premise mit unzähligen Z-Modifikationen und proprietären Schnittstellen.
- **Target Architecture:** Modifikationsfreies S/4HANA Private Cloud System (Clean Core) mit SAP BTP als Side-by-Side Integrationsplattform.
- **Transition Architecture:** 4-System-Landschaft (ES4.400 Sandbox, QS4.100 Integrations-Test 1, QS4.210 UAT/Pilot-BV, PS4 Produktivsystem) und stufenweise Bereinigung über LTMC Staging-Tabellen.

---

## 🔗 Verknüpfungen
- Masterarbeit CSF-Framework: [[02_Wirtschaftsinformatik_300ECTS/Modul_Masterarbeit]]
- SSB Lösungsdesign: [[03_SAP_EnterpriseArchitecture/SSB_Solution_Design_Volltext]]
- EAM Map of Content: [[03_SAP_EnterpriseArchitecture/00_MOCs/MOC_Enterprise_Architecture]]
"""
    write_vault_note("02_Wirtschaftsinformatik_300ECTS/Modul_TOGAF_Scape.md", note_togaf)

    # Note 4: 00_INDEX.md – Master Map of Content (MOC)
    note_master_index = f"""---
title: "Master Knowledge Graph & Wissensnetz Index"
author: "Visar Murseli, M.Sc."
degree: "Master of Science Wirtschaftsinformatik (Note 1,6 | Masterarbeit 1,0)"
experience: "36 Monate Berufserfahrung (24 Mo. SSB AG + 12 Mo. Datacenter One)"
last_updated: "{datetime.date.today().isoformat()}"
tags:
  - moc
  - index
  - master_knowledge_graph
  - second_brain
  - rag_lake
---

# 🧠 Visar Murseli | Master Knowledge Graph & Second Brain Index

> [!NOTE] **Local RAG & Wissensnetz Single Source of Truth**
> Dieser Obsidian Vault bildet die vollständige, verifizierte Wissensbasis von Visar Murseli ab:
> Er verbindet alle akademischen Originalarbeiten (300 ECTS an der Universität Stuttgart), die 24-monatige Großprojekterfahrung bei der SSB AG (SAP4SSB) und den 12-monatigen Rechenzentrumsbetrieb bei Datacenter One (ITIL 4) zu einem hochgradig vernetzten **Local RAG Data Lake**.

---

## 🧭 Die 5 Kernsäulen des Wissensnetzes

```mermaid
graph TD
    ROOT["🧠 Master Knowledge Hub (Visar Murseli)"]
    ROOT --> P0["00_Aktuelle_Bewerbungsunterlagen"]
    ROOT --> P1["01_SSB (24 Monate S/4HANA Transformation)"]
    ROOT --> P2["02_Master (120 ECTS | Note 1,6 | Thesis 1,0)"]
    ROOT --> P3["03_Bachelor (180 ECTS | Note 3,0 | Thesis 1,7)"]
    ROOT --> P4["04_DC1 (12 Monate ITIL 4 INOC Leitstand)"]
```

---

## 📂 1. Säule 00: Aktuelle Bewerbungsunterlagen & Karriere
- [[01_Karriere_Bewerbungen/00_Lebenslauf_Volltext|📄 Master-Lebenslauf Volltext & Stationen]]
- [[01_Karriere_Bewerbungen/00_Masterzeugnis_Leistungsuebersicht_Volltext|🎓 Amtliches Masterzeugnis (120 ECTS | Gesamtnote 1,6)]]
- [[01_Karriere_Bewerbungen/00_Bachelorzeugnis_Leistungsuebersicht_Volltext|🏛️ Amtliche Bachelor-Leistungsübersicht (180 ECTS | Gesamtnote 3,0)]]
- [[01_Karriere_Bewerbungen/00_Bewerbungsmanagement_Cockpit|📊 Bewerbungsmanagement Cockpit & Pipeline-Historie]]
- [[01_Karriere_Bewerbungen/Target_Roles|🎯 Zielrollen: Junior SAP Consultant & Traineeprogramme]]

---

## 🚄 2. Säule 01: SSB S/4HANA Großprojekt (SAP4SSB | 24 Monate)
- [[03_SAP_EnterpriseArchitecture/SSB_Solution_Design_Volltext|📐 Solution Design Document (SDD) Volltext (794 Absätze)]]
- [[03_SAP_EnterpriseArchitecture/SSB_Migration_Volltext|🔄 Datenmigrationskonzept (LTMC & CVI Saldo 0,00 €) Volltext]]
- [[03_SAP_EnterpriseArchitecture/SSB_Interviews_Experten_Transkripte|🎙️ 4 Experten-Interviews Transkripte (Nowak, Wimpff, Heinrich, Gerdes)]]
- [[03_SAP_EnterpriseArchitecture/SSB_Tool_Governance_CALM_EnableNow_Volltext|🛠️ Tool-Governance: CALM Quickguide, Spielregeln & Enable Now Übergabe]]
- [[03_SAP_EnterpriseArchitecture/SSB_Mitbestimmung_Betriebsrat_Dossier|🏛️ Betriebsrat-Governance & Modulbeschreibungen (§ 87 BetrVG)]]
- [[03_SAP_EnterpriseArchitecture/SSB_Grossprojekt_SAP4SSB|🚆 Programm-Übersicht TP1–TP5 & Meilensteine]]
- [[03_SAP_EnterpriseArchitecture/01_Architektur_Technik/Clean_Core_Paradigma|⭐ Clean Core Paradigma & BTP Entkopplung]]
- [[03_SAP_EnterpriseArchitecture/02_Kaufmaennische_Prozesse/Trennungsrechnung_OEPNV_EU1370|💶 Trennungsrechnung im ÖPNV (EU-VO 1370/2007)]]
- [[03_SAP_EnterpriseArchitecture/02_Kaufmaennische_Prozesse/Universal_Journal_ACDOCA|📑 Universal Journal (ACDOCA) & Single Source of Truth]]
- [[03_SAP_EnterpriseArchitecture/00_MOCs/MOC_SSB_Transformation|🗺️ MOC SSB Transformation Gesamtatlas]]

---

## 🎓 3. Säule 02: Masterstudium (120 ECTS | Gesamtnote 1,6 | Uni Stuttgart)
- [[02_Wirtschaftsinformatik_300ECTS/Modul_Masterarbeit|⭐ Masterarbeit: Kritische Erfolgsfaktoren der ERP-Plattformisierung (Note 1,0 | 126 Seiten)]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_Digitale_Nachhaltigkeit|🌱 Digitale Nachhaltigkeit: Fallstudie J. Schmalz GmbH (CSRD-Abfallbilanz | Note 1,0)]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_FPWI|⚡ FPWI: Smart Service Blueprinting für IoT (DSRM, SUS 85/100 | Note 1,3)]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_Advanced_Software_Engineering|💻 Advanced Software Engineering: Domain-Driven Design & Enterprise CI/CD (Note 1,6)]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_Seminar_WI2|🤖 Seminar WI 2: Mensch-Roboter-Kollaboration in Industrie 5.0 (PRISMA SLR | Note 1,7)]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_Software_Architektur|🏛️ Software-Architektur: Microservices, Event-Driven & Markov-Analyse (Note 1,7)]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_Innovationsmanagement|💡 Innovationsmanagement: Technologiediffusion & Plattform-Ökosysteme (Note 1,7)]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_TEUI|🌍 Theorie und Empirie internationaler Unternehmenstätigkeit (Note 1,7)]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_Applied_AI|🧠 Applied AI and Upcoming Technologies in Industries (Note 1,7)]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_AI4IoT|📡 AI4IoT: Sensor-Datenströme & Edge AI im Maschinenbau (Note 2,0)]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_Cloud_Computing|☁️ Cloud Computing: Serverless Architektur auf AWS (Note 2,0)]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_ISG|📦 Innovationsmethoden (ISG): Digital Venture PatentRadar für Klingele (Note 2,0)]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_Datenbanken|💾 Datenbanken und Informationssysteme: Relationale Modelle & Transaktionen (Note 2,7)]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_Management_IT_Unternehmen|📈 Management von IT-Unternehmen: COBIT, ITIL & IT-Kostenrechnung (Note 3,0)]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_SOM|🔄 Service Operations Management: Warteschlangentheorie & Durchsatz (Note 3,0)]]

---

## 🏛️ 4. Säule 03: Bachelorstudium (180 ECTS | Gesamtnote 3,0 | Uni Stuttgart)
- [[02_Wirtschaftsinformatik_300ECTS/Modul_Bachelorarbeit|📜 Bachelorarbeit: Boundary Resources in Low-Code Plattformen OutSystems & Mendix (Note 1,7 | 103 Seiten)]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_EBusiness|🛒 Informationssysteme im E-Business (Bestnote 1,0 | B2B & E-Procurement)]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_Informationsverarbeitungspraktikum|📊 IVP: Quantitative Unternehmensanalyse 0x539-Wear GmbH (Deckungsbeitragsrechnung | Note 2,3)]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_Modellierung|📐 Modellierung: BPMN 2.0, UML, Petrinetze, Relationale Algebra & Normalformen (Note 2,3)]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_TOGAF_Scape|🏛️ TOGAF 9 ADM Zertifizierung bei Scape Consulting (Dr. Daniel Simon, 16.01.2020)]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_Softwarepraktikum|💻 Softwarepraktikum (SOPRA): taskMasterPro 3 in Java (Note 3,0)]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_DSA|🌲 Datenstrukturen und Algorithmen (DSA): Bäume, Graphen, O-Notation (Note 3,0)]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_GBWL1|📚 GBWL 1: Strukturen der BWL & Rechnungslegung (Buchführung, GuV, Bilanz)]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_GBWL4|💰 GBWL 4: Finanzprozess (Investition & Finanzierung, Kapitalwertmethode)]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_GVWL1|📉 GVWL 1: Märkte & Entscheidungen (Mikroökonomik, Marktformen)]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_Informatikrecht|⚖️ Informatikrecht: DSGVO, Softwarevertragsrecht, Urheberrecht (Note 4,0)]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_PSE|☕ Programmierung und Softwareentwicklung (PSE): Java OOP (Note 4,0)]]
- [[02_Wirtschaftsinformatik_300ECTS/Modul_Übersicht|📋 Gesamtübersicht aller 300 ECTS Bachelor- und Masterprüfungen]]

---

## 🏢 5. Säule 04: Datacenter One (DC1 | 12 Monate ITIL 4 Service Operations)
- [[03_SAP_EnterpriseArchitecture/DC1_ITIL4_Service_Operations|🏢 DC1: 24/7 Leitstand, SPoC, PRTG-Monitoring & Confluence SOPs]]
- [[03_SAP_EnterpriseArchitecture/DC1_Hardware_Lifecycle_Management|💻 DC1: Hardware Lifecycle Management (HLM) & Rollout-Prozess in Visio]]

---

## 🎙️ 6. Interview-Masterclass & STAR-Stories
- [[03_SAP_EnterpriseArchitecture/SSB_Interview_Stories_STAR|🌟 5 unschlagbare STAR-Stories aus der Praxis]]
- [[01_Karriere_Bewerbungen/Aktuelle_Bewerbungsunterlagen|📂 Verbindliches Dokumenten-Register]]
"""
    write_vault_note("00_INDEX.md", note_master_index)

if __name__ == "__main__":
    run_dc1_and_index_extraction()
