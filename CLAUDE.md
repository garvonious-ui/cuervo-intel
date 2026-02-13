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
  3_2026_Strategy.py           # "The Playbook" — Social Brief scorecard, GOAT frameworks, action plan
  4_Inspiration_&_Explorer.py  # "The Toolbox" — Reference brands + full data explorer
  5_Hashtag_&_Search_Intel.py  # "The Landscape" — Brand hashtag comparison + search term intelligence
autostrat_parser.py    # PDF-to-JSON parser for autostrat.ai report exports
autostrat_loader.py    # JSON loader + cross-report extraction helpers
autostrat_components.py # Reusable UI components for narrative content
config.py              # Brand colors, BRAND_ORDER, GOAT frameworks, CUSTOM_CSS (Poplife palette)
templates.py           # BRANDS list, content themes, visual styles, tone options
analysis.py            # Core analysis engine — run_full_analysis(data_dir)
sample_data.py         # Demo data generator with realistic brand profiles
sprout_import.py       # Sprout Social CSV import adapter + AI content classifiers
dashboard.py           # Excel report generator (download button)
data/sprout/           # Drop Sprout Social CSV exports here
data/autostrat/        # Parsed autostrat JSON reports (6 subdirectories)
data/autostrat/pdfs/   # Drop autostrat PDF exports here for import
```

## Page Structure

### Page 1: Cuervo Performance ("The Mirror")
Uses UNFILTERED data — sidebar filters do NOT apply. Cuervo-only view.
- **Tab 1: KPI Dashboard** — Social Brief KPI scorecard (ER vs 3%, Reel ratio vs 50%, Reel views vs 10K, posts/week vs targets), "So What" narrative, platform cadence scorecard, engagement signals (save/share/comment rates)
- **Tab 2: Content Performance** — Format breakdown (pie + ER by format), theme performance chart, best & worst 5 posts with caption previews
- **Tab 3: Self-Audit Intelligence** — josecuervo + margaritatime autostrat reports (key insights, NOPD, How to Win, strategic actions, verbatims)

### Page 2: Competitive Landscape ("The Window")
Uses FILTERED data — sidebar brand/platform/type filters apply.
- **Tab 1: Competitive Overview** — Side-by-side comparison table, "Who's Winning & Why" narrative, ER bar chart with 3% target line
- **Tab 2: Content Gaps** — Cuervo vs category theme gap analysis, format strategy stacked bar, posting frequency comparison, "What to Steal" cards for brands beating Cuervo
- **Tab 3: Competitor Intelligence** — Cazadores + Hornitos autostrat reports, competitive brand mentions

### Page 3: 2026 Strategy & Brief ("The Playbook")
Uses UNFILTERED data — sidebar filters do NOT apply. Dedicated to the Social Brief.
- **Tab 1: Social Brief Scorecard** — Expanded KPI table with status indicators, dynamic vs static ER comparison, content source mix (Creator 70% / Brand 15% / Events 15%)
- **Tab 2: Content Strategy Frameworks** — GOAT content pillars (La Tradición / Cuervo Live / Life with a Lime / Culture Shaken), content mix funnel (Entertain 50% / Educate 30% / Connect 10% / Convince 10%), Gen Z engagement drivers
- **Tab 3: Action Plan** — 30-day weekly plan, threats & opportunities, all recommendations, qualitative intelligence (winning territories, content trends, creator archetypes, partnership opportunities)

### Page 4: Inspiration & Explorer ("The Toolbox")
- **Tab 1: Inspiration** — Duolingo/Poppi/Chipotle/Dunkin' reference brand profiles, "What Cuervo Can Steal" section, side-by-side audience comparison (NOPD), How to Win territories
- **Tab 2: Data Explorer** — Advanced filters, caption search, full data table, quick insights, CSV/Excel export

### Page 5: Hashtag & Search Intel ("The Landscape")
Uses autostrat hashtag reports only — sidebar filters do NOT apply. No quantitative metrics, purely qualitative intelligence.
- **Tab 1: Brand Hashtags** — Accordion comparison of #JoseCuervo, #Cuervo, #Cazadores, #Hornitos, #Lunazul, #MilagroTequila, #ElJimador: key insights, NOPD audience profiles, opportunities & strategic actions, How to Win territories. "What This Means for Cuervo" strategic takeaway with four cards: Where Cuervo Leads (unique territories), Where Competitors Are Winning (per-brand breakdown + gaps), Common Audience Friction (objections per brand), Cuervo's Path Forward (summary + desires)
- **Tab 2: Search Terms & Categories** — #MargaritaTime deep dive: executive summary, audience profile (NOPD), content opportunities, How to Win territories, "Cuervo's Play" narrative bridging brand and category hashtags

## Data Sources (3 modes, selected in sidebar)
1. **Demo Data** — synthetic data from `sample_data.py` (BRAND_PROFILES based on real research but posts are fake)
2. **Sprout Social Import** — real data from CSV exports dropped into `data/sprout/`. Auto-detected when CSVs are present.
3. **Custom CSV Folder** — manually created CSVs matching the schema in `templates.py`

## Social Brief KPI Targets
- Engagement Rate: 3%
- Avg Reel Views: 10,000
- Reel Ratio (IG): 50%
- IG Posts/Week: 4-5x
- TT Posts/Week: 3-4x
- Follower Growth: 15% (not tracked from static exports)

## GOAT Playbook Frameworks (config.py)
- **Content Pillars**: La Tradición (25%), Cuervo Live (15%), Life with a Lime (30%), Culture Shaken (30%)
- **Content Mix**: Entertain (50%), Educate (30%), Connect (10%), Convince (10%)
- **Content Source**: Creator & Influencer (70%), Brand-Owned (15%), Events & Partnerships (15%)
- **Cadence**: IG 8-10/month, TT 12-16/month

## Key Technical Details
- `st.session_state` shares data across pages: `results`, `df`, `filtered_df`, `sel_brands`, `sel_platforms`, `autostrat`
- `results` dict from `analysis.py` has keys: `posts`, `engagement`, `frequency`, `content`, `hashtags`, `creators`, `recommendations`
- Pages 1, 3 use unfiltered `st.session_state["df"]` — sidebar filters don't apply
- Pages 2, 4 use `st.session_state["filtered_df"]` — sidebar filters apply
- Page 5 uses `st.session_state["autostrat"]` directly — no quantitative data, sidebar filters do NOT apply
- Brand colors and CSS match poplife99.com palette (peach #F8C090, blue #2ea3f2, dark #333333)
- `st.logo("logo.png")` and `st.markdown(CUSTOM_CSS)` must be called in every page file
- Plotly charts use `width="stretch"` (not deprecated `use_container_width=True`)
- Favicon is `favicon.png` (Poplife "P" icon)

## Autostrat Intelligence
- Qualitative reports from autostrat.ai — audience psychographics, competitive positioning, content trends, creator archetypes
- `st.session_state["autostrat"]` stores `{report_type: {identifier: report_data}}`
- 6 report types: instagram_profiles, tiktok_profiles, instagram_hashtags, tiktok_hashtags, tiktok_keywords, google_news
- Current hashtag data: josecuervo.json, cuervo.json, cazadores.json, hornitos.json, lunazul.json, milagrotequila.json, eljimador.json, margaritatime.json
- Current profile data: duolingo.json, drinkpoppi.json, chipotle.json, dunkin.json
- NOPD framework: Needs (#2ea3f2), Objections (#D9534F), Desires (#5CB85C), Pain Points (#F8C090)
- PDF import: sidebar button triggers parser, outputs JSON to correct subdirectory

## Running
```bash
python3 -m streamlit run app.py --server.headless true
# Opens at http://localhost:8501
```

## Pending / Known Issues
- TikTok data not yet in Sprout exports — TikTok sections show zeros on Sprout import mode
- Don Julio and 1800 Tequila awaiting data population in Sprout
- Content theme classifier is keyword-based (~80-85% accuracy) — can be improved
- Follower growth % not trackable from single-month static exports
