# Poplife Social Intelligence Platform — Agent Handoff

## Project Overview

**Multi-tenant** competitive social media intelligence platform built for **Poplife** agency. Streamlit dashboard analyzing Instagram and TikTok performance with qualitative autostrat.ai intelligence. Serves multiple clients via `?client=` URL parameter.

```bash
python3 -m streamlit run app.py
# http://localhost:8501 → client picker
# http://localhost:8501/?client=cuervo → Cuervo dashboard
# http://localhost:8501/?client=devils_reserve → Devils Reserve dashboard
```

See `CLAUDE.md` for full architecture documentation.

---

## Multi-Tenant Architecture (Completed March 2026)

The codebase was refactored from a single-client Cuervo dashboard to a multi-tenant platform. Key changes:

### Client Config System
- `clients/_schema.py` — `ClientConfig` dataclass with ~50 fields
- `client_context.py` — `load_client_config()`, `get_client()`, `set_active_client()`
- Each client has `clients/{id}/client.py` exporting `get_config() -> ClientConfig`
- All pages call `cfg = get_client()` — no hardcoded brand names or constants

### Data Isolation
- Per-client data directories: `data/{client_id}/sprout/`, `data/{client_id}/autostrat/`
- Cache isolation via `client_id` in `@st.cache_data` function parameters
- Temp file paths include `client_id`

### Shared vs Client-Specific
- `config.py` — **shared only**: `CHART_TEMPLATE`, `CHART_FONT`, `POPLIFE_PEACH/BLUE/BG/DARK`, `PRIORITY_COLORS`
- All client-specific constants (brands, colors, KPIs, strategy, CSS, narrative copy) live in `clients/{id}/`

---

## Active Clients

### Jose Cuervo (`cuervo`)
- 13 tequila brands, Sprout data Oct 2025 – Feb 2026
- Full autostrat coverage: 12 hashtag reports, 2 keyword reports, 4 reference brand profiles, Google News
- Strategy: 2 pillars (Cuervo in Culture 80%, Tradicional Made Social 20%)

### Devils Reserve (`devils_reserve`)
- 5 brands (DR + Fireball, Pink Whitney, Jagermeister, Cazadores)
- Sprout data Nov 2025 – Feb 2026
- 4 competitor keyword autostrat PDFs (not yet parsed to JSON)
- Strategy: 3 pillars (Event Energy 45%, Creator & Influencer 30%, Flavor Forward 25%)
- Small/growth-phase account (~2K IG followers) — KPI targets calibrated accordingly
- Still needs: DR's own autostrat report, logo assets, hero_hashtag_ids

---

## Adding a New Client

1. Create directory: `clients/{client_id}/`
2. Create files following the pattern in `clients/cuervo/`:
   - `client.py` — `get_config() -> ClientConfig`
   - `brands.py` — competitive set, colors, Sprout handle mappings
   - `strategy.py` — pillars, KPIs, calendars, creator archetypes
   - `copy.py` — page headers, captions, narrative text blocks
   - `assets/` — logo.png, favicon.png, app_logo.png
3. Create data directories: `data/{client_id}/sprout/`, `data/{client_id}/autostrat/{report_types}/`
4. Drop Sprout CSV exports into `data/{client_id}/sprout/`
5. The BRAND_MAP in `brands.py` must map Sprout CSV "Profile" column values to your canonical brand names
6. Navigate to `?client={client_id}`

---

## Known Issues

1. **Devils Reserve autostrat PDFs** need to be parsed — click "Import PDFs" in sidebar when viewing DR dashboard
2. **Devils Reserve logo** — currently using Poplife logo as placeholder; needs custom DR assets
3. **Devils Reserve hero_hashtag_ids** — empty set until DR's own autostrat report is imported
4. **TikTok data gap** — TikTok sections show zeros when no TikTok post data in Sprout exports
5. **Content theme classifier** is keyword-based (~80-85% accuracy)
6. **Python 3.9 compat** — `_schema.py` uses `from __future__ import annotations` for `X | None` syntax

---

## Key Files Quick Reference

| File | Purpose |
|------|---------|
| `app.py` | Entry point, client routing, data loading, sidebar |
| `client_context.py` | Client config loader + session state helpers |
| `clients/_schema.py` | ClientConfig dataclass |
| `clients/{id}/client.py` | Per-client config assembler |
| `config.py` | Shared constants only (chart styling, colors) |
| `analysis.py` | Core analysis engine |
| `sprout_import.py` | Sprout CSV import + classifiers |
| `autostrat_parser.py` | PDF/PPTX → JSON parser |
| `autostrat_loader.py` | JSON loader + extraction helpers |
| `pages/1_Brand_Performance.py` | Hero brand KPIs + self-audit |
| `pages/2_Competitive_Landscape.py` | Cross-brand comparison |
| `pages/3_2026_Strategy.py` | Strategy playbook |
| `pages/4_Inspiration_&_Explorer.py` | Reference brands + data explorer |
| `pages/5_Conversation_Intel.py` | Hashtag/keyword/news intel |

---

*Last updated: March 4, 2026*
*Project root: `/Users/loucesario/cuervo-intel`*
