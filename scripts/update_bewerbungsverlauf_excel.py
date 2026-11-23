import os
import json
import re
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

EXCEL_PATH = r"c:\Users\SHQIPTAR634\Desktop\SSB Dateien\00_Aktuelle_Bewerbungsunterlagen\Bewerbungsverlauf.xlsx"
EMAILS_JSON = r"c:\Users\SHQIPTAR634\Desktop\SSB Dateien\00_Aktuelle_Bewerbungsunterlagen\all_application_emails.json"
COCKPIT_MD = r"C:\Users\SHQIPTAR634\Documents\Obsidian Vault\01_Karriere_Bewerbungen\00_Bewerbungsmanagement_Cockpit.md"
PIPELINE_JSON = r"c:\Users\SHQIPTAR634\Desktop\SSB Dateien\00_Aktuelle_Bewerbungsunterlagen\bewerbungen_pipeline.json"

def parse_date(date_str):
    if not date_str:
        return None
    # e.g. "Mon, 23 Nov 2026 14:30:00 +0100"
    m = re.search(r"(\d{1,2})\s+([A-Za-z]{3})\s+(\d{4})", date_str)
    if m:
        day = int(m.group(1))
        month_str = m.group(2).lower()
        year = int(m.group(3))
        months = {
            "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
            "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
            "mrz": 3, "mai": 5, "okt": 10, "dez": 12
        }
        month = months.get(month_str, 1)
        return datetime(year, month, day)
    return None

def format_date_de(dt):
    if isinstance(dt, datetime):
        return dt.strftime("%d.%m.%Y")
    return str(dt) if dt else "-"

def clean_company_name(sender, subject):
    # Known company extraction rules
    text = f"{sender} {subject}".lower()
    if "kpmg" in text:
        return "KPMG"
    elif "schwarz digits" in text or "schwarz-gruppe" in text:
        return "Schwarz Digits"
    elif "capgemini" in text:
        return "Capgemini Invent"
    elif "coop" in text:
        return "Coop-Gruppe"
    elif "msg" in text:
        return "msg systems"
    elif "horbach" in text:
        return "HORBACH"
    elif "kvjs" in text:
        return "KVJS"
    elif "communardo" in text:
        return "Communardo"
    elif "karle & brunold" in text or "karle &amp; brunold" in text:
        return "Karle & Brunold"
    elif "x1f" in text:
        return "x1F"
    elif "all for one" in text:
        return "All for One"
    elif "teamative" in text:
        return "Teamative"
    elif "axians" in text:
        return "Axians"
    elif "mercedes" in text:
        return "Mercedes-Benz"
    elif "deloitte" in text:
        return "Deloitte"
    elif "drees & sommer" in text:
        return "Drees & Sommer"
    elif "körber" in text or "koerber" in text:
        return "Körber"
    elif "convista" in text:
        return "convista"
    elif "cbs" in text:
        return "cbs"
    elif "lbbw" in text:
        return "LBBW"
    elif "thw" in text:
        return "THW"
    elif "hdm" in text:
        return "HdM Stuttgart"
        
    # Generic extraction from sender
    clean_s = re.sub(r"<[^>]+>", "", sender).strip().strip('"')
    if clean_s and len(clean_s) < 30 and not any(k in clean_s.lower() for k in ["gmx", "indeed", "stepstone", "xing", "linkedin", "noreply"]):
        return clean_s
    return None

def clean_position_title(subject):
    # Regex extract job title
    patterns = [
        r"(?:stelle\s+als|position\s+als|stelle|bewerbung\s+als|bewerbung\s+auf\s+die\s+position|bewerbung\s+auf\s+die\s+stelle|deine\s+bewerbung:\s*|deine\s+bewerbung\s+bei\s+[^:]+:\s*)([^\n\r,\.\(\)]+)",
        r"(?:für\s+die\s+position\s+)([^\n\r,\.\(\)]+)",
    ]
    for p in patterns:
        m = re.search(p, subject, re.I)
        if m:
            clean = m.group(1).strip()
            if len(clean) > 4:
                return clean
    if "junior it consultant" in subject.lower():
        return "(Junior) IT Consultant"
    if "junior sap consultant" in subject.lower():
        return "Junior SAP Consultant"
    if "bi consultant" in subject.lower():
        return "BI Consultant (80-100%)"
    if "cloud engineer" in subject.lower():
        return "Junior Cloud Engineer"
    if "sap basis" in subject.lower():
        return "SAP Basis Consultant"
    if "ai" in subject.lower():
        return "(Junior-) AI Consultant"
    return "Junior SAP / IT Consultant"

