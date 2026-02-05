"""
Sample/Demo Data Generator.
Creates realistic synthetic data for testing the analysis pipeline.
Patterns are modeled on typical tequila brand social media behavior.
"""

import csv
import os
import random
import re
from datetime import datetime, timedelta

from templates import (
    BRANDS, CONTENT_THEMES, VISUAL_STYLES, TONE_OPTIONS,
    CTA_TYPES, INSTAGRAM_POST_TYPES, TIKTOK_POST_TYPES,
)

random.seed(42)

# ─── BRAND PERSONALITY PROFILES ───────────────────────────────────────
# These define how each brand behaves on social media for realistic sample data.

BRAND_PROFILES = {
    "Jose Cuervo": {
        "ig_followers": 485_000,
        "tt_followers": 312_000,
        "ig_posts_per_month": 55,
        "tt_posts_per_month": 50,
        "ig_base_er": 1.8,
        "tt_base_er": 3.2,
        "themes": ["Cocktail Recipe", "Lifestyle/Aspirational", "Cultural Moment / Holiday",
                    "Product Showcase", "Meme / Humor"],
        "theme_weights": [0.25, 0.20, 0.15, 0.20, 0.20],
        "visual_bias": ["Raw / UGC-style", "Mixed / Hybrid", "Polished / Studio"],
        "tone_bias": ["Playful / Fun", "Casual / Conversational", "Bold / Edgy"],
        "collab_rate": 0.12,
        "avg_hashtags": 5,
        "caption_length_range": (15, 60),
        "ig_post_type_weights": {"Reel": 0.50, "Carousel": 0.25, "Static Image": 0.25},
    },
    "Patron": {
        "ig_followers": 1_100_000,
        "tt_followers": 520_000,
        "ig_posts_per_month": 58,
        "tt_posts_per_month": 52,
        "ig_base_er": 2.4,
        "tt_base_er": 4.1,
        "themes": ["Product Showcase", "Cocktail Recipe", "Lifestyle/Aspirational",
                    "Behind the Scenes", "Education (Tequila 101)", "Creator Collab / UGC"],
        "theme_weights": [0.20, 0.25, 0.15, 0.15, 0.10, 0.15],
        "visual_bias": ["Polished / Studio", "Mixed / Hybrid"],
        "tone_bias": ["Premium / Luxury", "Educational / Informative", "Aspirational / Lifestyle"],
        "collab_rate": 0.22,
        "avg_hashtags": 8,
        "caption_length_range": (30, 80),
        "ig_post_type_weights": {"Reel": 0.55, "Carousel": 0.30, "Static Image": 0.15},
    },
    "Don Julio": {
        "ig_followers": 890_000,
        "tt_followers": 445_000,
        "ig_posts_per_month": 55,
        "tt_posts_per_month": 50,
        "ig_base_er": 2.1,
        "tt_base_er": 3.8,
        "themes": ["Product Showcase", "Lifestyle/Aspirational", "Behind the Scenes",
                    "Brand Heritage / Story", "Event / Activation"],
        "theme_weights": [0.25, 0.25, 0.15, 0.20, 0.15],
        "visual_bias": ["Polished / Studio", "Polished / Studio", "Mixed / Hybrid"],
        "tone_bias": ["Premium / Luxury", "Aspirational / Lifestyle", "Nostalgic / Heritage"],
        "collab_rate": 0.18,
        "avg_hashtags": 6,
        "caption_length_range": (25, 70),
        "ig_post_type_weights": {"Reel": 0.45, "Carousel": 0.25, "Static Image": 0.30},
    },
    "Casamigos": {
        "ig_followers": 750_000,
        "tt_followers": 680_000,
        "ig_posts_per_month": 60,
        "tt_posts_per_month": 58,
        "ig_base_er": 3.1,
        "tt_base_er": 5.5,
        "themes": ["Lifestyle/Aspirational", "Meme / Humor", "Creator Collab / UGC",
                    "Music / Party", "Cocktail Recipe", "Cultural Moment / Holiday"],
        "theme_weights": [0.20, 0.20, 0.20, 0.15, 0.15, 0.10],
        "visual_bias": ["Raw / UGC-style", "Lo-fi / Authentic", "Mixed / Hybrid"],
        "tone_bias": ["Casual / Conversational", "Playful / Fun", "Humorous / Meme"],
        "collab_rate": 0.35,
        "avg_hashtags": 4,
        "caption_length_range": (8, 35),
        "ig_post_type_weights": {"Reel": 0.65, "Carousel": 0.15, "Static Image": 0.20},
    },
    "Espolon": {
        "ig_followers": 280_000,
        "tt_followers": 195_000,
        "ig_posts_per_month": 52,
        "tt_posts_per_month": 50,
        "ig_base_er": 2.0,
        "tt_base_er": 3.5,
        "themes": ["Brand Heritage / Story", "Product Showcase", "Cocktail Recipe",
                    "Education (Tequila 101)", "Cultural Moment / Holiday"],
        "theme_weights": [0.25, 0.20, 0.25, 0.15, 0.15],
        "visual_bias": ["Animation / Motion Graphics", "Polished / Studio", "Mixed / Hybrid"],
        "tone_bias": ["Bold / Edgy", "Educational / Informative", "Casual / Conversational"],
        "collab_rate": 0.10,
        "avg_hashtags": 7,
        "caption_length_range": (20, 65),
        "ig_post_type_weights": {"Reel": 0.40, "Carousel": 0.30, "Static Image": 0.30},
    },
    "Teremana": {
        "ig_followers": 620_000,
        "tt_followers": 890_000,
        "ig_posts_per_month": 55,
        "tt_posts_per_month": 55,
        "ig_base_er": 2.8,
        "tt_base_er": 6.2,
        "themes": ["Creator Collab / UGC", "Cocktail Recipe", "Meme / Humor",
                    "Lifestyle/Aspirational", "Music / Party", "Giveaway / Promo"],
        "theme_weights": [0.25, 0.20, 0.20, 0.15, 0.10, 0.10],
        "visual_bias": ["Raw / UGC-style", "Lo-fi / Authentic"],
        "tone_bias": ["Casual / Conversational", "Playful / Fun", "Humorous / Meme"],
        "collab_rate": 0.40,
        "avg_hashtags": 3,
        "caption_length_range": (5, 30),
        "ig_post_type_weights": {"Reel": 0.70, "Carousel": 0.15, "Static Image": 0.15},
    },
    "1800 Tequila": {
        "ig_followers": 410_000,
        "tt_followers": 275_000,
        "ig_posts_per_month": 52,
        "tt_posts_per_month": 50,
        "ig_base_er": 2.0,
        "tt_base_er": 3.6,
        "themes": ["Product Showcase", "Cocktail Recipe", "Lifestyle/Aspirational",
                    "Cultural Moment / Holiday", "Music / Party", "Meme / Humor"],
        "theme_weights": [0.25, 0.20, 0.20, 0.15, 0.10, 0.10],
        "visual_bias": ["Polished / Studio", "Mixed / Hybrid", "Raw / UGC-style"],
        "tone_bias": ["Bold / Edgy", "Casual / Conversational", "Playful / Fun"],
        "collab_rate": 0.15,
        "avg_hashtags": 5,
        "caption_length_range": (15, 55),
        "ig_post_type_weights": {"Reel": 0.50, "Carousel": 0.25, "Static Image": 0.25},
    },
}

