# -*- coding: utf-8 -*-
"""High-fidelity V2 document extractors for the Obsidian Career OS pipeline.

Supports PDF (PyMuPDF reading-order blocks, outline TOC, selective pdfplumber tables,
and RapidOCR fallback on image/scan pages), DOCX (interleaved paragraphs, tables,
and textboxes), legacy Word .doc (OLE piece-table parser), ODT, PPTX (recursive
group shapes, tables, speaker notes), XLSX/XLSM/CSV, Outlook .msg (including
non-image attachments), MS Visio .vsdx, MS Project .mpp OLE tasks, HTML, and text/code.
"""

from __future__ import annotations

import atexit
import csv
import hashlib
import io
import os
import posixpath
import re
import struct
import subprocess
import tempfile
import unicodedata
import zipfile
import xml.etree.ElementTree as ET
from collections import Counter
from typing import Any

import docx
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table
from docx.text.paragraph import Paragraph
import extract_msg
import olefile
import openpyxl
import pdfplumber
from PIL import Image
import pptx
from pptx.enum.shapes import MSO_SHAPE_TYPE
import pymupdf
from bs4 import BeautifulSoup

os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
from rapidocr_onnxruntime import RapidOCR

pymupdf.TOOLS.mupdf_display_errors(False)

_RAPID_OCR_ENGINE: RapidOCR | None = None
_WIN_OCR_BRIDGE: "_WinOcrBridge | None" = None
_WIN_OCR_MAX_DIM = 2200

_WIN_OCR_PS_SCRIPT = r"""
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
Function Await($WinRtTask, $ResultType) {
    $asTask = $asTaskGeneric.MakeGenericMethod($ResultType)
    $netTask = $asTask.Invoke($null, @($WinRtTask))
    $netTask.Wait(-1) | Out-Null
    $netTask.Result
}
[Windows.Storage.StorageFile, Windows.Storage, ContentType=WindowsRuntime] | Out-Null
[Windows.Graphics.Imaging.BitmapDecoder, Windows.Graphics.Imaging, ContentType=WindowsRuntime] | Out-Null
[Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType=WindowsRuntime] | Out-Null
[Windows.Globalization.Language, Windows.Foundation, ContentType=WindowsRuntime] | Out-Null

$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage((New-Object Windows.Globalization.Language("de-DE")))
if ($null -eq $engine) {
    $avail = [Windows.Media.Ocr.OcrEngine]::AvailableRecognizerLanguages
    if ($avail.Count -gt 0) {
        $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage($avail[0])
    }
}
if ($null -eq $engine) {
    Write-Output "__WINOCR_UNAVAILABLE__"
    exit 1
}
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
Write-Output ("__WINOCR_READY__:" + $engine.RecognizerLanguage.LanguageTag)

while (($line = [Console]::In.ReadLine()) -ne $null) {
    $p = $line.Trim()
    if ($p -eq "__QUIT__") { break }
    if ($p -eq "") { continue }
    $parts = $p -split "\|", 2
    $imgPath = $parts[0]
    $outPath = $parts[1]
    try {
        $file = Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($imgPath)) ([Windows.Storage.StorageFile])
        $stream = Await ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
        $decoder = Await ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
        $bitmap = Await ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
        $res = Await ($engine.RecognizeAsync($bitmap)) ([Windows.Media.Ocr.OcrResult])
        $linesOut = @()
        foreach ($ln in $res.Lines) { $linesOut += $ln.Text }
        [System.IO.File]::WriteAllText($outPath, ($linesOut -join "`n"), $utf8NoBom)
        Write-Output "===WINOCR_OK==="
        $bitmap.Dispose()
        $stream.Dispose()
    } catch {
        [System.IO.File]::WriteAllText($outPath, "", $utf8NoBom)
        Write-Output ("===WINOCR_ERR===" + $_.Exception.Message)
    }
}
"""


class _WinOcrBridge:
    """Persistent native Windows.Media.Ocr subprocess bridge (fast, preserves German umlauts & spaces)."""

    def __init__(self) -> None:
        self._proc: subprocess.Popen[str] | None = None
        self._available = False
        self._seq = 0
        tmp_dir = tempfile.gettempdir()
        self._tmp_dir = tmp_dir
        self._pid = os.getpid()
        self._tmp_img = os.path.join(tmp_dir, f"careeros_winocr_{self._pid}_0.png")
        self._tmp_txt = os.path.join(tmp_dir, f"careeros_winocr_{self._pid}.txt")
        self._start()

    def _start(self) -> None:
        if os.name != "nt":
            return
        try:
            flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
            self._proc = subprocess.Popen(
                ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", _WIN_OCR_PS_SCRIPT],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                encoding="utf-8",
                errors="replace",
                creationflags=flags,
            )
            ready = self._proc.stdout.readline().strip() if self._proc.stdout else ""
            self._available = ready.startswith("__WINOCR_READY__")
            if not self._available:
                self.close()
        except Exception:
            self.close()

    @property
    def available(self) -> bool:
        return self._available and self._proc is not None and self._proc.poll() is None

    def recognize_png_bytes(self, img_bytes: bytes) -> str | None:
        """Runs WinRT OCR on image bytes, rotating temp slots to avoid WinRT/AV file locks."""
        if not self.available:
            self._start()
        if not self.available or self._proc is None or self._proc.stdin is None or self._proc.stdout is None:
            return None
        slot = self._seq % 8
        self._seq += 1
        img_path = os.path.join(self._tmp_dir, f"careeros_winocr_{self._pid}_{slot}.png")
        try:
            with Image.open(io.BytesIO(img_bytes)) as im:
                w, h = im.size
                if w < 16 or h < 16:
                    return ""
                if max(w, h) > _WIN_OCR_MAX_DIM:
                    scale = float(_WIN_OCR_MAX_DIM) / float(max(w, h))
                    im = im.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.Resampling.LANCZOS)
                if im.mode not in ("RGB", "L"):
                    im = im.convert("RGB")
                im.save(img_path, format="PNG")
        except Exception:
            return None

        try:
            self._proc.stdin.write(f"{img_path}|{self._tmp_txt}\n")
            self._proc.stdin.flush()
            status = self._proc.stdout.readline()
            if not status:
                self._available = False
                return None
            if status.startswith("===WINOCR_OK===") and os.path.exists(self._tmp_txt):
                with open(self._tmp_txt, "r", encoding="utf-8", errors="replace") as f:
                    return f.read().strip()
            if status.startswith("===WINOCR_ERR==="):
                return None
            return ""
        except Exception:
            self._available = False
            return None

    def close(self) -> None:
        if self._proc is not None:
            try:
                if self._proc.stdin and self._proc.poll() is None:
                    self._proc.stdin.write("__QUIT__\n")
                    self._proc.stdin.flush()
                self._proc.wait(timeout=3)
            except Exception:
                try:
                    self._proc.kill()
                except Exception:
                    pass
            self._proc = None
        self._available = False
        for slot in range(8):
            p = os.path.join(self._tmp_dir, f"careeros_winocr_{self._pid}_{slot}.png")
            if os.path.exists(p):
                try:
                    os.remove(p)
                except Exception:
                    pass
        if os.path.exists(self._tmp_txt):
            try:
                os.remove(self._tmp_txt)
            except Exception:
                pass


def _close_win_ocr() -> None:
    global _WIN_OCR_BRIDGE
    if _WIN_OCR_BRIDGE is not None:
        _WIN_OCR_BRIDGE.close()
        _WIN_OCR_BRIDGE = None


atexit.register(_close_win_ocr)


