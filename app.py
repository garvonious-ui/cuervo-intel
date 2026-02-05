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

from config import PAGE_CONFIG, CUSTOM_CSS, BRAND_ORDER
from templates import BRANDS, CONTENT_THEMES, VISUAL_STYLES, TONE_OPTIONS

st.set_page_config(**PAGE_CONFIG)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ── Data Loading ──────────────────────────────────────────────────────

@st.cache_data(show_spinner="Running competitive analysis...")
def load_demo():
    from sample_data import generate_all_sample_data
    from analysis import run_full_analysis
    tmp = os.path.join(tempfile.gettempdir(), "cuervo_demo_streamlit")
    os.makedirs(tmp, exist_ok=True)
    generate_all_sample_data(tmp)
    return run_full_analysis(tmp), tmp


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
        df["engagement_rate"] = pd.to_numeric(df["engagement_rate"], errors="coerce").fillna(0.0)
    if "post_date" in df.columns:
        df["post_date"] = pd.to_datetime(df["post_date"], errors="coerce")
    if "post_hour" in df.columns:
        df["post_hour"] = pd.to_numeric(df["post_hour"], errors="coerce")
    return df


# ── Load Data ─────────────────────────────────────────────────────────

st.sidebar.title("\U0001F943 Cuervo Intel")

data_mode = st.sidebar.radio("Data source", ["Demo Data", "Custom CSV Folder"], index=0)

if data_mode == "Demo Data":
    results, data_dir = load_demo()
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

content_types = sorted(df["post_type"].dropna().unique().tolist())
sel_types = st.sidebar.multiselect("Content types", content_types, default=content_types)

# Apply filters
mask = (
    df["brand"].isin(sel_brands) &
    df["platform"].isin(sel_platforms) &
    df["post_type"].isin(sel_types)
)
filtered_df = df[mask].copy()

# Store in session state for pages
st.session_state["results"] = results
st.session_state["df"] = df
st.session_state["filtered_df"] = filtered_df
st.session_state["sel_brands"] = sel_brands
st.session_state["sel_platforms"] = sel_platforms
st.session_state["data_dir"] = data_dir

# ── Home Page ─────────────────────────────────────────────────────────

st.title("Jose Cuervo — Social Media Intelligence")
st.caption(f"Competitive analysis across {len(BRANDS)} tequila brands on Instagram & TikTok  "
           f"|  {len(df)} posts analyzed  |  Gen Z (21-24) strategy focus")

st.markdown("---")

# KPI row
c1, c2, c3, c4 = st.columns(4)

cuervo_posts = filtered_df[filtered_df["brand"] == "Jose Cuervo"]
all_ers = filtered_df.groupby("brand")["engagement_rate"].mean()
cuervo_er = all_ers.get("Jose Cuervo", 0)
cat_avg_er = all_ers.mean() if len(all_ers) else 0
best_brand = all_ers.idxmax() if len(all_ers) else "N/A"
best_er = all_ers.max() if len(all_ers) else 0

with c1:
    st.metric("Posts Analyzed", f"{len(filtered_df):,}")
with c2:
    st.metric("Cuervo Avg ER", f"{cuervo_er:.2f}%",
              delta=f"{cuervo_er - cat_avg_er:+.2f}% vs avg")
with c3:
    st.metric("Category Avg ER", f"{cat_avg_er:.2f}%")
with c4:
    st.metric("Top Brand (ER)", f"{best_brand}", delta=f"{best_er:.2f}%")

st.markdown("---")
st.subheader("Navigate")
st.markdown("""
| Page | What you'll find |
|------|-----------------|
| **Executive Summary** | KPIs, engagement comparison, priority recommendations, radar chart |
| **Brand Comparison** | Side-by-side metrics table, content mix, followers-vs-ER scatter |
| **Content Strategy** | Theme heatmap, caption analysis, CTA effectiveness, visual styles |
| **Engagement Deep Dive** | ER by content type, posting schedule heatmap, top posts, distributions |
| **Hashtag & Creator** | Hashtag strategy, creator collab rates, collab engagement lift |
| **Data Explorer** | Filter, sort, and query every post — download CSV or Excel |
| **Cuervo Strategy** | Gen Z recommendations, content gaps, 30-day action plan |
""")

# Excel export
st.markdown("---")
col_a, col_b = st.columns([3, 1])
with col_b:
    if st.button("Download Excel Report"):
        from dashboard import generate_dashboard
        path = os.path.join(tempfile.gettempdir(),
                            f"cuervo_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
        generate_dashboard(results, path)
        with open(path, "rb") as f:
            st.download_button("Save .xlsx", f, file_name="cuervo_intelligence_report.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
