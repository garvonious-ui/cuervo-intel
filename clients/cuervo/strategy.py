"""
Cuervo Client — Strategy Frameworks
=====================================
All Poplife playbook frameworks, KPI targets, content mix definitions,
cultural calendar, creator archetypes, and voice principles.
"""

# ── North Star ──────────────────────────────────────────────────────────────
NORTH_STAR = {
    "title": "Signal for Fun",
    "tagline": "Cuervo turns regular plans into stories.",
    "description": (
        "This is our guiding idea across all content. Whether it\u2019s a casual hang, "
        "a festival weekend, or a watch party, Cuervo is the catalyst that elevates the energy."
    ),
}

# ── Content Pillars (2026 Social Strategy — 4 pillars from Poplife deck) ─

PILLAR_MAP = {
    "The Ritual": [
        "Product/Lifestyle", "Cocktail Highlights", "Cultural Moment/Holiday",
    ],
    "The Pulse": [
        "Meme/Humor", "Creator Collab", "User Repost", "Giveaway/Promo",
    ],
    "The Front Row": [
        "Event/Activation", "Sports Tie-in", "Partner",
    ],
    "The Craft": [
        "Brand Heritage / Culture", "Behind the Scenes",
    ],
}

PILLAR_TARGETS = {
    "The Ritual": 35,
    "The Pulse": 35,
    "The Front Row": 25,
    "The Craft": 5,
}

PILLAR_COLORS = {
    "The Front Row": "#CC0000",    # Bold red — sports/events energy
    "The Ritual": "#F8C090",       # Warm peach — drinking occasions
    "The Pulse": "#2ea3f2",        # Blue — pop culture/reactive
    "The Craft": "#C9A87E",        # Gold — heritage/premium
}

PILLAR_DESCRIPTIONS = {
    "The Front Row": "NASCAR, UFC, music festivals — all-access pass to excitement (Especial + RTDs)",
    "The Ritual": "Drinking occasions — visual blueprint for the perfect serve (Especial + RTDs)",
    "The Pulse": "Pop culture, memes, trending moments — talk with the audience, not at them (Especial + RTDs)",
    "The Craft": "Heritage, bartender POV, distillery stories — defend the 230-year legacy (Tradicional)",
}

# ── Content Mix (Entertain / Educate / Convince) ────────────────────

CONTENT_MIX_MAP = {
    "Entertain": ["Meme/Humor", "Event/Activation", "Creator Collab", "Sports Tie-in",
                   "Product/Lifestyle", "Cultural Moment/Holiday", "User Repost"],
    "Educate": ["Cocktail Highlights", "Behind the Scenes", "Brand Heritage / Culture", "Partner"],
    "Convince": ["Giveaway/Promo"],
}

CONTENT_MIX_TARGETS = {"Entertain": 70, "Educate": 20, "Convince": 10}

CONTENT_MIX_COLORS = {
    "Entertain": "#F8C090",
    "Educate": "#2ea3f2",
    "Convince": "#D9534F",
}

# ── KPI Targets (2026 Social Brief) ─────────────────────────────────

KPI_TARGETS = {
    # Per-post averages (owned-only baseline: 85 avg eng, 3.3% save, 7.7% share)
    "engagements_per_post": 100,
    "eng_per_1k_followers": 1.5,
    "reel_ratio": 40,
    "carousel_ratio": 30,
    "ig_posts_per_month": (10, 14),
    "tt_posts_per_month": (8, 12),
    "save_rate": 3.0,
    "share_rate": 5.0,
    "creator_pct_target_june": 30,
    # Monthly volume targets (owned-only — 15-35% growth over current actuals)
    "saves_per_month": 35,
    "shares_per_month": 80,
    "likes_per_month": 800,
    "comments_per_month": 65,
    "reel_views_per_month": 25000,
    "carousel_impressions_per_month": 80000,
    "stories_per_month": 90,
    "story_views_per_month": 35000,
}

# ── Platform Cadence Targets ─────────────────────────────────────────

CADENCE_TARGETS = {
    "Instagram": {"low": 10, "high": 14},
    "TikTok": {"low": 8, "high": 12},
}

# ── IG Format Mix ────────────────────────────────────────────────────

IG_FORMAT_MIX = {
    "Reels": {"pct": 50, "role": "Reach + discovery"},
    "Carousels": {"pct": 35, "role": "Engagement driver"},
    "Stories": {"pct": 15, "role": "Community + utility"},
}

