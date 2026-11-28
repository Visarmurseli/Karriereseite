import json
import re

with open(r"c:\Users\SHQIPTAR634\Desktop\SSB Dateien\00_Aktuelle_Bewerbungsunterlagen\deep_emails_dump.json", "r", encoding="utf-8") as f:
    emails = json.load(f)

targets = [
    ("Schwarz / Lidl", ["schwarz", "lidl", "kadrija", "kelsch", "hertel"]),
    ("SSB AG", ["ssb-ag", "daniela.trotus", "laura.bulke", "solution architect"]),
    ("Coop", ["coop", "coopgroup"]),
    ("Computacenter", ["computacenter", "paula weber", "mb_hr_os"]),
    ("Deutsche Bahn", ["deutschebahn", "dbz-bewerbung", "alomerovic"]),
    ("EY", ["ey.com", "talentattraction", "zukowska", "iwaniak"]),
    ("Hengstenberg", ["hengstenberg", "deger"]),
    ("LTI-Metalltechnik", ["lti-metalltechnik", "lti"]),
    ("adesso", ["adesso"]),
    ("BITBW", ["bitbw", "julia.rupp"]),
    ("HdM Stuttgart", ["hdm-stuttgart", "zobel", "seiler"]),
    ("THW / BVA", ["bva.bund.de", "thw-2026"]),
    ("appliedAI", ["appliedai"]),
    ("MHP", ["mhp.com"]),
    ("Kärcher", ["karcher.com", "kärcher"]),
    ("Cpro", ["cpro"]),
    ("x1F", ["x1f"]),
    ("Communardo", ["communardo"]),
    ("HORBACH", ["horbach"]),
    ("KVJS", ["kvjs"]),
]

for label, keywords in targets:
    print(f"\n==================== {label} ====================")
    matched = []
    for em in emails:
        text = (em["subject"] + " " + em["sender"] + " " + em["body"][:1000]).lower()
        if any(k in text for k in keywords):
            matched.append(em)
    print(f"Matched {len(matched)} emails.")
    for em in matched[:5]:
        print(f"Date: {em['date']} | Sender: {em['sender'][:40]} | Subj: {em['subject'][:70]}")
        # Print clean body lines
        lines = [l.strip() for l in em["body"].splitlines() if l.strip() and not l.strip().startswith("<") and len(l.strip()) > 10]
        for l in lines[:6]:
            print("   ", l[:120])
        print("-" * 30)
