import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import io
import tempfile
from datetime import datetime

import pandas as pd
import streamlit as st

from config import BRAND_ORDER, CUSTOM_CSS

st.logo("logo.png")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
st.header("Data Explorer")

if "results" not in st.session_state:
    st.warning("Go to the home page first to load data.")
    st.stop()

results = st.session_state["results"]
df = st.session_state["filtered_df"].copy()

# ── Advanced filters ──────────────────────────────────────────────────

st.markdown("Use these filters to drill into the data. Global brand/platform filters from the sidebar still apply.")

fc1, fc2, fc3, fc4 = st.columns(4)

with fc1:
    er_min = float(df["engagement_rate"].min()) if len(df) and df["engagement_rate"].notna().any() else 0.0
    er_max = float(df["engagement_rate"].max()) if len(df) and df["engagement_rate"].notna().any() else 10.0
    er_range = st.slider("ER % range", er_min, max(er_max, er_min + 0.1),
                         (er_min, er_max), step=0.1, key="er_slider")

with fc2:
    likes_max = int(df["likes"].max()) if len(df) and df["likes"].notna().any() else 100
    likes_range = st.slider("Likes range", 0, max(likes_max, 1), (0, likes_max), key="likes_slider")

with fc3:
    themes_avail = sorted(df["content_theme"].dropna().unique().tolist())
    sel_themes = st.multiselect("Content theme", themes_avail, default=themes_avail, key="exp_themes")

with fc4:
    tones_avail = sorted(df["caption_tone"].dropna().unique().tolist())
    sel_tones = st.multiselect("Tone", tones_avail, default=tones_avail, key="exp_tones")

fc5, fc6, fc7, fc8 = st.columns(4)

with fc5:
    styles_avail = sorted(df["visual_style"].dropna().unique().tolist())
    sel_styles = st.multiselect("Visual style", styles_avail, default=styles_avail, key="exp_styles")

with fc6:
    ctas_avail = sorted(df["cta_type"].dropna().unique().tolist())
    sel_ctas = st.multiselect("CTA type", ctas_avail, default=ctas_avail, key="exp_ctas")

with fc7:
    collab_opt = st.selectbox("Creator collab", ["All", "Yes", "No"], key="exp_collab")

with fc8:
    paid_opt = st.selectbox("Paid partnership", ["All", "Yes", "No"], key="exp_paid")

# Apply advanced filters (use fillna to include rows with missing categorical values)
mask = (
    df["engagement_rate"].between(er_range[0], er_range[1]) &
    df["likes"].between(likes_range[0], likes_range[1]) &
    (df["content_theme"].isin(sel_themes) | df["content_theme"].isna()) &
    (df["caption_tone"].isin(sel_tones) | df["caption_tone"].isna()) &
    (df["visual_style"].isin(sel_styles) | df["visual_style"].isna()) &
    (df["cta_type"].isin(sel_ctas) | df["cta_type"].isna())
)

collab_col = df["has_creator_collab"].astype(str).str.lower()
paid_col = df["is_paid_partnership"].astype(str).str.lower()

if collab_opt == "Yes":
    mask = mask & (collab_col == "yes")
elif collab_opt == "No":
    mask = mask & (collab_col != "yes")

if paid_opt == "Yes":
    mask = mask & (paid_col == "yes")
elif paid_opt == "No":
    mask = mask & (paid_col != "yes")

filt = df[mask]

# ── Summary stats row ─────────────────────────────────────────────────

st.markdown("---")
m1, m2, m3, m4, m5 = st.columns(5)
with m1:
    st.metric("Matching Posts", f"{len(filt):,}")
with m2:
    st.metric("Avg ER", f"{filt['engagement_rate'].mean():.2f}%" if len(filt) else "N/A")
with m3:
    st.metric("Total Likes", f"{int(filt['likes'].sum()):,}" if len(filt) else "0")
with m4:
    st.metric("Brands", f"{filt['brand'].nunique()}")
with m5:
    st.metric("Platforms", f"{filt['platform'].nunique()}")

# ── Caption search ────────────────────────────────────────────────────

search = st.text_input("Search captions or hashtags", placeholder="e.g. margarita, #CuervoDay, recipe")
if search:
    search_lower = search.lower()
    filt = filt[
        filt["caption_text"].fillna("").str.lower().str.contains(search_lower, na=False) |
        filt["hashtags"].fillna("").str.lower().str.contains(search_lower, na=False)
    ]
    st.caption(f"{len(filt)} posts match '{search}'")

# ── Interactive data table ────────────────────────────────────────────

display_cols = [
    "brand", "platform", "post_date", "post_type", "engagement_rate",
    "likes", "comments", "shares", "views", "content_theme",
    "visual_style", "caption_tone", "cta_type", "has_creator_collab",
    "caption_word_count", "emoji_count_in_caption", "post_url",
]
show_df = filt[[c for c in display_cols if c in filt.columns]].copy()
show_df = show_df.sort_values("engagement_rate", ascending=False).reset_index(drop=True)
show_df.index = show_df.index + 1
show_df.index.name = "#"

if "engagement_rate" in show_df.columns:
    show_df["engagement_rate"] = show_df["engagement_rate"].round(2)

st.dataframe(
    show_df.style.apply(
        lambda row: ["background-color: #FDEBD6" if row.get("brand") == "Jose Cuervo" else "" for _ in row],
        axis=1,
    ),
    width="stretch",
    height=600,
)

# ── Quick insights ────────────────────────────────────────────────────

if len(filt) >= 5:
    with st.expander("Quick Insights on Filtered Data"):
        type_ers = filt.groupby("post_type")["engagement_rate"].mean().dropna()
        if len(type_ers):
            st.markdown(f"- **Best content type:** {type_ers.idxmax()} (avg ER {type_ers.max():.2f}%)")

        theme_ers = filt.groupby("content_theme")["engagement_rate"].mean().dropna()
        if len(theme_ers):
            st.markdown(f"- **Best theme:** {theme_ers.idxmax()} (avg ER {theme_ers.max():.2f}%)")

        collab_er = filt[filt["has_creator_collab"].str.lower() == "yes"]["engagement_rate"].mean()
        non_er = filt[filt["has_creator_collab"].str.lower() != "yes"]["engagement_rate"].mean()
        if pd.notna(collab_er) and pd.notna(non_er):
            lift = collab_er - non_er
            st.markdown(f"- **Creator collab lift:** {'+' if lift > 0 else ''}{lift:.2f}% ER")

        best_day = filt.copy()
        best_day["dow"] = pd.to_datetime(best_day["post_date"], errors="coerce").dt.day_name()
        day_er = best_day.groupby("dow")["engagement_rate"].mean()
        if len(day_er):
            st.markdown(f"- **Best posting day:** {day_er.idxmax()} (avg ER {day_er.max():.2f}%)")

# ── Export ─────────────────────────────────────────────────────────────

st.markdown("---")
ex1, ex2 = st.columns(2)

with ex1:
    csv_buf = io.BytesIO()
    filt.to_csv(csv_buf, index=False)
    st.download_button("Download filtered data (CSV)", csv_buf.getvalue(),
                       file_name="cuervo_filtered_data.csv", mime="text/csv")

with ex2:
    from dashboard import generate_dashboard
    xlsx_path = os.path.join(tempfile.gettempdir(), "cuervo_report_explorer.xlsx")
    generate_dashboard(results, xlsx_path)
    with open(xlsx_path, "rb") as f:
        st.download_button("Download Excel Report", f.read(),
                           file_name="cuervo_intelligence_report.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
