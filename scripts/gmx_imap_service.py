import os
import sys
import json
import imaplib
import email
from email.header import decode_header
import re
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONFIG_PATH = os.path.join(BASE_DIR, "config", "gmx_config.json")
TEMPLATE_PATH = os.path.join(BASE_DIR, "config", "gmx_config.template.json")
EXCEL_PATH = os.path.join(BASE_DIR, "00_Aktuelle_Bewerbungsunterlagen", "Bewerbungsverlauf.xlsx")
CSV_REMAINING_PATH = os.path.join(BASE_DIR, "config", "notion_crm_remaining.csv")
VAULT_COCKPIT_PATH = r"C:\Users\SHQIPTAR634\Documents\Obsidian Vault\01_Karriere_Bewerbungen\00_Bewerbungsmanagement_Cockpit.md"
PIPELINE_JSON_PATH = os.path.join(BASE_DIR, "00_Aktuelle_Bewerbungsunterlagen", "bewerbungen_pipeline.json")
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))

if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

# Bekannte Recruiter-/Absender-Bereinigungen auf echte Unternehmen
EMPLOYER_REMAP = {
    "berivan mutlutürk": ("Stadtwerke Pforzheim", None),
    "özlem sevinç": ("Amadeus FiRe AG (Ref: AF:0270702)", None),
    "webmailer amadeus fire": ("Amadeus FiRe AG", None),
    "amadeus fire": ("Amadeus FiRe AG", None),
    "marie-sophie.grootens@bkb.ch": ("Basler Kantonalbank (BKB)", "Trainee-Programm Finance & Controlling"),
}

DOMAIN_EMPLOYER_MAP = {
    "stadtwerke-pforzheim": "Stadtwerke Pforzheim",
    "amadeus-fire": "Amadeus FiRe AG",
    "bkb": "Basler Kantonalbank (BKB)",
    "mail.schwarz": "Schwarz Digits",
    "schwarz": "Schwarz Digits",
    "kpmg": "KPMG",
    "trumpf": "TRUMPF",
    "ssb-ag": "Stuttgarter Straßenbahnen AG (SSB)",
    "porsche": "Porsche AG",
    "mhp": "MHP (Porsche Company)",
    "mercedes-benz": "Mercedes-Benz",
    "bosch": "Bosch Group",
    "capgemini": "Capgemini Invent",
    "ey": "EY (Ernst & Young)",
    "msg.group": "msg systems",
    "computacenter": "Computacenter",
    "coop": "Coop (Schweiz)",
    "adesso": "adesso SE",
    "cgi": "CGI",
    "x1f": "x1F",
    "mindsquare": "mindsquare",
    "appliedai": "appliedAI",
    "lidl": "Lidl Stiftung & Co. KG",
}

ATS_DOMAINS = ("join.com", "personio", "softgarden", "recruitee", "workday", "greenhouse", "lever.co", "successfactors", "smartrecruiters")

DISTINCTIVE_ROLE_WORDS = {
    "public", "sector", "technical", "basis", "cloud", "product", "owner",
    "security", "hcm", "alm", "crm", "logistik", "developer", "architecture",
    "trainee", "data", "bi", "praktikum", "datenschutz", "werkstudent"
}

NOISE_SENDERS = ("gmxnet.de", "terminerinnerung", "stepstone", "indeed", "kununu", "linkedin", "xing", "jobware", "monster")

STATUS_RANK = {
    "In Prüfung": 1,
    "Eingegangen": 2,
    "1. Gespräch": 3,
    "2. Gespräch": 4,
    "Absage": 5,
    "Angebot": 6,
}


def normalize_whitespace(text):
    return re.sub(r"[ \t]+", " ", str(text or "")).strip()


