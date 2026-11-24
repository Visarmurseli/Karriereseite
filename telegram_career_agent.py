# -*- coding: utf-8 -*-
"""
Visar Murseli | Telegram Career OS Agent (V3 - Local Hybrid RAG, Pipeline & Obsidian Sync)
Unterstützt:
- Echtzeit-RAG-Retrieval über 137.000+ Chunks (Obsidian Second Brain & 4.980 Originaldokumente)
- Direktabruf der Live-Bewerbungspipeline (/pipeline)
- Volltextsuche (/rag <Suchbegriff>)
- Dokumenten- & Foto-Upload (multimodale Analyse)
- Notizen direkt in Obsidian Vault Inbox (/notiz oder 'Notiere: ...')
- Sicheres 1-Klick Rebuild & GitHub Pages Showcase Deploy (/deploy)
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
from datetime import datetime

for _stream in (sys.stdout, sys.stderr):
    if _stream is not None and hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

try:
    from local_rag_engine import search as rag_search, get_stats as rag_stats
    RAG_AVAILABLE = True
except Exception:
    RAG_AVAILABLE = False

try:
    import openpyxl
    OPENPYXL_AVAILABLE = True
except Exception:
    OPENPYXL_AVAILABLE = False

AGENTS_MD_PATH = os.path.join(BASE_DIR, "AGENTS.md")
ENV_PATH = os.path.join(BASE_DIR, ".env")
INBOX_DIR = os.path.join(BASE_DIR, "inbox")
NOTEBOOK_NOTES_PATH = os.path.join(INBOX_DIR, "mobile_notes.md")
OBSIDIAN_MOBILE_NOTE = r"C:\Users\SHQIPTAR634\Documents\Obsidian Vault\00_Inbox\Mobile_Notizen.md"
EXCEL_PIPELINE_PATH = os.path.join(BASE_DIR, "00_Aktuelle_Bewerbungsunterlagen", "Bewerbungsverlauf.xlsx")
BUILDER_PATH = os.path.join(BASE_DIR, "build_ultimate_portal.py")

GITHUB_REPO_DIR = r"C:\Users\SHQIPTAR634\Documents\GitHub\Karriereseite"
GEMINI_MODELS = ["gemini-3-flash-preview", "gemini-3.1-flash-lite", "gemini-3.1-pro-preview"]

os.makedirs(INBOX_DIR, exist_ok=True)


def load_env():
    config = {}
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    config[k.strip()] = v.strip().strip('"').strip("'")
    return config


def get_pipeline_summary(max_items=12):
    """Liest laufende Interviews und Top-Bewerbungen direkt aus Bewerbungsverlauf.xlsx."""
    if not OPENPYXL_AVAILABLE or not os.path.exists(EXCEL_PIPELINE_PATH):
        return "Bewerbungspipeline aktuell nicht ladbar."
    try:
        wb = openpyxl.load_workbook(EXCEL_PIPELINE_PATH, data_only=True)
        ws = wb["Bewerbungsverlauf"]
        interviews = []
        active = []
        for r in range(2, ws.max_row + 1):
            comp = str(ws.cell(r, 1).value or "").strip()
            role = str(ws.cell(r, 2).value or "").strip()
            g1 = str(ws.cell(r, 5).value or "-").strip()
            g2 = str(ws.cell(r, 6).value or "-").strip()
            status = str(ws.cell(r, 7).value or "").strip()
            if not comp or comp == "Terminerinnerung":
                continue
            line = f"• {comp} ({role[:48]}): {status}"
            if any(k in status for k in ["⭐", "🚀", "Gespräch", "Interview", "Einladung"]) and "Absage" not in status:
                interviews.append(f"{line} [Termine: G1={g1}, G2={g2}]")
            elif "Absage" not in status:
                active.append(line)
        summary = "AKTIVE INTERVIEWS & TOP-RUNDEN:\n" + ("\n".join(interviews) or "• Keine")
        summary += f"\n\nWEITERE OFFENE BEWERBUNGEN ({len(active)} aktiv, Auszug):\n" + "\n".join(active[:max_items])
        return summary
    except Exception as e:
        return f"Pipeline-Fehler: {e}"


def get_system_prompt():
    knowledge = ""
    if os.path.exists(AGENTS_MD_PATH):
        with open(AGENTS_MD_PATH, "r", encoding="utf-8") as f:
            knowledge = f.read()

    return f"""Du bist der persönliche mobile Career- & Architecture-Coach von Visar Murseli im Telegram-Chat.
