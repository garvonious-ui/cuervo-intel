# Decisions

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
New Sprout Social CSV exports and manually tagged content sheets are incoming for both Cuervo and Devils Reserve. Manual tagging is still in progress.

**When tagging is done:**
1. Drop new Sprout CSVs into `data/cuervo/sprout/` and `data/devils_reserve/sprout/`
2. Import the manually tagged sheets
3. Set `themes_ready=True` in Devils Reserve's `client.py`
4. Verify pillar/funnel sections render correctly on Pages 1-3 for both clients
