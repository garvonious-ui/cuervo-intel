"""
Page 2: Competitive Landscape — "The Window"
What competitors are doing. All 13 brands, sidebar filters apply.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from config import BRAND_COLORS, CHART_TEMPLATE, CHART_FONT, BRAND_ORDER, CUSTOM_CSS, SOCIAL_BRIEF_TARGETS

st.logo("logo.png")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
st.header("Competitive Landscape")
st.caption("What competitors are doing — sidebar filters apply here.")

if "results" not in st.session_state:
    st.warning("Go to the home page first to load data.")
    st.stop()

results = st.session_state["results"]
df = st.session_state["filtered_df"]
full_df = st.session_state["df"]
sel_brands = st.session_state["sel_brands"]
order = [b for b in BRAND_ORDER if b in sel_brands]

CUERVO = "Jose Cuervo"
ER_TARGET = SOCIAL_BRIEF_TARGETS["er"]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
tab_overview, tab_gaps = st.tabs([
    "Competitive Overview", "Content Gaps",
])

# ══════════════════════════════════════════════════════════════════════
# TAB 1 — Competitive Overview
# ══════════════════════════════════════════════════════════════════════

with tab_overview:

    # ── Comparison Table ───────────────────────────────────────────────
    st.subheader("Side-by-Side Metrics")

    benchmark = results.get("benchmark", {})
    has_bench = bool(benchmark)

    rows = []
    for brand in order:
        plat_df = df[df["brand"] == brand]
        eng = results["engagement"].get(brand, {})
        freq_b = results["frequency"].get(brand, {})
        cr = results["creators"].get(brand, {})

        followers = sum(eng.get(p, {}).get("followers", 0) for p in ["Instagram", "TikTok"])
        avg_er = plat_df["engagement_rate"].mean() if len(plat_df) else 0
        avg_er = 0 if pd.isna(avg_er) else avg_er
        ppw = sum(freq_b.get(p, {}).get("posts_per_week", 0) for p in ["Instagram", "TikTok"])
        _likes = plat_df["likes"].mean() if len(plat_df) else 0
        _likes = 0 if pd.isna(_likes) else _likes

        row_data = {
            "Brand": brand,
            "Followers": followers,
            "Posts": len(plat_df),
            "Posts/Week": round(ppw, 1),
            "Avg ER %": round(avg_er, 2),
            "Avg Likes": int(_likes),
            "Collab %": cr.get("collab_pct", 0),
        }

        # Add benchmark columns when benchmark data is available
        if has_bench:
            ig_eng = eng.get("Instagram", {})
            row_data["ER by Views %"] = round(ig_eng.get("benchmark_er_by_views", 0), 2)
            row_data["Reels"] = ig_eng.get("benchmark_reels_count", 0)
            row_data["Avg #tags"] = round(ig_eng.get("benchmark_avg_hashtags", 0), 1)

        rows.append(row_data)

    comp_tbl = pd.DataFrame(rows)

    def highlight_cuervo(row):
        return ["background-color: #FDEBD6" if row["Brand"] == CUERVO else "" for _ in row]

    def color_er(val):
        if isinstance(val, (int, float)):
            if val >= ER_TARGET * 1.5:
                return "background-color: #C8E6C9"
            elif val >= ER_TARGET * 0.85:
                return "background-color: #FDEBD6"
            elif val > 0:
                return "background-color: #FFCDD2"
        return ""

    er_cols = ["Avg ER %"]
    fmt = {"Followers": "{:,.0f}", "Avg Likes": "{:,.0f}",
           "Avg ER %": "{:.2f}", "Posts/Week": "{:.1f}",
           "Collab %": "{:.1f}"}
    if has_bench:
        er_cols.append("ER by Views %")
        fmt["ER by Views %"] = "{:.2f}"
        fmt["Avg #tags"] = "{:.1f}"

    styled_tbl = (
        comp_tbl.style
        .apply(highlight_cuervo, axis=1)
        .map(color_er, subset=er_cols)
        .format(fmt)
    )
    st.dataframe(styled_tbl, width="stretch", hide_index=True, height=320)

    if has_bench:
        bench_meta = next(iter(benchmark.values()), {})
        st.caption(f"ER by Views % from external benchmark ({bench_meta.get('date_range', 'N/A')}). "
                   f"Avg ER % from Sprout post-level data.")

    st.markdown("---")

    # ── "Who's Winning & Why" ──────────────────────────────────────────
    st.subheader("Who's Winning & Why")

    brand_ers = df.groupby("brand")["engagement_rate"].mean().dropna()
    brand_ers = brand_ers[brand_ers > 0].sort_values(ascending=False)
    top3 = brand_ers.head(3)

    for rank, (brand, er) in enumerate(top3.items(), 1):
        brand_df = df[df["brand"] == brand]
        top_theme = brand_df.groupby("content_theme")["engagement_rate"].mean()
        best_theme = top_theme.idxmax() if len(top_theme) else "N/A"
        reel_pct = len(brand_df[brand_df["post_type"] == "Reel"]) / max(len(brand_df), 1) * 100

        st.markdown(
            f"**#{rank} {brand}** — {er:.2f}% ER | "
            f"Top theme: {best_theme} | Reel mix: {reel_pct:.0f}%"
        )

    cuervo_er = brand_ers.get(CUERVO, 0)
    cuervo_rank = list(brand_ers.index).index(CUERVO) + 1 if CUERVO in brand_ers.index else len(brand_ers)
    st.info(f"**Cuervo ranks #{cuervo_rank}** out of {len(brand_ers)} brands at {cuervo_er:.2f}% ER. "
            f"The top brand beats Cuervo by {top3.iloc[0] - cuervo_er:.2f}pp." if len(top3) and cuervo_er < top3.iloc[0] else
            f"**Cuervo leads** at {cuervo_er:.2f}% ER.")

    st.markdown("---")

    # ── ER Comparison Bar Chart ────────────────────────────────────────
    st.subheader("Engagement Rate by Brand")

    er_data = df.groupby("brand")["engagement_rate"].mean().reset_index()
    er_data = er_data[er_data["brand"].isin(sel_brands)]

    fig_er = px.bar(er_data, x="brand", y="engagement_rate",
                    color="brand", color_discrete_map=BRAND_COLORS,
                    category_orders={"brand": order},
                    labels={"engagement_rate": "Avg ER %", "brand": ""},
                    template=CHART_TEMPLATE)
    fig_er.update_layout(font=CHART_FONT, height=420, showlegend=False)
    fig_er.add_hline(y=ER_TARGET, line_dash="dash", line_color="#D9534F",
                     annotation_text=f"{ER_TARGET}% Social Brief target",
                     annotation_position="top right")
    cat_avg = er_data[er_data["engagement_rate"] > 0]["engagement_rate"].mean()
    fig_er.add_hline(y=cat_avg, line_dash="dot", line_color="gray",
                     annotation_text=f"Category avg {cat_avg:.2f}%",
                     annotation_position="bottom right")
    st.plotly_chart(fig_er, width="stretch")

    st.markdown("---")

    # ── Top 10 Posts per Brand/Platform ──────────────────────────────
    st.subheader("Top 10 Posts by Brand")
    st.caption("Best-performing content per brand — study what's working")

    top10_brand = st.selectbox("Select brand", order, key="top10_brand_sel")
    top10_plat = st.radio("Platform", ["Instagram", "TikTok"], horizontal=True, key="top10_plat_sel")

    top10_data = results["engagement"].get(top10_brand, {}).get(top10_plat, {}).get("top_10_posts", [])

    if top10_data:
        top10_rows = []
        for i, p in enumerate(top10_data, 1):
            top10_rows.append({
                "#": i,
                "Caption": (p.get("caption_preview", "") or "")[:60] + ("..." if len(p.get("caption_preview", "")) > 60 else ""),
                "ER %": round(p.get("engagement_rate", 0), 2),
                "Likes": p.get("likes", 0),
                "Comments": p.get("comments", 0),
                "Views": p.get("views", 0),
                "Type": p.get("type", ""),
                "Theme": p.get("theme", ""),
                "Date": p.get("date", ""),
            })
        top10_df = pd.DataFrame(top10_rows)

        def color_top10_er(val):
            if isinstance(val, (int, float)):
                if val >= 4:
                    return "background-color: #C8E6C9"
                elif val >= 2.5:
                    return "background-color: #FDEBD6"
                elif val > 0:
                    return "background-color: #FFCDD2"
            return ""

        styled_top10 = top10_df.style.map(color_top10_er, subset=["ER %"]).format({
            "Likes": "{:,.0f}", "Comments": "{:,.0f}", "Views": "{:,.0f}", "ER %": "{:.2f}"
        })
        st.dataframe(styled_top10, width="stretch", hide_index=True, height=400)

        # So What
        best_type = pd.DataFrame(top10_rows).groupby("Type")["ER %"].mean()
        best_type_name = best_type.idxmax() if len(best_type) else "N/A"
        avg_top10_er = sum(r["ER %"] for r in top10_rows) / len(top10_rows)
        st.info(f"**{top10_brand}'s top 10** average {avg_top10_er:.2f}% ER on {top10_plat}. "
                f"Best-performing format: **{best_type_name}**. "
                f"{'Study their approach for Cuervo adaptation.' if top10_brand != CUERVO else 'Keep doubling down on what works.'}")
    else:
        st.info(f"No {top10_plat} post data available for {top10_brand}.")


# ══════════════════════════════════════════════════════════════════════
# TAB 2 — Content Gaps
# ══════════════════════════════════════════════════════════════════════

with tab_gaps:

    cuervo_df = full_df[full_df["brand"] == CUERVO]
    comp_df = full_df[full_df["brand"] != CUERVO]

    # ── Content Gap Analysis ───────────────────────────────────────────
    st.subheader("Content Gap Analysis: Cuervo vs Category")
    st.caption("Where competitors invest more content — and whether those themes drive higher ER")

    all_themes = sorted(full_df["content_theme"].dropna().unique())
    cuervo_total = len(cuervo_df) or 1
    comp_total = len(comp_df) or 1

    gap_rows = []
    for theme in all_themes:
        c_pct = len(cuervo_df[cuervo_df["content_theme"] == theme]) / cuervo_total * 100
        cat_pct = len(comp_df[comp_df["content_theme"] == theme]) / comp_total * 100
        c_er = cuervo_df[cuervo_df["content_theme"] == theme]["engagement_rate"].mean()
        cat_er = comp_df[comp_df["content_theme"] == theme]["engagement_rate"].mean()
        gap_rows.append({
            "theme": theme,
            "Cuervo %": round(c_pct, 1),
            "Category %": round(cat_pct, 1),
            "gap": round(cat_pct - c_pct, 1),
            "Cuervo ER": round(c_er, 2) if pd.notna(c_er) else 0,
            "Category ER": round(cat_er, 2) if pd.notna(cat_er) else 0,
        })

    gap_df = pd.DataFrame(gap_rows).sort_values("gap", ascending=False)

    fig_gap = go.Figure()
    fig_gap.add_trace(go.Bar(x=gap_df["theme"], y=gap_df["Cuervo %"],
                             name="Cuervo", marker_color=BRAND_COLORS[CUERVO]))
    fig_gap.add_trace(go.Bar(x=gap_df["theme"], y=gap_df["Category %"],
                             name="Category Avg", marker_color="#A3C4D9"))
    fig_gap.update_layout(barmode="group", template=CHART_TEMPLATE, font=CHART_FONT,
                          height=420, xaxis_tickangle=-35, yaxis_title="% of Content",
                          legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig_gap, width="stretch")

    # So What — biggest gaps
    top_gaps = gap_df[gap_df["gap"] > 0].head(3)
    if len(top_gaps):
        st.markdown("**Biggest content gaps (themes competitors use more):**")
        for _, row in top_gaps.iterrows():
            st.markdown(f"- **{row['theme']}**: Category at {row['Category %']}% vs Cuervo {row['Cuervo %']}% "
                        f"(+{row['gap']}% gap) — Category ER: {row['Category ER']}%")

    st.markdown("---")

    # ── Format Strategy Comparison ─────────────────────────────────────
    st.subheader("Format Strategy Comparison")

    type_data = df[df["brand"].isin(sel_brands)].groupby(["brand", "post_type"]).size().reset_index(name="count")
    totals = type_data.groupby("brand")["count"].transform("sum")
    type_data["pct"] = (type_data["count"] / totals * 100).round(1)

    fig_ct = px.bar(type_data, x="brand", y="pct", color="post_type",
                    barmode="stack", category_orders={"brand": order},
                    labels={"pct": "% of Posts", "brand": "", "post_type": "Type"},
                    template=CHART_TEMPLATE, color_discrete_sequence=px.colors.qualitative.Set2)
    fig_ct.update_layout(font=CHART_FONT, height=400, legend=dict(orientation="h", y=1.12))
    st.plotly_chart(fig_ct, width="stretch")

    st.markdown("---")

    # ── Engagement Rate by Format (Cross-Brand) ─────────────────────
    st.subheader("Engagement Rate by Format — Cross-Brand")
    st.caption("Which content formats drive the highest ER for each brand")

    er_by_fmt_rows = []
    for brand in order:
        for plat in ["Instagram", "TikTok"]:
            eng_by_type = results["engagement"].get(brand, {}).get(plat, {}).get("engagement_by_type", {})
            for fmt, er_val in eng_by_type.items():
                er_by_fmt_rows.append({"Brand": brand, "Format": fmt, "ER %": round(er_val, 2)})

    if er_by_fmt_rows:
        er_fmt_df = pd.DataFrame(er_by_fmt_rows)
        # Aggregate across platforms
        er_fmt_agg = er_fmt_df.groupby(["Brand", "Format"])["ER %"].mean().reset_index()

        fig_er_fmt = px.bar(er_fmt_agg, x="Brand", y="ER %", color="Format",
                            barmode="group",
                            category_orders={"Brand": order},
                            labels={"ER %": "Avg ER %", "Brand": ""},
                            template=CHART_TEMPLATE,
                            color_discrete_sequence=["#F8C090", "#2ea3f2", "#7B6B63", "#D4956A", "#C9A87E"])
        fig_er_fmt.add_hline(y=ER_TARGET, line_dash="dash", line_color="#D9534F",
                             annotation_text=f"{ER_TARGET}% target", annotation_position="top right")
        fig_er_fmt.update_layout(font=CHART_FONT, height=420,
                                 legend=dict(orientation="h", y=1.12))
        st.plotly_chart(fig_er_fmt, width="stretch")

        # So What
        best_fmt_overall = er_fmt_agg.groupby("Format")["ER %"].mean().sort_values(ascending=False)
        if len(best_fmt_overall):
            top_fmt = best_fmt_overall.index[0]
            top_fmt_er = best_fmt_overall.iloc[0]
            st.info(f"**{top_fmt}** drives the highest average ER across brands at {top_fmt_er:.2f}%. "
                    f"Ensure Cuervo's content mix prioritizes this format.")
    else:
        st.info("No engagement-by-format data available.")

    st.markdown("---")

    # ── Posting Frequency Comparison ───────────────────────────────────
    st.subheader("Posting Frequency (posts/week)")

    freq = results["frequency"]
    freq_rows = []
    for brand in sel_brands:
        for plat in ["Instagram", "TikTok"]:
            ppw = freq.get(brand, {}).get(plat, {}).get("posts_per_week", 0)
            freq_rows.append({"brand": brand, "platform": plat, "posts_per_week": ppw})
    freq_df = pd.DataFrame(freq_rows)

    fig_freq = px.bar(freq_df, x="brand", y="posts_per_week", color="platform",
                      barmode="group", color_discrete_map={"Instagram": "#D4956A", "TikTok": "#2ea3f2"},
                      category_orders={"brand": order},
                      labels={"posts_per_week": "Posts / Week", "brand": ""},
                      template=CHART_TEMPLATE)
    fig_freq.update_layout(font=CHART_FONT, height=380, legend=dict(orientation="h", y=1.12))
    st.plotly_chart(fig_freq, width="stretch")

    st.markdown("---")

    # ── Creator Collab Engagement Lift ───────────────────────────────
    st.subheader("Creator Collab Engagement Lift")
    st.caption("Does working with creators boost engagement? Collab vs organic ER comparison.")

    collab_rows = []
    for brand in order:
        cr = results["creators"].get(brand, {})
        collab_er = cr.get("avg_collab_engagement_rate", 0)
        non_collab_er = cr.get("avg_non_collab_engagement_rate", 0)
        lift = cr.get("collab_engagement_lift", 0)
        collab_pct = cr.get("collab_pct", 0)
        if collab_er > 0 or non_collab_er > 0:
            collab_rows.append({
                "Brand": brand,
                "Collab ER %": round(collab_er, 2),
                "Organic ER %": round(non_collab_er, 2),
                "Lift": round(lift, 2),
                "Collab %": round(collab_pct, 1),
            })

    if collab_rows:
        collab_df = pd.DataFrame(collab_rows)

        fig_collab = go.Figure()
        fig_collab.add_trace(go.Bar(
            x=collab_df["Brand"], y=collab_df["Collab ER %"],
            name="Creator Collab ER", marker_color="#2ea3f2",
            text=collab_df["Collab ER %"], textposition="outside", texttemplate="%{text:.2f}%"
        ))
        fig_collab.add_trace(go.Bar(
            x=collab_df["Brand"], y=collab_df["Organic ER %"],
            name="Organic ER", marker_color="#C9A87E",
            text=collab_df["Organic ER %"], textposition="outside", texttemplate="%{text:.2f}%"
        ))
        fig_collab.update_layout(barmode="group", template=CHART_TEMPLATE, font=CHART_FONT,
                                 height=420, legend=dict(orientation="h", y=1.12),
                                 yaxis_title="Avg ER %")
        st.plotly_chart(fig_collab, width="stretch")

        # Lift callout cards
        positive_lift = [r for r in collab_rows if r["Lift"] > 0]
        if positive_lift:
            lift_cols = st.columns(min(len(positive_lift), 4))
            for i, row in enumerate(sorted(positive_lift, key=lambda x: x["Lift"], reverse=True)[:4]):
                with lift_cols[i % len(lift_cols)]:
                    color = BRAND_COLORS.get(row["Brand"], "#888")
                    st.markdown(f"""
                    <div style="background: white; border-radius: 8px; padding: 12px;
                                border-top: 3px solid {color}; text-align: center;
                                border: 1px solid #E0D8D0;">
                        <strong>{row['Brand']}</strong><br>
                        <span style="font-size: 1.6rem; color: #2ea3f2;">+{row['Lift']:.2f}%</span><br>
                        <span style="font-size: 0.8rem; color: #777;">collab lift | {row['Collab %']:.0f}% collab rate</span>
                    </div>
                    """, unsafe_allow_html=True)

        # So What
        cuervo_lift = next((r["Lift"] for r in collab_rows if r["Brand"] == CUERVO), 0)
        avg_lift = sum(r["Lift"] for r in collab_rows) / len(collab_rows)
        if cuervo_lift > 0:
            st.info(f"**Creator collabs boost Cuervo's ER by +{cuervo_lift:.2f}pp.** "
                    f"Category avg lift: {avg_lift:+.2f}pp. Keep investing in creator partnerships.")
        else:
            st.info(f"**Cuervo's collab lift: {cuervo_lift:+.2f}pp.** "
                    f"Category avg: {avg_lift:+.2f}pp. Opportunity to improve creator selection and content style.")
    else:
        st.info("No creator collaboration data available.")

    st.markdown("---")

    # ── "What to Steal" Cards ──────────────────────────────────────────
    st.subheader("What to Steal")
    st.caption("Specific tactics from brands outperforming Cuervo")

    cuervo_er_val = full_df[full_df["brand"] == CUERVO]["engagement_rate"].mean()
    cuervo_er_val = 0 if pd.isna(cuervo_er_val) else cuervo_er_val

    all_brand_ers = full_df.groupby("brand")["engagement_rate"].mean().dropna()
    all_brand_ers = all_brand_ers[all_brand_ers > 0]
    beating_brands = all_brand_ers[all_brand_ers > cuervo_er_val].index.tolist() if CUERVO in full_df["brand"].values else []
    beating_brands = [b for b in beating_brands if b != CUERVO]

    if beating_brands:
        steal_cols = st.columns(min(len(beating_brands), 3))
        for i, brand in enumerate(beating_brands[:6]):
            bdf = full_df[full_df["brand"] == brand]
            brand_er = bdf["engagement_rate"].mean()
            cr = results["creators"].get(brand, {})
            top_theme_s = bdf.groupby("content_theme")["engagement_rate"].mean()
            best_theme_s = top_theme_s.idxmax() if len(top_theme_s) else "N/A"
            best_theme_er = top_theme_s.max() if len(top_theme_s) else 0
            reel_pct = len(bdf[bdf["post_type"] == "Reel"]) / max(len(bdf), 1) * 100
            collab_pct = cr.get("collab_pct", 0)

            with steal_cols[i % len(steal_cols)]:
                st.markdown(f"""
                <div style="background: white; border-radius: 10px; padding: 16px;
                            margin-bottom: 12px; border: 1px solid #E0D8D0;
                            border-top: 3px solid {BRAND_COLORS.get(brand, '#888')};">
                    <h4 style="font-family: 'Barlow Condensed', sans-serif; font-weight: 700;
                               color: #333; margin: 0 0 8px 0;">{brand}</h4>
                    <p style="font-size: 0.9rem; color: #555; margin: 0;">
                        <strong>{brand_er:.2f}% ER</strong> (+{brand_er - cuervo_er_val:.2f}pp vs Cuervo)<br>
                        Top theme: <strong>{best_theme_s}</strong> ({best_theme_er:.2f}% ER)<br>
                        Reel mix: <strong>{reel_pct:.0f}%</strong><br>
                        Creator collab: <strong>{collab_pct:.0f}%</strong>
                    </p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.success("Cuervo is outperforming all competitors — keep it up!")
