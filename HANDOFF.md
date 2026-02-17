# Cuervo Social Intelligence Dashboard — Agent Handoff

## Project Overview

Competitive social media intelligence tool for **Jose Cuervo** tequila, built for **Poplife** agency. Multi-page Streamlit dashboard analyzing Instagram and TikTok performance across tequila brands.

```bash
python3 -m streamlit run app.py
# Opens at http://localhost:8501
```

See `CLAUDE.md` for full architecture documentation, file structure, and technical details.

---

## Recent Work Completed

| Commit | Description |
|--------|-------------|
| `857e12a` | Fix NaN crash and display bugs across dashboard pages |
| `0e2a534` | Consolidate 11 pages into 6 with tabbed navigation |
| `3eb457d` | Remove TikTok from Executive Summary ER chart (was dwarfing Instagram bars) |
| `8666a44` | Fix NameError: define cuervo_df and leader_df before first use |
| `25aaaac` | Enhance dashboard with format strategy, content pillars, engagement signals |
| `dda52b7` | Integrate autostrat qualitative intelligence into Cuervo Strategy page |
| `a0ce58e` | Add autostrat intelligence integration (Pages 8-11, now merged into Page 6) |
| `3beec8b` | Replace hard-to-read charts with bar charts + fix ER calculations |

**Page consolidation (11 → 6):**
- Pages 1+2 → `1_Brand_Intelligence.py` (Executive Overview + Detailed Comparison tabs)
- Pages 3+4 → `2_Content_&_Engagement.py` (Content Strategy + Engagement Analysis tabs)
- Page 5 → `3_Hashtag_&_Creator.py`
- Page 6 → `4_Data_Explorer.py`
- Page 7 → `5_Cuervo_Strategy.py`
- Pages 8+9+10+11 → `6_Autostrat_Intelligence.py` (Strategic Playbook + Conversation Deep Dive + Profile Intelligence + Audience Profiles tabs)

---

## Pending Task: Add 5 Competitor Brands

From the **Cuervo 2026 Social Brief**, 5 spirit competitors need to be added to the dashboard:

**Lunazul, Hornitos, Cazadores, Milagro, El Jimador**

None of these brands have Sprout Social CSV data yet. They need config-only additions so the dashboard recognizes them when data arrives.

### Files to Modify

#### 1. `config.py`
- **`BRAND_COLORS`** (line ~13): Add a color for each brand. Suggested colors that don't conflict:
  - Lunazul: `#5B9BD5` (medium blue)
  - Hornitos: `#E8A838` (amber gold)
  - Cazadores: `#8B4513` (saddle brown)
  - Milagro: `#50C878` (emerald green)
  - El Jimador: `#CD5C5C` (indian red)
- **`BRAND_ORDER`** (line ~24): Append the 5 brands after "818 Tequila"

#### 2. `templates.py`
- **`BRANDS`** list (line ~11): Append the 5 brands
- **`known_hashtags`** dict in `generate_hashtag_template()` (line ~202): Add branded hashtags for each

#### 3. `sprout_import.py`
- **`BRAND_MAP`** dict (line ~22): Add handle-to-name mappings. Known handles:
  - Lunazul: `@lunazultequila`
  - Hornitos: `@hornitostequila`
  - Cazadores: `@cazaborestequila` / `@tequilacazadores`
  - Milagro: `@milagrotequila`
  - El Jimador: `@eljimador`
- **`classify_visual_style()`** `brand_defaults` dict (line ~305): Add visual style defaults

#### 4. `sample_data.py`
- **`BRAND_PROFILES`** dict (after line ~198): Add full profile entry for each brand with:
  - `ig_followers`, `tt_followers`, `ig_posts_per_month`, `tt_posts_per_month`
  - `ig_base_er`, `tt_base_er`
  - `themes`, `theme_weights`, `visual_bias`, `tone_bias`
  - `collab_rate`, `avg_hashtags`, `caption_length_range`
  - `ig_post_type_weights`
