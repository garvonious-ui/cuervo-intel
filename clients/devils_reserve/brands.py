"""
Devils Reserve Client — Brand Definitions
============================================
Competitive set, colors, Sprout handle mappings, and reference brands.
"""

# ── Competitive Set ──────────────────────────────────────────────────
# Spirit competitors from the brief + Cazadores (Proximo sibling)

BRANDS = [
    "Devils Reserve",
    "Fireball",
    "Pink Whitney",
    "Jagermeister",
    "Cazadores",
]

BRAND_ORDER = BRANDS.copy()

BRAND_COLORS = {
    "Devils Reserve": "#CC0000",  # Devil red — hero brand
    "Fireball": "#F8C090",        # Warm amber/peach
    "Pink Whitney": "#E88BBF",    # Pink
    "Jagermeister": "#2ea3f2",    # Cool blue
    "Cazadores": "#8B4513",       # Saddle brown
}

# ── Reference / Inspiration Brands ───────────────────────────────────
# From the brief: "Duolingo, Chipotle, E.L.F, Dunkin, Poppi"

REFERENCE_BRANDS = ["duolingo", "chipotle", "dunkin", "drinkpoppi"]

REFERENCE_BRAND_LABELS = {
    "duolingo": "Duolingo",
    "chipotle": "Chipotle",
    "dunkin": "Dunkin'",
    "drinkpoppi": "Poppi (drinkpoppi)",
}

# ── Autostrat Identifiers ────────────────────────────────────────────
# Keys match JSON filenames in data/devils_reserve/autostrat/

BRAND_HASHTAGS = {
    # Hero brand reports
    "devils_reserve": "devils reserve (keyword)",
    "devilsreserve": "#devilsreserve (hashtag)",
    # Competitor keyword reports (from autostrat PDFs)
    "fireball_whisky": "fireball whisky (keyword)",
    "jagermeister": "jagermeister (keyword)",
    "pink_whitney": "pink whitney (keyword)",
    "cazadores_tequila": "cazadores tequila (keyword)",
}

HERO_HASHTAG_IDS = {"devils_reserve", "devilsreserve"}

CATEGORY_HASHTAGS = {}  # TODO: populate with category conversation hashtag IDs once reports are imported

# ── Sprout Social Handle Mapping ─────────────────────────────────────
# Maps Sprout CSV "Profile" column values to our canonical brand names

BRAND_MAP = {
    # Hero brand handles
    "devilsreserve": "Devils Reserve",
    "devil's reserve": "Devils Reserve",
    "Devil's Reserve": "Devils Reserve",
    # Competitors
    "fireballwhisky": "Fireball",
    "fireball": "Fireball",
    "jagermeister": "Jagermeister",
    "jägermeister": "Jagermeister",
    "pinkwhitney": "Pink Whitney",
    "pink_whitney": "Pink Whitney",
    "tequilacazadores": "Cazadores",
    "cazadores": "Cazadores",
}

FALLBACK_FOLLOWERS = {
    "Devils Reserve": 2_033,
    "Fireball": 166_923,
    "Pink Whitney": 154_349,
    "Jagermeister": 509_901,
    "Cazadores": 37_925,
}

CREATOR_PROGRAM_SIGNALS = [
    "barstool", "it girl", "devils reserve",
    "devil's reserve", "paid partnership",
]

# ── Known Branded Hashtags ───────────────────────────────────────────

KNOWN_HASHTAGS = {
    "Devils Reserve": ["#DevilsReserve", "#RaiseALittleHell"],
    "Fireball": ["#Fireball", "#FireballWhisky", "#FireballFriday"],
    "Pink Whitney": ["#PinkWhitney", "#NewAmsterdam"],
    "Jagermeister": ["#Jagermeister", "#Jager", "#JagerBomb"],
    "Cazadores": ["#Cazadores", "#TequilaCazadores"],
}

BRAND_HANDLES = {
    "Devils Reserve": {"Instagram": "@devilsreserve", "TikTok": "@devilsreserve"},
    "Fireball": {"Instagram": "@fireballwhisky", "TikTok": "@fireballwhisky"},
    "Pink Whitney": {"Instagram": "@pinkwhitney", "TikTok": "@pinkwhitney"},
    "Jagermeister": {"Instagram": "@jagermeister", "TikTok": "@jagermeister"},
    "Cazadores": {"Instagram": "@tequilacazadores", "TikTok": "@tequilacazadores"},
}

# ── Demo Data ────────────────────────────────────────────────────────

BRAND_PROFILES = {
    "Devils Reserve": {
        "Instagram": {"followers": 2_033, "avg_engagement": 35},
        "TikTok": {"followers": 21, "avg_engagement": 5},
    },
    "Fireball": {
        "Instagram": {"followers": 166_923, "avg_engagement": 1200},
        "TikTok": {"followers": 50_000, "avg_engagement": 800},
    },
    "Pink Whitney": {
        "Instagram": {"followers": 154_349, "avg_engagement": 600},
        "TikTok": {"followers": 30_000, "avg_engagement": 400},
    },
    "Jagermeister": {
        "Instagram": {"followers": 509_901, "avg_engagement": 8000},
        "TikTok": {"followers": 100_000, "avg_engagement": 3000},
    },
    "Cazadores": {
        "Instagram": {"followers": 37_925, "avg_engagement": 150},
        "TikTok": {"followers": 5_000, "avg_engagement": 50},
    },
}

BRAND_BIOS = {}

HASHTAG_POOLS = {
    "Devils Reserve": ["#DevilsReserve", "#RaiseALittleHell", "#Tequila", "#Shots"],
    "Fireball": ["#Fireball", "#FireballWhisky", "#FireballFriday", "#Cinnamon"],
    "Pink Whitney": ["#PinkWhitney", "#NewAmsterdam", "#Hockey", "#Shots"],
    "Jagermeister": ["#Jagermeister", "#Jager", "#JagerBomb", "#NightOut"],
    "Cazadores": ["#Cazadores", "#TequilaCazadores", "#Tequila"],
}
