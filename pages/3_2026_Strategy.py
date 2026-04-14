"""
Page 3: 2026 Strategy & Brief — "The Playbook"
Dedicated to the Social Brief. Uses unfiltered data — sidebar filters do NOT apply.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from config import CHART_TEMPLATE, CHART_FONT, PRIORITY_COLORS, COLLAB_AMPLIFIED_TYPES
from client_context import get_client
from autostrat_loader import (
    has_autostrat_data, get_all_how_to_win, get_all_audience_profiles,
    get_all_content_trends, get_all_creator_archetypes,
    get_all_strategic_actions, get_all_sponsorship_suggestions,
)
from autostrat_components import (
    render_narrative_card, render_creator_archetype, render_sponsorship_card,
)
from ui_components import (
    render_page_hero, render_kpi_section_label, render_poplife_note,
    render_north_star, render_sku_card, render_sku_usage_card,
    render_engine_card, render_voice_card,
    render_ig_format_card, render_partner_event, render_quarter_card,
    render_swot_card, render_connect_callout,
    render_pillar_card, render_content_card_open, render_content_card_close,
    render_kpi_card, render_nopd_grid, render_territory_list,
)

if "results" not in st.session_state:
    st.warning("Go to the home page first to load data.")
    st.stop()

cfg = get_client()

st.logo(cfg.app_logo_path)
st.markdown(cfg.custom_css, unsafe_allow_html=True)

results = st.session_state["results"]
df = st.session_state["df"]  # Unfiltered

HERO = cfg.hero_brand
GEN_Z_LEADERS = cfg.gen_z_leaders
_t = cfg.kpi_targets
ENG_PER_POST_TARGET = _t["engagements_per_post"]

hero_df_full = df[df["brand"] == HERO]  # Stories already excluded in app.py; includes Edutain dupes for content mix funnel
hero_df = hero_df_full[hero_df_full["_mix_weight"] >= 1.0] if "_mix_weight" in hero_df_full.columns else hero_df_full
# Stories stored separately in session state for story volume KPIs
hero_stories = st.session_state.get("stories_df", pd.DataFrame())
hero_stories = hero_stories[hero_stories["brand"] == HERO] if len(hero_stories) else hero_stories
# Keep unfiltered copy for collaboration breakdown sections (which intentionally show Influencer data)
hero_df_with_influencer = hero_df.copy()
# Exclude collab posts (Influencer + Collective) from engagement metrics (they inflate due to higher reach)
if "collaboration" in hero_df.columns:
    hero_df = hero_df[~hero_df["collaboration"].str.strip().str.lower().isin(COLLAB_AMPLIFIED_TYPES)]
leader_df = df[df["brand"].isin(GEN_Z_LEADERS)]
if "collaboration" in leader_df.columns:
    leader_df = leader_df[~leader_df["collaboration"].str.strip().str.lower().isin(COLLAB_AMPLIFIED_TYPES)]

def _render_north_star():
    """Render the brand North Star dark callout if configured."""
    ns = cfg.north_star
    if not ns:
        return
    render_north_star(
        title=ns.get("title", ""),
        tagline=ns.get("tagline", ""),
        body=ns.get("description", ""),
    )


# ── Page hero ─────────────────────────────────────────────────────────
render_page_hero(
    title="The Playbook",
    kicker=f"{HERO} · 2026 Strategy",
    subtitle=cfg.page_captions.get(
        "strategy",
        f"The {HERO} Social Brief playbook — sidebar filters do not apply here.",
    ),
    stats=[
        {"value": str(len(cfg.pillar_map)), "label": "Content pillars"},
        {"value": str(len(cfg.content_mix_targets)), "label": "Funnel stages"},
        {"value": str(len(cfg.kpi_targets)), "label": "KPI targets"},
        {"value": str(len(cfg.platform_roles)), "label": "Platforms"},
    ],
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
tab_scorecard, tab_frameworks, tab_platform, tab_action = st.tabs([
    "Social Brief Scorecard", "Content Strategy Frameworks",
    "Platform Strategies", "Action Plan",
])

# ══════════════════════════════════════════════════════════════════════
# TAB 1 — Social Brief Scorecard
# ══════════════════════════════════════════════════════════════════════

with tab_scorecard:
    _render_north_star()

    # ── Expanded KPI Scorecard ─────────────────────────────────────────
    render_kpi_section_label("KPI scorecard")
    st.caption("Current performance vs 2026 Social Brief targets")

    hero_ig = hero_df[hero_df["platform"] == "Instagram"]
    avg_eng_per_post = hero_df["total_engagement"].mean() if len(hero_df) else 0
    avg_eng_per_post = 0 if pd.isna(avg_eng_per_post) else avg_eng_per_post
    reel_ratio = len(hero_ig[hero_ig["post_type"] == "Reel"]) / max(len(hero_ig), 1) * 100
    carousel_ratio = len(hero_ig[hero_ig["post_type"] == "Carousel"]) / max(len(hero_ig), 1) * 100

    # Save & share rates
    total_eng = hero_df["total_engagement"].sum() or 1
    save_rate = (hero_df["saves"].sum() / total_eng * 100) if "saves" in hero_df.columns else 0
    share_rate = (hero_df["shares"].sum() / total_eng * 100) if "shares" in hero_df.columns else 0

    freq = results["frequency"].get(HERO, {})
    ig_ppm = freq.get("Instagram", {}).get("posts_per_week", 0) * 4.33  # Convert to monthly
    tt_ppw = freq.get("TikTok", {}).get("posts_per_week", 0)
    tt_ppm = tt_ppw * 4.33
    # TODO: TikTok metrics show zeros when no TikTok data in Sprout exports — add graceful empty state

    # ── Monthly volume metrics (owned posts only) ──────────────────────
    hero_feed = hero_df  # Stories already excluded from hero_df above

    # Filter to owned posts for volume metrics
    from config import split_owned_collab
    _hero_owned_sc, _ = split_owned_collab(hero_feed)

    # Calculate months in dataset for averaging
    if len(hero_df) and "post_date" in hero_df.columns:
        date_range = (hero_df["post_date"].max() - hero_df["post_date"].min()).days
        n_months = max(date_range / 30.44, 1)
    else:
        n_months = 1

    # Monthly totals (owned feed posts, averaged across months)
    saves_pm = pd.to_numeric(_hero_owned_sc["saves"], errors="coerce").fillna(0).sum() / n_months if "saves" in _hero_owned_sc.columns else 0
    shares_pm = pd.to_numeric(_hero_owned_sc["shares"], errors="coerce").fillna(0).sum() / n_months if "shares" in _hero_owned_sc.columns else 0
    likes_pm = pd.to_numeric(_hero_owned_sc["likes"], errors="coerce").fillna(0).sum() / n_months if "likes" in _hero_owned_sc.columns else 0
    comments_pm = pd.to_numeric(_hero_owned_sc["comments"], errors="coerce").fillna(0).sum() / n_months if "comments" in _hero_owned_sc.columns else 0

    # Reel/Video views per month (owned only — use views, not impressions, to avoid double-counting)
    hero_reels = _hero_owned_sc[_hero_owned_sc["post_type"].isin(["Reel", "Video"])]
    reel_views_pm = pd.to_numeric(hero_reels["views"], errors="coerce").fillna(0).sum() / n_months if len(hero_reels) else 0

    # Carousel/Static impressions per month (owned only)
    hero_static = _hero_owned_sc[~_hero_owned_sc["post_type"].isin(["Reel", "Video"])]
    carousel_imp_pm = pd.to_numeric(hero_static["impressions"], errors="coerce").fillna(0).sum() / n_months if "impressions" in hero_static.columns and len(hero_static) else 0

    # Stories per month (all stories — not filtered by owned since stories are always brand-posted)
    stories_pm = len(hero_stories) / n_months
    story_views_pm = pd.to_numeric(hero_stories["impressions"], errors="coerce").fillna(0).sum() / n_months if "impressions" in hero_stories.columns and len(hero_stories) else 0

    # Scorecard table (targets from kpi_targets in client config)
    _ig_ppm = _t["ig_posts_per_month"]
    _tt_ppm = _t.get("tt_posts_per_month", None) or (tuple(x * 4 for x in _t["tt_posts_per_week"]) if "tt_posts_per_week" in _t else (12, 20))

    def _vol_row(kpi, actual, target_key):
        tgt = _t.get(target_key, 0)
        return {"KPI": kpi, "Actual": f"{actual:,.0f}", "Target": f"{tgt:,}/mo",
                "Status": "ON TRACK" if actual >= tgt else "BELOW",
                "Gap": f"{actual - tgt:+,.0f}"}

    scorecard_data = [
        {"KPI": "Avg Eng/Post", "Actual": f"{avg_eng_per_post:,.0f}",
         "Target": f"{_t['engagements_per_post']:,}+",
         "Status": "ON TRACK" if avg_eng_per_post >= _t["engagements_per_post"] else "BELOW",
         "Gap": f"{avg_eng_per_post - _t['engagements_per_post']:+,.0f}"},
        {"KPI": "Save Rate", "Actual": f"{save_rate:.1f}%",
         "Target": f"{_t['save_rate']}%+",
         "Status": "ON TRACK" if save_rate >= _t["save_rate"] else "BELOW",
         "Gap": f"{save_rate - _t['save_rate']:+.1f}pp"},
        {"KPI": "Share Rate", "Actual": f"{share_rate:.1f}%",
         "Target": f"{_t['share_rate']}%+",
         "Status": "ON TRACK" if share_rate >= _t["share_rate"] else "BELOW",
         "Gap": f"{share_rate - _t['share_rate']:+.1f}pp"},
        {"KPI": "Reel Ratio (IG)", "Actual": f"{reel_ratio:.0f}%",
         "Target": f"{_t['reel_ratio']}%",
         "Status": "ON TRACK" if reel_ratio >= _t["reel_ratio"] else "BELOW",
         "Gap": f"{reel_ratio - _t['reel_ratio']:+.0f}pp"},
        {"KPI": "IG Posts/Month", "Actual": f"{ig_ppm:.0f}",
         "Target": f"{_ig_ppm[0]}-{_ig_ppm[1]}/mo",
         "Status": "ON TRACK" if _ig_ppm[0] <= ig_ppm <= _ig_ppm[1] else ("BELOW" if ig_ppm < _ig_ppm[0] else "ABOVE"),
         "Gap": f"{ig_ppm - sum(_ig_ppm)/2:+.0f} vs mid"},
        {"KPI": "TT Posts/Month", "Actual": f"{tt_ppm:.0f}",
         "Target": f"{_tt_ppm[0]}-{_tt_ppm[1]}/mo",
         "Status": "ON TRACK" if _tt_ppm[0] <= tt_ppm <= _tt_ppm[1] else ("BELOW" if tt_ppm < _tt_ppm[0] else "ABOVE"),
         "Gap": f"{tt_ppm - sum(_tt_ppm)/2:+.0f} vs mid"},
        _vol_row("Likes/Month", likes_pm, "likes_per_month"),
        _vol_row("Comments/Month", comments_pm, "comments_per_month"),
        _vol_row("Saves/Month", saves_pm, "saves_per_month"),
        _vol_row("Shares/Month", shares_pm, "shares_per_month"),
        _vol_row("Reel Views/Mo", reel_views_pm, "reel_views_per_month"),
        _vol_row("Carousel Imp/Mo", carousel_imp_pm, "carousel_impressions_per_month"),
        _vol_row("Stories/Month", stories_pm, "stories_per_month"),
        _vol_row("Story Views/Month", story_views_pm, "story_views_per_month"),
    ]

    sc_df = pd.DataFrame(scorecard_data)

    def color_status(val):
        if val == "ON TRACK":
            return "background-color: #C8E6C9; color: #2E7D32; font-weight: bold"
        elif val == "BELOW":
            return "background-color: #FFCDD2; color: #C62828; font-weight: bold"
        elif val == "ABOVE":
            return "background-color: #FFE0B2; color: #E65100; font-weight: bold"
        elif val == "INFO":
            return "background-color: #E3F2FD; color: #1565C0; font-weight: bold"
        return ""

    st.dataframe(
        sc_df.style.map(color_status, subset=["Status"]),
        use_container_width=True, hide_index=True, height=560,
    )

    on_track = sum(1 for s in scorecard_data if s["Status"] == "ON TRACK")
    total = len(scorecard_data)
    _summary = (
        "Strong position — maintain momentum."
        if on_track >= 4
        else "Focus areas identified below."
        if on_track >= 2
        else "Significant gaps — prioritize the Action Plan tab."
    )
    render_poplife_note(
        f"<strong>{on_track}/{total} KPIs on track.</strong> {_summary}",
        variant="success" if on_track >= 4 else "default",
    )

    st.caption("**Reel Views** = number of times the video was played. **Carousel/Static Impressions** = number of times the post appeared on screen. "
               "These are different metrics — impressions are typically higher than views for equivalent reach.")

    st.markdown("---")

    if not cfg.themes_ready:
        st.markdown("---")
        render_poplife_note(
            f"<strong>Content source mix & theme analysis hidden</strong> — post-level theme "
            f"tagging is not yet complete for {HERO}. These sections will appear once all "
            f"posts have been manually reviewed and tagged.",
            variant="warning",
        )


# ══════════════════════════════════════════════════════════════════════
# TAB 2 — Content Strategy Frameworks
# ══════════════════════════════════════════════════════════════════════

with tab_frameworks:
    _render_north_star()

    # ── Content Pillars (4 pillars from 2026 deck) ──────────────────────
    # NOTE: Pillar distribution uses ALL posts (owned + collab) to reflect total content strategy mix.
    # This may change to owned-only in a future revision.
    _pillar_base = hero_df_with_influencer
    render_kpi_section_label("Content pillars")
    st.caption("4 pillars from the 2026 Social Strategy — SKU-aligned content territories")

    pillar_data = []
    for pillar_name, themes in cfg.pillar_map.items():
        # Distribution % from all posts (owned + collab)
        if "content_pillar" in _pillar_base.columns:
            matching_all = _pillar_base[_pillar_base["content_pillar"].astype(str).str.strip() == pillar_name]
        else:
            matching_all = _pillar_base[_pillar_base["content_theme"].isin(themes)]
        pct = len(matching_all) / max(len(_pillar_base), 1) * 100
        # Avg engagement from owned-only (collab posts inflate engagement)
        if "content_pillar" in hero_df.columns:
            matching_owned = hero_df[hero_df["content_pillar"].astype(str).str.strip() == pillar_name]
        else:
            matching_owned = hero_df[hero_df["content_theme"].isin(themes)]
        avg_eng = matching_owned["total_engagement"].mean() if len(matching_owned) else 0
        avg_eng = 0 if pd.isna(avg_eng) else avg_eng
        pillar_data.append({
            "Pillar": pillar_name,
            "Actual %": round(pct, 1),
            "Target %": cfg.pillar_targets[pillar_name],
            "Avg Eng": round(avg_eng, 0),
            "Posts": len(matching_all),
            "desc": cfg.pillar_descriptions.get(pillar_name, ""),
        })

    pillar_df = pd.DataFrame(pillar_data)

    # Pillar detail cards (Treatment C with per-pillar accent colors)
    for _, row in pillar_df.iterrows():
        render_pillar_card(
            name=row["Pillar"],
            actual_pct=row["Actual %"],
            target_pct=row["Target %"],
            description=row["desc"],
            post_count=int(row["Posts"]),
            avg_eng=row["Avg Eng"],
            accent_color=cfg.pillar_colors[row["Pillar"]],
        )

    col_pd1, col_pd2 = st.columns(2)
    with col_pd1:
        st.markdown("**Pillar Distribution: Actual vs Target**")
        fig_pd = go.Figure()
        fig_pd.add_trace(go.Bar(x=pillar_df["Pillar"], y=pillar_df["Actual %"],
                                name="Actual", marker_color=[cfg.pillar_colors[p] for p in pillar_df["Pillar"]],
                                text=pillar_df["Actual %"], textposition="outside", texttemplate="%{text:.0f}%"))
        fig_pd.add_trace(go.Scatter(x=pillar_df["Pillar"], y=pillar_df["Target %"],
                                    name="Target", mode="markers+lines",
                                    marker=dict(size=12, color="#333333", symbol="diamond"),
                                    line=dict(color="#333333", width=2, dash="dash")))
        fig_pd.update_layout(template=CHART_TEMPLATE, font=CHART_FONT, height=380,
                             yaxis_title="% of Content", legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(fig_pd, use_container_width=True)

    with col_pd2:
        st.markdown("**Avg Engagements by Pillar**")
        fig_pe = px.bar(pillar_df, x="Pillar", y="Avg Eng",
                        color="Pillar", color_discrete_map=cfg.pillar_colors,
                        labels={"Avg Eng": "Avg Engagements", "Pillar": ""},
                        template=CHART_TEMPLATE, text_auto=",.0f")
        fig_pe.add_hline(y=ENG_PER_POST_TARGET, line_dash="dash", line_color="#333",
                         annotation_text=f"{ENG_PER_POST_TARGET} eng target", annotation_position="top right")
        fig_pe.update_layout(showlegend=False, font=CHART_FONT, height=380)
        st.plotly_chart(fig_pe, use_container_width=True)

    st.markdown("---")

    # ── SKU Strategy ────────────────────────────────────────────────────
    render_kpi_section_label("SKU strategy")
    st.caption("Each SKU has a distinct energy and occasion — content should match")

    sku_cols = st.columns(len(cfg.sku_strategy))
    for col, (sku, info) in zip(sku_cols, cfg.sku_strategy.items()):
        with col:
            render_sku_card(
                name=sku,
                energy=info.get("energy", ""),
                occasions=info.get("occasions", ""),
            )

    # ── SKU Usage by Occasion ───────────────────────────────────────────
    # Matrix from the "Role of Variants" Mar 2026 deck: 17 occasions mapped
    # to which SKU variant should lead. Inverted here from occasion→SKU into
    # SKU→occasions so each card reads as a content-planning checklist.
    if cfg.sku_usage_matrix:
        st.markdown("")
        render_kpi_section_label("SKU usage by occasion")
        st.caption(
            "Source: Cuervo *Role of Variants* deck, Mar 2026. "
            "Use this as a content-planning reference — pick the occasion, read which SKU leads. "
            "Some occasions map to multiple variants."
        )

        # Preserve the order of cfg.sku_strategy for consistent column ordering.
        # Fall back to order-of-first-appearance in the matrix for any extras.
        sku_order = []
        for sku_name in cfg.sku_strategy.keys():
            display = "RTDs" if sku_name.upper() == "RTD" else sku_name
            sku_order.append(display)
        # Build SKU -> [occasions] from the occasion -> [SKUs] matrix.
        sku_to_occasions = {s: [] for s in sku_order}
        for occasion, sku_list in cfg.sku_usage_matrix.items():
            for sku in sku_list:
                if sku not in sku_to_occasions:
                    sku_to_occasions[sku] = []
                    sku_order.append(sku)
                sku_to_occasions[sku].append(occasion)

        usage_cols = st.columns(len(sku_order))
        for col, sku_name in zip(usage_cols, sku_order):
            with col:
                render_sku_usage_card(
                    name=sku_name,
                    occasions=sku_to_occasions.get(sku_name, []),
                )

    st.markdown("---")

    # ── 4 Execution Engines ─────────────────────────────────────────────
    render_kpi_section_label("The 4 execution engines")
    st.caption("How content gets made across both pillars")

    eng_cols = st.columns(2)
    for i, (engine, desc) in enumerate(cfg.execution_engines.items()):
        with eng_cols[i % 2]:
            render_engine_card(name=engine, description=desc)

    st.markdown("---")

    # ── Collaboration Mix ──────────────────────────────────────────────
    if cfg.themes_ready and "collaboration" in hero_df_with_influencer.columns and hero_df_with_influencer["collaboration"].notna().any():
        render_kpi_section_label("Collaboration mix")

        collab_total = max(len(hero_df_with_influencer[hero_df_with_influencer["collaboration"].notna()]), 1)
        collab_colors = {"Cuervo": "#2ea3f2", "Partner": "#66BB6A", "Influencer": "#F8C090", "Collective": "#C9A87E"}
        src_rows = []
        for collab_type in sorted(hero_df_with_influencer["collaboration"].dropna().unique()):
            count = len(hero_df_with_influencer[hero_df_with_influencer["collaboration"] == collab_type])
            avg_eng = hero_df_with_influencer[hero_df_with_influencer["collaboration"] == collab_type]["total_engagement"].mean()
            avg_eng = 0 if pd.isna(avg_eng) else avg_eng
            src_rows.append({
                "Source": collab_type,
                "Posts": count,
                "% of Content": round(count / collab_total * 100, 1),
                "Avg Eng": round(avg_eng, 0),
            })
        src_data = pd.DataFrame(src_rows).sort_values("% of Content", ascending=False)

        render_content_card_open(
            title=f"{HERO} collaboration breakdown",
            caption="Who is creating the brand's content — based on manual post tagging",
        )
        col_src1, col_src2 = st.columns([1.3, 1])
        with col_src1:
            fig_src = px.bar(src_data, x="Source", y="% of Content",
                             color="Source", color_discrete_map=collab_colors,
                             text="% of Content", template=CHART_TEMPLATE,
                             labels={"% of Content": "% of Content", "Source": ""})
            fig_src.update_traces(texttemplate="%{text:.0f}%", textposition="outside")
            fig_src.update_layout(font=CHART_FONT, height=360, showlegend=False,
                                  yaxis_title="% of Content",
                                  margin=dict(l=10, r=10, t=20, b=10))
            st.plotly_chart(fig_src, use_container_width=True)

        with col_src2:
            for _, row in src_data.iterrows():
                render_kpi_card(
                    label=row["Source"],
                    value=f"{row['% of Content']:.0f}%",
                    meta=f"{int(row['Posts'])} posts · {row['Avg Eng']:,.0f} avg eng",
                )
        render_content_card_close()

        best_collab = src_data.iloc[0]
        render_poplife_note(
            f"<strong>Top collaboration type: {best_collab['Source']}</strong> at "
            f"{best_collab['% of Content']:.0f}% of content with {best_collab['Avg Eng']:,.0f} "
            f"avg engagements.",
            variant="success",
        )

        st.markdown("---")

    # ── Best Performing Pillar ──────────────────────────────────────────
    # Uses owned-only posts (collab filtered out) for engagement comparison
    if cfg.themes_ready:
        _has_pillar_col = "content_pillar" in hero_df.columns and hero_df["content_pillar"].notna().any()
        if _has_pillar_col:
            render_kpi_section_label("Best performing content pillar")
            st.caption(f"Which content pillar drives the highest engagement for {HERO}")

            pillar_perf = (hero_df[hero_df["content_pillar"].notna()]
                           .groupby("content_pillar")
                           .agg(avg_eng=("total_engagement", "mean"), count=("total_engagement", "size"))
                           .reset_index()
                           .sort_values("avg_eng", ascending=False))
            pillar_perf["avg_eng"] = pillar_perf["avg_eng"].round(0)

            best_pillar = pillar_perf.iloc[0]
            bt_col1, bt_col2, bt_col3 = st.columns(3)
            with bt_col1:
                st.metric("Best Pillar", best_pillar["content_pillar"])
            with bt_col2:
                st.metric("Avg Engagements", f"{best_pillar['avg_eng']:,.0f}",
                          delta=f"{best_pillar['avg_eng'] - ENG_PER_POST_TARGET:+,.0f} vs {ENG_PER_POST_TARGET} target")
            with bt_col3:
                st.metric("Posts", f"{best_pillar['count']}")

            pillar_chart = pillar_perf.sort_values("avg_eng", ascending=True)
            fig_bt = px.bar(pillar_chart, x="avg_eng", y="content_pillar", orientation="h",
                            color="content_pillar", color_discrete_map=cfg.pillar_colors,
                            labels={"avg_eng": "Avg Engagements", "content_pillar": ""},
                            template=CHART_TEMPLATE, text_auto=",.0f",
                            hover_data={"count": True})
            fig_bt.add_vline(x=ENG_PER_POST_TARGET, line_dash="dash", line_color="#333",
                             annotation_text=f"{ENG_PER_POST_TARGET} eng target")
            fig_bt.update_layout(font=CHART_FONT, height=max(280, len(pillar_chart) * 50),
                                 showlegend=False)
            st.plotly_chart(fig_bt, use_container_width=True)

            render_poplife_note(
                f"<strong>Best pillar: {best_pillar['content_pillar']}</strong> at "
                f"{best_pillar['avg_eng']:,.0f} avg engagements — lean into this for upcoming "
                f"content. Pillars above the {ENG_PER_POST_TARGET} eng target are proven winners "
                f"worth scaling.",
                variant="success",
            )

        st.markdown("---")

    # ── The Creator Crew (Creator Archetypes) ────────────────────────
    _crew_header = cfg.narrative.get("strategy", {}).get("crew_header", f"The {HERO} Crew — Creator Archetypes")
    render_kpi_section_label(_crew_header)
    st.caption("Creators embedded in the brand — not hired talent. iPhone-first. Social-native.")

    # Prefer brief-defined archetypes (curated by social team, always complete).
    # Autostrat-derived archetypes are a fallback only — they mix competitor
    # archetypes with hero brand ones and often have missing descriptions.
    if cfg.creator_archetypes:
        arch_cols = st.columns(min(len(cfg.creator_archetypes), 5))
        for i, (archetype, fit) in enumerate(cfg.creator_archetypes.items()):
            with arch_cols[i % len(arch_cols)]:
                st.markdown(f"""<div style="background:white; border-radius:10px; padding:14px; text-align:center; border:1px solid #E0D8D0; min-height:100px;"><p style="font-weight:700; color:#333; margin:0 0 6px 0; font-size:0.9rem;">{archetype}</p><p style="color:#666; font-size:0.82rem; margin:0;">{fit}</p></div>""", unsafe_allow_html=True)
    else:
        # Fallback to autostrat-derived archetypes
        _autostrat_tmp = st.session_state.get("autostrat", {})
        _autostrat_archetypes = get_all_creator_archetypes(_autostrat_tmp) if has_autostrat_data(_autostrat_tmp) else []
        if _autostrat_archetypes:
            _arch_cols = st.columns(min(len(_autostrat_archetypes[:6]), 3))
            for i, arch in enumerate(_autostrat_archetypes[:6]):
                with _arch_cols[i % len(_arch_cols)]:
                    render_creator_archetype(arch)
            st.caption(f"*From autostrat.ai analysis — {len(_autostrat_archetypes)} archetypes identified*")

    st.markdown("---")

    # ── Content Mix Funnel ─────────────────────────────────────────────
    # Only show if posts have content_mix_funnel tags
    _mix_src_check = hero_df_full if "hero_df_full" in dir() else hero_df
    _has_funnel_data = ("content_mix_funnel" in _mix_src_check.columns
                        and _mix_src_check["content_mix_funnel"].notna().any()
                        and (_mix_src_check["content_mix_funnel"].astype(str).str.strip() != "").any())
    _mix_cats = list(cfg.content_mix_targets.keys())
    if _has_funnel_data:
        render_kpi_section_label(f"Content mix funnel — {' / '.join(_mix_cats)} / Connect")
        st.caption(f"Grab attention first ({_mix_cats[0]} {cfg.content_mix_targets[_mix_cats[0]]}%), then guide to action ({_mix_cats[-1]} {cfg.content_mix_targets[_mix_cats[-1]]}%)")

        hero_mix_data = []
        # Use hero_df_full but exclude stories (includes Edutain dupes with _mix_weight=0.5)
        _mix_src = hero_df_full if "hero_df_full" in dir() else hero_df
        if "is_story" in _mix_src.columns:
            _mix_src = _mix_src[_mix_src["is_story"].astype(str).str.lower() != "yes"]
        has_weight = "_mix_weight" in _mix_src.columns
        total_weight = _mix_src["_mix_weight"].sum() if has_weight else len(_mix_src)
        for cat in _mix_cats:
            if "content_mix_funnel" in _mix_src.columns:
                matching = _mix_src[_mix_src["content_mix_funnel"] == cat]
                if has_weight:
                    pct = matching["_mix_weight"].sum() / max(total_weight, 1) * 100
                else:
                    pct = len(matching) / max(len(_mix_src), 1) * 100
            else:
                cat_themes = cfg.content_mix_map[cat]
                matching = _mix_src[_mix_src["content_theme"].isin(cat_themes)]
                pct = len(matching) / max(len(_mix_src), 1) * 100
            target = cfg.content_mix_targets.get(cat, 0)
            hero_mix_data.append({
                "Category": cat,
                "Actual %": round(pct, 1),
                "Target %": target,
                "Gap": round(pct - target, 1),
                "Posts": len(matching),
            })

        mix_df = pd.DataFrame(hero_mix_data)

        render_content_card_open(
            title=f"{HERO} content mix: actual vs Poplife target",
            caption="Funnel logic — Entertain grabs attention → Educate builds relevance → Connect fosters relationships → Convince drives action",
        )
        col_mix1, col_mix2 = st.columns([1.3, 1])
        with col_mix1:
            fig_mix = go.Figure()
            fig_mix.add_trace(go.Bar(x=mix_df["Category"], y=mix_df["Actual %"],
                                     name="Actual", marker_color=[cfg.content_mix_colors.get(c, "#999999") for c in mix_df["Category"]],
                                     text=mix_df["Actual %"], textposition="outside", texttemplate="%{text:.0f}%"))
            fig_mix.add_trace(go.Scatter(x=mix_df["Category"], y=mix_df["Target %"],
                                         name="Poplife Target", mode="markers+lines",
                                         marker=dict(size=12, color="#333333", symbol="diamond"),
                                         line=dict(color="#333333", width=2, dash="dash")))
            fig_mix.update_layout(template=CHART_TEMPLATE, font=CHART_FONT, height=360,
                                  yaxis_title="% of Content",
                                  legend=dict(orientation="h", y=-0.15),
                                  margin=dict(l=10, r=10, t=20, b=10))
            st.plotly_chart(fig_mix, use_container_width=True)

        with col_mix2:
            for _, row in mix_df.iterrows():
                direction = "MORE" if row["Gap"] < -5 else ("LESS" if row["Gap"] > 5 else "ON TRACK")
                _body = (
                    f"<strong>{row['Category']}</strong>: {row['Actual %']:.0f}% actual / "
                    f"{row['Target %']}% target ({row['Gap']:+.0f}%)"
                )
                if direction == "ON TRACK":
                    render_poplife_note(_body, variant="success")
                elif direction == "MORE":
                    render_poplife_note(_body + " — Need MORE", variant="danger")
                else:
                    render_poplife_note(_body + " — Need LESS", variant="warning")
        render_content_card_close()

        render_connect_callout(
            "Connect — Always On",
            "Connection isn't a content category — it's how we show up every day. Replying to "
            "comments, engaging in DMs, reposting fan content, and jumping into conversations in "
            "the feed. This layer runs underneath everything and turns passive followers into "
            "active community.",
        )

    st.markdown("---")

    # ── Voice Principles ────────────────────────────────────────────────
    render_kpi_section_label("Tone of voice — The Life of the Party")
    st.caption(f"{HERO}'s social voice: lively, approachable, human-forward, extroverted")

    for principle, detail in cfg.voice_principles:
        render_voice_card(name=principle, detail=detail)



# ══════════════════════════════════════════════════════════════════════
# TAB 3 — Platform Strategies
# ══════════════════════════════════════════════════════════════════════

with tab_platform:

    # ── Section 1: Platform Roles at a Glance ──────────────────────────
    render_kpi_section_label("Platform roles at a glance")

    # Build Treatment C styled platform roles table in a content-card wrapper
    _rows_html = ""
    for plat, info in cfg.platform_roles.items():
        is_primary = info["priority"] == "Primary"
        name_cell = (
            f'<strong>{plat}</strong>' if is_primary
            else f'<span style="color:#8A817C;">{plat}</span>'
        )
        role_cell = (
            info["role"] if is_primary
            else f'<span style="color:#8A817C;">{info["role"]}</span>'
        )
        cadence_cell = (
            info["cadence"] if is_primary
            else f'<span style="color:#8A817C;">{info["cadence"]}</span>'
        )
        priority_chip_style = (
            'background:rgba(248,192,144,0.2); color:#1A1A1A; font-weight:700;'
            if is_primary
            else ''
        )
        _rows_html += (
            f'<tr>'
            f'<td>{name_cell}</td>'
            f'<td>{role_cell}</td>'
            f'<td><span class="meta-chip" style="{priority_chip_style}">{info["priority"]}</span></td>'
            f'<td>{cadence_cell}</td>'
            f'</tr>'
        )

    _plat_html = (
        f'<div class="content-card">'
        f'<h3>Where {HERO} plays — all {len(cfg.platform_roles)} platforms</h3>'
        f'<div class="card-caption">Primary platforms get the budget. Secondary maintain brand presence and syndicate top content.</div>'
        f'<table>'
        f'<thead><tr><th>Platform</th><th>Role</th><th>Priority</th><th>Cadence</th></tr></thead>'
        f'<tbody>{_rows_html}</tbody>'
        f'</table>'
        f'</div>'
    )
    st.markdown(_plat_html, unsafe_allow_html=True)

    # ── Instagram Format Mix ─────────────────────────────────────────
    render_kpi_section_label("Instagram format mix")
    fmt_cols = st.columns(len(cfg.ig_format_mix))
    _fmt_variants = {"Reel": "reels", "Reels": "reels",
                     "Carousel": "carousel", "Carousels": "carousel",
                     "Static": "static", "Static Image": "static",
                     "Story": "story", "Stories": "story"}
    for i, (fmt, info) in enumerate(cfg.ig_format_mix.items()):
        with fmt_cols[i]:
            render_ig_format_card(
                pct=info["pct"],
                name=fmt,
                role=info.get("role", ""),
                variant=_fmt_variants.get(fmt, "reels"),
            )

    # ── Content Production Needs ─────────────────────────────────────────
    if cfg.content_production_needs:
        render_kpi_section_label("Content production needs")

        # Build the CPN table rows
        cpn_rows_html = ""
        for item in cfg.content_production_needs:
            vol = item["volume"]
            is_numeric = vol not in ("As events occur", "As culture dictates", "Daily")
            vol_cell = f"<strong>{vol}</strong>" if is_numeric else vol
            cpn_rows_html += (
                f"<tr>"
                f"<td>{item['type']}</td>"
                f"<td>{item['source']}</td>"
                f"<td>{item.get('sku', '')}</td>"
                f"<td>{vol_cell}</td>"
                f"</tr>"
            )

        # Build source mix bar
        source_mix_html = ""
        if cfg.source_mix_target:
            _seg_class = {"Brand": "brand", "Influencer": "influencer",
                          "Collective": "collective", "Partner": "partner"}
            for label, pct in cfg.source_mix_target.items():
                cls = _seg_class.get(label, "brand")
                source_mix_html += f'<div class="seg {cls}" style="width:{pct}%;">{label} {pct}%</div>'

        # Build cadence rows
        cadence_rows_html = ""
        for plat, vals in cfg.cadence_targets.items():
            cadence_rows_html += f'<tr><td>{plat}</td><td>{vals["low"]}–{vals["high"]} / mo</td></tr>'
        reel_target = cfg.kpi_targets.get("reel_ratio", 50)
        cadence_rows_html += f'<tr><td>Reel Ratio (IG)</td><td>{reel_target}%</td></tr>'
        cadence_rows_html += '<tr><td>Cross-pollinate</td><td>YT Shorts + Pinterest</td></tr>'

        # Build summary dark card (no indentation — Streamlit markdown treats 4+ leading spaces as code block)
        ps = cfg.production_summary or {}
        summary_html = ""
        if ps:
            _monthly_note = ps.get("monthly_note", "").replace("\n", " ")
            summary_html = (
                f'<div class="cpn-summary-dark">'
                f'<div class="cpn-label">Monthly Total</div>'
                f'<div class="cpn-big">~{ps["monthly_low"]}–{ps["monthly_high"]} assets</div>'
                f'<div class="cpn-sub">{_monthly_note}</div>'
                f'<hr>'
                f'<div class="cpn-annual-label">2026 ({ps["annual_months"]}-Month) Need</div>'
                f'<div class="cpn-annual-value">~{ps["annual_low"]}–{ps["annual_high"]} assets</div>'
                f'</div>'
            )

        # Build the full CPN block as a single-line HTML string (no indentation — Streamlit markdown
        # treats 4+ leading spaces as a code fence, which breaks nested divs)
        _cpn_html = (
            f'<div class="content-card">'
            f'<h3>Content Production Needs</h3>'
            f'<div class="card-caption">Monthly asset requirements by content type, source, and SKU focus.</div>'
            f'<div class="cpn-layout">'
            f'<div>'
            f'<table>'
            f'<colgroup><col style="width:34%;"><col style="width:22%;"><col style="width:20%;"><col style="width:24%;"></colgroup>'
            f'<thead><tr><th>Content Type</th><th>Source</th><th>SKU Focus</th><th>Volume / Mo</th></tr></thead>'
            f'<tbody>{cpn_rows_html}</tbody>'
            f'</table>'
            f'<div class="source-mix-label">Source mix target</div>'
            f'<div class="source-mix-bar">{source_mix_html}</div>'
            f'<div class="sku-split-note">SKU Split: Especial 60% | RTD 35% | Tradicional 5%</div>'
            f'</div>'
            f'<div>'
            f'{summary_html}'
            f'<div class="cpn-cadence">'
            f'<div class="cpn-cadence-label">Cadence Targets</div>'
            f'<table>{cadence_rows_html}</table>'
            f'</div>'
            f'</div>'
            f'</div>'
            f'</div>'
        )
        st.markdown(_cpn_html, unsafe_allow_html=True)

    # ── Section 2: Instagram Deep Dive ──────────────────────────────────
    render_kpi_section_label("Instagram deep dive")

    hero_ig = hero_df[hero_df["platform"] == "Instagram"]
    ig_total = len(hero_ig)

    if ig_total == 0:
        render_poplife_note("No Instagram data available yet.")
    else:
        # ── Avg Engagements by Format ───────────────────────────────────
        col_eng, col_cadence = st.columns(2)

        with col_eng:
            st.markdown("##### Avg Engagements by Format")
            _eng_by_type = hero_ig.groupby("post_type")["total_engagement"].mean().sort_values(ascending=False)
            fig_eng = go.Figure()
            fig_eng.add_trace(go.Bar(
                x=_eng_by_type.index, y=_eng_by_type.values,
                marker_color=[cfg.brand_colors.get(HERO, cfg.primary_color)] * len(_eng_by_type),
                text=[f"{v:.0f}" for v in _eng_by_type.values],
                textposition="outside",
            ))
            fig_eng.add_hline(y=ENG_PER_POST_TARGET, line_dash="dash", line_color="#D9534F",
                              annotation_text=f"Target: {ENG_PER_POST_TARGET}")
            fig_eng.update_layout(
                template=CHART_TEMPLATE, font=CHART_FONT,
                yaxis_title="Avg Engagements", xaxis_title="",
                height=350, margin=dict(l=0, r=0, t=30, b=30),
                showlegend=False,
            )
            st.plotly_chart(fig_eng, use_container_width=True)

        # ── Posting Cadence ─────────────────────────────────────────────
        with col_cadence:
            st.markdown("##### Monthly Posting Cadence")
            hero_ig_dated = hero_ig.copy()
            hero_ig_dated["post_date_parsed"] = pd.to_datetime(hero_ig_dated["post_date"], errors="coerce")
            hero_ig_dated["month"] = hero_ig_dated["post_date_parsed"].dt.to_period("M")
            _monthly = hero_ig_dated.groupby("month").size().reset_index(name="posts")
            _monthly["month_str"] = _monthly["month"].astype(str)

            ig_target = cfg.cadence_targets.get("Instagram", {})
            ig_low = ig_target.get("low", 12)
            ig_high = ig_target.get("high", 16)

            fig_cad = go.Figure()
            _bar_colors = []
            for _, row in _monthly.iterrows():
                if row["posts"] < ig_low:
                    _bar_colors.append("#D9534F")  # below target
                elif row["posts"] > ig_high:
                    _bar_colors.append("#F0AD4E")  # above target
                else:
                    _bar_colors.append("#5CB85C")  # on target

            fig_cad.add_trace(go.Bar(
                x=_monthly["month_str"], y=_monthly["posts"],
                marker_color=_bar_colors,
                text=_monthly["posts"], textposition="outside",
            ))
            # Target range band
            fig_cad.add_hrect(y0=ig_low, y1=ig_high, fillcolor="#5CB85C", opacity=0.1,
                              line_width=0)
            fig_cad.add_hline(y=ig_low, line_dash="dot", line_color="#5CB85C", opacity=0.5,
                              annotation_text=f"Target: {ig_low}-{ig_high}/mo",
                              annotation_position="top right")
            fig_cad.update_layout(
                template=CHART_TEMPLATE, font=CHART_FONT,
                yaxis_title="Posts", xaxis_title="",
                height=350, margin=dict(l=0, r=0, t=30, b=30),
                showlegend=False,
            )
            st.plotly_chart(fig_cad, use_container_width=True)

        # ── Best Posting Times ──────────────────────────────────────────
        st.markdown("##### Best Posting Times")
        _freq = results.get("frequency", {}).get(HERO, {}).get("Instagram", {})
        _best_days = _freq.get("best_days", [])
        _best_hours = _freq.get("best_hours", [])

        col_days, col_hours, col_themes = st.columns(3)
        with col_days:
            st.markdown("**Best Days**")
            if _best_days:
                for d in _best_days[:3]:
                    day_name = d[0] if isinstance(d, (list, tuple)) else d
                    st.markdown(f"- {day_name}")
            else:
                st.caption("Not enough data")

        with col_hours:
            st.markdown("**Best Hours**")
            if _best_hours:
                for h in _best_hours[:3]:
                    hr_val = h[0] if isinstance(h, (list, tuple)) else h
                    hr = int(hr_val) if isinstance(hr_val, (int, float)) else hr_val
                    if isinstance(hr, int):
                        ampm = "AM" if hr < 12 else "PM"
                        display_hr = hr if hr <= 12 else hr - 12
                        if display_hr == 0:
                            display_hr = 12
                        st.markdown(f"- {display_hr} {ampm}")
                    else:
                        st.markdown(f"- {h}")
            else:
                st.caption("Not enough data")

        # ── Top Pillars on IG ────────────────────────────────────────────
        with col_themes:
            st.markdown("**Top Pillars (by Avg Eng)**")
            if "content_pillar" in hero_ig.columns and hero_ig["content_pillar"].notna().any():
                _pillar_eng = hero_ig[hero_ig["content_pillar"].notna()].groupby("content_pillar")["total_engagement"].mean().sort_values(ascending=False)
                for pillar, eng in _pillar_eng.head(5).items():
                    st.markdown(f"- {pillar}: **{eng:.0f}**")
            else:
                st.caption("No pillar data")



# ══════════════════════════════════════════════════════════════════════
# TAB 4 — Action Plan
# ══════════════════════════════════════════════════════════════════════

with tab_action:

    # ── 30-Day Action Plan ─────────────────────────────────────────────
    render_kpi_section_label(f"30-day action plan for {HERO}")

    hero_ppw = sum(results["frequency"].get(HERO, {}).get(p, {}).get("posts_per_week", 0)
                     for p in ["Instagram", "TikTok"])
    leader_avg_ppw = sum(
        results["frequency"].get(b, {}).get(p, {}).get("posts_per_week", 0)
        for b in GEN_Z_LEADERS for p in ["Instagram", "TikTok"]
    ) / max(len(GEN_Z_LEADERS), 1)
    rec_ppw = round(leader_avg_ppw, 0)

    top_pillars_for_leaders = leader_df.groupby("content_pillar")["total_engagement"].mean().nlargest(3) if "content_pillar" in leader_df.columns and leader_df["content_pillar"].notna().any() else leader_df.groupby("content_theme")["total_engagement"].mean().nlargest(3)

    _hero_ig_action = hero_df[hero_df["platform"] == "Instagram"]
    video_pct = len(_hero_ig_action[_hero_ig_action["post_type"].isin(["Reel", "Video"])]) / max(len(_hero_ig_action), 1) * 100

    plan = [
        {
            "week": "Week 1",
            "focus": "Format Reset & Creator Pipeline",
            "actions": [
                f"Ramp posting to {int(rec_ppw)}+ posts/week (currently {hero_ppw:.0f}/wk)",
                f"Shift IG mix to 60%+ Reels (currently {video_pct:.0f}% video)",
                "Build creator shortlist: 5 micro-creators (10K-100K) in Lifestyle, Comedy, and Food niches",
                "Audit current grid aesthetic — does it signal 'fun' at a glance?",
            ],
        },
        {
            "week": "Week 2",
            "focus": "Content Pillar Launch",
            "actions": [
                f"Launch content pillars: " + ", ".join(f"'{p}'" for p in list(cfg.pillar_map.keys())[:2]) + " — 2 Reels + 1 Carousel" if cfg.pillar_map else "Launch primary content pillars: 2 Reels + 1 Carousel",
                "Test first meme-format Reel (POV/trending audio) — keep it native, not ad-like",
                f"Test top-performing pillars from leaders: {', '.join(top_pillars_for_leaders.index[:2])}" if len(top_pillars_for_leaders) >= 2 else "Identify and test high-performing content pillars from competitors",
            ],
        },
        {
            "week": "Week 3",
            "focus": "Community & UGC Flywheel",
            "actions": [
                "Launch first creator collab — raw/UGC-style Reel, not polished ad",
                "Repost 2-3 pieces of UGC from followers (build repost pipeline)",
                "Add engagement-driving CTAs: 'Tag your +1', 'Drop your go-to order', 'Share to your story'",
                "Stories: run 3-5/day with polls, quizzes, and BTS content",
            ],
        },
        {
            "week": "Week 4",
            "focus": "Measure, Learn & Scale",
            "actions": [
                "Analyze Week 1-3: identify top 3 posts by engagements, saves, and shares",
                "Double down on winning formats — scale what works, drop what doesn't",
                f"Set engagement target: close gap to {ENG_PER_POST_TARGET} avg eng/post within 60 days",
                "Brief next month's cultural calendar content (holidays, events, trending moments)",
            ],
        },
    ]

    for item in plan:
        with st.expander(f"**{item['week']}** — {item['focus']}"):
            for action in item["actions"]:
                st.markdown(f"- {action}")

    st.markdown("---")

    # ── 2026 Cultural Calendar ──────────────────────────────────────────
    render_kpi_section_label("2026 cultural calendar")
    st.caption("Quarterly cultural moments and content angles")

    _q_variants = {"Q1": "q1", "Q2": "q2", "Q3": "q3", "Q4": "q4"}
    cal_cols = st.columns(len(cfg.cultural_calendar))
    for col, (quarter, info) in zip(cal_cols, cfg.cultural_calendar.items()):
        with col:
            render_quarter_card(
                quarter=quarter,
                moments=info.get("moments", ""),
                angle=info.get("angle", ""),
                variant=_q_variants.get(quarter, "q1"),
            )

    # ── Year-Round Partner Events ────────────────────────────────────────
    render_kpi_section_label("Year-round partner events")
    st.caption("Official brand partnerships with a recurring presence throughout the year")

    partners = [
        {"name": "NASCAR", "icon": "🏁", "desc": "Official tequila of NASCAR — on-site activations, race-day content, driver partnerships"},
        {"name": "UFC", "icon": "🥊", "desc": "Official tequila of UFC — fight night activations, athlete content, octagon branding"},
        {"name": "Love Island", "icon": "🏝️", "desc": "Official tequila of Love Island — in-show integration, watch party content, cast partnerships"},
    ]
    pcols = st.columns(len(partners))
    for col, p in zip(pcols, partners):
        with col:
            render_partner_event(emoji=p["icon"], name=p["name"], description=p["desc"])

    st.markdown("---")

    # ── Monthly Ramp (March-June) ───────────────────────────────────────
    render_kpi_section_label("Monthly ramp targets · March – June 2026")
    st.caption("Progressive scaling toward full strategy execution")

    ramp_rows = []
    for month, targets in cfg.monthly_ramp.items():
        ramp_rows.append({
            "Month": month,
            "Creator % of Total": targets["creator_pct"],
            "Avg Eng Target": targets["er_target"],
            "Proactive Comments/Wk": targets["proactive_comments_wk"],
        })
    ramp_df = pd.DataFrame(ramp_rows)
    st.dataframe(ramp_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── Threats & Opportunities ────────────────────────────────────────
    render_kpi_section_label("Threats & opportunities")

    # Build threats list
    _threats = []
    _df_owned = df[~df["collaboration"].str.strip().str.lower().isin(COLLAB_AMPLIFIED_TYPES)] if "collaboration" in df.columns else df
    brand_counts = _df_owned.groupby("brand").size()
    if len(brand_counts):
        highest_poster = brand_counts.idxmax()
        highest_post_count = brand_counts.max()
        hero_count = len(hero_df)
        if highest_poster != HERO:
            _threats.append(f"{highest_poster} leads with {highest_post_count} posts vs {HERO}'s {hero_count} — losing share of voice")

    brand_eng_all = _df_owned.groupby("brand")["total_engagement"].mean()
    if len(brand_eng_all):
        best_eng_brand = brand_eng_all.idxmax()
        best_eng_val = brand_eng_all.max()
        if best_eng_brand != HERO:
            _threats.append(f"{best_eng_brand} dominates engagement at {best_eng_val:,.0f} avg eng/post")

    if results["creators"]:
        collab_items = [(b, v.get("collab_pct", 0)) for b, v in results["creators"].items() if b != HERO]
        if collab_items:
            highest_collab = max(collab_items, key=lambda x: x[1])
            hero_collab = results["creators"].get(HERO, {}).get("collab_pct", 0)
            if highest_collab[1] > hero_collab:
                _threats.append(
                    f"{highest_collab[0]}'s creator collab rate ({highest_collab[1]:.0f}%) "
                    f"dwarfs {HERO}'s ({hero_collab:.0f}%)"
                )

    # Build opportunities list
    _opps = []
    hero_theme_eng = hero_df.groupby("content_pillar")["total_engagement"].mean() if (len(hero_df) and "content_pillar" in hero_df.columns and hero_df["content_pillar"].notna().any()) else pd.Series(dtype=float)
    hero_best_theme = hero_theme_eng.idxmax() if len(hero_theme_eng) else "N/A"
    hero_best_eng = hero_theme_eng.max() if len(hero_theme_eng) else 0
    if hero_best_theme != "N/A":
        _opps.append(f"{HERO}'s {hero_best_theme} content is the top-performing pillar at {hero_best_eng:,.0f} avg eng")

    reel_pct_opp = len(hero_df[hero_df["post_type"] == "Reel"]) / max(len(hero_df[hero_df["platform"] == "Instagram"]), 1) * 100
    if reel_pct_opp < 60:
        _opps.append(f"Instagram Reels at only {reel_pct_opp:.0f}% of IG content — room to grow to 60%+")
    for _opp in cfg.narrative.get("strategy", {}).get("opportunities", []):
        _opps.append(_opp)

    # Render as SWOT 2-col
    col_t, col_o = st.columns(2)
    with col_t:
        render_swot_card("threat", "Competitive Threats", _threats or ["No threats identified"])
    with col_o:
        render_swot_card("opportunity", f"Opportunities for {HERO}", _opps or ["No opportunities identified"])

    st.markdown("---")

    # ── Qualitative Strategic Intel ────────────────────────────────────
    autostrat = st.session_state.get("autostrat", {})
    _has_autostrat = has_autostrat_data(autostrat)

    if _has_autostrat:
        render_kpi_section_label("Qualitative strategic intelligence")
        st.caption("From autostrat.ai reports — audience insights, content trends, partnership opportunities")

        # ── Audience Profile (NOPD) ──────────────────────────────────────
        _all_aud = get_all_audience_profiles(autostrat, exclude_reference=True)
        # Filter to hero brand identifiers only
        _hero_ids = cfg.hero_hashtag_ids
        all_audience = [p for p in _all_aud if p["identifier"] in _hero_ids] if _hero_ids else _all_aud
        if all_audience:
            render_kpi_section_label("Audience profile — who we're talking to")
            # Merge NOPD across hero reports, deduplicating
            merged_nopd = {"needs": [], "objections": [], "desires": [], "pain_points": []}
            _seen = {"needs": set(), "objections": set(), "desires": set(), "pain_points": set()}
            for profile in all_audience:
                for dim in merged_nopd:
                    for item in profile.get("audience_profile", {}).get(dim, []):
                        key = item[:40] if isinstance(item, str) else str(item)[:40]
                        if key not in _seen[dim]:
                            merged_nopd[dim].append(item)
                            _seen[dim].add(key)
            render_nopd_grid(merged_nopd)
            st.caption(f"*Synthesized from {len(all_audience)} {HERO} autostrat reports*")
            st.markdown("---")

        # Winning Territories
        all_htw = get_all_how_to_win(autostrat, exclude_reference=True)
        if all_htw:
            render_kpi_section_label("Winning territories")
            all_territories = []
            for entry in all_htw:
                for territory in entry["how_to_win"].get("territories", []):
                    is_dupe = any(territory[:40] == existing[:40] for existing in all_territories)
                    if not is_dupe:
                        all_territories.append(territory)
            render_territory_list(all_territories[:8])
            st.markdown("---")

        # Content Trends
        all_trends = get_all_content_trends(autostrat)
        if all_trends:
            render_kpi_section_label("Content trends")
            cols = st.columns(2)
            for i, trend in enumerate(all_trends[:6]):
                with cols[i % 2]:
                    render_narrative_card(trend.get("trend", f"Trend {i+1}"),
                                         trend.get("description", ""), accent_color="#F8C090")
            st.markdown("---")

        # Partnership Opportunities
        all_suggestions = get_all_sponsorship_suggestions(autostrat, exclude_reference=True)
        if all_suggestions:
            render_kpi_section_label("Partnership opportunities")
            for entry in all_suggestions:
                source = f"{entry['source_label']} — {entry['identifier'].replace('_', ' ').title()}"
                st.markdown(f"**From: {source}**")
                sug_cols = st.columns(min(len(entry["suggestions"]), 2))
                for i, sug in enumerate(entry["suggestions"]):
                    with sug_cols[i % len(sug_cols)]:
                        render_sponsorship_card(sug)
                st.markdown("")
