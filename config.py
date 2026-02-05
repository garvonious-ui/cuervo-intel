"""
Configuration: brand colors, styling constants, custom CSS.
"""

BRAND_COLORS = {
    "Jose Cuervo": "#FFB300",
    "Patron": "#8D6E63",
    "Don Julio": "#1B3A5C",
    "Casamigos": "#388E3C",
    "Espolon": "#E64A19",
    "Teremana": "#6D4C41",
    "1800 Tequila": "#1565C0",
}

BRAND_ORDER = [
    "Jose Cuervo", "Patron", "Don Julio", "Casamigos",
    "Espolon", "Teremana", "1800 Tequila",
]

PLATFORM_COLORS = {
    "Instagram": "#C13584",
    "TikTok": "#EE1D52",
}

PRIORITY_COLORS = {
    "High": "#E53935",
    "Medium": "#FB8C00",
    "Low": "#43A047",
}

CHART_TEMPLATE = "plotly_white"
CHART_FONT = dict(family="Inter, Helvetica, Arial, sans-serif")

CUSTOM_CSS = """
<style>
    .block-container { padding-top: 1.5rem; }
    h1 { color: #1B2A4A; }
    [data-testid="stMetricValue"] { font-size: 1.8rem; font-weight: 700; }
    [data-testid="stMetricDelta"] { font-size: 0.9rem; }
    .stTabs [data-baseweb="tab"] { font-weight: 600; }
</style>
"""

PAGE_CONFIG = dict(
    page_title="Cuervo Social Intel",
    page_icon="\U0001F943",
    layout="wide",
    initial_sidebar_state="expanded",
)
