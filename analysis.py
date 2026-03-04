"""
Core Analysis Engine for Social Media Intelligence.
Processes collected CSV data and produces all competitive metrics.
"""
from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from datetime import datetime
from typing import Any

from templates import CONTENT_THEMES, TONE_OPTIONS


def _get_brands():
    """Get brands list from active client config, falling back to templates."""
    try:
        from client_context import get_client
        return get_client().brands
    except Exception:
        from templates import BRANDS
        return BRANDS


def _parse_int(val: str) -> int:
    """Safely parse a string to int, handling commas, floats, negatives."""
    if not val:
        return 0
    val = val.strip().replace(",", "")
    try:
        return int(float(val))
    except (ValueError, TypeError):
        return 0


def load_posts(filepath: str) -> list[dict]:
    """Load and clean posts data from CSV."""
    posts = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip example rows
            if "Example row" in row.get("notes", ""):
                continue
            # Clean numeric fields
            for field in ["likes", "comments", "shares", "saves", "views",
                          "video_length_seconds", "emoji_count_in_caption",
                          "caption_word_count", "mentions_count"]:
                row[field] = _parse_int(row.get(field, ""))

            # Parse date
            date_str = row.get("post_date", "").strip()
            if date_str:
                try:
                    row["post_date_parsed"] = datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    row["post_date_parsed"] = None
            else:
                row["post_date_parsed"] = None

            # Parse time
            time_str = row.get("post_time", "").strip()
            if time_str:
                try:
                    row["post_time_parsed"] = datetime.strptime(time_str, "%H:%M").time()
                    row["post_hour"] = row["post_time_parsed"].hour
                except ValueError:
                    row["post_time_parsed"] = None
                    row["post_hour"] = None
            else:
                row["post_time_parsed"] = None
                row["post_hour"] = None

            # Auto-calculate caption metrics if not provided
            caption = row.get("caption_text", "") or ""
            if row["caption_word_count"] == 0 and caption:
                row["caption_word_count"] = len(caption.split())
            if row["emoji_count_in_caption"] == 0 and caption:
                row["emoji_count_in_caption"] = count_emojis(caption)

            # Calculate engagement
            total_engagement = row["likes"] + row["comments"] + row["shares"] + row["saves"]
            row["total_engagement"] = total_engagement

            posts.append(row)
    return posts


def load_profiles(filepath: str) -> list[dict]:
    """Load brand profile data."""
    profiles = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in ["followers", "following", "total_posts"]:
                row[field] = _parse_int(row.get(field, ""))
            # Parse aggregate ER (float, computed from competitor performance CSVs)
            agg_er = row.get("aggregate_er", "")
            try:
                row["aggregate_er"] = float(agg_er) if agg_er else 0.0
            except (ValueError, TypeError):
                row["aggregate_er"] = 0.0
            profiles.append(row)
    return profiles


def load_hashtags(filepath: str) -> list[dict]:
    """Load hashtag tracking data."""
    tags = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["times_used_in_30_days"] = _parse_int(row.get("times_used_in_30_days", ""))
            tags.append(row)
    return tags


def load_creators(filepath: str) -> list[dict]:
    """Load creator collaboration data."""
    creators = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if "Example row" in row.get("notes", ""):
                continue
            row["creator_follower_count"] = _parse_int(row.get("creator_follower_count", ""))
            creators.append(row)
    return creators


def count_emojis(text: str) -> int:
    """Count emoji characters in text."""
    emoji_pattern = re.compile(
        "[\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001f926-\U0001f937"
        "\U0001F1F2-\U0001F1F4"
        "\U0001F620-\U0001F640"
        "\U0001F910-\U0001F9FF"
        "]", flags=re.UNICODE
    )
    return len(emoji_pattern.findall(text))


def extract_hashtags(text: str) -> list[str]:
    """Extract hashtags from text."""
    return re.findall(r"#\w+", text or "")


# ─── ANALYSIS FUNCTIONS ───────────────────────────────────────────────


