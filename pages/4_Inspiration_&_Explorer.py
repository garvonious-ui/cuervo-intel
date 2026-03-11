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

from config import CHART_TEMPLATE, CHART_FONT
from autostrat_loader import (
    has_autostrat_data, get_report, get_reference_profiles,
    get_all_audience_profiles, PROFILE_TYPES,
)
from autostrat_components import (
    render_section_label, render_territory_cards, render_nopd_cards,
    render_narrative_card, render_hits_misses, render_verbatim_quotes,
    render_sponsorship_card, render_statistics_section,
)

if "results" not in st.session_state:
    st.warning("Go to the home page first to load data.")
    st.stop()

from client_context import get_client
cfg = get_client()

st.logo(cfg.app_logo_path)
st.markdown(cfg.custom_css, unsafe_allow_html=True)
st.header(cfg.page_headers.get("inspiration", "Inspiration & Explorer"))

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
                cfg.reference_brand_labels.get(v["identifier"], v["identifier"].replace("_", " ").title()): k
                for k, v in available_refs.items()
            }
            selected_ref_label = st.selectbox("Select reference brand",
                                              list(ref_options.keys()), key="ref_brand_sel")
            ref_key = ref_options[selected_ref_label]
            ref_data = available_refs[ref_key]
            report_r = ref_data["report"]
            display_name = cfg.reference_brand_labels.get(ref_data["identifier"],
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
                    avg_eng = snapshot.get("avg_engagements", snapshot.get("avg_engagement_rate", 0))
                    st.metric("Avg Eng", f"{avg_eng:,.0f}" if isinstance(avg_eng, (int, float)) else str(avg_eng))
                st.markdown("---")

            # ── Creator Summary ────────────────────────────────────────
            cs = report_r.get("creator_summary", {})
            if cs.get("topline"):
                render_section_label("Brand Summary")
                topline_clean = cs["topline"].replace("\n", " ").strip()
                st.markdown(f"**{display_name}** — {topline_clean}")
                if cs.get("what_it_means"):
                    means_clean = cs["what_it_means"].replace("\n", " ").strip()
                    st.markdown(f"*{means_clean}*")
                st.markdown("---")

            # ── "What {hero_brand} Can Steal" ────────────────────────────
            steal_header = cfg.narrative.get("inspiration", {}).get(
                "steal_header_template", "What {hero_brand} Can Steal"
            ).format(hero_brand=cfg.hero_brand)
            render_section_label(steal_header)
            st.caption(f"Strategic patterns from {display_name} translated to {cfg.hero_brand}'s {cfg.industry} world")

            steal_points = []

            # Pull client-specific adaptation copy from config
            adapt = cfg.narrative.get("inspiration", {}).get("adaptation_templates", {})
            adapt_product = adapt.get("product_drops", "Apply the same energy to product drops and cultural moments")
            adapt_heritage = adapt.get("heritage", f"Mirror this with {cfg.industry} heritage storytelling")
            adapt_engagement = adapt.get("engagement", f"Apply these engagement triggers to {cfg.industry} moments")
            adapt_cadence = adapt.get("cadence", f"Mirror this cadence rhythm synced to {cfg.industry} calendar moments")

            # Translate what_hits into a hero-brand-relevant content principle
            if cs.get("what_hits"):
                hits_text = cs["what_hits"].replace("\n", " ").strip()
                steal_points.append(
                    f"**Content principle (from {display_name}):** Their top content uses "
                    f"*{hits_text[:150]}{'...' if len(hits_text) > 150 else ''}* — "
                    f"**{cfg.hero_brand} adaptation:** {adapt_product}, cocktail reveals, and cultural moments."
                )

            # Translate common themes into actionable playbook items
            if cs.get("common_themes"):
                clean_themes = [t.replace("\n", " ").strip() for t in cs["common_themes"][:2]]
                for theme in clean_themes:
                    steal_points.append(
                        f"**Theme to adapt:** *\"{theme[:120]}{'...' if len(theme) > 120 else ''}\"* → "
                        f"{cfg.hero_brand} can {adapt_heritage} and community-driven content."
                    )

            ea = report_r.get("engagement_analysis", {})
            if ea.get("summary"):
                ea_text = ea["summary"].replace("\n", " ").strip()
                steal_points.append(
                    f"**Engagement tactic (from {display_name}):** *{ea_text[:150]}"
                    f"{'...' if len(ea_text) > 150 else ''}* — "
                    f"**{cfg.hero_brand} adaptation:** {adapt_engagement} and community activations."
                )

            pa = report_r.get("posting_analysis", {})
            if pa.get("summary"):
                pa_text = pa["summary"].replace("\n", " ").strip()
                steal_points.append(
                    f"**Posting rhythm (from {display_name}):** *{pa_text[:150]}"
                    f"{'...' if len(pa_text) > 150 else ''}* — "
                    f"**{cfg.hero_brand} adaptation:** {adapt_cadence}."
                )

            avg_eng_val = snapshot.get("avg_engagements", snapshot.get("avg_engagement_rate", 0))
            if isinstance(avg_eng_val, (int, float)) and avg_eng_val > 500:
                steal_points.append(f"**Engagement benchmark:** {display_name} averages {avg_eng_val:,.0f} engagements/post — study their format mix for replicable patterns")

            if steal_points:
                for point in steal_points:
                    st.markdown(f"- {point}")
            else:
                st.info(f"Import more {display_name} report data for specific tactical recommendations.")
            st.markdown("---")

            # ── Audience Comparison: Hero Brand vs Reference ───────────────
            ap_ref = report_r.get("audience_profile", {})
            has_ref_nopd = any(ap_ref.get(k) for k in ["needs", "objections", "desires", "pain_points"])

            # Find hero brand audience profile from hashtag reports
            cuervo_profiles = get_all_audience_profiles(autostrat, exclude_reference=True)
            cuervo_ap = None
            for p in cuervo_profiles:
                if cfg.hero_brand.lower().split()[0] in p["identifier"].lower():
                    cuervo_ap = p["audience_profile"]
                    break

            if has_ref_nopd and cuervo_ap:
                comparison_header = cfg.narrative.get("inspiration", {}).get(
                    "audience_comparison_template", "Audience Comparison: {hero_brand} vs {display_name}"
                ).format(hero_brand=cfg.hero_brand, display_name=display_name)
                render_section_label(comparison_header)
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
                        st.markdown(f"**{cfg.hero_brand}**")
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
                render_section_label(f"{display_name} Audience Profile (Reference)")
                st.caption(
                    f"This is {display_name}'s audience — not {cfg.industry} drinkers. "
                    f"Study their engagement patterns and emotional drivers, "
                    f"then look for parallels in {cfg.hero_brand}'s Gen Z audience."
                )
                if ap_ref.get("summary"):
                    summary_clean = ap_ref["summary"].replace("\n", " ").strip()
                    st.markdown(f"*{summary_clean}*")
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



# ══════════════════════════════════════════════════════════════════════
# TAB 2 — Data Explorer (ported from pages/4_Data_Explorer.py)
# ══════════════════════════════════════════════════════════════════════

with tab_explorer:
    st.subheader("Data Explorer")
    st.markdown("Use these filters to drill into the data. Global brand/platform filters from the sidebar still apply.")

    # ── Advanced filters ───────────────────────────────────────────────
    fc1, fc2, fc3, fc4 = st.columns(4)

    with fc1:
        eng_min = int(df["total_engagement"].min()) if len(df) and df["total_engagement"].notna().any() else 0
        eng_max = int(df["total_engagement"].max()) if len(df) and df["total_engagement"].notna().any() else 1000
        eng_range = st.slider("Engagements range", eng_min, max(eng_max, eng_min + 1),
                              (eng_min, eng_max), step=1, key="eng_slider")

    with fc2:
        likes_max = int(df["likes"].max()) if len(df) and df["likes"].notna().any() else 100
        likes_range = st.slider("Likes range", 0, max(likes_max, 1), (0, likes_max), key="likes_slider")

    with fc3:
        themes_avail = sorted(df["content_theme"].dropna().unique().tolist())
        sel_themes = st.multiselect("Content theme", themes_avail, default=themes_avail, key="exp_themes")

    with fc4:
        tones_avail = sorted(df["caption_tone"].dropna().unique().tolist())
        sel_tones = st.multiselect("Tone", tones_avail, default=tones_avail, key="exp_tones")

    fc5, fc6, fc7 = st.columns(3)

    with fc5:
        ctas_avail = sorted(df["cta_type"].dropna().unique().tolist())
        sel_ctas = st.multiselect("CTA type", ctas_avail, default=ctas_avail, key="exp_ctas")

    with fc6:
        collab_opt = st.selectbox("Creator collab", ["All", "Yes", "No"], key="exp_collab")

    with fc7:
        paid_opt = st.selectbox("Paid partnership", ["All", "Yes", "No"], key="exp_paid")

    # Apply advanced filters
    mask = (
        df["total_engagement"].between(eng_range[0], eng_range[1]) &
        df["likes"].between(likes_range[0], likes_range[1]) &
        (df["content_theme"].isin(sel_themes) | df["content_theme"].isna()) &
        (df["caption_tone"].isin(sel_tones) | df["caption_tone"].isna()) &
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
        st.metric("Avg Eng", f"{filt['total_engagement'].mean():,.0f}" if len(filt) else "N/A")
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
        "brand", "platform", "post_date", "post_type", "total_engagement",
        "likes", "comments", "shares", "views", "content_theme",
        "caption_tone", "cta_type", "has_creator_collab",
        "caption_word_count", "emoji_count_in_caption", "post_url",
    ]
    show_df = filt[[c for c in display_cols if c in filt.columns]].copy()
    show_df = show_df.sort_values("total_engagement", ascending=False).reset_index(drop=True)
    show_df.index = show_df.index + 1
    show_df.index.name = "#"

    st.dataframe(
        show_df.style.apply(
            lambda row: [f"background-color: {cfg.highlight_fill_color}" if row.get("brand") == cfg.hero_brand else "" for _ in row],
            axis=1,
        ),
        use_container_width=True,
        height=600,
    )

    # ── Quick insights ─────────────────────────────────────────────────
    if len(filt) >= 5:
        with st.expander("Quick Insights on Filtered Data"):
            type_eng = filt.groupby("post_type")["total_engagement"].mean().dropna()
            if len(type_eng):
                st.markdown(f"- **Best content type:** {type_eng.idxmax()} ({type_eng.max():,.0f} avg eng)")

            theme_eng = filt.groupby("content_theme")["total_engagement"].mean().dropna()
            if len(theme_eng):
                st.markdown(f"- **Best theme:** {theme_eng.idxmax()} ({theme_eng.max():,.0f} avg eng)")

            collab_eng = filt[filt["has_creator_collab"].str.lower() == "yes"]["total_engagement"].mean()
            non_eng = filt[filt["has_creator_collab"].str.lower() != "yes"]["total_engagement"].mean()
            if pd.notna(collab_eng) and pd.notna(non_eng):
                lift = collab_eng - non_eng
                st.markdown(f"- **Creator collab lift:** {'+' if lift > 0 else ''}{lift:,.0f} engagements")

            best_day = filt.copy()
            best_day["dow"] = pd.to_datetime(best_day["post_date"], errors="coerce").dt.day_name()
            day_eng = best_day.groupby("dow")["total_engagement"].mean()
            if len(day_eng):
                st.markdown(f"- **Best posting day:** {day_eng.idxmax()} ({day_eng.max():,.0f} avg eng)")

    # ── Export ─────────────────────────────────────────────────────────
    st.markdown("---")
    ex1, ex2 = st.columns(2)

    with ex1:
        csv_buf = io.BytesIO()
        filt.to_csv(csv_buf, index=False)
        st.download_button("Download filtered data (CSV)", csv_buf.getvalue(),
                           file_name=f"{cfg.client_id}_filtered_data.csv", mime="text/csv")

    with ex2:
        from dashboard import generate_dashboard
        xlsx_path = os.path.join(tempfile.gettempdir(), f"{cfg.client_id}_report_explorer.xlsx")
        generate_dashboard(results, xlsx_path)
        with open(xlsx_path, "rb") as f:
            st.download_button("Download Excel Report", f.read(),
                               file_name=cfg.excel_filename,
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
