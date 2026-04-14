# Decisions

## 2026-04-14 — Use `<div>` instead of `<h1>`-`<h6>` inside `st.markdown` HTML when you need a specific layout

**Rule:** Inside `st.markdown(..., unsafe_allow_html=True)`, never put `<h1>`-`<h6>` tags inside a container where you need flex, grid, or any specific layout to hold. Use `<div>` (or `<p>`, `<span>`) with an explicit styling class instead. This applies to Treatment C cards, custom headers, any component where you inject raw HTML.

**Why:** Streamlit has a heading interceptor that processes all `<h1>`-`<h6>` elements in markdown output for anchor linking. It wraps each one in `<div data-testid="stHeadingWithActionElements">` and hoists the heading OUT of its original parent container, appending an anchor-link SVG next to it. If your `<h4>` was inside a `display: flex` parent alongside other children, the flex layout breaks because the h4 is no longer a direct child — the `stHeadingWithActionElements` wrapper is, and it has its own sizing that doesn't play nice with flex space-between or grid templates.

**How we hit it:** Session 5 `.sku-usage-card` component. First iteration of `render_sku_usage_card` put the SKU name in an `<h4>` alongside a `<span class="count-pill">` inside a `<div class="header">` with `display: flex; justify-content: space-between`. In the live DOM, the h4 and the pill had drastically different y-coordinates (nameY=-732, pillY=-703) — the h4 had been ripped out of the flex container and was floating elsewhere. Fix: swapped to `<div class="sku-name">` with explicit CSS for the Barlow Condensed / uppercase / variant color styling. Flex layout held perfectly on the next render.

**Rule going forward:**
- **DO**: use `<div class="...">` for all text-heavy elements inside Treatment C cards and custom HTML components
- **DO**: apply typographic styling (font-size, font-weight, color, text-transform) via CSS classes on those divs
- **DON'T**: use `<h1>`-`<h6>` tags inside markdown-injected HTML when you need a specific layout to hold — Streamlit will break it
- **Exception**: `<h1>`-`<h6>` are fine at the TOP LEVEL of a markdown block (outside any flex/grid container), since they stand alone and the stHeadingWithActionElements wrapping doesn't break anything

**Symptom to recognize:** Flex/grid layouts look correct in CSS but the DOM shows elements at the wrong y-position. First thing to check: are any `<h1>`-`<h6>` tags inside the container? If yes, swap them for `<div>` and the layout will probably snap into place.

**Related:** This is the second "Streamlit fights markdown-injected HTML" gotcha. The first was the font config issue (see 2026-04-09 entry below) where Streamlit's theme engine overrode CSS. Pattern: Streamlit has opinions about the DOM it renders, and some of those opinions conflict with raw HTML injection. When building Treatment C components, always DOM-probe after the first render (don't trust screenshots alone) to confirm the structure landed as intended.

**Files touched:**
- `ui_components.py` — `render_sku_usage_card` uses `<div class="sku-name">`
- `config.py` — `.sku-usage-card .header .sku-name` CSS rule (not `h4`)

---

## 2026-04-09 — Set fonts via Streamlit theme.fontFaces, NOT via CSS

**Decision:** All custom font registration goes in `.streamlit/config.toml` under `[theme]` + `[[theme.fontFaces]]` blocks. CSS `font-family` rules in `POPLIFE_TREATMENT_C_CSS` are only for *per-component overrides* (e.g., Inter on hero subtitles, content-card tables, North Star tagline). Never use CSS to set the global default font.

**Why:** Streamlit's theme engine applies `[theme]` settings AFTER CSS injection, so anything in the toml beats anything you put in `<style>` blocks injected via `st.markdown(..., unsafe_allow_html=True)` — even rules with `!important` and high specificity. We learned this the hard way:

1. Original `config.py` used `@import url(...)` inside the `POPLIFE_TREATMENT_C_CSS` `<style>` block to load Barlow Condensed. That worked for the explicitly-targeted Treatment C components but ALSO caused FOUT (Flash of Unstyled Text) on every page load because `@import` blocks the style block from parsing.
2. Session 3b first attempt (`fdb676a`): moved `@import` → `<link rel="stylesheet">` and added a giant selector list with `font-family: ... !important` covering every Streamlit `data-testid` (`stMetricValue`, `stMarkdownContainer`, `stDataFrame`, `stExpander`, `stButton`, `stRadio`, `stSelectbox`, sidebar, etc.). DID NOT WORK. Live DOM probe showed `body` computed font was still "Source Sans" — Streamlit's own widget CSS was loading later in the DOM and winning the cascade tie-breaker even against `!important`.
3. Session 3b second attempt (`8be51b2`): set `font = "Barlow Condensed"` in `.streamlit/config.toml` and registered 5 weights (400-800) via `[[theme.fontFaces]]` blocks. WORKED. Verified live: every native Streamlit widget (`st.metric`, `st.dataframe`, `st.markdown`, `st.button`, `st.selectbox`, sidebar nav, `st.tabs`, expanders, callouts) now renders in Barlow Condensed without any per-component CSS rule.

**Root cause**: Streamlit 1.32+ added `[[theme.fontFaces]]` as the supported way to register custom web fonts. It runs at framework startup, ahead of any markdown-injected CSS, so it sets the engine-level default that all native widgets inherit from.

**Rule going forward:**
- **DO**: register fonts in `.streamlit/config.toml` `[[theme.fontFaces]]`. Set `font = "..."` to make one of them the global default.
- **DO**: use CSS `font-family` rules ONLY for per-component overrides (e.g., the 6 places that should use Inter instead of Barlow Condensed).
- **DON'T**: try to set the global default font via CSS, even with `!important`. Streamlit will silently override you.
- **DON'T**: use `@import url(...)` inside an `st.markdown` style block — it causes FOUT and can be sanitized depending on Streamlit version.

