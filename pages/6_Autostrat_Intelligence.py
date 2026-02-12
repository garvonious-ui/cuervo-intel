"""
Autostrat Intelligence Hub — Consolidated qualitative intelligence
from autostrat.ai reports. Combines Strategic Playbook, Conversation &
Trends, Profile Deep Dive, and Audience Intelligence into tabbed views.
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from config import CUSTOM_CSS, CHART_TEMPLATE, CHART_FONT, BRAND_COLORS
from autostrat_loader import (
    has_autostrat_data,
    # Playbook
    get_all_how_to_win, get_all_strategic_actions, get_all_brand_mentions,
    get_all_sponsorship_suggestions,
    # Conversation
    CONVERSATION_TYPES, REPORT_TYPE_LABELS, get_available_identifiers, get_report,
    # Audience
    get_all_audience_profiles,
    # Profile
    PROFILE_TYPES, get_section_across_reports,
    # Reference brands
    is_reference_brand, get_reference_profiles, get_competitor_identifiers,
)
from config import REFERENCE_BRAND_LABELS
from autostrat_components import (
    render_territory_cards, render_verbatim_quotes, render_section_label,
    render_sponsorship_card, render_brand_mention,
    render_narrative_card, render_creator_archetype,
    render_nopd_cards, render_hits_misses,
    sentiment_badge_html, NOPD_STYLES,
)

st.logo("logo.png")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
st.header("Autostrat Intelligence")

if "autostrat" not in st.session_state:
    st.warning("Go to the home page first to load data.")
    st.stop()

autostrat = st.session_state["autostrat"]
if not has_autostrat_data(autostrat):
    st.info("No autostrat reports loaded. Import PDFs from the home page.")
    st.stop()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
tab_playbook, tab_convo, tab_profile, tab_audience, tab_reference = st.tabs([
    "Strategic Playbook", "Conversation Deep Dive",
    "Profile Intelligence", "Audience Profiles",
    "Reference & Inspiration",
])

# ══════════════════════════════════════════════════════════════════════
# TAB 1 — Strategic Playbook (formerly Page 10)
# ══════════════════════════════════════════════════════════════════════

with tab_playbook:
    st.caption("Consolidated strategic intelligence from all autostrat reports")

    # ── Winning Territories ───────────────────────────────────────────
    all_htw = get_all_how_to_win(autostrat, exclude_reference=True)
    if all_htw:
        render_section_label("Winning Territories")
        st.caption("Strategic territories identified across all reports")

        all_territories = []
        territory_sources = {}
        for entry in all_htw:
            for territory in entry["how_to_win"].get("territories", []):
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

    # ── Audience Verbatims ────────────────────────────────────────────
    all_verbatims = []
    if all_htw:
        for entry in all_htw:
            all_verbatims.extend(entry["how_to_win"].get("audience_verbatims", []))

    if all_verbatims:
        render_section_label("Audience Verbatims")
        st.caption("Real audience quotes from across all reports")
        unique_verbatims = list(dict.fromkeys(all_verbatims))
        render_verbatim_quotes(unique_verbatims, max_quotes=12)
        st.markdown("---")

    # ── Opportunities vs. Gaps/Risks ──────────────────────────────────
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
                for gap_item in all_gaps[:6]:
                    st.error(gap_item)

        if all_strategic:
            st.markdown("---")
            render_section_label("Strategic Actions")
            for i, action in enumerate(all_strategic[:8], 1):
                st.markdown(f"**{i}.** {action}")

        st.markdown("---")

    # ── Sponsorship Playbook ──────────────────────────────────────────
    all_suggestions = get_all_sponsorship_suggestions(autostrat, exclude_reference=True)
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

    # ── Competitive Brand Mentions ────────────────────────────────────
    all_mentions = get_all_brand_mentions(autostrat)
    if all_mentions:
        render_section_label("Competitive Brand Mentions")
        st.caption("How brands appear in the conversation space")
        for mention in all_mentions[:8]:
            render_brand_mention(mention)


# ══════════════════════════════════════════════════════════════════════
# TAB 2 — Conversation Deep Dive (formerly Page 9)
# ══════════════════════════════════════════════════════════════════════

with tab_convo:

    # ── Report Selector ───────────────────────────────────────────────
    available = []
    for rt in CONVERSATION_TYPES + ["google_news"]:
        for ident in get_available_identifiers(autostrat, rt):
            available.append((rt, ident))

    if not available:
        st.info("No hashtag, keyword, or news reports available. Import autostrat PDFs.")
    else:
        options = {f"{REPORT_TYPE_LABELS.get(rt, rt)}: {ident.replace('_', ' ').title()}": (rt, ident)
                   for rt, ident in available}

        selected_label = st.selectbox("Select report", list(options.keys()), key="convo_report")
        report_type, identifier = options[selected_label]
        report = get_report(autostrat, report_type, identifier)

        if not report:
            st.warning("Report not found.")
        else:
            # ── Executive Summary ─────────────────────────────────────
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

            # ── Audience Profile ──────────────────────────────────────
            ap = report.get("audience_profile", {})
            if any(ap.get(k) for k in ["needs", "objections", "desires", "pain_points"]):
                render_section_label("Audience Profile")
                if ap.get("summary"):
                    st.markdown(ap["summary"])
                render_nopd_cards(ap)
                st.markdown("---")

            # ── Hashtag Analysis ──────────────────────────────────────
            ha = report.get("hashtag_analysis", {})
            if ha:
                if ha.get("summary"):
                    render_section_label("Hashtag Analysis")
                    st.markdown(ha["summary"])

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

            # ── Conversation Map ──────────────────────────────────────
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

            # ── Interesting Conversations ─────────────────────────────
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

            # ── Content Trends ────────────────────────────────────────
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

            # ── Creator Archetypes ────────────────────────────────────
            archetypes = report.get("creator_archetypes", [])
            if archetypes:
                render_section_label("Creator Archetypes")
                cols = st.columns(min(len(archetypes), 3))
                for i, arch in enumerate(archetypes):
                    with cols[i % len(cols)]:
                        render_creator_archetype(arch)
                st.markdown("---")

            # ── Brand Mentions ────────────────────────────────────────
            mentions = report.get("brand_mentions", [])
            if mentions:
                render_section_label("Brand Mentions")
                for mention in mentions:
                    render_brand_mention(mention)
                st.markdown("---")

            # ── In-Market Campaigns ───────────────────────────────────
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

            # ── How to Win ────────────────────────────────────────────
            hw = report.get("how_to_win", {})
            if hw.get("territories"):
                render_section_label("How to Win")
                if hw.get("summary"):
                    st.markdown(f"*{hw['summary']}*")
                render_territory_cards(hw["territories"])

                if hw.get("audience_verbatims"):
                    render_section_label("Audience Verbatims")
                    render_verbatim_quotes(hw["audience_verbatims"])


# ══════════════════════════════════════════════════════════════════════
# TAB 3 — Profile Intelligence (formerly Page 11)
# ══════════════════════════════════════════════════════════════════════

with tab_profile:

    platform = st.radio("Platform", ["Instagram", "TikTok"], horizontal=True, key="profile_plat")
    report_type_p = "instagram_profiles" if platform == "Instagram" else "tiktok_profiles"
    identifiers_p = get_competitor_identifiers(autostrat, report_type_p)

    if not identifiers_p:
        st.info(f"No {platform} profile reports available. Import autostrat PDFs from the home page.")
    else:
        selected_p = st.selectbox("Select profile", identifiers_p,
                                  format_func=lambda x: x.replace("_", " ").title(),
                                  key="profile_sel")
        report_p = get_report(autostrat, report_type_p, selected_p)

        if not report_p:
            st.warning("Report not found.")
        else:
            display_name = selected_p.replace("_", " ").title()

            # ── Snapshot KPIs ─────────────────────────────────────────
            snapshot = report_p.get("snapshot", {})
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

            # ── Creator Summary ───────────────────────────────────────
            cs = report_p.get("creator_summary", {})
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

            # ── Audience Profile (NOPD) ───────────────────────────────
            ap = report_p.get("audience_profile", {})
            if any(ap.get(k) for k in ["needs", "objections", "desires", "pain_points"]):
                render_section_label("Audience Profile")
                if ap.get("summary"):
                    st.markdown(ap["summary"])
                render_nopd_cards(ap)
                st.markdown("---")

            # ── Statistics Chart ──────────────────────────────────────
            stats = report_p.get("statistics", {})
            all_posts = stats.get("all_posts", {})
            if any(all_posts.values()):
                render_section_label("Performance Statistics")

                metrics = ["views", "likes", "comments"]
                stat_types = ["min", "max", "median", "avg"]
                colors = {"min": "#A3C4D9", "max": "#D9534F", "median": "#F8C090", "avg": "#2ea3f2"}

                fig_stats = go.Figure()
                for stat in stat_types:
                    values = [all_posts.get(f"{stat}_{m}", 0) for m in metrics]
                    fig_stats.add_trace(go.Bar(
                        name=stat.capitalize(), x=metrics,
                        y=values, marker_color=colors[stat],
                        text=[f"{v:,.0f}" for v in values], textposition="outside",
                    ))
                fig_stats.update_layout(
                    barmode="group", template=CHART_TEMPLATE, font=CHART_FONT,
                    height=380, yaxis_title="Count",
                    legend=dict(orientation="h", y=1.12),
                )
                st.plotly_chart(fig_stats, use_container_width=True)
                st.markdown("---")

            # ── Top & Bottom Posts ────────────────────────────────────
            top_posts = report_p.get("top_posts", {})
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
                        er_val = post.get("engagement_rate", 0)
                        likes = post.get("likes", 0)
                        comments = post.get("comments", 0)
                        link = post.get("link", "")

                        st.markdown(f"**{label}**")
                        st.markdown(f'"{caption}..."')
                        st.caption(f"ER: {er_val}% | Likes: {likes:,} | Comments: {comments:,}")
                        if link:
                            st.markdown(f"[View post]({link})")
                st.markdown("---")

            # ── Posting & Engagement Analysis ─────────────────────────
            ea = report_p.get("engagement_analysis", {})
            pa = report_p.get("posting_analysis", {})
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

            # ── Sponsorship Intelligence ──────────────────────────────
            sponsorships = report_p.get("sponsorships", {})
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

            # ── Future Sponsorship Suggestions ────────────────────────
            suggestions = report_p.get("future_sponsorship_suggestions", [])
            if suggestions:
                st.markdown("---")
                render_section_label("Future Sponsorship Opportunities")
                cols = st.columns(min(len(suggestions), 2))
                for i, sug in enumerate(suggestions):
                    with cols[i % len(cols)]:
                        render_sponsorship_card(sug)

            # ── How to Win ────────────────────────────────────────────
            hw = report_p.get("how_to_win", {})
            if hw.get("territories"):
                st.markdown("---")
                render_section_label("How to Win")
                if hw.get("summary"):
                    st.markdown(f"*{hw['summary']}*")
                render_territory_cards(hw["territories"])
                if hw.get("audience_verbatims"):
                    render_section_label("Audience Verbatims")
                    render_verbatim_quotes(hw["audience_verbatims"])

            # ── Cross-Brand Snapshot Comparison ───────────────────────
            all_snapshots = {k: v for k, v in
                             get_section_across_reports(autostrat, report_type_p, "snapshot").items()
                             if not is_reference_brand(k)}
            if len(all_snapshots) > 1:
                st.markdown("---")
                render_section_label(f"Cross-Profile Comparison ({platform})")
                rows_snap = []
                for ident, snap in all_snapshots.items():
                    rows_snap.append({
                        "Profile": ident.replace("_", " ").title(),
                        "Followers": snap.get("followers", 0),
                        "Avg Likes": snap.get("avg_likes", 0),
                        "Avg Comments": snap.get("avg_comments", 0),
                        "Avg ER %": snap.get("avg_engagement_rate", 0),
                    })
                comp_snap_df = pd.DataFrame(rows_snap)
                st.dataframe(comp_snap_df, hide_index=True, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════
# TAB 4 — Audience Profiles (formerly Page 8)
# ══════════════════════════════════════════════════════════════════════

with tab_audience:

    all_profiles = get_all_audience_profiles(autostrat, exclude_reference=True)
    if not all_profiles:
        st.info("No audience profile data found in loaded reports.")
    else:
        identifiers_a = list(dict.fromkeys(p["identifier"] for p in all_profiles))
        identifier_labels = {ident: ident.replace("_", " ").title() for ident in identifiers_a}

        view = st.radio("View", ["Single Profile", "Comparison"], horizontal=True, key="aud_view")

        if view == "Single Profile":
            selected_a = st.selectbox("Select profile/topic", identifiers_a,
                                      format_func=lambda x: identifier_labels[x],
                                      key="aud_profile")

            matching = [p for p in all_profiles if p["identifier"] == selected_a]

            if len(matching) > 1:
                tabs_a = st.tabs([p["source_label"] for p in matching])
                for tab_a, profile_entry in zip(tabs_a, matching):
                    with tab_a:
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
            st.caption("Compare audience profiles across reports side by side")

            selected_ids = st.multiselect(
                "Select profiles to compare", identifiers_a,
                default=identifiers_a[:min(4, len(identifiers_a))],
                format_func=lambda x: identifier_labels[x],
                key="aud_compare",
            )

            if not selected_ids:
                st.info("Select at least one profile to compare.")
            else:
                profiles_to_compare = []
                for ident in selected_ids:
                    matching = [p for p in all_profiles if p["identifier"] == ident]
                    if matching:
                        profiles_to_compare.append(matching[0])

                if not profiles_to_compare:
                    st.info("No profiles found for selected items.")
                else:
                    for dimension in ["needs", "objections", "desires", "pain_points"]:
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

        # ── Sentiment Landscape ───────────────────────────────────────
        all_mentions_a = get_all_brand_mentions(autostrat)
        if all_mentions_a:
            st.markdown("---")
            render_section_label("Brand Sentiment Landscape")
            st.caption("How brands appear in conversation across hashtag and keyword reports")
            for mention in all_mentions_a[:10]:
                render_brand_mention(mention)


# ══════════════════════════════════════════════════════════════════════
# TAB 5 — Reference & Inspiration (non-tequila brands)
# ══════════════════════════════════════════════════════════════════════

with tab_reference:
    st.caption(
        "Non-competitive brands studied for content strategy inspiration. "
        "These are not tequila competitors — they are reference points for "
        "creative strategy, audience engagement, and content formats."
    )

    ref_profiles = get_reference_profiles(autostrat)

    if not ref_profiles:
        st.info(
            "No reference brand reports loaded. Import autostrat PDFs for "
            "inspiration brands (e.g., Duolingo, Poppi) from the home page."
        )
    else:
        ref_platform = st.radio(
            "Platform", ["Instagram", "TikTok"],
            horizontal=True, key="ref_plat",
        )
        ref_type = "instagram_profiles" if ref_platform == "Instagram" else "tiktok_profiles"

        available_refs = {
            k: v for k, v in ref_profiles.items()
            if v["report_type"] == ref_type
        }

        if not available_refs:
            st.info(f"No {ref_platform} reference brand reports available.")
        else:
            ref_options = {
                REFERENCE_BRAND_LABELS.get(v["identifier"], v["identifier"].replace("_", " ").title()): k
                for k, v in available_refs.items()
            }
            selected_ref_label = st.selectbox(
                "Select reference brand",
                list(ref_options.keys()),
                key="ref_brand_sel",
            )
            ref_key = ref_options[selected_ref_label]
            ref_data = available_refs[ref_key]
            report_r = ref_data["report"]
            display_name_r = REFERENCE_BRAND_LABELS.get(
                ref_data["identifier"],
                ref_data["identifier"].replace("_", " ").title(),
            )

            # ── Snapshot KPIs ─────────────────────────────────────────
            snapshot_r = report_r.get("snapshot", {})
            if any(snapshot_r.values()):
                render_section_label("Profile Snapshot")
                rc1, rc2, rc3, rc4, rc5 = st.columns(5)
                with rc1:
                    st.metric("Followers", f"{snapshot_r.get('followers', 0):,}")
                with rc2:
                    st.metric("Following", f"{snapshot_r.get('following', 0):,}")
                with rc3:
                    st.metric("Avg Likes", f"{snapshot_r.get('avg_likes', 0):,}")
                with rc4:
                    st.metric("Avg Comments", f"{snapshot_r.get('avg_comments', 0):,}")
                with rc5:
                    er_r = snapshot_r.get("avg_engagement_rate", 0)
                    st.metric("Avg ER", f"{er_r}%")
                st.markdown("---")

            # ── Creator Summary ───────────────────────────────────────
            cs_r = report_r.get("creator_summary", {})
            if cs_r.get("topline"):
                render_section_label("Brand Summary")
                st.markdown(f"**{display_name_r}** — {cs_r['topline']}")
                if cs_r.get("what_it_means"):
                    st.markdown(f"*{cs_r['what_it_means']}*")
                if cs_r.get("common_themes"):
                    themes_str_r = " | ".join(cs_r["common_themes"])
                    st.caption(f"Common themes: {themes_str_r}")
                if cs_r.get("what_hits") or cs_r.get("what_misses"):
                    render_hits_misses(cs_r.get("what_hits", ""), cs_r.get("what_misses", ""))
                st.markdown("---")

            # ── Audience Profile (NOPD) ───────────────────────────────
            ap_r = report_r.get("audience_profile", {})
            if any(ap_r.get(k) for k in ["needs", "objections", "desires", "pain_points"]):
                render_section_label("Audience Profile")
                if ap_r.get("summary"):
                    st.markdown(ap_r["summary"])
                render_nopd_cards(ap_r)
                st.markdown("---")

            # ── Statistics Chart ──────────────────────────────────────
            stats_r = report_r.get("statistics", {})
            all_posts_r = stats_r.get("all_posts", {})
            if any(all_posts_r.values()):
                render_section_label("Performance Statistics")
                metrics_r = ["views", "likes", "comments"]
                stat_types_r = ["min", "max", "median", "avg"]
                colors_r = {"min": "#A3C4D9", "max": "#D9534F", "median": "#F8C090", "avg": "#2ea3f2"}

                fig_stats_r = go.Figure()
                for stat_r in stat_types_r:
                    values_r = [all_posts_r.get(f"{stat_r}_{m}", 0) for m in metrics_r]
                    fig_stats_r.add_trace(go.Bar(
                        name=stat_r.capitalize(), x=metrics_r,
                        y=values_r, marker_color=colors_r[stat_r],
                        text=[f"{v:,.0f}" for v in values_r], textposition="outside",
                    ))
                fig_stats_r.update_layout(
                    barmode="group", template=CHART_TEMPLATE, font=CHART_FONT,
                    height=380, yaxis_title="Count",
                    legend=dict(orientation="h", y=1.12),
                )
                st.plotly_chart(fig_stats_r, use_container_width=True)
                st.markdown("---")

            # ── Top & Bottom Posts ────────────────────────────────────
            top_posts_r = report_r.get("top_posts", {})
            if top_posts_r:
                render_section_label("Top & Bottom Posts")
                cols_r = st.columns(min(len(top_posts_r), 3))
                labels_r = {
                    "most_liked": "Most Liked",
                    "most_engaged": "Most Engaged",
                    "least_engaged": "Least Engaged",
                    "least_liked": "Least Liked",
                    "most_comments": "Most Comments",
                }
                for i_r, (key_r, post_r) in enumerate(top_posts_r.items()):
                    with cols_r[i_r % len(cols_r)]:
                        label_r = labels_r.get(key_r, key_r.replace("_", " ").title())
                        caption_r = post_r.get("caption", "N/A")[:120]
                        er_val_r = post_r.get("engagement_rate", 0)
                        likes_r = post_r.get("likes", 0)
                        comments_r = post_r.get("comments", 0)
                        link_r = post_r.get("link", "")

                        st.markdown(f"**{label_r}**")
                        st.markdown(f'"{caption_r}..."')
                        st.caption(f"ER: {er_val_r}% | Likes: {likes_r:,} | Comments: {comments_r:,}")
                        if link_r:
                            st.markdown(f"[View post]({link_r})")
                st.markdown("---")

            # ── Posting & Engagement Analysis ─────────────────────────
            ea_r = report_r.get("engagement_analysis", {})
            pa_r = report_r.get("posting_analysis", {})
            if ea_r.get("summary") or pa_r.get("summary"):
                render_section_label("Engagement & Posting Analysis")
                col1_r, col2_r = st.columns(2)
                with col1_r:
                    if ea_r.get("summary"):
                        render_narrative_card("Engagement Analysis", ea_r["summary"])
                with col2_r:
                    if pa_r.get("summary"):
                        render_narrative_card("Posting Analysis", pa_r["summary"])
                st.markdown("---")

            # ── Sponsorship Intelligence ──────────────────────────────
            sponsorships_r = report_r.get("sponsorships", {})
            if sponsorships_r.get("summary") or sponsorships_r.get("categories"):
                render_section_label("Sponsorship Intelligence")
                if sponsorships_r.get("summary"):
                    st.markdown(sponsorships_r["summary"])
                col1_r, col2_r = st.columns(2)
                with col1_r:
                    if sponsorships_r.get("categories"):
                        st.markdown("**Current Categories:** " + ", ".join(sponsorships_r["categories"]))
                with col2_r:
                    if sponsorships_r.get("companies"):
                        st.markdown("**Current Partners:** " + ", ".join(sponsorships_r["companies"]))
                if sponsorships_r.get("integration_summary"):
                    st.caption(sponsorships_r["integration_summary"])

            # ── How to Win ────────────────────────────────────────────
            hw_r = report_r.get("how_to_win", {})
            if hw_r.get("territories"):
                st.markdown("---")
                render_section_label("How to Win")
                if hw_r.get("summary"):
                    st.markdown(f"*{hw_r['summary']}*")
                render_territory_cards(hw_r["territories"])
                if hw_r.get("audience_verbatims"):
                    render_section_label("Audience Verbatims")
                    render_verbatim_quotes(hw_r["audience_verbatims"])
