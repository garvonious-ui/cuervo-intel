"""
Page 1: Cuervo Performance — "The Mirror"
What Cuervo is doing and how it's performing.
Uses UNFILTERED data — sidebar brand/platform filters do NOT apply.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from config import (
    BRAND_COLORS, CHART_TEMPLATE, CHART_FONT, BRAND_ORDER, CUSTOM_CSS,
    GOAT_CADENCE_TARGETS,
)
from autostrat_loader import (
    has_autostrat_data, get_report, get_all_how_to_win,
    get_all_audience_profiles, get_all_strategic_actions,
)
from autostrat_components import (
    render_section_label, render_territory_cards, render_nopd_cards,
    render_narrative_card, render_verbatim_quotes,
)

st.logo("logo.png")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
st.header("Cuervo Performance")
st.caption("How Jose Cuervo is performing — sidebar filters do not apply here.")

if "results" not in st.session_state:
    st.warning("Go to the home page first to load data.")
    st.stop()

results = st.session_state["results"]
df = st.session_state["df"]  # Unfiltered

CUERVO = "Jose Cuervo"
cuervo_df = df[df["brand"] == CUERVO]
cuervo_ig = cuervo_df[cuervo_df["platform"] == "Instagram"]
cuervo_tt = cuervo_df[cuervo_df["platform"] == "TikTok"]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
tab_kpi, tab_content, tab_audit = st.tabs([
    "KPI Dashboard", "Content Performance", "Self-Audit Intelligence",
])

# ══════════════════════════════════════════════════════════════════════
# TAB 1 — KPI Dashboard
# ══════════════════════════════════════════════════════════════════════

with tab_kpi:

    # ── Social Brief KPI Scorecard ─────────────────────────────────────
    st.subheader("Social Brief KPI Scorecard")

    # Compute KPIs
    cuervo_er = cuervo_df["engagement_rate"].mean()
    cuervo_er = 0 if pd.isna(cuervo_er) else cuervo_er

    # Follower growth — not available from static export, show followers
    eng = results["engagement"].get(CUERVO, {})
    ig_followers = eng.get("Instagram", {}).get("followers", 0)
    tt_followers = eng.get("TikTok", {}).get("followers", 0)

    # Avg Reel Views
    cuervo_reels = cuervo_df[cuervo_df["post_type"] == "Reel"]
    avg_reel_views = cuervo_reels["views"].mean() if len(cuervo_reels) else 0
    avg_reel_views = 0 if pd.isna(avg_reel_views) else avg_reel_views

    # Reel ratio (IG only)
    reel_ratio = len(cuervo_ig[cuervo_ig["post_type"] == "Reel"]) / max(len(cuervo_ig), 1) * 100

    # Posts/week
    freq = results["frequency"].get(CUERVO, {})
    ig_ppw = freq.get("Instagram", {}).get("posts_per_week", 0)
    tt_ppw = freq.get("TikTok", {}).get("posts_per_week", 0)

    # Brief targets
    ER_TARGET = 3.0
    REEL_VIEW_TARGET = 10000
    REEL_RATIO_TARGET = 50
    IG_PPW_TARGET = (4, 5)
    TT_PPW_TARGET = (3, 4)

    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.metric("Avg ER", f"{cuervo_er:.2f}%",
                  delta=f"{cuervo_er - ER_TARGET:+.2f}% vs 3% target")
    with k2:
        st.metric("IG Followers", f"{ig_followers:,}")
    with k3:
        st.metric("Avg Reel Views", f"{avg_reel_views:,.0f}",
                  delta=f"{avg_reel_views - REEL_VIEW_TARGET:+,.0f} vs 10K target")
    with k4:
        st.metric("Reel Ratio (IG)", f"{reel_ratio:.0f}%",
                  delta=f"{reel_ratio - REEL_RATIO_TARGET:+.0f}% vs 50% target")
    with k5:
        st.metric("IG Posts/Wk", f"{ig_ppw:.1f}",
                  delta=f"Target: {IG_PPW_TARGET[0]}-{IG_PPW_TARGET[1]}/wk",
                  delta_color="off")

    # ── "So What" Narrative ────────────────────────────────────────────
    hits = []
    misses = []
    if cuervo_er >= ER_TARGET:
        hits.append(f"ER at {cuervo_er:.2f}% meets the 3% brief target")
    else:
        misses.append(f"ER at {cuervo_er:.2f}% is {ER_TARGET - cuervo_er:.2f}pp below the 3% target")

    if reel_ratio >= REEL_RATIO_TARGET:
        hits.append(f"Reel ratio at {reel_ratio:.0f}% meets the 50% target")
    else:
        misses.append(f"Reel ratio at {reel_ratio:.0f}% — need {REEL_RATIO_TARGET - reel_ratio:.0f}pp more to hit 50%")

    if avg_reel_views >= REEL_VIEW_TARGET:
        hits.append(f"Avg Reel views ({avg_reel_views:,.0f}) above 10K benchmark")
    else:
        misses.append(f"Avg Reel views ({avg_reel_views:,.0f}) below 10K benchmark")

    if IG_PPW_TARGET[0] <= ig_ppw <= IG_PPW_TARGET[1]:
        hits.append(f"IG posting cadence ({ig_ppw:.1f}/wk) on target")
    elif ig_ppw < IG_PPW_TARGET[0]:
        misses.append(f"IG posting at {ig_ppw:.1f}/wk — below {IG_PPW_TARGET[0]}/wk minimum")

    narrative = ""
    if hits:
        narrative += "**Hitting targets:** " + ". ".join(hits) + ". "
    if misses:
        narrative += "**Needs work:** " + ". ".join(misses) + "."

    if narrative:
        st.info(narrative)

    st.markdown("---")

    # ── Platform Cadence Scorecard ─────────────────────────────────────
    st.subheader("Platform Cadence Scorecard")
    st.caption("GOAT targets: Instagram 8-10 assets/month, TikTok 12-16 assets/month")

    cad1, cad2 = st.columns(2)
    for plat, col in [("Instagram", cad1), ("TikTok", cad2)]:
        with col:
            freq_p = results["frequency"].get(CUERVO, {}).get(plat, {})
            actual_ppm = freq_p.get("total_posts_30d", 0)
            actual_ppw = freq_p.get("posts_per_week", 0)
            target = GOAT_CADENCE_TARGETS.get(plat, {})
            target_low = target.get("low", 0)
            target_high = target.get("high", 0)

            on_track = target_low <= actual_ppm <= target_high
            status = "ON TRACK" if on_track else ("BELOW" if actual_ppm < target_low else "ABOVE")

            st.markdown(f"### {plat}")
            st.metric("Posts/Month", f"{actual_ppm}",
                      delta=f"Target: {target_low}-{target_high}/mo",
                      delta_color="off")
            st.metric("Posts/Week", f"{actual_ppw:.1f}",
                      delta=f"Target: {target_low / 4.3:.1f}-{target_high / 4.3:.1f}/wk",
                      delta_color="off")
            if on_track:
                st.success(f"**{status}**")
            elif actual_ppm < target_low:
                st.error(f"**{status}** — {target_low - actual_ppm} posts short")
            else:
                st.warning(f"**{status}**")

    st.markdown("---")

    # ── Engagement Signals ─────────────────────────────────────────────
    st.subheader("Engagement Signals")
    st.caption("Beyond likes — saves, shares, and comments indicate deeper audience connection")

    if len(cuervo_df):
        save_rate = cuervo_df["saves"].sum() / max(cuervo_df["likes"].sum(), 1) * 100
        share_rate = cuervo_df["shares"].sum() / max(cuervo_df["likes"].sum(), 1) * 100
        comment_rate = cuervo_df["comments"].sum() / max(cuervo_df["likes"].sum(), 1) * 100

        # Category averages for comparison
        cat_save = df["saves"].sum() / max(df["likes"].sum(), 1) * 100
        cat_share = df["shares"].sum() / max(df["likes"].sum(), 1) * 100
        cat_comment = df["comments"].sum() / max(df["likes"].sum(), 1) * 100

        s1, s2, s3 = st.columns(3)
        with s1:
            st.metric("Save Rate", f"{save_rate:.1f}%",
                      delta=f"{save_rate - cat_save:+.1f}% vs category",
                      help="Saves / Likes — content bookmarking signal")
        with s2:
            st.metric("Share Rate", f"{share_rate:.1f}%",
                      delta=f"{share_rate - cat_share:+.1f}% vs category",
                      help="Shares / Likes — organic reach amplifier")
        with s3:
            st.metric("Comment Rate", f"{comment_rate:.1f}%",
                      delta=f"{comment_rate - cat_comment:+.1f}% vs category",
                      help="Comments / Likes — community engagement")

        # So What
        best_signal = max([("Save", save_rate, cat_save), ("Share", share_rate, cat_share),
                           ("Comment", comment_rate, cat_comment)], key=lambda x: x[1] - x[2])
        worst_signal = min([("Save", save_rate, cat_save), ("Share", share_rate, cat_share),
                            ("Comment", comment_rate, cat_comment)], key=lambda x: x[1] - x[2])
        if best_signal[1] > best_signal[2]:
            st.info(f"**Strongest signal:** {best_signal[0]} rate outperforms category by {best_signal[1] - best_signal[2]:.1f}pp. "
                    f"**Watch:** {worst_signal[0]} rate {'trails' if worst_signal[1] < worst_signal[2] else 'leads'} by {abs(worst_signal[1] - worst_signal[2]):.1f}pp.")
    else:
        st.info("No Cuervo posts in the dataset.")


# ══════════════════════════════════════════════════════════════════════
# TAB 2 — Content Performance
# ══════════════════════════════════════════════════════════════════════

with tab_content:

    # ── Format Breakdown ───────────────────────────────────────────────
    st.subheader("Content Format Breakdown")
    st.caption("Cuervo's format mix on Instagram — Reels should be the primary driver per the Social Brief")

    if len(cuervo_ig):
        format_counts = cuervo_ig.groupby("post_type").size().reset_index(name="count")
        format_counts["pct"] = (format_counts["count"] / format_counts["count"].sum() * 100).round(1)
        format_er = cuervo_ig.groupby("post_type")["engagement_rate"].mean().reset_index()
        format_er.columns = ["post_type", "avg_er"]

        col_f1, col_f2 = st.columns(2)
        with col_f1:
            st.markdown("**Format Distribution**")
            fig_fmt = px.pie(format_counts, values="count", names="post_type",
                             color_discrete_sequence=["#F8C090", "#2ea3f2", "#7B6B63", "#D4956A"],
                             template=CHART_TEMPLATE)
            fig_fmt.update_layout(font=CHART_FONT, height=350)
            st.plotly_chart(fig_fmt, width="stretch")

        with col_f2:
            st.markdown("**Avg ER by Format**")
            fig_fer = px.bar(format_er, x="post_type", y="avg_er",
                             color_discrete_sequence=[BRAND_COLORS[CUERVO]],
                             labels={"avg_er": "Avg ER %", "post_type": ""},
                             template=CHART_TEMPLATE, text_auto=".2f")
            # Add 3% target line
            fig_fer.add_hline(y=ER_TARGET, line_dash="dash", line_color="#333",
                              annotation_text="3% Brief target", annotation_position="top right")
            fig_fer.update_layout(font=CHART_FONT, height=350, showlegend=False)
            st.plotly_chart(fig_fer, width="stretch")

        # Format KPIs
        reel_pct = len(cuervo_ig[cuervo_ig["post_type"] == "Reel"]) / max(len(cuervo_ig), 1) * 100
        carousel_pct = len(cuervo_ig[cuervo_ig["post_type"] == "Carousel"]) / max(len(cuervo_ig), 1) * 100
        best_fmt_er = cuervo_ig.groupby("post_type")["engagement_rate"].mean()
        best_fmt_er = best_fmt_er[best_fmt_er > 0]
        best_fmt = best_fmt_er.idxmax() if len(best_fmt_er) else "N/A"
        best_val = best_fmt_er.max() if len(best_fmt_er) else 0

        fk1, fk2, fk3 = st.columns(3)
        with fk1:
            st.metric("Reel %", f"{reel_pct:.0f}%",
                      delta=f"{reel_pct - 50:+.0f}% vs 50% target")
        with fk2:
            st.metric("Carousel %", f"{carousel_pct:.0f}%",
                      help="Carousels drive saves — aim for 20-25%")
        with fk3:
            st.metric("Best Format (ER)", best_fmt, delta=f"{best_val:.2f}%")

        # So What
        if reel_pct < 50:
            st.info(f"**Format gap:** Reels at {reel_pct:.0f}% — the Brief targets 50%+. "
                    f"{best_fmt} is the highest-performing format at {best_val:.2f}% ER.")
        else:
            st.info(f"**On track:** Reel ratio at {reel_pct:.0f}% exceeds the 50% target. "
                    f"{best_fmt} drives the best ER at {best_val:.2f}%.")
    else:
        st.info("No Cuervo Instagram posts in the dataset.")

    st.markdown("---")

    # ── Theme Performance ──────────────────────────────────────────────
    st.subheader("Content Theme Performance")
    st.caption("Which themes drive the highest engagement for Cuervo")

    if len(cuervo_df) and cuervo_df["content_theme"].notna().any():
        theme_er = (cuervo_df.groupby("content_theme")
                    .agg(avg_er=("engagement_rate", "mean"), count=("engagement_rate", "size"))
                    .reset_index()
                    .sort_values("avg_er", ascending=False))
        theme_er["avg_er"] = theme_er["avg_er"].round(2)

        fig_theme = px.bar(theme_er, x="content_theme", y="avg_er",
                           color_discrete_sequence=[BRAND_COLORS[CUERVO]],
                           labels={"avg_er": "Avg ER %", "content_theme": ""},
                           template=CHART_TEMPLATE, text_auto=".2f",
                           hover_data={"count": True})
        fig_theme.add_hline(y=ER_TARGET, line_dash="dash", line_color="#333",
                            annotation_text="3% target", annotation_position="top right")
        fig_theme.update_layout(font=CHART_FONT, height=400, showlegend=False,
                                xaxis_tickangle=-35)
        st.plotly_chart(fig_theme, width="stretch")

        # So What
        top_theme = theme_er.iloc[0]
        bottom_theme = theme_er.iloc[-1] if len(theme_er) > 1 else top_theme
        themes_above_target = theme_er[theme_er["avg_er"] >= ER_TARGET]
        st.info(f"**Top theme:** {top_theme['content_theme']} at {top_theme['avg_er']:.2f}% ER ({top_theme['count']} posts). "
                f"{len(themes_above_target)} of {len(theme_er)} themes meet the 3% target. "
                f"**Lowest:** {bottom_theme['content_theme']} at {bottom_theme['avg_er']:.2f}%.")

    st.markdown("---")

    # ── Best & Worst Posts ─────────────────────────────────────────────
    st.subheader("Best & Worst Posts")

    if len(cuervo_df):
        post_cols = ["platform", "post_type", "engagement_rate", "likes", "comments",
                     "shares", "views", "content_theme", "post_date", "caption_text", "post_url"]
        available_cols = [c for c in post_cols if c in cuervo_df.columns]

        col_best, col_worst = st.columns(2)
        with col_best:
            st.markdown("**Top 5 by ER**")
            top5 = cuervo_df.nlargest(5, "engagement_rate")[available_cols].reset_index(drop=True)
            top5.index = top5.index + 1
            for idx, row in top5.iterrows():
                caption_preview = str(row.get("caption_text", ""))[:100]
                er_val = row["engagement_rate"]
                url = row.get("post_url", "")
                with st.expander(f"#{idx} — {er_val:.2f}% ER | {row.get('post_type', '')} | {row.get('content_theme', '')}"):
                    st.markdown(f"*\"{caption_preview}...\"*")
                    st.caption(f"Likes: {row.get('likes', 0):,} | Comments: {row.get('comments', 0):,} | "
                               f"Shares: {row.get('shares', 0):,} | Views: {row.get('views', 0):,}")
                    if url:
                        st.markdown(f"[View post]({url})")

        with col_worst:
            st.markdown("**Bottom 5 by ER**")
            bottom5 = cuervo_df.nsmallest(5, "engagement_rate")[available_cols].reset_index(drop=True)
            bottom5.index = bottom5.index + 1
            for idx, row in bottom5.iterrows():
                caption_preview = str(row.get("caption_text", ""))[:100]
                er_val = row["engagement_rate"]
                url = row.get("post_url", "")
                with st.expander(f"#{idx} — {er_val:.2f}% ER | {row.get('post_type', '')} | {row.get('content_theme', '')}"):
                    st.markdown(f"*\"{caption_preview}...\"*")
                    st.caption(f"Likes: {row.get('likes', 0):,} | Comments: {row.get('comments', 0):,} | "
                               f"Shares: {row.get('shares', 0):,} | Views: {row.get('views', 0):,}")
                    if url:
                        st.markdown(f"[View post]({url})")
    else:
        st.info("No Cuervo posts in the dataset.")


# ══════════════════════════════════════════════════════════════════════
# TAB 3 — Self-Audit Intelligence
# ══════════════════════════════════════════════════════════════════════

with tab_audit:

    autostrat = st.session_state.get("autostrat", {})
    _has_autostrat = has_autostrat_data(autostrat)

    if not _has_autostrat:
        st.info("No autostrat reports loaded. Import PDFs from the home page to see "
                "Cuervo's self-audit intelligence — audience psychographics, winning territories, and strategic actions.")
    else:
        # ── Jose Cuervo Report ─────────────────────────────────────────
        jc_report = get_report(autostrat, "instagram_hashtags", "josecuervo")
        marg_report = get_report(autostrat, "instagram_hashtags", "margaritatime")

        cuervo_reports = []
        if jc_report:
            cuervo_reports.append(("josecuervo", "Jose Cuervo (#josecuervo)", jc_report))
        if marg_report:
            cuervo_reports.append(("margaritatime", "Margarita Time (#margaritatime)", marg_report))

        if not cuervo_reports:
            st.info("No Cuervo self-audit reports found. Import josecuervo or margaritatime autostrat PDFs.")
        else:
            for report_id, report_label, report in cuervo_reports:
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

                # How to Win
                hw = report.get("how_to_win", {})
                if hw.get("territories"):
                    render_section_label("How to Win")
                    if hw.get("summary"):
                        st.markdown(f"*{hw['summary']}*")
                    render_territory_cards(hw["territories"])

                # Strategic Actions
                ha = report.get("hashtag_analysis", {})
                if ha.get("strategic_actions"):
                    render_section_label("Strategic Actions")
                    for i, action in enumerate(ha["strategic_actions"][:6], 1):
                        st.markdown(f"**{i}.** {action}")

                # Audience Verbatims
                verbatims = hw.get("audience_verbatims", [])
                if verbatims:
                    with st.expander(f"Audience Verbatims ({len(verbatims)})"):
                        render_verbatim_quotes(verbatims, max_quotes=8)

                st.markdown("---")
