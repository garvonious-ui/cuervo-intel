"""
Cuervo Client — Brand Definitions
===================================
All brand-specific data: competitive set, colors, Sprout handle mappings,
demo data profiles, hashtag pools, and reference brands.
"""

# ── Competitive Set (13 tequila brands) ──────────────────────────────

BRANDS = [
    "Jose Cuervo", "Patron", "Don Julio", "Casamigos",
    "Espolon", "Teremana", "1800 Tequila", "818 Tequila",
    "Lunazul", "Hornitos", "Cazadores", "Milagro", "El Jimador",
]

BRAND_ORDER = [
    "Jose Cuervo", "Patron", "Don Julio", "Casamigos",
    "Espolon", "Teremana", "1800 Tequila", "818 Tequila",
    "Lunazul", "Hornitos", "Cazadores", "Milagro", "El Jimador",
]

BRAND_COLORS = {
    "Jose Cuervo": "#F8C090",   # Poplife peach — hero brand
    "Patron": "#2ea3f2",        # Poplife blue
    "Don Julio": "#7B6B63",     # Warm dark taupe
    "Casamigos": "#D4956A",     # Burnt peach
    "Espolon": "#A3C4D9",       # Muted sky blue
    "Teremana": "#C9A87E",      # Sandy tan
    "1800 Tequila": "#6B8FA3",  # Steel blue
    "818 Tequila": "#B88BBF",   # Soft purple
    "Lunazul": "#5B9BD5",       # Medium blue
    "Hornitos": "#E8A838",      # Amber gold
    "Cazadores": "#8B4513",     # Saddle brown
    "Milagro": "#50C878",       # Emerald green
    "El Jimador": "#CD5C5C",    # Indian red
}

# ── Reference / Inspiration Brands ───────────────────────────────────

REFERENCE_BRANDS = ["duolingo", "drinkpoppi", "chipotle", "dunkin"]

REFERENCE_BRAND_LABELS = {
    "duolingo": "Duolingo",
    "drinkpoppi": "Poppi (drinkpoppi)",
    "chipotle": "Chipotle",
    "dunkin": "Dunkin'",
}

# ── Autostrat Identifiers ────────────────────────────────────────────

BRAND_HASHTAGS = {
    "josecuervo": "#JoseCuervo",
    "cuervo": "#Cuervo",
    "jose_cuervo": "Jose Cuervo (keyword)",
    "cuervo_tequila": "cuervo tequila (keyword)",
    "cazadores": "#Cazadores",
    "hornitos": "#Hornitos",
    "lunazul": "#Lunazul",
    "milagrotequila": "#MilagroTequila",
    "eljimador": "#ElJimador",
    "teremanatequila": "#TeremanaTequila",
    "1800tequila": "#1800Tequila",
    "casamigos": "#Casamigos",
}

HERO_HASHTAG_IDS = {"josecuervo", "cuervo", "jose_cuervo", "cuervo_tequila"}

CATEGORY_HASHTAGS = {
    "margaritatime": "#MargaritaTime",
}

# ── Sprout Social Handle Mapping ─────────────────────────────────────

