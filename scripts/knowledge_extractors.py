# -*- coding: utf-8 -*-
"""
Multi-Format Knowledge Extractor Protocol
Extracts clean, structured text and tables from PDF, DOCX, PPTX, XLSX, and text files.
Author: Visar Murseli, M.Sc. | Data Science & Enterprise AI Architect
"""

import os
import re
from pypdf import PdfReader
from docx import Document
from pptx import Presentation
import openpyxl

def clean_text(text):
    if not text:
        return ""
    # Sanitize lone surrogates or unencodable characters
    text = text.encode('utf-8', 'replace').decode('utf-8')
    # Normalize excessive whitespace while preserving paragraph breaks
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def extract_pdf(path, max_pages=None):
    """Extracts text page-by-page from a PDF file."""
    try:
        reader = PdfReader(path)
        pages_text = []
        num_pages = len(reader.pages)
        limit = min(num_pages, max_pages) if max_pages else num_pages
        
        for idx in range(limit):
            try:
                page = reader.pages[idx]
                t = page.extract_text()
                if t and t.strip():
                    pages_text.append(f"#### Seite {idx + 1}\n{clean_text(t)}")
            except Exception as e:
                pages_text.append(f"#### Seite {idx + 1}\n*[Text auf Seite {idx + 1} konnte nicht extrahiert werden]*")
                
        full = "\n\n".join(pages_text)
        return {
            "success": True,
            "num_pages": num_pages,
            "text": full,
            "chars": len(full)
        }
    except Exception as e:
        return {"success": False, "error": str(e), "text": "", "chars": 0}

def extract_docx(path):
    """Extracts headings, paragraphs, and tables from a DOCX file."""
    try:
        doc = Document(path)
        blocks = []
        
        for para in doc.paragraphs:
            t = para.text.strip()
            if not t:
                continue
            style_name = para.style.name.lower() if para.style else ""
            if "heading 1" in style_name:
                blocks.append(f"### {t}")
            elif "heading 2" in style_name:
                blocks.append(f"#### {t}")
            elif "heading 3" in style_name:
                blocks.append(f"##### {t}")
            elif "bullet" in style_name or "list" in style_name:
                blocks.append(f"- {t}")
            else:
                blocks.append(t)
                
        # Extract tables
        for t_idx, table in enumerate(doc.tables):
            rows_data = []
            for row in table.rows:
                cells = [clean_text(c.text.replace("\n", " ")) for c in row.cells]
                rows_data.append(cells)
            if rows_data and len(rows_data) > 1:
                col_count = len(rows_data[0])
                # Deduplicate identical cells in row (merged cells)
                header = "| " + " | ".join(rows_data[0]) + " |"
                sep = "| " + " | ".join([":---"] * col_count) + " |"
                body_rows = ["| " + " | ".join(r[:col_count]) + " |" for r in rows_data[1:25]]
                table_md = "\n".join([f"**Tabelle {t_idx + 1}:**", header, sep] + body_rows)
                blocks.append(table_md)
                
        full = "\n\n".join(blocks)
        return {
            "success": True,
            "num_paragraphs": len(doc.paragraphs),
            "num_tables": len(doc.tables),
            "text": clean_text(full),
            "chars": len(full)
        }
    except Exception as e:
        return {"success": False, "error": str(e), "text": "", "chars": 0}

