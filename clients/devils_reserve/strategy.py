"""
Devils Reserve Client — Strategy Frameworks
==============================================
From the 2026 Social Brief: Events, Influencer Content, Flavor Profile Forward.
Target: Gen Z (21-28), trend-savvy, short-form video.
"""

# ── Content Pillars (from the brief) ─────────────────────────────────
# 3 pillars: Events, Influencer Content, Flavor Profile

PILLAR_MAP = {
    "Event Energy": [
        "Event/Activation", "Sports Tie-in", "Cultural Moment/Holiday",
        "Meme/Humor", "User Repost",
    ],
    "Creator & Influencer": [
        "Creator Collab", "Partner", "Giveaway/Promo",
    ],
    "Flavor Forward": [
        "Product/Lifestyle", "Cocktail Highlights", "Behind the Scenes",
        "Brand Heritage / Culture",
    ],
}

PILLAR_TARGETS = {
    "Event Energy": 45,
    "Creator & Influencer": 30,
    "Flavor Forward": 25,
}

PILLAR_COLORS = {
    "Event Energy": "#CC0000",       # Devil red — high energy events
    "Creator & Influencer": "#F8C090",  # Warm peach — creator content
    "Flavor Forward": "#2ea3f2",     # Cool blue — product/flavor
}

PILLAR_DESCRIPTIONS = {
    "Event Energy": "NASCAR, Spring Break, festivals — show the 'fun' atmosphere DR shows up in",
    "Creator & Influencer": "Paid influencer content into organic strategy + Barstool IT Girl content",
    "Flavor Forward": "Weave in the flavor profile (pineapple + jalapeño tequila) without being stiff",
}

# ── SKU Strategy ──────────────────────────────────────────────────────

SKU_STRATEGY = {
    "Devils Reserve Tequila": {
        "energy": "High energy, mischievous",
        "occasions": "Events, nightlife, shots, group moments",
    },
}

# ── Execution Engines ─────────────────────────────────────────────────

EXECUTION_ENGINES = {
    "Event Content Factory": "Capture NASCAR, Spring Break, festival moments for TikTok — film with trend formats in mind BEFORE the event.",
    "Creator-Led + Barstool": "Leverage paid influencer content into organic. Barstool IT Girl content. Creator diaries, POV storytelling.",
    "Flavor Profile Content": "Pineapple + jalapeño tequila — cocktail moments, taste reactions, recipe content that feels natural, not stiff.",
    "Memes + Reactive Culture": "Fun, mischievous, internet-native. Real-time commentary, cultural remixing, devil-themed humor.",
}

# ── Creator Archetypes ────────────────────────────────────────────────

CREATOR_ARCHETYPES = {
    "The Party Starter": "Nightlife, going-out energy, group shots",
    "The Barstool Girl": "IT Girl energy, lifestyle/social content",
    "The Event Correspondent": "Festival/NASCAR/event content creator",
    "The Flavor Explorer": "Food & drink, cocktail recipes, taste tests",
    "The Meme Lord": "Humor, mischievous energy, reactive content",
}

# ── Voice Principles ──────────────────────────────────────────────────
# Brand personality: "fun and mischievous"

VOICE_PRINCIPLES = [
    ("Fun and mischievous, always", "Devil's Reserve is the friend who starts the fun. Cheeky, bold, never boring."),
    ("Talk like a friend, not a brand", "Warm, knowing, a little dangerous. Never corporate."),
    ("Lead with the moment, not the product", "Show the experience first. The drink enters as part of the scene."),
    ("Earn the edge", "Be bold without being try-hard. Gen Z spots fake instantly."),
    ("Move at the speed of culture", "Quick, sharp, human reactions. Not two weeks later."),
]

# ── Content Mix ───────────────────────────────────────────────────────

CONTENT_MIX_MAP = {
    "Entertain": ["Meme/Humor", "Event/Activation", "Creator Collab", "Sports Tie-in"],
    "Educate": ["Cocktail Highlights", "Behind the Scenes", "Brand Heritage / Culture"],
    "Connect": ["Product/Lifestyle", "Cultural Moment/Holiday", "Partner", "User Repost"],
    "Convince": ["Giveaway/Promo"],
}

CONTENT_MIX_TARGETS = {"Entertain": 50, "Educate": 20, "Connect": 20, "Convince": 10}