def analyze_posting_frequency(posts: list[dict]) -> dict[str, Any]:
    """Analyze posting frequency by brand, platform, day, hour, and content type."""
    results = {}

    # Determine actual date span from all posts to calculate accurate frequency
    all_dates = [p["post_date_parsed"] for p in posts if p.get("post_date_parsed")]
    if all_dates:
        date_span_days = (max(all_dates) - min(all_dates)).days + 1
    else:
        date_span_days = 30  # fallback
    weeks_in_span = max(date_span_days / 7, 1)

    brands = _get_brands()
    for brand in brands:
        brand_posts = [p for p in posts if p["brand"] == brand]
        results[brand] = {}

        for platform in ["Instagram", "TikTok"]:
            plat_posts = [p for p in brand_posts if p["platform"] == platform]
            total = len(plat_posts)

            # Posts per week based on actual date range of data
            per_week = round(total / weeks_in_span, 1) if total > 0 else 0

            # By day of week
            day_counts = Counter()
            for p in plat_posts:
                if p["post_date_parsed"]:
                    day_counts[p["post_date_parsed"].strftime("%A")] += 1

            # By hour
            hour_counts = Counter()
            for p in plat_posts:
                if p["post_hour"] is not None:
                    hour_counts[p["post_hour"]] += 1

            # By content type
            type_counts = Counter(p.get("post_type", "Unknown") for p in plat_posts)

            # Best posting days (top 3)
            best_days = day_counts.most_common(3)

            # Best posting hours (top 3)
            best_hours = hour_counts.most_common(3)

            results[brand][platform] = {
                "total_posts": total,
                "date_span_days": date_span_days,
                "posts_per_week": per_week,
                "by_day": dict(day_counts),
                "by_hour": dict(hour_counts),
                "by_content_type": dict(type_counts),
                "best_days": best_days,
                "best_hours": best_hours,
            }

    return results


def analyze_engagement(posts: list[dict], profiles: list[dict],
                       benchmark: dict = None) -> dict[str, Any]:
    """Analyze engagement by brand, platform, and content type.
    Uses raw engagement counts as primary metric and engagements per
    1K followers for cross-brand normalization."""
    # Build follower lookup
    follower_map = {}
    for p in profiles:
        key = (p["brand"], p["platform"])
        follower_map[key] = p["followers"]

    # Override followers with benchmark's (more current) count
    if benchmark:
        for brand_name, bdata in benchmark.items():
            key = (brand_name, "Instagram")  # Benchmark is IG-only
            if bdata.get("followers", 0) > 0:
                follower_map[key] = bdata["followers"]

    results = {}

    for brand in _get_brands():
        brand_posts = [p for p in posts if p["brand"] == brand]
        results[brand] = {}

        for platform in ["Instagram", "TikTok"]:
            plat_posts = [p for p in brand_posts if p["platform"] == platform]
            followers = follower_map.get((brand, platform), 0)

            # Overall averages
            if plat_posts:
                avg_engagement = sum(p["total_engagement"] for p in plat_posts) / len(plat_posts)
                avg_likes = sum(p["likes"] for p in plat_posts) / len(plat_posts)
                avg_comments = sum(p["comments"] for p in plat_posts) / len(plat_posts)
                avg_shares = sum(p["shares"] for p in plat_posts) / len(plat_posts)
                avg_views = sum(p["views"] for p in plat_posts) / len(plat_posts)
            else:
                avg_engagement = avg_likes = avg_comments = avg_shares = avg_views = 0

            # Engagements per 1K followers (for cross-brand comparison)
            eng_per_1k = round((avg_engagement / followers) * 1000, 2) if followers > 0 else 0

            # By content type: avg engagements per type
            type_engagement = defaultdict(list)
            for p in plat_posts:
                type_engagement[p.get("post_type", "Unknown")].append(p["total_engagement"])

            type_avg = {}
            for ptype, engs in type_engagement.items():
                type_avg[ptype] = round(sum(engs) / len(engs), 1) if engs else 0

            # Top 10 posts by total engagement
            top_10 = sorted(plat_posts, key=lambda x: x["total_engagement"], reverse=True)[:10]
            top_10_summary = [{
                "url": p.get("post_url", ""),
                "date": p.get("post_date", ""),
                "type": p.get("post_type", ""),
                "total_engagement": p["total_engagement"],
                "likes": p["likes"],
                "comments": p["comments"],
                "views": p["views"],
                "theme": p.get("content_theme", ""),
                "caption_preview": (p.get("caption_text", "") or "")[:100],
            } for p in top_10]

            # Benchmark bonus metrics (IG only, from external benchmark CSV)
            bench = benchmark.get(brand, {}) if benchmark and platform == "Instagram" else {}

            results[brand][platform] = {
                "followers": followers,
                "avg_engagements": round(avg_engagement, 1),
                "engagement_per_1k_followers": eng_per_1k,
                "avg_likes": round(avg_likes, 1),
                "avg_comments": round(avg_comments, 1),
                "avg_shares": round(avg_shares, 1),
                "avg_views": round(avg_views, 1),
                "engagement_by_type": type_avg,
                "top_10_posts": top_10_summary,
                # Benchmark fields (keep for follower/reels data)
                "benchmark_reels_count": bench.get("reels_count", 0),
                "benchmark_reels_engagement": bench.get("reels_engagement", 0),
                "benchmark_avg_hashtags": bench.get("avg_hashtags_per_post", 0),
                "benchmark_avg_engagement": bench.get("avg_engagement", 0),
                "benchmark_posts": bench.get("posts", 0),
                "has_benchmark": bool(bench),
            }

    return results


