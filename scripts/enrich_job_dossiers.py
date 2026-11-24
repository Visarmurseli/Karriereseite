import os
import json
import re
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

EXCEL_PATH = r"c:\Users\SHQIPTAR634\Desktop\SSB Dateien\00_Aktuelle_Bewerbungsunterlagen\Bewerbungsverlauf.xlsx"
COCKPIT_MD = r"C:\Users\SHQIPTAR634\Documents\Obsidian Vault\01_Karriere_Bewerbungen\00_Bewerbungsmanagement_Cockpit.md"
PIPELINE_JSON = r"c:\Users\SHQIPTAR634\Desktop\SSB Dateien\00_Aktuelle_Bewerbungsunterlagen\bewerbungen_pipeline.json"

# Master database of exact job profiles with descriptions, tasks, contacts, and interview stages
JOB_PROFILES = [
    {
        "employer": "TRUMPF",
        "title": "Trainee (w/m/d) IT [Ref: R00042850]",
        "location": "Ditzingen (Headquarters)",
        "sub_date": "28.10.2026",
        "ack_date": "28.10.2026",
        "int1_date": "06.11.2026",
        "int1_time": "11:30 – 12:00 Uhr (Virtual Screen HR)",
        "int1_interviewer": "Jil Wachter (Attract to Hire Germany)",
        "int2_date": "23.11.2026",
        "int2_time": "09:30 – 10:30 Uhr (Teams Fachinterview)",
        "int2_interviewer": "Tanja Preissner (Head of IT Service Area - Governance), Martin Hartmann (Head of IT Service Area Infrastructure & RITC Europe), Jil Wachter",
        "status": "⭐ 2. Gespräch am 23.11.2026 absolviert (Tanja Preissner & Martin Hartmann)",
        "source": "Empfehlung durch Monika Augustin / Candidate Home Account R00042850",
        "tasks": "• 18–24-monatiges IT-Traineeprogramm bei TRUMPF mit Rotationen durch IT-Governance, IT-Infrastruktur & Enterprise Applications.\n• Aktive Mitgestaltung von konzernweiten Digitalisierungs- und Architekturprojekten im globalen Hochtechnologie-Maschinenbau.\n• Schnittstellenmanagement zwischen IT-Service-Bereichen, IT-Governance und internationalen Vertriebs-/Produktionsstandorten.\n• Einsatz moderner Kollaborations-, Cloud- und ERP-Architekturen.",
        "requirements": "Master-/Bachelor-Abschluss Wirtschaftsinformatik oder Informatik; Verständnis moderner IT-Service-Architekturen und Governance; ausgeprägte Kommunikations- und Moderationskompetenz; analytische Denkweise.",
        "notes": "Erstes Kennenlernen (Screening) am 06.11.2026 erfolgreich. Zweites, einstündiges Fachinterview heute am 23.11.2026 um 09:30 Uhr mit dem Head of IT Governance (Tanja Preissner) und dem Head of IT Infrastructure (Martin Hartmann)."
    },
    {
        "employer": "KPMG",
        "title": "(Junior) IT Consultant / IT-Berater IT-Transformation (w/m/d) [Ref: 224]",
        "location": "Stuttgart",
        "sub_date": "17.11.2026",
        "ack_date": "17.11.2026",
        "int1_date": "27.11.2026",
        "int1_time": "16:00 Uhr (Teams Interview)",
        "int1_interviewer": "Jasmin Habib (Recruiting) / Team Nevzat Canoglu (Digital Audit & FS Attestation)",
        "int2_date": "-",
        "int2_time": "-",
        "int2_interviewer": "-",
        "status": "⭐ Einladung zum Interview am 27.11.2026 (Jasmin Habib)",
        "source": "TopMATCH KPMG Mitarbeiterempfehlung durch Nevzat Canoglu (Assistant Manager Financial Services)",
        "tasks": "• Ganzheitliche Beratung nationaler und internationaler Unternehmenskunden bei der digitalen Transformation und ERP-/IT-Modernisierung.\n• Begleitung von IT-Audits, SAP S/4HANA Systemprüfungen, Prozess- und Schnittstellenanalysen.\n• Analyse von IT-Architekturen, Berechtigungskonzepten und internen Kontrollsystemen (IKS).\n• Entwicklung zukunftsfähiger IT-Governance- und Cloud-Strategien.",
        "requirements": "Abgeschlossenes Masterstudium Wirtschaftsinformatik; Know-how in ERP-Systemen (SAP S/4HANA), IT-Governance und Geschäftsprozessmodellierung; hohe Kundenorientierung.",
        "notes": "Mitarbeiterempfehlung via Talentry durch Nevzat Canoglu. Einladung von Jasmin Habib am 23.11.2026 erhalten. Vorgeschlagener Interview-Slot: Freitag, 27.11.2026 um 16:00 Uhr via Microsoft Teams."
    },
    {
        "employer": "msg systems",
        "title": "(Junior) Technical SAP Consultant (all genders)",
        "location": "Stuttgart / Leinfelden-Echterdingen",
        "sub_date": "17.09.2026",
        "ack_date": "17.09.2026",
        "int1_date": "29.09.2026",
        "int1_time": "15:00 – 15:45 Uhr (Teams Kennenlernen)",
        "int1_interviewer": "msg Recruiting Team / Sandra Ulber",
        "int2_date": "08.10.2026",
        "int2_time": "17:00 – 17:45 Uhr (Teams Zweitgespräch)",
        "int2_interviewer": "Matthaeus Glueck & Sandra Ulber (msg.insurance.recruiting)",
        "status": "⭐ 2. Gespräch am 08.10.2026 absolviert (Matthaeus Glueck & Sandra Ulber)",
        "source": "Bewerbungsportal msg systems (candidate-2f2f857c@jobs.msg.group)",
        "tasks": "• Technische Beratung und Implementierung von SAP-Lösungen (S/4HANA, BTP, CDS Views, ABAP Cloud, Integration Suite).\n• Konzeption und Implementierung von Schnittstellen zu heterogenen Vorsystemen und Cloud-Services.\n• Begleitung des gesamten Projektzyklus von der Anforderungsanalyse über Lösungsdesign bis hin zum Go-Live.",
        "requirements": "Wirtschaftsinformatik-Hintergrund; tiefes Verständnis von relationalen Datenbanken, SQL, BTP-Architektur und Schnittstellen-Design.",
        "notes": "Erstes Kennenlerngespräch am 29.09.2026 erfolgreich absolviert. Zweitgespräch nach Terminabstimmung am 08.10.2026 von 17:00 bis 17:45 Uhr mit Fachbereichsleiter Matthaeus Glueck und Sandra Ulber."
    },
    {
        "employer": "Coop (Schweiz)",
        "title": "BI Consultant (80–100%)",
        "location": "Basel, Schweiz",
        "sub_date": "17.11.2026",
        "ack_date": "17.11.2026",
        "int1_date": "-",
        "int1_time": "-",
        "int1_interviewer": "-",
        "int2_date": "-",
        "int2_time": "-",
        "int2_interviewer": "-",
        "status": "Bewerbungseingang bestätigt (17.11.2026, Update 20.11.2026)",
        "source": "Stellenportal der Coop-Gruppe (noreply.recruiting@coopgroup.ch)",
        "tasks": "• Weiterentwicklung und Betreuung der konzernweiten Business Intelligence- und Reporting-Landschaft bei Coop Schweiz.\n• Konzeption und Implementierung von Datenmodellen, ETL-Pipelines und Dashboards für den Schweizer Detail- und Großhandel.\n• Enge Zusammenarbeit mit Business-Stakeholdern zur Übersetzung betriebswirtschaftlicher KPIs in moderne Analyseplattformen.",
        "requirements": "Studium Wirtschaftsinformatik; fundierte Kenntnisse in Datenmodellierung, SQL, BI-Tools (Power BI, SAP Analytics Cloud / BW); Verständnis für Handels- und Logistikprozesse.",
        "notes": "Registrierung und Eingang der Bewerbung am 17.11.2026 bestätigt; Status-Update im Stellenportal am 20.11.2026."
    },
    {
        "employer": "Schwarz Digits",
        "title": "Junior SAP HCM User Maintenance & Access Management (IAM) Specialist (m/w/d) [Ref: 4972]",
        "location": "Neckarsulm",
        "sub_date": "13.11.2026",
        "ack_date": "13.11.2026",
        "int1_date": "-",
        "int1_time": "-",
        "int1_interviewer": "-",
        "int2_date": "-",
        "int2_time": "-",
        "int2_interviewer": "-",
        "status": "Bewerbungseingang bestätigt (16.11.2026 per Mail von Albina Kadrija)",
        "source": "Schwarz Gruppe Recruiting (Albina Kadrija <recruiting@mail.schwarz>)",
        "tasks": "• Administration und Qualitätssicherung von Benutzerberechtigungen, Rollen und Berechtigungskonzepten in SAP HCM.\n• Mitarbeit am Identity & Access Management (IAM) der Schwarz Gruppe (Lidl, Kaufland, Schwarz Digits, PreZero).\n• Umsetzung von Audit-, Compliance- und DSGVO-Vorgaben im Berechtigungswesen.",
        "requirements": "Wirtschaftsinformatik-Abschluss; Verständnis von Berechtigungsstrukturen in ERP/HCM; strukturierte und gewissenhafte Arbeitsweise.",
        "notes": "Eingang und Prüfung durch Talent Acquisition Specialist Albina Kadrija am 16.11.2026 bestätigt."
    },
    {
        "employer": "Schwarz Digits",
        "title": "SAP ALM Spezialist (m/w/d) - Schwerpunkt Focused Run und Cloud ALM [Ref: 3267]",
        "location": "Neckarsulm",
        "sub_date": "14.10.2026",
        "ack_date": "14.10.2026",
        "int1_date": "-",
        "int1_time": "-",
        "int1_interviewer": "-",
        "int2_date": "-",
        "int2_time": "-",
        "int2_interviewer": "-",
        "status": "Bewerbungseingang bestätigt (14.10.2026)",
        "source": "Schwarz Gruppe Recruiting (Albina Kadrija / Vanessa Kelsch)",
        "tasks": "• Konzeption, Einführung und operativer Betrieb von SAP Cloud ALM und SAP Focused Run für hochkomplexe Systemlandschaften.\n• Standardisierung von Application Lifecycle Management Prozessen über hybride Landschaften (On-Premise & BTP).\n• Etablierung automatisierter Monitoring-, Alerting- und Release-Management-Workflows.",
        "requirements": "Erfahrung mit SAP Solution Manager / Cloud ALM (wie im SSB-Großprojekt); Verständnis für Architektur-Governance.",
        "notes": "Direkte Passung zu Visars 24-monatiger Erfahrung bei der SSB AG mit SAP Cloud ALM Governance."
    },
    {
        "employer": "Schwarz Digits",
        "title": "(Junior-) AI Product Owner (m/w/d)",
        "location": "Neckarsulm / Heilbronn (Innovation Park AI)",
        "sub_date": "23.11.2026",
        "ack_date": "23.11.2026",
        "int1_date": "-",
        "int1_time": "-",
        "int1_interviewer": "-",
        "int2_date": "-",
        "int2_time": "-",
        "int2_interviewer": "-",
        "status": "Bewerbungseingang bestätigt (23.11.2026)",
        "source": "Schwarz Digits Recruiting Portal (noreply@mail.schwarz)",
        "tasks": "• Product Ownership und Roadmap-Gestaltung für KI-basierte Softwarelösungen und Enterprise-KI-Anwendungen.\n• Schnittstelle zwischen Data Science, Plattform-Engineering und Business-Stakeholdern der Handelssparten.\n• Priorisierung des Product Backlogs nach agilen Frameworks (Scrum, Kanban).",
        "requirements": "Wirtschaftsinformatik Master; fundiertes Verständnis generativer KI, API-Architekturen und digitaler Geschäftsmodelle.",
        "notes": "Ganz frisch eingereicht am 23.11.2026."
    },
    {
        "employer": "Stuttgarter Straßenbahnen AG (SSB)",
        "title": "IT Solution Architect (m/w/d)",
        "location": "Stuttgart-Möhringen",
        "sub_date": "19.09.2026",
        "ack_date": "19.09.2026",
        "int1_date": "-",
        "int1_time": "-",
        "int1_interviewer": "-",
        "int2_date": "-",
        "int2_time": "-",
        "int2_interviewer": "-",
        "status": "In Prüfung / Abstimmung (Rückmeldung Daniela Trotus am 06.11.2026)",
        "source": "Interne Bewerbung / SSB Stellenmarkt (Daniela Trotus, IT-Bereichsleitung)",
        "tasks": "• Architektonische Gesamtsteuerung und Weiterentwicklung der Anwendungs- und Schnittstellenlandschaft der SSB AG.\n• Definition verbindlicher Architekturstandards und Integrationsmuster im Rahmen der SAP S/4HANA Transformation.\n• Begleitung des Solution Designs (SDD) und Abstimmung zwischen Fachbereichen, TPLs und externen Implementierungspartnern.",
        "requirements": "Master Wirtschaftsinformatik; vertieftes Wissen über Enterprise Architecture Management (TOGAF, Bimodale IT); 24 Monate Praxiserfahrung im SSB-Projekt SAP4SSB.",
        "notes": "Direkte Fortführung der Werkstudententätigkeit im IT-PMO / TP5; regelmäßiger Austausch mit Daniela Trotus."
    },
    {
        "employer": "Stuttgarter Straßenbahnen AG (SSB)",
        "title": "Referent:in Prozessmanagement und Datenschutz im Bereich IT (m/w/d)",
        "location": "Stuttgart-Möhringen",
        "sub_date": "03.07.2026",
        "ack_date": "03.07.2026",
        "int1_date": "-",
        "int1_time": "-",
        "int1_interviewer": "-",
        "int2_date": "-",
        "int2_time": "-",
        "int2_interviewer": "-",
        "status": "In Prüfung (Laura Bulke, SSB AG)",
        "source": "Interne Bewerbung / SSB Stellenmarkt",
        "tasks": "• Modellierung, Harmonisierung und Dokumentation von IT- und Betriebsprozessen in SAP Signavio nach BPMN 2.0.\n• Sicherstellung der datenschutzrechtlichen Compliance (DSGVO, Löschkonzepte) in IT-Systemen und Migrationspipelines.\n• Beratung der Fachbereiche bei Prozessoptimierungen und internen Kontrollsystemen.",
        "requirements": "Kenntnisse in BPMN 2.0, Signavio, DSGVO und Prozess-Governance.",
        "notes": "Bewerbung eingereicht bei Laura Bulke."
    },
    {
        "employer": "Computacenter",
        "title": "Trainee IT Service Architecture & Design (w/m/d)",
        "location": "Stuttgart / Bundesweit",
        "sub_date": "27.05.2026",
        "ack_date": "27.05.2026",
        "int1_date": "11.06.2026",
        "int1_time": "17:00 Uhr (Teams Videointerview)",
        "int1_interviewer": "Lili Potyondi (HR) / Tobias (Lead Architect)",
        "int2_date": "-",
        "int2_time": "-",
        "int2_interviewer": "-",
        "status": "⭐ Videointerview am 11.06.2026 absolviert",
        "source": "Computacenter Karriere-Team (Paula Weber / Lili Potyondi / MB_HR_OS@computacenter.com)",
        "tasks": "• Ganzheitliches Design von Enterprise IT-Service-Architekturen nach ITIL 4 für globale Großkonzerne.\n• Konzeption hybrider Cloud- und Rechenzentrumsmodelle (Private/Public Cloud, DC1-Infrastruktur-Erfahrung).\n• Erstellung technischer Servicekataloge, SLAs und Service-Delivery-Konzepte.",
        "requirements": "Abschluss Wirtschaftsinformatik; Fundierung in ITIL 4 Service Operations (aus 12 Monaten Datacenter One INOC); analytische Stärke.",
        "notes": "Videointerview am 11.06.2026 um 17:00 Uhr via Microsoft Teams erfolgreich geführt."
    },
    {
        "employer": "Deutsche Bahn",
        "title": "Mitarbeiter:in Reisendenlenkung für Bahnhöfe in Baden-Württemberg [DB Zeitarbeit GmbH]",
        "location": "Stuttgart / Baden-Württemberg",
        "sub_date": "18.10.2026",
        "ack_date": "18.10.2026",
        "int1_date": "02.11.2026",
        "int1_time": "10:00 Uhr (Vorstellungsgespräch)",
        "int1_interviewer": "Berina Alomerovic (DB Zeitarbeit)",
        "int2_date": "-",
        "int2_time": "-",
        "int2_interviewer": "-",
        "status": "⭐ Vorstellungsgespräch am 02.11.2026 absolviert",
        "source": "Bewerbermanagement DB Zeitarbeit (Berina.B.Alomerovic@deutschebahn.com)",
        "tasks": "• Operative Unterstützung und Reisendenlenkung an Knotenbahnhöfen in Baden-Württemberg.\n• Deeskalation, Informationsbereitstellung und Schnittstelle zu Leitstellen.",
        "requirements": "Kommunikationsstärke, Flexibilität, Zuverlässigkeit.",
        "notes": "Terminbestätigung und Vorstellungsgespräch am 02.11.2026."
    },
    {
        "employer": "EY (Ernst & Young)",
        "title": "(Junior) Consultant - Technology Consulting / ERP & SAP Transformation [Ref: 13743137]",
        "location": "Stuttgart",
        "sub_date": "19.09.2026",
        "ack_date": "19.09.2026",
        "int1_date": "19.10.2026",
        "int1_time": "Online / Telefoninterview",
        "int1_interviewer": "Karolina Żukowska / Dorota Iwaniak (EY GDS / Talent Acquisition)",
        "int2_date": "-",
        "int2_time": "-",
        "int2_interviewer": "-",
        "status": "⭐ Interview bestätigt (19.10.2026 / 02.10.2026)",
        "source": "EY Talent Attraction & Acquisition (TalentAttractionandAcquisition@ey.com)",
        "tasks": "• Beratung internationaler Mandanten bei komplexen SAP S/4HANA Transformationsprogrammen.\n• Prozessanalyse, Fit-Gap-Workshops, Migrationskonzeption und Architektur-Audits.\n• Digitalisierungsberatung im Spannungsfeld von Cloud, ERP und Business Intelligence.",
        "requirements": "Sehr guter Masterabschluss Wirtschaftsinformatik; starke analytische Fähigkeiten; Englisch fließend.",
        "notes": "Bewerbungsfragebogen via DocuSign eingereicht; Interview und Statusabgleich im Oktober 2026 bestätigt."
    },
    {
        "employer": "x1F",
        "title": "(Junior) Consultant SAP Business Data Cloud (m/w/d)",
        "location": "Stuttgart / Frankfurt",
        "sub_date": "30.10.2026",
        "ack_date": "30.10.2026",
        "int1_date": "-",
        "int1_time": "-",
        "int1_interviewer": "-",
        "int2_date": "-",
        "int2_time": "-",
        "int2_interviewer": "-",
        "status": "Absage am 06.11.2026 per E-Mail (Sabrina Günzel)",
        "source": "x1F career (candidate-sr4sl8lx@career.x1f.one)",
        "tasks": "• Beratung zu modernen SAP Data Cloud Architekturen, SAP Datasphere und SAP Analytics Cloud.\n• Datenmodellierung und Konzeption cloudbasierter Data Warehouses.",
        "requirements": "Wirtschaftsinformatik; Kenntnisse in Cloud-Data-Plattformen und SQL.",
        "notes": "Unterlagen gesichtet, freundliche Absage am 06.11.2026 erhalten."
    },
    {
        "employer": "Hengstenberg",
        "title": "SAP Inhouse-Berater PM / CS bzw. PP (m/w/d)",
        "location": "Esslingen am Neckar",
        "sub_date": "19.05.2026",
        "ack_date": "19.05.2026",
        "int1_date": "-",
        "int1_time": "-",
        "int1_interviewer": "-",
        "int2_date": "-",
        "int2_time": "-",
        "int2_interviewer": "-",
        "status": "In Prüfung (Sülbiye Deger)",
        "source": "Hengstenberg Karriereportal (d.vinci easy)",
        "tasks": "• Betreuung und Customizing der SAP-Module PP (Produktionsplanung) sowie PM/CS (Instandhaltung & Customer Service).\n• Anforderungsaufnahme der Produktionsstandorte, Implementierung von Prozessverbesserungen.\n• First- und Second-Level Support für Key-User und Durchführung von Schulungen.",
        "requirements": "Wirtschaftsinformatik-Abschluss; Modulkenntnisse SAP ERP / S/4HANA; Freude an Schnittstellen zu Fertigungsprozessen.",
        "notes": "Bewerbung für beide Schwerpunkte eingereicht."
    },
    {
        "employer": "LTI-Metalltechnik",
        "title": "ERP-Anwendungsbetreuer (m/w/d)",
        "location": "Schrozberg / Boxberg",
        "sub_date": "05.11.2026",
        "ack_date": "05.11.2026",
        "int1_date": "-",
        "int1_time": "-",
        "int1_interviewer": "-",
        "int2_date": "-",
        "int2_time": "-",
        "int2_interviewer": "-",
        "status": "In Prüfung",
        "source": "jobs@lti-metalltechnik.de",
        "tasks": "• Ganzheitliche Betreuung und Optimierung der unternehmensweiten ERP-Landschaft.\n• Analyse betrieblicher Abläufe in Fertigung und Logistik zur digitalen Prozessabbildung.\n• Anbindung von Subsystemen und Erstellung von Auswertungen.",
        "requirements": "Fundiertes ERP-Verständnis, SQL-Kenntnisse, Hands-on-Mentalität.",
        "notes": "Eingangsbestätigung liegt vor."
    },
    {
        "employer": "Rheinmetall",
        "title": "SAP Power-Keyuser / Disponent (m/w/d)",
        "location": "Neckarsulm",
        "sub_date": "22.09.2026",
        "ack_date": "22.09.2026",
        "int1_date": "-",
        "int1_time": "-",
        "int1_interviewer": "-",
        "int2_date": "-",
        "int2_time": "-",
        "int2_interviewer": "-",
        "status": "Absage am 26.10.2026 per E-Mail",
        "source": "Alexander Flasch (alexander.flasch@cc.recruitmail.com)",
        "tasks": "• Steuerung von Dispositionsprozessen und Materialbedarfsplanung in SAP ERP / S/4HANA.\n• Keyuser-Tätigkeiten: Testen von Releasewechseln, Schulung von Anwendern.",
        "requirements": "Erfahrung in ERP-Disposition, Modulkenntnisse MM/PP.",
        "notes": "Absage per E-Mail am 26.10.2026."
    },
    {
        "employer": "appliedAI",
        "title": "AI Consultant (m/f/x)",
        "location": "München / Remote",
        "sub_date": "19.09.2026",
        "ack_date": "19.09.2026",
        "int1_date": "-",
        "int1_time": "-",
        "int1_interviewer": "-",
        "int2_date": "-",
        "int2_time": "-",
        "int2_interviewer": "-",
        "status": "In Prüfung (appliedAI People-Team)",
        "source": "jobs@appliedai.de",
        "tasks": "• Strategische Beratung von Industrieunternehmen bei der Einführung und Skalierung von Künstlicher Intelligenz.\n• Konzeption von AI-Use-Cases, Evaluation von GenAI-Architekturen und Begleitung von Piloten.",
        "requirements": "Master Wirtschaftsinformatik; fundiertes Verständnis für Maschinelles Lernen, LLM-Architekturen und Innovationsmanagement.",
        "notes": "Bestätigt am 21.09.2026."
    },
    {
        "employer": "MHP (Porsche Company)",
        "title": "SAP HCM Consultant (all genders) [RE-ID: nbiayduedl]",
        "location": "Ludwigsburg / Stuttgart",
        "sub_date": "01.10.2026",
        "ack_date": "01.10.2026",
        "int1_date": "-",
        "int1_time": "-",
        "int1_interviewer": "-",
        "int2_date": "-",
        "int2_time": "-",
        "int2_interviewer": "-",
        "status": "In Prüfung (MHP Recruiting)",
        "source": "job@recruiting.mhp.com",
        "tasks": "• Beratung führender Automobil- und Industriehersteller bei der digitalen Transformation von HR-Prozessen.\n• Konzeption und Implementierung von SAP SuccessFactors und SAP HCM-Lösungen.",
        "requirements": "Erfahrung im HR-IT-Umfeld, Begeisterung für Automotive und Consulting.",
        "notes": "Bewerbung im MHP Karriereportal eingereicht."
    },
    {
        "employer": "Bundesverwaltungsamt (THW)",
        "title": "Sachbearbeitung Administration (m/w/d) im ITCC [Kennziffer: THW-2026-135]",
        "location": "Neuhausen auf den Fildern",
        "sub_date": "19.05.2026",
        "ack_date": "19.05.2026",
        "int1_date": "-",
        "int1_time": "-",
        "int1_interviewer": "-",
        "int2_date": "-",
        "int2_time": "-",
        "int2_interviewer": "-",
        "status": "In Prüfung (Bundesverwaltungsamt / THW)",
        "source": "personalgewinnung@bva.bund.de",
        "tasks": "• Administrative und organisatorische Koordination im International Training Coordination Center (ITCC).\n• IT-Support, Benutzerverwaltung und Pflege von Ausbildungsdatenbanken.",
        "requirements": "Verwaltungs- und IT-Affinität, Zuverlässigkeitsüberprüfung.",
        "notes": "Bewerbung wird gesichtet."
    },
    {
        "employer": "HdM Stuttgart",
        "title": "Technischer Angestellter IT-Infrastruktur (m/w/d)",
        "location": "Stuttgart-Vaihingen",
        "sub_date": "19.05.2026",
        "ack_date": "19.05.2026",
        "int1_date": "-",
        "int1_time": "-",
        "int1_interviewer": "-",
        "int2_date": "-",
        "int2_time": "-",
        "int2_interviewer": "-",
        "status": "In Prüfung (Michaela Zobel-Kuffert / Naomi Seiler)",
        "source": "karriere.hdm-stuttgart.de",
        "tasks": "• Betreuung und Administration von Hochschulservern, Netzwerken und Medientechnik an der Hochschule der Medien.",
        "requirements": "Informatik/Wirtschaftsinformatik-Kenntnisse, Linux/Windows-Server.",
        "notes": "Bewerbung liegt dem Personalrat vor."
    },
    {
        "employer": "Teamative",
        "title": "(Junior) SAP S/4HANA Consultant (m/w/d)",
        "location": "Stuttgart / Remote",
        "sub_date": "29.04.2026",
        "ack_date": "30.04.2026",
        "int1_date": "04.05.2026",
        "int1_time": "Kennenlerngespräch",
        "int1_interviewer": "Teamative Geschäftsführung",
        "int2_date": "11.05.2026",
        "int2_time": "Zweitgespräch / Case Study",
        "int2_interviewer": "Senior SAP Architects",
        "status": "Absage am 19.05.2026 per Mail (\"Stelle wurde vorerst geschlossen\")",
        "source": "Teamative Karriere",
        "tasks": "• Beratung mittelständischer Kunden bei der Migration auf SAP S/4HANA.\n• Implementierung von Finanz- und Logistikmodulen.",
        "requirements": "S/4HANA Know-how, Hands-on-Mentalität.",
        "notes": "Beide Gesprächsrunden sehr erfolgreich absolviert. Absage erfolgte aus strategischen Gründen wegen vorübergehender Schließung der Stelle."
    },
    {
        "employer": "All for One Group",
        "title": "Integrationsmanager / SAP Integration Consultant (m/w/d)",
        "location": "Filderstadt",
        "sub_date": "05.05.2026",
        "ack_date": "12.05.2026",
        "int1_date": "-",
        "int1_time": "-",
        "int1_interviewer": "-",
        "int2_date": "-",
        "int2_time": "-",
        "int2_interviewer": "-",
        "status": "Absage am 12.05.2026 per Mail-Template",
        "source": "All for One Karriere",
        "tasks": "• Technische Integration von SAP S/4HANA mit Cloud- und Drittsystemen über SAP BTP Integration Suite.",
        "requirements": "Integrationswissen, API-Management.",
        "notes": "Absage per Mail-Template."
    },
    {
        "employer": "Drees & Sommer",
        "title": "HR IT Consultant (w/m/d) SAP SuccessFactors & Global HR Solutions",
        "location": "Stuttgart",
        "sub_date": "05.05.2026",
        "ack_date": "12.05.2026",
        "int1_date": "-",
        "int1_time": "-",
        "int1_interviewer": "-",
        "int2_date": "-",
        "int2_time": "-",
        "int2_interviewer": "-",
        "status": "Absage am 12.05.2026 per Mail-Template",
        "source": "Drees & Sommer Karriere",
        "tasks": "• Betreuung und Weiterentwicklung der globalen HR-IT-Systeme (SAP SuccessFactors).\n• Digitalisierung von HR-Workflows.",
        "requirements": "HR-IT-Verständnis, Consulting-Mentalität.",
        "notes": "Absage per Mail-Template."
    },
    {
        "employer": "cbs Corporate Business Solutions",
        "title": "Trainee SAP Landscape Transformation (m/w/d)",
        "location": "Heidelberg / Stuttgart",
        "sub_date": "15.05.2026",
        "ack_date": "18.05.2026",
        "int1_date": "-",
        "int1_time": "-",
        "int1_interviewer": "-",
        "int2_date": "-",
        "int2_time": "-",
        "int2_interviewer": "-",
        "status": "Absage am 18.05.2026 per Mail-Template",
        "source": "cbs Karriere",
        "tasks": "• Selektive Datenmigration und Landscape Transformation auf SAP S/4HANA mit dem cbs Enterprise Transformer.",
        "requirements": "Wirtschaftsinformatik, Begeisterung für Datenstrukturen.",
        "notes": "Absage per Mail-Template."
    },
    {
        "employer": "ConVista",
        "title": "Trainee (Mensch*) – Consulting Master Class mit Fokus SAP",
        "location": "Köln / Frankfurt / Remote",
        "sub_date": "17.05.2026",
        "ack_date": "17.05.2026",
        "int1_date": "-",
        "int1_time": "-",
        "int1_interviewer": "-",
        "int2_date": "-",
        "int2_time": "-",
        "int2_interviewer": "-",
        "status": "In Prüfung",
        "source": "ConVista Karriere",
        "tasks": "• Intensives Consulting-Traineeprogramm mit Zertifizierungen in SAP S/4HANA und Projektmanagement.",
        "requirements": "Master Wirtschaftsinformatik.",
        "notes": "Eingang bestätigt."
    },
    {
        "employer": "Deloitte",
        "title": "Consultant SAP Public Sector (m/w/d)",
        "location": "Stuttgart",
        "sub_date": "22.04.2026",
        "ack_date": "12.05.2026",
        "int1_date": "-",
        "int1_time": "-",
        "int1_interviewer": "-",
        "int2_date": "-",
        "int2_time": "-",
        "int2_interviewer": "-",
        "status": "Absage am 12.05.2026 per Mail-Template",
        "source": "Deloitte Karriere",
        "tasks": "• Beratung der öffentlichen Verwaltung bei der Einführung von SAP S/4HANA.",
        "requirements": "Public Sector Affinität, SAP-Kenntnisse.",
        "notes": "Absage per Mail-Template."
    },
    {
        "employer": "Axians",
        "title": "SAP Solution Architect (m/w/d)",
        "location": "Ulm / Stuttgart",
        "sub_date": "28.04.2026",
        "ack_date": "-",
        "int1_date": "-",
        "int1_time": "-",
        "int1_interviewer": "-",
        "int2_date": "-",
        "int2_time": "-",
        "int2_interviewer": "-",
        "status": "In Prüfung / Networking (Kontakt Axians Lead Architekten aus SSB-Projekt)",
        "source": "Axians Karriere",
        "tasks": "• Design komplexer SAP-Architekturen und Migrationspfade für Enterprise-Kunden.",
        "requirements": "Enterprise Architecture, S/4HANA Know-how.",
        "notes": "Axians war einer der beiden Hauptimplementierungspartner im SSB-Großprojekt."
    },
    {
        "employer": "Mercedes-Benz",
        "title": "SAP Junior Developer (d/m/w/x)",
        "location": "Stuttgart-Untertürkheim",
        "sub_date": "29.04.2026",
        "ack_date": "-",
        "int1_date": "-",
        "int1_time": "-",
        "int1_interviewer": "-",
        "int2_date": "-",
        "int2_time": "-",
        "int2_interviewer": "-",
        "status": "In Prüfung",
        "source": "Mercedes-Benz Karriere",
        "tasks": "• Entwicklung von ABAP / CDS Views und Erweiterungen in der Mercedes-Benz SAP-Infrastruktur.",
        "requirements": "Programmierkenntnisse, SAP-Basis.",
        "notes": "In Prüfung."
    }
]

