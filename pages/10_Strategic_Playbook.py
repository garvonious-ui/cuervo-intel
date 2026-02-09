"""
Page 10: Strategic Playbook — How Cuervo Wins.
Consolidates "How to Win" territories, strategic actions, and sponsorship opportunities
from all autostrat reports.
"""

import streamlit as st

from config import CUSTOM_CSS
from autostrat_loader import (
    get_all_how_to_win, get_all_strategic_actions, get_all_brand_mentions,
    get_all_sponsorship_suggestions, has_autostrat_data,
)
from autostrat_components import (
    render_territory_cards, render_verbatim_quotes, render_section_label,
    render_sponsorship_card, render_brand_mention,
)

st.logo("logo.png")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
st.header("Strategic Playbook")
st.caption("Consolidated strategic intelligence from all autostrat reports")

if "autostrat" not in st.session_state:
    st.warning("Go to the home page first to load data.")
    st.stop()

autostrat = st.session_state["autostrat"]
if not has_autostrat_data(autostrat):
    st.info("No autostrat reports loaded. Import PDFs from the home page.")
    st.stop()

# ── Winning Territories ──────────────────────────────────────────────

all_htw = get_all_how_to_win(autostrat)
if all_htw:
    render_section_label("Winning Territories")
    st.caption("Strategic territories identified across all reports")

    # Consolidate unique territories
    all_territories = []
    territory_sources = {}
    for entry in all_htw:
        for territory in entry["how_to_win"].get("territories", []):
            # Simple dedup by checking if territory is substantially different
            is_dupe = False
            for existing in all_territories:
                if territory[:40] == existing[:40]:
                    is_dupe = True
                    break
            if not is_dupe:
                all_territories.append(territory)
                territory_sources[territory] = (
                    f"{entry['source_label']} — {entry['identifier']}"
                )

    render_territory_cards(all_territories[:10])

    # ── Summaries ────────────────────────────────────────────────────
    summaries = [e["how_to_win"]["summary"] for e in all_htw
                 if e["how_to_win"].get("summary")]
    if summaries:
        with st.expander("Strategic Summaries (from each report)"):
            for i, (entry, summary) in enumerate(
                    [(e, e["how_to_win"]["summary"]) for e in all_htw
                     if e["how_to_win"].get("summary")]):
                source = f"{entry['source_label']} — {entry['identifier']}"
                st.markdown(f"**{source}:**")
                st.markdown(f"*{summary}*")
                if i < len(summaries) - 1:
                    st.markdown("---")

    st.markdown("---")

# ── Audience Verbatims ───────────────────────────────────────────────

all_verbatims = []
for entry in all_htw:
    all_verbatims.extend(entry["how_to_win"].get("audience_verbatims", []))

if all_verbatims:
    render_section_label("Audience Verbatims")
    st.caption("Real audience quotes from across all reports")
    # Deduplicate
    unique_verbatims = list(dict.fromkeys(all_verbatims))
    render_verbatim_quotes(unique_verbatims, max_quotes=12)
    st.markdown("---")

# ── Opportunities vs. Gaps/Risks ─────────────────────────────────────

all_actions = get_all_strategic_actions(autostrat)
if all_actions:
    render_section_label("Opportunities vs. Gaps & Risks")

    all_opps = []
    all_gaps = []
    all_strategic = []
    for entry in all_actions:
        all_opps.extend(entry.get("opportunities", []))
        all_gaps.extend(entry.get("gaps_risks_unmet_needs", []))
        all_strategic.extend(entry.get("strategic_actions", []))

    col1, col2 = st.columns(2)
    with col1:
        if all_opps:
            st.markdown("**Opportunities**")
            for opp in all_opps[:6]:
                st.success(opp)
    with col2:
        if all_gaps:
            st.markdown("**Gaps, Risks & Unmet Needs**")
            for gap in all_gaps[:6]:
                st.error(gap)

    # ── Strategic Actions ────────────────────────────────────────────
    if all_strategic:
        st.markdown("---")
        render_section_label("Strategic Actions")
        for i, action in enumerate(all_strategic[:8], 1):
            st.markdown(f"**{i}.** {action}")

    st.markdown("---")

# ── Sponsorship Playbook ─────────────────────────────────────────────

all_suggestions = get_all_sponsorship_suggestions(autostrat)
if all_suggestions:
    render_section_label("Sponsorship Playbook")
    st.caption("Future partnership opportunities from profile reports")

    for entry in all_suggestions:
        source = f"{entry['source_label']} — {entry['identifier']}"
        st.markdown(f"**From: {source}**")
        cols = st.columns(min(len(entry["suggestions"]), 2))
        for i, sug in enumerate(entry["suggestions"]):
            with cols[i % len(cols)]:
                render_sponsorship_card(sug)
        st.markdown("")

    st.markdown("---")

# ── Competitive Brand Mentions ───────────────────────────────────────

all_mentions = get_all_brand_mentions(autostrat)
if all_mentions:
    render_section_label("Competitive Brand Mentions")
    st.caption("How brands appear in the conversation space")
    for mention in all_mentions[:8]:
        render_brand_mention(mention)
