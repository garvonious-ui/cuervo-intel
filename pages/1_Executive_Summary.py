import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from config import BRAND_COLORS, CHART_TEMPLATE, CHART_FONT, PRIORITY_COLORS, BRAND_ORDER, CUSTOM_CSS

st.logo("logo.png")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
st.header("Executive Summary")

if "results" not in st.session_state:
    st.warning("Go to the home page first to load data.")
    st.stop()

results = st.session_state["results"]
df = st.session_state["filtered_df"]
sel_brands = st.session_state["sel_brands"]

# ── KPI cards ─────────────────────────────────────────────────────────

er_by_brand_plat = (
    df.groupby(["brand", "platform"])["engagement_rate"]
    .mean()
    .unstack(fill_value=0)
)

c1, c2, c3, c4 = st.columns(4)
cuervo_ig = er_by_brand_plat.loc["Jose Cuervo", "Instagram"] if "Jose Cuervo" in er_by_brand_plat.index and "Instagram" in er_by_brand_plat.columns else 0
cuervo_tt = er_by_brand_plat.loc["Jose Cuervo", "TikTok"] if "Jose Cuervo" in er_by_brand_plat.index and "TikTok" in er_by_brand_plat.columns else 0

freq = results["frequency"]
cuervo_ppw = 0
for p in ["Instagram", "TikTok"]:
    cuervo_ppw += freq.get("Jose Cuervo", {}).get(p, {}).get("posts_per_week", 0)

cuervo_combined_er = df[df["brand"] == "Jose Cuervo"]["engagement_rate"].mean() if "Jose Cuervo" in df["brand"].values else 0
cuervo_combined_er = 0 if pd.isna(cuervo_combined_er) else cuervo_combined_er
comp_ers = df[df["brand"] != "Jose Cuervo"].groupby("brand")["engagement_rate"].mean()
comp_ers = comp_ers[comp_ers > 0]
best_comp = comp_ers.idxmax() if len(comp_ers) else "N/A"
best_comp_er = comp_ers.max() if len(comp_ers) else 0
gap = round(cuervo_combined_er - best_comp_er, 2) if best_comp_er else 0

with c1:
    st.metric("Cuervo IG ER", f"{cuervo_ig:.2f}%")
with c2:
    st.metric("Cuervo TT ER", f"{cuervo_tt:.2f}%")
with c3:
    st.metric("Cuervo posts/wk", f"{cuervo_ppw:.1f}")
with c4:
    st.metric("Gap vs Best", f"{gap:+.2f}%", delta=f"vs {best_comp}")

# ── Engagement rate comparison ────────────────────────────────────────

st.subheader("Avg Engagement Rate by Brand & Platform")

er_data = df.groupby(["brand", "platform"])["engagement_rate"].mean().reset_index()
er_data = er_data[er_data["brand"].isin(sel_brands)]
order = [b for b in BRAND_ORDER if b in sel_brands]

fig = px.bar(er_data, x="brand", y="engagement_rate", color="platform",
             barmode="group", color_discrete_map={"Instagram": "#D4956A", "TikTok": "#2ea3f2"},
             category_orders={"brand": order},
             labels={"engagement_rate": "Avg ER %", "brand": "", "platform": "Platform"},
             template=CHART_TEMPLATE)
fig.update_layout(font=CHART_FONT, height=420, legend=dict(orientation="h", y=1.12))

# Category avg line
cat_avg = df[df["engagement_rate"] > 0]["engagement_rate"].mean() if len(df[df["engagement_rate"] > 0]) else 0
fig.add_hline(y=cat_avg, line_dash="dash", line_color="gray",
              annotation_text=f"Category avg {cat_avg:.2f}%", annotation_position="top right")

st.plotly_chart(fig, use_container_width=True)

# ── Posting frequency ─────────────────────────────────────────────────

st.subheader("Posting Frequency (posts/week)")
st.caption("Based on full 30-day dataset (not affected by content type filters)")

freq_rows = []
for brand in sel_brands:
    for plat in ["Instagram", "TikTok"]:
        ppw = freq.get(brand, {}).get(plat, {}).get("posts_per_week", 0)
        freq_rows.append({"brand": brand, "platform": plat, "posts_per_week": ppw})
