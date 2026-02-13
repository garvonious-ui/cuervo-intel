"""
Page 5: Hashtag & Search Intel — "The Landscape"
How Cuervo and competitors show up in hashtag conversations.
Qualitative intelligence from autostrat hashtag reports.
Sidebar filters do NOT apply — this page uses autostrat data directly.
"""

import streamlit as st

from config import CUSTOM_CSS, POPLIFE_PEACH, POPLIFE_BLUE, POPLIFE_BG, POPLIFE_DARK
from autostrat_loader import get_report
from autostrat_components import (
    render_nopd_cards,
    render_territory_cards,
    render_narrative_card,
    render_section_label,
)

st.logo("logo.png")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.title("Hashtag & Search Intel")
st.caption("How Cuervo and competitors show up in hashtag conversations on Instagram")

# ── Load autostrat hashtag reports ───────────────────────────────────
autostrat = st.session_state.get("autostrat", {})

# Brand hashtags
cuervo_ht = get_report(autostrat, "instagram_hashtags", "josecuervo")
cazadores_ht = get_report(autostrat, "instagram_hashtags", "cazadores")
hornitos_ht = get_report(autostrat, "instagram_hashtags", "hornitos")
lunazul_ht = get_report(autostrat, "instagram_hashtags", "lunazul")
milagro_ht = get_report(autostrat, "instagram_hashtags", "milagrotequila")

# General search terms
margarita_ht = get_report(autostrat, "instagram_hashtags", "margaritatime")

brand_reports = {
    "#JoseCuervo": cuervo_ht,
    "#Cazadores": cazadores_ht,
    "#Hornitos": hornitos_ht,
    "#Lunazul": lunazul_ht,
    "#MilagroTequila": milagro_ht,
}

has_brand_data = any(r is not None for r in brand_reports.values())
has_search_data = margarita_ht is not None

if not has_brand_data and not has_search_data:
    st.info(
        "No hashtag intelligence loaded. Drop autostrat PDF exports into "
        "`data/autostrat/pdfs/` and click **Import PDFs** in the sidebar."
    )
    st.stop()


# ── Helpers ──────────────────────────────────────────────────────────

def _get_insights(report):
    """Extract key insights, skipping the duplicated search prompt at index 0."""
    if not report:
        return []
    insights = report.get("executive_summary", {}).get("key_insights", [])
    return insights[1:] if len(insights) > 1 else insights


def _get_opps_actions(report):
    """Extract paired opportunities and strategic actions from hashtag_analysis.
    Arrays are interleaved: [insight, action, insight, action, ...]."""
    if not report:
        return []
    ha = report.get("hashtag_analysis", {})
    opps = ha.get("opportunities", [])
    actions = ha.get("strategic_actions", [])
    pairs = []
    for i in range(0, max(len(opps), len(actions)), 2):
        insight = opps[i] if i < len(opps) else ""
        action = opps[i + 1] if i + 1 < len(opps) else ""
        gap = actions[i] if i < len(actions) else ""
        response = actions[i + 1] if i + 1 < len(actions) else ""
        pairs.append({
            "opportunity": insight,
            "how": action,
            "gap": gap,
            "response": response,
        })
    return pairs


def _render_opp_action_card(pair, accent="#2ea3f2"):
    """Render a paired opportunity / strategic action card."""
    opp = pair.get("opportunity", "")
    how = pair.get("how", "")
    gap = pair.get("gap", "")
    response = pair.get("response", "")

    opp_html = f"<p style='color:#444; font-size:0.92rem; line-height:1.5; margin:0 0 8px 0;'>{opp}</p>" if opp else ""
    how_html = f"<p style='color:{accent}; font-size:0.88rem; font-weight:600; margin:0 0 8px 0;'>&#8594; {how}</p>" if how else ""
    gap_html = f"<p style='color:#D9534F; font-size:0.88rem; margin:0 0 4px 0;'><strong>Gap:</strong> {gap}</p>" if gap else ""
    resp_html = f"<p style='color:#5CB85C; font-size:0.88rem; margin:0;'><strong>Action:</strong> {response}</p>" if response else ""

    st.markdown(f"""
    <div style="background: white; border-radius: 10px; padding: 16px 18px;
                margin-bottom: 10px; border: 1px solid #E0D8D0;
                border-left: 4px solid {accent};">
        {opp_html}{how_html}{gap_html}{resp_html}
    </div>
    """, unsafe_allow_html=True)


