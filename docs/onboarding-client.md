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
- **Collaboration column taxonomy** (`manual_posts.csv` → `collaboration` column): Use the hero brand's name (e.g. `Cuervo`) for organic posts, and `Partner` / `Influencer` / `Collective` for posts whose reach is amplified by another account. Only posts tagged with the hero brand name go into the owned bucket used by the KPI scorecard on Page 1 — everything else gets filtered to the amplified bucket. See `docs/schemas.md` for the full column spec and `docs/decisions.md` (2026-04-09 entry) for the rationale. If your new client needs a different taxonomy, update `COLLAB_OWNED_TYPES` / `COLLAB_AMPLIFIED_TYPES` in `config.py` — or better, lift those sets into `ClientConfig` so they're per-client.
