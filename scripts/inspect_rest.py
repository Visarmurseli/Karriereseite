import json

with open(r"c:\Users\SHQIPTAR634\Desktop\SSB Dateien\00_Aktuelle_Bewerbungsunterlagen\deep_emails_dump.json", "r", encoding="utf-8") as f:
    emails = json.load(f)

for term in ['appliedai', 'karcher', 'mhp', 'bitbw', 'hdm', 'thw', 'drv', 'stuttgart']:
    print(f"=== {term} ===")
    for em in emails:
        if term in (em['subject'] + ' ' + em['sender']).lower():
            print(f"{em['date'][:16]} | {em['subject'][:70]}")
            for l in em['body'].splitlines()[:5]:
                if l.strip() and not l.strip().startswith('<'):
                    print("  ", l.strip()[:100])
            print('-'*20)
