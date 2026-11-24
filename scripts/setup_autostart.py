# -*- coding: utf-8 -*-
"""
Verwaltet den benutzerspezifischen Windows-Autostart für Career OS
(%APPDATA%/Microsoft/Windows/Start Menu/Programs/Startup/CareerOS_Autostart.vbs).
"""

import os
import sys
import argparse

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LAUNCHER_PYW = os.path.join(BASE_DIR, "scripts", "start_career_os.pyw")
STARTUP_DIR = os.path.join(os.environ.get("APPDATA", ""), r"Microsoft\Windows\Start Menu\Programs\Startup")
VBS_PATH = os.path.join(STARTUP_DIR, "CareerOS_Autostart.vbs")


def get_pythonw():
    py_exe = sys.executable
    if py_exe.lower().endswith("python.exe"):
        pyw = py_exe[:-10] + "pythonw.exe"
        if os.path.exists(pyw):
            return pyw
    return py_exe


def install():
    os.makedirs(STARTUP_DIR, exist_ok=True)
    pyw = get_pythonw()
    vbs = f'Set WshShell = CreateObject("WScript.Shell")\nWshShell.Run """{pyw}"" ""{LAUNCHER_PYW}""", 0, False\n'
    with open(VBS_PATH, "w", encoding="utf-8") as f:
        f.write(vbs)
    print(f"[OK] Windows-Autostart installiert: {VBS_PATH}")


def uninstall():
    if os.path.exists(VBS_PATH):
        os.remove(VBS_PATH)
        print(f"[OK] Windows-Autostart entfernt: {VBS_PATH}")
    else:
        print("[*] Kein Autostart-Eintrag vorhanden.")


def status():
    exists = os.path.exists(VBS_PATH)
    print(f"Autostart aktiv: {exists} | Pfad: {VBS_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Career OS Windows Startup Manager")
    parser.add_argument("--install", action="store_true", help="Installiert Startup VBS-Launcher")
    parser.add_argument("--uninstall", action="store_true", help="Entfernt Startup VBS-Launcher")
    parser.add_argument("--status", action="store_true", help="Zeigt Startup-Status")
    args = parser.parse_args()
    if args.install:
        install()
    elif args.uninstall:
        uninstall()
    else:
        status()
