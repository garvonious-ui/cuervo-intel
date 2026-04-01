# Adding a New Client

## Step-by-Step

1. **Create client directory**: `clients/{client_id}/`
2. **Create required files** (follow `clients/cuervo/` as template):
   - `client.py` — must export `get_config() -> ClientConfig`
   - `brands.py` — competitive set, `BRANDS`, `BRAND_ORDER`, `BRAND_COLORS`, `BRAND_MAP`, `FALLBACK_FOLLOWERS`
   - `strategy.py` — pillar maps, KPI targets, content mix, calendars, creator archetypes
   - `copy.py` — `PAGE_HEADERS`, `PAGE_CAPTIONS`, `NAV_TABLE`, `NARRATIVE`
   - `assets/` — logo.png, favicon.png, app_logo.png
   - `__init__.py` — empty file
3. **Create data directories**:
   - `data/{client_id}/sprout/`
   - `data/{client_id}/autostrat/` (with subdirs: instagram_profiles, tiktok_profiles, instagram_hashtags, tiktok_hashtags, instagram_keywords, tiktok_keywords, google_news, pdfs)
   - `data/{client_id}/sprout_imported/`
4. **Drop Sprout CSV exports** into `data/{client_id}/sprout/`
5. **Map Sprout handles**: `BRAND_MAP` in `brands.py` must map Sprout CSV "Profile" column values to canonical brand names
6. **Navigate to** `?client={client_id}` — dashboard renders

## Key Gotchas
- `BRAND_MAP` keys must exactly match the "Profile" column values in Sprout CSVs
- `FALLBACK_FOLLOWERS` provides follower counts when no Benchmark CSV is present
- Set `themes_ready=False` in `client.py` until all posts have been manually content-theme tagged
- Autostrat report IDs in `brands.py` must match the JSON filenames (without .json extension)