**Streamlit Cloud rebuild gotcha (Session 3b):** The toml fix only takes effect on a fresh build. Streamlit Cloud's auto-rebuild on push has been unreliable for this repo — both `12cf2fe` and `8be51b2` required manual reboots via `Manage app → Reboot` before the new code was actually served. Always verify with a DOM probe (don't trust `view source` or page title) and reboot if needed.

**Files touched:**
- `.streamlit/config.toml` — added `font = "Barlow Condensed"` + 5 `[[theme.fontFaces]]` blocks
- `config.py` — kept the per-component CSS overrides (Inter on subtitles/tables/callouts), removed the `@import` since fontFaces handles loading

---

## 2026-04-09 — Move Partner posts to the amplified collab bucket
**Decision:** Partner posts now live in `COLLAB_AMPLIFIED_TYPES` alongside Influencer and Collective. The owned bucket contains only the hero brand's own organic posts (tagged with the hero brand's name, e.g. `Cuervo`).

**Why:** The Partner tag covers two distinct things in practice — (a) regular Cuervo posts that *mention* a partner (tag them in the caption, feature their cocktail, etc.), and (b) IG Collab Posts where Cuervo and the partner co-author a post that appears on both accounts. The second category gets amplification from the partner's audience, which was inflating the hero KPI scorecard with non-organic reach. After a meeting with the social team, we decided to treat all Partner-tagged posts as amplified rather than try to split them into sub-categories. Cleaner logic, no per-post re-tagging required.

**Scope:** One-line config change in `config.py`. No data changes — the "Partner" tag stays on the same posts in `manual_posts.csv`; only its routing through `split_owned_collab()` changed.

**Impact on Cuervo scorecard** (179-post dataset, 159 after Edutain exclusion):
- Avg Eng/Post: 172 → **116** (was 29% inflated by Partner whales like the Akamba 2026 lineup reel)
- Avg Eng/Reel: 220 → **103**
- Likes/Month: 1,222 → **802**
- Shares/Month: 302 → **101**
- Reel Views/Mo: 26,728 → **21,268**
- Comments/Month and Reel Views flipped from above-target to below-target, revealing that Partner event content was doing the work on those metrics. This is a **feature, not a bug** — the scorecard now honestly reflects organic brand content performance and surfaces actionable gaps.

**Impact on code:**
- `config.py`: `COLLAB_OWNED_TYPES = {"cuervo"}`, `COLLAB_AMPLIFIED_TYPES = {"partner", "influencer", "collective"}`
- `pages/1_Brand_Performance.py`: Scorecard caption + Collab Amplification tooltips updated
- `analysis.py`, `pages/2_Competitive_Landscape.py`, `pages/3_2026_Strategy.py`: No changes needed — they already filter via `COLLAB_AMPLIFIED_TYPES` so the config change propagates automatically
- `docs/architecture.md`, `.claude/rules/data-layer.md`: Split descriptions updated to reflect the new taxonomy

**How to add a new collab type in the future:** If the next client needs a different taxonomy (e.g., "Sponsored" / "UGC" / "Earned"), update `COLLAB_AMPLIFIED_TYPES` in `config.py`. Any value not in `COLLAB_OWNED_TYPES` (currently just `{"cuervo"}`) will be excluded from hero KPIs. For multi-tenant hero brand support, consider making these sets per-client via `ClientConfig` fields.

## 2026-04-01 — Drop content theme & tone auto-classifiers
**Decision:** Stop using `classify_theme()` and `classify_tone()` from sprout_import.py. Replace with manually tagged `content_pillar` and `content_mix` columns from tagged import sheets.

**Why:** Keyword-based classifiers are ~80-85% accurate — not good enough to base dashboard sections on.

**Scope:** Pillars and content mix funnel are hero-brand-only and client-specific (from each client's strategy config). Competitors are not manually tagged, so competitor theme analysis goes away entirely — no replacement needed since other brands' posts don't map to the hero's pillars.

**Impact on code:**
- `classify_theme()`, `classify_tone()` in sprout_import.py → dead code for new imports
- `theme_keywords`, `tone_keywords` in ClientConfig → dead config
- Page 1 already prefers `content_pillar` over `content_theme` when present
- Page 2 competitor theme analysis → will be removed
- Page 4 explorer theme/tone filters → swap for pillar/funnel (hero posts only)

## 2026-04-01 — New Sprout imports pending for both clients
*(Updated 2026-04-09: Cuervo import is now complete. Devils Reserve still pending.)*

**Status:**
- ✅ **Cuervo done** — 14-month Sprout export (Feb 1 2025 – Apr 9 2026) imported, `manual_posts.csv` enriched to 179 posts at 100% caption coverage. See `docs/changelog.md` Session 1 entry for the full enrichment methodology.
- ⏳ **Devils Reserve pending** — waiting on updated Sprout exports at a wider date range + DR tag CSV with pillar/funnel/collaboration tags from the social team. `themes_ready` still `False` in `clients/devils_reserve/client.py`.

**When DR materials land:**
1. Drop new Sprout CSVs into `data/devils_reserve/sprout/` (delete the current files first for a clean swap)
2. Run the same enrichment pipeline we used for Cuervo (see Session 1 changelog for the script pattern)
3. Fill any captions Sprout didn't capture (use the `cuervo_captions_to_fill.csv` workflow)
4. Set `themes_ready=True` in Devils Reserve's `client.py`
5. Verify pillar/funnel sections render correctly on Pages 1-3 for DR
