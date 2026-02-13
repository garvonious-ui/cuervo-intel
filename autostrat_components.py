"""
Autostrat UI Components
========================
Reusable Streamlit rendering functions for qualitative intelligence data.
Used by all autostrat dashboard pages.
"""

from __future__ import annotations

import streamlit as st


# ── NOPD Quadrant Cards ──────────────────────────────────────────────

NOPD_STYLES = {
    "needs": {"color": "#2ea3f2", "bg": "#F0F8FF", "label": "NEEDS"},
    "objections": {"color": "#D9534F", "bg": "#FFF5F5", "label": "OBJECTIONS"},
    "desires": {"color": "#5CB85C", "bg": "#F0FFF0", "label": "DESIRES"},
    "pain_points": {"color": "#F8C090", "bg": "#FFFBF5", "label": "PAIN POINTS"},
}


def render_nopd_cards(audience_profile: dict):
    """Render a 2x2 grid of Needs/Objections/Desires/Pain Points cards."""
    col1, col2 = st.columns(2)

    with col1:
        _render_single_nopd("needs", audience_profile.get("needs", []))
        _render_single_nopd("desires", audience_profile.get("desires", []))

    with col2:
        _render_single_nopd("objections", audience_profile.get("objections", []))
        _render_single_nopd("pain_points", audience_profile.get("pain_points", []))


def _render_single_nopd(key: str, items: list[str]):
    """Render a single NOPD card."""
    style = NOPD_STYLES[key]
    items_html = "".join(f"<li>{item}</li>" for item in items) if items else "<li>No data</li>"

    st.markdown(f"""
    <div style="background: {style['bg']}; border-left: 4px solid {style['color']};
                border-radius: 0 8px 8px 0; padding: 16px; margin-bottom: 12px;">
        <h4 style="color: {style['color']}; font-family: 'Barlow Condensed', sans-serif;
                   font-weight: 700; margin: 0 0 10px 0; font-size: 1rem;
                   letter-spacing: 1px;">{style['label']}</h4>
        <ul style="margin: 0; padding-left: 20px; color: #444; font-size: 0.92rem;
                   line-height: 1.5;">
            {items_html}
        </ul>
    </div>
    """, unsafe_allow_html=True)


# ── Verbatim Quotes ──────────────────────────────────────────────────

def render_verbatim_quotes(quotes: list[str], max_quotes: int = 8):
    """Render audience verbatim quotes in blockquote style."""
    for quote in quotes[:max_quotes]:
        st.markdown(f"""
        <blockquote style="border-left: 4px solid #F8C090; padding: 10px 16px;
                           margin: 8px 0; background: #F3EDE6;
                           border-radius: 0 8px 8px 0; font-style: italic;
                           color: #555; font-size: 0.92rem; line-height: 1.5;">
            "{quote}"
        </blockquote>
        """, unsafe_allow_html=True)


# ── Territory Cards ──────────────────────────────────────────────────

def render_territory_card(number: int, text: str):
    """Render a numbered strategic territory card."""
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #FDEBD6 0%, #FFF8F0 100%);
                border-radius: 10px; padding: 18px 20px; margin-bottom: 12px;
                border-left: 5px solid #2ea3f2;">
        <div style="display: flex; align-items: flex-start; gap: 14px;">
            <div style="background: #2ea3f2; color: white; border-radius: 50%;
                        min-width: 32px; height: 32px; display: flex;
                        align-items: center; justify-content: center;
                        font-weight: 700; font-size: 0.95rem; flex-shrink: 0;">{number}</div>
            <div style="font-family: 'Barlow Condensed', sans-serif; font-size: 1.05rem;
                        font-weight: 600; color: #333333; line-height: 1.4;">{text}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_territory_cards(territories: list[str]):
    """Render a list of numbered territory cards."""
    for i, territory in enumerate(territories, 1):
        render_territory_card(i, territory)


# ── Sentiment Badge ──────────────────────────────────────────────────

