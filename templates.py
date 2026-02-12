"""
CSV Template Generator for Social Media Intelligence Data Collection.
Generates structured templates for manual data entry across all 10 tequila brands
on Instagram and TikTok.
"""

import csv
import os
from datetime import datetime, timedelta

BRANDS = [
    "Jose Cuervo",
    "Patron",
    "Don Julio",
    "Casamigos",
    "Espolon",
    "Teremana",
    "1800 Tequila",
    "818 Tequila",
    "Casadores",
    "Hornitos",
]

PLATFORMS = ["Instagram", "TikTok"]

INSTAGRAM_POST_TYPES = ["Reel", "Carousel", "Static Image", "Story"]
TIKTOK_POST_TYPES = ["Video", "Photo Carousel", "LIVE (archived)"]

CONTENT_THEMES = [
    "Product Showcase",
    "Cocktail Recipe",
    "Lifestyle/Aspirational",
    "Behind the Scenes",
    "Creator Collab / UGC",
    "Event / Activation",
    "Cultural Moment / Holiday",
    "Meme / Humor",
    "Education (Tequila 101)",
    "User Repost",
    "Giveaway / Promo",
    "Brand Heritage / Story",
    "Music / Party",
    "Sports Tie-in",
    "Other",
]

VISUAL_STYLES = [
    "Polished / Studio",
    "Raw / UGC-style",
    "Mixed / Hybrid",
    "Animation / Motion Graphics",
    "Text-heavy / Graphic",
    "Lo-fi / Authentic",
]

TONE_OPTIONS = [
    "Playful / Fun",
    "Premium / Luxury",
    "Educational / Informative",
    "Casual / Conversational",
    "Aspirational / Lifestyle",
    "Bold / Edgy",
    "Nostalgic / Heritage",
    "Humorous / Meme",
]

CTA_TYPES = [
    "None",
    "Link in bio",
    "Shop now",
    "Tag a friend",
    "Comment below",
    "Try this recipe",
    "Follow for more",
    "Share this",
    "Use our hashtag",
    "Visit website",
    "Enter giveaway",
    "Other",
]


def generate_posts_template(output_dir: str) -> str:
    """Generate the main posts data collection CSV."""
    filepath = os.path.join(output_dir, "posts_data.csv")
    headers = [
        "brand",
        "platform",
        "post_url",
        "post_date",
        "post_time",
        "post_type",
        "video_length_seconds",
        "caption_text",
        "hashtags",
        "likes",
        "comments",
        "shares",
        "saves",
        "views",
        "engagement_rate_manual",
        "content_theme",
        "visual_style",
        "caption_tone",
        "cta_type",
        "has_creator_collab",
        "creator_handle",
        "has_music_audio",
        "audio_description",
        "emoji_count_in_caption",
        "caption_word_count",
        "mentions_count",
        "is_paid_partnership",
        "notes",
    ]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        # Write example rows
        writer.writerow([
            "Jose Cuervo",
            "Instagram",
            "https://instagram.com/p/EXAMPLE",
            "2026-01-15",
            "14:30",
            "Reel",
            "28",
            "Nothing beats a Cuervo Margarita on a Friday 🍹 #MargaritaSeason",
            "#MargaritaSeason #JoseCuervo #Tequila #FridayVibes",
            "4520",
            "187",
            "92",
            "310",
            "125000",
            "",
            "Cocktail Recipe",
            "Raw / UGC-style",
            "Playful / Fun",
            "Try this recipe",
            "No",
            "",
            "Yes",
            "Trending audio - original sound",
            "1",
            "9",
            "0",
            "No",
            "Example row - delete this",
        ])

    return filepath


def generate_profile_template(output_dir: str) -> str:
    """Generate brand profile overview CSV."""
    filepath = os.path.join(output_dir, "brand_profiles.csv")
    headers = [
        "brand",
        "platform",
        "handle",
        "followers",
        "following",
        "total_posts",
        "bio_text",
        "bio_link",
        "is_verified",
        "profile_category",
        "date_collected",
        "notes",
    ]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        # Pre-populate with brand/platform combos
        for brand in BRANDS:
            for platform in PLATFORMS:
                writer.writerow([
                    brand, platform, "", "", "", "", "", "", "", "",
                    datetime.now().strftime("%Y-%m-%d"), ""
                ])

    return filepath


def generate_hashtag_template(output_dir: str) -> str:
    """Generate hashtag tracking CSV."""
    filepath = os.path.join(output_dir, "hashtag_tracking.csv")
    headers = [
        "brand",
        "hashtag",
        "times_used_in_30_days",
        "is_branded_hashtag",
        "estimated_hashtag_volume",
        "category",
        "notes",
    ]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        # Pre-populate known branded hashtags
        known_hashtags = {
            "Jose Cuervo": ["#JoseCuervo", "#Cuervo", "#CuervoMargarita", "#HaveACuervoDay"],
            "Patron": ["#Patron", "#PatronTequila", "#SimplyPerfect", "#PatronMargarita"],
            "Don Julio": ["#DonJulio", "#DonJulioTequila", "#DonJulio1942"],
            "Casamigos": ["#Casamigos", "#CasaAmigos", "#CasaFriends"],
            "Espolon": ["#Espolon", "#EspolonTequila"],
            "Teremana": ["#Teremana", "#TeremanaTequila", "#TeremanaTime"],
            "1800 Tequila": ["#1800Tequila", "#1800", "#1800Cristalino", "#1800Reposado"],
            "Casadores": ["#Casadores", "#CasadoresTequila"],
            "Hornitos": ["#Hornitos", "#HornitosTequila", "#HornitosPlata"],
        }
        for brand, tags in known_hashtags.items():
            for tag in tags:
                writer.writerow([brand, tag, "", "Yes", "", "Branded", ""])

    return filepath


