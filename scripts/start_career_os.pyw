# -*- coding: utf-8 -*-
"""
Windows Headless Daemon Launcher für Career OS:
Startet sowohl das lokale Career Portal (Port 8085, --no-browser) als auch
den Telegram Career Agent V3.2 ohne sichtbares Konsolenfenster mit Log-Dateien unter logs/.
"""

import os
import sys
import socket
import subprocess

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

PORTAL_SCRIPT = os.path.join(BASE_DIR, "s4hana-prep-portal", "run_portal.py")
TELEGRAM_SCRIPT = os.path.join(BASE_DIR, "telegram_career_agent.py")


def is_port_listening(port=8085):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            return s.connect_ex(("127.0.0.1", port)) == 0
    except Exception:
        return False


def _spawn(cmd, log_name):
    log_path = os.path.join(LOG_DIR, log_name)
    f = open(log_path, "a", encoding="utf-8")
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0) | getattr(subprocess, "DETACHED_PROCESS", 0)
    subprocess.Popen(
        cmd,
        cwd=BASE_DIR,
        stdout=f,
        stderr=f,
        stdin=subprocess.DEVNULL,
        creationflags=flags,
        close_fds=True,
    )


def main():
    py_exe = sys.executable
    if py_exe.lower().endswith("python.exe"):
        pyw = py_exe[:-10] + "pythonw.exe"
        if os.path.exists(pyw):
            py_exe = pyw

    if not is_port_listening(8085):
        _spawn([py_exe, PORTAL_SCRIPT, "--no-browser"], "portal.log")

    _spawn([py_exe, "-u", TELEGRAM_SCRIPT], "telegram_agent.log")


if __name__ == "__main__":
    main()
