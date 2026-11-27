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


if __name__ == "__main__":
    unittest.main()
