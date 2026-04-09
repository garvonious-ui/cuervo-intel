# Schemas & Data Reference

## ClientConfig Fields (clients/_schema.py)

### Identity
- `client_id` (str) — URL slug, e.g. "cuervo"
- `client_name` (str) — display name
- `hero_brand` (str) — primary brand being analyzed
- `agency_name` (str) — always "Poplife"
- `industry` (str) — e.g. "Tequila"

### Brands & Competitive Set
- `brands` (list[str]) — all brand names including hero
- `brand_order` (list[str]) — display ordering
- `brand_colors` (dict) — {brand_name: hex_color}
- `brand_map` (dict) — {sprout_csv_profile_value: canonical_brand_name}
- `fallback_followers` (dict) — {brand_name: follower_count}

### Reference Brands
- `reference_brands` (list[str]) — inspirational brand handles
- `reference_brand_labels` (dict) — {handle: display_label}

### Autostrat Report IDs
- `brand_hashtags` (dict) — {brand_name: [hashtag_ids]}
- `hero_hashtag_ids` (set) — hero brand's own hashtag report identifiers
- `category_hashtags` (dict) — {category_label: [hashtag_ids]}
- `hero_news_id` (str|None) — Google News report identifier

### Strategy
- `pillar_map` (dict) — {post_pillar: strategy_pillar}
- `pillar_targets` (dict) — {pillar: percentage_target}
- `pillar_colors` (dict) — {pillar: hex_color}
- `pillar_descriptions` (dict) — {pillar: description_text}
- `content_mix_map` (dict) — {content_type: funnel_stage}
- `content_mix_targets` (dict) — {stage: percentage}
- `content_mix_colors` (dict) — {stage: hex_color}
- `kpi_targets` (dict) — {metric_name: target_value}
- `cadence_targets` (dict) — {platform: posts_per_month}
- `ig_format_mix` (dict) — {format: percentage}
- `platform_roles` (dict) — {platform: role_description}
- `content_source_mix` (dict) — {source_type: percentage}
- `monthly_ramp` (dict) — {month: planned_posts}
- `testing_roadmap` (list) — ordered test items
- `cultural_calendar` (list[dict]) — events with dates
- `sku_strategy` (dict) — product line strategy
- `execution_engines` (list) — content engine descriptions
- `creator_archetypes` (list[dict]) — creator partnership types
- `voice_principles` (list) — brand voice guidelines
- `gen_z_leaders` (list[dict]) — Gen Z audience driver profiles

### Sprout Import Classifiers
- `creator_program_signals` (list[str]) — keywords triggering creator classification
- `theme_keywords` (dict) — {theme: [keywords]}
- `tone_keywords` (dict) — {tone: [keywords]}

### Theming & Assets
- `primary_color`, `background_color`, `dark_color`, `accent_color` (str) — hex colors
- `custom_css` (str) — injected via `st.markdown()`
- `logo_path`, `favicon_path`, `app_logo_path` (str) — asset file paths

### Copy & Narrative
- `page_title`, `home_title`, `home_subtitle_template` (str)
- `page_headers` (dict) — {page_key: header_text}
- `page_captions` (dict) — {page_key: caption_text}
- `nav_table` (list[dict]) — navigation metadata
- `excel_filename` (str) — export filename
- `highlight_fill_color` (str) — Excel highlight color
- `narrative` (dict) — nested `{page_key: {section_key: text_block}}`

### Feature Flags
- `themes_ready` (bool, default True) — set False to hide theme/content-source sections until manual post tagging is done

### Data Paths (resolved at load time)
- `data_dir` — `data/{client_id}/`
- `sprout_dir` — `data/{client_id}/sprout/`
- `autostrat_dir` — `data/{client_id}/autostrat/`
- `sprout_output_dir` — `data/{client_id}/sprout_imported/`

## Sprout Social CSV Schema
Expected CSV exports in `data/{client_id}/sprout/`:
- Post Performance — individual post metrics
- Profile Performance — account-level metrics
- Competitor Posts — competitor post data
- Competitor Performance — competitor account metrics
- Instagram Business Profiles — IG profile data
- TikTok Profiles — TikTok profile data
- Instagram Competitors — IG competitor profiles

Key columns: Profile, Date, Impressions, Engagements, Likes, Comments, Shares, Saves, Video Views, Post Type, Content Type, Permalink, Caption

## Manual Posts Schema (`manual_posts.csv`)
Lives at `data/{client_id}/sprout/manual_posts.csv`. Replaces the hero brand's Sprout-derived rows during import (see `sprout_import.py:816-851`). Used so the hero brand's posts carry manually-curated tags (pillar, funnel, collab type) that Sprout doesn't provide, and so posts Sprout missed can still be captured.

**Required columns:** `brand`, `platform`, `post_date`, `post_type`, `post_url`, `content_pillar`, `content_mix_funnel`, `collaboration`, `likes`, `comments`, `shares`, `saves`, `views`

**Important optional columns** (carried forward from Sprout exports when merged): `caption_text`, `hashtags`, `post_time`, `video_length_seconds`, `impressions`, `total_engagement`, `caption_word_count`, `creator_handle`, `has_creator_collab`, `is_paid_partnership`

**`collaboration` column values** (drives the owned vs amplified split — see `config.py split_owned_collab()` and `docs/decisions.md`):
- **`<hero_brand>`** (e.g. `Cuervo`) — the hero brand's own organic posts. These count as **owned** and flow into the hero KPI scorecard on Page 1.
- **`Partner`** — posts that involve a business/brand partnership. Treated as **amplified** because the Partner tag covers IG Collab Posts and event activations that get reach from the partner's audience.
- **`Influencer`** — paid creator posts (one-off creator partnerships). **Amplified.**
- **`Collective`** — recurring "Cuervo Collective" creator program posts. **Amplified.**

Amplified posts are excluded from hero KPIs on Pages 1 and 3, shown separately in Page 1's Collab Amplification section, and filtered out of Page 2's competitive comparisons for apples-to-apples brand benchmarking.

**`content_pillar` values** (must match `cfg.pillar_map.keys()` for the active client): For Cuervo: `The Ritual`, `The Pulse`, `The Front Row`, `The Craft`.

**`content_mix_funnel` values** (must match `cfg.content_mix_targets.keys()`, plus the special `Edutain` value): For Cuervo: `Convince`, `Educate`, `Entertain`, plus `Edutain` (which gets split 0.5/0.5 into Educate and Entertain at load time via `app.py:209-225`).

## Autostrat Report Types
7 directories under `data/{client_id}/autostrat/`:
- `instagram_profiles/` — IG brand profile analysis
- `tiktok_profiles/` — TikTok brand profile analysis
- `instagram_hashtags/` — IG hashtag conversation analysis
- `tiktok_hashtags/` — TikTok hashtag analysis
- `instagram_keywords/` — IG keyword analysis
- `tiktok_keywords/` — TikTok keyword analysis
- `google_news/` — Google News analysis
- `pdfs/` — raw PDF/PPTX files for import

NOPD framework colors: Needs (#2ea3f2), Objections (#D9534F), Desires (#5CB85C), Pain Points (#F8C090)