- **`HASHTAG_POOLS`** dict (after line ~304): Add hashtag pools for each brand
- **`generate_sample_profiles()`** — `bios` dict (line ~513) and `handles` dict (line ~524): Add entries for each brand

### Brand Research Notes (for demo data profiles)
- **Lunazul**: Beam Suntory brand, affordable tier, ~25K IG followers, product-focused content
- **Hornitos**: Sauza family, "A Shot Worth Taking" positioning, ~80K IG followers
- **Cazadores**: Bacardi brand, "Hunt for the Good Stuff", ~15K IG followers
- **Milagro**: William Grant & Sons, modern/colorful branding, ~30K IG followers
- **El Jimador**: Brown-Forman brand, Mexico's #1 tequila, ~50K IG followers

---

## Cuervo 2026 Social Brief — Key Strategy Points

### Target Audience
- Gen Z (21-27), 50/50 male-female
- First legal-drinking-age tequila consumers
- Digital-native, meme-literate, value authenticity

### Competitive Landscape
- **Spirit Competitors**: Lunazul, Hornitos, Cazadores, Milagro, El Jimador (same price tier)
- **Aspirational Brands on Social**: Duolingo, Chipotle, E.L.F, Dunkin, Poppi (content strategy benchmarks)
- **Current Dashboard Brands** (aspirational tier): Patron, Don Julio, Casamigos, Espolon, Teremana, 1800 Tequila, 818 Tequila

### Content Pillars
| Pillar | Product Line | Content Focus |
|--------|-------------|---------------|
| Party Starter | Especial | Nightlife, pregame, party moments |
| Elevated Sips | Tradicional | Cocktail craft, mixology, elevated occasions |
| Mix It Up | RTD (Ready-to-Drink) | Convenience, on-the-go, casual moments |
| Culture & Community | Brand-level | Cultural relevance, heritage, community building |

### Format Strategy
- 60% Reels (short-form video)
- 25% Carousels (educational, recipe, listicle)
- 15% Static Image (product, lifestyle)

### Posting Cadence
- Instagram: 4-5x/week
- TikTok: 3-4x/week

### KPI Targets
- 3% engagement rate
- 15% follower growth (annual)
- 10K average views per Reel
- 50% Reel ratio in content mix

### Strategic Priorities
1. Cultural relevance — tap into trending moments, memes, Gen Z language
2. Meme/humor content — "brand-safe absurdism", relatable scenarios
3. Creator collaborations — micro-influencers (10K-100K), food/drink/lifestyle verticals
4. UGC amplification — #HaveACuervoDay, user-generated cocktail content
5. Heritage storytelling — "Since 1795" as authenticity anchor

---

## Known Issues

1. **TikTok data gap**: TikTok data not yet in Sprout Social exports — TikTok sections show zeros when using Sprout import mode
2. **Incomplete brand data**: Don Julio and 1800 Tequila have profile data but 0 posts in Jan 2026 Sprout exports
3. **Content classifier accuracy**: Keyword-based classifier in `sprout_import.py` is ~80-85% accurate — could be improved with ML/embeddings
4. **UX consideration**: Consider hiding TikTok sections entirely when no TikTok data is present (instead of showing zero values)
5. **Sprout data range**: Current CSVs cover Oct 1, 2025 - Jan 31, 2026

---

## Git Status

- **Branch**: `main`
- **Working tree**: Clean (nothing to commit)
- **Remote**: Up to date with `origin/main`
- **Last commit**: `857e12a` — Fix NaN crash and display bugs across dashboard pages

---

## Current 8 Brands in Dashboard

