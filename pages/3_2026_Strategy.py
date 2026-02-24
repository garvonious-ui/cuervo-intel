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

from config import (
    BRAND_COLORS, CHART_TEMPLATE, CHART_FONT, BRAND_ORDER, CUSTOM_CSS,
    PRIORITY_COLORS, POPLIFE_CADENCE_TARGETS, SOCIAL_BRIEF_TARGETS,
    POPLIFE_PILLAR_MAP, POPLIFE_PILLAR_TARGETS, POPLIFE_PILLAR_COLORS,
    POPLIFE_PILLAR_DESCRIPTIONS,
    CONTENT_MIX_MAP, CONTENT_MIX_TARGETS, CONTENT_MIX_COLORS,
    CUERVO_HASHTAG_IDS,
    EXECUTION_ENGINES, CREATOR_ARCHETYPES, VOICE_PRINCIPLES,
    SKU_STRATEGY, PLATFORM_ROLES, IG_FORMAT_MIX,
    CULTURAL_CALENDAR, MONTHLY_RAMP, TESTING_ROADMAP,
)
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

st.logo("logo.png")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
st.header("2026 Strategy & Brief")
st.caption("The Cuervo Social Brief playbook — sidebar filters do not apply here.")

if "results" not in st.session_state:
    st.warning("Go to the home page first to load data.")
    st.stop()

results = st.session_state["results"]
df = st.session_state["df"]  # Unfiltered

CUERVO = "Jose Cuervo"
GEN_Z_LEADERS = ["Casamigos", "Teremana"]
_t = SOCIAL_BRIEF_TARGETS
ER_TARGET = _t["er_by_views"]

cuervo_df = df[df["brand"] == CUERVO]
leader_df = df[df["brand"].isin(GEN_Z_LEADERS)]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
tab_scorecard, tab_frameworks, tab_action = st.tabs([
    "Social Brief Scorecard", "Content Strategy Frameworks", "Action Plan",
])

# ══════════════════════════════════════════════════════════════════════
# TAB 1 — Social Brief Scorecard
# ══════════════════════════════════════════════════════════════════════

