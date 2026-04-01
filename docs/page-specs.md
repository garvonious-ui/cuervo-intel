# Page Specifications

## Page 1: Brand Performance ("The Mirror")
**Data**: UNFILTERED — sidebar filters do NOT apply. Hero brand-only view.

- **Tab 1: KPI Dashboard** — KPI scorecard vs targets, cadence scorecard, engagement signals
- **Tab 2: Content Performance** — Format breakdown, theme performance, best & worst posts, monthly engagement trend
- **Tab 3: Self-Audit Intelligence** — Hero brand autostrat reports (loaded via `cfg.hero_hashtag_ids`)

## Page 2: Competitive Landscape ("The Window")
**Data**: FILTERED — sidebar brand/platform/type filters apply.

- **Tab 1: Competitive Overview** — Side-by-side comparison, Eng/1K Followers chart
- **Tab 2: Content Gaps** — Theme gap analysis, format strategy, "What to Steal" cards

## Page 3: Strategy & Brief ("The Playbook")
**Data**: UNFILTERED — sidebar filters do NOT apply.

- **Tab 1: Scorecard** — KPI table, content source mix, content production needs
- **Tab 2: Content Strategy Frameworks** — Pillars, content mix funnel, Gen Z drivers
- **Tab 3: Action Plan** — 30-day plan, threats & opportunities, recommendations

## Page 4: Inspiration & Explorer ("The Toolbox")
- **Tab 1: Inspiration** — Reference brand profiles, "What {hero} Can Steal", audience comparison
- **Tab 2: Data Explorer** — Advanced filters, caption search, full data table, CSV/Excel export

## Page 5: Conversation Intel ("The Landscape")
**Data**: Autostrat reports only — sidebar filters do NOT apply.

- **Tab 1: Brand Hashtags** — Per-brand reports, "What This Means for {hero}" takeaway
- **Tab 2: Category & Cultural** — Category conversation reports, bridge narrative
- **Tab 3: Google Search News** — News analysis, SWOT, sentiment, action items

## Filter Behavior Summary
| Page | Sidebar Filters | Data Source |
|------|----------------|-------------|
| 1 - Brand Performance | IGNORED | Unfiltered hero brand data |
| 2 - Competitive Landscape | APPLIED | Filtered multi-brand data |
| 3 - Strategy & Brief | IGNORED | Unfiltered data + strategy config |
| 4 - Inspiration & Explorer | Tab-dependent | Reference brands + full data |
| 5 - Conversation Intel | IGNORED | Autostrat reports only |
