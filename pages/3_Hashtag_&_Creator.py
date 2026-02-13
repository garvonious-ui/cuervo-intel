import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from config import BRAND_COLORS, CHART_TEMPLATE, CHART_FONT, BRAND_ORDER, CUSTOM_CSS

st.logo("logo.png")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
st.header("Hashtag & Creator Analysis")
st.caption("Hashtag and creator metrics are based on the full 30-day dataset.")

if "results" not in st.session_state:
    st.warning("Go to the home page first to load data.")
    st.stop()

results = st.session_state["results"]
df = st.session_state["filtered_df"]
sel_brands = st.session_state["sel_brands"]
order = [b for b in BRAND_ORDER if b in sel_brands]

# ══════════════════════════════════════════════════════════════════════
#  HASHTAG STRATEGY
# ══════════════════════════════════════════════════════════════════════

st.subheader("Hashtag Strategy Overview")

ht_rows = []
for brand in order:
    ht = results["hashtags"].get(brand, {})
    ht_rows.append({
        "Brand": brand,
        "Unique Tags": ht.get("unique_hashtags", 0),
        "Avg/Post": ht.get("avg_hashtags_per_post", 0),
        "Branded %": ht.get("branded_hashtag_pct", 0),
        "Total Usage (30d)": ht.get("total_hashtag_usage", 0),
    })

ht_df = pd.DataFrame(ht_rows)
st.dataframe(
    ht_df.style.apply(
        lambda row: ["background-color: #FDEBD6" if row["Brand"] == "Jose Cuervo" else "" for _ in row],
        axis=1,
    ).format({"Avg/Post": "{:.1f}", "Branded %": "{:.1f}%"}),
    width="stretch", hide_index=True,
)

# Top hashtags per brand
st.subheader("Top Hashtags per Brand")

tag_brand = st.selectbox("Select brand", order, key="tag_brand")
tags = results["hashtags"].get(tag_brand, {}).get("top_15_hashtags", [])
if tags:
    tag_df = pd.DataFrame(tags, columns=["Hashtag", "Times Used"])
    fig_tags = px.bar(tag_df, x="Hashtag", y="Times Used",
                      color_discrete_sequence=[BRAND_COLORS.get(tag_brand, "#888")],
                      template=CHART_TEMPLATE,
                      labels={"Times Used": "Uses (30d)", "Hashtag": ""})
    fig_tags.update_layout(font=CHART_FONT, height=380, xaxis_tickangle=-40)
    st.plotly_chart(fig_tags, width="stretch")
else:
    st.info("No hashtag data for this brand.")


# ══════════════════════════════════════════════════════════════════════
#  CREATOR COLLABORATIONS
# ══════════════════════════════════════════════════════════════════════

st.markdown("---")
st.subheader("Creator Collaboration Rates")

# Gauge-style indicators
cols = st.columns(min(len(order), 4))
for i, brand in enumerate(order):
    cr = results["creators"].get(brand, {})
    pct = cr.get("collab_pct", 0)
    with cols[i % len(cols)]:
        fig_g = go.Figure(go.Indicator(
            mode="gauge+number",
            value=pct,
            title={"text": brand, "font": {"size": 13}},
            number={"suffix": "%"},
            gauge={
                "axis": {"range": [0, 50]},
                "bar": {"color": BRAND_COLORS.get(brand, "#888")},
                "steps": [
                    {"range": [0, 15], "color": "#FFCDD2"},
                    {"range": [15, 30], "color": "#FDEBD6"},
                    {"range": [30, 50], "color": "#C8E6C9"},
                ],
            },
        ))
        fig_g.update_layout(height=200, margin=dict(t=50, b=10, l=20, r=20))
        st.plotly_chart(fig_g, width="stretch")

# Collab vs non-collab ER
st.subheader("Collab vs Non-Collab Engagement")

collab_rows = []
for brand in order:
    cr = results["creators"].get(brand, {})
    collab_rows.append({"brand": brand, "type": "Collab", "er": cr.get("avg_collab_engagement_rate", 0)})
    collab_rows.append({"brand": brand, "type": "Non-Collab", "er": cr.get("avg_non_collab_engagement_rate", 0)})

cdf = pd.DataFrame(collab_rows)
fig_collab = px.bar(cdf, x="brand", y="er", color="type", barmode="group",
                    color_discrete_map={"Collab": "#F8C090", "Non-Collab": "#D9D3CC"},
                    category_orders={"brand": order},
                    labels={"er": "Avg ER %", "brand": "", "type": ""},
                    template=CHART_TEMPLATE)
fig_collab.update_layout(font=CHART_FONT, height=400, legend=dict(orientation="h", y=1.12))
st.plotly_chart(fig_collab, width="stretch")

# Engagement lift table
st.subheader("Creator Collab Summary")

cr_rows = []
for brand in order:
    cr = results["creators"].get(brand, {})
    cr_rows.append({
        "Brand": brand,
        "Collab Posts": cr.get("total_collab_posts", 0),
        "Collab ER %": round(cr.get("avg_collab_engagement_rate", 0), 2),
        "Non-Collab ER %": round(cr.get("avg_non_collab_engagement_rate", 0), 2),
        "ER Lift": round(cr.get("collab_engagement_lift", 0), 2),
        "Unique Creators": cr.get("unique_creators", 0),
        "Paid": cr.get("paid_partnerships", 0),
        "Organic": cr.get("organic_collabs", 0),
    })

cr_df = pd.DataFrame(cr_rows)
st.dataframe(
    cr_df.style.apply(
        lambda row: ["background-color: #FDEBD6" if row["Brand"] == "Jose Cuervo" else "" for _ in row],
        axis=1,
    ).map(
        lambda v: "color: #2E7D32; font-weight:bold" if isinstance(v, (int, float)) and v > 0.5 else
                  ("color: #C62828; font-weight:bold" if isinstance(v, (int, float)) and v < -0.3 else ""),
        subset=["ER Lift"],
    ),
    width="stretch", hide_index=True,
)
