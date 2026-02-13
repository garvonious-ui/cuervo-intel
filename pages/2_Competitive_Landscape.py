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

from config import BRAND_COLORS, CHART_TEMPLATE, CHART_FONT, BRAND_ORDER, CUSTOM_CSS
from autostrat_loader import (
    has_autostrat_data, get_report, get_all_brand_mentions,
)
from autostrat_components import (
    render_section_label, render_territory_cards, render_nopd_cards,
    render_narrative_card, render_brand_mention, render_verbatim_quotes,
)

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
ER_TARGET = 3.0

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
tab_overview, tab_gaps, tab_intel = st.tabs([
    "Competitive Overview", "Content Gaps", "Competitor Intelligence",
])

# ══════════════════════════════════════════════════════════════════════
# TAB 1 — Competitive Overview
# ══════════════════════════════════════════════════════════════════════

with tab_overview:

    # ── Comparison Table ───────────────────────────────────────────────
    st.subheader("Side-by-Side Metrics")

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

        rows.append({
            "Brand": brand,
            "Followers": followers,
            "Posts": len(plat_df),
            "Posts/Week": round(ppw, 1),
            "Avg ER %": round(avg_er, 2),
            "Avg Likes": int(_likes),
            "Collab %": cr.get("collab_pct", 0),
        })

    comp_tbl = pd.DataFrame(rows)

    def highlight_cuervo(row):
        return ["background-color: #FDEBD6" if row["Brand"] == CUERVO else "" for _ in row]

    def color_er(val):
        if isinstance(val, (int, float)):
            if val >= 4:
                return "background-color: #C8E6C9"
            elif val >= 2.5:
                return "background-color: #FDEBD6"
            elif val > 0:
                return "background-color: #FFCDD2"
        return ""

    styled_tbl = (
        comp_tbl.style
        .apply(highlight_cuervo, axis=1)
        .map(color_er, subset=["Avg ER %"])
        .format({"Followers": "{:,.0f}", "Avg Likes": "{:,.0f}",
                 "Avg ER %": "{:.2f}", "Posts/Week": "{:.1f}",
                 "Collab %": "{:.1f}"})
    )
    st.dataframe(styled_tbl, width="stretch", hide_index=True, height=320)

    st.markdown("---")

    # ── "Who's Winning & Why" ──────────────────────────────────────────
    st.subheader("Who's Winning & Why")

    brand_ers = df.groupby("brand")["engagement_rate"].mean().dropna()
    brand_ers = brand_ers[brand_ers > 0].sort_values(ascending=False)
    top3 = brand_ers.head(3)

    for rank, (brand, er) in enumerate(top3.items(), 1):
        brand_df = df[df["brand"] == brand]
        cr = results["creators"].get(brand, {})
        collab_pct = cr.get("collab_pct", 0)
        top_theme = brand_df.groupby("content_theme")["engagement_rate"].mean()
        best_theme = top_theme.idxmax() if len(top_theme) else "N/A"
        reel_pct = len(brand_df[brand_df["post_type"] == "Reel"]) / max(len(brand_df), 1) * 100

        st.markdown(
            f"**#{rank} {brand}** — {er:.2f}% ER | "
            f"Top theme: {best_theme} | Reel mix: {reel_pct:.0f}% | Creator collab: {collab_pct:.0f}%"
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
                     annotation_text="3% Social Brief target",
                     annotation_position="top right")
    cat_avg = er_data[er_data["engagement_rate"] > 0]["engagement_rate"].mean()
    fig_er.add_hline(y=cat_avg, line_dash="dot", line_color="gray",
                     annotation_text=f"Category avg {cat_avg:.2f}%",
                     annotation_position="bottom right")
    st.plotly_chart(fig_er, width="stretch")



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


# ══════════════════════════════════════════════════════════════════════
# TAB 3 — Competitor Intelligence
# ══════════════════════════════════════════════════════════════════════

with tab_intel:

    autostrat = st.session_state.get("autostrat", {})
    _has_autostrat = has_autostrat_data(autostrat)

    if not _has_autostrat:
        st.info("No autostrat reports loaded. Import PDFs from the home page to see "
                "competitor intelligence from Cazadores and Hornitos reports.")
    else:
        # ── Cazadores Intel ────────────────────────────────────────────
        caz_report = get_report(autostrat, "instagram_hashtags", "cazadores")
        horn_report = get_report(autostrat, "instagram_hashtags", "hornitos")

        competitor_reports = []
        if caz_report:
            competitor_reports.append(("Cazadores (#cazadores)", caz_report))
        if horn_report:
            competitor_reports.append(("Hornitos (#hornitos)", horn_report))

        if not competitor_reports:
            st.info("No competitor autostrat reports found. Import cazadores or hornitos PDFs.")
        else:
            for report_label, report in competitor_reports:
                st.subheader(report_label)

                # Executive Summary
                es = report.get("executive_summary", {})
                if es.get("key_insights"):
                    render_section_label("Key Insights")
                    cols = st.columns(min(len(es["key_insights"]), 2))
                    for i, insight in enumerate(es["key_insights"][:4]):
                        with cols[i % len(cols)]:
                            render_narrative_card(f"Insight {i+1}", insight)

                # Audience Profile (NOPD)
                ap = report.get("audience_profile", {})
                if any(ap.get(k) for k in ["needs", "objections", "desires", "pain_points"]):
                    render_section_label("Audience Profile (NOPD)")
                    if ap.get("summary"):
                        st.markdown(ap["summary"])
                    render_nopd_cards(ap)

                # Opportunities
                ha = report.get("hashtag_analysis", {})
                if ha.get("opportunities"):
                    render_section_label("Opportunities")
                    for opp in ha["opportunities"][:4]:
                        st.success(opp)

                # How to Win
                hw = report.get("how_to_win", {})
                if hw.get("territories"):
                    render_section_label("How to Win")
                    if hw.get("summary"):
                        st.markdown(f"*{hw['summary']}*")
                    render_territory_cards(hw["territories"][:5])

                st.markdown("---")

        # ── Competitive Brand Mentions ─────────────────────────────────
        all_mentions = get_all_brand_mentions(autostrat)
        if all_mentions:
            render_section_label("Competitive Brand Mentions")
            st.caption("How brands appear in the conversation space across all reports")
            for mention in all_mentions[:8]:
                render_brand_mention(mention)
