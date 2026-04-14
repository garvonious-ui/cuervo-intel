"""
UI Components — Treatment C (dark hero + light KPI + structured cards)

Reusable Streamlit components for rendering the branded Poplife Treatment C
layout. All components emit plain HTML via st.markdown(..., unsafe_allow_html=True)
and rely on CSS classes defined in config.POPLIFE_TREATMENT_C_CSS.

Core layout helpers:
- render_page_hero: dark editorial hero block (kicker + headline + subtitle + stats)
- render_kpi_section_label: section divider with peach accent + border line
- render_poplife_note: styled info box (default / success / danger / warning)
- render_content_card_open / render_content_card_close: generic card wrapper

Page 1 scorecard helpers:
- render_kpi_card: light KPI card (label + value + optional status pill or meta chip)
- render_status_pill: helper that returns a status dict for render_kpi_card

Page 3 (Strategy) helpers:
- render_north_star: dark north star callout
- render_pillar_card: content pillar card with actual/target/gap
- render_sku_card: SKU strategy card
- render_sku_usage_card: SKU usage-by-occasion card (dark header + occasion list)
- render_engine_card: execution engine card
- render_voice_card: tone of voice principle card
- render_ig_format_card: IG format mix card
- render_partner_event: year-round partner event card
- render_quarter_card: quarterly cultural calendar card
- render_swot_card: SWOT 2x2 card
- render_connect_callout: Content Mix funnel "Connect always-on" callout

Page 1, 4 & 5 helpers:
- render_nopd_card: Needs/Objections/Pain/Desires card (single quadrant)
- render_nopd_grid: full 4-quadrant NOPD grid (drop-in for autostrat.render_nopd_cards)
- render_verbatim_card: italic pull-quote with peach left border
- render_territory_card: numbered peach-gradient territory card (title optional)
- render_territory_list: auto-numbered wrapper for a list of territory strings
- render_brand_mention: brand mention card with sentiment badge
- render_sentiment_grid: 3-cell Positive/Neutral/Negative breakdown
- render_wtm_card: "What This Means for Hero" card (5 variants)
- render_news_narrative: trending news narrative card
"""

from __future__ import annotations

import html
from typing import Optional

import streamlit as st


# ═══════════════════════════════════════════════════════════════════════════
# Page hero — dark editorial block
# ═══════════════════════════════════════════════════════════════════════════

