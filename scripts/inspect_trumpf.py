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

with open(r"c:\Users\SHQIPTAR634\Desktop\SSB Dateien\config\gmx_config.json") as f:
    cfg = json.load(f)

for acc in cfg["accounts"]:
    u = acc["email_address"]
    p = acc["password"]
    imap = imaplib.IMAP4_SSL(acc["imap_server"], acc["imap_port"])
    imap.login(u, p)
    imap.select("INBOX", readonly=True)
    
    typ, data = imap.search(None, 'SUBJECT "TRUMPF"')
    msg_ids = data[0].split() if (typ == "OK" and data[0]) else []
    print(f"=== {u}: {len(msg_ids)} TRUMPF Mails ===")
    for mid in msg_ids:
        typ, mdata = imap.fetch(mid, "(RFC822)")
        msg = email.message_from_bytes(mdata[0][1])
        subj = decode_mime(msg.get("Subject", ""))
        date = msg.get("Date", "")
        sender = decode_mime(msg.get("From", ""))
        print(f"MID: {mid.decode()} | Date: {date} | From: {sender} | Subj: {subj}")
        
        # print full payload
        payload = ""
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                if ctype in ["text/plain", "text/calendar"]:
                    try:
                        payload += part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8", errors="replace") + "\n"
                    except:
                        pass
        else:
            try:
                payload = msg.get_payload(decode=True).decode(msg.get_content_charset() or "utf-8", errors="replace")
            except:
                payload = str(msg.get_payload())
                
        print("--- CONTENT SNIPPET ---")
        for line in payload.splitlines()[:25]:
            if line.strip():
                print("  ", line.strip())
        print("="*60)
    imap.logout()
