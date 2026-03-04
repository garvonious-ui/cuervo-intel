# Cuervo Social Intelligence Dashboard

## What This Is
A competitive social media intelligence tool for **Jose Cuervo** tequila, built for **Poplife** agency. Strategy-first Streamlit dashboard analyzing Instagram and TikTok performance across 13 tequila brands, with qualitative intelligence from autostrat.ai reports and a dedicated 2026 Social Brief playbook.

## Brands Tracked (13)
Jose Cuervo, Patron, Don Julio, Casamigos, Espolon, Teremana, 1800 Tequila, 818 Tequila, Lunazul, Hornitos, Cazadores, Milagro, El Jimador

## Reference Brands (non-tequila, inspiration only)
Duolingo, Poppi, Chipotle, Dunkin' — studied for Gen Z content strategy, not tequila competitors

## Architecture (5 pages)
```
app.py                 # Entry point — data loading, sidebar filters, session state, home page
pages/
  1_Cuervo_Performance.py      # "The Mirror" — KPI scorecard, content performance, self-audit
  2_Competitive_Landscape.py   # "The Window" — 13-brand comparison, content gaps, competitor intel
  3_2026_Strategy.py           # "The Playbook" — Social Brief scorecard, Poplife frameworks, action plan
  4_Inspiration_&_Explorer.py  # "The Toolbox" — Reference brands + full data explorer
  5_Conversation_Intel.py      # "The Landscape" — Brand hashtag comparison, category intel, Google News
autostrat_parser.py    # PDF/PPTX-to-JSON parser for autostrat.ai report exports
autostrat_loader.py    # JSON loader + cross-report extraction helpers
autostrat_components.py # Reusable UI components for narrative content
config.py              # Brand colors, BRAND_ORDER, Poplife frameworks, CUSTOM_CSS (Poplife palette)
templates.py           # BRANDS list, content themes, visual styles, tone options
analysis.py            # Core analysis engine — run_full_analysis(data_dir)
sample_data.py         # Demo data generator with realistic brand profiles
sprout_import.py       # Sprout Social CSV import adapter + AI content classifiers
dashboard.py           # Excel report generator (download button)
data/sprout/           # Drop Sprout Social CSV exports here
data/autostrat/        # Parsed autostrat JSON reports (8 subdirectories: 7 report types + pdfs/)
data/autostrat/pdfs/   # Drop autostrat PDF/PPTX exports here for import
```

## Page Structure

### Page 1: Cuervo Performance ("The Mirror")
Uses UNFILTERED data — sidebar filters do NOT apply. Cuervo-only view.
- **Tab 1: KPI Dashboard** — Social Brief KPI scorecard (Avg Eng/Post vs 200, Reel ratio vs 50%, Reel views vs 10K, posts/week vs targets), "So What" narrative, platform cadence scorecard, engagement signals (save/share/comment rates)
- **Tab 2: Content Performance** — Format breakdown (pie + engagements by format), theme performance chart, best & worst 5 posts with caption previews
- **Tab 3: Self-Audit Intelligence** — All Cuervo-related autostrat reports across platforms (dynamically loaded via `CUERVO_HASHTAG_IDS` + `CATEGORY_HASHTAGS`). Each report in a collapsible accordion. Hashtag reports: key insights, NOPD, How to Win, strategic actions, verbatims. Google News accordion: overview, sentiment breakdown, SWOT analysis, action items. Platform badges (IG/TT) on each expander.

### Page 2: Competitive Landscape ("The Window")
Uses FILTERED data — sidebar brand/platform/type filters apply.
- **Tab 1: Competitive Overview** — Side-by-side comparison table, "Who's Winning & Why" narrative, Eng/1K Followers bar chart with 1.5 target line
- **Tab 2: Content Gaps** — Cuervo vs category theme gap analysis, format strategy stacked bar, posting frequency comparison, "What to Steal" cards for brands beating Cuervo
- *(Purely quantitative — all qualitative competitor intel moved to Page 5)*

