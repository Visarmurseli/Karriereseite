# -*- coding: utf-8 -*-
"""
Master Builder for Visar Murseli's Enterprise Knowledge Hub & S/4HANA Career OS.
Assembles TWO strict builds from portal_builder:
1. s4hana-prep-portal/index.html        -> Full Local Private Cockpit (7 Core Tabs + 4 Private Prep/RAG Tabs)
2. s4hana-prep-portal/public_index.html -> Clean 7-Tab Public Showcase (Dashboard, SSB, DC1, Master, Bachelor, Synergies, FAQ)
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from portal_builder.header import get_header
from portal_builder.dashboard import get_dashboard
from portal_builder.ssb_tab import get_ssb_tab
from portal_builder.dc1_tab import get_dc1_tab
from portal_builder.master_tab import get_master_tab
from portal_builder.bachelor_tab import get_bachelor_tab
from portal_builder.synergies import get_synergies
from portal_builder.faq_tab import get_faq_tab
from portal_builder.cv_defense import get_cv_defense
from portal_builder.interview import get_interview
from portal_builder.files_tab import get_files_tab
from portal_builder.notebook import get_notebook
from portal_builder.vue_app import get_vue_app


def build_variant(public_mode=False):
    parts = [
        get_header(public_mode=public_mode),
        get_dashboard(public_mode=public_mode),
        get_ssb_tab(),
        get_dc1_tab(),
        get_master_tab(),
        get_bachelor_tab(),
        get_synergies(public_mode=public_mode),
        get_faq_tab(),
    ]
    if not public_mode:
        parts.extend([
            get_interview(),
            get_cv_defense(),
            get_files_tab(),
            get_notebook(),
        ])
    parts.append(get_vue_app(public_mode=public_mode))
    return "\n".join(parts)


def main():
    target_dir = os.path.join(BASE_DIR, "s4hana-prep-portal")
    os.makedirs(target_dir, exist_ok=True)
    index_path = os.path.join(target_dir, "index.html")
    public_path = os.path.join(target_dir, "public_index.html")

    # 1. Full Local Private Cockpit
    local_html = build_variant(public_mode=False)
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(local_html)

    # 2. Clean 7-Tab Public Showcase Build (for GitHub Pages)
    public_html = build_variant(public_mode=True)
    with open(public_path, "w", encoding="utf-8") as f:
        f.write(public_html)

    for forbidden in [
        "Gefahrenstufe Rot", "TÖDLICH", "cv_defense", "Fangfrage", "Gehaltskalkulation",
        "Roland Nowak", "Dietmar Fillinger", "Helmut Schmidpeter",
        "Sarah Lozano", "Thomas Wimpff", "Sebastian Neifer",
        "Markus Schmidt", "Joachim Kraus", "Henning Gerdes",
        "Armin Heinrich", "Michael Gehrung",
        "WBS 1–297", "Vorgang 110", "Vorgang 294", "Vorgang 297",
        "Atlassian", "Confluence", "Jira", "isCommandPaletteOpen", "openCommandPalette",
        "Interview_IP1", "Interview_IP2", "Interview_IP3", "Interview_IP4", "HLM_v2.vsdx", "Studium_Dokumente"
    ]:
        assert forbidden.lower() not in public_html.lower(), f"PRIVACY/BRANDING GATE ERROR: '{forbidden}' leaked into public_index.html!"

    root_index = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(root_index) or os.path.exists(os.path.join(BASE_DIR, ".git")):
        with open(root_index, "w", encoding="utf-8") as f:
            f.write(public_html)
        print(f"     Public Root sync: {root_index}")

    print("[OK] Streamlined Dual-Mode Portal generated successfully!")
    print(f"     Local Cockpit : {index_path} ({len(local_html.encode('utf-8'))/1024:.2f} KB)")
    print(f"     Public Showcase: {public_path} ({len(public_html.encode('utf-8'))/1024:.2f} KB | 7-Tab Executive Edition)")

    from scripts.test_portal import run_all_tests
    run_all_tests()


if __name__ == "__main__":
    main()
