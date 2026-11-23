import os
import sys
import re
import glob
import hashlib
import zipfile
import xml.etree.ElementTree as ET
import time
import pypdf

ROOT_DIR = r"c:\Users\SHQIPTAR634\Desktop\SSB Dateien"
VAULT_DIR = r"C:\Users\SHQIPTAR634\Documents\Obsidian Vault\02_Wirtschaftsinformatik_300ECTS"

# 1. Slide Extraction Helpers
def get_file_md5(filepath):
    h = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(16384):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None

def extract_pdf_slides(pdf_path, max_pages=150):
    slides = []
    try:
        reader = pypdf.PdfReader(pdf_path)
        total_p = len(reader.pages)
        limit = min(total_p, max_pages)
        for i in range(limit):
            try:
                page = reader.pages[i]
                text = page.extract_text() or ""
                # Clean whitespace
                clean = re.sub(r"[ \t]+", " ", text).strip()
                clean = re.sub(r"(\r?\n\s*){2,}", "\n", clean)
                # Filter out pure noise / page-only
                lines = [l.strip() for l in clean.split("\n") if l.strip()]
                if len(lines) > 0 and len(" ".join(lines)) > 15:
                    slides.append((i + 1, clean))
            except Exception:
                continue
    except Exception as e:
        print(f"    [WARN] PDF Error {os.path.basename(pdf_path)}: {e}")
    return slides

def extract_pptx_slides(pptx_path):
    slides = []
    try:
        with zipfile.ZipFile(pptx_path, "r") as z:
            slide_entries = [n for n in z.namelist() if n.startswith("ppt/slides/slide") and n.endswith(".xml")]
            def s_num(n):
                m = re.search(r"slide(\d+)\.xml", n)
                return int(m.group(1)) if m else 9999
            slide_entries.sort(key=s_num)
            for i, s_name in enumerate(slide_entries):
                xml_data = z.read(s_name)
                tree = ET.fromstring(xml_data)
                texts = [node.text for node in tree.iter() if node.text and node.tag.endswith("}t")]
                combined = " ".join(texts).strip()
                clean = re.sub(r"\s+", " ", combined)
                if len(clean) > 15:
                    slides.append((i + 1, clean))
    except Exception as e:
        print(f"    [WARN] PPTX Error {os.path.basename(pptx_path)}: {e}")
    return slides