def render_page_hero(
    title: str,
    kicker: str,
    subtitle: str,
    stats: list[dict],
    accent_color: str = "#F8C090",
) -> None:
    """
    Render the dark editorial hero block at the top of a page.

    Args:
        title: display headline, rendered uppercase (e.g. "The Mirror")
        kicker: small label above the headline (e.g. "Cuervo · Brand Performance")
        subtitle: descriptive line below the headline
        stats: list of {"value": str, "label": str} — 3-4 inline stats
        accent_color: peach by default; currently informational (CSS pins the peach)
    """
    stats_html = ""
    for s in stats:
        v = html.escape(str(s.get("value", "")))
        lbl = html.escape(str(s.get("label", "")))
        stats_html += (
            f'<div class="inline-stat">'
            f'<div class="value">{v}</div>'
            f'<div class="label">{lbl}</div>'
            f'</div>'
        )

    block = f"""
<header class="page-hero">
  <div class="kicker">{html.escape(kicker)}</div>
  <h1>{html.escape(title)}</h1>
  <p class="subtitle">{html.escape(subtitle)}</p>
  <div class="inline-stats">{stats_html}</div>
</header>
"""
    st.markdown(block, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# KPI card — light, with optional status pill or meta chip
# ═══════════════════════════════════════════════════════════════════════════

def render_kpi_card(
    label: str,
    value: str,
    status: Optional[dict] = None,
    meta: Optional[str] = None,
    hero: bool = False,
) -> None:
    """
    Render a single KPI card.

    Args:
        label: uppercase micro-label above the value
        value: the big number (already formatted with commas, e.g. "21,268")
        status: optional dict from render_status_pill — renders a status pill
        meta: optional str — renders a gray meta chip (alternative to status)
        hero: if True, renders the larger hero variant with peach top border

    Exactly one of `status` or `meta` should be supplied (or neither, for bare cards).
    """
    classes = "kpi-card hero" if hero else "kpi-card"
    label_safe = html.escape(label)
    value_safe = html.escape(value)

    pill_html = ""
    if status is not None:
        direction = status.get("direction", "neutral")
        delta = html.escape(str(status.get("delta", "")))
        target_text = html.escape(str(status.get("target_text", "")))
        arrow = {"up": "▲", "down": "▼", "neutral": "●"}.get(direction, "●")
        pill_class = {
            "up": "status-pill success",
            "down": "status-pill danger",
            "neutral": "status-pill neutral",
        }.get(direction, "status-pill neutral")
        pill_inner = (
            f'<span class="arrow">{arrow}</span> {delta} '
            f'<span class="target">{target_text}</span>'
        )
        pill_html = f'<div class="pill-row"><span class="{pill_class}">{pill_inner}</span></div>'
    elif meta is not None:
        pill_html = f'<div class="pill-row"><span class="meta-chip">{html.escape(meta)}</span></div>'

    card = (
        f'<div class="{classes}">'
        f'<div class="label">{label_safe}</div>'
        f'<div class="value">{value_safe}</div>'
        f'{pill_html}'
        f'</div>'
    )
    st.markdown(card, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# Section label — peach accent + border line
# ═══════════════════════════════════════════════════════════════════════════

def render_kpi_section_label(text: str) -> None:
    """
    Render a KPI section divider (uppercase label with peach accent line before
    and border line after). Named `render_kpi_section_label` to avoid clashing
    with the simpler `render_section_label` in autostrat_components.py.
    """
    st.markdown(
        f'<div class="section-label">{html.escape(text)}</div>',
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Status pill helper — returns dict (does not render)
# ═══════════════════════════════════════════════════════════════════════════

def render_status_pill(
    value: float,
    target,
    format: str = "number",
) -> Optional[dict]:
    """
    Compute a status pill descriptor from a value and a target.

    Args:
        value: the current metric value
        target: a numeric target. If a tuple/list is passed (range target),
                returns None so the caller can fall back to meta=.
        format: 'number' (raw +/-), 'percent' (adds %), 'thousand' (≥1000 → +38K)

    Returns:
        dict with keys: direction ('up'/'down'/'neutral'),
                        delta (formatted string e.g. '+16'),
                        target_text (e.g. 'vs 100 target')
        Or None if target is a range (tuple/list).
    """
    if target is None or isinstance(target, (tuple, list)):
        return None

    try:
        v = float(value)
        t = float(target)
    except (TypeError, ValueError):
        return None

    diff = v - t

    if abs(diff) < 0.5 and format != "percent":
        direction = "neutral"
    elif abs(diff) < 0.05 and format == "percent":
        direction = "neutral"
    elif diff > 0:
        direction = "up"
    else:
        direction = "down"

    # Format the delta
    if format == "percent":
        delta_str = f"{diff:+.0f}%"
        target_text = f"vs {t:.0f}% target"
    elif format == "thousand":
        if abs(diff) >= 1000:
            delta_str = f"{'+' if diff >= 0 else '-'}{abs(diff) / 1000:.0f}K"
        else:
            delta_str = f"{diff:+,.0f}"
        if abs(t) >= 1000:
            target_text = f"vs {t / 1000:.0f}K"
        else:
            target_text = f"vs {t:,.0f}"
    else:  # 'number'
        delta_str = f"{diff:+,.0f}"
        target_text = f"vs {t:,.0f} target"

    return {
        "direction": direction,
        "delta": delta_str,
        "target_text": target_text,
    }


# ═══════════════════════════════════════════════════════════════════════════
# Poplife note — styled info box (replaces Streamlit st.info)
# ═══════════════════════════════════════════════════════════════════════════

def render_poplife_note(body_html: str, variant: str = "default") -> None:
    """
    Render a styled info box. `body_html` is injected as-is (caller is
    responsible for escaping); this allows <strong> emphasis and inline spans.

    Args:
        body_html: inner HTML content
        variant: 'default' (peach) | 'success' (green) | 'danger' (red) | 'warning' (orange)
    """
    cls = "poplife-note"
    if variant in ("success", "danger", "warning"):
        cls = f"poplife-note {variant}"
    st.markdown(f'<div class="{cls}">{body_html}</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# North Star callout — Page 3 dark block
# ═══════════════════════════════════════════════════════════════════════════

def render_north_star(title: str, tagline: str, body: str, label: str = "Our North Star") -> None:
    """Render the North Star dark callout (Page 3)."""
    st.markdown(
        f"""
<div class="north-star">
  <div class="ns-label">{html.escape(label)}</div>
  <div class="ns-title">{html.escape(title)}</div>
  <div class="ns-tagline">{html.escape(tagline)}</div>
  <div class="ns-body">{html.escape(body)}</div>
</div>
""",
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Content card — open/close helpers for wrapping arbitrary content
# ═══════════════════════════════════════════════════════════════════════════

def render_content_card_open(
    title: Optional[str] = None,
    caption: Optional[str] = None,
    tight: bool = False,
) -> None:
    """Open a content card. Follow with render_content_card_close()."""
    cls = "content-card tight" if tight else "content-card"
    head = ""
    if title:
        head += f'<h3>{html.escape(title)}</h3>'
    if caption:
        head += f'<div class="card-caption">{html.escape(caption)}</div>'
    st.markdown(f'<div class="{cls}">{head}', unsafe_allow_html=True)


def render_content_card_close() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# Page 3: Pillar card
# ═══════════════════════════════════════════════════════════════════════════

def render_pillar_card(
    name: str,
    actual_pct: float,
    target_pct: float,
    description: str,
    post_count: int,
    avg_eng: float,
    accent_color: Optional[str] = None,
) -> None:
    """
    Render a single content pillar card with actual/target/gap.

    Args:
        accent_color: optional hex color (e.g. "#D4956A"). When set, overrides the
            default peach left-border via an inline CSS variable --accent-color.
            The pillar-card-detail CSS rule consumes var(--accent-color, #F8C090).
    """
    gap_pp = actual_pct - target_pct
    if abs(gap_pp) < 0.5:
        gap_class = "gap-up"
        gap_arrow = "●"
        gap_sign = "on target"
    elif gap_pp > 0:
        gap_class = "gap-up"
        gap_arrow = "▲"
        gap_sign = f"+{gap_pp:.0f} pp"
    else:
        gap_class = "gap-down"
        gap_arrow = "▼"
        gap_sign = f"{gap_pp:.0f} pp"

    style_attr = f' style="--accent-color: {accent_color}"' if accent_color else ""
    # Single-line HTML to avoid Streamlit's 4-space markdown-code-block trap
    st.markdown(
        f'<div class="pillar-card-detail"{style_attr}>'
        f'<div class="pillar-name">{html.escape(name)}</div>'
        f'<div class="pillar-pct-row">'
        f'<span class="pct-badge">{actual_pct:.0f}%</span>'
        f'<span class="pct-target">Target {target_pct:.0f}%</span>'
        f'</div>'
        f'<div class="pillar-desc">{html.escape(description)}</div>'
        f'<div class="pillar-stats">'
        f'<span><strong>{post_count}</strong> posts</span>'
        f'<span>Avg Eng <strong>{avg_eng:,.0f}</strong></span>'
        f'<span class="{gap_class}">{gap_arrow} {gap_sign}</span>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Page 3: SKU card
# ═══════════════════════════════════════════════════════════════════════════

def render_sku_card(name: str, energy: str, occasions: str) -> None:
    """Render a SKU strategy card."""
    st.markdown(
        f"""
<div class="sku-card">
  <h4>{html.escape(name)}</h4>
  <div class="sku-energy">{html.escape(energy)}</div>
  <div class="sku-occasions">{html.escape(occasions)}</div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_sku_usage_card(name: str, occasions: list) -> None:
    """Render a SKU card listing the occasions that should feature this variant.

    Used on Page 3 Tab 2 to visualize the "Role of Variants" usage matrix —
    one card per SKU, each listing the occasions it leads. An occasion can
    appear on multiple cards if it maps to multiple SKUs.

    Treatment C layout: dark header band with accent-colored SKU name and a
    count pill, light body with an occasion list.
    """
    # Per-SKU accent variant class (hooks into .sku-usage-card.tradicional / .rtds).
    variant = name.lower().replace(" ", "")
    if variant == "rtd":
        variant = "rtds"
    items_html = "".join(f"<li>{html.escape(occ)}</li>" for occ in occasions)
    count_label = f"{len(occasions)} OCCASION" + ("S" if len(occasions) != 1 else "")
    # Note: use <div class="sku-name"> instead of <h4> — Streamlit's heading
    # interceptor ("stHeadingWithActionElements") hoists h1-h6 out of their
    # parent container for anchor linking, which breaks the flex layout.
    st.markdown(
        f'<div class="sku-usage-card {variant}">'
        f'<div class="header"><div class="sku-name">{html.escape(name)}</div>'
        f'<span class="count-pill">{count_label}</span></div>'
        f'<div class="body"><ul>{items_html}</ul></div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Page 3: Execution engine card
# ═══════════════════════════════════════════════════════════════════════════

def render_engine_card(name: str, description: str) -> None:
    """Render an execution engine card."""
    st.markdown(
        f"""
<div class="engine-card">
  <h4>{html.escape(name)}</h4>
  <p>{html.escape(description)}</p>
</div>
""",
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Page 3: Voice card (tone of voice principle)
# ═══════════════════════════════════════════════════════════════════════════

def render_voice_card(name: str, detail: str) -> None:
    """Render a tone of voice principle card (stacked)."""
    st.markdown(
        f"""
<div class="voice-card">
  <div class="voice-name">{html.escape(name)}</div>
  <div class="voice-detail">{html.escape(detail)}</div>
</div>
""",
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Page 3: IG format mix card
# ═══════════════════════════════════════════════════════════════════════════

def render_ig_format_card(pct: float, name: str, role: str, variant: str = "reels") -> None:
    """Render an IG format mix card. variant: reels | carousel | static | story"""
    v = variant if variant in ("reels", "carousel", "static", "story") else "reels"
    st.markdown(
        f"""
<div class="ig-format-card {v}">
  <div class="pct {v}">{pct:.0f}%</div>
  <div class="fmt-name">{html.escape(name)}</div>
  <div class="fmt-role">{html.escape(role)}</div>
</div>
""",
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Page 3: Partner event card
# ═══════════════════════════════════════════════════════════════════════════

def render_partner_event(emoji: str, name: str, description: str) -> None:
    """Render a year-round partner event card."""
    st.markdown(
        f"""
<div class="partner-event">
  <h4><span class="emoji">{html.escape(emoji)}</span>{html.escape(name)}</h4>
  <p>{html.escape(description)}</p>
</div>
""",
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Page 3: Quarterly calendar card
# ═══════════════════════════════════════════════════════════════════════════

def render_quarter_card(
    quarter: str,
    moments: str,
    angle: str,
    variant: str = "q1",
) -> None:
    """Render a quarterly cultural calendar card. variant: q1 | q2 | q3 | q4"""
    v = variant if variant in ("q1", "q2", "q3", "q4") else "q1"
    st.markdown(
        f"""
<div class="quarter-card {v}">
  <h4>{html.escape(quarter)}</h4>
  <div class="q-moments">{html.escape(moments)}</div>
  <div class="q-angle">{html.escape(angle)}</div>
</div>
""",
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Page 3 & 5: SWOT card
# ═══════════════════════════════════════════════════════════════════════════

def render_swot_card(variant: str, label: str, items: list[str]) -> None:
    """
    Render one quadrant of a SWOT 2x2 grid.

    Args:
        variant: 'strength' | 'weakness' | 'opportunity' | 'threat'
        label: header text (e.g. 'Strengths')
        items: list of bullet strings
    """
    v = variant if variant in ("strength", "weakness", "opportunity", "threat") else "strength"
    lis = "".join(f"<li>{html.escape(i)}</li>" for i in items)
    st.markdown(
        f"""
<div class="swot-card {v}">
  <div class="swot-label">{html.escape(label)}</div>
  <ul>{lis}</ul>
</div>
""",
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Page 3: Connect callout (Content Mix Funnel)
# ═══════════════════════════════════════════════════════════════════════════

def render_connect_callout(title: str, body: str) -> None:
    """Render the 'Connect — Always On' callout under the content mix funnel."""
    st.markdown(
        f"""
<div class="connect-callout">
  <h4>{html.escape(title)}</h4>
  <p>{html.escape(body)}</p>
</div>
""",
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Page 4 & 5: NOPD card
# ═══════════════════════════════════════════════════════════════════════════

def render_nopd_card(variant: str, label: str, items: list[str]) -> None:
    """
    Render one quadrant of a NOPD (Needs/Objections/Pain/Desires) 2x2 grid.

    Args:
        variant: 'needs' | 'desires' | 'objections' | 'pain'
        label: header text (e.g. 'Needs — Jose Cuervo')
        items: list of bullet strings
    """
    v = variant if variant in ("needs", "desires", "objections", "pain") else "needs"
    lis = "".join(f"<li>{html.escape(str(i))}</li>" for i in items if i) or "<li>No data</li>"
    # Single-line HTML to avoid Streamlit's 4-space markdown-code-block trap
    st.markdown(
        f'<div class="nopd-card {v}"><h4>{html.escape(label)}</h4><ul>{lis}</ul></div>',
        unsafe_allow_html=True,
    )


def render_nopd_grid(audience_profile: dict, hero_label: str = "") -> None:
    """
    Render all four NOPD quadrants (Needs / Desires / Objections / Pain Points)
    in a 2x2 grid using Treatment C cards. Drop-in replacement for
    autostrat_components.render_nopd_cards.

    Args:
        audience_profile: dict with optional keys 'needs', 'desires',
            'objections', 'pain_points'. Any missing key renders as a "No data"
            card rather than being omitted, so the 2x2 grid always looks complete.
        hero_label: optional suffix for the card headers (e.g. "Jose Cuervo"
            renders headers like "Needs — Jose Cuervo"). Empty string by default.
    """
    if not audience_profile:
        return
    suffix = f" — {hero_label}" if hero_label else ""

    col1, col2 = st.columns(2)
    with col1:
        render_nopd_card("needs", f"Needs{suffix}", audience_profile.get("needs") or [])
        render_nopd_card("desires", f"Desires{suffix}", audience_profile.get("desires") or [])
    with col2:
        render_nopd_card("objections", f"Objections{suffix}", audience_profile.get("objections") or [])
        render_nopd_card("pain", f"Pain Points{suffix}", audience_profile.get("pain_points") or [])


# ═══════════════════════════════════════════════════════════════════════════
# Page 1, 4: Verbatim pull-quote card
# ═══════════════════════════════════════════════════════════════════════════

def render_verbatim_card(quote: str) -> None:
    """
    Render an italic audience verbatim as a Treatment C pull-quote card with
    a peach left border. Drop-in replacement for
    autostrat_components.render_verbatim_quotes (called in a loop).
    """
    if not quote:
        return
    # Single-line HTML to avoid Streamlit's 4-space markdown-code-block trap
    clean = str(quote).replace("\n", " ").strip()
    if not clean:
        return
    st.markdown(
        f'<blockquote class="verbatim-card">&ldquo;{html.escape(clean)}&rdquo;</blockquote>',
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Page 4 & 5: Territory card (numbered)
# ═══════════════════════════════════════════════════════════════════════════

def render_territory_card(number: int, text: str, title: Optional[str] = None) -> None:
    """
    Render a numbered territory card with peach gradient background.

    Args:
        number: 1-based position
        text: body text (required)
        title: optional header; if omitted or empty, no title div is emitted
    """
    # Single-line HTML to avoid Streamlit's 4-space markdown-code-block trap
    title_html = f'<div class="t-title">{html.escape(title)}</div>' if title else ""
    st.markdown(
        f'<div class="territory-card"><div class="num-circle">{number}</div>'
        f'<div class="t-body">{title_html}<div class="t-text">{html.escape(text)}</div></div></div>',
        unsafe_allow_html=True,
    )


def render_territory_list(items: list[str]) -> None:
    """
    Render a list of territory strings as auto-numbered Treatment C territory cards.
    Drop-in replacement for autostrat_components.render_territory_cards which takes
    a flat list of strings with no title.
    """
    if not items:
        return
    for i, text in enumerate(items, 1):
        if not text:
            continue
        render_territory_card(i, str(text))


# ═══════════════════════════════════════════════════════════════════════════
# Page 5: Brand mention card
# ═══════════════════════════════════════════════════════════════════════════

def render_brand_mention(
    name: str,
    context: str,
    source: str,
    sentiment: str = "pos",
) -> None:
    """
    Render a brand mention card with sentiment badge.

    Args:
        sentiment: 'pos' | 'neu' | 'neg'
    """
    s = sentiment if sentiment in ("pos", "neu", "neg") else "neu"
    label = {"pos": "Positive", "neu": "Neutral", "neg": "Negative"}[s]
    st.markdown(
        f"""
<div class="brand-mention">
  <div class="bm-head">
    <div class="bm-name">{html.escape(name)}</div>
    <span class="sentiment-badge {s}">{label}</span>
  </div>
  <div class="bm-context">{html.escape(context)}</div>
  <div class="bm-source">{html.escape(source)}</div>
</div>
""",
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Page 5: Sentiment 3-cell breakdown
# ═══════════════════════════════════════════════════════════════════════════

def render_sentiment_grid(
    positive_pct: float,
    neutral_pct: float,
    negative_pct: float,
) -> None:
    """Render a 3-cell Positive/Neutral/Negative breakdown."""
    st.markdown(
        f"""
<div class="sentiment-grid">
  <div class="sentiment-cell pos"><div class="sent-pct">{positive_pct:.0f}%</div><div class="sent-lbl">Positive</div></div>
  <div class="sentiment-cell neu"><div class="sent-pct">{neutral_pct:.0f}%</div><div class="sent-lbl">Neutral</div></div>
  <div class="sentiment-cell neg"><div class="sent-pct">{negative_pct:.0f}%</div><div class="sent-lbl">Negative</div></div>
</div>
""",
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Page 5: "What This Means for Hero" card
# ═══════════════════════════════════════════════════════════════════════════

def render_wtm_card(title: str, body_html: str, variant: str = "peach") -> None:
    """
    Render a "What This Means" colored card.

    Args:
        variant: 'blue' | 'green' | 'red' | 'orange' | 'peach'
        body_html: inner HTML content (caller escapes)
    """
    v = variant if variant in ("blue", "green", "red", "orange", "peach") else "peach"
    st.markdown(
        f"""
<div class="wtm-card {v}">
  <h4>{html.escape(title)}</h4>
  {body_html}
</div>
""",
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Page 5: News narrative card
# ═══════════════════════════════════════════════════════════════════════════

def render_news_narrative(
    title: str,
    body: str,
    brands_line: Optional[str] = None,
) -> None:
    """Render a trending news narrative card."""
    brands_html = (
        f'<div class="brands-line">{html.escape(brands_line)}</div>'
        if brands_line else ""
    )
    st.markdown(
        f"""
<div class="news-narrative">
  <h4>{html.escape(title)}</h4>
  <p>{html.escape(body)}</p>
  {brands_html}
</div>
""",
        unsafe_allow_html=True,
    )
