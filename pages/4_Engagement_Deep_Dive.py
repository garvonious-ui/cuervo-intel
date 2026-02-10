import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from config import BRAND_COLORS, CHART_TEMPLATE, CHART_FONT, BRAND_ORDER, CUSTOM_CSS

st.logo("logo.png")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
st.header("Engagement Deep Dive")

if "results" not in st.session_state:
    st.warning("Go to the home page first to load data.")
    st.stop()

results = st.session_state["results"]
df = st.session_state["filtered_df"]
sel_brands = st.session_state["sel_brands"]
order = [b for b in BRAND_ORDER if b in sel_brands]

# ── Platform filter (applies to entire page) ─────────────────────────

available_plats = sorted(df["platform"].unique().tolist())
plat_options = ["All"] + available_plats
sel_plat = st.selectbox("Platform", plat_options, key="deep_plat")
if sel_plat != "All":
    df = df[df["platform"] == sel_plat]

if df.empty:
    st.warning("No posts match the current filters.")
    st.stop()

# ── Engagement Signals Breakdown ─────────────────────────────────────

st.subheader("Engagement Signals Breakdown")
st.caption("Beyond likes — saves, shares, and comments indicate deeper audience connection and algorithmic favorability")

signal_brands = [b for b in order if b in sel_brands]
signal_rows = []
for brand in signal_brands:
    bdf = df[df["brand"] == brand]
    if len(bdf) == 0:
        continue
    signal_rows.append({
        "Brand": brand,
        "Avg Likes": int(bdf["likes"].mean()),
        "Avg Comments": int(bdf["comments"].mean()),
        "Avg Shares": int(bdf["shares"].mean()),
        "Avg Saves": int(bdf["saves"].mean()),
        "Avg Views": int(bdf["views"].mean()),
        "Save Rate": round(bdf["saves"].sum() / max(bdf["likes"].sum(), 1) * 100, 2),
        "Share Rate": round(bdf["shares"].sum() / max(bdf["likes"].sum(), 1) * 100, 2),
        "Comment Rate": round(bdf["comments"].sum() / max(bdf["likes"].sum(), 1) * 100, 2),
    })

if signal_rows:
    signal_df = pd.DataFrame(signal_rows)

    col_s1, col_s2 = st.columns(2)

    with col_s1:
        st.markdown("**Save Rate by Brand** (Saves ÷ Likes × 100)")
        st.caption("High save rates signal content worth returning to — strong algorithmic signal")
        fig_save = px.bar(signal_df, x="Save Rate", y="Brand", orientation="h",
                          color="Brand", color_discrete_map=BRAND_COLORS,
                          category_orders={"Brand": order},
                          labels={"Save Rate": "Save Rate %", "Brand": ""},
                          template=CHART_TEMPLATE, text_auto=".1f")
        fig_save.update_layout(showlegend=False, font=CHART_FONT, height=380)
        st.plotly_chart(fig_save, use_container_width=True)

    with col_s2:
        st.markdown("**Share Rate by Brand** (Shares ÷ Likes × 100)")
        st.caption("Shares extend reach organically — the strongest growth signal")
        fig_share = px.bar(signal_df, x="Share Rate", y="Brand", orientation="h",
                           color="Brand", color_discrete_map=BRAND_COLORS,
                           category_orders={"Brand": order},
                           labels={"Share Rate": "Share Rate %", "Brand": ""},
                           template=CHART_TEMPLATE, text_auto=".1f")
        fig_share.update_layout(showlegend=False, font=CHART_FONT, height=380)
        st.plotly_chart(fig_share, use_container_width=True)

    # Detailed signal table
    with st.expander("Full Engagement Signals Table"):
        def highlight_cuervo_signal(row):
            return ["background-color: #FDEBD6" if row["Brand"] == "Jose Cuervo" else "" for _ in row]

        styled_sig = (
            signal_df.style
            .apply(highlight_cuervo_signal, axis=1)
            .format({"Save Rate": "{:.2f}", "Share Rate": "{:.2f}", "Comment Rate": "{:.2f}",
                      "Avg Likes": "{:,.0f}", "Avg Comments": "{:,.0f}",
                      "Avg Shares": "{:,.0f}", "Avg Saves": "{:,.0f}", "Avg Views": "{:,.0f}"})
        )
        st.dataframe(styled_sig, use_container_width=True, hide_index=True)

st.markdown("---")

# ── ER by content type ────────────────────────────────────────────────

st.subheader("Engagement Rate by Content Type")

type_er = df[df["brand"].isin(sel_brands)].groupby(["brand", "post_type"])["engagement_rate"].mean().reset_index()
if len(type_er):
    fig = px.bar(type_er, x="post_type", y="engagement_rate", color="brand",
                 barmode="group", color_discrete_map=BRAND_COLORS,
                 category_orders={"brand": order},
                 labels={"engagement_rate": "Avg ER %", "post_type": "", "brand": "Brand"},
                 template=CHART_TEMPLATE)
    fig.update_layout(font=CHART_FONT, height=400, legend=dict(orientation="h", y=1.12))
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No data for the selected platform/brands.")

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
    sched_df = sched_df.dropna(subset=["day_of_week", "hour"])
    sched_df["hour"] = sched_df["hour"].astype(int)

    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    pivot = sched_df.groupby(["day_of_week", "hour"]).size().reset_index(name="posts")
    heatmap = pivot.pivot(index="day_of_week", columns="hour", values="posts").fillna(0)
    heatmap = heatmap.reindex(days_order).fillna(0)
    # Ensure all hours 0-23
    for h in range(24):
        if h not in heatmap.columns:
            heatmap[h] = 0
    heatmap = heatmap[[h for h in sorted(heatmap.columns) if pd.notna(h)]]

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
        lambda v: "background-color: #FDEBD6" if v == "Jose Cuervo" else "",
        subset=["brand"],
    ),
    use_container_width=True,
    height=min(700, 35 * top_n + 40),
)

# ── ER distribution violin ────────────────────────────────────────────

st.subheader("Avg Engagement Rate by Brand")

er_brand = (df[df["brand"].isin(sel_brands)]
            .groupby("brand")["engagement_rate"].mean()
            .reindex(order).fillna(0).reset_index())
er_brand.columns = ["brand", "avg_er"]
fig_v = px.bar(er_brand, x="avg_er", y="brand", orientation="h",
               color="brand", color_discrete_map=BRAND_COLORS,
               category_orders={"brand": order},
               labels={"avg_er": "Avg ER %", "brand": ""},
               template=CHART_TEMPLATE, text_auto=".2f")
fig_v.update_layout(showlegend=False, font=CHART_FONT, height=420)
st.plotly_chart(fig_v, use_container_width=True)
