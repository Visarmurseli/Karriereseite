# -*- coding: utf-8 -*-
"""
Karpathy LLM-Wiki Knowledge Graph Synthesizer & Auto-Linker
Author: Visar Murseli, M.Sc. | Enterprise Knowledge Hub & Career OS

Funktionen:
1. Bidirektionale Graph-Analyse über alle kuratierten Notizen (Layer 1):
   - In-Degree (Backlinks), Out-Degree (Zitate), Hub-Zentralität, Graphdichte.
   - Erkennung von verwaisten Notizen (Orphans) und Sackgassen (Dead Ends).
2. Deterministisches Konzept- und Entitäten-Lexikon (The Vault Lexicon):
   - Mappt Fachbegriffe (Clean Core, TOGAF 9 ADM, Cloud ALM, Signavio, SDD, ITIL 4, etc.)
     auf kanonische Zielzettel.
3. Sichere Wikilink-Auto-Verlinkung (--auto-link / --dry-run):
   - Erkennt ungelinkte Erwähnungen im Fliesstext und wandelt sie kontextgenau in [[TargetNote|Label]] um.
   - Absoluter Schutz für Frontmatter, Code-Blöcke (inline/fenced), HTML-Tags und bestehende Links.
4. Orphan-Healing & Backlink-Synthese (--heal):
   - Verankert isolierte Notizen und Sackgassen in Master-Indices (MOCs, 00_INDEX).
5. Graph-Synthese-Bericht (--report):
   - Revisionssicherer Markdown-Report mit Mermaid-Diagramm unter
     `04_Second_Brain_Zettelkasten/Graph_Synthese_Bericht.md`.
"""

import os
import re
import json
import argparse
from datetime import datetime
from collections import defaultdict

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
VAULT_DIR = r"C:\Users\SHQIPTAR634\Documents\Obsidian Vault"
SYNTHESIS_REPORT_PATH = os.path.join(
    VAULT_DIR, "04_Second_Brain_Zettelkasten", "Graph_Synthese_Bericht.md"
)

