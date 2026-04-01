---
globs: ["pages/*.py"]
---
# Streamlit Page Rules
- Always call `cfg = get_client()` at the top — never import client-specific constants directly
- Always call `st.logo(cfg.logo_path)` and `st.markdown(cfg.custom_css, unsafe_allow_html=True)`
- Page 1 and Page 3 use UNFILTERED data (st.session_state["df"]) — do NOT apply sidebar filters
- Page 2 uses FILTERED data (st.session_state["filtered_df"]) — sidebar filters apply
- Page 5 uses autostrat data only — no DataFrame filtering
- All narrative text comes from cfg.narrative[page_key][section_key] — never hardcode copy
- Use CHART_TEMPLATE and CHART_FONT from config.py for all Plotly charts
- Test with both ?client=cuervo and ?client=devils_reserve after any page change
- Reference @docs/page-specs.md for tab structure and data flow per page