SENTIMENT_STYLES = {
    "positive": {"bg": "#C8E6C9", "color": "#2E7D32"},
    "negative": {"bg": "#FFCDD2", "color": "#C62828"},
    "mixed": {"bg": "#FFE0B2", "color": "#E65100"},
    "neutral": {"bg": "#E0E0E0", "color": "#616161"},
}


def sentiment_badge_html(sentiment: str) -> str:
    """Return HTML for an inline sentiment badge."""
    key = "neutral"
    if sentiment:
        low = sentiment.lower()
        if "positive" in low or "enthusiast" in low:
            key = "positive"
        elif "negative" in low:
            key = "negative"
        elif "mixed" in low or "skeptic" in low:
            key = "mixed"

    style = SENTIMENT_STYLES[key]
    label = key.capitalize()
    return (f'<span style="background: {style["bg"]}; color: {style["color"]}; '
            f'padding: 3px 10px; border-radius: 12px; font-size: 0.82rem; '
            f'font-weight: 600;">{label}</span>')


# ── Narrative Card ───────────────────────────────────────────────────

def render_narrative_card(title: str, body: str, accent_color: str = "#2ea3f2"):
    """Render a card with a title and narrative body text."""
    st.markdown(f"""
    <div style="background: white; border-radius: 10px; padding: 18px 20px;
                margin-bottom: 12px; border: 1px solid #E0D8D0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
        <h4 style="font-family: 'Barlow Condensed', sans-serif; font-weight: 700;
                   color: {accent_color}; margin: 0 0 10px 0; font-size: 1rem;">{title}</h4>
        <p style="color: #444; font-size: 0.92rem; line-height: 1.55; margin: 0;">{body}</p>
    </div>
    """, unsafe_allow_html=True)


# ── Creator Archetype Card ───────────────────────────────────────────

def render_creator_archetype(archetype: dict):
    """Render a creator archetype card."""
    name = archetype.get("archetype", "Unknown")
    desc = archetype.get("description", "")
    appeal = archetype.get("appeal", "")
    examples = archetype.get("examples", [])

    examples_html = ""
    if examples:
        examples_html = "<div style='margin-top: 8px; font-size: 0.85rem; color: #777;'>"
        examples_html += "<strong>Examples:</strong> " + "; ".join(examples[:3])
        examples_html += "</div>"

    appeal_html = ""
    if appeal:
        appeal_html = (f"<div style='margin-top: 8px; font-size: 0.88rem; color: #555;'>"
                       f"<strong>Appeal:</strong> {appeal}</div>")

    st.markdown(f"""
    <div style="background: white; border-radius: 10px; padding: 18px 20px;
                margin-bottom: 12px; border: 1px solid #E0D8D0;
                border-top: 3px solid #F8C090;">
        <h4 style="font-family: 'Barlow Condensed', sans-serif; font-weight: 700;
                   color: #333; margin: 0 0 8px 0; font-size: 1.05rem;">{name}</h4>
        <p style="color: #444; font-size: 0.92rem; line-height: 1.5; margin: 0;">{desc}</p>
        {appeal_html}
        {examples_html}
    </div>
    """, unsafe_allow_html=True)


# ── Data Availability Table ──────────────────────────────────────────

def render_data_availability(autostrat: dict):
    """Render a compact table showing which report types have data."""
    from autostrat_loader import REPORT_TYPE_LABELS
    rows = []
    for rt, label in REPORT_TYPE_LABELS.items():
        count = len(autostrat.get(rt, {}))
        identifiers = list(autostrat.get(rt, {}).keys())
        if count > 0:
            rows.append(f"**{label}**: {count} report(s) — {', '.join(identifiers)}")
    if rows:
        for row in rows:
            st.markdown(row)
    else:
        st.info("No autostrat reports loaded. Drop PDF exports into data/autostrat/pdfs/ "
                "and click 'Import PDFs'.")


# ── Sponsorship Suggestion Card ──────────────────────────────────────

