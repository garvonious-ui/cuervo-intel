# Design System

## Poplife Palette (Shared — config.py)
- Peach: `#F8C090` — primary accent
- Blue: `#2ea3f2` — secondary accent
- Background: `#F3EDE6` — warm off-white
- Dark: `#333333` — text
- White: `#ffffff`

## Priority Colors
- High: `#D9534F` (red)
- Medium: `#F8C090` (peach)
- Low: `#8CBF8C` (green)

## Chart Styling
- Template: `plotly_white`
- Font: `Barlow Condensed, Helvetica, Arial, sans-serif`
- All charts use `CHART_TEMPLATE` and `CHART_FONT` from `config.py`

## NOPD Framework Colors (Autostrat)
- Needs: `#2ea3f2` (blue)
- Objections: `#D9534F` (red)
- Desires: `#5CB85C` (green)
- Pain Points: `#F8C090` (peach)

## Per-Client Theming
Each client's `client.py` can override:
- `primary_color`, `background_color`, `dark_color`, `accent_color`
- `custom_css` — injected via `st.markdown(unsafe_allow_html=True)`
- `logo_path`, `favicon_path`, `app_logo_path`

Cuervo uses gold/dark theme. Devils Reserve uses Poplife defaults (pending custom assets).

## UI Patterns
- `st.logo(cfg.logo_path)` on every page
- `st.markdown(cfg.custom_css, unsafe_allow_html=True)` on every page
- Tabs for page sections: `st.tabs(["Tab 1", "Tab 2", ...])`
- Metrics use `st.metric()` with delta indicators
- Cards use `st.container()` with custom CSS borders
- Expanders for detailed content: `st.expander()`