def generate_creator_template(output_dir: str) -> str:
    """Generate creator/influencer collaboration tracking CSV."""
    filepath = os.path.join(output_dir, "creator_collabs.csv")
    headers = [
        "brand",
        "platform",
        "creator_handle",
        "creator_follower_count",
        "creator_category",
        "collab_type",
        "post_url",
        "post_date",
        "engagement_on_post",
        "is_paid_partnership",
        "notes",
    ]

    collab_types = [
        "Branded Content",
        "Gifted / Organic",
        "Co-created Content",
        "Event Appearance",
        "Takeover",
        "Recipe Feature",
        "Unknown",
    ]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerow([
            "Jose Cuervo", "Instagram", "@example_creator", "250000",
            "Food & Drink", "Branded Content",
            "https://instagram.com/p/EXAMPLE",
            "2026-01-15", "8500", "Yes",
            "Example row - delete this"
        ])

    return filepath


def generate_collection_guide(output_dir: str) -> str:
    """Generate a markdown guide for data collection."""
    filepath = os.path.join(output_dir, "COLLECTION_GUIDE.md")

    today = datetime.now()
    thirty_days_ago = today - timedelta(days=30)

    guide = f"""# Social Media Intelligence Data Collection Guide

## Collection Period
**From:** {thirty_days_ago.strftime('%B %d, %Y')}
**To:** {today.strftime('%B %d, %Y')}

## Brands to Track

| Brand | Instagram Handle | TikTok Handle |
|-------|-----------------|---------------|
| Jose Cuervo | @josecuervo | @josecuervo |
| Patron | @patron | @patron |
| Don Julio | @donjuliotequila | @donjulio |
| Casamigos | @casamigos | @casamigos |
| Espolon | @espolontequila | @espolontequila |
| Teremana | @teaborhardstuff | @teremana |
| 1800 Tequila | @1800tequila | @1800tequila |
| Casadores | @casadores | @casadores |
| Hornitos | @hornitos | @hornitos |

> **Note:** Verify handles are current before collecting. Some brands may have
> regional accounts — use the primary US/global account.

## Files to Populate

### 1. `brand_profiles.csv`
Collect once at the start. Visit each brand profile and record:
- Follower/following counts
- Bio text and link
- Verification status
- Total post count

### 2. `posts_data.csv` (MAIN FILE)
This is the primary dataset. For each brand, scroll through the last 30 days of posts.

**Instagram data points per post:**
- Post URL (right-click > copy link)
- Date and approximate time posted
- Post type: Reel / Carousel / Static Image
- For Reels: video length in seconds
- Caption (copy full text)
- All hashtags used
- Likes count
- Comments count
- Shares and saves (visible on some posts via insights-style display)
- Views (for Reels)

**TikTok data points per post:**
- Video URL
- Date posted
- Video length in seconds
- Caption text
- Hashtags
- Likes, comments, shares, views (all publicly visible)

**Subjective fields (your assessment):**
- Content theme (pick from: {', '.join(CONTENT_THEMES[:8])}, etc.)
- Visual style: {', '.join(VISUAL_STYLES[:4])}
- Caption tone: {', '.join(TONE_OPTIONS[:4])}
- CTA type: What action does the post ask viewers to take?
- Creator collab: Is this a collab with an influencer/creator?
- Paid partnership: Does it have the "Paid partnership" label?

### 3. `hashtag_tracking.csv`
As you collect posts, note all unique hashtags each brand uses. After
collection, tally how many times each was used in the 30-day window.

### 4. `creator_collabs.csv`
When you spot a creator collab or paid partnership, log it here with the
creator's handle and follower count.

## Tips for Efficient Collection

1. **Use a desktop browser** — easier to copy captions and see all metrics
2. **Work brand by brand** — complete all posts for one brand before moving on
3. **Instagram Reels:** Click into each Reel to see view count and video length
4. **TikTok:** All metrics are visible on the post page
5. **Engagement rate** can be left blank — the analysis script calculates it
6. **Caption word count / emoji count** can be left blank — auto-calculated
7. **Date format:** Use YYYY-MM-DD (e.g., 2026-01-15)
8. **Time format:** Use 24-hour HH:MM (e.g., 14:30)
9. **For hashtags field:** Include the # symbol, separate with spaces

## Estimated Volume
Expect roughly 15-60 posts per brand per platform over 30 days, depending on
posting frequency. Total: ~180-720 rows in posts_data.csv.
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(guide)

    return filepath


def generate_all_templates(output_dir: str) -> list[str]:
    """Generate all CSV templates and the collection guide."""
    os.makedirs(output_dir, exist_ok=True)
    files = [
        generate_posts_template(output_dir),
        generate_profile_template(output_dir),
        generate_hashtag_template(output_dir),
        generate_creator_template(output_dir),
        generate_collection_guide(output_dir),
    ]
    return files
