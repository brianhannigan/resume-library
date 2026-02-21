#!/usr/bin/env python3
import argparse, json, re, pathlib

parser = argparse.ArgumentParser()
parser.add_argument('--resume', required=True, help='Path to resume markdown')
parser.add_argument('--keywords', required=True, help='Path to keywords json')
args = parser.parse_args()

text = pathlib.Path(args.resume).read_text(encoding='utf-8').lower()
kw = json.loads(pathlib.Path(args.keywords).read_text(encoding='utf-8'))

def coverage(words):
    found, missing = [], []
    for w in words:
        pat = re.escape(w.lower())
        if re.search(r'\b'+pat+r'\b', text) or w.lower() in text:
            found.append(w)
        else:
            missing.append(w)
    return found, missing

must_found, must_missing = coverage(kw.get('must_have', []))
nice_found, nice_missing = coverage(kw.get('nice_to_have', []))

out = pathlib.Path('dist/ats_report.md')
out.parent.mkdir(parents=True, exist_ok=True)

lines = [
"# ATS Keyword Coverage", "",
f"Resume: {args.resume}", f"Keywords: {args.keywords}", "",
"## Must‑Have",
f"Found ({len(must_found)}): " + (', '.join(must_found) or '—'),
f"Missing ({len(must_missing)}): " + (', '.join(must_missing) or '—'), "",
"## Nice‑to‑Have",
f"Found ({len(nice_found)}): " + (', '.join(nice_found) or '—'),
f"Missing ({len(nice_missing)}): " + (', '.join(nice_missing) or '—'),
""
]
out.write_text("\n".join(lines), encoding='utf-8')
print(f"Wrote ATS report → {out}")