def _get_rapid_ocr() -> RapidOCR:
    """Lazily initializes a process-local RapidOCR fallback tuned to 2 threads."""
    global _RAPID_OCR_ENGINE
    if _RAPID_OCR_ENGINE is None:
        _RAPID_OCR_ENGINE = RapidOCR(
            use_cls=False,
            det_intra_op_num_threads=2,
            rec_intra_op_num_threads=2,
        )
    return _RAPID_OCR_ENGINE


def _ocr_image_bytes(img_bytes: bytes) -> str:
    """Extracts text from raster bytes via native Windows OCR with RapidOCR fallback only on error."""
    global _WIN_OCR_BRIDGE
    if _WIN_OCR_BRIDGE is None:
        _WIN_OCR_BRIDGE = _WinOcrBridge()
    if _WIN_OCR_BRIDGE.available:
        txt = _WIN_OCR_BRIDGE.recognize_png_bytes(img_bytes)
        if txt is not None:
            return txt

    ocr = _get_rapid_ocr()
    res, _ = ocr(img_bytes)
    if not res:
        return ""
    sorted_items = sorted(res, key=lambda item: (round(item[0][0][1] / 12.0), item[0][0][0]))
    return "\n".join(item[1].strip() for item in sorted_items if len(item) >= 2 and item[1].strip())


# ---------------------------------------------------------------------------
# Shared Text Normalization & Markdown Hygiene Helpers
# ---------------------------------------------------------------------------

_LIGATURE_TABLE = str.maketrans({
    "\ufb00": "ff",   # ﬀ
    "\ufb01": "fi",   # ﬁ
    "\ufb02": "fl",   # ﬂ
    "\ufb03": "ffi",  # ﬃ
    "\ufb04": "ffl",  # ﬄ
    "\ufb05": "st",   # ﬅ
    "\ufb06": "st",   # ﬆ
    "\u2028": "\n",
    "\u2029": "\n\n",
})


def clean_text(text: str) -> str:
    """Applies Unicode NFC, expands PDF typographic ligatures, strips soft hyphens & control chars."""
    if not text:
        return ""
    text = unicodedata.normalize("NFC", text)
    text = text.translate(_LIGATURE_TABLE)
    text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\u00a0", " ")
    # Join soft-hyphen line breaks before removing remaining stray U+00AD soft hyphens
    text = re.sub(r"([A-Za-zÄÖÜäöüß]{2,})\u00ad[ \t]*\n+[ \t]*([a-zäöüß]{2,})", r"\1\2", text)
    text = text.replace("\u00ad", "")
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f\u200b\u200c\u200d\ufeff]", "", text)
    lines = [ln.rstrip() for ln in text.split("\n")]
    out = "\n".join(lines)
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out.strip()


def dehyphenate_text(text: str) -> str:
    """Rejoins hyphenated line-wraps in prose (e.g. 'Ent-\\nwicklung' -> 'Entwicklung')."""
    if not text:
        return ""
    return re.sub(r"([a-zäöüß]{2,})[-\u2010][ \t]*\n+[ \t]*([a-zäöüß]{2,})", r"\1\2", text)


def neutralize_stray_brackets(text: str) -> str:
    """Converts literal [[...]] in extracted raw sources to `⟦...⟧` to avoid broken wikilinks."""
    if not text or "[[" not in text:
        return text
    return re.sub(r"\[\[(.*?)\]\]", r"⟦\1⟧", text, flags=re.DOTALL)


def normalize_body_headings(text: str, min_level: int = 2) -> str:
    """Demotes headings ONLY if the extracted body contains top-level `# ` H1 headings."""
    if not text:
        return ""
    lines = text.splitlines()
    in_fence = False
    has_h1 = False
    for ln in lines:
        if ln.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence and re.match(r"^#\s+\S", ln):
            has_h1 = True
            break
    if not has_h1:
        return text

    in_fence = False
    out: list[str] = []
    shift = max(1, min_level - 1)
    for ln in lines:
        stripped = ln.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            out.append(ln)
            continue
        if not in_fence:
            m = re.match(r"^(#{1,6})\s+(.*)$", ln)
            if m:
                level = min(6, len(m.group(1)) + shift)
                out.append(f"{'#' * level} {m.group(2).strip()}")
                continue
        out.append(ln)
    return "\n".join(out)


_PLACEHOLDER_PATTERNS = {
    "geben sie ihren untertitel ein",
    "klicken sie, um text hinzuzufügen",
    "click to add title",
    "click to add subtitle",
    "click to add text",
    "um diesen platzhaltertext zu ersetzen, klicken sie darauf, und beginnen sie mit der eingabe.",
}


def _is_boilerplate_placeholder(text: str) -> bool:
    return clean_text(text).lower() in _PLACEHOLDER_PATTERNS


def finalize_markdown_body(raw_text: str) -> str:
    """Runs standard cleaning, dehyphenation, heading demotion, and bracket safety."""
    txt = clean_text(raw_text)
    txt = dehyphenate_text(txt)
    txt = normalize_body_headings(txt, min_level=2)
    txt = neutralize_stray_brackets(txt)
    return txt.strip()


def format_markdown_table(rows: list[list[Any]], max_cell_len: int = 220) -> str:
    """Formats a 2D list of rows as a valid GFM Markdown table."""
    if not rows:
        return ""
    clean_rows: list[list[str]] = []
    max_cols = 0
    for row in rows:
        cleaned = []
        for c in row:
            val = "" if c is None else str(c)
            val = clean_text(val).replace("\n", " ").replace("|", "\\|")
            val = re.sub(r"\s{2,}", " ", val).strip()
            if len(val) > max_cell_len:
                val = val[: max_cell_len - 1] + "…"
            cleaned.append(val)
        if any(cleaned):
            max_cols = max(max_cols, len(cleaned))
            clean_rows.append(cleaned)
    if not clean_rows or max_cols == 0:
        return ""
    norm = [r + [""] * (max_cols - len(r)) for r in clean_rows]
    header = norm[0]
    sep = ["---"] * max_cols
    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(sep) + " |",
    ]
    for r in norm[1:]:
        lines.append("| " + " | ".join(r) + " |")
    return "\n".join(lines)


def _normalize_hf_candidate(line: str) -> str:
    s = re.sub(r"\b\d+\b", "#", line.strip())
    return re.sub(r"\s+", " ", s).strip()


def strip_repeating_headers_footers(pages_texts: list[str]) -> list[str]:
    """Removes running page headers/footers and bare page numbers appearing across >=50% of pages."""
    n_pages = len(pages_texts)
    if n_pages < 4:
        return pages_texts

    top_counts: Counter[str] = Counter()
    bot_counts: Counter[str] = Counter()
    split_pages: list[list[str]] = []

    for txt in pages_texts:
        lines = [ln for ln in txt.splitlines() if ln.strip()]
        split_pages.append(lines)
        for ln in lines[:2]:
            norm = _normalize_hf_candidate(ln)
            if 4 <= len(norm) <= 120:
                top_counts[norm] += 1
        for ln in lines[-2:]:
            norm = _normalize_hf_candidate(ln)
            if 4 <= len(norm) <= 120:
                bot_counts[norm] += 1

    min_hits = max(3, int(n_pages * 0.45))
    rep_top = {k for k, v in top_counts.items() if v >= min_hits}
    rep_bot = {k for k, v in bot_counts.items() if v >= min_hits}
    bare_pagenum = re.compile(r"^(?:seite|page|folie|slide)?\s*\d+(?:\s*(?:/|of|von)\s*\d+)?\s*$", re.I)

    cleaned_pages: list[str] = []
    for lines in split_pages:
        if not lines:
            cleaned_pages.append("")
            continue
        start = 0
        while start < min(2, len(lines)):
            cand = lines[start].strip()
            if _normalize_hf_candidate(cand) in rep_top or bare_pagenum.match(cand):
                start += 1
            else:
                break
        end = len(lines)
        while end > start and end > len(lines) - 2:
            cand = lines[end - 1].strip()
            if _normalize_hf_candidate(cand) in rep_bot or bare_pagenum.match(cand):
                end -= 1
            else:
                break
        cleaned_pages.append("\n".join(lines[start:end]))
    return cleaned_pages


