import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from config import (
    BRAND_COLORS, CHART_TEMPLATE, CHART_FONT, BRAND_ORDER, PRIORITY_COLORS, CUSTOM_CSS,
    GOAT_PILLAR_MAP, GOAT_PILLAR_TARGETS, GOAT_PILLAR_COLORS,
    CONTENT_MIX_MAP, CONTENT_MIX_TARGETS, CONTENT_MIX_COLORS,
    GOAT_CADENCE_TARGETS,
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
st.header("Cuervo Gen Z Strategy Hub")
st.caption("Actionable insights for Jose Cuervo targeting Gen Z (21-24)")

if "results" not in st.session_state:
    st.warning("Go to the home page first to load data.")
    st.stop()

results = st.session_state["results"]
df = st.session_state["df"]  # Use unfiltered data for strategy comparisons
st.caption("This page uses the full dataset for strategy comparisons (sidebar filters do not apply here).")

CUERVO = "Jose Cuervo"
GEN_Z_LEADERS = ["Casamigos", "Teremana"]  # Highest ER / creator-forward brands

cuervo_df = df[df["brand"] == CUERVO]
leader_df = df[df["brand"].isin(GEN_Z_LEADERS)]

# ── Performance vs Gen Z leaders ──────────────────────────────────────

st.subheader("Cuervo vs Gen Z Leaders")

compare_brands = [CUERVO] + GEN_Z_LEADERS

c1, c2, c3, c4 = st.columns(4)

def brand_metric(brand, col):
    bdf = df[df["brand"] == brand]
    er = bdf["engagement_rate"].mean()
    er = 0 if pd.isna(er) else er
    cr = results["creators"].get(brand, {})
    freq = results["frequency"].get(brand, {})
    ppw = sum(freq.get(p, {}).get("posts_per_week", 0) for p in ["Instagram", "TikTok"])
    return er, cr.get("collab_pct", 0), ppw

cuervo_er, cuervo_collab, cuervo_ppw = brand_metric(CUERVO, c1)

for brand in GEN_Z_LEADERS:
    er, collab, ppw = brand_metric(brand, None)

# Show deltas
leader_avg_er = df[df["brand"].isin(GEN_Z_LEADERS)]["engagement_rate"].mean()
leader_avg_er = 0 if pd.isna(leader_avg_er) else leader_avg_er
leader_avg_collab = sum(results["creators"].get(b, {}).get("collab_pct", 0) for b in GEN_Z_LEADERS) / len(GEN_Z_LEADERS)
leader_avg_ppw = 0
for b in GEN_Z_LEADERS:
    for p in ["Instagram", "TikTok"]:
        leader_avg_ppw += results["frequency"].get(b, {}).get(p, {}).get("posts_per_week", 0)
leader_avg_ppw /= len(GEN_Z_LEADERS)

with c1:
    st.metric("Cuervo Avg ER", f"{cuervo_er:.2f}%",
              delta=f"{cuervo_er - leader_avg_er:+.2f}% vs leaders")
with c2:
    st.metric("Cuervo Collab Rate", f"{cuervo_collab:.1f}%",
              delta=f"{cuervo_collab - leader_avg_collab:+.1f}% vs leaders")
with c3:
    st.metric("Cuervo Posts/Wk", f"{cuervo_ppw:.1f}",
              delta=f"{cuervo_ppw - leader_avg_ppw:+.1f} vs leaders")
with c4:
    cuervo_tt_er = df[(df["brand"] == CUERVO) & (df["platform"] == "TikTok")]["engagement_rate"].mean()
    leader_tt_er = df[(df["brand"].isin(GEN_Z_LEADERS)) & (df["platform"] == "TikTok")]["engagement_rate"].mean()
    cuervo_tt_er = 0 if pd.isna(cuervo_tt_er) else cuervo_tt_er
    leader_tt_er = 0 if pd.isna(leader_tt_er) else leader_tt_er
    st.metric("Cuervo TikTok ER", f"{cuervo_tt_er:.2f}%",
              delta=f"{cuervo_tt_er - leader_tt_er:+.2f}% vs leaders")

# ── Gen Z engagement drivers radar ────────────────────────────────────

st.subheader("Gen Z Engagement Drivers")

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

raw_scores = {brand: compute_genz_scores(brand) for brand in compare_brands}

genz_rows = []
for brand in compare_brands:
    for i, dim in enumerate(dims):
        genz_rows.append({"Brand": brand, "Driver": dim, "Value": round(raw_scores[brand][i], 1)})

genz_df = pd.DataFrame(genz_rows)
fig_radar = px.bar(genz_df, x="Value", y="Driver", color="Brand", orientation="h",
                   barmode="group", color_discrete_map=BRAND_COLORS,
                   labels={"Value": "%", "Driver": ""},
                   template=CHART_TEMPLATE, text_auto=".1f")
fig_radar.update_layout(height=480, font=CHART_FONT,
                        legend=dict(orientation="h", y=-0.12))
st.plotly_chart(fig_radar, width="stretch")

# ── Content Format Strategy ───────────────────────────────────────────

st.subheader("Content Format Strategy")
st.caption("Reels should be the primary format driver — data shows format mix and ER performance")

cuervo_ig = cuervo_df[cuervo_df["platform"] == "Instagram"]
leader_ig = leader_df[leader_df["platform"] == "Instagram"]

format_compare_rows = []
for fmt in ["Reel", "Carousel", "Static Image"]:
    c_count = len(cuervo_ig[cuervo_ig["post_type"] == fmt])
    c_pct = c_count / max(len(cuervo_ig), 1) * 100
    c_er = cuervo_ig[cuervo_ig["post_type"] == fmt]["engagement_rate"].mean()
    l_count = len(leader_ig[leader_ig["post_type"] == fmt])
    l_pct = l_count / max(len(leader_ig), 1) * 100
    l_er = leader_ig[leader_ig["post_type"] == fmt]["engagement_rate"].mean()
    format_compare_rows.append({
        "Format": fmt,
        "Cuervo %": round(c_pct, 1),
        "Cuervo ER": round(c_er, 2) if pd.notna(c_er) else 0,
        "Leaders %": round(l_pct, 1),
        "Leaders ER": round(l_er, 2) if pd.notna(l_er) else 0,
    })

fc_df = pd.DataFrame(format_compare_rows)

col_fc1, col_fc2 = st.columns(2)
with col_fc1:
    st.markdown("**Format Mix: Cuervo vs Gen Z Leaders**")
    fc_melt = pd.melt(fc_df, id_vars=["Format"], value_vars=["Cuervo %", "Leaders %"],
                       var_name="Group", value_name="Pct")
    fig_fc = px.bar(fc_melt, x="Format", y="Pct", color="Group", barmode="group",
                    color_discrete_map={"Cuervo %": "#F8C090", "Leaders %": "#66BB6A"},
                    labels={"Pct": "% of IG Posts", "Format": ""},
                    template=CHART_TEMPLATE, text_auto=".0f")
    fig_fc.update_layout(font=CHART_FONT, height=380, legend=dict(orientation="h", y=-0.15))
    st.plotly_chart(fig_fc, width="stretch")

with col_fc2:
    st.markdown("**Avg ER by Format: Cuervo vs Gen Z Leaders**")
    fc_er_melt = pd.melt(fc_df, id_vars=["Format"], value_vars=["Cuervo ER", "Leaders ER"],
                          var_name="Group", value_name="ER")
    fig_fcer = px.bar(fc_er_melt, x="Format", y="ER", color="Group", barmode="group",
                      color_discrete_map={"Cuervo ER": "#F8C090", "Leaders ER": "#66BB6A"},
                      labels={"ER": "Avg ER %", "Format": ""},
                      template=CHART_TEMPLATE, text_auto=".2f")
    fig_fcer.update_layout(font=CHART_FONT, height=380, legend=dict(orientation="h", y=-0.15))
    st.plotly_chart(fig_fcer, width="stretch")

# Format KPI cards
reel_pct_now = len(cuervo_ig[cuervo_ig["post_type"] == "Reel"]) / max(len(cuervo_ig), 1) * 100
carousel_pct_now = len(cuervo_ig[cuervo_ig["post_type"] == "Carousel"]) / max(len(cuervo_ig), 1) * 100
leader_reel_pct = len(leader_ig[leader_ig["post_type"] == "Reel"]) / max(len(leader_ig), 1) * 100

fk1, fk2, fk3 = st.columns(3)
with fk1:
    st.metric("Cuervo Reel %", f"{reel_pct_now:.0f}%",
              delta=f"{reel_pct_now - leader_reel_pct:+.0f}% vs leaders",
              help="Target: 60%+ Reels for maximum reach")
with fk2:
    st.metric("Cuervo Carousel %", f"{carousel_pct_now:.0f}%",
              help="Carousels drive saves — aim for 20-25%")
with fk3:
    best_fmt_er = cuervo_ig.groupby("post_type")["engagement_rate"].mean()
    best_fmt_er = best_fmt_er[best_fmt_er > 0]
    best_fmt = best_fmt_er.idxmax() if len(best_fmt_er) else "N/A"
    best_val = best_fmt_er.max() if len(best_fmt_er) else 0
    st.metric("Best Format (ER)", best_fmt, delta=f"{best_val:.2f}%")

st.markdown("---")

# ── Posting Cadence Analysis ─────────────────────────────────────────

st.subheader("Posting Cadence Analysis")
st.caption("Optimal posting velocity by format — based on competitor benchmarks and engagement data")

cadence_rows = []
for brand in compare_brands:
    for plat in ["Instagram", "TikTok"]:
        by_type = results["frequency"].get(brand, {}).get(plat, {}).get("by_content_type", {})
        for fmt, count in by_type.items():
            cadence_rows.append({
                "Brand": brand,
                "Platform": plat,
                "Format": fmt,
                "Posts/Week": round(count / 4.3, 1),
            })

if cadence_rows:
    cadence_df = pd.DataFrame(cadence_rows)
    ig_cadence = cadence_df[cadence_df["Platform"] == "Instagram"]
    if len(ig_cadence):
        fig_cad = px.bar(ig_cadence, x="Brand", y="Posts/Week", color="Format",
                         barmode="stack",
                         color_discrete_sequence=["#F8C090", "#2ea3f2", "#7B6B63", "#D4956A"],
                         labels={"Posts/Week": "Posts / Week", "Brand": ""},
                         template=CHART_TEMPLATE, text_auto=".1f")
        fig_cad.update_layout(font=CHART_FONT, height=380, legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(fig_cad, width="stretch")

    cuervo_total_ppw = sum(
        results["frequency"].get(CUERVO, {}).get(p, {}).get("posts_per_week", 0)
        for p in ["Instagram", "TikTok"]
    )
    leader_total_ppw = sum(
        results["frequency"].get(b, {}).get(p, {}).get("posts_per_week", 0)
        for b in GEN_Z_LEADERS for p in ["Instagram", "TikTok"]
    ) / len(GEN_Z_LEADERS)

    rec_reels = max(3, round(leader_total_ppw * 0.6, 0))
    rec_carousels = max(1, round(leader_total_ppw * 0.2, 0))
    rec_static = max(1, round(leader_total_ppw * 0.15, 0))

    st.markdown("**Recommended Weekly Cadence (Instagram)**")
    rc1, rc2, rc3, rc4 = st.columns(4)
    with rc1:
        st.metric("Reels", f"{int(rec_reels)}/wk", help="60% of posts — maximize reach")
    with rc2:
        st.metric("Carousels", f"{int(rec_carousels)}/wk", help="20% of posts — drive saves")
    with rc3:
        st.metric("Static/Grid", f"{int(rec_static)}/wk", help="15% of posts — brand consistency")
    with rc4:
        st.metric("Stories", "3-5/day", help="Daily touchpoints — polls, BTS, product features")

st.markdown("---")

# ── Content gap analysis ──────────────────────────────────────────────

st.subheader("Content Gap Analysis: Cuervo vs Top Performers")

all_themes = sorted(df["content_theme"].dropna().unique())

cuervo_total = len(cuervo_df) or 1
leader_total = len(leader_df) or 1

gap_rows = []
for theme in all_themes:
    c_pct = len(cuervo_df[cuervo_df["content_theme"] == theme]) / cuervo_total * 100
    l_pct = len(leader_df[leader_df["content_theme"] == theme]) / leader_total * 100
    c_er = cuervo_df[cuervo_df["content_theme"] == theme]["engagement_rate"].mean()
    l_er = leader_df[leader_df["content_theme"] == theme]["engagement_rate"].mean()
    gap_rows.append({
        "theme": theme,
        "Cuervo %": round(c_pct, 1),
        "Leaders %": round(l_pct, 1),
        "gap": round(l_pct - c_pct, 1),
        "Cuervo ER": round(c_er, 2) if pd.notna(c_er) else 0,
        "Leader ER": round(l_er, 2) if pd.notna(l_er) else 0,
    })

gap_df = pd.DataFrame(gap_rows).sort_values("gap", ascending=False)

fig_gap = go.Figure()
fig_gap.add_trace(go.Bar(x=gap_df["theme"], y=gap_df["Cuervo %"],
                         name="Cuervo", marker_color=BRAND_COLORS["Jose Cuervo"]))
fig_gap.add_trace(go.Bar(x=gap_df["theme"], y=gap_df["Leaders %"],
                         name="Gen Z Leaders Avg", marker_color="#66BB6A"))
fig_gap.update_layout(barmode="group", template=CHART_TEMPLATE, font=CHART_FONT,
                      height=420, xaxis_tickangle=-35, yaxis_title="% of Content",
                      legend=dict(orientation="h", y=1.1))
st.plotly_chart(fig_gap, width="stretch")

st.markdown("**Biggest content gaps (themes leaders use more):**")
for _, row in gap_df.head(3).iterrows():
    if row["gap"] > 0:
        st.markdown(f"- **{row['theme']}**: Leaders at {row['Leaders %']}% vs Cuervo {row['Cuervo %']}% "
                    f"(+{row['gap']}% gap) — Leader ER: {row['Leader ER']}%")

# ── All recommendations ───────────────────────────────────────────────

st.markdown("---")
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
                    st.markdown(f"**Platform:** {r['platform']}")

# ── GOAT Content Pillars (Integration 1) ─────────────────────────────

st.markdown("---")
st.subheader("Content Pillars — GOAT Framework")
st.caption("Marg Mode content strategy: 4 pillars from the GOAT Agency Social Playbook Q1 2026. Charts show Cuervo's actual distribution vs GOAT targets.")

PILLARS = [
    {
        "name": "La Tradición",
        "icon": "🏛️",
        "target": 25,
        "quality": "Educational / Product",
        "objective": "Celebrate Cuervo's 250+ years of tequila craftsmanship, iconic heritage, and cultural legacy that shaped the margarita",
        "themes": GOAT_PILLAR_MAP["La Tradición"],
        "formats": "Carousels (educational), Reels (recipe), Grid posts",
        "tone": "Approachable expert — informative but not pretentious",
        "example": "3 margarita upgrades that'll change your summer",
    },
    {
        "name": "Cuervo Live",
        "icon": "🎤",
        "target": 15,
        "quality": "Experiential / Entertainment",
        "objective": "Front-row pass to cultural moments, events, and partnerships where Cuervo shows up and connects in real time",
        "themes": GOAT_PILLAR_MAP["Cuervo Live"],
        "formats": "Reels (event footage), Stories (live), Creator Reels",
        "tone": "Energetic, FOMO-inducing, real-time",
        "example": "Live from the Cuervo experience — who's here?",
    },
    {
        "name": "Life, with a Lime",
        "icon": "🍋",
        "target": 30,
        "quality": "Aspirational / Relatable",
        "objective": "Capture how Cuervo inspires everyday moments — from cocktails to culture — to feel bigger, brighter, and unmistakably more fun",
        "themes": GOAT_PILLAR_MAP["Life, with a Lime"],
        "formats": "Reels (lifestyle), Carousels (recipes), creative photography",
        "tone": "Aspirational but relatable, lifestyle over product",
        "example": "Sunsets taste better with Cuervo",
    },
    {
        "name": "Culture, Shaken",
        "icon": "🔥",
        "target": 30,
        "quality": "Entertainment / Timely",
        "objective": "Reactive, trend-driven content that taps into cultural conversations with Cuervo's Marg Mode energy",
        "themes": GOAT_PILLAR_MAP["Culture, Shaken"],
        "formats": "Reels (trending formats), memes, UGC reposts, duets",
        "tone": "Playful, quick-hitting, culturally plugged in",
        "example": "POV: You showed up with Cuervo and suddenly everyone loves you",
    },
]

for pillar in PILLARS:
    with st.expander(f"{pillar['icon']}  **{pillar['name']}** — {pillar['quality']} (Target: {pillar['target']}%)", expanded=False):
        st.markdown(f"**Objective:** {pillar['objective']}")
        st.markdown(f"**Target Themes:** {', '.join(pillar['themes'])}")
        st.markdown(f"**Recommended Formats:** {pillar['formats']}")
        st.markdown(f"**Tone:** {pillar['tone']}")
        st.markdown(f"**Example Post:** *\"{pillar['example']}\"*")

        matching = cuervo_df[cuervo_df["content_theme"].isin(pillar["themes"])]
        if len(matching):
            pct_of_cuervo = len(matching) / max(len(cuervo_df), 1) * 100
            avg_er_pillar = matching["engagement_rate"].mean()
            avg_er_pillar = 0 if pd.isna(avg_er_pillar) else avg_er_pillar
            delta = pct_of_cuervo - pillar["target"]
            pk1, pk2, pk3 = st.columns(3)
            with pk1:
                st.metric("% of Content", f"{pct_of_cuervo:.0f}%",
                          delta=f"{delta:+.0f}% vs {pillar['target']}% target")
            with pk2:
                st.metric("Posts in Pillar", f"{len(matching)}")
            with pk3:
                st.metric("Pillar ER", f"{avg_er_pillar:.2f}%")
        else:
            st.info("No Cuervo posts currently match this pillar's themes in the dataset.")

# Pillar distribution vs target chart
pillar_data = []
for pillar in PILLARS:
    matching = cuervo_df[cuervo_df["content_theme"].isin(pillar["themes"])]
    pct = len(matching) / max(len(cuervo_df), 1) * 100
    er = matching["engagement_rate"].mean() if len(matching) else 0
    er = 0 if pd.isna(er) else er
    pillar_data.append({
        "Pillar": pillar["name"],
        "Actual %": round(pct, 1),
        "Target %": pillar["target"],
        "Avg ER": round(er, 2),
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
                         yaxis_title="% of Content", legend=dict(orientation="h", y=-0.15),
                         barmode="group")
    st.plotly_chart(fig_pd, width="stretch")

with col_pd2:
    st.markdown("**Avg ER by Pillar**")
    fig_pe = px.bar(pillar_df, x="Pillar", y="Avg ER",
                    color="Pillar",
                    color_discrete_map=GOAT_PILLAR_COLORS,
                    labels={"Avg ER": "Avg ER %", "Pillar": ""},
                    template=CHART_TEMPLATE, text_auto=".2f")
    fig_pe.update_layout(showlegend=False, font=CHART_FONT, height=380)
    st.plotly_chart(fig_pe, width="stretch")

# ── 30-Day action plan ────────────────────────────────────────────────

st.markdown("---")
st.subheader("30-Day Action Plan for Cuervo")

rec_ppw = round(leader_avg_ppw, 0)
top_themes_for_leaders = leader_df.groupby("content_theme")["engagement_rate"].mean().nlargest(3)
ugc_score = compute_genz_scores(CUERVO)[0]

plan = [
    {
        "week": "Week 1",
        "focus": "Format Reset & Creator Pipeline",
        "actions": [
            f"Ramp posting to {int(rec_ppw)}+ posts/week (currently {cuervo_ppw:.0f}/wk)",
            f"Shift IG mix to 60%+ Reels (currently {compute_genz_scores(CUERVO)[3]:.0f}% video) — Reels drive reach, Carousels drive saves",
            "Build creator shortlist: 5 micro-creators (10K-100K) in Lifestyle, Comedy, and Food niches",
            "Audit current grid aesthetic — does it signal 'fun' at a glance?",
        ],
    },
    {
        "week": "Week 2",
        "focus": "Content Pillar Launch",
        "actions": [
            "Launch 'Party Starter' pillar: 2 Reels featuring Especial in social settings (house party, pregame)",
            "Launch 'Elevated Sips' pillar: 1 Carousel with cocktail recipe using Tradicional",
            "Test first meme-format Reel (POV/trending audio) — keep it native, not ad-like",
            f"Test top-performing themes from leaders: {', '.join(top_themes_for_leaders.index[:2])}",
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
            "Set ER target: close gap to category avg by 25% within 60 days",
            "Brief next month's cultural calendar content (holidays, events, trending moments)",
        ],
    },
]

for item in plan:
    with st.expander(f"**{item['week']}** — {item['focus']}"):
        for action in item["actions"]:
            st.markdown(f"- {action}")

# ── Threats & opportunities ───────────────────────────────────────────

st.markdown("---")
col_t, col_o = st.columns(2)

with col_t:
    st.error("**Competitive Threats**")
    brand_counts = df.groupby("brand").size()
    if len(brand_counts):
        highest_poster = brand_counts.idxmax()
        highest_post_count = brand_counts.max()
        cuervo_count = len(df[df["brand"] == CUERVO])
        st.markdown(f"- {highest_poster} leads with **{highest_post_count}** posts vs Cuervo's **{cuervo_count}** — losing share of voice")

    brand_ers = df.groupby("brand")["engagement_rate"].mean()
    if len(brand_ers):
        best_er_brand = brand_ers.idxmax()
        best_er_val = brand_ers.max()
        st.markdown(f"- {best_er_brand} dominates engagement at **{best_er_val:.2f}% ER**")

    if results["creators"]:
        highest_collab = max(results["creators"].items(), key=lambda x: x[1].get("collab_pct", 0))
        st.markdown(f"- {highest_collab[0]}'s creator collab rate ({highest_collab[1].get('collab_pct', 0):.0f}%) "
                    f"dwarfs Cuervo's ({cuervo_collab:.0f}%)")

with col_o:
    st.success("**Opportunities for Cuervo**")
    cuervo_theme_er = cuervo_df.groupby("content_theme")["engagement_rate"].mean() if len(cuervo_df) else pd.Series(dtype=float)
    cuervo_best_theme = cuervo_theme_er.idxmax() if len(cuervo_theme_er) else "N/A"
    cuervo_best_er = cuervo_theme_er.max() if len(cuervo_theme_er) else 0
    cat_theme_er = df.groupby("content_theme")["engagement_rate"].mean().get(cuervo_best_theme, 0) if cuervo_best_theme != "N/A" else 0
    if cuervo_best_er > cat_theme_er:
        st.markdown(f"- Cuervo's **{cuervo_best_theme}** content outperforms category avg "
                    f"({cuervo_best_er:.2f}% vs {cat_theme_er:.2f}%)")

    reel_pct_opp = len(cuervo_df[cuervo_df["post_type"] == "Reel"]) / max(len(cuervo_df[cuervo_df["platform"] == "Instagram"]), 1) * 100
    st.markdown(f"- Instagram Reels at only **{reel_pct_opp:.0f}%** of IG content — room to grow to 60%+")
    st.markdown(f"- Authenticity score ({ugc_score:.0f}% UGC-style) can be raised with creator partnerships")
    st.markdown("- Brand heritage (250+ yrs) is a unique differentiator vs newer brands (Casamigos, Teremana)")
    st.markdown("- RTD line (Playamar, Margarita cans) offers untapped content pillar for casual/outdoor occasions")
    st.markdown("- 'Fun signal' positioning aligns with Gen Z values — Cuervo doesn't need to be luxury, it needs to be the brand you bring")

# ── Content Mix Funnel (Integration 2) ────────────────────────────────

st.markdown("---")
st.subheader("Content Mix Funnel — Entertain / Educate / Connect / Convince")
st.caption("GOAT Playbook flags Cuervo's current funnel as **inverted** — too much Convince, not enough Entertain. Target: grab attention first, then guide to action.")

# Build a reverse lookup: theme → mix category
_theme_to_mix = {}
for cat, themes in CONTENT_MIX_MAP.items():
    for t in themes:
        _theme_to_mix[t] = cat

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
        cat = row["Category"]
        direction = "MORE" if row["Gap"] < 0 else ("LESS" if row["Gap"] > 5 else "ON TRACK")
        icon = "🔺" if direction == "MORE" else ("🔻" if direction == "LESS" else "✅")
        st.markdown(f"{icon} **{cat}**: {row['Actual %']:.0f}% actual / {row['Target %']}% target "
                    f"({row['Gap']:+.0f}%) — Post **{direction}**")
    st.markdown("")
    st.info("**Funnel logic**: Entertain grabs attention → Educate builds relevance → Connect fosters relationships → Convince drives action")

# ── Dynamic vs Static Performance (Integration 3) ────────────────────

st.markdown("---")
st.subheader("Dynamic vs Static Performance")
st.caption("GOAT benchmark: Dynamic (video) delivers 2.8% ER vs Static (image) 2.2% ER, with -26% lower CPM")

dynamic_types = ["Reel", "Video"]
static_types = ["Static Image", "Carousel"]

dyn_posts = cuervo_df[cuervo_df["post_type"].isin(dynamic_types)]
stat_posts = cuervo_df[cuervo_df["post_type"].isin(static_types)]

dyn_count = len(dyn_posts)
stat_count = len(stat_posts)
total_ds = dyn_count + stat_count or 1
dyn_pct = dyn_count / total_ds * 100
stat_pct = stat_count / total_ds * 100
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

# Compare across all brands
all_brand_ds_rows = []
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
    b_dyn_pct = len(b_dyn) / max(len(bdf), 1) * 100
    all_brand_ds_rows.append({"Brand": brand, "Dynamic ER": round(b_dyn_er, 2),
                              "Static ER": round(b_stat_er, 2), "Dynamic %": round(b_dyn_pct, 0)})

if all_brand_ds_rows:
    ds_df = pd.DataFrame(all_brand_ds_rows)
    ds_melt = pd.melt(ds_df, id_vars=["Brand"], value_vars=["Dynamic ER", "Static ER"],
                      var_name="Format", value_name="ER")
    fig_ds = px.bar(ds_melt, x="Brand", y="ER", color="Format", barmode="group",
                    color_discrete_map={"Dynamic ER": "#2ea3f2", "Static ER": "#C9A87E"},
                    labels={"ER": "Avg ER %", "Brand": ""},
                    template=CHART_TEMPLATE, text_auto=".2f")
    fig_ds.update_layout(font=CHART_FONT, height=380, legend=dict(orientation="h", y=-0.15))
    st.plotly_chart(fig_ds, width="stretch")

# ── Content Source Tracking (Integration 4) ──────────────────────────

st.markdown("---")
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
        icon = "✅" if abs(gap) < 10 else ("🔺" if gap < 0 else "🔻")
        st.markdown(f"{icon} **{row['Source']}**: {row['Actual %']:.0f}% actual / {row['Target %']}% target ({gap:+.0f}%)")
    st.markdown("")
    st.info("**GOAT strategy**: Creators & influencers are the primary content engine. Brand-owned content anchors the brand world. Events provide real-time cultural relevance.")

# ── Platform Cadence Scorecard (Integration 5) ───────────────────────

st.markdown("---")
st.subheader("Platform Cadence Scorecard")
st.caption("GOAT targets: Instagram 8-10 assets/month (2-3x/week), TikTok 12-16 assets/month (4-5x/week)")

cad1, cad2 = st.columns(2)
for plat, col in [("Instagram", cad1), ("TikTok", cad2)]:
    with col:
        freq = results["frequency"].get(CUERVO, {}).get(plat, {})
        actual_ppm = freq.get("total_posts_30d", 0)
        actual_ppw = freq.get("posts_per_week", 0)
        target = GOAT_CADENCE_TARGETS.get(plat, {})
        target_low = target.get("low", 0)
        target_high = target.get("high", 0)
        target_mid = (target_low + target_high) / 2

        on_track = target_low <= actual_ppm <= target_high
        status = "ON TRACK" if on_track else ("BELOW" if actual_ppm < target_low else "ABOVE")
        icon = "✅" if on_track else ("🔻" if actual_ppm < target_low else "🔺")

        st.markdown(f"### {plat} {icon}")
        st.metric(f"Posts/Month", f"{actual_ppm}",
                  delta=f"Target: {target_low}-{target_high}/mo",
                  delta_color="off")
        st.metric(f"Posts/Week", f"{actual_ppw:.1f}",
                  delta=f"Target: {target_low / 4.3:.1f}-{target_high / 4.3:.1f}/wk",
                  delta_color="off")
        st.markdown(f"**Status: {status}**")

# ══════════════════════════════════════════════════════════════════════
# AUTOSTRAT QUALITATIVE INTELLIGENCE
# ══════════════════════════════════════════════════════════════════════

st.markdown("---")

autostrat = st.session_state.get("autostrat", {})
_has_autostrat = has_autostrat_data(autostrat)

if _has_autostrat:
    st.header("Qualitative Intelligence")
    st.caption("Audience psychographics, strategic territories, and partnership opportunities from autostrat.ai reports")

    # ── 1. Winning Territories ────────────────────────────────────────
    all_htw = get_all_how_to_win(autostrat, exclude_reference=True)
    if all_htw:
        render_section_label("Winning Territories")
        st.caption("Strategic territories identified across all autostrat reports")

        all_territories = []
        for entry in all_htw:
            for territory in entry["how_to_win"].get("territories", []):
                is_dupe = any(territory[:40] == existing[:40] for existing in all_territories)
                if not is_dupe:
                    all_territories.append(territory)

        render_territory_cards(all_territories[:8])

        summaries = [(e, e["how_to_win"]["summary"]) for e in all_htw if e["how_to_win"].get("summary")]
        if summaries:
            with st.expander("Strategic Summaries by Report"):
                for entry, summary in summaries:
                    source = f"{entry['source_label']} — {entry['identifier']}"
                    st.markdown(f"**{source}:** *{summary}*")

        all_verbatims = []
        for entry in all_htw:
            all_verbatims.extend(entry["how_to_win"].get("audience_verbatims", []))
        if all_verbatims:
            unique_verbatims = list(dict.fromkeys(all_verbatims))
            with st.expander(f"Audience Verbatims ({len(unique_verbatims)})"):
                render_verbatim_quotes(unique_verbatims, max_quotes=10)

        st.markdown("---")

    # ── 2. Audience Psychographics (NOPD) ─────────────────────────────
    all_profiles = get_all_audience_profiles(autostrat, exclude_reference=True)
    if all_profiles:
        render_section_label("Audience Psychographics")
        st.caption("NOPD profiles from autostrat reports — understand who Cuervo needs to reach")

        identifiers = list(dict.fromkeys(p["identifier"] for p in all_profiles))
        identifier_labels = {ident: ident.replace("_", " ").title() for ident in identifiers}

        selected = st.selectbox("Select audience profile", identifiers,
                                format_func=lambda x: identifier_labels[x],
                                key="cuervo_nopd_profile")

        matching = [p for p in all_profiles if p["identifier"] == selected]
        if matching:
            ap = matching[0]["audience_profile"]
            if ap.get("summary"):
                st.markdown(ap["summary"])
            render_nopd_cards(ap)

        st.markdown("---")

    # ── 3. Content Trends ─────────────────────────────────────────────
    all_trends = get_all_content_trends(autostrat)
    if all_trends:
        render_section_label("Content Trends")
        st.caption("Trending content formats and themes from conversation analysis")

        cols = st.columns(2)
        for i, trend in enumerate(all_trends[:6]):
            with cols[i % 2]:
                render_narrative_card(
                    trend.get("trend", f"Trend {i+1}"),
                    trend.get("description", ""),
                    accent_color="#F8C090",
                )

        st.markdown("---")

    # ── 4. Creator Archetypes ─────────────────────────────────────────
    all_archetypes = get_all_creator_archetypes(autostrat)
    if all_archetypes:
        render_section_label("Creator Archetypes to Target")
        st.caption("Types of creators performing well in relevant conversation spaces")

        arch_cols = st.columns(min(len(all_archetypes), 3))
        for i, arch in enumerate(all_archetypes[:6]):
            with arch_cols[i % len(arch_cols)]:
                render_creator_archetype(arch)

        st.markdown("---")

    # ── 5. Strategic Opportunities & Risks ────────────────────────────
    all_actions = get_all_strategic_actions(autostrat)
    if all_actions:
        render_section_label("Strategic Opportunities & Risks")

        all_opps = []
        all_gaps = []
        all_strategic = []
        for entry in all_actions:
            all_opps.extend(entry.get("opportunities", []))
            all_gaps.extend(entry.get("gaps_risks_unmet_needs", []))
            all_strategic.extend(entry.get("strategic_actions", []))

        col_op, col_gap = st.columns(2)
        with col_op:
            if all_opps:
                st.markdown("**Opportunities**")
                for opp in all_opps[:5]:
                    st.success(opp)
        with col_gap:
            if all_gaps:
                st.markdown("**Gaps, Risks & Unmet Needs**")
                for gap in all_gaps[:5]:
                    st.error(gap)

        if all_strategic:
            with st.expander(f"Strategic Actions ({len(all_strategic)})"):
                for i, action in enumerate(all_strategic[:8], 1):
                    st.markdown(f"**{i}.** {action}")

        st.markdown("---")

    # ── 6. Partnership Opportunities ──────────────────────────────────
    all_suggestions = get_all_sponsorship_suggestions(autostrat, exclude_reference=True)
    if all_suggestions:
        render_section_label("Partnership Opportunities")
        st.caption("Sponsorship and partnership recommendations from profile analysis")

        for entry in all_suggestions:
            source = f"{entry['source_label']} — {entry['identifier'].replace('_', ' ').title()}"
            st.markdown(f"**From: {source}**")
            sug_cols = st.columns(min(len(entry["suggestions"]), 2))
            for i, sug in enumerate(entry["suggestions"]):
                with sug_cols[i % len(sug_cols)]:
                    render_sponsorship_card(sug)
            st.markdown("")

else:
    st.info("No autostrat qualitative intelligence loaded. Import autostrat PDF reports from the home page to enrich this strategy view with audience psychographics, winning territories, and partnership opportunities.")