def extract_pptx(path):
    """Extracts slides, titles, shapes, bullets, and speaker notes from a PPTX file."""
    try:
        prs = Presentation(path)
        slides_text = []
        
        for s_idx, slide in enumerate(prs.slides):
            slide_parts = []
            title = ""
            if slide.shapes.title and slide.shapes.title.text:
                title = clean_text(slide.shapes.title.text)
                
            header = f"#### Folie {s_idx + 1}: {title}" if title else f"#### Folie {s_idx + 1}"
            slide_parts.append(header)
            
            for shape in slide.shapes:
                if shape == slide.shapes.title:
                    continue
                if shape.has_text_frame:
                    for para in shape.text_frame.paragraphs:
                        t = clean_text(para.text)
                        if t:
                            slide_parts.append(f"- {t}")
                elif shape.has_table:
                    table = shape.table
                    rows_data = []
                    for row in table.rows:
                        cells = [clean_text(c.text.replace("\n", " ")) for c in row.cells]
                        rows_data.append(cells)
                    if rows_data and len(rows_data) > 1:
                        col_count = len(rows_data[0])
                        header_md = "| " + " | ".join(rows_data[0]) + " |"
                        sep = "| " + " | ".join([":---"] * col_count) + " |"
                        body_rows = ["| " + " | ".join(r[:col_count]) + " |" for r in rows_data[1:15]]
                        slide_parts.append("\n".join([header_md, sep] + body_rows))
                        
            # Speaker notes
            if slide.has_notes_slide and slide.notes_slide.notes_text_frame:
                notes = clean_text(slide.notes_slide.notes_text_frame.text)
                if notes:
                    slide_parts.append(f"> 💬 *Referenten-Notiz:* {notes}")
                    
            slides_text.append("\n".join(slide_parts))
            
        full = "\n\n---\n\n".join(slides_text)
        return {
            "success": True,
            "num_slides": len(prs.slides),
            "text": clean_text(full),
            "chars": len(full)
        }
    except Exception as e:
        return {"success": False, "error": str(e), "text": "", "chars": 0}

def extract_xlsx(path, max_rows=30):
    """Extracts sheet names, headers, and top summary rows from an XLSX file."""
    try:
        wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
        sheets_text = []
        
        for sheetname in wb.sheetnames:
            ws = wb[sheetname]
            rows_data = []
            row_count = 0
            empty_streak = 0
            # Guard against worksheets formatted down to 1,048,576 rows
            for row in ws.iter_rows(values_only=True, max_row=max_rows * 3):
                if any(v is not None and str(v).strip() != "" for v in row):
                    cells = [str(v).strip() if v is not None else "" for v in row]
                    # Trim empty trailing cells
                    while cells and cells[-1] == "":
                        cells.pop()
                    if cells:
                        rows_data.append(cells)
                        row_count += 1
                        empty_streak = 0
                else:
                    empty_streak += 1
                    if empty_streak >= 10:
                        break
                if row_count >= max_rows:
                    break
                    
            if rows_data:
                col_count = max(len(r) for r in rows_data)
                # Normalize length
                norm_rows = [r + [""] * (col_count - len(r)) for r in rows_data]
                header = "| " + " | ".join(norm_rows[0]) + " |"
                sep = "| " + " | ".join([":---"] * col_count) + " |"
                body = ["| " + " | ".join(r) + " |" for r in norm_rows[1:]]
                sheet_md = f"#### Tabellenblatt: `{sheetname}` ({row_count} Zeilen)\n" + "\n".join([header, sep] + body)
                sheets_text.append(sheet_md)
                
        full = "\n\n".join(sheets_text)
        return {
            "success": True,
            "num_sheets": len(wb.sheetnames),
            "text": clean_text(full),
            "chars": len(full)
        }
    except Exception as e:
        return {"success": False, "error": str(e), "text": "", "chars": 0}

def extract_generic_text(path):
    """Reads plain text, markdown, json, or html with encoding detection."""
    for enc in ["utf-8", "cp1252", "latin-1", "iso-8859-1"]:
        try:
            with open(path, "r", encoding=enc) as f:
                content = f.read()
            return {"success": True, "text": clean_text(content), "chars": len(content)}
        except UnicodeDecodeError:
            continue
        except Exception as e:
            return {"success": False, "error": str(e), "text": "", "chars": 0}
    return {"success": False, "error": "Unable to decode text file", "text": "", "chars": 0}

def extract_document(path):
    """Master dispatcher that extracts text based on file extension."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return extract_pdf(path)
    elif ext == ".docx":
        return extract_docx(path)
    elif ext == ".pptx":
        return extract_pptx(path)
    elif ext in [".xlsx", ".xlsm"]:
        return extract_xlsx(path)
    elif ext in [".txt", ".md", ".json", ".html", ".csv", ".py", ".sql"]:
        return extract_generic_text(path)
    else:
        return {"success": False, "error": f"Unsupported format: {ext}", "text": "", "chars": 0}