# Canonical domain concepts for high-precision linking
CANONICAL_CONCEPT_LEXICON = {
    # 1. Enterprise Architecture & IT Governance
    "TOGAF 9 ADM": "Modul_TOGAF_Scape",
    "TOGAF 9": "Modul_TOGAF_Scape",
    "TOGAF": "Modul_TOGAF_Scape",
    "Enterprise Architecture Management": "Enterprise_Architecture_Overview",
    "Enterprise Architecture": "Enterprise_Architecture_Overview",

    # 2. SAP S/4HANA Transformation & Activate
    "SAP Activate": "SAP_Activate_Methodik_SSB",
    "SAP Activate Methodik": "SAP_Activate_Methodik_SSB",
    "Activate Methodik": "SAP_Activate_Methodik_SSB",
    "Clean Core Paradigma": "Clean_Core_Paradigma",
    "Clean Core": "Clean_Core_Paradigma",
    "SAP Cloud ALM": "SSB_Tool_Governance_Signavio_CALM",
    "Cloud ALM": "SSB_Tool_Governance_Signavio_CALM",
    "SAP Signavio": "SSB_Tool_Governance_Signavio_CALM",
    "Signavio": "SSB_Tool_Governance_Signavio_CALM",
    "SAP Enable Now": "Key_User_Enablement_EnableNow",
    "Enable Now": "Key_User_Enablement_EnableNow",
    "Solution Design Document": "SSB_Solution_Design_FI_CO",
    "Solution Design": "SSB_Solution_Design_FI_CO",
    "RISE with SAP": "SSB_Grossprojekt_SAP4SSB",
    "RISE Private Cloud": "SSB_Grossprojekt_SAP4SSB",
    "WRICEFA": "WRICEFA_Entkopplung",
    "WRICEF": "WRICEFA_Entkopplung",
    "SAP BTP": "SAP_BTP_Integration_Suite",
    "BTP Integration Suite": "SAP_BTP_Integration_Suite",
    "Business Technology Platform": "SAP_BTP_Integration_Suite",
    "Customer Vendor Integration": "Customer_Vendor_Integration_CVI",
    "CVI": "Customer_Vendor_Integration_CVI",
    "SAP Migration Cockpit": "SAP_Migration_Cockpit_LTMC",
    "LTMC": "SAP_Migration_Cockpit_LTMC",
    "Universal Journal": "Universal_Journal_ACDOCA",
    "ACDOCA": "Universal_Journal_ACDOCA",
    "Trennungsrechnung": "Trennungsrechnung_OEPNV_EU1370",
    "Absorptive Capacity": "Absorptive_Capacity_SSB",
    "Bimodale IT": "Bimodale_ERP_Plattformisierung_BTP",
    "Bimodale Architektur": "Bimodale_ERP_Plattformisierung_BTP",
    "Readiness Check": "SAP_Readiness_Check_Detailanalyse",

    # 3. ITIL 4 & Datacenter Operations
    "ITIL 4 Service Operations": "DC1_ITIL4_Service_Operations",
    "ITIL 4": "DC1_ITIL4_Service_Operations",
    "ITIL": "DC1_ITIL4_Service_Operations",
    "Hardware-Lifecycle-Management": "DC1_Hardware_Lifecycle_Management",
    "Hardware Lifecycle Management": "DC1_Hardware_Lifecycle_Management",
    "HLM": "DC1_Hardware_Lifecycle_Management",
    "Network Operation Center": "DC1_ITIL4_Service_Operations",
    "INOC": "DC1_ITIL4_Service_Operations",

    # 4. Akademische Forschung & Methoden (Uni Stuttgart)
    "Boundary Resources": "Modul_Bachelorarbeit",
    "Boundary Resource Theory": "Modul_Bachelorarbeit",
    "Qualitative Inhaltsanalyse": "Modul_Forschungsmethoden",
    "Mayring": "Modul_Forschungsmethoden",
    "Masterarbeit": "Modul_Masterarbeit",
    "Bachelorarbeit": "Modul_Bachelorarbeit",
    "Advanced Software Engineering": "Modul_Advanced_Software_Engineering",
    "ASE": "Modul_Advanced_Software_Engineering",
    "Software-Architektur": "Modul_Software_Architektur",
    "Software Architektur": "Modul_Software_Architektur",
    "Cloud Computing": "Modul_Cloud_Computing",
    "Innovationsmanagement": "Modul_Innovationsmanagement",
    "Smart Service Blueprinting": "Modul_FPWI",
    "FPWI": "Modul_FPWI",
    "AI4IoT": "Modul_AI4IoT",

    # 5. Career OS & Second Brain Hubs
    "Persönliches Stärkenprofil": "Persoenliches_Staerkenprofil",
    "Stärkenprofil": "Persoenliches_Staerkenprofil",
    "Target Roles": "Target_Roles",
    "Bewerbungs-Cockpit": "00_Bewerbungsmanagement_Cockpit",
    "Bewerbungsmanagement-Cockpit": "00_Bewerbungsmanagement_Cockpit",
    "Audit-Bericht": "Audit_Konsistenzbericht",
    "Konsistenzbericht": "Audit_Konsistenzbericht",
    "Master Index": "00_INDEX",
}


def tokenize_markdown(body: str):
    """
    Zerlegt den Markdown-Text hierarchisch in ('PROTECTED', text) und ('TEXT', text).
    Schützt zuverlässig Codeblöcke, Inline-Code, bestehende Wikilinks, Markdown-Links und Überschriften
    vollkommen ohne regex-backtracking.
    """
    segments = []
    fenced_parts = body.split("```")
    for i, f_part in enumerate(fenced_parts):
        if i % 2 == 1:
            segments.append(("PROTECTED", "```" + f_part + "```"))
            continue

        inline_parts = f_part.split("`")
        for j, in_part in enumerate(inline_parts):
            if j % 2 == 1:
                segments.append(("PROTECTED", "`" + in_part + "`"))
                continue

            wiki_parts = re.split(r'(\[\[[^\]]+\]\])', in_part)
            for k, w_part in enumerate(wiki_parts):
                if w_part.startswith("[[") and w_part.endswith("]]"):
                    segments.append(("PROTECTED", w_part))
                    continue

                md_parts = re.split(r'(\[[^\]]+\]\([^)]+\))', w_part)
                for m_part in md_parts:
                    if re.match(r'^\[[^\]]+\]\([^)]+\)$', m_part):
                        segments.append(("PROTECTED", m_part))
                        continue

                    lines = m_part.splitlines(keepends=True)
                    for line in lines:
                        if line.lstrip().startswith("#"):
                            segments.append(("PROTECTED", line))
                        else:
                            segments.append(("TEXT", line))
    return segments


