"""
Devils Reserve Client — Page Copy & Narrative
================================================
All client-specific page headers, captions, and narrative text blocks.
"""

PAGE_HEADERS = {
    "performance": "Devils Reserve Performance",
    "competitive": "Competitive Landscape",
    "strategy": "Strategy & Brief",
    "inspiration": "Inspiration & Explorer",
    "conversation": "Conversation Intel",
}

PAGE_CAPTIONS = {
    "performance": "How Devils Reserve is performing — sidebar filters do not apply here.",
    "competitive": "What competitors are doing — sidebar filters apply here.",
    "strategy": "The Devils Reserve playbook — sidebar filters do not apply here.",
    "inspiration": "Reference brands studied for content strategy inspiration — plus the full data explorer.",
    "conversation": "Qualitative intelligence from autostrat reports — sidebar filters do not apply.",
}

NAV_TABLE = """
| Page | What you'll find |
|------|--------------------|
| **Devils Reserve Performance** | KPI scorecard, content format & theme performance, self-audit intelligence |
| **Competitive Landscape** | 5-brand comparison (Fireball, Pink Whitney, Jagermeister, Cazadores), content gaps |
| **Strategy & Brief** | Scorecard, 2 content pillars (Chaos 75% / Flavor 25%), action plan |
| **Inspiration & Explorer** | Duolingo, Chipotle, Dunkin', Poppi reference profiles + full data explorer |
| **Conversation Intel** | Competitor keyword analysis, category intel |
"""

# ── Narrative Blocks (per-page, per-section) ─────────────────────────
# Used as cfg.narrative["page_key"]["section_key"]

NARRATIVE = {
    "performance": {
        "cadence_caption": "Targets: Instagram 8-12 assets/month, TikTok 12-20 assets/month",
        "heatmap_caption": "When Devils Reserve posts across the week — find gaps and peak windows",
        "signals_caption": "Beyond likes — saves, shares, and comments indicate deeper audience connection",
        "format_caption": "Devils Reserve's format mix on Instagram — reach vs engagement by format",
        "theme_caption": "Which themes drive the highest engagement for Devils Reserve",
        "tone_caption": "How Devils Reserve's captions sound — the voice behind the brand",
        "cta_caption": "What Devils Reserve asks its audience to do — are we driving action?",
        "no_posts": "No Devils Reserve posts in the dataset.",
        "no_ig_posts": "No Devils Reserve Instagram posts in the dataset.",
        "no_tone_data": "No caption tone data available for Devils Reserve.",
        "no_cta_data": "No CTA data available for Devils Reserve.",
        "self_audit_intro": "Qualitative intelligence from Devils Reserve's self-audit autostrat reports.",
        "no_self_audit": "No Devils Reserve self-audit reports found. Import autostrat PDFs.",
    },
    "competitive": {
        "gap_header": "Content Gap Analysis: Devils Reserve vs Category",
        "steal_caption": "Specific tactics from brands outperforming Devils Reserve",
        "all_winning": "Devils Reserve is outperforming all competitors — keep it up!",
    },
    "strategy": {
        "kpi_header": "KPI Scorecard",
        "kpi_caption": "Current performance vs 2026 targets",
        "pillar_caption": "North Star: \"Raise a little hell\" — 2 pillars: Chaos (Lifestyle) 75%, Flavor (Product) 25%",
        "content_engine_narrative": "Chaos lifestyle content drives the feed (75%) — events, partnerships, creators, mischievous energy. Flavor product content (25%) weaves in the pineapple + jalapeño tequila story.",
        "theme_caption": "Which content theme drives the highest engagement for Devils Reserve",
        "crew_header": "The Devils Reserve Crew — Creator Archetypes",
        "mix_caption": "Grab attention first (Entertain 50%), then guide to action (Convince 10%)",
        "tone_caption": "Devils Reserve's social voice: fun, mischievous, bold, devil-may-care",
        "tone_header": "Tone of Voice — Fun & Mischievous",
        "action_plan_header": "30-Day Action Plan for Devils Reserve",
        "calendar_header": "2026 Cultural Calendar",
        "ramp_header": "Monthly Ramp Targets (March — June 2026)",
        "testing_header": "Monthly A/B tests to optimize content strategy",
        "threats_header": "Threats & Opportunities",
        "opportunities": [
            "Pineapple + jalapeño tequila flavor profile is unique and highly shareable",
            "NASCAR & Spring Break events provide high-energy content opportunities",
            "Barstool IT Girl partnership opens direct pipeline to Gen Z audience",
            "Small account = high growth potential; every new follower compounds",
        ],
        "self_audit_caption": "From Devils Reserve autostrat reports",
        "competitor_intel_caption": "What competitors are doing — use this to identify gaps Devils Reserve can exploit",
    },
    "inspiration": {
        "steal_header_template": "What {hero_brand} Can Steal",
        "adaptation_templates": {
            "product_drops": "Apply the same energy to event activations and flavor-forward drops",
            "heritage": "Mirror this with mischievous brand storytelling",
            "engagement": "Apply these engagement triggers to event culture, nightlife moments",
            "cadence": "Mirror this cadence rhythm synced to NASCAR and festival calendar",
        },
        "audience_comparison_template": "Audience Comparison: Devils Reserve vs {display_name}",
    },
    "conversation": {
        "cuervo_leads_header": "Where Devils Reserve Leads",
        "competitors_winning_header": "Where Competitors Are Winning",
        "audience_friction_caption": "Shared friction points signal category-wide opportunities.",
        "path_forward_header": "Devils Reserve's Path Forward",
        "cuervos_play": "Devils Reserve's Play",
        "bridge_template": "Bridging Devils Reserve to {cat_label}",
        "import_hint_template": "Import Devils Reserve and {cat_label} autostrat PDFs to see the bridge narrative.",
        "what_this_means": "What This Means for Devils Reserve",
    },
}
