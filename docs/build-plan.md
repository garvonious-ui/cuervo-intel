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

### Ad-Hoc Requests
- [x] Merge `preview/ui-phase-1` → `main` — 21 commits of UI Phase 1 + DR scorecard fixes now live on production (2026-04-14)
- [x] Add SKU Usage by Occasion matrix to Page 3 Tab 2 (Cuervo only) — 17 occasions × 3 variants from "Role of Variants" Mar 2026 deck, rendered as Treatment C cards with per-variant color story (2026-04-14)

### Known Issues
- [ ] TikTok sections show zeros when no TikTok post data in Sprout exports — add graceful empty state
- [x] Content theme classifier is keyword-based (~80-85% accuracy) — **decision: dropping auto-classifiers, using manual content_pillar + content_mix tagging instead (hero brand only)**
- [x] Review unmerged branch `claude/reverent-borg` (Strategy page restructure) — discarded (stale, conflicts with main)

### Code Quality
- [x] Add TODO/FIXME comments where known issues exist in code
- [x] Verify Python 3.9 compatibility across all files

## Phase 2 — Feature Enhancements

### Sprout API + Tagging Queue (NEW — feature branch)
Full design: `~/.claude/plans/what-i-would-like-rustling-spindle.md`. Branch: `feature/sprout-api-integration`. Ship in three phases:
- [ ] **Phase A** — Tagging Queue page (`pages/6_Tagging_Queue.py`). Tab 1: queue of untagged hero posts. Tab 2: manual entry for off-Sprout Partner/Influencer/Collective posts. File-lock writes to `manual_posts.csv`. Shippable standalone — no API creds needed.
- [ ] **Phase B** — Sprout REST client (`sprout_api.py`). OAuth2 Bearer from `st.secrets`. Manual "Sync now" button. Writes `data/{client}/sprout/api_posts.parquet`.
- [ ] **Phase C** — Scheduled daily sync via GitHub Actions (`sprout_sync.py` + `.github/workflows/sprout-sync.yml`).

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

## Known Gotchas (not blocking)
- Streamlit Cloud preview app serves code from `main` despite branch setting being `preview/ui-phase-1` — workaround: merge to `main` to ship Python code changes. Data file changes deploy fine from the preview branch. Root cause unknown; may need to delete and recreate the Streamlit Cloud app to fix for real.
- Streamlit hoists `<h1>`–`<h6>` out of their parent container inside `st.markdown(unsafe_allow_html=True)` blocks (for anchor linking) — breaks flex/grid layouts. Use `<div>` with explicit styling classes instead. See `docs/decisions.md`.
