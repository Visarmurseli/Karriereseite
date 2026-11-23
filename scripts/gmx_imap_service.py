import os
import sys
import json
import imaplib
import email
from email.header import decode_header
import re
from datetime import datetime

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "gmx_config.json")
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "gmx_config.template.json")
VAULT_COCKPIT_PATH = r"C:\Users\SHQIPTAR634\Documents\Obsidian Vault\01_Karriere_Bewerbungen\00_Bewerbungsmanagement_Cockpit.md"
PIPELINE_JSON_PATH = os.path.join(os.path.dirname(__file__), "..", "00_Aktuelle_Bewerbungsunterlagen", "bewerbungen_pipeline.json")

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    elif os.path.exists(TEMPLATE_PATH):
        with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    else:
        cfg = {
            "email_address": "Visar.murseli@gmx.de",
            "password": "",
            "imap_server": "imap.gmx.net",
            "imap_port": 993,
            "folders": ["INBOX"]
        }
    # Allow environment variable override
    if os.environ.get("GMX_PASSWORD"):
        cfg["password"] = os.environ.get("GMX_PASSWORD")
    if os.environ.get("GMX_EMAIL"):
        cfg["email_address"] = os.environ.get("GMX_EMAIL")
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
                    # simple tag strip
                    clean = re.sub(r"<[^>]+>", " ", html)
                    body_text += re.sub(r"\s+", " ", clean) + "\n"
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset() or "utf-8"
            body_text = payload.decode(charset, errors="replace")
    return body_text.strip()

def classify_application_email(subject, sender, body):
    combined = f"{subject}\n{body}".lower()
    
    # Check for rejection
    rejection_keywords = [
        "absage", "leider mitteilen", "anderweitig entschieden", 
        "nicht weiterverfolgen", "haben uns für einen anderen",
        "nicht berücksichtigen", "nicht erfolgreich", "stelle erstmal zu schließen"
    ]
    if any(k in combined for k in rejection_keywords):
        status = "Absage"
    # Check for 2. Gespräch
    elif any(k in combined for k in ["zweites gespräch", "zweitgespräch", "fachgespräch", "case study", "zweite runde"]):
        status = "2. Gespräch"
    # Check for 1. Gespräch
    elif any(k in combined for k in ["vorstellungsgespräch", "kennenlerngespräch", "telefoninterview", "terminvorschlag", "einladung zum gespräch", "videogespräch"]):
        status = "1. Gespräch"
    # Check for Eingangsbestätigung
    elif any(k in combined for k in ["eingangsbestätigung", "unterlagen erhalten", "vielen dank für ihre bewerbung", "haben wir erhalten"]):
        status = "Eingegangen"
    # Check for Offer
    elif any(k in combined for k in ["vertragsangebot", "arbeitsvertrag", "herzlichen glückwunsch", "freuen uns ihnen ein angebot"]):
        status = "Angebot"
    else:
        status = "In Prüfung"
        
    # Extract Company from Sender or Subject
    sender_clean = re.sub(r"<[^>]+>", "", sender).strip()
    company = sender_clean
    if "@" in sender:
        domain = sender.split("@")[-1].replace(">", "").strip()
        comp_guess = domain.split(".")[0].capitalize()
        if comp_guess.lower() not in ["gmail", "gmx", "web", "outlook", "mail", "postfach", "reply"]:
            company = comp_guess
    
    # Extract job position candidate
    pos = "SAP Consultant / Trainee"
    m_pos = re.search(r"(?:stelle\s+als|position\s+als|für\s+die\s+stelle|ihre\s+bewerbung\s+als|bewerbung\s+als|bewerbung\s+auf)\s+([^\n\r,\.]+)", subject, re.I)
    if m_pos:
        pos = m_pos.group(1).strip()
    
    return {
        "company": company,
        "position": pos,
        "status": status,
        "subject": subject,
        "sender": sender
    }

