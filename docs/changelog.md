# Changelog

## 2026-04-09 — Session 1 (DR autostrat refresh + Cuervo Sprout import)

### Devils Reserve autostrat refresh
- Re-parsed all 6 DR autostrat PDFs (1 hashtag + 5 keyword reports) via `parse_all_pdfs()`. All 14 DR reports now load cleanly via `autostrat_loader`; Page 5 Conversation Intel renders all 5 competitor keyword reports and the hero hashtag report for DR.
- Removed the stale TODO above `HERO_HASHTAG_IDS` in `clients/devils_reserve/brands.py` — the existing `{"devils_reserve", "devilsreserve"}` set already matches parsed filenames.
- Build-plan DR checkboxes updated: PDF parse, hashtag report import, and `hero_hashtag_ids` population all marked done.

### Cuervo Sprout data refresh
- Swapped Cuervo's 6 Sprout exports from `Oct 1 2025 – Mar 16 2026` → `Feb 1 2025 – Apr 9 2026` (14 months). New import: 2440 total rows across all 13 brands; hero = 1593 rows (1414 stories + 179 feed posts).
- Enriched `data/cuervo/sprout/manual_posts.csv` from 77 rows → 179 rows with **100% caption coverage** via a one-shot merge script:
  - Tag CSV (`Cuervo Pillars - cuervo_posts_with_manual_tags.csv`) was the source of truth for `content_pillar`, `content_mix_funnel`, `collaboration`, `sku`, `content_theme`.
  - 145 rows enriched with Sprout-derived columns (caption, hashtags, impressions, post_time, etc.) from the fresh Sprout import.
  - 19 rows fell back to the previous `manual_posts.csv` for Sprout columns.
  - 34 posts that Sprout had never captured (standalone Instagram posts its publishing integration missed) had captions manually provided by the user and merged by post slug.
  - `caption_word_count` recomputed for all enriched rows.
- Final distributions on the 179-row dataset:
  - **Pillars**: The Front Row 58, The Pulse 48, The Craft 37, The Ritual 36
  - **Funnel**: Entertain 131, Edutain 20, Educate 19, Convince 9 (Edutain rows are split 0.5/0.5 to Educate/Entertain in `app.py:209-225` for aggregation)
  - **Collaboration**: Cuervo 118, Collective 24, Influencer 20, Partner 17
- Smoke-tested all 5 pages for both Cuervo and Devils Reserve. Zero server errors. All 13 brands visible on Page 2, pillars render on Page 1 Content Performance, Page 3 funnel chart correctly shows only Educate/Entertain/Convince (Edutain is invisible, confirming the split works).

### Not touched / still pending
- 7 untracked CSVs at `data/{client_id}/{brand_profiles,creator_collabs,hashtag_tracking,posts_data}.csv` — user asked to hold off, provenance not yet confirmed. Left as-is.
- Devils Reserve Sprout import + manual tagging — waiting on DR tag CSV from user.
- DR custom logo assets — waiting on design team.
- TikTok empty-state handling — still open, deferred from this session.

### Sidebar cleanup (client-facing views)
- Hidden dev-only sidebar controls (data source radio, import status messages, filter widgets, autostrat Import PDFs button) whenever a `?client=X` URL parameter is present. Clients viewing the dashboard now see only page navigation in the sidebar — no dev clutter.
- Internal Poplife view (bare URL → client picker) keeps everything visible.
- `?client=X&dev=1` escape hatch restores all dev controls on a specific client dashboard without switching to the internal view.
- Filter session state (`sel_brands`, `sel_platforms`, `sel_types`) is still populated with all-selected defaults when the filter UI is hidden so Pages 2 (Competitive Landscape) and 4 (Inspiration & Explorer) keep working correctly.

### Partner posts → amplified collab bucket
- After a meeting with the social team, decided to move Partner posts from the owned bucket to the amplified bucket (alongside Influencer + Collective). Rationale: Partner posts include IG Collab Posts and sponsored event activations that get amplification from the partner's audience, which was inflating the hero KPI scorecard with non-organic reach.
- `config.py`: `COLLAB_OWNED_TYPES = {"cuervo"}`, `COLLAB_AMPLIFIED_TYPES = {"partner", "influencer", "collective"}`. Docstring updated.
- `pages/1_Brand_Performance.py`: scorecard caption and Collab Amplification tooltips updated to reflect new split.
- `docs/architecture.md` + `.claude/rules/data-layer.md`: split descriptions updated.
- No data changes — the "Partner" tag stays on the same posts in `manual_posts.csv`; only its routing through `split_owned_collab()` changed.
- Cuervo scorecard impact on the 159-post Page-1 view (Edutain-excluded):
  - Avg Eng/Post:    172 → **116**  (was 29% inflated)
  - Avg Eng/Reel:    220 → **103**
  - Likes/Month:    1,222 → **802**
  - Shares/Month:    302 → **101**
  - Reel Views/Mo: 26,728 → **21,268**
- Honest Cuervo-organic baseline now beats 9 of 12 scorecard targets; Comments/Month (-9) and Reel Views/Mo (-3,732) flip to under-target, revealing that Partner activations were doing the work on those metrics.

### Deploy
- All session work pushed to `origin/main` as of commit `caca90f`. Streamlit Community Cloud rebuilt within ~60 seconds of each push.

### Commits (chronological)
- `eb498bb` chore: sync build-plan checkboxes, add decisions.md, annotate deferred work (pre-session cleanup)
- `e7ae642` chore: remove completed REFACTOR_PLAN.md (pre-session cleanup)
- `71df6fd` chore: gitignore .claude/projects/ (pre-session cleanup)
- `66aa849` Refresh Devils Reserve autostrat reports from source PDFs
- `a618bb4` Refresh Cuervo Sprout exports + enrich manual_posts.csv to 179 posts
- `892c8e0` Add Session 1 changelog entry
- `764e1ed` Hide dev sidebar controls in client-facing views
- `caca90f` Move Partner posts from owned to amplified collaboration bucket

## 2026-04-01 — Session 0 (Baseline)
- Project restructured to follow Claude Code Project Structure Guide
- Created docs/ directory with architecture.md, schemas.md, build-plan.md, changelog.md, design-system.md, page-specs.md, onboarding-client.md
- Rewrote CLAUDE.md from 180 lines → ~88 lines (lean index pointing to docs/)
- Added .claude/commands/ (start, checkpoint, wrap, status)
- Added .claude/rules/ (pages.md, clients.md, data-layer.md)
- Absorbed HANDOFF.md content into docs/ files and removed it
- Cleaned up fully-merged Claude Code branches (cool-dubinsky, elegant-hypatia, jolly-poitras)
- Deleted claude/reverent-borg (1 unmerged Strategy page commit — stale, conflicts with main, discarded)

### Historical Summary (pre-structure, 293 commits)
- Initial build: single-client Cuervo competitive dashboard
- Refactored to multi-tenant architecture (March 2026)
- Added Devils Reserve as second client
- 5 dashboard pages: Brand Performance, Competitive Landscape, Strategy, Inspiration & Explorer, Conversation Intel
- Autostrat PDF/PPTX parser and qualitative intelligence system
- Sprout Social CSV import with AI content classifiers
- Excel report export
- Deployed on Streamlit Community Cloud
