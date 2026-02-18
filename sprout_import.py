"""
Sprout Social CSV Import Adapter
=================================
Maps Sprout Social report exports to the dashboard's internal CSV schema.
Includes keyword-based content classifiers for qualitative columns that
Sprout Social does not export (content_theme, visual_style, caption_tone, etc.).

Usage:
    from sprout_import import import_sprout_directory
    files = import_sprout_directory("data/sprout/", "data/imported/")
"""

import csv
import os
import re
from datetime import datetime
from typing import Optional

# ─── BRAND NAME MAPPING ──────────────────────────────────────────────
# Maps Sprout Social profile names/handles to our canonical brand names.

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

# ─── COLUMN NAME MAPPING ─────────────────────────────────────────────
# Maps common Sprout Social column names to our internal field names.

COLUMN_ALIASES = {
    "brand": ["profile", "profile name", "instagram profile", "tiktok profiles",
              "account", "brand", "author", "account name"],
    "platform": ["network", "platform", "channel", "network type"],
    "post_url": ["link", "permalink", "perma link", "post permalink",
                  "post link", "url", "post url"],
    "post_date": ["date", "date published", "publish date", "created date",
                   "created", "published", "date created"],
    "post_type": ["post type", "type", "media type"],
    "content_type": ["content type"],
    "caption_text": ["post", "text", "message", "content", "post text",
                      "caption", "description", "post message"],
    "likes": ["reactions", "likes", "like", "total likes", "post likes"],
    "comments": ["comments", "replies", "comment", "total comments"],
    "shares": ["shares", "retweets", "reposts", "share", "total shares"],
    "saves": ["saves", "bookmarks", "save", "total saves"],
    "views": ["video views", "views", "view", "total video views",
               "video plays", "plays"],
    "impressions": ["impressions", "organic impressions", "total impressions"],
    "reach": ["reach", "organic reach", "total reach"],
    "engagements": ["public engagements", "engagements", "total engagements",
                     "engagement"],
    "engagement_rate": ["engagement rate (per impression)", "engagement rate",
                         "engagement rate %"],
    "engagements_per_post": ["public engagements per post", "engagements per post",
                              "avg engagements per post"],
    "published_posts": ["published posts", "published posts & reels",
                         "total published posts"],
    "followers": ["followers", "audience", "follower count", "total followers",
                   "followers at time of post"],
}


def _normalize_col(name: str) -> str:
    return name.strip().lower().replace("_", " ").replace("-", " ")


def _find_column(df_columns: list[str], field: str) -> Optional[str]:
    """Find the DataFrame column matching a field via alias lookup."""
    aliases = COLUMN_ALIASES.get(field, [field])
    norm_cols = {_normalize_col(c): c for c in df_columns}
    for alias in aliases:
        if alias in norm_cols:
            return norm_cols[alias]
    return None


def _resolve_brand(raw_name: str) -> str:
    """Resolve a Sprout profile name to our canonical brand name."""
    cleaned = raw_name.strip().lower().replace("@", "").replace("_", "")
    if cleaned in BRAND_MAP:
        return BRAND_MAP[cleaned]
    # Partial match
    for key, brand in BRAND_MAP.items():
        if key in cleaned or cleaned in key:
            return brand
    return raw_name


def _resolve_platform(raw_network: str) -> str:
    n = raw_network.strip().lower()
    if "instagram" in n or "ig" in n:
        return "Instagram"
    if "tiktok" in n or "tik tok" in n:
        return "TikTok"
    return raw_network.strip()


def _resolve_post_type(raw_type: str, platform: str, content_type: str = "") -> str:
    """Resolve post type from Sprout's 'Post Type' and 'Content Type' columns."""
    t = (raw_type or "").strip().lower()
    ct = (content_type or "").strip().lower()
    if platform == "TikTok":
        return "Video"
    if "reel" in t:
        return "Reel"
    if "story" in t or "stories" in t:
        return "Story"
    if "carousel" in t or "carousel" in ct:
        return "Carousel"
    # Sprout uses "Post" as type — check Content Type for video vs photo
    if t == "post":
        if "video" in ct:
            return "Reel"
        if "carousel" in ct:
            return "Carousel"
        return "Static Image"
    if "video" in t or "video" in ct:
        return "Reel"
    if "image" in t or "photo" in t or "static" in t:
        return "Static Image"
    return "Static Image"


