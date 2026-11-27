#!/usr/bin/env python3
"""tokens.json에서 도구별 테마 파일을 dist/와 specimen/에 만든다.

    python3 generate.py          # 만든다
    python3 generate.py --check  # 대비 기준을 확인하고, dist/가 tokens.json과 맞는지 본다 (CI)
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOKENS = json.loads((ROOT / "tokens.json").read_text())
ANSI_NAMES = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def luminance(h):
    def ch(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def xterm256(h):
    """가장 가까운 xterm 256색 번호 (16–255만 본다. 0–15는 터미널마다 다르다)"""
    levels = [0, 95, 135, 175, 215, 255]
    cands = {16 + 36 * r + 6 * g + b: (levels[r], levels[g], levels[b]) for r in range(6) for g in range(6) for b in range(6)}
    cands.update({232 + i: (8 + 10 * i,) * 3 for i in range(24)})
    t = rgb(h)
    return min(cands, key=lambda k: sum((x - y) ** 2 for x, y in zip(cands[k], t)))


def palette(v):
    p = dict(v["primitive"])
    for i, h in enumerate(v["ansi"]):
        p[f"ansi{i}"] = h
    return p


def ref(v, name):
    return palette(v).get(name, name)


# ---------------- 검사 ----------------
def problems():
    out, c = [], TOKENS["contrast"]
    for key, v in TOKENS["variants"].items():
        p = v["primitive"]
        for rule in ("text", "faint"):
            for bg in c[rule]["on"]:
                for fg in c[rule]["fg"]:
                    r = contrast(p[fg], p[bg])
                    if r < c[rule]["min"]:
                        out.append(f"{key}: {fg} on {bg} {r:.2f} < {c[rule]['min']}")
        for i, h in enumerate(v["ansi"]):
            if i in (0, 8):
                need = c["ansi_dim_min"] if i == 8 else 0
            else:
                need = c["ansi_min"]
            r = contrast(h, p["void"])
            if r < need:
                out.append(f"{key}: ansi{i} {h} on void {r:.2f} < {need}")
    return out


# ---------------- 만들 파일 ----------------
def css():
    lines = ["/* tempo-theme: tokens.json에서 generate.py가 만든다. 고치지 말 것 */"]
    for key, v in TOKENS["variants"].items():
        p = v["primitive"]
        lines.append(f':root[data-theme="tempo-{key}"], .tempo-{key} {{')
        lines.append("  color-scheme: dark;")
        lines.append("  " + " ".join(f"--tempo-{k}: {h};" for k, h in p.items()))
        lines.append("  " + " ".join(f"--{k}: var(--tempo-{n});" for k, n in TOKENS["semantic"].items()))
        lines.append("  " + " ".join(f"--{k}: color-mix(in srgb, var(--tempo-{n}) {pct}%, var(--tempo-archive));" for k, (n, pct) in TOKENS["tint"].items()))
        lines.append(f"  --tempo-glow: 0 0 10px color-mix(in srgb, var(--tempo-thread) 45%, transparent); --tempo-selection: {v['selection']};")
        lines.append("}")
    return "\n".join(lines) + "\n"


def itermcolors(v):
    def entry(name, h):
        r, g, b = (x / 255 for x in rgb(h))
        return (f"\t<key>{name}</key>\n\t<dict>\n\t\t<key>Alpha Component</key>\n\t\t<real>1</real>\n"
                f"\t\t<key>Blue Component</key>\n\t\t<real>{b:.6f}</real>\n\t\t<key>Color Space</key>\n\t\t<string>sRGB</string>\n"
                f"\t\t<key>Green Component</key>\n\t\t<real>{g:.6f}</real>\n\t\t<key>Red Component</key>\n\t\t<real>{r:.6f}</real>\n\t</dict>\n")
    p = v["primitive"]
    items = [(f"Ansi {i} Color", h) for i, h in enumerate(v["ansi"])] + [
        ("Background Color", p["void"]), ("Foreground Color", p["paper"]), ("Bold Color", p["paper"]),
        ("Cursor Color", ref(v, v["cursor"])), ("Cursor Text Color", p["void"]), ("Cursor Guide Color", p["drawer"]),
        ("Selection Color", v["selection"]), ("Selected Text Color", p["paper"]), ("Link Color", p["brass"]),
        ("Badge Color", p["brass"]), ("Tab Color", p["archive"])]
    body = "".join(entry(n, h) for n, h in sorted(items))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" '
            '"http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n<plist version="1.0">\n<dict>\n' + body + "</dict>\n</plist>\n")


def ghostty(v):
    p = v["primitive"]
    out = [f"palette = {i}={h}" for i, h in enumerate(v["ansi"])]
    out += [f"background = {p['void']}", f"foreground = {p['paper']}", f"cursor-color = {ref(v, v['cursor'])}",
            f"cursor-text = {p['void']}", f"selection-background = {v['selection']}", f"selection-foreground = {p['paper']}"]
    return "\n".join(out) + "\n"


def herdr(v):
    p, a = v["primitive"], v["ansi"]
    custom = {"accent": p["brass"], "panel_bg": p["void"], "sidebar_bg": p["archive"], "active_row_bg": p["drawer"],
              "selection_bg": v["selection"], "surface0": p["archive"], "surface1": p["drawer"], "surface_dim": p["void"],
              "overlay0": p["ash"], "overlay1": p["dust"], "text": p["paper"], "subtext0": p["dust"],
              "mauve": a[5], "green": p["thread"], "yellow": p["signal"], "red": p["branch"], "blue": a[4], "teal": a[6], "peach": p["brass"]}
    return (f"# {v['title']} — ~/.config/herdr/config.toml에 붙인다\n[theme]\nname = \"catppuccin\"\n\n[theme.custom]\n"
            + "".join(f'{k} = "{h}"\n' for k, h in custom.items()))


def ansi256(v):
    return json.dumps({k: xterm256(h) for k, h in palette(v).items()}, indent=2) + "\n"


def swift():
    out = ["// tempo-theme: tokens.json에서 generate.py가 만든다. 고치지 말 것", "import AppKit", "",
           "enum TempoTheme {", "    struct Palette {"]
    keys = list(next(iter(TOKENS["variants"].values()))["primitive"])
    out += [f"        let {k}: NSColor" for k in keys] + ["    }", ""]
    for key, v in TOKENS["variants"].items():
        args = ",\n".join(f"        {k}: rgb(0x{v['primitive'][k][1:]})" for k in keys)
        out.append(f"    static let {key} = Palette(\n{args}\n    )\n")
    out += ["    private static func rgb(_ hex: UInt32) -> NSColor {",
            "        NSColor(srgbRed: CGFloat((hex >> 16) & 0xff) / 255, green: CGFloat((hex >> 8) & 0xff) / 255,",
            "                blue: CGFloat(hex & 0xff) / 255, alpha: 1)", "    }", "}"]
    return "\n".join(out) + "\n"


def obsidian(v):
    p, a = v["primitive"], v["ansi"]
    m = {"background-primary": p["void"], "background-primary-alt": p["archive"], "background-secondary": p["archive"],
         "background-secondary-alt": p["drawer"], "background-modifier-border": p["seam"], "background-modifier-hover": p["drawer"],
         "text-normal": p["paper"], "text-muted": p["dust"], "text-faint": p["ash"], "text-accent": p["brass"],
         "text-accent-hover": a[11], "interactive-accent": p["brass"], "interactive-accent-hover": a[11],
         "text-on-accent": p["void"], "text-selection": v["selection"], "text-highlight-bg": f"{p['signal']}33",
         "text-error": p["branch"], "text-success": p["thread"], "text-warning": p["signal"],
         "color-red": p["branch"], "color-green": p["thread"], "color-yellow": p["signal"], "color-orange": p["brass"],
         "color-blue": a[4], "color-purple": a[5], "color-cyan": a[6], "code-background": p["archive"]}
    return (f"/* {v['title']} — Obsidian 설정 > 모양 > CSS 스니펫. tokens.json에서 generate.py가 만든다 */\n.theme-dark {{\n"
            + "".join(f"  --{k}: {h};\n" for k, h in m.items()) + "}\n")


def specimen():
    tpl = (ROOT / "specimen" / "template.html").read_text()
    sw = lambda key: "".join(
        f'<div><i style="background:{h}"></i><b>{k}</b><span>{h}</span></div>' for k, h in TOKENS["variants"][key]["primitive"].items())
    ansi = lambda key: "".join(f'<i style="background:{h}" title="ansi{i} {h}"></i>' for i, h in enumerate(TOKENS["variants"][key]["ansi"]))
    for key, v in TOKENS["variants"].items():
        tpl = tpl.replace(f"{{{{swatches:{key}}}}}", sw(key)).replace(f"{{{{ansi:{key}}}}}", ansi(key)).replace(f"{{{{label:{key}}}}}", v["label"])
    return tpl


def claude_design():
    d = ROOT / "design"
    style = css() + (d / "components.css").read_text() + (d / "preview.css").read_text()

    def fill(frag, key):
        v = TOKENS["variants"][key]
        p = v["primitive"]
        sw = "".join(f'<div><i style="background:{h}"></i><b>{k}</b><span>{h}</span></div>' for k, h in p.items())
        ansi = "".join(f'<i style="background:{h}" title="ansi{i} {h}"></i>' for i, h in enumerate(v["ansi"]))
        rows = "".join(f'<tr><td class="mono">--{k}</td><td>{n}</td><td><i class="chip" style="background:{p[n]}"></i><span class="mono">{p[n]}</span></td></tr>'
                       for k, n in TOKENS["semantic"].items())
        rows += "".join(f'<tr><td class="mono">--{k}</td><td>{n} {pct}%</td><td><i class="chip" style="background:var(--{k})"></i>archive 위</td></tr>'
                        for k, (n, pct) in TOKENS["tint"].items())
        for name, val in (("label", v["label"]), ("swatches", sw), ("ansi", ansi), ("semantic", rows)):
            frag = frag.replace("{{" + name + "}}", val)
        return frag

    files = {"dist/claude-design/README.md": (d / "guide.md").read_text(), "dist/claude-design/tokens.css": css()}
    for card in sorted((d / "cards").glob("*.html")):
        marker, frag = card.read_text().split("\n", 1)
        body = "".join(f'<section class="v tempo-{key}">\n{fill(frag, key)}</section>\n' for key in TOKENS["variants"])
        files[f"dist/claude-design/preview/{card.name}"] = (
            f'{marker}\n<!doctype html>\n<html lang="ko">\n<meta charset="utf-8">\n<title>tempo · {card.stem}</title>\n'
            f'<style>\n{style}</style>\n<body>\n<div class="pair">\n{body}</div>\n</body>\n</html>\n')
    return files


def outputs():
    files = {"dist/css/tempo.css": css(), "dist/swift/TempoTheme.swift": swift(), "specimen/index.html": specimen()}
    for key, v in TOKENS["variants"].items():
        files[f"dist/iterm2/{v['title']}.itermcolors"] = itermcolors(v)
        files[f"dist/ghostty/tempo-{key}"] = ghostty(v)
        files[f"dist/herdr/tempo-{key}.toml"] = herdr(v)
        files[f"dist/ansi256/tempo-{key}.json"] = ansi256(v)
        files[f"dist/obsidian/tempo-{key}.css"] = obsidian(v)
    files.update(claude_design())
    return files


def main():
    bad = problems()
    for b in bad:
        print("대비 부족:", b, file=sys.stderr)
    stale = []
    for rel, text in outputs().items():
        f = ROOT / rel
        if "--check" in sys.argv:
            if not f.exists() or f.read_text() != text:
                stale.append(rel)
        else:
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(text)
    for s in stale:
        print("다시 만들어야 함:", s, file=sys.stderr)
    if bad or stale:
        sys.exit(1)
    print("check ok" if "--check" in sys.argv else f"{len(outputs())}개 파일을 만들었다")


if __name__ == "__main__":
    main()
