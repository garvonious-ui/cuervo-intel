# Poplife Social Intelligence Platform

## What This Is
Multi-tenant competitive social media intelligence dashboard for Poplife agency. Streamlit app analyzing Instagram & TikTok performance with Sprout Social data, autostrat.ai qualitative reports, and per-client strategy playbooks. Clients load via `?client=` URL parameter.

## Tech Stack
- Python 3.9+, Streamlit (multi-page app)
- Plotly for charts, Pandas for data, OpenPyXL for Excel export
- pdfplumber + python-pptx for autostrat PDF/PPTX parsing
- Deployed on Streamlit Community Cloud

## Active Clients
- `?client=cuervo` — Jose Cuervo (13 tequila competitors)
- `?client=devils_reserve` — Devils Reserve (5 competitors, growth-phase account)

## Critical Rules
- All pages call `cfg = get_client()` — NEVER import client-specific constants directly
- `config.py` contains ONLY shared constants — all client-specific config lives in `clients/{id}/`
- Page 1 and Page 3 use UNFILTERED data — sidebar filters do NOT apply
- Page 2 uses FILTERED data — sidebar brand/platform/type filters apply
- All autostrat report IDs are in @docs/schemas.md — never hardcode inline
- Always test with both `?client=cuervo` and `?client=devils_reserve` after changes
- Never break the deployed Streamlit Cloud instance on main branch

## Session Rules
- BEFORE starting work: read @docs/build-plan.md and @docs/changelog.md
- AFTER completing a feature or before /clear: update both files
- If session runs longer than 30 minutes, pause and offer to update changelog
- When I say "wrap up": update build-plan checkboxes, write changelog entry, summarize
- Use /clear between major features — context degrades after ~50k tokens

## Reference Docs
- Architecture + data flow: @docs/architecture.md
- ClientConfig fields + data specs: @docs/schemas.md
- Page behavior specs: @docs/page-specs.md
- Build plan: @docs/build-plan.md
- Session history: @docs/changelog.md
- Design system: @docs/design-system.md
- New client setup: @docs/onboarding-client.md
- Key decisions: @docs/decisions.md

## Commands
- `python3 -m streamlit run app.py --server.headless true` — start dev server (port 8501)
- No client param → internal client picker
- `?client=cuervo` → Cuervo dashboard
- `?client=devils_reserve` → Devils Reserve dashboard

## File Layout
```
app.py                    # Entry point — client routing, data loading, sidebar
client_context.py         # Client config loader + session state
config.py                 # SHARED constants only (Poplife palette, chart styling)
clients/_schema.py        # ClientConfig dataclass
clients/{id}/             # Per-client: client.py, brands.py, strategy.py, copy.py, assets/
pages/                    # 5 Streamlit pages (numbered for nav order)
analysis.py               # Core analysis engine
sprout_import.py          # Sprout CSV import + AI classifiers
autostrat_parser.py       # PDF/PPTX → JSON parser
autostrat_loader.py       # JSON loader + extraction helpers
autostrat_components.py   # Reusable UI for autostrat narrative content
data/{client_id}/         # Per-client sprout/ and autostrat/ directories
```

## Current Phase
Maintenance + Devils Reserve buildout
See @docs/build-plan.md for task checklist
