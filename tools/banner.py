# Regenerate assets/banner.svg:
#   V=16.38.0; mkdir -p /tmp/si && for s in linux go hyprland proxmox rust react debian nodedotjs qt nginx typescript wayland cloudflare python vite archlinux cplusplus blender mysql gnubash nuxt sqlite threedotjs; do curl -s -o /tmp/si/$s.svg https://cdn.jsdelivr.net/npm/simple-icons@$V/icons/$s.svg; done
#   python3 -I tools/banner.py /tmp/si assets/banner.svg
# Builds the animated profile banner: name + role in front, slowly drifting
# rows of monochrome brand icons (simple-icons, CC0) over the whole background.
# Usage: python3 -I banner.py <icons-dir> <out.svg>
import re, sys, pathlib

icons_dir, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
ORDER = ["linux", "go", "hyprland", "proxmox", "rust", "react", "debian", "nodedotjs", "qt", "nginx",
         "typescript", "wayland", "cloudflare", "python", "vite", "archlinux", "cplusplus", "blender",
         "mysql", "gnubash", "nuxt", "sqlite", "threedotjs"]
W, H, CELL, SIZE = 840, 210, 52, 22
ROWS = [22, 64, 106, 148, 190]          # icon centre lines
ACCENT = {(1, 4), (3, 11), (4, 2)}      # (row, col): the few icons drawn in blue
COLS = -(-W // CELL) + 1                # icons per tile, one tile is wider than the banner
TILE = COLS * CELL

paths = {}
for slug in ORDER:
    svg = (icons_dir / f"{slug}.svg").read_text()
    d = re.search(r'<path d="([^"]+)"', svg).group(1)
    assert re.fullmatch(r"[0-9MmLlHhVvCcSsQqTtAaZz.,\- e]+", d), slug  # plain path data only
    paths[slug] = d

defs = "".join(f'<symbol id="{s}" viewBox="0 0 24 24"><path d="{d}"/></symbol>' for s, d in paths.items())

rows = []
for r, cy in enumerate(ROWS):
    uses = []
    for tile in (0, 1):                 # two identical tiles, so the loop has no seam
        for c in range(COLS):
            slug = ORDER[(c + r * 5) % len(ORDER)]
            x = tile * TILE + c * CELL + (CELL // 2 if r % 2 else 0) + (CELL - SIZE) / 2
            cls = "a" if (r, c) in ACCENT else "i"
            uses.append(f'<use href="#{slug}" x="{x:.0f}" y="{cy - SIZE / 2:.0f}" width="{SIZE}" height="{SIZE}" class="{cls}"/>')
    rows.append(f'<g class="r r{r % 2}" style="animation-duration:{150 + 20 * (r % 3)}s">{"".join(uses)}</g>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Luxend, founder and head developer at InstantNode">
<style>
.bg{{fill:#fff;stroke:#e5e5e5}}.i{{fill:#171717;opacity:.08}}.a{{fill:#3b82f6;opacity:.6}}.s{{stop-color:#fff}}
.n{{font:800 54px Inter,system-ui,-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;fill:#0a0a0a;letter-spacing:-1px}}
.m{{font:17px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#525252}}
.r{{animation:drift linear infinite}}.r1{{animation-direction:reverse}}
@keyframes drift{{from{{transform:translateX(0)}}to{{transform:translateX(-{TILE}px)}}}}
@media (prefers-color-scheme:dark){{.bg{{fill:#0d1117;stroke:#30363d}}.i{{fill:#e5e5e5;opacity:.07}}.s{{stop-color:#0d1117}}.n{{fill:#f5f5f5}}.m{{fill:#8b8b8b}}}}
@media (prefers-reduced-motion:reduce){{.r{{animation:none}}}}
</style>
<defs>{defs}
<clipPath id="c"><rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="6"/></clipPath>
<linearGradient id="f" x1="0" x2="1" y1="0" y2="0">
<stop offset="0" class="s" stop-opacity=".97"/><stop offset=".38" class="s" stop-opacity=".9"/><stop offset=".68" class="s" stop-opacity="0"/>
</linearGradient></defs>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="6" class="bg"/>
<g clip-path="url(#c)">{"".join(rows)}<rect width="{W}" height="{H}" fill="url(#f)"/></g>
<text x="40" y="112" class="n">Luxend</text>
<text x="42" y="148" class="m">Founder and head developer at InstantNode</text>
</svg>
'''
out.write_text(svg)
print(out, len(svg), "bytes")
