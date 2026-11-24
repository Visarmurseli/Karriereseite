import imaplib
import email
from email.header import decode_header
import json
import re
import os
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONFIG_PATH = os.path.join(BASE_DIR, "config", "gmx_config.json")
OUTPUT_JSON = os.path.join(BASE_DIR, "00_Aktuelle_Bewerbungsunterlagen", "deep_emails_dump.json")

def decode_mime(raw):
    if not raw:
        return ""
    try:
        parts = []
        for t, e in decode_header(raw):
            if isinstance(t, bytes):
                parts.append(t.decode(e or "utf-8", errors="replace"))
            else:
                parts.append(str(t))
        return " ".join(parts).strip()
    except Exception:
        return str(raw)

def extract_body(msg):
    body = ""
    calendar_info = ""
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            if ctype == "text/plain":
                try:
                    charset = part.get_content_charset() or "utf-8"
                    body += part.get_payload(decode=True).decode(charset, errors="replace") + "\n"
                except Exception:
                    pass
            elif ctype == "text/calendar":
                try:
                    charset = part.get_content_charset() or "utf-8"
                    calendar_info += part.get_payload(decode=True).decode(charset, errors="replace") + "\n"
                except Exception:
                    pass
    else:
        try:
            charset = msg.get_content_charset() or "utf-8"
            body = msg.get_payload(decode=True).decode(charset, errors="replace")
        except Exception:
            body = str(msg.get_payload())
    return body.strip(), calendar_info.strip()

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    cfg = json.load(f)

deep_records = []

# Keywords to search
search_terms = ["Bewerbung", "Interview", "Trainee", "Consultant", "Stelle", "TRUMPF", "KPMG", "Schwarz", "Coop", "msg", "Axians", "Capgemini", "Deloitte", "Computacenter", "Deutsche Bahn", "Hengstenberg", "LTI", "adesso", "BITBW", "SSB"]

for acc in cfg["accounts"]:
    u = acc["email_address"]
    p = acc["password"]
    print(f"Connecting to {u}...")
    try:
        imap = imaplib.IMAP4_SSL(acc["imap_server"], acc["imap_port"])
        imap.login(u, p)
        imap.select("INBOX", readonly=True)
        
        all_mids = set()
        for term in search_terms:
            try:
                typ, data = imap.search(None, f'(SUBJECT "{term}")')
                if typ == "OK" and data[0]:
                    for mid in data[0].split():
                        all_mids.add(mid)
            except Exception as e:
                pass
                
        sorted_mids = sorted(all_mids, key=lambda x: int(x), reverse=True)
        print(f"  {u}: found {len(sorted_mids)} candidate emails. Fetching top {min(len(sorted_mids), 150)}...")
        
        for mid in sorted_mids[:150]:
            try:
                typ, data = imap.fetch(mid, "(RFC822)")
                if typ != "OK" or not data or not data[0]:
                    continue
                msg = email.message_from_bytes(data[0][1])
                subj = decode_mime(msg.get("Subject", ""))
                sender = decode_mime(msg.get("From", ""))
                to_addr = decode_mime(msg.get("To", ""))
                date_str = msg.get("Date", "")
                
                body, cal = extract_body(msg)
                
                deep_records.append({
                    "account": u,
                    "mid": mid.decode("ascii", errors="ignore"),
                    "subject": subj,
                    "sender": sender,
                    "recipient": to_addr,
                    "date": date_str,
                    "body": body[:5000], # store up to 5000 chars of body
                    "calendar": cal[:2000]
                })
            except Exception as e:
                continue
        imap.logout()
    except Exception as e:
        print(f"Error on {u}: {e}")

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(deep_records, f, indent=2, ensure_ascii=False)

print(f"Successfully dumped {len(deep_records)} emails with full bodies to {OUTPUT_JSON}!")
