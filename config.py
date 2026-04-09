"""
Configuration: shared styling constants.
Palette matched to poplife99.com

Client-specific constants (brands, strategy, KPIs) live in clients/{client_id}/.
Use client_context.get_client() to access them.
"""

import plotly.graph_objects as go
import plotly.io as pio

# ── Poplife palette (shared across clients) ─────────────────────────
# Extracted from poplife99.com visual identity:
#   - Peach (primary accent) and warm off-white background match the site
#   - Teal/cyan is a secondary accent used on the site for UI details
#   - Dark charcoal for text, used as sidebar bg and hover tooltips
POPLIFE_PEACH = "#F8C090"
POPLIFE_TEAL = "#7EBEC5"
POPLIFE_BLUE = "#2ea3f2"
POPLIFE_BG = "#F3EDE6"
POPLIFE_DARK = "#333333"
POPLIFE_WHITE = "#ffffff"

# Warm-tinted grays (used for card borders, chart gridlines) that harmonize
# with the warm off-white background instead of looking cold next to it.
POPLIFE_BORDER = "#E0D8D0"
POPLIFE_GRID = "#EDE3D8"
POPLIFE_MUTED = "#8A817C"

PRIORITY_COLORS = {
    "High": "#D9534F",
    "Medium": "#F8C090",
    "Low": "#8CBF8C",
}

# ── Poplife Plotly chart template ────────────────────────────────────
# Registered as "poplife" template so any chart passing template=CHART_TEMPLATE
# automatically picks up the brand palette, typography, and hover styling.
# Charts can still override individual fields via fig.update_layout().
#
# Color sequence is used when a chart doesn't explicitly set colors (i.e.
# categorical charts without color_discrete_map). Charts that pass
# color_discrete_map=cfg.brand_colors — like the competitive comparisons on
# Page 2 — continue to use per-brand colors and are unaffected.

POPLIFE_CHART_COLORS = [
    POPLIFE_PEACH,      # #F8C090 — primary brand accent
    POPLIFE_TEAL,       # #7EBEC5 — secondary brand accent
    POPLIFE_BLUE,       # #2ea3f2 — tertiary accent
    "#8CBF8C",          # sage green (from PRIORITY_COLORS.Low)
    "#A88FBF",          # muted lavender
    "#E6A96F",          # darker peach (button hover color)
    "#5C9DBE",          # muted blue
    "#D9886B",          # terracotta
    "#B8C9A8",          # sage muted
    "#C9A88F",          # warm tan
]

_CHART_FONT_FAMILY = "Barlow Condensed, Helvetica, Arial, sans-serif"

pio.templates["poplife"] = go.layout.Template(
    layout=go.Layout(
        font=dict(
            family=_CHART_FONT_FAMILY,
            color=POPLIFE_DARK,
            size=13,
        ),
        title=dict(
            font=dict(family=_CHART_FONT_FAMILY, size=18, color=POPLIFE_DARK),
            x=0,
            xanchor="left",
            pad=dict(b=12),
        ),
        paper_bgcolor=POPLIFE_WHITE,
        plot_bgcolor=POPLIFE_WHITE,
        colorway=POPLIFE_CHART_COLORS,
        xaxis=dict(
            gridcolor=POPLIFE_GRID,
            linecolor=POPLIFE_BORDER,
            tickfont=dict(family=_CHART_FONT_FAMILY, size=12, color=POPLIFE_MUTED),
            title=dict(font=dict(family=_CHART_FONT_FAMILY, size=13, color=POPLIFE_MUTED)),
            zerolinecolor=POPLIFE_BORDER,
        ),
        yaxis=dict(
            gridcolor=POPLIFE_GRID,
            linecolor=POPLIFE_BORDER,
            tickfont=dict(family=_CHART_FONT_FAMILY, size=12, color=POPLIFE_MUTED),
            title=dict(font=dict(family=_CHART_FONT_FAMILY, size=13, color=POPLIFE_MUTED)),
            zerolinecolor=POPLIFE_BORDER,
        ),
        legend=dict(
            font=dict(family=_CHART_FONT_FAMILY, size=12, color=POPLIFE_DARK),
            bgcolor="rgba(255,255,255,0.85)",
            bordercolor=POPLIFE_BORDER,
            borderwidth=1,
        ),
        hoverlabel=dict(
            bgcolor=POPLIFE_DARK,
            bordercolor=POPLIFE_PEACH,
            font=dict(family=_CHART_FONT_FAMILY, size=13, color=POPLIFE_WHITE),
        ),
        margin=dict(l=48, r=24, t=48, b=48),
        hovermode="closest",
    )
)

CHART_TEMPLATE = "poplife"
CHART_FONT = dict(family=_CHART_FONT_FAMILY)

# ── Collaboration type classification ──
# Owned = the hero brand's own organic content (posts authored solely by the
# brand account; untagged rows default here).
# Amplified = any post whose reach is NOT purely the hero brand's own audience.
# Partner, Collective, and Influencer all get amplification from another
# account's following (co-authored IG Collab Posts, creator reposts, event
# activations, etc.) and are excluded from hero KPI averages so the scorecard
# reflects organic brand content performance.
COLLAB_OWNED_TYPES = {"cuervo"}
COLLAB_AMPLIFIED_TYPES = {"partner", "influencer", "collective"}


def split_owned_collab(df):
    """Split a DataFrame into owned and collab subsets based on collaboration column.

    Owned = hero brand's own organic posts (tagged "Cuervo" or untagged).
    Collab = Partner + Influencer + Collective — any post whose reach is
             amplified by another account's audience.
    Returns (owned_df, collab_df). If no collaboration column, returns (df, empty_df).
    """
    if "collaboration" not in df.columns:
        return df, df.iloc[0:0]
    collab_lower = df["collaboration"].str.strip().str.lower()
    owned = df[collab_lower.isin(COLLAB_OWNED_TYPES) | collab_lower.isna()]
    collab = df[collab_lower.isin(COLLAB_AMPLIFIED_TYPES)]
    return owned, collab