# ─── SAMPLE CAPTION FRAGMENTS ────────────────────────────────────────

CAPTION_FRAGMENTS = {
    "Cocktail Recipe": [
        "The perfect {brand} margarita starts with fresh lime",
        "New recipe alert: {brand} Paloma with a twist",
        "3 ingredients. 1 legendary cocktail. All {brand}.",
        "Weekend vibes call for this {brand} spicy marg",
        "Save this recipe for your next gathering",
        "The only cocktail recipe you need this summer",
    ],
    "Product Showcase": [
        "Smooth. Bold. Unmistakably {brand}.",
        "Meet the bottle that started it all",
        "New look, same legendary taste",
        "{brand} — crafted for moments worth savoring",
        "The gold standard of tequila",
    ],
    "Lifestyle/Aspirational": [
        "Sunsets taste better with {brand}",
        "Every great night starts with great tequila",
        "This is how we weekend",
        "Find your moment. Make it {brand}.",
        "Good vibes only. {brand} required.",
    ],
    "Meme / Humor": [
        "POV: you brought the {brand} to the party",
        "When someone says they don't like tequila... *shows them {brand}*",
        "Friday energy: activated",
        "Tell me you're having a good time without telling me",
        "Me: I'll just have one. Also me: 🍹🍹🍹",
    ],
    "Creator Collab / UGC": [
        "Obsessed with this {brand} cocktail by @creator",
        "@creator knows how to do it right with {brand}",
        "When the homies bring the {brand} 🔥",
        "Y'all are making the best {brand} cocktails",
    ],
    "Behind the Scenes": [
        "From agave to glass — the {brand} journey",
        "Behind the scenes at the {brand} distillery",
        "Where the magic happens",
        "Meet the master distiller behind {brand}",
    ],
    "Cultural Moment / Holiday": [
        "Happy National Margarita Day from {brand}!",
        "Cinco de Mayo prep starts now",
        "New Year, same great {brand}",
        "Game day isn't complete without {brand}",
    ],
    "Brand Heritage / Story": [
        "Since {year}, we've been doing this different",
        "Generations of craft. One legendary tequila.",
        "The story behind every sip of {brand}",
    ],
    "Education (Tequila 101)": [
        "Blanco vs. Reposado vs. Añejo — which are you?",
        "Did you know? All tequila is mezcal, but not all mezcal is tequila",
        "The difference is in the detail",
    ],
    "Music / Party": [
        "Turn it up. Pour it up. {brand} up.",
        "This playlist + {brand} = perfect night",
        "The weekend starts now",
    ],
    "Giveaway / Promo": [
        "GIVEAWAY: Win a {brand} party pack!",
        "Tag 3 friends for a chance to win {brand}",
        "Limited edition {brand} drop — don't miss out",
        "Summer giveaway alert! Enter to win {brand}",
    ],
    "Event / Activation": [
        "Catch us at the {brand} pop-up this weekend",
        "Live from the {brand} experience — who's here?",
        "The {brand} activation was one for the books",
        "See you at the {brand} summer series",
    ],
}