Du hast Zugriff auf Visars gesamtes Second Brain (Local RAG über 4.980 Dokumente) und seine Live-Bewerbungspipeline.

Verbindliche Fakten aus AGENTS.md:
{knowledge}

REGELN FÜR DEINE ANTWORTEN:
1. Beantworte Fachfragen (SAP S/4HANA, HCM IAM, BTP, SSB-Lösungsdesign, Masterarbeit 1,0, Bachelorarbeit 1,7, 300 ECTS, DC1 ITIL 4) präzise auf Basis der mitgelieferten RAG-Treffer und nenne nach Möglichkeit konkrete Quelldokumente.
2. Betone den wissenschaftlichen Fokus der Masterarbeit korrekt: Transformation großer ERP-Systeme & Plattformisierung von SAP S/4HANA (niemals auf ein einziges Schlagwort reduzieren).
3. Formatiere klar, kompakt und smartphone-freundlich für Telegram.
"""


def build_rag_context(query, top_k=5):
    """Ruft passende Text-Chunks aus der lokalen SQLite FTS5 RAG-Datenbank ab."""
    if not RAG_AVAILABLE:
        return ""
    hits = rag_search(query, top_k=top_k)
    if not hits:
        return ""
    blocks = []
    for i, h in enumerate(hits, 1):
        blocks.append(f"[RAG-Quelle {i}: {h['file']} | Abschnitt: {h['section']}]\n{h['content'][:1600]}")
    return "\n\n---\n\n".join(blocks)


def call_gemini(api_key, conversation_history):
    """Ruft verifizierte aktive Gemini-Modelle ohne lange Timeouts auf."""
    last_err = None
    for model in GEMINI_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        payload = {
            "contents": conversation_history,
            "generationConfig": {
                "temperature": 0.35,
                "maxOutputTokens": 1500
            }
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=22.0) as resp:
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
    with open(file_path, "rb") as f:
        b64_data = base64.b64encode(f.read()).decode("utf-8")

    prompt = f"""Analysiere dieses Dokument für Visar Murselis Career OS & Obsidian Second Brain.
Kontext: {caption or 'Kein Kommentar'}
1. Dokumententyp bestimmen
2. Kernfakten (Module, Noten, Fristen, Gesprächspartner, Anforderungen) strukturiert extrahieren
3. Konkrete Empfehlung, ob es in Obsidian, Notion oder Webapp abgelegt werden soll."""

    last_err = None
    for model in GEMINI_MODELS:
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
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
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
    # Split long messages cleanly for Telegram 4096-char limit
    for chunk_start in range(0, len(text), 3900):
        chunk = text[chunk_start:chunk_start + 3900]
        res = telegram_api(bot_token, "sendMessage", {
            "chat_id": chat_id,
            "text": chunk,
            "parse_mode": "Markdown"
        })
        if not res or not res.get("ok"):
            telegram_api(bot_token, "sendMessage", {
                "chat_id": chat_id,
                "text": chunk
            })


def download_telegram_file(bot_token, file_id, dest_path):
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
    """Kompiliert Lokal + Öffentliche Showcase-Edition und pusht NUR die sichere Public-Edition nach GitHub."""
    try:
        res_build = subprocess.run([sys.executable, BUILDER_PATH], capture_output=True, text=True)
        if res_build.returncode != 0:
            return False, f"Fehler beim lokalen Build: {res_build.stderr}"

        if os.path.exists(GITHUB_REPO_DIR):
            src_public = os.path.join(BASE_DIR, "s4hana-prep-portal", "public_index.html")
            if not os.path.exists(src_public):
                return False, "public_index.html wurde nicht generiert!"
            dst_index = os.path.join(GITHUB_REPO_DIR, "index.html")
            shutil.copy2(src_public, dst_index)

            subprocess.run(["git", "-C", GITHUB_REPO_DIR, "add", "index.html"], capture_output=True)
            subprocess.run(["git", "-C", GITHUB_REPO_DIR, "commit", "-m", "chore(portal): automated public showcase deploy via Telegram Agent"], capture_output=True)
            subprocess.run(["git", "-C", GITHUB_REPO_DIR, "push", "origin", "main"], capture_output=True, text=True)
            return True, "Lokales Cockpit & öffentliche Showcase-Seite (ohne private Interview-Taktiken) neu gebaut und gepusht!"

        return True, "Webapp erfolgreich lokal neu gebaut."
    except Exception as e:
        return False, str(e)


def save_note(text):
    """Speichert eine Notiz sowohl in inbox/mobile_notes.md als auch direkt in Obsidian 00_Inbox/Mobile_Notizen.md."""
    today_hr = time.strftime("%d.%m.%Y %H:%M")
    today_iso = datetime.now().strftime("%Y-%m-%d")

    with open(NOTEBOOK_NOTES_PATH, "a", encoding="utf-8") as f:
        f.write(f"\n### Mobile Notiz ({today_hr})\n{text}\n")

    os.makedirs(os.path.dirname(OBSIDIAN_MOBILE_NOTE), exist_ok=True)
    if not os.path.exists(OBSIDIAN_MOBILE_NOTE):
        header = f"""---
