# -*- coding: utf-8 -*-
"""
Data Science RAG & Knowledge Graph Quality Validator
Verifies 100% LLM Readiness, Graph Edge Integrity, and Schema Compliance.
Author: Visar Murseli, M.Sc. | Data Science & Enterprise AI Architect
"""

import os
import re
import json

VAULT_DIR = r"C:\Users\SHQIPTAR634\Documents\Obsidian Vault"

def run_validation():
    print("=" * 70)
    print("🔬 RUNNING OBSIDIAN VAULT DATA SCIENCE & LLM-READINESS AUDIT")
    print("=" * 70)

    md_files = []
    all_basenames = {}
    for r, ds, fs in os.walk(VAULT_DIR):
        ds[:] = [d for d in ds if d not in (".obsidian", ".trash")]
        for f in fs:
            if f.endswith(".md"):
                fullpath = os.path.join(r, f)
                rel = os.path.relpath(fullpath, VAULT_DIR)
                bname = os.path.splitext(f)[0].lower()
                all_basenames[bname] = rel
                md_files.append((f, rel, fullpath))

    total_files = len(md_files)
    valid_fm_count = 0
    missing_fm = []
    broken_links = []
    total_links = 0
    multi_h1_files = []
    word_counts = []
    domains = {}
    types = {}

    for fname, rel, fullpath in md_files:
        with open(fullpath, "r", encoding="utf-8", errors="ignore") as fp:
            content = fp.read()

        words = len(content.split())
        word_counts.append(words)

        # 1. Frontmatter check
        fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if fm_match:
            valid_fm_count += 1
            fm_txt = fm_match.group(1)
            for line in fm_txt.splitlines():
                if line.startswith("domain:"):
                    d = line.split(":", 1)[1].strip()
                    domains[d] = domains.get(d, 0) + 1
                elif line.startswith("type:"):
                    t = line.split(":", 1)[1].strip()
                    types[t] = types.get(t, 0) + 1
        else:
            missing_fm.append(rel)

        # 2. Wikilinks check
        links = re.findall(r'\[\[(.*?)\]\]', content)
        total_links += len(links)
        for l in links:
            raw = l.split("|")[0].split("#")[0].strip().lower()
            if raw and raw not in all_basenames:
                broken_links.append((rel, l))

        # 3. Heading check
        body = content[len(fm_match.group(0)):] if fm_match else content
        h1s = re.findall(r'^#\s+(.*)', body, flags=re.MULTILINE)
        if len(h1s) > 1:
            multi_h1_files.append((rel, len(h1s)))

    print(f"\n[1] METADATA & SCHEMA COMPLIANCE:")
    print(f"    - Total Markdown Documents: {total_files}")
    print(f"    - Files with Valid Frontmatter: {valid_fm_count} ({valid_fm_count / total_files * 100:.1f}%)")
    if missing_fm:
        print(f"    - ❌ Missing Frontmatter ({len(missing_fm)}): {missing_fm}")
    else:
        print(f"    - ✅ 100% Frontmatter Schema Compliance Achieved!")

    print(f"\n[2] KNOWLEDGE GRAPH INTEGRITY & EDGE DENSITY:")
    print(f"    - Total Semantic Edges (Wikilinks): {total_links}")
    print(f"    - Average Outgoing Links per Note: {total_links / total_files:.1f}")
    print(f"    - Broken Link Occurrences: {len(broken_links)}")
    if broken_links:
        print(f"    - ⚠️ Remaining Broken Links ({len(broken_links)}):")
        for src, target in broken_links[:10]:
            print(f"        In {src} -> [[{target}]]")
    else:
        print(f"    - ✅ 100% Graph Connectivity (0 Broken Links)!")

    print(f"\n[3] AST HEADING HIERARCHY & CHUNKING SANITY:")
    print(f"    - Files with Multiple H1 Tags: {len(multi_h1_files)}")
    if multi_h1_files:
        for src, cnt in multi_h1_files:
            print(f"        {src}: {cnt} H1 tags")
    else:
        print(f"    - ✅ 100% Clean Single-H1 AST Hierarchy Across All Notes!")

    print(f"\n[4] DOMAIN ONTOLOGY DISTRIBUTION:")
    for d, c in sorted(domains.items(), key=lambda x: x[1], reverse=True):
        print(f"    - {d}: {c} notes")

    print(f"\n[5] NOTE TYPE CLASSIFICATION:")
    for t, c in sorted(types.items(), key=lambda x: x[1], reverse=True):
        print(f"    - {t}: {c} notes")

    print(f"\n[6] INFORMATION CAPACITY & FILE CHUNKING HEALTH:")
    layer1 = [(f, rel, full) for f, rel, full in md_files if not rel.startswith("05_Archiv")]
    layer2 = [(f, rel, full) for f, rel, full in md_files if rel.startswith("05_Archiv")]
    print(f"    - Layer 1 (Curated Knowledge & Profile Foreground): {len(layer1)} notes")
    print(f"    - Layer 2 (05_Archiv/Volltexte_DataLake Archive): {len(layer2)} notes")
    print(f"    - Total Word Count: {sum(word_counts):,} words")
    print(f"    - Total Token Estimate: ~{int(sum(word_counts) * 1.35):,} tokens")
    oversized = [(rel, round(os.path.getsize(full) / (1024 * 1024), 2)) for _, rel, full in md_files if os.path.getsize(full) > 10 * 1024 * 1024]
    print(f"    - Oversized Files (>10 MB): {len(oversized)}")
    for rel, mb in oversized:
        print(f"        ⚠️ {rel}: {mb:.2f} MB")

    manifest_path = os.path.join(VAULT_DIR, "graph_manifest.json")
    orphan_count = 0
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, "r", encoding="utf-8") as mf:
                mdata = json.load(mf)
            node_ids = {n["id"] for n in mdata.get("nodes", [])}
            connected = {e["source"] for e in mdata.get("edges", [])} | {e["target"] for e in mdata.get("edges", [])}
            orphan_count = len(node_ids - connected)
            print(f"    - Graph Orphans (0 in & 0 out in manifest): {orphan_count}")
        except Exception:
            pass

    # Overall verdict
    is_success = (valid_fm_count == total_files) and (len(broken_links) == 0) and (len(multi_h1_files) == 0) and (len(oversized) == 0) and (orphan_count == 0)
    print("\n" + "=" * 70)
    if is_success:
        print("🎯 FINAL VERDICT: 100% LLM & RAG READINESS - PASSED WITH DISTINCTION")
    else:
        print(f"⚠️ FINAL VERDICT: ATTENTION NEEDED ({len(broken_links)} links, {len(multi_h1_files)} headings, {len(oversized)} oversized, {orphan_count} orphans)")
    print("=" * 70)

if __name__ == "__main__":
    run_validation()