HASHTAG_POOLS = {
    "Jose Cuervo": ["#JoseCuervo", "#Cuervo", "#CuervoMargarita", "#HaveACuervoDay",
                     "#MargaritaSeason", "#Tequila", "#TequilaCocktails", "#FridayVibes",
                     "#CocktailRecipe", "#WeekendVibes", "#DrinkResponsibly"],
    "Patron": ["#Patron", "#PatronTequila", "#SimplyPerfect", "#PatronMargarita",
                "#PerfectMargarita", "#Tequila", "#CocktailArt", "#MixologyLife",
                "#PremiumTequila", "#CraftCocktails", "#PatronPaloma"],
    "Don Julio": ["#DonJulio", "#DonJulioTequila", "#DonJulio1942", "#LuxuryTequila",
                   "#Tequila", "#ElevateYourSpirits", "#CocktailCulture", "#AgaveLove"],
    "Casamigos": ["#Casamigos", "#CasaAmigos", "#CasaFriends", "#PartyStarter",
                   "#Tequila", "#GoodVibes", "#NightOut", "#SquadGoals", "#WeekendMood"],
    "Espolon": ["#Espolon", "#EspolonTequila", "#UnbridledSpirit", "#MexicanCulture",
                 "#Tequila", "#TequilaLover", "#ArtOfTequila", "#CocktailRecipe",
                 "#TequilaEducation"],
    "Teremana": ["#Teremana", "#TeremanaTequila", "#TeremanaTime", "#RockTequila",
                  "#Tequila", "#CleanTequila", "#SmallBatch", "#PartyTime",
                  "#CocktailVibes"],
    "1800 Tequila": ["#1800Tequila", "#1800", "#1800Cristalino", "#1800Reposado",
                      "#Tequila", "#TequilaNight", "#SmoothSip", "#CocktailHour",
                      "#NightLife"],
}

CREATOR_HANDLES = [
    "@mixology_mike", "@cocktail.queen", "@sip_and_savor", "@tequila_tony",
    "@drinkswithdev", "@bar.basics", "@shakeandstir", "@agave.girl",
    "@cocktail.content", "@drink.culture", "@lime.and.salt", "@spirited.sips",
    "@thirsty.thursday", "@pour.decisions", "@happy.hour.hero", "@sip.happens",
    "@boozy.brunch", "@cocktail.king", "@drink.diva", "@mixup.maria",
]

