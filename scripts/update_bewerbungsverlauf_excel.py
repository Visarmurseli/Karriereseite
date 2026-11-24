import os
import json
import re
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_DIR = os.path.join(BASE_DIR, "00_Aktuelle_Bewerbungsunterlagen")
if not os.path.exists(DOCS_DIR):
    DOCS_DIR = r"c:\Users\SHQIPTAR634\Desktop\SSB Dateien\00_Aktuelle_Bewerbungsunterlagen"

EXCEL_PATH = os.path.join(DOCS_DIR, "Bewerbungsverlauf.xlsx")
EMAILS_JSON = os.path.join(DOCS_DIR, "deep_emails_dump.json")
FALLBACK_EMAILS_JSON = os.path.join(DOCS_DIR, "all_application_emails.json")
COCKPIT_MD = r"C:\Users\SHQIPTAR634\Documents\Obsidian Vault\01_Karriere_Bewerbungen\00_Bewerbungsmanagement_Cockpit.md"
PIPELINE_JSON = os.path.join(DOCS_DIR, "bewerbungen_pipeline.json")

# Master high-precision profiles for key companies & interview tracks
ENRICHED_PROFILES = {
    "trumpf": {
        "employer": "TRUMPF",
        "title": "Trainee (w/m/d) IT [Ref: R00042850]",
        "location": "Ditzingen",
        "sub_date": "28.10.2026",
        "ack_date": "28.10.2026",
        "int1_date": "06.11.2026",
        "int1_details": "11:30 – 12:00 Uhr (Virtual Screen HR mit Jil Wachter)",
        "int2_date": "23.11.2026",
        "int2_details": "09:30 – 10:30 Uhr (Teams Interview mit Tanja Preissner & Martin Hartmann)",
        "status": "⭐ 2. Gespräch am 23.11.2026 absolviert (Tanja Preissner & Martin Hartmann)",
        "tasks": "• 18–24-monatiges IT-Traineeprogramm bei TRUMPF mit Rotationen durch IT-Governance, IT-Infrastruktur & Enterprise Applications.\n• Aktive Mitgestaltung von konzernweiten Digitalisierungs- und Architekturprojekten im globalen Hochtechnologie-Maschinenbau.\n• Schnittstellenmanagement zwischen IT-Service-Bereichen, IT-Governance und internationalen Standorten.",
        "requirements": "Master Wirtschaftsinformatik; Verständnis moderner IT-Service-Architekturen und Governance; ausgeprägte Kommunikationskompetenz.",
        "notes": "Erstes Screening am 06.11.2026 erfolgreich absolviert. Zweites, einstündiges Fachinterview am 23.11.2026 um 09:30 Uhr mit Tanja Preissner (Head of IT Governance) und Martin Hartmann (Head of IT Infrastructure)."
    },
    "kpmg": {
        "employer": "KPMG",
        "title": "(Junior) IT Consultant / IT-Berater IT-Transformation (w/m/d) [Ref: 224]",
        "location": "Stuttgart",
        "sub_date": "17.11.2026",
        "ack_date": "17.11.2026",
        "int1_date": "27.11.2026",
        "int1_details": "16:00 Uhr (Teams Interview mit Jasmin Habib / Team Nevzat Canoglu)",
        "int2_date": "-",
        "int2_details": "-",
        "status": "⭐ Einladung zum Interview am 27.11.2026 (Jasmin Habib)",
        "tasks": "• Ganzheitliche Beratung nationaler und internationaler Unternehmenskunden bei der digitalen Transformation und ERP-/IT-Modernisierung.\n• Begleitung von IT-Audits, SAP S/4HANA Systemprüfungen, Prozess- und Schnittstellenanalysen.\n• Analyse von IT-Architekturen, Berechtigungskonzepten und internen Kontrollsystemen (IKS).",
        "requirements": "Master Wirtschaftsinformatik; ERP-/SAP-Verständnis, IT-Governance, IT-Audit.",
        "notes": "Mitarbeiterempfehlung durch Nevzat Canoglu (Assistant Manager Financial Services). Intervieweinladung am 23.11.2026 erhalten."
    },
    "msg systems": {
        "employer": "msg systems",
        "title": "(Junior) Technical SAP Consultant (all genders)",
        "location": "Stuttgart / Leinfelden-Echterdingen",
        "sub_date": "17.09.2026",
        "ack_date": "17.09.2026",
        "int1_date": "29.09.2026",
        "int1_details": "15:00 – 15:45 Uhr (Teams Kennenlerngespräch)",
        "int2_date": "08.10.2026",
        "int2_details": "17:00 – 17:45 Uhr (Teams Zweitgespräch mit Matthaeus Glueck & Sandra Ulber)",
        "status": "⭐ 2. Gespräch am 08.10.2026 absolviert (Matthaeus Glueck & Sandra Ulber)",
        "tasks": "• Technische Beratung und Implementierung von SAP-Lösungen (S/4HANA, BTP, CDS Views, Integration Suite).\n• Konzeption und Implementierung von Schnittstellen zu heterogenen Vorsystemen und Cloud-Services.\n• Begleitung des gesamten Projektzyklus von der Anforderungsanalyse bis zum Go-Live.",
        "requirements": "Wirtschaftsinformatik-Abschluss; SQL, BTP-Architektur, Schnittstellen-Design.",
        "notes": "Beide Gesprächsrunden erfolgreich absolviert."
    },
    "computacenter": {
        "employer": "Computacenter",
        "title": "Trainee IT Service Architecture & Design (w/m/d)",
        "location": "Stuttgart / Bundesweit",
        "sub_date": "27.05.2026",
        "ack_date": "27.05.2026",
        "int1_date": "11.06.2026",
        "int1_details": "17:00 Uhr (Teams Videointerview mit Tobias & Lili Potyondi)",
        "int2_date": "-",
        "int2_details": "-",
        "status": "⭐ Videointerview am 11.06.2026 absolviert",
        "tasks": "• Ganzheitliches Design von Enterprise IT-Service-Architekturen nach ITIL 4 für Großkonzerne.\n• Konzeption hybrider Cloud- und Rechenzentrumsmodelle (Private/Public Cloud).\n• Erstellung technischer Servicekataloge, SLAs und Service-Delivery-Konzepte.",
        "requirements": "Wirtschaftsinformatik; ITIL 4 Service Operations (aus 12 Monaten Datacenter One INOC); analytische Stärke.",
        "notes": "Videointerview am 11.06.2026 um 17:00 Uhr via Microsoft Teams geführt."
    },
    "deutsche bahn": {
        "employer": "Deutsche Bahn",
        "title": "Mitarbeiter:in Reisendenlenkung für Bahnhöfe in Baden-Württemberg [DB Zeitarbeit GmbH]",
        "location": "Stuttgart / Baden-Württemberg",
        "sub_date": "18.10.2026",
        "ack_date": "18.10.2026",
        "int1_date": "02.11.2026",
        "int1_details": "10:00 Uhr (Vorstellungsgespräch mit Berina Alomerovic)",
        "int2_date": "-",
        "int2_details": "-",
        "status": "⭐ Vorstellungsgespräch am 02.11.2026 absolviert",
        "tasks": "• Operative Unterstützung und Reisendenlenkung an Knotenbahnhöfen in Baden-Württemberg.\n• Deeskalation, Informationsbereitstellung und Schnittstelle zu Leitstellen.",
        "requirements": "Kommunikationsstärke, Flexibilität, Zuverlässigkeit.",
        "notes": "Terminbestätigung und Vorstellungsgespräch am 02.11.2026."
    },
    "ey (ernst & young)": {
        "employer": "EY (Ernst & Young)",
        "title": "(Junior) Consultant - Technology Consulting / ERP & SAP Transformation [Ref: 13743137]",
        "location": "Stuttgart",
        "sub_date": "19.09.2026",
        "ack_date": "19.09.2026",
        "int1_date": "19.10.2026",
        "int1_details": "Online / Telefoninterview mit Karolina Żukowska / Dorota Iwaniak",
        "int2_date": "-",
        "int2_details": "-",
        "status": "⭐ Interview bestätigt (19.10.2026 / 02.10.2026)",
        "tasks": "• Beratung internationaler Mandanten bei komplexen SAP S/4HANA Transformationsprogrammen.\n• Prozessanalyse, Fit-Gap-Workshops, Migrationskonzeption und Architektur-Audits.",
        "requirements": "Masterabschluss Wirtschaftsinformatik; starke analytische Fähigkeiten; Englisch fließend.",
        "notes": "Bewerbungsfragebogen via DocuSign eingereicht; Interview im Oktober 2026 bestätigt."
    },
    "instaff": {
        "employer": "InStaff",
        "title": "IT-Support & Promotion Specialist (m/w/d)",
        "location": "Stuttgart",
        "sub_date": "24.09.2026",
        "ack_date": "24.09.2026",
        "int1_date": "24.09.2026",
        "int1_details": "Telefoninterview mit Jennifer Balk (InStaff)",
        "int2_date": "-",
        "int2_details": "-",
        "status": "⭐ Telefoninterview am 24.09.2026 absolviert",
        "tasks": "• Technische Unterstützung und Host-Betreuung bei Veranstaltungen und Projekten.",
        "requirements": "Zuverlässigkeit, Kommunikationsstärke.",
        "notes": "Telefoninterview am 24.09.2026 absolviert."
    },
    "teamative": {
        "employer": "Teamative",
        "title": "(Junior) SAP S/4HANA Consultant (m/w/d)",
        "location": "Stuttgart / Remote",
        "sub_date": "29.04.2026",
        "ack_date": "30.04.2026",
        "int1_date": "04.05.2026",
        "int1_details": "Kennenlerngespräch mit der Geschäftsführung",
        "int2_date": "11.05.2026",
        "int2_details": "Zweitgespräch / Case Study mit Senior SAP Architects",
        "status": "Absage am 19.05.2026 per Mail (\"Stelle wurde vorerst geschlossen\")",
        "tasks": "• Beratung mittelständischer Kunden bei der Migration auf SAP S/4HANA.\n• Implementierung von Finanz- und Logistikmodulen.",
        "requirements": "S/4HANA Know-how, Hands-on-Mentalität.",
        "notes": "Beide Runden exzellent absolviert; Stelle aus internen Gründen vorübergehend geschlossen."
    },
    "coop (schweiz)": {
        "employer": "Coop (Schweiz)",
        "title": "BI Consultant (80–100%)",
        "location": "Basel, Schweiz",
        "sub_date": "17.11.2026",
        "ack_date": "17.11.2026",
        "int1_date": "-",
        "int1_details": "-",
        "int2_date": "-",
        "int2_details": "-",
        "status": "Bewerbungseingang bestätigt (17.11.2026, Update 20.11.2026)",
        "tasks": "• Weiterentwicklung und Betreuung der konzernweiten Business Intelligence- und Reporting-Landschaft bei Coop Schweiz.\n• Konzeption und Implementierung von Datenmodellen, ETL-Pipelines und Dashboards für den Detail- und Großhandel.",
        "requirements": "Wirtschaftsinformatik; Datenmodellierung, SQL, BI-Tools (Power BI, SAP Analytics Cloud).",
        "notes": "Registrierung und Eingang der Bewerbung am 17.11.2026 bestätigt."
    }
}

