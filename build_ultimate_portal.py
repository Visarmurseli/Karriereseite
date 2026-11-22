# -*- coding: utf-8 -*-
"""
Master Builder for Visar Murseli's Personal Knowledge Hub & S/4HANA Career OS.
Assembles all modules from portal_builder and writes to s4hana-prep-portal/index.html.
"""

import os
import sys

# Ensure current dir is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from portal_builder.header import get_header
from portal_builder.dashboard import get_dashboard
from portal_builder.cv_defense import get_cv_defense
from portal_builder.project import get_project
from portal_builder.solution_design import get_solution_design
from portal_builder.migration import get_migration
from portal_builder.tools import get_tools
from portal_builder.thesis import get_thesis
from portal_builder.enterprise_arch import get_enterprise_arch
from portal_builder.cheatsheet import get_cheatsheet
from portal_builder.career import get_career
from portal_builder.interview import get_interview
from portal_builder.files_tab import get_files_tab
from portal_builder.notebook import get_notebook
from portal_builder.vue_app import get_vue_app

def main():
    index_path = os.path.join(BASE_DIR, "index.html")

    html_parts = [
        get_header(),
        get_dashboard(),
        get_cv_defense(),
        get_project(),
        get_solution_design(),
        get_migration(),
        get_tools(),
        get_thesis(),
        get_enterprise_arch(),
        get_cheatsheet(),
        get_career(),
        get_interview(),
        get_files_tab(),
        get_notebook(),
        get_vue_app()
    ]

    full_html = "\n".join(html_parts)

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    size_kb = len(full_html.encode('utf-8')) / 1024
    print(f"[OK] Masterpiece generated successfully!")
    print(f"     Path: {index_path}")
    print(f"     Size: {size_kb:.2f} KB ({len(full_html)} chars)")

if __name__ == "__main__":
    main()