EMOJIS = ["🍹", "🔥", "🥃", "🍋", "✨", "🎉", "💯", "🌮", "🎶", "😎",
           "🍸", "🥂", "🌵", "☀️", "🤙", "💚", "🙌", "❤️‍🔥"]


def _weighted_choice(items, weights):
    """Pick from items with given weights."""
    return random.choices(items, weights=weights, k=1)[0]


def _generate_caption(brand: str, theme: str) -> str:
    """Generate a realistic caption for a brand and theme."""
    fragments = CAPTION_FRAGMENTS.get(theme, CAPTION_FRAGMENTS["Product Showcase"])
    base = random.choice(fragments).format(brand=brand, year=random.choice([1795, 1942, 2013, 2017, 2020]))

    # Add emojis
    num_emojis = random.randint(0, 4)
    emoji_str = " ".join(random.choices(EMOJIS, k=num_emojis))

    # Add hashtags
    brand_tags = HASHTAG_POOLS.get(brand, ["#Tequila"])
    num_tags = random.randint(2, 8)
    tags = random.sample(brand_tags, min(num_tags, len(brand_tags)))

    return f"{base} {emoji_str}\n\n{' '.join(tags)}"


def _generate_cta(theme: str) -> str:
    """Pick a CTA based on content theme."""
    theme_ctas = {
        "Cocktail Recipe": ["Try this recipe", "Link in bio", "Comment below"],
        "Giveaway / Promo": ["Enter giveaway", "Tag a friend", "Follow for more"],
        "Creator Collab / UGC": ["Follow for more", "Use our hashtag", "Tag a friend"],
        "Product Showcase": ["Link in bio", "Shop now", "Visit website"],
        "Meme / Humor": ["Tag a friend", "Share this", "Comment below"],
    }
    options = theme_ctas.get(theme, ["None", "Link in bio", "Comment below"])
    return random.choice(options)