def parse_date(date_str):
    if not date_str or date_str == "-":
        return None
    # e.g. "Mon, 23 Nov 2026 14:30:00 +0100"
    m = re.search(r"(\d{1,2})\s+([A-Za-z]{3})\s+(\d{4})", str(date_str))
    if m:
        day = int(m.group(1))
        month_str = m.group(2).lower()
        year = int(m.group(3))
        months = {
            "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
            "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
            "mrz": 3, "mai": 5, "okt": 10, "dez": 12
        }
        month = months.get(month_str, 1)
        return datetime(year, month, day)
    # e.g. "23.11.2026"
    m2 = re.search(r"(\d{1,2})\.(\d{1,2})\.(\d{4})", str(date_str))
    if m2:
        return datetime(int(m2.group(3)), int(m2.group(2)), int(m2.group(1)))
    return None

def format_date_de(dt):
    if isinstance(dt, datetime):
        return dt.strftime("%d.%m.%Y")
    return str(dt) if dt else "-"

def clean_company_name(sender, subject):
    text = f"{sender} {subject}".lower()
    
    blacklist = [
        "amazon", "dhl paket", "dhl zustell", "ebay", "otto-kundenservice", "notino", 
        "discovercars", "adidas", "zon-stuttgart", "mail-stz.de", "handelsblatt", 
        "accounts.google.com", "sicher.gmx.net", "mailer-daemon", "verimi", 
        "veronamurseli", "lbbw-jobnotification", "indeed-passkey", "match.indeed.com",
        "stepstone-gehalt", "newsletter", "corporate benefits", "corporate-benefits"
    ]
    if any(b in text for b in blacklist):
        return None

    if "flasch" in text or "recruitmail" in text or "rheinmetall" in text:
        return "Rheinmetall"
    elif "kpmg" in text or "talentry" in text:
        return "KPMG"
    elif "trumpf" in text:
        return "TRUMPF"
    elif "computacenter" in text or "paula.weber" in text or "paula weber" in text or "mb_hr_os" in text:
        return "Computacenter"
    elif "schwarz" in text or "lidl" in text or "kadrija" in text or "jessica hertel" in text or "vanessa kelsch" in text or "jule rhein" in text or "selina hermann" in text or "karsten gilbert" in text:
        if "digits" in text or "cloud" in text or "ai product" in text:
            return "Schwarz Digits"
        elif "lidl" in text:
            return "Lidl Stiftung & Co. KG"
        return "Schwarz-Gruppe"
    elif "deutschebahn" in text or "db zeitarbeit" in text or "alomerovic" in text:
        return "Deutsche Bahn"
    elif "ey.com" in text or "ernst & young" in text or "talentattractionandacquisition" in text or "karolina.zukowska" in text or "iwaniak" in text or "correspondenceeyhrisprd1" in text:
        return "EY (Ernst & Young)"
    elif "capgemini" in text:
        return "Capgemini Invent"
    elif "coop" in text:
        return "Coop (Schweiz)"
    elif "msg" in text:
        return "msg systems"
    elif "horbach" in text:
        return "HORBACH"
    elif "hengstenberg" in text or "deger" in text:
        return "Hengstenberg"
    elif "adesso" in text:
        return "adesso SE"
    elif "lti-metalltechnik" in text:
        return "LTI-Metalltechnik"
    elif "stuttgart.bewerbung.dvvbw" in text or "landeshauptstadt stuttgart" in text:
        return "Landeshauptstadt Stuttgart"
    elif "kvjs" in text:
        return "KVJS"
    elif "bva.bund.de" in text or "thw" in text:
        return "Bundesverwaltungsamt (THW)"
    elif "prognum" in text:
        return "prognum Automotive"
    elif "rolls-royce" in text or "rollsroyce" in text:
        return "Rolls-Royce Power Systems"
    elif "ssb-ag.de" in text or "ssb ag" in text or "trotus" in text or "bulke" in text:
        return "Stuttgarter Straßenbahnen AG (SSB)"
    elif "cpro" in text:
        return "Cpro INDUSTRY"
    elif "communardo" in text or "schober" in text:
        return "Communardo"
    elif "karle & brunold" in text or "karle &amp; brunold" in text:
        return "Karle & Brunold"
    elif "x1f" in text:
        return "x1F"
    elif "all for one" in text:
        return "All for One Group"
    elif "teamative" in text:
        return "Teamative"
    elif "axians" in text:
        return "Axians"
    elif "mercedes" in text:
        return "Mercedes-Benz"
    elif "deloitte" in text:
        return "Deloitte"
    elif "drees & sommer" in text:
        return "Drees & Sommer"
    elif "körber" in text or "koerber" in text:
        return "Körber"
    elif "convista" in text:
        return "ConVista"
    elif "cbs" in text:
        return "cbs Corporate Business Solutions"
    elif "lbbw" in text:
        return "LBBW"
    elif "hdm" in text or "hdm-stuttgart" in text or "zobel" in text or "seiler" in text:
        return "HdM Stuttgart"
    elif "bitbw" in text or "julia rupp" in text:
        return "BITBW"
    elif "cgi" in text or "njoyn" in text:
        return "CGI"
    elif "drv-bw" in text:
        return "DRV Baden-Württemberg"
    elif "appliedai" in text:
        return "appliedAI"
    elif "kärcher" in text or "karcher" in text:
        return "Alfred Kärcher SE & Co. KG"
    elif "mhp" in text:
        return "MHP (Porsche Company)"
    elif "porsche" in text:
        return "Porsche AG"
    elif "ntt data" in text:
        return "NTT DATA Business Solutions"
    elif "smartrecruiters" in text or "bosch" in text:
        return "Bosch Group (JMP)"
    elif "instaff" in text:
        return "InStaff"
    elif "mindsquare" in text:
        return "mindsquare"
    elif "jobvalley" in text or "studitemps" in text or "julia koch" in text:
        return "jobvalley"
    elif "jobmensa" in text:
        return "jobmensa"
    elif "abacus" in text:
        return "Abacus HR Services"
    elif "manß & partner" in text or "manß" in text:
        return "Manß & Partner"
        
    clean_s = re.sub(r"<[^>]+>", "", sender).strip().strip('"')
    if clean_s and len(clean_s) < 30 and not any(k in clean_s.lower() for k in ["gmx", "indeed", "stepstone", "xing", "linkedin", "noreply", "kundenservice", "support", "no-reply"]):
        return clean_s
    return None