def _make_result(
    fmt: str,
    body_md: str,
    units: int = 1,
    ocr_pages: int = 0,
    toc_entries: int = 0,
    tables_count: int = 0,
    meta: dict[str, Any] | None = None,
    error: str | None = None,
) -> dict[str, Any]:
    final_body = finalize_markdown_body(body_md) if body_md else ""
    words = len(final_body.split()) if final_body else 0
    return {
        "success": error is None and bool(final_body),
        "format": fmt,
        "text": final_body,
        "chars": len(final_body),
        "words": words,
        "pages_or_units": units,
        "ocr_pages": ocr_pages,
        "toc_entries": toc_entries,
        "tables_count": tables_count,
        "meta": meta or {},
        "error": error,
    }


# ---------------------------------------------------------------------------
# PDF Extractor V2 (PyMuPDF Reading-Order + Outline TOC + pdfplumber + OCR)
# ---------------------------------------------------------------------------

def _ocr_pymupdf_page(page: pymupdf.Page, target_max_px: int = 1600) -> str:
    """Renders a PDF page up to target_max_px and OCRs via Windows.Media.Ocr (or RapidOCR fallback)."""
    max_dim = max(1.0, float(page.rect.width), float(page.rect.height))
    zoom = min(2.0, float(target_max_px) / max_dim)
    pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), colorspace=pymupdf.csRGB)
    return _ocr_image_bytes(pix.tobytes("png"))


def _extract_pdf_bytes_or_path(
    source: str | bytes,
    ext_label: str = "pdf",
    ocr_max_pages: int = 80,
    enable_ocr: bool = True,
) -> dict[str, Any]:
    doc = None
    plumber_doc = None
    try:
        if isinstance(source, bytes):
            doc = pymupdf.open(stream=source, filetype="pdf")
        else:
            doc = pymupdf.open(source)

        page_count = doc.page_count
        if page_count == 0:
            return _make_result(ext_label, "", units=0)

        meta_raw = doc.metadata or {}
        pdf_meta = {
            k: clean_text(str(v))
            for k, v in meta_raw.items()
            if k in ("title", "author", "subject", "creator") and v and str(v).strip()
        }

        toc_raw = doc.get_toc(simple=True) or []
        toc_by_page: dict[int, list[tuple[int, str]]] = {}
        for item in toc_raw:
            if len(item) >= 3:
                lvl, ttl, pg_num = int(item[0]), clean_text(str(item[1])), int(item[2])
                if ttl and 1 <= pg_num <= page_count:
                    toc_by_page.setdefault(pg_num - 1, []).append((lvl, ttl))

        raw_page_texts: list[str] = []
        ocr_used: list[int] = []
        low_visual_pages = 0
        table_candidates: dict[int, list[str]] = {}
        total_tables = 0

        # Selective pdfplumber table extraction for non-mega portrait docs with vector rules
        use_plumber = isinstance(source, str) and page_count <= 45
        eff_ocr_cap = ocr_max_pages if page_count <= 60 else min(ocr_max_pages, 15)
        for p_idx in range(page_count):
            page = doc[p_idx]
            blocks = page.get_text("blocks", sort=True)
            txt_parts = [clean_text(b[4]) for b in blocks if len(b) >= 7 and b[6] == 0 and b[4].strip()]
            pg_txt = "\n\n".join(txt_parts)

            non_ws = len(re.sub(r"\s+", "", pg_txt))
            if non_ws < 40:
                has_visual = bool(page.get_images(full=False)) or len(page.get_drawings()) > 8
                if has_visual:
                    low_visual_pages += 1
                    if enable_ocr and len(ocr_used) < eff_ocr_cap:
                        try:
                            ocr_txt = _ocr_pymupdf_page(page, target_max_px=1600)
                            if len(re.sub(r"\s+", "", ocr_txt)) > non_ws:
                                pg_txt = ocr_txt
                                ocr_used.append(p_idx + 1)
                        except Exception:
                            pass

            # Bounded table extraction with pdfplumber only when ruled lines look tabular
            if use_plumber and non_ws >= 40 and page.rect.height >= page.rect.width * 0.9:
                drawings_cnt = len(page.get_drawings())
                if 6 <= drawings_cnt <= 220:
                    try:
                        if plumber_doc is None:
                            plumber_doc = pdfplumber.open(source)
                        p_pg = plumber_doc.pages[p_idx]
                        if len(p_pg.lines) >= 3 or len(p_pg.rects) >= 2:
                            extracted_tabs = p_pg.extract_tables() or []
                            rendered_tabs = []
                            for t in extracted_tabs:
                                if t and len(t) >= 2 and max(len(r) for r in t) >= 2:
                                    md_t = format_markdown_table(t)
                                    if md_t:
                                        rendered_tabs.append(md_t)
                                        total_tables += 1
                            if rendered_tabs:
                                table_candidates[p_idx] = rendered_tabs
                    except Exception:
                        pass

            raw_page_texts.append(pg_txt)

        cleaned_pages = strip_repeating_headers_footers(raw_page_texts)

        sections: list[str] = []
        # Add concise TOC overview for large multi-chapter PDFs
        toc_overview = [
            f"{'  ' * (max(0, min(2, int(it[0]) - 1)))}- S. {int(it[2])}: {clean_text(str(it[1]))}"
            for it in toc_raw
            if len(it) >= 3 and int(it[0]) <= 2 and clean_text(str(it[1]))
        ]
        if len(toc_overview) >= 5:
            capped_toc = toc_overview[:60]
            if len(toc_overview) > 60:
                capped_toc.append(f"- … (+{len(toc_overview) - 60} weitere Lesezeichen)")
            sections.append("## Inhaltsverzeichnis (PDF-Lesezeichen)\n\n" + "\n".join(capped_toc))

        ocr_set = set(ocr_used)
        for p_idx, pg_body in enumerate(cleaned_pages):
            pg_num = p_idx + 1
            pg_chunks: list[str] = []
            for lvl, ttl in toc_by_page.get(p_idx, []):
                h_lvl = min(4, max(2, lvl + 1))
                pg_chunks.append(f"{'#' * h_lvl} {ttl}")

            clean_b = pg_body.strip()
            tabs = table_candidates.get(p_idx, [])
            if not clean_b and not tabs:
                continue

            if page_count > 1:
                badge = " *(OCR)*" if pg_num in ocr_set else ""
                pg_chunks.append(f"### Seite {pg_num}{badge}")
            if clean_b:
                pg_chunks.append(clean_b)
            if tabs:
                pg_chunks.append("#### Strukturierte Tabellen (Seite " + str(pg_num) + ")\n\n" + "\n\n".join(tabs))
            sections.append("\n\n".join(pg_chunks))

        full_md = "\n\n".join(sections)
        if not full_md.strip():
            full_md = f"*(Visuelles PDF mit {page_count} Seite(n) ohne erkennbaren Textinhalt)*"

        pdf_meta["low_visual_pages"] = low_visual_pages
        return _make_result(
            ext_label,
            full_md,
            units=page_count,
            ocr_pages=len(ocr_used),
            toc_entries=len(toc_raw),
            tables_count=total_tables,
            meta=pdf_meta,
        )
    except Exception as exc:
        return _make_result(ext_label, "", error=f"PDF error: {exc}")
    finally:
        if plumber_doc is not None:
            try:
                plumber_doc.close()
            except Exception:
                pass
        if doc is not None:
            try:
                doc.close()
            except Exception:
                pass


