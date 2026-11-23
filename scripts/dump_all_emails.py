import json
import imaplib
import email
from email.header import decode_header
import re
import os

CONFIG_PATH = r"c:\Users\SHQIPTAR634\Desktop\SSB Dateien\config\gmx_config.json"
OUTPUT_JSON = r"c:\Users\SHQIPTAR634\Desktop\SSB Dateien\00_Aktuelle_Bewerbungsunterlagen\all_application_emails.json"

def decode_mime_words(raw_header):
    if not raw_header:
        return ""
    try:
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
    except Exception:
        return str(raw_header)

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    cfg = json.load(f)

all_emails = []

for acc in cfg.get("accounts", []):
    u = acc.get("email_address")
    p = acc.get("password")
    print(f"Lese Header fuer {u}...")
    try:
        imap = imaplib.IMAP4_SSL(acc["imap_server"], acc["imap_port"])
        imap.login(u, p)
        imap.select("INBOX", readonly=True)
        
        search_terms = ["Bewerbung", "Interview", "Absage", "Status", "Stelle", "Trainee", "Consultant", "KPMG", "Schwarz"]
        msg_ids = set()
        for st in search_terms:
            typ, data = imap.search(None, f'(SUBJECT "{st}")')
            if typ == "OK" and data[0]:
                for mid in data[0].split():
                    msg_ids.add(mid)
                    
        sorted_ids = sorted(msg_ids, key=lambda x: int(x), reverse=True)
        print(f"  {u}: {len(sorted_ids)} passende Mails. Lade die neuesten {min(len(sorted_ids), 120)}...")
        
        for mid in sorted_ids[:120]:
            try:
                typ, data = imap.fetch(mid, "(BODY.PEEK[HEADER.FIELDS (FROM TO SUBJECT DATE)])")
                if typ != "OK" or not data or not data[0]:
                    continue
                raw_header = data[0][1]
                msg = email.message_from_bytes(raw_header)
                
                subj = decode_mime_words(msg.get("Subject", ""))
                sender = decode_mime_words(msg.get("From", ""))
                recipient = decode_mime_words(msg.get("To", ""))
                date_str = msg.get("Date", "")
                
                all_emails.append({
                    "account": u,
                    "mid": mid.decode("ascii", errors="ignore"),
                    "subject": subj,
                    "sender": sender,
                    "recipient": recipient,
                    "date": date_str
                })
            except Exception:
                continue
                
        imap.logout()
    except Exception as e:
        print(f"  Fehler bei {u}: {e}")

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(all_emails, f, indent=2, ensure_ascii=False)

print(f"Erfolgreich {len(all_emails)} E-Mails in {OUTPUT_JSON} gespeichert.")
