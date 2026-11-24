# -*- coding: utf-8 -*-
"""
Data Science Knowledge Graph & Obsidian Vault Harmonizer
Optimizes Visar Murseli's Second Brain for LLMs, RAG, and Vector Databases.
Author: Visar Murseli, M.Sc. | Data Science & Enterprise AI Architect
"""

import os
import re
import json
from datetime import datetime

VAULT_DIR = r"C:\Users\SHQIPTAR634\Documents\Obsidian Vault"
MANIFEST_PATH = os.path.join(VAULT_DIR, "graph_manifest.json")

# 1. Exact canonical mapping for conceptual and path-mismatched targets
CANONICAL_CONCEPT_MAP = {
    "03_sap_enterprisearchitecture/bpmn_signavio": ("SSB_Tool_Governance_Signavio_CALM", "BPMN Modellierung in SAP Signavio"),
    "bpmn_signavio": ("SSB_Tool_Governance_Signavio_CALM", "BPMN Modellierung in SAP Signavio"),
    "03_sap_enterprisearchitecture/sap_fi_financials": ("SSB_Solution_Design_FI_CO", "SAP S/4HANA Finance (FI)"),
    "sap_fi_financials": ("SSB_Solution_Design_FI_CO", "SAP S/4HANA Finance (FI)"),
    "03_sap_enterprisearchitecture/sap_co_controlling": ("Kostenrechnung_PSP_vs_Innenauftrag", "SAP S/4HANA Controlling (CO)"),
    "sap_co_controlling": ("Kostenrechnung_PSP_vs_Innenauftrag", "SAP S/4HANA Controlling (CO)"),
    "04_second_brain_zettelkasten/rechnungswesen_hgb": ("Anlagenbuchhaltung_HGB_Steuerrecht", "Rechnungswesen nach HGB & Steuerrecht"),
    "rechnungswesen_hgb": ("Anlagenbuchhaltung_HGB_Steuerrecht", "Rechnungswesen nach HGB & Steuerrecht"),
    "04_second_brain_zettelkasten/business_intelligence": ("Generative_AI_LLM", "Business Intelligence & Data Analytics"),
    "business_intelligence": ("Generative_AI_LLM", "Business Intelligence & Data Analytics"),
    "04_second_brain_zettelkasten/innovationsmanagement_frameworks": ("Modul_Innovationsmanagement", "Innovationsmanagement & Stage-Gate-Frameworks"),
    "innovationsmanagement_frameworks": ("Modul_Innovationsmanagement", "Innovationsmanagement & Stage-Gate-Frameworks"),
    "04_second_brain_zettelkasten/geschäftsmodellinnovation": ("E_Business_Konzepte", "Digitale Geschäftsmodellinnovation"),
    "geschäftsmodellinnovation": ("E_Business_Konzepte", "Digitale Geschäftsmodellinnovation"),
    "04_second_brain_zettelkasten/it_strategie": ("Enterprise_Architecture_Overview", "IT-Strategie & Enterprise Architecture Management"),
    "it_strategie": ("Enterprise_Architecture_Overview", "IT-Strategie & Enterprise Architecture Management"),
    "04_second_brain_zettelkasten/datenmodellierung": ("SQL_und_Datenmodellierung", "Relationales & NoSQL Datenmodellierungs-Design"),
    "datenmodellierung": ("SQL_und_Datenmodellierung", "Relationales & NoSQL Datenmodellierungs-Design"),
    "04_second_brain_zettelkasten/java_entwicklung": ("Software_Engineering_Prinzipien", "Objektorientierte Java-Softwareentwicklung"),
    "java_entwicklung": ("Software_Engineering_Prinzipien", "Objektorientierte Java-Softwareentwicklung"),
    "04_second_brain_zettelkasten/projektmanagement": ("Gesamtprojektplan_MS_Project", "Agiles & Klassisches IT-Projektmanagement"),
    "projektmanagement": ("Gesamtprojektplan_MS_Project", "Agiles & Klassisches IT-Projektmanagement"),
    "04_second_brain_zettelkasten/service_management": ("DC1_ITIL4_Service_Operations", "IT Service Management & ITIL 4"),
    "service_management": ("DC1_ITIL4_Service_Operations", "IT Service Management & ITIL 4"),
    "04_second_brain_zettelkasten/volkswirtschaftslehre": ("Modul_GVWL1", "Grundlagen der Volkswirtschaftslehre"),
    "volkswirtschaftslehre": ("Modul_GVWL1", "Grundlagen der Volkswirtschaftslehre"),
    "04_second_brain_zettelkasten/internationales_management": ("Modul_Management_IT_Unternehmen", "Internationales Management von IT-Unternehmen"),
    "internationales_management": ("Modul_Management_IT_Unternehmen", "Internationales Management von IT-Unternehmen"),
}