# ── Content Production Needs ─────────────────────────────────────────

CONTENT_PRODUCTION_NEEDS = [
    {"type": "Creator Reels + Carousels", "source": "Influencer (31%)", "sku": "Especial + RTD", "volume": "8-10"},
    {"type": "Memes + Graphics", "source": "In-house design", "sku": "Especial + RTD", "volume": "4-6"},
    {"type": "Brand Reels", "source": "In-house / Agency", "sku": "Especial + RTD", "volume": "3-5"},
    {"type": "Brand Carousels + Stills", "source": "In-house design", "sku": "All SKUs", "volume": "2-3"},
    {"type": "Event / Partnership", "source": "Partner (7%)", "sku": "Especial + RTD", "volume": "As events occur"},
    {"type": "Reactive / Trend Content", "source": "Social team / Creator", "sku": "Especial + RTD", "volume": "As culture dictates"},
    {"type": "Stories (polls, Q&As, BTS)", "source": "Social team", "sku": "All SKUs", "volume": "Daily"},
    {"type": "Collective / Crew Content", "source": "Collective (10%)", "sku": "Especial", "volume": "2-4"},
]

# Source mix target percentages for the production needs stacked bar
SOURCE_MIX_TARGET = {"Brand": 52, "Influencer": 31, "Collective": 10, "Partner": 7}

# Monthly total and annual projections
PRODUCTION_SUMMARY = {
    "monthly_low": 23, "monthly_high": 32,
    "monthly_note": "across IG + TikTok + secondary\nplus daily Stories",
    "annual_months": 9, "annual_low": 207, "annual_high": 288,
}

# ── Platform Roles ───────────────────────────────────────────────────

PLATFORM_ROLES = {
    "Instagram": {"role": "The Main Stage — curated, social-first", "priority": "Primary", "cadence": "10-14/mo"},
    "TikTok": {"role": "The Culture Lab — reactive, entertainment", "priority": "Primary", "cadence": "8-12/mo"},
    "Facebook": {"role": "Syndicate top IG posts", "priority": "Secondary", "cadence": "Maintain presence"},
    "X / Threads": {"role": "The Listener — reactive community", "priority": "Secondary", "cadence": "Real time relevance"},
    "YouTube Shorts": {"role": "Reel & TikTok syndication", "priority": "Secondary", "cadence": "3-5x/week"},
    "Pinterest": {"role": "Inspiration Engine — recipes, discovery", "priority": "Secondary", "cadence": "10-12 pins/mo"},
}

# ── Content Source Mix ───────────────────────────────────────────────

CONTENT_SOURCE_MIX = {
    "Owned / Sponsored Live Events": 50,
    "Creator / Influencer / UGC": 30,
    "Brand-Owned": 20,
}

# ── Monthly Ramp Targets (March-June 2026) ───────────────────────────

MONTHLY_RAMP = {
    "March": {"creator_pct": "20%+", "er_target": "85+", "proactive_comments_wk": "15-20"},
    "April": {"creator_pct": "23%+", "er_target": "90+", "proactive_comments_wk": "20-25"},
    "May": {"creator_pct": "27%+", "er_target": "95+", "proactive_comments_wk": "25-30"},
    "June": {"creator_pct": "30%", "er_target": "100+", "proactive_comments_wk": "30+"},
}

# ── Testing Roadmap ──────────────────────────────────────────────────

TESTING_ROADMAP = {
    "March": {"variable": "Creator carousel vs. creator Reel", "learning": "Which format drives higher ER?"},
    "April": {"variable": "Humor/meme vs. lifestyle content", "learning": "What entertainment style resonates?"},
    "May": {"variable": "Short caption vs. story-driven", "learning": "How much copy do people engage with?"},
    "June": {"variable": "Especial-led vs. RTD-led", "learning": "Which SKU drives more summer engagement?"},
}

# ── SKU Strategy ─────────────────────────────────────────────────────

SKU_STRATEGY = {
    "Especial": {"energy": "High energy, fun", "occasions": "Everyday mixing, margs"},
    "Tradicional": {"energy": "Elevated", "occasions": "Night out, gifting, sipping"},
    "RTD": {"energy": "Mid-high, daytime", "occasions": "BBQ, tailgate, concerts"},
}

