# Poplife Social Intelligence Platform

## What This Is
A **multi-tenant** competitive social media intelligence platform built for **Poplife** agency. Strategy-first Streamlit dashboard analyzing Instagram and TikTok performance, with qualitative intelligence from autostrat.ai reports and per-client strategy playbooks.

Supports multiple clients via `?client=` URL parameter. No param shows an internal client picker.

## Active Clients

### Jose Cuervo (`?client=cuervo`)
- **Hero brand**: Jose Cuervo | **Industry**: Tequila
- **Competitive set**: 13 tequila brands (Patron, Don Julio, Casamigos, Espolon, Teremana, 1800, 818, Lunazul, Hornitos, Cazadores, Milagro, El Jimador)
- **Strategy pillars**: Cuervo in Culture (80%), Tradicional Made Social (20%)
- **Data**: Sprout Social CSV exports (Oct 2025 – Feb 2026) + 12 autostrat hashtag reports + Google News

### Devils Reserve (`?client=devils_reserve`)
- **Hero brand**: Devils Reserve | **Industry**: Tequila (flavored — pineapple + jalapeño)
- **Competitive set**: 5 brands (Fireball, Pink Whitney, Jagermeister, Cazadores)
- **Strategy pillars**: Event Energy (45%), Creator & Influencer (30%), Flavor Forward (25%)
- **Data**: Sprout Social CSV exports (Nov 2025 – Feb 2026) + 4 competitor keyword autostrat PDFs

## Architecture

```
app.py                          # Entry point — ?client= routing, client picker, data loading, sidebar filters
client_context.py               # ClientConfig loader: load_client_config(), get_client(), set_active_client()
config.py                       # SHARED constants only: CHART_TEMPLATE, CHART_FONT, POPLIFE colors, PRIORITY_COLORS

clients/
  _schema.py                    # ClientConfig dataclass definition (all fields)
  cuervo/
    client.py                   # get_config() -> ClientConfig
    brands.py                   # BRANDS, BRAND_ORDER, BRAND_COLORS, BRAND_MAP, FALLBACK_FOLLOWERS, etc.
    strategy.py                 # Pillar maps, KPI targets, content mix, calendars, etc.
    copy.py                     # PAGE_HEADERS, PAGE_CAPTIONS, NAV_TABLE, NARRATIVE
    assets/                     # logo.png, favicon.png, app_logo.png
  devils_reserve/
    client.py, brands.py, strategy.py, copy.py, assets/

data/
  cuervo/                       # Per-client data directories
    sprout/                     # Drop Sprout Social CSV exports here
    autostrat/                  # Parsed autostrat JSON reports (7 report type subdirs + pdfs/)
    sprout_imported/            # Auto-generated from Sprout import
  devils_reserve/
    sprout/
    autostrat/
    sprout_imported/

pages/
  1_Brand_Performance.py        # "The Mirror" — KPI scorecard, content performance, self-audit
  2_Competitive_Landscape.py    # "The Window" — cross-brand comparison, content gaps
  3_2026_Strategy.py            # "The Playbook" — strategy scorecard, frameworks, action plan
  4_Inspiration_&_Explorer.py   # "The Toolbox" — reference brands + data explorer
  5_Conversation_Intel.py       # "The Landscape" — hashtag/keyword intel, Google News

# Core modules (client-agnostic)
analysis.py                     # Core analysis engine — run_full_analysis(data_dir)
sprout_import.py                # Sprout Social CSV import + AI content classifiers
autostrat_parser.py             # PDF/PPTX-to-JSON parser for autostrat.ai exports
autostrat_loader.py             # JSON loader + cross-report extraction helpers
autostrat_components.py         # Reusable UI components for narrative content
dashboard.py                    # Excel report generator
templates.py                    # Shared content taxonomy (themes, tones, CTAs)
sample_data.py                  # Demo data generator
```

## Multi-Tenant Architecture

### Client Routing (app.py)
```python
client_id = st.query_params.get("client", None)
if client_id is None:
    # Internal view — client picker dropdown
else:
    cfg = load_client_config(client_id)  # imports clients/{client_id}/client.py
    set_active_client(cfg)               # stores in st.session_state
```

### Accessing Client Config (any page)
```python
from client_context import get_client
cfg = get_client()
# cfg.hero_brand, cfg.brand_colors, cfg.kpi_targets, cfg.narrative, etc.
```

### Adding a New Client
1. Create `clients/{client_id}/` with `client.py`, `brands.py`, `strategy.py`, `copy.py`, `assets/`
2. `client.py` must export `get_config() -> ClientConfig`
3. Create `data/{client_id}/sprout/` and `data/{client_id}/autostrat/` directories
4. Drop Sprout CSV exports into `data/{client_id}/sprout/`
5. Add handle→brand mappings to `brands.py` `BRAND_MAP`
6. Navigate to `?client={client_id}` — dashboard renders

