"""
Social Intelligence Dashboard — Multi-Client
=================================================
Main entry point. Run with: streamlit run app.py

Supports multiple clients via ?client= query parameter.
No param → internal client picker. ?client=cuervo → Cuervo dashboard.
"""

import os
import sys
import tempfile
from datetime import datetime

import pandas as pd
import streamlit as st

# Ensure project root is importable
sys.path.insert(0, os.path.dirname(__file__))

from client_context import load_client_config, get_client, set_active_client, list_available_clients
from config import CHART_TEMPLATE, CHART_FONT

# ── Client Routing ───────────────────────────────────────────────────
# Must happen before set_page_config so we can use client's page_title.

client_id = st.query_params.get("client", None)

if client_id is None:
    # Internal view — client picker
    st.set_page_config(page_title="Poplife | Social Intel", page_icon="favicon.png",
                       layout="wide", initial_sidebar_state="expanded")
    st.title("Poplife — Social Media Intelligence")
    st.caption("Select a client to launch their dashboard")

    available = list_available_clients()
    if not available:
        st.error("No client configurations found in clients/ directory.")
        st.stop()

    # Build display names from each client's config
    display_names = {}
    for cid in available:
        try:
            _cfg = load_client_config(cid)
            display_names[cid] = _cfg.hero_brand
        except Exception:
            display_names[cid] = cid

    selected = st.selectbox(
        "Select Client",
        available,
        format_func=lambda x: display_names.get(x, x),
    )
    if st.button("Launch Dashboard"):
        st.query_params["client"] = selected
        st.rerun()
    st.stop()

# Load client config
try:
    cfg = load_client_config(client_id)
    set_active_client(cfg)
except Exception as e:
    st.set_page_config(page_title="Error", layout="wide")
    st.error(f"Failed to load client '{client_id}': {e}")
    st.stop()

