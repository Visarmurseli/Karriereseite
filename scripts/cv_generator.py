# -*- coding: utf-8 -*-
"""
Executive ATS-Ready CV Generator (DOCX, Vector PDF & Markdown) for Visar Murseli.
Operationalizes all CV De-Risking recommendations (zero coding-trap wording,
1,0 Master thesis prominence, IT-PMO framing, B.Sc. 180 ECTS + TOGAF 9 ADM)
into clean A4 deliverables without brittle Word textboxes.
"""

import io
import os
import re
import gc
import html
import tempfile
from copy import deepcopy

import docx
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls
import pymupdf


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENV_PATH = os.path.join(BASE_DIR, ".env")
SOURCE_CV_DOCX = os.path.join(BASE_DIR, "00_Aktuelle_Bewerbungsunterlagen", "Lebenslauf_Murseli_Vsar.docx")


def _load_local_cv_contact():
    """Loads personal CV contact details at runtime from local .env or local source DOCX (never stored in Git)."""
    email = os.environ.get("CV_CONTACT_EMAIL", "").strip()
    phone = os.environ.get("CV_CONTACT_PHONE", "").strip()
    address = os.environ.get("CV_CONTACT_ADDRESS", "").strip()
    if not (email and phone and address) and os.path.exists(ENV_PATH):
        try:
            with open(ENV_PATH, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    s = line.strip()
                    if s.startswith("CV_CONTACT_EMAIL=") and not email:
                        email = s.split("=", 1)[1].strip().strip('"\'')
                    elif s.startswith("CV_CONTACT_PHONE=") and not phone:
                        phone = s.split("=", 1)[1].strip().strip('"\'')
                    elif s.startswith("CV_CONTACT_ADDRESS=") and not address:
                        address = s.split("=", 1)[1].strip().strip('"\'')
        except Exception:
            pass
    if not (email and phone and address) and os.path.exists(SOURCE_CV_DOCX):
        try:
            import zipfile, xml.etree.ElementTree as ET
            with zipfile.ZipFile(SOURCE_CV_DOCX) as z:
                root = ET.fromstring(z.read("word/document.xml"))
            ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
            for p in root.findall(".//w:p", ns)[:8]:
                line = "".join(t.text for t in p.findall(".//w:t", ns) if t.text).strip()
                if "@" in line and "•" in line:
                    parts = [x.strip() for x in line.split("•") if x.strip()]
                    if len(parts) >= 1 and not email:
                        email = parts[0]
                    if len(parts) >= 2 and not phone:
                        phone = parts[1]
                    if len(parts) >= 3 and not address:
                        address = parts[2]
                    break
        except Exception:
            pass
    return {
        "email": email or "kontakt@beispiel.de",
        "phone": phone or "",
        "address": address or "Ludwigsburg / Region Stuttgart",
    }


BASE_CV_PROFILE = {
    "preset": "universal",
    "theme": "modern-cobalt",
    "compact": True,
    "showSummary": True,
    "showMasterDetails": True,
    "showBachelor": True,
    "showVismuv": True,
    "showPdr": False,
    "showExtra": True,
    "header": {
        "name": "Visar Murseli",
        "subtitle": "M.Sc. Wirtschaftsinformatik (1,6) • SAP S/4HANA Transformation & IT-PMO",
        "email": "",
        "phone": "",
        "address": "Ludwigsburg / Region Stuttgart",
        "links": "Portfolio: S/4HANA Career OS • Ludwigsburg / Region Stuttgart",
    },
    "summary": (
        "Wirtschaftsinformatiker (M.Sc. 1,6, Masterarbeit 1,0) mit 36 Monaten Enterprise-Praxiserfahrung "
        "in der SAP S/4HANA-Transformation (24 Monate IT-PMO & Lösungsdesign) und im 24/7 ITIL 4 Servicebetrieb "
        "(12 Monate Rechenzentrums-INOC). Spezialisiert auf Clean-Core-Governance, End-to-End Prozessdesign "
        "(SAP Signavio, Cloud ALM) sowie revisionssichere ERP-Datenmigration."
    ),
    "education": [
        {
            "id": "msc",
            "institution": "Universität Stuttgart",
            "period": "2023 – 09/2026",
            "degree": "Master of Science (M.Sc.), Wirtschaftsinformatik – Gesamtnote: 1,6 „gut“ (120 ECTS)",
            "details": [
                "Masterarbeit (Note 1,0): „Kritische Erfolgsfaktoren in der Transformation großer ERP-Systeme: Eine Untersuchung am Beispiel der Plattformisierung von SAP S/4HANA“ (12 Experteninterviews, Inhaltsanalyse nach Mayring)",
                "Vertiefung: Enterprise Architecture & Software-Architektur (1,7), Applied AI (1,7), Digitale Nachhaltigkeit (1,0), Smart Service Blueprinting (1,3)",
            ],
        },
        {
            "id": "bsc",
            "institution": "Universität Stuttgart",
            "period": "2019 – 2023",
            "degree": "Bachelor of Science (B.Sc.), Wirtschaftsinformatik – Gesamtnote: 3,0 (180 ECTS)",
            "details": [
                "Bachelorarbeit (Note 1,7): „Die Bedeutung von Boundary Resources in Low-Code Entwicklungsplattformen (OutSystems & Mendix)“",
                "Kernfächer: Informationssysteme im E-Business (Bestnote 1,0), Geschäftsprozessmodellierung (BPMN 2.0 / ERM / UML), Datenbanken",
            ],
        },
    ],
    "experience": [
        {
            "id": "ssb",
            "company": "Stuttgarter Straßenbahnen AG (SSB AG)",
            "period": "05/2024 – 04/2026",
            "role": "IT-PMO & Lösungsdesign SAP S/4HANA Transformation (Werkstudent, 24 Monate)",
            "bullets": [
                "Multiprojekt-Governance & Teilprojektsteuerung (TP1–TP5) inklusive MS-Project-Meilensteinplanung, Ressourcenplanung und Fortschrittsanalysen",
                "Analyse und Dokumentation kaufmännischer Geschäftsprozesse im SAP S/4HANA-Umfeld zur Erstellung des Solution Design Documents (ACDOCA, Trennungsrechnung nach EU-VO 1370/2007)",
                "Tool-Governance & End-to-End Traceability: Erstellung des verbindlichen Quickguides „SAP Cloud ALM How2Handle“, Prozessstandardisierung in SAP Signavio (BPMN 2.0) sowie Übergabekonzept für SAP Enable Now",
                "Unterstützung der Datenmigrations- und Schnittstellenkonzeption (LTMC, Business-Partner-/CVI-Harmonisierung, Clean-Core-Entkopplung von Subsystemen wie PATRIS, xSuite und d.velop)",
            ],
        },
        {
            "id": "dc1",
            "company": "Datacenter One GmbH",
            "period": "05/2023 – 04/2024",
            "role": "ITIL 4 Service Operations im 24/7 Information Network Operation Center (Werkstudent, 12 Monate)",
            "bullets": [
                "Prozessorientiertes IT-Service- und Incident-Management nach ITIL 4 als Single Point of Contact (SPoC) unter strengen SLA-Vorgaben (99,99 %)",
                "Konzeption und Aufbau einer standardisierten Wissensdatenbank sowie Betriebs-SOPs für das 24/7 Rechenzentrums-Monitoring (Core-Netzwerke, USV, PRTG)",
                "Prozessdesign für Hardware Lifecycle Management (100+ Systeme) sowie Service-Transition des Carriermanagements in den Leitstandsbetrieb",
            ],
        },
        {
            "id": "pdr",
            "company": "PDR Team GmbH",
            "period": "09/2026 – 11/2026",
            "role": "Technisches Fahrzeug-Scanning & Schadensmanagement (Übergangsbeschäftigung)",
            "bullets": [
                "Strukturierte Datenerfassung, Prozessdokumentation und operative Qualitätssicherung im technischen Scanning-Betrieb nach Abschluss des Masterstudiums",
            ],
        },
    ],
    "projects": [
        {
            "id": "vismuv",
            "title": "VISMUV (Gründer & Inhaber, nebenberuflich)",
            "period": "ab 11/2026",
            "bullets": [
                "Eigenverantwortlicher Aufbau und kaufmännische Steuerung von Dienstleistungsprozessen (Fahrzeugüberführungen, Kurierlogistik, Kundenservice) inkl. Kalkulation und Disposition",
            ],
        },
        {
            "id": "klingele",
            "title": "Innovationsprojekt: KI-gestützte Patentmanagement-Plattform (Verpackungsindustrie)",
            "period": "02/2024",
            "bullets": [
                "Entwicklung und wirtschaftliche Konzeption eines hybriden SaaS-/Beratungs-Geschäftsmodells inkl. Business-Process-Automation-Machbarkeitsprüfung (UiPath PDD/Prozesskosten) und BPMN-Prozessmodellierung (Note 2,0)",
            ],
        },
        {
            "id": "schmalz",
            "title": "Automatisierungsprojekt: Optimierung der Abfallbilanz & Nachhaltigkeitsberichterstattung (CSRD)",
            "period": "07/2024",
            "bullets": [
                "Modellierung von Ist-Prozessen im industriellen Abfallmanagement sowie PowerShell-gestützte Datenextraktion zur Eliminierung manueller Eingabefehler und Reduktion des Bilanzierungsaufwands (Note 1,0)",
            ],
        },
        {
            "id": "portfolio",
            "title": "Privatprojekt: Interactive S/4HANA Knowledge Hub & Portfolio-Website",
            "period": "seit 2023",
            "bullets": [
                "Konzeption und Betrieb einer responsiven Single-Page-Application (GitHub Pages) zur strukturierten Präsentation von SAP-S/4HANA-, EAM- und akademischen Transformationsprojekten",
            ],
        },
    ],
    "skills": {
        "erp_governance": (
            "SAP S/4HANA Transformation Governance, Clean Core & SAP BTP-Architektur, Universal Journal (ACDOCA), "
            "SAP Cloud ALM, SAP Signavio (BPMN 2.0), SAP Enable Now, SAP Migration Cockpit (LTMC / CVI), ITIL 4, TOGAF 9 ADM"
        ),
        "data_analysis": (
            "Architektur- & Datenverständnis (Relationale Datenmodelle, SQL-Validierung), "
            "Business Process Automation & Machbarkeitsanalyse (BPMN 2.0, Prozesskosten-Kalkulation), Datenanalyse (Python-Auswertung, PowerShell-Automatisierung)"
        ),
        "pmo_tools": (
            "Multiprojekt-Steuerung (MS Project), Solution Design Dokumentation, Stakeholder- & Partnersteuerung (Nagarro, Evora, Axians), Microsoft 365 & MindManager"
        ),
        "languages": "Deutsch (Muttersprache), Albanisch (Muttersprache), Englisch (C1 – verhandlungssicher), Französisch & Spanisch (Grundkenntnisse)",
    },
    "extra": [
        "Zertifizierung: TOGAF 9 ADM Intensivkurs (Scape Consulting, Universität Stuttgart, 16.01.2020)",
        "Ehrenamt: Geflüchtetenhilfe (Refugees Welcome, HVF) sowie schulische Hausaufgabenbetreuung",
    ],
}


def get_default_cv_presets():
    """Returns curated role-specific optimized CV presets strictly aligned with De-Risking rules."""
    contact = _load_local_cv_contact()
    universal = deepcopy(BASE_CV_PROFILE)
    universal["header"].update(contact)

    consulting = deepcopy(universal)
    consulting["preset"] = "consulting"
    consulting["header"]["subtitle"] = "Junior SAP S/4HANA Transformation & Clean Core Consultant • M.Sc. (1,6)"
    consulting["summary"] = (
        "Wirtschaftsinformatiker (M.Sc. 1,6, Masterarbeit 1,0 zur Plattformisierung von SAP S/4HANA) mit "
        "24 Monaten Projektpraxis in einer Greenfield RISE-with-SAP-Transformation (SSB AG) und 12 Monaten "
        "ITIL 4 Rechenzentrumsbetrieb. Stark in Fit-to-Standard-Governance, SAP Cloud ALM, Signavio und BTP-Entkopplung."
    )

    audit_iam = deepcopy(universal)
    audit_iam["preset"] = "audit_iam"
    audit_iam["header"]["subtitle"] = "IT-Audit, IKS & SAP Governance / IAM Consultant • M.Sc. (1,6)"
    audit_iam["summary"] = (
        "Wirtschaftsinformatiker (M.Sc. 1,6, Masterarbeit 1,0) mit tiefem Praxisverständnis für revisionssichere "
        "S/4HANA-Prozesse, Internes Kontrollsystem (IKS), Trennungsrechnung nach EU-VO 1370/2007 sowie "
        "Eröffnungsbilanz- und Datenmigrations-Abstimmung (LTMC/CVI Saldo 0,00 €) und ITIL 4 Operations."
    )
    audit_iam["experience"][0]["bullets"][1] = (
        "Revisionssicheres Lösungsdesign im kaufmännischen Bereich (FI/CO Universal Journal ACDOCA, "
        "Trennungsrechnung EU 1370/2007, Compliance & Mitbestimmungs-Alignment)"
    )

    trainee_eam = deepcopy(universal)
    trainee_eam["preset"] = "trainee_eam"
    trainee_eam["header"]["subtitle"] = "IT- / Management-Trainee Enterprise Architecture & Digital Transformation • M.Sc. (1,6)"
    trainee_eam["summary"] = (
        "Master of Science Wirtschaftsinformatik (1,6; Masterarbeit 1,0) mit TOGAF 9 ADM Zertifizierung, "
        "24 Monaten IT-PMO in der ERP-Großtransformation und 12 Monaten 24/7 ITIL 4 Service Operations. "
        "Verbindet unternehmerisches Denken (VISMUV), CSRD-Automatisierung (1,0) und Plattform-Governance."
    )

    return {
        "universal": universal,
        "consulting": consulting,
        "audit_iam": audit_iam,
        "trainee_eam": trainee_eam,
    }


def _active_sections(cv_data):
    """Filters visible sections according to user toggles cleanly for all exporters."""
    edu_list = []
    for ed in (cv_data.get("education") or []):
        if ed.get("id") == "bsc" and not cv_data.get("showBachelor", True):
            continue
        item = dict(ed)
        if ed.get("id") == "msc" and not cv_data.get("showMasterDetails", True):
            item["details"] = item.get("details", [])[:1]
        edu_list.append(item)

    exp_list = []
    for ex in (cv_data.get("experience") or []):
        if ex.get("id") == "pdr" and not cv_data.get("showPdr", False):
            continue
        bullets = [b.strip() for b in (ex.get("bullets") or []) if str(b).strip()]
        if cv_data.get("compact", True):
            bullets = bullets[:3] if ex.get("id") == "ssb" else bullets[:2]
        exp_list.append({**ex, "bullets": bullets})

    proj_list = []
    for pr in (cv_data.get("projects") or []):
        if pr.get("id") == "vismuv" and not cv_data.get("showVismuv", True):
            continue
        if cv_data.get("compact", True) and pr.get("id") == "portfolio":
            continue
        bullets = [b.strip() for b in (pr.get("bullets") or []) if str(b).strip()]
        proj_list.append({**pr, "bullets": bullets})

    return edu_list, exp_list, proj_list


def _set_cell_margins(cell, top=0, bottom=0, left=0, right=0):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for side, val in (("top", top), ("bottom", bottom), ("left", left), ("right", right)):
        node = OxmlElement(f"w:{side}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)


def _set_borderless_table(table):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        '<w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/>'
        '<w:right w:val="none"/><w:insideH w:val="none"/><w:insideV w:val="none"/>'
        "</w:tblBorders>"
    )
    tblPr.append(borders)


def _add_section_heading(doc, title, accent_hex="1E40AF", compact=True):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4 if compact else 9)
    p.paragraph_format.space_after = Pt(1.5 if compact else 4)
    p.paragraph_format.keep_with_next = True
    pPr = p._p.get_or_add_pPr()
    pBdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'<w:bottom w:val="single" w:sz="6" w:space="1" w:color="{accent_hex}"/>'
        "</w:pBdr>"
    )
    pPr.append(pBdr)
    run = p.add_run(title.upper())
    run.bold = True
    run.font.name = "Calibri"
    run.font.size = Pt(8.8 if compact else 10.5)
    run.font.color.rgb = RGBColor.from_string(accent_hex)


