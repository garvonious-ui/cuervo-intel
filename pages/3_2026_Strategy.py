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
    render_section_label, render_territory_cards, render_nopd_cards,
    render_narrative_card, render_creator_archetype,
    render_sponsorship_card, render_verbatim_quotes,
)

if "results" not in st.session_state:
    st.warning("Go to the home page first to load data.")
    st.stop()

cfg = get_client()

st.logo(cfg.app_logo_path)
st.markdown(cfg.custom_css, unsafe_allow_html=True)
st.header(cfg.page_headers["strategy"])
st.caption(cfg.page_captions["strategy"])

results = st.session_state["results"]
df = st.session_state["df"]  # Unfiltered

HERO = cfg.hero_brand
GEN_Z_LEADERS = cfg.gen_z_leaders
_t = cfg.kpi_targets
ENG_PER_POST_TARGET = _t["engagements_per_post"]

hero_df_full = df[df["brand"] == HERO]  # Includes Edutain dupes — only for content mix funnel
hero_df = hero_df_full[hero_df_full["_mix_weight"] >= 1.0] if "_mix_weight" in hero_df_full.columns else hero_df_full
# Keep unfiltered copy for collaboration breakdown sections (which intentionally show Influencer data)
hero_df_with_influencer = hero_df.copy()
# Exclude collab posts (Influencer + Collective) from engagement metrics (they inflate due to higher reach)
if "collaboration" in hero_df.columns:
    hero_df = hero_df[~hero_df["collaboration"].str.strip().str.lower().isin(COLLAB_AMPLIFIED_TYPES)]
leader_df = df[df["brand"].isin(GEN_Z_LEADERS)]
if "collaboration" in leader_df.columns:
    leader_df = leader_df[~leader_df["collaboration"].str.strip().str.lower().isin(COLLAB_AMPLIFIED_TYPES)]

