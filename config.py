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
}

BRAND_ORDER = [
    "Jose Cuervo", "Patron", "Don Julio", "Casamigos",
    "Espolon", "Teremana", "1800 Tequila",
]

PLATFORM_COLORS = {
    "Instagram": "#D4956A",
    "TikTok": "#2ea3f2",
}

PRIORITY_COLORS = {
    "High": "#D9534F",
    "Medium": "#F8C090",
    "Low": "#8CBF8C",
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
</style>
"""

PAGE_CONFIG = dict(
    page_title="Poplife | Cuervo Social Intel",
    page_icon="favicon.png",
    layout="wide",
    initial_sidebar_state="expanded",
)