# ─── CONTENT CLASSIFIERS ─────────────────────────────────────────────

THEME_KEYWORDS = {
    "Cocktail Recipe": [
        "recipe", "cocktail", "margarita", "paloma", "mix", "ingredients",
        "garnish", "pour", "shake", "stir", "muddle", "splash", "oz",
        "simple syrup", "lime juice", "make this", "how to make",
    ],
    "Meme / Humor": [
        "pov:", "pov ", "when you", "when someone", "mood:", "me:", "me when",
        "tell me without telling", "iykyk", "literally", "ngl", "no cap",
        "fr fr", "it's giving", "core", "lol", "lmao",
    ],
    "Creator Collab / UGC": [
        "collab", "featuring", "feat.", "ft.", " x @", "with @",
        "repost", "regram", "created by", "styled by", "made by",
    ],
    "Giveaway / Promo": [
        "giveaway", "win", "enter to", "chance to", "sweepstakes", "contest",
        "limited edition", "tag to win",
    ],
    "Cultural Moment / Holiday": [
        "cinco de mayo", "national margarita day", "new year", "valentine",
        "4th of july", "game day", "super bowl", "halloween", "holiday",
        "thanksgiving", "christmas", "mother's day", "father's day",
    ],
    "Behind the Scenes": [
        "behind the scenes", "bts", "distillery", "how it's made",
        "agave field", "harvest", "process", "master distiller",
        "from agave", "jimador",
    ],
    "Brand Heritage / Story": [
        "since", "est.", "heritage", "tradition", "founder", "generations",
        "legacy", "history", "roots", "origin", "began in",
    ],
    "Education (Tequila 101)": [
        "tequila 101", "did you know", "the difference", "blanco vs",
        "reposado vs", "añejo", "cristalino", "guide to",
        "everything you need", "what makes", "how tequila",
    ],
    "Music / Party": [
        "playlist", "turn up", "turn it up", "dj", "concert",
        "festival", "dance", "club", "night out", "pre-game",
    ],
    "Event / Activation": [
        "pop-up", "pop up", "live from", "activation", "launch party",
        "catch us", "meet us", "join us at", "hosted by",
    ],
    "Product Showcase": [
        "bottle", "smooth", "bold", "crafted", "premium", "introducing",
        "meet the", "collection", "expression", "tasting notes", "new drop",
    ],
    "Lifestyle/Aspirational": [
        "sunset", "vibes", "moment", "weekend", "summer",
        "golden hour", "rooftop", "pool", "beach", "cheers",
        "elevated", "living",
    ],
}

TONE_KEYWORDS = {
    "Humorous / Meme": [
        "pov", "mood", "literally", "me:", "lol", "ngl",
        "fr fr", "iykyk", "no cap", "it's giving",
    ],
    "Premium / Luxury": [
        "luxury", "premium", "crafted", "elevated", "refined", "exclusive",
        "elegant", "exquisite", "rare", "aged", "ultra-premium",
    ],
    "Educational / Informative": [
        "learn", "difference", "guide", "tip", "how to",
        "did you know", "101", "fact", "here's why",
    ],
    "Nostalgic / Heritage": [
        "since", "tradition", "heritage", "generations",
        "roots", "founder", "legacy", "history",
    ],
    "Bold / Edgy": [
        "bold", "unleash", "dare", "rebel", "revolution",
        "unapologetic", "unbridled", "fierce", "raw",
    ],
    "Playful / Fun": [
        "fun", "party", "let's go", "woohoo", "cheers",
        "celebrate", "good times",
    ],
    "Casual / Conversational": [
        "hey", "y'all", "tbh", "honestly",
        "let's", "who's", "what's your", "drop a",
    ],
    "Aspirational / Lifestyle": [
        "dream", "lifestyle", "sunset", "aspirational",
        "golden", "perfect", "bliss", "paradise",
    ],
}