def generate_sample_posts(output_dir: str) -> str:
    """Generate realistic sample posts data."""
    filepath = os.path.join(output_dir, "posts_data.csv")
    headers = [
        "brand", "platform", "post_url", "post_date", "post_time",
        "post_type", "video_length_seconds", "caption_text", "hashtags",
        "likes", "comments", "shares", "saves", "views",
        "engagement_rate_manual", "content_theme", "visual_style",
        "caption_tone", "cta_type", "has_creator_collab", "creator_handle",
        "has_music_audio", "audio_description", "emoji_count_in_caption",
        "caption_word_count", "mentions_count", "is_paid_partnership", "notes",
    ]

    today = datetime(2026, 2, 5)
    thirty_days_ago = today - timedelta(days=30)

    rows = []

    for brand in BRANDS:
        profile = BRAND_PROFILES[brand]

        for platform in ["Instagram", "TikTok"]:
            if platform == "Instagram":
                num_posts = profile["ig_posts_per_month"]
                base_er = profile["ig_base_er"]
                followers = profile["ig_followers"]
            else:
                num_posts = profile["tt_posts_per_month"]
                base_er = profile["tt_base_er"]
                followers = profile["tt_followers"]

            for i in range(num_posts):
                # Random date within 30-day window, with consistent hour
                peak_hours = [11, 12, 13, 17, 18, 19, 20, 21]
                if random.random() < 0.6:
                    post_hour = random.choice(peak_hours)
                else:
                    post_hour = random.randint(8, 23)
                post_minute = random.randint(0, 59)
                post_date = thirty_days_ago + timedelta(
                    days=random.randint(0, 29),
                    hours=post_hour,
                    minutes=post_minute,
                )

                # Content type
                if platform == "Instagram":
                    type_weights = profile["ig_post_type_weights"]
                    post_type = _weighted_choice(
                        list(type_weights.keys()),
                        list(type_weights.values())
                    )
                else:
                    post_type = "Video"  # TikTok is mostly video

                # Video length
                if post_type in ("Reel", "Video"):
                    video_length = random.choices(
                        [random.randint(7, 15), random.randint(15, 30),
                         random.randint(30, 60), random.randint(60, 180)],
                        weights=[0.25, 0.35, 0.25, 0.15], k=1
                    )[0]
                else:
                    video_length = 0

                # Theme
                theme = _weighted_choice(profile["themes"], profile["theme_weights"])

                # Caption
                caption = _generate_caption(brand, theme)
                hashtags = " ".join(re.findall(r"#\w+", caption))

                word_count = len(caption.split())
                emoji_count = len(re.findall(
                    "[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF"
                    "\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251"
                    "\U0001f926-\U0001f937\U0001F1F2-\U0001F1F4\U0001F620-\U0001F640"
                    "\U0001F910-\U0001F9FF]", caption))

                # Visual style
                visual_style = random.choice(profile["visual_bias"])

                # Tone
                tone = random.choice(profile["tone_bias"])

                # CTA
                cta = _generate_cta(theme)

                # Creator collab
                is_collab = random.random() < profile["collab_rate"]
                creator_handle = random.choice(CREATOR_HANDLES) if is_collab else ""
                is_paid = "Yes" if (is_collab and random.random() < 0.6) else "No"

                # Engagement — varies by content type and theme
                er_multiplier = 1.0
                if post_type == "Reel":
                    er_multiplier *= random.uniform(1.1, 1.6)
                elif post_type == "Carousel":
                    er_multiplier *= random.uniform(0.9, 1.3)
                elif post_type == "Static Image":
                    er_multiplier *= random.uniform(0.5, 0.9)
                if post_type == "Video" and platform == "TikTok":
                    er_multiplier *= random.uniform(0.8, 1.5)

                if theme in ("Meme / Humor", "Creator Collab / UGC"):
                    er_multiplier *= random.uniform(1.2, 1.8)
                elif theme in ("Product Showcase", "Brand Heritage / Story"):
                    er_multiplier *= random.uniform(0.6, 1.0)

                if is_collab:
                    er_multiplier *= random.uniform(1.1, 1.5)

                actual_er = base_er * er_multiplier * random.uniform(0.5, 1.8)

                likes = int(followers * actual_er / 100 * random.uniform(0.7, 1.0))
                comments = int(likes * random.uniform(0.02, 0.08))
                shares = int(likes * random.uniform(0.01, 0.05))
                saves = int(likes * random.uniform(0.03, 0.10)) if platform == "Instagram" else int(likes * random.uniform(0.01, 0.06))
                views = int(likes * random.uniform(8, 25)) if post_type in ("Reel", "Video") else 0

                # Music
                has_music = "Yes" if post_type in ("Reel", "Video") and random.random() < 0.85 else "No"
                audio_desc = "Trending audio" if has_music == "Yes" and random.random() < 0.4 else \
                    "Original sound" if has_music == "Yes" else ""

                post_url = f"https://{'instagram.com/p' if platform == 'Instagram' else 'tiktok.com/@' + brand.lower().replace(' ', '')}/SAMPLE{brand[:3].upper()}{i:03d}"

                rows.append([
                    brand, platform, post_url,
                    post_date.strftime("%Y-%m-%d"),
                    f"{post_hour}:{post_minute:02d}",
                    post_type, video_length, caption, hashtags,
                    likes, comments, shares, saves, views,
                    "", theme, visual_style, tone, cta,
                    "Yes" if is_collab else "No", creator_handle,
                    has_music, audio_desc, emoji_count, word_count,
                    1 if is_collab else 0, is_paid, "",
                ])

    # Shuffle for realism
    random.shuffle(rows)

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    return filepath


