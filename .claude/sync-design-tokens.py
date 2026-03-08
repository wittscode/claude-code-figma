#!/usr/bin/env python3
"""
Auto-syncs design tokens from index.html into CLAUDE.md after every file edit.
Triggered by Claude Code PostToolUse hook.
"""

import json
import re
import sys
from pathlib import Path

def main():
    # Read hook payload from stdin
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    # Only run when index.html was edited or written
    tool_input = payload.get("tool_input", {})
    file_path = tool_input.get("file_path", "")
    if not file_path.endswith("index.html"):
        sys.exit(0)

    root = Path(file_path).parent
    html_file   = root / "index.html"
    claude_file = root / "CLAUDE.md"

    if not html_file.exists() or not claude_file.exists():
        sys.exit(0)

    html = html_file.read_text()

    # ── Extract :root { ... } block ──────────────────────────────────────────
    root_match = re.search(r':root\s*\{([^}]+)\}', html, re.DOTALL)
    if not root_match:
        sys.exit(0)

    raw = root_match.group(1)

    # Parse each CSS variable and its inline comment
    token_lines = []
    for line in raw.splitlines():
        line = line.strip()
        if not line or not line.startswith("--"):
            continue
        token_lines.append(f"  {line}" if not line.endswith(";") else f"  {line}")

    new_root_block = ":root {\n" + "\n".join(token_lines) + "\n}"

    # ── Extract fonts from <link> tags ───────────────────────────────────────
    font_match = re.search(r"family=([^&\"]+)", html)
    fonts = []
    if font_match:
        raw_fonts = re.findall(r"family=([^&\"]+)", html)
        for f in raw_fonts:
            fonts.append(f.replace("+", " ").split(":")[0])

    # ── Extract button variants ───────────────────────────────────────────────
    btn_variants = re.findall(r'\.(btn-\w+)\s*\{', html)
    btn_variants = sorted(set(v for v in btn_variants if v != "btn"))

    # ── Extract section selectors ─────────────────────────────────────────────
    sections = re.findall(r'<!--\s+([A-Z ]+)\s+-->', html)

    # ── Extract breakpoint ────────────────────────────────────────────────────
    bp_match = re.search(r'@media\s*\(max-width:\s*(\d+px)\)', html)
    breakpoint = bp_match.group(1) if bp_match else "768px"

    # ── Extract grid layouts ──────────────────────────────────────────────────
    grids = re.findall(r'\.([\w-]+)\s*\{[^}]*grid-template-columns:[^}]*\}', html, re.DOTALL)

    # ── Build updated CLAUDE.md ───────────────────────────────────────────────
    claude = claude_file.read_text()

    # Replace the :root code block (between ```css\n:root and closing ```)
    claude = re.sub(
        r'(```css\n):root \{[^`]+?\}(\n```)',
        lambda m: f"{m.group(1)}{new_root_block}{m.group(2)}",
        claude,
        count=1,
        flags=re.DOTALL
    )

    # Update breakpoint value
    claude = re.sub(
        r'Single breakpoint at `\d+px`',
        f'Single breakpoint at `{breakpoint}`',
        claude
    )

    claude_file.write_text(claude)
    print(f"[sync-design-tokens] CLAUDE.md updated from index.html ✓")

if __name__ == "__main__":
    main()
