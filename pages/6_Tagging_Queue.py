"""
Page 6: Tagging Queue — dev only (?dev=1)
==========================================
Two tabs:
  Tab 1 – Queue: hero-brand Sprout posts not yet in manual_posts.csv.
           Tag one at a time (pillar / funnel / collab / sku / theme).
           Submit → append to manual_posts.csv, bust cache, rerun.
  Tab 2 – Add Off-Sprout Post: manual entry form for Partner / Influencer /
           Collective posts that live on a non-hero account (Sprout never
           captured these). Append with is_manual_entry=Yes flag.

Access: append ?dev=1 to any client URL, e.g.
  http://localhost:8501/?client=cuervo&dev=1
"""

import csv
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import streamlit as st

from client_context import get_client
from config import COLLAB_AMPLIFIED_TYPES, COLLAB_OWNED_TYPES

# ── Dev guard ────────────────────────────────────────────────────────────────

_dev = str(st.query_params.get("dev", "")).lower() in ("1", "true", "yes")
if not _dev:
    st.set_page_config(page_title="Tagging Queue", layout="wide")
    st.error("This page requires **?dev=1** in the URL.")
    st.caption("Example: `/?client=cuervo&dev=1` then navigate to Tagging Queue.")
    st.stop()

# ── Data guard ───────────────────────────────────────────────────────────────

if "results" not in st.session_state:
    st.warning("Go to the **Home** page first to load data.")
    st.stop()

cfg = get_client()
st.logo(cfg.app_logo_path)
st.markdown(cfg.custom_css, unsafe_allow_html=True)


# ── Helpers ──────────────────────────────────────────────────────────────────

def _get_raw_hero_posts(sprout_dir: str, hero_brand: str) -> pd.DataFrame:
    """Read raw Sprout post-level CSVs and return hero brand feed posts.

    Mirrors the file-detection logic in import_sprout_directory() so we
    read the same files — without applying the manual_posts.csv override.
    """
    from sprout_import import import_sprout_posts

    all_posts: list[dict] = []
    if not os.path.isdir(sprout_dir):
        return pd.DataFrame()

    for fname in sorted(os.listdir(sprout_dir)):
        if not fname.lower().endswith(".csv"):
            continue
        # Skip the manual posts file and benchmark files
        if fname.lower() == "manual_posts.csv" or fname.lower().startswith("benchmark_csv"):
            continue
        fpath = os.path.join(sprout_dir, fname)
        try:
            sample = pd.read_csv(fpath, encoding="utf-8-sig", nrows=2)
            cols_lower = [c.lower().strip() for c in sample.columns]
            col_text = " ".join(cols_lower)
            is_post_level = (
                any(kw in col_text for kw in ["post id", "permalink", "perma link"])
                or ("link" in cols_lower and "post" in cols_lower)
            )
            is_aggregate = any(
                kw in col_text
                for kw in ["audience", "net audience growth", "published posts",
                            "published posts & reels"]
            )
            if is_post_level and not is_aggregate:
                all_posts.extend(import_sprout_posts(fpath))
        except Exception:
            continue

    if not all_posts:
        return pd.DataFrame()

    df = pd.DataFrame(all_posts)
    if "brand" in df.columns:
        df = df[df["brand"] == hero_brand]
    # Drop stories — queue is for feed posts only
    if "is_story" in df.columns:
        df = df[df["is_story"].astype(str).str.lower() != "yes"]
    # Drop rows without a real URL
    if "post_url" in df.columns:
        df = df[df["post_url"].str.startswith("http", na=False)]
    return df.reset_index(drop=True)


def _get_untagged_posts(sprout_dir: str, hero_brand: str) -> pd.DataFrame:
    """Return hero brand Sprout posts whose post_url is not in manual_posts.csv."""
    raw = _get_raw_hero_posts(sprout_dir, hero_brand)
    if raw.empty:
        return raw

    manual_path = os.path.join(sprout_dir, "manual_posts.csv")
    if os.path.isfile(manual_path):
        try:
            manual = pd.read_csv(manual_path, encoding="utf-8-sig")
            if "post_url" in manual.columns and "post_url" in raw.columns:
                tagged_urls = set(manual["post_url"].dropna().str.strip())
                raw = raw[~raw["post_url"].str.strip().isin(tagged_urls)]
        except Exception:
            pass  # If manual CSV can't be read, show all hero posts

    if "post_date" in raw.columns:
        raw = raw.sort_values("post_date", ascending=False, ignore_index=True)
    return raw