def _render_north_star():
    """Display the brand North Star banner if configured."""
    ns = cfg.north_star
    if not ns:
        return
    st.markdown(f"""
    <div style="background-color:#3D6B7E; border-radius:10px; padding:28px 32px; margin-bottom:24px;">
        <div style="font-size:0.85rem; font-weight:700; letter-spacing:2px; color:#E8E0D4; text-transform:uppercase; margin-bottom:6px;">
            Our North Star
        </div>
        <div style="font-size:1.6rem; font-weight:800; color:#D4A843; text-transform:uppercase; margin-bottom:10px;">
            {ns.get("title", "")}
        </div>
        <div style="font-size:1.05rem; color:#E8E0D4; font-weight:600; margin-bottom:4px;">
            {ns.get("tagline", "")}
        </div>
        <div style="font-size:0.95rem; color:#C8C0B4; line-height:1.5;">
            {ns.get("description", "")}
        </div>
    </div>
    """, unsafe_allow_html=True)

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
    st.subheader("Social Brief KPI Scorecard")
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

    # Creator content %
    creator_posts = hero_df[hero_df["has_creator_collab"].astype(str).str.lower() == "yes"] if "has_creator_collab" in hero_df.columns else pd.DataFrame()
    creator_pct = len(creator_posts) / max(len(hero_df), 1) * 100
    creator_avg_eng = creator_posts["total_engagement"].mean() if len(creator_posts) else 0
    creator_avg_eng = 0 if pd.isna(creator_avg_eng) else creator_avg_eng

    freq = results["frequency"].get(HERO, {})
    ig_ppm = freq.get("Instagram", {}).get("posts_per_week", 0) * 4.33  # Convert to monthly
    tt_ppw = freq.get("TikTok", {}).get("posts_per_week", 0)

    # Scorecard table (targets from kpi_targets in client config)
    _ig_ppm = _t["ig_posts_per_month"]
    _tt_ppw = _t["tt_posts_per_week"]
    scorecard_data = [
        {"KPI": "Avg Eng/Post", "Actual": f"{avg_eng_per_post:,.0f}",
         "Target": f"{_t['engagements_per_post']:,}+",
         "Status": "ON TRACK" if avg_eng_per_post >= _t["engagements_per_post"] else "BELOW",
         "Gap": f"{avg_eng_per_post - _t['engagements_per_post']:+,.0f}"},
        {"KPI": "Creator Avg Eng", "Actual": f"{creator_avg_eng:,.0f}",
         "Target": f"{_t['creator_engagements_per_post']:,}+",
         "Status": "ON TRACK" if creator_avg_eng >= _t["creator_engagements_per_post"] else "BELOW",
         "Gap": f"{creator_avg_eng - _t['creator_engagements_per_post']:+,.0f}"},
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
        {"KPI": "TT Posts/Week", "Actual": f"{tt_ppw:.1f}",
         "Target": f"{_tt_ppw[0]}-{_tt_ppw[1]}/wk",
         "Status": "ON TRACK" if _tt_ppw[0] <= tt_ppw <= _tt_ppw[1] else ("BELOW" if tt_ppw < _tt_ppw[0] else "ABOVE"),
         "Gap": f"{tt_ppw - sum(_tt_ppw)/2:+.1f} vs mid"},
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
        use_container_width=True, hide_index=True, height=340,
    )

    on_track = sum(1 for s in scorecard_data if s["Status"] == "ON TRACK")
    total = len(scorecard_data)
    st.info(f"**{on_track}/{total} KPIs on track.** "
            f"{'Strong position — maintain momentum.' if on_track >= 4 else 'Focus areas identified below.' if on_track >= 2 else 'Significant gaps — prioritize the Action Plan tab.'}")

    st.markdown("---")

    if cfg.themes_ready:
        st.markdown("---")

        # ── Collaboration Mix ──────────────────────────────────────────────
        if "collaboration" in hero_df_with_influencer.columns and hero_df_with_influencer["collaboration"].notna().any():
            st.subheader("Collaboration Mix")
            st.caption(f"Who is creating {HERO}'s content — based on manual post tagging")

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

            col_src1, col_src2 = st.columns(2)
            with col_src1:
                st.markdown(f"**{HERO} Collaboration Breakdown**")
                fig_src = px.bar(src_data, x="Source", y="% of Content",
                                 color="Source", color_discrete_map=collab_colors,
                                 text="% of Content", template=CHART_TEMPLATE,
                                 labels={"% of Content": "% of Content", "Source": ""})
                fig_src.update_traces(texttemplate="%{text:.0f}%", textposition="outside")
                fig_src.update_layout(font=CHART_FONT, height=380, showlegend=False,
                                      yaxis_title="% of Content")
                st.plotly_chart(fig_src, use_container_width=True)

            with col_src2:
                st.markdown("**Collaboration Scorecard**")
                for _, row in src_data.iterrows():
                    st.markdown(f"**{row['Source']}**: {row['Posts']} posts ({row['% of Content']:.0f}%) — "
                                f"Avg Eng: {row['Avg Eng']:,.0f}")
                best_collab = src_data.iloc[0]
                st.info(f"**Top collaboration type: {best_collab['Source']}** at {best_collab['% of Content']:.0f}% of content "
                        f"with {best_collab['Avg Eng']:,.0f} avg engagements.")

        st.markdown("---")

        # ── Best Performing Pillar ──────────────────────────────────────────
        _has_pillar_col = "content_pillar" in hero_df.columns and hero_df["content_pillar"].notna().any()
        if _has_pillar_col:
            st.subheader("Best Performing Content Pillar")
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

            st.info(f"**Best pillar: {best_pillar['content_pillar']}** at {best_pillar['avg_eng']:,.0f} avg engagements — lean into this for upcoming content. "
                    f"Pillars above the {ENG_PER_POST_TARGET} eng target are proven winners worth scaling.")
        else:
            st.info(f"No content pillar data available for {HERO}.")
    else:
        st.markdown("---")
        st.info(f"**Content source mix & theme analysis hidden** — post-level theme tagging is not yet complete for {HERO}. "
                f"These sections will appear once all posts have been manually reviewed and tagged.")


# ══════════════════════════════════════════════════════════════════════
# TAB 2 — Content Strategy Frameworks
# ══════════════════════════════════════════════════════════════════════

