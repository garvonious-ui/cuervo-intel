import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import plotly.express as px
import streamlit as st

from config import BRAND_COLORS, CHART_TEMPLATE, CHART_FONT, BRAND_ORDER, CUSTOM_CSS

st.logo("logo.png")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
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
        "Matching Posts": len(plat_df),
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

st.subheader("Followers & Engagement Rate by Brand")

fe_rows = []
for brand in sel_brands:
    for plat in st.session_state["sel_platforms"]:
        bdf = df[(df["brand"] == brand) & (df["platform"] == plat)]
        if len(bdf) == 0:
            continue
        eng = results["engagement"].get(brand, {}).get(plat, {})
        followers = eng.get("followers", 0)
        avg_er = bdf["engagement_rate"].mean()
        if followers > 0 and avg_er > 0:
            fe_rows.append({
                "brand": brand,
                "platform": plat,
                "followers": followers,
                "avg_er": round(avg_er, 2),
            })

fe_df = pd.DataFrame(fe_rows)
if len(fe_df):
    col_f, col_e = st.columns(2)
    with col_f:
        st.markdown("**Followers**")
        fig_fol = px.bar(fe_df, x="followers", y="brand", color="platform", orientation="h",
                         barmode="group",
                         color_discrete_map={"Instagram": "#D4956A", "TikTok": "#2ea3f2"},
                         category_orders={"brand": order},
                         labels={"followers": "Followers", "brand": ""},
                         template=CHART_TEMPLATE, text_auto=".3s")
        fig_fol.update_layout(font=CHART_FONT, height=400, showlegend=False)
        st.plotly_chart(fig_fol, use_container_width=True)
    with col_e:
        st.markdown("**Avg Engagement Rate**")
        fig_er = px.bar(fe_df, x="avg_er", y="brand", color="platform", orientation="h",
                        barmode="group",
                        color_discrete_map={"Instagram": "#D4956A", "TikTok": "#2ea3f2"},
                        category_orders={"brand": order},
                        labels={"avg_er": "Avg ER %", "brand": ""},
                        template=CHART_TEMPLATE, text_auto=".2f")
        fig_er.update_layout(font=CHART_FONT, height=400,
                             legend=dict(orientation="h", y=1.12))
        st.plotly_chart(fig_er, use_container_width=True)
