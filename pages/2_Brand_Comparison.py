import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import plotly.express as px
import streamlit as st

from config import BRAND_COLORS, CHART_TEMPLATE, CHART_FONT, BRAND_ORDER

st.header("Brand Comparison")

if "results" not in st.session_state:
    st.warning("Go to the home page first to load data.")
    st.stop()

results = st.session_state["results"]
df = st.session_state["filtered_df"]
sel_brands = st.session_state["sel_brands"]
order = [b for b in BRAND_ORDER if b in sel_brands]

# ── Comparison matrix ─────────────────────────────────────────────────

st.subheader("Side-by-Side Metrics")

platform_tab = st.radio("Platform", ["Instagram", "TikTok", "Combined"], horizontal=True)

rows = []
for brand in order:
    plat_df = df[df["brand"] == brand]
    if platform_tab != "Combined":
        plat_df = plat_df[plat_df["platform"] == platform_tab]

    eng = results["engagement"].get(brand, {})
    freq = results["frequency"].get(brand, {})
    cr = results["creators"].get(brand, {})
    ht = results["hashtags"].get(brand, {})

    if platform_tab == "Combined":
        followers = sum(eng.get(p, {}).get("followers", 0) for p in ["Instagram", "TikTok"])
        avg_er = plat_df["engagement_rate"].mean() if len(plat_df) else 0
        ppw = sum(freq.get(p, {}).get("posts_per_week", 0) for p in ["Instagram", "TikTok"])
    else:
        followers = eng.get(platform_tab, {}).get("followers", 0)
        avg_er = plat_df["engagement_rate"].mean() if len(plat_df) else 0
        ppw = freq.get(platform_tab, {}).get("posts_per_week", 0)

    rows.append({
        "Brand": brand,
        "Followers": followers,
        "Posts (30d)": len(plat_df),
        "Posts/Week": round(ppw, 1),
        "Avg ER %": round(avg_er, 3),
        "Avg Likes": int(plat_df["likes"].mean()) if len(plat_df) else 0,
        "Avg Comments": int(plat_df["comments"].mean()) if len(plat_df) else 0,
        "Avg Views": int(plat_df["views"].mean()) if len(plat_df) else 0,
        "Collab %": cr.get("collab_pct", 0),
        "Hashtags/Post": ht.get("avg_hashtags_per_post", 0),
    })

comp_df = pd.DataFrame(rows)


def highlight_cuervo(row):
    return ["background-color: #FDEBD6" if row["Brand"] == "Jose Cuervo" else "" for _ in row]


def color_er(val):
    if isinstance(val, (int, float)):
        if val >= 4:
            return "background-color: #C8E6C9"
        elif val >= 2.5:
            return "background-color: #FDEBD6"
        elif val > 0:
            return "background-color: #FFCDD2"
    return ""


styled = (
    comp_df.style
    .apply(highlight_cuervo, axis=1)
    .map(color_er, subset=["Avg ER %"])
    .format({"Followers": "{:,.0f}", "Avg Likes": "{:,.0f}",
             "Avg Comments": "{:,.0f}", "Avg Views": "{:,.0f}",
             "Avg ER %": "{:.2f}", "Posts/Week": "{:.1f}",
             "Collab %": "{:.1f}", "Hashtags/Post": "{:.1f}"})
)
st.dataframe(styled, use_container_width=True, hide_index=True, height=320)

# ── Content type distribution ─────────────────────────────────────────

st.subheader("Content Type Distribution")

type_data = df[df["brand"].isin(sel_brands)].groupby(["brand", "post_type"]).size().reset_index(name="count")
totals = type_data.groupby("brand")["count"].transform("sum")
type_data["pct"] = (type_data["count"] / totals * 100).round(1)

fig = px.bar(type_data, x="brand", y="pct", color="post_type",
             barmode="stack", category_orders={"brand": order},
             labels={"pct": "% of Posts", "brand": "", "post_type": "Type"},
             template=CHART_TEMPLATE, color_discrete_sequence=px.colors.qualitative.Set2)
fig.update_layout(font=CHART_FONT, height=400, legend=dict(orientation="h", y=1.12))
st.plotly_chart(fig, use_container_width=True)

# ── Followers vs ER scatter ───────────────────────────────────────────

st.subheader("Followers vs Engagement Rate")

scatter_rows = []
for brand in sel_brands:
    for plat in st.session_state["sel_platforms"]:
        bdf = df[(df["brand"] == brand) & (df["platform"] == plat)]
        if len(bdf) == 0:
            continue
        eng = results["engagement"].get(brand, {}).get(plat, {})
        scatter_rows.append({
            "brand": brand,
            "platform": plat,
            "followers": eng.get("followers", 0),
            "avg_er": bdf["engagement_rate"].mean(),
            "posts": len(bdf),
        })

sdf = pd.DataFrame(scatter_rows)
if len(sdf):
    fig2 = px.scatter(sdf, x="followers", y="avg_er", color="brand", symbol="platform",
                      size="posts", size_max=30,
                      color_discrete_map=BRAND_COLORS,
                      labels={"followers": "Followers", "avg_er": "Avg ER %",
                              "posts": "Post Count"},
                      template=CHART_TEMPLATE, hover_name="brand")
    fig2.update_layout(font=CHART_FONT, height=450)
    # Quadrant lines
    fig2.add_hline(y=sdf["avg_er"].median(), line_dash="dot", line_color="#ccc")
    fig2.add_vline(x=sdf["followers"].median(), line_dash="dot", line_color="#ccc")
    st.plotly_chart(fig2, use_container_width=True)