id: mobile-notizen-telegram-inbox
title: "Mobile Notizen (Telegram Career Agent)"
type: concept
domain: second-brain
status: active
summary: "Mobile Sprach- und Textnotizen aus dem Telegram Career OS Agenten direkt im Obsidian Vault."
tags:
  - telegram_sync
  - second_brain
  - inbox
last_updated: "{today_iso}"
---

# 📱 Mobile Notizen (Telegram Sync)

> [!SUMMARY] **Direkte Erfassung von unterwegs**
> Verknüpft mit [[00_INDEX|🧠 Master Index]] • [[00_Bewerbungsmanagement_Cockpit|📊 Bewerbungs-Cockpit]].

"""
        with open(OBSIDIAN_MOBILE_NOTE, "w", encoding="utf-8") as f:
            f.write(header)

    with open(OBSIDIAN_MOBILE_NOTE, "a", encoding="utf-8") as f:
        f.write(f"\n## 📝 Notiz ({today_hr})\n\n{text.strip()}\n\n---\n")


def run():
    print("=" * 60, flush=True)
    print("  Visar Murseli | Telegram Career OS Agent V3 (RAG & Pipeline)", flush=True)
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

    bot_user = bot_info["result"]["username"]
    r_stats = rag_stats() if RAG_AVAILABLE else {"exists": False}
    print(f"[✓] Verbunden mit Telegram Bot: @{bot_user}", flush=True)
    print(f"[✓] Local RAG: {r_stats}", flush=True)
    print("=" * 60, flush=True)

    system_prompt = get_system_prompt()
    conversation_history = [
        {"role": "user", "parts": [{"text": system_prompt}]},
        {"role": "model", "parts": [{"text": "Verstanden. Ich bin bereit mit direktem Zugriff auf dein Obsidian RAG Second Brain und deine Bewerbungspipeline."}]}
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

                    if "document" in msg:
                        doc = msg["document"]
                        file_id = doc["file_id"]
                        file_name = doc.get("file_name", f"document_{int(time.time())}.pdf")
                        mime_type = doc.get("mime_type", "application/pdf")
                        dest_path = os.path.join(INBOX_DIR, file_name)
                        send_message(bot_token, chat_id, f"📥 *Dokument empfangen:* `{file_name}`\n⏳ Analysiere mit Gemini...")
                        if download_telegram_file(bot_token, file_id, dest_path):
                            analysis = analyze_document_with_gemini(gemini_key, dest_path, mime_type, caption)
                            save_note(f"Dokument hochgeladen: {file_name}\n\n{analysis}")
                            send_message(bot_token, chat_id, f"✅ *Dokument gesichert & in Obsidian Inbox vermerkt:*\n\n{analysis}")
                        else:
                            send_message(bot_token, chat_id, f"❌ Download fehlgeschlagen für `{file_name}`.")
                        continue

                    elif "photo" in msg:
                        best_photo = msg["photo"][-1]
                        file_name = f"photo_{int(time.time())}.jpg"
                        dest_path = os.path.join(INBOX_DIR, file_name)
                        send_message(bot_token, chat_id, "📷 *Foto empfangen.* Analysiere mit Gemini Vision...")
                        if download_telegram_file(bot_token, best_photo["file_id"], dest_path):
                            analysis = analyze_document_with_gemini(gemini_key, dest_path, "image/jpeg", caption)
                            save_note(f"Foto hochgeladen: {file_name}\n\n{analysis}")
                            send_message(bot_token, chat_id, f"✅ *Bild-Analyse in Obsidian Inbox gespeichert:*\n\n{analysis}")
                        else:
                            send_message(bot_token, chat_id, "❌ Fehler beim Herunterladen des Bildes.")
                        continue

                    if "text" in msg:
                        user_text = msg["text"].strip()

                        if user_text.lower() in ["/start", "/hilfe", "help"]:
                            welcome = (
                                f"Hallo {sender}! 🚀 *Career OS Agent V3 (RAG Connected)*\n\n"
                                "• *Freie Frage:* Durchsucht automatisch 137.000+ Chunks aus Obsidian & antwortet mit Quellen.\n"
                                "• `/rag <Begriff>` — Direkte Volltext-Treffer aus Studium, SSB & DC1\n"
                                "• `/pipeline` — Live-Bewerbungsstatus & nächste Gespräche\n"
                                "• `Notiere: <Text>` oder `/notiz <Text>` — Direkt in Obsidian `00_Inbox/Mobile_Notizen.md`\n"
                                "• `/deploy` — Lokales Portal + öffentliche Showcase-Seite sicher live aktualisieren"
                            )
                            send_message(bot_token, chat_id, welcome)
                            continue

                        elif user_text.lower() == "/pipeline":
                            send_message(bot_token, chat_id, get_pipeline_summary())
                            continue

                        elif user_text.lower().startswith("/rag "):
                            q = user_text[5:].strip()
                            hits = rag_search(q, top_k=5) if RAG_AVAILABLE else []
                            if not hits:
                                send_message(bot_token, chat_id, f"Keine RAG-Treffer für _{q}_.")
                            else:
                                out = [f"🔍 *RAG-Treffer für:* `{q}`\n"]
                                for idx, h in enumerate(hits, 1):
                                    out.append(f"*{idx}. {h['file']}* (_{h['section']}_)\n{h['snippet'][:420]}...\n")
                                send_message(bot_token, chat_id, "\n".join(out))
                            continue

                        elif user_text.lower() in ["/build", "/deploy", "deploy", "build", "portal neu bauen"]:
                            send_message(bot_token, chat_id, "⏳ Kompiliere Lokales Cockpit + Öffentliche Showcase-Edition...")
                            ok, status_msg = deploy_to_github()
                            if ok:
                                send_message(bot_token, chat_id, f"✅ {status_msg}\n👉 https://visarmurseli.github.io/Karriereseite/")
                            else:
                                send_message(bot_token, chat_id, f"❌ Fehler: {status_msg}")
                            continue

                        elif user_text.lower().startswith("notiere:") or user_text.lower().startswith("notiz:") or user_text.lower().startswith("/notiz "):
                            note_content = user_text.split(":", 1)[1].strip() if ":" in user_text else user_text[7:].strip()
                            save_note(note_content)
                            send_message(bot_token, chat_id, f"📝 *Notiz direkt in Obsidian `00_Inbox/Mobile_Notizen.md` gespeichert:*\n\n_{note_content}_")
                            continue

                        # Regular RAG-augmented AI query
                        rag_ctx = build_rag_context(user_text, top_k=5)
                        pipeline_ctx = get_pipeline_summary(max_items=6) if any(k in user_text.lower() for k in ["bewerb", "gespräch", "interview", "schwarz", "kpmg", "trumpf", "status", "termin"]) else ""
                        enriched_prompt = f"""FRAGE VON VISAR:
{user_text}