BRAND_MAP = {
    "josecuervotequila": "Jose Cuervo",
    "josecuervo": "Jose Cuervo",
    "jose cuervo": "Jose Cuervo",
    "jose cuervo usa": "Jose Cuervo",
    "jose cuervo tequila": "Jose Cuervo",
    "patron": "Patron",
    "patrón": "Patron",
    "patrón tequila": "Patron",
    "patron tequila": "Patron",
    "donjuliotequila": "Don Julio",
    "donjulio": "Don Julio",
    "don julio": "Don Julio",
    "don julio tequila": "Don Julio",
    "tequila don julio": "Don Julio",
    "casamigos": "Casamigos",
    "casamigos tequila": "Casamigos",
    "espolontequila": "Espolon",
    "espolon": "Espolon",
    "espolòn": "Espolon",
    "espolòn tequila": "Espolon",
    "espolon tequila": "Espolon",
    "teremana": "Teremana",
    "teremanatequila": "Teremana",
    "teremana tequila": "Teremana",
    "1800tequila": "1800 Tequila",
    "1800 tequila": "1800 Tequila",
    "tequila 1800": "1800 Tequila",
    "drink818": "818 Tequila",
    "818": "818 Tequila",
    "818 tequila": "818 Tequila",
    "818tequila": "818 Tequila",
    "lunazultequila": "Lunazul",
    "lunazul": "Lunazul",
    "lunazul tequila": "Lunazul",
    "hornitostequila": "Hornitos",
    "hornitos": "Hornitos",
    "hornitos tequila": "Hornitos",
    "sauza hornitos": "Hornitos",
    "tequila hornitos": "Hornitos",
    "tequilacazadores": "Cazadores",
    "cazadorestequila": "Cazadores",
    "cazadores": "Cazadores",
    "tequila cazadores": "Cazadores",
    "cazadores tequila": "Cazadores",
    "milagrotequila": "Milagro",
    "milagro": "Milagro",
    "milagro tequila": "Milagro",
    "eljimadortequila": "El Jimador",
    "eljimador": "El Jimador",
    "el jimador": "El Jimador",
    "el jimador tequila": "El Jimador",
}

FALLBACK_FOLLOWERS = {
    "1800 Tequila": 108_000,
    "Don Julio": 460_000,
    "El Jimador": 43_400,
    "Hornitos": 36_100,
    "Lunazul": 12_200,
    "Milagro": 23_700,
}

CREATOR_PROGRAM_SIGNALS = ["cuervopartner", "cuervocollective"]

# ── Known Branded Hashtags (for template generation) ─────────────────

KNOWN_HASHTAGS = {
    "Jose Cuervo": ["#JoseCuervo", "#Cuervo", "#CuervoMargarita", "#HaveACuervoDay"],
    "Patron": ["#Patron", "#PatronTequila", "#SimplyPerfect", "#PatronMargarita"],
    "Don Julio": ["#DonJulio", "#DonJulioTequila", "#DonJulio1942"],
    "Casamigos": ["#Casamigos", "#CasaAmigos", "#CasaFriends"],
    "Espolon": ["#Espolon", "#EspolonTequila"],
    "Teremana": ["#Teremana", "#TeremanaTequila", "#TeremanaTime"],
    "1800 Tequila": ["#1800Tequila", "#1800", "#1800Cristalino", "#1800Reposado"],
    "818 Tequila": ["#818Tequila", "#drink818", "#818"],
    "Lunazul": ["#Lunazul", "#LunazulTequila"],
    "Hornitos": ["#Hornitos", "#HornitosTequila", "#AShotWorthTaking"],
    "Cazadores": ["#TequilaCazadores", "#Cazadores", "#RealTequilaForRealPeople", "#HuntForTheGoodStuff"],
    "Milagro": ["#Milagro", "#MilagroTequila"],
    "El Jimador": ["#ElJimador", "#ElJimadorTequila", "#SipForYourself"],
}

# ── Brand Handles ────────────────────────────────────────────────────

BRAND_HANDLES = {
    "Jose Cuervo": {"Instagram": "@josecuervotequila", "TikTok": "@josecuervo"},
    "Patron": {"Instagram": "@patron", "TikTok": "@patron"},
    "Don Julio": {"Instagram": "@donjuliotequila", "TikTok": "@donjulio"},
    "Casamigos": {"Instagram": "@casamigos", "TikTok": "@casamigos"},
    "Espolon": {"Instagram": "@espolontequila", "TikTok": "@espolontequila"},
    "Teremana": {"Instagram": "@teremana", "TikTok": "@teremanatequila"},
    "1800 Tequila": {"Instagram": "@1800tequila", "TikTok": "@1800tequila"},
    "818 Tequila": {"Instagram": "@drink818", "TikTok": "@drink818"},
    "Lunazul": {"Instagram": "@lunazultequila", "TikTok": "@lunazultequila"},
    "Hornitos": {"Instagram": "@hornitostequila", "TikTok": "@hornitostequila"},
    "Cazadores": {"Instagram": "@tequilacazadores", "TikTok": "@tequilacazadores"},
    "Milagro": {"Instagram": "@milagrotequila", "TikTok": "@milagrotequila"},
    "El Jimador": {"Instagram": "@eljimadortequila", "TikTok": "@eljimadortequila"},
}

