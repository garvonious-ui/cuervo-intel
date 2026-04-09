# Changelog

## 2026-04-09 — Session 3 (UI Phase 1 finish: Treatment C consistency pass across all 5 pages) — COMMIT READY, NOT PUSHED

### What shipped
Finished the Treatment C rollout by sweeping the remaining old-blue `autostrat_components` calls out of every page. After Session 2, hero blocks and most top-level section labels were already Treatment C — but `render_section_label`, `render_nopd_cards`, `render_territory_cards`, and `render_verbatim_quotes` from `autostrat_components.py` were still being called in all 5 pages (Page 1 Tab 3 Self-Audit, Page 3 Tab 4 Action Plan, Page 4 Tab 1 Inspiration, Page 5 all 3 tabs). That inconsistency is now gone.

**`ui_components.py` additions**
- `render_verbatim_card(quote)` — new italic pull-quote with peach left border
- `render_nopd_grid(audience_profile, hero_label="")` — new convenience wrapper that calls `render_nopd_card` 4 times (needs/desires/objections/pain). Signature matches the old `autostrat_components.render_nopd_cards(ap)` so it's a drop-in rename
- `render_territory_list(items)` — new auto-numbering wrapper over `render_territory_card` for flat lists of strings (matches the autostrat data shape)
- `render_territory_card` signature extended: `title: Optional[str] = None`. When omitted, the `<div class="t-title">` is not emitted at all (no empty div eating vertical space)
- `render_pillar_card` signature extended: `accent_color: Optional[str] = None`. Emits an inline `style="--accent-color: {color}"` CSS variable so each pillar card can keep its per-pillar border color from `cfg.pillar_colors`

**`config.py` CSS additions**
- `.verbatim-card` — italic pull-quote styling (warm `#F3EDE6` bg, 4px peach left border, Barlow Condensed)
- `.pillar-card-detail` — changed `border-left: 5px solid #F8C090` → `border-left: 5px solid var(--accent-color, #F8C090)` so the new `accent_color` parameter cascades through. Also added `margin-bottom: 14px` for breathing room between pillar cards

**Page-level changes**

`pages/1_Brand_Performance.py` — Tab 3 Self-Audit Intelligence:
- 7 `render_section_label` → `render_kpi_section_label`
- `render_nopd_cards(ap)` → `render_nopd_grid(ap)`
- 2× `render_territory_cards(...)` → `render_territory_list(...)` (Self-Audit + News Action Items)
- `render_verbatim_quotes(verbatims, max_quotes=8)` → loop over `verbatims[:8]` calling `render_verbatim_card`
- Import cleanup: dropped `render_section_label, render_territory_cards, render_nopd_cards, render_verbatim_quotes` from `autostrat_components`; added `render_nopd_grid, render_territory_list, render_verbatim_card` to `ui_components`