def run_reconciliation():
    if not os.path.exists(EMAILS_JSON):
        print(f"Emails JSON nicht gefunden: {EMAILS_JSON}")
        return
        
    with open(EMAILS_JSON, "r", encoding="utf-8") as f:
        emails = json.load(f)
        
    print(f"Lade {len(emails)} E-Mails zur Rechnungs- und Statusanalyse...")
    
    # 1. Parse and classify events
    company_events = {}
    
    for em in emails:
        subj = em.get("subject", "")
        sender = em.get("sender", "")
        dt = parse_date(em.get("date", ""))
        
        # Skip spam / news alerts
        subj_low = subj.lower()
        sender_low = sender.lower()
        if any(sp in subj_low or sp in sender_low for sp in [
            "gmx sicherheitshinweis", "stellenempfehlungen", "passende jobs", 
            "job-alert", "suchauftrag", "newsletter", "neue jobs", "empfehlungen für sie"
        ]):
            continue
            
        comp = clean_company_name(sender, subj)
        if not comp:
            continue
            
        pos = clean_position_title(subj)
        
        if comp not in company_events:
            company_events[comp] = {
                "company": comp,
                "position": pos,
                "submissions": [],
                "acknowledgments": [],
                "first_interviews": [],
                "second_interviews": [],
                "rejections": [],
                "offers": [],
                "latest_date": dt,
                "notes": []
            }
            
        entry = company_events[comp]
        if pos and entry["position"] == "Junior SAP / IT Consultant":
            entry["position"] = pos
            
        if dt and (not entry["latest_date"] or dt > entry["latest_date"]):
            entry["latest_date"] = dt
            
        # Classify email type
        if any(k in subj_low for k in ["einladung zum interview", "interview extension", "terminvereinbarung", "vorstellungsgespräch", "kennenlerngespräch"]):
            entry["first_interviews"].append((dt, subj))
        elif any(k in subj_low for k in ["absage", "nicht berücksichtigen", "anderweitig entschieden"]):
            entry["rejections"].append((dt, subj))
        elif any(k in subj_low for k in ["eingangsbestätigung", "deine bewerbung", "vielen dank für deine bewerbung", "vielen dank für ihre bewerbung", "bestätigung"]):
            entry["acknowledgments"].append((dt, subj))
        else:
            entry["notes"].append((dt, subj))
            
    print(f"Identifizierte Bewerbungskontakte: {len(company_events)} Unternehmen.")
    
    # 2. Load existing Bewerbungsverlauf.xlsx
    wb = openpyxl.load_workbook(EXCEL_PATH)
    ws = wb.active
    
    # Read existing rows
    existing_rows = list(ws.iter_rows(values_only=True))
    header = existing_rows[0]
    
    rows_by_comp = {}
    for r in existing_rows[1:]:
        c_name = str(r[0]).strip() if r[0] else ""
        if c_name:
            rows_by_comp[c_name.lower()] = list(r)
            
    # Update existing and add new
    for comp, data in company_events.items():
        comp_key = comp.lower()
        
        # Determine best dates & status
        ack_dt = data["acknowledgments"][0][0] if data["acknowledgments"] else None
        int1_dt = data["first_interviews"][0][0] if data["first_interviews"] else None
        rej_dt = data["rejections"][0][0] if data["rejections"] else None
        
        if int1_dt:
            status_text = f"⭐ Einladung zum Interview am {format_date_de(int1_dt)}"
        elif rej_dt:
            status_text = f"Absage am {format_date_de(rej_dt)} per E-Mail."
        elif ack_dt:
            status_text = f"Bewerbungseingang bestätigt ({format_date_de(ack_dt)})"
        else:
            status_text = "In Prüfung"
            
        # Match with existing row
        matched_key = None
        for k in rows_by_comp.keys():
            if comp_key in k or k in comp_key:
                matched_key = k
                break
                
        if matched_key:
            row = rows_by_comp[matched_key]
            # row structure: [Arbeitgeber, Stellenbeschreibung, Tag der Einreichung, Bewerbungseingang, Erstes Gesrpäch, Zweites Gespräch, Ergebnis]
            if int1_dt:
                row[4] = int1_dt
                row[6] = status_text
            elif rej_dt and not row[6]:
                row[6] = status_text
            elif ack_dt and (not row[3] or row[3] == "-"):
                row[3] = ack_dt
            if data["position"] and (not row[1] or row[1] == "-"):
                row[1] = data["position"]
        else:
            # Create new row
            sub_dt = ack_dt or data["latest_date"]
            new_row = [
                comp,
                data["position"],
                sub_dt,
                ack_dt or "-",
                int1_dt or "-",
                "-",
                status_text
            ]
            rows_by_comp[comp_key] = new_row
            
    # Rebuild Excel Sheet
    wb.remove(ws)
    new_ws = wb.create_sheet(title="Bewerbungsverlauf")
    
    # Styles
    navy_fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    white_font = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
    zebra_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    highlight_interview = PatternFill(start_color="ECFDF5", end_color="ECFDF5", fill_type="solid")
    green_font = Font(name="Segoe UI", size=10, bold=True, color="047857")
    reg_font = Font(name="Segoe UI", size=10)
    center_align = Alignment(horizontal="center", vertical="center")
    left_align = Alignment(horizontal="left", vertical="center")
    thin_border = Border(
        left=Side(style="thin", color="E2E8F0"),
        right=Side(style="thin", color="E2E8F0"),
        top=Side(style="thin", color="E2E8F0"),
        bottom=Side(style="thin", color="E2E8F0")
    )
    
    # Header
    col_headers = [
        "Arbeitgeber", "Stellenbeschreibung", "Tag der Einreichung", 
        "Bewerbungseingang", "1. Gespräch", "2. Gespräch", "Status / Ergebnis"
    ]
    new_ws.append(col_headers)
    new_ws.row_dimensions[1].height = 28
    
    for c_idx in range(1, len(col_headers) + 1):
        cell = new_ws.cell(row=1, column=c_idx)
        cell.fill = navy_fill
        cell.font = white_font
        cell.alignment = center_align
        cell.border = thin_border
        
    # Sort rows by submission date (newest first)
    all_sorted_rows = list(rows_by_comp.values())
    def sort_key(r):
        d = r[2]
        if isinstance(d, datetime):
            return d
        return datetime(2024, 1, 1)
    all_sorted_rows.sort(key=sort_key, reverse=True)
    
    # Write data rows
    for r_idx, r_data in enumerate(all_sorted_rows, start=2):
        new_ws.row_dimensions[r_idx].height = 22
        is_interview = "interview" in str(r_data[6]).lower() or r_data[4] not in ["-", None]
        is_even = (r_idx % 2 == 0)
        
        for c_idx, val in enumerate(r_data, start=1):
            cell = new_ws.cell(row=r_idx, column=c_idx)
            cell.border = thin_border
            
            # Formatting values
            if isinstance(val, datetime):
                cell.value = val.strftime("%d.%m.%Y")
                cell.alignment = center_align
            elif val is None:
                cell.value = "-"
                cell.alignment = center_align
            else:
                cell.value = str(val)
                cell.alignment = center_align if c_idx in [3, 4, 5, 6] else left_align
                
            if is_interview:
                cell.fill = highlight_interview
                cell.font = green_font if c_idx in [1, 5, 7] else reg_font
            elif is_even:
                cell.fill = zebra_fill
                cell.font = reg_font
            else:
                cell.font = reg_font
                
    # Auto-adjust column widths
    for col in new_ws.columns:
        max_len = max(len(str(cell.value or "")) for cell in col)
        col_letter = get_column_letter(col[0].column)
        new_ws.column_dimensions[col_letter].width = max(max_len + 4, 14)
        
    wb.save(EXCEL_PATH)
    print(f"✅ Bewerbungsverlauf.xlsx erfolgreich aktualisiert: {len(all_sorted_rows)} Bewerbungen eingetragen!")
    
    # 3. Synchronize Obsidian Cockpit Markdown
    table_lines = [
        "| Arbeitgeber | Stellenbezeichnung | Datum | Bewerbungseingang | 1. Gespräch | 2. Gespräch | Status / Feedback |",
        "| :--- | :--- | :---: | :---: | :---: | :---: | :--- |"
    ]
    for r in all_sorted_rows:
        comp = f"**{r[0]}**"
        pos = str(r[1] or "-")
        dt_sub = format_date_de(r[2])
        dt_ack = format_date_de(r[3])
        dt_int1 = format_date_de(r[4])
        dt_int2 = format_date_de(r[5])
        status = str(r[6] or "-")
        table_lines.append(f"| {comp} | {pos} | {dt_sub} | {dt_ack} | {dt_int1} | {dt_int2} | {status} |")
        
    table_md = "\n".join(table_lines)
    
    if os.path.exists(COCKPIT_MD):
        with open(COCKPIT_MD, "r", encoding="utf-8") as f:
            md_content = f.read()
            
        # Replace table in markdown
        start_token = "## 📋 Status-Matrix der Bewerbungen"
        end_token = "## 🎯 Strategische Learnings für anstehende Gespräche"
        
        if start_token in md_content and end_token in md_content:
            before = md_content.split(start_token)[0]
            after = md_content.split(end_token)[1]
            new_md = before + start_token + "\n\n" + table_md + "\n\n---\n\n## 🎯 Strategische Learnings für anstehende Gespräche" + after
            with open(COCKPIT_MD, "w", encoding="utf-8") as f:
                f.write(new_md)
            print(f"✅ Obsidian-Cockpit synchronisiert: {COCKPIT_MD}")
            
    # 4. Save JSON Pipeline
    pipeline_records = []
    for r in all_sorted_rows:
        pipeline_records.append({
            "employer": r[0],
            "position": r[1],
            "submission_date": format_date_de(r[2]),
            "ack_date": format_date_de(r[3]),
            "interview_1": format_date_de(r[4]),
            "interview_2": format_date_de(r[5]),
            "status": r[6]
        })
    with open(PIPELINE_JSON, "w", encoding="utf-8") as f:
        json.dump(pipeline_records, f, indent=2, ensure_ascii=False)
    print(f"✅ JSON-Pipeline exportiert: {PIPELINE_JSON}")

if __name__ == "__main__":
    run_reconciliation()