# ── Performance Statistics Table ─────────────────────────────────────

def render_statistics_section(statistics: dict):
    """Render performance statistics as a compact metric grid."""
    all_posts = statistics.get("all_posts", {})
    if not any(all_posts.values()):
        return

    metrics = [
        ("Views", "views"),
        ("Likes", "likes"),
        ("Comments", "comments"),
    ]

    for label, key in metrics:
        min_val = all_posts.get(f"min_{key}", 0)
        max_val = all_posts.get(f"max_{key}", 0)
        median_val = all_posts.get(f"median_{key}", 0)
        avg_val = all_posts.get(f"avg_{key}", 0)

        if not any([min_val, max_val, median_val, avg_val]):
            continue

        st.markdown(f"""
        <div style="font-family: 'Barlow Condensed', sans-serif; font-weight: 600;
                    color: #555; font-size: 0.85rem; letter-spacing: 0.5px;
                    margin: 8px 0 4px 0;">{label}</div>
        """, unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Min", f"{min_val:,.0f}")
        with c2:
            st.metric("Max", f"{max_val:,.0f}")
        with c3:
            st.metric("Median", f"{median_val:,.0f}")
        with c4:
            st.metric("Avg", f"{avg_val:,.0f}")


# ── Top Post Card ───────────────────────────────────────────────────

def render_top_post_card(post: dict, label: str, accent: str = "#2ea3f2"):
    """Render a single top/bottom post card."""
    caption = post.get("caption", "")
    er = post.get("engagement_rate", 0)
    likes = post.get("likes", 0)
    comments = post.get("comments", 0)
    link = post.get("link", "")

    if not caption and not likes and not link:
        return

    link_html = ""
    if link:
        link_html = (f'<a href="{link}" target="_blank" style="color: #2ea3f2; '
                     f'font-size: 0.82rem; text-decoration: none;">View Post</a>')

    st.markdown(f"""
    <div style="background: white; border-radius: 10px; padding: 16px 18px;
                margin-bottom: 10px; border: 1px solid #E0D8D0;
                border-top: 3px solid {accent};">
        <div style="font-family: 'Barlow Condensed', sans-serif; font-weight: 700;
                    color: {accent}; font-size: 0.82rem; letter-spacing: 1px;
                    margin-bottom: 8px;">{label}</div>
        <p style="color: #444; font-size: 0.9rem; line-height: 1.45; margin: 0 0 10px 0;
                  display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;
                  overflow: hidden;">{caption}</p>
        <div style="display: flex; gap: 16px; flex-wrap: wrap; align-items: center;
                    font-size: 0.85rem; color: #666;">
            <span><strong>ER:</strong> {er}%</span>
            <span><strong>Likes:</strong> {likes:,}</span>
            <span><strong>Comments:</strong> {comments:,}</span>
            {link_html}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_top_posts_section(top_posts: dict):
    """Render all top post pairs (Most/Least) for Liked, Comments, Engaged."""
    pairs = [
        ("Liked", "most_liked", "least_liked"),
        ("Comments", "most_comments", "least_comments"),
        ("Engaged", "most_engaged", "least_engaged"),
    ]

    for pair_label, most_key, least_key in pairs:
        most = top_posts.get(most_key, {})
        least = top_posts.get(least_key, {})

        has_most = most.get("caption") or most.get("likes") or most.get("link")
        has_least = least.get("caption") or least.get("likes") or least.get("link")

        if not has_most and not has_least:
            continue

        col_m, col_l = st.columns(2)
        with col_m:
            render_top_post_card(most, f"MOST {pair_label.upper()}", "#5CB85C")
        with col_l:
            render_top_post_card(least, f"LEAST {pair_label.upper()}", "#D9534F")


def render_sponsorship_card(suggestion: dict):
    """Render a future sponsorship suggestion card."""
    cat = suggestion.get("category", "")
    why = suggestion.get("why_it_works", "")
    how = suggestion.get("how_to_activate", [])

    how_html = ""
    if how:
        items = "".join(f"<li>{h}</li>" for h in how[:5])
        how_html = (f"<div style='margin-top: 8px;'>"
                    f"<strong style='font-size: 0.85rem; color: #2ea3f2;'>How to Activate:</strong>"
                    f"<ul style='margin: 4px 0 0 0; padding-left: 18px; font-size: 0.88rem; "
                    f"color: #555;'>{items}</ul></div>")

    st.markdown(f"""
    <div style="background: white; border-radius: 10px; padding: 18px 20px;
                margin-bottom: 12px; border: 1px solid #E0D8D0;
                border-left: 4px solid #F8C090;">
        <h4 style="font-family: 'Barlow Condensed', sans-serif; font-weight: 700;
                   color: #333; margin: 0 0 8px 0; font-size: 1rem;">{cat}</h4>
        <p style="color: #444; font-size: 0.92rem; line-height: 1.5; margin: 0;">{why}</p>
        {how_html}
    </div>
    """, unsafe_allow_html=True)


# ── Section Header ───────────────────────────────────────────────────

def render_section_label(text: str):
    """Render a small uppercase section label."""
    st.markdown(f"""
    <div style="font-family: 'Barlow Condensed', sans-serif; font-size: 0.82rem;
                font-weight: 600; color: #2ea3f2; text-transform: uppercase;
                letter-spacing: 1.5px; margin: 20px 0 8px 0;">{text}</div>
    """, unsafe_allow_html=True)


# ── What Hits / What Misses ──────────────────────────────────────────

def render_hits_misses(what_hits: str, what_misses: str):
    """Render What Hits / What Misses in green/red containers."""
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="background: #F0FFF0; border-left: 4px solid #5CB85C;
                    border-radius: 0 8px 8px 0; padding: 14px 16px; margin-bottom: 12px;">
            <h4 style="color: #2E7D32; font-family: 'Barlow Condensed', sans-serif;
                       font-weight: 700; margin: 0 0 8px 0; font-size: 0.95rem;">WHAT HITS</h4>
            <p style="color: #444; font-size: 0.9rem; line-height: 1.5; margin: 0;">{what_hits}</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="background: #FFF5F5; border-left: 4px solid #D9534F;
                    border-radius: 0 8px 8px 0; padding: 14px 16px; margin-bottom: 12px;">
            <h4 style="color: #C62828; font-family: 'Barlow Condensed', sans-serif;
                       font-weight: 700; margin: 0 0 8px 0; font-size: 0.95rem;">WHAT MISSES</h4>
            <p style="color: #444; font-size: 0.9rem; line-height: 1.5; margin: 0;">{what_misses}</p>
        </div>
        """, unsafe_allow_html=True)


# ── Brand Mention Row ────────────────────────────────────────────────

def render_brand_mention(mention: dict):
    """Render a brand mention with sentiment badge."""
    brand = mention.get("brand", "Unknown")
    context = mention.get("context", "")
    sentiment = mention.get("sentiment", "")
    badge = sentiment_badge_html(sentiment)
    source = mention.get("source_label", "")
    source_id = mention.get("source_identifier", "")

    st.markdown(f"""
    <div style="background: white; border-radius: 8px; padding: 14px 18px;
                margin-bottom: 8px; border: 1px solid #E0D8D0;">
        <div style="display: flex; justify-content: space-between; align-items: center;
                    margin-bottom: 8px;">
            <strong style="font-family: 'Barlow Condensed', sans-serif; font-size: 1.05rem;
                          color: #333;">{brand}</strong>
            {badge}
        </div>
        <p style="color: #555; font-size: 0.9rem; line-height: 1.45; margin: 0;">{context}</p>
        <div style="margin-top: 6px; font-size: 0.8rem; color: #999;">
            Source: {source} — {source_id}
        </div>
    </div>
    """, unsafe_allow_html=True)
