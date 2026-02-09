"""
Page 11: Profile Deep Dive — Per-brand intelligence from autostrat profile reports.
"""

import streamlit as st
import plotly.graph_objects as go

from config import CUSTOM_CSS, CHART_TEMPLATE, CHART_FONT, BRAND_COLORS
from autostrat_loader import (
    PROFILE_TYPES, REPORT_TYPE_LABELS, get_available_identifiers, get_report,
    get_section_across_reports,
)
from autostrat_components import (
    render_nopd_cards, render_hits_misses, render_territory_cards,
    render_verbatim_quotes, render_section_label, render_sponsorship_card,
    render_narrative_card,
)

st.logo("logo.png")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
st.header("Profile Deep Dive")

if "autostrat" not in st.session_state:
    st.warning("Go to the home page first to load data.")
    st.stop()

autostrat = st.session_state["autostrat"]

# ── Selectors ────────────────────────────────────────────────────────

platform = st.radio("Platform", ["Instagram", "TikTok"], horizontal=True)
report_type = "instagram_profiles" if platform == "Instagram" else "tiktok_profiles"
identifiers = get_available_identifiers(autostrat, report_type)

if not identifiers:
    st.info(f"No {platform} profile reports available. Import autostrat PDFs from the home page.")
    st.stop()

selected = st.selectbox("Select profile", identifiers,
                         format_func=lambda x: x.replace("_", " ").title())
report = get_report(autostrat, report_type, selected)

if not report:
    st.warning("Report not found.")
    st.stop()

display_name = selected.replace("_", " ").title()

# ── Snapshot KPIs ────────────────────────────────────────────────────

snapshot = report.get("snapshot", {})
if any(snapshot.values()):
    render_section_label("Profile Snapshot")
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric("Followers", f"{snapshot.get('followers', 0):,}")
    with c2:
        st.metric("Following", f"{snapshot.get('following', 0):,}")
    with c3:
        st.metric("Avg Likes", f"{snapshot.get('avg_likes', 0):,}")
    with c4:
        st.metric("Avg Comments", f"{snapshot.get('avg_comments', 0):,}")
    with c5:
        er = snapshot.get("avg_engagement_rate", 0)
        st.metric("Avg ER", f"{er}%")
    st.markdown("---")

# ── Creator Summary ──────────────────────────────────────────────────

cs = report.get("creator_summary", {})
if cs.get("topline"):
    render_section_label("Creator Summary")
    st.markdown(f"**{display_name}** — {cs['topline']}")

    if cs.get("what_it_means"):
        st.markdown(f"*{cs['what_it_means']}*")

    if cs.get("common_themes"):
        themes_str = " | ".join(cs["common_themes"])
        st.caption(f"Common themes: {themes_str}")

    if cs.get("what_hits") or cs.get("what_misses"):
        render_hits_misses(cs.get("what_hits", ""), cs.get("what_misses", ""))

    st.markdown("---")

# ── Audience Profile (NOPD) ──────────────────────────────────────────

ap = report.get("audience_profile", {})
if any(ap.get(k) for k in ["needs", "objections", "desires", "pain_points"]):
    render_section_label("Audience Profile")
    if ap.get("summary"):
        st.markdown(ap["summary"])
    render_nopd_cards(ap)
    st.markdown("---")

# ── Statistics Chart ─────────────────────────────────────────────────

