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

# ── Collaboration type classification ──
COLLAB_OWNED_TYPES = {"cuervo", "partner"}        # brand-account posts
COLLAB_AMPLIFIED_TYPES = {"influencer", "collective"}  # other-account posts


def split_owned_collab(df):
    """Split a DataFrame into owned and collab subsets based on collaboration column.

    Owned = Cuervo + Partner (brand-account posts).
    Collab = Influencer + Collective (other-account posts with inflated reach).
    Returns (owned_df, collab_df). If no collaboration column, returns (df, empty_df).
    """
    if "collaboration" not in df.columns:
        return df, df.iloc[0:0]
    collab_lower = df["collaboration"].str.strip().str.lower()
    owned = df[collab_lower.isin(COLLAB_OWNED_TYPES) | collab_lower.isna()]
    collab = df[collab_lower.isin(COLLAB_AMPLIFIED_TYPES)]
    return owned, collab
