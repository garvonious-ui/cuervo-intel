# Architecture

## Multi-Tenant System

### Client Routing (app.py)
- `st.query_params.get("client", None)` determines active client
- No param → internal client picker dropdown
- `load_client_config(client_id)` imports `clients/{client_id}/client.py`
- `set_active_client(cfg)` stores config in `st.session_state`

### Accessing Client Config (any page)
```python
from client_context import get_client
cfg = get_client()
# cfg.hero_brand, cfg.brand_colors, cfg.kpi_targets, cfg.narrative, etc.
```

### Data Isolation
- Per-client data dirs: `data/{client_id}/sprout/`, `data/{client_id}/autostrat/`
- Cache isolation: `@st.cache_data` functions use `client_id` as cache key
- Temp file paths include `client_id`

### Shared vs Client-Specific
- `config.py` — SHARED ONLY: `CHART_TEMPLATE`, `CHART_FONT`, Poplife palette, `PRIORITY_COLORS`, `split_owned_collab()`
- All client-specific constants (brands, colors, KPIs, strategy, CSS, narrative) → `clients/{id}/`

## Session State
`st.session_state` shares data across pages:
- `results` — output of `run_full_analysis()`
- `df` — full unfiltered DataFrame
- `filtered_df` — DataFrame after sidebar brand/platform/type filters
- `sel_brands`, `sel_platforms` — current sidebar filter selections
- `autostrat` — loaded autostrat reports dict
- `client_config` — active `ClientConfig` instance

## Data Sources (3 modes, sidebar selector)
1. **Demo Data** — synthetic from `sample_data.py`
2. **Sprout Social Import** — real CSV exports from `data/{client_id}/sprout/` (auto-detected)
3. **Custom CSV Folder** — manually created CSVs matching schema in `templates.py`

## Autostrat Intelligence
- Qualitative reports from autostrat.ai (audience psychographics, competitive positioning, trends)
- `st.session_state["autostrat"]` stores `{report_type: {identifier: report_data}}`
- 7 report type dirs: instagram_profiles, tiktok_profiles, instagram_hashtags, tiktok_hashtags, instagram_keywords, tiktok_keywords, google_news (+ pdfs/)
- PDF/PPTX import: sidebar button triggers parser → outputs JSON to correct subdirectory

## Engagement Methodology
- **Primary metric**: `total_engagement` = likes + comments + shares + saves
- **Cross-brand normalization**: `engagement_per_1k_followers` = `(avg_engagement / followers) × 1000`
- **Fallback followers** per client in `brands.py` `FALLBACK_FOLLOWERS`
- **Benchmark CSV**: auto-detected when filename starts with `benchmark_csv`; overrides fallback followers

## Key Technical Notes
- `st.logo(cfg.logo_path)` and `st.markdown(cfg.custom_css)` called on every page
- Cache busting: `_sprout_fingerprint()` includes `CODE_VERSION` string
- Python 3.9 compat: `_schema.py` uses `from __future__ import annotations` for `X | None` syntax
- Collaboration type split: owned (cuervo + partner) vs amplified (influencer + collective)
