# -*- coding: utf-8 -*-
"""
Unabridged Full-Text Extractor for SSB Solution Design Document (SDD)
Parses all 794 paragraphs and all 36 tables in exact document order.
Target: C:\\Users\\SHQIPTAR634\\Documents\\Obsidian Vault\\03_SAP_EnterpriseArchitecture\\SSB_Solution_Design_Volltext.md
"""
import os
import docx
from docx.table import Table
from docx.text.paragraph import Paragraph

WS_DIR = r"c:\Users\SHQIPTAR634\Desktop\SSB Dateien"
VAULT_DIR = r"C:\Users\SHQIPTAR634\Documents\Obsidian Vault"

def extract_clean_table(tbl):
    rows = tbl.rows
    if not rows:
        return ""
    
    # Check if callout box (1x1 table)
    first_row = [c.text.strip().replace('\n', ' ') for c in rows[0].cells]
    if len(rows) == 1 and len(first_row) == 1:
        txt = first_row[0]
        if txt.startswith("ACHTUNG:"):
            txt = txt[len("ACHTUNG:"):].strip()
        return f"\n> [!WARNING] **Hinweis aus Lösungsdesign (Nagarro / SSB):**\n> {txt}\n"

    # Extract all rows, deduplicating merged horizontal cells
    cleaned_rows = []
    for r in rows:
        cleaned_cells = []
        for c in r.cells:
            t = c.text.strip().replace('\n', '<br>')
            if not cleaned_cells or cleaned_cells[-1] != t:
                cleaned_cells.append(t)
        if any(cleaned_cells):
            cleaned_rows.append(cleaned_cells)

    if not cleaned_rows:
        return ""

    # Determine max columns
    max_cols = max(len(r) for r in cleaned_rows)
    # Normalize rows
    norm_rows = []
    for r in cleaned_rows:
        while len(r) < max_cols:
            r.append("")
        norm_rows.append(r)

    # Format as Markdown table
    header = norm_rows[0]
    md_lines = []
    md_lines.append("| " + " | ".join(header) + " |")
    md_lines.append("| " + " | ".join([":---"] * max_cols) + " |")
    for r in norm_rows[1:]:
        md_lines.append("| " + " | ".join(r) + " |")

    return "\n" + "\n".join(md_lines) + "\n"

def run_sdd_unabridged():
    print("\n=== STARTING UNABRIDGED SDD FULL-TEXT EXTRACTION ===")
    sdd_path = os.path.join(WS_DIR, "01_SSB", "02_Teilprojekte_TP1_bis_TP5", "TP2_Kaufmaennische_Prozesse", "Explore_Phase", "SSB Lösungsdesign", "SSB Lösungsdesign Dokument.docx")
    doc = docx.Document(sdd_path)
    
    body_elements = []
    p_idx = 0
    t_idx = 0

    for child in doc.element.body:
        tag = child.tag.split('}')[-1]
        if tag == 'p':
            p = Paragraph(child, doc)
            txt = p.text.strip()
            if not txt:
                continue
            style = p.style.name
            if style == 'Heading 1':
                body_elements.append(f"\n# {txt}\n")
            elif style == 'Heading 2':
                body_elements.append(f"\n## {txt}\n")
            elif style == 'Heading 3':
                body_elements.append(f"\n### {txt}\n")
            elif style == 'Heading 4':
                body_elements.append(f"\n#### {txt}\n")
            else:
                body_elements.append(txt)
            p_idx += 1
        elif tag == 'tbl':
            tbl = Table(child, doc)
            md_tbl = extract_clean_table(tbl)
            if md_tbl:
                body_elements.append(md_tbl)
            t_idx += 1

    content_body = "\n\n".join(body_elements)
    
    header = f"""---
title: "SSB Solution Design Document (SDD) – Lückenloser Volltext"
program: "SAP4SSB"
phase: "Explore-Phase (100% finalisiert & genehmigt)"
total_paragraphs: {p_idx}
total_tables: {t_idx}
source_file: "file:///{sdd_path.replace('\\', '/')}"
partner: "Nagarro Enterprise Services & Axians"
tags:
  - ssb
  - s4hana
  - solution_design
  - unabridged_fulltext
  - clean_core
  - architecture
  - wricef
  - calm
---

# 📐 SSB Solution Design Document (SDD) – Vollständiges Master-Dokument

> [!IMPORTANT] **Offizieller Status bei Projektaustritt Visar Murseli**
> Dieses Dossier enthält den **vollständigen, ungekürzten Text aller {p_idx} Absätze und aller {t_idx} Tabellen** des offiziellen Lösungsdesign-Dokuments der Stuttgarter Straßenbahnen AG.
> Es dokumentiert den **erfolgreichen Abschluss der Explore-Phase** und die genehmigte Architektur für den Eintritt in die Realize-Phase (WBS 197–202).

---

{content_body}

---

## 🔗 Verknüpfungen im Wissensnetz
- [[03_SAP_EnterpriseArchitecture/SSB_Migration_Volltext]]
- [[03_SAP_EnterpriseArchitecture/SSB_Tool_Governance_CALM_EnableNow_Volltext]]
- [[03_SAP_EnterpriseArchitecture/SSB_Interviews_Experten_Transkripte]]
- [[03_SAP_EnterpriseArchitecture/01_Architektur_Technik/Clean_Core_Paradigma]]
- [[03_SAP_EnterpriseArchitecture/02_Kaufmaennische_Prozesse/Trennungsrechnung_OEPNV_EU1370]]
- [[03_SAP_EnterpriseArchitecture/02_Kaufmaennische_Prozesse/Universal_Journal_ACDOCA]]
"""

    out_path = os.path.join(VAULT_DIR, "03_SAP_EnterpriseArchitecture", "SSB_Solution_Design_Volltext.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(header)
    print(f"[OK] Successfully wrote unabridged SDD: {len(header)} chars ({p_idx} paras, {t_idx} tables).")

if __name__ == "__main__":
    run_sdd_unabridged()