def extract_pdf_v2(file_path: str, enable_ocr: bool = True) -> dict[str, Any]:
    """Extracts complete PDF content with reading order, TOC headings, tables, and optional OCR."""
    return _extract_pdf_bytes_or_path(file_path, ext_label="pdf", enable_ocr=enable_ocr)


# ---------------------------------------------------------------------------
# DOCX / Legacy DOC / ODT Extractors
# ---------------------------------------------------------------------------

def _iter_docx_body_md(doc_obj: docx.document.Document) -> tuple[str, int, int]:
    """Walks DOCX body in exact document order so paragraphs and tables stay interleaved."""
    blocks: list[str] = []
    para_count = 0
    table_count = 0

    for child in doc_obj.element.body.iterchildren():
        if isinstance(child, CT_P):
            p = Paragraph(child, doc_obj)
            txt = clean_text(p.text)
            if not txt:
                continue
            para_count += 1
            style_name = (p.style.name or "").lower() if p.style else ""
            if style_name.startswith("heading ") or style_name.startswith("überschrift "):
                try:
                    lvl = int(re.findall(r"\d+", style_name)[0])
                    lvl = min(6, max(2, lvl + 1))
                except Exception:
                    lvl = 2
                blocks.append(f"{'#' * lvl} {txt}")
            elif "title" in style_name or "titel" == style_name:
                blocks.append(f"## {txt}")
            else:
                # Detect list items via numbering properties (w:numPr)
                pPr = child.pPr
                if pPr is not None and pPr.numPr is not None:
                    ilvl_el = pPr.numPr.ilvl
                    indent = int(ilvl_el.val) if ilvl_el is not None and ilvl_el.val is not None else 0
                    blocks.append(f"{'  ' * min(4, indent)}- {txt}")
                else:
                    blocks.append(txt)
        elif isinstance(child, CT_Tbl):
            tbl = Table(child, doc_obj)
            rows = [[c.text for c in row.cells] for row in tbl.rows]
            md_t = format_markdown_table(rows)
            if md_t:
                table_count += 1
                blocks.append(md_t)

    # Extract header/footer notes & textbox shapes not yet captured verbatim
    seen_snippets = {b.strip() for b in blocks}
    extra_boxes: list[str] = []
    for txbx in doc_obj.element.body.findall(".//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}txbxContent"):
        box_lines = []
        for p_el in txbx.findall("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p"):
            t = clean_text("".join(p_el.itertext()))
            if t and t not in seen_snippets and not t.startswith("- " + t):
                box_lines.append(t)
                seen_snippets.add(t)
        if box_lines:
            extra_boxes.append("- " + " | ".join(box_lines))
    if extra_boxes:
        blocks.append("## Textfelder & Diagramm-Beschriftungen\n\n" + "\n".join(extra_boxes))

    return "\n\n".join(blocks), para_count, table_count


def extract_docx_v2(file_path: str | bytes) -> dict[str, Any]:
    """Extracts complete DOCX content preserving paragraph/table interleaving."""
    try:
        src = io.BytesIO(file_path) if isinstance(file_path, bytes) else file_path
        doc_obj = docx.Document(src)
        body_md, p_cnt, t_cnt = _iter_docx_body_md(doc_obj)
        return _make_result("docx", body_md, units=max(1, p_cnt + t_cnt), tables_count=t_cnt)
    except Exception as exc:
        return _make_result("docx", "", error=f"DOCX error: {exc}")


def extract_doc_v2(file_path: str) -> dict[str, Any]:
    """Extracts legacy Word 97-2003 (.doc) text cleanly via OLE FIB + CLX piece table."""
    try:
        with olefile.OleFileIO(file_path) as ole:
            if not ole.exists("WordDocument"):
                return _make_result("doc", "", error="Missing WordDocument stream")
            wdoc = ole.openstream("WordDocument").read()
            flags = struct.unpack_from("<H", wdoc, 0x0A)[0]
            table_name = "1Table" if (flags & 0x0200) else "0Table"
            ccp_text = struct.unpack_from("<I", wdoc, 0x4C)[0]
            fc_min = struct.unpack_from("<I", wdoc, 0x18)[0]

            pieces_text: list[str] = []
            if len(wdoc) > 0x1AA and ole.exists(table_name):
                fc_clx, lcb_clx = struct.unpack_from("<II", wdoc, 0x1A2)
                tbl_stream = ole.openstream(table_name).read()
                clx = tbl_stream[fc_clx : fc_clx + lcb_clx]
                pos = 0
                while pos < len(clx):
                    clxt = clx[pos]
                    if clxt == 1:
                        cb = struct.unpack_from("<H", clx, pos + 1)[0]
                        pos += 3 + cb
                    elif clxt == 2:
                        lcb = struct.unpack_from("<I", clx, pos + 1)[0]
                        pcdt = clx[pos + 5 : pos + 5 + lcb]
                        n = (len(pcdt) - 4) // 12
                        cps = [struct.unpack_from("<I", pcdt, i * 4)[0] for i in range(n + 1)]
                        for i in range(n):
                            char_cnt = cps[i + 1] - cps[i]
                            fc_raw = struct.unpack_from("<I", pcdt, (n + 1) * 4 + i * 8 + 2)[0]
                            is_ansi = bool(fc_raw & 0x40000000)
                            fc = (fc_raw & 0x3FFFFFFF) // (2 if is_ansi else 1)
                            if is_ansi:
                                pieces_text.append(wdoc[fc : fc + char_cnt].decode("cp1252", errors="replace"))
                            else:
                                pieces_text.append(wdoc[fc : fc + char_cnt * 2].decode("utf-16-le", errors="replace"))
                        break
                    else:
                        break

            raw = "".join(pieces_text)[:ccp_text] if pieces_text else ""
            if not raw.strip():
                raw = wdoc[fc_min : fc_min + ccp_text].decode("cp1252", errors="replace")

        raw = re.sub(r"\x13[^\x14\x15]*\x14([^\x15]*)\x15", r"\1", raw)
        raw = re.sub(r"\x13[^\x15]*\x15", "", raw)
        raw = raw.replace("\r", "\n").replace("\x0b", "\n")

        # Format Word table rows (\x07 cell delimiter) into clean GFM tables & paragraphs
        blocks_out: list[str] = []
        table_buf: list[list[str]] = []

        def flush_doc_table() -> None:
            if table_buf:
                md_t = format_markdown_table(table_buf)
                if md_t:
                    blocks_out.append(md_t)
                table_buf.clear()

        for ln in raw.splitlines():
            if "\x07" in ln:
                cells = [re.sub(r"\s+", " ", c).strip() for c in ln.split("\x07")]
                if cells and cells[-1] == "":
                    cells = cells[:-1]
                if any(cells):
                    table_buf.append(cells)
            elif ln.strip():
                flush_doc_table()
                blocks_out.append(ln.strip())
        flush_doc_table()

        return _make_result("doc", "\n\n".join(blocks_out), units=max(1, len(blocks_out)))
    except Exception as exc:
        return _make_result("doc", "", error=f"DOC error: {exc}")