### Page 3: 2026 Strategy & Brief ("The Playbook")
Uses UNFILTERED data — sidebar filters do NOT apply. Dedicated to the Social Brief.
- **Tab 1: Social Brief Scorecard** — Expanded KPI table with status indicators, dynamic vs static ER comparison, content source mix (Creator 70% / Brand 15% / Events 15%)
- **Tab 2: Content Strategy Frameworks** — Poplife content pillars (La Tradición / Cuervo Live / Life with a Lime / Culture Shaken), content mix funnel (Entertain 50% / Educate 30% / Connect 10% / Convince 10%), Gen Z engagement drivers
- **Tab 3: Action Plan** — 30-day weekly plan, threats & opportunities, all recommendations, qualitative intelligence (winning territories, content trends, creator archetypes, partnership opportunities)

### Page 4: Inspiration & Explorer ("The Toolbox")
- **Tab 1: Inspiration** — Duolingo/Poppi/Chipotle/Dunkin' reference brand profiles, "What Cuervo Can Steal" section, side-by-side audience comparison (NOPD), How to Win territories, Sponsorship Intelligence, Performance Statistics (min/max/median/avg for views/likes/comments), Top & Bottom Posts (most/least by likes, comments, engagement)
- **Tab 2: Data Explorer** — Advanced filters, caption search, full data table, quick insights, CSV/Excel export

### Page 5: Conversation Intel ("The Landscape")
Uses autostrat hashtag/keyword/news reports only — sidebar filters do NOT apply. No quantitative metrics, purely qualitative intelligence. Dynamic multi-platform support (Instagram + TikTok) with platform badges (IG/TT) on each expander.
- **Tab 1: Brand Hashtags** — Dynamically loaded via `get_brand_hashtag_reports()` using `BRAND_HASHTAGS` config whitelist. Covers all brands across Instagram hashtags, TikTok hashtags, and TikTok keywords. Per-report: key insights, NOPD audience profiles, opportunities & strategic actions, How to Win territories. "What This Means for Cuervo" strategic takeaway with four cards: Where Cuervo Leads (unique territories), Where Competitors Are Winning (per-brand breakdown + gaps), Common Audience Friction (objections per brand), Cuervo's Path Forward (summary + desires). Brand Mentions section at bottom (moved from former Page 2 Tab 3).
- **Tab 2: Category & Cultural** — Dynamically loaded via `get_category_reports()` using `CATEGORY_HASHTAGS` config whitelist (only explicitly listed identifiers appear). Per-report: executive summary, audience profile (NOPD), content opportunities, How to Win territories. "Cuervo's Play" bridge narrative dynamically pairs first Cuervo brand report with first category report.
- **Tab 3: Google Search News** — Per-report accordions with: executive summary + key insights, news analysis with sentiment breakdown (positive/neutral/negative gauges), key topics, opportunities & risks (side-by-side), audience profile (NOPD), SWOT analysis (strengths/weaknesses/opportunities/threats), brand mentions with sentiment badges, trending narratives, strategic implications + action items, in-market campaigns, key statistics, news quotes

## Data Sources (3 modes, selected in sidebar)
1. **Demo Data** — synthetic data from `sample_data.py` (BRAND_PROFILES based on real research but posts are fake)
2. **Sprout Social Import** — real data from CSV exports dropped into `data/sprout/`. Auto-detected when CSVs are present.
3. **Custom CSV Folder** — manually created CSVs matching the schema in `templates.py`

## Social Brief KPI Targets (2026 Social Strategy Deck)
All targets centralized in `SOCIAL_BRIEF_TARGETS` dict in `config.py`.
- Avg Engagements/Post: 200 (primary metric — total_engagement = likes + comments + shares + saves)
- Engagements per 1K Followers: 1.5 (for cross-brand normalization on Page 2)
- Creator Avg Engagements/Post: 300
- Reel Ratio (IG): 50% of feed
- Carousel Ratio (IG): 30% of feed
- IG Posts/Month: 12-16 (updated from 8-10)
- TT Posts/Week: 3-5x (updated from 2-3x)
- Save Rate: 5.0%+
- Share Rate: 5.0%+
- Creator % of Total: Ramp to 30% by June 2026

