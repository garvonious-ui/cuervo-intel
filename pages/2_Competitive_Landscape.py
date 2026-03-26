"""
Page 2: Competitive Landscape — "The Window"
What competitors are doing. All 13 brands, sidebar filters apply.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from config import CHART_TEMPLATE, CHART_FONT, COLLAB_AMPLIFIED_TYPES
from client_context import get_client

if "results" not in st.session_state:
    st.warning("Go to the home page first to load data.")
    st.stop()

cfg = get_client()

st.logo(cfg.app_logo_path)
st.markdown(cfg.custom_css, unsafe_allow_html=True)
st.header(cfg.page_headers.get("competitive", "Competitive Landscape"))
st.caption(cfg.page_captions.get("competitive", "What competitors are doing — sidebar filters apply here."))

results = st.session_state["results"]
df = st.session_state["filtered_df"]
full_df = st.session_state["df"]
sel_brands = st.session_state["sel_brands"]
order = [b for b in cfg.brand_order if b in sel_brands]

HERO = cfg.hero_brand
ENG_PER_POST_TARGET = cfg.kpi_targets["engagements_per_post"]
ENG_PER_1K_TARGET = cfg.kpi_targets["eng_per_1k_followers"]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
tab_overview, tab_gaps = st.tabs([
    "Competitive Overview", "Format & Frequency",
])

# ══════════════════════════════════════════════════════════════════════
# TAB 1 — Competitive Overview
# ══════════════════════════════════════════════════════════════════════

with tab_overview:

    # ── Comparison Table ───────────────────────────────────────────────
    st.subheader("Side-by-Side Metrics")
    st.caption("Includes all post types (owned + collab/influencer) for apples-to-apples competitive comparison.")

    benchmark = results.get("benchmark", {})
    has_bench = bool(benchmark)

    rows = []
    for brand in order:
        plat_df = df[df["brand"] == brand]
        eng = results["engagement"].get(brand, {})
        freq_b = results["frequency"].get(brand, {})
        followers = sum(eng.get(p, {}).get("followers", 0) for p in ["Instagram", "TikTok"])
        avg_eng = plat_df["total_engagement"].mean() if len(plat_df) else 0
        avg_eng = 0 if pd.isna(avg_eng) else avg_eng
        ppw = sum(freq_b.get(p, {}).get("posts_per_week", 0) for p in ["Instagram", "TikTok"])
        _likes = plat_df["likes"].mean() if len(plat_df) else 0
        _likes = 0 if pd.isna(_likes) else _likes

        # Engagement per 1K followers (avg across platforms)
        epk_vals = [eng.get(p, {}).get("engagement_per_1k_followers", 0) for p in ["Instagram", "TikTok"]]
        epk_vals = [v for v in epk_vals if v > 0]
        eng_per_1k = sum(epk_vals) / len(epk_vals) if epk_vals else 0

        row_data = {
            "Brand": brand,
            "Followers": followers,
            "Posts": len(plat_df),
            "Posts/Week": round(ppw, 1),
            "Avg Eng": int(avg_eng),
            "Eng/1K Fol": round(eng_per_1k, 2),
            "Avg Likes": int(_likes),
        }

        if has_bench:
            ig_eng = eng.get("Instagram", {})
            bench_posts = ig_eng.get("benchmark_posts", 0)
            if bench_posts:
                row_data["Posts"] = bench_posts
                row_data["Posts/Week"] = round(bench_posts / 4, 1)
            bench_avg_eng = ig_eng.get("benchmark_avg_engagement", 0)
            if bench_avg_eng:
                row_data["Avg Eng"] = int(bench_avg_eng)
            row_data["Avg #tags"] = round(ig_eng.get("benchmark_avg_hashtags", 0), 1)

        rows.append(row_data)

    comp_tbl = pd.DataFrame(rows)

    def highlight_hero(row):
        return ["background-color: #FDEBD6" if row["Brand"] == HERO else "" for _ in row]

    def color_epk(val):
        if isinstance(val, (int, float)):
            if val >= ENG_PER_1K_TARGET * 1.5:
                return "background-color: #C8E6C9"
            elif val >= ENG_PER_1K_TARGET * 0.85:
                return "background-color: #FDEBD6"
            elif val > 0:
                return "background-color: #FFCDD2"
        return ""

    fmt = {"Followers": "{:,.0f}", "Avg Eng": "{:,.0f}", "Avg Likes": "{:,.0f}",
           "Eng/1K Fol": "{:.2f}", "Posts/Week": "{:.1f}"}
    if has_bench:
        fmt["Avg #tags"] = "{:.1f}"

    styled_tbl = (
        comp_tbl.style
        .apply(highlight_hero, axis=1)
        .map(color_epk, subset=["Eng/1K Fol"])
        .format(fmt)
    )
    st.dataframe(styled_tbl, use_container_width=True, hide_index=True, height=320)

    # ── Micro-brand footnote on Eng/1K ────────────────────────────────
    _micro_brands = comp_tbl[comp_tbl["Followers"] < 10_000]
    if not _micro_brands.empty:
        _names = ", ".join(_micro_brands["Brand"].tolist())
        st.caption(
            f"**Note on Eng/1K Followers:** {_names} ha{'s' if len(_micro_brands) == 1 else 've'} "
            f"fewer than 10K followers. Micro-brands naturally produce higher per-follower "
            f"engagement rates because small, engaged communities interact at a higher ratio "
            f"than large audiences. This metric is mathematically valid but not a direct "
            f"apples-to-apples comparison against brands with 100K+ followers."
        )

    st.markdown("---")

    # ── "Who's Winning & Why" ──────────────────────────────────────────
    st.subheader("Who's Winning & Why")

    _df_owned = df[~df["collaboration"].str.strip().str.lower().isin(COLLAB_AMPLIFIED_TYPES)] if "collaboration" in df.columns else df
    brand_engs = _df_owned.groupby("brand")["total_engagement"].mean().dropna()
    brand_engs = brand_engs[brand_engs > 0].sort_values(ascending=False)
    top3 = brand_engs.head(3)

    for rank, (brand, avg_e) in enumerate(top3.items(), 1):
        brand_df = _df_owned[_df_owned["brand"] == brand]
        top_theme = brand_df.groupby("content_theme")["total_engagement"].mean()
        best_theme = top_theme.idxmax() if len(top_theme) else "N/A"
        reel_pct = len(brand_df[brand_df["post_type"] == "Reel"]) / max(len(brand_df), 1) * 100

        st.markdown(
            f"**#{rank} {brand}** — {avg_e:,.0f} avg engagements | "
            f"Top theme: {best_theme} | Reel mix: {reel_pct:.0f}%"
        )

    hero_avg_eng = brand_engs.get(HERO, 0)
    hero_rank = list(brand_engs.index).index(HERO) + 1 if HERO in brand_engs.index else len(brand_engs)
    st.info(f"**{HERO} ranks #{hero_rank}** out of {len(brand_engs)} brands at {hero_avg_eng:,.0f} avg engagements. "
            f"The top brand leads by {top3.iloc[0] - hero_avg_eng:,.0f}." if len(top3) and hero_avg_eng < top3.iloc[0] else
            f"**{HERO} leads** at {hero_avg_eng:,.0f} avg engagements.")

    st.markdown("---")

    # ── Engagement per 1K Followers Chart ──────────────────────────────
    st.subheader("Engagements per 1K Followers by Brand")

    epk_rows = []
    for brand in sel_brands:
        eng_b = results["engagement"].get(brand, {})
        epk_vals = [eng_b.get(p, {}).get("engagement_per_1k_followers", 0) for p in ["Instagram", "TikTok"]]
        epk_vals = [v for v in epk_vals if v > 0]
        avg_epk = sum(epk_vals) / len(epk_vals) if epk_vals else 0
        epk_rows.append({"brand": brand, "eng_per_1k": avg_epk})

    epk_data = pd.DataFrame(epk_rows)

    fig_epk = px.bar(epk_data, x="brand", y="eng_per_1k",
                     color="brand", color_discrete_map=cfg.brand_colors,
                     category_orders={"brand": order},
                     labels={"eng_per_1k": "Eng / 1K Followers", "brand": ""},
                     template=CHART_TEMPLATE)
    fig_epk.update_layout(font=CHART_FONT, height=420, showlegend=False)
    fig_epk.add_hline(y=ENG_PER_1K_TARGET, line_dash="dash", line_color="#D9534F",
                      annotation_text=f"{ENG_PER_1K_TARGET} eng/1K target",
                      annotation_position="top right")
    cat_avg_epk = epk_data[epk_data["eng_per_1k"] > 0]["eng_per_1k"].mean()
    fig_epk.add_hline(y=cat_avg_epk, line_dash="dot", line_color="gray",
                      annotation_text=f"Category avg {cat_avg_epk:.2f}",
                      annotation_position="bottom right")
    st.plotly_chart(fig_epk, use_container_width=True)

    if not _micro_brands.empty:
        st.caption(
            f"**Note:** {_names}'s high Eng/1K rate reflects the engagement efficiency "
            f"typical of micro-brands (<10K followers), not necessarily higher raw engagement. "
            f"See the table above for absolute engagement numbers."
        )

    st.markdown("---")

    # ── Top 10 Posts per Brand/Platform ──────────────────────────────
    st.subheader("Top 10 Posts by Brand")
    st.caption("Best-performing content per brand — study what's working")

    top10_brand = st.selectbox("Select brand", order, key="top10_brand_sel")
    top10_plat = st.radio("Platform", ["Instagram", "TikTok"], horizontal=True, key="top10_plat_sel")

    top10_data = results["engagement"].get(top10_brand, {}).get(top10_plat, {}).get("top_10_posts", [])

    if top10_data:
        top10_rows = []
        # For the hero brand, look up manual columns from the main df
        _hero_lookup = {}
        _is_hero = top10_brand == HERO
        _has_pillars = _is_hero and "content_pillar" in df.columns
        if _is_hero:
            for _, row in df[df["brand"] == HERO].iterrows():
                url = row.get("post_url", "")
                if url:
                    _hero_lookup[url] = {
                        "pillar": row.get("content_pillar", "") if pd.notna(row.get("content_pillar")) else "",
                        "collab": row.get("collaboration", "") if pd.notna(row.get("collaboration")) else "",
                        "funnel": row.get("content_mix_funnel", "") if pd.notna(row.get("content_mix_funnel")) else "",
                    }

        for i, p in enumerate(top10_data, 1):
            post_url = p.get("url", p.get("post_url", ""))
            hero_data = _hero_lookup.get(post_url, {})

            row_data = {
                "#": i,
                "Post": post_url if post_url else "",
                "Engagements": p.get("total_engagement", 0),
                "Likes": p.get("likes", 0),
                "Comments": p.get("comments", 0),
                "Type": p.get("type", ""),
            }

            if _is_hero and _has_pillars:
                row_data["Pillar"] = hero_data.get("pillar", p.get("theme", ""))
                row_data["Collab"] = hero_data.get("collab", "")
                row_data["Funnel"] = hero_data.get("funnel", "")
            else:
                row_data["Theme"] = p.get("theme", "")

            row_data["Date"] = p.get("date", "")
            top10_rows.append(row_data)
        top10_df = pd.DataFrame(top10_rows)

        def color_top10_eng(val):
            if isinstance(val, (int, float)):
                if val >= 500:
                    return "background-color: #C8E6C9"
                elif val >= 200:
                    return "background-color: #FDEBD6"
                elif val > 0:
                    return "background-color: #FFCDD2"
            return ""

        styled_top10 = top10_df.style.map(color_top10_eng, subset=["Engagements"]).format({
            "Engagements": "{:,.0f}", "Likes": "{:,.0f}", "Comments": "{:,.0f}"
        })
        st.dataframe(
            styled_top10,
            use_container_width=True,
            hide_index=True,
            height=400,
            column_config={
                "Post": st.column_config.LinkColumn("Post", display_text="View Post"),
            },
        )

        # So What
        best_type = pd.DataFrame(top10_rows).groupby("Type")["Engagements"].mean()
        best_type_name = best_type.idxmax() if len(best_type) else "N/A"
        avg_top10_eng = sum(r["Engagements"] for r in top10_rows) / len(top10_rows)
        st.info(f"**{top10_brand}'s top 10** average {avg_top10_eng:,.0f} engagements on {top10_plat}. "
                f"Best-performing format: **{best_type_name}**. "
                f"{'Study their approach for ' + HERO + ' adaptation.' if top10_brand != HERO else 'Keep doubling down on what works.'}")
    else:
        st.info(f"No {top10_plat} post data available for {top10_brand}.")

    # ── Dynamic vs Static Performance ──────────────────────────────────
    st.divider()
    st.subheader("Dynamic vs Static Performance")
    st.caption("Comparing avg engagements: Dynamic (video) vs Static (image) content")

    dynamic_types = ["Reel", "Video"]
    static_types = ["Static Image", "Carousel"]

    # Category-wide metrics (all brands in competitive set)
    _all_dyn = df[df["post_type"].isin(dynamic_types)]
    _all_stat = df[df["post_type"].isin(static_types)]
    _all_total = len(_all_dyn) + len(_all_stat) or 1
    dyn_pct = len(_all_dyn) / _all_total * 100
    stat_pct = len(_all_stat) / _all_total * 100
    dyn_eng = _all_dyn["total_engagement"].mean() if len(_all_dyn) else 0
    stat_eng = _all_stat["total_engagement"].mean() if len(_all_stat) else 0
    dyn_eng = 0 if pd.isna(dyn_eng) else dyn_eng
    stat_eng = 0 if pd.isna(stat_eng) else stat_eng

    ds1, ds2, ds3, ds4 = st.columns(4)
    with ds1:
        st.metric("Dynamic %", f"{dyn_pct:.0f}%", help="Reels + Video — category average across all brands")
    with ds2:
        st.metric("Dynamic Avg Eng", f"{dyn_eng:,.0f}",
                  delta=f"{dyn_eng - stat_eng:+,.0f} vs Static" if stat_eng > 0 else None)
    with ds3:
        st.metric("Static %", f"{stat_pct:.0f}%", help="Static Image + Carousel — category average across all brands")
    with ds4:
        st.metric("Static Avg Eng", f"{stat_eng:,.0f}")

    # Cross-brand comparison
    all_brand_ds = []
    for brand in order:
        bdf = df[df["brand"] == brand]
        if "collaboration" in bdf.columns:
            bdf = bdf[~bdf["collaboration"].str.strip().str.lower().isin(COLLAB_AMPLIFIED_TYPES)]
        if len(bdf) == 0:
            continue
        b_dyn = bdf[bdf["post_type"].isin(dynamic_types)]
        b_stat = bdf[bdf["post_type"].isin(static_types)]
        b_dyn_eng = b_dyn["total_engagement"].mean() if len(b_dyn) else 0
        b_stat_eng = b_stat["total_engagement"].mean() if len(b_stat) else 0
        b_dyn_eng = 0 if pd.isna(b_dyn_eng) else b_dyn_eng
        b_stat_eng = 0 if pd.isna(b_stat_eng) else b_stat_eng
        all_brand_ds.append({"Brand": brand, "Dynamic Eng": round(b_dyn_eng, 0), "Static Eng": round(b_stat_eng, 0)})

    if all_brand_ds:
        ds_df = pd.DataFrame(all_brand_ds)
        ds_melt = pd.melt(ds_df, id_vars=["Brand"], value_vars=["Dynamic Eng", "Static Eng"],
                          var_name="Format", value_name="Avg Eng")
        fig_ds = px.bar(ds_melt, x="Brand", y="Avg Eng", color="Format", barmode="group",
                        color_discrete_map={"Dynamic Eng": "#2ea3f2", "Static Eng": "#C9A87E"},
                        labels={"Avg Eng": "Avg Engagements", "Brand": ""},
                        template=CHART_TEMPLATE, text_auto=",.0f")
        fig_ds.update_layout(font=CHART_FONT, height=380, legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(fig_ds, use_container_width=True)

    st.info(f"**Dynamic content {'outperforms' if dyn_eng > stat_eng else 'underperforms vs'} static** by "
            f"{abs(dyn_eng - stat_eng):,.0f} avg engagements. {HERO}'s dynamic mix is {dyn_pct:.0f}% — "
            f"{'meeting' if dyn_pct >= 50 else 'below'} the 50%+ target.")


# ══════════════════════════════════════════════════════════════════════
# TAB 2 — Content Gaps
# ══════════════════════════════════════════════════════════════════════

with tab_gaps:

    # ── Format Strategy Comparison ─────────────────────────────────────
    st.subheader("Format Strategy Comparison")

    type_data = df[df["brand"].isin(sel_brands)].groupby(["brand", "post_type"]).size().reset_index(name="count")
    totals = type_data.groupby("brand")["count"].transform("sum")
    type_data["pct"] = (type_data["count"] / totals * 100).round(1)

    fig_ct = px.bar(type_data, x="brand", y="pct", color="post_type",
                    barmode="stack", category_orders={"brand": order},
                    labels={"pct": "% of Posts", "brand": "", "post_type": "Type"},
                    template=CHART_TEMPLATE, color_discrete_sequence=px.colors.qualitative.Set2)
    fig_ct.update_layout(font=CHART_FONT, height=400, legend=dict(orientation="h", y=1.12))
    st.plotly_chart(fig_ct, use_container_width=True)

    st.markdown("---")

    # ── Avg Engagements by Format (Cross-Brand) ─────────────────────
    st.subheader("Avg Engagements by Format — Cross-Brand")
    st.caption("Which content formats drive the most engagement for each brand")

    eng_by_fmt_rows = []
    for brand in order:
        for plat in ["Instagram", "TikTok"]:
            eng_by_type = results["engagement"].get(brand, {}).get(plat, {}).get("engagement_by_type", {})
            for fmt, eng_val in eng_by_type.items():
                eng_by_fmt_rows.append({"Brand": brand, "Format": fmt, "Avg Eng": round(eng_val, 0)})

    if eng_by_fmt_rows:
        eng_fmt_df = pd.DataFrame(eng_by_fmt_rows)
        eng_fmt_agg = eng_fmt_df.groupby(["Brand", "Format"])["Avg Eng"].mean().reset_index()

        fig_eng_fmt = px.bar(eng_fmt_agg, x="Brand", y="Avg Eng", color="Format",
                             barmode="group",
                             category_orders={"Brand": order},
                             labels={"Avg Eng": "Avg Engagements", "Brand": ""},
                             template=CHART_TEMPLATE,
                             color_discrete_sequence=["#F8C090", "#2ea3f2", "#7B6B63", "#D4956A", "#C9A87E"])
        fig_eng_fmt.add_hline(y=ENG_PER_POST_TARGET, line_dash="dash", line_color="#D9534F",
                              annotation_text=f"{ENG_PER_POST_TARGET} eng/post target", annotation_position="top right")
        fig_eng_fmt.update_layout(font=CHART_FONT, height=420,
                                  legend=dict(orientation="h", y=1.12))
        st.plotly_chart(fig_eng_fmt, use_container_width=True)

        # So What
        best_fmt_overall = eng_fmt_agg.groupby("Format")["Avg Eng"].mean().sort_values(ascending=False)
        if len(best_fmt_overall):
            top_fmt = best_fmt_overall.index[0]
            top_fmt_eng = best_fmt_overall.iloc[0]
            st.info(f"**{top_fmt}** drives the highest avg engagement across brands at {top_fmt_eng:,.0f}. "
                    f"Ensure {HERO}'s content mix prioritizes this format.")
    else:
        st.info("No engagement-by-format data available.")

    st.markdown("---")

    # ── Posting Frequency Comparison ───────────────────────────────────
    st.subheader("Posting Frequency (posts/week)")

    freq = results["frequency"]
    freq_rows = []
    for brand in sel_brands:
        for plat in ["Instagram", "TikTok"]:
            ppw = freq.get(brand, {}).get(plat, {}).get("posts_per_week", 0)
            freq_rows.append({"brand": brand, "platform": plat, "posts_per_week": ppw})
    freq_df = pd.DataFrame(freq_rows)

    fig_freq = px.bar(freq_df, x="brand", y="posts_per_week", color="platform",
                      barmode="group", color_discrete_map={"Instagram": "#D4956A", "TikTok": "#2ea3f2"},
                      category_orders={"brand": order},
                      labels={"posts_per_week": "Posts / Week", "brand": ""},
                      template=CHART_TEMPLATE)
    fig_freq.update_layout(font=CHART_FONT, height=380, legend=dict(orientation="h", y=1.12))
    st.plotly_chart(fig_freq, use_container_width=True)

    st.markdown("---")