### ClientConfig Fields (clients/_schema.py)
- **Identity**: `client_id`, `client_name`, `hero_brand`, `agency_name`, `industry`
- **Brands**: `brands`, `brand_order`, `brand_colors`, `brand_map`, `fallback_followers`
- **Reference brands**: `reference_brands`, `reference_brand_labels`
- **Autostrat**: `brand_hashtags`, `hero_hashtag_ids`, `category_hashtags`, `hero_news_id`
- **Strategy**: `pillar_map/targets/colors/descriptions`, `content_mix_map/targets/colors`, `kpi_targets`, `cadence_targets`, `ig_format_mix`, `platform_roles`, `content_source_mix`, `monthly_ramp`, `testing_roadmap`, `cultural_calendar`, `sku_strategy`, `execution_engines`, `creator_archetypes`, `voice_principles`, `gen_z_leaders`
- **Sprout import**: `creator_program_signals`, `theme_keywords`, `tone_keywords`
- **Demo data**: `brand_profiles`, `hashtag_pools`
- **Theming**: `primary_color`, `background_color`, `dark_color`, `accent_color`, `custom_css`
- **Assets**: `logo_path`, `favicon_path`, `app_logo_path`
- **Copy**: `page_title`, `home_title`, `home_subtitle_template`, `page_headers`, `page_captions`, `nav_table`, `excel_filename`, `highlight_fill_color`
- **Narrative**: `narrative` (nested dict: `narrative["page_key"]["section_key"]`)
- **Data paths**: `data_dir`, `sprout_dir`, `autostrat_dir`, `sprout_output_dir` (resolved at load time)

## Page Structure

### Page 1: Brand Performance ("The Mirror")
Uses UNFILTERED data — sidebar filters do NOT apply. Hero brand-only view.
- **Tab 1: KPI Dashboard** — KPI scorecard vs targets, cadence scorecard, engagement signals
- **Tab 2: Content Performance** — Format breakdown, theme performance, best & worst posts
- **Tab 3: Self-Audit Intelligence** — Hero brand autostrat reports (loaded via `cfg.hero_hashtag_ids`)

### Page 2: Competitive Landscape ("The Window")
Uses FILTERED data — sidebar brand/platform/type filters apply.
- **Tab 1: Competitive Overview** — Side-by-side comparison, Eng/1K Followers chart
- **Tab 2: Content Gaps** — Theme gap analysis, format strategy, "What to Steal" cards

### Page 3: Strategy & Brief ("The Playbook")
Uses UNFILTERED data — sidebar filters do NOT apply.
- **Tab 1: Scorecard** — KPI table, content source mix
- **Tab 2: Content Strategy Frameworks** — Pillars, content mix funnel, Gen Z drivers
- **Tab 3: Action Plan** — 30-day plan, threats & opportunities, recommendations

### Page 4: Inspiration & Explorer ("The Toolbox")
- **Tab 1: Inspiration** — Reference brand profiles, "What {hero} Can Steal", audience comparison
- **Tab 2: Data Explorer** — Advanced filters, caption search, full data table, CSV/Excel export

### Page 5: Conversation Intel ("The Landscape")
Uses autostrat reports only — sidebar filters do NOT apply.
- **Tab 1: Brand Hashtags** — Per-brand reports, "What This Means for {hero}" takeaway
- **Tab 2: Category & Cultural** — Category conversation reports, bridge narrative
- **Tab 3: Google Search News** — News analysis, SWOT, sentiment, action items

## Data Sources (3 modes, selected in sidebar)
1. **Demo Data** — synthetic from `sample_data.py`
2. **Sprout Social Import** — real CSV exports from `data/{client_id}/sprout/`. Auto-detected.
3. **Custom CSV Folder** — manually created CSVs matching schema in `templates.py`

## Key Technical Details
- `st.session_state` shares data across pages: `results`, `df`, `filtered_df`, `sel_brands`, `sel_platforms`, `autostrat`, `client_config`
- All pages call `cfg = get_client()` — never import client-specific constants directly
- `config.py` contains ONLY shared constants (chart styling, Poplife palette colors)
- All client-specific constants live in `clients/{client_id}/` modules
- `st.logo(cfg.logo_path)` and `st.markdown(cfg.custom_css)` called in every page
- Cache isolation: `load_demo(client_id)` uses client_id as cache key; `load_sprout()` uses per-client sprout dir + fingerprint
- Data paths resolved at load time by `client_context.py`: `data/{client_id}/sprout/`, `data/{client_id}/autostrat/`

## Engagement Methodology
- **Primary metric**: `total_engagement` (likes + comments + shares + saves)
- **Cross-brand normalization**: `engagement_per_1k_followers` = `(avg_engagement / followers) × 1000`
- **Fallback follower counts** per client in `brands.py` `FALLBACK_FOLLOWERS`
- **Benchmark CSV**: auto-detected when filename starts with `benchmark_csv`; overrides fallback followers
- **Cache busting**: `_sprout_fingerprint()` includes `CODE_VERSION` string

## Autostrat Intelligence
- Qualitative reports from autostrat.ai — audience psychographics, competitive positioning, content trends
- `st.session_state["autostrat"]` stores `{report_type: {identifier: report_data}}`
- 7 report type directories: instagram_profiles, tiktok_profiles, instagram_hashtags, tiktok_hashtags, instagram_keywords, tiktok_keywords, google_news (+ pdfs/)
- Report classification whitelists in each client's `brands.py`: `BRAND_HASHTAGS`, `CATEGORY_HASHTAGS`, `HERO_HASHTAG_IDS`
- NOPD framework: Needs (#2ea3f2), Objections (#D9534F), Desires (#5CB85C), Pain Points (#F8C090)
- PDF/PPTX import: sidebar button triggers parser, outputs JSON to correct subdirectory
- To add reports: drop JSON/PDF into `data/{client_id}/autostrat/` and click "Import PDFs"

## Running
```bash
python3 -m streamlit run app.py --server.headless true
# Opens at http://localhost:8501
# No query param → client picker
# ?client=cuervo → Cuervo dashboard
# ?client=devils_reserve → Devils Reserve dashboard
```

## Dependencies
- streamlit, plotly, pandas, openpyxl, pdfplumber, python-pptx