def _add_row_header(doc, left_title, right_period, sub_role="", accent_hex="0F172A", compact=True):
    tbl = doc.add_table(rows=1, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    _set_borderless_table(tbl)

    row = tbl.rows[0]
    trPr = row._tr.get_or_add_trPr()
    trPr.append(OxmlElement("w:cantSplit"))

    c_left, c_right = row.cells[0], row.cells[1]
    c_left.width = Cm(14.5)
    c_right.width = Cm(3.5)
    _set_cell_margins(c_left, top=4, bottom=0, left=0, right=60)
    _set_cell_margins(c_right, top=4, bottom=0, left=0, right=0)

    p_l = c_left.paragraphs[0]
    p_l.paragraph_format.space_before = Pt(0)
    p_l.paragraph_format.space_after = Pt(0 if sub_role else 1)
    p_l.paragraph_format.keep_with_next = True
    r_l = p_l.add_run(left_title)
    r_l.bold = True
    r_l.font.name = "Calibri"
    r_l.font.size = Pt(9.0 if compact else 10.5)
    r_l.font.color.rgb = RGBColor(15, 23, 42)

    if sub_role:
        p_sub = c_left.add_paragraph()
        p_sub.paragraph_format.space_before = Pt(0)
        p_sub.paragraph_format.space_after = Pt(1)
        p_sub.paragraph_format.keep_with_next = True
        r_sub = p_sub.add_run(sub_role)
        r_sub.italic = True
        r_sub.font.name = "Calibri"
        r_sub.font.size = Pt(8.3 if compact else 9.5)
        r_sub.font.color.rgb = RGBColor.from_string(accent_hex)

    p_r = c_right.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_r.paragraph_format.space_before = Pt(0)
    p_r.paragraph_format.space_after = Pt(0)
    r_r = p_r.add_run(right_period)
    r_r.bold = True
    r_r.font.name = "Calibri"
    r_r.font.size = Pt(8.2 if compact else 9.3)
    r_r.font.color.rgb = RGBColor(71, 85, 105)


def _add_bullet(doc, text, compact=True):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.38)
    p.paragraph_format.first_line_indent = Cm(-0.22)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(1.0 if compact else 2.2)
    p.paragraph_format.line_spacing = 1.03 if compact else 1.14
    r_dot = p.add_run("•  ")
    r_dot.bold = True
    r_dot.font.name = "Calibri"
    r_dot.font.size = Pt(8.1 if compact else 9.3)
    r_dot.font.color.rgb = RGBColor(51, 65, 85)

    r_txt = p.add_run(text)
    r_txt.font.name = "Calibri"
    r_txt.font.size = Pt(8.1 if compact else 9.4)
    r_txt.font.color.rgb = RGBColor(30, 41, 59)