# ── SKU Usage Matrix (Role of Variants — Mar 2026 Cuervo deck) ───────
# Maps 17 occasions/activities to which SKU variant(s) should be featured.
# Used on Page 3 Tab 2 to guide content planning: given an occasion (e.g.
# "poolside reel"), which SKU leads? An occasion can map to multiple SKUs.
# Source: "Esp vs. Trad Usage Differentiation" deck, slide 2.

SKU_USAGE_MATRIX = {
    "Everyday mixing at home":                      ["Especial"],
    "High energy and fun":                          ["Especial", "RTDs"],
    "Upscale dinner with nicer attire":             ["Tradicional"],
    "Poolside, happy mood, sun is out":             ["Especial", "RTDs"],
    "Tequila educational event":                    ["Tradicional"],
    "Margaritas in a casual cup or glass":          ["Especial"],
    "Upscale cocktails or cocktail-focused bar":    ["Tradicional"],
    "T-shirt and shorts, outdoor gathering at home":["Especial", "RTDs"],
    "Gifting or special occasions":                 ["Tradicional"],
    "Agave fields experience":                      ["Tradicional"],
    "Party atmosphere, upbeat music":               ["Especial", "RTDs"],
    "Outdoors by the beach, bringing your cooler":  ["RTDs"],
    "Music festival, dancing, casual environment":  ["Especial", "RTDs"],
    "On the go":                                    ["RTDs"],
    "In the stands at a sporting event":            ["Especial", "RTDs"],
    "In a suite at a sporting event":               ["Tradicional"],
    "Serving on ice or out of the cooler":          ["RTDs"],
}

# ── Execution Engines ────────────────────────────────────────────────

EXECUTION_ENGINES = {
    "Memes + Reactive Culture": "Fast, funny, internet-native. Real-time commentary, cultural remixing, POV humor, reaction formats.",
    "Creator-Led + UGC": "POV storytelling, diaries, lives, fan cams, giveaways. The Cuervo Crew — creators embedded in the brand.",
    "Event + Festival Trend Factory": "Capture moments for TikTok — not recap videos. Film with trend formats in mind BEFORE the event.",
    "Lifestyle Shoot Bank": "Evergreen assets: meme templates, product hero, seasonal fillers, cocktail how-tos, story backgrounds.",
}

# ── Creator Archetypes ───────────────────────────────────────────────

CREATOR_ARCHETYPES = {
    "The Party Starter": "Nightlife, going-out energy",
    "The Home Bartender": "Cocktail recipes (saves)",
    "The Lifestyle Bestie": "Fashion/lifestyle (aspirational)",
    "The Culture Commentator": "Pop culture, meme (shares)",
    "The Festival Friend": "Events, RTD occasions",
}

# ── Voice Principles ─────────────────────────────────────────────────

VOICE_PRINCIPLES = [
    ("Talk like a friend, not a brand", "Warm, knowing, a little cheeky. Never corporate."),
    ("Be funny without forcing it", "Gen-Z can smell 'trying too hard' instantly."),
    ("Celebrate the moment, not the product", "Lead with what's happening. Cuervo enters as part of the scene."),
    ("Be confident, not cocky", "We invented tequila. That's earned confidence."),
    ("Move at the speed of culture", "Quick, sharp, human reactions. Not two weeks later."),
]

# ── Cultural Calendar (2026) ─────────────────────────────────────────

CULTURAL_CALENDAR = {
    "Q1": {"moments": "Super Bowl, Oscars, Grammys, Nat'l Margarita Day", "angle": "Game day serves, awards content, Valentine's cocktails"},
    "Q2": {"moments": "Cinco de Mayo, Kentucky Derby, Memorial Day, NBA Finals", "angle": "Summer Fridays and Marg Season launch, cocktail culture, summer kickoff"},
    "Q3": {"moments": "4th of July, Love Island, Labor Day, Mexican Independence Day", "angle": "Peak summer, RTD outdoor, reality TV tie-ins, tailgate season"},
    "Q4": {"moments": "Halloween, Day of the Dead, NFL, holiday hosting, NYE", "angle": "Holiday serves, cultural celebrations, game day"},
}

# ── Gen Z Leader Brands (for strategy page comparisons) ──────────────

GEN_Z_LEADERS = ["Casamigos", "Teremana"]
