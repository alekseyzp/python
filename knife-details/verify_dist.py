#!/usr/bin/env python3
"""Reject broken/static-only frontend artifacts before publishing."""
import sys
from pathlib import Path
import re
root=Path(sys.argv[1]).resolve()
assert root.is_dir(), "Missing Vite dist directory"
index=(root/"index.html").read_text(encoding="utf-8")
assert "Knife Details" in index, "Branding was not compiled"
wasm=list(root.rglob("*.wasm"))
assert wasm, "Genuine Rust WebAssembly module missing"
for f in wasm:
    data=f.read_bytes()
    assert len(data)>100_000, f"Suspiciously small WASM: {f}"
    assert data[:4]==b"\0asm", f"Invalid WASM signature: {f}"
scripts=re.findall(r'(?:src|href)="([^"]+)"', index)
for path in scripts:
    if path.startswith(("./assets/","assets/")):
        assert (root/path.lstrip("./")).is_file(), f"Broken asset reference: {path}"
assert any(p.suffix==".js" for p in root.rglob("*.js")), "Missing JS application"
assert any(p.name=="THIRD_PARTY_NOTICES.txt" for p in root.rglob("*")), "Missing dependency notices"
print("VALID: genuine WebAssembly, frontend assets, package notices and Knife Details branding")
for p in wasm: print("WASM:",p.relative_to(root),p.stat().st_size,"bytes")