def build_cv_docx(cv_data):
    """Generates a cleanly typeset, ATS-safe Word (.docx) CV matching executive typography."""
    compact = bool(cv_data.get("compact", True))
    theme = cv_data.get("theme", "modern-cobalt")
    accent_hex = "1E40AF" if theme == "modern-cobalt" else "1E293B"
    hdr = cv_data.get("header") or {}
    edu_list, exp_list, proj_list = _active_sections(cv_data)
    skills = cv_data.get("skills") or {}
    extra = cv_data.get("extra") or []

    doc = docx.Document()
    sec = doc.sections[0]
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.top_margin = Cm(1.05 if compact else 1.55)
    sec.bottom_margin = Cm(0.95 if compact else 1.45)
    sec.left_margin = Cm(1.5 if compact else 1.6)
    sec.right_margin = Cm(1.5 if compact else 1.6)

    # Name & Subtitle
    p_name = doc.add_paragraph()
    p_name.paragraph_format.space_before = Pt(0)
    p_name.paragraph_format.space_after = Pt(1.0)
    r_name = p_name.add_run(hdr.get("name", "Visar Murseli"))
    r_name.bold = True
    r_name.font.name = "Calibri"
    r_name.font.size = Pt(17 if compact else 21)
    r_name.font.color.rgb = RGBColor(15, 23, 42)

    sub = (hdr.get("subtitle") or "").strip()
    if sub:
        p_sub = doc.add_paragraph()
        p_sub.paragraph_format.space_before = Pt(0)
        p_sub.paragraph_format.space_after = Pt(1.5)
        r_sub = p_sub.add_run(sub)
        r_sub.bold = True
        r_sub.font.name = "Calibri"
        r_sub.font.size = Pt(9.0 if compact else 10.5)
        r_sub.font.color.rgb = RGBColor.from_string(accent_hex)

    # Contact line
    contact_parts = [hdr.get("email", ""), hdr.get("phone", ""), hdr.get("address", ""), hdr.get("links", "")]
    contact_str = "  •  ".join(x.strip() for x in contact_parts if x and str(x).strip())
    p_c = doc.add_paragraph()
    p_c.paragraph_format.space_before = Pt(0)
    p_c.paragraph_format.space_after = Pt(2.5 if compact else 6)
    r_c = p_c.add_run(contact_str)
    r_c.font.name = "Calibri"
    r_c.font.size = Pt(8.0 if compact else 9.0)
    r_c.font.color.rgb = RGBColor(71, 85, 105)

    # Executive Summary
    if cv_data.get("showSummary", True) and (cv_data.get("summary") or "").strip():
        _add_section_heading(doc, "Kurzprofil", accent_hex, compact)
        p_sum = doc.add_paragraph()
        p_sum.paragraph_format.space_before = Pt(0)
        p_sum.paragraph_format.space_after = Pt(1.5)
        p_sum.paragraph_format.line_spacing = 1.05 if compact else 1.12
        r_sum = p_sum.add_run(cv_data["summary"].strip())
        r_sum.font.name = "Calibri"
        r_sum.font.size = Pt(8.2 if compact else 9.5)
        r_sum.font.color.rgb = RGBColor(30, 41, 59)

    # Berufserfahrung
    if exp_list:
        _add_section_heading(doc, "Berufserfahrung", accent_hex, compact)
        for ex in exp_list:
            _add_row_header(doc, ex.get("company", ""), ex.get("period", ""), ex.get("role", ""), accent_hex, compact)
            for b in ex.get("bullets", []):
                _add_bullet(doc, b, compact)

    # Studium
    if edu_list:
        _add_section_heading(doc, "Studium", accent_hex, compact)
        for ed in edu_list:
            _add_row_header(doc, ed.get("institution", ""), ed.get("period", ""), ed.get("degree", ""), accent_hex, compact)
            for d in ed.get("details", []):
                _add_bullet(doc, d, compact)

    # Projekte & Unternehmertum
    if proj_list:
        _add_section_heading(doc, "Projekte & Unternehmertum", accent_hex, compact)
        for pr in proj_list:
            _add_row_header(doc, pr.get("title", ""), pr.get("period", ""), "", accent_hex, compact)
            for b in pr.get("bullets", []):
                _add_bullet(doc, b, compact)

    # Qualifikationen
    _add_section_heading(doc, "Qualifikationen & Kompetenzen", accent_hex, compact)
    skill_rows = [
        ("ERP & Architektur-Governance:", skills.get("erp_governance", "")),
        ("Daten & Prozessautomatisierung:", skills.get("data_analysis", "")),
        ("PMO, Steuerung & Tools:", skills.get("pmo_tools", "")),
        ("Sprachen:", skills.get("languages", "")),
    ]
    for label, val in skill_rows:
        if not str(val).strip():
            continue
        p_sk = doc.add_paragraph()
        p_sk.paragraph_format.space_before = Pt(0)
        p_sk.paragraph_format.space_after = Pt(1.0 if compact else 2.2)
        p_sk.paragraph_format.line_spacing = 1.03 if compact else 1.14
        r_lbl = p_sk.add_run(label + " ")
        r_lbl.bold = True
        r_lbl.font.name = "Calibri"
        r_lbl.font.size = Pt(8.1 if compact else 9.3)
        r_lbl.font.color.rgb = RGBColor(15, 23, 42)
        r_val = p_sk.add_run(str(val).strip())
        r_val.font.name = "Calibri"
        r_val.font.size = Pt(8.1 if compact else 9.3)
        r_val.font.color.rgb = RGBColor(30, 41, 59)

    # Zertifizierung & Ehrenamt
    if cv_data.get("showExtra", True) and extra:
        _add_section_heading(doc, "Zertifizierung & Engagement", accent_hex, compact)
        for item in extra:
            if str(item).strip():
                _add_bullet(doc, str(item).strip(), compact)

    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()


