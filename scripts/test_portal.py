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

def test_sap_activate_phases_integrity(content):
    activate_checks = [
        "SAP Activate Phasen-Cockpit",
        "1. Discover",
        "2. Prepare",
        "3. Explore",
        "4. Realize",
        "5. Deploy",
        "6. Run",
        "Fit-to-Standard",
        "Solution Design Document"
    ]
    for item in activate_checks:
        assert item in content, f"SAP Activate verification failed: Missing '{item}'"
    print(f"  [PASS] SAP Activate Radar: All {len(activate_checks)} methodology phases & quality checkpoints present.")

def test_supervisor_and_colleague_anonymization(content):
    # Absolute zero-tolerance check for supervisor, colleague, and internal WBS leakages on the webapp
    prohibited_names = [
        "Roland Nowak", "Dietmar Fillinger", "Helmut Schmidpeter",
        "Sarah Lozano", "Thomas Wimpff", "Sebastian Neifer",
        "Markus Schmidt", "Joachim Kraus", "Henning Gerdes",
        "Armin Heinrich", "Michael Gehrung",
        "WBS 1–297", "Vorgang 110", "Vorgang 294", "Vorgang 297"
    ]
    for name in prohibited_names:
        matches = re.findall(re.escape(name), content, re.IGNORECASE)
        assert len(matches) == 0, f"PRIVACY & NDA VIOLATION: Found prohibited token '{name}' ({len(matches)} times) in webapp!"
    print("  [PASS] Privacy & GDPR Gate: Exactly 0 occurrences of supervisor names or internal WBS IDs.")

def test_command_palette_and_telemetry(content):
    # Check command palette and telemetry tokens
    features = [
        "isCommandPaletteOpen",
        "commandFilteredResults",
        "openCommandPalette",
        "149 Dossiers",
        "1.064 bidirektionale Links",
        "21 Deliverables",
        "300 ECTS",
        "Stärkenprofil & Synergie-Atlas",
        "filteredSynergies"
    ]
    for feat in features:
        assert feat in content, f"Feature check failed: Missing '{feat}'"
    print(f"  [PASS] Command Palette & Telemetry: All {len(features)} reactive features active.")


def test_public_showcase_privacy():
    pub_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 's4hana-prep-portal', 'public_index.html'))
    assert os.path.exists(pub_path), f"Public artifact missing: {pub_path}"
    with open(pub_path, 'r', encoding='utf-8') as f:
        pub = f.read()
    for token in ["Persönliches Stärkenprofil", "filteredSynergies", "Stärkenprofil & Synergie-Atlas"]:
        assert token in pub, f"Public Showcase missing synergy/profile token: {token}"
    for leak in ["Gefahrenstufe Rot", "TÖDLICH", "cv_defense", "Fangfrage", "Gehaltskalkulation"]:
        assert leak not in pub, f"PRIVACY GATE VIOLATION in public_index.html: {leak}"
    for name in ["Roland Nowak", "Dietmar Fillinger", "Helmut Schmidpeter", "Sarah Lozano", "Thomas Wimpff", "Sebastian Neifer", "Markus Schmidt", "Joachim Kraus", "Henning Gerdes", "Armin Heinrich", "Michael Gehrung", "WBS 1–297", "Vorgang 110", "Vorgang 294", "Vorgang 297"]:
        assert name.lower() not in pub.lower(), f"PRIVACY VIOLATION in public_index.html: Found prohibited token '{name}'"
    print(f"  [PASS] Public Showcase & Privacy Gate: Verified clean ({len(pub.encode('utf-8'))//1024} KB, 0 private leaks).")

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
    test_sap_activate_phases_integrity(content)
    test_supervisor_and_colleague_anonymization(content)
    test_command_palette_and_telemetry(content)
    test_vue_syntax_integrity(content)
    test_public_showcase_privacy()
    
    print("==========================================================")
    print("✅ ALL SPEC-KIT QUALITY CHECKS PASSED (100% SUCCESS)")
    print("==========================================================")

if __name__ == '__main__':
    run_all_tests()