def _owned_collab_label() -> str:
    """Derive the collaboration label for owned (hero brand) posts.

    COLLAB_OWNED_TYPES uses lowercase keys ("cuervo", "devils reserve").
    We find the match and title-case it for storage, e.g. "Cuervo".
    split_owned_collab() lowercases before comparing, so case doesn't matter.
    """
    hero_lower = cfg.hero_brand.lower()
    client_lower = cfg.client_id.lower().replace("_", " ")
    for k in COLLAB_OWNED_TYPES:
        if k in hero_lower or k in client_lower:
            return k.title()
    return cfg.hero_brand  # Fallback: just use the full hero brand name


def _pillar_themes() -> list[str]:
    """Unique content themes from this client's pillar map, sorted A-Z."""
    seen: set[str] = set()
    out: list[str] = []
    for t_list in cfg.pillar_map.values():
        for t in t_list:
            if t not in seen:
                seen.add(t)
                out.append(t)
    return sorted(out)


def _append_manual_row(manual_path: str, row: dict) -> None:
    """Append one row to manual_posts.csv with an exclusive file lock.

    Reads the existing CSV header (if present) to preserve column order.
    Fields in `row` not in the existing header are silently dropped
    (extrasaction='ignore'). Fields in the header missing from `row`
    default to empty string (restval='').
    """
    import portalocker

    has_content = os.path.isfile(manual_path) and os.path.getsize(manual_path) > 0
    if has_content:
        with open(manual_path, "r", encoding="utf-8-sig", newline="") as fh:
            reader = csv.reader(fh)
            try:
                fieldnames: list[str] = next(reader)
            except StopIteration:
                fieldnames = list(row.keys())
        write_header = False
    else:
        fieldnames = list(row.keys())
        write_header = True

    with open(manual_path, "a", newline="", encoding="utf-8-sig") as fh:
        portalocker.lock(fh, portalocker.LOCK_EX)
        try:
            writer = csv.DictWriter(
                fh, fieldnames=fieldnames,
                extrasaction="ignore", restval=""
            )
            if write_header:
                writer.writeheader()
            writer.writerow(row)
        finally:
            portalocker.unlock(fh)


# ── Derived config ────────────────────────────────────────────────────────────

SPROUT_DIR = cfg.sprout_dir
HERO = cfg.hero_brand
OWNED_COLLAB = _owned_collab_label()                              # e.g. "Cuervo"
COLLAB_OPTS = [OWNED_COLLAB] + [c.title() for c in sorted(COLLAB_AMPLIFIED_TYPES)]
AMPLIFIED_OPTS = [c.title() for c in sorted(COLLAB_AMPLIFIED_TYPES)]
FUNNEL_OPTS = list(cfg.content_mix_map.keys()) + ["Edutain"]
PILLAR_OPTS = list(cfg.pillar_map.keys())
THEME_OPTS = _pillar_themes()
SHOW_SKU = len(cfg.sku_strategy) > 1                              # True for Cuervo (3 SKUs)
SKU_OPTS = list(cfg.sku_strategy.keys()) if SHOW_SKU else []

# ── Page header ───────────────────────────────────────────────────────────────

st.title("Tagging Queue")
st.caption(f"**{HERO}** · dev only · tag untagged Sprout posts or add off-Sprout entries")

tab_queue, tab_manual = st.tabs(["Queue", "Add Off-Sprout Post"])


# ════════════════════════════════════════════════════════════════════════════
# Tab 1 — Queue
# ════════════════════════════════════════════════════════════════════════════

