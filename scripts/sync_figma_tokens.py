# -*- coding: utf-8 -*-
"""Sync Career OS Figma Variables (portal_builder/figma_tokens.json) into portal_builder/header.py.

Usage:
  python scripts/sync_figma_tokens.py --dry-run
  python scripts/sync_figma_tokens.py --apply --build
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
TOKENS_PATH = ROOT_DIR / "portal_builder" / "figma_tokens.json"
HEADER_PATH = ROOT_DIR / "portal_builder" / "header.py"
BUILD_SCRIPT = ROOT_DIR / "build_ultimate_portal.py"

FIGMA_TO_CSS_MAP = {
    "--surface-base": "--ds-surface",
    "--surface-sunken": "--ds-surface-sunken",
    "--surface-raised": "--ds-surface-raised",
    "--text-primary": "--ds-text",
    "--text-subtle": "--ds-text-subtle",
    "--text-subtlest": "--ds-text-subtlest",
    "--brand-primary": "--ds-brand-bold",
    "--brand-subtlest": "--ds-brand-subtlest",
    "--border-default": "--ds-border",
    "--status-success-bg": "--ds-bg-success",
    "--status-success-text": "--ds-text-success",
}


def update_css_block(block_text: str, figma_mode_tokens: dict[str, str], mode_name: str) -> tuple[str, list[str]]:
    """Replace mapped --ds-* CSS variables inside a single CSS rule block."""
    changes: list[str] = []
    updated = block_text

    for figma_var, css_var in FIGMA_TO_CSS_MAP.items():
        if figma_var not in figma_mode_tokens:
            continue
        new_val = figma_mode_tokens[figma_var]
        pattern = re.compile(rf"(^\s*{re.escape(css_var)}\s*:\s*)([^;]+)(;)", re.MULTILINE)

        def _repl(match: re.Match[str]) -> str:
            old_val = match.group(2).strip()
            if old_val.lower() != new_val.lower():
                changes.append(f"[{mode_name}] {css_var}: {old_val} -> {new_val}")
            return f"{match.group(1)}{new_val}{match.group(3)}"

        updated = pattern.sub(_repl, updated, count=1)

    return updated, changes


def sync_tokens(apply: bool, build: bool) -> int:
    """Sync Figma tokens into header.py and optionally rebuild the portal."""
    if not TOKENS_PATH.exists():
        print(f"ERROR: Token file not found: {TOKENS_PATH}", file=sys.stderr)
        return 1
    if not HEADER_PATH.exists():
        print(f"ERROR: Header file not found: {HEADER_PATH}", file=sys.stderr)
        return 1

    tokens_data = json.loads(TOKENS_PATH.read_text(encoding="utf-8"))
    header_src = HEADER_PATH.read_text(encoding="utf-8")

    root_match = re.search(r"(:root\s*\{.*?\n\s*\})", header_src, re.DOTALL)
    dark_match = re.search(r"(html\.dark\s*\{.*?\n\s*\})", header_src, re.DOTALL)

    if not root_match or not dark_match:
        print("ERROR: Could not locate :root or html.dark CSS blocks in header.py", file=sys.stderr)
        return 1

    new_root, root_changes = update_css_block(root_match.group(1), tokens_data.get("light", {}), "light")
    new_dark, dark_changes = update_css_block(dark_match.group(1), tokens_data.get("dark", {}), "dark")
    all_changes = root_changes + dark_changes

    if not all_changes:
        print("OK: All 11 mapped Light/Dark tokens in header.py already match figma_tokens.json.")
    else:
        print(f"Found {len(all_changes)} token difference(s):")
        for line in all_changes:
            print(f"  - {line}")

    if apply and all_changes:
        updated_src = header_src.replace(root_match.group(1), new_root, 1).replace(dark_match.group(1), new_dark, 1)
        HEADER_PATH.write_text(updated_src, encoding="utf-8")
        print(f"APPLIED: Updated {HEADER_PATH}")
    elif not apply and all_changes:
        print("DRY-RUN: No files modified (pass --apply to write changes).")

    if build:
        if not BUILD_SCRIPT.exists():
            print(f"ERROR: Build script not found: {BUILD_SCRIPT}", file=sys.stderr)
            return 1
        res = subprocess.run([sys.executable, str(BUILD_SCRIPT)], cwd=str(ROOT_DIR), check=False)
        return res.returncode

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync Figma Career OS Tokens into portal_builder/header.py")
    parser.add_argument("--apply", action="store_true", help="Write token changes into portal_builder/header.py")
    parser.add_argument("--dry-run", action="store_true", help="Preview diffs without writing files (default)")
    parser.add_argument("--build", action="store_true", help="Run build_ultimate_portal.py after sync")
    args = parser.parse_args()
    return sync_tokens(apply=args.apply and not args.dry_run, build=args.build)


if __name__ == "__main__":
    raise SystemExit(main())