def extract_odt_v2(file_path: str) -> dict[str, Any]:
    """Extracts OpenDocument Text (.odt) headings, paragraphs, lists, and tables."""
    try:
        ns_text = "urn:oasis:names:tc:opendocument:xmlns:text:1.0"
        ns_table = "urn:oasis:names:tc:opendocument:xmlns:table:1.0"
        with zipfile.ZipFile(file_path) as zf:
            root = ET.fromstring(zf.read("content.xml"))
        blocks: list[str] = []
        tables_count = 0

        def walk_node(el: ET.Element, in_list: int = 0) -> None:
            nonlocal tables_count
            tag = el.tag
            if tag == f"{{{ns_text}}}h":
                txt = clean_text("".join(el.itertext()))
                if txt:
                    lvl = int(el.attrib.get(f"{{{ns_text}}}outline-level", "1"))
                    blocks.append(f"{'#' * min(6, max(2, lvl + 1))} {txt}")
            elif tag == f"{{{ns_text}}}p":
                txt = clean_text("".join(el.itertext()))
                if txt:
                    blocks.append(f"{'  ' * max(0, in_list - 1)}- {txt}" if in_list else txt)
            elif tag == f"{{{ns_text}}}list":
                for child in el:
                    walk_node(child, in_list + 1)
            elif tag == f"{{{ns_table}}}table":
                rows = []
                for tr in el.findall(f"{{{ns_table}}}table-row"):
                    rows.append([clean_text("".join(tc.itertext())) for tc in tr.findall(f"{{{ns_table}}}table-cell")])
                md_t = format_markdown_table(rows)
                if md_t:
                    tables_count += 1
                    blocks.append(md_t)
            else:
                for child in el:
                    walk_node(child, in_list)

        walk_node(root)
        return _make_result("odt", "\n\n".join(blocks), units=max(1, len(blocks)), tables_count=tables_count)
    except Exception as exc:
        return _make_result("odt", "", error=f"ODT error: {exc}")


# ---------------------------------------------------------------------------
# PPTX Extractor V2 (Recursive Group Shapes + Complete Tables + Speaker Notes)
# ---------------------------------------------------------------------------

def _extract_pptx_shape(shape: Any, blocks: list[str], title_shape_id: int | None) -> int:
    tables_added = 0
    try:
        sh_type = shape.shape_type
    except Exception:
        sh_type = None

    if sh_type == MSO_SHAPE_TYPE.GROUP:
        sub_shapes = sorted(shape.shapes, key=lambda s: (getattr(s, "top", 0) or 0, getattr(s, "left", 0) or 0))
        for sub in sub_shapes:
            tables_added += _extract_pptx_shape(sub, blocks, title_shape_id)
        return tables_added

    if getattr(shape, "has_table", False):
        rows = [[c.text for c in r.cells] for r in shape.table.rows]
        md_t = format_markdown_table(rows)
        if md_t:
            blocks.append(md_t)
            tables_added += 1

    if getattr(shape, "has_text_frame", False) and shape.shape_id != title_shape_id:
        tf_lines: list[str] = []
        for p in shape.text_frame.paragraphs:
            t = clean_text(p.text)
            if t and not _is_boilerplate_placeholder(t):
                lvl = min(4, max(0, getattr(p, "level", 0) or 0))
                tf_lines.append(f"{'  ' * lvl}- {t}")
        if tf_lines:
            blocks.append("\n".join(tf_lines))
    return tables_added


def _extract_pptx_slide_rels(
    zf: zipfile.ZipFile | None, slide_idx: int
) -> tuple[list[str], list[str]]:
    """Returns referenced SmartArt diagram XML paths and media image paths for a 1-based slide."""
    if zf is None:
        return [], []
    rels_name = f"ppt/slides/_rels/slide{slide_idx}.xml.rels"
    if rels_name not in zf.namelist():
        return [], []
    diags: list[str] = []
    imgs: list[str] = []
    try:
        root = ET.fromstring(zf.read(rels_name))
        for el in root:
            rtype = (el.attrib.get("Type") or "").lower()
            target = el.attrib.get("Target") or ""
            resolved = os.path.normpath(os.path.join("ppt/slides", target)).replace("\\", "/")
            if resolved not in zf.namelist():
                continue
            if rtype.endswith("/diagramdata"):
                diags.append(resolved)
            elif rtype.endswith("/image"):
                ext = os.path.splitext(resolved)[1].lower()
                if ext in {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}:
                    imgs.append(resolved)
    except Exception:
        pass
    return diags, imgs


def _extract_smartart_texts(zf: zipfile.ZipFile, diagram_path: str) -> list[str]:
    """Extracts ordered non-empty DrawingML text runs from a PPTX SmartArt data XML."""
    out: list[str] = []
    seen: set[str] = set()
    try:
        root = ET.fromstring(zf.read(diagram_path))
        for node in root.findall(".//{http://schemas.openxmlformats.org/drawingml/2006/main}t"):
            t = clean_text(node.text or "")
            if t and t not in seen:
                seen.add(t)
                out.append(t)
    except Exception:
        pass
    return out


def extract_pptx_v2(file_path: str, enable_ocr: bool = True) -> dict[str, Any]:
    """Extracts PowerPoint slides, nested groups, tables, SmartArt XML, notes, and fallback media OCR."""
    zf: zipfile.ZipFile | None = None
    try:
        prs = pptx.Presentation(file_path)
        try:
            zf = zipfile.ZipFile(file_path)
        except Exception:
            zf = None

        slides_md: list[str] = []
        total_tables = 0
        ocr_pages = 0
        seen_img_hashes: set[str] = set()

        for idx, slide in enumerate(prs.slides, start=1):
            title_shape = slide.shapes.title
            title_id = title_shape.shape_id if title_shape is not None else None
            title_txt = clean_text(title_shape.text) if title_shape is not None else ""
            header = f"## Folie {idx}: {title_txt}" if title_txt else f"## Folie {idx}"

            shape_blocks: list[str] = []
            ordered = sorted(slide.shapes, key=lambda s: (getattr(s, "top", 0) or 0, getattr(s, "left", 0) or 0))
            for sh in ordered:
                total_tables += _extract_pptx_shape(sh, shape_blocks, title_id)

            diag_paths, media_paths = _extract_pptx_slide_rels(zf, idx)
            if zf is not None and diag_paths:
                sa_items: list[str] = []
                for dp in diag_paths:
                    sa_items.extend(_extract_smartart_texts(zf, dp))
                if sa_items:
                    shape_blocks.append(f"### SmartArt / Diagramm (Folie {idx})\n\n" + "\n".join(f"- {s}" for s in sa_items))

            if slide.has_notes_slide and slide.notes_slide.notes_text_frame:
                notes = clean_text(slide.notes_slide.notes_text_frame.text)
                if notes:
                    shape_blocks.append(f"### Sprechernotizen (Folie {idx})\n\n{notes}")

            slide_text_len = len(re.sub(r"\s+", "", title_txt + " ".join(shape_blocks)))
            if enable_ocr and zf is not None and media_paths and slide_text_len < 20:
                ocr_chunks: list[str] = []
                for mp in media_paths[:6]:
                    try:
                        img_bytes = zf.read(mp)
                        if len(img_bytes) < 1500:
                            continue
                        ih = hashlib.sha1(img_bytes).hexdigest()
                        if ih in seen_img_hashes:
                            continue
                        seen_img_hashes.add(ih)
                        txt = clean_text(_ocr_image_bytes(img_bytes))
                        if len(re.sub(r"\s+", "", txt)) >= 10:
                            ocr_chunks.append(txt)
                    except Exception:
                        continue
                if ocr_chunks:
                    ocr_pages += 1
                    shape_blocks.append(
                        f"### Bildtext / Screenshot (Folie {idx}) *(OCR)*\n\n" + "\n\n".join(ocr_chunks)
                    )

            if title_txt or shape_blocks:
                slides_md.append("\n\n".join([header] + shape_blocks))

        return _make_result(
            "pptx", "\n\n".join(slides_md), units=len(prs.slides), ocr_pages=ocr_pages, tables_count=total_tables
        )
    except Exception as exc:
        return _make_result("pptx", "", error=f"PPTX error: {exc}")
    finally:
        if zf is not None:
            try:
                zf.close()
            except Exception:
                pass