## Poplife Playbook Frameworks (config.py) — Updated Feb 2026
- **Content Pillars** (2): Cuervo in Culture (80% — Especial + RTDs + Tradicional), Tradicional Made Social (20% — Cuervo Tradicional)
- **Content Mix**: Entertain (50%), Educate (30%), Connect (10%), Convince (10%)
- **Content Source / Engine**: Owned / Sponsored Live Events (50%), Creator / Influencer / UGC (30%), Brand-Owned (20%)
- **Product Focus**: Especial (60%), RTDs (10%), Tradicional (30%)
- **Cadence**: IG 12-16/month, TT 3-5x/week
- **Execution Engines** (4): Memes + Reactive Culture, Creator-Led + UGC, Event + Festival Trend Factory, Lifestyle Shoot Bank
- **Creator Archetypes** (5): The Party Starter, The Home Bartender, The Lifestyle Bestie, The Culture Commentator, The Festival Friend
- **SKU Strategy**: Especial (high energy/fun), Tradicional (elevated), RTD (mid-high/daytime)
- **North Star**: "Spark the Moment — Everyday to Unforgettable"
- **Brand Persona**: "The Life of the Party"

## Key Technical Details
- `st.session_state` shares data across pages: `results`, `df`, `filtered_df`, `sel_brands`, `sel_platforms`, `autostrat`
- `results` dict from `analysis.py` has keys: `posts`, `profiles`, `frequency`, `engagement`, `captions`, `hashtags`, `themes`, `creators`, `recommendations`
- Pages 1, 3 use unfiltered `st.session_state["df"]` — sidebar filters don't apply
- Pages 2, 4 use `st.session_state["filtered_df"]` — sidebar filters apply
- Page 5 uses `st.session_state["autostrat"]` directly — no quantitative data, sidebar filters do NOT apply. Reports are classified via `BRAND_HASHTAGS` and `CATEGORY_HASHTAGS` config whitelists.
- Brand colors and CSS match poplife99.com palette (peach #F8C090, blue #2ea3f2, dark #333333)
- `st.logo("logo.png")` and `st.markdown(CUSTOM_CSS)` must be called in every page file
- Plotly charts use `use_container_width=True` for responsive sizing
- Favicon is `favicon.png` (Poplife "P" icon)

## Engagement Methodology
- **Primary metric**: `total_engagement` (likes + comments + shares + saves) — raw count, reliably available across all data sources
- **Cross-brand normalization**: `engagement_per_1k_followers` = `(avg_engagement / followers) × 1000` — used on Page 2 (Competitive Landscape) for fair comparison across different audience sizes
- **No ER calculation**: The old 3-tier engagement rate system (`calc_engagement_rate()`) was removed. All charts/scorecards now use raw engagement counts or per-1K-followers normalization.
- **Benchmark CSV** (`import_benchmark_csv()` in `sprout_import.py`): Still used for follower counts, Reels data, and avg hashtags per post. Auto-detected when filename starts with `benchmark_csv`. Benchmark follower counts override Sprout/fallback followers.
- **Fallback follower counts** in `sprout_import.py` for brands missing from Sprout aggregates: 1800 Tequila (108K), Don Julio (460K), El Jimador (43.4K), Hornitos (36.1K), Lunazul (12.2K), Milagro (23.7K). Overridden by benchmark when present.
- **Cache busting**: `_sprout_fingerprint()` in `app.py` includes `CODE_VERSION` string — bump this whenever sprout_import.py or analysis.py logic changes

## Autostrat Intelligence
- Qualitative reports from autostrat.ai — audience psychographics, competitive positioning, content trends, creator archetypes
- `st.session_state["autostrat"]` stores `{report_type: {identifier: report_data}}`
- 8 report type directories: instagram_profiles, tiktok_profiles, instagram_hashtags, tiktok_hashtags, instagram_keywords, tiktok_keywords, google_news (+ pdfs/ for imports)
- Current Instagram hashtag data (12 reports): josecuervo, cuervo, cazadores, hornitos, lunazul, milagrotequila, eljimador, teremanatequila, 1800tequila, casamigos, margaritatime
- Current Instagram keyword data (2 Cuervo reports): jose_cuervo, cuervo_tequila
- Current Instagram profile data (4 reference brands): duolingo, drinkpoppi, chipotle, dunkin
- Current TikTok profile data (4 reference brands): duolingo, drinkpoppi, chipotle, dunkin
- Current TikTok hashtag/keyword data: none yet (directories exist with templates only — TikTok reports to be added)
- Current Google News data: jose_cuervo_tequila.json (full report with NOPD, SWOT, news trends/topics, campaigns, quotes, statistics)
- Report classification whitelists in config.py: `BRAND_HASHTAGS` (12 identifiers → Page 5 Tab 1, includes 10 brand hashtags + 2 Cuervo keywords), `CATEGORY_HASHTAGS` (category conversations → Page 5 Tab 2), `CUERVO_HASHTAG_IDS` (Cuervo-specific subset for Page 1 Tab 3 + cross-brand comparison logic)
- NOPD framework: Needs (#2ea3f2), Objections (#D9534F), Desires (#5CB85C), Pain Points (#F8C090)
- PDF/PPTX import: sidebar button triggers parser, outputs JSON to correct subdirectory. Supports both PDF (via pdfplumber) and PPTX (via python-pptx) autostrat exports. PPTX extractor handles shape positioning, row clustering, group shapes, and NOPD table detection.
- To add new reports: drop JSON into the correct `data/autostrat/{report_type}/` directory, or drop PDF/PPTX into `data/autostrat/pdfs/` and click "Import PDFs" in sidebar. For brand hashtags, add the identifier to `BRAND_HASHTAGS` in config.py. For category hashtags, add to `CATEGORY_HASHTAGS`.

## Running
```bash
python3 -m streamlit run app.py --server.headless true
# Opens at http://localhost:8501
```

## Dependencies
- streamlit, plotly, pandas, openpyxl, pdfplumber, python-pptx

## Sprout Social CSV Files (data/sprout/)
Currently 7 CSV exports covering Oct 1, 2025 – Jan 31, 2026:
- `Post Performance` — Cuervo's own posts (77 non-Story), has `Engagement Rate (per Impression)`, impressions, likes, comments, shares, saves
- `Competitor Posts` — 305 competitor posts, has `Public Engagements`, comments, shares — NO impressions or ER
- `Competitor Performance` — Daily aggregate rows (1722), has `Public Engagements per Post` and `Audience`
- `Competitor Performance 2` — Reference brands aggregate (861 rows)
- `Instagram Competitors` — Daily competitor data (1599 rows), has `Public Engagements per Post` and `Followers`
- `Instagram Business Profiles` — Cuervo only (123 rows)
- `Profile Performance` — Cuervo only (123 rows)

## Pending / Known Issues
- **Impressions data incoming:** Sprout's Post Performance export only has impressions for Stories, not feed posts (Reels/Carousels/Static). The format breakdown chart currently uses total engagements as a volume proxy. Once we get post-level impressions data, swap the "Avg Total Engagements by Format" chart in Page 1 Tab 2 back to "Avg Reach (Impressions) by Format" — the impressions code path is already in `sprout_import.py` (the `impressions` field is imported), just needs data that has non-zero values for feed posts.
- TikTok data not yet in Sprout exports — TikTok sections show zeros on Sprout import mode
- TikTok autostrat reports (hashtags, keywords) not yet imported — directories exist with templates only. TikTok profiles imported for 4 reference brands.
- Instagram keyword autostrat reports: 2 Cuervo reports imported (jose_cuervo, cuervo_tequila); no competitor keyword reports yet
- Don Julio and 1800 Tequila awaiting data population in Sprout (using fallback follower counts)
- Content theme classifier is keyword-based (~80-85% accuracy) — can be improved
- Follower growth % not trackable from single-month static exports
- Cross-brand engagement comparison uses per-1K-followers normalization (not ER) — accuracy depends on follower count data quality