with tab_frameworks:
    _render_north_star()

    # ── Content Pillars (4 pillars from 2026 deck) ──────────────────────
    st.subheader("Content Pillars")
    st.caption("4 pillars from the 2026 Social Strategy — SKU-aligned content territories")

    pillar_data = []
    for pillar_name, themes in cfg.pillar_map.items():
        # Use direct content_pillar column if available, fall back to theme-based lookup
        if "content_pillar" in hero_df.columns:
            matching = hero_df[hero_df["content_pillar"].astype(str).str.strip() == pillar_name]
        else:
            matching = hero_df[hero_df["content_theme"].isin(themes)]
        pct = len(matching) / max(len(hero_df), 1) * 100
        avg_eng = matching["total_engagement"].mean() if len(matching) else 0
        avg_eng = 0 if pd.isna(avg_eng) else avg_eng
        pillar_data.append({
            "Pillar": pillar_name,
            "Actual %": round(pct, 1),
            "Target %": cfg.pillar_targets[pillar_name],
            "Avg Eng": round(avg_eng, 0),
            "Posts": len(matching),
            "desc": cfg.pillar_descriptions.get(pillar_name, ""),
        })

    pillar_df = pd.DataFrame(pillar_data)

    # Pillar detail cards
    for _, row in pillar_df.iterrows():
        gap = row["Actual %"] - row["Target %"]
        color = cfg.pillar_colors[row["Pillar"]]
        desc = row["desc"]
        st.markdown(f"""
        <div style="background:white; border-radius:10px; padding:18px 22px; margin-bottom:14px;
                    border-left:5px solid {color}; border:1px solid #E0D8D0;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <h4 style="margin:0; color:#333;">{row['Pillar']}</h4>
                <span style="background:{color}; color:white; padding:4px 12px; border-radius:20px;
                             font-weight:600; font-size:0.85rem;">{row['Actual %']:.0f}% actual / {row['Target %']}% target</span>
            </div>
            <p style="color:#666; margin:4px 0 8px 0; font-size:0.9rem;">{desc}</p>
            <div style="display:flex; gap:24px; font-size:0.88rem;">
                <span><strong>{row['Posts']}</strong> posts</span>
                <span><strong>{row['Avg Eng']:,.0f}</strong> avg eng</span>
                <span style="color:{'#2E7D32' if abs(gap) < 10 else '#C62828'};">{gap:+.0f}pp gap</span>
            </div>
        </div>""", unsafe_allow_html=True)

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
    st.subheader("SKU Strategy")
    st.caption("Each SKU has a distinct energy and occasion — content should match")

    sku_cols = st.columns(len(cfg.sku_strategy))
    sku_colors = {"Especial": "#F8C090", "Tradicional": "#C9A87E", "RTD": "#2ea3f2"}
    for col, (sku, info) in zip(sku_cols, cfg.sku_strategy.items()):
        with col:
            c = sku_colors.get(sku, "#999")
            st.markdown(f"""
            <div style="background:white; border-radius:10px; padding:16px; text-align:center;
                        border-top:4px solid {c}; border:1px solid #E0D8D0;">
                <h4 style="margin:0 0 6px 0; color:{c};">{sku}</h4>
                <p style="font-weight:600; margin:4px 0; color:#333;">{info['energy']}</p>
                <p style="color:#666; font-size:0.85rem; margin:0;">{info['occasions']}</p>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── 4 Execution Engines ─────────────────────────────────────────────
    st.subheader("The 4 Execution Engines")
    st.caption("How content gets made across both pillars")

    engine_colors = ["#2ea3f2", "#F8C090", "#C9A87E", "#66BB6A"]
    eng_cols = st.columns(2)
    for i, (engine, desc) in enumerate(cfg.execution_engines.items()):
        with eng_cols[i % 2]:
            c = engine_colors[i]
            st.markdown(f"""
            <div style="background:white; border-radius:10px; padding:16px 18px; margin-bottom:12px;
                        border-top:4px solid {c}; border:1px solid #E0D8D0; min-height:120px;">
                <h4 style="margin:0 0 8px 0; color:{c}; font-size:0.95rem;">{engine.upper()}</h4>
                <p style="color:#555; font-size:0.88rem; line-height:1.5; margin:0;">{desc}</p>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── The Creator Crew (Creator Archetypes) ────────────────────────
    _crew_header = cfg.narrative.get("strategy", {}).get("crew_header", f"The {HERO} Crew — Creator Archetypes")
    st.subheader(_crew_header)
    st.caption("Creators embedded in the brand — not hired talent. iPhone-first. Social-native.")

    # Prefer autostrat-derived archetypes (richer: description, appeal, examples)
    _autostrat_tmp = st.session_state.get("autostrat", {})
    _autostrat_archetypes = get_all_creator_archetypes(_autostrat_tmp) if has_autostrat_data(_autostrat_tmp) else []

    if _autostrat_archetypes:
        _arch_cols = st.columns(min(len(_autostrat_archetypes[:6]), 3))
        for i, arch in enumerate(_autostrat_archetypes[:6]):
            with _arch_cols[i % len(_arch_cols)]:
                render_creator_archetype(arch)
        st.caption(f"*From autostrat.ai analysis — {len(_autostrat_archetypes)} archetypes identified*")
    else:
        # Fallback to brief-defined archetypes
        arch_cols = st.columns(min(len(cfg.creator_archetypes), 5))
        for i, (archetype, fit) in enumerate(cfg.creator_archetypes.items()):
            with arch_cols[i % len(arch_cols)]:
                st.markdown(f"""
                <div style="background:white; border-radius:10px; padding:14px; text-align:center;
                            border:1px solid #E0D8D0; min-height:100px;">
                    <p style="font-weight:700; color:#333; margin:0 0 6px 0; font-size:0.9rem;">{archetype}</p>
                    <p style="color:#666; font-size:0.82rem; margin:0;">{fit}</p>
                </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── Content Mix Funnel ─────────────────────────────────────────────
    _mix_cats = list(cfg.content_mix_targets.keys())
    st.subheader(f"Content Mix Funnel — {' / '.join(_mix_cats)} / Connect")
    st.caption(f"Grab attention first ({_mix_cats[0]} {cfg.content_mix_targets[_mix_cats[0]]}%), then guide to action ({_mix_cats[-1]} {cfg.content_mix_targets[_mix_cats[-1]]}%)")

    hero_mix_data = []
    # Use hero_df_full (includes Edutain dupes with _mix_weight=0.5)
    _mix_src = hero_df_full if "hero_df_full" in dir() else hero_df
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

    col_mix1, col_mix2 = st.columns(2)
    with col_mix1:
        st.markdown(f"**{HERO} Content Mix: Actual vs Poplife Target**")
        fig_mix = go.Figure()
        fig_mix.add_trace(go.Bar(x=mix_df["Category"], y=mix_df["Actual %"],
                                 name="Actual", marker_color=[cfg.content_mix_colors.get(c, "#999999") for c in mix_df["Category"]],
                                 text=mix_df["Actual %"], textposition="outside", texttemplate="%{text:.0f}%"))
        fig_mix.add_trace(go.Scatter(x=mix_df["Category"], y=mix_df["Target %"],
                                     name="Poplife Target", mode="markers+lines",
                                     marker=dict(size=12, color="#333333", symbol="diamond"),
                                     line=dict(color="#333333", width=2, dash="dash")))
        fig_mix.update_layout(template=CHART_TEMPLATE, font=CHART_FONT, height=380,
                              yaxis_title="% of Content", legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(fig_mix, use_container_width=True)

    with col_mix2:
        st.markdown("**Content Mix Scorecard**")
        for _, row in mix_df.iterrows():
            direction = "MORE" if row["Gap"] < -5 else ("LESS" if row["Gap"] > 5 else "ON TRACK")
            if direction == "ON TRACK":
                st.success(f"**{row['Category']}**: {row['Actual %']:.0f}% actual / {row['Target %']}% target ({row['Gap']:+.0f}%)")
            elif direction == "MORE":
                st.error(f"**{row['Category']}**: {row['Actual %']:.0f}% actual / {row['Target %']}% target ({row['Gap']:+.0f}%) — Need MORE")
            else:
                st.warning(f"**{row['Category']}**: {row['Actual %']:.0f}% actual / {row['Target %']}% target ({row['Gap']:+.0f}%) — Need LESS")
        st.markdown("")
        st.info("**Funnel logic**: Entertain grabs attention → Educate builds relevance → Connect fosters relationships → Convince drives action")

    st.markdown("""
    <div style="border-left: 4px solid #2ea3f2; background: linear-gradient(135deg, #f0f7fc 0%, #e8f4f8 100%); border-radius: 0 8px 8px 0; padding: 20px 24px; margin: 16px 0 24px 0;">
        <div style="display: flex; align-items: center; margin-bottom: 8px;">
            <span style="font-size: 1.1rem; font-weight: 700; color: #2ea3f2; letter-spacing: 1px; text-transform: uppercase;">Connect — Always On</span>
        </div>
        <div style="font-size: 0.95rem; color: #444; line-height: 1.6;">
            Connection isn't a content category — it's how we show up every day. Replying to comments, engaging in DMs, reposting fan content, and jumping into conversations in the feed. This layer runs underneath everything and turns passive followers into active community.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Voice Principles ────────────────────────────────────────────────
    st.subheader("Tone of Voice — The Life of the Party")
    st.caption(f"{HERO}'s social voice: lively, approachable, human-forward, extroverted")

    for principle, detail in cfg.voice_principles:
        st.markdown(f"""
        <div style="background:white; border-radius:8px; padding:12px 18px; margin-bottom:8px;
                    border-left:4px solid #F8C090; border:1px solid #E0D8D0;">
            <strong style="color:#333;">{principle}</strong>
            <span style="color:#888; margin-left:12px;">{detail}</span>
        </div>""", unsafe_allow_html=True)



# ══════════════════════════════════════════════════════════════════════
# TAB 3 — Platform Strategies
# ══════════════════════════════════════════════════════════════════════

with tab_platform:

    # ── Section 1: Platform Roles at a Glance ──────────────────────────
    st.subheader("Platform Roles at a Glance")

    _header_bg = "#4A6B7A"
    _row_bg = "#F9F7F4"
    _primary_color = "#333333"
    _secondary_color = "#888888"

    _rows_html = ""
    for i, (plat, info) in enumerate(cfg.platform_roles.items()):
        is_primary = info["priority"] == "Primary"
        name_style = f"font-weight:700; color:{_primary_color}" if is_primary else f"color:{_secondary_color}"
        row_bg = "#ffffff" if i % 2 == 0 else _row_bg
        _rows_html += (
            f'<tr style="background:{row_bg}; border-bottom:1px solid #e0ddd8;">'
            f'<td style="padding:10px 16px; {name_style}">{plat}</td>'
            f'<td style="padding:10px 16px;">{info["role"]}</td>'
            f'<td style="padding:10px 16px;">{info["priority"]}</td>'
            f'<td style="padding:10px 16px;">{info["cadence"]}</td>'
            f'</tr>'
        )
    _table_html = (
        f'<table style="width:100%; border-collapse:collapse; font-family:Barlow Condensed, Helvetica, Arial, sans-serif; font-size:0.95rem;">'
        f'<thead><tr style="background:{_header_bg}; color:white;">'
        f'<th style="padding:12px 16px; text-align:left; font-weight:700; text-transform:uppercase; letter-spacing:1px;">Platform</th>'
        f'<th style="padding:12px 16px; text-align:left; font-weight:700; text-transform:uppercase; letter-spacing:1px;">Role</th>'
        f'<th style="padding:12px 16px; text-align:left; font-weight:700; text-transform:uppercase; letter-spacing:1px;">Priority</th>'
        f'<th style="padding:12px 16px; text-align:left; font-weight:700; text-transform:uppercase; letter-spacing:1px;">Cadence</th>'
        f'</tr></thead><tbody>{_rows_html}</tbody></table>'
    )
    st.markdown(_table_html, unsafe_allow_html=True)

    # ── Instagram Format Mix ─────────────────────────────────────────
    st.markdown("")
    st.markdown("**Instagram Format Mix**")
    fmt_cols = st.columns(len(cfg.ig_format_mix))
    fmt_colors = ["#2ea3f2", "#F8C090", "#C9A87E", "#66BB6A"]
    for i, (fmt, info) in enumerate(cfg.ig_format_mix.items()):
        with fmt_cols[i]:
            c = fmt_colors[i]
            st.markdown(f"""
            <div style="text-align:center; background:white; border-radius:8px; padding:12px;
                        border-top:3px solid {c}; border:1px solid #E0D8D0;">
                <p style="font-size:1.4rem; font-weight:700; color:{c}; margin:0;">{info['pct']}%</p>
                <p style="font-weight:600; margin:2px 0; color:#333;">{fmt}</p>
                <p style="color:#888; font-size:0.8rem; margin:0;">{info['role']}</p>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── Section 2: Instagram Deep Dive ──────────────────────────────────
    st.subheader("Instagram Deep Dive")

    hero_ig = hero_df[hero_df["platform"] == "Instagram"]
    ig_total = len(hero_ig)

    if ig_total == 0:
        st.info("No Instagram data available yet.")
    else:
        # ── Format Mix: Actual vs Target ────────────────────────────────
        st.markdown("##### Format Mix: Actual vs Target")

        # Compute actual format distribution
        _type_counts = hero_ig["post_type"].value_counts()
        _format_map = {
            "Reels": _type_counts.get("Reel", 0) + _type_counts.get("Video", 0),
            "Carousels": _type_counts.get("Carousel", 0),
            "Stories": _type_counts.get("Story", 0),
            "Collabs/Lives": _type_counts.get("Live", 0),
        }
        # Static images count toward Carousels bucket for format mix context,
        # but let's show them separately and note it
        _static_count = _type_counts.get("Static Image", 0)
        if _static_count > 0:
            _format_map["Static Image"] = _static_count

        _actual_pcts = {k: (v / ig_total * 100) for k, v in _format_map.items() if v > 0}

        _fmt_data = []
        for fmt, target_info in cfg.ig_format_mix.items():
            _fmt_data.append({"Format": fmt, "Type": "Target", "Pct": target_info["pct"],
                              "Role": target_info["role"]})
            _fmt_data.append({"Format": fmt, "Type": "Actual", "Pct": _actual_pcts.get(fmt, 0),
                              "Role": target_info["role"]})
        # Add Static Image if present (no target for it)
        if "Static Image" in _actual_pcts:
            _fmt_data.append({"Format": "Static Image", "Type": "Actual",
                              "Pct": _actual_pcts["Static Image"], "Role": "—"})
            _fmt_data.append({"Format": "Static Image", "Type": "Target",
                              "Pct": 0, "Role": "—"})

        _fmt_df = pd.DataFrame(_fmt_data)
        fig_fmt = px.bar(
            _fmt_df, x="Pct", y="Format", color="Type", barmode="group",
            orientation="h",
            color_discrete_map={"Target": "#4A6B7A", "Actual": "#F8C090"},
            text="Pct",
        )
        fig_fmt.update_traces(texttemplate="%{text:.0f}%", textposition="outside")
        fig_fmt.update_layout(
            template=CHART_TEMPLATE, font=CHART_FONT,
            xaxis_title="% of Posts", yaxis_title="",
            legend_title="", height=300,
            yaxis=dict(categoryorder="array",
                       categoryarray=list(reversed(list(cfg.ig_format_mix.keys()) + (["Static Image"] if "Static Image" in _actual_pcts else [])))),
            margin=dict(l=0, r=40, t=10, b=30),
        )
        st.plotly_chart(fig_fmt, use_container_width=True)

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
                    st.markdown(f"- {d}")
            else:
                st.caption("Not enough data")

        with col_hours:
            st.markdown("**Best Hours**")
            if _best_hours:
                for h in _best_hours[:3]:
                    hr = int(h) if isinstance(h, (int, float)) else h
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

        # ── Top Themes on IG ────────────────────────────────────────────
        with col_themes:
            st.markdown("**Top Themes (by Avg Eng)**")
            if "content_theme" in hero_ig.columns:
                _theme_eng = hero_ig.groupby("content_theme")["total_engagement"].mean().sort_values(ascending=False)
                for theme, eng in _theme_eng.head(5).items():
                    st.markdown(f"- {theme}: **{eng:.0f}**")
            else:
                st.caption("No theme data")

    st.markdown("---")

    # ── Section 3: Other Platforms ──────────────────────────────────────
    st.subheader("Other Platforms")

    _other_platforms = {k: v for k, v in cfg.platform_roles.items() if k != "Instagram"}
    _cols = st.columns(min(len(_other_platforms), 3))

    for i, (plat, info) in enumerate(_other_platforms.items()):
        with _cols[i % 3]:
            is_primary = info["priority"] == "Primary"
            _border_color = "#F8C090" if is_primary else "#ccc"
            _priority_badge = f'<span style="background:#F8C090;color:#333;padding:2px 8px;border-radius:4px;font-size:0.8rem;font-weight:600;">PRIMARY</span>' if is_primary else f'<span style="background:#e8e5e0;color:#666;padding:2px 8px;border-radius:4px;font-size:0.8rem;">SECONDARY</span>'

            # Check if we have data for this platform
            _plat_key = plat.split(" /")[0].split(" ")[0]  # "TikTok", "Facebook", etc.
            _plat_posts = len(hero_df[hero_df["platform"] == _plat_key]) if _plat_key in hero_df["platform"].values else 0

            if _plat_posts > 0:
                _status_html = f'<div style="color:#5CB85C;font-size:0.85rem;margin-top:8px;">{_plat_posts} posts tracked</div>'
            elif is_primary:
                _status_html = '<div style="color:#F0AD4E;font-size:0.85rem;margin-top:8px;">Data incoming</div>'
            else:
                _status_html = '<div style="color:#999;font-size:0.85rem;margin-top:8px;">Not yet tracked</div>'

            st.markdown(f"""
            <div style="border:1px solid #e0ddd8; border-top:4px solid {_border_color};
                        border-radius:8px; padding:16px; margin-bottom:12px; min-height:180px;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                    <strong style="font-size:1.1rem;">{plat}</strong>
                    {_priority_badge}
                </div>
                <div style="color:#555;font-size:0.9rem;margin-bottom:8px;">{info['role']}</div>
                <div style="color:#333;font-size:0.9rem;"><strong>Cadence:</strong> {info['cadence']}</div>
                {_status_html}
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# TAB 4 — Action Plan
# ══════════════════════════════════════════════════════════════════════

with tab_action:

    # ── 30-Day Action Plan ─────────────────────────────────────────────
    st.subheader(f"30-Day Action Plan for {HERO}")

    hero_ppw = sum(results["frequency"].get(HERO, {}).get(p, {}).get("posts_per_week", 0)
                     for p in ["Instagram", "TikTok"])
    leader_avg_ppw = sum(
        results["frequency"].get(b, {}).get(p, {}).get("posts_per_week", 0)
        for b in GEN_Z_LEADERS for p in ["Instagram", "TikTok"]
    ) / max(len(GEN_Z_LEADERS), 1)
    rec_ppw = round(leader_avg_ppw, 0)

    top_themes_for_leaders = leader_df.groupby("content_theme")["total_engagement"].mean().nlargest(3)

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
                f"Test top-performing themes from leaders: {', '.join(top_themes_for_leaders.index[:2])}" if len(top_themes_for_leaders) >= 2 else "Identify and test high-performing themes from competitors",
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
    st.subheader("2026 Cultural Calendar")
    st.caption("Quarterly cultural moments and content angles")

    cal_colors = {"Q1": "#2ea3f2", "Q2": "#F8C090", "Q3": "#66BB6A", "Q4": "#C9A87E"}
    cal_cols = st.columns(len(cfg.cultural_calendar))
    for col, (quarter, info) in zip(cal_cols, cfg.cultural_calendar.items()):
        with col:
            c = cal_colors.get(quarter, "#999")
            st.markdown(f"""
            <div style="background:white; border-radius:10px; padding:14px; min-height:140px;
                        border-top:4px solid {c}; border:1px solid #E0D8D0;">
                <h4 style="margin:0 0 6px 0; color:{c};">{quarter}</h4>
                <p style="font-weight:600; color:#333; font-size:0.85rem; margin:0 0 6px 0;">{info['moments']}</p>
                <p style="color:#666; font-size:0.82rem; margin:0;">{info['angle']}</p>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── Monthly Ramp (March-June) ───────────────────────────────────────
    st.subheader("Monthly Ramp Targets (March — June 2026)")
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

    # ── Testing Roadmap ─────────────────────────────────────────────────
    st.subheader("Testing Roadmap")
    st.caption("Monthly A/B tests to optimize content strategy")

    test_rows = []
    for month, info in cfg.testing_roadmap.items():
        test_rows.append({"Month": month, "Test Variable": info["variable"], "What We're Learning": info["learning"]})
    test_df = pd.DataFrame(test_rows)
    st.dataframe(test_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── Threats & Opportunities ────────────────────────────────────────
    st.subheader("Threats & Opportunities")

    col_t, col_o = st.columns(2)

    with col_t:
        st.error("**Competitive Threats**")
        _df_owned = df[~df["collaboration"].str.strip().str.lower().isin(COLLAB_AMPLIFIED_TYPES)] if "collaboration" in df.columns else df
        brand_counts = _df_owned.groupby("brand").size()
        if len(brand_counts):
            highest_poster = brand_counts.idxmax()
            highest_post_count = brand_counts.max()
            hero_count = len(hero_df)
            if highest_poster != HERO:
                st.markdown(f"- {highest_poster} leads with **{highest_post_count}** posts vs {HERO}'s **{hero_count}** — losing share of voice")

        brand_eng_all = _df_owned.groupby("brand")["total_engagement"].mean()
        if len(brand_eng_all):
            best_eng_brand = brand_eng_all.idxmax()
            best_eng_val = brand_eng_all.max()
            if best_eng_brand != HERO:
                st.markdown(f"- {best_eng_brand} dominates engagement at **{best_eng_val:,.0f} avg eng/post**")

        if results["creators"]:
            collab_items = [(b, v.get("collab_pct", 0)) for b, v in results["creators"].items() if b != HERO]
            if collab_items:
                highest_collab = max(collab_items, key=lambda x: x[1])
                hero_collab = results["creators"].get(HERO, {}).get("collab_pct", 0)
                if highest_collab[1] > hero_collab:
                    st.markdown(f"- {highest_collab[0]}'s creator collab rate ({highest_collab[1]:.0f}%) "
                                f"dwarfs {HERO}'s ({hero_collab:.0f}%)")

    with col_o:
        st.success(f"**Opportunities for {HERO}**")
        hero_theme_eng = hero_df.groupby("content_theme")["total_engagement"].mean() if len(hero_df) else pd.Series(dtype=float)
        hero_best_theme = hero_theme_eng.idxmax() if len(hero_theme_eng) else "N/A"
        hero_best_eng = hero_theme_eng.max() if len(hero_theme_eng) else 0
        if hero_best_theme != "N/A":
            st.markdown(f"- {HERO}'s **{hero_best_theme}** content is the top-performing theme at {hero_best_eng:,.0f} avg eng")

        reel_pct_opp = len(hero_df[hero_df["post_type"] == "Reel"]) / max(len(hero_df[hero_df["platform"] == "Instagram"]), 1) * 100
        if reel_pct_opp < 60:
            st.markdown(f"- Instagram Reels at only **{reel_pct_opp:.0f}%** of IG content — room to grow to 60%+")
        for _opp in cfg.narrative.get("strategy", {}).get("opportunities", []):
            st.markdown(f"- {_opp}")

    st.markdown("---")

    # ── Strategic Actions (consolidated) ──────────────────────────────
    st.subheader("Strategic Actions")
    st.caption("Side-by-side: what the numbers say vs what the conversations say")

    autostrat = st.session_state.get("autostrat", {})

    # Helper: aggregate autostrat entries into flat action lists
    def _aggregate_actions(entries):
        actions = []
        seen = set()
        for entry in entries:
            src = entry["source_identifier"].replace("_", " ").title()
            for a in entry.get("strategic_actions", []):
                key = a[:50]
                if key not in seen:
                    actions.append({"source": src, "text": a})
                    seen.add(key)
            for o in entry.get("opportunities", []):
                key = o[:50]
                if key not in seen:
                    actions.append({"source": src, "text": o})
                    seen.add(key)
        return actions

    col_data_recs, col_convo_recs = st.columns(2)

    with col_data_recs:
        st.markdown("**From Performance Data**")
        recs = results["recommendations"]
        if recs:
            for priority in ["High", "Medium", "Low"]:
                pri_recs = [r for r in recs if r["priority"] == priority]
                if pri_recs:
                    color = PRIORITY_COLORS[priority]
                    st.markdown(f"**{priority} Priority** ({len(pri_recs)})")
                    for r in pri_recs:
                        st.markdown(f"- [{r['platform']}] {r['recommendation']}")
        else:
            st.info("No data-driven recommendations generated.")

    with col_convo_recs:
        st.markdown("**From Conversation Intelligence**")
        if has_autostrat_data(autostrat):
            all_strat = get_all_strategic_actions(autostrat)
            hero_strat = [a for a in all_strat if a["source_identifier"] in cfg.hero_hashtag_ids]
            comp_strat = [a for a in all_strat if a["source_identifier"] not in cfg.hero_hashtag_ids]

            hero_actions = _aggregate_actions(hero_strat)
            comp_actions = _aggregate_actions(comp_strat)

            if hero_actions:
                st.markdown(f"**{HERO} Insights** ({len(hero_actions)})")
                for item in hero_actions[:8]:
                    st.markdown(f"- {item['text']}")
            if comp_actions:
                with st.expander(f"Competitive Insights ({len(comp_actions)})"):
                    for item in comp_actions[:8]:
                        st.markdown(f"- **{item['source']}** — {item['text']}")
        else:
            st.info("Import autostrat reports to see conversation-driven insights.")

    st.markdown("---")

    # ── Qualitative Strategic Intel ────────────────────────────────────
    _has_autostrat = has_autostrat_data(autostrat)

    if _has_autostrat:
        st.subheader("Qualitative Strategic Intelligence")
        st.caption("From autostrat.ai reports — audience insights, content trends, partnership opportunities")

        # ── Audience Profile (NOPD) ──────────────────────────────────────
        _all_aud = get_all_audience_profiles(autostrat, exclude_reference=True)
        # Filter to hero brand identifiers only
        _hero_ids = cfg.hero_hashtag_ids
        all_audience = [p for p in _all_aud if p["identifier"] in _hero_ids] if _hero_ids else _all_aud
        if all_audience:
            render_section_label("Audience Profile — Who We're Talking To")
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
            render_nopd_cards(merged_nopd)
            st.caption(f"*Synthesized from {len(all_audience)} {HERO} autostrat reports*")
            st.markdown("---")

        # Winning Territories
        all_htw = get_all_how_to_win(autostrat, exclude_reference=True)
        if all_htw:
            render_section_label("Winning Territories")
            all_territories = []
            for entry in all_htw:
                for territory in entry["how_to_win"].get("territories", []):
                    is_dupe = any(territory[:40] == existing[:40] for existing in all_territories)
                    if not is_dupe:
                        all_territories.append(territory)
            render_territory_cards(all_territories[:8])
            st.markdown("---")

        # Content Trends
        all_trends = get_all_content_trends(autostrat)
        if all_trends:
            render_section_label("Content Trends")
            cols = st.columns(2)
            for i, trend in enumerate(all_trends[:6]):
                with cols[i % 2]:
                    render_narrative_card(trend.get("trend", f"Trend {i+1}"),
                                         trend.get("description", ""), accent_color="#F8C090")
            st.markdown("---")

        # Partnership Opportunities
        all_suggestions = get_all_sponsorship_suggestions(autostrat, exclude_reference=True)
        if all_suggestions:
            render_section_label("Partnership Opportunities")
            for entry in all_suggestions:
                source = f"{entry['source_label']} — {entry['identifier'].replace('_', ' ').title()}"
                st.markdown(f"**From: {source}**")
                sug_cols = st.columns(min(len(entry["suggestions"]), 2))
                for i, sug in enumerate(entry["suggestions"]):
                    with sug_cols[i % len(sug_cols)]:
                        render_sponsorship_card(sug)
                st.markdown("")
