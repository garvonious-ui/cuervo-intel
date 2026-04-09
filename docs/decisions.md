# Decisions

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
