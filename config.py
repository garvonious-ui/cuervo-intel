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