# ---------------------------------------------------------------------------
# Spreadsheet Extractors (XLSX / XLSM / CSV)
# ---------------------------------------------------------------------------

def _trim_sheet_rows(raw_rows: list[list[Any]]) -> list[list[Any]]:
    """Removes leading/trailing completely empty rows and trailing empty columns."""
    non_empty = [list(r) for r in raw_rows if any(c is not None and str(c).strip() != "" for c in r)]
    if not non_empty:
        return []
    max_used_col = 0
    for r in non_empty:
        for c_idx in range(len(r) - 1, -1, -1):
            if r[c_idx] is not None and str(r[c_idx]).strip() != "":
                max_used_col = max(max_used_col, c_idx + 1)
                break
    return [r[:max_used_col] for r in non_empty] if max_used_col > 0 else []


def _extract_xlsx_xml_fallback(src: str | io.BytesIO, max_rows_per_sheet: int = 4000) -> dict[str, Any]:
    """Direct ZIP/XML XLSX reader bypassing broken stylesheet or Chartsheet metadata."""
    with zipfile.ZipFile(src) as zf:
        shared: list[str] = []
        if "xl/sharedStrings.xml" in zf.namelist():
            ss_root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
            for si in ss_root.findall("{*}si"):
                shared.append("".join(t.text or "" for t in si.iter() if t.tag.endswith("}t")))

        sheet_files = sorted(n for n in zf.namelist() if re.match(r"xl/worksheets/sheet\d+\.xml$", n))
        sheets_md: list[str] = []
        total_tables = 0
        for idx, s_path in enumerate(sheet_files, start=1):
            root = ET.fromstring(zf.read(s_path))
            collected: list[list[Any]] = []
            total_non_empty = 0
            for row_el in root.findall(".//{*}row"):
                row_vals: list[Any] = []
                for c in row_el.findall("{*}c"):
                    c_type = c.attrib.get("t", "")
                    v_el = c.find("{*}v")
                    is_el = c.find("{*}is")
                    val: str = ""
                    if c_type == "s" and v_el is not None and v_el.text:
                        val = shared[int(v_el.text)] if int(v_el.text) < len(shared) else v_el.text
                    elif is_el is not None:
                        val = "".join(t.text or "" for t in is_el.iter() if t.tag.endswith("}t"))
                    elif v_el is not None and v_el.text:
                        val = v_el.text
                    row_vals.append(val)
                if any(str(x).strip() for x in row_vals):
                    total_non_empty += 1
                    if len(collected) < max_rows_per_sheet:
                        collected.append(row_vals)
            trimmed = _trim_sheet_rows(collected)
            if trimmed:
                md_t = format_markdown_table(trimmed)
                if md_t:
                    total_tables += 1
                    sheets_md.append(f"## Tabellenblatt `Sheet{idx}` ({total_non_empty:,} Zeilen)\n\n{md_t}")
        return _make_result("xlsx", "\n\n".join(sheets_md), units=len(sheet_files), tables_count=total_tables)


def extract_xlsx_v2(file_path: str | bytes, max_rows_per_sheet: int = 4000) -> dict[str, Any]:
    """Extracts active cell grids across all sheets of XLSX/XLSM files without tight truncation."""
    wb = None
    try:
        src = io.BytesIO(file_path) if isinstance(file_path, bytes) else file_path
        wb = openpyxl.load_workbook(src, read_only=True, data_only=True)
        sheets_md: list[str] = []
        total_tables = 0
        for sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
            if not hasattr(ws, "iter_rows"):
                continue
            collected: list[list[Any]] = []
            total_non_empty = 0
            for row in ws.iter_rows(values_only=True):
                if any(c is not None and str(c).strip() != "" for c in row):
                    total_non_empty += 1
                    if len(collected) < max_rows_per_sheet:
                        collected.append(list(row))
            trimmed = _trim_sheet_rows(collected)
            if not trimmed:
                continue
            md_t = format_markdown_table(trimmed)
            if md_t:
                total_tables += 1
                note = ""
                if total_non_empty > max_rows_per_sheet:
                    note = f"\n\n*(Hinweis: Auszug der ersten {max_rows_per_sheet:,} von insgesamt {total_non_empty:,} belegten Zeilen)*"
                sheets_md.append(f"## Tabellenblatt: `{clean_text(sheet_name)}` ({total_non_empty:,} Zeilen)\n\n{md_t}{note}")
        return _make_result("xlsx", "\n\n".join(sheets_md), units=len(wb.sheetnames), tables_count=total_tables)
    except Exception as exc:
        try:
            src_fb = io.BytesIO(file_path) if isinstance(file_path, bytes) else file_path
            return _extract_xlsx_xml_fallback(src_fb, max_rows_per_sheet=max_rows_per_sheet)
        except Exception:
            return _make_result("xlsx", "", error=f"XLSX error: {exc}")
    finally:
        if wb is not None:
            try:
                wb.close()
            except Exception:
                pass


def extract_csv_v2(file_path: str, max_rows: int = 4000) -> dict[str, Any]:
    """Extracts CSV tabular data with encoding and delimiter autodetection."""
    try:
        raw_bytes = open(file_path, "rb").read()
        text = None
        for enc in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
            try:
                text = raw_bytes.decode(enc)
                break
            except UnicodeDecodeError:
                continue
        if text is None:
            text = raw_bytes.decode("utf-8", errors="replace")
        sample = text[:4096]
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=";,\t|")
        except Exception:
            dialect = csv.excel
        rows = list(csv.reader(io.StringIO(text), dialect=dialect))
        total = len(rows)
        md_t = format_markdown_table(rows[:max_rows])
        note = f"\n\n*(Hinweis: Erste {max_rows:,} von {total:,} CSV-Zeilen)*" if total > max_rows else ""
        return _make_result("csv", (md_t + note).strip(), units=total, tables_count=1 if md_t else 0)
    except Exception as exc:
        return _make_result("csv", "", error=f"CSV error: {exc}")


# ---------------------------------------------------------------------------
# Outlook .msg, Visio .vsdx, MS Project .mpp, HTML & Plain Text Extractors
# ---------------------------------------------------------------------------