def clean_position_title(subject):
    s = subject.replace("\r", " ").replace("\n", " ").strip()
    
    if "trainee (w/m/d) it" in s.lower() or "trainee it" in s.lower():
        return "Trainee (w/m/d) IT [Ref: R00042850]"
    if "trainee-programm zum sap" in s.lower():
        return "Trainee SAP Consultant (m/w/d)"
    if "ai product owner" in s.lower():
        return "(Junior-) AI Product Owner (m/w/d)"
    if "sap inhouse‑berater" in s.lower() or "sap inhouse-berater" in s.lower():
        return "SAP Inhouse-Berater PM / CS bzw. PP (m/w/d)"
    if "erp-anwendungsbetreuer" in s.lower():
        return "ERP-Anwendungsbetreuer (m/w/d)"
    if "junior sap hcm" in s.lower():
        return "Junior SAP HCM User Maintenance & Access Management (IAM) Specialist (m/w/d) [Ref: 4972]"
    if "sap alm spezialist" in s.lower():
        return "SAP ALM Spezialist (m/w/d) - Schwerpunkt Focused Run und Cloud ALM [Ref: 3267]"
    if "bi consultant" in s.lower():
        return "BI Consultant (80–100%)"
    if "it solution architect" in s.lower():
        return "IT Solution Architect (m/w/d)"
    if "referent:in prozessmanagement" in s.lower():
        return "Referent:in Prozessmanagement und Datenschutz im Bereich IT (m/w/d)"
    if "technischer angestellter" in s.lower():
        return "Technischer Angestellter IT-Infrastruktur (m/w/d)"
    if "technical sap consultant" in s.lower():
        return "(Junior) Technical SAP Consultant (all genders)"
    if "junior sap consultant public" in s.lower():
        return "Junior SAP Consultant Public (m/w/d)"
    if "cloud engineer" in s.lower() or "cloud application" in s.lower():
        return "Junior Cloud Engineer (m/w/d) - STACKIT"
    if "ai consultant" in s.lower():
        return "AI Consultant (m/f/x)"
    if "sap power-" in s.lower():
        return "SAP Power-Keyuser / Disponent (m/w/d)"
    if "sachbearbeitung administration" in s.lower() or "thw-2026" in s.lower():
        return "Sachbearbeitung Administration (m/w/d) im ITCC [Kennziffer: THW-2026-135]"
    if "koordination it-support" in s.lower():
        return "Koordination IT-Support & Service (m/w/d) [Kennziffer: 2026-IT]"
    if "junior managers program" in s.lower() or "jmp" in s.lower():
        return "Junior Managers Program (JMP) IT"
    if "sap business data cloud" in s.lower():
        return "(Junior) Consultant SAP Business Data Cloud (m/w/d)"
    if "praktikum im consulting" in s.lower():
        return "Praktikum im Consulting (m/w/d)"
    if "sap-basis consultant" in s.lower():
        return "(Junior) SAP-Basis Consultant (m/w/d)"
    if "lohnrechner" in s.lower() or "lohn" in s.lower():
        return "Software Berater/in ERP (m/w/d) im Bereich Lohnbuchhaltung"
        
    patterns = [
        r"(?:stelle\s+als|position\s+als|bewerbung\s+als|bewerbung\s+auf\s+die\s+position|bewerbung\s+auf\s+die\s+stelle|deine\s+bewerbung:\s*|deine\s+bewerbung\s+bei\s+[^:]+:\s*)([^\n\r,\.\(\)]+)",
        r"(?:für\s+die\s+position\s+)([^\n\r,\.\(\)]+)",
        r"(?:Bewerbung\s+auf\s+unsere\s+Ausschreibung\s+)([^\n\r,\.\(\)]+)",
    ]
    for p in patterns:
        m = re.search(p, s, re.I)
        if m:
            clean = m.group(1).strip()
            if len(clean) > 4:
                return clean
    if "junior it consultant" in s.lower() or "it consultant" in s.lower():
        return "(Junior) IT Consultant / IT-Berater IT-Transformation (w/m/d)"
    if "junior sap consultant" in s.lower():
        return "Junior SAP Consultant (m/w/d)"
    return "(Junior) SAP / IT Consultant"

