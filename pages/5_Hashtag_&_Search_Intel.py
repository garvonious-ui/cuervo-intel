"""
Page 5: Hashtag & Search Intel — "The Landscape"
How Cuervo and competitors show up in hashtag conversations.
Qualitative intelligence from autostrat hashtag reports.
Sidebar filters do NOT apply — this page uses autostrat data directly.
"""

import streamlit as st

from config import CUSTOM_CSS, POPLIFE_PEACH, POPLIFE_BLUE, POPLIFE_BG, POPLIFE_DARK
from autostrat_loader import get_report, load_all_reports
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
cuervo2_ht = get_report(autostrat, "instagram_hashtags", "cuervo")
cazadores_ht = get_report(autostrat, "instagram_hashtags", "cazadores")
hornitos_ht = get_report(autostrat, "instagram_hashtags", "hornitos")
lunazul_ht = get_report(autostrat, "instagram_hashtags", "lunazul")
milagro_ht = get_report(autostrat, "instagram_hashtags", "milagrotequila")
eljimador_ht = get_report(autostrat, "instagram_hashtags", "eljimador")
teremana_ht = get_report(autostrat, "instagram_hashtags", "teremanatequila")
tequila1800_ht = get_report(autostrat, "instagram_hashtags", "1800tequila")

# General search terms
margarita_ht = get_report(autostrat, "instagram_hashtags", "margaritatime")

