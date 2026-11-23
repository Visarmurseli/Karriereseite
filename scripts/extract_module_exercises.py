import os
import sys
import re
import glob
import hashlib
import zipfile
import xml.etree.ElementTree as ET
import time
import docx
import pypdf

ROOT_DIR = r"c:\Users\SHQIPTAR634\Desktop\SSB Dateien"
VAULT_DIR = r"C:\Users\SHQIPTAR634\Documents\Obsidian Vault\02_Wirtschaftsinformatik_300ECTS"

def get_file_md5(filepath):
    h = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(16384):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None

def extract_pdf_exercise(pdf_path, max_pages=80):
    pages_text = []
    try:
        reader = pypdf.PdfReader(pdf_path)
        total_p = len(reader.pages)
        limit = min(total_p, max_pages)
        for i in range(limit):
            try:
                page = reader.pages[i]
                text = page.extract_text() or ""
                clean = re.sub(r"[ \t]+", " ", text).strip()
                clean = re.sub(r"(\r?\n\s*){2,}", "\n", clean)
                if len(clean) > 15:
                    pages_text.append(f"##### Seite {i+1}\n{clean}\n")
            except Exception:
                continue
    except Exception as e:
        print(f"    [WARN] PDF Error {os.path.basename(pdf_path)}: {e}")
    return pages_text

def extract_docx_exercise(docx_path):
    sections = []
    try:
        doc = docx.Document(docx_path)
        paras = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        if paras:
            sections.append("\n".join(paras))
        for t_idx, table in enumerate(doc.tables):
            table_lines = []
            for r_idx, row in enumerate(table.rows):
                row_vals = [re.sub(r"\s+", " ", cell.text.strip()) for cell in row.cells]
                # Deduplicate identical adjacent cells from merged horizontal cells
                dedup = []
                for v in row_vals:
                    if not dedup or v != dedup[-1]:
                        dedup.append(v)
                table_lines.append("| " + " | ".join(dedup) + " |")
                if r_idx == 0:
                    table_lines.append("| " + " | ".join([":---"] * len(dedup)) + " |")
            if table_lines:
                sections.append(f"##### Tabelle {t_idx+1}\n" + "\n".join(table_lines))
    except Exception as e:
        print(f"    [WARN] DOCX Error {os.path.basename(docx_path)}: {e}")
    return ["\n\n".join(sections)] if sections else []

def extract_pptx_exercise(pptx_path):
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
                    slides.append(f"##### Folie {i+1}\n{clean}\n")
    except Exception as e:
        print(f"    [WARN] PPTX Error {os.path.basename(pptx_path)}: {e}")
    return slides