# ── Demo Data: Brand Profiles ────────────────────────────────────────

BRAND_PROFILES = {
    "Jose Cuervo": {
        "ig_followers": 112_000,
        "tt_followers": 28_000,
        "ig_posts_per_month": 55,
        "tt_posts_per_month": 50,
        "ig_base_er": 1.8,
        "tt_base_er": 2.7,
        "themes": ["Cocktail Recipe", "Cultural Moment / Holiday", "Product Showcase",
                    "Lifestyle/Aspirational", "Meme / Humor", "Brand Heritage / Story",
                    "Creator Collab / UGC", "Event / Activation", "Giveaway / Promo"],
        "theme_weights": [0.22, 0.15, 0.18, 0.13, 0.10, 0.08, 0.06, 0.05, 0.03],
        "tone_bias": ["Playful / Fun", "Casual / Conversational", "Nostalgic / Heritage"],
        "collab_rate": 0.08,
        "avg_hashtags": 6,
        "caption_length_range": (15, 60),
        "ig_post_type_weights": {"Reel": 0.45, "Carousel": 0.25, "Static Image": 0.30},
    },
    "Patron": {
        "ig_followers": 350_000,
        "tt_followers": 2_500,
        "ig_posts_per_month": 58,
        "tt_posts_per_month": 48,
        "ig_base_er": 1.5,
        "tt_base_er": 3.0,
        "themes": ["Cocktail Recipe", "Product Showcase",
                    "Behind the Scenes", "Lifestyle/Aspirational", "Creator Collab / UGC"],
        "theme_weights": [0.35, 0.20, 0.15, 0.15, 0.15],
        "tone_bias": ["Premium / Luxury", "Educational / Informative", "Aspirational / Lifestyle"],
        "collab_rate": 0.18,
        "avg_hashtags": 8,
        "caption_length_range": (30, 80),
        "ig_post_type_weights": {"Reel": 0.50, "Carousel": 0.30, "Static Image": 0.20},
    },
    "Don Julio": {
        "ig_followers": 459_000,
        "tt_followers": 180_000,
        "ig_posts_per_month": 52,
        "tt_posts_per_month": 55,
        "ig_base_er": 2.1,
        "tt_base_er": 3.9,
        "themes": ["Product Showcase", "Lifestyle/Aspirational", "Brand Heritage / Story",
                    "Creator Collab / UGC", "Event / Activation", "Cocktail Recipe"],
        "theme_weights": [0.22, 0.20, 0.18, 0.18, 0.12, 0.10],
        "tone_bias": ["Premium / Luxury", "Aspirational / Lifestyle", "Nostalgic / Heritage"],
        "collab_rate": 0.28,
        "avg_hashtags": 5,
        "caption_length_range": (25, 70),
        "ig_post_type_weights": {"Reel": 0.45, "Carousel": 0.25, "Static Image": 0.30},
    },
    "Casamigos": {
        "ig_followers": 310_000,
        "tt_followers": 145_000,
        "ig_posts_per_month": 56,
        "tt_posts_per_month": 52,
        "ig_base_er": 2.7,
        "tt_base_er": 4.2,
        "themes": ["Lifestyle/Aspirational", "Meme / Humor", "Creator Collab / UGC",
                    "Event / Activation", "Cocktail Recipe", "Cultural Moment / Holiday"],
        "theme_weights": [0.20, 0.20, 0.20, 0.15, 0.15, 0.10],
        "tone_bias": ["Casual / Conversational", "Playful / Fun", "Humorous / Meme"],
        "collab_rate": 0.22,
        "avg_hashtags": 4,
        "caption_length_range": (8, 35),
        "ig_post_type_weights": {"Reel": 0.60, "Carousel": 0.15, "Static Image": 0.25},
    },
    "Espolon": {
        "ig_followers": 66_000,
        "tt_followers": 15_000,
        "ig_posts_per_month": 55,
        "tt_posts_per_month": 48,
        "ig_base_er": 1.6,
        "tt_base_er": 2.4,
        "themes": ["Brand Heritage / Story", "Product Showcase", "Cocktail Recipe",
                    "Cultural Moment / Holiday"],
        "theme_weights": [0.25, 0.20, 0.35, 0.20],
        "tone_bias": ["Bold / Edgy", "Educational / Informative", "Casual / Conversational"],
        "collab_rate": 0.08,
        "avg_hashtags": 7,
        "caption_length_range": (20, 65),
        "ig_post_type_weights": {"Reel": 0.40, "Carousel": 0.30, "Static Image": 0.30},
    },
    "Teremana": {
        "ig_followers": 785_000,
        "tt_followers": 420_000,
        "ig_posts_per_month": 55,
        "tt_posts_per_month": 52,
        "ig_base_er": 3.0,
        "tt_base_er": 4.8,
        "themes": ["Creator Collab / UGC", "Cocktail Recipe", "Meme / Humor",
                    "Lifestyle/Aspirational", "Event / Activation", "Giveaway / Promo"],
        "theme_weights": [0.25, 0.20, 0.20, 0.15, 0.10, 0.10],
        "tone_bias": ["Casual / Conversational", "Playful / Fun", "Humorous / Meme"],
        "collab_rate": 0.35,
        "avg_hashtags": 4,
        "caption_length_range": (5, 30),
        "ig_post_type_weights": {"Reel": 0.70, "Carousel": 0.15, "Static Image": 0.15},
    },
    "1800 Tequila": {
        "ig_followers": 49_000,
        "tt_followers": 12_000,
        "ig_posts_per_month": 52,
        "tt_posts_per_month": 50,
        "ig_base_er": 1.4,
        "tt_base_er": 2.1,
        "themes": ["Product Showcase", "Cocktail Recipe", "Lifestyle/Aspirational",
                    "Cultural Moment / Holiday", "Event / Activation", "Meme / Humor"],
        "theme_weights": [0.25, 0.22, 0.18, 0.15, 0.10, 0.10],
        "tone_bias": ["Bold / Edgy", "Casual / Conversational", "Playful / Fun"],
        "collab_rate": 0.10,
        "avg_hashtags": 5,
        "caption_length_range": (15, 55),
        "ig_post_type_weights": {"Reel": 0.50, "Carousel": 0.25, "Static Image": 0.25},
    },
    "818 Tequila": {
        "ig_followers": 1_189_000,
        "tt_followers": 350_000,
        "ig_posts_per_month": 50,
        "tt_posts_per_month": 48,
        "ig_base_er": 1.4,
        "tt_base_er": 3.0,
        "themes": ["Cocktail Recipe", "Lifestyle/Aspirational", "Creator Collab / UGC",
                    "Product Showcase", "Meme / Humor", "Cultural Moment / Holiday"],
        "theme_weights": [0.25, 0.22, 0.18, 0.15, 0.10, 0.10],
        "tone_bias": ["Casual / Conversational", "Playful / Fun", "Aspirational / Lifestyle"],
        "collab_rate": 0.25,
        "avg_hashtags": 4,
        "caption_length_range": (8, 40),
        "ig_post_type_weights": {"Reel": 0.60, "Carousel": 0.20, "Static Image": 0.20},
    },
    "Lunazul": {
        "ig_followers": 25_000,
        "tt_followers": 3_000,
        "ig_posts_per_month": 48,
        "tt_posts_per_month": 42,
        "ig_base_er": 1.0,
        "tt_base_er": 1.8,
        "themes": ["Product Showcase", "Giveaway / Promo", "Lifestyle/Aspirational",
                    "Cocktail Recipe", "Cultural Moment / Holiday"],
        "theme_weights": [0.30, 0.25, 0.20, 0.15, 0.10],
        "tone_bias": ["Casual / Conversational", "Playful / Fun"],
        "collab_rate": 0.03,
        "avg_hashtags": 4,
        "caption_length_range": (15, 50),
        "ig_post_type_weights": {"Reel": 0.30, "Carousel": 0.20, "Static Image": 0.50},
    },
    "Hornitos": {
        "ig_followers": 80_000,
        "tt_followers": 18_000,
        "ig_posts_per_month": 52,
        "tt_posts_per_month": 48,
        "ig_base_er": 1.6,
        "tt_base_er": 2.5,
        "themes": ["Meme / Humor", "Event / Activation", "Lifestyle/Aspirational",
                    "Creator Collab / UGC", "Cocktail Recipe", "Cultural Moment / Holiday"],
        "theme_weights": [0.25, 0.20, 0.18, 0.15, 0.12, 0.10],
        "tone_bias": ["Playful / Fun", "Humorous / Meme", "Casual / Conversational"],
        "collab_rate": 0.10,
        "avg_hashtags": 5,
        "caption_length_range": (8, 35),
        "ig_post_type_weights": {"Reel": 0.65, "Carousel": 0.10, "Static Image": 0.25},
    },
    "Cazadores": {
        "ig_followers": 38_000,
        "tt_followers": 5_000,
        "ig_posts_per_month": 48,
        "tt_posts_per_month": 40,
        "ig_base_er": 1.2,
        "tt_base_er": 1.9,
        "themes": ["Cocktail Recipe", "Product Showcase", "Lifestyle/Aspirational",
                    "Cultural Moment / Holiday", "Meme / Humor"],
        "theme_weights": [0.30, 0.25, 0.20, 0.15, 0.10],
        "tone_bias": ["Casual / Conversational", "Aspirational / Lifestyle", "Playful / Fun"],
        "collab_rate": 0.05,
        "avg_hashtags": 5,
        "caption_length_range": (15, 55),
        "ig_post_type_weights": {"Reel": 0.25, "Carousel": 0.30, "Static Image": 0.45},
    },
    "Milagro": {
        "ig_followers": 30_000,
        "tt_followers": 8_000,
        "ig_posts_per_month": 52,
        "tt_posts_per_month": 45,
        "ig_base_er": 1.4,
        "tt_base_er": 2.1,
        "themes": ["Product Showcase", "Cocktail Recipe", "Event / Activation",
                    "Lifestyle/Aspirational"],
        "theme_weights": [0.25, 0.35, 0.22, 0.18],
        "tone_bias": ["Premium / Luxury", "Educational / Informative", "Aspirational / Lifestyle"],
        "collab_rate": 0.06,
        "avg_hashtags": 3,
        "caption_length_range": (10, 45),
        "ig_post_type_weights": {"Reel": 0.35, "Carousel": 0.30, "Static Image": 0.35},
    },
    "El Jimador": {
        "ig_followers": 50_000,
        "tt_followers": 12_000,
        "ig_posts_per_month": 48,
        "tt_posts_per_month": 44,
        "ig_base_er": 1.3,
        "tt_base_er": 2.1,
        "themes": ["Product Showcase", "Cocktail Recipe", "Brand Heritage / Story",
                    "Cultural Moment / Holiday", "Lifestyle/Aspirational", "Meme / Humor"],
        "theme_weights": [0.25, 0.20, 0.18, 0.15, 0.12, 0.10],
        "tone_bias": ["Casual / Conversational", "Nostalgic / Heritage", "Playful / Fun"],
        "collab_rate": 0.06,
        "avg_hashtags": 4,
        "caption_length_range": (12, 50),
        "ig_post_type_weights": {"Reel": 0.40, "Carousel": 0.25, "Static Image": 0.35},
    },
}