# Explicit frontmatter metadata for files missing frontmatter
EXPLICIT_FRONTMATTER = {
    "00_CHANGELOG.md": {
        "id": "changelog-system-releases",
        "title": "Changelog & System Release Protocol",
        "type": "log",
        "domain": "system-governance",
        "status": "evergreen",
        "summary": "Revisionssicheres Änderungsprotokoll nach Keep a Changelog und Conventional Commits für alle Systemupdates und Git-Releases auf main.",
        "tags": ["changelog", "governance", "releases", "system_history"],
        "aliases": ["Release Notes", "Changelog", "System History"]
    },
    r"01_Karriere_Bewerbungen\Aktuelle_Bewerbungsunterlagen.md": {
        "id": "aktuelle-master-bewerbungsunterlagen",
        "title": "Aktuelle Master-Bewerbungsunterlagen | Visar Murseli",
        "type": "hub",
        "domain": "career-pmo",
        "status": "verified",
        "summary": "Zentraler Dokumenten-Hub für verifizierte Master-Bewerbungsunterlagen (M.Sc. Wirtschaftsinformatik 1,6, Masterarbeit 1,0, B.Sc. 3,0, Lebenslauf, Zeugnisse).",
        "tags": ["career", "bewerbung", "zeugnisse", "lebenslauf", "master_of_science"],
        "aliases": ["Master Bewerbungsunterlagen", "Bewerbungsdokumente", "CV Vault"]
    },
    r"01_Karriere_Bewerbungen\Target_Roles.md": {
        "id": "target-roles-positioning",
        "title": "Zielrollen & Positioning | Visar Murseli",
        "type": "concept",
        "domain": "career-pmo",
        "status": "active",
        "summary": "Strategisches Rollenprofil und Positionierungsmatrix (Trainee IT, Junior SAP Consultant, IT-Transformation, Enterprise Architecture) mit Pitch-Archetypen.",
        "tags": ["career", "positioning", "target_roles", "trainee", "sap_consultant"],
        "aliases": ["Target Roles", "Zielrollen", "Karriere-Positionierung"]
    },
    r"01_Karriere_Bewerbungen\Interview_Vorbereitungen\2026-11-24_Schwarz_Digits_SAP_HCM_IAM.md": {
        "id": "interview-prep-schwarz-digits-iam",
        "title": "Interview Vorbereitung: Schwarz Digits – Junior SAP HCM IAM Specialist",
        "type": "interview-prep",
        "domain": "career-pmo",
        "status": "active",
        "summary": "Exklusives Interview-Dossier für Schwarz Digits (Ref: 4972), SAP HCM Berechtigungsobjekte (P_ORGIN, P_PERNR, OOSP), JML-Lifecycle, Ausweis-Check und STAR-Storytelling.",
        "tags": ["interview_prep", "schwarz_digits", "sap_hcm", "iam", "authorization", "star_method"],
        "aliases": ["Schwarz Digits Interview", "SAP HCM IAM Vorbereitung", "Ref 4972"]
    },
    r"03_SAP_EnterpriseArchitecture\00_MOCs\MOC_SSB_Dokumentenatlas.md": {
        "id": "moc-ssb-dokumentenatlas",
        "title": "MOC: SSB Dokumentenatlas & Artefakt-Register (1.890 Dateien)",
        "type": "moc",
        "domain": "sap-transformation",
        "status": "verified",
        "summary": "Strukturierter Dokumentenatlas und Metadaten-Katalog über 1.890 Originalartefakte des Großprojekts SAP4SSB (TP1 bis TP5, Solution Design, Migration, Governance).",
        "tags": ["moc", "ssb", "dokumentenatlas", "s4hana", "artefakt_register"],
        "aliases": ["SSB Dokumentenatlas", "Artefakt-Register SSB"]
    },
    r"03_SAP_EnterpriseArchitecture\02_Kaufmaennische_Prozesse\Stream_Grants_Management_Drittmittel_LGVFG.md": {
        "id": "stream-grants-management-lgvfg",
        "title": "Stream Grants Management (GM): Drittmittel, Zuschüsse & ÖPNV-Förderung (LGVFG / GVFG)",
        "type": "concept",
        "domain": "sap-transformation",
        "status": "verified",
        "summary": "Fachkonzept und Ableitungslogik für SAP Grants Management (GTE), Drittmittelabrechnung und Förderrichtlinien (LGVFG/GVFG) bei der SSB AG.",
        "tags": ["sap_gm", "grants_management", "drittmittel", "lgvfg", "foerderung", "ssb"],
        "aliases": ["Grants Management Fachkonzept", "LGVFG Drittmittel", "SAP GM"]
    },
    r"03_SAP_EnterpriseArchitecture\02_Kaufmaennische_Prozesse\Stream_Sales_Distribution_PATRIS.md": {
        "id": "stream-sales-distribution-patris",
        "title": "Stream Sales & Distribution (SD) & Subsystem-Integration PATRIS",
        "type": "concept",
        "domain": "sap-transformation",
        "status": "verified",
        "summary": "Fit-to-Standard Scoping für SAP SD und Schnittstellen-Architektur zum Ticketing- und Tarif-Vorsystem PATRIS im ÖPNV-Vertrieb der SSB AG.",
        "tags": ["sap_sd", "patris", "ticketing", "schnittstellen", "vertrieb", "ssb"],
        "aliases": ["SD PATRIS Integration", "PATRIS Schnittstelle", "SAP SD Scoping"]
    },
    r"03_SAP_EnterpriseArchitecture\S4HANA_Plattformisierung.md": {
        "id": "s4hana-plattformisierung-thesis",
        "title": "SAP S/4HANA Plattformisierung & ERP-Transformation",
        "type": "concept",
        "domain": "enterprise-architecture",
        "status": "verified",
        "summary": "Wissenschaftliches Fundament der Masterarbeit (Note 1,0): Kritische Erfolgsfaktoren, Boundary Resources Theory, Plattform-Governance und bimodale Entkopplung.",
        "tags": ["plattformisierung", "s4hana", "master_thesis", "boundary_resources", "governance"],
        "aliases": ["S/4HANA Plattformisierung", "Masterarbeit Plattformisierung", "ERP-Transformation"]
    },
    r"03_SAP_EnterpriseArchitecture\SSB_Datenmigration_LTMC_CVI.md": {
        "id": "ssb-datenmigration-ltmc-cvi",
        "title": "Datenmigrations-Architektur: SAP Migration Cockpit (LTMC) & CVI",
        "type": "concept",
        "domain": "sap-transformation",
        "status": "verified",
        "summary": "Architektur und Cutover-Strategie der Datenmigration von ECC 6.0 nach S/4HANA Private Cloud via LTMC, Staging-Tabellen und Customer-Vendor-Integration (CVI).",
        "tags": ["datenmigration", "ltmc", "cvi", "cutover", "s4hana", "ssb"],
        "aliases": ["SSB Datenmigration", "LTMC CVI Architektur", "Migration Cockpit"]
    },
    r"03_SAP_EnterpriseArchitecture\SSB_Foerdermittel_Grants_Management.md": {
        "id": "ssb-foerdermittel-grants-management",
        "title": "Fördermittel- & Drittmittelmanagement (SAP Grants Management)",
        "type": "concept",
        "domain": "sap-transformation",
        "status": "verified",
        "summary": "Integration von SAP Grants Management mit PS (Projekt-System) und FI/CO zur revisionssicheren Abwicklung öffentlicher Fördermittel im Nahverkehr.",
        "tags": ["grants_management", "foerdermittel", "sap_ps", "oepnv", "ssb"],
        "aliases": ["SSB Fördermittel", "Grants Management Integration"]
    },
    r"03_SAP_EnterpriseArchitecture\SSB_Grossprojekt_SAP4SSB.md": {
        "id": "ssb-grossprojekt-sap4ssb",
        "title": "Großprojekt SAP4SSB – Transformation & Multiprojekt-Governance",
        "type": "hub",
        "domain": "sap-transformation",
        "status": "verified",
        "summary": "Gesamtschau des 24-monatigen S/4HANA-Transformationsprojekts SAP4SSB: Struktur der 5 Teilprojekte, Phasenmodell, Meilensteine und C-Level Reporting.",
        "tags": ["sap4ssb", "grossprojekt", "governance", "pmo", "transformation", "ssb"],
        "aliases": ["Großprojekt SAP4SSB", "SAP4SSB Transformation", "SSB S/4HANA"]
    },
    r"03_SAP_EnterpriseArchitecture\SSB_Interview_Stories_STAR.md": {
        "id": "ssb-interview-stories-star",
        "title": "SSB Interview Masterclass – 5 authentische STAR-Storys",
        "type": "interview-prep",
        "domain": "career-pmo",
        "status": "verified",
        "summary": "Fünf handlungsorientierte STAR-Erfolgsstorys aus 24 Monaten SSB PMO & Architektur (Projektplanung, CVI-Konflikt, Signavio-Rollout, Betriebsrat, Cutover).",
        "tags": ["star_stories", "interview_masterclass", "pmo", "ssb", "leadership"],
        "aliases": ["STAR Stories SSB", "Interview Masterclass", "SSB Praxisbeispiele"]
    },
    r"03_SAP_EnterpriseArchitecture\SSB_S4HANA_12_Strategische_Domaenen_Notebook.md": {
        "id": "ssb-s4hana-12-strategische-domaenen",
        "title": "SSB S/4HANA Transformation | Strategisches Enterprise Notebook",
        "type": "hub",
        "domain": "sap-transformation",
        "status": "verified",
        "summary": "Aggregiertes Wissens-Cockpit über alle 12 strategischen Domänen von SAP4SSB für NotebookLM und tiefe Kontextinjektion in LLM-Agenten.",
        "tags": ["strategische_domaenen", "notebooklm", "s4hana", "ssb", "knowledge_lake"],
        "aliases": ["12 Strategische Domänen", "SSB Enterprise Notebook", "NotebookLM Mining"]
    },
    r"03_SAP_EnterpriseArchitecture\SSB_Solution_Design_FI_CO.md": {
        "id": "ssb-solution-design-fi-co",
        "title": "SSB Solution Design – Kaufmännische Prozesse (FI / CO)",
        "type": "concept",
        "domain": "sap-transformation",
        "status": "verified",
        "summary": "Lösungsarchitektur für Hauptbuchhaltung, Anlagenbuchhaltung, Kostenstellen- und Profitcenter-Rechnung sowie Trennungsrechnung nach EU-Verordnung 1370/2007.",
        "tags": ["solution_design", "fi_co", "acdoca", "trennungsrechnung", "controlling", "ssb"],
        "aliases": ["Solution Design FI/CO", "Kaufmännische Prozesse SSB", "ACDOCA Lösungsdesign"]
    },
    r"03_SAP_EnterpriseArchitecture\SSB_Tool_Governance_Signavio_CALM.md": {
        "id": "ssb-tool-governance-signavio-calm",
        "title": "Tool-Governance: SAP Signavio, SAP Cloud ALM & SAP Enable Now",
        "type": "concept",
        "domain": "enterprise-architecture",
        "status": "verified",
        "summary": "BPMN 2.0 Modellierungs-Governance in Signavio, Test- und Release-Management in SAP Cloud ALM und Schulungscontent-Lifecycle in Enable Now.",
        "tags": ["tool_governance", "signavio", "cloud_alm", "enable_now", "bpmn", "ssb"],
        "aliases": ["Tool-Governance SSB", "Signavio CALM EnableNow", "BPMN Governance"]
    },
    r"04_Second_Brain_Zettelkasten\Retrospektive_Wintersemester_23_24.md": {
        "id": "retrospektive-wintersemester-23-24",
        "title": "Semester-Retrospektive: Wintersemester 2023/2024",
        "type": "zettel",
        "domain": "personal-growth",
        "status": "verified",
        "summary": "Akademische und persönliche Reflexion des Wintersemesters 2023/24 an der Universität Stuttgart, Learnings, Work-Life-Balance und Prüfungsstrategie.",
        "tags": ["retrospektive", "learnings", "studium", "wintersemester", "second_brain"],
        "aliases": ["WS 23/24 Retrospektive", "Semesterreflexion"]
    },
    r"04_Second_Brain_Zettelkasten\Trainingsplan_Visar.md": {
        "id": "trainingsplan-visar-4er-split",
        "title": "Visars 4er-Split Hypertrophie Trainingsplan",
        "type": "zettel",
        "domain": "personal-growth",
        "status": "active",
        "summary": "Strukturierter 4er-Split Trainingsplan (Brust/Bizeps, Beine/Bauch, Schultern/Trizeps, Rücken) mit Rote Beete Saft Pre-Workout und Regenerationsmanagement.",
        "tags": ["fitness", "trainingsplan", "hypertrophie", "bodybuilding", "health"],
        "aliases": ["Trainingsplan", "4er-Split", "Fitness Routine"]
    }
}

