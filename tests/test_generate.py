import copy
import json
import plistlib
import subprocess
import sys
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import generate  # noqa: E402


class Generate(unittest.TestCase):
    def test_tokens_meet_contrast(self):
        self.assertEqual(generate.problems(), [])

    def test_low_contrast_is_reported(self):
        saved = generate.TOKENS
        try:
            generate.TOKENS = copy.deepcopy(saved)
            generate.TOKENS["variants"]["ember"]["primitive"]["dust"] = "#2a241d"
            generate.TOKENS["variants"]["ember"]["ansi"][4] = "#1f2a33"
            got = generate.problems()
        finally:
            generate.TOKENS = saved
        self.assertTrue(any("dust on void" in p for p in got), got)
        self.assertTrue(any("ansi4" in p for p in got), got)

    def test_dist_matches_tokens(self):
        r = subprocess.run([sys.executable, str(ROOT / "generate.py"), "--check"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_variants_share_keys(self):
        vs = list(generate.TOKENS["variants"].values())
        self.assertTrue(all(v["primitive"].keys() == vs[0]["primitive"].keys() and len(v["ansi"]) == 16 for v in vs))

    def test_iterm_ghostty_herdr_parse(self):
        for key, v in generate.TOKENS["variants"].items():
            plist = plistlib.loads((ROOT / f"dist/iterm2/{v['title']}.itermcolors").read_bytes())
            self.assertEqual(len([k for k in plist if k.startswith("Ansi ")]), 16)
            bg = plist["Background Color"]
            self.assertEqual(tuple(round(bg[f"{c} Component"] * 255) for c in ("Red", "Green", "Blue")), generate.rgb(v["primitive"]["void"]))
            lines = (ROOT / f"dist/ghostty/tempo-{key}").read_text().splitlines()
            self.assertEqual([l.split("=", 1)[0].strip() for l in lines].count("palette"), 16)
            herdr = tomllib.loads((ROOT / f"dist/herdr/tempo-{key}.toml").read_text())
            self.assertEqual(len(herdr["theme"]["custom"]), 19)
            self.assertEqual(herdr["theme"]["custom"]["text"], v["primitive"]["paper"])

    def test_xterm256_nearest(self):
        self.assertEqual(generate.xterm256("#000000"), 16)
        self.assertEqual(generate.xterm256("#ffffff"), 231)
        self.assertEqual(generate.xterm256("#d78700"), 172)

    def test_css_semantic_names_match_dashboard(self):
        css = (ROOT / "dist/css/tempo.css").read_text()
        for name in ("--bg:", "--panel:", "--ink:", "--muted:", "--accent:", "--ok:", "--warn:", "--err:", "--ok-bg:", "--line:"):
            self.assertEqual(css.count(name), len(generate.TOKENS["variants"]), name)


    def test_claude_design_cards(self):
        cards = sorted((ROOT / "dist/claude-design/preview").glob("*.html"))
        self.assertEqual(len(cards), len(list((ROOT / "design/cards").glob("*.html"))))
        for f in cards:
            text = f.read_text()
            self.assertRegex(text.split("\n", 1)[0], r'^<!-- @dsCard group="[^"]+" -->$', f.name)
            self.assertNotIn("{{", text, f.name)
            self.assertNotIn("<link", text, f"{f.name}: 카드는 혼자 열려야 한다")
            for key in generate.TOKENS["variants"]:
                self.assertIn(f'class="v tempo-{key}"', text, f.name)
        guide = (ROOT / "dist/claude-design/README.md").read_text()
        self.assertEqual(guide, (ROOT / "design/guide.md").read_text())


    def test_kit_has_tokens_and_parts(self):
        kit = (ROOT / "dist/css/tempo-kit.css").read_text()
        self.assertTrue(kit.startswith((ROOT / "dist/css/tempo.css").read_text()))
        self.assertTrue(kit.endswith((ROOT / "design/components.css").read_text()))

    def test_conventions_classes_exist_in_kit(self):
        import re
        kit = (ROOT / "dist/css/tempo-kit.css").read_text()
        conv = (ROOT / ".design-sync/conventions.md").read_text()
        part = conv.split("## 부품 클래스", 1)[1].split("## 어디를 읽나", 1)[0]
        names = set(re.findall(r"\.([a-z][a-z0-9-]*)", " ".join(re.findall(r"`([^`]+)`", part))))
        self.assertTrue(names)
        missing = sorted(n for n in names if not re.search(r"\." + re.escape(n) + r"(?![a-z0-9-])", kit))
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