print(f"Definierte Detail-Profile: {len(JOB_PROFILES)}")

def parse_date(date_str):
    if not date_str or date_str == "-":
        return None
    m = re.search(r"(\d{1,2})\.(\d{1,2})\.(\d{4})", str(date_str))
    if m:
        return datetime(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    return None

def build_excel_and_markdown():
    # Load or create Excel
    wb = openpyxl.Workbook()
    
    # ------------------ SHEET 1: Bewerbungsverlauf ------------------
    ws1 = wb.active
    ws1.title = "Bewerbungsverlauf"
    
    # Styles
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
        
    # Sort profiles: newest sub_date first
    def profile_sort_key(p):
        d = parse_date(p.get("sub_date"))
        if d:
            return d
        return datetime(2024, 1, 1)
        
    sorted_profiles = sorted(JOB_PROFILES, key=profile_sort_key, reverse=True)
    
    for r_idx, p in enumerate(sorted_profiles, start=2):
        ws1.row_dimensions[r_idx].height = 24
        is_interview = (p.get("int1_date") not in ["-", None]) or ("interview" in p.get("status", "").lower()) or ("gespräch" in p.get("status", "").lower())
        is_even = (r_idx % 2 == 0)
        
        row_vals = [
            p["employer"],
            p["title"],
            p["sub_date"],
            p["ack_date"],
            p["int1_date"],
            p["int2_date"],
            p["status"]
        ]
        
        for c_idx, val in enumerate(row_vals, start=1):
            cell = ws1.cell(row=r_idx, column=c_idx)
            cell.value = str(val or "-")
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
        "Interview-Historie & Gesprächspartner", "Quelle / Empfehlung"
    ]
    ws2.append(col_headers_2)
    ws2.row_dimensions[1].height = 28
    
    for c_idx in range(1, len(col_headers_2) + 1):
        cell = ws2.cell(row=1, column=c_idx)
        cell.fill = navy_fill
        cell.font = white_font
        cell.alignment = center_align
        cell.border = thin_border
        
    for r_idx, p in enumerate(sorted_profiles, start=2):
        ws2.row_dimensions[r_idx].height = 65
        is_even = (r_idx % 2 == 0)
        
        int_history = ""
        if p["int1_date"] != "-":
            int_history += f"1. Gespräch: {p['int1_date']} ({p.get('int1_time', '')}) | {p.get('int1_interviewer', '')}\n"
        if p["int2_date"] != "-":
            int_history += f"2. Gespräch: {p['int2_date']} ({p.get('int2_time', '')}) | {p.get('int2_interviewer', '')}\n"
        if not int_history:
            int_history = p.get("status", "-")
            
        row_vals = [
            p["employer"],
            p["title"],
            p.get("location", "Deutschland"),
            p.get("tasks", "-"),
            p.get("requirements", "-"),
            int_history.strip(),
            p.get("source", "-")
        ]
        
        for c_idx, val in enumerate(row_vals, start=1):
            cell = ws2.cell(row=r_idx, column=c_idx)
            cell.value = str(val or "-")
            cell.border = thin_border
            cell.alignment = wrap_left if c_idx in [2, 4, 5, 6, 7] else (center_align if c_idx == 3 else left_align)
            cell.font = bold_font if c_idx == 1 else reg_font
            if is_even:
                cell.fill = zebra_fill
                
    ws2.column_dimensions["A"].width = 22
    ws2.column_dimensions["B"].width = 40
    ws2.column_dimensions["C"].width = 20
    ws2.column_dimensions["D"].width = 65
    ws2.column_dimensions["E"].width = 50
    ws2.column_dimensions["F"].width = 55
    ws2.column_dimensions["G"].width = 40
    
    wb.save(EXCEL_PATH)
    print(f"✅ Excel erfolgreich mit 2 Sheets gespeichert: {EXCEL_PATH}")
    
    # ------------------ Obsidian Cockpit Markdown ------------------
    table_lines = [
        "| Arbeitgeber | Genaue Stellenbezeichnung | Datum | Eingang | 1. Gespräch | 2. Gespräch | Status / Ergebnis |",
        "| :--- | :--- | :---: | :---: | :---: | :---: | :--- |"
    ]
    for p in sorted_profiles:
        comp = f"**{p['employer']}**"
        title = p["title"]
        sub_d = p["sub_date"]
        ack_d = p["ack_date"]
        int1_d = p["int1_date"]
        int2_d = p["int2_date"]
        stat = p["status"]
        table_lines.append(f"| {comp} | {title} | {sub_d} | {ack_d} | {int1_d} | {int2_d} | {stat} |")
    table_md = "\n".join(table_lines)
    
    # Generate Dossier Cards in Markdown
    dossier_blocks = []
    dossier_blocks.append("## 📑 Detaillierte Stellenbeschreibungen, Aufgaben & Interview-Historie\n")
    
    for p in sorted_profiles:
        comp = p["employer"]
        title = p["title"]
        loc = p.get("location", "-")
        stat = p.get("status", "-")
        tasks_fmt = "\n".join([f">   {line}" for line in p.get("tasks", "").splitlines() if line.strip()])
        req_fmt = p.get("requirements", "-")
        notes_fmt = p.get("notes", "-")
        
        int_section = ""
        if p["int1_date"] != "-":
            int_section += f"> - **1. Gespräch:** {p['int1_date']} ({p.get('int1_time', '')}) – *Interviewer:* {p.get('int1_interviewer', '-')}\n"
        if p["int2_date"] != "-":
            int_section += f"> - **2. Gespräch:** {p['int2_date']} ({p.get('int2_time', '')}) – *Interviewer:* {p.get('int2_interviewer', '-')}\n"
        if not int_section:
            int_section = f"> - *Kein Vorstellungsgespräch terminiert / Status: {stat}*\n"
            
        card = f"""> [!INFO] **{comp} – {title}**
> - **Standort:** {loc}
> - **Tag der Einreichung:** {p['sub_date']} | **Bewerbungseingang:** {p['ack_date']}
> - **Quelle / Kontakt:** {p.get('source', '-')}
> - **Aktueller Status:** `{stat}`
> 
> #### 💬 Gesprächsrunden & Interview-Timeline
{int_section}> 
> #### 📌 Aufgaben & Tätigkeitsbereiche
{tasks_fmt}
> 
> #### 🎯 Anforderungsprofil & Passung
>   {req_fmt}
> 
> #### 💡 Prozess-Notizen & Hintergrund
>   {notes_fmt}
"""
        dossier_blocks.append(card)
        
    dossier_md = "\n".join(dossier_blocks)
    
    # Read and replace in Obsidian Cockpit
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
        
    # Export enriched JSON Pipeline
    with open(PIPELINE_JSON, "w", encoding="utf-8") as f:
        json.dump(sorted_profiles, f, indent=2, ensure_ascii=False)
    print(f"✅ JSON Pipeline exportiert: {PIPELINE_JSON}")

if __name__ == "__main__":
    build_excel_and_markdown()