def connect_imap(cfg):
    server = cfg.get("imap_server", "imap.gmx.net")
    port = cfg.get("imap_port", 993)
    user = cfg.get("email_address", "Visar.murseli@gmx.de")
    pwd = cfg.get("password", "")
    
    if not pwd:
        print("\n" + "!" * 70)
        print("⚠️ GMX IMAP PASSWORT NICHT HINTERLEGT")
        print("!" * 70)
        print("Um die E-Mails automatisch abzurufen, wird ein GMX-Passwort benötigt.")
        print("Anleitung zur Aktivierung:")
        print("  1. Logge dich im Browser auf gmx.net ein.")
        print("  2. Klicke links unten auf 'Einstellungen' (Zahnrad).")
        print("  3. Wähle 'Zu den Einstellungen' -> 'E-Mail' -> 'POP3/IMAP Abruf'.")
        print("  4. Aktiviere das Häkchen bei: 'POP3 und IMAP Zugriff erlauben' und speichere.")
        print("  5. Trage das Passwort in 'config/gmx_config.json' ein oder setze die Umgebungsvariable:")
        print("     $env:GMX_PASSWORD='dein_passwort'")
        print("!" * 70)
        return None
    
    try:
        print(f"Verbinde mit {server}:{port} via SSL...")
        imap = imaplib.IMAP4_SSL(server, port)
        imap.login(user, pwd)
        print(f"✅ Erfolgreich angemeldet als {user}!")
        return imap
    except imaplib.IMAP4.error as e:
        print(f"❌ IMAP Login fehlgeschlagen: {e}")
        print("Hinweis: Falls das Passwort korrekt ist, überprüfe bitte, ob 'POP3/IMAP Zugriff' in den GMX-Webmail-Einstellungen aktiviert ist.")
        return None
    except Exception as e:
        print(f"❌ Verbindungsfehler: {e}")
        return None

def fetch_pipeline_records(imap, cfg):
    records = []
    folders = cfg.get("folders", ["INBOX"])
    keywords = cfg.get("keywords", ["Bewerbung", "Eingangsbestätigung", "Absage", "Interview"])
    
    for folder in folders:
        try:
            status, count = imap.select(folder, readonly=True)
            if status != "OK":
                continue
            print(f"Durchsuche Ordner '{folder}'...")
            
            # Search with OR conditions or individual keywords
            all_ids = set()
            for kw in keywords:
                typ, data = imap.search(None, f'(SUBJECT "{kw}")')
                if typ == "OK" and data[0]:
                    for msg_id in data[0].split():
                        all_ids.add(msg_id)
            
            print(f"  Gefundene relevante E-Mails: {len(all_ids)}")
            
            # Fetch each email
            for msg_id in sorted(all_ids, reverse=True)[:50]:
                typ, msg_data = imap.fetch(msg_id, "(RFC822.PEEK[HEADER.FIELDS (FROM TO SUBJECT DATE)] BODY.PEEK[TEXT])")
                if typ != "OK":
                    continue
                raw = msg_data[0][1]
                msg = email.message_from_bytes(raw)
                
                subject = decode_mime_words(msg.get("Subject", ""))
                sender = decode_mime_words(msg.get("From", ""))
                date_str = msg.get("Date", "")
                body = extract_body_text(msg)
                
                parsed = classify_application_email(subject, sender, body)
                parsed["date"] = date_str[:16] if len(date_str) >= 16 else date_str
                records.append(parsed)
                
        except Exception as e:
            print(f"Fehler beim Abruf von {folder}: {e}")
            
    return records

def sync_to_obsidian_cockpit(records):
    if not os.path.exists(VAULT_COCKPIT_PATH):
        print(f"Cockpit-Datei nicht gefunden: {VAULT_COCKPIT_PATH}")
        return
    
    with open(VAULT_COCKPIT_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Save JSON backup
    os.makedirs(os.path.dirname(PIPELINE_JSON_PATH), exist_ok=True)
    with open(PIPELINE_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
    print(f"Gespeichert: {PIPELINE_JSON_PATH}")

def print_status_summary():
    cfg = load_config()
    print("=" * 60)
    print("📬 GMX IMAP BEWERBUNGS-CONNECTOR STATUS")
    print("=" * 60)
    print(f"  Konto:       {cfg.get('email_address')}")
    print(f"  Server:      {cfg.get('imap_server')}:{cfg.get('imap_port')}")
    print(f"  Passwort:    {'[Gesetzt/Konfiguriert]' if cfg.get('password') else '[FEHLT - Bitte konfigurieren]'}")
    print(f"  Suchordner:  {', '.join(cfg.get('folders', []))}")
    print(f"  Config-Pfad: {CONFIG_PATH}")
    print("=" * 60)

if __name__ == "__main__":
    if "--status" in sys.argv:
        print_status_summary()
    elif "--test" in sys.argv or "--sync" in sys.argv:
        cfg = load_config()
        imap = connect_imap(cfg)
        if imap:
            records = fetch_pipeline_records(imap, cfg)
            print(f"Erfolgreich {len(records)} Bewerbungs-Mails analysiert.")
            sync_to_obsidian_cockpit(records)
            imap.logout()
    else:
        print_status_summary()
        print("\nVerwendung:")
        print("  python scripts/gmx_imap_service.py --status     # Konfiguration anzeigen")
        print("  python scripts/gmx_imap_service.py --test       # Verbindung testen & Mails synchronisieren")
