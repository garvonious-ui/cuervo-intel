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
}

# ─── COLUMN NAME MAPPING ─────────────────────────────────────────────
# Maps common Sprout Social column names to our internal field names.

COLUMN_ALIASES = {
    "brand": ["profile", "profile name", "account", "brand", "author",
              "account name"],
    "platform": ["network", "platform", "channel", "network type"],
    "post_url": ["permalink", "perma link", "post permalink", "post link",
                  "url", "link", "post url"],
    "post_date": ["date", "date published", "publish date", "created date",
                   "created", "published", "date created"],
    "post_type": ["type", "post type", "content type", "media type"],
    "caption_text": ["text", "message", "content", "post text", "caption",
                      "description", "post message"],
    "likes": ["likes", "reactions", "like", "total likes", "post likes"],
    "comments": ["comments", "replies", "comment", "total comments"],
    "shares": ["shares", "retweets", "reposts", "share", "total shares"],
    "saves": ["saves", "bookmarks", "save", "total saves"],
    "views": ["video views", "views", "view", "total video views",
               "video plays", "plays"],
    "impressions": ["impressions", "total impressions"],
    "reach": ["reach", "total reach"],
    "engagements": ["engagements", "total engagements", "engagement"],
    "followers": ["followers", "follower count", "total followers",
                   "followers at time of post", "net follower growth"],
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


def _resolve_post_type(raw_type: str, platform: str) -> str:
    t = (raw_type or "").strip().lower()
    if platform == "TikTok":
        return "Video"
    if "reel" in t:
        return "Reel"
    if "carousel" in t or "album" in t:
        return "Carousel"
    if "video" in t:
        return "Reel"
    if "image" in t or "photo" in t or "static" in t:
        return "Static Image"
    if "story" in t:
        return "Story"
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
        post_type = _resolve_post_type(raw_type, platform)

        caption = str(row.get(col_map.get("caption_text", ""), ""))
        if caption == "nan":
            caption = ""
        hashtags = _extract_hashtags(caption)

        def safe_int(val):
            try:
                return int(float(val))
            except (ValueError, TypeError):
                return 0

        likes = safe_int(row.get(col_map.get("likes", ""), 0))
        comments = safe_int(row.get(col_map.get("comments", ""), 0))
        shares = safe_int(row.get(col_map.get("shares", ""), 0))
        saves = safe_int(row.get(col_map.get("saves", ""), 0))
        views = safe_int(row.get(col_map.get("views", ""), 0))

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
            "engagement_rate_manual": "",
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
    """Import a Sprout Social Profile Report."""
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

        def safe_int(val):
            try:
                return int(float(val))
            except (ValueError, TypeError):
                return 0

        followers = safe_int(row.get(col_map.get("followers", ""), 0))
        rows.append({
            "brand": brand,
            "platform": platform,
            "handle": raw_brand,
            "followers": followers,
            "following": 0,
            "total_posts": 0,
            "bio_text": "",
            "bio_link": "",
            "is_verified": "Yes",
            "profile_category": "Alcohol Brand",
            "date_collected": datetime.now().strftime("%Y-%m-%d"),
            "notes": "Imported from Sprout Social",
        })

    return rows


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
        fpath = os.path.join(sprout_dir, fname)
        try:
            sample = pd.read_csv(fpath, encoding="utf-8-sig", nrows=2)
        except Exception:
            continue

        cols_lower = [c.lower().strip() for c in sample.columns]
        col_text = " ".join(cols_lower)

        has_post_metrics = any(
            kw in col_text for kw in ["likes", "reactions", "comments", "engagements"]
        )
        has_profile_metrics = any(
            kw in col_text for kw in ["followers", "follower count"]
        )

        if has_post_metrics:
            posts = import_sprout_posts(fpath)
            all_posts.extend(posts)
            imported_files.append(fname)

        if has_profile_metrics and not has_post_metrics:
            profiles = import_sprout_profiles(fpath)
            all_profiles.extend(profiles)
            imported_files.append(fname)

    files = []

    # Write posts_data.csv
    if all_posts:
        posts_path = os.path.join(output_dir, "posts_data.csv")
        pd.DataFrame(all_posts).to_csv(posts_path, index=False)
        files.append(posts_path)

    # Write brand_profiles.csv
    if all_profiles:
        profiles_path = os.path.join(output_dir, "brand_profiles.csv")
        pd.DataFrame(all_profiles).to_csv(profiles_path, index=False)
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
