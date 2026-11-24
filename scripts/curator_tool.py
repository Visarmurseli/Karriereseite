# -*- coding: utf-8 -*-
"""
CareerOS Curator CLI Tool
Hilfswerkzeug für Visar Murseli & den Antigravity Curator Agenten.
Prüft die Inbox, den Serverstatus und führt bei Bedarf den Rebuild aus.
"""

import os
import sys
import urllib.request
import subprocess

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INBOX_DIR = os.path.join(BASE_DIR, "inbox")
PORTAL_DIR = os.path.join(BASE_DIR, "s4hana-prep-portal")
BUILDER_SCRIPT = os.path.join(BASE_DIR, "build_ultimate_portal.py")

def check_inbox():
    print("=" * 60)
    print("  CareerOS Curator – Inbox Status")
    print("=" * 60)
    if not os.path.exists(INBOX_DIR):
        os.makedirs(INBOX_DIR, exist_ok=True)
        print("[!] Inbox-Ordner wurde neu erstellt.")
        return []

    files = [f for f in os.listdir(INBOX_DIR) if f != "README.md" and not f.startswith(".")]
    if not files:
        print("[✓] Inbox ist leer. Keine ausstehenden Dokumente.")
    else:
        print(f"[*] {len(files)} Dokument(e) warten auf Verarbeitung:")
        for idx, f in enumerate(files, 1):
            fpath = os.path.join(INBOX_DIR, f)
            size_kb = os.path.getsize(fpath) / 1024
            print(f"    {idx}. {f} ({size_kb:.1f} KB)")
    return files

def check_server():
    print("\n" + "=" * 60)
    print("  Portal Live-Status")
    print("=" * 60)
    try:
        req = urllib.request.Request("http://127.0.0.1:8085/index.html")
        with urllib.request.urlopen(req, timeout=1.0) as resp:
            if resp.status == 200:
                print("[✓] Server läuft aktiv auf: http://localhost:8085/index.html (Status: 200 OK)")
                return True
    except Exception:
        pass
    print("[!] Server antwortet nicht auf Port 8085. Starte über run_portal.py oder Portal_Starten.bat.")
    return False

def rebuild():
    print("\n" + "=" * 60)
    print("  Kompiliere Webapp (build_ultimate_portal.py)")
    print("=" * 60)
    res = subprocess.run([sys.executable, BUILDER_SCRIPT], capture_output=True, text=True)
    print(res.stdout)
    if res.returncode == 0:
        print("[✓] Rebuild erfolgreich abgeschlossen!")
    else:
        print("[!] Rebuild fehlgeschlagen:", res.stderr)

if __name__ == "__main__":
    check_inbox()
    check_server()
    if len(sys.argv) > 1 and sys.argv[1] == "--build":
        rebuild()
