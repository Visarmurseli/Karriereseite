# -*- coding: utf-8 -*-
"""
Auto-Organizer & Short-Title Renamer for `05_Fachliteratur_Bibliothek/`.

Reads metadata/title + frontmatter/first pages of .epub and .pdf files,
shortens filenames cleanly to book titles, checks thematic fit against Visar's
Career OS domains (SAP/ERP, Audit/Governance, EAM/Cloud/BPM, AI/Data, Consulting/BWL),
routes off-topic books to `99_Off_Topic_Nicht_Fuer_RAG/` (skipped by RAG), and
moves matching books into `01_...`..`06_...` subfolders.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import os
import re
import shutil
import sys
import xml.etree.ElementTree as ET
import zipfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
LIB_DIR = os.path.join(BASE_DIR, "05_Fachliteratur_Bibliothek")

CATEGORY_DIRS = [
    "01_SAP_S4HANA_BTP_CleanCore",
    "02_IT_Audit_Governance_Compliance",
    "03_Enterprise_Architecture_Cloud",
    "04_AI_Engineering_Data_Automation",
    "05_Consulting_BWL_VISMUV",
    "06_Open_Access_Standards",
    "07_Wirtschaftsinformatik_IT_Grundlagen",
    "08_Unternehmertum_Marketing_VISMUV",
    "99_Off_Topic_Nicht_Fuer_RAG",
]

OFF_TOPIC_SUBDIRS = [
    "01_Belletristik_Klassiker_Romane",
    "02_Biografien_Musik_Zeitgeschichte",
    "03_Psychologie_Fitness_SelfHelp",
    "04_Politik_Gesellschaft_Medien_Recht",
    "05_Finanzen_Boerse_Krypto_VWL",
    "06_Branchen_Medizin_Biotech_Varia",
    "07_Privatdokumente_Unvollstaendige_Downloads",
]

SKIP_TRACKER_FILES = {"00_UB_Stuttgart_Literatur_Checkliste.md", "README.md", "Thumbs.db", ".DS_Store"}

UMLAUT_TRANS = str.maketrans({
    "ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss",
    "Ä": "Ae", "Ö": "Oe", "Ü": "Ue",
})

# Weighted domain scoring keywords (match against title * 4 + intro_text * 1 using boundary-aware regexes)
DOMAIN_KEYWORDS = {
    "01_SAP_S4HANA_BTP_CleanCore": [
        "sap", "s/4hana", "s4hana", "btp", "abap", "clean core", "fiori", "ltmc",
        "integration suite", "embedded analytics", "business warehouse", "bw/4hana",
        "sap pp", "asset management", "erp-software", "erp software", "financial accounting",
        "controlling", "elementarfaktoren", "signavio", "cloud alm", "enable now",
        "rise with sap", "hyperscaler clouds", "e-learning artefact", "berechtigungen",
        "brownfield", "greenfield", "web dynpro", "smartforms", "sap scripts",
        "successfactors", "architekturmodell für sap", "profikurs abap",
        "sap hana", "sap ui", "business data cloud", "event-driven sap",
        "bn4l", "sap enterprise portfolio", "sap supply chain", "sap rise",
        "enterprise resource planning",
    ],
    "02_IT_Audit_Governance_Compliance": [
        "audit", "it-audit", "it-revision", "it-grc", "wirtschaftsprüfung", "iks",
        "interne kontrollsysteme", "internal control", "segregation of duties", "cobit",
        "compliance", "dsgvo", "gdpr", "betriebsrat", "betrvg", "idw ps", "sox",
        "nis2", "ai act", "risikomanagement", "it-sicherheit", "it-sicherheitsmaßnahmen",
        "cybersecurity", "cyber security", "cyberstrategien", "cyber-souveränität", "grundschutz",
        "datenschutz", "datenschutzanforderungen", "penetration testing", "hacking",
        "information security", "informationssicherheit", "identity and access",
        "identity access management", "identity analytics", "enterprise identity",
        "identity operating model", "enterprise governance of information technology",
        "it governance", "governance-first ai", "ai governance", "iso 27002",
        "softwarelizenzmanagement", "jailbreaking llms", "sap security governance",
    ],
    "03_Enterprise_Architecture_Cloud": [
        "enterprise architecture", "enterprise design", "togaf", "geschäftsprozess",
        "geschäftsprozesse", "business process management", "bpmn", "domain-driven",
        "microservices", "event-driven", "cloud-architektur", "cloud architecture",
        "cloud computing", "cloud-native", "cloud networking", "public cloud",
        "spring boot", "spring cloud", "itil", "service operations",
        "it service management", "servicenow", "site reliability engineering",
        "schatten-it", "information systems outsourcing", "digitale transformation",
        "digital transformation", "software architecture", "software-architektur",
        "architekturreview", "serverless", "kubernetes", "informationsmanagement",
        "open source software", "offene systeme", "digitale souveränität",
        "digitale plattformen", "digitalen plattformen", "management digitaler plattformen",
        "netzwerktechnik", "systemintegration",
    ],
    "04_AI_Engineering_Data_Automation": [
        "artificial intelligence", "künstliche intelligenz", "ki mit köpfchen",
        "machine learning", "maschinelles lernen", "deep learning", "large language model",
        "llm", "llms", "retrieval-augmented", "rag", "generative ai", "agentic ai",
        "agenticdev", "ai agents", "business ai", "prompt engineering", "vector search",
        "knowledge graph", "data engineering", "data science", "data analytics", "big data",
        "business analytics", "digital analytics", "python for business",
        "datenmanagement", "cloud-datenmanagement", "datenbankentwurf", "datenbanken",
        "datenanalyse", "sql", "azure sql", "powershell", "python automation",
        "building ai systems", "chatgpt", "langchain", "langgraph", "n8n", "ollama",
        "objektorientierte programmierung", "grundkurs java", "java", "softwareentwicklung",
        "automatisierter softwaretests", "softwaretesting", "neural network", "transformer",
        "sprachmodelle", "ai explained", "robotic process automation", "rpa",
        "hyperautomation", "hybrid intelligence", "hybrid artificial intelligent",
        "applied ai", "ai through llms", "data lakehouse", "ki, statistik",
        "managing human and artificial knowledge", "intelligent technologies",
        "information technology and intelligence",
    ],
    "05_Consulting_BWL_VISMUV": [
        "consulting", "beratung", "unternehmensberatung", "case interview", "stakeholder",
        "projektmanagement", "project management", "ipma", "agil", "scrum",
        "kostenrechnung", "kalkulation", "kennzahlen", "organisationstheorie",
        "personalmanagement", "betriebswirtschaft", "führung", "leadership",
        "verhandlung", "transportrecht", "logistik", "kurier", "fuhrpark", "einkauf",
        "geschäftsmodell", "geschäftsmodelle", "business model", "business models",
        "change management", "human element", "overcoming the resistance",
        "schnelles denken", "verhaltensökonomie", "behavioral economics", "kahneman",
        "management reporting", "unternehmensführung", "wertschöpfungsnetzwerk",
        "wissensmanagement", "knowledge management", "knowledge is power", "innovation gap",
        "innovationsmanagement", "ambidextres",
        "knowledge & co-creation", "wirtschaftsinformatik-forschung",
        "forschungsdesigns der wirtschaftsinformatik", "digitales management",
        "organizational transmission of ai", "ai adoption", "supply chain",
        "supply chain management", "arbeitswelt", "arbeit 4.0", "beyond automation",
        "digitaler humanismus", "people management", "human capital supply chain",
        "dienstleistungsmanagement", "agilität", "motivation & agilität",
        "plattform-geschäftsmodelle", "integrierte business",
        "effiziente zentralisierung in it", "chefsache zukunft", "digitalen wandel",
    ],
    "06_Open_Access_Standards": [
        "bsi-standard", "nist", "eu-verordnung", "richtlinie (eu)", "rfc", "iso/iec",
    ],
    "07_Wirtschaftsinformatik_IT_Grundlagen": [
        "wirtschaftsinformatik", "anwendungsorientierte wirtschaftsinformatik",
        "grundkurs wirtschaftsinformatik", "einführung in die wirtschaftsinformatik",
        "grundzüge der wirtschaftsinformatik", "anforderungsmanagement",
        "requirements engineering", "prozessanalyse", "javafx", "openjfx",
        "javaserver faces", "jsf", "kotlin", "creative dsls",
        "programm- und systementwicklung", "lagerverwaltung", "smile prototyp",
        "vba für office", "office-automatisierung", "microsoft 365", "portable genius",
        "robotik in der wirtschaftsinformatik",
    ],
    "08_Unternehmertum_Marketing_VISMUV": [
        "gmbh-gründung", "software-startup gründen", "gründen mit erfolg", "business-inkubation",
        "nachhaltig gründen", "nachhaltige unternehmensführung", "gemeinwohlorientierte unternehmensführung",
        "regenerative geschäftsmodelle", "marketing", "datengetriebenes marketing",
        "marktforschung", "kundenmanagement", "vertrieb", "verkauf", "crm",
        "sales enablement", "sales management", "sales strategies",
        "ai startup", "entrepreneurship", "e-commerce",
    ],
}

OFF_TOPIC_DAMPENERS = [
    "kochbuch", "rezepte", "roman", "fantasy", "thriller", "gedichte", "garten",
    "fitness-rezepte", "strick", "häkel", "astrophysik", "zahnmedizin",
    "börse", "aktien", "wall street", "bitcoin", "substanzen", "alkohol",
    "pro forma", "proforma", "bestellungsdokument", "männlichkeit", "seduction",
    "fasting", "why we sleep", "bodybuilding", "mentzer", "diary of a ceo",
    "surrounded by idiots", "make the right choice", "unleash the fun", "human action",
    "aryan brotherhood", "rothschilds", "che guevara", "elon musk", "steve jobs",
    "tupac", "big five for life", "die kunst, einen",
    "ehealth", "life sciences", "disaster management", "higher education", "university of the future",
    "canadian economy", "older adults", "veranstaltungsbranche", "online-coaching",
    "human rights", "zwischen wissen und nichtwissen", "heidi heilmann", "navigating your career",
    "moroccan", "automotive firms", "sustainable human resource",
    "coveronly", "palm sap", "sweeteners", "plant viruses", "characterization of plant",
    "medical imaging", "digital health", "healthy world", "vehicle dynamics", "human-vehicle",
    "soc design", "bankbetriebslehre", "gesellschaft in der gesellschaft", "crew resource management",
    "lobachevskii", "sozialer arbeit", "alles steckt in dir", "emotional kompetent",
    "resilienz-stärkende", "berufliche bildung", "insurance & innovation",
    "arbeitsschutz", "desktop-publishing", "building and activating innovative human capital",
    "big data industry", "okved2", "understanding_the_success_factors_of_technological",
    "climate change", "fashion marketing", "bauwirtschaft", "kultureinrichtungen",
    "new world order", "brics", "trumps zweite", "ukraine-krieg", "kalte krieg",
    "sicherheitspolitik", "friedensordnungen", "staatsbildung", "georessourcen",
    "environment as a weapon", "digital ethics lab",
    "karriere-helfer", "karriere helfer", "karriere-websites", "selbstmanagement",
    "anti-stress-trainer", "resilienzprinzipien", "glück im arbeitsleben",
    "vorurteile im arbeitsleben", "familie – beruf", "internationale fachkräfte",
    "berufseinstieg", "lebenslanges lernen", "weiterbildung", "schutz- und sicherheitskraft",
    "sport und öffentliche", "publishing-strategien", "facility management",
    "destinationen", "web3 startup", "immigrant entrepreneurship", "inclusive entrepreneurship",
    "startup fundraising", "entrepreneurship through acquisition", "investmentstrategien",
    "startup ecosystems", "from startup to unicorn", "startup players handbook",
    "exploring entrepreneurship", "building trust in startup", "asset sales", "sales on the go",
    "familienunternehmer-code", "onlinekurses", "industrieller medizin", "pflege",
    "dilemma überlastung", "arbeitsrecht flexibel nutzen", "technische mechanik",
    "ertragsteuern", "besteuerung der unternehmen", "zoll und umsatzsteuer",
    "praxislehrbuch steuerrecht", "steuern und strategie", "buchhaltung klipp",
    "doppelten buchhaltung", "bilanzierung", "bankwirtschaft", "kreditaufnahme",
    "nachhaltige finanzen", "finanzielle bildung", "gesellschaftsrecht", "arbeitsrecht",
    "salesforce", "grapevine", "romanian indigenous",
    "tourismus", "zukunft verantwortungsvoll gestalten", "politische bildung",
    "bildungskonzepte", "zukunft der medien", "bauen – pflegen", "automobile der zukunft",
    "markenmanagement", "verhaltensorientiertes innovationsmanagement", "hybrides innovationsmanagement",
    "trendbasiertes innovationsmanagement", "guerilla innovationsmanagement",
]


def _sha256(fp: str) -> str:
    h = hashlib.sha256()
    with open(fp, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def _inspect_book(file_path: str) -> tuple[str, str, str]:
    """Returns `(full_title, edition_hint, intro_sample)` for an EPUB or PDF file."""
    ext = os.path.splitext(file_path)[1].lower()
    title = ""
    intro_parts: list[str] = []

    if ext == ".epub":
        try:
            with zipfile.ZipFile(file_path, "r") as zf:
                names = zf.namelist()
                nlow = {n.lower(): n for n in names}
                opf = ""
                ck = "META-INF/container.xml" if "META-INF/container.xml" in names else nlow.get("meta-inf/container.xml", "")
                if ck:
                    for rf in ET.fromstring(zf.read(ck)).iter():
                        if rf.tag.endswith("rootfile") and rf.attrib.get("full-path"):
                            opf = rf.attrib["full-path"]
                            break
                ordered: list[str] = []
                if opf and opf in names:
                    import posixpath
                    opf_dir = posixpath.dirname(opf)
                    opf_root = ET.fromstring(zf.read(opf))
                    manifest = {}
                    for el in opf_root.iter():
                        tl = el.tag.split("}")[-1].lower()
                        if tl == "title" and not title and (el.text or "").strip():
                            title = html.unescape(el.text.strip())
                        elif el.tag.endswith("item"):
                            iid = el.attrib.get("id", "")
                            href = el.attrib.get("href", "").split("#")[0]
                            mtype = el.attrib.get("media-type", "").lower()
                            if iid and href and ("html" in mtype or href.lower().endswith((".xhtml", ".html", ".htm"))):
                                manifest[iid] = posixpath.normpath(posixpath.join(opf_dir, href)) if opf_dir else href
                        elif el.tag.endswith("itemref"):
                            cand = manifest.get(el.attrib.get("idref", ""))
                            if cand and cand in names:
                                ordered.append(cand)
                if not ordered:
                    ordered = sorted(n for n in names if n.lower().endswith((".xhtml", ".html", ".htm")))[:4]
                for cp in ordered[:4]:
                    raw = zf.read(cp).decode("utf-8", errors="ignore")
                    txt = re.sub(r"<[^>]+>", " ", raw)
                    txt = re.sub(r"\s+", " ", txt).strip()
                    if txt:
                        intro_parts.append(txt[:1500])
        except Exception:
            pass
    elif ext == ".pdf":
        try:
            import pymupdf
            bn = os.path.splitext(os.path.basename(file_path))[0]
            fn_hint = bn.replace("_", " ").replace("-", " ").strip()
            is_coded = bool(
                re.match(
                    r"^(?:97[89][-_\s]|s\d{5}|S\d{6,}|ssrn[-_]|1-s2\.0-|cesifo|admsci|gnag|f\d{8,}|1155\d+|3843\d+|1257a|\d{4}-\d{3}|KD\d+|ULMNUF|KM-Essentials|Das-Kuratierte)",
                    bn,
                    re.I,
                )
            ) or len(re.findall(r"[A-Za-zÄÖÜäöüß]", bn)) < 5

            with pymupdf.open(file_path) as doc:
                meta_t = html.unescape((doc.metadata or {}).get("title") or "").strip()
                if (
                    meta_t
                    and not re.match(
                        r"^(?:microsoft word|untitled|document|[\d_\-\.]+$|KD\d+\s+Erster\s+Test|CESifo Working Paper|"
                        r"Datenschutz und Datensicherheit|LobJMat.*)",
                        meta_t,
                        re.I,
                    )
                    and not re.search(r"\.(book|indd|docx?|pdf|fm)$", meta_t, re.I)
                    and len(re.findall(r"[A-Za-zÄÖÜäöüß]", meta_t)) >= 4
                ):
                    title = meta_t

                for pi in range(min(4, len(doc))):
                    t = doc[pi].get_text() or ""
                    if t.strip():
                        intro_parts.append(re.sub(r"\s+", " ", t).strip()[:1500])

                full_sample_low = " ".join(intro_parts).lower()
                rel_parts = os.path.relpath(file_path, LIB_DIR).replace("\\", "/").split("/")
                already_organized = len(rel_parts) > 1 and rel_parts[0] in CATEGORY_DIRS
                if len(doc) <= 2 and "bereitgestellt von:" in full_sample_low and "urheberrecht" in full_sample_low:
                    title = fn_hint if fn_hint.lower().startswith("coveronly") else f"CoverOnly {fn_hint}"
                elif not title:
                    noisy_fn = any(w in fn_hint.lower() for w in ("basics", "e-book", "rechnung", "cover")) or re.match(r"^(?=.*\d)[0-9a-zA-Z]{10,}_", bn)
                    if (already_organized and not is_coded) or (not is_coded and not noisy_fn and len(fn_hint) >= 12):
                        toc0 = doc.get_toc() or []
                        first_toc = html.unescape((toc0[0][1] or "").strip()) if toc0 and toc0[0][0] == 1 else ""
                        if not already_organized and first_toc and first_toc.replace("-", " ").lower().startswith(fn_hint.lower()) and len(first_toc) > len(fn_hint) + 5:
                            title = first_toc
                        else:
                            title = fn_hint

                toc = doc.get_toc() or []
                is_monograph_toc = any(
                    re.match(r"^(vorwort|geleitwort|acknowledgements|inhaltsverzeichnis|inhaltsübersicht|table of contents|preface|part\s+[ivx]+|\d+\s)", html.unescape((t[1] or "").strip()), re.I)
                    for t in toc[:8]
                )

                # For journal articles / non-monograph PDFs, prefer substantive L1 TOC article title
                if not title and intro_parts and toc and not is_monograph_toc:
                    skip_toc = re.compile(
                        r"^(cover|title page|half[- ]?title|copyright|vorwort|geleitwort|acknowledgements|"
                        r"danksagung|acronyms|inhaltsverzeichnis|inhaltsübersicht|table of contents|"
                        r"warum dieses buch|einleitung|introduction|haftungsausschluss|abstract|zusammenfassung|"
                        r"conclusions?|references|welcome|active content list|preface|urheberrecht|autoranschrift|tabellenverzeichnis|"
                        r"abbildungsverzeichnis|abkürzungsverzeichnis|literatur(?:verzeichnis)?|sachwortverzeichnis|"
                        r"stichwortverzeichnis|anhang|index|part\s+[ivx]+|\d+[\.\s])",
                        re.I,
                    )
                    for lvl, toc_t, *_ in toc:
                        cand_t = html.unescape((toc_t or "").strip().lstrip("\ufeff"))
                        if lvl == 1 and len(cand_t) >= 8 and not skip_toc.match(cand_t):
                            title = cand_t
                            break

                # For monographs or TOC-less papers (Springer/Vieweg/SSRN/CESifo/IJBEX), scan p0..p3 for real title page
                if not title and intro_parts:
                    skip_line = re.compile(
                        r"^(?:[\d\W]+$|123$|copyright|©|http://|https://|doi:|issn|isbn|electronic copy|"
                        r"int\.\s*j\.|published by|distributed under|publisher|working papers|imprint:|"
                        r"hmd\b|hauptbeitr|rezension|nachruf|editorial|schwerpunkt|einwurf|lnbip|lecture notes|"
                        r"bestmasters|series editors|bibliothek der|die reihe |mit „bestmasters|reih|herausgegeben von|"
                        r"die schriftenreihe|das recht der|springer|vieweg|lobachevskii|gabler\b|sozialwissenschaft|"
                        r"mit einem geleitwort|russian text|"
                        r"digitale schriftenreihe|version\s+\d|original version|this version|"
                        r"schriftenreihe|erscheinungsort|haftungsausschluss|inhaltsverzeichnis|\d{4}$|\d+\.\s*auf)",
                        re.I,
                    )
                    common_titles = r"\b(sap|abap|itil|ai|audit|cobit|cloud|management|blockchain|organizational|grundkurs|innovative|überlegene|daten|marketing|javaserver|bankbetriebslehre|generating|architekturreview|robotic|process|automation|executable|scripts|programmierung|big|data|industry|rise|transformationsmodell|erfolgsstrategien|systementwicklung)\b"
                    best_title = ""
                    # Articles/short papers start on page 0; monographs often have cover (p0) and interior title page (p3/p2)
                    page_order = [0, 1, 2] if len(doc) <= 45 else [3, 2, 0, 1]
                    for pi in page_order:
                        if pi >= len(doc):
                            continue
                        page_txt = doc[pi].get_text() or ""
                        page_low = page_txt.lower()
                        if any(blurb in page_low for blurb in ("deutsche nationalbibliothek", "die reihe ", "bibliographische daten", "der dritten sektors", "schriftenreihe präsentiert", "bestmasters“ zeichnet", "mit einem geleitwort von univ", "danksagung", "problemstellungen von unternehmen")):
                            continue
                        raw_lines = [ln.strip() for ln in page_txt.splitlines() if 3 <= len(ln.strip()) <= 90]
                        kept = [
                            ln for ln in raw_lines
                            if not skip_line.match(ln)
                            and "http" not in ln.lower()
                            and "isbn" not in ln.lower()
                            and not ln[0].islower()
                        ]
                        if not kept:
                            continue
                        while (
                            len(kept) >= 2
                            and not re.match(r"^(the|a|an|die|der|das|ein|eine|on|in|for|über)\b", kept[0], re.I)
                            and (
                                "|" in kept[0]
                                or "hrsg" in kept[0].lower()
                                or "·" in kept[0]
                                or (len(kept[0].split()) <= 3 and not re.search(common_titles, kept[0], re.I))
                            )
                        ):
                            kept = kept[1:]
                        title_lines = []
                        for ln in kept[:5]:
                            if re.search(r"[@*]|\b(phd|abstract|april|january|auflage|auﬂage)\b", ln, re.I) or "universi" in ln.lower() or ln.lower().startswith("mit einem geleitwort"):
                                break
                            if re.match(r"^[A-ZÄÖÜ][a-zäöüß\-]+(?:\s+[A-ZÄÖÜ][a-zäöüß\-]+){1,2}(?:\s*\*)?$", ln) and not re.search(common_titles, ln, re.I):
                                if title_lines:
                                    break
                                continue
                            if title_lines and title_lines[-1].endswith("-"):
                                title_lines[-1] = title_lines[-1][:-1] + ln
                            else:
                                title_lines.append(ln)
                        cand = " ".join(title_lines).strip()
                        if len(cand) >= 6:
                            best_title = re.sub(r"^\d+\s+(?=[A-ZÄÖÜ])", "", cand)
                            # Strip trailing lowercase wrap fragment if PDF stopped mid-prose
                            if not re.search(r"[,;:\.]\s*$", best_title) and len(best_title.split()) >= 14:
                                best_title = " ".join(best_title.split()[:10])
                            break
                    if best_title:
                        title = best_title
        except Exception:
            pass

    if not title:
        title = os.path.splitext(os.path.basename(file_path))[0].replace("_", " ").replace("-", " ")

    # Special fix: PDF metadata occasionally holds subtitle only ("Overcoming ...") when filename holds main title
    if "human_element" in os.path.basename(file_path).lower() and title.lower().startswith("overcoming "):
        title = f"The Human Element: {title}"

    intro_text = " ".join(intro_parts)[:4000]
    edition_hint = ""
    vol_m = re.search(r"\b(?:Volume|Vol\.?|Teil)\s*(\d+|[IVX]+)\b", title, re.IGNORECASE)
    if vol_m:
        edition_hint = f"Vol{vol_m.group(1)}"
    else:
        ed_m = re.search(r"\b(\d{1,2})\.\s*(?:Aufl(?:\.|age)?|Ed(?:ition)?)\b|\b(202[0-9])\b", intro_text[:1200], re.IGNORECASE)
        if ed_m:
            if ed_m.group(1):
                edition_hint = f"{ed_m.group(1)}Aufl"
            elif ed_m.group(2):
                edition_hint = ed_m.group(2)

    return title, edition_hint, intro_text


def shorten_title_slug(title: str, max_len: int = 52) -> str:
    """Shortens a book title cleanly without cutting mid-word or leaving dangling articles."""
    import unicodedata
    clean = unicodedata.normalize("NFC", title).replace("®", "").replace("™", "").replace("\u202f", " ").replace("\xa0", " ").replace("\u2009", " ").strip()
    clean = re.sub(r"^(?:[\s\-–—]+|[\d]+\s*[\-–—\.]\s*)+(?=[A-Za-zÄÖÜäöüß])", "", clean)
    clean = re.sub(r"\s*\((?:German Edition|B[0-9A-Z]{8,}|z-lib\.org)\)\s*$", "", clean, flags=re.I)
    clean = re.sub(r"\bS\s*/\s*4\s*HANA\b", "S4HANA", clean, flags=re.I)
    if ":" in clean:
        head, tail = [s.strip() for s in clean.split(":", 1)]
        # Handle "Lastname, Firstname: Book Title"
        if "," in head and len(head.split()) <= 3 and len(tail) >= 10:
            clean = tail
        elif len(head) >= 12 and len(head.split()) >= 2:
            clean = head
    clean = re.sub(r"^(A Practical Guide to|Practical Guide to|Handbook for|Design and Evaluation of an|Building an)\s+", "", clean, flags=re.I)
    clean = re.sub(r"\s+[-–—]\s+(Ein|Eine|A|An|The|Praxishandbuch|Concepts|Konzepte)\b.*$", "", clean, flags=re.I)
    clean = re.sub(r"\bfor the Implementation of\b", "for", clean, flags=re.I)
    clean = re.sub(r"\bIntegration von\b", "Integration", clean, flags=re.I)
    clean = re.sub(r"\bin der betrieblichen\b", "in der", clean, flags=re.I)

    clean = clean.translate(UMLAUT_TRANS)
    clean = re.sub(r"[^A-Za-z0-9]+", "_", clean).strip("_")
    dangling = {"in", "of", "the", "a", "an", "for", "and", "und", "der", "die", "das", "mit", "zu", "with", "into", "von"}

    def _trim_tail(toks: list[str]) -> list[str]:
        while len(toks) > 2 and toks[-1].lower() in dangling:
            toks.pop()
        return toks

    if len(clean) <= max_len:
        return "_".join(_trim_tail(clean.split("_"))) or "Fachbuch"

    words = clean.split("_")
    out: list[str] = []
    cur = 0
    for w in words:
        add_len = len(w) + (1 if out else 0)
        if cur + add_len > max_len:
            break
        out.append(w)
        cur += add_len
    out = _trim_tail(out)
    return "_".join(out) if out else clean[:max_len]


def _kw_in_text(kw: str, text_low: str) -> bool:
    """Boundary-aware keyword matcher so short stems (e.g. 'rag', 'sap', 'agil') do not match inside unrelated words."""
    k = kw.strip().lower()
    if not k:
        return False
    esc = re.escape(k)
    if " " not in k and len(k) <= 6:
        return bool(re.search(rf"(?<![a-zäöüß0-9]){esc}(?![a-zäöüß0-9])", text_low))
    return bool(re.search(rf"(?<![a-zäöüß0-9]){esc}", text_low))


def _classify_offtopic_subdir(title: str, intro: str, fname: str) -> str:
    """Assigns clean thematic subfolder inside 99_Off_Topic_Nicht_Fuer_RAG."""
    # Match primarily against title + filename first to avoid blurb keywords misrouting finance/policy books into SelfHelp
    title_fn = f" {title.lower()} {fname.lower()} "
    txt = f"{title_fn} {intro[:400].lower()} "
    if any(k in txt for k in ("coveronly", "pro forma", "proforma", "rechnungs", "bestellungsdokument")):
        return "07_Privatdokumente_Unvollstaendige_Downloads"
    if any(k in title_fn for k in ("alchimist", "alchemist", "der prozess", "der spieler", "dickens", "zwei städten", "zwei staedten", "fabian", "misérables", "elenden", "momo und die", "papillon", "thirteen stories", "invisible man", "verbrechen und strafe")):
        return "01_Belletristik_Klassiker_Romane"
    if any(k in title_fn for k in ("aryan brotherhood", "che guevara", "rothschilds", "elon musk", "steve jobs", "tupac", "thugs heart", "thug's heart", "permanent record", "shore, stein", "shore stein")):
        return "02_Biografien_Musik_Zeitgeschichte"
    if any(k in title_fn for k in (
        "alles steckt in dir", "can't hurt me", "die kunst, einen", "die_kunst", "einsamkeit",
        "emotional kompetent", "online-coaching", "feel better fast", "härte", "haerte",
        "mike mentzer", "hooked", "persönlichkeitsentwicklung", "männlichkeit", "maennlichkeit",
        "make the right choice", "resilienzprinzipien", "resilienz-stärkende", "resilienz staerkende",
        "surrounded by idiots", "50th law", "art of seduction", "big five for life", "fasting",
        "daily laws", "diary of a ceo", "fastest way to success", "laws of human nature",
        "self-empowerment", "value of others", "superior man", "wisdom codes", "alkohol bis zucker",
        "why we sleep", "brain on porn", "karriere-helfer", "karriere helfer", "karriere‐websites",
        "karriere-websites", "selbstmanagement", "anti-stress-trainer", "glück im arbeitsleben",
        "vorurteile im arbeitsleben", "familie – beruf", "berufseinstieg", "freiberufler werden",
        "berufliche selbstständigkeit", "lebenslanges lernen", "weiterbildung", "didaktiken",
        "bildungskonzepte",
    )):
        return "03_Psychologie_Fitness_SelfHelp"
    if any(k in title_fn for k in (
        "bankbetriebslehre", "bankwirtschaft", "bitcoin-standard", "börse einen schritt",
        "finanz-tsunami", "human action", "canadian economy", "insurance & innovation",
        "kopfgeldjagd", "moroccan electronic payment", "wer regiert das geld", "wolff of wall street",
        "buchhaltung", "buchfuehrung", "buchführung", "bilanzierung", "ertragsteuern",
        "steuern und strategie", "kreditaufnahme", "nachhaltige finanzen", "finanzielle bildung",
        "fintech", "investmentstrategien", "startup fundraising", "asset sales",
        "physik und finanzen", "sport und öffentliche finanzen", "konzerncontrolling",
    )):
        return "05_Finanzen_Boerse_Krypto_VWL"
    if any(k in title_fn for k in (
        "imperium der milliardäre", "angekündigten krise", "deutschland schafft sich ab",
        "angst der eliten", "gesellschaft in der gesellschaft", "factfulness", "media control",
        "kosovo-krieg", "nie wieder krieg", "pandemie", "human rights", "new world order",
        "brics", "trumps zweite", "ukraine-krieg", "kalte krieg", "sicherheitspolitik",
        "geopolitik", "friedensordnungen", "staatsbildung", "georessourcen",
        "environment as a weapon", "brasilien-china", "china", "digital ethics lab",
        "arbeitsrecht", "gesellschaftsrecht", "zoll und umsatzsteuer", "umsatzsteuer",
        "juristische personen", "praxislehrbuch steuerrecht", "besteuerung der unternehmen",
        "internationale fachkräfte", "schutz- und sicherheitskraft",
        "politische bildung", "zukunft der medien",
    )):
        return "04_Politik_Gesellschaft_Medien_Recht"
    if any(k in txt for k in ("resilienz", "online-coaching", "persönlichkeitsentwicklung")):
        return "03_Psychologie_Fitness_SelfHelp"
    return "06_Branchen_Medizin_Biotech_Varia"


_CURATED_TITLE_FIXES = {
    "die_kunst.pdf": "Die Kunst, einen Scheiss drauf zu geben",
    "pro_forma_proforma_data_wystawienia.pdf": "Pro forma Rechnung Nr 684394",
    "miteinem_geleitwort_von_prof_dr_gerald_heidegger.pdf": "Berufliche Bildung und Persoenlichkeitsentwicklung",
    "das_kuratierte_dossier_bd_8_mai_2026_issn_2940_1372.pdf": "Knowledge and Co-Creation GfWM 2026",
    "diese_schriftenreihe_schafft_eine_plattform_um.pdf": "Nachhaltige Unternehmensfuehrung Ulm NUF",
    "dietmar_abts_wilhelm_muelder_grundkurs.pdf": "Grundkurs Wirtschaftsinformatik Abts Muelder",
    "unter_mitarbeit_von_alexander_malkis.pdf": "Logische und Methodische Grundlagen der Programm- und Systementwicklung",
    "3-540-27856-7.pdf": "Personalmanagement Holtbruegge 2Aufl",
    "978-3-322-82164-5.pdf": "Outsourcing von CRM Prozessen",
    "978-3-531-19434-9.pdf": "Renaissance der Geopolitik Deutsche Sicherheitspolitik",
    "978-3-642-14385-4.pdf": "Projektabwicklung in der Bauwirtschaft",
    "978-3-642-36637-6.pdf": "Kalkulation Preisbildung und Controlling in der Bauwirtschaft",
    "kalkulation_preisbildung_und_controlling.pdf": "Kalkulation Preisbildung Controlling Bauwirtschaft",
    "978-3-658-00923-6.pdf": "Wertschoepfungskompetenz und Unternehmertum in Regionen",
    "978-3-658-01463-6.pdf": "Exzellenz in der Unternehmensberatung 1Aufl",
    "978-3-658-05078-8.pdf": "Berufseinstieg fuer Wirtschaftswissenschaftler",
    "978-3-658-09414-0.pdf": "Der zweite Kalte Krieg Zur Geopolitik der USA",
    "978-3-658-16289-4.pdf": "Netzwerke beim Berufseinstieg",
    "978-3-658-18145-1.pdf": "Grundzuege der doppelten Buchhaltung 9Aufl",
    "978-3-658-20787-8.pdf": "Der Umgang mit Schatten IT in Unternehmen",
    "978-3-658-22718-0.pdf": "Uebungsbuch Buchfuehrung Bilanzierung und Umsatzsteuer",
    "978-3-658-23367-9.pdf": "Lebenslanges Lernen in der Mediengesellschaft",
    "978-3-658-23920-6.pdf": "Europaeische Friedensordnungen und Sicherheitsarchitekturen",
    "978-3-658-24347-0.pdf": "Strategische Neupositionierung von Unternehmungen",
    "978-3-658-24651-8.pdf": "Digitalen Wandel gestalten HFT Stuttgart",
    "978-3-658-29239-3.pdf": "Effiziente Zentralisierung in IT und Finanzen",
    "978-3-658-29738-1.pdf": "Rationales Entscheiden bei der Kreditaufnahme",
    "978-3-658-30463-8.pdf": "Selbststaendige Erwerbstaetigkeit in spaeteren Lebensphasen",
    "978-3-658-31310-4.pdf": "Projektmanagement im Einkauf 2Aufl",
    "978-3-658-34324-8.pdf": "KI im Dienstleistungsmanagement Band 1 Geschaeftsmodelle",
    "978-3-658-34326-2.pdf": "KI im Dienstleistungsmanagement Band 2 Einsatzfelder",
    "978-3-658-42144-1.pdf": "Fallstudien zum Arbeitsrecht 3Aufl",
    "978-3-658-42989-8.pdf": "Lernpraktiken in der Unternehmensberatung",
    "978-3-658-45487-6.pdf": "Bankwirtschaft und Controlling Teil 1",
    "978-3-658-45747-1.pdf": "Datenschutz und IT Sicherheit Industrie 4 0",
    "978-3-662-58528-3.epub": "Handbuch Industrie 4 0 Automatisierung Sensorik",
    "978-3-662-58530-6.epub": "Handbuch Industrie 4 0 Logistik KI",
    "978-3-662-58532-0.epub": "Handbuch Industrie 4 0 Cloud Digitale Transformation",
    "978-3-662-64116-3.pdf": "Automobile der Zukunft elektrisch digital autonom",
    "978-3-662-66295-3.pdf": "Management der Zukunft Zukunftsmanagement",
    "978-3-662-68871-7.pdf": "Anforderungsmanagement in sieben Tagen KI 2Aufl",
    "978-3-8349-4206-7.pdf": "Strategie Organisation Performance Innovationsmanagement",
    "978-3-8349-4472-6.pdf": "Innovationsmanagement Instrumente und Methoden",
    "s00058-023-3220-y.pdf": "Arbeitsrecht flexibel nutzen Dilemma Pflege",
}


def classify_book_category(title: str, intro: str, current_rel: str, recategorize_offtopic: bool = False) -> tuple[str, int]:
    """Classifies thematic category + relevance score (`0` means off-topic for Career OS RAG)."""
    parts = current_rel.replace("\\", "/").split("/")
    # Keep already-sorted files stable in their assigned folder unless recategorizing 99_Off_Topic
    if len(parts) > 1 and parts[0] in CATEGORY_DIRS:
        if parts[0] == "99_Off_Topic_Nicht_Fuer_RAG":
            if not recategorize_offtopic:
                return "99_Off_Topic_Nicht_Fuer_RAG", 0
        else:
            return parts[0], 10

    title_low = f" {title.lower()} "
    title_norm = title_low.replace("-", " ").replace("‐", " ").replace("–", " ")
    intro_low = f" {intro.lower()} "
    fn_low = f" {os.path.basename(current_rel).lower()} "

    scores: dict[str, int] = {}
    for cat, kws in DOMAIN_KEYWORDS.items():
        sc = 0
        for kw in kws:
            if _kw_in_text(kw, title_low) or _kw_in_text(kw, title_norm):
                sc += 4
            elif _kw_in_text(kw, intro_low):
                sc += 1
        scores[cat] = sc

    # Primary-topic tie-breakers for AI-in-ERP, IAM, EAM, Platforms, WI & VISMUV
    if any(k in title_norm for k in ("artificial intelligence", "künstliche intelligenz", "ki mit köpfchen", "business ai", "data science", "ai explained", "agentic ai", "generative ai", "big data", "transformers", "langchain", "llms", "robotic process automation", "intelligent technologies", "hybrid artificial intelligent", "managing human and artificial", "nutzenpotenziale von ki", "python for business", "business analytics")):
        if "cybersecurity" in title_norm or "audit" in title_norm or "governance" in title_norm or "jailbreaking" in title_norm:
            scores["02_IT_Audit_Governance_Compliance"] += 8
        elif "enterprise architecture" in title_norm or "site reliability engineering" in title_norm:
            scores["03_Enterprise_Architecture_Cloud"] += 8
        elif "business models" in title_norm or "transmission of ai" in title_norm or "arbeitswelt" in title_norm or "revolution der arbeitswelt" in title_norm or "dienstleistungsmanagement" in title_norm:
            scores["05_Consulting_BWL_VISMUV"] += 6
        elif "desktop publishing" not in title_norm:
            scores["04_AI_Engineering_Data_Automation"] += 8
    elif any(k in title_norm for k in ("enterprise architecture", "architekturreview", "microservices", "cloud computing", "cloud native", "cloud networking", "public cloud", "itil", "it service management", "site reliability engineering", "schatten it", "information systems outsourcing", "digitale plattformen", "digitalen plattformen", "digitaler plattformen", "cloud digitale transformation")):
        scores["03_Enterprise_Architecture_Cloud"] += 8
    elif re.search(r"\b(sap|s/4hana|s4hana|abap|btp|successfactors|bw/4hana)\b", title_norm) and "palm sap" not in title_norm:
        if "datenschutz" in title_norm or "security governance" in title_norm:
            scores["02_IT_Audit_Governance_Compliance"] += 7
        else:
            scores["01_SAP_S4HANA_BTP_CleanCore"] += 6
    elif re.search(r"\b(hacking|security|audit|compliance|identity|it governance|enterprise governance of information|softwarelizenzmanagement|datenschutz|it revision|it grc|cyberstrategien)\b", title_norm):
        scores["02_IT_Audit_Governance_Compliance"] += 6
    elif any(k in title_norm for k in ("wirtschaftsinformatik", "anforderungsmanagement", "requirements engineering", "prozessanalyse", "javafx", "javaserver faces", "creative dsls", "lagerverwaltung", "vba für office", "microsoft 365", "programm  und systementwicklung", "programm- und systementwicklung")):
        if "forschungsdesigns" in title_norm or "forschung" in title_norm or "klipp" in title_norm or "basiswissen" in title_norm:
            pass
        else:
            scores["07_Wirtschaftsinformatik_IT_Grundlagen"] += 8
    elif any(k in title_norm for k in ("gmbh gründung", "software startup gründen", "gründen mit erfolg", "business inkubation", "nachhaltig gründen", "nachhaltige unternehmensführung", "gemeinwohlorientierte unternehmensführung", "regenerative geschäftsmodelle", "datengetriebenes marketing", "kundenmanagement im vertrieb", "sales enablement", "sales management", "sales strategies", "ai startup", "handbuch entrepreneurship", "e commerce", "crm", "marktforschung", "zukunft verkauf")) or re.match(r"^\s*(marketing|entrepreneurship)\b", title_norm):
        scores["08_Unternehmertum_Marketing_VISMUV"] += 8
    elif any(k in title_norm for k in ("project management", "projektmanagement", "unternehmensberatung", "business consulting", "human element", "leadership", "schnelles denken", "wissensmanagement", "knowledge management", "management reporting", "geschäftsmodelle", "geschäftsmodell", "dienstleistungsmanagement", "agilität in teams", "people management", "beyond automation", "arbeit 4", "innovation gap", "innovationsmanagement", "ambidextres", "knowledge is power", "knowledge and co creation", "human capital supply chain", "digitaler humanismus", "effiziente zentralisierung in it", "chefsache finanzen in einkauf", "logistik ki", "chefsache zukunft", "organisationstheorie", "irrtümer über kennzahlen", "personalmanagement holtbruegge")):
        scores["05_Consulting_BWL_VISMUV"] += 6

    best_cat, best_score = max(scores.items(), key=lambda x: x[1])

    for bad in OFF_TOPIC_DAMPENERS:
        if bad in title_low or bad in title_norm or bad in fn_low:
            best_score = max(0, best_score - 15)

    if best_score < 2:
        return "99_Off_Topic_Nicht_Fuer_RAG", best_score

    return best_cat, best_score


def organize_library(apply: bool = False, recategorize_offtopic: bool = False) -> dict:
    for d in CATEGORY_DIRS:
        if apply:
            os.makedirs(os.path.join(LIB_DIR, d), exist_ok=True)
    if apply:
        for sd in OFF_TOPIC_SUBDIRS:
            os.makedirs(os.path.join(LIB_DIR, "99_Off_Topic_Nicht_Fuer_RAG", sd), exist_ok=True)

    candidates: list[str] = []
    for root, dirs, files in os.walk(LIB_DIR):
        dirs[:] = sorted(d for d in dirs if not d.startswith("."))
        for fn in sorted(files):
            if fn in SKIP_TRACKER_FILES or fn.startswith(("~$", "._")):
                continue
            ext = os.path.splitext(fn)[1].lower()
            if ext in (".epub", ".pdf", ".docx", ".txt", ".md"):
                candidates.append(os.path.join(root, fn))

    entries = []
    for abs_p in candidates:
        rel_p = os.path.relpath(abs_p, LIB_DIR)
        ext = os.path.splitext(abs_p)[1].lower()
        sha = _sha256(abs_p)
        title, edition, intro = _inspect_book(abs_p)
        fn_low = os.path.basename(abs_p).lower()
        if fn_low in _CURATED_TITLE_FIXES:
            title = _CURATED_TITLE_FIXES[fn_low]
        target_cat, score = classify_book_category(title, intro, rel_p, recategorize_offtopic=recategorize_offtopic)
        offtopic_sub = _classify_offtopic_subdir(title, intro, os.path.basename(abs_p)) if target_cat == "99_Off_Topic_Nicht_Fuer_RAG" else ""
        short_base = shorten_title_slug(title, max_len=52)
        entries.append({
            "src_abs": abs_p,
            "src_rel": rel_p,
            "ext": ext,
            "sha256": sha,
            "title": title,
            "edition": edition,
            "target_cat": target_cat,
            "offtopic_sub": offtopic_sub,
            "score": score,
            "short_base": short_base,
        })

    # Prioritize already-organized canonical files and non-"(1)" downloads for deterministic SHA-256 dedup
    entries.sort(
        key=lambda e: (
            0 if os.sep in e["src_rel"] or "/" in e["src_rel"] else 1,
            1 if re.search(r"\(\d+\)", e["src_rel"]) else 0,
            e["src_rel"].lower(),
        )
    )

    seen_sha: dict[str, dict] = {}
    unique_entries = []
    dedup_entries = []
    for e in entries:
        if e["sha256"] in seen_sha:
            dedup_entries.append((e, seen_sha[e["sha256"]]))
        else:
            seen_sha[e["sha256"]] = e
            unique_entries.append(e)

    # Detect colliding short names with different SHAs -> append edition tag if distinct
    base_ext_groups: dict[tuple[str, str, str], set[str]] = {}
    for e in unique_entries:
        k = (e["target_cat"], e["short_base"].lower(), e["ext"])
        base_ext_groups.setdefault(k, set()).add(e["sha256"])

    used_targets: dict[str, str] = {}
    actions = []
    for e in unique_entries:
        rel_parts = e["src_rel"].replace("\\", "/").split("/")
        # Preserve already-organized RAG files identically (01_..08_); also preserve nested 99_ files unless recategorize_offtopic
        if len(rel_parts) > 1 and rel_parts[0] in CATEGORY_DIRS:
            in_rag = rel_parts[0] != "99_Off_Topic_Nicht_Fuer_RAG"
            already_sub_offtopic = rel_parts[0] == "99_Off_Topic_Nicht_Fuer_RAG" and len(rel_parts) >= 3
            if in_rag or (already_sub_offtopic and not recategorize_offtopic):
                dest_rel = e["src_rel"]
                dest_abs = e["src_abs"]
                used_targets[dest_abs.lower()] = e["sha256"]
                actions.append({**e, "dest_rel": dest_rel, "dest_abs": dest_abs, "changed": False})
                continue

        base = e["short_base"]
        target_parent = (
            os.path.join("99_Off_Topic_Nicht_Fuer_RAG", e["offtopic_sub"])
            if e["target_cat"] == "99_Off_Topic_Nicht_Fuer_RAG" and e["offtopic_sub"]
            else e["target_cat"]
        )
        # Preserve explicit manual filename if already cleanly named in 99_Off_Topic unless in _CURATED_TITLE_FIXES
        if len(rel_parts) > 1 and rel_parts[0] == "99_Off_Topic_Nicht_Fuer_RAG" and os.path.basename(e["src_rel"]).lower() not in _CURATED_TITLE_FIXES:
            existing_stem = os.path.splitext(os.path.basename(e["src_rel"]))[0]
            fname = f"{existing_stem}{e['ext']}"
            base = existing_stem
        else:
            k = (target_parent, base.lower(), e["ext"])
            if len(base_ext_groups.get((e["target_cat"], e["short_base"].lower(), e["ext"]), set())) > 1 and e["edition"]:
                base = f"{base[:43]}_{e['edition']}"
            fname = f"{base}{e['ext']}"

        dest_rel = os.path.join(target_parent, fname)
        dest_abs = os.path.join(LIB_DIR, dest_rel)

        # Ensure unique filename if collision still exists among distinct files
        idx = 2
        while (dest_abs.lower() in used_targets and used_targets[dest_abs.lower()] != e["sha256"]) or (
            os.path.exists(dest_abs) and os.path.normpath(dest_abs) != os.path.normpath(e["src_abs"]) and _sha256(dest_abs) != e["sha256"]
        ):
            fname = f"{base[:46]}_{idx}{e['ext']}"
            dest_rel = os.path.join(target_parent, fname)
            dest_abs = os.path.join(LIB_DIR, dest_rel)
            idx += 1

        used_targets[dest_abs.lower()] = e["sha256"]
        changed = os.path.normpath(e["src_abs"]) != os.path.normpath(dest_abs)
        actions.append({**e, "dest_rel": dest_rel, "dest_abs": dest_abs, "changed": changed})

    moved = 0
    dedup_removed = 0
    off_topic = 0
    for a in actions:
        if a["target_cat"] == "99_Off_Topic_Nicht_Fuer_RAG":
            off_topic += 1
        tag = "MOVE" if a["changed"] else "KEEP"
        print(f"[{tag}] {a['src_rel']} -> {a['dest_rel']}  | score={a['score']} | title='{a['title']}'")
        if apply and a["changed"]:
            os.makedirs(os.path.dirname(a["dest_abs"]), exist_ok=True)
            shutil.move(a["src_abs"], a["dest_abs"])
            moved += 1

    for dup_e, canon_e in dedup_entries:
        print(f"[DEDUP-RM] {dup_e['src_rel']} == {canon_e['src_rel']} (sha256={dup_e['sha256'][:12]})")
        if apply and os.path.exists(dup_e["src_abs"]):
            os.remove(dup_e["src_abs"])
            dedup_removed += 1

    print(
        f"\n[SUMMARY] Total scanned: {len(entries)} | Canonical kept: {len(actions)} | "
        f"Moved/Renamed: {moved} | SHA-Dup removed: {dedup_removed} | Off-Topic excluded: {off_topic} | Apply={apply}"
    )
    return {"total": len(entries), "moved": moved, "dedup_removed": dedup_removed, "off_topic": off_topic, "apply": apply}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auto-sort and shorten-rename library books by title & thematic relevance.")
    parser.add_argument("--apply", action="store_true", help="Execute file moves & renames (default is dry-run)")
    parser.add_argument("--recategorize-offtopic", action="store_true", help="Re-evaluate files in 99_Off_Topic and sort remaining off-topic files into subfolders")
    args = parser.parse_args()
    organize_library(apply=args.apply, recategorize_offtopic=args.recategorize_offtopic)
