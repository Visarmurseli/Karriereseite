import json
import re

with open(r"c:\Users\SHQIPTAR634\Desktop\SSB Dateien\00_Aktuelle_Bewerbungsunterlagen\deep_emails_dump.json", "r", encoding="utf-8") as f:
    emails = json.load(f)

print(f"Loaded {len(emails)} deep emails.")

# Check KPMG specifically
print("\n=== KPMG EMAILS ===")
for em in emails:
    text = (em["subject"] + " " + em["sender"] + " " + em["body"]).lower()
    if "kpmg" in text:
        print(f"Date: {em['date']} | Sender: {em['sender']} | Subj: {em['subject']}")
        print("Body snippet:")
        for line in em["body"].splitlines()[:12]:
            if line.strip():
                print("  ", line.strip())
        print("-" * 40)

# Check Coop specifically
print("\n=== COOP EMAILS ===")
for em in emails:
    text = (em["subject"] + " " + em["sender"]).lower()
    if "coop" in text:
        print(f"Date: {em['date']} | Sender: {em['sender']} | Subj: {em['subject']}")
        for line in em["body"].splitlines()[:10]:
            if line.strip():
                print("  ", line.strip())
        print("-" * 40)

# Check msg specifically
print("\n=== MSG EMAILS ===")
for em in emails:
    text = (em["subject"] + " " + em["sender"]).lower()
    if "msg" in text:
        print(f"Date: {em['date']} | Sender: {em['sender']} | Subj: {em['subject']}")
        for line in em["body"].splitlines()[:10]:
            if line.strip():
                print("  ", line.strip())
        print("-" * 40)