| Brand | IG Followers | Color | Notes |
|-------|-------------|-------|-------|
| Jose Cuervo | 112K | #F8C090 (peach) | Hero brand |
| Patron | 350K | #2ea3f2 (blue) | Ultra-premium |
| Don Julio | 459K | #7B6B63 (taupe) | 0 posts in Sprout |
| Casamigos | 310K | #D4956A (burnt peach) | Top engagement |
| Espolon | 66K | #A3C4D9 (sky blue) | Campari Group |
| Teremana | 785K | #C9A87E (tan) | The Rock's brand |
| 1800 Tequila | 49K | #6B8FA3 (steel blue) | 0 posts in Sprout |
| 818 Tequila | 1.19M | #B88BBF (purple) | Kendall Jenner |

---

## Poplife Social Media Playbook Q1 2026

Source: `Copy of EXT - Cuervo Playbook V1.pdf` (Poplife)

This is the comprehensive social strategy playbook from Poplife. It defines Cuervo's brand persona, content frameworks, platform strategy, and measurement approach for 2026. **These frameworks should guide dashboard development.**

### Brand Persona & Creative Platform

- **Creative Platform**: "Marg Mode" (#MargMode) — brings Cuervo's margarita legacy to life with creativity, culture, and energy
- **Brand Persona**: "The tequila that invented tequila" — 250+ years of heritage
- **TOV**: Friendly, dynamic, approachable yet elevated, heritage-fueled, "the IT person in the group"
- **What we are**: Rich heritage, party with a purpose, the connector, used in the first margarita
- **What we are NOT**: Trying too hard, AI-generated, shots-focused, bottom shelf, ad-like, text-heavy

### Content Pillars (Poplife Framework)

These **replace** the earlier Social Brief pillars (Party Starter/Elevated Sips/Mix It Up/Culture & Community).

| Pillar | Target % | Key Quality | Description |
|--------|----------|-------------|-------------|
| **La Tradición** | 25% | Educational / Product | Heritage, recipes, tequila education, craftsmanship |
| **Cuervo Live** | 15% | Experiential / Entertainment | Events, partnerships, live cultural moments |
| **Life, with a Lime** | 30% | Aspirational / Relatable | Lifestyle content, everyday moments, cocktails to culture |
| **Culture, Shaken** | 30% | Entertainment / Timely | Reactive, trend-driven, memes, cultural conversations |

### Content Mix (Entertain / Educate / Connect / Convince)

| Category | Target % | Current % (Sep-Nov 2025) | Action |
|----------|----------|--------------------------|--------|
| **Entertain** | 50% | 17% | Post MORE — reels with humor, memes, trend-driven |
| **Educate** | 30% | 20% | Post MORE — tequila deep dives, recipes, hosting tips |
| **Connect** | 10% | 29% | Post LESS — UGC, polls, interactive stories |
| **Convince** | 10% | 34% | Post LESS — product launches, sales, CTAs |

The current funnel is **inverted** — heavy on selling, light on earning attention. Target: Entertain → Educate → Connect → Convince.

### Content Engine (3 Sources)

| Source | Target % | Description |
|--------|----------|-------------|
| **Creators & Influencers** | 70% | Human-first, social-first, trend-led content for owned + paid |
| **Brand-Owned Content** | 15% | Studio shoots, post-production, carousels, stills |
| **Events & Partnerships** | 15% | Brand collabs, event coverage, recaps, giveaways |

- **Creators** (micro 10K-100K): Focus on content creation for Cuervo channels, flexibility within pillars
- **Influencers** (micro to macro 500K+): Post on their own channels, leverage personal authenticity
- Campaigns with 70%+ creator control deliver **3x higher engagement** (Traackr, 2025)

### Platform Strategy

| Platform | Role | Cadence | Format |
|----------|------|---------|--------|
| **Instagram** | Content Catalog | 8-10 assets/month, 2-3x/week | Video & carousel-first, human-first |
| **TikTok** | The Entertainer | 12-16 assets/month, 4-5x/week | Short-form video, reactive/trend-led |
| **Pinterest** | Inspiration Engine | 10-12 pins/month, 2-3x/week | Recipe/hosting inspiration |
| **Facebook** | Performance Powerhouse | 3 paid assets/month | Paid amplification of best IG content |
| **X / Threads** | Community Follower | Reactive | Listening, responding, cultural pulse |
| **YouTube** | Immersive Teacher | 4-5 assets/month | Long-form educational + Shorts |

### Competitive Insights (Tubular Labs, Jan 2024 - Nov 2025)

- Patron leads with 160 creator posts — 2x more than Casamigos (74)
- 64% of all competitor creator posts live on Instagram
- **818 Tequila**: 71% creator content on TikTok, highest ER at 2.8% despite lowest post volume (21)
- TikTok = less saturated for tequila brands = opportunity for Cuervo

### Partnership Audience Archetypes

| Archetype | Age | Skew | Interests |
|-----------|-----|------|-----------|
| **The Power Players** | 21-38 | Male | UFC, NFL, NBA, sports culture, watch parties |
| **The Culture Clique** | 21-34 | Female | Reality TV, pop culture, memes, fandoms |
| **The Festival Friends** | 21-35 | Mixed | Coachella, ACL, live music, festivals |

Strategy: Use **influencer ambassadors** within each archetype's niche rather than posting niche content on main Cuervo channel (avoids alienating other archetypes).

### Key Performance Benchmarks

- Dynamic (video) ER: **2.8%** vs Static (image): **2.2%**
- Dynamic posts: **-26% CPM**, **-34% CPE** vs Static
- Content under 30s is most efficient on paid
- Text overlays boost hook rate by **27%**
- Human-first video outperforms static by **77%**
- Proactive outbound comments (50-99 chars) → **151.6% higher engagement**
- 68% of TikTok users want brands to engage more via comments
- VFX creative: **78.32% ER** (+41% above Poplife US benchmark) — untapped potential

### Content Best Practices

- **Hook formula**: Grab attention in first 3 seconds → guide to action (CTA)
- **Product integration**: Should feel natural, not ad-like
- **Trend reactivity framework**: (1) Which pillar? (2) Authentic to brand? (3) Natural integration or ad?
- **Trend types**: Evergreen (long life), Culture (short, tied to pop culture moment), Sound (very short, specific audio)
- **Biggest pain point**: Acting on trends faster internally — need streamlined approval process

### Measurement Framework

| Stage | Role | Key Metrics |
|-------|------|-------------|
| **Awareness** | Shift brand perception | Impressions, Views, Engagements, EMV, CER, VTR |
| **Consideration** | Create desirability | Comments/Replies, Shares, Traffic, Sentiment, CTR |
| **Conversion** | Drive purchases | Traffic, Sign-ups, Sales, CPA, AOV |

---

## Dashboard Integration Recommendations

These are concrete ways to wire the Poplife Playbook frameworks into the existing dashboard code. All use existing data fields — no new data sources needed.

### Integration 1: Poplife Content Pillar Tracking

**What:** Map existing 13 `content_theme` values to Poplife's 4 pillars with target % overlay
**Where:** New mapping dict in `config.py`, chart on Page 5 (`5_Cuervo_Strategy.py`)
**How:**
```python
POPLIFE_PILLAR_MAP = {
    "La Tradición": ["Brand Heritage / Story", "Education (Tequila 101)", "Behind the Scenes"],
    "Cuervo Live": ["Event / Activation", "Music / Party", "Sports Tie-in"],
    "Life, with a Lime": ["Lifestyle/Aspirational", "Cocktail Recipe", "Product Showcase"],
    "Culture, Shaken": ["Meme / Humor", "Creator Collab / UGC", "Cultural Moment / Holiday", "User Repost", "Giveaway / Promo"],
}
POPLIFE_PILLAR_TARGETS = {"La Tradición": 25, "Cuervo Live": 15, "Life, with a Lime": 30, "Culture, Shaken": 30}
```
**Also:** Replace current Page 5 content pillars (Party Starter/Elevated Sips/Mix It Up/Culture & Community) with these Poplife pillars at `pages/5_Cuervo_Strategy.py` lines ~315-360.
**Data field:** `content_theme` (exists on every post)

### Integration 2: Content Mix Funnel (Entertain / Educate / Connect / Convince)

**What:** Classify posts into Poplife's 4 content mix categories; show current vs target
**Where:** New mapping dict + chart on Page 5
**How:**
```python
CONTENT_MIX_MAP = {
    "Entertain": ["Meme / Humor", "Music / Party", "Creator Collab / UGC"],
    "Educate": ["Education (Tequila 101)", "Behind the Scenes", "Cocktail Recipe", "Brand Heritage / Story"],
    "Connect": ["Lifestyle/Aspirational", "Cultural Moment / Holiday", "User Repost", "Sports Tie-in"],
    "Convince": ["Product Showcase", "Giveaway / Promo", "Event / Activation"],
}
CONTENT_MIX_TARGETS = {"Entertain": 50, "Educate": 30, "Connect": 10, "Convince": 10}
```
**Dashboard:** Current vs Target bar chart with color coding. Poplife flags inverted funnel as critical problem.
**Data field:** `content_theme` (same field, different grouping)

### Integration 3: Dynamic vs Static Performance

**What:** Split posts by Dynamic (Reel/Video) vs Static (Static Image/Carousel) and compare ER
**Where:** Page 2 (`2_Content_&_Engagement.py`) or Page 5
**How:** Filter on `post_type` — Dynamic = `["Reel", "Video"]`, Static = `["Static Image", "Carousel"]`
**Dashboard:** Side-by-side ER comparison with Poplife benchmark overlay (2.8% vs 2.2%)
**Data field:** `post_type` (exists on every post)

### Integration 4: Content Source Tracking (Creator vs Brand vs Events)

**What:** Split Cuervo posts by content source with target overlay (70/15/15)
**Where:** Page 5 (Cuervo Strategy)
**How:**
- Creator = `has_creator_collab == "Yes"`
- Events = `content_theme in ["Event / Activation", "Music / Party"]` AND `has_creator_collab == "No"`
- Brand-owned = everything else
**Dashboard:** Donut chart with actual vs target (70% Creator / 15% Brand / 15% Events)
**Data fields:** `has_creator_collab` + `content_theme`

### Integration 5: Platform Cadence Scorecard

**What:** Compare Cuervo's actual posting frequency against Poplife targets
**Where:** Page 5 (Cuervo Strategy)
**How:**
- IG target: 8-10 assets/month (2-3x/week)
- TikTok target: 12-16 assets/month (4-5x/week)
- Show actual vs target as KPI metrics with green/red delta
**Data field:** `frequency` analysis already computed in `analysis.py`

### Integration 6: TOV & Content Quality Signals

**What:** Track tone distribution against Poplife's TOV guidelines
**Where:** Page 2 (Content & Engagement) or Page 5
**How:** `caption_tone` field already classifies into 8 tone options. Poplife wants:
- MORE: Playful/Fun, Casual/Conversational, Humorous/Meme
- LESS: Premium/Luxury (save for product moments), Bold/Edgy
**Data field:** `caption_tone` (exists on every post)

### What CANNOT Be Tracked (data not in Sprout exports)

- Hook rate / first 3 seconds retention
- Watch time / average view duration
- Community management response rate
- Paid media metrics (CPM, CPE, CPA)
- Trend reactivity speed (would need trend origin timestamps)
- Influencer follower tier (creator_follower_count not consistently populated)
- Pinterest, Facebook, X/Threads, YouTube data (only IG + TikTok currently)

---

*Last updated: Feb 10, 2026*
*Project root: `/Users/loucesario/cuervo-intel`*