`pages/3_2026_Strategy.py` — Tab 2 Frameworks + Tab 4 Action Plan:
- **Pillar cards** (lines ~288-299): replaced the inline custom HTML loop with `render_pillar_card(..., accent_color=cfg.pillar_colors[row["Pillar"]])`. Cleaner code, same per-pillar visual identity
- **Collaboration Mix**: wrapped the 2-column Plotly bar + scorecard in `render_content_card_open("Cuervo collaboration breakdown", caption=...) / render_content_card_close()`. Scorecard bullets in the right column converted to a stack of `render_kpi_card(label=..., value=..., meta=...)` so the KPI card component gets reuse outside Page 1
- **Content Mix Funnel**: wrapped the 2-column chart + scorecard in a content card (user's choice — "wrap the chart in a content card"). Plotly figure itself unchanged. The `render_connect_callout` lives below the content card
- **Tab 4 Action Plan**: 4 `render_section_label` → `render_kpi_section_label`, `render_nopd_cards(merged_nopd)` → `render_nopd_grid(merged_nopd)`, `render_territory_cards(all_territories[:8])` → `render_territory_list(all_territories[:8])`
- Import cleanup: dropped `render_section_label, render_territory_cards, render_nopd_cards, render_verbatim_quotes` from `autostrat_components`; added `render_pillar_card, render_content_card_open, render_content_card_close, render_kpi_card, render_nopd_grid, render_territory_list` to `ui_components`

`pages/4_Inspiration_&_Explorer.py` — Tab 1 Inspiration:
- 6 `render_section_label` → `render_kpi_section_label`
- **Audience comparison (hero vs reference)**: the old side-by-side comparison iterated 4 times through `NOPD_STYLES` with per-dimension headers and manual bullet rendering (~25 lines of custom inline HTML). Replaced with a clean 2-column layout calling `render_nopd_grid(cuervo_ap)` on the left and `render_nopd_grid(ap_ref)` on the right. Loses per-dimension sub-headers but gains Treatment C consistency and drops ~25 lines of inline HTML
- Fallback single-brand NOPD: `render_nopd_cards(ap_ref)` → `render_nopd_grid(ap_ref)`
- `render_territory_cards(hw["territories"])` → `render_territory_list(hw["territories"])`
- `render_verbatim_quotes(hw["audience_verbatims"])` → loop over `[:8]` calling `render_verbatim_card` (inside the existing expander wrapper)
- Import cleanup: dropped `render_section_label, render_territory_cards, render_nopd_cards, render_verbatim_quotes` from `autostrat_components` AND removed the inline `from autostrat_components import NOPD_STYLES` that was sitting mid-function; added `render_nopd_grid, render_territory_list, render_verbatim_card` to `ui_components`

`pages/5_Conversation_Intel.py` — all 3 tabs interior swap, no structural changes:
- 20 `render_section_label` → `render_kpi_section_label` (via replace_all)
- 4 `render_nopd_cards(ap)` → `render_nopd_grid(ap)` across Tabs 1-3
- 3 `render_territory_cards(...)` → `render_territory_list(...)` across Tabs 1-3
- Import cleanup: dropped `render_nopd_cards, render_territory_cards, render_section_label` from `autostrat_components`; added `render_kpi_section_label, render_nopd_grid, render_territory_list` to `ui_components`
- **The expander-wall structure stays intact** — Tier C structural redesign (brand card grid + drill-in panel) remains deferred to Phase 2

`pages/2_Competitive_Landscape.py` — unchanged, had no old-blue calls remaining from Session 2.

### Verified (final smoke test)
Dev server started via `preview_start`. Navigated via sidebar nav links (which preserve session state across Streamlit pages — direct URL navigation resets the session and shows the "Go to the home page first" warning, so must click the nav).

Cuervo sweep:
- Page 1 Brand Performance: 13 KPI cards, 26 peach section labels, 20 NOPD cards, 33 territory cards, 16 verbatim cards — 0 exceptions
- Page 2 Competitive Landscape: hero "THE WINDOW", 8 section labels — 0 exceptions
- Page 3 Strategy: hero "THE PLAYBOOK", Frameworks tab shows 4 pillar cards with **distinct per-pillar border colors** (peach/blue/red/tan — confirming the `--accent-color` CSS variable cascades correctly), 4 content cards, Action Plan tab has NOPD grid + 8 territory cards — 0 exceptions
- Page 4 Inspiration: hero "THE TOOLBOX", side-by-side NOPD comparison renders as 2× `render_nopd_grid` (8 total cards), 5 territory cards, 8 verbatim cards — 0 exceptions
- Page 5 Conversation Intel: hero "THE LANDSCAPE", all 3 tabs clean, 20 section labels per tab — 0 exceptions

Devils Reserve sweep:
- Page 1: 13 KPI cards, 12 section labels, 8 NOPD cards, 10 territories, 8 verbatims — 0 exceptions
- Page 2: "THE WINDOW", 8 section labels — 0 exceptions
- Page 3: "THE PLAYBOOK", Frameworks shows 4 DR pillar cards with per-pillar colors ("The Sweet Heat" peach, "The Devil's Advocate" yellow, etc.), 2 content cards (DR has `themes_ready=False` so collab mix is hidden) — 0 exceptions
- Page 4: "THE TOOLBOX", 8 NOPD cards, 5 territories, 8 verbatims — 0 exceptions
- Page 5: "THE LANDSCAPE", 6 section labels, 24 NOPD cards, 30 territories — 0 exceptions

10 page loads total across both clients, **zero Streamlit exceptions, zero server errors** in `preview_logs`. Visual proof: screenshots captured of both Cuervo and DR Page 3 Frameworks tab pillar cards showing per-pillar colored borders.

### Deprecated but kept
The old autostrat helpers (`render_section_label`, `render_nopd_cards`, `render_territory_cards`, `render_territory_card`, `render_verbatim_quotes`, `NOPD_STYLES`) are no longer imported by any page, but the functions are **not deleted** this session. Keeping them reduces rollback risk and lets `autostrat_parser.py` or any other non-page caller keep working. Phase 2 can prune them after the polish has bedded in.

### Still deferred (Phase 2)
- **Page 5 expander-wall structural redesign** (Tier C) — the "kinda lame" flat list of 8-16 expanders on Tab 1 (Brand Hashtags) where brand X's insights, NOPD, opportunities, and territories get scattered into separate expanders instead of being grouped per-brand. The structure is unchanged, only the interiors are Treatment C. Real redesign (brand card grid + drill-in panel) is its own session
- `autostrat_components.render_narrative_card` — still used at `pages/1_Brand_Performance.py:814` and `pages/5_Conversation_Intel.py:854`. Blue-header white card looks mildly inconsistent with Treatment C but not egregious
- `autostrat_components.render_brand_mention` — still used at page 5:456. Signature differs from `ui_components.render_brand_mention` (dict-based vs individual args), so swap is non-mechanical
- `autostrat_components.render_creator_archetype` + `render_sponsorship_card` — rich data structures, would need new Treatment C helpers
- Page 3 pillar distribution Plotly charts (lines ~311-335) — already use `CHART_TEMPLATE` so they're Poplife-branded, just not wrapped in content cards
- DR Sprout data refresh (waiting on DR tag CSV from social team), DR logo assets (waiting on design team), TikTok empty-state handling (Phase 2)

### Files changed this session (all staged but NOT committed yet)
```
 M clients/cuervo/client.py          ← Session 2 carryover, unchanged in Session 3
 M clients/devils_reserve/client.py  ← Session 2 carryover, unchanged in Session 3
 M config.py                         ← +.verbatim-card rule, .pillar-card-detail CSS var
 M docs/changelog.md                 ← this entry + Session 2 entry below
 M pages/1_Brand_Performance.py      ← Tab 3 Self-Audit swap (7 labels + NOPD + territories + verbatims)
 M pages/2_Competitive_Landscape.py  ← Session 2 carryover, unchanged in Session 3
 M pages/3_2026_Strategy.py          ← pillar cards + collab mix wrap + funnel wrap + Tab 4 swap
 M pages/4_Inspiration_&_Explorer.py ← Tab 1 swap + custom NOPD comparison restyle
 M pages/5_Conversation_Intel.py     ← 20 labels + 4 NOPD + 3 territories swap across 3 tabs
 M ui_components.py                  ← 3 new helpers + 2 signature extensions (was untracked in Session 2)
?? data/cuervo/brand_profiles.csv           ← pre-existing, not touched
?? data/cuervo/creator_collabs.csv          ← pre-existing, not touched
?? data/cuervo/hashtag_tracking.csv         ← pre-existing, not touched
?? data/devils_reserve/brand_profiles.csv   ← pre-existing, not touched
?? data/devils_reserve/creator_collabs.csv  ← pre-existing, not touched
?? data/devils_reserve/hashtag_tracking.csv ← pre-existing, not touched
?? data/devils_reserve/posts_data.csv       ← pre-existing, not touched
```

### How to pick back up
Commit has been created locally but NOT pushed to `origin/main`. User to decide:
1. `git push origin main` to ship it — Streamlit Cloud will rebuild within ~60s
2. `git commit --amend` + re-stage to tweak the commit
3. `git reset HEAD~1 --mixed` to unwind and keep the working tree for further edits

---

## 2026-04-09 — Session 2 (UI Phase 1: Treatment C rollout to pages 2–5) — IN PROGRESS, NOT COMMITTED

### Status at pause
All code changes are complete and verified on both Cuervo and DR. **Nothing has been committed yet** — working directory has 8 modified files + 1 new file (`ui_components.py`). Pick up by running the dev server, eyeballing a few pages in the browser, and then deciding on a commit.

### What shipped
- **Shared CSS constant** in `config.py` — new `POPLIFE_TREATMENT_C_CSS` with ~30 Treatment C component classes (page-hero, section-label, content-card, pillar/sku/engine/voice cards, swot/nopd/territory/brand-mention cards, sentiment grid, wtm cards, news narrative, cpn layout, etc.). Both client files now concatenate this with their client-specific overrides instead of duplicating the CSS.
- **`ui_components.py`** expanded from 4 → 23 helper functions covering every Tier 3 component. All return single-line HTML strings to avoid Streamlit's markdown-code-block gotcha (4+ leading spaces get interpreted as code blocks and break nested divs).
- **Page 2 — Competitive Landscape** — dark hero "THE WINDOW", 8 peach section labels, 4 poplife notes replacing `st.info`. Native dataframes and Plotly charts preserved.
- **Page 3 — 2026 Strategy** — dark hero "THE PLAYBOOK", North Star dark callout, 18 section labels, full **Content Production Needs layout** (table + dark monthly summary + cadence sidebar + source mix bar), Platform Roles table in a content card (all 6 platforms), 3 IG format mix cards, SKU cards, execution engine cards, voice cards, 4 quarter cards (cultural calendar), 3 partner event cards (NASCAR/UFC/Love Island), SWOT 2-col for Threats & Opportunities, Connect callout, content-mix funnel status notes. Math preserved throughout.
- **Page 4 — Inspiration & Explorer** — dark hero "THE TOOLBOX", section label, poplife notes.
- **Page 5 — Conversation Intel** — dark hero "THE LANDSCAPE", poplife notes replacing `st.info`. Existing autostrat rendering (expanders, NOPD, territory cards) preserved — deeper redesign of the expander-wall is Phase 2.

### Verified
Final smoke test on all 5 pages × both clients (10 total page loads): every hero rendered correctly, 0 exceptions, 0 server errors. CPN layout renders its full 3-part structure (table + dark summary + cadence sidebar).

### Gotcha caught and fixed
Streamlit's markdown parser treats 4+ leading spaces in `st.markdown(..., unsafe_allow_html=True)` as a code block, which was silently dropping the right column of the nested CPN layout. Fixed by building complex nested HTML as single-line f-strings (see the `_cpn_html` and `_plat_html` constructions in Page 3).

### Deferred to future sessions (not in scope for this rollout)
- **Page 3 pillar cards, Content Mix funnel chart, Gen Z Leaders, Collaboration Mix charts** — still use existing custom HTML / Plotly rendering. They work and look decent but aren't Treatment-C-pure cards. Optional polish for a later session.
- **Page 4 NOPD audience comparison / territory cards / verbatims** inside Tab 1 — still use autostrat components with the old blue section-label style. Works correctly.
- **Page 5 expander-wall redesign** (the "kinda lame" structural problem) — still existing autostrat rendering inside each expander. Real redesign (probably a brand card grid + drill-in panel) is Phase 2.

### Files changed (all uncommitted)
```
 M clients/cuervo/client.py        — uses shared CSS + Cuervo overrides only
 M clients/devils_reserve/client.py — uses shared CSS + DR overrides only
 M config.py                        — +POPLIFE_TREATMENT_C_CSS constant
 M pages/1_Brand_Performance.py     — no changes from Session 1 end state
 M pages/2_Competitive_Landscape.py — hero + 8 section labels + poplife notes
 M pages/3_2026_Strategy.py         — hero + 18 section labels + all the Tier 3 cards
 M pages/4_Inspiration_&_Explorer.py — hero + section label + poplife notes
 M pages/5_Conversation_Intel.py    — hero + poplife notes
?? ui_components.py                 — 23 helper functions (was 4)
```
(7 untracked data CSVs are pre-existing, not touched this session.)

### How to pick back up
1. `python3 -m streamlit run app.py --server.headless true`
2. Open `?client=cuervo` and eyeball all 5 pages — key thing to verify is Page 3 Platform Strategies tab (Content Production Needs layout is the most complex piece)
3. Same on `?client=devils_reserve`
4. If happy, commit with a single message like `Implement Treatment C rollout to pages 2-5 (UI Phase 1)` and push to `origin/main`
5. Streamlit Cloud will rebuild within ~60s

### Reference
- Full-density mockup lives at `~/Downloads/pages_2to5_full_mockup.html` — the pixel target we built against. Open in a browser side-by-side with the live app to spot any differences.
- Earlier KPI prototype: `~/Downloads/kpi_prototype_C_mixed.html` (Page 1 target, already shipped last session).

---

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

### Docs updates (post-meeting)
- `docs/decisions.md`: Recorded the Partner-to-amplified decision with full rationale, scorecard impact, and guidance for future clients. Updated the April 1 "imports pending" entry to mark Cuervo complete.
- `docs/schemas.md`: Added Manual Posts Schema section documenting `manual_posts.csv` columns and the `collaboration` column taxonomy (Cuervo / Partner / Influencer / Collective) with owned-vs-amplified routing.
- `docs/onboarding-client.md`: Added collab taxonomy gotcha for new client setups.

### UI Phase 1 work (afternoon)
- Fetched `poplife99.com` for brand DNA grounding. Key findings: dark-first editorial aesthetic, Cubano headline font, peach (#F8C090) + teal/cyan (#7EBEC5) accents on dark, bold uppercase typography, hover micro-interactions. "Music festival meets creative agency" — not corporate, not minimal.
- Produced comprehensive UI/UX audit covering typography, KPI scorecard, charts, cards, page heroes, sidebar, and UX/IA findings. Full audit doc NOT committed (lives in conversation history) — the actionable outputs are below.
- **Shipped**: Branded Poplife Plotly chart template (`c8f08f1`). Registered `pio.templates["poplife"]` with peach-teal-blue-sage colorway, warm gridlines, Barlow Condensed everywhere, dark hover tooltips with peach border. All 26 existing usage sites in pages/ continue to work without changes. Charts with explicit `color_discrete_sequence` / `color_discrete_map` (like Page 2 competitive charts) keep their explicit colors — the template only fills in defaults. Added supporting constants `POPLIFE_TEAL`, `POPLIFE_BORDER`, `POPLIFE_GRID`, `POPLIFE_MUTED` to `config.py` for future component CSS work. Smoke-tested: 21 Plotly charts across pages 1-3 render with peach as primary, zero server errors.
- Built three KPI card HTML prototypes for visual direction decision:
  - `~/Downloads/kpi_prototype_A_editorial_light.html` (all light)
  - `~/Downloads/kpi_prototype_B_editorial_dark.html` (all dark)
  - `~/Downloads/kpi_prototype_C_mixed.html` (dark hero + light cards — picked)
- **Direction locked**: Treatment C (mixed dark hero + light cards). Implementation deferred to a fresh session because it's a ~4-hour focused block of work on the Page 1 scorecard. Full implementation handoff doc at `docs/ui-phase-1-handoff.md` — next session can pick up cleanly from there.

### Commits (chronological)
- `eb498bb` chore: sync build-plan checkboxes, add decisions.md, annotate deferred work (pre-session cleanup)
- `e7ae642` chore: remove completed REFACTOR_PLAN.md (pre-session cleanup)
- `71df6fd` chore: gitignore .claude/projects/ (pre-session cleanup)
- `66aa849` Refresh Devils Reserve autostrat reports from source PDFs
- `a618bb4` Refresh Cuervo Sprout exports + enrich manual_posts.csv to 179 posts
- `892c8e0` Add Session 1 changelog entry (initial entry, later extended)
- `764e1ed` Hide dev sidebar controls in client-facing views
- `caca90f` Move Partner posts from owned to amplified collaboration bucket
- `dcf77c6` Extend Session 1 changelog with sidebar cleanup + Partner split
- `5d4f0db` Document Partner-to-amplified decision + collab taxonomy
- `c8f08f1` Add branded Poplife Plotly chart template
- `<this commit>` Session 1 wrap: extend changelog + UI Phase 1 handoff doc

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
