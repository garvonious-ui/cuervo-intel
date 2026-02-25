"""
Cuervo Competitive Social Intelligence Dashboard
=================================================
Main entry point. Run with: streamlit run app.py
"""

import os
import sys
import tempfile
from datetime import datetime

import pandas as pd
import streamlit as st

# Ensure project root is importable
sys.path.insert(0, os.path.dirname(__file__))

from config import PAGE_CONFIG, CUSTOM_CSS, BRAND_ORDER, SOCIAL_BRIEF_TARGETS
from templates import BRANDS, CONTENT_THEMES, TONE_OPTIONS

st.set_page_config(**PAGE_CONFIG)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ── Data Loading ──────────────────────────────────────────────────────

SPROUT_INPUT_DIR = os.path.join(os.path.dirname(__file__), "data", "sprout")
SPROUT_OUTPUT_DIR = os.path.join(tempfile.gettempdir(), "cuervo_sprout_imported")


@st.cache_data(show_spinner="Running competitive analysis...")
def load_demo():
    from sample_data import generate_all_sample_data
    from analysis import run_full_analysis
    tmp = os.path.join(tempfile.gettempdir(), "cuervo_demo_streamlit")
    os.makedirs(tmp, exist_ok=True)
    generate_all_sample_data(tmp)
    return run_full_analysis(tmp), tmp


def _sprout_fingerprint(sprout_dir: str) -> str:
    """Return a hash of CSV filenames + sizes + code version so cache busts
    when files change OR analysis logic is updated."""
    import hashlib
    # Bump this version whenever sprout_import.py or analysis.py logic changes
    CODE_VERSION = "v17_merged_themes"
    entries = [CODE_VERSION]
    if os.path.isdir(sprout_dir):
        for f in sorted(os.listdir(sprout_dir)):
            if f.lower().endswith(".csv"):
                fp = os.path.join(sprout_dir, f)
                entries.append(f"{f}:{os.path.getsize(fp)}")
    return hashlib.md5("|".join(entries).encode()).hexdigest()


@st.cache_data(show_spinner="Importing Sprout Social data...")
def load_sprout(sprout_dir: str, fingerprint: str = ""):
    from sprout_import import import_sprout_directory, import_benchmark_csv
    from analysis import run_full_analysis
    os.makedirs(SPROUT_OUTPUT_DIR, exist_ok=True)

    # Load benchmark CSV if present (e.g. Benchmark_CSV_ig_*.csv)
    benchmark_data = {}
    if os.path.isdir(sprout_dir):
        for f in sorted(os.listdir(sprout_dir)):
            if f.lower().startswith("benchmark_csv") and f.lower().endswith(".csv"):
                benchmark_data = import_benchmark_csv(os.path.join(sprout_dir, f))
                break  # Only one benchmark file expected

    files, stats = import_sprout_directory(sprout_dir, SPROUT_OUTPUT_DIR)
    results = run_full_analysis(SPROUT_OUTPUT_DIR, benchmark=benchmark_data)
    return results, SPROUT_OUTPUT_DIR, stats


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
    # Combine related content themes for clearer analysis
    if "content_theme" in df.columns:
        _theme_map = {
            "Education (Tequila 101)": "Education & Recipes",
            "Cocktail Recipe": "Education & Recipes",
            "Event / Activation": "Events & Music",
            "Music / Party": "Events & Music",
        }
        df["content_theme"] = df["content_theme"].replace(_theme_map)
    return df


# ── Load Data ─────────────────────────────────────────────────────────

st.logo("logo.png")

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
    results, data_dir = load_demo()
elif data_mode == "Sprout Social Import":
    results, data_dir, sprout_stats = load_sprout(
        SPROUT_INPUT_DIR, fingerprint=_sprout_fingerprint(SPROUT_INPUT_DIR)
    )
    st.sidebar.success(
        f"Imported {sprout_stats['total_posts']} posts from "
        f"{sprout_stats['files_imported']} file(s)"
    )
    if sprout_stats["brands_found"]:
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

cuervo_only = st.sidebar.checkbox("Jose Cuervo only")
if cuervo_only:
    sel_brands = ["Jose Cuervo"]
else:
    sel_brands = st.sidebar.multiselect("Brands", BRAND_ORDER, default=BRAND_ORDER)

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
        st.sidebar.info("No PDFs found in data/autostrat/pdfs/")

if has_autostrat_data(autostrat):
    from autostrat_loader import get_report_counts
    counts = get_report_counts(autostrat)
    total = sum(counts.values())
    st.sidebar.caption(f"{total} autostrat report(s) loaded")

# ── Home Page ─────────────────────────────────────────────────────────

logo_col, title_col = st.columns([1, 5])
with logo_col:
    st.image("cuervo_logo.png", width=140)
with title_col:
    st.title("Cuervo — Social Media Intelligence")
    st.caption(f"Competitive analysis across {len(BRANDS)} tequila brands on Instagram & TikTok  "
               f"|  {len(df)} posts analyzed  |  Gen Z (21-24) strategy focus")

st.markdown("---")

st.markdown("---")
st.subheader("Navigate")
st.markdown("""
| Page | What you'll find |
|------|-----------------|
| **Cuervo Performance** | KPI scorecard vs Brief targets, content format & theme performance, self-audit intelligence |
| **Competitive Landscape** | 13-brand comparison, content gaps, "What to Steal" cards, competitor autostrat intel |
| **2026 Strategy & Brief** | Social Brief scorecard, Poplife content pillars & mix funnel, 30-day action plan |
| **Inspiration & Explorer** | Duolingo & Poppi reference profiles, audience comparison, full data explorer |
| **Hashtag & Search Intel** | Brand hashtag comparison (#JoseCuervo vs #Cazadores vs #Hornitos), search term intelligence (#MargaritaTime) |
""")

# Excel export
st.markdown("---")


def _generate_excel(results):
    from dashboard import generate_dashboard
    path = os.path.join(tempfile.gettempdir(), "cuervo_report.xlsx")
    generate_dashboard(results, path)
    with open(path, "rb") as f:
        return f.read()


col_a, col_b = st.columns([3, 1])
with col_b:
    xlsx_bytes = _generate_excel(results)
    st.download_button("Download Excel Report", xlsx_bytes,
                       file_name="cuervo_intelligence_report.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
