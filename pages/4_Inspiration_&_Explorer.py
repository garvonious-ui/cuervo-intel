"""
Page 4: Inspiration & Explorer — "The Toolbox"
Reference brands + power-user data access.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import io
import tempfile
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from config import (
    BRAND_COLORS, CHART_TEMPLATE, CHART_FONT, BRAND_ORDER, CUSTOM_CSS,
    REFERENCE_BRAND_LABELS,
)
from autostrat_loader import (
    has_autostrat_data, get_report, get_reference_profiles,
    get_all_audience_profiles, PROFILE_TYPES,
)
from autostrat_components import (
    render_section_label, render_territory_cards, render_nopd_cards,
    render_narrative_card, render_hits_misses, render_verbatim_quotes,
    render_sponsorship_card, render_statistics_section, render_top_posts_section,
)

st.logo("logo.png")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
st.header("Inspiration & Explorer")

if "results" not in st.session_state:
    st.warning("Go to the home page first to load data.")
    st.stop()

results = st.session_state["results"]
df = st.session_state["filtered_df"].copy()
full_df = st.session_state["df"]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
tab_inspo, tab_explorer = st.tabs(["Inspiration", "Data Explorer"])


# ══════════════════════════════════════════════════════════════════════
# TAB 1 — Inspiration (Reference Brands)
# ══════════════════════════════════════════════════════════════════════

with tab_inspo:
    st.caption(
        "Non-competitive brands studied for content strategy inspiration. "
        "These are not tequila competitors — they are reference points for "
        "creative strategy, audience engagement, and content formats."
    )

    autostrat = st.session_state.get("autostrat", {})
    ref_profiles = get_reference_profiles(autostrat)

    if not ref_profiles:
        st.info(
            "No reference brand reports loaded. Import autostrat PDFs for "
            "inspiration brands (e.g., Duolingo, Poppi) from the home page."
        )
    else:
        ref_platform = st.radio("Platform", ["Instagram", "TikTok"],
                                horizontal=True, key="ref_plat")
        ref_type = "instagram_profiles" if ref_platform == "Instagram" else "tiktok_profiles"

        available_refs = {k: v for k, v in ref_profiles.items() if v["report_type"] == ref_type}

        if not available_refs:
            st.info(f"No {ref_platform} reference brand reports available.")
        else:
            ref_options = {
                REFERENCE_BRAND_LABELS.get(v["identifier"], v["identifier"].replace("_", " ").title()): k
                for k, v in available_refs.items()
            }
            selected_ref_label = st.selectbox("Select reference brand",
                                              list(ref_options.keys()), key="ref_brand_sel")
            ref_key = ref_options[selected_ref_label]
            ref_data = available_refs[ref_key]
            report_r = ref_data["report"]
            display_name = REFERENCE_BRAND_LABELS.get(ref_data["identifier"],
                                                       ref_data["identifier"].replace("_", " ").title())

            # ── Snapshot KPIs ──────────────────────────────────────────
            snapshot = report_r.get("snapshot", {})
            if any(snapshot.values()):
                render_section_label("Profile Snapshot")
                rc1, rc2, rc3, rc4, rc5 = st.columns(5)
                with rc1:
                    st.metric("Followers", f"{snapshot.get('followers', 0):,}")
                with rc2:
                    st.metric("Following", f"{snapshot.get('following', 0):,}")
                with rc3:
                    st.metric("Avg Likes", f"{snapshot.get('avg_likes', 0):,}")
                with rc4:
                    st.metric("Avg Comments", f"{snapshot.get('avg_comments', 0):,}")
                with rc5:
                    er = snapshot.get("avg_engagement_rate", 0)
                    st.metric("Avg ER", f"{er}%")
                st.markdown("---")

            # ── Creator Summary / What Hits & Misses ───────────────────
            cs = report_r.get("creator_summary", {})
            if cs.get("topline"):
                render_section_label("Brand Summary")
                st.markdown(f"**{display_name}** — {cs['topline']}")
                if cs.get("what_it_means"):
                    st.markdown(f"*{cs['what_it_means']}*")
                if cs.get("common_themes"):
                    st.caption(f"Common themes: {' | '.join(cs['common_themes'])}")
                if cs.get("what_hits") or cs.get("what_misses"):
                    render_hits_misses(cs.get("what_hits", ""), cs.get("what_misses", ""))
                st.markdown("---")

            # ── "What Cuervo Can Steal" ────────────────────────────────
            render_section_label("What Cuervo Can Steal")
            st.caption(f"Specific tactics from {display_name} that Cuervo could adapt")

            steal_points = []
            if cs.get("what_hits"):
                steal_points.append(f"**Content approach:** {cs['what_hits'][:200]}")
            if cs.get("common_themes"):
                steal_points.append(f"**Theme playbook:** Adapt their use of {', '.join(cs['common_themes'][:3])} to tequila culture")

            ea = report_r.get("engagement_analysis", {})
            if ea.get("summary"):
                steal_points.append(f"**Engagement strategy:** {ea['summary'][:200]}")

            pa = report_r.get("posting_analysis", {})
            if pa.get("summary"):
                steal_points.append(f"**Posting rhythm:** {pa['summary'][:200]}")

            if snapshot.get("avg_engagement_rate", 0) > 3:
                steal_points.append(f"**ER benchmark:** {display_name} achieves {snapshot['avg_engagement_rate']}% ER — study their format mix")

            if steal_points:
                for point in steal_points:
                    st.markdown(f"- {point}")
            else:
                st.info(f"Import more {display_name} report data for specific tactical recommendations.")
            st.markdown("---")

            # ── Audience Comparison: Cuervo vs Reference ───────────────
            ap_ref = report_r.get("audience_profile", {})
            has_ref_nopd = any(ap_ref.get(k) for k in ["needs", "objections", "desires", "pain_points"])

            # Find Cuervo audience profile from hashtag reports
            cuervo_profiles = get_all_audience_profiles(autostrat, exclude_reference=True)
            cuervo_ap = None
            for p in cuervo_profiles:
                if "cuervo" in p["identifier"].lower():
                    cuervo_ap = p["audience_profile"]
                    break

            if has_ref_nopd and cuervo_ap:
                render_section_label(f"Audience Comparison: Cuervo vs {display_name}")
                for dimension in ["needs", "objections", "desires", "pain_points"]:
                    from autostrat_components import NOPD_STYLES
                    style = NOPD_STYLES[dimension]
                    st.markdown(f"""
                    <div style="font-family: 'Barlow Condensed', sans-serif; font-weight: 700;
                                color: {style['color']}; font-size: 1rem; letter-spacing: 1px;
                                margin: 16px 0 8px 0;">{style['label']}</div>
                    """, unsafe_allow_html=True)

                    col_c, col_r = st.columns(2)
                    with col_c:
                        st.markdown("**Cuervo**")
                        for item in cuervo_ap.get(dimension, []):
                            st.markdown(f"- {item}")
                        if not cuervo_ap.get(dimension):
                            st.caption("No data")
                    with col_r:
                        st.markdown(f"**{display_name}**")
                        for item in ap_ref.get(dimension, []):
                            st.markdown(f"- {item}")
                        if not ap_ref.get(dimension):
                            st.caption("No data")
                st.markdown("---")
            elif has_ref_nopd:
                render_section_label(f"{display_name} Audience Profile")
                if ap_ref.get("summary"):
                    st.markdown(ap_ref["summary"])
                render_nopd_cards(ap_ref)
                st.markdown("---")

            # ── How to Win ─────────────────────────────────────────────
            hw = report_r.get("how_to_win", {})
            if hw.get("territories"):
                render_section_label("How to Win")
                if hw.get("summary"):
                    st.markdown(f"*{hw['summary']}*")
                render_territory_cards(hw["territories"])
                if hw.get("audience_verbatims"):
                    with st.expander("Audience Verbatims"):
                        render_verbatim_quotes(hw["audience_verbatims"])
                st.markdown("---")

            # ── Sponsorship Intelligence ───────────────────────────────
            suggestions = report_r.get("future_sponsorship_suggestions", [])
            if suggestions:
                render_section_label("Sponsorship Intelligence")
                cols_s = st.columns(min(len(suggestions), 2))
                for i, sug in enumerate(suggestions):
                    with cols_s[i % len(cols_s)]:
                        render_sponsorship_card(sug)
                st.markdown("---")

            # ── Performance Statistics ────────────────────────────────
            stats = report_r.get("statistics", {})
            if stats and any(stats.get("all_posts", {}).values()):
                render_section_label("Performance Statistics")
                st.caption("Min / Max / Median / Avg across all analyzed posts")
                render_statistics_section(stats)
                st.markdown("---")

            # ── Top & Bottom Posts ────────────────────────────────────
            top_posts = report_r.get("top_posts", {})
            if top_posts:
                render_section_label("Top & Bottom Posts")
                st.caption("Best and worst performing posts by likes, comments, and overall engagement")
                render_top_posts_section(top_posts)


# ══════════════════════════════════════════════════════════════════════
# TAB 2 — Data Explorer (ported from pages/4_Data_Explorer.py)
# ══════════════════════════════════════════════════════════════════════

with tab_explorer:
    st.subheader("Data Explorer")
    st.markdown("Use these filters to drill into the data. Global brand/platform filters from the sidebar still apply.")

    # ── Advanced filters ───────────────────────────────────────────────
    fc1, fc2, fc3, fc4 = st.columns(4)

    with fc1:
        er_min = float(df["engagement_rate"].min()) if len(df) and df["engagement_rate"].notna().any() else 0.0
        er_max = float(df["engagement_rate"].max()) if len(df) and df["engagement_rate"].notna().any() else 10.0
        er_range = st.slider("ER % range", er_min, max(er_max, er_min + 0.1),
                             (er_min, er_max), step=0.1, key="er_slider")

    with fc2:
        likes_max = int(df["likes"].max()) if len(df) and df["likes"].notna().any() else 100
        likes_range = st.slider("Likes range", 0, max(likes_max, 1), (0, likes_max), key="likes_slider")

    with fc3:
        themes_avail = sorted(df["content_theme"].dropna().unique().tolist())
        sel_themes = st.multiselect("Content theme", themes_avail, default=themes_avail, key="exp_themes")

    with fc4:
        tones_avail = sorted(df["caption_tone"].dropna().unique().tolist())
        sel_tones = st.multiselect("Tone", tones_avail, default=tones_avail, key="exp_tones")

    fc5, fc6, fc7, fc8 = st.columns(4)

    with fc5:
        styles_avail = sorted(df["visual_style"].dropna().unique().tolist())
        sel_styles = st.multiselect("Visual style", styles_avail, default=styles_avail, key="exp_styles")

    with fc6:
        ctas_avail = sorted(df["cta_type"].dropna().unique().tolist())
        sel_ctas = st.multiselect("CTA type", ctas_avail, default=ctas_avail, key="exp_ctas")

    with fc7:
        collab_opt = st.selectbox("Creator collab", ["All", "Yes", "No"], key="exp_collab")

    with fc8:
        paid_opt = st.selectbox("Paid partnership", ["All", "Yes", "No"], key="exp_paid")

    # Apply advanced filters
    mask = (
        df["engagement_rate"].between(er_range[0], er_range[1]) &
        df["likes"].between(likes_range[0], likes_range[1]) &
        (df["content_theme"].isin(sel_themes) | df["content_theme"].isna()) &
        (df["caption_tone"].isin(sel_tones) | df["caption_tone"].isna()) &
        (df["visual_style"].isin(sel_styles) | df["visual_style"].isna()) &
        (df["cta_type"].isin(sel_ctas) | df["cta_type"].isna())
    )

    collab_col = df["has_creator_collab"].astype(str).str.lower()
    paid_col = df["is_paid_partnership"].astype(str).str.lower()

    if collab_opt == "Yes":
        mask = mask & (collab_col == "yes")
    elif collab_opt == "No":
        mask = mask & (collab_col != "yes")

    if paid_opt == "Yes":
        mask = mask & (paid_col == "yes")
    elif paid_opt == "No":
        mask = mask & (paid_col != "yes")

    filt = df[mask]

    # ── Summary stats ──────────────────────────────────────────────────
    st.markdown("---")
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.metric("Matching Posts", f"{len(filt):,}")
    with m2:
        st.metric("Avg ER", f"{filt['engagement_rate'].mean():.2f}%" if len(filt) else "N/A")
    with m3:
        st.metric("Total Likes", f"{int(filt['likes'].sum()):,}" if len(filt) else "0")
    with m4:
        st.metric("Brands", f"{filt['brand'].nunique()}")
    with m5:
        st.metric("Platforms", f"{filt['platform'].nunique()}")

    # ── Caption search ─────────────────────────────────────────────────
    search = st.text_input("Search captions or hashtags", placeholder="e.g. margarita, #CuervoDay, recipe")
    if search:
        search_lower = search.lower()
        filt = filt[
            filt["caption_text"].fillna("").str.lower().str.contains(search_lower, na=False) |
            filt["hashtags"].fillna("").str.lower().str.contains(search_lower, na=False)
        ]
        st.caption(f"{len(filt)} posts match '{search}'")

    # ── Data table ─────────────────────────────────────────────────────
    display_cols = [
        "brand", "platform", "post_date", "post_type", "engagement_rate",
        "likes", "comments", "shares", "views", "content_theme",
        "visual_style", "caption_tone", "cta_type", "has_creator_collab",
        "caption_word_count", "emoji_count_in_caption", "post_url",
    ]
    show_df = filt[[c for c in display_cols if c in filt.columns]].copy()
    show_df = show_df.sort_values("engagement_rate", ascending=False).reset_index(drop=True)
    show_df.index = show_df.index + 1
    show_df.index.name = "#"

    if "engagement_rate" in show_df.columns:
        show_df["engagement_rate"] = show_df["engagement_rate"].round(2)

    st.dataframe(
        show_df.style.apply(
            lambda row: ["background-color: #FDEBD6" if row.get("brand") == "Jose Cuervo" else "" for _ in row],
            axis=1,
        ),
        width="stretch",
        height=600,
    )

    # ── Quick insights ─────────────────────────────────────────────────
    if len(filt) >= 5:
        with st.expander("Quick Insights on Filtered Data"):
            type_ers = filt.groupby("post_type")["engagement_rate"].mean().dropna()
            if len(type_ers):
                st.markdown(f"- **Best content type:** {type_ers.idxmax()} (avg ER {type_ers.max():.2f}%)")

            theme_ers = filt.groupby("content_theme")["engagement_rate"].mean().dropna()
            if len(theme_ers):
                st.markdown(f"- **Best theme:** {theme_ers.idxmax()} (avg ER {theme_ers.max():.2f}%)")

            collab_er = filt[filt["has_creator_collab"].str.lower() == "yes"]["engagement_rate"].mean()
            non_er = filt[filt["has_creator_collab"].str.lower() != "yes"]["engagement_rate"].mean()
            if pd.notna(collab_er) and pd.notna(non_er):
                lift = collab_er - non_er
                st.markdown(f"- **Creator collab lift:** {'+' if lift > 0 else ''}{lift:.2f}% ER")

            best_day = filt.copy()
            best_day["dow"] = pd.to_datetime(best_day["post_date"], errors="coerce").dt.day_name()
            day_er = best_day.groupby("dow")["engagement_rate"].mean()
            if len(day_er):
                st.markdown(f"- **Best posting day:** {day_er.idxmax()} (avg ER {day_er.max():.2f}%)")

    # ── Export ─────────────────────────────────────────────────────────
    st.markdown("---")
    ex1, ex2 = st.columns(2)

    with ex1:
        csv_buf = io.BytesIO()
        filt.to_csv(csv_buf, index=False)
        st.download_button("Download filtered data (CSV)", csv_buf.getvalue(),
                           file_name="cuervo_filtered_data.csv", mime="text/csv")

    with ex2:
        from dashboard import generate_dashboard
        xlsx_path = os.path.join(tempfile.gettempdir(), "cuervo_report_explorer.xlsx")
        generate_dashboard(results, xlsx_path)
        with open(xlsx_path, "rb") as f:
            st.download_button("Download Excel Report", f.read(),
                               file_name="cuervo_intelligence_report.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