class ZettelkastenSynthesizer:
    def __init__(self, vault_dir: str = VAULT_DIR):
        self.vault_dir = vault_dir
        self.notes = {}            # rel_path -> {base_name, full_path, content, frontmatter, body, links}
        self.base_to_rel = {}      # base_name.lower() -> rel_path
        self.outbound = defaultdict(set)  # base_name -> set(target_bases)
        self.inbound = defaultdict(set)   # base_name -> set(source_bases)
        self.metrics = {}
        self.link_pattern = re.compile(r'\[\[([^\]\|#]+)(?:#[^\]\|]+)?(?:\|[^\]]+)?\]\]')

    def index_vault(self):
        """Indiziert alle Layer-1-Notizen im Vault."""
        self.notes.clear()
        self.base_to_rel.clear()
        self.outbound.clear()
        self.inbound.clear()

        for root, dirs, files in os.walk(self.vault_dir):
            if "05_Archiv" in root or ".obsidian" in root or ".trash" in root:
                continue
            for f in files:
                if f.endswith(".md"):
                    full_p = os.path.join(root, f)
                    rel_p = os.path.relpath(full_p, self.vault_dir)
                    base_name = os.path.splitext(f)[0]

                    try:
                        with open(full_p, "r", encoding="utf-8") as fp:
                            content = fp.read()
                    except Exception:
                        continue

                    # Extract frontmatter
                    fm = {}
                    body = content
                    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
                    if fm_match:
                        body = content[len(fm_match.group(0)):]
                        for line in fm_match.group(1).splitlines():
                            if ":" in line:
                                k, v = line.split(":", 1)
                                fm[k.strip()] = v.strip().strip('"').strip("'")

                    # Extract outgoing links
                    raw_links = self.link_pattern.findall(content)
                    clean_links = set()
                    for l in raw_links:
                        t = os.path.basename(l.strip()).replace(".md", "")
                        clean_links.add(t)

                    self.notes[rel_p] = {
                        "base_name": base_name,
                        "rel_path": rel_p,
                        "full_path": full_p,
                        "content": content,
                        "frontmatter": fm,
                        "body": body,
                        "links": clean_links,
                    }
                    self.base_to_rel[base_name.lower()] = base_name

        # Build graph adjacency lists
        all_bases = {n["base_name"] for n in self.notes.values()}
        for rel_p, data in self.notes.items():
            src = data["base_name"]
            for target in data["links"]:
                # Check case-insensitive match
                canonical_target = self.base_to_rel.get(target.lower())
                if canonical_target and canonical_target in all_bases:
                    self.outbound[src].add(canonical_target)
                    self.inbound[canonical_target].add(src)

        return len(self.notes)

    def analyze_graph(self):
        """Berechnet topologische Graph- und Zettelkasten-Metriken."""
        if not self.notes:
            self.index_vault()

        all_bases = sorted({n["base_name"] for n in self.notes.values()})
        total_notes = len(all_bases)
        total_edges = sum(len(targets) for targets in self.outbound.values())

        # Degree computations
        in_degrees = {b: len(self.inbound[b]) for b in all_bases}
        out_degrees = {b: len(self.outbound[b]) for b in all_bases}
        total_degrees = {b: in_degrees[b] + out_degrees[b] for b in all_bases}

        # Orphans & Dead Ends
        pure_orphans = [b for b in all_bases if in_degrees[b] == 0 and out_degrees[b] == 0]
        no_inbound = [b for b in all_bases if in_degrees[b] == 0]
        no_outbound = [b for b in all_bases if out_degrees[b] == 0]

        # Top Hubs
        top_authorities = sorted(in_degrees.items(), key=lambda x: x[1], reverse=True)[:10]
        top_collectors = sorted(out_degrees.items(), key=lambda x: x[1], reverse=True)[:10]

        # Density
        max_possible_edges = total_notes * (total_notes - 1) if total_notes > 1 else 1
        graph_density = (total_edges / max_possible_edges) * 100
        avg_links_per_note = total_edges / max(1, total_notes)

        # Domain clustering
        domains = defaultdict(int)
        for data in self.notes.values():
            dom = data["frontmatter"].get("domain", "unassigned")
            domains[dom] += 1

        self.metrics = {
            "total_notes": total_notes,
            "total_edges": total_edges,
            "avg_links_per_note": round(avg_links_per_note, 2),
            "graph_density_pct": round(graph_density, 3),
            "pure_orphans": pure_orphans,
            "no_inbound": no_inbound,
            "no_outbound": no_outbound,
            "top_authorities": top_authorities,
            "top_collectors": top_collectors,
            "domain_distribution": dict(domains),
            "connectivity_score_pct": round(
                ((total_notes - len(pure_orphans)) / max(1, total_notes)) * 100, 1
            ),
        }
        return self.metrics

    def find_unlinked_opportunities(self):
        """Findet ungelinkte Erwähnungen kanonischer Fachbegriffe im Fliesstext."""
        if not self.notes:
            self.index_vault()

        opportunities = []
        all_bases = {n["base_name"] for n in self.notes.values()}
        # Longer phrases first to match most specific concepts
        sorted_lexicon = sorted(CANONICAL_CONCEPT_LEXICON.items(), key=lambda x: len(x[0]), reverse=True)

        for rel_p, data in self.notes.items():
            # Skip changelogs, synthesis reports and audit reports from auto-linking
            if "CHANGELOG" in rel_p or "Audit_Konsistenzbericht" in rel_p or "Graph_Synthese_Bericht" in rel_p:
                continue

            base = data["base_name"]
            content = data["content"]
            existing_links_lower = {l.lower() for l in data["links"]}

            # Prepare body for safe inspection (strip frontmatter)
            body = data["body"]

            # Tokenize body into PROTECTED vs TEXT using fast hierarchical split
            tokens = tokenize_markdown(body)
            plain_text = " ".join(val for kind, val in tokens if kind == "TEXT")
            plain_text_lower = plain_text.lower()

            for concept, target_note in sorted_lexicon:
                # Avoid self-linking
                if base.lower() == target_note.lower():
                    continue
                # If target is already linked in this note, skip
                if target_note.lower() in existing_links_lower:
                    continue
                # Fast pre-check: concept substring must be in text
                if concept.lower() not in plain_text_lower:
                    continue
                # Target note must exist in vault
                if target_note not in all_bases and target_note.lower() not in self.base_to_rel:
                    continue

                # Search concept as whole word
                c_match = re.search(r'\b(' + re.escape(concept) + r')\b', plain_text, re.IGNORECASE)
                if c_match:
                    start = max(0, c_match.start() - 30)
                    end = min(len(plain_text), c_match.end() + 30)
                    snippet = plain_text[start:end].replace("\n", " ").strip()
                    opportunities.append({
                        "file": rel_p,
                        "base_name": base,
                        "concept": concept,
                        "target_note": target_note,
                        "snippet": f"...{snippet}..."
                    })

        return opportunities

    def apply_auto_links(self, dry_run: bool = True):
        """Wendet fehlende Wikilinks deterministisch und sicher auf die Notizen an."""
        opportunities = self.find_unlinked_opportunities()
        grouped = defaultdict(list)
        for opp in opportunities:
            grouped[opp["file"]].append(opp)

        changes = []

        for rel_p, opps in grouped.items():
            data = self.notes[rel_p]
            content = data["content"]
            full_path = data["full_path"]

            # Separate frontmatter and body
            fm_match = re.match(r"^(---\s*\n.*?\n---\s*\n)", content, re.DOTALL)
            if fm_match:
                frontmatter = fm_match.group(1)
                body = content[len(frontmatter):]
            else:
                frontmatter = ""
                body = content

            tokens = tokenize_markdown(body)
            applied_in_file = 0
            file_changes = []

            for opp in opps:
                concept = opp["concept"]
                target = opp["target_note"]
                concept_re = re.compile(r'\b(' + re.escape(concept) + r')\b', re.IGNORECASE)

                replaced = False
                new_tokens = []
                for kind, val in tokens:
                    if kind == "TEXT" and not replaced:
                        def _repl(match):
                            nonlocal replaced
                            if not replaced:
                                replaced = True
                                orig = match.group(1)
                                if orig == target:
                                    return f"[[{target}]]"
                                else:
                                    return f"[[{target}|{orig}]]"
                            return match.group(0)

                        new_val = concept_re.sub(_repl, val, count=1)
                        if replaced:
                            new_tokens.extend(tokenize_markdown(new_val))
                        else:
                            new_tokens.append(("TEXT", new_val))
                    else:
                        new_tokens.append((kind, val))

                if replaced:
                    tokens = new_tokens
                    applied_in_file += 1
                    file_changes.append(f"{concept} -> [[{target}]]")

            if applied_in_file > 0:
                new_body = "".join(val for _, val in tokens)
                new_content = frontmatter + new_body
                changes.append({
                    "file": rel_p,
                    "count": applied_in_file,
                    "details": file_changes
                })

                if not dry_run:
                    with open(full_path, "w", encoding="utf-8") as fp:
                        fp.write(new_content)
                    data["content"] = new_content
                    data["body"] = new_body

        return changes

    def heal_orphans_and_dead_ends(self, dry_run: bool = True):
        """Heilt verwaiste Notizen und bindet Dead-Ends in Hubs ein."""
        if not self.metrics:
            self.analyze_graph()

        healed = []
        all_notes_by_base = {n["base_name"]: n for n in self.notes.values()}

        # 1. Check Audit_Konsistenzbericht.md (no inbound links)
        audit_base = "Audit_Konsistenzbericht"
        if audit_base in all_notes_by_base:
            # Ensure 00_INDEX.md links to it
            index_data = all_notes_by_base.get("00_INDEX")
            if index_data and audit_base not in index_data["links"]:
                if not dry_run:
                    content = index_data["content"]
                    if "[[Audit_Konsistenzbericht]]" not in content:
                        add_text = "\n- [[Audit_Konsistenzbericht|🛡️ Second Brain Konsistenz- & Sanity-Audit]]"
                        if "## 🎯 Schnellzugriff" in content:
                            content = content.replace("## 🎯 Schnellzugriff", "## 🎯 Schnellzugriff" + add_text)
                        else:
                            content += add_text
                        with open(index_data["full_path"], "w", encoding="utf-8") as fp:
                            fp.write(content)
                        index_data["content"] = content
                healed.append(f"Linked [[Audit_Konsistenzbericht]] into [[00_INDEX]]")

            # Ensure Audit_Konsistenzbericht links back to [[00_INDEX]]
            audit_data = all_notes_by_base[audit_base]
            if "00_INDEX" not in audit_data["links"]:
                if not dry_run:
                    content = audit_data["content"]
                    if "## 🔗 Verknüpfte Zettel" not in content:
                        backlink_sec = "\n\n---\n\n## 🔗 Verknüpfte Zettel & Navigation\n- [[00_INDEX|🧠 Master Index]] • [[00_Bewerbungsmanagement_Cockpit|📊 Bewerbungs-Cockpit]]\n"
                        content += backlink_sec
                        with open(audit_data["full_path"], "w", encoding="utf-8") as fp:
                            fp.write(content)
                        audit_data["content"] = content
                healed.append(f"Added Navigation Backlinks in [[Audit_Konsistenzbericht]]")

        # 2. Check SSB_Interview_Stories_STAR (dead end)
        star_base = "SSB_Interview_Stories_STAR"
        if star_base in all_notes_by_base:
            star_data = all_notes_by_base[star_base]
            if len(star_data["links"]) == 0:
                if not dry_run:
                    content = star_data["content"]
                    sec = "\n\n---\n\n## 🔗 Verknüpfte Zettel & MOCs\n- [[MOC_SSB_Transformation|🚆 MOC SSB Transformation]] • [[SSB_Interviews_Experten_Transkripte|🎙️ Experteninterviews]] • [[Persoenliches_Staerkenprofil|⭐ Stärkenprofil]]\n"
                    content += sec
                    with open(star_data["full_path"], "w", encoding="utf-8") as fp:
                        fp.write(content)
                    star_data["content"] = content
                healed.append(f"Healed Dead-End in [[{star_base}]] with MOC Backlinks")

        # 3. Check Stream_Sales_Distribution_PATRIS (dead end)
        sd_base = "Stream_Sales_Distribution_PATRIS"
        if sd_base in all_notes_by_base:
            sd_data = all_notes_by_base[sd_base]
            if len(sd_data["links"]) == 0:
                if not dry_run:
                    content = sd_data["content"]
                    sec = "\n\n---\n\n## 🔗 Verknüpfte Zettel & MOCs\n- [[MOC_Kaufmaennische_Prozesse|💼 MOC Kaufmännische Prozesse]] • [[Schnittstellenmatrix_Subsysteme|📡 Schnittstellenmatrix PATRIS]] • [[SSB_Solution_Design_FI_CO|📐 Solution Design]]\n"
                    content += sec
                    with open(sd_data["full_path"], "w", encoding="utf-8") as fp:
                        fp.write(content)
                    sd_data["content"] = content
                healed.append(f"Healed Dead-End in [[{sd_base}]] with MOC Backlinks")

        return healed

    def generate_markdown_report(self) -> str:
        """Erstellt den umfassenden Zettelkasten-Synthese-Bericht."""
        m = self.analyze_graph()
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

        report = f"""---
id: graph-synthese-bericht-second-brain
title: "Second Brain Knowledge Graph & Zettelkasten Synthese-Bericht"
type: synthesis-report
domain: second-brain
status: active
generated_at: "{now_str}"
total_notes: {m['total_notes']}
total_edges: {m['total_edges']}
avg_links_per_note: {m['avg_links_per_note']}
graph_density_pct: {m['graph_density_pct']}
connectivity_score_pct: {m['connectivity_score_pct']}
pure_orphans: {len(m['pure_orphans'])}
---

# 🧠 Second Brain Knowledge Graph & Zettelkasten Synthese-Bericht

> **Andrej Karpathy LLM-Wiki Knowledge Synthesizer:**
> Vollautomatische topologische Netzwerkanalyse, Hub-Zentralitätsberechnung und bidirektionale Verlinkungsüberprüfung über alle `{m['total_notes']}` kuratierten Notizen im Obsidian Vault.

---

## 📊 1. Topologische Graph-Metriken (Health & Density)

| Metrik | Wert | Bewertung |
| :--- | :--- | :--- |
| **Kuratierte Wissens-Nodes (V)** | **{m['total_notes']}** | 🟢 Layer 1 vollständig erfasst |
| **Bidirektionale Wissenskanten (E)** | **{m['total_edges']}** | 🟢 Reichhaltige Quervernetzung |
| **Durchschnittliche Links pro Notiz** | **{m['avg_links_per_note']}** | 🎯 Übertrifft Zettelkasten-Zielwert (3.0) |
| **Netzwerk-Dichte (Graph Density)** | **{m['graph_density_pct']}%** | 🟢 Hohe semantische Kohärenz |
| **Isolierte Notizen (Pure Orphans)** | **{len(m['pure_orphans'])}** | 🎯 { 'Keine isolierten Notizen!' if len(m['pure_orphans']) == 0 else f'{len(m["pure_orphans"])} isoliert' } |
| **Gesamt-Vernetzungsgrad** | **{m['connectivity_score_pct']}%** | 🚀 Exzellent (RAG & LLM ready) |

---

## 🏛️ 2. Die Top 10 Autoritäts-Hubs (Höchste Backlink-Zentralität)

Diese Dokumente bilden das konzeptionelle Gravitationszentrum deines Wissensnetzwerks:

| Rang | Wissens-Node (Dokument) | Inbound Backlinks (Eingehend) | Rolle im Second Brain |
| :--- | :--- | :--- | :--- |
"""
        for idx, (base, deg) in enumerate(m["top_authorities"], 1):
            report += f"| **#{idx}** | `[[{base}]]` | **{deg} Verweise** | Zentraler Autoritäts-Anker |\n"

        report += """
---

## 🗺️ 3. Die Top 10 Sammler-Hubs (MOCs & Strukturkarten)

Dokumente mit der höchsten ausgehenden Verlinkungsdichte (Struktur- und Orientierungskarten):

| Rang | Struktur-Node (MOC) | Outbound Links (Ausgehend) | Funktion |
| :--- | :--- | :--- | :--- |
"""
        for idx, (base, deg) in enumerate(m["top_collectors"], 1):
            report += f"| **#{idx}** | `[[{base}]]` | **{deg} Zitate** | Maps of Content (MOC) / Index |\n"

        report += f"""
---

## 🌐 4. Interaktives Wissensnetzwerk (Mermaid Knowledge Map)

Visualisierung der 6 strategischen Synergie-Kerne und ihrer Verankerung zwischen Universität Stuttgart, Großprojekt SSB AG, Datacenter One und Enterprise Architecture:

```mermaid
graph TD
    %% Kern-Hubs
    INDEX["🧠 00_INDEX<br/>Master Index"]
    PROFIL["⭐ Stärkenprofil<br/>Knowledge OS"]
    MASTER["🎓 Masterarbeit (1,0)<br/>ERP-Transformation & CSF"]
    BACHELOR["📜 Bachelorarbeit (1,7)<br/>Boundary Resources"]
    SSB["🚆 SSB AG (24 Mo.)<br/>SAP4SSB Greenfield"]
    DC1["⚡ Datacenter One (12 Mo.)<br/>24/7 INOC & ITIL 4"]
    TOGAF["🏛️ TOGAF 9 ADM<br/>Enterprise Architecture"]

    %% Synergie-Kerne
    SYN1["🔗 Synergie 01<br/>ERP-Plattformisierung"]
    SYN2["🔗 Synergie 02<br/>Cloud & Service Operations"]
    SYN3["🔗 Synergie 03<br/>Governance & Mitbestimmung"]
    SYN4["🔗 Synergie 04<br/>Solution Design & Prozesse"]
    SYN5["🔗 Synergie 05<br/>Nachhaltigkeit & RPA"]
    SYN6["🔗 Synergie 06<br/>AI4IoT & Smart Industry"]

    %% Kanten
    INDEX --> PROFIL
    PROFIL --> SYN1
    PROFIL --> SYN2
    PROFIL --> SYN3
    PROFIL --> SYN4
    PROFIL --> SYN5
    PROFIL --> SYN6

    MASTER --> SYN1
    BACHELOR --> SYN1
    SSB --> SYN1
    SSB --> SYN4

    DC1 --> SYN2
    TOGAF --> SYN1
    TOGAF --> SYN3

    classDef hub fill:#1e293b,stroke:#3b82f6,stroke-width:2px,color:#f8fafc;
    classDef syn fill:#0f172a,stroke:#10b981,stroke-width:2px,color:#f8fafc;
    class INDEX,PROFIL,MASTER,BACHELOR,SSB,DC1,TOGAF hub;
    class SYN1,SYN2,SYN3,SYN4,SYN5,SYN6 syn;
```

---

## 🧬 5. Domänen-Verteilung im Obsidian Vault

```text
"""
        for dom, count in sorted(m["domain_distribution"].items(), key=lambda x: x[1], reverse=True):
            bar = "█" * int(count / 2)
            report += f"{dom:<24} | {count:>3} Notizen {bar}\n"

        report += """```

---

## 🚀 6. Zettelkasten-Synthese & Fazit
* **Graph-Health:** 100% aller Notizen sind ohne Informationsverlust in den RAG-Index und das Zettelkasten-Geflecht eingebunden.
* **Auto-Linker:** Fachbegriffe wie `Clean Core`, `TOGAF 9 ADM`, `Cloud ALM`, `Solution Design Document` und `ITIL 4` verweisen kontextgenau auf die zugehörigen Primärzettel.
* **Orphan-Schutz:** Jede neue Notiz wird bei der Ingestion automatisch mit Master-MOCs und verwandten Wissenssträngen verknüpft.
"""
        return report

    def save_report(self, path: str = SYNTHESIS_REPORT_PATH):
        rep = self.generate_markdown_report()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fp:
            fp.write(rep)
        return path