# ── Demo Data: Brand Bios ────────────────────────────────────────────

BRAND_BIOS = {
    "Jose Cuervo": "The world's #1 tequila since 1795. Drink responsibly. 21+",
    "Patron": "Simply Perfect. Handcrafted ultra-premium tequila from the Highlands of Jalisco, Mexico.",
    "Don Julio": "Our passion for tequila-making began in 1942. For Don Julio, it was always Por Amor. 21+",
    "Casamigos": "Brought to you by those who drink it. House of Friends. 21+",
    "Espolon": "Born from the unbridled spirit of Mexico. To the Bone. Drink responsibly. 21+",
    "Teremana": "Small batch tequila crafted with Mana. @therock | Responsibly enjoyed. 21+",
    "1800 Tequila": "100% blue Weber agave tequila since 1800. Crafted in Mexico. 21+",
    "818 Tequila": "Hand-selected tequila from Jalisco, Mexico. @kendalljenner. 21+",
    "Lunazul": "100% de agave tequila. Beam Suntory. Enjoy responsibly. 21+",
    "Hornitos": "A shot worth taking. Premium tequila from the Sauza family. Enjoy responsibly. 21+",
    "Cazadores": "Real tequila for real people. Crafted in the Highlands of Jalisco. 21+",
    "Milagro": "A tequila born from passion. William Grant & Sons. Enjoy responsibly. 21+",
    "El Jimador": "Mexico's #1 tequila. Crafted by the hands of the jimador. Brown-Forman. 21+",
}