st.set_page_config(
    page_title=cfg.page_title,
    page_icon=cfg.favicon_path,
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(cfg.custom_css, unsafe_allow_html=True)

# Store config in session state for pages
st.session_state["client_config"] = cfg


# ── Data Loading ──────────────────────────────────────────────────────

SPROUT_INPUT_DIR = cfg.sprout_dir
SPROUT_OUTPUT_DIR = cfg.sprout_output_dir


@st.cache_data(show_spinner="Running competitive analysis...")
def load_demo(client_id: str):
    from sample_data import generate_all_sample_data
    from analysis import run_full_analysis
    tmp = os.path.join(tempfile.gettempdir(), f"{client_id}_demo_streamlit")
    os.makedirs(tmp, exist_ok=True)
    generate_all_sample_data(tmp)
    return run_full_analysis(tmp), tmp


def _sprout_fingerprint(sprout_dir: str) -> str:
    """Return a hash of CSV filenames + sizes + code version so cache busts
    when files change OR analysis logic is updated."""
    import hashlib
    # Bump this version whenever sprout_import.py or analysis.py logic changes
    CODE_VERSION = "v33_exclude_stories_from_analysis"
    entries = [CODE_VERSION]
    if os.path.isdir(sprout_dir):
        for f in sorted(os.listdir(sprout_dir)):
            if f.lower().endswith(".csv"):
                fp = os.path.join(sprout_dir, f)
                entries.append(f"{f}:{os.path.getsize(fp)}")
    return hashlib.md5("|".join(entries).encode()).hexdigest()


def load_sprout(sprout_dir: str, output_dir: str, fingerprint: str = ""):
    from sprout_import import import_sprout_directory, import_benchmark_csv
    from analysis import run_full_analysis
    os.makedirs(output_dir, exist_ok=True)

    # Load benchmark CSV if present (e.g. Benchmark_CSV_ig_*.csv)
    benchmark_data = {}
    if os.path.isdir(sprout_dir):
        for f in sorted(os.listdir(sprout_dir)):
            if f.lower().startswith("benchmark_csv") and f.lower().endswith(".csv"):
                benchmark_data = import_benchmark_csv(os.path.join(sprout_dir, f))
                break  # Only one benchmark file expected

    # Re-import from Sprout CSVs when fingerprint changes (new data or code version bump).
    # Store last fingerprint so we know when to reimport.
    posts_path = os.path.join(output_dir, "posts_data.csv")
    fp_path = os.path.join(output_dir, ".fingerprint")
    last_fp = ""
    if os.path.isfile(fp_path):
        with open(fp_path) as _f:
            last_fp = _f.read().strip()
    if os.path.isfile(posts_path) and last_fp == fingerprint:
        stats = {"skipped": True, "reason": "posts_data.csv up to date"}
    else:
        # Remove stale posts_data so import_sprout_directory regenerates it
        if os.path.isfile(posts_path):
            os.remove(posts_path)
        files, stats = import_sprout_directory(sprout_dir, output_dir)
        with open(fp_path, "w") as _f:
            _f.write(fingerprint)

    results = run_full_analysis(output_dir, benchmark=benchmark_data)
    return results, output_dir, stats


@st.cache_data(show_spinner="Analyzing your data...")
def load_custom(data_dir: str):
    from analysis import run_full_analysis
    return run_full_analysis(data_dir)


def results_to_df(results: dict) -> pd.DataFrame:
    """Convert posts list[dict] to a DataFrame with clean types."""
    posts = results["posts"]
    df = pd.DataFrame(posts)
    # Keep only useful columns, drop parsed objects
    drop = [c for c in df.columns if c.endswith("_parsed")]
    df = df.drop(columns=drop, errors="ignore")
    for col in ["likes", "comments", "shares", "saves", "views",
                 "total_engagement", "video_length_seconds",
                 "caption_word_count", "emoji_count_in_caption"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
    if "engagement_rate" in df.columns:
        df["engagement_rate"] = pd.to_numeric(df["engagement_rate"], errors="coerce")
    if "post_date" in df.columns:
        df["post_date"] = pd.to_datetime(df["post_date"], errors="coerce")
    if "post_hour" in df.columns:
        df["post_hour"] = pd.to_numeric(df["post_hour"], errors="coerce")
    # Normalize content themes to current taxonomy
    if "content_theme" in df.columns:
        _theme_map = {
            # Legacy names → current taxonomy
            "Education (Tequila 101)": "Cocktail Highlights",
            "Music / Party": "Event/Activation",
            "Cocktail Recipe": "Cocktail Highlights",
            "Brand Heritage / Story": "Brand Heritage / Culture",
            "Creator Collab / UGC": "Creator Collab",
            "Event / Activation": "Event/Activation",
            "Cultural Moment / Holiday": "Cultural Moment/Holiday",
            "Meme / Humor": "Meme/Humor",
            "Giveaway / Promo": "Giveaway/Promo",
            "Product Showcase": "Product/Lifestyle",
            "Lifestyle/Aspirational": "Product/Lifestyle",
            "Events & Music": "Event/Activation",
            "Education & Recipes": "Cocktail Highlights",
        }
        df["content_theme"] = df["content_theme"].replace(_theme_map)

    # Apply manual theme overrides from CSV (hero brand posts only)
    override_path = os.path.join(cfg.sprout_dir, "theme_overrides.csv")
    if os.path.isfile(override_path) and "caption_text" in df.columns:
        try:
            overrides = pd.read_csv(override_path)
            if "Primary Theme" in overrides.columns and "Caption (first 200 chars)" in overrides.columns:
                hero_mask = df["brand"] == cfg.hero_brand
                for _, orow in overrides.iterrows():
                    caption_prefix = str(orow.get("Caption (first 200 chars)", ""))[:80].strip()
                    theme = str(orow["Primary Theme"]).strip()
                    if not caption_prefix or not theme:
                        continue
                    match = hero_mask & df["caption_text"].fillna("").str[:80].str.strip().eq(caption_prefix)
                    if match.any():
                        df.loc[match, "content_theme"] = theme
        except Exception:
            pass  # Silently skip if override CSV is malformed

    # Split "Edutain" posts: duplicate each as 0.5 Educate + 0.5 Entertain
    if "content_mix_funnel" in df.columns:
        edutain_mask = df["content_mix_funnel"] == "Edutain"
        if edutain_mask.any():
            edutain_rows = df[edutain_mask].copy()
            # Create Educate half
            edu_half = edutain_rows.copy()
            edu_half["content_mix_funnel"] = "Educate"
            edu_half["_mix_weight"] = 0.5
            # Create Entertain half
            ent_half = edutain_rows.copy()
            ent_half["content_mix_funnel"] = "Entertain"
            ent_half["_mix_weight"] = 0.5
            # Remove original Edutain rows and append split rows
            df = df[~edutain_mask]
            df["_mix_weight"] = 1.0
            df = pd.concat([df, edu_half, ent_half], ignore_index=True)

    return df


# ── Load Data ─────────────────────────────────────────────────────────

st.logo(cfg.app_logo_path)

# Check if Sprout Social CSVs are present
sprout_csvs = [f for f in os.listdir(SPROUT_INPUT_DIR) if f.lower().endswith(".csv")] \
    if os.path.isdir(SPROUT_INPUT_DIR) else []
has_sprout = len(sprout_csvs) > 0

data_options = ["Demo Data", "Custom CSV Folder"]
if has_sprout:
    data_options.insert(1, "Sprout Social Import")

# Default to Sprout if available, persist selection across page navigation
default_idx = 1 if has_sprout else 0
data_mode = st.sidebar.radio("Data source", data_options, index=default_idx, key="data_source")

if data_mode == "Demo Data":
    results, data_dir = load_demo(cfg.client_id)
elif data_mode == "Sprout Social Import":
    results, data_dir, sprout_stats = load_sprout(
        SPROUT_INPUT_DIR, SPROUT_OUTPUT_DIR,
        fingerprint=_sprout_fingerprint(SPROUT_INPUT_DIR)
    )
    if sprout_stats.get("skipped"):
        st.sidebar.success("Loaded data from posts_data.csv")
    else:
        st.sidebar.success(
            f"Imported {sprout_stats.get('total_posts', '?')} posts from "
            f"{sprout_stats.get('files_imported', '?')} file(s)"
        )
        if sprout_stats.get("brands_found"):
            st.sidebar.caption(f"Brands: {', '.join(sprout_stats['brands_found'])}")
    # Show benchmark status
    benchmark = results.get("benchmark", {})
    if benchmark:
        st.sidebar.caption(f"Benchmark: {len(benchmark)} brands (ER by Views)")
else:
    data_dir = st.sidebar.text_input("Path to CSV folder")
    if not data_dir or not os.path.isdir(data_dir):
        st.info("Enter a valid folder containing posts_data.csv, brand_profiles.csv, "
                "hashtag_tracking.csv, and creator_collabs.csv in the sidebar.")
        st.stop()
    results = load_custom(data_dir)

df = results_to_df(results)

# ── Global Filters ────────────────────────────────────────────────────

st.sidebar.markdown("---")
st.sidebar.subheader("Filters")

hero_only = st.sidebar.checkbox(f"{cfg.hero_brand} only")
if hero_only:
    sel_brands = [cfg.hero_brand]
else:
    sel_brands = st.sidebar.multiselect("Brands", cfg.brand_order, default=cfg.brand_order)

sel_platforms = st.sidebar.multiselect("Platforms", ["Instagram", "TikTok"],
                                       default=["Instagram", "TikTok"])

content_types = sorted(df["post_type"].dropna().unique().tolist()) if len(df) else []
sel_types = st.sidebar.multiselect("Content types", content_types, default=content_types)

# Apply filters
mask = (
    df["brand"].isin(sel_brands) &
    df["platform"].isin(sel_platforms) &
    df["post_type"].isin(sel_types)
)
filtered_df = df[mask].copy() if len(df) else df.copy()

if filtered_df.empty:
    st.session_state["results"] = results
    st.session_state["df"] = df
    st.session_state["filtered_df"] = filtered_df
    st.session_state["sel_brands"] = sel_brands
    st.session_state["sel_platforms"] = sel_platforms
    st.session_state["data_dir"] = data_dir
    st.warning("No posts match the current filters. Adjust filters in the sidebar.")
    st.stop()

# Store in session state for pages
st.session_state["results"] = results
st.session_state["df"] = df
st.session_state["filtered_df"] = filtered_df
st.session_state["sel_brands"] = sel_brands
st.session_state["sel_platforms"] = sel_platforms
st.session_state["data_dir"] = data_dir

# ── Autostrat Intelligence ───────────────────────────────────────────
from autostrat_loader import load_all_autostrat, has_autostrat_data

autostrat = load_all_autostrat()
st.session_state["autostrat"] = autostrat

# PDF import sidebar section
st.sidebar.markdown("---")
st.sidebar.subheader("Autostrat Intel")
if st.sidebar.button("Import PDFs"):
    from autostrat_parser import parse_all_pdfs
    import_results = parse_all_pdfs()
    ok = [r for r in import_results if not r["error"]]
    errors = [r for r in import_results if r["error"]]
    if ok:
        st.sidebar.success(f"Imported {len(ok)} report(s)")
        for r in ok:
            st.sidebar.caption(f"{r['report_type']}: {r['identifier']}")
        autostrat = load_all_autostrat()
        st.session_state["autostrat"] = autostrat
    if errors:
        for r in errors:
            st.sidebar.error(f"{r['pdf']}: {r['error']}")
    if not import_results:
        st.sidebar.info("No PDFs found in autostrat/pdfs/")

if has_autostrat_data(autostrat):
    from autostrat_loader import get_report_counts
    counts = get_report_counts(autostrat)
    total = sum(counts.values())
    st.sidebar.caption(f"{total} autostrat report(s) loaded")

# ── Home Page ─────────────────────────────────────────────────────────

logo_col, title_col = st.columns([1, 5])
with logo_col:
    if cfg.logo_path and os.path.isfile(cfg.logo_path):
        st.image(cfg.logo_path, width=140)
with title_col:
    st.title(cfg.home_title)
    st.caption(cfg.home_subtitle_template.format(n=len(cfg.brands))
               + f"  |  {len(df)} posts analyzed")

st.markdown("---")

st.markdown("---")
st.subheader("Navigate")
st.markdown(cfg.nav_table)

# Excel export
st.markdown("---")


def _generate_excel(results):
    from dashboard import generate_dashboard
    path = os.path.join(tempfile.gettempdir(), f"{cfg.client_id}_report.xlsx")
    generate_dashboard(results, path)
    with open(path, "rb") as f:
        return f.read()


col_a, col_b = st.columns([3, 1])
with col_b:
    xlsx_bytes = _generate_excel(results)
    st.download_button("Download Excel Report", xlsx_bytes,
                       file_name=cfg.excel_filename,
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
