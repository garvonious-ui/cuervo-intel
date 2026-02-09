"""
Page 8: Audience Intelligence — Psychographic profiles and sentiment across brands.
"""

import streamlit as st

from config import CUSTOM_CSS
from autostrat_loader import (
    get_all_audience_profiles, get_all_brand_mentions, has_autostrat_data,
    REPORT_TYPE_LABELS,
)
from autostrat_components import (
    render_nopd_cards, render_section_label, render_brand_mention,
    sentiment_badge_html,
)

st.logo("logo.png")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
st.header("Audience Intelligence")

if "autostrat" not in st.session_state:
    st.warning("Go to the home page first to load data.")
    st.stop()

autostrat = st.session_state["autostrat"]
if not has_autostrat_data(autostrat):
    st.info("No autostrat reports loaded. Import PDFs from the home page.")
    st.stop()

# ── Collect audience profiles ────────────────────────────────────────

all_profiles = get_all_audience_profiles(autostrat)
if not all_profiles:
    st.info("No audience profile data found in loaded reports.")
    st.stop()

# Build list of unique identifiers
identifiers = list(dict.fromkeys(p["identifier"] for p in all_profiles))
identifier_labels = {ident: ident.replace("_", " ").title() for ident in identifiers}

# ── View Mode ────────────────────────────────────────────────────────

view = st.radio("View", ["Single Profile", "Comparison"], horizontal=True)

if view == "Single Profile":
    # ── Single Profile Deep Dive ─────────────────────────────────────
    selected = st.selectbox("Select profile/topic", identifiers,
                            format_func=lambda x: identifier_labels[x])

    matching = [p for p in all_profiles if p["identifier"] == selected]

    if len(matching) > 1:
        tabs = st.tabs([p["source_label"] for p in matching])
        for tab, profile_entry in zip(tabs, matching):
            with tab:
                ap = profile_entry["audience_profile"]
                if ap.get("summary"):
                    st.markdown(ap["summary"])
                render_nopd_cards(ap)
    elif matching:
        ap = matching[0]["audience_profile"]
        st.caption(f"Source: {matching[0]['source_label']}")
        if ap.get("summary"):
            st.markdown(ap["summary"])
        render_nopd_cards(ap)

else:
    # ── Comparison View ──────────────────────────────────────────────
    st.caption("Compare audience profiles across reports side by side")

    # Let user pick which profiles to compare
    selected_ids = st.multiselect(
        "Select profiles to compare", identifiers,
        default=identifiers[:min(4, len(identifiers))],
        format_func=lambda x: identifier_labels[x],
    )

    if not selected_ids:
        st.info("Select at least one profile to compare.")
        st.stop()

    # For each selected identifier, take the first available profile
    profiles_to_compare = []
    for ident in selected_ids:
        matching = [p for p in all_profiles if p["identifier"] == ident]
        if matching:
            profiles_to_compare.append(matching[0])

    if not profiles_to_compare:
        st.info("No profiles found for selected items.")
        st.stop()

    # Render comparison matrix
    for dimension in ["needs", "objections", "desires", "pain_points"]:
        from autostrat_components import NOPD_STYLES
        style = NOPD_STYLES[dimension]

        st.markdown(f"""
        <div style="font-family: 'Barlow Condensed', sans-serif; font-weight: 700;
                    color: {style['color']}; font-size: 1rem; letter-spacing: 1px;
                    margin: 16px 0 8px 0;">{style['label']}</div>
        """, unsafe_allow_html=True)

        cols = st.columns(len(profiles_to_compare))
        for col, profile_entry in zip(cols, profiles_to_compare):
            with col:
                label = identifier_labels[profile_entry["identifier"]]
                st.markdown(f"**{label}**")
                items = profile_entry["audience_profile"].get(dimension, [])
                for item in items:
                    st.markdown(f"- {item}")
                if not items:
                    st.caption("No data")

    st.markdown("---")

# ── Sentiment Landscape ──────────────────────────────────────────────

all_mentions = get_all_brand_mentions(autostrat)
if all_mentions:
    st.markdown("---")
    render_section_label("Brand Sentiment Landscape")
    st.caption("How brands appear in conversation across hashtag and keyword reports")

    for mention in all_mentions[:10]:
        render_brand_mention(mention)