def build_vault_inventory():
    all_files = {}
    for r, ds, fs in os.walk(VAULT_DIR):
        if ".obsidian" in r:
            continue
        for f in fs:
            if f.endswith(".md"):
                bname = os.path.splitext(f)[0].lower()
                rel = os.path.relpath(os.path.join(r, f), VAULT_DIR)
                all_files[bname] = (f, rel, os.path.join(r, f))
    return all_files

def relocate_root_personal_files():
    zettel_dir = os.path.join(VAULT_DIR, "04_Second_Brain_Zettelkasten")
    os.makedirs(zettel_dir, exist_ok=True)
    
    # 1. Gewohnheiten.md
    gew_src = os.path.join(VAULT_DIR, "Gewohnheiten.md")
    gew_dst = os.path.join(zettel_dir, "Gewohnheiten.md")
    if os.path.exists(gew_src) and not os.path.exists(gew_dst):
        with open(gew_src, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.read().splitlines()
        clean_lines = [l.strip() for l in lines if l.strip()]
        body_items = "\n".join([f"- [ ] {l.lstrip('-* ')}" for l in clean_lines])
        
        content = f"""---
id: gewohnheiten-daily-routines
title: "Tägliche Routinen & Gewohnheiten"
type: zettel
domain: personal-growth
status: active
summary: "Persönlicher Gewohnheitstracker und tägliche Disziplin-Routinen für Körper, Geist und spirituelle Balance."
tags:
  - habits
  - routines
  - discipline
  - health
  - personal_growth
aliases:
  - Daily Habits
  - Gewohnheiten
last_updated: "2026-11-24"
---

# ⚡ Tägliche Routinen & Gewohnheiten

> [!SUMMARY] **Core Habits & Daily Non-Negotiables**
> Tägliche Disziplin- und Gesundheitsroutinen zur Maximierung von kognitivem Fokus, Energie und physischer Leistungsfähigkeit.

{body_items}
"""
        with open(gew_dst, "w", encoding="utf-8") as f:
            f.write(content)
        os.remove(gew_src)
        print("  [+] Moved and harmonized Gewohnheiten.md -> 04_Second_Brain_Zettelkasten/Gewohnheiten.md")

    # 2. NoFap.md
    nofap_src = os.path.join(VAULT_DIR, "NoFap.md")
    nofap_dst = os.path.join(zettel_dir, "NoFap.md")
    if os.path.exists(nofap_src) and not os.path.exists(nofap_dst):
        with open(nofap_src, "r", encoding="utf-8", errors="ignore") as f:
            orig = f.read()
        
        content = f"""---
id: nofap-dopamin-reset-protocol
title: "Dopamin Reset & NoFap Timeline Protokoll"
type: zettel
domain: personal-growth
status: verified
summary: "Phasenbasierte Neuro-Dopamin-Rekalibrierung, Testosteron-Entwicklung, Notfallprotokolle und mentale Resilienzphasen (Tag 1 bis 100+)."
tags:
  - dopamin_reset
  - neuroplasticity
  - nofap
  - mental_health
  - personal_growth
aliases:
  - Dopamin Reset
  - NoFap Timeline
  - Neuro-Rekalibrierung
last_updated: "2026-11-24"
---

# 🧠 Dopamin Reset & NoFap Timeline Protokoll

> [!SUMMARY] **Neurobiologischer Reset & Resilienz-Manifest**
> Systematische Dokumentation der Rekalibrierung des Belohnungssystems, der Dopaminrezeptoren-Dichte und mentaler Leistungsfähigkeit.

{orig.strip()}
"""
        with open(nofap_dst, "w", encoding="utf-8") as f:
            f.write(content)
        os.remove(nofap_src)
        print("  [+] Moved and harmonized NoFap.md -> 04_Second_Brain_Zettelkasten/NoFap.md")

def sanitize_math_logic_brackets(text, rel_path):
    """
    Replaces OCR predicate logic semantic brackets [[F]] with Unicode double-bracket ⟦F⟧
    only in theoretical computer science / logic sections to avoid broken wikilinks.
    """
    if "Modul_Seminar_Interdisziplinaer" not in rel_path and "Modul_Wissensverarbeitung" not in rel_path:
        return text
        
    def replace_logic(match):
        inner = match.group(1).strip()
        # If it's a known markdown note or file name, leave it as wikilink
        if len(inner) > 12 or "_" in inner or "/" in inner or inner.startswith("Modul_"):
            return match.group(0)
        # Check if inner looks like propositional/predicate formula or single variable
        logic_tokens = ["F", "F1", "F2", "G", "A", "t1", "tn", "Hund(x)", "Bellen(x)", "¬Beißen(x)", 
                        "¬F", "F1 ∧ F2", "F1 ∨ F2", "F1 ⇒ F2", "¬F1", "F1 ⇔ F2", "t", "x", 
                        "f(t1,...,tn)", "p(t1,...,tn)", "∀xG", "∃xG", "c", "n,k"]
        for lt in logic_tokens:
            if inner == lt or inner.startswith("∀") or inner.startswith("∃") or inner.startswith("¬"):
                return f"`⟦{inner}⟧`"
        return match.group(0)

    # Regex for wikilinks
    pattern = re.compile(r'\[\[(.*?)\]\]')
    return pattern.sub(replace_logic, text)

def canonicalize_wikilinks(text, all_files):
    """
    Canonicalizes all wikilinks in text to target actual existing note names without path prefixes,
    and maps conceptual broken links to authoritative vault notes.
    """
    # Fix escaped pipes in table wikilinks: [[target\|alias]] -> [[target|alias]]
    text = text.replace(r"\|", "|")
    
    # Fix Quantum information code bracket: [[n,k]] -> `⟦n,k⟧`
    text = text.replace("[[n,k]]", "`⟦n,k⟧`")

    def link_replacer(match):
        raw = match.group(1).strip()
        if "|" in raw:
            target_part, alias_part = raw.split("|", 1)
            target_part = target_part.strip()
            alias_part = alias_part.strip()
        else:
            target_part = raw
            alias_part = None

        anchor = ""
        if "#" in target_part:
            target_part, anchor = target_part.split("#", 1)
            anchor = "#" + anchor.strip()

        t_clean = target_part.strip().lower()
        if not t_clean:
            return match.group(0)

        # 1. Check conceptual map
        if t_clean in CANONICAL_CONCEPT_MAP:
            canon_name, auto_alias = CANONICAL_CONCEPT_MAP[t_clean]
            display = alias_part if alias_part else auto_alias
            return f"[[{canon_name}{anchor}|{display}]]"

        # 2. Check direct basename in vault
        bname = os.path.splitext(os.path.basename(target_part))[0].lower()
        if bname in all_files:
            actual_filename, rel, full = all_files[bname]
            canon_base = os.path.splitext(actual_filename)[0]
            if alias_part:
                return f"[[{canon_base}{anchor}|{alias_part}]]"
            elif "/" in target_part:
                return f"[[{canon_base}{anchor}]]"
            else:
                return f"[[{canon_base}{anchor}]]"

        # Return original if unresolved
        return match.group(0)

    pattern = re.compile(r'\[\[(.*?)\]\]')
    return pattern.sub(link_replacer, text)

def normalize_heading_hierarchy(text, title):
    """
    Ensures exactly one H1 at the top of the body, and demotes rogue H1 tags inside slide dumps.
    """
    # Separate frontmatter
    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', text, re.DOTALL)
    if fm_match:
        fm_block = fm_match.group(0)
        body = text[len(fm_block):]
    else:
        fm_block = ""
        body = text

    # Remove isolated hash on empty line
    body = re.sub(r'^#\s*$', '', body, flags=re.MULTILINE)

    lines = body.splitlines()
    new_lines = []
    found_first_h1 = False

    for line in lines:
        stripped = line.strip()
        if line.startswith("# ") and not line.startswith("##"):
            if not found_first_h1:
                found_first_h1 = True
                new_lines.append(line)
            else:
                # Check if it's an interview partner in SSB_Interviews or slide junk
                if re.match(r'^#\s+\d+\.\s+Interviewpartner', line):
                    new_lines.append("#" + line) # Demote to H2
                else:
                    new_lines.append("### " + line[2:].strip()) # Demote slide commands to H3
        elif stripped == "#":
            continue
        else:
            new_lines.append(line)

    # If no H1 found at all, prepend H1 matching title
    if not found_first_h1:
        new_lines.insert(0, f"# {title}\n")

    return fm_block + "\n".join(new_lines) + "\n"

def process_frontmatter(text, rel_path, default_title):
    """
    Guarantees rich, standardized YAML frontmatter for every note.
    """
    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', text, re.DOTALL)
    
    # Check if we have an explicit frontmatter override
    explicit = EXPLICIT_FRONTMATTER.get(rel_path, None)

    if explicit:
        tags_yaml = "\n".join([f"  - {t}" for t in explicit["tags"]])
        aliases_yaml = "\n".join([f"  - {a}" for a in explicit.get("aliases", [])])
        new_fm = f"""---
id: {explicit["id"]}
title: "{explicit["title"]}"
type: {explicit["type"]}
domain: {explicit["domain"]}
status: {explicit["status"]}
summary: "{explicit["summary"]}"
tags:
{tags_yaml}
aliases:
{aliases_yaml}
last_updated: "{explicit.get("last_updated", "2026-11-24")}"
---
"""
        if fm_match:
            body = text[len(fm_match.group(0)):]
            return new_fm + body.lstrip()
        else:
            return new_fm + "\n" + text.lstrip()

    if not fm_match:
        # Generate clean fallback frontmatter for missing note
        slug = os.path.splitext(os.path.basename(rel_path))[0].lower().replace("_", "-")
        clean_title = default_title or os.path.splitext(os.path.basename(rel_path))[0].replace("_", " ")
        new_fm = f"""---
id: {slug}
title: "{clean_title}"
type: concept
domain: enterprise-architecture
status: verified
summary: "Strukturierte Wissenseinheit und Fachdokumentation zu {clean_title} im Enterprise Architecture Knowledge Graph."
tags:
  - knowledge_graph
  - second_brain
  - enterprise_architecture
last_updated: "2026-11-24"
---
"""
        return new_fm + "\n" + text.lstrip()

    # If frontmatter exists, ensure standard fields are intact
    fm_content = fm_match.group(1)
    body = text[len(fm_match.group(0)):]
    
    # Add last_updated if missing
    if "last_updated:" not in fm_content:
        fm_content += f'\nlast_updated: "{datetime.now().strftime("%Y-%m-%d")}"'
    
    # Add domain if missing
    if "domain:" not in fm_content:
        if "02_Wirtschaftsinformatik" in rel_path:
            dom = "academic-curriculum"
        elif "03_SAP" in rel_path:
            dom = "sap-transformation"
        elif "01_Karriere" in rel_path:
            dom = "career-pmo"
        elif "DC1" in rel_path:
            dom = "datacenter-operations"
        else:
            dom = "second-brain"
        fm_content += f'\ndomain: {dom}'

    # Add type if missing
    if "type:" not in fm_content:
        if "MOC" in rel_path or "INDEX" in rel_path:
            ntype = "moc"
        elif "Modul_" in rel_path:
            ntype = "module"
        else:
            ntype = "concept"
        fm_content += f'\ntype: {ntype}'

    return f"---\n{fm_content.strip()}\n---\n" + body

def harmonize_vault():
    print("=" * 70)
    print("🚀 STARTING DATA SCIENCE OBSIDIAN VAULT HARMONIZATION")
    print("=" * 70)

    # Step 1: Relocate root personal notes
    print("\n[1/6] Relocating loose personal files from root...")
    relocate_root_personal_files()

    # Step 2: Build master file inventory
    all_files = build_vault_inventory()
    print(f"\n[2/6] Indexed {len(all_files)} Markdown files across Obsidian Vault.")

    # Step 3: Iterate through all files and harmonize
    print("\n[3/6] Applying Data Science transformations across all files:")
    print("      - YAML Schema Compliance")
    print("      - Wikilink Canonicalization & Edge Healing")
    print("      - Mathematical Logic Semantic Brackets")
    print("      - AST Heading Hierarchy Normalization")

    modified_count = 0

    for bname, (fname, rel, fullpath) in sorted(all_files.items()):
        with open(fullpath, "r", encoding="utf-8", errors="ignore") as f:
            original_text = f.read()

        # Extract title from first H1 or filename
        h1_match = re.search(r'^#\s+(.*)', original_text, re.MULTILINE)
        default_title = h1_match.group(1).strip() if h1_match else os.path.splitext(fname)[0].replace("_", " ")

        # 1. Frontmatter
        step1_text = process_frontmatter(original_text, rel, default_title)

        # 2. Logic brackets
        step2_text = sanitize_math_logic_brackets(step1_text, rel)

        # 3. Canonicalize wikilinks
        step3_text = canonicalize_wikilinks(step2_text, all_files)

        # 4. Normalize headings
        final_text = normalize_heading_hierarchy(step3_text, default_title)

        if final_text != original_text:
            with open(fullpath, "w", encoding="utf-8") as f:
                f.write(final_text)
            modified_count += 1

    print(f"  [OK] Harmonization complete! {modified_count} files enriched and updated.")

    # Step 4: Generate Graph Manifest for LLMs / Vector DBs
    print("\n[4/6] Generating Knowledge Graph Semantic Manifest...")
    updated_files = build_vault_inventory()
    nodes = []
    edges = []

    for bname, (fname, rel, fullpath) in updated_files.items():
        with open(fullpath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Parse frontmatter
        fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        fm_dict = {}
        if fm_match:
            for line in fm_match.group(1).splitlines():
                if ":" in line and not line.strip().startswith("-"):
                    k, v = line.split(":", 1)
                    fm_dict[k.strip()] = v.strip().strip('"\'')

        node_id = fm_dict.get("id", bname)
        title = fm_dict.get("title", fname)
        domain = fm_dict.get("domain", "general")
        ntype = fm_dict.get("type", "concept")
        summary = fm_dict.get("summary", "")
        word_count = len(content.split())

        nodes.append({
            "id": node_id,
            "label": title,
            "file": rel,
            "type": ntype,
            "domain": domain,
            "summary": summary,
            "words": word_count
        })

        # Edges
        links = re.findall(r'\[\[(.*?)\]\]', content)
        for l in links:
            raw_target = l.split("|")[0].split("#")[0].strip().lower()
            if raw_target in updated_files:
                target_base = raw_target
                target_id = updated_files[target_base][0].replace(".md", "").lower()
                edges.append({
                    "source": node_id,
                    "target": target_id,
                    "relation": "references"
                })

    manifest = {
        "vault_name": "Visar Murseli | Enterprise Knowledge Hub & Second Brain",
        "generated_at": datetime.now().isoformat(),
        "total_nodes": len(nodes),
        "total_edges": len(edges),
        "nodes": nodes,
        "edges": edges
    }

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"  [OK] Graph Manifest saved: {MANIFEST_PATH} ({len(nodes)} nodes, {len(edges)} verified edges)")

if __name__ == "__main__":
    harmonize_vault()
