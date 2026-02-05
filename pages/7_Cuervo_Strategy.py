import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from config import BRAND_COLORS, CHART_TEMPLATE, CHART_FONT, BRAND_ORDER, PRIORITY_COLORS

st.header("Cuervo Gen Z Strategy Hub")
st.caption("Actionable insights for Jose Cuervo targeting Gen Z (21-24)")

if "results" not in st.session_state:
    st.warning("Go to the home page first to load data.")
    st.stop()

results = st.session_state["results"]
df = st.session_state["df"]  # Use unfiltered data for strategy comparisons

CUERVO = "Jose Cuervo"
GEN_Z_LEADERS = ["Casamigos", "Teremana"]  # Highest ER / creator-forward brands

# ── Performance vs Gen Z leaders ──────────────────────────────────────

st.subheader("Cuervo vs Gen Z Leaders")

compare_brands = [CUERVO] + GEN_Z_LEADERS

c1, c2, c3, c4 = st.columns(4)

def brand_metric(brand, col):
    bdf = df[df["brand"] == brand]
    er = bdf["engagement_rate"].mean()
    cr = results["creators"].get(brand, {})
    freq = results["frequency"].get(brand, {})
    ppw = sum(freq.get(p, {}).get("posts_per_week", 0) for p in ["Instagram", "TikTok"])
    return er, cr.get("collab_pct", 0), ppw

cuervo_er, cuervo_collab, cuervo_ppw = brand_metric(CUERVO, c1)

for brand in GEN_Z_LEADERS:
    er, collab, ppw = brand_metric(brand, None)

# Show deltas
leader_avg_er = df[df["brand"].isin(GEN_Z_LEADERS)]["engagement_rate"].mean()
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
    # Authenticity = % UGC-style or Lo-fi content
    ugc_pct = len(bdf[bdf["visual_style"].isin(["Raw / UGC-style", "Lo-fi / Authentic"])]) / total * 100
    # Creator partnerships
    collab_pct = results["creators"].get(brand, {}).get("collab_pct", 0)
    # Humor/meme
    humor_pct = len(bdf[bdf["content_theme"].isin(["Meme / Humor"])]) / total * 100
    # Short-form video
    video_pct = len(bdf[bdf["post_type"].isin(["Reel", "Video"])]) / total * 100
    # Music integration
    music_pct = len(bdf[bdf["has_music_audio"].str.lower() == "yes"]) / total * 100 if "has_music_audio" in bdf.columns else 0
    # Community engagement (avg comment rate)
    comment_rate = (bdf["comments"].sum() / max(bdf["likes"].sum(), 1)) * 100

    return [ugc_pct, collab_pct, humor_pct, video_pct, music_pct, comment_rate]

dims = ["Authenticity\n(UGC %)", "Creator\nPartners %", "Humor/Meme\n%",
        "Short-form\nVideo %", "Music\nIntegration %", "Community\nEngagement"]

fig_radar = go.Figure()
for brand in compare_brands:
    scores = compute_genz_scores(brand)
    fig_radar.add_trace(go.Scatterpolar(
        r=scores + [scores[0]], theta=dims + [dims[0]],
        fill="toself", name=brand, opacity=0.55,
        line=dict(color=BRAND_COLORS.get(brand, "#888"), width=2),
    ))

fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
    height=480, template=CHART_TEMPLATE, font=CHART_FONT,
    legend=dict(orientation="h", y=-0.12),
)
st.plotly_chart(fig_radar, use_container_width=True)

# ── Content gap analysis ──────────────────────────────────────────────

st.subheader("Content Gap Analysis: Cuervo vs Top Performers")

all_themes = sorted(df["content_theme"].dropna().unique())

cuervo_df = df[df["brand"] == CUERVO]
leader_df = df[df["brand"].isin(GEN_Z_LEADERS)]
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
st.plotly_chart(fig_gap, use_container_width=True)

# Highlight biggest gaps
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

# ── 30-Day action plan ────────────────────────────────────────────────

st.markdown("---")
st.subheader("30-Day Action Plan for Cuervo")

# Compute recommended actions from data
rec_ppw = round(leader_avg_ppw, 0)
top_themes_for_leaders = leader_df.groupby("content_theme")["engagement_rate"].mean().nlargest(3)
ugc_score = compute_genz_scores(CUERVO)[0]

plan = [
    {
        "week": "Week 1",
        "focus": "Increase Velocity & Creator Outreach",
        "actions": [
            f"Ramp posting to {int(rec_ppw)}+ posts/week (currently {cuervo_ppw:.0f}/wk)",
            "Reach out to 5 micro-creators (10K-100K) in Lifestyle, Comedy, and Food categories",
            "Test 2 Meme/Humor format posts on TikTok",
        ],
    },
    {
        "week": "Week 2",
        "focus": "Content Mix Optimization",
        "actions": [
            f"Shift to 60%+ Reels/Video (currently {compute_genz_scores(CUERVO)[3]:.0f}%)",
            "Launch first creator collab series — raw/UGC-style",
            f"Test top-performing themes from leaders: {', '.join(top_themes_for_leaders.index[:2])}",
        ],
    },
    {
        "week": "Week 3",
        "focus": "Engagement & Community",
        "actions": [
            "Add 'Tag a friend' and 'Comment below' CTAs to every post",
            "Repost 2-3 pieces of UGC from followers",
            "Use trending audio on 80%+ of Reels/TikToks",
        ],
    },
    {
        "week": "Week 4",
        "focus": "Measure & Double Down",
        "actions": [
            "Analyze Week 1-3 performance — identify top 3 posts by ER",
            "Double down on winning formats and themes",
            "Set ER target: close gap to category avg by 25%",
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
    # Compute dynamic threats
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
    # Compute dynamic opportunities
    cuervo_theme_er = cuervo_df.groupby("content_theme")["engagement_rate"].mean() if len(cuervo_df) else pd.Series(dtype=float)
    cuervo_best_theme = cuervo_theme_er.idxmax() if len(cuervo_theme_er) else "N/A"
    cuervo_best_er = cuervo_theme_er.max() if len(cuervo_theme_er) else 0
    cat_theme_er = df.groupby("content_theme")["engagement_rate"].mean().get(cuervo_best_theme, 0) if cuervo_best_theme != "N/A" else 0
    if cuervo_best_er > cat_theme_er:
        st.markdown(f"- Cuervo's **{cuervo_best_theme}** content outperforms category avg "
                    f"({cuervo_best_er:.2f}% vs {cat_theme_er:.2f}%)")

    reel_pct = len(cuervo_df[cuervo_df["post_type"] == "Reel"]) / max(len(cuervo_df[cuervo_df["platform"] == "Instagram"]), 1) * 100
    st.markdown(f"- Instagram Reels at only **{reel_pct:.0f}%** of IG content — room to grow to 60%+")
    st.markdown(f"- Authenticity score ({ugc_score:.0f}% UGC-style) can be raised with creator partnerships")
    st.markdown(f"- Brand heritage is a unique differentiator vs newer brands (Casamigos, Teremana)")
