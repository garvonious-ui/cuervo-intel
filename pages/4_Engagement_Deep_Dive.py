import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from config import BRAND_COLORS, CHART_TEMPLATE, CHART_FONT, BRAND_ORDER

st.header("Engagement Deep Dive")

if "results" not in st.session_state:
    st.warning("Go to the home page first to load data.")
    st.stop()

results = st.session_state["results"]
df = st.session_state["filtered_df"]
sel_brands = st.session_state["sel_brands"]
order = [b for b in BRAND_ORDER if b in sel_brands]

# ── ER by content type per platform ───────────────────────────────────

st.subheader("Engagement Rate by Content Type")

tab_ig, tab_tt = st.tabs(["Instagram", "TikTok"])

for tab, plat in [(tab_ig, "Instagram"), (tab_tt, "TikTok")]:
    with tab:
        pdata = df[(df["brand"].isin(sel_brands)) & (df["platform"] == plat)]
        type_er = pdata.groupby(["brand", "post_type"])["engagement_rate"].mean().reset_index()
        if len(type_er):
            fig = px.bar(type_er, x="post_type", y="engagement_rate", color="brand",
                         barmode="group", color_discrete_map=BRAND_COLORS,
                         category_orders={"brand": order},
                         labels={"engagement_rate": "Avg ER %", "post_type": "", "brand": "Brand"},
                         template=CHART_TEMPLATE)
            fig.update_layout(font=CHART_FONT, height=400, legend=dict(orientation="h", y=1.12))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(f"No {plat} data for selected brands.")

# ── Posting schedule heatmap ──────────────────────────────────────────

st.subheader("Posting Schedule Heatmap")

sched_brand = st.selectbox("Brand", ["All Brands"] + order, key="sched_brand")

if sched_brand == "All Brands":
    sched_df = df[df["brand"].isin(sel_brands)]
else:
    sched_df = df[df["brand"] == sched_brand]

if "post_date" in sched_df.columns:
    sched_df = sched_df.copy()
    sched_df["day_of_week"] = pd.to_datetime(sched_df["post_date"], errors="coerce").dt.day_name()
    sched_df["hour"] = pd.to_numeric(sched_df["post_hour"], errors="coerce")

    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    pivot = sched_df.groupby(["day_of_week", "hour"]).size().reset_index(name="posts")
    heatmap = pivot.pivot(index="day_of_week", columns="hour", values="posts").fillna(0)
    heatmap = heatmap.reindex(days_order)
    # Ensure all hours 0-23
    for h in range(24):
        if h not in heatmap.columns:
            heatmap[h] = 0
    heatmap = heatmap[sorted(heatmap.columns)]

    fig_hm = go.Figure(go.Heatmap(
        z=heatmap.values, x=[f"{h}:00" for h in heatmap.columns],
        y=heatmap.index, colorscale="YlOrRd",
        colorbar=dict(title="Posts"),
    ))
    fig_hm.update_layout(height=350, template=CHART_TEMPLATE, font=CHART_FONT,
                         xaxis_title="Hour of Day", yaxis_title="")
    st.plotly_chart(fig_hm, use_container_width=True)

# ── Top posts leaderboard ─────────────────────────────────────────────

st.subheader("Top Performing Posts")

top_n = st.slider("Show top", 10, 50, 20, step=5)

top_df = (
    df[df["brand"].isin(sel_brands)]
    .nlargest(top_n, "engagement_rate")
    [["brand", "platform", "post_type", "engagement_rate", "likes", "comments",
      "shares", "views", "content_theme", "post_date", "post_url"]]
    .reset_index(drop=True)
)
top_df.index = top_df.index + 1
top_df.index.name = "Rank"
top_df["engagement_rate"] = top_df["engagement_rate"].round(2)

st.dataframe(
    top_df.style.map(
        lambda v: "background-color: #FFF8E1" if v == "Jose Cuervo" else "",
        subset=["brand"],
    ),
    use_container_width=True,
    height=min(700, 35 * top_n + 40),
)

# ── ER distribution violin ────────────────────────────────────────────

st.subheader("Engagement Rate Distribution by Brand")

fig_v = px.violin(df[df["brand"].isin(sel_brands)], x="brand", y="engagement_rate",
                  color="brand", color_discrete_map=BRAND_COLORS,
                  category_orders={"brand": order}, box=True, points="outliers",
                  labels={"engagement_rate": "ER %", "brand": ""},
                  template=CHART_TEMPLATE)
fig_v.update_layout(showlegend=False, font=CHART_FONT, height=420)
st.plotly_chart(fig_v, use_container_width=True)
