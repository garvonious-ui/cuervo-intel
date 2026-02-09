"""
Page 9: Conversation & Trends — Hashtag/keyword analysis, content trends,
creator archetypes, brand mentions, and news intelligence.
"""

import streamlit as st

from config import CUSTOM_CSS
from autostrat_loader import (
    CONVERSATION_TYPES, REPORT_TYPE_LABELS, has_autostrat_data,
    get_available_identifiers, get_report,
)
from autostrat_components import (
    render_section_label, render_narrative_card, render_creator_archetype,
    render_brand_mention, render_verbatim_quotes, render_territory_cards,
    render_nopd_cards,
)

st.logo("logo.png")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
st.header("Conversation & Trends")

if "autostrat" not in st.session_state:
    st.warning("Go to the home page first to load data.")
    st.stop()

autostrat = st.session_state["autostrat"]
if not has_autostrat_data(autostrat):
    st.info("No autostrat reports loaded. Import PDFs from the home page.")
    st.stop()

# ── Report Selector ──────────────────────────────────────────────────

# Build list of available conversation/trend reports
available = []
for rt in CONVERSATION_TYPES + ["google_news"]:
    for ident in get_available_identifiers(autostrat, rt):
        available.append((rt, ident))

if not available:
    st.info("No hashtag, keyword, or news reports available. Import autostrat PDFs.")
    st.stop()

# Create display labels
options = {f"{REPORT_TYPE_LABELS.get(rt, rt)}: {ident.replace('_', ' ').title()}": (rt, ident)
           for rt, ident in available}

selected_label = st.selectbox("Select report", list(options.keys()))
report_type, identifier = options[selected_label]
report = get_report(autostrat, report_type, identifier)

if not report:
    st.warning("Report not found.")
    st.stop()

# ── Executive Summary ────────────────────────────────────────────────

es = report.get("executive_summary", {})
if es.get("overview") or es.get("key_insights"):
    render_section_label("Executive Summary")

    if es.get("search_term"):
        st.markdown(f"**Search:** {es['search_term']}")
    if es.get("search_purpose"):
        st.caption(es["search_purpose"])

    if es.get("key_insights"):
        cols = st.columns(min(len(es["key_insights"]), 2))
        for i, insight in enumerate(es["key_insights"][:4]):
            with cols[i % len(cols)]:
                render_narrative_card(f"Insight {i+1}", insight)

    st.markdown("---")

# ── Audience Profile ─────────────────────────────────────────────────

ap = report.get("audience_profile", {})
if any(ap.get(k) for k in ["needs", "objections", "desires", "pain_points"]):
    render_section_label("Audience Profile")
    if ap.get("summary"):
        st.markdown(ap["summary"])
    render_nopd_cards(ap)
    st.markdown("---")

# ── Hashtag Analysis ─────────────────────────────────────────────────

ha = report.get("hashtag_analysis", {})
if ha:
    if ha.get("summary"):
        render_section_label("Hashtag Analysis")
        st.markdown(ha["summary"])

    # Key Findings & Opportunities
    findings = ha.get("key_findings", [])
    opportunities = ha.get("opportunities", [])
    if findings or opportunities:
        col1, col2 = st.columns(2)
        with col1:
            if findings:
                st.markdown("**Key Findings**")
                for f in findings:
                    st.info(f)
        with col2:
            if opportunities:
                st.markdown("**Opportunities**")
                for o in opportunities:
                    st.success(o)

    # Gaps & Strategic Actions
    gaps = ha.get("gaps_risks_unmet_needs", [])
    actions = ha.get("strategic_actions", [])
    if gaps or actions:
        col1, col2 = st.columns(2)
        with col1:
            if gaps:
                st.markdown("**Gaps, Risks & Unmet Needs**")
                for g in gaps:
                    st.error(g)
        with col2:
            if actions:
                st.markdown("**Strategic Actions**")
                for a in actions:
                    st.markdown(f"- {a}")

    if ha:
        st.markdown("---")

# ── Conversation Map ─────────────────────────────────────────────────

cm = report.get("conversation_map", {})
if cm.get("summary") or cm.get("overarching_patterns"):
    render_section_label("Conversation Map")

    if cm.get("summary"):
        st.markdown(cm["summary"])

    if cm.get("relationship_analysis"):
        with st.expander("Relationship Analysis"):
            st.markdown(cm["relationship_analysis"])

    if cm.get("overarching_patterns"):
        st.markdown("**Overarching Patterns:**")
        for pattern in cm["overarching_patterns"]:
            st.markdown(f"- {pattern}")

    if cm.get("action_opportunities"):
        st.markdown("**Action Opportunities:**")
        for opp in cm["action_opportunities"]:
            st.success(opp)

    st.markdown("---")

# ── Interesting Conversations ────────────────────────────────────────

convos = report.get("interesting_conversations", [])
if convos:
    render_section_label("Interesting Conversations")
    cols = st.columns(min(len(convos), 2))
    for i, convo in enumerate(convos):
        with cols[i % len(cols)]:
            render_narrative_card(
                convo.get("title", f"Conversation {i+1}"),
                convo.get("description", ""),
            )
    st.markdown("---")

# ── Content Trends ───────────────────────────────────────────────────

trends = report.get("content_trends", [])
if trends:
    render_section_label("Content Trends")
    cols = st.columns(min(len(trends), 2))
    for i, trend in enumerate(trends):
        with cols[i % len(cols)]:
            render_narrative_card(
                trend.get("trend", f"Trend {i+1}"),
                trend.get("description", ""),
                accent_color="#F8C090",
            )
    st.markdown("---")

# ── Creator Archetypes ───────────────────────────────────────────────

archetypes = report.get("creator_archetypes", [])
if archetypes:
    render_section_label("Creator Archetypes")
    cols = st.columns(min(len(archetypes), 3))
    for i, arch in enumerate(archetypes):
        with cols[i % len(cols)]:
            render_creator_archetype(arch)
    st.markdown("---")

# ── Brand Mentions ───────────────────────────────────────────────────

mentions = report.get("brand_mentions", [])
if mentions:
    render_section_label("Brand Mentions")
    for mention in mentions:
        render_brand_mention(mention)
    st.markdown("---")

# ── In-Market Campaigns ─────────────────────────────────────────────

campaigns = report.get("in_market_campaigns", [])
if campaigns:
    render_section_label("In-Market Campaigns")
    cols = st.columns(min(len(campaigns), 3))
    for i, campaign in enumerate(campaigns):
        with cols[i % len(cols)]:
            render_narrative_card(
                campaign.get("campaign", f"Campaign {i+1}"),
                campaign.get("description", ""),
                accent_color="#5CB85C",
            )
    st.markdown("---")

# ── How to Win ───────────────────────────────────────────────────────

hw = report.get("how_to_win", {})
if hw.get("territories"):
    render_section_label("How to Win")
    if hw.get("summary"):
        st.markdown(f"*{hw['summary']}*")
    render_territory_cards(hw["territories"])

    if hw.get("audience_verbatims"):
        render_section_label("Audience Verbatims")
        render_verbatim_quotes(hw["audience_verbatims"])
