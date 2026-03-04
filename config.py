"""
Configuration: shared styling constants.
Palette matched to poplife99.com

Client-specific constants (brands, strategy, KPIs) live in clients/{client_id}/.
Use client_context.get_client() to access them.
"""

# Poplife palette (shared across clients)
POPLIFE_PEACH = "#F8C090"
POPLIFE_BLUE = "#2ea3f2"
POPLIFE_BG = "#F3EDE6"
POPLIFE_DARK = "#333333"
POPLIFE_WHITE = "#ffffff"

PRIORITY_COLORS = {
    "High": "#D9534F",
    "Medium": "#F8C090",
    "Low": "#8CBF8C",
}

CHART_TEMPLATE = "plotly_white"
CHART_FONT = dict(family="Barlow Condensed, Helvetica, Arial, sans-serif")
