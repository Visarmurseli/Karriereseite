import imaplib
import email
from email.header import decode_header
import json

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

with open(r"c:\Users\SHQIPTAR634\Desktop\SSB Dateien\config\gmx_config.json") as f:
    cfg = json.load(f)

print("=== Suche nach Schwarz E-Mails zu '4972' oder '11' Uhr / Interview ===")

for acc in cfg["accounts"]:
    u = acc["email_address"]
    p = acc["password"]
    try:
        imap = imaplib.IMAP4_SSL(acc["imap_server"], acc["imap_port"])
        imap.login(u, p)
        imap.select("INBOX", readonly=True)
        
        # Search all mails mentioning schwarz or kadrija or 4972
        search_queries = [
            'SUBJECT "4972"',
            'SUBJECT "Schwarz"',
            'FROM "schwarz"',
            'SUBJECT "Interview"',
            'SUBJECT "Einladung"'
        ]
        found_mids = set()
        for q in search_queries:
            typ, data = imap.search(None, q)
            if typ == "OK" and data[0]:
                for mid in data[0].split():
                    found_mids.add(mid)
                    
        sorted_mids = sorted(found_mids, key=lambda x: int(x), reverse=True)
        print(f"{u}: {len(sorted_mids)} Mails gefunden.")
        
        for mid in sorted_mids[:30]:
            typ, mdata = imap.fetch(mid, "(RFC822)")
            if typ != "OK" or not mdata or not mdata[0]:
                continue
            msg = email.message_from_bytes(mdata[0][1])
            subj = decode_mime(msg.get("Subject", ""))
            sender = decode_mime(msg.get("From", ""))
            date = msg.get("Date", "")
            
            # Check if relevant to Schwarz or 4972 or 11 Uhr
            body, cal = extract_body(msg)
            full_text = (subj + " " + sender + " " + body + " " + cal).lower()
            
            if "schwarz" in full_text or "kadrija" in full_text or "4972" in full_text:
                print(f"\n--- MATCH [{u} | MID {mid.decode()}] ---")
                print(f"Date: {date}")
                print(f"From: {sender}")
                print(f"Subj: {subj}")
                if cal:
                    print(">>> CALENDAR / TEAMS DETECTED <<<")
                    for l in cal.splitlines()[:20]:
                        if l.strip():
                            print("  [CAL]", l.strip())
                print("Body:")
                for l in body.splitlines()[:25]:
                    if l.strip():
                        print("  ", l.strip())
        imap.logout()
    except Exception as e:
        print(f"Fehler bei {u}: {e}")