brand_reports = {
    "#JoseCuervo": cuervo_ht,
    "#Cuervo": cuervo2_ht,
    "#Cazadores": cazadores_ht,
    "#Hornitos": hornitos_ht,
    "#Lunazul": lunazul_ht,
    "#MilagroTequila": milagro_ht,
    "#ElJimador": eljimador_ht,
    "#TeremanaTequila": teremana_ht,
    "#1800Tequila": tequila1800_ht,
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

# Google News reports
news_reports = autostrat.get("google_news", {})
has_news_data = len(news_reports) > 0

tab_brands, tab_search, tab_news = st.tabs(
    ["Brand Hashtags", "Search Terms & Categories", "Google Search News"]
)


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
        for label, report in active_brands.items():
            with st.expander(f"{label} — Key Insights", expanded=label == "#JoseCuervo"):
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
        for label, report in active_brands.items():
            with st.expander(f"{label} — How to Win", expanded=label == "#JoseCuervo"):
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

        # Gather territories per brand (both Cuervo hashtags count as Cuervo)
        cuervo_terrs = []
        if cuervo_ht:
            cuervo_terrs.extend(cuervo_ht.get("how_to_win", {}).get("territories", []))
        if cuervo2_ht:
            cuervo_terrs.extend(cuervo2_ht.get("how_to_win", {}).get("territories", []))
        comp_terr_map = {}
        for name, rpt in [("#Cazadores", cazadores_ht), ("#Hornitos", hornitos_ht),
                          ("#Lunazul", lunazul_ht), ("#MilagroTequila", milagro_ht),
                          ("#ElJimador", eljimador_ht), ("#TeremanaTequila", teremana_ht),
                          ("#1800Tequila", tequila1800_ht)]:
            if rpt:
                comp_terr_map[name] = rpt.get("how_to_win", {}).get("territories", [])
        all_comp_terrs = set()
        for terrs in comp_terr_map.values():
            all_comp_terrs.update(terrs)
        cuervo_unique = set(cuervo_terrs) - all_comp_terrs
        comp_unique = all_comp_terrs - set(cuervo_terrs)

        # ── Cuervo's Winning Territories ──
        if cuervo_terrs:
            items_html = "".join(
                f"<li style='margin-bottom:6px;'>{t}</li>" for t in cuervo_terrs
            )
            unique_note = ""
            if cuervo_unique:
                unique_tags = "".join(
                    f"<span style='background:#C8E6C9; color:#2E7D32; padding:2px 8px; "
                    f"border-radius:10px; font-size:0.8rem; font-weight:600; "
                    f"margin-right:6px;'>Unique to Cuervo</span>"
                    for _ in range(1)
                )
                unique_items = "".join(
                    f"<li style='margin-bottom:4px;'>{t}</li>" for t in cuervo_unique
                )
                unique_note = (
                    f"<div style='margin-top:12px; padding-top:10px; border-top:1px solid #E0D8D0;'>"
                    f"{unique_tags} Territories no competitor is claiming:"
                    f"<ul style='margin:6px 0 0 0; padding-left:20px; color:#2E7D32; "
                    f"font-size:0.88rem;'>{unique_items}</ul></div>"
                )
            st.markdown(f"""
            <div style="background:white; border-radius:10px; padding:18px 20px;
                        margin-bottom:14px; border:1px solid #E0D8D0;
                        border-left:5px solid #5CB85C;">
                <h4 style="font-family:'Barlow Condensed',sans-serif; font-weight:700;
                           color:#5CB85C; margin:0 0 10px 0; font-size:1rem;">
                    Where Cuervo Leads</h4>
                <ul style="margin:0; padding-left:20px; color:#444; font-size:0.92rem;
                           line-height:1.55;">{items_html}</ul>
                {unique_note}
            </div>
            """, unsafe_allow_html=True)

        # ── Where Competitors Are Winning ──
        if comp_terr_map:
            cards_html = ""
            for brand_label, terrs in comp_terr_map.items():
                if not terrs:
                    continue
                terr_items = "".join(
                    f"<li style='margin-bottom:4px;'>{t}</li>" for t in terrs
                )
                cards_html += (
                    f"<div style='margin-bottom:12px;'>"
                    f"<strong style='color:#D9534F; font-size:0.95rem;'>{brand_label}</strong>"
                    f"<ul style='margin:4px 0 0 0; padding-left:20px; color:#444; "
                    f"font-size:0.88rem; line-height:1.5;'>{terr_items}</ul></div>"
                )
            if comp_unique:
                threat_items = "".join(
                    f"<li style='margin-bottom:4px;'>{t}</li>"
                    for t in list(comp_unique)[:5]
                )
                cards_html += (
                    f"<div style='margin-top:12px; padding-top:10px; border-top:1px solid #E0D8D0;'>"
                    f"<span style='background:#FFCDD2; color:#C62828; padding:2px 8px; "
                    f"border-radius:10px; font-size:0.8rem; font-weight:600;'>"
                    f"Not in Cuervo's playbook</span> "
                    f"Territories competitors own that Cuervo does not:"
                    f"<ul style='margin:6px 0 0 0; padding-left:20px; color:#C62828; "
                    f"font-size:0.88rem;'>{threat_items}</ul></div>"
                )
            st.markdown(f"""
            <div style="background:white; border-radius:10px; padding:18px 20px;
                        margin-bottom:14px; border:1px solid #E0D8D0;
                        border-left:5px solid #D9534F;">
                <h4 style="font-family:'Barlow Condensed',sans-serif; font-weight:700;
                           color:#D9534F; margin:0 0 10px 0; font-size:1rem;">
                    Where Competitors Are Winning</h4>
                {cards_html}
            </div>
            """, unsafe_allow_html=True)

        # ── Common Audience Friction ──
        brand_objections = {}
        for name, rpt in [("#JoseCuervo", cuervo_ht), ("#Cuervo", cuervo2_ht),
                          ("#Cazadores", cazadores_ht), ("#Hornitos", hornitos_ht),
                          ("#Lunazul", lunazul_ht), ("#MilagroTequila", milagro_ht),
                          ("#ElJimador", eljimador_ht), ("#TeremanaTequila", teremana_ht),
                          ("#1800Tequila", tequila1800_ht)]:
            if rpt:
                objs = rpt.get("audience_profile", {}).get("objections", [])
                if objs:
                    brand_objections[name] = objs

        if brand_objections:
            obj_html = ""
            for brand_label, objs in brand_objections.items():
                obj_items = "".join(
                    f"<li style='margin-bottom:4px;'>{o}</li>" for o in objs
                )
                obj_html += (
                    f"<div style='margin-bottom:10px;'>"
                    f"<strong style='color:#E65100; font-size:0.95rem;'>{brand_label}</strong>"
                    f"<ul style='margin:4px 0 0 0; padding-left:20px; color:#444; "
                    f"font-size:0.88rem; line-height:1.5;'>{obj_items}</ul></div>"
                )
            st.markdown(f"""
            <div style="background:white; border-radius:10px; padding:18px 20px;
                        margin-bottom:14px; border:1px solid #E0D8D0;
                        border-left:5px solid #F8C090;">
                <h4 style="font-family:'Barlow Condensed',sans-serif; font-weight:700;
                           color:#E65100; margin:0 0 4px 0; font-size:1rem;">
                    Common Audience Friction</h4>
                <p style="color:#777; font-size:0.85rem; margin:0 0 12px 0;">
                    Objections and pushback themes across all brand hashtag audiences —
                    shared friction points signal category-wide opportunities.</p>
                {obj_html}
            </div>
            """, unsafe_allow_html=True)

        # ── Cuervo's Strategic Summary ──
        if cuervo_ht:
            summary = cuervo_ht.get("how_to_win", {}).get("summary", "")
            cuervo_desires = cuervo_ht.get("audience_profile", {}).get("desires", [])
            if summary or cuervo_desires:
                desires_html = ""
                if cuervo_desires:
                    d_items = "".join(
                        f"<li style='margin-bottom:4px;'>{d}</li>" for d in cuervo_desires
                    )
                    desires_html = (
                        f"<div style='margin-top:10px;'>"
                        f"<strong style='font-size:0.9rem;'>What the #JoseCuervo audience wants:</strong>"
                        f"<ul style='margin:4px 0 0 0; padding-left:20px; color:#444; "
                        f"font-size:0.88rem; line-height:1.5;'>{d_items}</ul></div>"
                    )
                summary_html = (
                    f"<p style='color:#444; font-size:0.92rem; line-height:1.55; "
                    f"margin:0;'>{summary}</p>" if summary else ""
                )
                st.markdown(f"""
                <div style="background:linear-gradient(135deg, #FDEBD6 0%, #FFF8F0 100%);
                            border-radius:10px; padding:18px 20px; margin-bottom:14px;
                            border-left:5px solid {POPLIFE_PEACH};">
                    <h4 style="font-family:'Barlow Condensed',sans-serif; font-weight:700;
                               color:{POPLIFE_DARK}; margin:0 0 10px 0; font-size:1rem;">
                        Cuervo's Path Forward</h4>
                    {summary_html}
                    {desires_html}
                </div>
                """, unsafe_allow_html=True)

        if not cuervo_terrs and not comp_terr_map and not brand_objections:
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


# ═══════════════════════════════════════════════════════════════════════
# TAB 3: GOOGLE SEARCH NEWS
# ═══════════════════════════════════════════════════════════════════════
with tab_news:
    if not has_news_data:
        st.info(
            "No Google News reports loaded. Drop autostrat Google News PDF exports "
            "into `data/autostrat/pdfs/` and click **Import PDFs** in the sidebar."
        )
    else:
        st.markdown(
            "What the news is saying about tequila brands — sentiment, narratives, "
            "and strategic implications from Google News intelligence."
        )

        for query_id, report in news_reports.items():
            query_label = report.get("search_query", query_id).replace("_", " ").title()

            with st.expander(f"{query_label} — News Intelligence", expanded=True):

                # ── Executive Summary ─────────────────────
                exec_sum = report.get("executive_summary", {})
                overview = exec_sum.get("overview", "")
                insights = exec_sum.get("key_insights", [])
                # Skip first element if it duplicates the search prompt
                if len(insights) > 1:
                    insights = insights[1:]

                if overview:
                    render_narrative_card("Overview", overview, accent_color=POPLIFE_BLUE)

                if insights:
                    render_section_label("Key Insights")
                    for insight in insights:
                        st.markdown(f"- {insight}")

                # ── News Analysis ─────────────────────────
                news_analysis = report.get("news_analysis", {})
                na_summary = news_analysis.get("summary", "")
                if na_summary:
                    st.markdown("---")
                    render_section_label("News Analysis")
                    st.markdown(na_summary)

                # Sentiment breakdown
                sentiment = news_analysis.get("sentiment_breakdown", {})
                pos = sentiment.get("positive_pct", 0)
                neu = sentiment.get("neutral_pct", 0)
                neg = sentiment.get("negative_pct", 0)
                if pos or neu or neg:
                    s1, s2, s3 = st.columns(3)
                    with s1:
                        st.markdown(f"""
                        <div style="background:#F0FFF0; border-left:4px solid #5CB85C;
                                    border-radius:0 8px 8px 0; padding:12px 16px; text-align:center;">
                            <div style="font-size:1.5rem; font-weight:700; color:#2E7D32;">{pos}%</div>
                            <div style="font-size:0.85rem; color:#555;">Positive</div>
                        </div>""", unsafe_allow_html=True)
                    with s2:
                        st.markdown(f"""
                        <div style="background:#F5F5F5; border-left:4px solid #9E9E9E;
                                    border-radius:0 8px 8px 0; padding:12px 16px; text-align:center;">
                            <div style="font-size:1.5rem; font-weight:700; color:#616161;">{neu}%</div>
                            <div style="font-size:0.85rem; color:#555;">Neutral</div>
                        </div>""", unsafe_allow_html=True)
                    with s3:
                        st.markdown(f"""
                        <div style="background:#FFF5F5; border-left:4px solid #D9534F;
                                    border-radius:0 8px 8px 0; padding:12px 16px; text-align:center;">
                            <div style="font-size:1.5rem; font-weight:700; color:#C62828;">{neg}%</div>
                            <div style="font-size:0.85rem; color:#555;">Negative</div>
                        </div>""", unsafe_allow_html=True)

                # Key topics
                topics = news_analysis.get("key_topics", [])
                if topics:
                    render_section_label("Key Topics")
                    for topic in topics:
                        st.markdown(f"- {topic}")

                # Opportunities & Risks
                opps = news_analysis.get("opportunities", [])
                risks = news_analysis.get("risks", [])
                if opps or risks:
                    st.markdown("---")
                    o_col, r_col = st.columns(2)
                    with o_col:
                        if opps:
                            st.markdown(f"""
                            <div style="background:#F0FFF0; border-left:4px solid #5CB85C;
                                        border-radius:0 8px 8px 0; padding:14px 16px;">
                                <h4 style="color:#2E7D32; font-family:'Barlow Condensed',sans-serif;
                                           font-weight:700; margin:0 0 8px 0; font-size:0.95rem;">
                                    OPPORTUNITIES</h4>
                                <ul style="margin:0; padding-left:18px; color:#444;
                                           font-size:0.9rem; line-height:1.5;">
                                    {''.join(f'<li style="margin-bottom:4px;">{o}</li>' for o in opps)}
                                </ul>
                            </div>""", unsafe_allow_html=True)
                    with r_col:
                        if risks:
                            st.markdown(f"""
                            <div style="background:#FFF5F5; border-left:4px solid #D9534F;
                                        border-radius:0 8px 8px 0; padding:14px 16px;">
                                <h4 style="color:#C62828; font-family:'Barlow Condensed',sans-serif;
                                           font-weight:700; margin:0 0 8px 0; font-size:0.95rem;">
                                    RISKS</h4>
                                <ul style="margin:0; padding-left:18px; color:#444;
                                           font-size:0.9rem; line-height:1.5;">
                                    {''.join(f'<li style="margin-bottom:4px;">{r}</li>' for r in risks)}
                                </ul>
                            </div>""", unsafe_allow_html=True)

                # ── Brand Mentions ────────────────────────
                mentions = report.get("brand_mentions", [])
                if mentions:
                    st.markdown("---")
                    render_section_label("Brand Mentions")
                    for mention in mentions:
                        from autostrat_components import render_brand_mention
                        render_brand_mention({
                            "brand": mention.get("brand", ""),
                            "context": mention.get("context", ""),
                            "sentiment": mention.get("sentiment", ""),
                            "source_label": "Google News",
                            "source_identifier": query_label,
                        })

                # ── Trending Narratives ───────────────────
                narratives = report.get("trending_narratives", [])
                if narratives:
                    st.markdown("---")
                    render_section_label("Trending Narratives")
                    for narr in narratives:
                        title = narr.get("narrative", narr.get("trend", ""))
                        desc = narr.get("description", "")
                        brands = narr.get("brands_involved", [])
                        brands_tag = ""
                        if brands:
                            brands_tag = (
                                f"<div style='margin-top:6px; font-size:0.82rem; color:#999;'>"
                                f"Brands: {', '.join(brands)}</div>"
                            )
                        if title or desc:
                            st.markdown(f"""
                            <div style="background:white; border-radius:10px; padding:16px 18px;
                                        margin-bottom:10px; border:1px solid #E0D8D0;
                                        border-top:3px solid {POPLIFE_BLUE};">
                                <strong style="font-family:'Barlow Condensed',sans-serif;
                                               font-size:1rem; color:#333;">{title}</strong>
                                <p style="color:#444; font-size:0.9rem; line-height:1.5;
                                          margin:6px 0 0 0;">{desc}</p>
                                {brands_tag}
                            </div>""", unsafe_allow_html=True)

                # ── Strategic Implications ────────────────
                strat = report.get("strategic_implications", {})
                strat_summary = strat.get("summary", "")
                action_items = strat.get("action_items", [])
                if strat_summary or action_items:
                    st.markdown("---")
                    render_section_label("Strategic Implications")
                    if strat_summary:
                        render_narrative_card(
                            "What This Means", strat_summary, accent_color=POPLIFE_PEACH
                        )
                    if action_items:
                        render_territory_cards(action_items)
