import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from config import BRAND_COLORS, CHART_TEMPLATE, CHART_FONT, BRAND_ORDER, CUSTOM_CSS

st.logo("logo.png")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
st.header("Content & Engagement")

if "results" not in st.session_state:
    st.warning("Go to the home page first to load data.")
    st.stop()

results = st.session_state["results"]
df = st.session_state["filtered_df"]
sel_brands = st.session_state["sel_brands"]
order = [b for b in BRAND_ORDER if b in sel_brands]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
tab_content, tab_engage = st.tabs(["Content Strategy", "Engagement Analysis"])

# ══════════════════════════════════════════════════════════════════════
# TAB 1 — Content Strategy (formerly Page 3)
# ══════════════════════════════════════════════════════════════════════

with tab_content:

    # ── Content Format Breakdown ──────────────────────────────────────
    st.subheader("Content Format Breakdown")
    st.caption("How each brand distributes content across Reels, Carousels, and Static Images — and which formats drive the highest engagement")

    format_data = (
        df[df["brand"].isin(sel_brands)]
        .groupby(["brand", "post_type"]).size().reset_index(name="count")
    )
    totals = format_data.groupby("brand")["count"].transform("sum")
    format_data["pct"] = (format_data["count"] / totals * 100).round(1)

    col_fmt1, col_fmt2 = st.columns(2)

    with col_fmt1:
        st.markdown("**Format Mix by Brand (%)**")
        fig_fmix = px.bar(format_data, x="brand", y="pct", color="post_type",
                          barmode="stack", category_orders={"brand": order},
                          labels={"pct": "% of Posts", "brand": "", "post_type": "Format"},
                          template=CHART_TEMPLATE,
                          color_discrete_sequence=["#F8C090", "#2ea3f2", "#7B6B63", "#D4956A", "#A3C4D9"])
        fig_fmix.update_layout(font=CHART_FONT, height=420, legend=dict(orientation="h", y=-0.18))
        st.plotly_chart(fig_fmix, use_container_width=True)

    with col_fmt2:
        st.markdown("**Avg Engagement Rate by Format**")
        format_er = (
            df[df["brand"].isin(sel_brands)]
            .groupby(["brand", "post_type"])["engagement_rate"].mean().reset_index()
        )
        format_er = format_er[(format_er["engagement_rate"] > 0) & (format_er["post_type"] != "Video")]
        if len(format_er):
            fig_fer = px.bar(format_er, x="post_type", y="engagement_rate", color="brand",
                             barmode="group", color_discrete_map=BRAND_COLORS,
                             category_orders={"brand": order},
                             labels={"engagement_rate": "Avg ER %", "post_type": "", "brand": "Brand"},
                             template=CHART_TEMPLATE, text_auto=".2f")
            fig_fer.update_layout(font=CHART_FONT, height=420, legend=dict(orientation="h", y=-0.18))
            st.plotly_chart(fig_fer, use_container_width=True)
        else:
            st.info("No engagement rate data available for format comparison.")

    # Format insights callout
    cuervo_fmts = df[df["brand"] == "Jose Cuervo"]
    if len(cuervo_fmts):
        cuervo_total = len(cuervo_fmts)
        reel_pct = len(cuervo_fmts[cuervo_fmts["post_type"] == "Reel"]) / cuervo_total * 100
        carousel_pct = len(cuervo_fmts[cuervo_fmts["post_type"] == "Carousel"]) / cuervo_total * 100
        static_pct = len(cuervo_fmts[cuervo_fmts["post_type"] == "Static Image"]) / cuervo_total * 100

        cuervo_format_er = cuervo_fmts.groupby("post_type")["engagement_rate"].mean()
        cuervo_format_er = cuervo_format_er[cuervo_format_er > 0]
        best_format = cuervo_format_er.idxmax() if len(cuervo_format_er) else "N/A"
        best_format_er = cuervo_format_er.max() if len(cuervo_format_er) else 0

        insight_col1, insight_col2, insight_col3 = st.columns(3)
        with insight_col1:
            st.metric("Cuervo Reels", f"{reel_pct:.0f}%", help="% of Cuervo posts that are Reels")
        with insight_col2:
            st.metric("Cuervo Carousels", f"{carousel_pct:.0f}%", help="% of Cuervo posts that are Carousels")
        with insight_col3:
            st.metric("Best Format (ER)", f"{best_format}", delta=f"{best_format_er:.2f}% avg ER")

    st.markdown("---")

    # ── Theme × Brand heatmap ─────────────────────────────────────────
    st.subheader("Content Theme Performance Heatmap (Avg ER %)")

    all_themes = sorted(set(df["content_theme"].dropna().unique()))
    brands_for_hm = order

    matrix = []
    for brand in brands_for_hm:
        row = []
        for theme in all_themes:
            sub = df[(df["brand"] == brand) & (df["content_theme"] == theme)]
            _er = sub["engagement_rate"].mean() if len(sub) else 0
            er = round(_er, 2) if pd.notna(_er) else 0
            row.append(er)
        matrix.append(row)

    fig_hm_theme = go.Figure(go.Heatmap(
        z=matrix, x=all_themes, y=brands_for_hm,
        colorscale="YlGnBu", texttemplate="%{z:.1f}",
        colorbar=dict(title="ER %"),
    ))
    fig_hm_theme.update_layout(height=max(350, 50 * len(brands_for_hm)), template=CHART_TEMPLATE,
                               font=CHART_FONT, xaxis_tickangle=-40, margin=dict(b=120))
    st.plotly_chart(fig_hm_theme, use_container_width=True)

    # ── Caption analysis ──────────────────────────────────────────────
    st.subheader("Caption Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Avg Caption Word Count by Brand**")
        wc_data = (df[df["brand"].isin(sel_brands)]
                   .groupby("brand")["caption_word_count"].mean()
                   .reindex(order).fillna(0).reset_index())
        wc_data.columns = ["brand", "avg_words"]
        fig_box = px.bar(wc_data, x="avg_words", y="brand", orientation="h",
                         color="brand", color_discrete_map=BRAND_COLORS,
                         category_orders={"brand": order},
                         labels={"avg_words": "Avg Word Count", "brand": ""},
                         template=CHART_TEMPLATE, text_auto=".0f")
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

    # ── Tone distribution ─────────────────────────────────────────────
    st.subheader("Caption Tone Distribution")

    tone_data = (
        df[df["brand"].isin(sel_brands) & df["caption_tone"].notna()]
        .groupby(["brand", "caption_tone"]).size().reset_index(name="count")
    )
    totals_t = tone_data.groupby("brand")["count"].transform("sum")
    tone_data["pct"] = (tone_data["count"] / totals_t * 100).round(1)

    fig_tone = px.bar(tone_data, x="brand", y="pct", color="caption_tone",
                      barmode="stack", category_orders={"brand": order},
                      labels={"pct": "% of Posts", "brand": "", "caption_tone": "Tone"},
                      template=CHART_TEMPLATE, color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_tone.update_layout(font=CHART_FONT, height=420, legend=dict(orientation="h", y=-0.25))
    st.plotly_chart(fig_tone, use_container_width=True)

    # ── CTA effectiveness ─────────────────────────────────────────────
    st.subheader("CTA Effectiveness (Avg ER by CTA Type)")

    cta_data = df[df["brand"].isin(sel_brands) & df["cta_type"].notna() & (df["cta_type"] != "")]
    cta_er = cta_data.groupby(["cta_type", "platform"])["engagement_rate"].mean().reset_index()

    if len(cta_er):
        fig_cta = px.bar(cta_er, x="cta_type", y="engagement_rate", color="platform",
                         barmode="group",
                         color_discrete_map={"Instagram": "#D4956A", "TikTok": "#2ea3f2"},
                         labels={"engagement_rate": "Avg ER %", "cta_type": "", "platform": "Platform"},
                         template=CHART_TEMPLATE)
        fig_cta.update_layout(font=CHART_FONT, height=400, xaxis_tickangle=-30,
                              legend=dict(orientation="h", y=1.12))
        st.plotly_chart(fig_cta, use_container_width=True)

    # ── Visual style performance ──────────────────────────────────────
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

    # ── Posting Cadence by Format ────────────────────────────────────
    st.markdown("---")
    st.subheader("Posting Cadence by Format")
    st.caption("Weekly posting frequency broken down by content format — shows each brand's format velocity")

    freq = results["frequency"]
    cadence_rows = []
    for brand in sel_brands:
        for plat in st.session_state["sel_platforms"]:
            by_type = freq.get(brand, {}).get(plat, {}).get("by_content_type", {})
            for fmt, count in by_type.items():
                cadence_rows.append({
                    "brand": brand,
                    "platform": plat,
                    "format": fmt,
                    "posts_30d": count,
                    "posts_per_week": round(count / 4.3, 1),
                })

    if cadence_rows:
        cadence_df = pd.DataFrame(cadence_rows)
        cadence_agg = cadence_df.groupby(["brand", "format"])["posts_per_week"].sum().reset_index()

        fig_cadence = px.bar(cadence_agg, x="brand", y="posts_per_week", color="format",
                             barmode="stack", category_orders={"brand": order},
                             labels={"posts_per_week": "Posts / Week", "brand": "", "format": "Format"},
                             template=CHART_TEMPLATE,
                             color_discrete_sequence=["#F8C090", "#2ea3f2", "#7B6B63", "#D4956A", "#A3C4D9"])
        fig_cadence.update_layout(font=CHART_FONT, height=420, legend=dict(orientation="h", y=-0.18))
        st.plotly_chart(fig_cadence, use_container_width=True)

        cuervo_cadence = cadence_agg[cadence_agg["brand"] == "Jose Cuervo"]
        if len(cuervo_cadence):
            st.markdown("**Cuervo Format Cadence:**")
            for _, row in cuervo_cadence.iterrows():
                st.markdown(f"- **{row['format']}**: {row['posts_per_week']:.1f} posts/week")
    else:
        st.info("No posting cadence data available.")


# ══════════════════════════════════════════════════════════════════════
# TAB 2 — Engagement Analysis (formerly Page 4)
# ══════════════════════════════════════════════════════════════════════

with tab_engage:

    # ── Platform filter (applies to this tab) ─────────────────────────
    available_plats = sorted(df["platform"].unique().tolist())
    plat_options = ["All"] + available_plats
    sel_plat = st.selectbox("Platform", plat_options, key="deep_plat")
    eng_df = df.copy()
    if sel_plat != "All":
        eng_df = eng_df[eng_df["platform"] == sel_plat]

    if eng_df.empty:
        st.warning("No posts match the current filters.")
    else:

        # ── Engagement Signals Breakdown ──────────────────────────────
        st.subheader("Engagement Signals Breakdown")
        st.caption("Beyond likes — saves, shares, and comments indicate deeper audience connection and algorithmic favorability")

        signal_brands = [b for b in order if b in sel_brands]
        signal_rows = []
        for brand in signal_brands:
            bdf = eng_df[eng_df["brand"] == brand]
            if len(bdf) == 0:
                continue
            _safe_int = lambda s: int(s.mean()) if pd.notna(s.mean()) else 0
            signal_rows.append({
                "Brand": brand,
                "Avg Likes": _safe_int(bdf["likes"]),
                "Avg Comments": _safe_int(bdf["comments"]),
                "Avg Shares": _safe_int(bdf["shares"]),
                "Avg Saves": _safe_int(bdf["saves"]),
                "Avg Views": _safe_int(bdf["views"]),
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

        # ── ER by content type ────────────────────────────────────────
        st.subheader("Engagement Rate by Content Type")

        type_er = eng_df[eng_df["brand"].isin(sel_brands)].groupby(["brand", "post_type"])["engagement_rate"].mean().reset_index()
        if len(type_er):
            fig_ter = px.bar(type_er, x="post_type", y="engagement_rate", color="brand",
                             barmode="group", color_discrete_map=BRAND_COLORS,
                             category_orders={"brand": order},
                             labels={"engagement_rate": "Avg ER %", "post_type": "", "brand": "Brand"},
                             template=CHART_TEMPLATE)
            fig_ter.update_layout(font=CHART_FONT, height=400, legend=dict(orientation="h", y=1.12))
            st.plotly_chart(fig_ter, use_container_width=True)
        else:
            st.info("No data for the selected platform/brands.")

        # ── Posting schedule heatmap ──────────────────────────────────
        st.subheader("Posting Schedule Heatmap")

        sched_brand = st.selectbox("Brand", ["All Brands"] + order, key="sched_brand")

        if sched_brand == "All Brands":
            sched_df = eng_df[eng_df["brand"].isin(sel_brands)]
        else:
            sched_df = eng_df[eng_df["brand"] == sched_brand]

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

        # ── Top posts leaderboard ─────────────────────────────────────
        st.subheader("Top Performing Posts")

        top_n = st.slider("Show top", 10, 50, 20, step=5)

        top_df = (
            eng_df[eng_df["brand"].isin(sel_brands)]
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

        # ── Avg ER by Brand ──────────────────────────────────────────
        st.subheader("Avg Engagement Rate by Brand")

        er_brand = (eng_df[eng_df["brand"].isin(sel_brands)]
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
