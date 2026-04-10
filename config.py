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


# ════════════════════════════════════════════════════════════════════════
# Treatment C CSS — shared across all clients
# ════════════════════════════════════════════════════════════════════════
# Dark editorial hero block + light KPI/content cards + peach accents.
# Both clients include this via `CUSTOM_CSS = POPLIFE_TREATMENT_C_CSS + CLIENT_CSS`.
# See docs/ui-phase-1-handoff.md for design rationale.
#
# Classes provided:
#   Layout:        .page-hero .section-label .content-card .tab-row .tab-btn
#                  .row-2col .row-3col .row-4col
#   KPI scorecard: .kpi-grid .kpi-card .meta-chip .status-pill
#   Callouts:      .poplife-note (+ .success .danger .warning)
#                  .north-star .connect-callout
#   Page 3:        .pillar-card-detail .sku-card .engine-card .voice-card
#                  .cpn-layout .cpn-summary-dark .cpn-cadence .source-mix-bar
#                  .ig-format-card .week-expander .quarter-card .partner-event
#                  .swot-grid .swot-card
#   Page 4:        .ref-brand-picker .ref-platform-radio .ref-pill
#                  .filter-bar .filter-chip .slider-group .search-input
#   Page 4/5:      .nopd-2x2 .nopd-card .territory-card
#                  .brand-mention .sentiment-badge .sentiment-grid .sentiment-cell
#   Page 5:        .insight-expander .wtm-card .news-narrative .news-quote

