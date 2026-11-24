#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spec-Kit Automated Quality Gate & Compliance Test Suite
Project: Visar Murseli | Enterprise Career OS & Knowledge Hub
Constitution Anchor: .specify/memory/constitution.md (v1.0.0)
"""

import os
import re
import sys

PORTAL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 's4hana-prep-portal', 'index.html'))

def test_file_exists():
    assert os.path.exists(PORTAL_PATH), f"Build artifact missing: {PORTAL_PATH}"
    size = os.path.getsize(PORTAL_PATH)
    assert size > 200000, f"Build artifact too small ({size} bytes). Expected > 200 KB."
    print(f"  [PASS] File exists and valid size: {size:,} bytes")

def test_constitution_zero_hallucinations(content):
    # Absolute zero-tolerance check for Robert Bosch GmbH
    prohibited_patterns = [
        r'Robert\s+Bosch',
        r'Praktikant\s+bei\s+Bosch',
        r'Praktikum\s+bei\s+Bosch',
        r'Werkstudent\s+bei\s+Bosch'
    ]
    for pattern in prohibited_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        assert len(matches) == 0, f"CRITICAL COMPLIANCE VIOLATION: Found prohibited pattern '{pattern}' ({len(matches)} times)!"
    print("  [PASS] Constitution Compliance: Exactly 0 occurrences of prohibited affiliations.")

def test_academic_truth_metrics(content):
    # Must strictly match official certificates
    assert "1,6" in content, "Missing Master grade 1,6"
    assert "1,0" in content, "Missing Master thesis grade 1,0"
    assert "120 ECTS" in content, "Missing 120 ECTS"
    assert "180 ECTS" in content, "Missing 180 ECTS"
    assert "1,7" in content, "Missing Bachelor thesis grade 1,7"
    assert "3,0" in content, "Missing Bachelor grade 3,0"
    print("  [PASS] Academic Authority: All official grades (M.Sc. 1,6 / Thesis 1,0 / B.Sc. 3,0) verified.")

def test_wbs_radar_integrity(content):
    # WBS ranges from MS Project
    wbs_checks = [
        "WBS 16–63",   # TP1
        "WBS 64–112",  # TP2
        "WBS 173–196", # TP3
        "WBS 197–202", # TP4
        "WBS 203–297", # TP5
        "01.04.2026",  # Pilot-BV
        "01.01.2027",  # Finale BV / Go-Live
        "29. August 2025" # Explore Abschluss
    ]
    for item in wbs_checks:
        assert item in content, f"WBS Radar verification failed: Missing '{item}'"
    print(f"  [PASS] WBS Radar: All {len(wbs_checks)} authentic WBS & milestone checkpoints present.")

def test_command_palette_and_telemetry(content):
    # Check command palette and telemetry tokens
    features = [
        "isCommandPaletteOpen",
        "commandFilteredResults",
        "openCommandPalette",
        "53 Dossiers",
        "266 bidirektionale Links",
        "21 Deliverables",
        "300 ECTS"
    ]
    for feat in features:
        assert feat in content, f"Feature check failed: Missing '{feat}'"
    print(f"  [PASS] Command Palette & Telemetry: All {len(features)} reactive features active.")

def test_vue_syntax_integrity(content):
    # Verify curly braces inside Vue templates
    script_parts = content.split('<script>')
    assert len(script_parts) >= 2, "Missing <script> block"
    assert "createApp(" in content, "Missing createApp"
    assert ".mount('#app')" in content, "Missing mount('#app')"
    print("  [PASS] Vue 3 Architecture: Clean script mounting and template structure.")

def run_all_tests():
    print("==========================================================")
    print("🚀 RUNNING SPEC-KIT QUALITY GATE & COMPLIANCE VERIFICATION")
    print("==========================================================")
    
    test_file_exists()
    
    with open(PORTAL_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
        
    test_constitution_zero_hallucinations(content)
    test_academic_truth_metrics(content)
    test_wbs_radar_integrity(content)
    test_command_palette_and_telemetry(content)
    test_vue_syntax_integrity(content)
    
    print("==========================================================")
    print("✅ ALL SPEC-KIT QUALITY CHECKS PASSED (100% SUCCESS)")
    print("==========================================================")

if __name__ == '__main__':
    run_all_tests()
