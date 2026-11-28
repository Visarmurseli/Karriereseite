import os

vault_root = r"C:\Users\SHQIPTAR634\Documents\Obsidian Vault"
zettel_dir = os.path.join(vault_root, "04_Second_Brain_Zettelkasten")
sap_dir = os.path.join(vault_root, "03_SAP_EnterpriseArchitecture")
os.makedirs(zettel_dir, exist_ok=True)
os.makedirs(sap_dir, exist_ok=True)

concept_cards = [
    (zettel_dir, "Software_Engineering_Prinzipien.md", """---
title: "Software Engineering Prinzipien"
category: "Software Engineering"
tags:
  - zettelkasten
  - clean_code
  - software_architecture
---

# 💻 Software Engineering Prinzipien

> [!SUMMARY] **Fundamentale Entwurfs- und Architekturprinzipien**
> Kernprinzipien für wartbare, skalierbare und robuste Enterprise-Systeme aus den Modulen [[02_Wirtschaftsinformatik_300ECTS/Modul_Advanced_Software_Engineering|ASE]], [[02_Wirtschaftsinformatik_300ECTS/Modul_Software_Architektur|Software-Architektur]] und [[02_Wirtschaftsinformatik_300ECTS/Modul_EST|EST]].

## 1. SOLID-Prinzipien
- **Single Responsibility Principle (SRP):** Eine Klasse hat nur eine Verantwortlichkeit.
- **Open/Closed Principle (OCP):** Offen für Erweiterungen, geschlossen für Modifikationen.
- **Liskov Substitution Principle (LSP):** Subtypen müssen durch Basistypen austauschbar sein.
- **Interface Segregation Principle (ISP):** Schlanke, fachspezifische Interfaces.
- **Dependency Inversion Principle (DIP):** Abhängigkeit von Abstraktionen, nicht von Konkretisierungen.

## 2. Bezug zur Clean Core Strategie
Im ERP-Umfeld spiegelt sich das Dependency Inversion Principle direkt im **SAP Clean Core Paradigma** wider: Statt Modifikationen im Core vorzunehmen, werden Erweiterungen über definierte Remote-APIs auf der SAP BTP entkoppelt.
"""),
    (zettel_dir, "IoT_Architekturen.md", """---
title: "IoT-Architekturen & OT-IT-Konvergenz"
category: "IoT & Embedded AI"
tags:
  - iot
  - edge_computing
  - digitaler_zwilling
---

# 📡 IoT-Architekturen & OT-IT-Konvergenz

> [!SUMMARY] **Konvergenz industrieller Systeme**
> Systemarchitektur zur Erfassung, Aggregation und Auswertung industrieller Sensordatenströme aus [[02_Wirtschaftsinformatik_300ECTS/Modul_AI4IoT|AI4IoT]] und [[02_Wirtschaftsinformatik_300ECTS/Modul_SmartCities|Smart Cities]].

## 1. Schichtenarchitektur im IoT
1. **Sensorebene (Shopfloor / OT):** SPS, Feldbusse, Wearables, LoRaWAN, MQTT.
2. **Edge-Ebene:** Vorfilterung, lokale Inferenz (Edge AI), Protokollübersetzung.
3. **Plattformebene:** Zeitreihendatenbanken, Digitale Zwillinge (Asset Administration Shell).
4. **Applikationsebene:** ERP-Integration (z.B. SAP PM Instandhaltung bei SSB), Dashboarding.
"""),
    (zettel_dir, "Generative_AI_LLM.md", """---
title: "Generative AI & Large Language Models im Enterprise-Kontext"
category: "Artificial Intelligence"
tags:
  - ai
  - llm
  - rag
---

# 🧠 Generative AI & LLMs im Enterprise-Kontext

> [!SUMMARY] **Einsatzpotenziale & Architekturen generativer KI**
> Grundlagen aus [[02_Wirtschaftsinformatik_300ECTS/Modul_Applied_AI|Applied AI]], [[02_Wirtschaftsinformatik_300ECTS/Modul_Seminar_Interdisziplinaer|Seminar ML]] und [[02_Wirtschaftsinformatik_300ECTS/Modul_Wissensverarbeitung|Wissensverarbeitung]].

## 1. Retrieval-Augmented Generation (RAG)
Verbindung vortrainierter Sprachmodelle mit firmeneigenen Wissensdatenbanken (wie diesem Obsidian Second Brain Vault) zur Generierung faktentreuer, quellenbelegter Antworten.

## 2. Relevanz für ERP & IT-Service
- Automatisierte Ticketklassifikation (z.B. Jira im DC1 INOC).
- Intelligente Assistenz in SAP S/4HANA (SAP Joule).
"""),
    (zettel_dir, "SQL_und_Datenmodellierung.md", """---
title: "SQL & Fortgeschrittene Datenmodellierung"
category: "Databases"
tags:
  - sql
  - datenbanken
  - normalisierung
---

# 💾 SQL & Fortgeschrittene Datenmodellierung

> [!SUMMARY] **Relationale und analytische Datenstrukturen**
> Grundlagen aus [[02_Wirtschaftsinformatik_300ECTS/Modul_Datenbanken|DBIS]], [[02_Wirtschaftsinformatik_300ECTS/Modul_Modellierung|Modellierung]] und [[02_Wirtschaftsinformatik_300ECTS/Modul_Informationsmanagement_Bachelor|Informationsmanagement/BI]].

## 1. Normalformenlehre (1NF – BCNF)
- **1NF:** Atomare Wertebereiche.
- **2NF:** Keine partiellen funktionalen Abhängigkeiten von Schlüsselkandidaten.
- **3NF:** Keine transitiven Abhängigkeiten von Nicht-Schlüsselattributen.

## 2. Brücke zu SAP HANA
In SAP HANA (In-Memory Column-Store) wird durch Spaltenkompression und extreme Aggregationsleistung auf viele historische Aggregattabellen verzichtet (Single Source of Truth im [[03_SAP_EnterpriseArchitecture/02_Kaufmaennische_Prozesse/Universal_Journal_ACDOCA|ACDOCA]]).
"""),
    (zettel_dir, "Algorithmen_und_Datenstrukturen.md", """---
title: "Algorithmen und Datenstrukturen (Konzepte)"
category: "Computer Science"
tags:
  - algorithms
  - datastructures
  - complexity
---

# 🌲 Algorithmen und Datenstrukturen

> [!SUMMARY] **Effiziente Algorithmen & Komplexität**
> Aus [[02_Wirtschaftsinformatik_300ECTS/Modul_DSA|DSA]] und [[02_Wirtschaftsinformatik_300ECTS/Modul_Programmentwicklung|Programmentwicklung]].

- **Asymptotische Analyse:** O-Notation, Omega-, Theta-Schranken.
- **Baumstrukturen:** Binäre Suchbäume, AVL-Bäume, B-Bäume (wichtig für DB-Indizes).
- **Graphenalgorithmen:** Dijkstra (kürzeste Wege im ÖPNV-Netz), Spannbäume (Kruskal, Prim).
"""),
    (zettel_dir, "E_Business_Konzepte.md", """---
title: "E-Business Konzepte & Plattformökonomie"
category: "Wirtschaftsinformatik"
tags:
  - ebusiness
  - platform_economy
  - b2b
---

# 🛒 E-Business Konzepte & Plattformökonomie

> [!SUMMARY] **Elektronische Märkte und Plattformen**
> Aus [[02_Wirtschaftsinformatik_300ECTS/Modul_EBusiness|E-Business (Note 1,0)]] und [[02_Wirtschaftsinformatik_300ECTS/Modul_Bachelorarbeit|Bachelorarbeit (Note 1,7)]].

- **Elektronische Marktplätze:** 1:1, 1:n, n:m Beziehungen.
- **EDI & Standards:** EDIFACT, XML, RESTful Web Services.
- **Plattformisierung:** Boundary Resources zur Aktivierung externer Entwickler.
"""),
    (zettel_dir, "Wissenschaftliche_Methodik.md", """---
title: "Wissenschaftliche Methodik & Forschungsdesigns"
category: "Research Methodology"
tags:
  - research
  - dsrm
  - slr
---

# 📚 Wissenschaftliche Methodik & Forschungsdesigns

> [!SUMMARY] **Methodische Werkzeuge der Wirtschaftsinformatik**
> Aus [[02_Wirtschaftsinformatik_300ECTS/Modul_Forschungsmethoden|Forschungsmethoden]], [[02_Wirtschaftsinformatik_300ECTS/Modul_Seminar_WI2|Seminar WI 2]] und [[02_Wirtschaftsinformatik_300ECTS/Modul_Masterarbeit|Masterarbeit]].

- **Design Science Research (DSR nach Peffers et al. 2007):** Problem identification, objectives, design, demonstration, evaluation, communication.
- **Qualitative Inhaltsanalyse nach Mayring (2015):** Deduktiv-induktives Kategoriensystem, Paraphrasierung, Generalisierung, Reduktion.
- **Systematic Literature Review (SLR nach vom Brocke et al. 2009 / PRISMA):** Protokollgestützte Literaturselektion.
"""),
    (sap_dir, "Enterprise_Architecture_Overview.md", """---
title: "Enterprise Architecture Management (EAM) Übersicht"
category: "Enterprise Architecture"
tags:
  - eam
  - togaf
  - sap
---

# 🏛️ Enterprise Architecture Management (EAM) Übersicht

> [!SUMMARY] **EAM-Methoden und Praxistransfer**
> Verbindung aus [[02_Wirtschaftsinformatik_300ECTS/Modul_TOGAF_Scape|TOGAF 9 ADM]] und 24 Monaten SSB S/4HANA Transformation.

- **TOGAF Architecture Development Method (ADM):** Von Preliminary Phase über Architecture Vision (Phase A), Business (B), Information Systems (C), Technology (D) bis Transition Planning (Phase E & F).
- **Alignment von Business & IT:** Abbildung in SAP Signavio (Prozesse) und SAP Cloud ALM (Solution Architecture).
"""),
    (sap_dir, "HANA_Datenbank.md", """---
title: "SAP HANA In-Memory Datenbankarchitektur"
category: "SAP Architecture"
tags:
  - sap_hana
  - in_memory
  - columnar
---

# ⚡ SAP HANA In-Memory Datenbankarchitektur

> [!SUMMARY] **Technologische Basis von SAP S/4HANA**
> Verknüpft [[02_Wirtschaftsinformatik_300ECTS/Modul_Datenbanken|DBIS]] mit der [[03_SAP_EnterpriseArchitecture/SSB_Solution_Design_Volltext|SSB S/4HANA Transformation]].

- **Columnar Storage:** Spaltenorientierte Speicherung für maximale Kompression und blitzschnelle Aggregationen.
- **OLTP + OLAP Konvergenz:** Wegfall redundanter Aggregat- und Sekundärindextabellen.
- **Universal Journal (ACDOCA):** Zusammenführung von Finanzbuchhaltung (FI) und Controlling (CO) in einer einzigen Tabelle.
""")
]

for folder, fname, content in concept_cards:
    fpath = os.path.join(folder, fname)
    if not os.path.exists(fpath):
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        print(f"Created: {fname}")
    else:
        print(f"Exists: {fname}")
