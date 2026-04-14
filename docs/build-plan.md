# Build Plan

## Phase 1 — Stabilization & Cleanup (Current)

### Data Imports
- [x] Import updated Sprout CSVs + manually tagged content sheets for Cuervo (extended date range) — swapped to Feb 1 2025 – Apr 9 2026 window (14 months), enriched `manual_posts.csv` to 179 hero posts with 100% caption coverage (2026-04-09)
- [x] Import updated Sprout CSVs + manually tagged content sheets for Devils Reserve (extended date range) — 133 IG posts with 100% caption + pillar coverage, TikTok posts removed from manual sheet (2026-04-10)

### Devils Reserve Completion
- [x] Parse Devils Reserve autostrat PDFs — 6 PDFs parsed into 1 IG hashtag + 5 IG keyword reports (2026-04-09)
- [x] Import Devils Reserve's own autostrat hashtag report — `instagram_hashtags/devilsreserve.json` + `instagram_keywords/devils_reserve.json` both parsing and rendering on Page 5
- [x] Populate `hero_hashtag_ids` in DR config — already set to `{"devils_reserve", "devilsreserve"}`; verified against parsed filenames (2026-04-09)
- [ ] Create custom Devils Reserve logo assets (logo.png, favicon.png, app_logo.png)
- [x] Complete manual content pillar tagging for DR posts, set `themes_ready=True` — 133/133 IG posts tagged, `content_mix_funnel` still pending (2026-04-10)
- [ ] Complete `content_mix_funnel` tagging for DR posts (Entertain/Educate/Convince) — chart hidden until tagged

### Known Issues
- [ ] TikTok sections show zeros when no TikTok post data in Sprout exports — add graceful empty state
- [x] Content theme classifier is keyword-based (~80-85% accuracy) — **decision: dropping auto-classifiers, using manual content_pillar + content_mix tagging instead (hero brand only)**
- [x] Review unmerged branch `claude/reverent-borg` (Strategy page restructure) — discarded (stale, conflicts with main)

### Code Quality
- [x] Add TODO/FIXME comments where known issues exist in code
- [x] Verify Python 3.9 compatibility across all files

## Phase 2 — Feature Enhancements

### Data & Analysis
- [x] ~~Improve content theme classifier accuracy~~ — replaced by manual pillar/funnel tagging
- [ ] Add TikTok-specific metrics and analysis sections
- [ ] Benchmark CSV auto-import improvements

### Dashboard UX
- [ ] Loading states for slow data operations
- [ ] Better empty-state handling across all pages
- [ ] Mobile responsiveness improvements

### New Clients
- [ ] Template/checklist for rapid client onboarding (streamline from docs/onboarding-client.md)
- [ ] Automated Sprout CSV schema validation on import

## Pending Data / Blockers
- Devils Reserve needs custom logo assets from design team
- Devils Reserve `content_mix_funnel` tagging needed before funnel chart shows (pillar tagging done)
- TikTok data coverage depends on Sprout Social export availability per client
- Streamlit Cloud preview app serves code from `main` despite branch setting — merge to main needed for code changes to deploy (data file changes deploy fine from preview branch)