stats = report.get("statistics", {})
all_posts = stats.get("all_posts", {})
if any(all_posts.values()):
    render_section_label("Performance Statistics")

    metrics = ["views", "likes", "comments"]
    stat_types = ["min", "max", "median", "avg"]
    colors = {"min": "#A3C4D9", "max": "#D9534F", "median": "#F8C090", "avg": "#2ea3f2"}

    fig = go.Figure()
    for stat in stat_types:
        values = [all_posts.get(f"{stat}_{m}", 0) for m in metrics]
        fig.add_trace(go.Bar(
            name=stat.capitalize(), x=metrics,
            y=values, marker_color=colors[stat],
            text=[f"{v:,.0f}" for v in values], textposition="outside",
        ))

    fig.update_layout(
        barmode="group", template=CHART_TEMPLATE, font=CHART_FONT,
        height=380, yaxis_title="Count",
        legend=dict(orientation="h", y=1.12),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

# ── Top & Bottom Posts ───────────────────────────────────────────────

top_posts = report.get("top_posts", {})
if top_posts:
    render_section_label("Top & Bottom Posts")
    cols = st.columns(min(len(top_posts), 3))
    labels = {
        "most_liked": "Most Liked",
        "most_engaged": "Most Engaged",
        "least_engaged": "Least Engaged",
        "least_liked": "Least Liked",
        "most_comments": "Most Comments",
    }
    for i, (key, post) in enumerate(top_posts.items()):
        with cols[i % len(cols)]:
            label = labels.get(key, key.replace("_", " ").title())
            caption = post.get("caption", "N/A")[:120]
            er = post.get("engagement_rate", 0)
            likes = post.get("likes", 0)
            comments = post.get("comments", 0)
            link = post.get("link", "")

            st.markdown(f"**{label}**")
            st.markdown(f'"{caption}..."')
            st.caption(f"ER: {er}% | Likes: {likes:,} | Comments: {comments:,}")
            if link:
                st.markdown(f"[View post]({link})")
    st.markdown("---")

# ── Posting & Engagement Analysis ────────────────────────────────────

ea = report.get("engagement_analysis", {})
pa = report.get("posting_analysis", {})
if ea.get("summary") or pa.get("summary"):
    render_section_label("Engagement & Posting Analysis")
    col1, col2 = st.columns(2)
    with col1:
        if ea.get("summary"):
            render_narrative_card("Engagement Analysis", ea["summary"])
    with col2:
        if pa.get("summary"):
            render_narrative_card("Posting Analysis", pa["summary"])
    st.markdown("---")

# ── Sponsorship Intelligence ─────────────────────────────────────────

sponsorships = report.get("sponsorships", {})
if sponsorships.get("summary") or sponsorships.get("categories"):
    render_section_label("Sponsorship Intelligence")
    if sponsorships.get("summary"):
        st.markdown(sponsorships["summary"])

    col1, col2 = st.columns(2)
    with col1:
        if sponsorships.get("categories"):
            st.markdown("**Current Categories:** " + ", ".join(sponsorships["categories"]))
    with col2:
        if sponsorships.get("companies"):
            st.markdown("**Current Partners:** " + ", ".join(sponsorships["companies"]))

    if sponsorships.get("integration_summary"):
        st.caption(sponsorships["integration_summary"])

# ── Future Sponsorship Suggestions ───────────────────────────────────

suggestions = report.get("future_sponsorship_suggestions", [])
if suggestions:
    st.markdown("---")
    render_section_label("Future Sponsorship Opportunities")
    cols = st.columns(min(len(suggestions), 2))
    for i, sug in enumerate(suggestions):
        with cols[i % len(cols)]:
            render_sponsorship_card(sug)

# ── How to Win ───────────────────────────────────────────────────────

hw = report.get("how_to_win", {})
if hw.get("territories"):
    st.markdown("---")
    render_section_label("How to Win")
    if hw.get("summary"):
        st.markdown(f"*{hw['summary']}*")
    render_territory_cards(hw["territories"])

    if hw.get("audience_verbatims"):
        render_section_label("Audience Verbatims")
        render_verbatim_quotes(hw["audience_verbatims"])

# ── Cross-Brand Snapshot Comparison ──────────────────────────────────

all_snapshots = get_section_across_reports(autostrat, report_type, "snapshot")
if len(all_snapshots) > 1:
    st.markdown("---")
    render_section_label(f"Cross-Profile Comparison ({platform})")

    import pandas as pd
    rows = []
    for ident, snap in all_snapshots.items():
        rows.append({
            "Profile": ident.replace("_", " ").title(),
            "Followers": snap.get("followers", 0),
            "Avg Likes": snap.get("avg_likes", 0),
            "Avg Comments": snap.get("avg_comments", 0),
            "Avg ER %": snap.get("avg_engagement_rate", 0),
        })
    comp_df = pd.DataFrame(rows)
    st.dataframe(comp_df, hide_index=True, use_container_width=True)
