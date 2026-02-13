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
CUERVO_HASHTAG_IDS = {"josecuervo", "cuervo"}

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

# ─── GOAT PLAYBOOK FRAMEWORKS (Q1 2026) ─────────────────────────────
# Maps existing content_theme values to GOAT Agency strategy frameworks.

GOAT_PILLAR_MAP = {
    "La Tradición": ["Brand Heritage / Story", "Education (Tequila 101)", "Behind the Scenes"],
    "Cuervo Live": ["Event / Activation", "Music / Party", "Sports Tie-in"],
    "Life, with a Lime": ["Lifestyle/Aspirational", "Cocktail Recipe", "Product Showcase"],
    "Culture, Shaken": ["Meme / Humor", "Creator Collab / UGC", "Cultural Moment / Holiday", "User Repost", "Giveaway / Promo"],
}
GOAT_PILLAR_TARGETS = {"La Tradición": 25, "Cuervo Live": 15, "Life, with a Lime": 30, "Culture, Shaken": 30}
GOAT_PILLAR_COLORS = {
    "La Tradición": "#C9A87E",     # Sandy tan — heritage
    "Cuervo Live": "#D4956A",      # Burnt peach — live events
    "Life, with a Lime": "#66BB6A", # Green — lifestyle
    "Culture, Shaken": "#2ea3f2",   # Blue — culture/trends
}

CONTENT_MIX_MAP = {
    "Entertain": ["Meme / Humor", "Music / Party", "Creator Collab / UGC"],
    "Educate": ["Education (Tequila 101)", "Behind the Scenes", "Cocktail Recipe", "Brand Heritage / Story"],
    "Connect": ["Lifestyle/Aspirational", "Cultural Moment / Holiday", "User Repost", "Sports Tie-in"],
    "Convince": ["Product Showcase", "Giveaway / Promo", "Event / Activation"],
}
CONTENT_MIX_TARGETS = {"Entertain": 50, "Educate": 30, "Connect": 10, "Convince": 10}
CONTENT_MIX_COLORS = {
    "Entertain": "#F8C090",  # Peach — fun/playful
    "Educate": "#2ea3f2",    # Blue — informative
    "Connect": "#66BB6A",    # Green — community
    "Convince": "#D9534F",   # Red — action/sales
}

# GOAT platform cadence targets (posts per month)
GOAT_CADENCE_TARGETS = {
    "Instagram": {"low": 8, "high": 10},   # 2-3x/week
    "TikTok": {"low": 12, "high": 16},     # 4-5x/week
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
