"""
Page 5: Conversation Intel -- "The Landscape"
All qualitative intelligence: brand hashtags, category/cultural research,
and Google News. Multi-platform (Instagram + TikTok).
Sidebar filters do NOT apply -- this page uses autostrat data directly.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st

from config import POPLIFE_PEACH, POPLIFE_BLUE, POPLIFE_BG, POPLIFE_DARK
from autostrat_loader import (
    get_report, get_all_brand_mentions,
    get_brand_hashtag_reports, get_category_reports,
    REPORT_TYPE_LABELS,
)
from autostrat_components import (
    render_nopd_cards,
    render_territory_cards,
    render_narrative_card,
    render_section_label,
    render_brand_mention,
    platform_label,
)

# ── Load data dynamically ─────────────────────────────────────────────
autostrat = st.session_state.get("autostrat", {})

from client_context import get_client
cfg = get_client()

st.logo(cfg.app_logo_path)
st.markdown(cfg.custom_css, unsafe_allow_html=True)

st.title(cfg.page_headers.get("conversation", "Conversation Intel"))
st.caption(
    "Qualitative intelligence from brand hashtags, category research, "
    "and news -- Instagram & TikTok"
)

brand_ht_map = get_brand_hashtag_reports(autostrat)
category_reports = get_category_reports(autostrat)
news_reports = autostrat.get("google_news", {})
_all_mentions_raw = get_all_brand_mentions(autostrat)
_allowed_ids = set(cfg.brand_hashtags) | set(cfg.category_hashtags) | set(autostrat.get("google_news", {}).keys())
all_mentions = [m for m in _all_mentions_raw if m.get("source_identifier") in _allowed_ids]

has_brand_data = len(brand_ht_map) > 0
has_category_data = len(category_reports) > 0
has_news_data = len(news_reports) > 0

if not has_brand_data and not has_category_data and not has_news_data:
    st.info(
        "No conversation intelligence loaded. Drop autostrat PDF exports into "
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
    """Extract paired opportunities and strategic actions from hashtag_analysis
    or how_to_win territories (keyword reports).
    Arrays are parallel: opportunities[i] pairs with strategic_actions[i]."""
    if not report:
        return []
    # Hashtag reports: hashtag_analysis.opportunities + strategic_actions
    ha = report.get("hashtag_analysis", {})
    opps = ha.get("opportunities", [])
    actions = ha.get("strategic_actions", [])
    if opps or actions:
        pairs = []
        for i in range(max(len(opps), len(actions))):
            pairs.append({
                "opportunity": opps[i] if i < len(opps) else "",
                "action": actions[i] if i < len(actions) else "",
            })
        return pairs
    # Keyword reports: how_to_win.territories as opportunities
    htw = report.get("how_to_win", {})
    territories = htw.get("territories", [])
    if territories:
        return [{"opportunity": t, "action": ""} for t in territories]
    return []


def _render_opp_action_card(pair, accent="#2ea3f2"):
    """Render a paired opportunity / strategic action card."""
    opp = pair.get("opportunity", "")
    action = pair.get("action", "")

    opp_html = f"<p style='color:#444; font-size:0.92rem; line-height:1.5; margin:0 0 8px 0;'><strong>Opportunity:</strong> {opp}</p>" if opp else ""
    action_html = f"<p style='color:{accent}; font-size:0.88rem; font-weight:600; margin:0;'>&#8594; {action}</p>" if action else ""

    st.markdown(f"""
    <div style="background: white; border-radius: 10px; padding: 16px 18px;
                margin-bottom: 10px; border: 1px solid #E0D8D0;
                border-left: 4px solid {accent};">
        {opp_html}{action_html}
    </div>
    """, unsafe_allow_html=True)


# ── Build ordered flat list of brand reports ──────────────────────────
# (display_label, report_type, identifier, report)
brand_display_order = list(cfg.brand_hashtags.keys())
active_brand_reports = []
for ident in brand_display_order:
    if ident in brand_ht_map:
        for rt, label, report in brand_ht_map[ident]:
            active_brand_reports.append((label, rt, ident, report))


# ── Tabs ─────────────────────────────────────────────────────────────

tab_brands, tab_category, tab_news = st.tabs(
    ["Brand Hashtags", "Category & Cultural", "Google Search News"]
)


# ═══════════════════════════════════════════════════════════════════════
# TAB 1: BRAND HASHTAGS (multi-platform)
# ═══════════════════════════════════════════════════════════════════════
with tab_brands:
    if not has_brand_data:
        st.info("No brand hashtag reports loaded.")
    else:
        st.markdown("Compare how each brand's hashtag space looks across Instagram & TikTok.")

        # ── Key Insights ──────────────────────────────────────
        render_section_label("Key Insights")
        for label, rt, ident, report in active_brand_reports:
            plat = platform_label(rt)
            is_hero = ident in cfg.hero_hashtag_ids
            with st.expander(f"{label} ({plat}) -- Key Insights", expanded=is_hero):
                for insight in _get_insights(report):
                    st.markdown(f"- {insight}")

        st.markdown("---")

        # ── Audience Comparison (NOPD per brand) ────────────
        render_section_label("Audience Comparison (NOPD)")
        st.markdown("How each brand's hashtag audience thinks and feels.")
        for label, rt, ident, report in active_brand_reports:
            if report.get("audience_profile"):
                plat = platform_label(rt)
                is_hero = ident in cfg.hero_hashtag_ids
                with st.expander(f"{label} ({plat}) -- Audience Profile", expanded=is_hero):
                    ap = report["audience_profile"]
                    if ap.get("summary"):
                        st.markdown(f"*{ap['summary']}*")
                    render_nopd_cards(ap)

        st.markdown("---")

        # ── Opportunities & Strategic Actions ───────────────
        render_section_label("Opportunities & Strategic Actions")
        for label, rt, ident, report in active_brand_reports:
            pairs = _get_opps_actions(report)
            if pairs:
                plat = platform_label(rt)
                is_hero = ident in cfg.hero_hashtag_ids
                with st.expander(f"{label} ({plat}) -- Opportunities", expanded=is_hero):
                    for pair in pairs:
                        _render_opp_action_card(pair)

        st.markdown("---")

        # ── How to Win Territories ─────────────────────────────
        render_section_label("How to Win Territories")
        for label, rt, ident, report in active_brand_reports:
            htw = report.get("how_to_win", {})
            if not htw.get("territories") and not htw.get("summary"):
                continue
            plat = platform_label(rt)
            is_hero = ident in cfg.hero_hashtag_ids
            with st.expander(f"{label} ({plat}) — How to Win", expanded=is_hero):
                if htw.get("summary"):
                    st.caption(htw["summary"])
                territories = htw.get("territories", [])
                if territories:
                    render_territory_cards(territories)
                else:
                    st.caption("No territories")

        st.markdown("---")

        # ── What This Means for {hero_brand} ──────────────────────
        conv_narrative = cfg.narrative.get("conversation", {})
        what_this_means_header = conv_narrative.get("what_this_means", f"What This Means for {cfg.hero_brand}")
        render_section_label(what_this_means_header)

        # Gather hero brand territories (across platforms)
        hero_terrs = []
        for ident in cfg.hero_hashtag_ids:
            if ident in brand_ht_map:
                for rt, label, report in brand_ht_map[ident]:
                    hero_terrs.extend(
                        report.get("how_to_win", {}).get("territories", [])
                    )

        # Gather competitor territories
        comp_terr_map = {}
        for ident, entries in brand_ht_map.items():
            if ident not in cfg.hero_hashtag_ids:
                for rt, label, report in entries:
                    plat = platform_label(rt)
                    key = f"{label} ({plat})"
                    terrs = report.get("how_to_win", {}).get("territories", [])
                    if terrs:
                        comp_terr_map[key] = terrs

        all_comp_terrs = set()
        for terrs in comp_terr_map.values():
            all_comp_terrs.update(terrs)
        hero_unique = set(hero_terrs) - all_comp_terrs
        comp_unique = all_comp_terrs - set(hero_terrs)

        # ── No hero data: reframe as "What to Steal" ──
        if not hero_terrs and comp_terr_map:
            steal_caption = conv_narrative.get(
                "steal_caption",
                f"Competitor strategies {cfg.hero_brand} can adapt and steal"
            )
            st.caption(steal_caption)
            for brand_label, terrs in comp_terr_map.items():
                if not terrs:
                    continue
                terr_items = "".join(
                    f"<li style='margin-bottom:6px;'>{t}</li>" for t in terrs
                )
                st.markdown(f"""
                <div style="background:white; border-radius:10px; padding:18px 20px;
                            margin-bottom:14px; border:1px solid #E0D8D0;
                            border-left:5px solid {POPLIFE_BLUE};">
                    <h4 style="font-family:'Barlow Condensed',sans-serif; font-weight:700;
                               color:{POPLIFE_BLUE}; margin:0 0 10px 0; font-size:1rem;">
                        What to steal from {brand_label}</h4>
                    <ul style="margin:0; padding-left:20px; color:#444; font-size:0.92rem;
                               line-height:1.55;">{terr_items}</ul>
                </div>
                """, unsafe_allow_html=True)

            # Also show competitor audience insights as steal signals
            comp_desires = {}
            for label_item, rt, ident, report in active_brand_reports:
                desires = report.get("audience_profile", {}).get("desires", [])
                if desires and ident not in cfg.hero_hashtag_ids:
                    plat = platform_label(rt)
                    comp_desires[f"{label_item} ({plat})"] = desires
            if comp_desires:
                st.markdown(f"""
                <div style="background:#E8F5E9; border-radius:10px; padding:18px 20px;
                            margin-top:14px; border:1px solid #C8E6C9;
                            border-left:5px solid #5CB85C;">
                    <h4 style="font-family:'Barlow Condensed',sans-serif; font-weight:700;
                               color:#2E7D32; margin:0 0 10px 0; font-size:1rem;">
                        Audience Desires {cfg.hero_brand} Can Tap Into</h4>
                """, unsafe_allow_html=True)
                for brand_label, desires in comp_desires.items():
                    desire_items = "".join(
                        f"<li style='margin-bottom:4px;'>{d}</li>" for d in desires[:3]
                    )
                    st.markdown(f"""
                    <div style="margin-bottom:10px;">
                        <strong style="color:#2E7D32; font-size:0.95rem;">{brand_label}</strong>
                        <ul style="margin:4px 0 0 0; padding-left:20px; color:#444;
                                   font-size:0.88rem; line-height:1.5;">{desire_items}</ul>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        # ── Hero Brand's Winning Territories ──
        cuervo_leads_header = conv_narrative.get("cuervo_leads_header", f"Where {cfg.hero_brand} Leads")
        if hero_terrs:
            items_html = "".join(
                f"<li style='margin-bottom:6px;'>{t}</li>" for t in hero_terrs
            )
            unique_note = ""
            if hero_unique:
                unique_items = "".join(
                    f"<li style='margin-bottom:4px;'>{t}</li>" for t in hero_unique
                )
                unique_note = (
                    f"<div style='margin-top:12px; padding-top:10px; border-top:1px solid #E0D8D0;'>"
                    f"<span style='background:#C8E6C9; color:#2E7D32; padding:2px 8px; "
                    f"border-radius:10px; font-size:0.8rem; font-weight:600; "
                    f"margin-right:6px;'>Unique to {cfg.hero_brand}</span>"
                    f" Territories no competitor is claiming:"
                    f"<ul style='margin:6px 0 0 0; padding-left:20px; color:#2E7D32; "
                    f"font-size:0.88rem;'>{unique_items}</ul></div>"
                )
            st.markdown(f"""
            <div style="background:white; border-radius:10px; padding:18px 20px;
                        margin-bottom:14px; border:1px solid #E0D8D0;
                        border-left:5px solid #5CB85C;">
                <h4 style="font-family:'Barlow Condensed',sans-serif; font-weight:700;
                           color:#5CB85C; margin:0 0 10px 0; font-size:1rem;">
                    {cuervo_leads_header}</h4>
                <ul style="margin:0; padding-left:20px; color:#444; font-size:0.92rem;
                           line-height:1.55;">{items_html}</ul>
                {unique_note}
            </div>
            """, unsafe_allow_html=True)

        # ── Where Competitors Are Winning ──
        competitors_winning_header = conv_narrative.get("competitors_winning_header", "Where Competitors Are Winning")
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
                    f"Not in {cfg.hero_brand}'s playbook</span> "
                    f"Territories competitors own that {cfg.hero_brand} does not:"
                    f"<ul style='margin:6px 0 0 0; padding-left:20px; color:#C62828; "
                    f"font-size:0.88rem;'>{threat_items}</ul></div>"
                )
            st.markdown(f"""
            <div style="background:white; border-radius:10px; padding:18px 20px;
                        margin-bottom:14px; border:1px solid #E0D8D0;
                        border-left:5px solid #D9534F;">
                <h4 style="font-family:'Barlow Condensed',sans-serif; font-weight:700;
                           color:#D9534F; margin:0 0 10px 0; font-size:1rem;">
                    {competitors_winning_header}</h4>
                {cards_html}
            </div>
            """, unsafe_allow_html=True)

        # ── Common Audience Friction ──
        brand_objections = {}
        for label, rt, ident, report in active_brand_reports:
            objs = report.get("audience_profile", {}).get("objections", [])
            if objs:
                plat = platform_label(rt)
                brand_objections[f"{label} ({plat})"] = objs

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
            friction_caption = conv_narrative.get(
                "audience_friction_caption",
                "Shared friction points signal category-wide opportunities."
            )
            st.markdown(f"""
            <div style="background:white; border-radius:10px; padding:18px 20px;
                        margin-bottom:14px; border:1px solid #E0D8D0;
                        border-left:5px solid #F8C090;">
                <h4 style="font-family:'Barlow Condensed',sans-serif; font-weight:700;
                           color:#E65100; margin:0 0 4px 0; font-size:1rem;">
                    Common Audience Friction</h4>
                <p style="color:#777; font-size:0.85rem; margin:0 0 12px 0;">
                    Objections and pushback themes across all brand hashtag audiences --
                    {friction_caption}</p>
                {obj_html}
            </div>
            """, unsafe_allow_html=True)

        # ── Hero Brand's Strategic Summary ──
        # Find the first hero brand report for summary + desires
        _hero_report = None
        for ident in cfg.hero_hashtag_ids:
            if ident in brand_ht_map:
                _hero_report = brand_ht_map[ident][0][2]  # first report
                break

        if _hero_report:
            summary = _hero_report.get("how_to_win", {}).get("summary", "")
            hero_desires = _hero_report.get("audience_profile", {}).get("desires", [])
            if summary or hero_desires:
                desires_html = ""
                if hero_desires:
                    d_items = "".join(
                        f"<li style='margin-bottom:4px;'>{d}</li>" for d in hero_desires
                    )
                    desires_html = (
                        f"<div style='margin-top:10px;'>"
                        f"<strong style='font-size:0.9rem;'>What the {cfg.hero_brand} hashtag audience wants:</strong>"
                        f"<ul style='margin:4px 0 0 0; padding-left:20px; color:#444; "
                        f"font-size:0.88rem; line-height:1.5;'>{d_items}</ul></div>"
                    )
                summary_html = (
                    f"<p style='color:#444; font-size:0.92rem; line-height:1.55; "
                    f"margin:0;'>{summary}</p>" if summary else ""
                )
                path_forward_header = conv_narrative.get("path_forward_header", f"{cfg.hero_brand}'s Path Forward")
                st.markdown(f"""
                <div style="background:linear-gradient(135deg, #FDEBD6 0%, #FFF8F0 100%);
                            border-radius:10px; padding:18px 20px; margin-bottom:14px;
                            border-left:5px solid {POPLIFE_PEACH};">
                    <h4 style="font-family:'Barlow Condensed',sans-serif; font-weight:700;
                               color:{POPLIFE_DARK}; margin:0 0 10px 0; font-size:1rem;">
                        {path_forward_header}</h4>
                    {summary_html}
                    {desires_html}
                </div>
                """, unsafe_allow_html=True)

        if not hero_terrs and not comp_terr_map and not brand_objections:
            st.caption("Add more hashtag reports to unlock cross-brand comparison.")

        # ── Brand Mentions (moved from Page 2) ────────────────
        if all_mentions:
            st.markdown("---")
            render_section_label("Brand Mentions Across All Conversations")
            st.caption("How brands appear in the conversation space across all hashtag, keyword, and news reports")
            for mention in all_mentions[:12]:
                render_brand_mention(mention)


