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
    PRIORITY_COLORS, GOAT_CADENCE_TARGETS,
    GOAT_PILLAR_MAP, GOAT_PILLAR_TARGETS, GOAT_PILLAR_COLORS,
    CONTENT_MIX_MAP, CONTENT_MIX_TARGETS, CONTENT_MIX_COLORS,
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
ER_TARGET = 3.0

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

    cuervo_ig = cuervo_df[cuervo_df["platform"] == "Instagram"]
    cuervo_reels = cuervo_df[cuervo_df["post_type"] == "Reel"]
    avg_reel_views = cuervo_reels["views"].mean() if len(cuervo_reels) else 0
    avg_reel_views = 0 if pd.isna(avg_reel_views) else avg_reel_views
    reel_ratio = len(cuervo_ig[cuervo_ig["post_type"] == "Reel"]) / max(len(cuervo_ig), 1) * 100

    freq = results["frequency"].get(CUERVO, {})
    ig_ppw = freq.get("Instagram", {}).get("posts_per_week", 0)
    tt_ppw = freq.get("TikTok", {}).get("posts_per_week", 0)

    # Scorecard table
    scorecard_data = [
        {"KPI": "Avg Engagement Rate", "Actual": f"{cuervo_er:.2f}%", "Target": "3.0%",
         "Status": "ON TRACK" if cuervo_er >= 3.0 else "BELOW",
         "Gap": f"{cuervo_er - 3.0:+.2f}pp"},
        {"KPI": "Avg Reel Views", "Actual": f"{avg_reel_views:,.0f}", "Target": "10,000",
         "Status": "ON TRACK" if avg_reel_views >= 10000 else "BELOW",
         "Gap": f"{avg_reel_views - 10000:+,.0f}"},
        {"KPI": "Reel Ratio (IG)", "Actual": f"{reel_ratio:.0f}%", "Target": "50%",
         "Status": "ON TRACK" if reel_ratio >= 50 else "BELOW",
         "Gap": f"{reel_ratio - 50:+.0f}pp"},
        {"KPI": "IG Posts/Week", "Actual": f"{ig_ppw:.1f}", "Target": "4-5/wk",
         "Status": "ON TRACK" if 4 <= ig_ppw <= 5 else ("BELOW" if ig_ppw < 4 else "ABOVE"),
         "Gap": f"{ig_ppw - 4.5:+.1f} vs mid"},
        {"KPI": "TT Posts/Week", "Actual": f"{tt_ppw:.1f}", "Target": "3-4/wk",
         "Status": "ON TRACK" if 3 <= tt_ppw <= 4 else ("BELOW" if tt_ppw < 3 else "ABOVE"),
         "Gap": f"{tt_ppw - 3.5:+.1f} vs mid"},
    ]

    sc_df = pd.DataFrame(scorecard_data)

    def color_status(val):
        if val == "ON TRACK":
            return "background-color: #C8E6C9; color: #2E7D32; font-weight: bold"
        elif val == "BELOW":
            return "background-color: #FFCDD2; color: #C62828; font-weight: bold"
        elif val == "ABOVE":
            return "background-color: #FFE0B2; color: #E65100; font-weight: bold"
        return ""

    st.dataframe(
        sc_df.style.map(color_status, subset=["Status"]),
        width="stretch", hide_index=True, height=230,
    )

    on_track = sum(1 for s in scorecard_data if s["Status"] == "ON TRACK")
    total = len(scorecard_data)
    st.info(f"**{on_track}/{total} KPIs on track.** "
            f"{'Strong position — maintain momentum.' if on_track >= 4 else 'Focus areas identified below.' if on_track >= 2 else 'Significant gaps — prioritize the Action Plan tab.'}")

    st.markdown("---")

    # ── Dynamic vs Static Performance ──────────────────────────────────
    st.subheader("Dynamic vs Static Performance")
    st.caption("GOAT benchmark: Dynamic (video) delivers 2.8% ER vs Static (image) 2.2% ER")

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
        st.plotly_chart(fig_ds, width="stretch")

    st.info(f"**Dynamic content {'outperforms' if dyn_er > stat_er else 'underperforms vs'} static** by "
            f"{abs(dyn_er - stat_er):.2f}pp ER. Cuervo's dynamic mix is {dyn_pct:.0f}% — "
            f"{'meeting' if dyn_pct >= 50 else 'below'} the 50%+ target.")

    st.markdown("---")

    # ── Content Source Mix ─────────────────────────────────────────────
    st.subheader("Content Source Mix — Creator / Brand / Events")
    st.caption("GOAT target: 70% Creator & Influencer, 15% Brand-Owned, 15% Events & Partnerships")

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
        st.markdown("**Content Source: Actual vs GOAT Target**")
        fig_src = go.Figure()
        fig_src.add_trace(go.Bar(x=src_data["Source"], y=src_data["Actual %"],
                                 name="Actual", marker_color=[src_colors[s] for s in src_data["Source"]],
                                 text=src_data["Actual %"], textposition="outside", texttemplate="%{text:.0f}%"))
        fig_src.add_trace(go.Scatter(x=src_data["Source"], y=src_data["Target %"],
                                     name="GOAT Target", mode="markers+lines",
                                     marker=dict(size=12, color="#333333", symbol="diamond"),
                                     line=dict(color="#333333", width=2, dash="dash")))
        fig_src.update_layout(template=CHART_TEMPLATE, font=CHART_FONT, height=380,
                              yaxis_title="% of Content", legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(fig_src, width="stretch")

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
        st.info("**GOAT strategy**: Creators & influencers are the primary content engine. "
                "Brand-owned anchors the brand world. Events provide real-time cultural relevance.")


# ══════════════════════════════════════════════════════════════════════
# TAB 2 — Content Strategy Frameworks
# ══════════════════════════════════════════════════════════════════════

with tab_frameworks:

    # ── GOAT Content Pillars ───────────────────────────────────────────
    st.subheader("Content Pillars — GOAT Framework")
    st.caption("4 pillars from the GOAT Agency Social Playbook Q1 2026")

    PILLARS = [
        {"name": "La Tradición", "target": 25,
         "themes": GOAT_PILLAR_MAP["La Tradición"],
         "desc": "Heritage, education, cocktail recipes — approachable expert tone"},
        {"name": "Cuervo Live", "target": 15,
         "themes": GOAT_PILLAR_MAP["Cuervo Live"],
         "desc": "Events, music, sports — energetic FOMO-inducing content"},
        {"name": "Life, with a Lime", "target": 30,
         "themes": GOAT_PILLAR_MAP["Life, with a Lime"],
         "desc": "Lifestyle, aspirational moments — feel bigger and brighter"},
        {"name": "Culture, Shaken", "target": 30,
         "themes": GOAT_PILLAR_MAP["Culture, Shaken"],
         "desc": "Memes, UGC, trending content — culturally plugged in"},
    ]

    pillar_data = []
    for p in PILLARS:
        matching = cuervo_df[cuervo_df["content_theme"].isin(p["themes"])]
        pct = len(matching) / max(len(cuervo_df), 1) * 100
        er = matching["engagement_rate"].mean() if len(matching) else 0
        er = 0 if pd.isna(er) else er
        pillar_data.append({
            "Pillar": p["name"],
            "Actual %": round(pct, 1),
            "Target %": p["target"],
            "Avg ER": round(er, 2),
            "Posts": len(matching),
            "desc": p["desc"],
        })

    pillar_df = pd.DataFrame(pillar_data)

    col_pd1, col_pd2 = st.columns(2)
    with col_pd1:
        st.markdown("**Pillar Distribution: Actual vs Target**")
        fig_pd = go.Figure()
        fig_pd.add_trace(go.Bar(x=pillar_df["Pillar"], y=pillar_df["Actual %"],
                                name="Actual", marker_color=[GOAT_PILLAR_COLORS[p] for p in pillar_df["Pillar"]],
                                text=pillar_df["Actual %"], textposition="outside", texttemplate="%{text:.0f}%"))
        fig_pd.add_trace(go.Scatter(x=pillar_df["Pillar"], y=pillar_df["Target %"],
                                    name="GOAT Target", mode="markers+lines",
                                    marker=dict(size=12, color="#333333", symbol="diamond"),
                                    line=dict(color="#333333", width=2, dash="dash")))
        fig_pd.update_layout(template=CHART_TEMPLATE, font=CHART_FONT, height=380,
                             yaxis_title="% of Content", legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(fig_pd, width="stretch")

    with col_pd2:
        st.markdown("**Avg ER by Pillar**")
        fig_pe = px.bar(pillar_df, x="Pillar", y="Avg ER",
                        color="Pillar", color_discrete_map=GOAT_PILLAR_COLORS,
                        labels={"Avg ER": "Avg ER %", "Pillar": ""},
                        template=CHART_TEMPLATE, text_auto=".2f")
        fig_pe.add_hline(y=ER_TARGET, line_dash="dash", line_color="#333",
                         annotation_text="3% target", annotation_position="top right")
        fig_pe.update_layout(showlegend=False, font=CHART_FONT, height=380)
        st.plotly_chart(fig_pe, width="stretch")

    # Pillar scorecard
    pillar_desc_map = {p["Pillar"]: p["desc"] for p in pillar_data}
    for _, row in pillar_df.iterrows():
        gap = row["Actual %"] - row["Target %"]
        direction = "ON TRACK" if abs(gap) < 5 else ("MORE" if gap < 0 else "LESS")
        desc = pillar_desc_map.get(row["Pillar"], "")
        if direction == "ON TRACK":
            st.success(f"**{row['Pillar']}** ({desc}): {row['Actual %']:.0f}% actual / {row['Target %']}% target — ON TRACK")
        elif direction == "MORE":
            st.error(f"**{row['Pillar']}** ({desc}): {row['Actual %']:.0f}% actual / {row['Target %']}% target — Need MORE (+{abs(gap):.0f}pp)")
        else:
            st.warning(f"**{row['Pillar']}** ({desc}): {row['Actual %']:.0f}% actual / {row['Target %']}% target — Need LESS ({gap:+.0f}pp)")

    st.markdown("---")

    # ── Content Mix Funnel ─────────────────────────────────────────────
    st.subheader("Content Mix Funnel — Entertain / Educate / Connect / Convince")
    st.caption("GOAT Playbook: grab attention first (Entertain), then guide to action (Convince)")

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
        st.markdown("**Cuervo Content Mix: Actual vs GOAT Target**")
        fig_mix = go.Figure()
        fig_mix.add_trace(go.Bar(x=mix_df["Category"], y=mix_df["Actual %"],
                                 name="Actual", marker_color=[CONTENT_MIX_COLORS[c] for c in mix_df["Category"]],
                                 text=mix_df["Actual %"], textposition="outside", texttemplate="%{text:.0f}%"))
        fig_mix.add_trace(go.Scatter(x=mix_df["Category"], y=mix_df["Target %"],
                                     name="GOAT Target", mode="markers+lines",
                                     marker=dict(size=12, color="#333333", symbol="diamond"),
                                     line=dict(color="#333333", width=2, dash="dash")))
        fig_mix.update_layout(template=CHART_TEMPLATE, font=CHART_FONT, height=380,
                              yaxis_title="% of Content", legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(fig_mix, width="stretch")

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
        ugc_pct = len(bdf[bdf["visual_style"].isin(["Raw / UGC-style", "Lo-fi / Authentic"])]) / total * 100
        collab_pct = results["creators"].get(brand, {}).get("collab_pct", 0)
        humor_pct = len(bdf[bdf["content_theme"].isin(["Meme / Humor"])]) / total * 100
        video_pct = len(bdf[bdf["post_type"].isin(["Reel", "Video"])]) / total * 100
        music_pct = len(bdf[bdf["has_music_audio"].str.lower() == "yes"]) / total * 100 if "has_music_audio" in bdf.columns else 0
        comment_rate = (bdf["comments"].sum() / max(bdf["likes"].sum(), 1)) * 100
        return [ugc_pct, collab_pct, humor_pct, video_pct, music_pct, comment_rate]

    dims = ["Authenticity (UGC %)", "Creator Partners %", "Humor/Meme %",
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
    st.plotly_chart(fig_radar, width="stretch")

    # So What
    cuervo_scores = compute_genz_scores(CUERVO)
    leader_avg_scores = [sum(compute_genz_scores(b)[i] for b in GEN_Z_LEADERS) / len(GEN_Z_LEADERS) for i in range(6)]
    biggest_gap_idx = max(range(6), key=lambda i: leader_avg_scores[i] - cuervo_scores[i])
    biggest_lead_idx = max(range(6), key=lambda i: cuervo_scores[i] - leader_avg_scores[i])
    st.info(f"**Biggest gap vs leaders:** {dims[biggest_gap_idx]} "
            f"(Cuervo {cuervo_scores[biggest_gap_idx]:.0f}% vs leaders {leader_avg_scores[biggest_gap_idx]:.0f}%). "
            f"**Strongest area:** {dims[biggest_lead_idx]} "
            f"(Cuervo {cuervo_scores[biggest_lead_idx]:.0f}% vs leaders {leader_avg_scores[biggest_lead_idx]:.0f}%).")


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
                "Launch 'Life, with a Lime' pillar: 2 Reels featuring Cuervo in social settings",
                "Launch 'La Tradicion' pillar: 1 Carousel with cocktail recipe using Tradicional",
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

    # ── Qualitative Strategic Intel ────────────────────────────────────
    autostrat = st.session_state.get("autostrat", {})
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
