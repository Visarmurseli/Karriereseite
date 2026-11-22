# -*- coding: utf-8 -*-
"""
Visar Murseli | Telegram Career OS Agent (V2 - Multimodal & Autonomous)
Unterstützt:
- Text-Coaching & Interview-Training
- Dokumenten- & Foto-Upload (PDFs, Notenspiegel, Zertifikate direkt in Telegram)
- Multimodale KI-Analyse über Gemini 3.5 Flash
- Automatische Ablage in der Inbox
- 1-Klick Rebuild & GitHub Pages Live-Deploy (/deploy oder /build)
"""

import os
import sys
import json
import time
import base64
import urllib.request
import urllib.parse
import subprocess
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AGENTS_MD_PATH = os.path.join(BASE_DIR, "AGENTS.md")
ENV_PATH = os.path.join(BASE_DIR, ".env")
INBOX_DIR = os.path.join(BASE_DIR, "inbox")
NOTEBOOK_NOTES_PATH = os.path.join(INBOX_DIR, "mobile_notes.md")
BUILDER_PATH = os.path.join(BASE_DIR, "build_ultimate_portal.py")

# Pfad zum GitHub-Repository für Live-Deploy
GITHUB_REPO_DIR = r"C:\Users\SHQIPTAR634\Documents\GitHub\Karriereseite"

os.makedirs(INBOX_DIR, exist_ok=True)

def load_env():
    """Liest .env Datei."""
    config = {}
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    config[k.strip()] = v.strip().strip('"').strip("'")
    return config

def get_system_prompt():
    """Lädt die wissenschaftlichen und beruflichen Leitlinien aus AGENTS.md."""
    knowledge = ""
    if os.path.exists(AGENTS_MD_PATH):
        with open(AGENTS_MD_PATH, "r", encoding="utf-8") as f:
            knowledge = f.read()
    
    return f"""Du bist der persönliche mobile Career- & Architecture-Coach von Visar Murseli im Telegram-Chat.
Du begleitest Visar bei seiner Karriere in Enterprise Architecture, SAP Consulting, IT-Strategie und IT-PMO.

Hier sind die verbindlichen Fakten und Richtlinien über Visar Murseli:
{knowledge}

DEINE AUFGABEN IM TELEGRAM-CHAT:
1. Beantworte alle Fachfragen zu Visars Masterarbeit, Modulen, Noten, SSB-Projekten (TP1-TP5) und IT-Architekturen präzise und fundiert.
2. Wenn Visar für Vorstellungsgespräche übt, trainiere mit ihm: Liefere schlagfertige Antworten, 60-Sekunden-Pitches, STAR-Stories und CV-De-Risking nach den hinterlegten Leitlinien.
3. Betone Visars wissenschaftlichen Schwerpunkt: „Kritische Erfolgsfaktoren in der Transformation großer ERP-Systeme: Eine Untersuchung am Beispiel der Plattformisierung von SAP S/4HANA“ (Note 1,0, Prof. Herzwurm). Reduziere ihn NIEMALS auf ein isoliertes Schlagwort wie Clean Core.
4. Halte Antworten prägnant, professionell und auf den Punkt für das Smartphone formatiert (Absätze, Bullet Points, Emoticons sparsam und passend).
5. Wenn Visar dir eine Notiz gibt (z.B. 'Notiere: ...'), antworte mit einer Bestätigung und fasse die Kernaussage zusammen.
"""

def call_gemini(api_key, conversation_history):
    """Ruft die offizielle Gemini API auf mit automatischem Modell-Fallback."""
    models_to_try = [
        "gemini-3.5-flash",
        "gemini-3.5-flash-lite",
        "gemini-3.8-flash",
        "gemini-3.1-flash-lite"
    ]
    last_err = None
    
    for model in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": conversation_history,
            "generationConfig": {
                "temperature": 0.4,
                "maxOutputTokens": 1400
            }
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers)
        
        try:
            with urllib.request.urlopen(req, timeout=20.0) as resp:
                res_json = json.loads(resp.read().decode("utf-8"))
                candidates = res_json.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "Keine Antwort erhalten.")
        except Exception as e:
            last_err = e
            continue
            
    raise Exception(f"Alle Gemini-Modelle fehlgeschlagen: {last_err}")