# ── Tabs ─────────────────────────────────────────────────────────────

tab_brands, tab_search = st.tabs(["Brand Hashtags", "Search Terms & Categories"])


# ═══════════════════════════════════════════════════════════════════════
# TAB 1: BRAND HASHTAGS
# ═══════════════════════════════════════════════════════════════════════
with tab_brands:
    if not has_brand_data:
        st.info("No brand hashtag reports loaded.")
    else:
        st.markdown("Compare how each brand's hashtag space looks on Instagram.")

        # ── Key Insights ──────────────────────────────────────
        render_section_label("Key Insights")
        active_brands = {k: v for k, v in brand_reports.items() if v is not None}
        cols = st.columns(min(len(active_brands), 3))
        for idx, (label, report) in enumerate(active_brands.items()):
            with cols[idx % len(cols)]:
                st.markdown(f"**{label}**")
                for insight in _get_insights(report):
                    st.markdown(f"- {insight}")

        st.markdown("---")

        # ── Audience Comparison (NOPD per brand) ────────────
        render_section_label("Audience Comparison (NOPD)")
        st.markdown("How each brand's hashtag audience thinks and feels.")
        for label, report in brand_reports.items():
            if report and report.get("audience_profile"):
                with st.expander(f"{label} — Audience Profile", expanded=label == "#JoseCuervo"):
                    ap = report["audience_profile"]
                    if ap.get("summary"):
                        st.markdown(f"*{ap['summary']}*")
                    render_nopd_cards(ap)

        st.markdown("---")

        # ── Opportunities & Strategic Actions ───────────────
        render_section_label("Opportunities & Strategic Actions")
        for label, report in brand_reports.items():
            if report:
                pairs = _get_opps_actions(report)
                if pairs:
                    with st.expander(f"{label} — Opportunities", expanded=label == "#JoseCuervo"):
                        for pair in pairs:
                            _render_opp_action_card(pair)

        st.markdown("---")

        # ── How to Win Territories ──────────────────────────
        render_section_label("How to Win Territories")
        cols = st.columns(min(len(active_brands), 3))
        for idx, (label, report) in enumerate(active_brands.items()):
            with cols[idx % len(cols)]:
                st.markdown(f"**{label}**")
                htw = report.get("how_to_win", {})
                if htw.get("summary"):
                    st.caption(htw["summary"])
                territories = htw.get("territories", [])
                if territories:
                    render_territory_cards(territories)
                else:
                    st.caption("No territories")

        st.markdown("---")

        # ── What This Means for Cuervo ──────────────────────
        render_section_label("What This Means for Cuervo")

        # Build comparison narrative from territories
        cuervo_terrs = set()
        comp_terrs = set()
        if cuervo_ht:
            cuervo_terrs = set(cuervo_ht.get("how_to_win", {}).get("territories", []))
        for rpt in [cazadores_ht, hornitos_ht, lunazul_ht, milagro_ht]:
            if rpt:
                comp_terrs.update(rpt.get("how_to_win", {}).get("territories", []))

        # Unique to Cuervo
        cuervo_unique = cuervo_terrs - comp_terrs
        # Competitor-only
        comp_unique = comp_terrs - cuervo_terrs

        narrative_parts = []
        if cuervo_unique:
            narrative_parts.append(
                "**Where Cuervo leads:** " +
                " | ".join(t[:80] for t in list(cuervo_unique)[:3])
            )
        if comp_unique:
            narrative_parts.append(
                "**Where competitors are winning:** " +
                " | ".join(t[:80] for t in list(comp_unique)[:3])
            )

        # Common gaps — look at NOPD objections across all brands
        all_objections = []
        for rpt in [cuervo_ht, cazadores_ht, hornitos_ht, lunazul_ht, milagro_ht]:
            if rpt:
                all_objections.extend(rpt.get("audience_profile", {}).get("objections", []))
        if all_objections:
            # Find recurring themes
            narrative_parts.append(
                "**Common audience friction across all brands:** " +
                all_objections[0][:120]
            )

        if narrative_parts:
            render_narrative_card(
                "Strategic Takeaway",
                "<br>".join(narrative_parts),
                accent_color=POPLIFE_PEACH,
            )
        else:
            st.caption("Add more hashtag reports to unlock cross-brand comparison.")