def run_master_update():
    # 1. Load Emails
    emails_file = EMAILS_JSON if os.path.exists(EMAILS_JSON) else FALLBACK_EMAILS_JSON
    with open(emails_file, "r", encoding="utf-8") as f:
        emails = json.load(f)
        
    print(f"Lade {len(emails)} E-Mails aus {emails_file}...")
    
    # 2. Extract Events
    company_events = {}
    for em in emails:
        subj = em.get("subject", "")
        sender = em.get("sender", "")
        body = em.get("body", "")
        dt = parse_date(em.get("date", ""))
        
        subj_low = subj.lower()
        sender_low = sender.lower()
        
        comp = clean_company_name(sender, subj)
        if not comp:
            continue
            
        pos = clean_position_title(subj)
        event_key = (comp, pos)
        
        if event_key not in company_events:
            company_events[event_key] = {
                "company": comp,
                "position": pos,
                "submissions": [],
                "acknowledgments": [],
                "first_interviews": [],
                "second_interviews": [],
                "rejections": [],
                "latest_date": dt,
                "body_snippet": body[:500] if body else ""
            }
            
        entry = company_events[event_key]
        if dt and (not entry["latest_date"] or dt > entry["latest_date"]):
            entry["latest_date"] = dt
            
        is_interview = any(k in subj_low for k in [
            "einladung zum interview", "interview extension", "terminvereinbarung", 
            "vorstellungsgespräch", "kennenlerngespräch", "teams interview", 
            "videointerview", "telefoninterview", "interview confirmed", "terminbestätigung",
            "einladung zum videointerview", "einladung zum zweitgespräch"
        ])
        is_rejection = any(k in subj_low for k in [
            "absage", "nicht berücksichtigen", "anderweitig entschieden", "leider mitteilen",
            "nicht geklappt", "geschlossen"
        ])
        is_ack = any(k in subj_low for k in [
            "eingangsbestätigung", "deine bewerbung", "vielen dank für deine bewerbung", 
            "vielen dank für ihre bewerbung", "bestätigung", "haben ihre bewerbung erhalten",
            "bewerbung ist bei uns eingegangen", "ihre bewerbung ist eingegangen", 
            "bestätigung bewerbungseingang", "ihre bewerbung bei"
        ])
        
        if is_interview:
            entry["first_interviews"].append((dt, subj))
        elif is_rejection:
            entry["rejections"].append((dt, subj))
        elif is_ack:
            entry["acknowledgments"].append((dt, subj))

    # 3. Read existing Excel rows
    existing_rows = []
    if os.path.exists(EXCEL_PATH):
        wb_old = openpyxl.load_workbook(EXCEL_PATH)
        ws_old = wb_old["Bewerbungsverlauf"] if "Bewerbungsverlauf" in wb_old.sheetnames else wb_old.active
        for r in list(ws_old.iter_rows(values_only=True))[1:]:
            c_name = str(r[0]).strip() if r[0] else ""
            if c_name:
                existing_rows.append(list(r))
                
    # Blacklist cleanup
    blacklist_comps = [
        "amazon", "dhl", "ebay", "otto", "notino", "discovercars", "adidas", 
        "zon", "stz", "handelsblatt", "google", "sicherheit", "mailer-daemon", 
        "verimi", "verona", "lbbw-jobnotification", "indeed", "kundenservice",
        "no-reply", "stellenmarkt ssb ag", "ihre bewerbung", "daniel troturs",
        "corporate benefits", "corporate-benefits", "ssb corporate"
    ]
    
    aliases = {
        "coop-gruppe": "Coop (Schweiz)",
        "adesso group": "adesso SE",
        "jobs": "LTI-Metalltechnik",
        "prognum automotive gmbh": "prognum Automotive",
        "alfred kärcher se & co. kg": "Alfred Kärcher SE & Co. KG",
        "lidl stiftung & co. kg": "Schwarz Digits",
        "schwarz-gruppe": "Schwarz Digits",
    }
    
    rows_map = {}
    for r in existing_rows:
        c_name = str(r[0]).strip()
        c_low = c_name.lower()
        if any(b in c_low for b in blacklist_comps):
            continue
        if c_low in aliases:
            r[0] = aliases[c_low]
            c_low = aliases[c_low].lower()
        p_name = str(r[1]).strip() if r[1] else ""
        rows_map[(c_low, p_name.lower())] = r
        
    # Merge detected events
    for (comp, pos), data in company_events.items():
        comp_key = comp.lower()
        pos_key = pos.lower()
        
        ack_dt = data["acknowledgments"][0][0] if data["acknowledgments"] else None
        int1_dt = data["first_interviews"][0][0] if data["first_interviews"] else None
        rej_dt = data["rejections"][0][0] if data["rejections"] else None
        
        if int1_dt:
            status_text = f"⭐ Einladung zum Interview am {format_date_de(int1_dt)}"
        elif rej_dt:
            status_text = f"Absage am {format_date_de(rej_dt)} per E-Mail."
        elif ack_dt:
            status_text = f"Bewerbungseingang bestätigt ({format_date_de(ack_dt)})"
        else:
            status_text = "In Prüfung"
            
        matched_pair = None
        for (ck, pk) in rows_map.keys():
            if comp_key == ck or (comp_key in ck and len(comp_key) > 4):
                if pk == pos_key or "junior" in pk or "consultant" in pk or len(pk) < 5:
                    matched_pair = (ck, pk)
                    break
                    
        if matched_pair:
            row = rows_map[matched_pair]
            if int1_dt:
                row[4] = format_date_de(int1_dt)
                row[6] = status_text
            elif rej_dt and not row[6]:
                row[6] = status_text
            elif ack_dt and (not row[3] or row[3] == "-"):
                row[3] = format_date_de(ack_dt)
            if pos and (not row[1] or row[1] in ["-", "Junior SAP / IT Consultant", "(Junior) SAP / IT Consultant"]):
                row[1] = pos
        else:
            sub_dt = ack_dt or data["latest_date"]
            new_row = [
                comp,
                pos,
                format_date_de(sub_dt),
                format_date_de(ack_dt),
                format_date_de(int1_dt),
                "-",
                status_text
            ]
            rows_map[(comp_key, pos_key)] = new_row
            
    # Apply ENRICHED_PROFILES overrides (100% precision for TRUMPF, KPMG, msg, Computacenter, DB, EY, etc.)
    for ep_key, ep in ENRICHED_PROFILES.items():
        # Purge any existing partial or duplicate entries for this company
        keys_to_del = [k for k in list(rows_map.keys()) if ep_key == k[0] or (ep_key in k[0] and len(ep_key) > 4)]
        for k in keys_to_del:
            del rows_map[k]
            
        # Insert single canonical enriched row
        rows_map[(ep["employer"].lower(), ep["title"].lower())] = [
            ep["employer"],
            ep["title"],
            ep["sub_date"],
            ep["ack_date"],
            ep["int1_date"],
            ep["int2_date"],
            ep["status"]
        ]
        
    # Purge duplicate Ref 4972
    ref_4972_keys = [k for k in list(rows_map.keys()) if "4972" in k[1]]
    if len(ref_4972_keys) > 1:
        for k in ref_4972_keys[1:]:
            del rows_map[k]
            
    # Purge generic SSB rows if specific roles exist
    ssb_keys = [k for k in list(rows_map.keys()) if "stuttgarter straßenbahnen" in k[0] or "ssb ag" in k[0]]
    for k in ssb_keys:
        if k[1].lower() in ["(junior) sap / it consultant", "junior sap / it consultant"]:
            del rows_map[k]

    # Rebuild Excel with 2 Tabs
    wb = openpyxl.Workbook()
    
    # ------------------ SHEET 1: Bewerbungsverlauf ------------------
    ws1 = wb.active
    ws1.title = "Bewerbungsverlauf"
    
    navy_fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    white_font = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
    zebra_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    highlight_interview = PatternFill(start_color="ECFDF5", end_color="ECFDF5", fill_type="solid")
    green_font = Font(name="Segoe UI", size=10, bold=True, color="047857")
    reg_font = Font(name="Segoe UI", size=10)
    bold_font = Font(name="Segoe UI", size=10, bold=True)
    center_align = Alignment(horizontal="center", vertical="center")
    left_align = Alignment(horizontal="left", vertical="center")
    wrap_left = Alignment(horizontal="left", vertical="center", wrap_text=True)
    thin_border = Border(
        left=Side(style="thin", color="E2E8F0"),
        right=Side(style="thin", color="E2E8F0"),
        top=Side(style="thin", color="E2E8F0"),
        bottom=Side(style="thin", color="E2E8F0")
    )
    
    col_headers_1 = [
        "Arbeitgeber", "Genaue Stellenbezeichnung & Referenz", "Tag der Einreichung", 
        "Bewerbungseingang", "1. Gespräch", "2. Gespräch", "Status / Gesprächsergebnis"
    ]
    ws1.append(col_headers_1)
    ws1.row_dimensions[1].height = 28
    
    for c_idx in range(1, len(col_headers_1) + 1):
        cell = ws1.cell(row=1, column=c_idx)
        cell.fill = navy_fill
        cell.font = white_font
        cell.alignment = center_align
        cell.border = thin_border
        
    all_sorted_rows = list(rows_map.values())
    def sort_key(r):
        d = r[2]
        dt = parse_date(d)
        if dt:
            return dt
        return datetime(2024, 1, 1)
        
    all_sorted_rows.sort(key=sort_key, reverse=True)
    
    for r_idx, r_data in enumerate(all_sorted_rows, start=2):
        ws1.row_dimensions[r_idx].height = 24
        is_interview = (str(r_data[4]) not in ["-", "None", ""]) or (str(r_data[5]) not in ["-", "None", ""]) or ("gespräch" in str(r_data[6]).lower()) or ("interview" in str(r_data[6]).lower())
        is_even = (r_idx % 2 == 0)
        
        for c_idx, val in enumerate(r_data, start=1):
            cell = ws1.cell(row=r_idx, column=c_idx)
            val_str = str(val or "-")
            cell.value = val_str
            cell.border = thin_border
            cell.alignment = center_align if c_idx in [3, 4, 5, 6] else left_align
            
            if is_interview:
                cell.fill = highlight_interview
                cell.font = green_font if c_idx in [1, 5, 6, 7] else reg_font
            elif is_even:
                cell.fill = zebra_fill
                cell.font = reg_font
            else:
                cell.font = reg_font
                
    for col in ws1.columns:
        max_len = max(len(str(cell.value or "")) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws1.column_dimensions[col_letter].width = min(max(max_len + 4, 14), 50)
        
    # ------------------ SHEET 2: Stellenbeschreibungen & Aufgaben ------------------
    ws2 = wb.create_sheet(title="Stellenprofile_Details")
    col_headers_2 = [
        "Arbeitgeber", "Exakter Stellentitel & Referenz", "Standort", 
        "Aufgaben & Tätigkeitsbereiche", "Anforderungsprofil", 
        "Interview-Historie & Gesprächspartner", "Quelle / Prozess-Notizen"
    ]
    ws2.append(col_headers_2)
    ws2.row_dimensions[1].height = 28
    
    for c_idx in range(1, len(col_headers_2) + 1):
        cell = ws2.cell(row=1, column=c_idx)
        cell.fill = navy_fill
        cell.font = white_font
        cell.alignment = center_align
        cell.border = thin_border
        
    # Write details for all enriched profiles and detected rows
    for r_idx, r_data in enumerate(all_sorted_rows, start=2):
        ws2.row_dimensions[r_idx].height = 55
        c_emp = r_data[0]
        c_title = r_data[1]
        c_key = c_emp.lower()
        
        ep = ENRICHED_PROFILES.get(c_key, None)
        if not ep:
            for k, v in ENRICHED_PROFILES.items():
                if k in c_key or c_key in k:
                    ep = v
                    break
                    
        loc = ep["location"] if ep else "Baden-Württemberg / Deutschland"
        tasks = ep["tasks"] if ep else f"• Verantwortliche Begleitung und Fachberatung im Bereich {c_title}.\n• Analyse, Modellierung und Weiterentwicklung von IT- und Geschäftsprozessen.\n• Schnittstellenkoordination zwischen Business-Stakeholdern und technischen Entwicklungsteams."
        reqs = ep["requirements"] if ep else "Master-/Bachelor-Abschluss Wirtschaftsinformatik; Fundierung in ERP-, Daten- oder IT-Architekturen; strukturierte, lösungsorientierte Arbeitsweise."
        notes = ep["notes"] if ep else f"Bewerbungseingang erfasst am {r_data[3]}. Status: {r_data[6]}."
        
        int_hist = ""
        if str(r_data[4]) not in ["-", "None", ""]:
            int_hist += f"1. Gespräch: {r_data[4]}"
            if ep and ep.get("int1_details"):
                int_hist += f" ({ep['int1_details']})"
            int_hist += "\n"
        if str(r_data[5]) not in ["-", "None", ""]:
            int_hist += f"2. Gespräch: {r_data[5]}"
            if ep and ep.get("int2_details"):
                int_hist += f" ({ep['int2_details']})"
            int_hist += "\n"
        if not int_hist:
            int_hist = str(r_data[6])
            
        row_vals = [
            c_emp,
            c_title,
            loc,
            tasks,
            reqs,
            int_hist.strip(),
            notes
        ]
        
        for c_idx, val in enumerate(row_vals, start=1):
            cell = ws2.cell(row=r_idx, column=c_idx)
            cell.value = str(val or "-")
            cell.border = thin_border
            cell.alignment = wrap_left if c_idx in [2, 4, 5, 6, 7] else (center_align if c_idx == 3 else left_align)
            cell.font = bold_font if c_idx == 1 else reg_font
            if (r_idx % 2 == 0):
                cell.fill = zebra_fill
                
    ws2.column_dimensions["A"].width = 22
    ws2.column_dimensions["B"].width = 40
    ws2.column_dimensions["C"].width = 20
    ws2.column_dimensions["D"].width = 65
    ws2.column_dimensions["E"].width = 50
    ws2.column_dimensions["F"].width = 55
    ws2.column_dimensions["G"].width = 40
    
    wb.save(EXCEL_PATH)
    print(f"✅ Excel erfolgreich mit 2 Sheets gespeichert: {len(all_sorted_rows)} Bewerbungen eingetragen!")
    
    # ------------------ Obsidian Cockpit Markdown ------------------
    table_lines = [
        "| Arbeitgeber | Genaue Stellenbezeichnung & Referenz | Datum | Eingang | 1. Gespräch | 2. Gespräch | Status / Ergebnis |",
        "| :--- | :--- | :---: | :---: | :---: | :---: | :--- |"
    ]
    for r in all_sorted_rows:
        comp = f"**{r[0]}**"
        title = r[1]
        sub_d = r[2]
        ack_d = r[3]
        int1_d = r[4]
        int2_d = r[5]
        stat = r[6]
        table_lines.append(f"| {comp} | {title} | {sub_d} | {ack_d} | {int1_d} | {int2_d} | {stat} |")
    table_md = "\n".join(table_lines)
    
    # Dossiers
    dossier_blocks = ["## 📑 Detaillierte Stellenbeschreibungen, Aufgaben & Interview-Historie\n"]
    for r in all_sorted_rows:
        c_emp = r[0]
        c_title = r[1]
        c_key = c_emp.lower()
        ep = ENRICHED_PROFILES.get(c_key, None)
        if not ep:
            for k, v in ENRICHED_PROFILES.items():
                if k in c_key or c_key in k:
                    ep = v
                    break
        loc = ep["location"] if ep else "Baden-Württemberg / Deutschland"
        tasks = ep["tasks"] if ep else f"• Verantwortliche Begleitung und Fachberatung im Bereich {c_title}.\n• Analyse, Modellierung und Weiterentwicklung von IT- und Geschäftsprozessen.\n• Schnittstellenkoordination zwischen Business-Stakeholdern und technischen Entwicklungsteams."
        reqs = ep["requirements"] if ep else "Master-/Bachelor-Abschluss Wirtschaftsinformatik; Fundierung in ERP-, Daten- oder IT-Architekturen; strukturierte Arbeitsweise."
        notes = ep["notes"] if ep else f"Bewerbungseingang erfasst am {r[3]}. Status: {r[6]}."
        
        int_section = ""
        if str(r[4]) not in ["-", "None", ""]:
            int_section += f"> - **1. Gespräch:** {r[4]}"
            if ep and ep.get("int1_details"):
                int_section += f" ({ep['int1_details']})"
            int_section += "\n"
        if str(r[5]) not in ["-", "None", ""]:
            int_section += f"> - **2. Gespräch:** {r[5]}"
            if ep and ep.get("int2_details"):
                int_section += f" ({ep['int2_details']})"
            int_section += "\n"
        if not int_section:
            int_section = f"> - *Kein Vorstellungsgespräch terminiert / Status: {r[6]}*\n"
            
        tasks_fmt = "\n".join([f">   {line}" for line in tasks.splitlines() if line.strip()])
        
        card = f"""> [!INFO] **{c_emp} – {c_title}**
> - **Standort:** {loc}
> - **Tag der Einreichung:** {r[2]} | **Bewerbungseingang:** {r[3]}
> - **Aktueller Status:** `{r[6]}`
> 
> #### 💬 Gesprächsrunden & Interview-Timeline
{int_section}> 
> #### 📌 Aufgaben & Tätigkeitsbereiche
{tasks_fmt}
> 
> #### 🎯 Anforderungsprofil & Qualifikation
>   {reqs}
> 
> #### 💡 Prozess-Notizen & Hintergrund
>   {notes}
"""
        dossier_blocks.append(card)
        
    dossier_md = "\n".join(dossier_blocks)
    
    if os.path.exists(COCKPIT_MD):
        with open(COCKPIT_MD, "r", encoding="utf-8") as f:
            content = f.read()
            
        header_part = content.split("## 📋 Status-Matrix der Bewerbungen")[0]
        footer_part = content.split("## 🎯 Strategische Learnings für anstehende Gespräche")[1] if "## 🎯 Strategische Learnings für anstehende Gespräche" in content else ""
        
        new_content = (
            header_part
            + "## 📋 Status-Matrix der Bewerbungen\n\n"
            + table_md
            + "\n\n---\n\n"
            + dossier_md
            + "\n---\n\n## 🎯 Strategische Learnings für anstehende Gespräche"
            + footer_part
        )
        with open(COCKPIT_MD, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"✅ Obsidian Cockpit erfolgreich aktualisiert: {COCKPIT_MD}")
        
    # JSON Pipeline export
    pipeline_records = []
    for r in all_sorted_rows:
        pipeline_records.append({
            "employer": r[0],
            "position": r[1],
            "submission_date": r[2],
            "ack_date": r[3],
            "interview_1": r[4],
            "interview_2": r[5],
            "status": r[6]
        })
    with open(PIPELINE_JSON, "w", encoding="utf-8") as f:
        json.dump(pipeline_records, f, indent=2, ensure_ascii=False)
    print(f"✅ JSON Pipeline exportiert: {PIPELINE_JSON}")

if __name__ == "__main__":
    run_master_update()