with tab_scorecard:

    # ── Expanded KPI Scorecard ─────────────────────────────────────────
    st.subheader("Social Brief KPI Scorecard")
    st.caption("Current performance vs 2026 Social Brief targets")

    cuervo_er = cuervo_df["engagement_rate"].mean()
    cuervo_er = 0 if pd.isna(cuervo_er) else cuervo_er
    cat_er = df[df["brand"] != CUERVO]["engagement_rate"].mean()
    cat_er = 0 if pd.isna(cat_er) else cat_er

    # Separate ER metrics
    er_by_followers = results.get("cuervo_er_by_followers", 0)
    benchmark = results.get("benchmark", {})
    cuervo_bench = benchmark.get("Jose Cuervo", {})
    er_by_views = cuervo_bench.get("er_by_views", 0) if cuervo_bench else 0

    cuervo_ig = cuervo_df[cuervo_df["platform"] == "Instagram"]
    avg_eng_per_post = cuervo_df["total_engagement"].mean() if len(cuervo_df) else 0
    avg_eng_per_post = 0 if pd.isna(avg_eng_per_post) else avg_eng_per_post
    reel_ratio = len(cuervo_ig[cuervo_ig["post_type"] == "Reel"]) / max(len(cuervo_ig), 1) * 100
    carousel_ratio = len(cuervo_ig[cuervo_ig["post_type"] == "Carousel"]) / max(len(cuervo_ig), 1) * 100

    # Save & share rates
    total_eng = cuervo_df["total_engagement"].sum() or 1
    save_rate = (cuervo_df["saves"].sum() / total_eng * 100) if "saves" in cuervo_df.columns else 0
    share_rate = (cuervo_df["shares"].sum() / total_eng * 100) if "shares" in cuervo_df.columns else 0

    # Creator content %
    creator_posts = cuervo_df[cuervo_df["has_creator_collab"].astype(str).str.lower() == "yes"] if "has_creator_collab" in cuervo_df.columns else pd.DataFrame()
    creator_pct = len(creator_posts) / max(len(cuervo_df), 1) * 100
    creator_er = creator_posts["engagement_rate"].mean() if len(creator_posts) else 0
    creator_er = 0 if pd.isna(creator_er) else creator_er

    freq = results["frequency"].get(CUERVO, {})
    ig_ppm = freq.get("Instagram", {}).get("posts_per_week", 0) * 4.33  # Convert to monthly
    tt_ppw = freq.get("TikTok", {}).get("posts_per_week", 0)

    # Scorecard table (targets from SOCIAL_BRIEF_TARGETS in config.py)
    _ig_ppm = _t["ig_posts_per_month"]
    _tt_ppw = _t["tt_posts_per_week"]
    scorecard_data = [
        {"KPI": "ER by Followers", "Actual": f"{er_by_followers:.2f}%",
         "Target": f"{_t['er_by_followers']}%+",
         "Status": "ON TRACK" if er_by_followers >= _t["er_by_followers"] else "BELOW",
         "Gap": f"{er_by_followers - _t['er_by_followers']:+.2f}pp"},
        {"KPI": "ER by Views", "Actual": f"{er_by_views:.2f}%",
         "Target": f"{_t['er_by_views']}%+",
         "Status": "ON TRACK" if er_by_views >= _t["er_by_views"] else "BELOW",
         "Gap": f"{er_by_views - _t['er_by_views']:+.2f}pp"},
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
        {"KPI": "Creator ER", "Actual": f"{creator_er:.2f}%",
         "Target": f"{_t['creator_er']}%+",
         "Status": "ON TRACK" if creator_er >= _t["creator_er"] else "BELOW",
         "Gap": f"{creator_er - _t['creator_er']:+.2f}pp"},
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

    # ── Dynamic vs Static Performance ──────────────────────────────────
    st.subheader("Dynamic vs Static Performance")
    st.caption("Poplife benchmark: Dynamic (video) delivers 2.8% ER vs Static (image) 2.2% ER")

    dynamic_types = ["Reel", "Video"]
    static_types = ["Static Image", "Carousel"]

    dyn_posts = cuervo_df[cuervo_df["post_type"].isin(dynamic_types)]
    stat_posts = cuervo_df[cuervo_df["post_type"].isin(static_types)]
    total_ds = len(dyn_posts) + len(stat_posts) or 1
    dyn_pct = len(dyn_posts) / total_ds * 100
    stat_pct = len(stat_posts) / total_ds * 100
    dyn_er = dyn_posts["engagement_rate"].mean() if len(dyn_posts) else 0
    stat_er = stat_posts["engagement_rate"].mean() if len(stat_posts) else 0
    dyn_er = 0 if pd.isna(dyn_er) else dyn_er
    stat_er = 0 if pd.isna(stat_er) else stat_er

    ds1, ds2, ds3, ds4 = st.columns(4)
    with ds1:
        st.metric("Dynamic %", f"{dyn_pct:.0f}%", help="Reels + Video")
    with ds2:
        st.metric("Dynamic ER", f"{dyn_er:.2f}%",
                  delta=f"{dyn_er - stat_er:+.2f}% vs Static" if stat_er > 0 else None)
    with ds3:
        st.metric("Static %", f"{stat_pct:.0f}%", help="Static Image + Carousel")
    with ds4:
        st.metric("Static ER", f"{stat_er:.2f}%")

    # Cross-brand comparison
    all_brand_ds = []
    for brand in BRAND_ORDER:
        bdf = df[df["brand"] == brand]
        if len(bdf) == 0:
            continue
        b_dyn = bdf[bdf["post_type"].isin(dynamic_types)]
        b_stat = bdf[bdf["post_type"].isin(static_types)]
        b_dyn_er = b_dyn["engagement_rate"].mean() if len(b_dyn) else 0
        b_stat_er = b_stat["engagement_rate"].mean() if len(b_stat) else 0
        b_dyn_er = 0 if pd.isna(b_dyn_er) else b_dyn_er
        b_stat_er = 0 if pd.isna(b_stat_er) else b_stat_er
        all_brand_ds.append({"Brand": brand, "Dynamic ER": round(b_dyn_er, 2), "Static ER": round(b_stat_er, 2)})

    if all_brand_ds:
        ds_df = pd.DataFrame(all_brand_ds)
        ds_melt = pd.melt(ds_df, id_vars=["Brand"], value_vars=["Dynamic ER", "Static ER"],
                          var_name="Format", value_name="ER")
        fig_ds = px.bar(ds_melt, x="Brand", y="ER", color="Format", barmode="group",
                        color_discrete_map={"Dynamic ER": "#2ea3f2", "Static ER": "#C9A87E"},
                        labels={"ER": "Avg ER %", "Brand": ""},
                        template=CHART_TEMPLATE, text_auto=".2f")
        fig_ds.update_layout(font=CHART_FONT, height=380, legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(fig_ds, use_container_width=True)

    st.info(f"**Dynamic content {'outperforms' if dyn_er > stat_er else 'underperforms vs'} static** by "
            f"{abs(dyn_er - stat_er):.2f}pp ER. Cuervo's dynamic mix is {dyn_pct:.0f}% — "
            f"{'meeting' if dyn_pct >= 50 else 'below'} the 50%+ target.")

    st.markdown("---")

    # ── Content Source Mix ─────────────────────────────────────────────
    st.subheader("Content Source Mix — Creator / Brand / Events")
    st.caption("Poplife target: 70% Creator & Influencer, 15% Brand-Owned, 15% Events & Partnerships")

    event_themes = ["Event / Activation", "Music / Party"]
    creator_posts = cuervo_df[cuervo_df["has_creator_collab"] == "Yes"] if "has_creator_collab" in cuervo_df.columns else pd.DataFrame()
    event_posts = cuervo_df[(cuervo_df["content_theme"].isin(event_themes)) &
                            (cuervo_df.get("has_creator_collab", pd.Series(dtype=str)) != "Yes")] if "has_creator_collab" in cuervo_df.columns else cuervo_df[cuervo_df["content_theme"].isin(event_themes)]
    brand_posts_count = len(cuervo_df) - len(creator_posts) - len(event_posts)

    src_total = max(len(cuervo_df), 1)
    src_data = pd.DataFrame([
        {"Source": "Creators & Influencers", "Actual %": round(len(creator_posts) / src_total * 100, 1), "Target %": 70},
        {"Source": "Events & Partnerships", "Actual %": round(len(event_posts) / src_total * 100, 1), "Target %": 15},
        {"Source": "Brand-Owned", "Actual %": round(brand_posts_count / src_total * 100, 1), "Target %": 15},
    ])

    src_colors = {"Creators & Influencers": "#2ea3f2", "Events & Partnerships": "#D4956A", "Brand-Owned": "#C9A87E"}

    col_src1, col_src2 = st.columns(2)
    with col_src1:
        st.markdown("**Content Source: Actual vs Poplife Target**")
        fig_src = go.Figure()
        fig_src.add_trace(go.Bar(x=src_data["Source"], y=src_data["Actual %"],
                                 name="Actual", marker_color=[src_colors[s] for s in src_data["Source"]],
                                 text=src_data["Actual %"], textposition="outside", texttemplate="%{text:.0f}%"))
        fig_src.add_trace(go.Scatter(x=src_data["Source"], y=src_data["Target %"],
                                     name="Poplife Target", mode="markers+lines",
                                     marker=dict(size=12, color="#333333", symbol="diamond"),
                                     line=dict(color="#333333", width=2, dash="dash")))
        fig_src.update_layout(template=CHART_TEMPLATE, font=CHART_FONT, height=380,
                              yaxis_title="% of Content", legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(fig_src, use_container_width=True)

    with col_src2:
        st.markdown("**Content Source Scorecard**")
        for _, row in src_data.iterrows():
            gap = row["Actual %"] - row["Target %"]
            direction = "ON TRACK" if abs(gap) < 10 else ("MORE" if gap < 0 else "LESS")
            if direction == "ON TRACK":
                st.success(f"**{row['Source']}**: {row['Actual %']:.0f}% actual / {row['Target %']}% target ({gap:+.0f}%)")
            elif direction == "MORE":
                st.error(f"**{row['Source']}**: {row['Actual %']:.0f}% actual / {row['Target %']}% target ({gap:+.0f}%) — Need MORE")
            else:
                st.warning(f"**{row['Source']}**: {row['Actual %']:.0f}% actual / {row['Target %']}% target ({gap:+.0f}%) — Need LESS")
        st.markdown("")
        st.info("**Poplife strategy**: Creators & influencers are the primary content engine. "
                "Brand-owned anchors the brand world. Events provide real-time cultural relevance.")

    st.markdown("---")

    # ── Best Performing Theme ──────────────────────────────────────────
    st.subheader("Best Performing Content Theme")
    st.caption("Which content theme drives the highest engagement for Cuervo")

    theme_perf = results["themes"].get(CUERVO, {}).get("theme_performance", {})
    best_theme_name = results["themes"].get(CUERVO, {}).get("best_performing_theme", "N/A")

    if theme_perf and best_theme_name != "N/A":
        best_theme_data = theme_perf.get(best_theme_name, {})
        best_er = best_theme_data.get("avg_engagement_rate", 0)
        best_count = best_theme_data.get("count", 0)

        # Metric card
        bt_col1, bt_col2, bt_col3 = st.columns(3)
        with bt_col1:
            st.metric("Best Theme", best_theme_name)
        with bt_col2:
            st.metric("Theme ER", f"{best_er:.2f}%",
                      delta=f"{best_er - ER_TARGET:+.2f}% vs {ER_TARGET}% target")
        with bt_col3:
            st.metric("Posts", f"{best_count}")

        # Mini bar chart of all themes by ER
        theme_rows = [{"Theme": t, "ER %": round(v["avg_engagement_rate"], 2), "Posts": v["count"]}
                      for t, v in theme_perf.items() if v.get("avg_engagement_rate", 0) > 0]
        if theme_rows:
            theme_chart_df = pd.DataFrame(theme_rows).sort_values("ER %", ascending=True)
            fig_bt = px.bar(theme_chart_df, x="ER %", y="Theme", orientation="h",
                            color_discrete_sequence=[BRAND_COLORS[CUERVO]],
                            labels={"ER %": "Avg ER %", "Theme": ""},
                            template=CHART_TEMPLATE, text_auto=".2f",
                            hover_data={"Posts": True})
            fig_bt.add_vline(x=ER_TARGET, line_dash="dash", line_color="#333",
                             annotation_text=f"{ER_TARGET}% target")
            fig_bt.update_layout(font=CHART_FONT, height=max(280, len(theme_rows) * 35),
                                 showlegend=False)
            st.plotly_chart(fig_bt, use_container_width=True)

        st.info(f"**Best theme: {best_theme_name}** at {best_er:.2f}% ER — lean into this for upcoming content. "
                f"Themes above the {ER_TARGET}% target are proven winners worth scaling.")
    else:
        st.info("No content theme performance data available for Cuervo.")


# ══════════════════════════════════════════════════════════════════════
# TAB 2 — Content Strategy Frameworks
# ══════════════════════════════════════════════════════════════════════

with tab_frameworks:

    # ── Content Pillars (2 pillars from 2026 deck) ──────────────────────
    st.subheader("Content Pillars")
    st.caption("2 pillars from the 2026 Social Strategy — SKU-aligned content territories")

    pillar_data = []
    for pillar_name, themes in POPLIFE_PILLAR_MAP.items():
        matching = cuervo_df[cuervo_df["content_theme"].isin(themes)]
        pct = len(matching) / max(len(cuervo_df), 1) * 100
        er = matching["engagement_rate"].mean() if len(matching) else 0
        er = 0 if pd.isna(er) else er
        pillar_data.append({
            "Pillar": pillar_name,
            "Actual %": round(pct, 1),
            "Target %": POPLIFE_PILLAR_TARGETS[pillar_name],
            "Avg ER": round(er, 2),
            "Posts": len(matching),
            "desc": POPLIFE_PILLAR_DESCRIPTIONS.get(pillar_name, ""),
        })

    pillar_df = pd.DataFrame(pillar_data)

    # Pillar detail cards
    for _, row in pillar_df.iterrows():
        gap = row["Actual %"] - row["Target %"]
        color = POPLIFE_PILLAR_COLORS[row["Pillar"]]
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
                <span><strong>{row['Avg ER']:.2f}%</strong> avg ER</span>
                <span style="color:{'#2E7D32' if abs(gap) < 10 else '#C62828'};">{gap:+.0f}pp gap</span>
            </div>
        </div>""", unsafe_allow_html=True)

    col_pd1, col_pd2 = st.columns(2)
    with col_pd1:
        st.markdown("**Pillar Distribution: Actual vs Target**")
        fig_pd = go.Figure()
        fig_pd.add_trace(go.Bar(x=pillar_df["Pillar"], y=pillar_df["Actual %"],
                                name="Actual", marker_color=[POPLIFE_PILLAR_COLORS[p] for p in pillar_df["Pillar"]],
                                text=pillar_df["Actual %"], textposition="outside", texttemplate="%{text:.0f}%"))
        fig_pd.add_trace(go.Scatter(x=pillar_df["Pillar"], y=pillar_df["Target %"],
                                    name="Target", mode="markers+lines",
                                    marker=dict(size=12, color="#333333", symbol="diamond"),
                                    line=dict(color="#333333", width=2, dash="dash")))
        fig_pd.update_layout(template=CHART_TEMPLATE, font=CHART_FONT, height=380,
                             yaxis_title="% of Content", legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(fig_pd, use_container_width=True)

    with col_pd2:
        st.markdown("**Avg ER by Pillar**")
        fig_pe = px.bar(pillar_df, x="Pillar", y="Avg ER",
                        color="Pillar", color_discrete_map=POPLIFE_PILLAR_COLORS,
                        labels={"Avg ER": "Avg ER %", "Pillar": ""},
                        template=CHART_TEMPLATE, text_auto=".2f")
        fig_pe.add_hline(y=ER_TARGET, line_dash="dash", line_color="#333",
                         annotation_text=f"{ER_TARGET}% target", annotation_position="top right")
        fig_pe.update_layout(showlegend=False, font=CHART_FONT, height=380)
        st.plotly_chart(fig_pe, use_container_width=True)

    st.markdown("---")

    # ── SKU Strategy ────────────────────────────────────────────────────
    st.subheader("SKU Strategy")
    st.caption("Each SKU has a distinct energy and occasion — content should match")

    sku_cols = st.columns(len(SKU_STRATEGY))
    sku_colors = {"Especial": "#F8C090", "Tradicional": "#C9A87E", "RTD": "#2ea3f2"}
    for col, (sku, info) in zip(sku_cols, SKU_STRATEGY.items()):
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
    for i, (engine, desc) in enumerate(EXECUTION_ENGINES.items()):
        with eng_cols[i % 2]:
            c = engine_colors[i]
            st.markdown(f"""
            <div style="background:white; border-radius:10px; padding:16px 18px; margin-bottom:12px;
                        border-top:4px solid {c}; border:1px solid #E0D8D0; min-height:120px;">
                <h4 style="margin:0 0 8px 0; color:{c}; font-size:0.95rem;">{engine.upper()}</h4>
                <p style="color:#555; font-size:0.88rem; line-height:1.5; margin:0;">{desc}</p>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── The Cuervo Crew (Creator Archetypes) ────────────────────────────
    st.subheader("The Cuervo Crew — Creator Archetypes")
    st.caption("Creators embedded in the brand — not hired talent. iPhone-first. Social-native.")

    arch_cols = st.columns(min(len(CREATOR_ARCHETYPES), 5))
    for i, (archetype, fit) in enumerate(CREATOR_ARCHETYPES.items()):
        with arch_cols[i % len(arch_cols)]:
            st.markdown(f"""
            <div style="background:white; border-radius:10px; padding:14px; text-align:center;
                        border:1px solid #E0D8D0; min-height:100px;">
                <p style="font-weight:700; color:#333; margin:0 0 6px 0; font-size:0.9rem;">{archetype}</p>
                <p style="color:#666; font-size:0.82rem; margin:0;">{fit}</p>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── Content Mix Funnel ─────────────────────────────────────────────
    st.subheader("Content Mix Funnel — Entertain / Educate / Connect / Convince")
    st.caption("Grab attention first (Entertain 50%), then guide to action (Convince 10%)")

    cuervo_mix_data = []
    for cat in ["Entertain", "Educate", "Connect", "Convince"]:
        cat_themes = CONTENT_MIX_MAP[cat]
        matching = cuervo_df[cuervo_df["content_theme"].isin(cat_themes)]
        pct = len(matching) / max(len(cuervo_df), 1) * 100
        target = CONTENT_MIX_TARGETS[cat]
        cuervo_mix_data.append({
            "Category": cat,
            "Actual %": round(pct, 1),
            "Target %": target,
            "Gap": round(pct - target, 1),
            "Posts": len(matching),
        })

    mix_df = pd.DataFrame(cuervo_mix_data)

    col_mix1, col_mix2 = st.columns(2)
    with col_mix1:
        st.markdown("**Cuervo Content Mix: Actual vs Poplife Target**")
        fig_mix = go.Figure()
        fig_mix.add_trace(go.Bar(x=mix_df["Category"], y=mix_df["Actual %"],
                                 name="Actual", marker_color=[CONTENT_MIX_COLORS[c] for c in mix_df["Category"]],
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

    st.markdown("---")

    # ── Gen Z Engagement Drivers ───────────────────────────────────────
    st.subheader("Gen Z Engagement Drivers")
    st.caption("Cuervo vs Gen Z leaders on 6 key dimensions")

    compare_brands = [CUERVO] + GEN_Z_LEADERS

    def compute_genz_scores(brand):
        bdf = df[df["brand"] == brand]
        total = len(bdf) or 1
        ugc_pct = len(bdf[bdf["has_creator_collab"].astype(str).str.lower() == "yes"]) / total * 100 if "has_creator_collab" in bdf.columns else 0
        collab_pct = results["creators"].get(brand, {}).get("collab_pct", 0)
        humor_pct = len(bdf[bdf["content_theme"].isin(["Meme / Humor"])]) / total * 100
        video_pct = len(bdf[bdf["post_type"].isin(["Reel", "Video"])]) / total * 100
        music_pct = len(bdf[bdf["has_music_audio"].str.lower() == "yes"]) / total * 100 if "has_music_audio" in bdf.columns else 0
        comment_rate = (bdf["comments"].sum() / max(bdf["likes"].sum(), 1)) * 100
        return [ugc_pct, collab_pct, humor_pct, video_pct, music_pct, comment_rate]

    dims = ["Creator/UGC Content %", "Creator Partners %", "Humor/Meme %",
            "Short-form Video %", "Music Integration %", "Community Engagement"]

    genz_rows = []
    for brand in compare_brands:
        scores = compute_genz_scores(brand)
        for i, dim in enumerate(dims):
            genz_rows.append({"Brand": brand, "Driver": dim, "Value": round(scores[i], 1)})

    genz_df = pd.DataFrame(genz_rows)
    fig_radar = px.bar(genz_df, x="Value", y="Driver", color="Brand", orientation="h",
                       barmode="group", color_discrete_map=BRAND_COLORS,
                       labels={"Value": "%", "Driver": ""},
                       template=CHART_TEMPLATE, text_auto=".1f")
    fig_radar.update_layout(height=480, font=CHART_FONT,
                            legend=dict(orientation="h", y=-0.12))
    st.plotly_chart(fig_radar, use_container_width=True)

    # So What
    cuervo_scores = compute_genz_scores(CUERVO)
    leader_avg_scores = [sum(compute_genz_scores(b)[i] for b in GEN_Z_LEADERS) / len(GEN_Z_LEADERS) for i in range(6)]
    biggest_gap_idx = max(range(6), key=lambda i: leader_avg_scores[i] - cuervo_scores[i])
    biggest_lead_idx = max(range(6), key=lambda i: cuervo_scores[i] - leader_avg_scores[i])
    st.info(f"**Biggest gap vs leaders:** {dims[biggest_gap_idx]} "
            f"(Cuervo {cuervo_scores[biggest_gap_idx]:.0f}% vs leaders {leader_avg_scores[biggest_gap_idx]:.0f}%). "
            f"**Strongest area:** {dims[biggest_lead_idx]} "
            f"(Cuervo {cuervo_scores[biggest_lead_idx]:.0f}% vs leaders {leader_avg_scores[biggest_lead_idx]:.0f}%).")

    st.markdown("---")

    # ── Voice Principles ────────────────────────────────────────────────
    st.subheader("Tone of Voice — The Life of the Party")
    st.caption("Cuervo's social voice: lively, approachable, human-forward, extroverted")

    for principle, detail in VOICE_PRINCIPLES:
        st.markdown(f"""
        <div style="background:white; border-radius:8px; padding:12px 18px; margin-bottom:8px;
                    border-left:4px solid #F8C090; border:1px solid #E0D8D0;">
            <strong style="color:#333;">{principle}</strong>
            <span style="color:#888; margin-left:12px;">{detail}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── Platform Playbook ───────────────────────────────────────────────
    st.subheader("Platform Playbook")
    st.caption("Platform roles, priority levels, and cadence targets")

    plat_rows = []
    for plat, info in PLATFORM_ROLES.items():
        plat_rows.append({"Platform": plat, "Role": info["role"], "Priority": info["priority"], "Cadence": info["cadence"]})
    plat_df = pd.DataFrame(plat_rows)

    def color_priority(val):
        if val == "Primary":
            return "background-color: #C8E6C9; color: #2E7D32; font-weight: bold"
        return "background-color: #E0E0E0; color: #555"

    st.dataframe(
        plat_df.style.map(color_priority, subset=["Priority"]),
        use_container_width=True, hide_index=True, height=260,
    )

    # IG Format Mix
    st.markdown("**Instagram Format Mix**")
    fmt_cols = st.columns(len(IG_FORMAT_MIX))
    fmt_colors = ["#2ea3f2", "#F8C090", "#C9A87E", "#66BB6A"]
    for i, (fmt, info) in enumerate(IG_FORMAT_MIX.items()):
        with fmt_cols[i]:
            c = fmt_colors[i]
            st.markdown(f"""
            <div style="text-align:center; background:white; border-radius:8px; padding:12px;
                        border-top:3px solid {c}; border:1px solid #E0D8D0;">
                <p style="font-size:1.4rem; font-weight:700; color:{c}; margin:0;">{info['pct']}%</p>
                <p style="font-weight:600; margin:2px 0; color:#333;">{fmt}</p>
                <p style="color:#888; font-size:0.8rem; margin:0;">{info['role']}</p>
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# TAB 3 — Action Plan
# ══════════════════════════════════════════════════════════════════════

with tab_action:

    # ── 30-Day Action Plan ─────────────────────────────────────────────
    st.subheader("30-Day Action Plan for Cuervo")

    cuervo_ppw = sum(results["frequency"].get(CUERVO, {}).get(p, {}).get("posts_per_week", 0)
                     for p in ["Instagram", "TikTok"])
    leader_avg_ppw = sum(
        results["frequency"].get(b, {}).get(p, {}).get("posts_per_week", 0)
        for b in GEN_Z_LEADERS for p in ["Instagram", "TikTok"]
    ) / max(len(GEN_Z_LEADERS), 1)
    rec_ppw = round(leader_avg_ppw, 0)

    top_themes_for_leaders = leader_df.groupby("content_theme")["engagement_rate"].mean().nlargest(3)

    cuervo_scores_local = compute_genz_scores(CUERVO)
    video_pct = cuervo_scores_local[3]

    plan = [
        {
            "week": "Week 1",
            "focus": "Format Reset & Creator Pipeline",
            "actions": [
                f"Ramp posting to {int(rec_ppw)}+ posts/week (currently {cuervo_ppw:.0f}/wk)",
                f"Shift IG mix to 60%+ Reels (currently {video_pct:.0f}% video)",
                "Build creator shortlist: 5 micro-creators (10K-100K) in Lifestyle, Comedy, and Food niches",
                "Audit current grid aesthetic — does it signal 'fun' at a glance?",
            ],
        },
        {
            "week": "Week 2",
            "focus": "Content Pillar Launch",
            "actions": [
                "Launch 'Cuervo in Culture' pillar: 2 Reels featuring meme/reactive cultural content (Especial + RTDs)",
                "Launch 'Tradicional, Made Social' pillar: 1 Carousel with cocktail recipe using Tradicional",
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
                "Analyze Week 1-3: identify top 3 posts by ER, saves, and shares",
                "Double down on winning formats — scale what works, drop what doesn't",
                f"Set ER target: close gap to {ER_TARGET}% by 25% within 60 days",
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
    cal_cols = st.columns(len(CULTURAL_CALENDAR))
    for col, (quarter, info) in zip(cal_cols, CULTURAL_CALENDAR.items()):
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
    for month, targets in MONTHLY_RAMP.items():
        ramp_rows.append({
            "Month": month,
            "Creator % of Total": targets["creator_pct"],
            "Avg ER Target": targets["er_target"],
            "Proactive Comments/Wk": targets["proactive_comments_wk"],
        })
    ramp_df = pd.DataFrame(ramp_rows)
    st.dataframe(ramp_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── Testing Roadmap ─────────────────────────────────────────────────
    st.subheader("Testing Roadmap")
    st.caption("Monthly A/B tests to optimize content strategy")

    test_rows = []
    for month, info in TESTING_ROADMAP.items():
        test_rows.append({"Month": month, "Test Variable": info["variable"], "What We're Learning": info["learning"]})
    test_df = pd.DataFrame(test_rows)
    st.dataframe(test_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── Threats & Opportunities ────────────────────────────────────────
    st.subheader("Threats & Opportunities")

    col_t, col_o = st.columns(2)

    with col_t:
        st.error("**Competitive Threats**")
        brand_counts = df.groupby("brand").size()
        if len(brand_counts):
            highest_poster = brand_counts.idxmax()
            highest_post_count = brand_counts.max()
            cuervo_count = len(cuervo_df)
            if highest_poster != CUERVO:
                st.markdown(f"- {highest_poster} leads with **{highest_post_count}** posts vs Cuervo's **{cuervo_count}** — losing share of voice")

        brand_ers_all = df.groupby("brand")["engagement_rate"].mean()
        if len(brand_ers_all):
            best_er_brand = brand_ers_all.idxmax()
            best_er_val = brand_ers_all.max()
            if best_er_brand != CUERVO:
                st.markdown(f"- {best_er_brand} dominates engagement at **{best_er_val:.2f}% ER**")

        if results["creators"]:
            collab_items = [(b, v.get("collab_pct", 0)) for b, v in results["creators"].items() if b != CUERVO]
            if collab_items:
                highest_collab = max(collab_items, key=lambda x: x[1])
                cuervo_collab = results["creators"].get(CUERVO, {}).get("collab_pct", 0)
                if highest_collab[1] > cuervo_collab:
                    st.markdown(f"- {highest_collab[0]}'s creator collab rate ({highest_collab[1]:.0f}%) "
                                f"dwarfs Cuervo's ({cuervo_collab:.0f}%)")

    with col_o:
        st.success("**Opportunities for Cuervo**")
        cuervo_theme_er = cuervo_df.groupby("content_theme")["engagement_rate"].mean() if len(cuervo_df) else pd.Series(dtype=float)
        cuervo_best_theme = cuervo_theme_er.idxmax() if len(cuervo_theme_er) else "N/A"
        cuervo_best_er = cuervo_theme_er.max() if len(cuervo_theme_er) else 0
        if cuervo_best_theme != "N/A":
            st.markdown(f"- Cuervo's **{cuervo_best_theme}** content is the top-performing theme at {cuervo_best_er:.2f}% ER")

        reel_pct_opp = len(cuervo_df[cuervo_df["post_type"] == "Reel"]) / max(len(cuervo_df[cuervo_df["platform"] == "Instagram"]), 1) * 100
        if reel_pct_opp < 60:
            st.markdown(f"- Instagram Reels at only **{reel_pct_opp:.0f}%** of IG content — room to grow to 60%+")
        st.markdown("- Brand heritage (250+ yrs) is a unique differentiator vs newer brands")
        st.markdown("- RTD line (Playamar, Margarita cans) offers untapped content pillar")
        st.markdown("- 'Fun signal' positioning aligns with Gen Z values — be the brand you bring")

    st.markdown("---")

    # ── All Recommendations ────────────────────────────────────────────
    st.subheader("All Recommendations")

    recs = results["recommendations"]
    if recs:
        for priority in ["High", "Medium", "Low"]:
            pri_recs = [r for r in recs if r["priority"] == priority]
            if pri_recs:
                color = PRIORITY_COLORS[priority]
                st.markdown(f"#### {priority} Priority ({len(pri_recs)})")
                for r in pri_recs:
                    with st.expander(f"[{r['platform']}] {r['category']}: {r['recommendation'][:80]}"):
                        st.markdown(f"**Insight:** {r['insight']}")
                        st.markdown(f"**Action:** {r['recommendation']}")
    else:
        st.info("No recommendations generated.")

    st.markdown("---")

    # ── Autostrat Strategic Actions ────────────────────────────────────
    autostrat = st.session_state.get("autostrat", {})
    _has_autostrat_actions = has_autostrat_data(autostrat)

    if _has_autostrat_actions:
        # Split: Cuervo-specific reports vs competitor reports
        cuervo_strat = get_all_strategic_actions(autostrat, identifier_filter=CUERVO_HASHTAG_IDS)
        all_strat = get_all_strategic_actions(autostrat)
        competitor_strat = [a for a in all_strat if a["source_identifier"] not in CUERVO_HASHTAG_IDS]

        # Helper: aggregate entries into categorized lists
        def _aggregate(entries):
            findings, opps, gaps, actions = [], [], [], []
            for entry in entries:
                src = entry["source_identifier"].replace("_", " ").title()
                for f in entry.get("key_findings", []):
                    findings.append({"source": src, "text": f})
                for o in entry.get("opportunities", []):
                    opps.append({"source": src, "text": o})
                for g in entry.get("gaps_risks_unmet_needs", []):
                    gaps.append({"source": src, "text": g})
                for a in entry.get("strategic_actions", []):
                    actions.append({"source": src, "text": a})
            return findings, opps, gaps, actions

        # ── Section A: Cuervo Strategic Intelligence ──────────────────────
        if cuervo_strat:
            st.subheader("Cuervo Strategic Intelligence")
            st.caption("From #JoseCuervo, #Cuervo, and Cuervo keyword reports")

            c_findings, c_opps, c_gaps, c_actions = _aggregate(cuervo_strat)

            col_sa1, col_sa2 = st.columns(2)
            with col_sa1:
                if c_findings:
                    with st.expander(f"Key Findings ({len(c_findings)})", expanded=True):
                        for item in c_findings:
                            st.markdown(f"- {item['text']}")
                if c_opps:
                    with st.expander(f"Opportunities ({len(c_opps)})"):
                        for item in c_opps:
                            st.markdown(f"- {item['text']}")
            with col_sa2:
                if c_gaps:
                    with st.expander(f"Gaps, Risks & Unmet Needs ({len(c_gaps)})", expanded=True):
                        for item in c_gaps:
                            st.markdown(f"- {item['text']}")
                if c_actions:
                    with st.expander(f"Strategic Actions ({len(c_actions)})"):
                        for item in c_actions:
                            st.markdown(f"- {item['text']}")

            total_cuervo = len(c_findings) + len(c_opps) + len(c_gaps) + len(c_actions)
            st.info(f"**{total_cuervo} Cuervo-specific insights** from {len(cuervo_strat)} reports.")

        # ── Section B: Competitive Context ────────────────────────────────
        if competitor_strat:
            comp_findings, comp_opps, comp_gaps, comp_actions = _aggregate(competitor_strat)
            total_comp = len(comp_findings) + len(comp_opps) + len(comp_gaps) + len(comp_actions)

            with st.expander(f"Competitive Context — {total_comp} insights from {len(competitor_strat)} competitor reports"):
                st.caption("What competitors are doing — use this to identify gaps Cuervo can exploit")

                col_cc1, col_cc2 = st.columns(2)
                with col_cc1:
                    if comp_findings:
                        st.markdown("**Key Findings**")
                        for item in comp_findings[:8]:
                            st.markdown(f"- **{item['source']}** — {item['text']}")
                    if comp_opps:
                        st.markdown("**Opportunities**")
                        for item in comp_opps[:8]:
                            st.markdown(f"- **{item['source']}** — {item['text']}")
                with col_cc2:
                    if comp_gaps:
                        st.markdown("**Gaps & Risks**")
                        for item in comp_gaps[:8]:
                            st.markdown(f"- **{item['source']}** — {item['text']}")
                    if comp_actions:
                        st.markdown("**Strategic Actions**")
                        for item in comp_actions[:8]:
                            st.markdown(f"- **{item['source']}** — {item['text']}")

    st.markdown("---")

    # ── Qualitative Strategic Intel ────────────────────────────────────
    _has_autostrat = has_autostrat_data(autostrat)

    if _has_autostrat:
        st.subheader("Qualitative Strategic Intelligence")
        st.caption("From autostrat.ai reports — audience insights, content trends, creator archetypes")

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

        # Creator Archetypes
        all_archetypes = get_all_creator_archetypes(autostrat)
        if all_archetypes:
            render_section_label("Creator Archetypes to Target")
            arch_cols = st.columns(min(len(all_archetypes), 3))
            for i, arch in enumerate(all_archetypes[:6]):
                with arch_cols[i % len(arch_cols)]:
                    render_creator_archetype(arch)
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