def analyze_document_with_gemini(api_key, file_path, mime_type, caption=""):
    """Analysiert ein hochgeladenes Dokument (PDF, Bild, etc.) multimodal mit Gemini 3.5 Flash."""
    with open(file_path, "rb") as f:
        file_bytes = f.read()
    b64_data = base64.b64encode(file_bytes).decode("utf-8")
    
    prompt = f"""Du analysierst ein offizielles Dokument für Visar Murselis Career OS & Enterprise Knowledge Hub.
Benutzer-Kommentar / Kontext: {caption or 'Kein Kommentar angegeben'}

AUFGABE:
1. Identifiziere den Dokumententyp (z. B. Bachelor-Zeugnis, Modulübersicht, Arbeitszeugnis, Zertifikat, etc.).
2. Extrahiere alle relevanten Fakten:
   - Vollständige Modulbezeichnungen, ECTS-Punkte, Noten
   - Ausstellende Institution, Datum, Prüfer
   - Schlüsselkompetenzen und erlernte Technologien
3. Fasse kurz zusammen, in welches Modul der Webapp diese Information gehört (z.B. thesis.py für Bachelor-Curriculum, cv_defense.py für Zertifikate).
4. Formatiere die Antwort übersichtlich mit Aufzählungspunkten für Telegram.
"""
    
    models = ["gemini-3.5-flash", "gemini-3.8-flash", "gemini-3.5-flash-lite"]
    last_err = None
    
    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        payload = {
            "contents": [{
                "parts": [
                    {"inlineData": {"mimeType": mime_type, "data": b64_data}},
                    {"text": prompt}
                ]
            }],
            "generationConfig": {"temperature": 0.2, "maxOutputTokens": 1800}
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=30.0) as resp:
                res_json = json.loads(resp.read().decode("utf-8"))
                candidates = res_json.get("candidates", [])
                if candidates:
                    return candidates[0]["content"]["parts"][0]["text"]
        except Exception as e:
            last_err = e
            continue
            
    return f"Fehler bei der Dokumentenanalyse: {last_err}"

def telegram_api(bot_token, method, params=None):
    """Führt einen Request gegen die Telegram Bot API aus."""
    url = f"https://api.telegram.org/bot{bot_token}/{method}"
    if params:
        data = urllib.parse.urlencode(params).encode("utf-8")
        req = urllib.request.Request(url, data=data)
    else:
        req = urllib.request.Request(url)
        
    try:
        with urllib.request.urlopen(req, timeout=35.0) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"[!] Telegram API Fehler ({method}): {e}", flush=True)
        return None

def send_message(bot_token, chat_id, text):
    """Sendet eine Nachricht an Telegram (mit Fallback bei Markdown-Konflikten)."""
    # Zuerst als Markdown versuchen
    res = telegram_api(bot_token, "sendMessage", {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    })
    # Falls Sonderzeichen den Markdown-Parser stören, als Plaintext senden
    if not res or not res.get("ok"):
        telegram_api(bot_token, "sendMessage", {
            "chat_id": chat_id,
            "text": text
        })

def download_telegram_file(bot_token, file_id, dest_path):
    """Lädt eine von Telegram gesendete Datei herunter."""
    file_info = telegram_api(bot_token, "getFile", {"file_id": file_id})
    if file_info and file_info.get("ok"):
        file_path = file_info["result"]["file_path"]
        download_url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
        try:
            with urllib.request.urlopen(download_url, timeout=30.0) as resp:
                with open(dest_path, "wb") as f:
                    f.write(resp.read())
            return True
        except Exception as e:
            print(f"[!] Fehler beim Dateidownload: {e}", flush=True)
            return False
    return False

def deploy_to_github():
    """Kompiliert das Webportal, synchronisiert es mit dem GitHub-Repo und pusht zu GitHub Pages."""
    try:
        # 1. Lokal kompilieren
        res_build = subprocess.run([sys.executable, BUILDER_PATH], capture_output=True, text=True)
        if res_build.returncode != 0:
            return False, f"Fehler beim lokalen Build: {res_build.stderr}"

        # 2. Falls GitHub-Verzeichnis existiert, Dateien synchronisieren und pushen
        if os.path.exists(GITHUB_REPO_DIR):
            # Kopiere kompilierte index.html
            src_index = os.path.join(BASE_DIR, "s4hana-prep-portal", "index.html")
            dst_index = os.path.join(GITHUB_REPO_DIR, "index.html")
            shutil.copy2(src_index, dst_index)

            # Git commit & push
            subprocess.run(["git", "-C", GITHUB_REPO_DIR, "add", "."], capture_output=True)
            subprocess.run(["git", "-C", GITHUB_REPO_DIR, "commit", "-m", "Automated update via Telegram Career Agent"], capture_output=True)
            push_res = subprocess.run(["git", "-C", GITHUB_REPO_DIR, "push", "origin", "main"], capture_output=True, text=True)
            
            return True, "Webapp erfolgreich neu gebaut und live auf GitHub Pages synchronisiert!"
        
        return True, "Webapp erfolgreich lokal neu gebaut."
    except Exception as e:
        return False, str(e)

