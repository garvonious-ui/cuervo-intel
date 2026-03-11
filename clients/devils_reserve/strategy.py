"""
Devils Reserve Client — Strategy Frameworks
==============================================
North Star: "Raise a little hell"
2 pillars: Chaos (Lifestyle) 75%, Flavor (Product) 25%
Content Mediums: Events, Partnerships, Influencers/Creators, Evergreen Photoshoots
Target: Gen Z (21-28), trend-savvy, short-form video.
"""

# ── Content Pillars ──────────────────────────────────────────────────
# North Star: "Raise a little hell"
# 2 pillars: Chaos (Lifestyle) 75%, Flavor (Product) 25%

PILLAR_MAP = {
    "Chaos (Lifestyle)": [
        "Event/Activation", "Sports Tie-in", "Cultural Moment/Holiday",
        "Meme/Humor", "User Repost", "Creator Collab", "Partner",
        "Giveaway/Promo", "Behind the Scenes",
    ],
    "Flavor (Product)": [
        "Product/Lifestyle", "Cocktail Highlights",
        "Brand Heritage / Culture",
    ],
}

PILLAR_TARGETS = {
    "Chaos (Lifestyle)": 75,
    "Flavor (Product)": 25,
}

PILLAR_COLORS = {
    "Chaos (Lifestyle)": "#CC0000",    # Devil red — raise a little hell
    "Flavor (Product)": "#F8C090",     # Warm peach — product/flavor
}

PILLAR_DESCRIPTIONS = {
    "Chaos (Lifestyle)": "Raise a little hell — events, partnerships, creators, mischievous energy",
    "Flavor (Product)": "Pineapple + jalapeño tequila — cocktail moments, taste reactions, product content",
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
    "Events": "Capture NASCAR, Spring Break, festival moments — film with trend formats in mind BEFORE the event.",
    "Partnerships": "Brand collaborations, co-branded content, cross-promotions that amplify reach.",
    "Influencers / Content Creators": "Leverage paid influencer content into organic. Barstool IT Girl content. Creator diaries, POV storytelling.",
    "Evergreen Photoshoots": "Planned product/lifestyle shoots — cocktail moments, flavor-forward visuals, brand world-building.",
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
    "engagements_per_post": 75,         # Event content (NASCAR, Spring Break) should push averages up
    "eng_per_1k_followers": 25.0,       # Small accounts routinely hit 20-30+; 15 was too conservative
    "reel_ratio": 60,                   # Heavy on Reels for discovery
    "carousel_ratio": 20,              # Some carousels for engagement
    "ig_posts_per_month": (8, 12),     # Building cadence
    "tt_posts_per_week": (5, 7),       # Need volume to break through at 21 followers
    "save_rate": 2.0,                  # Realistic for Chaos-heavy mix (cocktail saves are 25% of content)
    "share_rate": 3.0,                 # Memes drive shares but not every post
    "creator_engagements_per_post": 150, # Creator content should 2-3x brand-owned
    "creator_pct_target_june": 30,     # Creator / influencer content share
}

# ── Platform Cadence ──────────────────────────────────────────────────

CADENCE_TARGETS = {
    "Instagram": {"low": 8, "high": 12},
    "TikTok": {"low": 20, "high": 28},
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
    "Events": 30,
    "Partnerships": 20,
    "Influencers / Content Creators": 30,
    "Evergreen Photoshoots": 20,
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