# ── Demo Data: Hashtag Pools ─────────────────────────────────────────

HASHTAG_POOLS = {
    "Jose Cuervo": ["#JoseCuervo", "#Cuervo", "#CuervoMargarita", "#HaveACuervoDay",
                     "#CuervoTradicional", "#MargaritaSeason", "#Tequila",
                     "#TequilaCocktails", "#CocktailRecipe", "#DrinkResponsibly",
                     "#Since1795"],
    "Patron": ["#PatronTequila", "#Patron", "#SimplyPerfect", "#PatronMargarita",
                "#AgaveFamilia", "#Remixology", "#Tequila", "#CocktailArt",
                "#MixologyLife", "#PremiumTequila", "#PatronPaloma"],
    "Don Julio": ["#DonJulio", "#DonJulioTequila", "#DonJulio1942", "#PorAmor",
                   "#Tequila", "#LuxuryTequila", "#CocktailCulture", "#AgaveLove"],
    "Casamigos": ["#Casamigos", "#HouseOfFriends", "#AnythingGoes", "#CasaAmigos",
                   "#Tequila", "#GoodVibes", "#NightOut", "#SquadGoals",
                   "#WeekendMood"],
    "Espolon": ["#Espolon", "#EspolonTequila", "#ToTheBone", "#JoinTheRevolution",
                 "#UnbridledSpirit", "#Tequila", "#TequilaLover", "#ArtOfTequila",
                 "#MexicanCulture"],
    "Teremana": ["#Teremana", "#TeremanaTequila", "#TeremanaTuesday", "#TeremanaTime",
                  "#ManaTequila", "#Tequila", "#SmallBatch", "#PartyTime",
                  "#CocktailVibes"],
    "1800 Tequila": ["#1800Tequila", "#1800", "#Essential1800", "#1800Cristalino",
                      "#1800Reposado", "#Tequila", "#TequilaNight", "#CocktailHour",
                      "#NightLife"],
    "818 Tequila": ["#818Tequila", "#drink818", "#818", "#Tequila",
                     "#CocktailVibes", "#GoodVibes", "#WeekendMood",
                     "#TequilaTime", "#Cheers"],
    "Lunazul": ["#Lunazul", "#LunazulTequila", "#Tequila",
                 "#TequilaCocktails", "#DrinkResponsibly", "#GameDay"],
    "Hornitos": ["#Hornitos", "#HornitosTequila", "#AShotWorthTaking",
                  "#Tequila", "#TequilaTime", "#DanceWithHornitos",
                  "#NightOut", "#PartyTime"],
    "Cazadores": ["#TequilaCazadores", "#Cazadores", "#RealTequilaForRealPeople",
                   "#HuntForTheGoodStuff", "#Tequila", "#CocktailRecipes",
                   "#MexicanOldFashioned", "#Margarita"],
    "Milagro": ["#Milagro", "#MilagroTequila", "#Tequila",
                 "#CocktailVibes", "#Reposado", "#CriticsChoice",
                 "#PremiumTequila"],
    "El Jimador": ["#ElJimador", "#ElJimadorTequila", "#SipForYourself",
                    "#Tequila", "#MexicanTequila", "#TequilaTime",
                    "#DrinkResponsibly"],
}
