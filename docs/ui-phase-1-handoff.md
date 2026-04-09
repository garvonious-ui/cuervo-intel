# UI Phase 1 — Handoff to Next Session

**Status:** Chart template shipped. KPI card implementation pending. Visual direction locked: **Treatment C (dark hero + light cards)**.

**Session context to skip re-loading:** See `docs/changelog.md` Session 1 entry + the commit history `eb498bb..c8f08f1`. The session covered data refresh, Partner-to-amplified decision, sidebar cleanup, UI audit, chart template, and KPI prototypes.

---

## The direction

The UI/UX audit identified three prioritized wins:

1. **✅ Branded Plotly chart template** — shipped as `c8f08f1` (poplife template registered, charts use peach primary, warm gridlines, dark hover tooltips)
2. **⏳ Custom KPI cards — Treatment C** — this document
3. **⏳ Page hero component** — deferred, but will be built as part of Treatment C since the hero block is the hero component

The visual direction is **Treatment C — dark editorial hero block + light readable KPI cards**. It was picked over all-light (A) and all-dark (B) because:

- The dark hero gives Poplife's editorial brand DNA a proper entrance moment
- The light KPI cards keep data scannable (13+ numbers need high readability)
- The dark → light rhythm matches how Poplife's website transitions between section titles and content
- Safest to implement in Streamlit since the body stays light (doesn't conflict with tabs, expanders, charts, tables)

### Reference prototype

The final HTML prototype is at `~/Downloads/kpi_prototype_C_mixed.html`. **Open that file in a browser before starting implementation** — it's the pixel-level target. Every CSS value in the handoff below is extracted from it.

## Implementation plan

### New file: `ui_components.py` (~180 lines)

Location: project root, alongside `autostrat_components.py`. Functions to build:

**`render_page_hero(title, kicker, subtitle, stats, accent_color='#F8C090')`**

- `title` (str) — display headline, rendered uppercase, 800 weight, 4rem
- `kicker` (str) — small label above the headline (e.g., "Cuervo · Brand Performance"), uppercase, peach
- `subtitle` (str) — descriptive line below the headline
- `stats` (list[dict]) — 4 inline stats: `[{"value": "179", "label": "Cuervo posts"}, ...]`
- `accent_color` — peach by default, takes client primary color

Outputs: dark block (`#1A1A1A` bg), 16px border-radius, 48px padding, peach accent bar at top-left (120px × 3px), decorative radial-gradient corner glow bottom-right, stats divider line (rgba white 0.12), 44px bottom margin.

**`render_kpi_card(label, value, status=None, meta=None, hero=False)`**

- `label` (str) — uppercase micro-label above the value
- `value` (str) — the big number (formatted with commas already, e.g. "21,268")
- `status` (dict or None) — `{"direction": "up"/"down"/"neutral", "delta": "+16", "target_text": "vs 100 target"}` — renders as status pill
- `meta` (str or None) — alternative to status, renders as gray meta chip (e.g., "Target 10–14/mo" for no-target metrics)
- `hero` (bool) — if True, renders the larger hero variant with 4rem number and peach top border

Outputs: white card, `#E0D8D0` border, 12px border-radius, hover state (`#F8C090` border + 4px/16px peach shadow + -1px translateY).

**`render_section_label(text)`**

Uppercase label with peach accent line before + border after. 44px top margin, 18px bottom. Use this to delineate the 3-4 KPI groups.

**`render_status_pill(value, target, format='number')`**

Helper that takes raw numbers and returns the `status` dict for `render_kpi_card`. Handles:
- Positive delta → green (`#5CB85C` bg 0.12, `#3a8f3a` text), `▲` arrow
- Negative delta → red (`#D9534F` bg 0.12, `#a83e3a` text), `▼` arrow
- At target (delta == 0) → neutral gray
- Format variants: `'number'` (just +/- number), `'percent'` (add %), `'thousand'` (format as e.g. "+38K")

### CSS additions

Two files need the same CSS block appended to their `CUSTOM_CSS`:
- `clients/cuervo/client.py` (line 31, inside `CUSTOM_CSS = """..."""`)
- `clients/devils_reserve/client.py` (line 30, same)

Extract the CSS from `~/Downloads/kpi_prototype_C_mixed.html` — everything inside the `<style>` block from `.page-hero` down to the hover states (skip the `body`, `.container`, and `.proto-banner` rules — those are prototype-only).

**Scope the selectors carefully** — the current CUSTOM_CSS targets Streamlit-injected elements. The new components use plain classes (`.page-hero`, `.kpi-card`, `.kpi-grid`, `.status-pill`, `.section-label`) that render via `st.markdown(..., unsafe_allow_html=True)`. Those classes should NOT collide with Streamlit's own class names.

**Font loading** — the prototype uses Google Fonts `Barlow Condensed + Inter`. The current CUSTOM_CSS already imports Barlow Condensed but not Inter. Add the Inter import at the top of CUSTOM_CSS alongside the existing Barlow Condensed import, or use `system-ui` fallback in the Inter stack if you want to avoid a second Google Fonts request.

### Page 1 KPI scorecard rewrite

**File:** `pages/1_Brand_Performance.py`

**Current state** (lines 60–230 roughly):
- Tab structure: `tab_kpi, tab_content, tab_audit = st.tabs([...])`
- Inside `tab_kpi`: `st.subheader("Monthly KPI Scorecard")` + `st.caption(...)` + computes for all metrics (~50 lines of math that must be preserved) + renders 13 `st.metric` calls in 2 rows (5 + 4 + 4).

**Target state:**

```python
with tab_kpi:
    # ── PRESERVE ALL EXISTING MATH UNCHANGED ──
    # Everything from line ~75 to ~127 computing: eng, freq, targets,
    # n_months, avg_eng_per_post, avg_eng_per_reel, reel_ratio,
    # _likes_pm, _comments_pm, _saves_pm, _shares_pm, _reel_views,
    # _carousel_imp, _stories_pm, _story_views_pm, ig_followers

    # ── NEW: Page hero block ──
    render_page_hero(
        title="The Mirror",  # from cfg.narrative or hardcoded per page
        kicker=f"{cfg.hero_brand} · Brand Performance",
        subtitle=cfg.page_captions.get("performance", "..."),
        stats=[
            {"value": f"{len(hero_df):,}", "label": f"{cfg.hero_brand} posts"},
            {"value": f"{int(_n_months)} mo", "label": f"{_date_range_text}"},  # "Feb '25 – Apr '26"
            {"value": str(len(cfg.pillar_map)), "label": "Content pillars"},
            {"value": f"{avg_eng_per_post:,.0f}", "label": "Avg eng/post"},
        ],
    )

    # ── Section 1: Performance averages ──
    render_section_label("Performance averages")

    # Hero metric full-width
    render_kpi_card(
        label="Avg engagement per post",
        value=f"{avg_eng_per_post:,.0f}",
        status=render_status_pill(avg_eng_per_post, ENG_PER_POST_TARGET),
        hero=True,
    )

    # 3-col grid for supporting averages
    c1, c2, c3 = st.columns(3)
    with c1:
        render_kpi_card(
            label="Avg Eng/Reel",
            value=f"{avg_eng_per_reel:,.0f}",
            status=render_status_pill(avg_eng_per_reel, ENG_PER_POST_TARGET),
        )
    with c2:
        render_kpi_card(
            label="Reel Ratio (IG)",
            value=f"{reel_ratio:.0f}%",
            status=render_status_pill(reel_ratio, REEL_RATIO_TARGET, format='percent'),
        )
    with c3:
        render_kpi_card(
            label="IG Posts/Mo",
            value=f"{ig_ppm:.0f}",
            meta=f"Target {IG_PPM_TARGET[0]}–{IG_PPM_TARGET[1]}/mo",
        )

    # ── Section 2: Monthly volume ──
    render_section_label("Monthly volume")
    v1, v2, v3, v4 = st.columns(4)
    # Likes, Comments, Saves, Shares — all with status pills vs targets

    # ── Section 3: Reach & format ──
    render_section_label("Reach & format")
    r1, r2, r3, r4 = st.columns(4)
    # Reel Views, Carousel Imp, Stories, Story Views

    # ── Section 4: Audience ──
    render_section_label("Audience")
    render_kpi_card(
        label="IG Followers",
        value=f"{ig_followers:,}",
        meta="Instagram",
    )
```

**What to remove:** the existing `st.subheader("Monthly KPI Scorecard")` + caption + 13 `st.metric` calls.

**What to preserve:** all the computed values (the `avg_eng_per_post`, `_likes_pm`, etc. variables) exactly as they are. The rewrite is purely about rendering.

**What to add:** a computed `_date_range_text` variable near the top of `tab_kpi` that formats the date range for the hero stat (e.g., `f"{hero_df['post_date'].min().strftime('%b \'%y')} – {hero_df['post_date'].max().strftime('%b \'%y')}"`).

### Streamlit-specific gotchas to watch out for

1. **`unsafe_allow_html=True`** — all card HTML must be wrapped in `st.markdown(html, unsafe_allow_html=True)`. Make sure `html` is a complete standalone HTML string per card (not split across multiple `st.markdown` calls) or they'll render with Streamlit wrappers between them.

2. **Column layout interaction** — `st.columns(N)` creates N equal-width columns. The card HTML inside each column should be **full-width of the column** (`width: 100%`). Don't use CSS grid inside a Streamlit column — it'll behave unexpectedly.

3. **Reruns and state** — the scorecard values come from `st.session_state["df"]` which is computed fresh on each rerun. No caching logic changes needed; the rewrite is display-only.

4. **Edutain filter** — the hero_df is already filtered to `_mix_weight >= 1.0` on lines 44-46. Preserve that line unchanged. The Edutain posts are intentionally excluded from the scorecard.

5. **Streamlit columns and card hover** — hover effects on KPI cards work inside columns, but `transform: translateY(-1px)` can visually clip against column borders if the hover shadow extends outside. Either make the card-hover shadow smaller (4px max) or add slight padding to the column to give the shadow room.

### Smoke test checklist (must do both clients)

For each of **Cuervo (`?client=cuervo`)** and **Devils Reserve (`?client=devils_reserve`)**:

1. Navigate to Page 1 Brand Performance → KPI Dashboard tab
2. Verify page hero renders: dark block, peach kicker, big headline, 4 inline stats, no JS errors
3. Verify hero KPI card renders: Avg Eng/Post with correct number and status pill
4. Verify all 3 sections render: Performance averages / Monthly volume / Reach & format
5. Verify all 13 metrics show correct numbers (match pre-change state)
6. Verify status pills: green for above-target, red for below-target, neutral for IG Posts/Mo
7. Hover over a card — verify peach border + shadow + 1px lift animation
8. Check sidebar still clean on client URL, still shows dev controls on `?dev=1`
9. Check other 4 pages still load without errors (pages 2, 3, 4, 5)
10. Cuervo expected scorecard: Avg Eng/Post **116**, Likes/Month **802**, Comments/Month **56** (below target), Reel Views/Mo **21,268** (below target)

### Commit + deploy

Single commit, clear message:
```
Implement Treatment C KPI cards (dark hero + light cards)

- New ui_components.py with render_page_hero, render_kpi_card,
  render_section_label, render_status_pill helpers.
- CSS additions to Cuervo + DR client custom_css for the new
  component styles.
- Page 1 Brand Performance KPI Dashboard tab rewritten to use new
  components with 3-section grouping and hero metric treatment.
- Preserves all existing scorecard math unchanged.

Smoke-tested on both Cuervo and Devils Reserve. Pages 2-5 unaffected.
```

**Push gotcha reminder from last session:** if you push multiple commits in rapid succession, Streamlit Cloud can debounce the second rebuild and serve stale code. If the live dashboard doesn't reflect the changes after ~90 seconds, reboot the app manually from share.streamlit.io admin → ⋮ → Reboot app.

## Open questions for when implementation starts

- **Hero title per page** — "The Mirror" is Page 1's name from the page-specs doc. Should each page get its own short editorial title as the hero headline? (Probably yes — Page 2 = "The Window", Page 3 = "The Playbook", Page 4 = "The Toolbox", Page 5 = "The Landscape". Those are already in `docs/page-specs.md`.) Decision: start with Page 1 only ("The Mirror"). Other pages get the treatment in a follow-up.
- **Should the hero stats be dynamic or hardcoded?** Dynamic is correct long-term but adds ~15 min. For the first implementation, hardcode them per page, then refactor to dynamic if it works well.
- **Do we update `CHART_TEMPLATE` exports anywhere?** No — the chart template is done. This work is pure KPI scorecard + hero block.

## After Treatment C ships: next priorities

From the Phase 1 audit, still queued:
1. **Page hero component rolled out to pages 2-5** (uses the component already built, ~1 hr)
2. **Sidebar client summary card** (~45 min) — client name, date range, dataset stats
3. **Stronger custom CSS polish** — typographic hierarchy cleanup, card hover states on existing autostrat cards
4. **The Self-Audit Intelligence redesign** (the "kinda lame" one) — Phase 2 work, bigger scope
5. **The Conversation Intel redesign** (wall of expanders) — Phase 2 work, biggest scope

These are all for future sessions and should NOT be bundled into the Treatment C implementation.
