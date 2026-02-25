"""
Configuration: brand colors, styling constants, custom CSS.
Palette matched to poplife99.com
"""

# Poplife palette
POPLIFE_PEACH = "#F8C090"
POPLIFE_BLUE = "#2ea3f2"
POPLIFE_BG = "#F3EDE6"
POPLIFE_DARK = "#333333"
POPLIFE_WHITE = "#ffffff"

BRAND_COLORS = {
    "Jose Cuervo": "#F8C090",   # Poplife peach — hero brand
    "Patron": "#2ea3f2",        # Poplife blue
    "Don Julio": "#7B6B63",     # Warm dark taupe
    "Casamigos": "#D4956A",     # Burnt peach
    "Espolon": "#A3C4D9",       # Muted sky blue
    "Teremana": "#C9A87E",      # Sandy tan
    "1800 Tequila": "#6B8FA3",  # Steel blue
    "818 Tequila": "#B88BBF",   # Soft purple
    "Lunazul": "#5B9BD5",       # Medium blue
    "Hornitos": "#E8A838",      # Amber gold
    "Cazadores": "#8B4513",     # Saddle brown
    "Milagro": "#50C878",       # Emerald green
    "El Jimador": "#CD5C5C",    # Indian red
}

BRAND_ORDER = [
    "Jose Cuervo", "Patron", "Don Julio", "Casamigos",
    "Espolon", "Teremana", "1800 Tequila", "818 Tequila",
    "Lunazul", "Hornitos", "Cazadores", "Milagro", "El Jimador",
]

# Reference / inspiration brands (non-tequila) — autostrat profiles only
# Keys are lowercase identifiers matching JSON filenames in data/autostrat/
REFERENCE_BRANDS = ["duolingo", "drinkpoppi", "chipotle", "dunkin"]

REFERENCE_BRAND_LABELS = {
    "duolingo": "Duolingo",
    "drinkpoppi": "Poppi (drinkpoppi)",
    "chipotle": "Chipotle",
    "dunkin": "Dunkin'",
}

PLATFORM_COLORS = {
    "Instagram": "#D4956A",
    "TikTok": "#2ea3f2",
}

# Brand hashtag identifiers → display names
# Keys are lowercase slugs matching JSON filenames in data/autostrat/
# Only identifiers listed here appear on the Brand Hashtags tab (Page 5 Tab 1)
BRAND_HASHTAGS = {
    "josecuervo": "#JoseCuervo",
    "cuervo": "#Cuervo",
    "jose_cuervo": "Jose Cuervo (keyword)",
    "cuervo_tequila": "cuervo tequila (keyword)",
    "cazadores": "#Cazadores",
    "hornitos": "#Hornitos",
    "lunazul": "#Lunazul",
    "milagrotequila": "#MilagroTequila",
    "eljimador": "#ElJimador",
    "teremanatequila": "#TeremanaTequila",
    "1800tequila": "#1800Tequila",
    "casamigos": "#Casamigos",
}

# Cuervo's own hashtag identifiers (subset of BRAND_HASHTAGS)
CUERVO_HASHTAG_IDS = {"josecuervo", "cuervo", "jose_cuervo", "cuervo_tequila"}

# Category / cultural hashtag identifiers → display names
# Only identifiers listed here appear on the Category & Cultural tab (Page 5 Tab 2)
CATEGORY_HASHTAGS = {
    "margaritatime": "#MargaritaTime",
}

PRIORITY_COLORS = {
    "High": "#D9534F",
    "Medium": "#F8C090",
    "Low": "#8CBF8C",
}

# ─── POPLIFE PLAYBOOK FRAMEWORKS (2026 Social Strategy) ──────────────
# Maps existing content_theme values to the 2 content pillars from the deck.

POPLIFE_PILLAR_MAP = {
    "Cuervo in Culture": [
        "Meme / Humor", "Creator Collab / UGC", "Cultural Moment / Holiday",
        "Events & Music", "Giveaway / Promo",
        "User Repost", "Sports Tie-in", "Lifestyle/Aspirational",
    ],
    "Tradicional, Made Social": [
        "Brand Heritage / Story", "Education & Recipes", "Behind the Scenes",
        "Product Showcase",
    ],
}
POPLIFE_PILLAR_TARGETS = {"Cuervo in Culture": 60, "Tradicional, Made Social": 40}
POPLIFE_PILLAR_COLORS = {
    "Cuervo in Culture": "#2ea3f2",          # Blue — culture/entertainment
    "Tradicional, Made Social": "#C9A87E",   # Sandy tan — heritage elevated
}
POPLIFE_PILLAR_DESCRIPTIONS = {
    "Cuervo in Culture": "Cultural moments, memes, reactive content, UGC — Especial + RTDs",
    "Tradicional, Made Social": "Heritage reimagined, bartender POV, distillery stories — Cuervo Tradicional",
}

# SKU strategy from the 2026 Social Strategy deck
SKU_STRATEGY = {
    "Especial": {"energy": "High energy, fun", "occasions": "Everyday mixing, margs"},
    "Tradicional": {"energy": "Elevated", "occasions": "Night out, gifting, sipping"},
    "RTD": {"energy": "Mid-high, daytime", "occasions": "BBQ, tailgate, concerts"},
}