CTA_KEYWORDS = {
    "Link in bio": ["link in bio", "linkinbio", "tap the link"],
    "Shop now": ["shop now", "buy now", "order now", "get yours"],
    "Tag a friend": ["tag a friend", "tag someone", "tag your", "tag 3"],
    "Comment below": ["comment below", "tell us", "drop a", "let us know"],
    "Try this recipe": ["try this", "make this", "recipe at home"],
    "Follow for more": ["follow for", "subscribe"],
    "Enter giveaway": ["enter to", "giveaway", "chance to win"],
    "Share this": ["share this", "send this to"],
    "Use our hashtag": ["use #", "use our hashtag"],
}


def classify_theme(caption: str) -> str:
    """Classify content theme from caption text using keyword matching."""
    if not caption:
        return "Other"
    text = caption.lower()
    scores = {}
    for theme, keywords in THEME_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scores[theme] = score
    return max(scores, key=scores.get) if scores else "Lifestyle/Aspirational"


def classify_tone(caption: str) -> str:
    """Classify caption tone from text."""
    if not caption:
        return "Casual / Conversational"
    text = caption.lower()
    scores = {}
    for tone, keywords in TONE_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scores[tone] = score
    return max(scores, key=scores.get) if scores else "Casual / Conversational"


def classify_cta(caption: str) -> str:
    """Detect CTA type from caption text."""
    if not caption:
        return "None"
    text = caption.lower()
    scores = {}
    for cta, keywords in CTA_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scores[cta] = score
    return max(scores, key=scores.get) if scores else "None"


def classify_visual_style(post_type: str, theme: str, brand: str = "") -> str:
    """Estimate visual style (best-effort without image analysis)."""
    if theme in ("Meme / Humor", "Creator Collab / UGC"):
        return "Raw / UGC-style"
    if theme == "Behind the Scenes":
        return "Lo-fi / Authentic"
    if theme in ("Brand Heritage / Story", "Education (Tequila 101)"):
        return "Animation / Motion Graphics"
    if theme == "Product Showcase":
        return "Polished / Studio"
    brand_defaults = {
        "Jose Cuervo": "Mixed / Hybrid",
        "Patron": "Polished / Studio",
        "Don Julio": "Polished / Studio",
        "Casamigos": "Raw / UGC-style",
        "Espolon": "Animation / Motion Graphics",
        "Teremana": "Raw / UGC-style",
        "1800 Tequila": "Mixed / Hybrid",
        "818 Tequila": "Raw / UGC-style",
        "Lunazul": "Mixed / Hybrid",
        "Hornitos": "Raw / UGC-style",
        "Cazadores": "Polished / Studio",
        "Milagro": "Polished / Studio",
        "El Jimador": "Mixed / Hybrid",
    }
    return brand_defaults.get(brand, "Mixed / Hybrid")


def detect_creator_collab(caption: str, brand_handle: str = "") -> tuple[bool, str]:
    """Detect creator collaboration and extract handle from caption."""
    if not caption:
        return False, ""
    mentions = re.findall(r"@[\w.]+", caption)
    brand_clean = brand_handle.replace("@", "").lower()
    other_mentions = [m for m in mentions if m.replace("@", "").lower() != brand_clean]
    text = caption.lower()
    collab_signals = ["collab", "featuring", "feat.", "ft.", " x @", "with @",
                       "created by", "styled by", "made by", "partnered with"]
    has_signal = any(s in text for s in collab_signals)
    if has_signal and other_mentions:
        return True, other_mentions[0]
    if len(other_mentions) >= 2:
        return True, other_mentions[0]
    return False, ""


def detect_paid_partnership(caption: str) -> bool:
    """Detect paid partnership indicators in caption."""
    if not caption:
        return False
    text = caption.lower()
    indicators = ["paid partnership", "#ad ", "#ad\n", "#sponsored",
                   "ad |", "| ad", "#partner", "in partnership with",
                   "sponsored by", "ambassador"]
    return any(ind in text for ind in indicators)