# ═══════════════════════════════════════════════════════════════════════
# TAB 2: CATEGORY & CULTURAL
# ═══════════════════════════════════════════════════════════════════════
with tab_category:
    if not has_category_data:
        st.info("No category or cultural reports loaded yet.")
    else:
        st.markdown(
            "Cultural hashtags, category search terms, and keyword research "
            "across Instagram & TikTok."
        )

        for rt, identifier, cat_label, report in category_reports:
            plat = platform_label(rt)
            with st.expander(f"{cat_label} ({plat})", expanded=True):

                # ── Executive Summary ───────────────────────────
                insights = _get_insights(report)
                if insights:
                    render_section_label("Executive Summary")
                    for insight in insights:
                        st.markdown(f"- {insight}")

                # ── Audience Profile ────────────────────────────
                ap = report.get("audience_profile", {})
                has_nopd = any(ap.get(k) for k in ["needs", "objections", "desires", "pain_points"])
                if has_nopd:
                    st.markdown("---")
                    render_section_label(f"Who's Searching {cat_label}")
                    if ap.get("summary"):
                        st.markdown(f"*{ap['summary']}*")
                    render_nopd_cards(ap)

                # ── Content Opportunities ───────────────────────
                pairs = _get_opps_actions(report)
                if pairs:
                    st.markdown("---")
                    render_section_label("Content Opportunities & Strategic Actions")
                    for pair in pairs:
                        _render_opp_action_card(pair, accent=POPLIFE_BLUE)

                # ── How to Win ──────────────────────────────────
                htw = report.get("how_to_win", {})
                if htw.get("territories") or htw.get("summary"):
                    st.markdown("---")
                    render_section_label(f"How to Win {cat_label}")
                    if htw.get("summary"):
                        st.caption(htw["summary"])
                    if htw.get("territories"):
                        render_territory_cards(htw["territories"])

        # ── Hero Brand's Play: bridge brand + category ─────────────
        _hero_rpt = None
        for ident in cfg.hero_hashtag_ids:
            if ident in brand_ht_map:
                _hero_rpt = brand_ht_map[ident][0][2]
                break

        if _hero_rpt and category_reports:
            st.markdown("---")
            cuervos_play_header = conv_narrative.get("cuervos_play", f"{cfg.hero_brand}'s Play")
            render_section_label(cuervos_play_header)

            cat_rpt = category_reports[0][3]
            cat_lbl = category_reports[0][2]

            bridge_parts = []

            hero_needs = _hero_rpt.get("audience_profile", {}).get("needs", [])
            cat_needs = cat_rpt.get("audience_profile", {}).get("needs", [])
            if hero_needs and cat_needs:
                bridge_parts.append(
                    "<strong>Brand audience needs:</strong> " + hero_needs[0]
                )
                bridge_parts.append(
                    "<strong>Category audience needs:</strong> " + cat_needs[0]
                )

            hero_t = set(_hero_rpt.get("how_to_win", {}).get("territories", []))
            cat_t = set(cat_rpt.get("how_to_win", {}).get("territories", []))
            overlap = hero_t & cat_t
            cat_only = cat_t - hero_t

            if overlap:
                bridge_parts.append(
                    "<strong>Already aligned:</strong> " +
                    list(overlap)[0][:100]
                )
            if cat_only:
                bridge_parts.append(
                    "<strong>Untapped category territory:</strong> " +
                    list(cat_only)[0][:100]
                )

            if bridge_parts:
                bridge_title = conv_narrative.get(
                    "bridge_template", "Bridging {hero_brand} to {cat_label}"
                ).format(hero_brand=cfg.hero_brand, cat_label=cat_lbl)
                render_narrative_card(
                    bridge_title,
                    "<br><br>".join(bridge_parts),
                    accent_color=POPLIFE_PEACH,
                )
            else:
                import_hint = conv_narrative.get(
                    "import_hint_template",
                    "Import both {hero_brand} and {cat_label} reports to see "
                    "how {hero_brand} can bridge brand and category territory."
                ).format(hero_brand=cfg.hero_brand, cat_label=cat_lbl)
                st.caption(import_hint)


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
            f"What the news is saying about {cfg.industry} brands -- sentiment, narratives, "
            "and strategic implications from Google News intelligence."
        )

        for query_id, report in news_reports.items():
            query_label = report.get("search_query", query_id).replace("_", " ").title()

            with st.expander(f"{query_label} -- News Intelligence", expanded=True):

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

                # ── Audience Profile (NOPD) ─────────────
                ap = report.get("audience_profile", {})
                has_nopd = any(ap.get(k) for k in ["needs", "objections", "desires", "pain_points"])
                if has_nopd:
                    st.markdown("---")
                    render_section_label("News Audience Profile")
                    if ap.get("summary"):
                        st.markdown(f"*{ap['summary']}*")
                    render_nopd_cards(ap)

                # ── SWOT Analysis ──────────────────────────
                swot = report.get("swot_analysis", {})
                has_swot = any(swot.get(k) for k in ["strengths", "weaknesses", "opportunities", "threats"])
                if has_swot:
                    st.markdown("---")
                    render_section_label("SWOT Analysis")
                    sw_col, ot_col = st.columns(2)
                    with sw_col:
                        strengths = swot.get("strengths", [])
                        if strengths:
                            s_items = "".join(f'<li style="margin-bottom:6px;">{s}</li>' for s in strengths)
                            st.markdown(f"""
                            <div style="background:#F0FFF0; border-left:4px solid #5CB85C;
                                        border-radius:0 8px 8px 0; padding:14px 16px; margin-bottom:12px;">
                                <h4 style="color:#2E7D32; font-family:'Barlow Condensed',sans-serif;
                                           font-weight:700; margin:0 0 8px 0; font-size:0.95rem;">
                                    STRENGTHS</h4>
                                <ul style="margin:0; padding-left:18px; color:#444;
                                           font-size:0.88rem; line-height:1.5;">{s_items}</ul>
                            </div>""", unsafe_allow_html=True)
                        weaknesses = swot.get("weaknesses", [])
                        if weaknesses:
                            w_items = "".join(f'<li style="margin-bottom:6px;">{w}</li>' for w in weaknesses)
                            st.markdown(f"""
                            <div style="background:#FFF5F5; border-left:4px solid #D9534F;
                                        border-radius:0 8px 8px 0; padding:14px 16px;">
                                <h4 style="color:#C62828; font-family:'Barlow Condensed',sans-serif;
                                           font-weight:700; margin:0 0 8px 0; font-size:0.95rem;">
                                    WEAKNESSES</h4>
                                <ul style="margin:0; padding-left:18px; color:#444;
                                           font-size:0.88rem; line-height:1.5;">{w_items}</ul>
                            </div>""", unsafe_allow_html=True)
                    with ot_col:
                        opportunities = swot.get("opportunities", [])
                        if opportunities:
                            o_items = "".join(f'<li style="margin-bottom:6px;">{o}</li>' for o in opportunities)
                            st.markdown(f"""
                            <div style="background:#E3F2FD; border-left:4px solid {POPLIFE_BLUE};
                                        border-radius:0 8px 8px 0; padding:14px 16px; margin-bottom:12px;">
                                <h4 style="color:#1565C0; font-family:'Barlow Condensed',sans-serif;
                                           font-weight:700; margin:0 0 8px 0; font-size:0.95rem;">
                                    OPPORTUNITIES</h4>
                                <ul style="margin:0; padding-left:18px; color:#444;
                                           font-size:0.88rem; line-height:1.5;">{o_items}</ul>
                            </div>""", unsafe_allow_html=True)
                        threats = swot.get("threats", [])
                        if threats:
                            t_items = "".join(f'<li style="margin-bottom:6px;">{t}</li>' for t in threats)
                            st.markdown(f"""
                            <div style="background:#FFF3E0; border-left:4px solid #F8C090;
                                        border-radius:0 8px 8px 0; padding:14px 16px;">
                                <h4 style="color:#E65100; font-family:'Barlow Condensed',sans-serif;
                                           font-weight:700; margin:0 0 8px 0; font-size:0.95rem;">
                                    THREATS</h4>
                                <ul style="margin:0; padding-left:18px; color:#444;
                                           font-size:0.88rem; line-height:1.5;">{t_items}</ul>
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

                # ── In-Market Campaigns ────────────────────
                campaigns = report.get("in_market_campaigns", [])
                if campaigns:
                    st.markdown("---")
                    render_section_label("In-Market Campaigns")
                    for camp in campaigns:
                        name = camp.get("campaign", "")
                        desc = camp.get("description", "")
                        if name and desc:
                            st.markdown(f"""
                            <div style="background:white; border-radius:10px; padding:16px 18px;
                                        margin-bottom:10px; border:1px solid #E0D8D0;
                                        border-left:4px solid {POPLIFE_BLUE};">
                                <strong style="font-family:'Barlow Condensed',sans-serif;
                                               font-size:0.95rem; color:#333;">
                                    {' '.join(name.split())}</strong>
                                <p style="color:#444; font-size:0.88rem; line-height:1.5;
                                          margin:6px 0 0 0;">{' '.join(desc.split())}</p>
                            </div>""", unsafe_allow_html=True)

                # ── Key Statistics ─────────────────────────
                key_stats = report.get("key_statistics", [])
                if key_stats:
                    st.markdown("---")
                    render_section_label("Key Statistics")
                    for stat in key_stats:
                        st.markdown(f"- {stat}")

                # ── Quotes ─────────────────────────────────
                quotes = report.get("quotes", [])
                if quotes:
                    st.markdown("---")
                    with st.expander("News Quotes & Sources", expanded=False):
                        for quote in quotes:
                            st.markdown(f"""
                            <div style="background:#FAFAFA; border-left:3px solid #CCC;
                                        padding:10px 14px; margin-bottom:8px; border-radius:0 6px 6px 0;
                                        font-size:0.88rem; color:#555; line-height:1.5;">
                                {quote}
                            </div>""", unsafe_allow_html=True)