CONTENT_MIX_COLORS = {
    "Entertain": "#CC0000",   # Devil red — fun/playful
    "Educate": "#2ea3f2",     # Blue — informative
    "Connect": "#66BB6A",     # Green — community
    "Convince": "#F8C090",    # Peach — action/sales
}

# ── KPI Targets ───────────────────────────────────────────────────────
# Starting from a small base (~2K IG followers, ~21 TT followers)
# Targets are growth-oriented for a brand in launch phase

KPI_TARGETS = {
    "engagements_per_post": 50,         # Small audience, realistic starting target
    "eng_per_1k_followers": 15.0,       # Small accounts can have high relative ER
    "reel_ratio": 60,                   # Heavy on Reels for discovery
    "carousel_ratio": 20,              # Some carousels for engagement
    "ig_posts_per_month": (8, 12),     # Building cadence
    "tt_posts_per_week": (3, 5),       # TikTok-first for discovery
    "save_rate": 3.0,
    "share_rate": 5.0,
    "creator_engagements_per_post": 100,
    "creator_pct_target_june": 30,     # Creator / influencer content share
}

# ── Platform Cadence ──────────────────────────────────────────────────

CADENCE_TARGETS = {
    "Instagram": {"low": 8, "high": 12},
    "TikTok": {"low": 12, "high": 20},
}

# ── IG Format Mix ─────────────────────────────────────────────────────

IG_FORMAT_MIX = {
    "Reels": {"pct": 60, "role": "Reach + discovery (priority for small account)"},
    "Carousels": {"pct": 20, "role": "Engagement driver + event recaps"},
    "Stories": {"pct": 15, "role": "Community + event BTS"},
    "Collabs/Lives": {"pct": 5, "role": "Creator amplification"},
}

# ── Platform Roles ────────────────────────────────────────────────────

PLATFORM_ROLES = {
    "Instagram": {"role": "The Main Stage — curated, event-driven", "priority": "Primary", "cadence": "8-12/mo"},
    "TikTok": {"role": "The Culture Lab — reactive, mischievous, trend-first", "priority": "Primary", "cadence": "3-5x/week"},
    "Facebook": {"role": "Syndicate top IG posts", "priority": "Secondary", "cadence": "Maintain presence"},
}

# ── Content Source Mix ────────────────────────────────────────────────

CONTENT_SOURCE_MIX = {
    "Event Content (NASCAR, Spring Break)": 45,
    "Creator / Influencer / Barstool": 30,
    "Brand-Owned (Flavor, Product)": 25,
}

# ── Monthly Ramp Targets ─────────────────────────────────────────────

MONTHLY_RAMP = {
    "March": {"creator_pct": "20%+", "er_target": "1.0%", "proactive_comments_wk": "10-15"},
    "April": {"creator_pct": "23%+", "er_target": "1.5%", "proactive_comments_wk": "15-20"},
    "May": {"creator_pct": "27%+", "er_target": "2.0%", "proactive_comments_wk": "20-25"},
    "June": {"creator_pct": "30%", "er_target": "2.5%", "proactive_comments_wk": "25+"},
}

# ── Testing Roadmap ───────────────────────────────────────────────────

TESTING_ROADMAP = {
    "March": {"variable": "Event recap Reel vs. event meme format", "learning": "Which event format drives more shares?"},
    "April": {"variable": "Barstool creator vs. micro-influencer", "learning": "Which creator tier drives higher ER?"},
    "May": {"variable": "Flavor-forward vs. lifestyle content", "learning": "Does product education or vibe drive engagement?"},
    "June": {"variable": "Short caption vs. story-driven", "learning": "How much copy do people engage with?"},
}

# ── Cultural Calendar ─────────────────────────────────────────────────

CULTURAL_CALENDAR = {
    "Q1": {"moments": "Super Bowl, NASCAR season start, Spring Break", "angle": "Game day content, event energy, group shots"},
    "Q2": {"moments": "Cinco de Mayo, Coachella, NBA Finals, Memorial Day", "angle": "Festival content, summer kickoff, outdoor moments"},
    "Q3": {"moments": "4th of July, NASCAR summer races, Lollapalooza", "angle": "Peak summer, tailgate content, event factory"},
    "Q4": {"moments": "Halloween, Day of the Dead, NFL, holiday hosting, NYE", "angle": "Devil-themed Halloween, holiday party content"},
}

# ── Gen Z Leaders (competitive aspirational set) ─────────────────────

GEN_Z_LEADERS = ["Fireball", "Pink Whitney"]