def _extract_hashtags(caption: str) -> str:
    return " ".join(re.findall(r"#\w+", caption)) if caption else ""


def _count_emojis(text: str) -> int:
    if not text:
        return 0
    return len(re.findall(
        "[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251"
        "\U0001f926-\U0001f937\U0001F1F2-\U0001F1F4\U0001F620-\U0001F640"
        "\U0001F910-\U0001F9FF]", text))


# ─── MAIN IMPORT FUNCTIONS ───────────────────────────────────────────

def import_sprout_posts(csv_path: str) -> list[dict]:
    """
    Import a Sprout Social post-level CSV export and convert to our schema.
    Handles Competitor Report and Post Performance Report formats.
    """
    import pandas as pd

    df = pd.read_csv(csv_path, encoding="utf-8-sig")

    col_map = {}
    for field in COLUMN_ALIASES:
        found = _find_column(df.columns.tolist(), field)
        if found:
            col_map[field] = found

    rows = []
    for _, row in df.iterrows():
        raw_brand = str(row.get(col_map.get("brand", ""), ""))
        brand = _resolve_brand(raw_brand)

        raw_platform = str(row.get(col_map.get("platform", ""), ""))
        platform = _resolve_platform(raw_platform)
        if platform not in ("Instagram", "TikTok"):
            continue

        post_url = str(row.get(col_map.get("post_url", ""), ""))

        raw_date = str(row.get(col_map.get("post_date", ""), ""))
        try:
            dt = pd.to_datetime(raw_date)
            post_date = dt.strftime("%Y-%m-%d")
            post_time = dt.strftime("%H:%M")
        except Exception:
            post_date = raw_date
            post_time = ""

        raw_type = str(row.get(col_map.get("post_type", ""), ""))
        raw_content_type = str(row.get(col_map.get("content_type", ""), ""))
        post_type = _resolve_post_type(raw_type, platform, raw_content_type)

        # Skip Stories — ephemeral, different metrics, not available for competitors
        if post_type == "Story":
            continue

        caption = str(row.get(col_map.get("caption_text", ""), ""))
        if caption in ("nan", "None", ""):
            caption = ""
        hashtags = _extract_hashtags(caption)

        def safe_int(val):
            """Parse int from values that may have commas or be empty."""
            if val is None or str(val).strip() in ("", "nan", "None"):
                return 0
            try:
                return int(float(str(val).replace(",", "").replace("%", "")))
            except (ValueError, TypeError):
                return 0

        def safe_float_er(val):
            """Parse Sprout's engagement rate string (e.g. '3.57%') to float."""
            if val is None or str(val).strip() in ("", "nan", "None", "N/A", "-"):
                return ""
            try:
                cleaned = str(val).replace(",", "").replace("%", "").strip()
                parsed = float(cleaned)
                return parsed if parsed >= 0 else ""
            except (ValueError, TypeError):
                return ""

        likes = safe_int(row.get(col_map.get("likes", ""), 0))
        comments = safe_int(row.get(col_map.get("comments", ""), 0))
        shares = safe_int(row.get(col_map.get("shares", ""), 0))
        saves = safe_int(row.get(col_map.get("saves", ""), 0))
        views = safe_int(row.get(col_map.get("views", ""), 0))

        # Capture Sprout's pre-calculated ER (per impression) when available
        sprout_er = safe_float_er(row.get(col_map.get("engagement_rate", ""), ""))

        theme = classify_theme(caption)
        visual_style = classify_visual_style(post_type, theme, brand)
        tone = classify_tone(caption)
        cta = classify_cta(caption)

        is_collab, creator_handle = detect_creator_collab(caption)
        is_paid = detect_paid_partnership(caption)

        has_music = "Yes" if post_type in ("Reel", "Video") else "No"
        word_count = len(caption.split()) if caption else 0
        emoji_count = _count_emojis(caption)
        mentions_count = len(re.findall(r"@[\w.]+", caption)) if caption else 0

        rows.append({
            "brand": brand,
            "platform": platform,
            "post_url": post_url,
            "post_date": post_date,
            "post_time": post_time,
            "post_type": post_type,
            "video_length_seconds": 0,
            "caption_text": caption,
            "hashtags": hashtags,
            "likes": likes,
            "comments": comments,
            "shares": shares,
            "saves": saves,
            "views": views,
            "engagement_rate_manual": sprout_er,
            "content_theme": theme,
            "visual_style": visual_style,
            "caption_tone": tone,
            "cta_type": cta,
            "has_creator_collab": "Yes" if is_collab else "No",
            "creator_handle": creator_handle,
            "has_music_audio": has_music,
            "audio_description": "",
            "emoji_count_in_caption": emoji_count,
            "caption_word_count": word_count,
            "mentions_count": mentions_count,
            "is_paid_partnership": "Yes" if is_paid else "No",
            "notes": f"Imported from Sprout Social — {os.path.basename(csv_path)}",
        })

    return rows


