"""
Cuervo Client — Page Copy & Narrative
=======================================
All client-specific page headers, captions, and narrative text blocks.
"""

PAGE_HEADERS = {
    "performance": "Cuervo Performance",
    "competitive": "Competitive Landscape",
    "strategy": "2026 Strategy & Brief",
    "inspiration": "Inspiration & Explorer",
    "conversation": "Conversation Intel",
}

PAGE_CAPTIONS = {
    "performance": "How Jose Cuervo is performing — sidebar filters do not apply here.",
    "competitive": "What competitors are doing — sidebar filters apply here.",
    "strategy": "The Cuervo Social Brief playbook — sidebar filters do not apply here.",
    "inspiration": "Non-competitive brands studied for content strategy inspiration — plus the full data explorer.",
    "conversation": "Qualitative intelligence from autostrat reports — sidebar filters do not apply.",
}

NAV_TABLE = """
| Page | What you'll find |
|------|-----------------|
| **Brand Performance** | KPI scorecard vs Brief targets, content format & theme performance, self-audit intelligence |
| **Competitive Landscape** | 13-brand comparison, content gaps, "What to Steal" cards, competitor autostrat intel |
| **2026 Strategy** | Social Brief scorecard, Poplife content pillars & mix funnel, 30-day action plan |
| **Inspiration & Explorer** | Duolingo & Poppi reference profiles, audience comparison, full data explorer |
| **Conversation Intel** | Brand hashtag comparison (#JoseCuervo vs #Cazadores), category & cultural conversation, Google News sentiment & action items |
"""

# ── Narrative Blocks (per-page, per-section) ─────────────────────────
# Used as cfg.narrative["page_key"]["section_key"]

NARRATIVE = {
    "performance": {
        "cadence_caption": "Poplife targets: Instagram 12-16 assets/month, TikTok 12-20 assets/month",
        "heatmap_caption": "When Cuervo posts across the week — find gaps and peak windows",
        "signals_caption": "Beyond likes — saves, shares, and comments indicate deeper audience connection",
        "format_caption": "Cuervo's format mix on Instagram — reach vs engagement by format",
        "theme_caption": "Which themes drive the highest engagement for Cuervo",
        "tone_caption": "How Cuervo's captions sound — the voice behind the brand",
        "cta_caption": "What Cuervo asks its audience to do — are we driving action?",
        "no_posts": "No Cuervo posts in the dataset.",
        "no_ig_posts": "No Cuervo Instagram posts in the dataset.",
        "no_tone_data": "No caption tone data available for Cuervo.",
        "no_cta_data": "No CTA data available for Cuervo.",
        "self_audit_intro": "Qualitative intelligence from Cuervo's self-audit autostrat reports.",
        "no_self_audit": "No Cuervo self-audit reports found. Import josecuervo or margaritatime autostrat PDFs.",
    },
    "competitive": {
        "gap_header": "Content Gap Analysis: Cuervo vs Category",
        "steal_caption": "Specific tactics from brands outperforming Cuervo",
        "all_winning": "Cuervo is outperforming all competitors — keep it up!",
    },
    "strategy": {
        "kpi_header": "Social Brief KPI Scorecard",
        "kpi_caption": "Current performance vs 2026 Social Brief targets",
        "pillar_caption": "2 pillars from the 2026 Social Strategy — SKU-aligned content territories",
        "content_engine_narrative": "Owned / Sponsored Live Events anchor the feed (50%). Creator & influencer partnerships drive 1.7x more engagement (30%). Brand-owned content fills gaps with evergreen assets (20%).",
        "theme_caption": "Which content theme drives the highest engagement for Cuervo",
        "crew_header": "The Cuervo Crew — Creator Archetypes",
        "mix_caption": "Grab attention first (Entertain 50%), then guide to action (Convince 10%)",
        "tone_caption": "Cuervo's social voice: lively, approachable, human-forward, extroverted",
        "tone_header": "Tone of Voice — The Life of the Party",
        "action_plan_header": "30-Day Action Plan for Cuervo",
        "calendar_header": "2026 Cultural Calendar",
        "ramp_header": "Monthly Ramp Targets (March — June 2026)",
        "testing_header": "Monthly A/B tests to optimize content strategy",
        "threats_header": "Threats & Opportunities",
        "opportunities": [
            "Brand heritage (250+ yrs) is a unique differentiator vs newer brands",
            "RTD line (Playamar, Margarita cans) offers untapped content pillar",
            "'Fun signal' positioning aligns naturally with Gen Z content preferences",
        ],
        "self_audit_caption": "From #JoseCuervo, #Cuervo, and Cuervo keyword reports",
        "competitor_intel_caption": "What competitors are doing — use this to identify gaps Cuervo can exploit",
    },
    "inspiration": {
        "steal_header_template": "What {hero_brand} Can Steal",
        "adaptation_templates": {
            "product_drops": "Apply the same energy to new product drops (Playamar, seasonal margarita kits), cocktail reveals, and cultural moments",
            "heritage": "mirror this with tequila heritage storytelling, cocktail culture moments",
            "engagement": "Apply these engagement triggers to cocktail culture, tequila heritage moments",
            "cadence": "Mirror this cadence rhythm synced to tequila calendar moments (Margarita Day, Cinco de Mayo, summer kickoff, holiday entertaining)",
        },
        "audience_comparison_template": "Audience Comparison: Cuervo vs {display_name}",
    },
    "conversation": {
        "cuervo_leads_header": "Where Cuervo Leads",
        "competitors_winning_header": "Where Competitors Are Winning",
        "audience_friction_caption": "Shared friction points signal category-wide opportunities.",
        "path_forward_header": "Cuervo's Path Forward",
        "cuervos_play": "Cuervo's Play",
        "bridge_template": "Bridging #JoseCuervo to {cat_label}",
        "import_hint_template": "Import both #JoseCuervo and {cat_label} autostrat PDFs to see the bridge narrative.",
        "what_this_means": "What This Means for Cuervo",
    },
}