def generate_sample_profiles(output_dir: str) -> str:
    """Generate sample brand profiles."""
    filepath = os.path.join(output_dir, "brand_profiles.csv")
    headers = [
        "brand", "platform", "handle", "followers", "following",
        "total_posts", "bio_text", "bio_link", "is_verified",
        "profile_category", "date_collected", "notes",
    ]

    bios = {
        "Jose Cuervo": "The world's #1 tequila since 1795. 🥃 Drink responsibly. 21+",
        "Patron": "Simply Perfect. Handcrafted tequila from Jalisco, Mexico.",
        "Don Julio": "The tequila that started it all. Est. 1942. Drink responsibly.",
        "Casamigos": "Brought to you by those who drink it. 🥂 21+",
        "Espolon": "Born from the unbridled spirit of Mexico. Drink responsibly. 21+",
        "Teremana": "Small batch tequila. Responsibly enjoyed. 21+ 🌵",
        "1800 Tequila": "100% blue Weber agave tequila. Est. 1800. Drink smart. 21+",
    }

    handles = {
        "Jose Cuervo": {"Instagram": "@josecuervo", "TikTok": "@josecuervo"},
        "Patron": {"Instagram": "@patron", "TikTok": "@patron"},
        "Don Julio": {"Instagram": "@donjuliotequila", "TikTok": "@donjulio"},
        "Casamigos": {"Instagram": "@casamigos", "TikTok": "@casamigos"},
        "Espolon": {"Instagram": "@espolontequila", "TikTok": "@espolontequila"},
        "Teremana": {"Instagram": "@teaborhardstuff", "TikTok": "@teremana"},
        "1800 Tequila": {"Instagram": "@1800tequila", "TikTok": "@1800tequila"},
    }

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for brand in BRANDS:
            profile = BRAND_PROFILES[brand]
            for platform in ["Instagram", "TikTok"]:
                followers = profile["ig_followers"] if platform == "Instagram" else profile["tt_followers"]
                writer.writerow([
                    brand, platform,
                    handles[brand][platform],
                    followers,
                    random.randint(50, 500),
                    random.randint(200, 3000),
                    bios[brand],
                    f"https://{brand.lower().replace(' ', '')}.com",
                    "Yes",
                    "Alcohol Brand",
                    "2026-02-05",
                    "Sample data",
                ])

    return filepath


def generate_sample_hashtags(output_dir: str) -> str:
    """Generate sample hashtag tracking data."""
    filepath = os.path.join(output_dir, "hashtag_tracking.csv")
    headers = [
        "brand", "hashtag", "times_used_in_30_days",
        "is_branded_hashtag", "estimated_hashtag_volume",
        "category", "notes",
    ]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for brand in BRANDS:
            tags = HASHTAG_POOLS.get(brand, [])
            for tag in tags:
                is_branded = "Yes" if brand.lower().replace(" ", "") in tag.lower().replace("#", "") else "No"
                times_used = random.randint(3, 25) if is_branded == "Yes" else random.randint(1, 15)
                volume = random.randint(10_000, 50_000_000)
                writer.writerow([
                    brand, tag, times_used, is_branded,
                    volume, "Branded" if is_branded == "Yes" else "Community",
                    "",
                ])

    return filepath


def generate_sample_creators(output_dir: str) -> str:
    """Generate sample creator collaboration data."""
    filepath = os.path.join(output_dir, "creator_collabs.csv")
    headers = [
        "brand", "platform", "creator_handle", "creator_follower_count",
        "creator_category", "collab_type", "post_url", "post_date",
        "engagement_on_post", "is_paid_partnership", "notes",
    ]

    categories = ["Food & Drink", "Lifestyle", "Comedy", "Music", "Fashion", "Fitness"]
    collab_types = ["Branded Content", "Gifted / Organic", "Co-created Content",
                    "Event Appearance", "Recipe Feature"]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for brand in BRANDS:
            profile = BRAND_PROFILES[brand]
            num_collabs = int(profile["collab_rate"] * (profile["ig_posts_per_month"] + profile["tt_posts_per_month"]))

            for _ in range(max(1, num_collabs)):
                platform = random.choice(["Instagram", "TikTok"])
                creator = random.choice(CREATOR_HANDLES)
                writer.writerow([
                    brand, platform, creator,
                    random.choice([15_000, 50_000, 150_000, 500_000, 1_200_000]),
                    random.choice(categories),
                    random.choice(collab_types),
                    f"https://example.com/collab/{brand[:3]}{random.randint(100,999)}",
                    (datetime(2026, 2, 5) - timedelta(days=random.randint(0, 29))).strftime("%Y-%m-%d"),
                    random.randint(2000, 50000),
                    random.choice(["Yes", "No"]),
                    "",
                ])

    return filepath


def generate_all_sample_data(output_dir: str) -> list[str]:
    """Generate all sample data files."""
    os.makedirs(output_dir, exist_ok=True)
    return [
        generate_sample_posts(output_dir),
        generate_sample_profiles(output_dir),
        generate_sample_hashtags(output_dir),
        generate_sample_creators(output_dir),
    ]
