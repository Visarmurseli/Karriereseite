# -*- coding: utf-8 -*-
import os
from collections import Counter

ws = r"c:\Users\SHQIPTAR634\Desktop\SSB Dateien"
ext_counter = Counter()
dir_counter = Counter()
pillar_exts = {}
total_files = 0
total_bytes = 0

for root, dirs, files in os.walk(ws):
    if any(k in root for k in ['.git', '.obsidian', '__pycache__', '.specify']):
        continue
    rel = os.path.relpath(root, ws)
    top = rel.split(os.sep)[0] if rel != '.' else 'ROOT'
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        ext_counter[ext] += 1
        dir_counter[top] += 1
        pillar_exts.setdefault(top, Counter())[ext] += 1
        total_files += 1
        try:
            total_bytes += os.path.getsize(os.path.join(root, f))
        except:
            pass

print(f"Total files in workspace: {total_files}")
print(f"Total workspace size: {total_bytes / (1024*1024):.1f} MB")
print("\nFiles by Pillar / Directory:")
for d, c in sorted(dir_counter.items()):
    print(f"  {d}: {c} files")

print("\nTop 15 File Extensions:")
for ext, count in ext_counter.most_common(15):
    lbl = ext if ext else "[no ext]"
    print(f"  {lbl:<12}: {count:>5} files")

print("\nBreakdown of Document Formats per Pillar:")
doc_exts = {'.pdf', '.docx', '.doc', '.pptx', '.ppt', '.xlsx', '.xls', '.txt', '.md', '.html', '.zip'}
for p, counts in sorted(pillar_exts.items()):
    relevant = {k: v for k, v in counts.items() if k in doc_exts}
    if relevant:
        print(f"  {p}: {sum(relevant.values())} extractable docs {dict(relevant)}")