def _html_to_markdown(html_str: str) -> tuple[str, int]:
    soup = BeautifulSoup(html_str, "html.parser")
    for tag in soup(["script", "style", "svg", "noscript"]):
        tag.decompose()
    blocks: list[str] = []
    tables_cnt = 0

    for tbl in soup.find_all("table"):
        rows = []
        for tr in tbl.find_all("tr"):
            cells = [clean_text(c.get_text(" ", strip=True)) for c in tr.find_all(["th", "td"])]
            if any(cells):
                rows.append(cells)
        md_t = format_markdown_table(rows)
        if md_t:
            tables_cnt += 1
            tbl.replace_with(soup.new_string(f"\n\n{md_t}\n\n"))
        else:
            tbl.decompose()

    for h_lvl in range(1, 7):
        for h in soup.find_all(f"h{h_lvl}"):
            t = clean_text(h.get_text(" ", strip=True))
            if t:
                h.replace_with(soup.new_string(f"\n\n{'#' * min(6, max(2, h_lvl + 1))} {t}\n\n"))

    for code_blk in soup.find_all(lambda tag: tag.name == "pre" or (tag.name == "div" and any(k in " ".join(tag.get("class") or []) for k in ("ProgramCode", "CodeBlock")))):
        line_divs = code_blk.find_all("div", class_=lambda c: c and "FixedLine" in " ".join(c) if isinstance(c, list) else (c and "FixedLine" in str(c)))
        if line_divs:
            code_lines = [ld.get_text("").replace("\xa0", " ").rstrip() for ld in line_divs]
            code_txt = "\n".join(code_lines).strip("\r\n")
        else:
            code_txt = code_blk.get_text("").replace("\xa0", " ").strip("\r\n")
        if code_txt.strip():
            code_blk.replace_with(soup.new_string(f"\n\n```\n{code_txt}\n```\n\n"))
        else:
            code_blk.decompose()

    for li in soup.find_all("li"):
        t = clean_text(li.get_text(" ", strip=True))
        if t:
            li.replace_with(soup.new_string(f"\n- {t}"))

    raw_txt = soup.get_text("\n")
    return clean_text(raw_txt), tables_cnt


def extract_msg_v2(file_path: str, enable_ocr: bool = True) -> dict[str, Any]:
    """Extracts Outlook .msg headers, plain/HTML body, and inline document attachment text."""
    msg = None
    try:
        msg = extract_msg.Message(file_path)
        subj = clean_text(str(msg.subject or "(Ohne Betreff)"))
        sender = clean_text(str(msg.sender or ""))
        to = clean_text(str(msg.to or ""))
        cc = clean_text(str(msg.cc or ""))
        date_str = clean_text(str(msg.date or ""))

        body = clean_text(str(msg.body or ""))
        if not body and getattr(msg, "htmlBody", None):
            html_raw = msg.htmlBody.decode("utf-8", errors="replace") if isinstance(msg.htmlBody, bytes) else str(msg.htmlBody)
            body, _ = _html_to_markdown(html_raw)

        att_sections: list[str] = []
        att_names: list[str] = []
        for att in getattr(msg, "attachments", []) or []:
            att_name = clean_text(str(getattr(att, "longFilename", None) or getattr(att, "shortFilename", None) or "attachment"))
            att_names.append(att_name)
            ext = os.path.splitext(att_name)[1].lower()
            data = getattr(att, "data", None)
            if isinstance(data, bytes) and ext in (".pdf", ".docx", ".xlsx", ".xlsm", ".txt", ".md", ".html"):
                if ext == ".pdf":
                    sub_res = _extract_pdf_bytes_or_path(data, "pdf", ocr_max_pages=20, enable_ocr=enable_ocr)
                elif ext == ".docx":
                    sub_res = extract_docx_v2(data)
                elif ext in (".xlsx", ".xlsm"):
                    sub_res = extract_xlsx_v2(data)
                elif ext == ".html":
                    h_md, _ = _html_to_markdown(data.decode("utf-8", errors="replace"))
                    sub_res = _make_result("html", h_md)
                else:
                    sub_res = _make_result("text", data.decode("utf-8", errors="replace"))
                if sub_res.get("text"):
                    att_sections.append(f"### Anhang: `{att_name}`\n\n{sub_res['text']}")

        header_lines = [
            f"## E-Mail-Metadaten: {subj}",
            f"- **Betreff:** {subj}",
            f"- **Von:** {sender or '-'}",
            f"- **An:** {to or '-'}",
        ]
        if cc:
            header_lines.append(f"- **CC:** {cc}")
        if date_str:
            header_lines.append(f"- **Datum:** {date_str}")
        if att_names:
            header_lines.append(f"- **Anhänge ({len(att_names)}):** " + ", ".join(f"`{a}`" for a in att_names))

        parts = ["\n".join(header_lines), "## Nachrichteninhalt\n\n" + (body or "*(Kein Nachrichtentext)*")]
        if att_sections:
            parts.append("## Extrahierte Dokument-Anhänge\n\n" + "\n\n".join(att_sections))

        return _make_result(
            "msg",
            "\n\n".join(parts),
            units=1 + len(att_sections),
            meta={"subject": subj, "sender": sender, "date": date_str},
        )
    except Exception as exc:
        return _make_result("msg", "", error=f"MSG error: {exc}")
    finally:
        if msg is not None:
            try:
                msg.close()
            except Exception:
                pass


def extract_vsdx_v2(file_path: str) -> dict[str, Any]:
    """Extracts Visio .vsdx diagram page shapes sorted visually top-to-bottom."""
    try:
        with zipfile.ZipFile(file_path) as zf:
            page_files = sorted(n for n in zf.namelist() if n.startswith("visio/pages/page") and n.endswith(".xml"))
            pages_md: list[str] = []
            for p_idx, p_name in enumerate(page_files, start=1):
                root = ET.fromstring(zf.read(p_name))
                nodes: list[tuple[float, float, str]] = []
                for sh in root.iter():
                    if sh.tag.endswith("Shape"):
                        pin_x, pin_y = 0.0, 0.0
                        texts: list[str] = []
                        for child in sh:
                            if child.tag.endswith("Cell"):
                                n_attr = child.attrib.get("N")
                                val = child.attrib.get("V", "0")
                                if n_attr == "PinX":
                                    try:
                                        pin_x = float(val)
                                    except ValueError:
                                        pass
                                elif n_attr == "PinY":
                                    try:
                                        pin_y = float(val)
                                    except ValueError:
                                        pass
                            elif child.tag.endswith("Text"):
                                t = clean_text("".join(child.itertext()))
                                if t:
                                    texts.append(t)
                        if texts:
                            nodes.append((-pin_y, pin_x, " — ".join(texts)))
                if nodes:
                    nodes.sort()
                    items = "\n".join(f"- {n[2].replace(chr(10), ' / ')}" for n in nodes)
                    pages_md.append(f"## Visio-Seite {p_idx} (`{os.path.basename(p_name)}`)\n\n{items}")
        return _make_result("vsdx", "\n\n".join(pages_md), units=max(1, len(page_files)))
    except Exception as exc:
        return _make_result("vsdx", "", error=f"VSDX error: {exc}")


