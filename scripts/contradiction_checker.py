# -*- coding: utf-8 -*-
"""
Contradiction & Sanity Checker for Visar Murseli's Personal Career OS & Second Brain
Inspired by the Andrej Karpathy LLM-Wiki Pattern:
Autonomously audits the knowledge vault for factual contradictions, outdated information,
architectural misconceptions, and reductionism against official ground-truth rules (AGENTS.md).

Author: Visar Murseli, M.Sc. | Data Science & Enterprise AI Architect
"""

import os
import sys
import re
import json
import argparse
from datetime import datetime
from typing import List, Dict, Any, Optional

# Base directories
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
VAULT_DIR = r"C:\Users\SHQIPTAR634\Documents\Obsidian Vault"
AGENTS_MD_PATH = os.path.join(BASE_DIR, "AGENTS.md")
ENV_PATH = os.path.join(BASE_DIR, ".env")
AUDIT_REPORT_PATH = os.path.join(VAULT_DIR, "01_Karriere_Bewerbungen", "Audit_Konsistenzbericht.md")


def load_env() -> Dict[str, str]:
    config = {}
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    config[k.strip()] = v.strip().strip('"').strip("'")
    return config


class VaultAuditor:
    def __init__(self, vault_dir: str = VAULT_DIR):
        self.vault_dir = vault_dir
        self.issues: List[Dict[str, Any]] = []
        self.stats = {
            "scanned_files": 0,
            "layer1_files": 0,
            "layer2_files": 0,
            "critical_count": 0,
            "warning_count": 0,
            "notice_count": 0,
            "clean_files": 0,
            "audit_time": ""
        }

    def _add_issue(self, file_rel: str, category: str, severity: str, rule_id: str, message: str, snippet: str = "", suggestion: str = ""):
        issue = {
            "file": file_rel,
            "category": category,
            "severity": severity,
            "rule_id": rule_id,
            "message": message,
            "snippet": snippet.strip()[:200] if snippet else "",
            "suggestion": suggestion
        }
        self.issues.append(issue)
        if severity == "CRITICAL":
            self.stats["critical_count"] += 1
        elif severity == "WARNING":
            self.stats["warning_count"] += 1
        else:
            self.stats["notice_count"] += 1

    def audit_file(self, rel_path: str, full_path: str, content: str):
        if "Audit_Konsistenzbericht.md" in rel_path:
            return

        is_layer2 = "05_Archiv" in rel_path or "DataLake" in rel_path
        lower = content.lower()

        # In Layer 2 DataLake (raw archive files), only check critical constitution rule
        if is_layer2:
            if "bosch" in lower:
                if re.search(r'\b(?:praktik|werkstud|angestellt|gearbeitet)\w*\s+(?:bei|für)\s+(?:robert\s+)?bosch\b', lower):
                    if not re.search(r'\b(kein|nicht|niemals|nie)\b', lower):
                        self._add_issue(
                            rel_path, "CONSTITUTION", "CRITICAL", "A1_BOSCH_AFFILIATION",
                            "Unzulässige Assoziation mit Robert Bosch GmbH gefunden.",
                            snippet=content[:200],
                            suggestion="Klarstellen: Das Patentmanagement-Projekt war für Klingele Paper & Packaging / ISG."
                        )
            return

        # -------------------------------------------------------------
        # LAYER 1 CURATED NOTES: Deep Audit & Contradiction Checking
        # -------------------------------------------------------------
        
        # 1.1 Bosch Affiliation Check (Strict zero tolerance)
        if "bosch" in lower:
            bosch_matches = re.finditer(r'(?:Praktikant|Praktikum|Werkstudent|Mitarbeiter|Angestellter|gearbeitet)\s+(?:bei|für)\s+(?:Robert\s+)?Bosch\b', content, re.IGNORECASE)
            for m in bosch_matches:
                start = max(0, m.start() - 40)
                end = min(len(content), m.end() + 40)
                ctx = content[start:end]
                if not re.search(r'\b(kein|nicht|niemals|nie|weder)\b', ctx, re.IGNORECASE):
                    self._add_issue(
                        rel_path, "CONSTITUTION", "CRITICAL", "A1_BOSCH_AFFILIATION",
                        "Unzulässige Assoziation mit Robert Bosch GmbH gefunden.",
                        snippet=ctx,
                        suggestion="Klarstellen: Das Patentmanagement-Projekt war für Klingele Paper & Packaging / ISG. Visar war NIE bei Bosch tätig!"
                    )

        # 1.2 Master Grade Check (Official: 1,6)
        if "master" in lower or "m.sc" in lower:
            m_grade = re.finditer(r'(?:Gesamtnote\s+(?:Master|M\.Sc\.)|Master(?:abschluss)?\s+Gesamtnote|Master\s+(?:mit\s+der\s+)?Note)\s*(?:von|:)?\s*([1-4][,\.][0-9])', content, re.IGNORECASE)
            for m in m_grade:
                val = m.group(1).replace(".", ",")
                if val != "1,6":
                    start = max(0, m.start() - 30)
                    ctx = content[start:m.end() + 30]
                    if "arbeit" not in ctx.lower() and "thesis" not in ctx.lower() and "modul" not in ctx.lower():
                        self._add_issue(
                            rel_path, "ACADEMIC", "CRITICAL", "A2_MASTER_GRADE",
                            f"Widersprüchliche Master-Gesamtnote '{val}' gefunden (Offiziell: 1,6).",
                            snippet=ctx,
                            suggestion="Auf amtliche Gesamtnote 1,6 ('gut') korrigieren (Zeugnis vom 17.09.2026)."
                        )

            # 1.3 Master Thesis Grade Check (Official: 1,0)
            if "masterarbeit" in lower or "master-thesis" in lower:
                mt_grade = re.finditer(r'(?:Masterarbeit|Master-Thesis)\s*(?:(?:mit\s+der\s+)?Note|bewertet\s+mit)?\s*(?:von|:)?\s*([1-4][,\.][0-9])', content, re.IGNORECASE)
                for m in mt_grade:
                    val = m.group(1).replace(".", ",")
                    if val != "1,0":
                        ctx = content[max(0, m.start() - 20):min(len(content), m.end() + 20)]
                        self._add_issue(
                            rel_path, "ACADEMIC", "CRITICAL", "A3_MASTER_THESIS_GRADE",
                            f"Widersprüchliche Masterarbeits-Note '{val}' gefunden (Offiziell: 1,0).",
                            snippet=ctx,
                            suggestion="Auf offizielle Bestnote 1,0 ('sehr gut') korrigieren."
                        )

        # 1.4 Bachelor Grade Check (Official: 3,0)
        if "bachelor" in lower or "b.sc" in lower:
            b_grade = re.finditer(r'(?:Gesamtnote\s+(?:Bachelor|B\.Sc\.)|Bachelor(?:abschluss)?\s+Gesamtnote)\s*(?:von|:)?\s*([1-4][,\.][0-9])', content, re.IGNORECASE)
            for m in b_grade:
                val = m.group(1).replace(".", ",")
                if val != "3,0":
                    ctx = content[max(0, m.start() - 20):min(len(content), m.end() + 20)]
                    if "arbeit" not in ctx.lower() and "thesis" not in ctx.lower():
                        self._add_issue(
                            rel_path, "ACADEMIC", "CRITICAL", "A4_BACHELOR_GRADE",
                            f"Widersprüchliche Bachelor-Gesamtnote '{val}' gefunden (Offiziell: 3,0).",
                            snippet=ctx,
                            suggestion="Auf offizielle Bachelor-Gesamtnote 3,0 korrigieren."
                        )

            # 1.5 Bachelor Thesis Grade Check (Official: 1,7)
            if "bachelorarbeit" in lower or "bachelor-thesis" in lower:
                bt_grade = re.finditer(r'(?:Bachelorarbeit|Bachelor-Thesis)\s*(?:(?:mit\s+der\s+)?Note|bewertet\s+mit)?\s*(?:von|:)?\s*([1-4][,\.][0-9])', content, re.IGNORECASE)
                for m in bt_grade:
                    val = m.group(1).replace(".", ",")
                    if val != "1,7":
                        ctx = content[max(0, m.start() - 20):min(len(content), m.end() + 20)]
                        self._add_issue(
                            rel_path, "ACADEMIC", "CRITICAL", "A5_BACHELOR_THESIS_GRADE",
                            f"Widersprüchliche Bachelorarbeits-Note '{val}' gefunden (Offiziell: 1,7).",
                            snippet=ctx,
                            suggestion="Auf offizielle Bachelorarbeits-Note 1,7 ('gut') korrigieren."
                        )

        # 1.6 ECTS Integrity Check (only Layer 1)
        if not is_layer2 and "ects" in lower:
            if "master" in lower:
                for line in content.splitlines():
                    l_low = line.lower()
                    if "master" in l_low and "ects" in l_low and "gesamt" in l_low:
                        # Allow 300 ECTS when combined with Bachelor (180 B.Sc. + 120 M.Sc. = 300 ECTS Gesamtstudium)
                        if "bachelor" in l_low and "300" in line:
                            continue
                        if not re.search(r'\b120\s*ects\b', line, re.IGNORECASE):
                            m_match = re.search(r'\b([0-9]{2,3})\s*ects\b', line, re.IGNORECASE)
                            if m_match and m_match.group(1) not in ("120", "300"):
                                self._add_issue(
                                    rel_path, "ACADEMIC", "WARNING", "A6_MASTER_ECTS_MISMATCH",
                                    f"Möglicher abweichender Master-ECTS-Wert '{m_match.group(0)}' (Offiziell: 120 ECTS).",
                                    snippet=line.strip()[:150],
                                    suggestion="Prüfen und auf 120 ECTS (M.Sc. Wirtschaftsinformatik) vereinheitlichen."
                                )

        # 1.7 Tenure Durations (only Layer 1)
        if not is_layer2:
            if "ssb" in lower and "monat" in lower:
                for line in content.splitlines():
                    l_low = line.lower()
                    if ("ssb" in l_low or "sap4ssb" in l_low) and "monat" in l_low:
                        # If the line correctly includes 24 months for SSB, skip
                        if re.search(r'\b24\s*(?:mo\.?|monate)\b', l_low):
                            continue
                        # If it's a sum total line like "36 Monate (24 Mo. SSB + 12 Mo. DC1)"
                        if "36 monate" in l_low and ("24" in l_low or "dc1" in l_low or "datacenter" in l_low):
                            continue
                        # If the duration mentions datacenter one or dc1 or inoc specifically:
                        if ("datacenter" in l_low or "dc1" in l_low or "inoc" in l_low) and re.search(r'\b12\s*(?:mo\.?|monate)\b', l_low):
                            # Check if the 12 Monate is attached to Datacenter One and not SSB
                            if re.search(r'(?:datacenter|dc1|inoc)[^.\n]{0,50}\b12\s*(?:mo\.?|monate)\b', l_low) or \
                               re.search(r'\b12\s*(?:mo\.?|monate)\b[^.\n]{0,50}(?:datacenter|dc1|inoc)', l_low):
                                continue
                        dur_match = re.search(r'\b([0-9]{1,2})\s*monate\b', line, re.IGNORECASE)
                        if dur_match and dur_match.group(1) not in ("24", "36"):
                            self._add_issue(
                                rel_path, "EXPERIENCE", "WARNING", "A7_SSB_DURATION",
                                f"Abweichende SSB-Dauer '{dur_match.group(0)}' gefunden (Offiziell: 24 Monate, 05/2024–04/2026).",
                                snippet=line.strip()[:150],
                                suggestion="Auf 24 Monate (05/2024–04/2026) vereinheitlichen."
                            )

            if ("datacenter one" in lower or "dc1" in lower or "inoc" in lower) and "monat" in lower:
                for line in content.splitlines():
                    l_low = line.lower()
                    if ("datacenter one" in l_low or "dc1" in l_low or "inoc" in l_low) and "monat" in l_low:
                        # If the line correctly includes 12 months for DC1, skip
                        if re.search(r'\b12\s*(?:mo\.?|monate)\b', l_low):
                            continue
                        # If it's a sum total line
                        if "36 monate" in l_low and ("12" in l_low or "ssb" in l_low):
                            continue
                        # If the duration mentions ssb specifically:
                        if ("ssb" in l_low or "sap4ssb" in l_low) and re.search(r'\b24\s*(?:mo\.?|monate)\b', l_low):
                            if re.search(r'(?:ssb|sap4ssb)[^.\n]{0,50}\b24\s*(?:mo\.?|monate)\b', l_low) or \
                               re.search(r'\b24\s*(?:mo\.?|monate)\b[^.\n]{0,50}(?:ssb|sap4ssb)', l_low):
                                continue
                        dur_match = re.search(r'\b([0-9]{1,2})\s*monate\b', line, re.IGNORECASE)
                        if dur_match and dur_match.group(1) not in ("12", "36"):
                            self._add_issue(
                                rel_path, "EXPERIENCE", "WARNING", "A8_DC1_DURATION",
                                f"Abweichende Datacenter One Dauer '{dur_match.group(0)}' gefunden (Offiziell: 12 Monate, 05/2023–04/2024).",
                                snippet=line.strip()[:150],
                                suggestion="Auf 12 Monate (05/2023–04/2024) vereinheitlichen."
                            )

        # -------------------------------------------------------------
        # RULE SET 2: Master Thesis Scope & Reductionism (Warning)
        # -------------------------------------------------------------
        if not is_layer2 and ("masterarbeit" in lower or "master-thesis" in lower):
            has_clean_core = "clean core" in lower
            has_transformation = "transformation" in lower or "plattformisierung" in lower or "erfolgsfaktoren" in lower or "csf" in lower
            if has_clean_core and not has_transformation:
                self._add_issue(
                    rel_path, "REDUCTIONISM", "WARNING", "B1_CLEAN_CORE_REDUCTIONISM",
                    "Masterarbeit wird möglicherweise unvollständig auf 'Clean Core' verkürzt.",
                    snippet=content[:250],
                    suggestion="Ergänzen: Ganzheitliche ERP-Transformation, Plattformisierung von SAP S/4HANA und empirische Kritische Erfolgsfaktoren (12 Interviews, Mayring)."
                )

        # -------------------------------------------------------------
        # RULE SET 3: Enterprise & Architectural Consistency
        # -------------------------------------------------------------
        if not is_layer2 and ("sap4ssb" in lower or ("ssb" in lower and "s/4" in lower)):
            if "brownfield" in lower:
                is_valid_comparison = any(term in lower for term in [
                    "kein brownfield", "keine brownfield", "warum kein", "statt brownfield",
                    "vs. brownfield", "versus brownfield", "vs brownfield", "greenfield vs",
                    "greenfield oder brownfield", "greenfield statt brownfield", "greenfield und kein",
                    "vergleich", "gegenüber", "im gegensatz", "einstieg: greenfield"
                ])
                if not is_valid_comparison:
                    if re.search(r'\b(?:ssb|transformation|programm|migration)\b[^.\n]{0,40}\b(?:war|ist|als)\s+brownfield\b', lower):
                        self._add_issue(
                            rel_path, "ARCHITECTURE", "WARNING", "C1_BROWNFIELD_CONFUSION",
                            "Mögliche Verwechslung: SSB wurde als Greenfield (nicht Brownfield) umgesetzt.",
                            snippet="Fundstelle zu 'Brownfield' im SSB-Kontext",
                            suggestion="Sicherstellen, dass Greenfield RISE Private Cloud hervorgehoben wird (historische Z-Modifikationen machten Brownfield unmöglich)."
                        )

        # -------------------------------------------------------------
        # RULE SET 4: Temporal & Status Inconsistencies
        # -------------------------------------------------------------
        if not is_layer2:
            if "masterarbeit" in lower or "master-thesis" in lower:
                for line in content.splitlines():
                    if ("masterarbeit" in line.lower() or "master-thesis" in line.lower()) and any(t in line.lower() for t in ["in bearbeitung", "laufend", "voraussichtlich bis", "geplant abgabe"]):
                        self._add_issue(
                            rel_path, "TEMPORAL", "NOTICE", "D1_OUTDATED_THESIS_STATUS",
                            "Veralteter Bearbeitungsstatus der Masterarbeit gefunden.",
                            snippet=line.strip()[:150],
                            suggestion="Auf 'Erfolgreich abgeschlossen (Note 1,0, 20.04.2026, Zeugnis 17.09.2026)' aktualisieren."
                        )

        # Interview prep debriefing check
        if "Interview_Vorbereitungen" in rel_path:
            date_match = re.search(r'2026-(\d{2})-(\d{2})', rel_path)
            if date_match:
                try:
                    int_date = datetime.strptime(date_match.group(0), "%Y-%m-%d").date()
                    now_date = datetime.now().date()
                    if int_date < now_date and not any(k in lower for k in ["debriefing", "ergebnis", "erfolgreich absolviert", "gesprächsnotiz"]):
                        self._add_issue(
                            rel_path, "TEMPORAL", "NOTICE", "D2_PAST_INTERVIEW_STATUS",
                            f"Interviewdatum {int_date} liegt in der Vergangenheit, Notiz enthält noch kein Debriefing/Ergebnis.",
                            snippet=f"Interview am {int_date}",
                            suggestion="Gesprächsverlauf, Feedback und nächste Schritte in der Interview-Notiz ergänzen."
                        )
                except Exception:
                    pass

    def run_audit(self) -> Dict[str, Any]:
        self.stats["audit_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        md_files = []
        for r, ds, fs in os.walk(self.vault_dir):
            ds[:] = [d for d in ds if d not in (".obsidian", ".trash")]
            for f in fs:
                if f.endswith(".md"):
                    full = os.path.join(r, f)
                    rel = os.path.relpath(full, self.vault_dir)
                    md_files.append((rel, full))

        self.stats["scanned_files"] = len(md_files)
        clean_count = 0

        for rel, full in md_files:
            if "05_Archiv" in rel or "DataLake" in rel:
                self.stats["layer2_files"] += 1
            else:
                self.stats["layer1_files"] += 1

            pre_len = len(self.issues)
            try:
                with open(full, "r", encoding="utf-8", errors="ignore") as fp:
                    content = fp.read()
                self.audit_file(rel, full, content)
            except Exception as e:
                self._add_issue(rel, "SYSTEM", "WARNING", "E0_READ_ERROR", f"Datei nicht lesbar: {e}")

            if len(self.issues) == pre_len:
                clean_count += 1

        self.stats["clean_files"] = clean_count
        return {
            "stats": self.stats,
            "issues": self.issues
        }

    def generate_markdown_report(self) -> str:
        s = self.stats
        report = f"""---
id: audit-konsistenzbericht-second-brain
title: "Second Brain Sanity & Contradiction Audit Report"
type: audit-report
domain: system-governance
status: active
generated_at: "{s['audit_time']}"
total_files_audited: {s['scanned_files']}
layer1_curated_notes: {s['layer1_files']}
layer2_datalake_notes: {s['layer2_files']}
critical_contradictions: {s['critical_count']}
warnings: {s['warning_count']}
notices: {s['notice_count']}
---

# 🛡️ Second Brain Sanity & Contradiction Audit Report
> **Inspiriert vom Andrej Karpathy LLM-Wiki-Muster:**
> Vollautomatischer Audit über alle `{s['scanned_files']}` Markdown-Dokumente im Obsidian Vault zur Erkennung von Faktenwidersprüchen, veralteten Statusangaben und architektonischem Reduktionismus.

---

## 📊 Zusammenfassung der System-Gesundheit

| Metrik | Wert | Status |
| :--- | :--- | :--- |
| **Geprüfte Notizen** | **{s['scanned_files']}** ({s['layer1_files']} Layer 1 Kuratiert, {s['layer2_files']} Layer 2 DataLake) | 🟢 Vollständig |
| **Kritische Faktenwidersprüche (FATAL)** | **{s['critical_count']}** | {'🟢 0 (Perfekt)' if s['critical_count'] == 0 else '🔴 Handlungsbedarf'} |
| **Architektur- & Thesenwarnungen (WARNING)** | **{s['warning_count']}** | {'🟢 0 (Perfekt)' if s['warning_count'] == 0 else '🟠 Prüfenswert'} |
| **Veraltete Status / Zeitliche Notizen (NOTICE)** | **{s['notice_count']}** | {'🟢 0' if s['notice_count'] == 0 else '🟡 Pflegehinweise'} |
| **Vollständig konsistente Dokumente** | **{s['clean_files']}** ({s['clean_files'] / max(1, s['scanned_files']) * 100:.1f}%) | 🎯 Exzellent |

---

## 🔍 Detaillierte Befunde & Handlungsempfehlungen

"""
        if not self.issues:
            report += "### ✅ 100% Konsistenz erreicht!\n\nEs wurden keinerlei Faktenwidersprüche, falsche Noten, ECTS-Abweichungen oder unzulässige Unternehmens-Zuschreibungen im gesamten Second Brain gefunden.\n"
        else:
            # Group by severity
            crit = [i for i in self.issues if i['severity'] == "CRITICAL"]
            warn = [i for i in self.issues if i['severity'] == "WARNING"]
            noti = [i for i in self.issues if i['severity'] == "NOTICE"]

            if crit:
                report += f"### 🔴 Kritische Faktenwidersprüche ({len(crit)})\n\n"
                for idx, item in enumerate(crit, 1):
                    report += f"#### {idx}. `{item['file']}` [{item['rule_id']}]\n"
                    report += f"- **Problem:** {item['message']}\n"
                    if item['snippet']:
                        report += f"- **Fundstelle:** `...{item['snippet']}...`\n"
                    report += f"- **Lösungsvorschlag:** {item['suggestion']}\n\n"

            if warn:
                report += f"### 🟠 Architektur- & Konzept-Warnungen ({len(warn)})\n\n"
                for idx, item in enumerate(warn, 1):
                    report += f"#### {idx}. `{item['file']}` [{item['rule_id']}]\n"
                    report += f"- **Problem:** {item['message']}\n"
                    if item['snippet']:
                        report += f"- **Fundstelle:** `...{item['snippet']}...`\n"
                    report += f"- **Lösungsvorschlag:** {item['suggestion']}\n\n"

            if noti:
                report += f"### 🟡 Zeitliche & Status-Hinweise ({len(noti)})\n\n"
                for idx, item in enumerate(noti, 1):
                    report += f"#### {idx}. `{item['file']}` [{item['rule_id']}]\n"
                    report += f"- **Hinweis:** {item['message']}\n"
                    if item['snippet']:
                        report += f"- **Fundstelle:** `...{item['snippet']}...`\n"
                    report += f"- **Empfehlung:** {item['suggestion']}\n\n"

        report += """---

## 🚀 Regelwerk & Ground Truth (AGENTS.md)
* **Master of Science (M.Sc.):** Wirtschaftsinformatik, Uni Stuttgart, **1,6** („gut“), **120 ECTS** (Zeugnis: 17.09.2026).
* **Masterarbeit:** Note **1,0** („sehr gut“), Titel: *„Kritische Erfolgsfaktoren in der Transformation großer ERP-Systeme: Eine Untersuchung am Beispiel der Plattformisierung von SAP S/4HANA“* (Prof. Herzwurm, 126 S., 12 Interviews, Mayring). Niemals auf 'Clean Core' reduzieren!
* **Bachelor of Science (B.Sc.):** Wirtschaftsinformatik, Uni Stuttgart, **3,0**, **180 ECTS**, Bachelorarbeit Note **1,7** (14 Boundary-Resource-Klassen, OutSystems & Mendix).
* **Praxisstationen:** SSB AG (24 Monate, 05/2024–04/2026, IT-PMO & TP5 Greenfield RISE Private Cloud) • Datacenter One (12 Monate, 05/2023–04/2024, INOC ITIL 4).
* **Unternehmensprojekte:** Patentmanagement-Plattform für Klingele Paper & Packaging / ISG (kein Praktikum bei Robert Bosch GmbH!).

---

## 🔗 Navigation & Wissensnetz
- [[00_INDEX|🧠 Master Index]] • [[00_Bewerbungsmanagement_Cockpit|📊 Bewerbungs-Cockpit]] • [[MOC_Fachbibliothek_Masterhub|📚 Fachbibliothek-Hub]]
"""
        return report


def run_cli():
    parser = argparse.ArgumentParser(description="Career OS Contradiction & Sanity Checker")
    parser.add_argument("--vault", default=VAULT_DIR, help="Path to Obsidian Vault")
    parser.add_argument("--save-report", action="store_true", default=True, help="Save markdown audit report to vault")
    parser.add_argument("--json", action="store_true", help="Print report as JSON")
    args = parser.parse_args()

    print("=" * 72)
    print("🛡️  RUNNING CAREER OS CONTRADICTION & SANITY CHECKER (KARPATHY-LLM-WIKI)")
    print("=" * 72)

    auditor = VaultAuditor(vault_dir=args.vault)
    results = auditor.run_audit()
    stats = results["stats"]

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return

    print(f"\n[+] Geprüfte Dokumente: {stats['scanned_files']} ({stats['layer1_files']} Layer 1, {stats['layer2_files']} Layer 2)")
    print(f"[+] Status:")
    print(f"    - 🔴 Kritische Widersprüche (FATAL): {stats['critical_count']}")
    print(f"    - 🟠 Architektur- & Thesenwarnungen (WARNING): {stats['warning_count']}")
    print(f"    - 🟡 Zeitliche & Status-Hinweise (NOTICE): {stats['notice_count']}")
    print(f"    - 🟢 Vollständig konsistente Notizen: {stats['clean_files']} ({stats['clean_files'] / max(1, stats['scanned_files']) * 100:.1f}%)")

    if results["issues"]:
        print("\n" + "=" * 72)
        print("🔍 GEFUNDENE BEFUNDE:")
        print("=" * 72)
        for issue in results["issues"]:
            sev_icon = "🔴" if issue["severity"] == "CRITICAL" else ("🟠" if issue["severity"] == "WARNING" else "🟡")
            print(f"\n{sev_icon} [{issue['severity']}] {issue['file']} ({issue['rule_id']})")
            print(f"   Problem: {issue['message']}")
            if issue['snippet']:
                print(f"   Snippet: \"{issue['snippet']}\"")
            print(f"   Vorschlag: {issue['suggestion']}")
    else:
        print("\n🎯 PERFEKT! 100% Fakten- und Architekturkonsistenz über alle Notizen hinweg.")

    if args.save_report:
        report_md = auditor.generate_markdown_report()
        try:
            with open(AUDIT_REPORT_PATH, "w", encoding="utf-8") as f:
                f.write(report_md)
            print(f"\n[✓] Audit-Bericht erfolgreich gespeichert unter:\n    {AUDIT_REPORT_PATH}")
        except Exception as e:
            print(f"\n[!] Fehler beim Speichern des Audit-Berichts: {e}")

    print("=" * 72)


if __name__ == "__main__":
    run_cli()