def import_sprout_profiles(csv_path: str) -> list[dict]:
    """
    Import a Sprout Social aggregate report (Competitor Performance,
    Instagram Competitors) and extract the latest follower count per profile.
    These reports have one row per day per profile — we take the most recent.
    """
    import pandas as pd

    df = pd.read_csv(csv_path, encoding="utf-8-sig")
    col_map = {}
    for field in COLUMN_ALIASES:
        found = _find_column(df.columns.tolist(), field)
        if found:
            col_map[field] = found

    def safe_int(val):
        if val is None or str(val).strip() in ("", "nan", "None"):
            return 0
        try:
            return int(float(str(val).replace(",", "").replace("%", "")))
        except (ValueError, TypeError):
            return 0

    # Detect platform from the brand column name itself
    # "TikTok Profiles" → TikTok, "Instagram Profile" → Instagram
    brand_col_name = col_map.get("brand", "")
    default_platform = "Instagram"
    if "tiktok" in brand_col_name.lower():
        default_platform = "TikTok"

    def safe_float(val):
        if val is None or str(val).strip() in ("", "nan", "None"):
            return 0.0
        try:
            return float(str(val).replace(",", "").replace("%", ""))
        except (ValueError, TypeError):
            return 0.0

    # Collect all rows, then pick the latest date per brand+platform
    all_rows = []
    for _, row in df.iterrows():
        raw_brand = str(row.get(brand_col_name, ""))
        brand = _resolve_brand(raw_brand)
        raw_platform = str(row.get(col_map.get("platform", ""), ""))
        if not raw_platform or raw_platform in ("nan", "None"):
            platform = default_platform
        else:
            platform = _resolve_platform(raw_platform)
        if platform not in ("Instagram", "TikTok"):
            continue

        followers = safe_int(row.get(col_map.get("followers", ""), 0))
        engagements = safe_float(row.get(col_map.get("engagements", ""), 0))
        published = safe_float(row.get(col_map.get("published_posts", ""), 0))

        raw_date = str(row.get(col_map.get("post_date", ""), ""))
        try:
            dt = pd.to_datetime(raw_date)
        except Exception:
            dt = pd.Timestamp.now()

        all_rows.append({
            "brand": brand, "platform": platform, "handle": raw_brand,
            "followers": followers, "date": dt,
            "engagements": engagements, "published_posts": published,
        })

    if not all_rows:
        return []

    tmp_df = pd.DataFrame(all_rows)

    # Compute aggregate ER: sum engagements / sum posts / avg followers × 100
    # This gives a more accurate per-post ER than individual post-level calculation
    agg = tmp_df.groupby(["brand", "platform"]).agg({
        "engagements": "sum",
        "published_posts": "sum",
        "followers": "max",  # Most recent non-zero follower count
    }).reset_index()
    agg["aggregate_er"] = 0.0
    mask = (agg["published_posts"] > 0) & (agg["followers"] > 0)
    agg.loc[mask, "aggregate_er"] = (
        (agg.loc[mask, "engagements"] / agg.loc[mask, "published_posts"])
        / agg.loc[mask, "followers"] * 100
    ).round(4)
    agg_er_map = {(r["brand"], r["platform"]): r["aggregate_er"]
                  for _, r in agg.iterrows()}

    # Pick the latest date per (brand, platform) to get most recent follower count
    # Only keep rows where followers > 0
    with_followers = tmp_df[tmp_df["followers"] > 0]
    if with_followers.empty:
        return []
    latest = with_followers.sort_values("date").drop_duplicates(
        subset=["brand", "platform"], keep="last")

    rows = []
    for _, r in latest.iterrows():
        rows.append({
            "brand": r["brand"],
            "platform": r["platform"],
            "handle": r["handle"],
            "followers": r["followers"],
            "following": 0,
            "total_posts": 0,
            "aggregate_er": agg_er_map.get((r["brand"], r["platform"]), 0.0),
            "bio_text": "",
            "bio_link": "",
            "is_verified": "Yes",
            "profile_category": "Alcohol Brand",
            "date_collected": r["date"].strftime("%Y-%m-%d"),
            "notes": "Imported from Sprout Social",
        })

    return rows