# 4 Execution Engines that drive content creation across pillars
EXECUTION_ENGINES = {
    "Memes + Reactive Culture": "Fast, funny, internet-native. Real-time commentary, cultural remixing, POV humor, reaction formats.",
    "Creator-Led + UGC": "POV storytelling, diaries, lives, fan cams, giveaways. The Cuervo Crew — creators embedded in the brand.",
    "Event + Festival Trend Factory": "Capture moments for TikTok — not recap videos. Film with trend formats in mind BEFORE the event.",
    "Lifestyle Shoot Bank": "Evergreen assets: meme templates, product hero, seasonal fillers, cocktail how-tos, story backgrounds.",
}

# Creator archetypes — "The Cuervo Crew"
CREATOR_ARCHETYPES = {
    "The Party Starter": "Nightlife, going-out energy",
    "The Home Bartender": "Cocktail recipes (saves)",
    "The Lifestyle Bestie": "Fashion/lifestyle (aspirational)",
    "The Culture Commentator": "Pop culture, meme (shares)",
    "The Festival Friend": "Events, RTD occasions",
}

# Voice principles from the deck
VOICE_PRINCIPLES = [
    ("Talk like a friend, not a brand", "Warm, knowing, a little cheeky. Never corporate."),
    ("Be funny without forcing it", "Gen-Z can smell 'trying too hard' instantly."),
    ("Celebrate the moment, not the product", "Lead with what's happening. Cuervo enters as part of the scene."),
    ("Be confident, not cocky", "We invented tequila. That's earned confidence."),
    ("Move at the speed of culture", "Quick, sharp, human reactions. Not two weeks later."),
]

# 2026 Cultural Calendar
CULTURAL_CALENDAR = {
    "Q1": {"moments": "Super Bowl, Oscars, Grammys, Nat'l Margarita Day", "angle": "Game day serves, awards content, Valentine's cocktails"},
    "Q2": {"moments": "Cinco de Mayo, Coachella, Met Gala, NBA Finals", "angle": "Marg Season launch, festival content, summer drops"},
    "Q3": {"moments": "4th of July, Lollapalooza, Love Island, US Open", "angle": "Peak summer, RTD outdoor, reality TV tie-ins"},
    "Q4": {"moments": "Halloween, Day of the Dead, NFL, holiday hosting, NYE", "angle": "Holiday serves, cultural celebrations, game day"},
}

CONTENT_MIX_MAP = {
    "Entertain": ["Meme / Humor", "Events & Music", "Creator Collab / UGC"],
    "Educate": ["Education & Recipes", "Behind the Scenes", "Brand Heritage / Story"],
    "Connect": ["Lifestyle/Aspirational", "Cultural Moment / Holiday", "User Repost", "Sports Tie-in"],
    "Convince": ["Product Showcase", "Giveaway / Promo"],
}
CONTENT_MIX_TARGETS = {"Entertain": 50, "Educate": 30, "Connect": 10, "Convince": 10}
CONTENT_MIX_COLORS = {
    "Entertain": "#F8C090",  # Peach — fun/playful
    "Educate": "#2ea3f2",    # Blue — informative
    "Connect": "#66BB6A",    # Green — community
    "Convince": "#D9534F",   # Red — action/sales
}

# Platform cadence targets (posts per month) — 2026 Social Strategy deck
POPLIFE_CADENCE_TARGETS = {
    "Instagram": {"low": 12, "high": 16},   # 12-16/mo (curated, social-first)
    "TikTok": {"low": 12, "high": 20},      # 3-5x/week (reactive, entertainment)
}

# IG Format Mix targets from Platform Playbook slide
IG_FORMAT_MIX = {
    "Reels": {"pct": 50, "role": "Reach + discovery"},
    "Carousels": {"pct": 30, "role": "Engagement driver"},
    "Stories": {"pct": 15, "role": "Community + utility"},
    "Collabs/Lives": {"pct": 5, "role": "Creator amplification"},
}

# Platform roles at a glance
PLATFORM_ROLES = {
    "Instagram": {"role": "The Main Stage — curated, social-first", "priority": "Primary", "cadence": "12-16/mo"},
    "TikTok": {"role": "The Culture Lab — reactive, entertainment", "priority": "Primary", "cadence": "3-5x/week"},
    "Pinterest": {"role": "Inspiration Engine — recipes, discovery", "priority": "Secondary", "cadence": "10-12 pins/mo"},
    "Facebook": {"role": "Performance Amplifier — paid distribution", "priority": "Secondary", "cadence": "3 paid/mo"},
    "X / Threads": {"role": "The Listener — reactive community", "priority": "Secondary", "cadence": "Reactive"},
    "YouTube": {"role": "Deep Dive — education + Shorts", "priority": "Secondary", "cadence": "4-5/mo"},
}

# Content source mix targets (2026 Social Strategy deck — "The Content Engine")
CONTENT_SOURCE_MIX = {
    "Brand-Owned": 50,
    "Creator / Influencer Partnerships / UGC": 30,
    "Events": 20,
}

