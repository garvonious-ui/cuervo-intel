import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from config import BRAND_COLORS, CHART_TEMPLATE, CHART_FONT, BRAND_ORDER

st.header("Content Strategy")

if "results" not in st.session_state:
    st.warning("Go to the home page first to load data.")
    st.stop()

results = st.session_state["results"]
df = st.session_state["filtered_df"]
sel_brands = st.session_state["sel_brands"]
order = [b for b in BRAND_ORDER if b in sel_brands]

# ── Theme × Brand heatmap ─────────────────────────────────────────────

st.subheader("Content Theme Performance Heatmap (Avg ER %)")

all_themes = sorted(set(df["content_theme"].dropna().unique()))
brands_for_hm = order

matrix, annotations = [], []
for brand in brands_for_hm:
    row = []
    for theme in all_themes:
        sub = df[(df["brand"] == brand) & (df["content_theme"] == theme)]
        er = round(sub["engagement_rate"].mean(), 2) if len(sub) else 0
        row.append(er)
    matrix.append(row)

fig = go.Figure(go.Heatmap(
    z=matrix, x=all_themes, y=brands_for_hm,
    colorscale="YlGnBu", texttemplate="%{z:.1f}",
    colorbar=dict(title="ER %"),
))
fig.update_layout(height=max(350, 50 * len(brands_for_hm)), template=CHART_TEMPLATE,
                  font=CHART_FONT, xaxis_tickangle=-40, margin=dict(b=120))
st.plotly_chart(fig, use_container_width=True)

# ── Caption analysis ──────────────────────────────────────────────────

st.subheader("Caption Analysis")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Caption Word Count by Brand**")
    fig_box = px.box(df[df["brand"].isin(sel_brands)], x="brand", y="caption_word_count",
                     color="brand", color_discrete_map=BRAND_COLORS,
                     category_orders={"brand": order},
                     labels={"caption_word_count": "Word Count", "brand": ""},
                     template=CHART_TEMPLATE)
    fig_box.update_layout(showlegend=False, height=380, font=CHART_FONT)
    st.plotly_chart(fig_box, use_container_width=True)

with col2:
    st.markdown("**Avg Emoji Usage per Post**")
    emoji_data = df[df["brand"].isin(sel_brands)].groupby("brand")["emoji_count_in_caption"].mean().reindex(order).fillna(0).reset_index()
    emoji_data.columns = ["brand", "avg_emojis"]
    fig_em = px.bar(emoji_data, x="brand", y="avg_emojis",
                    color="brand", color_discrete_map=BRAND_COLORS,
                    labels={"avg_emojis": "Avg Emojis", "brand": ""},
                    template=CHART_TEMPLATE)
    fig_em.update_layout(showlegend=False, height=380, font=CHART_FONT)
    st.plotly_chart(fig_em, use_container_width=True)

# ── Tone distribution ─────────────────────────────────────────────────

st.subheader("Caption Tone Distribution")

tone_data = (
    df[df["brand"].isin(sel_brands) & df["caption_tone"].notna()]
    .groupby(["brand", "caption_tone"]).size().reset_index(name="count")
)
totals = tone_data.groupby("brand")["count"].transform("sum")
tone_data["pct"] = (tone_data["count"] / totals * 100).round(1)

fig_tone = px.bar(tone_data, x="brand", y="pct", color="caption_tone",
                  barmode="stack", category_orders={"brand": order},
                  labels={"pct": "% of Posts", "brand": "", "caption_tone": "Tone"},
                  template=CHART_TEMPLATE, color_discrete_sequence=px.colors.qualitative.Pastel)
fig_tone.update_layout(font=CHART_FONT, height=420, legend=dict(orientation="h", y=-0.25))
st.plotly_chart(fig_tone, use_container_width=True)

# ── CTA effectiveness ─────────────────────────────────────────────────

st.subheader("CTA Effectiveness (Avg ER by CTA Type)")

cta_data = df[df["brand"].isin(sel_brands) & df["cta_type"].notna() & (df["cta_type"] != "")]
cta_er = cta_data.groupby(["cta_type", "platform"])["engagement_rate"].mean().reset_index()

if len(cta_er):
    fig_cta = px.bar(cta_er, x="cta_type", y="engagement_rate", color="platform",
                     barmode="group",
                     color_discrete_map={"Instagram": "#C13584", "TikTok": "#EE1D52"},
                     labels={"engagement_rate": "Avg ER %", "cta_type": "", "platform": "Platform"},
                     template=CHART_TEMPLATE)
    fig_cta.update_layout(font=CHART_FONT, height=400, xaxis_tickangle=-30,
                          legend=dict(orientation="h", y=1.12))
    st.plotly_chart(fig_cta, use_container_width=True)

# ── Visual style performance ──────────────────────────────────────────

st.subheader("Visual Style Performance")

style_data = (
    df[df["brand"].isin(sel_brands) & df["visual_style"].notna()]
    .groupby(["visual_style", "brand"])["engagement_rate"].mean().reset_index()
)

if len(style_data):
    fig_vs = px.bar(style_data, x="visual_style", y="engagement_rate", color="brand",
                    barmode="group", color_discrete_map=BRAND_COLORS,
                    category_orders={"brand": order},
                    labels={"engagement_rate": "Avg ER %", "visual_style": "", "brand": "Brand"},
                    template=CHART_TEMPLATE)
    fig_vs.update_layout(font=CHART_FONT, height=420, xaxis_tickangle=-20,
                         legend=dict(orientation="h", y=-0.20))
    st.plotly_chart(fig_vs, use_container_width=True)
