"""
Devils Reserve Client Configuration
======================================
Assembles all Devils Reserve-specific config into a ClientConfig instance.
"""

from clients._schema import ClientConfig
from config import POPLIFE_TREATMENT_C_CSS
from clients.devils_reserve.brands import (
    BRANDS, BRAND_ORDER, BRAND_COLORS, BRAND_MAP, FALLBACK_FOLLOWERS,
    REFERENCE_BRANDS, REFERENCE_BRAND_LABELS,
    BRAND_HASHTAGS, HERO_HASHTAG_IDS, CATEGORY_HASHTAGS,
    CREATOR_PROGRAM_SIGNALS,
    BRAND_PROFILES, HASHTAG_POOLS,
)
from clients.devils_reserve.strategy import (
    PILLAR_MAP, PILLAR_TARGETS, PILLAR_COLORS, PILLAR_DESCRIPTIONS,
    CONTENT_MIX_MAP, CONTENT_MIX_TARGETS, CONTENT_MIX_COLORS,
    KPI_TARGETS, CADENCE_TARGETS, IG_FORMAT_MIX, PLATFORM_ROLES,
    CONTENT_SOURCE_MIX, MONTHLY_RAMP, TESTING_ROADMAP,
    CULTURAL_CALENDAR, SKU_STRATEGY, EXECUTION_ENGINES,
    CREATOR_ARCHETYPES, VOICE_PRINCIPLES, GEN_Z_LEADERS,
)
from clients.devils_reserve.copy import (
    PAGE_HEADERS, PAGE_CAPTIONS, NAV_TABLE, NARRATIVE,
)

# ── Devils Reserve-specific client CSS (devil red accent, dark sidebar) ──
# All shared Treatment C styles come from POPLIFE_TREATMENT_C_CSS in config.py.
# This block only contains DR overrides (red buttons, dark sidebar theme).

_DR_CLIENT_CSS = """
<style>
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1a1a1a;
    }
    [data-testid="stSidebar"] * {
        color: #F3EDE6 !important;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #CC0000 !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: #CC0000;
        color: #ffffff;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        font-family: 'Barlow Condensed', sans-serif;
    }
    .stButton > button:hover {
        background-color: #990000;
        color: #ffffff;
    }

    /* Download button */
    .stDownloadButton > button {
        background-color: #2ea3f2;
        color: #ffffff;
        border: none;
        border-radius: 6px;
        font-weight: 600;
    }
    .stDownloadButton > button:hover {
        background-color: #1b8fd4;
    }

    /* Sidebar inputs */
    [data-testid="stSidebar"] [data-baseweb="select"],
    [data-testid="stSidebar"] [data-baseweb="input"] {
        background-color: #252525;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] div[class*="ValueContainer"],
    [data-testid="stSidebar"] [data-baseweb="select"] div[class*="control"],
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background-color: #252525 !important;
    }
    [data-testid="stSidebar"] [data-baseweb="tag"] span,
    [data-testid="stSidebar"] [data-baseweb="tag"],
    [data-testid="stSidebar"] [data-baseweb="tag"] svg,
    [data-testid="stSidebar"] [data-baseweb="tag"] [role="presentation"] {
        color: #1a1a1a !important;
        fill: #1a1a1a !important;
    }

    /* Selectbox / multiselect on main area */
    .stSelectbox label, .stMultiSelect label { font-weight: 600; color: #1a1a1a; }

    /* Expander headers */
    .streamlit-expanderHeader { font-weight: 600; color: #1a1a1a; }

    /* Autostrat narrative content */
    blockquote { border-left: 4px solid #CC0000; padding: 10px 16px; margin: 8px 0;
                 background: #FFF0F0; border-radius: 0 8px 8px 0; }
</style>
"""

# Concatenate shared Treatment C CSS + DR-specific overrides.
CUSTOM_CSS = POPLIFE_TREATMENT_C_CSS + _DR_CLIENT_CSS


def get_config() -> ClientConfig:
    """Return the complete Devils Reserve client configuration."""
    return ClientConfig(
        # Identity
        client_id="devils_reserve",
        client_name="Devils Reserve Social Intelligence",
        hero_brand="Devils Reserve",
        agency_name="Poplife",
        industry="tequila",
        themes_ready=True,  # Manual pillar tags imported from DR Themes CSV (2026-04-10)

        # Brands
        brands=BRANDS,
        brand_order=BRAND_ORDER,
        brand_colors=BRAND_COLORS,
        brand_map=BRAND_MAP,
        fallback_followers=FALLBACK_FOLLOWERS,

        # Reference brands
        reference_brands=REFERENCE_BRANDS,
        reference_brand_labels=REFERENCE_BRAND_LABELS,

        # Autostrat
        brand_hashtags=BRAND_HASHTAGS,
        hero_hashtag_ids=HERO_HASHTAG_IDS,
        category_hashtags=CATEGORY_HASHTAGS,
        hero_news_id="",

        # Strategy frameworks
        pillar_map=PILLAR_MAP,
        pillar_targets=PILLAR_TARGETS,
        pillar_colors=PILLAR_COLORS,
        pillar_descriptions=PILLAR_DESCRIPTIONS,
        content_mix_map=CONTENT_MIX_MAP,
        content_mix_targets=CONTENT_MIX_TARGETS,
        content_mix_colors=CONTENT_MIX_COLORS,
        kpi_targets=KPI_TARGETS,
        cadence_targets=CADENCE_TARGETS,
        ig_format_mix=IG_FORMAT_MIX,
        platform_roles=PLATFORM_ROLES,
        content_source_mix=CONTENT_SOURCE_MIX,
        monthly_ramp=MONTHLY_RAMP,
        testing_roadmap=TESTING_ROADMAP,
        cultural_calendar=CULTURAL_CALENDAR,
        sku_strategy=SKU_STRATEGY,
        execution_engines=EXECUTION_ENGINES,
        creator_archetypes=CREATOR_ARCHETYPES,
        voice_principles=VOICE_PRINCIPLES,
        gen_z_leaders=GEN_Z_LEADERS,

        # Sprout import
        creator_program_signals=CREATOR_PROGRAM_SIGNALS,

        # Demo data
        brand_profiles=BRAND_PROFILES,
        hashtag_pools=HASHTAG_POOLS,

        # Theming
        primary_color="#CC0000",
        background_color="#F3EDE6",
        dark_color="#1a1a1a",
        accent_color="#CC0000",
        custom_css=CUSTOM_CSS,

        # Assets (relative to clients/devils_reserve/assets/)
        # TODO: create custom Devils Reserve logo assets — currently using placeholder/defaults
        logo_path="logo.png",
        favicon_path="favicon.png",
        app_logo_path="app_logo.png",

        # Page copy
        page_title="Poplife | Devils Reserve Social Intel",
        home_title="Devils Reserve — Social Media Intelligence",
        home_subtitle_template="Competitive analysis across {n} brands on Instagram & TikTok",
        page_headers=PAGE_HEADERS,
        page_captions=PAGE_CAPTIONS,
        nav_table=NAV_TABLE,
        excel_filename="devils_reserve_intelligence_report.xlsx",
        highlight_fill_color="#FFE0E0",

        # Narrative
        narrative=NARRATIVE,
    )