def build_cv_pdf(cv_data):
    """Generates a selectable vector A4 PDF CV using PyMuPDF Story HTML-to-PDF rendering."""
    compact = bool(cv_data.get("compact", True))
    theme = cv_data.get("theme", "modern-cobalt")
    accent = "#1E40AF" if theme == "modern-cobalt" else "#1E293B"
    sub_accent = "#2563EB" if theme == "modern-cobalt" else "#334155"
    hdr = cv_data.get("header") or {}
    edu_list, exp_list, proj_list = _active_sections(cv_data)
    skills = cv_data.get("skills") or {}
    extra = cv_data.get("extra") or []

    def esc(val):
        return html.escape(str(val or "").strip())

    contact_parts = [hdr.get("email", ""), hdr.get("phone", ""), hdr.get("address", ""), hdr.get("links", "")]
    contact_str = " &bull; ".join(esc(x) for x in contact_parts if str(x or "").strip())

    body_fs = "7.95pt" if compact else "9.4pt"
    body_lh = "1.20" if compact else "1.34"
    head_mt = "5.2pt" if compact else "11pt"
    li_mb = "0.9pt" if compact else "3pt"
    entry_mb = "2.6pt" if compact else "5.5pt"

    parts = [
        f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
body {{ font-family: Helvetica, Arial, sans-serif; color: #1E293B; font-size: {body_fs}; line-height: {body_lh}; margin: 0; padding: 0; }}
.name {{ font-size: {"16.5pt" if compact else "19.5pt"}; font-weight: bold; color: #0F172A; margin: 0 0 1pt 0; letter-spacing: -0.3pt; }}
.subtitle {{ font-size: {"8.9pt" if compact else "10pt"}; font-weight: bold; color: {sub_accent}; margin: 0 0 1.5pt 0; }}
.contact {{ font-size: {"7.6pt" if compact else "8.3pt"}; color: #475569; margin: 0 0 {"3.5pt" if compact else "6pt"} 0; }}
h2 {{ font-size: {"8.3pt" if compact else "9.3pt"}; font-weight: bold; color: {accent}; text-transform: uppercase; letter-spacing: 0.8pt; border-bottom: 0.85pt solid {accent}; padding-bottom: 1pt; margin: {head_mt} 0 {"2.2pt" if compact else "4pt"} 0; }}
.entry {{ margin-bottom: {entry_mb}; }}
table.row {{ width: 100%; border-collapse: collapse; margin: 0; padding: 0; }}
td.left {{ font-weight: bold; color: #0F172A; font-size: {"8.6pt" if compact else "9.5pt"}; padding: 0; text-align: left; vertical-align: top; }}
td.right {{ font-weight: bold; color: #475569; font-size: {"7.8pt" if compact else "8.6pt"}; padding: 0; text-align: right; white-space: nowrap; vertical-align: top; width: 95pt; }}
.role {{ font-style: italic; color: {sub_accent}; font-size: {"8.1pt" if compact else "9.0pt"}; margin: 0.3pt 0 1.2pt 0; }}
ul {{ margin: 1pt 0 1.5pt 11pt; padding: 0; }}
li {{ margin: 0 0 {li_mb} 0; }}
.skill {{ margin: 0 0 {"1.3pt" if compact else "2.5pt"} 0; }}
.summary {{ margin: 0 0 {"2pt" if compact else "3pt"} 0; text-align: left; }}
</style></head><body>"""
    ]

    parts.append(f'<div class="name">{esc(hdr.get("name", "Visar Murseli"))}</div>')
    if (hdr.get("subtitle") or "").strip():
        parts.append(f'<div class="subtitle">{esc(hdr.get("subtitle"))}</div>')
    parts.append(f'<div class="contact">{contact_str}</div>')

    if cv_data.get("showSummary", True) and (cv_data.get("summary") or "").strip():
        parts.append("<h2>Kurzprofil</h2>")
        parts.append(f'<p class="summary">{esc(cv_data["summary"])}</p>')

    if exp_list:
        parts.append("<h2>Berufserfahrung</h2>")
        for ex in exp_list:
            parts.append('<div class="entry">')
            parts.append(
                f'<table class="row"><tr><td class="left">{esc(ex.get("company"))}</td>'
                f'<td class="right">{esc(ex.get("period"))}</td></tr></table>'
            )
            if ex.get("role"):
                parts.append(f'<div class="role">{esc(ex.get("role"))}</div>')
            if ex.get("bullets"):
                parts.append("<ul>" + "".join(f"<li>{esc(b)}</li>" for b in ex["bullets"]) + "</ul>")
            parts.append("</div>")

    if edu_list:
        parts.append("<h2>Studium</h2>")
        for ed in edu_list:
            parts.append('<div class="entry">')
            parts.append(
                f'<table class="row"><tr><td class="left">{esc(ed.get("institution"))}</td>'
                f'<td class="right">{esc(ed.get("period"))}</td></tr></table>'
            )
            if ed.get("degree"):
                parts.append(f'<div class="role">{esc(ed.get("degree"))}</div>')
            if ed.get("details"):
                parts.append("<ul>" + "".join(f"<li>{esc(d)}</li>" for d in ed["details"]) + "</ul>")
            parts.append("</div>")

    if proj_list:
        parts.append("<h2>Projekte &amp; Unternehmertum</h2>")
        for pr in proj_list:
            parts.append('<div class="entry">')
            parts.append(
                f'<table class="row"><tr><td class="left">{esc(pr.get("title"))}</td>'
                f'<td class="right">{esc(pr.get("period"))}</td></tr></table>'
            )
            if pr.get("bullets"):
                parts.append("<ul>" + "".join(f"<li>{esc(b)}</li>" for b in pr["bullets"]) + "</ul>")
            parts.append("</div>")

    parts.append("<h2>Qualifikationen &amp; Kompetenzen</h2>")
    for label, key in (
        ("ERP &amp; Architektur-Governance", "erp_governance"),
        ("Daten &amp; Prozessautomatisierung", "data_analysis"),
        ("PMO, Steuerung &amp; Tools", "pmo_tools"),
        ("Sprachen", "languages"),
    ):
        val = str(skills.get(key) or "").strip()
        if val:
            parts.append(f'<p class="skill"><strong>{label}:</strong> {esc(val)}</p>')

    if cv_data.get("showExtra", True) and extra:
        parts.append("<h2>Zertifizierung &amp; Engagement</h2>")
        parts.append("<ul>" + "".join(f"<li>{esc(i)}</li>" for i in extra if str(i).strip()) + "</ul>")

    parts.append("</body></html>")
    html_doc = "\n".join(parts)

    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".pdf")
    os.close(tmp_fd)
    writer = None
    try:
        story = pymupdf.Story(html=html_doc)
        writer = pymupdf.DocumentWriter(tmp_path)
        mediabox = pymupdf.paper_rect("a4")
        where = mediabox + ((32, 22, -32, -20) if compact else (38, 32, -38, -30))
        more = True
        while more:
            dev = writer.begin_page(mediabox)
            more, _ = story.place(where)
            story.draw(dev, None)
            writer.end_page()
        writer.close()
        writer = None
        gc.collect()
        with open(tmp_path, "rb") as f:
            return f.read()
    finally:
        if writer is not None:
            try:
                writer.close()
            except Exception:
                pass
            del writer
            gc.collect()
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            pass


def build_cv_markdown(cv_data):
    """Exports the optimized CV as clean structured Markdown."""
    hdr = cv_data.get("header") or {}
    edu_list, exp_list, proj_list = _active_sections(cv_data)
    skills = cv_data.get("skills") or {}
    extra = cv_data.get("extra") or []

    lines = [
        f"# {hdr.get('name', 'Visar Murseli')}",
        f"**{hdr.get('subtitle', '')}**",
        " • ".join(x for x in (hdr.get("email"), hdr.get("phone"), hdr.get("address"), hdr.get("links")) if x),
        "",
    ]
    if cv_data.get("showSummary", True) and (cv_data.get("summary") or "").strip():
        lines.extend(["## Kurzprofil", cv_data["summary"].strip(), ""])

    if exp_list:
        lines.append("## Berufserfahrung")
        for ex in exp_list:
            lines.append(f"### {ex.get('company', '')} ({ex.get('period', '')})")
            if ex.get("role"):
                lines.append(f"*{ex['role']}*")
            lines.extend(f"- {b}" for b in ex.get("bullets", []))
            lines.append("")

    if edu_list:
        lines.append("## Studium")
        for ed in edu_list:
            lines.append(f"### {ed.get('institution', '')} ({ed.get('period', '')})")
            if ed.get("degree"):
                lines.append(f"*{ed['degree']}*")
            lines.extend(f"- {d}" for d in ed.get("details", []))
            lines.append("")

    if proj_list:
        lines.append("## Projekte & Unternehmertum")
        for pr in proj_list:
            lines.append(f"### {pr.get('title', '')} ({pr.get('period', '')})")
            lines.extend(f"- {b}" for b in pr.get("bullets", []))
            lines.append("")

    lines.append("## Qualifikationen & Kompetenzen")
    for label, key in (
        ("ERP & Architektur-Governance", "erp_governance"),
        ("Daten & Prozessautomatisierung", "data_analysis"),
        ("PMO, Steuerung & Tools", "pmo_tools"),
        ("Sprachen", "languages"),
    ):
        val = str(skills.get(key) or "").strip()
        if val:
            lines.append(f"- **{label}:** {val}")
    if cv_data.get("showExtra", True) and extra:
        lines.extend(["", "## Zertifizierung & Engagement"])
        lines.extend(f"- {i}" for i in extra if str(i).strip())

    return "\n".join(lines)