with tab_queue:
    untagged = _get_untagged_posts(SPROUT_DIR, HERO)

    if untagged.empty:
        st.success("Queue is empty — all hero posts are tagged. ✓")
    else:
        n = len(untagged)
        st.info(
            f"**{n} post{'s' if n != 1 else ''} in queue.** "
            "Tag each to include it in dashboard KPIs."
        )

        # ── Queue navigation ──────────────────────────────────────────────
        # Reset index when client changes to avoid out-of-bounds
        if (
            "queue_idx" not in st.session_state
            or st.session_state.get("queue_client") != cfg.client_id
        ):
            st.session_state["queue_idx"] = 0
            st.session_state["queue_client"] = cfg.client_id

        idx = min(int(st.session_state["queue_idx"]), n - 1)
        post = untagged.iloc[idx].to_dict()

        # ── Post preview card ─────────────────────────────────────────────
        st.caption(f"Post **{idx + 1}** of **{n}**")

        url = str(post.get("post_url", ""))
        if url.startswith("http"):
            st.markdown(f"[↗ Open post]({url})  `{url}`")
        else:
            st.code(url)

        col_meta, col_metrics = st.columns([3, 1])
        with col_meta:
            st.caption(
                f"**{post.get('platform', '')}** · "
                f"{post.get('post_type', '')} · "
                f"{str(post.get('post_date', ''))[:10]}"
            )
            caption = str(post.get("caption_text", ""))
            if caption:
                st.text_area(
                    "caption_preview", caption, height=100,
                    disabled=True, label_visibility="collapsed"
                )
            else:
                st.caption("_(no caption)_")

        with col_metrics:
            for label, key in [
                ("Likes", "likes"), ("Comments", "comments"),
                ("Saves", "saves"), ("Views", "views"),
            ]:
                raw_val = post.get(key, 0)
                try:
                    v = int(raw_val) if raw_val not in (None, "", "nan") else 0
                except (ValueError, TypeError):
                    v = 0
                st.metric(label, f"{v:,}" if v else "—")

        c_prev, c_skip, _ = st.columns([1, 1, 4])
        with c_prev:
            if st.button("← Prev", disabled=(idx == 0), key="q_prev"):
                st.session_state["queue_idx"] = idx - 1
                st.rerun()
        with c_skip:
            if st.button("Skip →", key="q_skip"):
                st.session_state["queue_idx"] = (idx + 1) % n
                st.rerun()

        st.divider()

        # ── Tagging form ──────────────────────────────────────────────────
        with st.form("queue_tag_form"):
            st.subheader("Tag this post")

            pillar_sel = st.selectbox("Content Pillar *", ["— select —"] + PILLAR_OPTS)
            funnel_sel = st.selectbox("Funnel Stage *", ["— select —"] + FUNNEL_OPTS)
            collab_sel = st.selectbox("Collaboration", COLLAB_OPTS, index=0)
            if SHOW_SKU:
                sku_sel = st.selectbox("SKU", ["(none)"] + SKU_OPTS)
            theme_sel = st.selectbox("Content Theme", ["— select —"] + THEME_OPTS)

            save_btn = st.form_submit_button("Save & Next →", type="primary")

        if save_btn:
            if pillar_sel == "— select —" or funnel_sel == "— select —":
                st.error("Content Pillar and Funnel Stage are required.")
            else:
                sku_val = (sku_sel if SHOW_SKU and sku_sel != "(none)" else "")
                theme_val = (theme_sel if theme_sel != "— select —" else "")

                def _safe_int(v) -> int:
                    try:
                        return int(float(str(v))) if v not in (None, "", "nan") else 0
                    except (ValueError, TypeError):
                        return 0

                eng = sum(_safe_int(post.get(k)) for k in ["likes", "comments", "shares", "saves"])
                row = {
                    "brand":                  HERO,
                    "platform":               str(post.get("platform", "")),
                    "post_date":              str(post.get("post_date", ""))[:10],
                    "post_type":              str(post.get("post_type", "")),
                    "content_theme":          theme_val,
                    "collaboration":          collab_sel,
                    "content_pillar":         pillar_sel,
                    "sku":                    sku_val,
                    "content_mix_funnel":     funnel_sel,
                    "post_url":               url,
                    "likes":                  _safe_int(post.get("likes")),
                    "comments":               _safe_int(post.get("comments")),
                    "shares":                 _safe_int(post.get("shares")),
                    "saves":                  _safe_int(post.get("saves")),
                    "views":                  _safe_int(post.get("views")),
                    "caption_text":           str(post.get("caption_text", "")),
                    "post_time":              str(post.get("post_time", "")),
                    "video_length_seconds":   _safe_int(post.get("video_length_seconds")),
                    "hashtags":               str(post.get("hashtags", "")),
                    "impressions":            _safe_int(post.get("impressions")),
                    "engagement_rate_manual": str(post.get("engagement_rate_manual", "")),
                    "caption_tone":           str(post.get("caption_tone", "")),
                    "cta_type":               str(post.get("cta_type", "")),
                    "has_creator_collab":     str(post.get("has_creator_collab", "")),
                    "creator_handle":         str(post.get("creator_handle", "")),
                    "has_music_audio":        str(post.get("has_music_audio", "")),
                    "emoji_count_in_caption": _safe_int(post.get("emoji_count_in_caption")),
                    "caption_word_count":     _safe_int(post.get("caption_word_count")),
                    "mentions_count":         _safe_int(post.get("mentions_count")),
                    "is_paid_partnership":    str(post.get("is_paid_partnership", "")),
                    "total_engagement":       eng,
                }
                try:
                    _append_manual_row(
                        os.path.join(SPROUT_DIR, "manual_posts.csv"), row
                    )
                    st.cache_data.clear()
                    # Stay at same index — the tagged post disappears and the
                    # next post shifts into that position automatically
                    st.session_state["queue_idx"] = idx
                    st.success("Saved! Loading next post…")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Failed to save: {exc}")


# ════════════════════════════════════════════════════════════════════════════
# Tab 2 — Add Off-Sprout Post
# ════════════════════════════════════════════════════════════════════════════