def extract_mpp_v2(file_path: str) -> dict[str, Any]:
    """Extracts MS Project (.mpp) task, milestone, and resource strings cleanly via OLE streams."""
    try:
        with olefile.OleFileIO(file_path) as ole:
            task_strings: list[str] = []
            rsc_strings: list[str] = []
            meta_strings: list[str] = []

            def extract_u16_items(data: bytes) -> list[str]:
                decoded = data.decode("utf-16-le", errors="ignore")
                raw_hits = re.findall(r"[A-Za-zÄÖÜäöüß0-9][A-Za-zÄÖÜäöüß0-9 \.,;:\-\/\(\)&%€\+_]{2,140}", decoded)
                cleaned: list[str] = []
                seen: set[str] = set()
                for item in raw_hits:
                    s = re.sub(r"\s+", " ", item).strip()
                    if len(s) >= 3 and s not in seen and not re.fullmatch(r"[0-9\.,\-\s]+", s):
                        seen.add(s)
                        cleaned.append(s)
                return cleaned

            for dir_entry in ole.listdir():
                stream_path = "/".join(dir_entry)
                if "TBkndTask" in stream_path and stream_path.endswith("Var2Data"):
                    task_strings.extend(extract_u16_items(ole.openstream(dir_entry).read()))
                elif "TBkndRsc" in stream_path and stream_path.endswith("Var2Data"):
                    rsc_strings.extend(extract_u16_items(ole.openstream(dir_entry).read()))
                elif stream_path in ("Props14", "Props"):
                    meta_strings.extend(extract_u16_items(ole.openstream(dir_entry).read()))

        sections: list[str] = []
        if task_strings:
            sections.append("## MS Project Vorgänge & Meilensteine (OLE-Extrakt)\n\n" + "\n".join(f"- {t}" for t in task_strings))
        if rsc_strings:
            sections.append("## Ressourcen & Rollen\n\n" + "\n".join(f"- {r}" for r in rsc_strings))
        if meta_strings and not task_strings:
            sections.append("## Projekt-Metadaten\n\n" + "\n".join(f"- {m}" for m in meta_strings[:60]))

        return _make_result("mpp", "\n\n".join(sections), units=max(1, len(task_strings)))
    except Exception as exc:
        return _make_result("mpp", "", error=f"MPP error: {exc}")


def extract_html_v2(file_path: str) -> dict[str, Any]:
    """Extracts readable HTML content preserving headings, lists, and tables."""
    try:
        raw_bytes = open(file_path, "rb").read()
        html_str = None
        for enc in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
            try:
                html_str = raw_bytes.decode(enc)
                break
            except UnicodeDecodeError:
                continue
        if html_str is None:
            html_str = raw_bytes.decode("utf-8", errors="replace")
        md_txt, t_cnt = _html_to_markdown(html_str)
        return _make_result("html", md_txt, units=1, tables_count=t_cnt)
    except Exception as exc:
        return _make_result("html", "", error=f"HTML error: {exc}")


def extract_text_v2(file_path: str, code_fence: str | None = None) -> dict[str, Any]:
    """Extracts UTF-8/CP1252 plain text, Markdown, or script/source files cleanly."""
    ext = os.path.splitext(file_path)[1].lower().lstrip(".") or "txt"
    try:
        raw_bytes = open(file_path, "rb").read()
        text = None
        for enc in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
            try:
                text = raw_bytes.decode(enc)
                break
            except UnicodeDecodeError:
                continue
        if text is None:
            text = raw_bytes.decode("utf-8", errors="replace")
        cleaned = clean_text(text)
        if code_fence and cleaned:
            cleaned = f"```{code_fence}\n{cleaned}\n```"
        return _make_result(ext, cleaned, units=max(1, len(cleaned.splitlines())))
    except Exception as exc:
        return _make_result(ext, "", error=f"Text error: {exc}")


def extract_epub_v2(file_path: str) -> dict[str, Any]:
    """Extracts EPUB chapters in official OPF spine order using stdlib zipfile + BeautifulSoup."""
    try:
        with zipfile.ZipFile(file_path, "r") as zf:
            names = zf.namelist()
            name_lookup = {n.lower(): n for n in names}

            opf_path = ""
            if "META-INF/container.xml" in names or "meta-inf/container.xml" in name_lookup:
                c_name = "META-INF/container.xml" if "META-INF/container.xml" in names else name_lookup["meta-inf/container.xml"]
                c_xml = ET.fromstring(zf.read(c_name))
                for rf in c_xml.iter():
                    if rf.tag.endswith("rootfile") and rf.attrib.get("full-path"):
                        opf_path = rf.attrib["full-path"]
                        break

            book_title = ""
            authors: list[str] = []
            ordered_paths: list[str] = []

            if opf_path and opf_path in names:
                opf_dir = posixpath.dirname(opf_path)
                opf_root = ET.fromstring(zf.read(opf_path))

                for elem in opf_root.iter():
                    tag_low = elem.tag.split("}")[-1].lower()
                    txt = clean_text(elem.text or "")
                    if not txt:
                        continue
                    if tag_low == "title" and not book_title:
                        book_title = txt
                    elif tag_low == "creator" and txt not in authors:
                        authors.append(txt)

                manifest_map: dict[str, str] = {}
                for item in opf_root.iter():
                    if item.tag.endswith("item"):
                        iid = item.attrib.get("id", "")
                        href = item.attrib.get("href", "").split("#")[0]
                        mtype = item.attrib.get("media-type", "").lower()
                        if iid and href and ("html" in mtype or href.lower().endswith((".xhtml", ".html", ".htm"))):
                            joined = posixpath.normpath(posixpath.join(opf_dir, href)) if opf_dir else href
                            manifest_map[iid] = joined

                for iref in opf_root.iter():
                    if iref.tag.endswith("itemref"):
                        idref = iref.attrib.get("idref", "")
                        cand = manifest_map.get(idref)
                        if cand and cand in names and cand not in ordered_paths:
                            ordered_paths.append(cand)

            if not ordered_paths:
                ordered_paths = sorted(
                    n for n in names
                    if n.lower().endswith((".xhtml", ".html", ".htm"))
                    and not os.path.basename(n).lower().startswith(("nav", "toc"))
                )

            chapters_md: list[str] = []
            if book_title or authors:
                hdr = []
                if book_title:
                    hdr.append(f"## 📖 {book_title}")
                if authors:
                    hdr.append(f"**Autor(en):** {', '.join(authors)}")
                chapters_md.append("\n".join(hdr))

            tables_total = 0
            chapter_units = 0
            for ch_path in ordered_paths:
                raw_bytes = zf.read(ch_path)
                html_str = raw_bytes.decode("utf-8", errors="replace")
                md_part, t_cnt = _html_to_markdown(html_str)
                tables_total += t_cnt
                if md_part and len(md_part.strip()) >= 25:
                    chapters_md.append(md_part)
                    chapter_units += 1

            combined = "\n\n---\n\n".join(chapters_md)
            meta = {"title": book_title} if book_title else {}
            return _make_result(
                "epub",
                combined,
                units=max(1, chapter_units),
                tables_count=tables_total,
                meta=meta,
            )
    except Exception as exc:
        return _make_result("epub", "", error=f"EPUB error: {exc}")


def extract_document_v2(file_path: str, enable_ocr: bool = True) -> dict[str, Any]:
    """Dispatches any supported file path to its optimal V2 extractor."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_pdf_v2(file_path, enable_ocr=enable_ocr)
    if ext == ".epub":
        return extract_epub_v2(file_path)
    if ext == ".docx":
        return extract_docx_v2(file_path)
    if ext == ".doc":
        return extract_doc_v2(file_path)
    if ext == ".odt":
        return extract_odt_v2(file_path)
    if ext == ".pptx":
        return extract_pptx_v2(file_path, enable_ocr=enable_ocr)
    if ext in (".xlsx", ".xlsm"):
        return extract_xlsx_v2(file_path)
    if ext == ".csv":
        return extract_csv_v2(file_path)
    if ext == ".msg":
        return extract_msg_v2(file_path, enable_ocr=enable_ocr)
    if ext == ".vsdx":
        return extract_vsdx_v2(file_path)
    if ext == ".mpp":
        return extract_mpp_v2(file_path)
    if ext in (".html", ".htm"):
        return extract_html_v2(file_path)
    if ext == ".ps1":
        return extract_text_v2(file_path, code_fence="powershell")
    if ext in (".md", ".txt"):
        return extract_text_v2(file_path)
    return _make_result(ext.lstrip(".") or "unknown", "", error=f"Unsupported extension: {ext}")