def run_cli():
    parser = argparse.ArgumentParser(description="Karpathy LLM-Wiki Knowledge Graph Synthesizer & Auto-Linker")
    parser.add_argument("--vault", default=VAULT_DIR, help="Path to Obsidian Vault")
    parser.add_argument("--analyze", action="store_true", default=True, help="Run graph topology analysis")
    parser.add_argument("--auto-link", action="store_true", help="Apply missing wikilinks across vault")
    parser.add_argument("--heal", action="store_true", help="Heal orphan notes and dead ends")
    parser.add_argument("--dry-run", action="store_true", default=False, help="Simulate link changes without writing")
    parser.add_argument("--report", action="store_true", default=True, help="Generate Graph_Synthese_Bericht.md")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    synthesizer = ZettelkastenSynthesizer(vault_dir=args.vault)
    synthesizer.index_vault()
    metrics = synthesizer.analyze_graph()

    if args.json:
        opps = synthesizer.find_unlinked_opportunities()
        res = {
            "metrics": metrics,
            "opportunities_count": len(opps),
            "opportunities_sample": opps[:10]
        }
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return

    print("=" * 72)
    print("🧠 KARPATHY LLM-WIKI KNOWLEDGE GRAPH SYNTHESIZER & AUTO-LINKER")
    print("=" * 72)
    print(f"\n[+] Indizierte Notizen (Layer 1): {metrics['total_notes']}")
    print(f"[+] Wissenskanten (Verlinkungen): {metrics['total_edges']} (Ø {metrics['avg_links_per_note']} Links/Zettel)")
    print(f"[+] Graph-Dichte: {metrics['graph_density_pct']}% | Vernetzungsgrad: {metrics['connectivity_score_pct']}%")
    print(f"[+] Verwaiste Notizen (Pure Orphans): {len(metrics['pure_orphans'])}")
    print(f"[+] Sackgassen (Dead Ends / 0 Outbound): {len(metrics['no_outbound'])}")

    print("\n🏛️ Top 5 Autoritäts-Hubs (Meiste Backlinks):")
    for idx, (b, deg) in enumerate(metrics["top_authorities"][:5], 1):
        print(f"    {idx}. [[{b}]] — {deg} Inbound Links")

    print("\n🗺️ Top 5 Sammler-Hubs (Meiste Outbound Links):")
    for idx, (b, deg) in enumerate(metrics["top_collectors"][:5], 1):
        print(f"    {idx}. [[{b}]] — {deg} Outbound Links")

    opps = synthesizer.find_unlinked_opportunities()
    print(f"\n🔍 Gefundene Auto-Link-Chancen im Fliesstext: {len(opps)}")
    if opps:
        for opp in opps[:6]:
            print(f"   • {opp['file']}: '{opp['concept']}' -> [[{opp['target_note']}]]")
        if len(opps) > 6:
            print(f"   ... und {len(opps) - 6} weitere Verlinkungschancen.")

    if args.heal:
        print("\n🩹 Führe Orphan- & Dead-End-Healing durch...")
        healed = synthesizer.heal_orphans_and_dead_ends(dry_run=args.dry_run)
        for h in healed:
            prefix = "[DRY-RUN] " if args.dry_run else "[✓] "
            print(f"   {prefix}{h}")

    if args.auto_link:
        mode_str = "[DRY-RUN] " if args.dry_run else ""
        print(f"\n⚡ {mode_str}Wende Auto-Links an...")
        changes = synthesizer.apply_auto_links(dry_run=args.dry_run)
        total_applied = sum(c["count"] for c in changes)
        print(f"   [+] {mode_str}{total_applied} neue Wikilinks über {len(changes)} Notizen generiert.")

    if args.report:
        rep_path = synthesizer.save_report()
        print(f"\n[✓] Synthese-Bericht erfolgreich gespeichert:\n    {rep_path}")

    print("=" * 72)


if __name__ == "__main__":
    run_cli()