with tab_manual:
    st.subheader("Add Off-Sprout Post")
    st.caption(
        "Use this for posts on a **partner, influencer, or collective account** "
        "that Sprout never captured (standalone posts on a non-hero account). "
        "These count toward hero brand amplified reach in all KPIs."
    )

    with st.form("off_sprout_form"):

        # ── Post identity ─────────────────────────────────────────────────
        st.markdown("**Post details**")
        post_url_m = st.text_input(
            "Post URL *",
            placeholder="https://www.instagram.com/p/…  or  https://www.tiktok.com/@…"
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            platform_m = st.selectbox("Platform *", ["Instagram", "TikTok"])
        with col2:
            post_type_m = st.selectbox(
                "Post Type *", ["Reel", "Carousel", "Image", "Video", "Story"]
            )
        with col3:
            import datetime
            post_date_m = st.date_input("Post Date *", value=datetime.date.today())

        caption_m = st.text_area("Caption text", height=80)

        # ── Metrics ───────────────────────────────────────────────────────
        st.markdown("**Metrics** _(type from partner's Insights screenshot)_")
        mc1, mc2, mc3 = st.columns(3)
        with mc1:
            likes_m    = st.number_input("Likes",       min_value=0, step=1, value=0)
            saves_m    = st.number_input("Saves",       min_value=0, step=1, value=0)
        with mc2:
            comments_m = st.number_input("Comments",    min_value=0, step=1, value=0)
            views_m    = st.number_input("Views",       min_value=0, step=1, value=0)
        with mc3:
            shares_m     = st.number_input("Shares",      min_value=0, step=1, value=0)
            impressions_m = st.number_input("Impressions", min_value=0, step=1, value=0)

        # ── Tags ──────────────────────────────────────────────────────────
        st.markdown("**Tags**")
        tg1, tg2 = st.columns(2)
        with tg1:
            collab_m = st.selectbox(
                "Collaboration *",
                ["— select —"] + AMPLIFIED_OPTS,
                help="Off-Sprout posts are always Partner, Influencer, or Collective."
            )
            pillar_m = st.selectbox("Content Pillar *", ["— select —"] + PILLAR_OPTS)
        with tg2:
            funnel_m = st.selectbox("Funnel Stage *", ["— select —"] + FUNNEL_OPTS)
            theme_m  = st.selectbox("Content Theme",  ["— select —"] + THEME_OPTS)

        if SHOW_SKU:
            sku_m = st.selectbox("SKU", ["(none)"] + SKU_OPTS)

        submit_manual = st.form_submit_button("Add Post →", type="primary")

    if submit_manual:
        errors: list[str] = []
        if not post_url_m.strip().startswith("http"):
            errors.append("Post URL must start with http.")
        if collab_m == "— select —":
            errors.append("Collaboration is required.")
        if pillar_m == "— select —":
            errors.append("Content Pillar is required.")
        if funnel_m == "— select —":
            errors.append("Funnel Stage is required.")

        if errors:
            for err in errors:
                st.error(err)
        else:
            sku_val_m   = (sku_m if SHOW_SKU and sku_m != "(none)" else "")
            theme_val_m = (theme_m if theme_m != "— select —" else "")
            eng_m = int(likes_m) + int(comments_m) + int(shares_m) + int(saves_m)
            row_m = {
                "brand":                  HERO,
                "platform":               platform_m,
                "post_date":              str(post_date_m),
                "post_type":              post_type_m,
                "content_theme":          theme_val_m,
                "collaboration":          collab_m,
                "content_pillar":         pillar_m,
                "sku":                    sku_val_m,
                "content_mix_funnel":     funnel_m,
                "post_url":               post_url_m.strip(),
                "likes":                  int(likes_m),
                "comments":               int(comments_m),
                "shares":                 int(shares_m),
                "saves":                  int(saves_m),
                "views":                  int(views_m),
                "caption_text":           caption_m,
                "post_time":              "",
                "video_length_seconds":   0,
                "hashtags":               "",
                "impressions":            int(impressions_m),
                "engagement_rate_manual": "",
                "caption_tone":           "",
                "cta_type":               "",
                "has_creator_collab":     "",
                "creator_handle":         "",
                "has_music_audio":        "",
                "emoji_count_in_caption": 0,
                "caption_word_count":     len(caption_m.split()) if caption_m else 0,
                "mentions_count":         0,
                "is_paid_partnership":    "",
                "total_engagement":       eng_m,
                "is_manual_entry":        "Yes",
            }
            try:
                _append_manual_row(
                    os.path.join(SPROUT_DIR, "manual_posts.csv"), row_m
                )
                st.cache_data.clear()
                st.success(
                    f"Added off-Sprout post for **{HERO}** ({collab_m}). "
                    "Navigate to any other page to see it in KPIs."
                )
                st.rerun()
            except Exception as exc:
                st.error(f"Failed to save: {exc}")
