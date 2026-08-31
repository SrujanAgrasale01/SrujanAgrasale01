import json
from pathlib import Path

data = json.loads(Path("data/contributions.json").read_text(encoding="utf-8"))
days = data.get("days", [])
levels = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

W, H = 860, 205
cell_w, cell_h, gap = 14, 10, 3
left, top = 25, 80

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
svg.append('<rect width="860" height="205" rx="14" fill="#0d1117"/>')
svg.append('<rect x="1" y="1" width="858" height="203" rx="14" fill="none" stroke="#30363d"/>')
svg.append(f'<text x="25" y="34" fill="#8b949e" font-family="monospace" font-size="14">github@contributions ~ $ ./heatmap --user {data.get("username","")}</text>')
svg.append('<text x="25" y="57" fill="#58a6ff" font-family="monospace" font-size="12">live contribution activity • auto-updated by GitHub Actions</text>')

# Keep the latest 364 days and arrange them by week/day.
days = sorted(days, key=lambda x: x["date"])[-364:]
for i, item in enumerate(days):
    col = i // 7
    row = i % 7
    x = left + col * (cell_w + gap)
    y = top + row * (cell_h + gap)
    level = max(0, min(4, int(item.get("level", 0))))
    delay = round((col * 0.03) + (row * 0.01), 2)
    svg.append(
        f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" rx="2" '
        f'fill="{levels[level]}" opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" dur="0.35s" begin="{delay}s" fill="freeze"/></rect>'
    )

svg.append('<text x="25" y="190" fill="#8b949e" font-family="monospace" font-size="11">less</text>')
for j, c in enumerate(levels):
    svg.append(f'<rect x="{65+j*18}" y="181" width="12" height="10" rx="2" fill="{c}"/>')
svg.append('<text x="165" y="190" fill="#8b949e" font-family="monospace" font-size="11">more</text>')
svg.append("</svg>")

Path("contrib-heatmap.svg").write_text("\n".join(svg), encoding="utf-8")