def import_benchmark_csv(csv_path: str) -> dict:
    """
    Import a benchmark CSV (e.g. from Metricool / Rival IQ) with brand-level
    aggregate metrics including ER by Views, ER by Followers, follower counts,
    Reels metrics, and hashtag usage.

    Returns dict keyed by canonical brand name:
    {
        "Jose Cuervo": {
            "handle": "josecuervotequila",
            "followers": 111871,
            "total_engagement": 909,
            "posts": 7,
            "er_by_followers": 0.116,
            "er_by_views": 1.287,       # PRIMARY METRIC (percentage)
            "er_by_reach": 1.102,
            "avg_engagement": 129.86,
            "avg_hashtags_per_post": 0.0,
            "reels_count": 1,
            "reels_engagement": 52,
            "date_range": "Jan 20 – Feb 17",
        },
        ...
    }
    """
    import pandas as pd

    df = pd.read_csv(csv_path, encoding="utf-8-sig")

    # Parse date range from filename: Benchmark_CSV_ig_..._20-Jan_to_17-Feb.csv
    date_range = ""
    fname = os.path.basename(csv_path)
    m = re.search(r"(\d{1,2})-(\w+)_to_(\d{1,2})-(\w+)", fname)
    if m:
        date_range = f"{m.group(2)} {m.group(1)} – {m.group(4)} {m.group(3)}"

    result = {}
    for _, row in df.iterrows():
        handle = str(row.get("Page", "")).strip()
        if not handle or handle in ("nan", "None"):
            continue

        brand = _resolve_brand(handle)
        if brand == handle:
            # Could not resolve — skip unknown handles
            continue

        def safe_float(val):
            try:
                return float(val) if val is not None and str(val).strip() not in ("", "nan", "None") else 0.0
            except (ValueError, TypeError):
                return 0.0

        def safe_int(val):
            try:
                return int(float(val)) if val is not None and str(val).strip() not in ("", "nan", "None") else 0
            except (ValueError, TypeError):
                return 0

        # Handle duplicate "Reels Count" column — pandas suffixes as "Reels Count.1"
        reels_col = "Reels Count"
        reels_count = safe_int(row.get(reels_col, 0))

        result[brand] = {
            "handle": handle,
            "followers": safe_int(row.get("Followers", 0)),
            "total_engagement": safe_int(row.get("Engagement", 0)),
            "posts": safe_int(row.get("Posts", 0)),
            "er_by_followers": safe_float(row.get("Avg. Eng. Rate by Followers", 0)),
            "er_by_views": safe_float(row.get("Avg. Eng. Rate by Views", 0)),
            "er_by_reach": safe_float(row.get("Avg. Eng. Rate by Reach", 0)),
            "avg_engagement": safe_float(row.get("Avg. Engagement", 0)),
            "avg_hashtags_per_post": safe_float(row.get("Average Hashtags Per Post", 0)),
            "reels_count": reels_count,
            "reels_engagement": safe_int(row.get("Reels Engagement", 0)),
            "date_range": date_range,
        }

    return result


