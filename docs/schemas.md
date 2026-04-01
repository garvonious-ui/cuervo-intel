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