def normalize_employer_and_role(employer, role):
    emp = normalize_whitespace(employer)
    rl = normalize_whitespace(role)
    key = emp.lower()
    if key in ("terminerinnerung", "mailings@gmxnet.de"):
        return None, None
    if key in EMPLOYER_REMAP:
        new_emp, forced_role = EMPLOYER_REMAP[key]
        emp = new_emp
        if forced_role and ("(junior) sap" in rl.lower() or not rl):
            rl = forced_role
    return emp, rl


def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    elif os.path.exists(TEMPLATE_PATH):
        with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    else:
        cfg = {"accounts": []}

    accounts = cfg.get("accounts", [])
    if not accounts and cfg.get("email_address"):
        accounts = [{
            "name": "Standard-Konto",
            "email_address": cfg.get("email_address"),
            "password": cfg.get("password", ""),
            "imap_server": cfg.get("imap_server", "imap.gmx.net"),
            "imap_port": cfg.get("imap_port", 993),
            "folders": cfg.get("folders", ["INBOX"])
        }]
    cfg["accounts"] = accounts
    return cfg


def decode_mime_words(raw_header):
    if not raw_header:
        return ""
    decoded_fragments = decode_header(raw_header)
    parts = []
    for text, enc in decoded_fragments:
        if isinstance(text, bytes):
            try:
                parts.append(text.decode(enc or "utf-8", errors="replace"))
            except Exception:
                parts.append(text.decode("latin1", errors="replace"))
        else:
            parts.append(str(text))
    return " ".join(parts).strip()


def extract_body_text(msg):
    body_text = ""
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdisp = str(part.get("Content-Disposition", ""))
            if ctype == "text/plain" and "attachment" not in cdisp:
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or "utf-8"
                    body_text += payload.decode(charset, errors="replace") + "\n"
            elif ctype == "text/html" and not body_text and "attachment" not in cdisp:
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or "utf-8"
                    html = payload.decode(charset, errors="replace")
                    clean = re.sub(r"<[^>]+>", " ", html)
                    body_text += re.sub(r"\s+", " ", clean) + "\n"
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset() or "utf-8"
            body_text = payload.decode(charset, errors="replace")
    return body_text.strip()


def _parse_email_dt_and_de(raw_date):
    try:
        from email.utils import parsedate_to_datetime
        dt = parsedate_to_datetime(raw_date)
        dt_naive = dt.replace(tzinfo=None)
        return dt_naive, dt_naive.strftime("%d.%m.%Y")
    except Exception:
        now = datetime.now()
        return now, now.strftime("%d.%m.%Y")


