# design-sync notes

- Tokens-only DS: no React components. Root `package.json` and `index.js` (`export {};`) exist only so the converter has a package entry; `[ZERO_MATCH] ... treating as tokens-only DS` is expected.
- Build: `python3 generate.py` regenerates `dist/` (committed). Converter deps (esbuild, ts-morph, @types/react, react@18, react-dom@18) are installed in `.ds-sync/`; pass `--node-modules ./.ds-sync/node_modules --entry ./index.js`.
- Driver runs with `--no-render-check`: there are no previews to render, so playwright was never installed. `! [RENDER_SKIPPED]` is the one expected warning. `[DTS_REACT]` is irrelevant with zero components.
- Only `dist/css/tempo.css` (`cssEntry`) and `design/guide.md` (`guidelinesGlob`) are published. `design/components.css` (`.card`, `.st.ok`, …) and the `design/cards/*.html` @dsCard cards are NOT synced; those target the older claude.ai/design project bundle in `dist/claude-design/`.
- `tokens.json` shows 23 of 28 vars: `--ok-bg` `--warn-bg` `--err-bg` `--info-bg` `--tempo-glow` use `color-mix()`, which the artifact page cannot read. They still ship in `components/bundle.css`, but only under `[data-theme="tempo-*"]` / `.tempo-*`; the conventions header tells the agent to set `data-theme`.

## Re-sync risks

- Conventions header names every semantic var; a renamed or added token in `tokens.json` needs a matching edit in `.design-sync/conventions.md`.
- Node 18.19 was used; some converter deps declare `node >=20` (EBADENGINE warnings) but the build passed.
