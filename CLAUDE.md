# Cuervo Social Intelligence Dashboard

## What This Is
A competitive social media intelligence tool for **Jose Cuervo** tequila, built for **Poplife** agency. Multi-page Streamlit dashboard analyzing Instagram and TikTok performance across 8 tequila brands.

## Brands Tracked
Jose Cuervo, Patron, Don Julio, Casamigos, Espolon, Teremana, 1800 Tequila, 818 Tequila

## Architecture
```
app.py                 # Entry point — data loading, sidebar filters, session state
pages/
  1_Executive_Summary.py
  2_Brand_Comparison.py
  3_Content_Strategy.py
  4_Engagement_Deep_Dive.py
  5_Hashtag_&_Creator.py
  6_Data_Explorer.py
  7_Cuervo_Strategy.py  # Gen Z recommendations, 30-day action plan
  8_Audience_Intelligence.py   # Psychographic profiles, NOPD comparison, sentiment
  9_Conversation_&_Trends.py   # Hashtag/keyword analysis, content trends, archetypes
  10_Strategic_Playbook.py     # Consolidated winning territories, sponsorship playbook
  11_Profile_Deep_Dive.py      # Per-brand profile intelligence (IG & TikTok)
autostrat_parser.py    # PDF-to-JSON parser for autostrat.ai report exports
autostrat_loader.py    # JSON loader + cross-report extraction helpers
autostrat_components.py # Reusable UI components for narrative content
config.py              # Brand colors, BRAND_ORDER, CUSTOM_CSS (Poplife palette)
templates.py           # BRANDS list, content themes, visual styles, tone options
analysis.py            # Core analysis engine — run_full_analysis(data_dir)
sample_data.py         # Demo data generator with realistic brand profiles
sprout_import.py       # Sprout Social CSV import adapter + AI content classifiers
dashboard.py           # Excel report generator (download button)
data/sprout/           # Drop Sprout Social CSV exports here
data/autostrat/        # Parsed autostrat JSON reports (6 subdirectories)
data/autostrat/pdfs/   # Drop autostrat PDF exports here for import
```

## Data Sources (3 modes, selected in sidebar)
1. **Demo Data** — synthetic data from `sample_data.py` (BRAND_PROFILES based on real research but posts are fake)
2. **Sprout Social Import** — real data from CSV exports dropped into `data/sprout/`. Auto-detected when CSVs are present. The importer (`sprout_import.py`) maps Sprout column names, resolves brand handles, classifies content themes/tone/CTA from caption text, filters out Stories, and extracts follower counts from aggregate reports.
3. **Custom CSV Folder** — manually created CSVs matching the schema in `templates.py`

## Current Sprout Data (Jan 2026)
- Only Instagram data (no TikTok in exports yet)
- Don Julio and 1800 Tequila have profile data but 0 posts in Jan exports
- Stories are filtered out during import (ephemeral, no competitor parity)
- 818 Tequila (drink818 / Kendall Jenner) was in the Sprout tracking

## Key Technical Details
- `st.session_state` shares data across pages: `results`, `df`, `filtered_df`, `sel_brands`, `sel_platforms`
- `results` dict from `analysis.py` has keys: `posts`, `engagement`, `frequency`, `content`, `hashtags`, `creators`, `recommendations`
- Page 7 (Cuervo Strategy) uses unfiltered `st.session_state["df"]` — sidebar filters don't apply
- Brand colors and CSS match poplife99.com palette (peach #F8C090, blue #2ea3f2, dark #333333)
- `st.logo("logo.png")` and `st.markdown(CUSTOM_CSS)` must be called in every page file
- Emoji counting uses Unicode regex (no `+` quantifier — counts each emoji individually)
- Favicon is `favicon.png` (Poplife "P" icon)

## Sprout Social Import Details
- Column mapping handles variations: "Post" → caption, "Reactions" → likes, "Audience" → followers, "Link" → post URL
- Numbers with commas (e.g., "111,893") are parsed correctly
- Brand resolution: handle names like "josecuervotequila" → "Jose Cuervo", "drink818" → "818 Tequila"
- Content classifiers in `sprout_import.py`: `classify_theme()`, `classify_tone()`, `classify_cta()`, `classify_visual_style()`, `detect_creator_collab()`, `detect_paid_partnership()`
- Aggregate reports (Competitor Performance, Instagram Competitors) → profile/follower data
- Post-level reports (Competitor Posts, Post Performance) → individual posts

## Running
```bash
python3 -m streamlit run app.py
# Opens at http://localhost:8501
```

## Autostrat Intelligence (Pages 8-11)
- Qualitative reports from autostrat.ai — audience psychographics, competitive positioning, content trends, creator archetypes, strategic recommendations
- Reports are Google Slides exported as PDFs, parsed via `pdftotext` (poppler)
- `st.session_state["autostrat"]` stores `{report_type: {identifier: report_data}}`
- 6 report types: instagram_profiles, tiktok_profiles, instagram_hashtags, tiktok_hashtags, tiktok_keywords, google_news
- Parser detects report type from title line, splits on section headings, extracts structured fields
- NOPD framework: Needs (#2ea3f2), Objections (#D9534F), Desires (#5CB85C), Pain Points (#F8C090)
- PDF import: sidebar button triggers parser, outputs JSON to correct subdirectory
- Pages 8-11 gracefully handle missing data (show info messages, don't crash)
- Python 3.9.6 compatibility: `from __future__ import annotations` in parser

## Pending / Known Issues
- TikTok data not yet in Sprout exports — TikTok sections show zeros on Sprout import mode
- Don Julio and 1800 Tequila awaiting data population in Sprout
- Content theme classifier is keyword-based (~80-85% accuracy) — can be improved
- Consider hiding TikTok sections when no TikTok data is present
