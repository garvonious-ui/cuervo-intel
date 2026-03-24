"""
Page 1: Brand Performance — "The Mirror"
What the hero brand is doing and how it's performing.
Uses UNFILTERED data — sidebar brand/platform filters do NOT apply.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from config import CHART_TEMPLATE, CHART_FONT, split_owned_collab
from client_context import get_client
from autostrat_loader import (
    has_autostrat_data, get_report, get_all_how_to_win,
    get_all_audience_profiles, get_all_strategic_actions,
    get_brand_hashtag_reports, get_category_reports,
    CONVERSATION_TYPES,
)
from autostrat_components import (
    render_section_label, render_territory_cards, render_nopd_cards,
    render_narrative_card, render_verbatim_quotes, platform_label,
)

if "results" not in st.session_state:
    st.warning("Go to the home page first to load data.")
    st.stop()

cfg = get_client()
_perf = cfg.narrative.get("performance", {})

st.logo(cfg.app_logo_path)
st.markdown(cfg.custom_css, unsafe_allow_html=True)
st.header(cfg.page_headers.get("performance", "Brand Performance"))
st.caption(cfg.page_captions.get("performance", "How the brand is performing — sidebar filters do not apply here."))

results = st.session_state["results"]
df = st.session_state["df"]  # Unfiltered

HERO = cfg.hero_brand
hero_df = df[df["brand"] == HERO]
# Filter out Edutain half-row duplicates (weight=0.5) to avoid inflating stats
if "_mix_weight" in hero_df.columns:
    hero_df = hero_df[hero_df["_mix_weight"] >= 1.0]
# Separate stories before filtering — needed for story volume KPIs
_is_story_p1 = hero_df["is_story"].astype(str).str.lower() == "yes" if "is_story" in hero_df.columns else pd.Series(False, index=hero_df.index)
hero_stories = hero_df[_is_story_p1]
hero_df = hero_df[~_is_story_p1]
hero_ig = hero_df[hero_df["platform"] == "Instagram"]
hero_tt = hero_df[hero_df["platform"] == "TikTok"]

# Segment owned vs collab posts
hero_owned, hero_collab = split_owned_collab(hero_df)
hero_ig_owned, hero_ig_collab = split_owned_collab(hero_ig)
hero_tt_owned, hero_tt_collab = split_owned_collab(hero_tt)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
tab_kpi, tab_content, tab_audit = st.tabs([
    "KPI Dashboard", "Content Performance", "Self-Audit Intelligence",
])

# ══════════════════════════════════════════════════════════════════════
# TAB 1 — KPI Dashboard
# ══════════════════════════════════════════════════════════════════════

with tab_kpi:

    # ── Social Brief KPI Scorecard ─────────────────────────────────────
    st.subheader("Monthly KPI Scorecard")
    st.caption(f"All metrics averaged per month across the dataset")

    # Compute base data
    eng = results["engagement"].get(HERO, {})
    ig_followers = eng.get("Instagram", {}).get("followers", 0)
    tt_followers = eng.get("TikTok", {}).get("followers", 0)

    freq = results["frequency"].get(HERO, {})
    ig_ppw = freq.get("Instagram", {}).get("posts_per_week", 0)
    ig_ppm = ig_ppw * 4.33
    tt_ppw = freq.get("TikTok", {}).get("posts_per_week", 0)

    _t = cfg.kpi_targets
    ENG_PER_POST_TARGET = _t["engagements_per_post"]
    REEL_RATIO_TARGET = _t["reel_ratio"]
    IG_PPM_TARGET = _t["ig_posts_per_month"]
    TT_PPM_TARGET = _t.get("tt_posts_per_month", None) or (tuple(x * 4 for x in _t["tt_posts_per_week"]) if "tt_posts_per_week" in _t else (12, 20))

    # Stories already excluded from hero_df above; use pre-saved hero_stories
    _hero_feed = hero_df
    _hero_stories = hero_stories

    # Calculate months in dataset
    if "post_date" in hero_df.columns and len(hero_df):
        _date_range = (hero_df["post_date"].max() - hero_df["post_date"].min()).days
        _n_months = max(_date_range / 30.44, 1)
    else:
        _n_months = 1

    # Per-post averages (monthly context)
    avg_eng_per_post = hero_owned["total_engagement"].mean() if len(hero_owned) else 0
    avg_eng_per_post = 0 if pd.isna(avg_eng_per_post) else avg_eng_per_post

    hero_reels_owned = hero_owned[hero_owned["post_type"] == "Reel"]
    avg_eng_per_reel = hero_reels_owned["total_engagement"].mean() if len(hero_reels_owned) else 0
    avg_eng_per_reel = 0 if pd.isna(avg_eng_per_reel) else avg_eng_per_reel

    reel_ratio = len(hero_ig_owned[hero_ig_owned["post_type"] == "Reel"]) / max(len(hero_ig_owned), 1) * 100

    # Monthly volume metrics (owned posts only — excludes Influencer, Collective)
    _owned_feed = _hero_feed[_hero_feed.index.isin(hero_owned.index)]
    _likes_pm = pd.to_numeric(_owned_feed["likes"], errors="coerce").fillna(0).sum() / _n_months
    _comments_pm = pd.to_numeric(_owned_feed["comments"], errors="coerce").fillna(0).sum() / _n_months
    _saves_pm = pd.to_numeric(_owned_feed["saves"], errors="coerce").fillna(0).sum() / _n_months if "saves" in _owned_feed.columns else 0
    _shares_pm = pd.to_numeric(_owned_feed["shares"], errors="coerce").fillna(0).sum() / _n_months if "shares" in _owned_feed.columns else 0

    _owned_reels = _owned_feed[_owned_feed["post_type"].isin(["Reel", "Video"])]
    _reel_views = pd.to_numeric(_owned_reels["views"], errors="coerce").fillna(0).sum() / _n_months if len(_owned_reels) else 0

    _owned_static = _owned_feed[~_owned_feed["post_type"].isin(["Reel", "Video"])]
    _carousel_imp = pd.to_numeric(_owned_static["impressions"], errors="coerce").fillna(0).sum() / _n_months if "impressions" in _owned_static.columns and len(_owned_static) else 0

    _stories_pm = len(_hero_stories) / _n_months
    _story_views_pm = pd.to_numeric(_hero_stories["impressions"], errors="coerce").fillna(0).sum() / _n_months if "impressions" in _hero_stories.columns and len(_hero_stories) else 0

    # Row 1: Averages + Cadence + Followers
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.metric("Avg Eng/Post", f"{avg_eng_per_post:,.0f}",
                  delta=f"{avg_eng_per_post - ENG_PER_POST_TARGET:+,.0f} vs {ENG_PER_POST_TARGET} target")
    with k2:
        st.metric("Avg Eng/Reel", f"{avg_eng_per_reel:,.0f}",
                  delta=f"{avg_eng_per_reel - ENG_PER_POST_TARGET:+,.0f} vs {ENG_PER_POST_TARGET} target")
    with k3:
        st.metric("Reel Ratio (IG)", f"{reel_ratio:.0f}%",
                  delta=f"{reel_ratio - REEL_RATIO_TARGET:+.0f}% vs {REEL_RATIO_TARGET}% target")
    with k4:
        st.metric("IG Posts/Mo", f"{ig_ppm:.0f}",
                  delta=f"Target: {IG_PPM_TARGET[0]}-{IG_PPM_TARGET[1]}/mo",
                  delta_color="off")
    with k5:
        ig_followers_display = f"{ig_followers:,}" if ig_followers else "N/A"
        st.metric("IG Followers", ig_followers_display)

    # Row 2: Monthly engagement volumes
    v1, v2, v3, v4 = st.columns(4)
    with v1:
        _likes_tgt = _t.get("likes_per_month", 0)
        st.metric("Likes/Month", f"{_likes_pm:,.0f}",
                  delta=f"{_likes_pm - _likes_tgt:+,.0f} vs {_likes_tgt:,} target")
    with v2:
        _comments_tgt = _t.get("comments_per_month", 0)
        st.metric("Comments/Month", f"{_comments_pm:,.0f}",
                  delta=f"{_comments_pm - _comments_tgt:+,.0f} vs {_comments_tgt:,} target")
    with v3:
        _saves_tgt = _t.get("saves_per_month", 0)
        st.metric("Saves/Month", f"{_saves_pm:,.0f}",
                  delta=f"{_saves_pm - _saves_tgt:+,.0f} vs {_saves_tgt:,} target")
    with v4:
        _shares_tgt = _t.get("shares_per_month", 0)
        st.metric("Shares/Month", f"{_shares_pm:,.0f}",
                  delta=f"{_shares_pm - _shares_tgt:+,.0f} vs {_shares_tgt:,} target")

    # Row 3: Views, impressions, stories
    v5, v6, v7, v8 = st.columns(4)
    with v5:
        _rv_tgt = _t.get("reel_views_per_month", 0)
        st.metric("Reel Views/Mo", f"{_reel_views:,.0f}",
                  delta=f"{_reel_views - _rv_tgt:+,.0f} vs {_rv_tgt:,} target")
    with v6:
        _ci_tgt = _t.get("carousel_impressions_per_month", 0)
        st.metric("Carousel Imp/Mo", f"{_carousel_imp:,.0f}",
                  delta=f"{_carousel_imp - _ci_tgt:+,.0f} vs {_ci_tgt:,} target")
    with v7:
        _st_tgt = _t.get("stories_per_month", 0)
        st.metric("Stories/Month", f"{_stories_pm:,.0f}",
                  delta=f"{_stories_pm - _st_tgt:+,.0f} vs {_st_tgt:,} target")
    with v8:
        _sv_tgt = _t.get("story_views_per_month", 0)
        st.metric("Story Views/Month", f"{_story_views_pm:,.0f}",
                  delta=f"{_story_views_pm - _sv_tgt:+,.0f} vs {_sv_tgt:,} target")

    st.caption("**Reel Views** = number of times the video was played. **Carousel/Static Impressions** = number of times the post appeared on screen. "
               "These are different metrics — impressions are typically higher than views for equivalent reach.")

    # ── "So What" Narrative ────────────────────────────────────────────
    hits = []
    misses = []
    if avg_eng_per_post >= ENG_PER_POST_TARGET:
        hits.append(f"Avg engagements/post ({avg_eng_per_post:,.0f}) above {ENG_PER_POST_TARGET} target")
    else:
        misses.append(f"Avg engagements/post ({avg_eng_per_post:,.0f}) below {ENG_PER_POST_TARGET} target — gap of {ENG_PER_POST_TARGET - avg_eng_per_post:,.0f}")

    if reel_ratio >= REEL_RATIO_TARGET:
        hits.append(f"Reel ratio at {reel_ratio:.0f}% meets the {REEL_RATIO_TARGET}% target")
    else:
        misses.append(f"Reel ratio at {reel_ratio:.0f}% — need {REEL_RATIO_TARGET - reel_ratio:.0f}pp more to hit {REEL_RATIO_TARGET}%")

    if IG_PPM_TARGET[0] <= ig_ppm <= IG_PPM_TARGET[1]:
        hits.append(f"IG posting cadence (~{ig_ppm:.0f}/mo) on target")
    elif ig_ppm < IG_PPM_TARGET[0]:
        misses.append(f"IG posting at ~{ig_ppm:.0f}/mo — below {IG_PPM_TARGET[0]}/mo minimum")

    narrative = ""
    if hits:
        narrative += "**Hitting targets:** " + ". ".join(hits) + ". "
    if misses:
        narrative += "**Needs work:** " + ". ".join(misses) + "."

    if narrative:
        st.info(narrative)

    st.markdown("---")

    # ── Day / Hour Posting Heatmap ─────────────────────────────────────
    st.subheader("Posting Heatmap — Day & Hour")
    st.caption(_perf.get("heatmap_caption", f"When {HERO} posts across the week — find gaps and peak windows"))

    heatmap_plat = st.radio("Platform", ["Instagram", "TikTok"], horizontal=True, key="heatmap_plat")
    freq_hm = results["frequency"].get(HERO, {}).get(heatmap_plat, {})
    by_day = freq_hm.get("by_day", {})
    by_hour = freq_hm.get("by_hour", {})

    if by_day and by_hour:
        days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        hours = list(range(24))

        # Rebuild heatmap from raw posts — need day+hour combos
        hm_data = {}
        for p in hero_df[hero_df["platform"] == heatmap_plat].itertuples():
            pdate = getattr(p, "post_date", None)
            phour = getattr(p, "post_hour", None)
            if pd.notna(pdate) and pd.notna(phour):
                try:
                    day_name = pd.Timestamp(pdate).day_name()
                except Exception:
                    continue
                phour = int(phour)
                hm_data[(day_name, phour)] = hm_data.get((day_name, phour), 0) + 1

        z = [[hm_data.get((d, h), 0) for h in hours] for d in days_order]

        fig_hm = go.Figure(data=go.Heatmap(
            z=z,
            x=[f"{h}:00" for h in hours],
            y=days_order,
            colorscale=[[0, "#FFF5EB"], [0.5, "#F8C090"], [1, "#D4956A"]],
            text=z,
            texttemplate="%{text}",
            hovertemplate="Day: %{y}<br>Hour: %{x}<br>Posts: %{z}<extra></extra>",
        ))
        fig_hm.update_layout(template=CHART_TEMPLATE, font=CHART_FONT, height=320,
                             xaxis_title="Hour of Day", yaxis_title="",
                             yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_hm, use_container_width=True)

        # Best posting time
        best_days = freq_hm.get("best_days", [])
        best_hours = freq_hm.get("best_hours", [])
        best_day_str = best_days[0][0] if best_days else "N/A"
        if best_hours:
            _bh = int(best_hours[0][0])
            _ampm = "AM" if _bh < 12 else "PM"
            _dh = _bh if _bh <= 12 else _bh - 12
            if _dh == 0:
                _dh = 12
            best_hour_str = f"{_dh} {_ampm}"
        else:
            best_hour_str = "N/A"
        st.info(f"**Peak posting window:** {best_day_str} at {best_hour_str} on {heatmap_plat}. "
                f"Total posts in period: {freq_hm.get('total_posts', 0)}.")
    else:
        st.info(f"No {heatmap_plat} posting data available for {HERO}.")

    st.markdown("---")


# ══════════════════════════════════════════════════════════════════════
# TAB 2 — Content Performance
# ══════════════════════════════════════════════════════════════════════

with tab_content:

    # ── Format Breakdown ───────────────────────────────────────────────
    st.subheader("Content Format Breakdown")
    st.caption(_perf.get("format_caption", f"{HERO}'s format mix on Instagram — reach vs engagement by format"))

    if len(hero_ig_owned):
        format_counts = hero_ig_owned.groupby("post_type").size().reset_index(name="count")
        format_counts["pct"] = (format_counts["count"] / format_counts["count"].sum() * 100).round(1)

        # Avg total engagements by format (brand-owned only)
        format_eng = (hero_ig_owned.groupby("post_type")["total_engagement"].mean().reset_index())
        format_eng.columns = ["post_type", "avg_engagements"]

        col_f1, col_f2 = st.columns(2)
        with col_f1:
            st.markdown("**Format Distribution (Brand-Owned)**")
            fig_fmt = px.pie(format_counts, values="count", names="post_type",
                             color_discrete_sequence=["#F8C090", "#2ea3f2", "#7B6B63", "#D4956A"],
                             template=CHART_TEMPLATE)
            fig_fmt.update_layout(font=CHART_FONT, height=350)
            st.plotly_chart(fig_fmt, use_container_width=True)

        with col_f2:
            st.markdown("**Avg Engagements by Format (Brand-Owned)**")
            fig_eng = px.bar(format_eng, x="post_type", y="avg_engagements",
                             color_discrete_sequence=[cfg.brand_colors[HERO]],
                             labels={"avg_engagements": "Avg Engagements", "post_type": ""},
                             template=CHART_TEMPLATE, text_auto=",.0f")
            fig_eng.add_hline(y=ENG_PER_POST_TARGET, line_dash="dash", line_color="#333",
                              annotation_text=f"{ENG_PER_POST_TARGET} eng/post target", annotation_position="top right")
            fig_eng.update_layout(font=CHART_FONT, height=350, showlegend=False)
            st.plotly_chart(fig_eng, use_container_width=True)

        st.caption("Total engagements = likes + comments + shares + saves. Metrics reflect brand-owned posts (Cuervo + Partner).")

        # Format KPIs
        reel_pct = len(hero_ig_owned[hero_ig_owned["post_type"] == "Reel"]) / max(len(hero_ig_owned), 1) * 100
        carousel_pct = len(hero_ig_owned[hero_ig_owned["post_type"] == "Carousel"]) / max(len(hero_ig_owned), 1) * 100

        # Best format by engagements
        best_eng_fmt = format_eng.loc[format_eng["avg_engagements"].idxmax(), "post_type"] if len(format_eng) else "N/A"
        best_eng_val = format_eng["avg_engagements"].max() if len(format_eng) else 0

        fk1, fk2, fk3 = st.columns(3)
        with fk1:
            st.metric("Reel %", f"{reel_pct:.0f}%",
                      delta=f"{reel_pct - REEL_RATIO_TARGET:+.0f}% vs {REEL_RATIO_TARGET}% target")
        with fk2:
            st.metric("Carousel %", f"{carousel_pct:.0f}%",
                      help="Carousels drive reach and saves")
        with fk3:
            st.metric("Most Engaging Format", best_eng_fmt,
                      delta=f"{best_eng_val:,.0f} avg engagements" if best_eng_val else "N/A",
                      help="Format with highest avg total engagements per post")

        # So What
        if reel_pct < REEL_RATIO_TARGET:
            st.info(f"**Format gap:** Reels at {reel_pct:.0f}% — the Brief targets {REEL_RATIO_TARGET}%+. "
                    f"{best_eng_fmt} drives the most engagement at {best_eng_val:,.0f} avg per post.")
        else:
            st.info(f"**On track:** Reel ratio at {reel_pct:.0f}% exceeds the {REEL_RATIO_TARGET}% target. "
                    f"{best_eng_fmt} drives the most engagement at {best_eng_val:,.0f} avg per post.")
    else:
        st.info(_perf.get("no_ig_posts", f"No {HERO} Instagram posts in the dataset."))

    st.markdown("---")

    # ── Collaboration Amplification ──────────────────────────────────────
    st.subheader("Collaboration Amplification")
    st.caption(f"Owned posts reflect {HERO}'s organic audience. Collab posts (Influencer + Collective) "
               "are posted by partner accounts and reflect their larger reach.")

    if len(hero_collab):
        owned_avg = hero_owned["total_engagement"].mean() if len(hero_owned) else 0
        owned_avg = 0 if pd.isna(owned_avg) else owned_avg
        collab_avg = hero_collab["total_engagement"].mean() if len(hero_collab) else 0
        collab_avg = 0 if pd.isna(collab_avg) else collab_avg
        lift = collab_avg / owned_avg if owned_avg > 0 else 0

        ca1, ca2, ca3 = st.columns(3)
        with ca1:
            st.metric("Owned Avg Eng", f"{owned_avg:,.0f}",
                      help=f"{HERO} + Partner posts ({len(hero_owned)} posts)")
        with ca2:
            st.metric("Collab Avg Eng", f"{collab_avg:,.0f}",
                      help=f"Influencer + Collective posts ({len(hero_collab)} posts)")
        with ca3:
            st.metric("Collab Lift", f"{lift:.1f}x",
                      help="How much more engagement collab posts generate vs owned")

        # Grouped bar: Owned vs Collab by Format
        fmt_comparison = []
        for fmt in ["Reel", "Carousel", "Static Image"]:
            owned_fmt = hero_owned[hero_owned["post_type"] == fmt]
            collab_fmt = hero_collab[hero_collab["post_type"] == fmt]
            if len(owned_fmt):
                fmt_comparison.append({"Format": fmt, "Source": "Owned",
                                       "Avg Eng": owned_fmt["total_engagement"].mean()})
            if len(collab_fmt):
                fmt_comparison.append({"Format": fmt, "Source": "Collab",
                                       "Avg Eng": collab_fmt["total_engagement"].mean()})

        if fmt_comparison:
            fmt_df = pd.DataFrame(fmt_comparison)
            fig_collab = px.bar(fmt_df, x="Format", y="Avg Eng", color="Source",
                                barmode="group",
                                color_discrete_map={"Owned": cfg.brand_colors.get(HERO, "#2ea3f2"),
                                                    "Collab": "#F8C090"},
                                template=CHART_TEMPLATE, text_auto=",.0f")
            fig_collab.update_layout(font=CHART_FONT, height=380,
                                     yaxis_title="Avg Engagements", xaxis_title="")
            st.plotly_chart(fig_collab, use_container_width=True)

        # Narrative
        collab_eng_share = hero_collab["total_engagement"].sum() / max(hero_df["total_engagement"].sum(), 1) * 100
        collab_post_share = len(hero_collab) / max(len(hero_df), 1) * 100
        st.info(f"**Collab amplification:** Influencer + Collective posts are **{collab_post_share:.0f}%** of content "
                f"but drive **{collab_eng_share:.0f}%** of total engagements — a **{lift:.1f}x** lift over brand-owned posts.")
    else:
        st.info("No collab posts detected in the dataset.")

    st.markdown("---")

    # ── Content Pillar Performance ──────────────────────────────────────
    if cfg.themes_ready:
        # Show pillar performance if content_pillar column exists, otherwise fall back to content_theme
        has_pillars = "content_pillar" in hero_df.columns and hero_df["content_pillar"].notna().any()

        if has_pillars:
            st.subheader("Content Pillar Performance")
            st.caption(f"Which pillars drive the highest engagement for {HERO} (brand-owned posts only)")

            _pillar_valid = hero_owned[hero_owned["content_pillar"].notna() & (hero_owned["content_pillar"].astype(str).str.strip() != "")]
            pillar_eng = (_pillar_valid
                          .groupby("content_pillar")
                          .agg(avg_eng=("total_engagement", "mean"), count=("total_engagement", "size"))
                          .reset_index()
                          .sort_values("avg_eng", ascending=False))
            pillar_eng["avg_eng"] = pillar_eng["avg_eng"].round(0)

            fig_pillar = px.bar(pillar_eng, x="content_pillar", y="avg_eng",
                                color="content_pillar", color_discrete_map=cfg.pillar_colors,
                                labels={"avg_eng": "Avg Engagements", "content_pillar": ""},
                                template=CHART_TEMPLATE, text_auto=",.0f",
                                hover_data={"count": True})
            fig_pillar.add_hline(y=ENG_PER_POST_TARGET, line_dash="dash", line_color="#333",
                                 annotation_text=f"{ENG_PER_POST_TARGET} eng/post target", annotation_position="top right")
            fig_pillar.update_layout(font=CHART_FONT, height=400, showlegend=False,
                                     xaxis_tickangle=-35)
            st.plotly_chart(fig_pillar, use_container_width=True)

            top_p = pillar_eng.iloc[0]
            bottom_p = pillar_eng.iloc[-1] if len(pillar_eng) > 1 else top_p
            pillars_above = pillar_eng[pillar_eng["avg_eng"] >= ENG_PER_POST_TARGET]
            st.info(f"**Top pillar:** {top_p['content_pillar']} at {top_p['avg_eng']:,.0f} avg engagements ({top_p['count']} posts). "
                    f"{len(pillars_above)} of {len(pillar_eng)} pillars meet the {ENG_PER_POST_TARGET} eng/post target. "
                    f"**Lowest:** {bottom_p['content_pillar']} at {bottom_p['avg_eng']:,.0f}.")
        else:
            st.subheader("Content Theme Performance")
            st.caption(_perf.get("theme_caption", f"Which themes drive the highest engagement for {HERO}"))

            if len(hero_owned) and hero_owned["content_theme"].notna().any():
                theme_eng = (hero_owned.groupby("content_theme")
                             .agg(avg_eng=("total_engagement", "mean"), count=("total_engagement", "size"))
                             .reset_index()
                             .sort_values("avg_eng", ascending=False))
                theme_eng["avg_eng"] = theme_eng["avg_eng"].round(0)

                fig_theme = px.bar(theme_eng, x="content_theme", y="avg_eng",
                                   color_discrete_sequence=[cfg.brand_colors[HERO]],
                                   labels={"avg_eng": "Avg Engagements", "content_theme": ""},
                                   template=CHART_TEMPLATE, text_auto=",.0f",
                                   hover_data={"count": True})
                fig_theme.add_hline(y=ENG_PER_POST_TARGET, line_dash="dash", line_color="#333",
                                    annotation_text=f"{ENG_PER_POST_TARGET} eng/post target", annotation_position="top right")
                fig_theme.update_layout(font=CHART_FONT, height=400, showlegend=False,
                                        xaxis_tickangle=-35)
                st.plotly_chart(fig_theme, use_container_width=True)

                top_theme = theme_eng.iloc[0]
                bottom_theme = theme_eng.iloc[-1] if len(theme_eng) > 1 else top_theme
                themes_above_target = theme_eng[theme_eng["avg_eng"] >= ENG_PER_POST_TARGET]
                st.info(f"**Top theme:** {top_theme['content_theme']} at {top_theme['avg_eng']:,.0f} avg engagements ({top_theme['count']} posts). "
                        f"{len(themes_above_target)} of {len(theme_eng)} themes meet the {ENG_PER_POST_TARGET} eng/post target. "
                        f"**Lowest:** {bottom_theme['content_theme']} at {bottom_theme['avg_eng']:,.0f}.")
    else:
        st.info(f"**Content theme analysis hidden** — post-level theme tagging is not yet complete for {HERO}. "
                f"This section will appear once all posts have been manually reviewed and tagged.")

    st.markdown("---")

    # ── CTA Distribution ────────────────────────────────────────────
    st.subheader("CTA Distribution")
    st.caption(_perf.get("cta_caption", f"What {HERO} asks its audience to do — are we driving action?"))

    hero_ctas = {}
    for plat in ["Instagram", "TikTok"]:
        plat_ctas = results["captions"].get(HERO, {}).get(plat, {}).get("cta_distribution", {})
        for cta, count in plat_ctas.items():
            hero_ctas[cta] = hero_ctas.get(cta, 0) + count

    if hero_ctas:
        cta_df_all = pd.DataFrame(list(hero_ctas.items()), columns=["CTA", "Count"])
        total_posts = cta_df_all["Count"].sum()
        no_cta_count = cta_df_all[cta_df_all["CTA"].str.lower().isin(["none", "no cta"])]["Count"].sum()
        no_cta_pct = no_cta_count / max(total_posts, 1) * 100

        # Show only posts with a CTA (exclude None/No CTA — inflated by stories)
        cta_df = cta_df_all[~cta_df_all["CTA"].str.lower().isin(["none", "no cta"])]
        cta_df = cta_df.sort_values("Count", ascending=True)
        cta_df["Pct"] = (cta_df["Count"] / cta_df["Count"].sum() * 100).round(1) if cta_df["Count"].sum() > 0 else 0

        if len(cta_df):
            fig_cta = px.bar(cta_df, x="Count", y="CTA", orientation="h",
                             color_discrete_sequence=["#F8C090"],
                             labels={"Count": "# Posts", "CTA": ""},
                             template=CHART_TEMPLATE,
                             text=cta_df["Pct"].apply(lambda x: f"{x:.0f}%"))
            fig_cta.update_layout(font=CHART_FONT, height=max(250, len(cta_df) * 40), showlegend=False)
            st.plotly_chart(fig_cta, use_container_width=True)

        top_cta = cta_df.iloc[-1] if len(cta_df) else None
        if top_cta is not None and no_cta_pct > 30:
            st.info(f"**Most used CTA: {top_cta['CTA']}** ({top_cta['Pct']:.0f}% of posts with a CTA). "
                    f"**Watch:** {no_cta_pct:.0f}% of feed posts have no clear CTA — missed conversion opportunities.")
        else:
            st.info(f"**Most used CTA: {top_cta['CTA']}** ({top_cta['Pct']:.0f}%). "
                    f"Good CTA coverage — keep testing engagement-driving CTAs like 'Tag a friend' or 'Share to story'.")
    else:
        st.info(_perf.get("no_cta_data", f"No CTA data available for {HERO}."))

    st.markdown("---")

    # ── Best & Worst Posts ─────────────────────────────────────────────
    st.subheader("Best & Worst Posts")

    def _post_label(row):
        pillar = row.get("content_pillar", "") or ""
        collab = row.get("collaboration", "") or ""
        parts = [row.get("post_type", "")]
        if pillar:
            parts.append(pillar)
        if collab:
            parts.append(collab)
        return " | ".join(p for p in parts if p)

    def _render_post_list(source_df, label_best="Top 10", label_worst="Bottom 10"):
        """Render best/worst posts for a DataFrame, split by platform."""
        _has_platform = "platform" in source_df.columns
        if _has_platform:
            ig_df = source_df[source_df["platform"].str.lower().str.contains("instagram", na=False)]
            tt_df = source_df[source_df["platform"].str.lower().str.contains("tiktok", na=False)]
        else:
            ig_df = source_df
            tt_df = pd.DataFrame()

        for plat_label, plat_df in [("Instagram", ig_df), ("TikTok", tt_df)]:
            if len(plat_df) == 0:
                continue
            st.markdown(f"#### {plat_label}")
            col_best, col_worst = st.columns(2)
            with col_best:
                st.markdown(f"**{label_best} by Engagements**")
                top5 = plat_df.nlargest(10, "total_engagement").reset_index(drop=True)
                top5.index = top5.index + 1
                for idx, row in top5.iterrows():
                    caption_preview = str(row.get("caption_text", ""))[:100]
                    if caption_preview == "nan":
                        caption_preview = ""
                    eng_val = row["total_engagement"]
                    url = row.get("post_url", "")
                    with st.expander(f"#{idx} — {eng_val:,} eng | {_post_label(row)}"):
                        if caption_preview:
                            st.markdown(f"*\"{caption_preview}...\"*")
                        st.caption(f"Likes: {row.get('likes', 0):,} | Comments: {row.get('comments', 0):,} | "
                                   f"Shares: {row.get('shares', 0):,} | Saves: {row.get('saves', 0):,}")
                        if url:
                            st.markdown(f"[View post]({url})")

            with col_worst:
                st.markdown(f"**{label_worst} by Engagements**")
                bottom5 = plat_df.nsmallest(10, "total_engagement").reset_index(drop=True)
                bottom5.index = bottom5.index + 1
                for idx, row in bottom5.iterrows():
                    caption_preview = str(row.get("caption_text", ""))[:100]
                    if caption_preview == "nan":
                        caption_preview = ""
                    eng_val = row["total_engagement"]
                    url = row.get("post_url", "")
                    with st.expander(f"#{idx} — {eng_val:,} eng | {_post_label(row)}"):
                        if caption_preview:
                            st.markdown(f"*\"{caption_preview}...\"*")
                        st.caption(f"Likes: {row.get('likes', 0):,} | Comments: {row.get('comments', 0):,} | "
                                   f"Shares: {row.get('shares', 0):,} | Saves: {row.get('saves', 0):,}")
                        if url:
                            st.markdown(f"[View post]({url})")

    if len(hero_df):
        if len(hero_collab):
            bw_owned_tab, bw_collab_tab = st.tabs(["Brand-Owned Posts", "Collab Posts"])
            with bw_owned_tab:
                if len(hero_owned):
                    _render_post_list(hero_owned)
                else:
                    st.info(f"No brand-owned {HERO} posts in the dataset.")
            with bw_collab_tab:
                st.caption("These posts appeared on Cuervo's feed via collab. "
                           "Engagement reflects the partner's audience reach.")
                _render_post_list(hero_collab, label_best="Top Collab", label_worst="Bottom Collab")
        else:
            _render_post_list(hero_owned)
    else:
        st.info(_perf.get("no_posts", f"No {HERO} posts in the dataset."))

    # ── Collaboration Type Breakdown ──────────────────────────────────
    # Use feed posts only (exclude stories)
    _hero_feed_collab = hero_df[hero_df["is_story"].astype(str).str.lower() != "yes"] if "is_story" in hero_df.columns else hero_df
    if "collaboration" in _hero_feed_collab.columns and _hero_feed_collab["collaboration"].notna().any():
        st.divider()
        st.subheader("Collaboration Type Breakdown")
        st.caption("Who's creating the content — brand-owned vs. partners, influencers, and collective")

        collab_data = []
        for collab_type in _hero_feed_collab["collaboration"].dropna().unique():
            collab_posts = _hero_feed_collab[_hero_feed_collab["collaboration"] == collab_type]
            collab_pct = len(collab_posts) / max(len(_hero_feed_collab), 1) * 100
            avg_eng = collab_posts["total_engagement"].mean() if len(collab_posts) else 0
            avg_eng = 0 if pd.isna(avg_eng) else avg_eng
            collab_data.append({
                "Type": collab_type,
                "Posts": len(collab_posts),
                "% of Content": round(collab_pct, 1),
                "Avg Engagement": round(avg_eng, 0),
            })

        collab_df = pd.DataFrame(collab_data).sort_values("% of Content", ascending=False)
        collab_colors = {"Cuervo": "#2ea3f2", "Partner": "#66BB6A", "Influencer": "#F8C090", "Collective": "#C9A87E"}

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown("**Content by Collaboration Type**")
            fig_collab = px.bar(collab_df, x="Type", y="% of Content",
                                color="Type", color_discrete_map=collab_colors,
                                template=CHART_TEMPLATE, text_auto=".0f")
            fig_collab.update_layout(showlegend=False, font=CHART_FONT, height=380,
                                     yaxis_title="% of Content")
            st.plotly_chart(fig_collab, use_container_width=True)

        with col_c2:
            st.markdown("**Avg Engagement by Collaboration Type**")
            fig_collab_eng = px.bar(collab_df, x="Type", y="Avg Engagement",
                                    color="Type", color_discrete_map=collab_colors,
                                    template=CHART_TEMPLATE, text_auto=",.0f")
            fig_collab_eng.update_layout(showlegend=False, font=CHART_FONT, height=380,
                                         yaxis_title="Avg Engagements")
            st.plotly_chart(fig_collab_eng, use_container_width=True)

        if len(collab_df):
            top = collab_df.iloc[0]
            best_eng = collab_df.sort_values("Avg Engagement", ascending=False).iloc[0]
            st.info(f"**Most used:** {top['Type']} ({top['% of Content']:.0f}% of posts). "
                    f"**Highest engagement:** {best_eng['Type']} ({best_eng['Avg Engagement']:,.0f} avg eng/post).")


# ══════════════════════════════════════════════════════════════════════
# TAB 3 — Self-Audit Intelligence
# ══════════════════════════════════════════════════════════════════════

with tab_audit:

    autostrat = st.session_state.get("autostrat", {})
    _has_autostrat = has_autostrat_data(autostrat)

    if not _has_autostrat:
        st.info(_perf.get("no_self_audit",
               f"No {HERO} self-audit reports found. Import autostrat PDFs for this brand."))
    else:
        # ── Gather all hero-brand-related hashtag reports dynamically ──────
        hero_reports = []

        # Brand hashtags (hero_hashtag_ids) across all platforms
        for rt in CONVERSATION_TYPES:
            for ident in cfg.hero_hashtag_ids:
                rpt = get_report(autostrat, rt, ident)
                if rpt:
                    plat = platform_label(rt)
                    label = cfg.brand_hashtags.get(ident, f"#{ident}")
                    hero_reports.append((ident, f"{label} ({plat})", rpt))

        # Category hashtags (margaritatime, etc.) across all platforms
        for rt in CONVERSATION_TYPES:
            for ident, display in cfg.category_hashtags.items():
                rpt = get_report(autostrat, rt, ident)
                if rpt:
                    plat = platform_label(rt)
                    hero_reports.append((ident, f"{display} ({plat})", rpt))

        if not hero_reports:
            st.info(_perf.get("no_self_audit",
                   f"No {HERO} self-audit reports found. Import autostrat PDFs for this brand."))
        else:
            for report_id, report_label, report in hero_reports:
                with st.expander(report_label):

                    # Executive Summary
                    es = report.get("executive_summary", {})
                    if es.get("key_insights"):
                        render_section_label("Key Insights")
                        insights = es["key_insights"]
                        # Skip first if it duplicates the search prompt
                        if len(insights) > 1:
                            insights = insights[1:]
                        cols = st.columns(min(len(insights), 2))
                        for i, insight in enumerate(insights[:4]):
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
                        render_section_label("Audience Verbatims")
                        render_verbatim_quotes(verbatims, max_quotes=8)

        # ── Google News ───────────────────────────────────────────────
        news_report = get_report(autostrat, "google_news", cfg.hero_news_id) if cfg.hero_news_id else None
        if news_report:
            with st.expander(f"Google News: {HERO}"):

                # Overview
                exec_sum = news_report.get("executive_summary", {})
                overview = exec_sum.get("overview", "")
                if overview:
                    render_narrative_card("News Overview", overview, accent_color=cfg.accent_color)

                # Sentiment breakdown
                news_analysis = news_report.get("news_analysis", {})
                sentiment = news_analysis.get("sentiment_breakdown", {})
                pos = sentiment.get("positive_pct", 0)
                neu = sentiment.get("neutral_pct", 0)
                neg = sentiment.get("negative_pct", 0)
                if pos or neu or neg:
                    s1, s2, s3 = st.columns(3)
                    with s1:
                        st.metric("Positive", f"{pos}%")
                    with s2:
                        st.metric("Neutral", f"{neu}%")
                    with s3:
                        st.metric("Negative", f"{neg}%")

                # SWOT
                swot = news_report.get("swot_analysis", {})
                has_swot = any(swot.get(k) for k in ["strengths", "weaknesses", "opportunities", "threats"])
                if has_swot:
                    render_section_label("SWOT Analysis")
                    sw_col, ot_col = st.columns(2)
                    with sw_col:
                        for key, label, color in [("strengths", "Strengths", "#5CB85C"), ("weaknesses", "Weaknesses", "#D9534F")]:
                            items = swot.get(key, [])
                            if items:
                                for item in items:
                                    st.markdown(f"- **{label}:** {item}")
                    with ot_col:
                        for key, label, color in [("opportunities", "Opportunities", "#2ea3f2"), ("threats", "Threats", "#F8C090")]:
                            items = swot.get(key, [])
                            if items:
                                for item in items:
                                    st.markdown(f"- **{label}:** {item}")

                # Strategic Implications
                strat = news_report.get("strategic_implications", {})
                action_items = strat.get("action_items", [])
                if action_items:
                    render_section_label("News Action Items")
                    render_territory_cards(action_items)