# Monthly ramp targets (March-June 2026)
MONTHLY_RAMP = {
    "March": {"creator_pct": "20%+", "er_target": "0.15%", "proactive_comments_wk": "15-20"},
    "April": {"creator_pct": "23%+", "er_target": "0.18%", "proactive_comments_wk": "20-25"},
    "May": {"creator_pct": "27%+", "er_target": "0.22%", "proactive_comments_wk": "25-30"},
    "June": {"creator_pct": "30%", "er_target": "0.25%", "proactive_comments_wk": "30+"},
}

# Testing roadmap (March-June 2026)
TESTING_ROADMAP = {
    "March": {"variable": "Creator carousel vs. creator Reel", "learning": "Which format drives higher ER?"},
    "April": {"variable": "Humor/meme vs. lifestyle content", "learning": "What entertainment style resonates?"},
    "May": {"variable": "Short caption vs. story-driven", "learning": "How much copy do people engage with?"},
    "June": {"variable": "Especial-led vs. RTD-led", "learning": "Which SKU drives more summer engagement?"},
}

# ─── SOCIAL BRIEF KPI TARGETS (2026) ─────────────────────────────────
# Centralized KPI targets for all scorecard comparisons across the dashboard.
# Updated from original brief based on actual performance data (Feb 2026).
# Note: POPLIFE_CADENCE_TARGETS above are monthly asset targets from the Playbook;
# the weekly posting targets below are Social Brief KPIs (may differ).

SOCIAL_BRIEF_TARGETS = {
    "er_by_followers": 0.25,              # ER by Followers target (current 0.11%, 2x stretch)
    "er_by_views": 2.0,                   # ER by Views target (category median ~1.78%, aiming above)
    "engagements_per_post": 200,        # Avg engagements per post target (current 122, ~1.6x stretch)
    "reel_ratio": 50,                   # Reel Ratio % on Instagram (Reels = 50% of feed)
    "carousel_ratio": 30,              # Carousel Ratio % on Instagram
    "ig_posts_per_month": (12, 16),    # IG posts/month range
    "tt_posts_per_week": (3, 5),       # TT posts/week range
    "save_rate": 5.0,                   # Save Rate % target (current 2.9%, ~1.7x stretch)
    "share_rate": 5.0,                  # Share Rate % target (current 5.9%, already beating)
    "creator_er": 2.0,                  # Creator content ER by views target (current 1.70%)
    "creator_pct_target_june": 30,     # Creator % of total by June 2026 (Content Engine: 50% brand / 30% creator / 20% events)
}

CHART_TEMPLATE = "plotly_white"
CHART_FONT = dict(family="Barlow Condensed, Helvetica, Arial, sans-serif")

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700&display=swap');

    .block-container { padding-top: 3rem; }

    /* Headings */
    h1, h2, h3 { color: #333333; font-family: 'Barlow Condensed', sans-serif; font-weight: 700; }

    /* Metrics */
    [data-testid="stMetricValue"] { font-size: 1.8rem; font-weight: 700; color: #333333; }
    [data-testid="stMetricDelta"] { font-size: 0.9rem; }

    /* Tabs */
    .stTabs [data-baseweb="tab"] { font-weight: 600; font-family: 'Barlow Condensed', sans-serif; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #333333;
    }
    [data-testid="stSidebar"] * {
        color: #F3EDE6 !important;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #F8C090 !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: #F8C090;
        color: #333333;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        font-family: 'Barlow Condensed', sans-serif;
    }
    .stButton > button:hover {
        background-color: #e6a96f;
        color: #333333;
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

    /* Sidebar inputs — darker than sidebar bg (#333333) */
    [data-testid="stSidebar"] [data-baseweb="select"],
    [data-testid="stSidebar"] [data-baseweb="input"] {
        background-color: #252525;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] div[class*="ValueContainer"],
    [data-testid="stSidebar"] [data-baseweb="select"] div[class*="control"],
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background-color: #252525 !important;
    }
    /* Tag/chip text and close button inside sidebar multiselects */
    [data-testid="stSidebar"] [data-baseweb="tag"] span,
    [data-testid="stSidebar"] [data-baseweb="tag"],
    [data-testid="stSidebar"] [data-baseweb="tag"] svg,
    [data-testid="stSidebar"] [data-baseweb="tag"] [role="presentation"] {
        color: #333333 !important;
        fill: #333333 !important;
    }

    /* Selectbox / multiselect on main area */
    .stSelectbox label, .stMultiSelect label { font-weight: 600; color: #333333; }

    /* Expander headers */
    .streamlit-expanderHeader { font-weight: 600; color: #333333; }

    /* Autostrat narrative content */
    blockquote { border-left: 4px solid #F8C090; padding: 10px 16px; margin: 8px 0;
                 background: #F3EDE6; border-radius: 0 8px 8px 0; }
</style>
"""

PAGE_CONFIG = dict(
    page_title="Poplife | Cuervo Social Intel",
    page_icon="favicon.png",
    layout="wide",
    initial_sidebar_state="expanded",
)