def _parse_de_date(val):
    m = re.search(r"(\d{1,2})\.(\d{1,2})\.(\d{4})", str(val or ""))
    if m:
        return datetime(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    return None


def classify_application_email(subject, sender, body, raw_date=""):
    combined = f"{subject}\n{body}".lower()
    subj_low = subject.lower()
    s_low = f"{subject} {sender}".lower()
    if any(ns in s_low for ns in NOISE_SENDERS):
        return None

    rejection_keywords = [
        "leider absagen", "eine absage erteilen", "absage", "leider mitteilen",
        "anderweitig entschieden", "nicht weiterverfolgen",
        "haben uns für einen anderen", "nicht berücksichtigen",
        "nicht erfolgreich", "stelle erstmal zu schließen", "vorerst geschlossen"
    ]
    if any(k in subj_low for k in ["einladung zum erstgespräch", "einladung zum vorstellungsgespräch", "einladung zum interview", "microsoft teams interview", "terminbestätigung"]):
        status = "1. Gespräch"
    elif any(k in combined for k in ["vertragsangebot", "arbeitsvertrag beiliegend", "freuen uns, ihnen ein angebot", "freuen uns ihnen ein angebot", "ihr konkretes angebot"]):
        status = "Angebot"
    elif any(k in combined for k in rejection_keywords):
        status = "Absage"
    elif any(k in combined for k in ["zweites gespräch", "zweitgespräch", "fachgespräch", "zweite runde"]):
        status = "2. Gespräch"
    elif any(k in combined for k in ["vorstellungsgespräch", "kennenlerngespräch", "telefoninterview", "terminvorschlag", "einladung zum gespräch", "einladung zum interview", "einladung zum erstgespräch", "videogespräch"]):
        status = "1. Gespräch"
    elif any(k in combined for k in ["eingangsbestätigung", "unterlagen erhalten", "vielen dank für ihre bewerbung", "vielen dank für deine bewerbung", "haben wir erhalten", "bewerbungseingang", "deine bewerbung ist da"]):
        status = "Eingegangen"
    else:
        status = "In Prüfung"

    sender_clean = re.sub(r"<[^>]+>", "", sender).strip().strip('"')
    sender_clean = re.sub(r"\s*(Recruiting Team|Recruiting|HR Team|Talent Acquisition)\s*$", "", sender_clean, flags=re.I).strip()
    company = sender_clean
    if "@" in sender:
        domain = sender.split("@")[-1].replace(">", "").strip().lower()
        is_ats = any(ats in domain for ats in ATS_DOMAINS)
        dom_hit = None if is_ats else next((v for k, v in DOMAIN_EMPLOYER_MAP.items() if k in domain), None)
        if dom_hit:
            company = dom_hit
        elif not is_ats:
            comp_guess = domain.split(".")[0].capitalize()
            if comp_guess.lower() not in ["gmail", "gmx", "web", "outlook", "mail", "postfach", "reply", "noreply", "recruiting", "jobs", "career", "karriere", "candidate"]:
                company = comp_guess
    # Fallback: "Deine Bewerbung bei <Company>"
    if company == sender_clean or not company:
        m_sub_comp = re.search(r"bewerbung\s+bei\s+([^:|\n\r]+)", subject, re.I)
        if m_sub_comp:
            cand_c = normalize_whitespace(m_sub_comp.group(1))
            if len(cand_c) >= 3:
                company = cand_c

    pos = "SAP / IT Consultant"
    m_pos = re.search(r"(?:stelle\s+als|position\s+als|für\s+die\s+stelle|ihre\s+bewerbung\s+als|bewerbung\s+als|bewerbung\s+auf|schwarz\s+digits\s*[:\-]|deine\s+bewerbung\s*[:\-])\s*([^\n\r,\|]+)", subject, re.I)
    if m_pos:
        pos = normalize_whitespace(m_pos.group(1))

    company, pos = normalize_employer_and_role(company, pos)
    if not company:
        return None

    dt_obj, date_de = _parse_email_dt_and_de(raw_date)
    return {
        "company": company,
        "position": pos,
        "status": status,
        "status_rank": STATUS_RANK.get(status, 1),
        "date_de": date_de,
        "timestamp": dt_obj.isoformat(),
        "subject": normalize_whitespace(subject),
        "sender": normalize_whitespace(sender)
    }


def connect_account(acc):
    server = acc.get("imap_server", "imap.gmx.net")
    port = acc.get("imap_port", 993)
    user = acc.get("email_address", "")
    pwd = acc.get("password", "")
    name = acc.get("name", user)

    print(f"\n--- [Konto: {name}] ---")
    if not pwd:
        print(f"  ⚠️ Kein Passwort für {user} hinterlegt.")
        return None

    try:
        imap = imaplib.IMAP4_SSL(server, port, timeout=15)
        imap.login(user, pwd)
        print(f"  ✅ Erfolgreich angemeldet als {user}!")
        return imap
    except Exception as e:
        print(f"  ❌ IMAP Fehler für {user}: {e}")
        return None


def fetch_account_records(imap, acc, keywords, max_msgs=35):
    records = []
    folders = acc.get("folders", ["INBOX"])
    user = acc.get("email_address", "")

    # IMAP SEARCH requires ASCII-safe query terms unless RFC-6855 UTF8 is negotiated
    ascii_keywords = []
    for kw in keywords:
        clean_kw = re.sub(r"[^\x20-\x7E]+", "", str(kw))
        # Take longest ASCII stem >= 4 chars (e.g. Vorstellungsgespräch -> Vorstellungsgespr)
        stems = [s for s in re.split(r"[^A-Za-z0-9]+", str(kw)) if s.isascii() and len(s) >= 4]
        if str(kw).isascii():
            ascii_keywords.append(str(kw))
        elif stems:
            ascii_keywords.append(max(stems, key=len))
    ascii_keywords = list(dict.fromkeys(ascii_keywords))

    for folder in folders:
        try:
            status, _ = imap.select(folder, readonly=True)
            if status != "OK":
                continue

            all_ids = set()
            for kw in ascii_keywords:
                typ, data = imap.search(None, f'(SUBJECT "{kw}")')
                if typ == "OK" and data[0]:
                    for msg_id in data[0].split():
                        all_ids.add(msg_id)

            print(f"  Gefundene relevante E-Mails in {folder}: {len(all_ids)}")
            sorted_ids = sorted(all_ids, key=lambda x: int(x), reverse=True)
            for msg_id in sorted_ids[:max_msgs]:
                typ, msg_data = imap.fetch(msg_id, "(BODY.PEEK[])")
                if typ != "OK" or not msg_data or not isinstance(msg_data[0], tuple):
                    continue
                msg = email.message_from_bytes(msg_data[0][1])

                subject = decode_mime_words(msg.get("Subject", ""))
                sender = decode_mime_words(msg.get("From", ""))
                date_str = msg.get("Date", "")
                body = extract_body_text(msg)[:4500]

                parsed = classify_application_email(subject, sender, body, date_str)
                if not parsed:
                    continue
                parsed["date"] = date_str[:16] if len(date_str) >= 16 else date_str
                parsed["account"] = user
                records.append(parsed)
        except Exception as e:
            print(f"  Fehler beim Abruf von {folder}: {e}")

    return records


def clean_existing_tracker():
    """Bereinigt Excel (beide Sheets), Obsidian-Cockpit & Remaining-CSV nicht-destruktiv in-place."""
    changes = []
    if os.path.exists(EXCEL_PATH):
        import openpyxl
        wb = openpyxl.load_workbook(EXCEL_PATH)
        for sheet_name in ("Bewerbungsverlauf", "Stellenprofile_Details"):
            if sheet_name not in wb.sheetnames:
                continue
            ws = wb[sheet_name]
            rows_to_delete = []
            for r in range(2, ws.max_row + 1):
                comp = ws.cell(r, 1).value
                role = ws.cell(r, 2).value
                new_comp, new_role = normalize_employer_and_role(comp, role)
                if new_comp is None:
                    rows_to_delete.append(r)
                    changes.append(f"{sheet_name}: Zeile {r} ('Terminerinnerung') entfernt")
                    continue
                if new_comp != comp:
                    ws.cell(r, 1).value = new_comp
                    changes.append(f"{sheet_name}: '{comp}' -> '{new_comp}'")
                if new_role != role:
                    ws.cell(r, 2).value = new_role
                # Collapse double/triple spaces in all cells on cleaned rows
                for c in range(1, ws.max_column + 1):
                    v = ws.cell(r, c).value
                    if isinstance(v, str) and "  " in v:
                        ws.cell(r, c).value = normalize_whitespace(v)
            for r_del in reversed(rows_to_delete):
                ws.delete_rows(r_del, 1)
        wb.save(EXCEL_PATH)

    if os.path.exists(VAULT_COCKPIT_PATH):
        txt = open(VAULT_COCKPIT_PATH, "r", encoding="utf-8").read()
        orig = txt
        txt = re.sub(r"\|\s*\*\*Terminerinnerung\*\*[^\n]*\n", "", txt)
        txt = re.sub(r"> \[!INFO\] \*\*Terminerinnerung –[^\n]*\n(?:>[^\n]*\n)*\n?", "", txt)
        txt = txt.replace("**Berivan Mutlutürk**", "**Stadtwerke Pforzheim**")
        txt = txt.replace("[!INFO] **Berivan Mutlutürk –", "[!INFO] **Stadtwerke Pforzheim –")
        txt = txt.replace("**Özlem Sevinç**", "**Amadeus FiRe AG (Ref: AF:0270702)**")
        txt = txt.replace("[!INFO] **Özlem Sevinç –", "[!INFO] **Amadeus FiRe AG (Ref: AF:0270702) –")
        txt = txt.replace("**Webmailer Amadeus Fire**", "**Amadeus FiRe AG**")
        txt = txt.replace("[!INFO] **Webmailer Amadeus Fire –", "[!INFO] **Amadeus FiRe AG –")
        txt = txt.replace("**marie-sophie.grootens@bkb.ch**", "**Basler Kantonalbank (BKB)**")
        txt = txt.replace("[!INFO] **marie-sophie.grootens@bkb.ch –", "[!INFO] **Basler Kantonalbank (BKB) –")
        txt = txt.replace("Referent:in   Prozessmanagement", "Referent:in Prozessmanagement")
        txt = txt.replace("energiewirtschaftliche   Anwendungen", "energiewirtschaftliche Anwendungen")
        if txt != orig:
            with open(VAULT_COCKPIT_PATH, "w", encoding="utf-8") as f:
                f.write(txt)
            changes.append("Obsidian 00_Bewerbungsmanagement_Cockpit.md normalisiert")

    if os.path.exists(CSV_REMAINING_PATH):
        import csv
        with open(CSV_REMAINING_PATH, "r", encoding="utf-8-sig", newline="") as f:
            rows = list(csv.reader(f))
        if rows:
            hdr, body = rows[0], rows[1:]
            cleaned = []
            for r in body:
                if not r:
                    continue
                nc, nr = normalize_employer_and_role(r[0], r[1] if len(r) > 1 else "")
                if nc is None:
                    continue
                r[0] = nc
                if len(r) > 1:
                    r[1] = nr
                cleaned.append([normalize_whitespace(cell) for cell in r])
            with open(CSV_REMAINING_PATH, "w", encoding="utf-8-sig", newline="") as f:
                w = csv.writer(f)
                w.writerow(hdr)
                w.writerows(cleaned)
            changes.append(f"CSV remaining normalisiert ({len(cleaned)} Zeilen)")

    try:
        from local_rag_engine import upsert_note
        upsert_note(VAULT_COCKPIT_PATH)
    except Exception:
        pass
    return changes


def _best_matching_row(ws, company, position, subject, date_de):
    """Finds exact company+role row avoiding collisions across distinct postings at the same employer."""
    ck = company.lower()
    email_tokens = set(re.findall(r"[a-z0-9]{2,}", f"{position} {subject}".lower()))
    email_dist = email_tokens & DISTINCTIVE_ROLE_WORDS
    pos_tokens = {w for w in email_tokens if len(w) >= 4 and w not in ("junior", "consultant", "bewerbung", "ihre", "stelle", "genders")}

    candidates = []
    for r in range(2, ws.max_row + 1):
        c_name = str(ws.cell(r, 1).value or "").strip().lower()
        c_role = str(ws.cell(r, 2).value or "").strip().lower()
        c_date = str(ws.cell(r, 3).value or "").strip()
        c_ack = str(ws.cell(r, 4).value or "").strip()
        if not c_name:
            continue
        if ck in c_name or c_name in ck:
            role_tokens_all = set(re.findall(r"[a-z0-9]{2,}", c_role))
            role_dist = role_tokens_all & DISTINCTIVE_ROLE_WORDS
            # Guard: two completely different specialized postings at the same employer (e.g., Technical SAP vs Public Sector)
            if email_dist and role_dist and not (email_dist & role_dist):
                continue
            role_tokens = {w for w in role_tokens_all if len(w) >= 4}
            overlap = len(pos_tokens & role_tokens)
            date_bonus = 2 if date_de in (c_date, c_ack) else 0
            candidates.append((overlap + date_bonus, r))
    if not candidates:
        return None
    candidates.sort(key=lambda x: x[0], reverse=True)
    if len(candidates) > 1 and candidates[0][0] == 0:
        return None
    return candidates[0][1]


def sync_imap_to_career_os(max_per_account=35, dry_run=False):
    """Synchronisiert GMX IMAP live mit Bewerbungsverlauf.xlsx, Obsidian Cockpit & RAG."""
    cfg = load_config()
    keywords = [
        "Bewerbung", "Eingangsbest", "Vorstellungsgespr",
        "Interview", "Kennenlernen", "Absage", "Stelle", "Trainee", "Consultant", "Einladung"
    ]
    accounts_ok = 0
    accounts_err = 0
    all_records = []
    seen_keys = set()

    for acc in cfg.get("accounts", []):
        imap = connect_account(acc)
        if imap:
            accounts_ok += 1
            acc_records = fetch_account_records(imap, acc, keywords, max_msgs=max_per_account)
            for r in acc_records:
                key = (r["company"].lower(), r["subject"].lower(), r["date"][:10])
                if key not in seen_keys:
                    seen_keys.add(key)
                    all_records.append(r)
            try:
                imap.logout()
            except Exception:
                pass
        else:
            accounts_err += 1

    os.makedirs(os.path.dirname(PIPELINE_JSON_PATH), exist_ok=True)
    with open(PIPELINE_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(all_records, f, indent=2, ensure_ascii=False)

    updated = []
    added = []
    if os.path.exists(EXCEL_PATH) and all_records:
        import openpyxl
        wb = openpyxl.load_workbook(EXCEL_PATH)
        ws = wb["Bewerbungsverlauf"]

        best_by_key = {}
        for rec in all_records:
            # Skip automated sender domains without strong company extraction
            if rec["company"].lower() in ("mailings", "noreply", "no-reply", "notifications", "gmx", "info", "service"):
                continue
            bk = (rec["company"].lower(), rec["position"].lower()[:30])
            if bk not in best_by_key or rec["status_rank"] > best_by_key[bk]["status_rank"]:
                best_by_key[bk] = rec

        for (_, _), rec in best_by_key.items():
            rec_dt = _parse_de_date(rec["date_de"])
            r_idx = _best_matching_row(ws, rec["company"], rec["position"], rec["subject"], rec["date_de"])
            if r_idx is not None:
                # Chronology guard: never apply an older email over a newer Excel milestone
                row_dates = [d for d in (_parse_de_date(ws.cell(r_idx, c).value) for c in (3, 4, 5, 6)) if d]
                latest_row_dt = max(row_dates) if row_dates else None
                if rec_dt and latest_row_dt and rec_dt < latest_row_dt:
                    continue

                cur_status = str(ws.cell(r_idx, 7).value or "")
                cur_rank = 1
                if "Absage" in cur_status:
                    cur_rank = 5
                elif "2." in cur_status or "Runde 2" in cur_status or "Fachinterview" in cur_status:
                    cur_rank = 4
                elif any(x in cur_status for x in ["Gespräch", "Interview", "Einladung"]):
                    cur_rank = 3
                elif "bestätigt" in cur_status or "Eingegangen" in cur_status:
                    cur_rank = 2

                # Never overwrite active interviews (cur_rank >= 3) with unspecific rejections without exact role match
                if rec["status_rank"] > cur_rank and cur_rank < 5:
                    if not dry_run:
                        ws.cell(r_idx, 7).value = f"{rec['status']} (IMAP Sync {rec['date_de']})"
                        if rec["status"] == "1. Gespräch" and str(ws.cell(r_idx, 5).value or "-") == "-":
                            ws.cell(r_idx, 5).value = rec["date_de"]
                    updated.append(f"{ws.cell(r_idx, 1).value}: {cur_status} -> {rec['status']}")
            elif rec["status_rank"] >= 3 and len(rec["company"]) >= 3:
                # Skip historical emails older than 14 days when auto-creating unmatched rows
                if rec_dt and (datetime.now() - rec_dt).days > 14:
                    continue
                if not dry_run:
                    ws.append([
                        rec["company"],
                        rec["position"],
                        rec["date_de"],
                        rec["date_de"],
                        rec["date_de"] if rec["status"] == "1. Gespräch" else "-",
                        rec["date_de"] if rec["status"] == "2. Gespräch" else "-",
                        f"{rec['status']} (IMAP Sync {rec['date_de']})"
                    ])
                added.append(f"{rec['company']} ({rec['status']} | {rec['date_de']})")
        if not dry_run and (updated or added):
            wb.save(EXCEL_PATH)
            _sync_excel_matrix_to_cockpit(ws)
            try:
                from local_rag_engine import upsert_note
                upsert_note(VAULT_COCKPIT_PATH)
            except Exception:
                pass

    return {
        "accounts_ok": accounts_ok,
        "accounts_err": accounts_err,
        "fetched": len(all_records),
        "updated": updated,
        "added": added
    }


def _sync_excel_matrix_to_cockpit(ws):
    """Aktualisiert die Status-Matrix-Tabelle in 00_Bewerbungsmanagement_Cockpit.md aus Excel."""
    if not os.path.exists(VAULT_COCKPIT_PATH):
        return
    txt = open(VAULT_COCKPIT_PATH, "r", encoding="utf-8").read()
    marker_start = "## 📋 Status-Matrix der Bewerbungen"
    marker_end = "## 📑 Detaillierte Stellenbeschreibungen"
    if marker_start not in txt or marker_end not in txt:
        return
    lines = [
        marker_start,
        "",
        "| Arbeitgeber | Genaue Stellenbezeichnung & Referenz | Datum | Eingang | 1. Gespräch | 2. Gespräch | Status / Ergebnis |",
        "| :--- | :--- | :---: | :---: | :---: | :---: | :--- |",
    ]
    for r in range(2, ws.max_row + 1):
        vals = [normalize_whitespace(ws.cell(r, c).value or "-") for c in range(1, 8)]
        if vals[0] in ("-", ""):
            continue
        lines.append(f"| **{vals[0]}** | {vals[1]} | {vals[2]} | {vals[3]} | {vals[4]} | {vals[5]} | {vals[6]} |")
    prefix = txt.split(marker_start, 1)[0]
    suffix = txt.split(marker_end, 1)[1]
    new_txt = prefix + "\n".join(lines) + "\n\n---\n\n" + marker_end + suffix
    with open(VAULT_COCKPIT_PATH, "w", encoding="utf-8") as f:
        f.write(new_txt)


def print_status_summary():
    cfg = load_config()
    print("=" * 65)
    print("📬 GMX MULTI-ACCOUNT IMAP BEWERBUNGS-CONNECTOR")
    print("=" * 65)
    for i, acc in enumerate(cfg.get("accounts", []), start=1):
        pwd_set = bool(acc.get("password"))
        print(f"  [{i}] {acc.get('name', 'Konto')}:")
        print(f"      E-Mail:    {acc.get('email_address')}")
        print(f"      Server:    {acc.get('imap_server')}:{acc.get('imap_port')}")
        print(f"      Passwort:  {'[Konfiguriert]' if pwd_set else '[FEHLT]'}")
        print(f"      Suchordner: {', '.join(acc.get('folders', []))}")
    print("=" * 65)


if __name__ == "__main__":
    if "--status" in sys.argv:
        print_status_summary()
    elif "--clean-excel" in sys.argv:
        res = clean_existing_tracker()
        print("CLEANED:", json.dumps(res, ensure_ascii=False, indent=2))
    elif "--test" in sys.argv or "--sync" in sys.argv:
        res = sync_imap_to_career_os(dry_run=("--dry-run" in sys.argv))
        print("SYNC_RESULT:", json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print_status_summary()