# ═══════════════════════════════════════════════════════════════════════
# TAB 2: SEARCH TERMS & CATEGORIES
# ═══════════════════════════════════════════════════════════════════════
with tab_search:
    if not has_search_data:
        st.info("No search term / category hashtag reports loaded.")
    else:
        st.markdown(
            "**#MargaritaTime** — Cuervo's natural territory. "
            "Who owns it and what does winning content look like?"
        )

        # ── Executive Summary ───────────────────────────────
        render_section_label("Executive Summary")
        insights = _get_insights(margarita_ht)
        for insight in insights:
            st.markdown(f"- {insight}")

        st.markdown("---")

        # ── Audience Profile ────────────────────────────────
        render_section_label("Who's Searching #MargaritaTime")
        ap = margarita_ht.get("audience_profile", {})
        if ap.get("summary"):
            st.markdown(f"*{ap['summary']}*")
        render_nopd_cards(ap)

        st.markdown("---")

        # ── Content Opportunities ───────────────────────────
        render_section_label("Content Opportunities & Strategic Actions")
        pairs = _get_opps_actions(margarita_ht)
        for pair in pairs:
            _render_opp_action_card(pair, accent=POPLIFE_BLUE)

        st.markdown("---")

        # ── How to Win ──────────────────────────────────────
        render_section_label("How to Win #MargaritaTime")
        htw = margarita_ht.get("how_to_win", {})
        if htw.get("summary"):
            st.caption(htw["summary"])
        territories = htw.get("territories", [])
        if territories:
            render_territory_cards(territories)

        st.markdown("---")

        # ── Cuervo's Play ───────────────────────────────────
        render_section_label("Cuervo's Play")

        # Build a bridge narrative between brand hashtag and category hashtag
        bridge_parts = []

        # Compare audiences: brand vs category
        if cuervo_ht and margarita_ht:
            cuervo_needs = cuervo_ht.get("audience_profile", {}).get("needs", [])
            marg_needs = margarita_ht.get("audience_profile", {}).get("needs", [])
            if cuervo_needs and marg_needs:
                bridge_parts.append(
                    "<strong>Brand audience needs:</strong> " + cuervo_needs[0]
                )
                bridge_parts.append(
                    "<strong>Category audience needs:</strong> " + marg_needs[0]
                )

            # Territory overlap
            cuervo_t = set(cuervo_ht.get("how_to_win", {}).get("territories", []))
            marg_t = set(margarita_ht.get("how_to_win", {}).get("territories", []))
            overlap = cuervo_t & marg_t
            marg_only = marg_t - cuervo_t

            if overlap:
                bridge_parts.append(
                    "<strong>Already aligned:</strong> " +
                    list(overlap)[0][:100]
                )
            if marg_only:
                bridge_parts.append(
                    "<strong>Untapped category territory:</strong> " +
                    list(marg_only)[0][:100]
                )

        if bridge_parts:
            render_narrative_card(
                "Bridging #JoseCuervo to #MargaritaTime",
                "<br><br>".join(bridge_parts),
                accent_color=POPLIFE_PEACH,
            )
        else:
            st.caption(
                "Import both #JoseCuervo and #MargaritaTime reports to see "
                "how Cuervo can bridge brand and category territory."
            )