POPLIFE_TREATMENT_C_CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@300;400;500;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
    .block-container { padding-top: 2rem; }

    /* ══════════════════════════════════════════════════════════════════
       Global font cascade — make Barlow Condensed the default for every
       Streamlit widget, then individual component rules override where
       Inter is preferred (hero subtitle, content-card tables, callouts).
       Without this, native widgets (st.metric, st.dataframe, st.markdown,
       st.button, st.selectbox, sidebar nav, expanders) fall back to
       Streamlit's bundled font.
       ══════════════════════════════════════════════════════════════════ */
    html, body, .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stHeader"],
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] *,
    [data-testid="stSidebarNav"],
    [data-testid="stSidebarNavLink"],
    [data-testid="stSidebarNavLink"] span,
    [data-testid="stMetricValue"],
    [data-testid="stMetricLabel"],
    [data-testid="stMetricDelta"],
    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] td,
    [data-testid="stMarkdownContainer"] th,
    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] p,
    [data-testid="stDataFrame"],
    [data-testid="stDataFrame"] *,
    [data-testid="stTable"],
    [data-testid="stTable"] *,
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary *,
    [data-testid="stNotificationContentInfo"],
    [data-testid="stNotificationContentWarning"],
    [data-testid="stNotificationContentError"],
    [data-testid="stNotificationContentSuccess"],
    .stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown td, .stMarkdown th,
    .stCaption,
    .stButton button, .stDownloadButton button, .stFormSubmitButton button,
    .stSelectbox label, .stSelectbox [data-baseweb="select"],
    .stSelectbox [data-baseweb="select"] *,
    .stMultiSelect label, .stMultiSelect [data-baseweb="select"] *,
    .stTextInput label, .stTextInput input,
    .stTextArea label, .stTextArea textarea,
    .stRadio label, .stRadio [data-baseweb="radio"],
    .stCheckbox label,
    .stSlider label,
    .stDateInput label, .stDateInput input,
    .stNumberInput label, .stNumberInput input {
        font-family: 'Barlow Condensed', Helvetica, Arial, sans-serif !important;
    }

    /* Base headings */
    h1, h2, h3, h4, h5, h6 { color: #333333; font-family: 'Barlow Condensed', sans-serif; font-weight: 700; }

    /* ══════════════════════════════════════════════════════════════════
       Streamlit icon font preservation
       ══════════════════════════════════════════════════════════════════
       Streamlit uses Material Symbols Rounded ligatures for native icons
       (sidebar collapse arrow, expander chevron, button icons, etc.).
       Setting `font = "Barlow Condensed"` in .streamlit/config.toml
       cascades that font down to icon spans too, breaking the ligature
       transformation — so users see the literal icon name as text
       (e.g. "keyboard_double_arrow_left", "arrow_drop_down").
       Force Material Symbols back onto the icon elements explicitly.
       ══════════════════════════════════════════════════════════════════ */
    [data-testid="stIconMaterial"],
    span[data-testid="stIconMaterial"],
    .material-icons,
    .material-symbols-rounded,
    .material-symbols-outlined {
        font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons' !important;
        font-weight: normal !important;
        font-style: normal !important;
        font-feature-settings: 'liga' !important;
        -webkit-font-feature-settings: 'liga' !important;
    }

    /* Restyled Streamlit tabs to match Treatment C tab row */
    .stTabs [data-baseweb="tab-list"] {
        border-bottom: 1px solid #E0D8D0;
        gap: 0;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Barlow Condensed', sans-serif !important;
        font-size: 1rem;
        font-weight: 600;
        color: #8A817C;
        padding: 14px 22px 13px 22px;
        border-bottom: 3px solid transparent !important;
    }
    .stTabs [data-baseweb="tab"]:hover { color: #1A1A1A; }
    .stTabs [aria-selected="true"] {
        color: #1A1A1A !important;
        border-bottom-color: #F8C090 !important;
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none; }

    /* ══════════════════════════════════════════════════════════════════
       Page hero — DARK editorial block
       ══════════════════════════════════════════════════════════════════ */
    .page-hero {
        background: #1A1A1A;
        color: #ffffff;
        border-radius: 16px;
        padding: 48px 40px 44px 40px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    .page-hero::before {
        content: ''; position: absolute; top: 0; left: 0;
        width: 120px; height: 3px; background: #F8C090;
    }
    .page-hero::after {
        content: ''; position: absolute;
        right: -80px; bottom: -80px;
        width: 240px; height: 240px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(248,192,144,0.08) 0%, transparent 70%);
        pointer-events: none;
    }
    .page-hero .kicker {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.78rem; font-weight: 600;
        text-transform: uppercase; letter-spacing: 0.18em;
        color: #F8C090; margin-bottom: 16px;
        position: relative;
    }
    .page-hero h1 {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 4rem; font-weight: 800;
        text-transform: uppercase; letter-spacing: -0.015em;
        line-height: 0.92; color: #ffffff; margin: 0 0 18px 0;
        position: relative;
    }
    .page-hero .subtitle {
        font-family: 'Inter', -apple-system, system-ui, sans-serif;
        font-size: 1rem; color: rgba(255,255,255,0.7);
        max-width: 620px; line-height: 1.5;
        position: relative; margin: 0;
    }
    .page-hero .inline-stats {
        display: flex; gap: 56px; margin-top: 36px;
        padding-top: 28px; border-top: 1px solid rgba(255,255,255,0.12);
        position: relative; flex-wrap: wrap;
    }
    .page-hero .inline-stat .value {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 2rem; font-weight: 700; color: #ffffff; line-height: 1;
    }
    .page-hero .inline-stat .label {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.12em;
        color: rgba(255,255,255,0.55); margin-top: 6px;
    }

    /* ══════════════════════════════════════════════════════════════════
       Section label
       ══════════════════════════════════════════════════════════════════ */
    .section-label {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.82rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.18em;
        color: #1A1A1A; margin: 28px 0 14px 0;
        display: flex; align-items: center; gap: 14px;
    }
    .section-label:first-child { margin-top: 4px; }
    .section-label::before {
        content: ''; width: 24px; height: 2px; background: #F8C090;
        flex-shrink: 0;
    }
    .section-label::after { content: ''; flex: 1; height: 1px; background: #E0D8D0; }

    /* ══════════════════════════════════════════════════════════════════
       Content card (wraps tables, sections, chart blocks)
       ══════════════════════════════════════════════════════════════════ */
    .content-card {
        background: #ffffff;
        border: 1px solid #E0D8D0;
        border-radius: 12px;
        padding: 24px 24px 20px 24px;
        margin-bottom: 14px;
    }
    .content-card.tight { padding: 18px 20px 14px 20px; }
    .content-card h3 {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 1.3rem; font-weight: 700;
        margin: 0 0 6px 0; color: #1A1A1A;
        text-transform: none;
    }
    .content-card .card-caption {
        font-size: 0.85rem; color: #8A817C; margin-bottom: 16px;
    }
    .content-card table {
        width: 100%; border-collapse: collapse;
        font-family: 'Inter', system-ui, sans-serif;
        font-size: 0.86rem;
    }
    .content-card table th {
        text-align: left;
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.7rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.08em;
        color: #8A817C;
        padding: 10px 10px;
        border-bottom: 1px solid #E0D8D0;
    }
    .content-card table td {
        padding: 10px 10px;
        border-bottom: 1px solid #F3EDE6;
        color: #333;
    }
    .content-card table tr:last-child td { border-bottom: none; }
    .content-card table td.num { text-align: right; font-variant-numeric: tabular-nums; }
    .content-card table th.num { text-align: right; }
    .content-card table th.ctr, .content-card table td.ctr { text-align: center; }
    .content-card table tr.hero-row { background: rgba(248,192,144,0.16); }
    .content-card table tr.hero-row td:first-child { font-weight: 700; color: #1A1A1A; }
    .content-card table td.hot { background: rgba(92,184,92,0.10); color: #3a8f3a; font-weight: 600; }
    .content-card table td.low { background: rgba(217,83,79,0.08); color: #a83e3a; font-weight: 600; }
    .content-card table td.warn { background: rgba(240,173,78,0.10); color: #b07020; font-weight: 600; }

    /* Row layouts (for side-by-side content inside Streamlit columns) */
    .row-2col { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 14px; }
    .row-3col { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px; margin-bottom: 14px; }
    .row-4col { display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 14px; margin-bottom: 14px; }

    /* ══════════════════════════════════════════════════════════════════
       Poplife note (styled info box) + semantic variants
       ══════════════════════════════════════════════════════════════════ */
    .poplife-note {
        background: rgba(248,192,144,0.12);
        border-left: 3px solid #F8C090;
        border-radius: 0 8px 8px 0;
        padding: 14px 18px;
        margin: 14px 0;
        font-family: 'Inter', system-ui, sans-serif;
        font-size: 0.92rem;
        color: #333333; line-height: 1.55;
    }
    .poplife-note strong { color: #1A1A1A; }
    .poplife-note.success { background: rgba(92,184,92,0.10); border-left-color: #5CB85C; }
    .poplife-note.success strong { color: #2d6a2d; }
    .poplife-note.danger  { background: rgba(217,83,79,0.10); border-left-color: #D9534F; }
    .poplife-note.danger strong { color: #8a332f; }
    .poplife-note.warning { background: rgba(240,173,78,0.12); border-left-color: #F0AD4E; }

    /* ══════════════════════════════════════════════════════════════════
       North Star callout (Page 3)
       ══════════════════════════════════════════════════════════════════ */
    .north-star {
        background: #1A1A1A; color: #ffffff;
        border-radius: 12px;
        padding: 30px 32px 28px 32px;
        margin: 4px 0 22px 0;
        position: relative; overflow: hidden;
    }
    .north-star::before {
        content: ''; position: absolute; top: 0; left: 0;
        width: 80px; height: 2px; background: #F8C090;
    }
    .north-star .ns-label {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.72rem; font-weight: 600;
        text-transform: uppercase; letter-spacing: 0.18em;
        color: #F8C090; margin-bottom: 10px;
    }
    .north-star .ns-title {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 2.1rem; font-weight: 800;
        text-transform: uppercase; letter-spacing: -0.005em;
        line-height: 1.0; color: #F8C090; margin-bottom: 14px;
    }
    .north-star .ns-tagline {
        font-family: 'Inter', system-ui, sans-serif;
        font-size: 1rem; font-weight: 600;
        color: #ffffff; margin-bottom: 10px;
    }
    .north-star .ns-body {
        font-family: 'Inter', system-ui, sans-serif;
        font-size: 0.9rem; color: rgba(255,255,255,0.72);
        line-height: 1.55; max-width: 720px;
    }

    /* ══════════════════════════════════════════════════════════════════
       KPI grid + KPI card
       ══════════════════════════════════════════════════════════════════ */
    .kpi-grid { display: grid; gap: 14px; grid-template-columns: repeat(5, 1fr); }
    .kpi-grid.four  { grid-template-columns: repeat(4, 1fr); }
    .kpi-grid.three { grid-template-columns: repeat(3, 1fr); }
    .kpi-grid.two   { grid-template-columns: repeat(2, 1fr); }
    .kpi-card {
        background: #ffffff;
        border: 1px solid #E0D8D0;
        border-radius: 12px;
        padding: 24px 22px 20px 22px;
        transition: all 0.2s ease;
        position: relative;
        overflow: hidden;
        width: 100%;
    }
    .kpi-card:hover {
        border-color: #F8C090;
        box-shadow: 0 4px 16px rgba(248,192,144,0.18);
        transform: translateY(-1px);
    }
    .kpi-card .label {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.72rem; font-weight: 600;
        text-transform: uppercase; letter-spacing: 0.12em;
        color: #8A817C; margin-bottom: 14px;
    }
    .kpi-card .value {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 2.5rem; font-weight: 800;
        color: #333333; line-height: 0.95;
        letter-spacing: -0.01em;
    }
    .kpi-card .sub { font-size: 0.78rem; color: #8A817C; margin-top: 6px; }
    .kpi-card .pill-row {
        margin-top: 14px;
        display: flex; align-items: center; gap: 8px;
        min-height: 28px;
    }
    .kpi-card.hero {
        padding: 32px 30px 26px 30px;
        border-top: 3px solid #F8C090;
    }
    .kpi-card.hero .label { font-size: 0.8rem; margin-bottom: 18px; }
    .kpi-card.hero .value { font-size: 4rem; }
    .kpi-card.small .value { font-size: 1.8rem; }
    .kpi-card.small { padding: 18px 18px 14px 18px; }
    .kpi-card.small .label { font-size: 0.66rem; margin-bottom: 10px; }

    /* Status pill (used inside KPI cards) */
    .status-pill {
        display: inline-flex; align-items: center; gap: 6px;
        padding: 4px 10px;
        border-radius: 999px;
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.82rem; font-weight: 700;
        letter-spacing: 0.02em;
    }
    .status-pill.success { background: rgba(92,184,92,0.12); color: #3a8f3a; }
    .status-pill.danger  { background: rgba(217,83,79,0.12); color: #a83e3a; }
    .status-pill.neutral { background: rgba(138,129,124,0.12); color: #8A817C; }
    .status-pill .arrow  { font-size: 0.72rem; line-height: 1; }
    .status-pill .target { color: #8A817C; font-weight: 500; margin-left: 2px; }
    .meta-chip {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 999px;
        background: rgba(138,129,124,0.1);
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.78rem; color: #8A817C;
    }

    /* ══════════════════════════════════════════════════════════════════
       Page 3: Pillar card (with data)
       ══════════════════════════════════════════════════════════════════ */
    .pillar-card-detail {
        background: #ffffff;
        border: 1px solid #E0D8D0;
        border-left: 5px solid var(--accent-color, #F8C090);
        border-radius: 10px;
        padding: 18px 20px 14px 20px;
        margin-bottom: 14px;
    }
    .pillar-card-detail .pillar-name {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 1.2rem; font-weight: 800;
        text-transform: uppercase; letter-spacing: -0.005em;
        color: #1A1A1A; margin-bottom: 2px;
    }
    .pillar-card-detail .pillar-pct-row {
        display: flex; align-items: center; gap: 10px; margin: 6px 0 10px 0;
    }
    .pillar-card-detail .pct-badge {
        background: #1A1A1A; color: #F8C090;
        padding: 3px 10px; border-radius: 999px;
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.8rem; font-weight: 700;
    }
    .pillar-card-detail .pct-target {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.75rem; color: #8A817C;
        text-transform: uppercase; letter-spacing: 0.08em;
    }
    .pillar-card-detail .pillar-desc {
        font-size: 0.84rem; color: #555; line-height: 1.5; margin-bottom: 10px;
    }
    .pillar-card-detail .pillar-stats {
        display: flex; gap: 16px; flex-wrap: wrap;
        padding-top: 10px; border-top: 1px solid #F3EDE6;
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.78rem;
    }
    .pillar-card-detail .pillar-stats span { color: #8A817C; }
    .pillar-card-detail .pillar-stats strong { color: #1A1A1A; }
    .pillar-card-detail .gap-up   { color: #3a8f3a; font-weight: 700; }
    .pillar-card-detail .gap-down { color: #a83e3a; font-weight: 700; }

    /* SKU card */
    .sku-card {
        background: #ffffff; border: 1px solid #E0D8D0;
        border-top: 4px solid #F8C090;
        border-radius: 10px;
        padding: 18px 20px 16px 20px;
    }
    .sku-card h4 {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 1.15rem; font-weight: 800;
        text-transform: uppercase;
        color: #1A1A1A; margin-bottom: 6px;
    }
    .sku-card .sku-energy {
        font-size: 0.8rem; color: #8A817C;
        font-style: italic; margin-bottom: 10px;
    }
    .sku-card .sku-occasions {
        font-size: 0.85rem; color: #444; line-height: 1.5;
    }

    /* Execution engine card */
    .engine-card {
        background: #ffffff; border: 1px solid #E0D8D0;
        border-top: 4px solid #2ea3f2;
        border-radius: 10px;
        padding: 18px 20px 14px 20px;
        min-height: 130px;
    }
    .engine-card h4 {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 1.05rem; font-weight: 800;
        text-transform: uppercase;
        color: #1A1A1A; margin-bottom: 6px;
    }
    .engine-card p { font-size: 0.84rem; color: #555; line-height: 1.5; }

    /* Voice card */
    .voice-card {
        background: #ffffff; border: 1px solid #E0D8D0;
        border-left: 4px solid #F8C090;
        border-radius: 0 8px 8px 0;
        padding: 14px 18px;
        margin-bottom: 10px;
    }
    .voice-card .voice-name {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.95rem; font-weight: 700;
        color: #1A1A1A; margin-bottom: 4px;
    }
    .voice-card .voice-detail { font-size: 0.86rem; color: #555; line-height: 1.5; }

    /* Content Production Needs layout */
    .cpn-layout { display: grid; grid-template-columns: 3fr 2fr; gap: 14px; margin-bottom: 14px; }
    .cpn-summary-dark {
        background: #1A1A1A; color: #ffffff;
        border-radius: 12px;
        padding: 22px 24px 20px 24px;
        position: relative; overflow: hidden;
    }
    .cpn-summary-dark::before {
        content: ''; position: absolute; top: 0; left: 0;
        width: 60px; height: 2px; background: #F8C090;
    }
    .cpn-summary-dark .cpn-label {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.72rem; font-weight: 600;
        text-transform: uppercase; letter-spacing: 0.18em;
        color: #F8C090; margin-bottom: 8px;
    }
    .cpn-summary-dark .cpn-big {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 2.4rem; font-weight: 800;
        color: #ffffff; line-height: 1; letter-spacing: -0.01em;
    }
    .cpn-summary-dark .cpn-sub {
        font-family: 'Inter', system-ui, sans-serif;
        font-size: 0.82rem; color: rgba(255,255,255,0.6);
        margin: 6px 0 16px 0;
    }
    .cpn-summary-dark hr {
        border: none; height: 1px;
        background: rgba(248,192,144,0.3);
        margin: 6px 0 10px 0;
    }
    .cpn-summary-dark .cpn-annual-label {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.7rem; color: #F8C090;
        text-transform: uppercase; letter-spacing: 0.12em;
        margin-bottom: 4px;
    }
    .cpn-summary-dark .cpn-annual-value {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 1.2rem; font-weight: 800; color: #ffffff;
    }
    .cpn-cadence {
        background: #ffffff; border: 1px solid #E0D8D0;
        border-radius: 12px;
        padding: 18px 20px 14px 20px;
        margin-top: 10px;
    }
    .cpn-cadence .cpn-cadence-label {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.72rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.14em;
        color: #8A817C; margin-bottom: 12px;
    }
    .cpn-cadence table { width: 100%; }
    .cpn-cadence table td {
        padding: 6px 0; font-size: 0.88rem;
        border-bottom: 1px solid #F3EDE6;
    }
    .cpn-cadence table tr:last-child td { border-bottom: none; }
    .cpn-cadence table td:last-child {
        text-align: right;
        font-family: 'Barlow Condensed', sans-serif;
        font-weight: 700; color: #1A1A1A;
    }

    /* Source mix bar */
    .source-mix-bar {
        display: flex; border-radius: 6px; overflow: hidden;
        margin-top: 10px; height: 32px;
        border: 1px solid #E0D8D0;
    }
    .source-mix-bar .seg {
        display: flex; align-items: center; justify-content: center;
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.74rem; font-weight: 700;
        padding: 0 6px;
    }
    .source-mix-bar .seg.brand      { background: #1A1A1A; color: #F8C090; }
    .source-mix-bar .seg.influencer { background: #F8C090; color: #1A1A1A; }
    .source-mix-bar .seg.collective { background: #8B7355; color: #ffffff; }
    .source-mix-bar .seg.partner    { background: #C9A87E; color: #1A1A1A; }
    .source-mix-label {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.72rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.12em;
        color: #8A817C; margin: 14px 0 4px 0;
    }
    .sku-split-note { font-size: 0.78rem; color: #8A817C; margin-top: 6px; }

    /* Week expander (30-day plan) */
    .week-expander {
        background: #ffffff; border: 1px solid #E0D8D0;
        border-radius: 10px; margin-bottom: 8px;
        overflow: hidden;
    }
    .week-expander:hover { border-color: #F8C090; }
    .week-expander summary {
        padding: 14px 20px;
        cursor: pointer; list-style: none;
        display: flex; justify-content: space-between; align-items: center;
        border-left: 3px solid #F8C090;
    }
    .week-expander summary::-webkit-details-marker { display: none; }
    .week-expander summary::after {
        content: '+'; color: #F8C090;
        font-size: 1.3rem; font-weight: 300;
    }
    .week-expander[open] summary::after { content: '−'; }
    .week-expander .week-title {
        font-family: 'Barlow Condensed', sans-serif;
        font-weight: 700; color: #1A1A1A; font-size: 1rem;
    }
    .week-expander .week-title span {
        color: #F8C090; font-weight: 800; margin-right: 8px;
    }
    .week-expander .week-body {
        padding: 6px 20px 16px 26px;
        border-top: 1px solid #F3EDE6;
    }
    .week-expander .week-body ul {
        margin: 10px 0 0 16px;
        font-size: 0.88rem; color: #444; line-height: 1.55;
    }
    .week-expander .week-body li { margin-bottom: 4px; }

    /* Quarterly calendar card */
    .quarter-card {
        background: #ffffff; border: 1px solid #E0D8D0;
        border-top: 4px solid #2ea3f2;
        border-radius: 10px;
        padding: 16px 18px 14px 18px;
        min-height: 140px;
    }
    .quarter-card.q1 { border-top-color: #2ea3f2; }
    .quarter-card.q2 { border-top-color: #F8C090; }
    .quarter-card.q3 { border-top-color: #66BB6A; }
    .quarter-card.q4 { border-top-color: #C9A87E; }
    .quarter-card h4 {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 1.2rem; font-weight: 800;
        color: #1A1A1A; margin-bottom: 4px;
    }
    .quarter-card .q-moments {
        font-size: 0.82rem; font-weight: 600; color: #333; margin-bottom: 6px;
    }
    .quarter-card .q-angle { font-size: 0.78rem; color: #8A817C; line-height: 1.45; }

    /* Partner event card */
    .partner-event {
        background: #ffffff; border: 1px solid #E0D8D0;
        border-left: 4px solid #D9534F;
        border-radius: 0 10px 10px 0;
        padding: 16px 20px 14px 20px;
        min-height: 120px;
    }
    .partner-event h4 {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 1.1rem; font-weight: 800;
        color: #1A1A1A; margin-bottom: 8px;
    }
    .partner-event h4 .emoji { font-size: 1.3rem; margin-right: 6px; }
    .partner-event p { font-size: 0.86rem; color: #555; line-height: 1.5; }

    /* SWOT 2x2 */
    .swot-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
    .swot-card {
        background: #ffffff; border: 1px solid #E0D8D0;
        border-radius: 10px;
        padding: 16px 18px 14px 18px;
    }
    .swot-card.strength    { border-top: 3px solid #5CB85C; }
    .swot-card.weakness    { border-top: 3px solid #F0AD4E; }
    .swot-card.opportunity { border-top: 3px solid #2ea3f2; }
    .swot-card.threat      { border-top: 3px solid #D9534F; }
    .swot-card .swot-label {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.7rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.14em;
        color: #8A817C; margin-bottom: 10px;
    }
    .swot-card ul {
        margin-left: 16px; font-size: 0.84rem;
        color: #444; line-height: 1.55;
    }
    .swot-card li { margin-bottom: 4px; }

    /* NOPD 2x2 (Page 4/5) */
    .nopd-2x2 {
        display: grid; grid-template-columns: 1fr 1fr;
        gap: 12px; margin-bottom: 10px;
    }
    .nopd-card {
        background: #ffffff; border: 1px solid #E0D8D0;
        border-left: 4px solid #ccc;
        border-radius: 0 10px 10px 0;
        padding: 14px 18px 10px 18px;
    }
    .nopd-card.needs      { border-left-color: #2ea3f2; }
    .nopd-card.desires    { border-left-color: #5CB85C; }
    .nopd-card.objections { border-left-color: #D9534F; }
    .nopd-card.pain       { border-left-color: #F8C090; }
    .nopd-card h4 {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.75rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.14em;
        color: #1A1A1A; margin-bottom: 8px;
    }
    .nopd-card ul {
        margin-left: 16px; font-size: 0.82rem;
        color: #444; line-height: 1.5;
    }
    .nopd-card li { margin-bottom: 3px; }

    /* Territory card (numbered) */
    .territory-card {
        background: linear-gradient(135deg, #FDEBD6 0%, #FFF8F0 100%);
        border: 1px solid #E0D8D0;
        border-radius: 10px;
        padding: 14px 18px 12px 18px;
        margin-bottom: 8px;
        display: flex; gap: 14px;
    }
    .territory-card .num-circle {
        width: 32px; height: 32px;
        border-radius: 50%;
        background: #2ea3f2; color: #ffffff;
        display: flex; align-items: center; justify-content: center;
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 1rem; font-weight: 800;
        flex-shrink: 0;
    }
    .territory-card .t-body { flex: 1; }
    .territory-card .t-title {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.96rem; font-weight: 700;
        color: #1A1A1A; margin-bottom: 4px;
    }
    .territory-card .t-text { font-size: 0.84rem; color: #555; line-height: 1.5; }

    /* Verbatim pull-quote card (audience verbatims) */
    .verbatim-card {
        background: #F3EDE6;
        border: 1px solid #E0D8D0;
        border-left: 4px solid #F8C090;
        border-radius: 8px;
        padding: 12px 18px;
        margin: 8px 0;
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 1.02rem;
        font-style: italic;
        color: #444;
        line-height: 1.55;
        word-break: break-word;
        overflow-wrap: break-word;
    }

    /* Brand mention card */
    .brand-mention {
        background: #ffffff; border: 1px solid #E0D8D0;
        border-radius: 10px;
        padding: 14px 18px 12px 18px;
        margin-bottom: 8px;
    }
    .brand-mention .bm-head {
        display: flex; align-items: center; gap: 10px; margin-bottom: 6px;
    }
    .brand-mention .bm-name {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 1rem; font-weight: 700; color: #1A1A1A;
    }
    .sentiment-badge {
        padding: 2px 9px; border-radius: 999px;
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.7rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.08em;
    }
    .sentiment-badge.pos { background: rgba(92,184,92,0.15); color: #3a8f3a; }
    .sentiment-badge.neu { background: rgba(138,129,124,0.15); color: #8A817C; }
    .sentiment-badge.neg { background: rgba(217,83,79,0.15); color: #a83e3a; }
    .brand-mention .bm-context {
        font-size: 0.84rem; color: #555; line-height: 1.5; margin-bottom: 4px;
    }
    .brand-mention .bm-source {
        font-size: 0.74rem; color: #8A817C; font-style: italic;
    }

    /* Sentiment 3-col breakdown */
    .sentiment-grid {
        display: grid; grid-template-columns: 1fr 1fr 1fr;
        gap: 12px; margin-bottom: 14px;
    }
    .sentiment-cell {
        background: #ffffff; border: 1px solid #E0D8D0;
        border-left: 4px solid #ccc;
        border-radius: 0 10px 10px 0;
        padding: 16px 20px 14px 20px;
        text-align: center;
    }
    .sentiment-cell.pos { border-left-color: #5CB85C; }
    .sentiment-cell.neu { border-left-color: #8A817C; }
    .sentiment-cell.neg { border-left-color: #D9534F; }
    .sentiment-cell .sent-pct {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 2rem; font-weight: 800;
        color: #1A1A1A; line-height: 1;
    }
    .sentiment-cell .sent-lbl {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.74rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.12em;
        color: #8A817C; margin-top: 6px;
    }

    /* Page 4: Reference brand pills + filters */
    .ref-brand-picker {
        display: flex; gap: 10px; margin: 6px 0 16px 0; flex-wrap: wrap;
        align-items: center;
    }
    .ref-platform-radio {
        display: inline-flex; gap: 8px;
        background: #fff; border: 1px solid #E0D8D0;
        border-radius: 999px; padding: 4px;
        margin-right: 14px;
    }
    .ref-platform-radio span {
        padding: 5px 14px; border-radius: 999px;
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.82rem; font-weight: 600;
        color: #8A817C;
    }
    .ref-platform-radio span.active { background: #F8C090; color: #1A1A1A; }
    .ref-pill {
        padding: 8px 16px; border-radius: 999px;
        border: 1px solid #E0D8D0; background: #ffffff;
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.86rem; font-weight: 600;
        color: #333;
    }
    .ref-pill.active { background: #1A1A1A; color: #F8C090; border-color: #1A1A1A; }

    /* Connect callout (Page 3 content mix) */
    .connect-callout {
        background: linear-gradient(135deg, rgba(46,163,242,0.08) 0%, rgba(46,163,242,0.02) 100%);
        border-left: 4px solid #2ea3f2;
        border-radius: 0 10px 10px 0;
        padding: 16px 20px 14px 20px;
        margin: 14px 0;
    }
    .connect-callout h4 {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.9rem; font-weight: 800;
        text-transform: uppercase; letter-spacing: 0.08em;
        color: #2ea3f2; margin-bottom: 6px;
    }
    .connect-callout p { font-size: 0.88rem; color: #444; line-height: 1.55; }

    /* IG format mix card */
    .ig-format-card {
        background: #ffffff; border: 1px solid #E0D8D0;
        border-top: 3px solid #2ea3f2;
        border-radius: 10px;
        padding: 18px 20px 14px 20px;
        text-align: center;
    }
    .ig-format-card.reels    { border-top-color: #2ea3f2; }
    .ig-format-card.carousel { border-top-color: #F8C090; }
    .ig-format-card.static   { border-top-color: #C9A87E; }
    .ig-format-card.story    { border-top-color: #66BB6A; }
    .ig-format-card .pct {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 1.8rem; font-weight: 800;
        color: #1A1A1A; line-height: 1;
    }
    .ig-format-card .pct.reels    { color: #2ea3f2; }
    .ig-format-card .pct.carousel { color: #F8C090; }
    .ig-format-card .pct.static   { color: #C9A87E; }
    .ig-format-card .pct.story    { color: #66BB6A; }
    .ig-format-card .fmt-name {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 1rem; font-weight: 700;
        color: #1A1A1A; margin: 8px 0 4px 0;
    }
    .ig-format-card .fmt-role { font-size: 0.78rem; color: #8A817C; }

    /* Insight expander (Page 5) */
    .insight-expander {
        background: #ffffff; border: 1px solid #E0D8D0;
        border-radius: 10px; margin-bottom: 8px;
        overflow: hidden; transition: border-color 0.2s ease;
    }
    .insight-expander:hover { border-color: #F8C090; }

    /* "What this means for hero" custom cards (Page 5) */
    .wtm-card {
        background: #ffffff; border: 1px solid #E0D8D0;
        border-left: 4px solid #ccc;
        border-radius: 0 10px 10px 0;
        padding: 16px 20px 14px 20px;
        margin-bottom: 10px;
    }
    .wtm-card.blue   { border-left-color: #2ea3f2; }
    .wtm-card.green  { border-left-color: #5CB85C; background: #F0FFF0; }
    .wtm-card.red    { border-left-color: #D9534F; }
    .wtm-card.orange { border-left-color: #F0AD4E; }
    .wtm-card.peach  {
        border-left-color: #F8C090;
        background: linear-gradient(135deg, #FDEBD6 0%, #FFF8F0 100%);
    }
    .wtm-card h4 {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 1.05rem; font-weight: 800;
        color: #1A1A1A; margin-bottom: 8px;
    }
    .wtm-card p, .wtm-card li {
        font-size: 0.88rem; color: #444; line-height: 1.55;
    }
    .wtm-card ul { margin-left: 16px; }

    /* News trending narrative card */
    .news-narrative {
        background: #ffffff; border: 1px solid #E0D8D0;
        border-top: 3px solid #2ea3f2;
        border-radius: 10px;
        padding: 14px 18px 12px 18px;
        margin-bottom: 8px;
    }
    .news-narrative h4 {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.98rem; font-weight: 700;
        color: #1A1A1A; margin-bottom: 4px;
    }
    .news-narrative p { font-size: 0.86rem; color: #555; line-height: 1.5; }
    .news-narrative .brands-line {
        margin-top: 6px; font-size: 0.74rem;
        color: #8A817C; font-style: italic;
    }
    .news-quote {
        background: #F7F3EE; border-left: 3px solid #8A817C;
        padding: 12px 16px; margin: 8px 0;
        font-size: 0.86rem; color: #444;
        font-style: italic; line-height: 1.55;
        border-radius: 0 6px 6px 0;
    }
</style>
"""