def save_note(text):
    """Speichert eine Notiz in der Inbox."""
    today = time.strftime("%d.%m.%Y %H:%M")
    with open(NOTEBOOK_NOTES_PATH, "a", encoding="utf-8") as f:
        f.write(f"\n### Mobile Notiz ({today})\n{text}\n")

def run():
    print("=" * 60, flush=True)
    print("  Visar Murseli | Telegram Career OS Agent V2 (Multimodal)", flush=True)
    print("=" * 60, flush=True)
    
    env = load_env()
    bot_token = env.get("TELEGRAM_BOT_TOKEN") or os.environ.get("TELEGRAM_BOT_TOKEN")
    gemini_key = env.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
    
    if not bot_token or not gemini_key:
        print("[!] Konfiguration unvollständig in .env!", flush=True)
        return

    bot_info = telegram_api(bot_token, "getMe")
    if not bot_info or not bot_info.get("ok"):
        print("[!] Ungültiger Telegram Bot Token!", flush=True)
        return

    bot_name = bot_info["result"]["first_name"]
    bot_user = bot_info["result"]["username"]
    print(f"[✓] Verbunden mit Telegram Bot: @{bot_user} ({bot_name})", flush=True)
    print("[*] Multimodaler Agent lauscht auf Nachrichten & Datei-Uploads...", flush=True)
    print("=" * 60, flush=True)

    system_prompt = get_system_prompt()
    conversation_history = [
        {"role": "user", "parts": [{"text": system_prompt}]},
        {"role": "model", "parts": [{"text": "Verstanden. Ich bin bereit als dein persönlicher Career- & Architecture-Coach für Visar Murseli."}]}
    ]

    offset = 0

    while True:
        try:
            updates = telegram_api(bot_token, "getUpdates", {"offset": offset, "timeout": 25})
            if updates and updates.get("ok"):
                for update in updates.get("result", []):
                    offset = update["update_id"] + 1
                    msg = update.get("message")
                    if not msg:
                        continue

                    chat_id = msg["chat"]["id"]
                    sender = msg.get("from", {}).get("first_name", "Visar")
                    caption = msg.get("caption", "").strip()

                    # ================= FALL 1: DOKUMENT-UPLOAD (PDF, DOCX, BILD, etc.) =================
                    if "document" in msg:
                        doc = msg["document"]
                        file_id = doc["file_id"]
                        file_name = doc.get("file_name", f"document_{int(time.time())}.pdf")
                        mime_type = doc.get("mime_type", "application/pdf")
                        dest_path = os.path.join(INBOX_DIR, file_name)

                        print(f"\n[📥] Dokument empfangen von {sender}: {file_name} ({mime_type})", flush=True)
                        send_message(bot_token, chat_id, f"📥 *Dokument empfangen:* `{file_name}`\n⏳ Ich lade die Datei in deine `inbox/` und starte die multimodale KI-Analyse mit Gemini...")

                        if download_telegram_file(bot_token, file_id, dest_path):
                            # Multimodale Analyse starten
                            analysis = analyze_document_with_gemini(gemini_key, dest_path, mime_type, caption)
                            
                            # Notiz in mobile_notes.md vermerken
                            save_note(f"Dokument hochgeladen: {file_name}\nAnalyse:\n{analysis}")

                            response_text = (
                                f"✅ *Dokument erfolgreich verarbeitet & in inbox/ gesichert!*\n\n"
                                f"📋 *Analyse-Ergebnis:*\n{analysis}\n\n"
                                f"💡 *Nächster Schritt:* Du kannst mich bitten, die Daten einzupflegen oder sende `/build`, um das Webportal live zu aktualisieren."
                            )
                            send_message(bot_token, chat_id, response_text)
                        else:
                            send_message(bot_token, chat_id, f"❌ Fehler beim Herunterladen der Datei `{file_name}`.")
                        continue

                    # ================= FALL 2: FOTO-UPLOAD (Screenshot, Foto von Notenbescheid) =================
                    elif "photo" in msg:
                        photos = msg["photo"]
                        best_photo = photos[-1] # Größte Auflösung
                        file_id = best_photo["file_id"]
                        file_name = f"photo_{int(time.time())}.jpg"
                        dest_path = os.path.join(INBOX_DIR, file_name)

                        print(f"\n[📷] Foto empfangen von {sender}: {file_name}", flush=True)
                        send_message(bot_token, chat_id, f"📷 *Foto empfangen.* Ich analysiere das Bild mit Gemini Vision...")

                        if download_telegram_file(bot_token, file_id, dest_path):
                            analysis = analyze_document_with_gemini(gemini_key, dest_path, "image/jpeg", caption)
                            save_note(f"Foto hochgeladen: {file_name}\nAnalyse:\n{analysis}")
                            
                            send_message(bot_token, chat_id, f"✅ *Bild-Analyse abgeschlossen:*\n\n{analysis}")
                        else:
                            send_message(bot_token, chat_id, "❌ Fehler beim Herunterladen des Bildes.")
                        continue

                    # ================= FALL 3: TEXT-NACHRICHT =================
                    if "text" in msg:
                        user_text = msg["text"].strip()
                        print(f"\n[+] Nachricht von {sender}: {user_text}", flush=True)

                        # Befehl: Hilfe
                        if user_text.lower() in ["/start", "/hilfe", "help"]:
                            welcome_msg = (
                                f"Hallo {sender}! 🚀\n\n"
                                "Ich bin dein persönlicher **Career OS & Architecture Agent**.\n\n"
                                "Hier ist alles, was du mit mir machen kannst:\n\n"
                                "📤 *Dateien & Dokumente hochladen:*\n"
                                "• Sende mir einfach ein **PDF** (z. B. Bachelor-Zeugnis, Modulübersicht) oder ein **Foto/Screenshot** direkt im Chat.\n"
                                "• Ich lade die Datei auf deinen Laptop in `inbox/`, analysiere sie mit Gemini und bereite die Einbindung in deine Webapp vor.\n\n"
                                "🎙️ *Interview- & Fach-Coaching:*\n"
                                "• *„Trainiere mit mir den 60-Sekunden Pitch“*\n"
                                "• *„Erkläre mir mein Platform Excellence Framework“*\n"
                                "• *„Welche Noten habe ich in Software-Architektur und ASE?“*\n\n"
                                "📝 *Mobiles Notizbuch (Second Brain):*\n"
                                "• *„Notiere: Gespräch mit Porsche war positiv, Fokus BTP“*\n\n"
                                "🚀 *Webportal live aktualisieren:*\n"
                                "• *„/deploy“* oder *„/build“* (kompiliert die Webapp und aktualisiert deine Live-Seite auf GitHub Pages!)\n"
                            )
                            send_message(bot_token, chat_id, welcome_msg)
                            continue

                        # Befehl: Build & Live-Deploy auf GitHub Pages
                        elif user_text.lower() in ["/build", "/deploy", "deploy", "build", "portal neu bauen"]:
                            send_message(bot_token, chat_id, "⏳ Kompiliere Webportal auf dem Laptop und synchronisiere mit GitHub Pages...")
                            ok, status_msg = deploy_to_github()
                            if ok:
                                reply = (
                                    "✅ *Webportal erfolgreich neu gebaut & live geschaltet!*\n\n"
                                    "👉 *Live auf deinem iPhone ansehen:*\n"
                                    "https://visarmurseli.github.io/Karriereseite/"
                                )
                                send_message(bot_token, chat_id, reply)
                            else:
                                send_message(bot_token, chat_id, f"❌ Fehler beim Rebuild: {status_msg}")
                            continue

                        # Befehl: Notiz speichern
                        elif user_text.lower().startswith("notiere:") or user_text.lower().startswith("notiz:"):
                            note_content = user_text.split(":", 1)[1].strip()
                            save_note(note_content)
                            send_message(bot_token, chat_id, f"📝 *Notiz erfolgreich in deiner Inbox gespeichert:*\n\n_{note_content}_")
                            continue

                        # Reguläre KI-Anfrage
                        conversation_history.append({"role": "user", "parts": [{"text": user_text}]})
                        
                        try:
                            reply = call_gemini(gemini_key, conversation_history)
                            conversation_history.append({"role": "model", "parts": [{"text": reply}]})
                            
                            if len(conversation_history) > 22:
                                conversation_history = [conversation_history[0], conversation_history[1]] + conversation_history[-18:]
                                
                            send_message(bot_token, chat_id, reply)
                        except Exception as e:
                            print(f"[!] Fehler bei Gemini-Aufruf: {e}", flush=True)
                            send_message(bot_token, chat_id, f"⚠️ Fehler bei der Antwortgenerierung: {e}")

        except KeyboardInterrupt:
            print("\n[*] Telegram Agent wird beendet...", flush=True)
            break
        except Exception as e:
            print(f"[!] Unerwarteter Fehler im Loop: {e}", flush=True)
            time.sleep(2)

if __name__ == "__main__":
    run()