{('LIVE-BEWERBUNGSPIPELINE:' + chr(10) + pipeline_ctx + chr(10)*2) if pipeline_ctx else ''}{('RELEVANTE QUELLEN AUS OBSIDIAN SECOND BRAIN (LOCAL RAG):' + chr(10) + rag_ctx) if rag_ctx else ''}"""

                        conversation_history.append({"role": "user", "parts": [{"text": enriched_prompt}]})
                        try:
                            reply = call_gemini(gemini_key, conversation_history)
                            # Keep compact user_text in rolling history to stay lean
                            conversation_history[-1] = {"role": "user", "parts": [{"text": user_text}]}
                            conversation_history.append({"role": "model", "parts": [{"text": reply}]})
                            if len(conversation_history) > 18:
                                conversation_history = [conversation_history[0], conversation_history[1]] + conversation_history[-14:]
                            send_message(bot_token, chat_id, reply)
                        except Exception as e:
                            send_message(bot_token, chat_id, f"⚠️ Fehler bei der Antwortgenerierung: {e}")

        except KeyboardInterrupt:
            print("\n[*] Telegram Agent wird beendet...", flush=True)
            break
        except Exception as e:
            print(f"[!] Unerwarteter Fehler im Loop: {e}", flush=True)
            time.sleep(2)


if __name__ == "__main__":
    run()