def analyze_captions(posts: list[dict]) -> dict[str, Any]:
    """Analyze caption patterns: length, tone, emoji usage, CTAs."""
    results = {}

    for brand in _get_brands():
        brand_posts = [p for p in posts if p["brand"] == brand]
        results[brand] = {}

        for platform in ["Instagram", "TikTok"]:
            plat_posts = [p for p in brand_posts if p["platform"] == platform]

            if not plat_posts:
                results[brand][platform] = {
                    "avg_caption_length": 0,
                    "avg_word_count": 0,
                    "avg_emoji_count": 0,
                    "tone_distribution": {},
                    "cta_distribution": {},
                    "top_ctas": [],
                }
                continue

            # Caption length
            caption_lengths = [len(p.get("caption_text", "") or "") for p in plat_posts]
            word_counts = [p["caption_word_count"] for p in plat_posts]
            emoji_counts = [p["emoji_count_in_caption"] for p in plat_posts]

            avg_len = sum(caption_lengths) / len(caption_lengths)
            avg_words = sum(word_counts) / len(word_counts)
            avg_emojis = sum(emoji_counts) / len(emoji_counts)

            # Tone distribution
            tones = Counter(p.get("caption_tone", "Unknown") for p in plat_posts if p.get("caption_tone"))

            # CTA distribution
            ctas = Counter(p.get("cta_type", "None") for p in plat_posts if p.get("cta_type"))

            # Correlation: do longer captions get more engagement?
            if len(plat_posts) >= 5:
                sorted_by_eng = sorted(plat_posts, key=lambda x: x.get("total_engagement", 0), reverse=True)
                top_half = sorted_by_eng[:len(sorted_by_eng)//2]
                bottom_half = sorted_by_eng[len(sorted_by_eng)//2:]
                top_avg_words = sum(p["caption_word_count"] for p in top_half) / len(top_half) if top_half else 0
                bottom_avg_words = sum(p["caption_word_count"] for p in bottom_half) / len(bottom_half) if bottom_half else 0
                caption_length_insight = "longer" if top_avg_words > bottom_avg_words * 1.15 else \
                    "shorter" if bottom_avg_words > top_avg_words * 1.15 else "similar length"
            else:
                caption_length_insight = "insufficient data"

            results[brand][platform] = {
                "avg_caption_length_chars": round(avg_len, 1),
                "avg_word_count": round(avg_words, 1),
                "avg_emoji_count": round(avg_emojis, 1),
                "tone_distribution": dict(tones.most_common()),
                "cta_distribution": dict(ctas.most_common()),
                "top_ctas": ctas.most_common(3),
                "caption_length_vs_engagement": caption_length_insight,
            }

    return results


def analyze_hashtags(posts: list[dict], hashtag_data: list[dict]) -> dict[str, Any]:
    """Analyze hashtag strategies across brands."""
    results = {}

    for brand in _get_brands():
        brand_posts = [p for p in posts if p["brand"] == brand]
        brand_tags = [h for h in hashtag_data if h["brand"] == brand]

        # Extract all hashtags from posts
        all_tags = []
        tags_per_post = []
        for p in brand_posts:
            caption_tags = extract_hashtags(p.get("caption_text", ""))
            field_tags = extract_hashtags(p.get("hashtags", ""))
            combined = list(set(caption_tags + field_tags))
            all_tags.extend(combined)
            tags_per_post.append(len(combined))

        tag_freq = Counter(t.lower() for t in all_tags)

        # Branded vs. community vs. trending
        branded_tags = [h["hashtag"].lower() for h in brand_tags if h.get("is_branded_hashtag", "").lower() == "yes"]

        branded_usage = sum(tag_freq.get(t, 0) for t in branded_tags)
        total_tag_usage = sum(tag_freq.values())

        results[brand] = {
            "unique_hashtags": len(tag_freq),
            "avg_hashtags_per_post": round(sum(tags_per_post) / len(tags_per_post), 1) if tags_per_post else 0,
            "top_15_hashtags": tag_freq.most_common(15),
            "branded_hashtags": branded_tags,
            "branded_hashtag_pct": round(branded_usage / total_tag_usage * 100, 1) if total_tag_usage else 0,
            "total_hashtag_usage": total_tag_usage,
        }

    return results


def analyze_content_themes(posts: list[dict]) -> dict[str, Any]:
    """Analyze content theme/pillar distribution and performance."""
    results = {}

    for brand in _get_brands():
        brand_posts = [p for p in posts if p["brand"] == brand]

        # Theme distribution
        themes = Counter(p.get("content_theme", "Unknown") for p in brand_posts if p.get("content_theme"))

        # Theme performance (avg engagements per theme)
        theme_engagement = defaultdict(list)
        for p in brand_posts:
            theme = p.get("content_theme", "Unknown")
            if theme:
                theme_engagement[theme].append(p.get("total_engagement", 0))

        theme_performance = {}
        for theme, engs in theme_engagement.items():
            theme_performance[theme] = {
                "count": len(engs),
                "avg_engagements": round(sum(engs) / len(engs), 1) if engs else 0,
                "pct_of_content": round(len(engs) / len(brand_posts) * 100, 1) if brand_posts else 0,
            }

        results[brand] = {
            "theme_distribution": dict(themes.most_common()),
            "theme_performance": theme_performance,
            "top_theme": themes.most_common(1)[0] if themes else ("N/A", 0),
            "best_performing_theme": max(theme_performance.items(),
                                         key=lambda x: x[1]["avg_engagements"])[0] if theme_performance else "N/A",
        }

    return results


def analyze_creators(posts: list[dict], creator_data: list[dict]) -> dict[str, Any]:
    """Analyze creator collaboration patterns."""
    results = {}

    for brand in _get_brands():
        brand_posts = [p for p in posts if p["brand"] == brand]
        brand_creators = [c for c in creator_data if c["brand"] == brand]

        # Collab posts from main posts data
        collab_posts = [p for p in brand_posts
                        if p.get("has_creator_collab", "").lower() in ("yes", "true", "1")]
        non_collab_posts = [p for p in brand_posts
                           if p.get("has_creator_collab", "").lower() not in ("yes", "true", "1")]

        collab_count = len(collab_posts)
        total = len(brand_posts)

        # Engagement comparison: collab vs. non-collab (avg total engagements)
        collab_engs = [p.get("total_engagement", 0) for p in collab_posts]
        non_collab_engs = [p.get("total_engagement", 0) for p in non_collab_posts]
        collab_avg_eng = sum(collab_engs) / len(collab_engs) if collab_engs else 0
        non_collab_avg_eng = sum(non_collab_engs) / len(non_collab_engs) if non_collab_engs else 0

        # Paid vs. organic collabs
        paid = sum(1 for p in collab_posts if p.get("is_paid_partnership", "").lower() in ("yes", "true", "1"))

        # Unique creators
        unique_creators = set()
        for c in brand_creators:
            if c.get("creator_handle"):
                unique_creators.add(c["creator_handle"].lower())
        for p in collab_posts:
            if p.get("creator_handle"):
                unique_creators.add(p["creator_handle"].lower())

        results[brand] = {
            "total_collab_posts": collab_count,
            "collab_pct": round(collab_count / total * 100, 1) if total else 0,
            "unique_creators": len(unique_creators),
            "avg_collab_engagements": round(collab_avg_eng, 1),
            "avg_non_collab_engagements": round(non_collab_avg_eng, 1),
            "collab_engagement_lift": round(collab_avg_eng - non_collab_avg_eng, 1),
            "paid_partnerships": paid,
            "organic_collabs": collab_count - paid,
        }

    return results


def generate_hero_recommendations(
    frequency: dict,
    engagement: dict,
    captions: dict,
    hashtags: dict,
    themes: dict,
    creators: dict,
    hero_brand: str | None = None,
    brands: list[str] | None = None,
) -> list[dict]:
    """Generate actionable recommendations for the hero brand based on competitive analysis."""
    recs = []
    if hero_brand is None:
        try:
            from client_context import get_client
            hero_brand = get_client().hero_brand
        except Exception:
            hero_brand = "Jose Cuervo"
    if brands is None:
        brands = _get_brands()

    hero = hero_brand

    # 1. Posting frequency comparison
    competitors = [b for b in brands if b != hero]
    for platform in ["Instagram", "TikTok"]:
        hero_freq = frequency.get(hero, {}).get(platform, {}).get("posts_per_week", 0)
        comp_freqs = [frequency.get(b, {}).get(platform, {}).get("posts_per_week", 0) for b in competitors]
        avg_comp = sum(comp_freqs) / len(comp_freqs) if comp_freqs else 0

        if hero_freq < avg_comp * 0.8:
            recs.append({
                "category": "Posting Frequency",
                "platform": platform,
                "priority": "High",
                "insight": f"{hero} posts {hero_freq}x/week on {platform} vs. competitor avg of {round(avg_comp, 1)}x/week",
                "recommendation": f"Increase {platform} posting frequency to at least {round(avg_comp, 1)}x/week to maintain visibility",
            })

    # 2. Content type gaps
    for platform in ["Instagram", "TikTok"]:
        hero_types = frequency.get(hero, {}).get(platform, {}).get("by_content_type", {})

        # Check which types competitors use that hero doesn't
        comp_types = set()
        for b in competitors:
            for t in frequency.get(b, {}).get(platform, {}).get("by_content_type", {}).keys():
                comp_types.add(t)

        missing_types = comp_types - set(hero_types.keys())
        if missing_types:
            recs.append({
                "category": "Content Diversification",
                "platform": platform,
                "priority": "Medium",
                "insight": f"{hero} is not using these content types on {platform}: {', '.join(missing_types)}",
                "recommendation": f"Test {', '.join(missing_types)} content — competitors are finding success with these formats",
            })

    # 3. Engagement benchmarking (per 1K followers for fair comparison)
    for platform in ["Instagram", "TikTok"]:
        hero_epk = engagement.get(hero, {}).get(platform, {}).get("engagement_per_1k_followers", 0)
        comp_epks = [engagement.get(b, {}).get(platform, {}).get("engagement_per_1k_followers", 0) for b in competitors]
        best_comp_epk = max(comp_epks) if comp_epks else 0
        best_comp_name = competitors[comp_epks.index(best_comp_epk)] if comp_epks and best_comp_epk > 0 else "Unknown"

        if hero_epk < best_comp_epk * 0.7 and best_comp_epk > 0:
            recs.append({
                "category": "Engagement Gap",
                "platform": platform,
                "priority": "High",
                "insight": f"{hero}'s avg eng/1K followers ({hero_epk}) trails {best_comp_name} ({best_comp_epk}) on {platform}",
                "recommendation": f"Study {best_comp_name}'s top-performing content and adapt successful patterns",
            })

    # 5. Creator strategy
    hero_collabs = creators.get(hero, {})
    comp_collab_rates = [creators.get(b, {}).get("collab_pct", 0) for b in competitors]
    avg_collab = sum(comp_collab_rates) / len(comp_collab_rates) if comp_collab_rates else 0

    if hero_collabs.get("collab_pct", 0) < avg_collab * 0.5 and avg_collab > 0:
        recs.append({
            "category": "Creator Strategy",
            "platform": "Both",
            "priority": "High",
            "insight": f"{hero} collab rate ({hero_collabs.get('collab_pct', 0)}%) is well below competitor avg ({round(avg_collab, 1)}%)",
            "recommendation": "Invest in creator partnerships — especially micro-creators (10K-100K followers) resonating with Gen Z",
        })

    # Check if collabs drive engagement lift across the category
    for b in competitors:
        lift = creators.get(b, {}).get("collab_engagement_lift", 0)
        if lift > 50:
            recs.append({
                "category": "Creator Strategy",
                "platform": "Both",
                "priority": "Medium",
                "insight": f"{b} sees +{round(lift)} avg engagements from creator collabs vs. brand-only content",
                "recommendation": "Creator collabs outperform brand content across the category — prioritize partnerships",
            })
            break  # One example is enough

    # 6. Hashtag strategy
    hero_tags = hashtags.get(hero, {})
    for b in competitors:
        comp_tags = hashtags.get(b, {})
        if comp_tags.get("avg_hashtags_per_post", 0) > hero_tags.get("avg_hashtags_per_post", 0) * 1.5:
            recs.append({
                "category": "Hashtag Strategy",
                "platform": "Both",
                "priority": "Low",
                "insight": f"{b} uses {comp_tags['avg_hashtags_per_post']} hashtags/post vs {hero}'s {hero_tags.get('avg_hashtags_per_post', 0)}",
                "recommendation": "Test increasing hashtag count to improve discoverability",
            })
            break

    # 7. Caption / CTA insights
    for platform in ["Instagram", "TikTok"]:
        hero_cap = captions.get(hero, {}).get(platform, {})
        for b in competitors:
            comp_cap = captions.get(b, {}).get(platform, {})
            comp_eng = engagement.get(b, {}).get(platform, {}).get("engagement_per_1k_followers", 0)
            hero_eng = engagement.get(hero, {}).get(platform, {}).get("engagement_per_1k_followers", 0)

            if comp_eng > hero_eng and comp_cap.get("top_ctas"):
                top_cta = comp_cap["top_ctas"][0][0] if comp_cap["top_ctas"] else "None"
                if top_cta != "None":
                    recs.append({
                        "category": "Caption Strategy",
                        "platform": platform,
                        "priority": "Medium",
                        "insight": f"{b} (higher engagement) heavily uses '{top_cta}' CTAs on {platform}",
                        "recommendation": f"Incorporate more '{top_cta}' CTAs in {platform} captions",
                    })
                    break

    # 8. Timing optimization
    for platform in ["Instagram", "TikTok"]:
        best_hours_across = Counter()
        for b in brands:
            bh = frequency.get(b, {}).get(platform, {}).get("best_hours", [])
            for hour, count in bh:
                best_hours_across[hour] += count

        hero_hours = frequency.get(hero, {}).get(platform, {}).get("by_hour", {})
        top_category_hours = best_hours_across.most_common(3)

        if top_category_hours:
            hour_strs = [f"{h}:00" for h, _ in top_category_hours]
            recs.append({
                "category": "Posting Schedule",
                "platform": platform,
                "priority": "Low",
                "insight": f"Category-wide peak posting hours on {platform}: {', '.join(hour_strs)}",
                "recommendation": f"Align {platform} posting schedule to peak hours: {', '.join(hour_strs)}",
            })

    # Sort by priority
    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    recs.sort(key=lambda x: priority_order.get(x["priority"], 3))

    return recs


def run_full_analysis(data_dir: str, benchmark: dict = None) -> dict[str, Any]:
    """Run the complete analysis pipeline and return all results."""
    import os

    posts = load_posts(os.path.join(data_dir, "posts_data.csv"))
    profiles = load_profiles(os.path.join(data_dir, "brand_profiles.csv"))
    hashtag_data = load_hashtags(os.path.join(data_dir, "hashtag_tracking.csv"))
    creator_data = load_creators(os.path.join(data_dir, "creator_collabs.csv"))

    frequency = analyze_posting_frequency(posts)
    engagement = analyze_engagement(posts, profiles, benchmark=benchmark)
    caption_analysis = analyze_captions(posts)
    hashtag_analysis = analyze_hashtags(posts, hashtag_data)
    theme_analysis = analyze_content_themes(posts)
    creator_analysis = analyze_creators(posts, creator_data)
    recommendations = generate_hero_recommendations(
        frequency, engagement, caption_analysis,
        hashtag_analysis, theme_analysis, creator_analysis
    )

    return {
        "posts": posts,
        "profiles": profiles,
        "benchmark": benchmark or {},
        "frequency": frequency,
        "engagement": engagement,
        "captions": caption_analysis,
        "hashtags": hashtag_analysis,
        "themes": theme_analysis,
        "creators": creator_analysis,
        "recommendations": recommendations,
    }
