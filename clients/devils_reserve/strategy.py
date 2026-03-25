"""
Devils Reserve Client — Strategy Frameworks
==============================================
North Star: "Raise a little hell"
4 pillars: The Diablito Made Me Do It (45%), The Sweet Heat (25%),
           The Devil's Advocate (20%), Hell on Wheels (10%)
Content Mediums: Events, Partnerships, Influencers/Creators, Evergreen Photoshoots
Target: Gen Z (21-28), trend-savvy, short-form video.
"""

# ── Content Pillars ──────────────────────────────────────────────────
# North Star: "Raise a little hell"
# 4 pillars mapped to content themes (finalized via manual tagging sheet)

PILLAR_MAP = {
    "The Diablito Made Me Do It": [
        "Meme/Humor", "Creator Collab", "User Repost",
        "Behind the Scenes", "Giveaway/Promo",
    ],
    "The Sweet Heat": [
        "Product/Lifestyle", "Cocktail Highlights",
        "Brand Heritage / Culture",
    ],
    "The Devil's Advocate": [
        "Cultural Moment/Holiday", "Sports Tie-in",
    ],
    "Hell on Wheels": [
        "Event/Activation", "Partner",
    ],
}

PILLAR_TARGETS = {
    "The Diablito Made Me Do It": 45,
    "The Sweet Heat": 25,
    "The Devil's Advocate": 20,
    "Hell on Wheels": 10,
}

PILLAR_COLORS = {
    "The Diablito Made Me Do It": "#CC0000",  # Devil red — mischievous lifestyle
    "The Sweet Heat": "#F8C090",              # Warm peach — product/flavor
    "The Devil's Advocate": "#FFD700",        # Gold — hot takes
    "Hell on Wheels": "#1a1a1a",              # Black — IRL activations
}

PILLAR_DESCRIPTIONS = {
    "The Diablito Made Me Do It": "Mischievous lifestyle & social chaos — confessional POVs, chaotic photodumps, memes about 'one quick drink'",
    "The Sweet Heat": "Product profile — sweet heat jalapeño + pineapple flavor education, cocktail recipes, product shots",
    "The Devil's Advocate": "Cultural commentary & hot takes — spicy polls, reactive takes on dating, fashion, social etiquette",
    "Hell on Wheels": "IRL mischief & partnerships — Branded Bronco, NASCAR, Love Island, Summer Fridays",
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
    # Per-post averages — 14-month actuals (Feb 25 – Mar 26): 121 IG feed posts
    "engagements_per_post": 85,         # 14mo avg 84.3 — maintain; Reels avg 103, Static avg 38
    "eng_per_1k_followers": 40.0,       # Current 48.8 — will decrease as followers grow
    "reel_ratio": 50,                   # 14mo avg 43% — push toward 50% (was 60%, unrealistic)
    "carousel_ratio": 25,              # 14mo avg 34% — carousels performing well (92.7 avg eng)
    "ig_posts_per_month": (8, 12),     # 14mo avg 8.6/mo — on track
    "tt_posts_per_month": (4, 8),      # 14mo avg 2.1/mo — ramp target
    "save_rate": 7.0,                  # 14mo avg 7.1% — maintain (4mo was inflated by Jan/Feb)
    "share_rate": 8.0,                 # 14mo avg 8.1% — maintain
    "creator_pct_target_june": 30,     # Creator / influencer content share
    # Monthly volume targets — 14-month actuals (Feb 25 – Mar 26)
    "saves_per_month": 55,             # 14mo avg 52/mo (excl Oct outlier)
    "shares_per_month": 60,            # 14mo avg 59/mo — maintain
    "likes_per_month": 500,            # 14mo avg 462/mo — slight growth target
    "comments_per_month": 30,          # 14mo median ~25/mo (Oct 1,892 is outlier, avg 156 skewed)
    "reel_views_per_month": 30000,     # 14mo avg 30,848/mo — maintain baseline
    "carousel_impressions_per_month": 16000,  # 14mo avg 15,777/mo — maintain
    "stories_per_month": 35,           # 14mo avg 36.5/mo — maintain
    "story_views_per_month": 30000,    # 14mo avg 30,405/mo — maintain
}

# ── Platform Cadence ──────────────────────────────────────────────────

CADENCE_TARGETS = {
    "Instagram": {"low": 8, "high": 12},
    "TikTok": {"low": 4, "high": 8},
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