freq_df = pd.DataFrame(freq_rows)

fig2 = px.bar(freq_df, x="brand", y="posts_per_week", color="platform",
              barmode="group", color_discrete_map={"Instagram": "#D4956A", "TikTok": "#2ea3f2"},
              category_orders={"brand": order},
              labels={"posts_per_week": "Posts / Week", "brand": ""},
              template=CHART_TEMPLATE)
fig2.update_layout(font=CHART_FONT, height=380, legend=dict(orientation="h", y=1.12))
st.plotly_chart(fig2, use_container_width=True)

# ── Radar chart ───────────────────────────────────────────────────────

st.subheader("Competitive Comparison — Cuervo vs Top 2 Competitors")

# Pick top 2 competitors by ER
comp_avg_er = df[df["brand"] != "Jose Cuervo"].groupby("brand")["engagement_rate"].mean()
comp_avg_er = comp_avg_er[comp_avg_er > 0]
top2 = comp_avg_er.nlargest(2).index.tolist() if len(comp_avg_er) >= 2 else comp_avg_er.index.tolist()
radar_brands = ["Jose Cuervo"] + top2

dimensions = ["Avg ER %", "Posts/Week", "Collab %", "Hashtags/Post", "Avg Likes"]

raw_vals = {}
for brand in radar_brands:
    brand_df = df[df["brand"] == brand]
    er = brand_df["engagement_rate"].mean() if len(brand_df) else 0
    er = 0 if pd.isna(er) else er
    ppw = round(len(brand_df) / 4.3, 1) if len(brand_df) else 0
    collab_count = len(brand_df[brand_df["has_creator_collab"].astype(str).str.lower() == "yes"]) if len(brand_df) else 0
    collab_pct = round(collab_count / len(brand_df) * 100, 1) if len(brand_df) else 0
    htag_counts = brand_df["hashtags"].fillna("").apply(lambda x: len(x.split()) if x.strip() else 0)
    htags = round(htag_counts.mean(), 1) if len(htag_counts) else 0
    avg_likes = brand_df["likes"].mean() if len(brand_df) else 0
    avg_likes = 0 if pd.isna(avg_likes) else avg_likes
    raw_vals[brand] = [er, ppw, collab_pct, htags, avg_likes]

# Normalize to 0-100 for comparable bars
maxes = [max((raw_vals[b][i] for b in radar_brands), default=1) or 1 for i in range(5)]

comp_rows = []
for brand in radar_brands:
    for i, dim in enumerate(dimensions):
        comp_rows.append({
            "Brand": brand, "Metric": dim,
            "Normalized": round(raw_vals[brand][i] / maxes[i] * 100, 1),
            "Raw": round(raw_vals[brand][i], 1),
        })

comp_df = pd.DataFrame(comp_rows)
fig3 = px.bar(comp_df, x="Normalized", y="Metric", color="Brand", orientation="h",
              barmode="group", color_discrete_map=BRAND_COLORS,
              labels={"Normalized": "Score (0–100)", "Metric": ""},
              template=CHART_TEMPLATE, text="Raw",
              hover_data={"Raw": ":.1f", "Normalized": False})
fig3.update_traces(texttemplate="%{text}", textposition="outside")
fig3.update_layout(height=450, font=CHART_FONT,
                   legend=dict(orientation="h", y=-0.15))
st.plotly_chart(fig3, use_container_width=True)

# ── Priority recommendations ──────────────────────────────────────────

st.subheader("Priority Recommendations for Cuervo")

recs = results["recommendations"]
if recs:
    rec_df = pd.DataFrame(recs)
    # Color-code priority
    def priority_style(val):
        colors = {"High": "background-color: #FFCDD2", "Medium": "background-color: #FFE0B2",
                  "Low": "background-color: #C8E6C9"}
        return colors.get(val, "")

    styled = rec_df[["priority", "category", "platform", "insight", "recommendation"]].style.map(
        priority_style, subset=["priority"]
    )
    st.dataframe(styled, use_container_width=True, height=400)
else:
    st.info("No recommendations generated — populate data and re-run.")
