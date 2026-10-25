#!/usr/bin/env python3
"""Customize a pinned upstream Nestbolt checkout for Knife Details. Fail closed."""
from pathlib import Path
import re
root=Path(__file__).resolve().parents[2]
app=root/"web/src/app.tsx"
html=root/"web/index.html"
s=app.read_text()
def replace_one(old,new):
    global s
    assert s.count(old)==1, f"Upstream changed or ambiguous: {old[:90]} (found {s.count(old)})"
    s=s.replace(old,new)
replace_one("{ label: 'Sheet metal 1250×2500', w: 1250, h: 2500 },","{ label: 'Knife Details 900×600', w: 900, h: 600 },\n  { label: 'Sheet metal 1250×2500', w: 1250, h: 2500 },")
replace_one("const blankSheet = (w = 600, h = 400): RequestSheet => ({","const blankSheet = (w = 900, h = 600): RequestSheet => ({")
replace_one("const emptyRequest = (): NestRequest => ({ parts: [], sheets: [blankSheet()], spacing_mm: 1, edge_spacing_mm: 1, mode: 'all' });","const emptyRequest = (): NestRequest => ({ parts: [], sheets: [blankSheet()], spacing_mm: 3, edge_spacing_mm: 0, mode: 'all' });")
# Set automatic rotations and mirror on imported parts only; do not alter third-party example settings.
old="rotations: ROTATIONS[0].value, allow_mirror: false, priority: 1"
count=s.count(old)
assert count==2,f"Expected two imported-part defaults, found {count}"
s=s.replace(old,"rotations: { kind: 'free' }, allow_mirror: true, priority: 1")
replace_one("<h1>Nestbolt</h1>","<h1>Knife Details <small style={{ fontWeight: 400, opacity: 0.55, fontSize: '0.55em' }}>powered by Nestbolt</small></h1>")
app.write_text(s)
h=html.read_text()
h=h.replace("<title>Nestbolt: free nesting for laser, CNC and fabric, in your browser</title>","<title>Knife Details — Fixed Sheet Nesting</title>")
# Remove upstream canonical and structured metadata so the fork does not claim upstream canonical URLs.
h=re.sub(r'\s*<link rel="canonical"[^>]*>', '',h)
h=re.sub(r'\s*<script type="application/ld\+json">.*?</script>', '',h, flags=re.S)
html.write_text(h)
print("Applied Knife Details defaults to pinned upstream.")