def import_sprout_directory(sprout_dir: str, output_dir: str) -> tuple[list[str], dict]:
    """
    Scan a directory for Sprout Social CSV exports, import them,
    and write unified CSVs to output_dir for the analysis pipeline.

    Returns (list of generated file paths, import stats dict).
    """
    import pandas as pd

    os.makedirs(output_dir, exist_ok=True)

    all_posts = []
    all_profiles = []
    imported_files = []

    for fname in sorted(os.listdir(sprout_dir)):
        if not fname.lower().endswith(".csv"):
            continue
        if fname.lower().startswith("benchmark_csv"):
            continue  # Handled separately by import_benchmark_csv()
        fpath = os.path.join(sprout_dir, fname)
        try:
            sample = pd.read_csv(fpath, encoding="utf-8-sig", nrows=2)
        except Exception:
            continue

        cols_lower = [c.lower().strip() for c in sample.columns]
        col_text = " ".join(cols_lower)

        # Post-level reports have individual post identifiers
        is_post_level = any(
            kw in col_text for kw in ["post id", "permalink", "perma link"]
        ) or ("link" in cols_lower and "post" in cols_lower)

        # Aggregate/profile reports have audience growth and published totals
        is_aggregate = any(
            kw in col_text
            for kw in ["audience", "net audience growth", "% audience growth",
                        "net follower growth", "% follower growth",
                        "published posts", "published posts & reels"]
        )

        if is_post_level and not is_aggregate:
            posts = import_sprout_posts(fpath)
            all_posts.extend(posts)
            imported_files.append(fname)

        if is_aggregate:
            profiles = import_sprout_profiles(fpath)
            all_profiles.extend(profiles)
            imported_files.append(fname)

    files = []

    # Write posts_data.csv
    if all_posts:
        posts_path = os.path.join(output_dir, "posts_data.csv")
        pd.DataFrame(all_posts).to_csv(posts_path, index=False)
        files.append(posts_path)

    # Fallback follower counts for brands missing from Sprout aggregate data.
    # These are manually sourced Instagram follower counts (Feb 2026).
    _FALLBACK_FOLLOWERS = {
        "1800 Tequila": 108_000,
        "Don Julio": 460_000,
        "El Jimador": 43_400,
        "Hornitos": 36_100,
        "Lunazul": 12_200,
        "Milagro": 23_700,
    }

    # Fill in missing brand+platform combos with fallback followers
    existing_keys = {(p["brand"], p["platform"]) for p in all_profiles}
    # Also add from post data — any brand with posts but no profile
    post_brands = {(p["brand"], p["platform"]) for p in all_posts}
    for brand, platform in post_brands:
        if (brand, platform) not in existing_keys and brand in _FALLBACK_FOLLOWERS:
            # Compute aggregate ER from post data for this brand
            brand_posts = [p for p in all_posts
                           if p["brand"] == brand and p["platform"] == platform]
            total_eng = sum(p["likes"] + p["comments"] + p["shares"] + p["saves"]
                            for p in brand_posts)
            num_posts = len(brand_posts)
            fb_followers = _FALLBACK_FOLLOWERS[brand]
            agg_er = ((total_eng / num_posts) / fb_followers * 100
                      if num_posts > 0 and fb_followers > 0 else 0.0)
            all_profiles.append({
                "brand": brand, "platform": platform,
                "handle": "", "followers": fb_followers,
                "following": 0, "total_posts": num_posts,
                "aggregate_er": round(agg_er, 4),
                "bio_text": "", "bio_link": "", "is_verified": "Yes",
                "profile_category": "Alcohol Brand",
                "date_collected": datetime.now().strftime("%Y-%m-%d"),
                "notes": "Fallback followers — not in Sprout aggregate data",
            })

    # Write brand_profiles.csv (deduplicate — keep highest follower count per brand+platform)
    if all_profiles:
        profiles_path = os.path.join(output_dir, "brand_profiles.csv")
        prof_df = pd.DataFrame(all_profiles)
        prof_df = prof_df.sort_values("followers").drop_duplicates(
            subset=["brand", "platform"], keep="last")
        prof_df.to_csv(profiles_path, index=False)
        files.append(profiles_path)
    elif all_posts:
        # Auto-generate from post data if no profile report
        posts_df = pd.DataFrame(all_posts)
        profile_rows = []
        for (brand, platform), group in posts_df.groupby(["brand", "platform"]):
            profile_rows.append({
                "brand": brand, "platform": platform, "handle": "",
                "followers": 0, "following": 0, "total_posts": len(group),
                "bio_text": "", "bio_link": "", "is_verified": "Yes",
                "profile_category": "Alcohol Brand",
                "date_collected": datetime.now().strftime("%Y-%m-%d"),
                "notes": "Auto-generated — add follower counts from Profile Report",
            })
        profiles_path = os.path.join(output_dir, "brand_profiles.csv")
        pd.DataFrame(profile_rows).to_csv(profiles_path, index=False)
        files.append(profiles_path)

    # Generate hashtag_tracking.csv from post hashtags
    if all_posts:
        ht_path = os.path.join(output_dir, "hashtag_tracking.csv")
        ht_rows = []
        for post in all_posts:
            for tag in post["hashtags"].split():
                if tag.startswith("#"):
                    ht_rows.append({"brand": post["brand"], "hashtag": tag})
        if ht_rows:
            ht_df = pd.DataFrame(ht_rows)
            ht_counts = ht_df.groupby(["brand", "hashtag"]).size().reset_index(
                name="times_used_in_30_days")
            ht_counts["is_branded_hashtag"] = ht_counts.apply(
                lambda r: "Yes" if r["brand"].lower().replace(" ", "") in
                r["hashtag"].lower().replace("#", "") else "No", axis=1)
            ht_counts["estimated_hashtag_volume"] = 0
            ht_counts["category"] = ht_counts["is_branded_hashtag"].apply(
                lambda v: "Branded" if v == "Yes" else "Community")
            ht_counts["notes"] = ""
            ht_counts.to_csv(ht_path, index=False)
        else:
            pd.DataFrame(columns=["brand", "hashtag", "times_used_in_30_days",
                                   "is_branded_hashtag", "estimated_hashtag_volume",
                                   "category", "notes"]).to_csv(ht_path, index=False)
        files.append(ht_path)

    # Generate creator_collabs.csv from detected collabs
    if all_posts:
        cr_path = os.path.join(output_dir, "creator_collabs.csv")
        cr_rows = [
            {
                "brand": p["brand"], "platform": p["platform"],
                "creator_handle": p["creator_handle"],
                "creator_follower_count": 0, "creator_category": "",
                "collab_type": "Unknown", "post_url": p["post_url"],
                "post_date": p["post_date"],
                "engagement_on_post": p["likes"] + p["comments"],
                "is_paid_partnership": p["is_paid_partnership"],
                "notes": "Auto-detected from caption",
            }
            for p in all_posts if p["has_creator_collab"] == "Yes"
        ]
        pd.DataFrame(cr_rows or [],
                      columns=["brand", "platform", "creator_handle",
                               "creator_follower_count", "creator_category",
                               "collab_type", "post_url", "post_date",
                               "engagement_on_post", "is_paid_partnership",
                               "notes"]).to_csv(cr_path, index=False)
        files.append(cr_path)

    stats = {
        "files_imported": len(imported_files),
        "file_names": imported_files,
        "total_posts": len(all_posts),
        "brands_found": sorted(set(p["brand"] for p in all_posts)),
        "platforms_found": sorted(set(p["platform"] for p in all_posts)),
        "profiles_imported": len(all_profiles),
    }

    return files, stats
