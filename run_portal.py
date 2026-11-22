# -*- coding: utf-8 -*-
"""
SAP4SSB S/4HANA Transformation & Career Intelligence Portal Server
Entwickelt für Visar Murseli | M.Sc. Wirtschaftsinformatik
Multi-Threaded HTTP Server mit nativer Windows Browser-Integration
"""

import http.server
import socketserver
import webbrowser
import os
import sys
import socket
import subprocess
import urllib.request

PORT = 8085
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Falls unter pythonw.exe gestartet (ohne Konsole), stdout/stderr sicher abfangen
if sys.stdout is None:
    try:
        sys.stdout = open(os.devnull, "w")
    except Exception:
        pass

if sys.stderr is None:
    try:
        sys.stderr = open(os.devnull, "w")
    except Exception:
        pass

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        try:
            if sys.stderr is not None:
                sys.stderr.write("%s - - [%s] %s\n" %
                                 (self.address_string(),
                                  self.log_date_time_string(),
                                  format % args))
        except Exception:
            pass

class ThreadingServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

def is_server_alive(port):
    """Prüft per echtem HTTP-Request mit Timeout, ob der Server auf dem Port antwortet."""
    try:
        req = urllib.request.Request(f"http://127.0.0.1:{port}/index.html", headers={"User-Agent": "PortalHealthCheck"})
        with urllib.request.urlopen(req, timeout=0.8) as resp:
            return resp.status == 200
    except Exception:
        return False

def open_portal(url):
    """
    Öffnet das Portal direkt und zuverlässig im Standard-Browser des Nutzers.
    Nutzt nacheinander os.startfile, webbrowser und cmd start.
    """
    try:
        os.startfile(url)
        return True
    except Exception:
        pass

    try:
        webbrowser.open(url)
        return True
    except Exception:
        pass

    try:
        subprocess.Popen(f'explorer "{url}"', shell=True)
        return True
    except Exception:
        return False

def run():
    os.chdir(DIRECTORY)
    url = f"http://localhost:{PORT}/index.html"
    
    # 1. Prüfen, ob der Server bereits aktiv antwortet
    if is_server_alive(PORT):
        print(f"[*] Server läuft bereits aktiv auf Port {PORT}.")
        print(f"[*] Öffne Portal im Browser: {url}")
        open_portal(url)
        return

    # 2. Server starten (Multi-Threaded)
    httpd = None
    target_port = PORT
    
    for p in [PORT, 8086, 8087, 8088]:
        try:
            httpd = ThreadingServer(("127.0.0.1", p), Handler)
            target_port = p
            break
        except (OSError, PermissionError):
            continue
            
    if httpd is None:
        print("[!] Alle Ports von 8085 bis 8088 sind belegt.")
        open_portal(f"http://localhost:{PORT}/index.html")
        return

    url = f"http://localhost:{target_port}/index.html"
    print("=" * 60)
    print("  SAP4SSB S/4HANA Transformation & Career Intelligence Portal")
    print("  Entwickelt für Visar Murseli | M.Sc. Wirtschaftsinformatik")
    print("=" * 60)
    print(f"[*] Multi-Threaded Server läuft unter: {url}")
    print("=" * 60)

    # Browser öffnen
    open_portal(url)

    # Server im Loop ausführen
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Server wird beendet...")
    finally:
        try:
            httpd.server_close()
        except Exception:
            pass
        print("[*] Server sauber geschlossen.")

if __name__ == "__main__":
    run()