def extract_deck(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".pdf":
        return extract_pdf_slides(filepath)
    elif ext == ".pptx":
        return extract_pptx_slides(filepath)
    return []

# 2. Module Registry
MODULES = [
    # --- MASTER MODULES ---
    {
        "file": "Modul_AI4IoT.md",
        "title": "AI4IoT – Artificial Intelligence for the Internet of Things",
        "degree": "Master of Science",
        "modul_code": "107250",
        "ects": "6,0",
        "grade": "2,0",
        "prof": "Prof. Dr. Heiko Lachenmaier / Prof. Dr. Georg Herzwurm",
        "rel_dirs": [r"02_Master\AI4IoT – Artificial Intelligence for the Internet of Things\01_Vorlesungsunterlagen"],
        "skip_patterns": ["Lasi_Digital_Playbook"],
        "desc": "Konvergenz von Operational Technology (OT), Information Technology (IT) und Internet of Things (IoT). Fallstudie Bademeister, Sensornetzwerke, Edge AI, Trustworthy IoT und Verfassung eines wissenschaftlichen Shortpapers.",
        "skills": ["OT-IT-IoT Konvergenz", "Edge Computing & Edge AI", "Wearable Sensorik", "Trustworthy IoT", "Wissenschaftliches Poster & Shortpaper"]
    },
    {
        "file": "Modul_Advanced_Software_Engineering.md",
        "title": "Advanced Software Engineering (ASE)",
        "degree": "Master of Science",
        "modul_code": "10040",
        "ects": "6,0",
        "grade": "1,6",
        "prof": "Prof. Dr. Steffen Becker (Institut für Softwaretechnologie)",
        "rel_dirs": [r"02_Master\Advanced Software Engineering\01_Vorlesungsfolien"],
        "skip_patterns": [],
        "desc": "Fortgeschrittene Methoden des Software-Engineerings: Modellgetriebene Entwicklung (MDD/MDE), Software-Produktlinien (SPL), Architekturbewertung, Metamodellierung (EMF/Ecore) und Continuous Delivery.",
        "skills": ["Modellgetriebene Softwareentwicklung (MDD)", "Software-Produktlinien (SPL)", "EMF & Metamodellierung", "Architekturanalyse & Metriken", "Domain-Specific Languages (DSL)"]
    },
    {
        "file": "Modul_Applied_AI.md",
        "title": "Applied AI and Upcoming Technologies in Industries",
        "degree": "Master of Science",
        "modul_code": "107260",
        "ects": "6,0",
        "grade": "1,7",
        "prof": "Lehrstuhl für ABWL und Wirtschaftsinformatik II",
        "rel_dirs": [r"02_Master\Applied AI and Upcoming Technologies in Industries\01_Vorlesungsunterlagen"],
        "skip_patterns": [],
        "desc": "Industrielle Anwendung von KI, Deep Learning Architekturen, Computer Vision, NLP und Entwicklung des Prototyps Yarro (KI-basierte Dokumentenanalyse).",
        "skills": ["Industrial AI Architekturen", "Computer Vision & NLP Pipelines", "Prototyping & Business Value von KI", "Prompt Engineering & RAG Grundlagen"]
    },
    {
        "file": "Modul_Datenbanken.md",
        "title": "Datenbanken und Informationssysteme (DBIS)",
        "degree": "Master of Science",
        "modul_code": "10080",
        "ects": "6,0",
        "grade": "2,7",
        "prof": "Prof. Dr. Bernhard Mitschang (Institut für Parallele und Verteilte Systeme)",
        "rel_dirs": [r"02_Master\Datenbanken und Informationssysteme\01_Vorlesungsunterlagen"],
        "skip_patterns": [],
        "desc": "Relationale Datenmodellierung (ER-Modelle, Normalformen 1NF–BCNF), SQL (DDL, DML, DQL), Physische Speicherstrukturen, B-Bäume, Hashing, Transaktionsverwaltung (ACID), Mehrbenutzersynchronisation (2PL) und Recovery-Mechanismen.",
        "skills": ["Relationales Datenbankdesign", "Fortgeschrittenes SQL", "Normalisierung (1NF-3NF, BCNF)", "Transaktionsmanagement (ACID)", "Indexierung & Performanz"]
    },
    {
        "file": "Modul_Digitale_Nachhaltigkeit.md",
        "title": "Digitale Nachhaltigkeit",
        "degree": "Master of Science",
        "modul_code": "107270",
        "ects": "6,0",
        "grade": "1,0",
        "prof": "Dr. Dimitri Petrik / Prof. Dr. Georg Herzwurm",
        "rel_dirs": [r"02_Master\Digitale Nachhaltigkeit\01_Vorlesung_und_Uebungen"],
        "skip_patterns": [],
        "desc": "Nachhaltigkeit durch Digitalisierung (Green through IT) und nachhaltige IT-Infrastrukturen (Green in IT). ESG-Reporting (CSRD, GHG Protocol Scope 1-3), Circular Economy, Life Cycle Assessment (LCA) und Digital Product Passports.",
        "skills": ["Green through IT & Green in IT", "Corporate Sustainability Reporting (CSRD)", "GHG Protocol (Scope 1, 2, 3)", "Life Cycle Assessment (LCA)", "Circular Economy Geschäftsmodelle"]
    },
    {
        "file": "Modul_Forschungsmethoden.md",
        "title": "Forschungsmethoden in der Wirtschaftsinformatik",
        "degree": "Master of Science",
        "modul_code": "107280",
        "ects": "6,0",
        "grade": "1,7",
        "prof": "Lehrstuhl für ABWL und Wirtschaftsinformatik II",
        "rel_dirs": [r"02_Master\Forschungsmethoden in der Wirtschaftsinformatik\01_Vorlesungsfolien"],
        "skip_patterns": [],
        "desc": "Wissenschaftstheorie, quantitative und qualitative Forschungsmethoden, Design Science Research (DSR nach Peffers), strukturierte Literaturanalysen (Vom Brocke) und empirische Datenerhebung.",
        "skills": ["Design Science Research (DSR)", "Systematische Literaturanalyse (SLR)", "Qualitative Inhaltsanalyse (Mayring)", "Empirisches Forschungsdesign", "Wissenschaftliches Publizieren"]
    },
    {
        "file": "Modul_Innovationsmanagement.md",
        "title": "Innovationsmanagement",
        "degree": "Master of Science",
        "modul_code": "107290",
        "ects": "6,0",
        "grade": "1,7",
        "prof": "Lehrstuhl für Innovations- und Dienstleistungsmanagement",
        "rel_dirs": [r"02_Master\Innovationsmanagement\01_Vorlesungsunterlagen"],
        "skip_patterns": [],
        "desc": "Strategisches Innovationsmanagement: Technologiefrüherkennung, Patentanalyse, Quality Function Deployment (House of Quality), Szenarioanalyse und Standardisierungsstrategien.",
        "skills": ["Technologiediffusion & S-Kurven", "Patentanalyse & Bewertung", "Quality Function Deployment (QFD)", "Szenarioanalyse", "Standardisierung & Netzwerkeffekte"]
    },
    {
        "file": "Modul_ISG.md",
        "title": "Innovationsmethoden für software- und datenintensive Geschäftsmodelle",
        "degree": "Master of Science",
        "modul_code": "107300",
        "ects": "6,0",
        "grade": "2,0",
        "prof": "Lehrstuhl für ABWL und Wirtschaftsinformatik II",
        "rel_dirs": [r"02_Master\Innovationsmethoden für software- und datenintensive Geschäftsmodelle\01_Vorlesung_und_Grundlagen"],
        "skip_patterns": [],
        "desc": "Methoden zur Entwicklung digitaler Geschäftsmodelle: Business Model Canvas, Value Proposition Design, Plattform-Ökosysteme, PatentRadar-Projekt für die Klingele Paper & Packaging Gruppe.",
        "skills": ["Business Model Canvas & Platformization", "Lean Startup & Customer Development", "Design Thinking für Enterprise AI", "Value Proposition Design", "Pitch Deck & Venture Evaluation"]
    },
    {
        "file": "Modul_Management_IT_Unternehmen.md",
        "title": "Management von IT-Unternehmen",
        "degree": "Master of Science",
        "modul_code": "107310",
        "ects": "6,0",
        "grade": "3,0",
        "prof": "Lehrstuhl für ABWL und Wirtschaftsinformatik II",
        "rel_dirs": [r"02_Master\Management von IT-Unternehmen\01_Vorlesungsfolien"],
        "skip_patterns": [],
        "desc": "Strategische Führung von Software- und IT-Unternehmen: Geschäftsmodelle (SaaS, On-Premise, Open Source), Go-to-Market, Vertriebskanäle, Pricing-Modelle und Skalierungsstrategien.",
        "skills": ["IT-Geschäftsmodell-Typologien", "Software Pricing & Monetarisierung", "Partnerökosysteme & Channel Management", "IT-Unternehmensbewertung", "Skalierungs- und Wachstumsstrategien"]
    },
    {
        "file": "Modul_Cloud_Computing.md",
        "title": "Service Management and Cloud Computing, and Evaluation",
        "degree": "Master of Science",
        "modul_code": "107320",
        "ects": "6,0",
        "grade": "2,0",
        "prof": "Lehrstuhl für ABWL und Wirtschaftsinformatik II",
        "rel_dirs": [r"02_Master\Service Management and Cloud Computing, and Evaluation\01_Vorlesungsunterlagen"],
        "skip_patterns": [],
        "desc": "Cloud-Service-Modelle (IaaS, PaaS, SaaS), Cloud-Architekturen, SLA-Management, Multi-Cloud-Governance, FinOps und Evaluation von Hyperscalern (AWS, Azure, GCP, SAP BTP).",
        "skills": ["Cloud Architecture Patterns", "IaaS, PaaS, SaaS Servicemodelle", "SLA & Availability Management", "Cloud FinOps & Cost Optimization", "Multi-Cloud Governance & Compliance"]
    },
    {
        "file": "Modul_SOM.md",
        "title": "Service Operations Management (SOM)",
        "degree": "Master of Science",
        "modul_code": "107330",
        "ects": "6,0",
        "grade": "3,0",
        "prof": "Lehrstuhl für Innovations- und Dienstleistungsmanagement",
        "rel_dirs": [r"02_Master\Service Operations Management\01_Vorlesungsunterlagen"],
        "skip_patterns": [],
        "desc": "Operatives Dienstleistungsmanagement: Kapazitäts- und Nachfragesteuerung im Servicebereich, Warteschlangentheorie, Service Blueprinting, Servicequalitätsmessung (SERVQUAL) und Yield Management.",
        "skills": ["Service Blueprinting & Prozessdesign", "Warteschlangentheorie (Queuing Models)", "Yield Management & Kapazitätssteuerung", "Servicequalitätsmessung (SERVQUAL)", "Customer Journey Mapping"]
    },
    {
        "file": "Modul_Software_Architektur.md",
        "title": "Software-Architektur (QASD)",
        "degree": "Master of Science",
        "modul_code": "10050",
        "ects": "6,0",
        "grade": "1,7",
        "prof": "Prof. Dr. Steffen Becker (Institut für Softwaretechnologie)",
        "rel_dirs": [r"02_Master\Software-Architektur\01_Vorlesungsfolien"],
        "skip_patterns": [],
        "desc": "Qualitätsgetriebene Software-Architektur (Quality-Aware Software Design): Architekturstile, Microservices, Event-Driven Architecture, Nicht-funktionale Anforderungen (ISO 25010), ATAM (Architecture Tradeoff Analysis Method) und Palladio Component Model.",
        "skills": ["Architekturmuster (Microservices, Event-Driven)", "Qualitätsmodellierung (ISO 25010)", "Architecture Tradeoff Analysis (ATAM)", "Palladio Component Model (PCM)", "Clean Architecture & Entkopplung"]
    },
    {
        "file": "Modul_TEUI.md",
        "title": "Theorie und Empirie internationaler Unternehmenstätigkeit",
        "degree": "Master of Science",
        "modul_code": "107340",
        "ects": "6,0",
        "grade": "1,7",
        "prof": "Prof. Dr. Michael-Jörg Oesterle",
        "rel_dirs": [r"02_Master\Theorie und Empirie internationaler Unternehmenstätigkeit\01_Vorlesungsskript_und_Folien"],
        "skip_patterns": [],
        "desc": "Internationales Management: Theorien der multinationalen Unternehmung (OLI-Paradigma nach Dunning, Internalisierungstheorie), Internationalisierungsstrategien, Markteintrittsmodi, globale Wertschöpfungsketten und kulturelle Distanz (Hofstede).",
        "skills": ["OLI-Paradigma (Eclectic Paradigm)", "Markteintrittsstrategien & Allianzen", "Globale Wertschöpfungsketten", "Transaktionskostentheorie", "Kulturdimensionen & Governance"]
    },
    {
        "file": "Modul_AIM.md",
        "title": "Advanced Information Management (AIM)",
        "degree": "Master of Science (Zusatzmodul)",
        "modul_code": "xZusatz_AIM",
        "ects": "6,0",
        "grade": "Zusatzmodul",
        "prof": "Universität Stuttgart",
        "rel_dirs": [r"02_Master\xZusatz_Advanced Information Management (AIM)\01_Lecture_Slides"],
        "skip_patterns": [],
        "desc": "Fortgeschrittenes Informationsmanagement: Data Governance, Data Mesh Architekturen, Informationslebenszyklus, Master Data Management (MDM) und strategische Informationssystemplanung.",
        "skills": ["Strategic Information Systems Planning", "Master Data Management (MDM)", "Data Governance Frameworks", "Data Mesh & Data Fabric", "Enterprise Content Management"]
    },
    {
        "file": "Modul_Quanteninformatik.md",
        "title": "Grundlagen der Quanteninformatik",
        "degree": "Master of Science (Zusatzmodul)",
        "modul_code": "xZusatz_QI",
        "ects": "Zusatzmodul",
        "grade": "Zusatzmodul",
        "prof": "Universität Stuttgart",
        "rel_dirs": [r"02_Master\xZusatz_nice2have-Grundlagen der Quanteninformatik\01_Vorlesungsfolien"],
        "skip_patterns": [],
        "desc": "Grundlagen des Quantum Computing: Qubits, Superposition, Verschränkung, Quantengatter, Quantenalgorithmen (Deutsch-Jozsa, Grover, Shor) und Quantenkryptographie (BB84).",
        "skills": ["Qubit-Zustandsräume & Bloch-Kugel", "Quantengatter & Schaltkreise", "Quantenverschränkung & Teleportation", "Grover- und Shor-Algorithmen", "Post-Quantum-Kryptographie Grundlagen"]
    },
    {
        "file": "Modul_SmartCities.md",
        "title": "Smart Cities and Internet of Things",
        "degree": "Master of Science (Zusatzmodul)",
        "modul_code": "xZusatz_SmartCities",
        "ects": "Zusatzmodul",
        "grade": "Zusatzmodul",
        "prof": "Universität Stuttgart",
        "rel_dirs": [r"02_Master\xZusatz_nice2have-Smart Cities and Internet of Things\01_Lecture_Slides"],
        "skip_patterns": [],
        "desc": "Urbane IoT-Architekturen: Sensornetzwerke, Smart Mobility, intelligente Energienetze (Smart Grids), urbane Datenplattformen und datengestützte Stadtentwicklung.",
        "skills": ["Urbane IoT-Architekturen", "Smart Mobility & ÖPNV-Vernetzung", "Smart Grid Datenmodelle", "Urbane Datenplattformen (FIWARE)", "Sensorik & Funkprotokolle (LoRaWAN)"]
    },

    # --- BACHELOR MODULES ---
    {
        "file": "Modul_AFS.md",
        "title": "Automaten und Formale Sprachen (AFS)",
        "degree": "Bachelor of Science",
        "modul_code": "10010",
        "ects": "6,0",
        "grade": "3,7",
        "prof": "Prof. Dr. Volker Diekert (Institut für Formale Methoden der Informatik)",
        "rel_dirs": [r"03_Bachelor\Automaten und Formale Sprachen\01_Theoretische_Informatik_WS20\Vorlesung"],
        "skip_patterns": [],
        "desc": "Theoretische Informatik: Endliche Automaten (DFA, NFA), Reguläre Ausdrücke, Pumping-Lemma, Kontextfreie Grammatiken, Kellerautomaten, Turingmaschinen, Chomsky-Hierarchie, Entscheidbarkeit und das Halteproblem.",
        "skills": ["Endliche Automaten (DFA/NFA)", "Reguläre Sprachen & RegEx", "Kontextfreie Grammatiken & CYK-Algorithmus", "Turingmaschinen & Berechenbarkeit", "Chomsky-Hierarchie (Typ 0-3)"]
    },
    {
        "file": "Modul_BWL1.md",
        "title": "BWL 1: Organisation, Personalführung & Strategisches Management",
        "degree": "Bachelor of Science",
        "modul_code": "10020",
        "ects": "9,0",
        "grade": "3,3",
        "prof": "Prof. Dr. Michael-Jörg Oesterle / Prof. Dr. Birgit Renzl",
        "rel_dirs": [
            r"03_Bachelor\BWL 1 - Organisation, Personalführung, Strategisches Management\01_Strategisches_Management_WS20",
            r"03_Bachelor\BWL 1 - Organisation, Personalführung, Strategisches Management\02_Organisation_und_Personal_WS20"
        ],
        "skip_patterns": [],
        "desc": "Grundlagen der Unternehmensführung: Strategische Analyse (Porter Five Forces, Ressourcentheorie, VRIO), Organisationsstrukturen (Funktional, Divisional, Matrix), Führungstheorien, Motivationstheorien und Change Management.",
        "skills": ["Strategische Analyse (Porter 5 Forces, VRIO)", "Organisationsdesign (Matrix, Divisionen)", "Führungs- & Motivationstheorien", "Change Management Konzepte", "Corporate Governance & Stakeholder-Theorie"]
    },
    {
        "file": "Modul_EBusiness.md",
        "title": "Informationssysteme im E-Business",
        "degree": "Bachelor of Science",
        "modul_code": "10030",
        "ects": "4,5",
        "grade": "1,0",
        "prof": "Prof. Dr. Georg Herzwurm (Lehrstuhl BWI II)",
        "rel_dirs": [r"03_Bachelor\Betriebliche Informationssysteme (WI 1)\01_Informationssysteme_im_E-Business_WS19"],
        "skip_patterns": [],
        "desc": "Elektronische Geschäftsprozesse: E-Commerce-Architekturen, EDIFACT/XML-Standards, elektronische Beschaffung (E-Procurement), Plattformökonomie, Function-Point-Analyse und Bewertung von Web-Architekturen.",
        "skills": ["E-Commerce & Marktplatz-Architekturen", "Elektronischer Datenaustausch (EDI/XML)", "E-Procurement Prozesse", "Function Point Analyse (FPA)", "Plattform-Geschäftsmodelle"]
    },
    {
        "file": "Modul_MBIS.md",
        "title": "Management betrieblicher Informationssysteme (MBIS)",
        "degree": "Bachelor of Science",
        "modul_code": "10035",
        "ects": "4,5",
        "grade": "2,7",
        "prof": "Prof. Dr. Georg Herzwurm (Lehrstuhl BWI II)",
        "rel_dirs": [r"03_Bachelor\Betriebliche Informationssysteme (WI 1)\02_Management_betrieblicher_Informationssysteme_SS20"],
        "skip_patterns": [],
        "desc": "Architektur und Steuerung integrierter Standard-Unternehmenssoftware (ERP-Systeme wie SAP, SCM, CRM). Lebenszyklus betrieblicher Informationssysteme, Customizing, Systemauswahl und Einführungsstrategien.",
        "skills": ["ERP-Systemarchitekturen (SAP)", "Supply Chain Management (SCM) Systeme", "Customer Relationship Management (CRM)", "Softwareauswahl & Einführungsmethoden", "Customizing vs. Standardsoftware-Governance"]
    },
    {
        "file": "Modul_DSA.md",
        "title": "Datenstrukturen und Algorithmen (DSA)",
        "degree": "Bachelor of Science",
        "modul_code": "10045",
        "ects": "9,0",
        "grade": "3,0",
        "prof": "Prof. Dr. Stefan Funke (Institut für Formale Methoden der Informatik)",
        "rel_dirs": [r"03_Bachelor\Datenstrukturen und Algorithmen\01_Vorlesungsfolien"],
        "skip_patterns": [],
        "desc": "Grundlegende Datenstrukturen und Entwurf effizienter Algorithmen: Listen, Stacks, Queues, Binärbäume, AVL-Bäume, B-Bäume, Graphen (Dijkstra, Bellman-Ford, Kruskal, Prim), Sortieralgorithmen (Quicksort, Mergesort, Heapsort) und Komplexitätsanalyse (O-Notation).",
        "skills": ["Komplexitätsanalyse & Asymptotik (O-Notation)", "Baumstrukturen (AVL, B-Bäume)", "Graphenalgorithmen (Kürzeste Wege, Spannbäume)", "Effiziente Sortier- und Suchverfahren", "Dynamische Programmierung & Greedy"]
    },
    {
        "file": "Modul_EST.md",
        "title": "Einführung in die Softwaretechnik (EST)",
        "degree": "Bachelor of Science",
        "modul_code": "10055",
        "ects": "6,0",
        "grade": "3,7",
        "prof": "Prof. Dr. Steffen Becker (Institut für Softwaretechnologie)",
        "rel_dirs": [r"03_Bachelor\Einführung in die Softwaretechnik\02_Softwaretechnik_EST_SS18\Folien der Vorlesung"],
        "skip_patterns": [],
        "desc": "Vorgehensmodelle im Software-Lebenszyklus: Wasserfall, V-Modell, Scrum, Anforderungsanalyse (Lastenheft/Pflichtenheft), Entwurfsmuster (GoF Patterns), Softwarequalität, Testen (Unit-, Integrations-, Systemtests) und Versionskontrolle.",
        "skills": ["V-Modell & Agile Entwicklung (Scrum)", "Anforderungsanalyse & Spezifikation", "GoF Design Patterns", "Testmethoden (Unit-, Mocking, Black/White-Box)", "Software-Qualitätssicherung"]
    },
    {
        "file": "Modul_EWI.md",
        "title": "Einführung in die Wirtschaftsinformatik (EWI)",
        "degree": "Bachelor of Science",
        "modul_code": "10065",
        "ects": "6,0",
        "grade": "2,7",
        "prof": "Prof. Dr. Georg Herzwurm (Lehrstuhl BWI II)",
        "rel_dirs": [r"03_Bachelor\Einführung in die Wirtschaftsinformatik\01_Vorlesungsfolien"],
        "skip_patterns": [],
        "desc": "Fundamentale Grundlagen der Wirtschaftsinformatik: Begriff und Gegenstand, Informationslogistik, Systemtheorie, Daten- und Prozessmodellierung, Informationssysteme in Industrie und Dienstleistung, IT-Organisation und Rollenprofile.",
        "skills": ["Gegenstand & Methoden der Wirtschaftsinformatik", "Betriebliche Informationssysteme Überblick", "Prozess- und Datenmodellierung Grundlagen", "IT-Organisation & Rollenmodelle", "Wirtschaftlichkeitsanalyse von IT-Systemen"]
    },
    {
        "file": "Modul_GBWL1.md",
        "title": "GBWL 1: Strukturen der Betriebswirtschaftslehre & Rechnungslegung",
        "degree": "Bachelor of Science",
        "modul_code": "10075",
        "ects": "6,0",
        "grade": "2,7",
        "prof": "Prof. Dr. Burkhard Pedell (Institut für Betriebswirtschaftslehre)",
        "rel_dirs": [
            r"03_Bachelor\GBWL 1 - Strukturen der Betriebswirtschaftslehre\01_Einfuehrung_BWL_WS17",
            r"03_Bachelor\GBWL 1 - Strukturen der Betriebswirtschaftslehre\02_Einfuehrung_Rechnungswesen_WS17"
        ],
        "skip_patterns": [],
        "desc": "Grundlagen der BWL und des betrieblichen Rechnungswesens: Rechtsformen, Standortwahl, doppelte Buchführung, Bilanzierung nach HGB, Gewinn- und Verlustrechnung (GuV), Kosten- und Leistungsrechnung (KLR) sowie Deckungsbeitragsrechnung.",
        "skills": ["Doppelte Buchführung & Buchungssätze", "Bilanzierung & GuV nach HGB", "Kostenarten-, Kostenstellen-, Kostenträgerrechnung", "Deckungsbeitragsrechnung", "Rechtsformen & Unternehmensverfassungen"]
    },
    {
        "file": "Modul_GBWL4.md",
        "title": "GBWL 4: Finanzprozess (Investition & Finanzierung)",
        "degree": "Bachelor of Science",
        "modul_code": "10085",
        "ects": "6,0",
        "grade": "2,7",
        "prof": "Prof. Dr. Henry Schäfer (Institut für Betriebswirtschaftslehre)",
        "rel_dirs": [r"03_Bachelor\GBWL 4 - Finanzprozess\01_Investition_und_Finanzierung_WS19"],
        "skip_patterns": [],
        "desc": "Investition und Finanzierung: Dynamische Investitionsrechnung (Kapitalwertmethode, Interne Zinssatzmethode, Annuitätenmethode), Finanzierungsformen (Eigen-, Fremd-, Mezzanine-Finanzierung), Innenfinanzierung, Kapitalstruktur und Verschuldungsgrad.",
        "skills": ["Kapitalwertmethode (NPV) & Zinseszinsrechnung", "Interne Zinsfußmethode (IRR)", "Eigen- vs. Fremdfinanzierungsinstrumente", "Cashflow-Analyse & Liquiditätssteuerung", "Finanzmathematik & Portfoliomanagement"]
    },
    {
        "file": "Modul_GVWL1.md",
        "title": "GVWL 1: Märkte & wirtschaftliche Entscheidungen",
        "degree": "Bachelor of Science",
        "modul_code": "10095",
        "ects": "6,0",
        "grade": "2,7",
        "prof": "Prof. Dr. Frank C. Englmann (Institut für Volkswirtschaftslehre)",
        "rel_dirs": [r"03_Bachelor\GVWL 1 - Märkte & wirtschaftliche Entscheidungen\01_Vorlesungsunterlagen"],
        "skip_patterns": [],
        "desc": "Mikroökonomik: Haushalts- und Unternehmenstheorie, Angebot und Nachfrage, Marktgleichgewicht, vollkommener Wettbewerb, Monopol, Oligopol, Preiselastizitäten und Wohlfahrtsökonomik.",
        "skills": ["Mikroökonomische Modellierung", "Preis- und Mengenbildung im Marktgleichgewicht", "Preiselastizitäten von Angebot & Nachfrage", "Monopol- und Oligopoltheorien", "Wohlfahrtstheorie & Marktversagen"]
    },
    {
        "file": "Modul_Informatikrecht.md",
        "title": "Informatikrecht",
        "degree": "Bachelor of Science",
        "modul_code": "10105",
        "ects": "3,0",
        "grade": "4,0",
        "prof": "Institut für Rechtswissenschaften (Universität Stuttgart)",
        "rel_dirs": [r"03_Bachelor\Informatikrecht\01_Vorlesungsunterlagen"],
        "skip_patterns": [],
        "desc": "Rechtliche Rahmenbedingungen der IT: Datenschutzrecht (DSGVO, BDSG), Urheberrecht an Software und Datenbanken, Open-Source-Lizenzen, Softwarevertragsrecht (EVB-IT, SLA), IT-Sicherheitsrecht und Haftung im Internet.",
        "skills": ["Datenschutzrecht nach DSGVO", "Softwareurheberrecht & Lizenzverträge", "EVB-IT Vertragsgestaltung", "Haftung für IT-Sicherheit & Schäden", "Domain- und Telekommunikationsrecht"]
    },
    {
        "file": "Modul_Informationsmanagement_Bachelor.md",
        "title": "Informationsmanagement (Grundlagen & Business Intelligence)",
        "degree": "Bachelor of Science",
        "modul_code": "10115",
        "ects": "9,0",
        "grade": "3,0",
        "prof": "Prof. Dr. Hans-Georg Kemper (Institut für Betriebswirtschaftslehre)",
        "rel_dirs": [
            r"03_Bachelor\Informationsmanagement\01_Grundlagen_Informationsmanagement_WS19",
            r"03_Bachelor\Informationsmanagement\02_Business_Intelligence_SS20"
        ],
        "skip_patterns": [],
        "desc": "Informationsmanagement & Business Intelligence: Strategisches Informationsmanagement, IT-Architekturen, Data Warehousing, ETL-Prozesse, Multidimensionale Datenmodellierung (Star-Schema, Snowflake-Schema), OLAP-Würfel und Management Reporting.",
        "skills": ["Data Warehousing & ETL-Architektur", "Multidimensionale Datenmodellierung (Star/Snowflake)", "OLAP-Cubes & MDX Abfragen", "Business Intelligence Reporting & KPIs", "Strategisches Informationsmanagement"]
    },
    {
        "file": "Modul_Dienstleistungsmanagement.md",
        "title": "Management von Dienstleistungsunternehmen",
        "degree": "Bachelor of Science",
        "modul_code": "10125",
        "ects": "6,0",
        "grade": "4,0",
        "prof": "Lehrstuhl für ABWL und Dienstleistungsmanagement",
        "rel_dirs": [r"03_Bachelor\Management von Dienstleistungsunternehmen\01_Vorlesungsunterlagen"],
        "skip_patterns": [],
        "desc": "Besonderheiten von Dienstleistungsunternehmen: Immaterialität, uno-actu-Prinzip, Dienstleistungsqualität (SERVQUAL, Gap-Modell), Kapazitätssteuerung, Yield Management und Dienstleistungsmarketing im ÖPNV und Hospitality-Sektor.",
        "skills": ["Dienstleistungs-Typologien & Uno-Actu-Prinzip", "Service Gap Modell & SERVQUAL", "Dienstleistungskapazitätssteuerung", "Service Relationship Marketing", "ÖPNV Dienstleistungsmanagement"]
    },
    {
        "file": "Modul_Mathematik.md",
        "title": "Mathematik für Wirtschaftswissenschaftler",
        "degree": "Bachelor of Science",
        "modul_code": "10135",
        "ects": "9,0",
        "grade": "4,0",
        "prof": "Fachbereich Mathematik (Universität Stuttgart)",
        "rel_dirs": [r"03_Bachelor\Mathematik für Wirtschaftswissenschaftler\01_Vorlesungsunterlagen"],
        "skip_patterns": [],
        "desc": "Höhere Mathematik für Ökonomen: Lineare Algebra (Matrizen, Determinanten, lineare Gleichungssysteme, Gauß-Algorithmus), Analysis einer und mehrerer Variablen, partielle Ableitungen, Lagrange-Multiplikatoren zur Optimierung und Integralrechnung.",
        "skills": ["Lineare Algebra & Matrizenrechnung", "Gaußsches Eliminationsverfahren", "Differenzialrechnung mehrerer Veränderlicher", "Extrema unter Nebenbedingungen (Lagrange)", "Finanzmathematische Optimierungsverfahren"]
    },
    {
        "file": "Modul_MCI.md",
        "title": "Mensch-Computer-Interaktion (MCI)",
        "degree": "Bachelor of Science",
        "modul_code": "10145",
        "ects": "6,0",
        "grade": "3,3",
        "prof": "Prof. Dr. Albrecht Schmidt (Institut für Visualisierung und Interaktive Systeme)",
        "rel_dirs": [r"03_Bachelor\Mensch-Computer-Interaktion\01_Vorlesungsfolien"],
        "skip_patterns": [],
        "desc": "Gestaltung interaktiver Systeme: Wahrnehmungspsychologie, Usability Engineering Lifecycle, User-Centered Design (UCD), Heuristische Evaluation (Nielsen), Barrierefreiheit, UI-Design-Prinzipien und Fiori UX Grundlagen.",
        "skills": ["User-Centered Design (UCD)", "Usability Heuristiken nach Nielsen", "Informationsarchitektur & Wireframing", "Cognitive Walkthrough & Usability Testing", "Barrierefreiheit & Human Factors"]
    },
    {
        "file": "Modul_Modellierung.md",
        "title": "Modellierung",
        "degree": "Bachelor of Science",
        "modul_code": "10155",
        "ects": "6,0",
        "grade": "2,3",
        "prof": "Prof. Dr. Bernhard Mitschang (Institut für Parallele und Verteilte Systeme)",
        "rel_dirs": [r"03_Bachelor\Modellierung\01_Vorlesungsfolien"],
        "skip_patterns": [],
        "desc": "Modellierungsmethoden der Informatik: Entity-Relationship-Modellierung (ERM), Relationale Algebra, Normalformenlehre (1NF bis BCNF), Petrinetze (Bedingungs-Ereignis-Netze), UML (Klassen-, Sequenz-, Zustandsdiagramme) und BPMN 2.0 Geschäftsprozessmodellierung.",
        "skills": ["Entity-Relationship-Modellierung (ERM)", "Relationale Algebra & SQL-Abbildung", "Petrinetze (Lebendigkeit, Sicherheit)", "UML 2.0 Klassendiagramme & Sequenzen", "BPMN 2.0 Geschäftsprozessmodellierung"]
    },
    {
        "file": "Modul_Programmentwicklung.md",
        "title": "Programmentwicklung (PE)",
        "degree": "Bachelor of Science",
        "modul_code": "10165",
        "ects": "6,0",
        "grade": "3,0",
        "prof": "Institut für Formale Methoden der Informatik",
        "rel_dirs": [r"03_Bachelor\Programmentwicklung\01_Programmentwicklung_WS20"],
        "skip_patterns": [],
        "desc": "Konzepte moderner Programmiersprachen: Funktionale Programmierung (Rekursion, Higher-Order Functions, Lambda-Kalkül), Logische Programmierung (Prolog, Unifikation), Typisierungssysteme und Softwarekorrektheit.",
        "skills": ["Funktionale Programmierung (Haskell/Scheme)", "Rekursive Algorithmenmuster", "Logische Programmierung & Inferenz", "Typensysteme & Typsicherheit", "Formale Verifikation von Code"]
    },
    {
        "file": "Modul_PSE.md",
        "title": "Programmierung und Software-Entwicklung (PSE)",
        "degree": "Bachelor of Science",
        "modul_code": "10175",
        "ects": "9,0",
        "grade": "4,0",
        "prof": "Institut für Softwaretechnologie",
        "rel_dirs": [r"03_Bachelor\Programmierung und Software-Entwicklung\01_Vorlesungsunterlagen_und_Folien"],
        "skip_patterns": [],
        "desc": "Objektorientierte Programmierung in Java: Klassen, Objekte, Kapselung, Vererbung, Polymorphie, Schnittstellen, Ausnahmebehandlung (Exceptions), Java Collections Framework, Generics und I/O-Streams.",
        "skills": ["Java OOP (Kapselung, Vererbung, Polymorphie)", "Java Collections Framework", "Exception Handling & Robustheit", "Generics & Clean Code", "Multithreading & Nebenläufigkeit Grundlagen"]
    },
    {
        "file": "Modul_Softwarepraktikum.md",
        "title": "Softwarepraktikum (SoPra taskMasterPro)",
        "degree": "Bachelor of Science",
        "modul_code": "10185",
        "ects": "6,0",
        "grade": "3,0",
        "prof": "Lehrstuhl für ABWL und Wirtschaftsinformatik II",
        "rel_dirs": [r"03_Bachelor\Softwarepraktikum\04_Vorlesung"],
        "skip_patterns": [],
        "desc": "Praktische Softwareentwicklung im Team: Konzeption, Spezifikation, agile Umsetzung und Deployment der Projektmanagement- und Task-Tracking-Software taskMasterPro in Java mit GUI und Datenbankanbindung.",
        "skills": ["Agile Softwareentwicklung im Team (Scrum)", "Fullstack Java & GUI-Entwicklung", "Software-Spezifikation (Lastenheft/Pflichtenheft)", "Git Workflow & Code Reviews", "Systemtest & Release-Management"]
    },
    {
        "file": "Modul_Statistik1.md",
        "title": "Statistik I (Deskriptive Statistik)",
        "degree": "Bachelor of Science",
        "modul_code": "10195",
        "ects": "6,0",
        "grade": "4,0",
        "prof": "Institut für Volkswirtschaftslehre und Recht",
        "rel_dirs": [r"03_Bachelor\Statistik I\01_Uebungen"],
        "skip_patterns": [],
        "desc": "Deskriptive Statistik: Eindimensionale Häufigkeitsverteilungen, Lage- und Streuungsmaße (Mittelwert, Median, Varianz, Standardabweichung), zweidimensionale Verteilungen, Kontingenztabelle, Korrelationsrechnung (Bravais-Pearson, Spearman) und lineare Regression.",
        "skills": ["Deskriptive Datenanalyse", "Lage- und Streuungsparameter", "Korrelationsanalyse", "Lineare Regressionsrechnung", "Verteilungsfunktionen & Gini-Koeffizient"]
    },
    {
        "file": "Modul_Statistik2.md",
        "title": "Statistik II (Induktive Statistik)",
        "degree": "Bachelor of Science",
        "modul_code": "10205",
        "ects": "6,0",
        "grade": "2,7",
        "prof": "Institut für Volkswirtschaftslehre und Recht",
        "rel_dirs": [r"03_Bachelor\Statistik II\02_Uebungen"],
        "skip_patterns": [],
        "desc": "Induktive Statistik & Wahrscheinlichkeitsrechnung: Zufallsvariablen, diskrete und stetige Verteilungen (Binomial-, Poisson-, Normalverteilung), Schätztheorie (Punkt- und Intervallschätzung, Konfidenzintervalle), statistische Hypothesentests (t-Test, Chi-Quadrat-Test) und Fehler 1. und 2. Art.",
        "skills": ["Wahrscheinlichkeitsrechnung & Verteilungen", "Statistische Schätztheorie", "Konfidenzintervalle berechnen", "Signifikanztests (t-Test, Gauß-Test)", "Güte von Hypothesentests"]
    },
    {
        "file": "Modul_Wissensverarbeitung.md",
        "title": "Wissensverarbeitung",
        "degree": "Bachelor of Science",
        "modul_code": "10215",
        "ects": "6,0",
        "grade": "3,7",
        "prof": "Institut für Intelligente Systeme (Universität Stuttgart)",
        "rel_dirs": [r"03_Bachelor\Wissensverarbeitung\01_Vorlesungsfolien"],
        "skip_patterns": [],
        "desc": "Wissensbasierte Systeme & Künstliche Intelligenz: Wissensrepräsentation, Prädikatenlogik erster Stufe, Resolutionsprinzip, semantische Netze, Frames, Ontologien (OWL, RDF), Inferenzmechanismen (Forward/Backward Chaining) und Expertensysteme.",
        "skills": ["Wissensrepräsentation & Logik", "Semantische Netze & Ontologien (RDF/OWL)", "Inferenzmaschinen (Vorwärts-/Rückwärtsverkettung)", "Resolutionsbeweise in Prädikatenlogik", "Wissensgraphen & Reasoning"]
    },
    {
        "file": "Modul_Schreibwerkstatt.md",
        "title": "Schreibwerkstatt - Vom studentischen zum beruflichen Schreiben",
        "degree": "Bachelor of Science",
        "modul_code": "10225",
        "ects": "3,0",
        "grade": "BE (Bestanden)",
        "prof": "Schreibzentrum der Universität Stuttgart",
        "rel_dirs": [r"03_Bachelor\Schreibwerkstatt - Vom studentischen zum beruflichen Schreiben\01_Leitfaeden_und_Materialien"],
        "skip_patterns": [],
        "desc": "Wissenschaftliche und berufsbezogene Schreibkompetenz: Strukturierung wissenschaftlicher Arbeiten, Exposés, präzises Paraphrasieren, korrekte Zitierweise (APA/IEEE), zielgruppengerechte Geschäftskommunikation und Textredaktion.",
        "skills": ["Wissenschaftliches Formulieren & Gliedern", "Exposé- & Abstract-Erstellung", "Plagiatssicheres Zitieren & Paraphrasieren", "Geschäftskorrespondenz & Management Summaries", "Textüberarbeitung & Peer Feedback"]
    },
    {
        "file": "Modul_Profilseminar_HRM.md",
        "title": "Profilseminar zum Human Resource Management",
        "degree": "Bachelor of Science",
        "modul_code": "10235",
        "ects": "6,0",
        "grade": "3,0",
        "prof": "Prof. Dr. Marion Büttgen (Institut für Betriebswirtschaftslehre)",
        "rel_dirs": [r"03_Bachelor\Profilseminar zum Human Resource Management\01_Seminararbeit_Mensch_Roboter_Interaktion"],
        "skip_patterns": [],
        "desc": "Wissenschaftliches Seminar zu Human Resource Management & Mensch-Roboter-Interaktion: Untersuchung der Kundenwahrnehmung und Akzeptanz humanoider Serviceroboter an der Service-Frontline, Erstellung der Seminararbeit und wissenschaftliche Abschlusspräsentation.",
        "skills": ["Mensch-Roboter-Interaktion (HRI) im Service", "Empirische Akzeptanzforschung (TAM)", "Wissenschaftliche Seminararbeit & Konzeption", "Fachpräsentation & Diskussion", "HR-Transformationsdynamiken"]
    },
    {
        "file": "Modul_Seminar_Interdisziplinaer.md",
        "title": "Seminar interdisziplinäre Themen (Maschinelles Lernen)",
        "degree": "Bachelor of Science",
        "modul_code": "10245",
        "ects": "6,0",
        "grade": "2,3",
        "prof": "Lehrstuhl für Wirtschaftsinformatik",
        "rel_dirs": [r"03_Bachelor\Seminar interdisziplinäre Themen\01_Seminar_Maschinelles_Lernen_SS19"],
        "skip_patterns": [],
        "desc": "Interdisziplinäres Seminar zu Machine Learning & Big Data: Verfahren des überwachten und unüberwachten Lernens (Klassifikation, Regression, Clustering), Algorithmen (Random Forest, SVM, K-Means), wissenschaftliches Handout und Präsentation.",
        "skills": ["Supervised & Unsupervised Learning", "Regressions- und Klassifikationsmodelle", "Modellvalidierung & Metriken", "Wissenschaftliches Handout & Vortrag", "Data-Mining-Prozess (CRISP-DM)"]
    }
]

print(f"Registry configured with {len(MODULES)} modules.")

def build_new_module_header(mod):
    skills_md = "\n".join([f"- **{s}**" for s in mod.get("skills", [])])
    first_dir = mod["rel_dirs"][0]
    # top level folder
    top_folder = first_dir.split(os.sep)[0] if os.sep in first_dir else first_dir
    local_path = os.path.join(ROOT_DIR, first_dir).replace("\\", "/")
    
    deg_slug = "master_of_science" if "Master" in mod["degree"] else "bachelor_of_science"
    
    header = f"""---
title: "{mod['title']}"
modul_code: "{mod['modul_code']}"
degree: "{mod['degree']}"
ects: "{mod['ects']}"
grade: "{mod['grade']}"
prof: "{mod['prof']}"
local_path: "file:///{local_path}"
status: completed
tags:
  - university
  - academics
  - {deg_slug}
---

# 🎓 {mod['title']}

> [!INFO] **Akademische Eckdaten**
> - **Abschluss:** {mod['degree']} (Universität Stuttgart)
> - **Modulcode:** `{mod['modul_code']}` | **ECTS:** **{mod['ects']} ECTS**
> - **Offizielle Note:** **{mod['grade']}**
> - **Verantwortlicher Lehrstuhl / Dozent:** {mod['prof']}

---

## 📌 Modulbeschreibung & Inhalt
{mod['desc']}

---

## 🛠️ Erlernte Methoden & Schlüsselkompetenzen
{skills_md}

---

## 📂 Lokaler Klick-Pfad zum Modul-Archiv
Direkter Zugriff auf alle Vorlesungsfolien, Übungen, Altklausuren und Ausarbeitungen:
👉 [{mod['title']} (Lokaler Ordner)](file:///{local_path})

---

## 🧠 Neurale Vernetzung & Praxisbezug
- Zur Gesamtübersicht: [[02_Wirtschaftsinformatik_300ECTS/Modul_Übersicht|300 ECTS Modulübersicht]]
"""
    return header

def run_extraction():
    os.makedirs(VAULT_DIR, exist_ok=True)
    t_start = time.time()
    total_decks_processed = 0
    total_slides_extracted = 0
    total_chars_written = 0

    print("=" * 70)
    print("🚀 SYSTEMATISCHE VOLLTEXT-EXTRAKTION ALLER VORLESUNGSFOLIEN")
    print(f"Target Vault: {VAULT_DIR}")
    print("=" * 70)

    for idx, mod in enumerate(MODULES, start=1):
        target_path = os.path.join(VAULT_DIR, mod["file"])
        print(f"\n[{idx}/{len(MODULES)}] Verarbeite {mod['title']} -> {mod['file']}")
        
        # 1. Collect all slide files
        slide_files = []
        for rel_d in mod["rel_dirs"]:
            full_d = os.path.join(ROOT_DIR, rel_d)
            if not os.path.exists(full_d):
                continue
            for root, dirs, files in os.walk(full_d):
                for f in files:
                    if f.lower().endswith((".pdf", ".pptx")) and not f.startswith(("~", "._")):
                        # Check skip patterns
                        if any(sk.lower() in f.lower() for sk in mod.get("skip_patterns", [])):
                            continue
                        # Filter out non-slide files if needed
                        fn_low = f.lower()
                        if any(ex in fn_low for ex in ["klausur", "altklausur", "blatt", "loesung", "solution", "bwi-zitier"]):
                            continue
                        slide_files.append(os.path.join(root, f))
        
        # Deduplicate by file content hash
        unique_files = []
        seen_hashes = set()
        for sf in slide_files:
            h = get_file_md5(sf)
            if h and h not in seen_hashes:
                seen_hashes.add(h)
                unique_files.append(sf)
        
        # Sort naturally by filename
        unique_files.sort(key=lambda x: os.path.basename(x).lower())
        print(f"  Gefundene einzigartige Foliendecks: {len(unique_files)}")
        
        # Extract slides
        deck_sections = []
        mod_slides_count = 0
        for sf in unique_files:
            fn = os.path.basename(sf)
            slides = extract_deck(sf)
            if not slides:
                continue
            mod_slides_count += len(slides)
            file_url = sf.replace("\\", "/")
            deck_md = [
                f"\n### 📑 Vorlesungseinheit: {os.path.splitext(fn)[0]}",
                f"**Datei:** [{fn}](file:///{file_url})  ",
                f"**Extrahierte Folien:** {len(slides)}\n"
            ]
            for s_idx, s_text in slides:
                deck_md.append(f"#### Folie {s_idx}\n{s_text}\n")
            
            deck_sections.append("\n".join(deck_md))
        
        # Build the lecture section markdown
        if deck_sections:
            slides_section = (
                "\n\n---\n\n"
                "## 🖥️ Vorlesungsfolien & Lehrinhalte (Volltext-Transkript)\n\n"
                "> [!NOTE] **Systematische Volltext-Dokumentation**\n"
                f"> Die folgenden Abschnitte enthalten die vollständigen, extrahierten Lehrinhalte aus {len(deck_sections)} Foliendecks ({mod_slides_count} Folien) zu diesem Modul.\n"
                "> Dient dem lokalen RAG-System und dem Second Brain als unverkürzte Wissensbasis.\n"
                + "\n".join(deck_sections)
            )
        else:
            slides_section = (
                "\n\n---\n\n"
                "## 🖥️ Vorlesungsfolien & Lehrinhalte (Volltext-Transkript)\n\n"
                "> [!NOTE] **Foliendokumentation**\n"
                "> Für dieses Modul lagen vorwiegend praktische Aufgabenblätter, Seminararbeiten oder Projektdateien vor. Ausgewählte Lehrinhalte sind oben aufgeführt.\n"
            )
        
        # Read or create target note
        if os.path.exists(target_path):
            with open(target_path, "r", encoding="utf-8") as f:
                content = f.read()
            # Split off existing slide section if present
            split_token = "## 🖥️ Vorlesungsfolien & Lehrinhalte (Volltext-Transkript)"
            if split_token in content:
                content = content.split(split_token)[0].rstrip()
            final_content = content + slides_section
        else:
            header = build_new_module_header(mod)
            final_content = header + slides_section
        
        # Write out
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(final_content)
        
        total_decks_processed += len(deck_sections)
        total_slides_extracted += mod_slides_count
        total_chars_written += len(final_content)
        print(f"  -> Gespeichert: {len(deck_sections)} Decks, {mod_slides_count} Folien, {len(final_content):,} Zeichen.")

    elapsed = time.time() - t_start
    print("\n" + "=" * 70)
    print("✅ VOLLTEXT-EXTRAKTION ERFOLGREICH ABGESCHLOSSEN!")
    print(f"  Verarbeitete Module: {len(MODULES)}")
    print(f"  Extrahierte Foliendecks: {total_decks_processed}")
    print(f"  Extrahierte Einzelfolien: {total_slides_extracted}")
    print(f"  Gesamter Textumfang in Vault: {total_chars_written:,} Zeichen")
    print(f"  Benötigte Zeit: {elapsed:.2f} Sekunden")
    print("=" * 70)

if __name__ == "__main__":
    run_extraction()