def extract_file_content(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".pdf":
        return extract_pdf_exercise(filepath), "PDF"
    elif ext == ".docx":
        return extract_docx_exercise(filepath), "DOCX"
    elif ext == ".pptx":
        return extract_pptx_exercise(filepath), "PPTX"
    return [], "UNKNOWN"

# Mapping table
EXERCISE_REGISTRY = [
    # --- MASTER MODULES ---
    {
        "file": "Modul_AI4IoT.md",
        "title": "AI4IoT – Artificial Intelligence for the Internet of Things",
        "dirs": [
            r"02_Master\AI4IoT – Artificial Intelligence for the Internet of Things\02_Fallstudie_Bademeister",
            r"02_Master\AI4IoT – Artificial Intelligence for the Internet of Things\03_Projektleistung_Poster_und_Shortpaper",
        ],
        "skip": ["~$"]
    },
    {
        "file": "Modul_Advanced_Software_Engineering.md",
        "title": "Advanced Software Engineering (ASE)",
        "dirs": [
            r"02_Master\Advanced Software Engineering\02_Aufgabenblaetter_und_Uebungen",
        ],
        "skip": ["~$"]
    },
    {
        "file": "Modul_Applied_AI.md",
        "title": "Applied AI and Upcoming Technologies in Industries",
        "dirs": [
            r"02_Master\Applied AI and Upcoming Technologies in Industries\02_Uebungen",
            r"02_Master\Applied AI and Upcoming Technologies in Industries\03_Projektarbeit_Yarro_Abgabe",
        ],
        "skip": ["~$"]
    },
    {
        "file": "Modul_Datenbanken.md",
        "title": "Datenbanken und Informationssysteme (DBIS)",
        "dirs": [
            r"02_Master\Datenbanken und Informationssysteme\02_Uebungsunterlagen",
        ],
        "skip": ["~$"]
    },
    {
        "file": "Modul_Digitale_Nachhaltigkeit.md",
        "title": "Digitale Nachhaltigkeit",
        "dirs": [
            r"02_Master\Digitale Nachhaltigkeit\01_Vorlesung_und_Uebungen",
            r"02_Master\Digitale Nachhaltigkeit\02_Schmalz_Praxisprojekt",
        ],
        "skip": ["~$"]
    },
    {
        "file": "Modul_Forschungsmethoden.md",
        "title": "Forschungsmethoden in der Wirtschaftsinformatik",
        "dirs": [
            r"02_Master\Forschungsmethoden in der Wirtschaftsinformatik\02_Methoden_und_Uebungsworkshops",
            r"02_Master\Forschungsmethoden in der Wirtschaftsinformatik\03_Schriftliche_Ausarbeitung_Algorithm_Aversion",
        ],
        "skip": ["~$"]
    },
    {
        "file": "Modul_Innovationsmanagement.md",
        "title": "Innovationsmanagement",
        "dirs": [
            r"02_Master\Innovationsmanagement\02_Uebungen_und_Zusatzmaterial",
        ],
        "skip": ["~$"]
    },
    {
        "file": "Modul_ISG.md",
        "title": "Innovationsmethoden für software- und datenintensive Geschäftsmodelle",
        "dirs": [
            r"02_Master\Innovationsmethoden für software- und datenintensive Geschäftsmodelle\02_Protokollleistungen",
            r"02_Master\Innovationsmethoden für software- und datenintensive Geschäftsmodelle\03_PatentRadar_Pitch_und_Business_Case",
        ],
        "skip": ["~$"]
    },
    {
        "file": "Modul_Management_IT_Unternehmen.md",
        "title": "Management von IT-Unternehmen",
        "dirs": [
            r"02_Master\Management von IT-Unternehmen\02_Uebungen_und_Fallstudien",
        ],
        "skip": ["~$"]
    },
    {
        "file": "Modul_Cloud_Computing.md",
        "title": "Service Management and Cloud Computing, and Evaluation",
        "dirs": [
            r"02_Master\Service Management and Cloud Computing, and Evaluation\02_Exercises_und_Workshops",
            r"02_Master\Service Management and Cloud Computing, and Evaluation\03_Exam_Paper_Hausarbeit",
        ],
        "skip": ["~$"]
    },
    {
        "file": "Modul_SOM.md",
        "title": "Service Operations Management (SOM)",
        "dirs": [
            r"02_Master\Service Operations Management\02_Uebungsunterlagen",
        ],
        "skip": ["~$"]
    },
    {
        "file": "Modul_Software_Architektur.md",
        "title": "Software-Architektur (QASD)",
        "dirs": [
            r"02_Master\Software-Architektur\02_Uebungsblaetter_und_Loesungen",
        ],
        "skip": ["~$"]
    },
    {
        "file": "Modul_TEUI.md",
        "title": "Theorie und Empirie internationaler Unternehmenstätigkeit",
        "dirs": [
            r"02_Master\Theorie und Empirie internationaler Unternehmenstätigkeit\02_Uebungen_mit_Loesungen",
        ],
        "skip": ["~$"]
    },
    {
        "file": "Modul_AIM.md",
        "title": "Advanced Information Management (AIM)",
        "dirs": [
            r"02_Master\xZusatz_Advanced Information Management (AIM)\02_Exercises_and_Sample_Exam",
            r"02_Master\xZusatz_Advanced Information Management (AIM)\03_Assignments",
        ],
        "skip": ["~$"]
    },
    {
        "file": "Modul_SmartCities.md",
        "title": "Smart Cities and Internet of Things",
        "dirs": [
            r"02_Master\xZusatz_nice2have-Smart Cities and Internet of Things\02_Practicals_Slides",
            r"02_Master\xZusatz_nice2have-Smart Cities and Internet of Things\03_Tutorials",
        ],
        "skip": ["~$"]
    },

    # --- BACHELOR MODULES ---
    {
        "file": "Modul_AFS.md",
        "title": "Automaten und Formale Sprachen (AFS)",
        "dirs": [
            r"03_Bachelor\Automaten und Formale Sprachen\01_Theoretische_Informatik_WS20\TI1 Übungsblätter",
            r"03_Bachelor\Automaten und Formale Sprachen\01_Theoretische_Informatik_WS20\Ergänzung-18",
            r"03_Bachelor\Automaten und Formale Sprachen\02_Theoretische_Informatik_WS18\Übungsblätter",
        ],
        "skip": ["~$"]
    },
    {
        "file": "Modul_BWL1.md",
        "title": "BWL 1: Organisation, Personalführung & Strategisches Management",
        "dirs": [
            r"03_Bachelor\BWL 1 - Organisation, Personalführung, Strategisches Management",
        ],
        "skip": ["~$", "vorlesung"]
    },
    {
        "file": "Modul_EBusiness.md",
        "title": "Informationssysteme im E-Business",
        "dirs": [
            r"03_Bachelor\Betriebliche Informationssysteme (WI 1)\01_Informationssysteme_im_E-Business_WS19",
        ],
        "skip": ["~$"]
    },
    {
        "file": "Modul_MBIS.md",
        "title": "Management betrieblicher Informationssysteme (MBIS)",
        "dirs": [
            r"03_Bachelor\Betriebliche Informationssysteme (WI 1)\02_Management_betrieblicher_Informationssysteme_SS20",
        ],
        "skip": ["~$"]
    },
    {
        "file": "Modul_DSA.md",
        "title": "Datenstrukturen und Algorithmen (DSA)",
        "dirs": [
            r"03_Bachelor\Datenstrukturen und Algorithmen\02_Uebungen_und_Tutorien",
        ],
        "skip": ["~$"]
    },
    {
        "file": "Modul_EST.md",
        "title": "Einführung in die Softwaretechnik (EST)",
        "dirs": [
            r"03_Bachelor\Einführung in die Softwaretechnik\02_Softwaretechnik_EST_SS18\Uebungsblaetter",
            r"03_Bachelor\Einführung in die Softwaretechnik\02_Softwaretechnik_EST_SS18\Folien der Uebung",
        ],
        "skip": ["~$"]
    },
    {
        "file": "Modul_EWI.md",
        "title": "Einführung in die Wirtschaftsinformatik (EWI)",
        "dirs": [
            r"03_Bachelor\Einführung in die Wirtschaftsinformatik\02_Uebungen",
        ],
        "skip": ["~$"]
    },
    {
        "file": "Modul_GBWL1.md",
        "title": "GBWL 1: Strukturen der Betriebswirtschaftslehre & Rechnungslegung",
        "dirs": [
            r"03_Bachelor\GBWL 1 - Strukturen der Betriebswirtschaftslehre",
        ],
        "skip": ["~$"]
    },
    {
        "file": "Modul_GBWL4.md",
        "title": "GBWL 4: Finanzprozess (Investition & Finanzierung)",
        "dirs": [
            r"03_Bachelor\GBWL 4 - Finanzprozess\01_Investition_und_Finanzierung_WS19",
        ],
        "skip": ["~$"]
    },
    {
        "file": "Modul_GVWL1.md",
        "title": "GVWL 1: Märkte & wirtschaftliche Entscheidungen",
        "dirs": [
            r"03_Bachelor\GVWL 1 - Märkte & wirtschaftliche Entscheidungen\02_Uebungsblaetter_und_Loesungen",
            r"03_Bachelor\GVWL 1 - Märkte & wirtschaftliche Entscheidungen\03_Tutorium",
        ],
        "skip": ["~$"]
    },
    {
        "file": "Modul_Informatikrecht.md",
        "title": "Informatikrecht",
        "dirs": [
            r"03_Bachelor\Informatikrecht\01_Vorlesungsunterlagen",
        ],
        "skip": ["~$"]
    },
    {
        "file": "Modul_Informationsmanagement_Bachelor.md",
        "title": "Informationsmanagement (Grundlagen & Business Intelligence)",
        "dirs": [
            r"03_Bachelor\Informationsmanagement",
        ],
        "skip": ["~$"]
    },
    {
        "file": "Modul_Dienstleistungsmanagement.md",
        "title": "Management von Dienstleistungsunternehmen",
        "dirs": [
            r"03_Bachelor\Management von Dienstleistungsunternehmen\02_Fallstudien_und_Uebungen",
        ],
        "skip": ["~$"]
    },
    {
        "file": "Modul_Mathematik.md",
        "title": "Mathematik für Wirtschaftswissenschaftler",
        "dirs": [
            r"03_Bachelor\Mathematik für Wirtschaftswissenschaftler\02_Uebungen_und_Tutorien",
        ],
        "skip": ["~$"]
    },
    {
        "file": "Modul_MCI.md",
        "title": "Mensch-Computer-Interaktion (MCI)",
        "dirs": [
            r"03_Bachelor\Mensch-Computer-Interaktion\02_Uebungen_und_Design",
        ],
        "skip": ["~$"]
    },
    {
        "file": "Modul_Modellierung.md",
        "title": "Modellierung",
        "dirs": [
            r"03_Bachelor\Modellierung\02_Uebungen_und_Tutorien",
        ],
        "skip": ["~$"]
    },
    {
        "file": "Modul_Programmentwicklung.md",
        "title": "Programmentwicklung (PE)",
        "dirs": [
            r"03_Bachelor\Programmentwicklung\01_Programmentwicklung_WS20\PE1\Aufgabenblaetter",
            r"03_Bachelor\Programmentwicklung\01_Programmentwicklung_WS20\PE2\Aufgabenblätter",
            r"03_Bachelor\Programmentwicklung\02_Programmentwicklung_WS18\Aufgabenblaetter",
            r"03_Bachelor\Programmentwicklung\02_Programmentwicklung_WS18\Uebungsblaetter",
        ],
        "skip": ["~$"]
    },
    {
        "file": "Modul_PSE.md",
        "title": "Programmierung und Software-Entwicklung (PSE)",
        "dirs": [
            r"03_Bachelor\Programmierung und Software-Entwicklung\02_Uebungsblaetter",
            r"03_Bachelor\Programmierung und Software-Entwicklung\03_Projekt_Abgaben",
        ],
        "skip": ["~$"]
    },
    {
        "file": "Modul_Softwarepraktikum.md",
        "title": "Softwarepraktikum (SoPra taskMasterPro)",
        "dirs": [
            r"03_Bachelor\Softwarepraktikum\01_Projekt_taskMasterPro",
            r"03_Bachelor\Softwarepraktikum\02_Spezifikation_und_Lastenheft",
        ],
        "skip": ["~$"]
    },
    {
        "file": "Modul_Statistik1.md",
        "title": "Statistik I (Deskriptive Statistik)",
        "dirs": [
            r"03_Bachelor\Statistik I\01_Uebungen",
        ],
        "skip": ["~$"]
    },
    {
        "file": "Modul_Statistik2.md",
        "title": "Statistik II (Induktive Statistik)",
        "dirs": [
            r"03_Bachelor\Statistik II\02_Uebungen",
        ],
        "skip": ["~$"]
    },
    {
        "file": "Modul_Profilseminar_HRM.md",
        "title": "Profilseminar zum Human Resource Management",
        "dirs": [
            r"03_Bachelor\Profilseminar zum Human Resource Management\01_Seminararbeit_Mensch_Roboter_Interaktion",
            r"03_Bachelor\Profilseminar zum Human Resource Management\02_Seminarorganisation_und_Literatur",
        ],
        "skip": ["~$"]
    },
    {
        "file": "Modul_Seminar_Interdisziplinaer.md",
        "title": "Seminar interdisziplinäre Themen (Maschinelles Lernen)",
        "dirs": [
            r"03_Bachelor\Seminar interdisziplinäre Themen\01_Seminar_Maschinelles_Lernen_SS19",
        ],
        "skip": ["~$"]
    }
]

def run_exercise_extraction():
    t_start = time.time()
    total_files_extracted = 0
    total_chars_added = 0
    
    print("=" * 70)
    print("🚀 SYSTEMATISCHE VOLLTEXT-EXTRAKTION ALLER ÜBUNGEN & FALLSTUDIEN")
    print(f"Vault Verzeichnis: {VAULT_DIR}")
    print("=" * 70)
    
    for idx, mod in enumerate(EXERCISE_REGISTRY, start=1):
        target_path = os.path.join(VAULT_DIR, mod["file"])
        if not os.path.exists(target_path):
            print(f"[{idx}/{len(EXERCISE_REGISTRY)}] Ziel-Dossier fehlt: {mod['file']} (übersprungen)")
            continue
        
        print(f"\n[{idx}/{len(EXERCISE_REGISTRY)}] Verarbeite Übungen für {mod['title']} -> {mod['file']}")
        
        # 1. Collect files
        raw_files = []
        for rel_d in mod["dirs"]:
            full_d = os.path.join(ROOT_DIR, rel_d)
            if not os.path.exists(full_d):
                continue
            for root, dirs, files in os.walk(full_d):
                for f in files:
                    if f.lower().endswith((".pdf", ".docx", ".pptx")) and not f.startswith(("~", "._")):
                        if any(sk.lower() in f.lower() for sk in mod.get("skip", [])):
                            continue
                        # If in a parent directory, check that it's an exercise/aufgabe file
                        fn_low = f.lower()
                        # Skip pure lecture slides if already extracted in slides step
                        if "vorlesung" in fn_low and not any(k in fn_low for k in ["uebung", "übung", "blatt", "aufgabe"]):
                            continue
                        raw_files.append(os.path.join(root, f))
        
        # Deduplicate by file content hash
        unique_files = []
        seen_hashes = set()
        for f in raw_files:
            h = get_file_md5(f)
            if h and h not in seen_hashes:
                seen_hashes.add(h)
                unique_files.append(f)
        
        unique_files.sort(key=lambda x: os.path.basename(x).lower())
        print(f"  Gefundene einzigartige Übungsdateien: {len(unique_files)}")
        
        ex_sections = []
        for f in unique_files:
            fn = os.path.basename(f)
            content_list, fmt = extract_file_content(f)
            if not content_list:
                continue
            file_url = f.replace("\\", "/")
            block = [
                f"\n### 📋 Übungseinheit / Aufgabenblatt: {os.path.splitext(fn)[0]}",
                f"**Datei:** [{fn}](file:///{file_url})  ",
                f"**Format:** {fmt} | **Extrahierte Abschnitte:** {len(content_list)}\n",
                f"#### Aufgabeninhalt & Problemstellung\n" + "\n".join(content_list)
            ]
            ex_sections.append("\n".join(block))
        
        if ex_sections:
            ex_block = (
                "\n\n---\n\n"
                "## 📝 Übungen, Fallstudien & Aufgabenblätter (Volltext-Transkript)\n\n"
                "> [!NOTE] **Systematische Volltext-Dokumentation der Übungs- und Fallstudieninhalte**\n"
                f"> Die folgenden Abschnitte enthalten die unverkürzten Aufgabenstellungen, Fallstudien, Übungsblätter und Lösungsskizzen aus {len(ex_sections)} Übungseinheiten zu diesem Modul.\n"
                "> Dient dem lokalen RAG-System und dem Second Brain als fundierte Methoden- und Praxisbasis.\n"
                + "\n".join(ex_sections)
            )
        else:
            ex_block = (
                "\n\n---\n\n"
                "## 📝 Übungen, Fallstudien & Aufgabenblätter (Volltext-Transkript)\n\n"
                "> [!NOTE] **Übungsdokumentation**\n"
                "> Die praktischen Übungsinhalte wurden primär interaktiv im Tutorium oder integriert in den Vorlesungsfolien bearbeitet.\n"
            )
        
        # Read target note and insert/replace
        with open(target_path, "r", encoding="utf-8") as fp:
            doc_content = fp.read()
        
        split_token = "## 📝 Übungen, Fallstudien & Aufgabenblätter (Volltext-Transkript)"
        if split_token in doc_content:
            doc_content = doc_content.split(split_token)[0].rstrip()
        
        updated_content = doc_content + ex_block
        with open(target_path, "w", encoding="utf-8") as fp:
            fp.write(updated_content)
        
        total_files_extracted += len(ex_sections)
        total_chars_added += len(ex_block)
        print(f"  -> Gespeichert: {len(ex_sections)} Übungseinheiten ({len(ex_block):,} Zeichen).")

    elapsed = time.time() - t_start
    print("\n" + "=" * 70)
    print("✅ ÜBUNGS-EXTRAKTION ERFOLGREICH ABGESCHLOSSEN!")
    print(f"  Extrahierte Übungseinheiten: {total_files_extracted}")
    print(f"  Hinzugefügter Textumfang: {total_chars_added:,} Zeichen")
    print(f"  Benötigte Zeit: {elapsed:.2f} Sekunden")
    print("=" * 70)

if __name__ == "__main__":
    run_exercise_extraction()
