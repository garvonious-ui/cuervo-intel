---
globs: ["analysis.py", "sprout_import.py", "autostrat_parser.py", "autostrat_loader.py", "autostrat_components.py", "templates.py", "sample_data.py", "dashboard.py"]
---
# Data Layer Rules
- Primary engagement metric: total_engagement = likes + comments + shares + saves
- Cross-brand normalization: engagement_per_1k_followers = (avg_engagement / followers) × 1000
- Collaboration split: owned (cuervo + partner) vs amplified (influencer + collective) — see config.py split_owned_collab()
- Cache isolation: all @st.cache_data functions must include client_id as a parameter
- Autostrat report types: 7 directories + pdfs/ — see @docs/schemas.md
- NOPD framework: Needs (#2ea3f2), Objections (#D9534F), Desires (#5CB85C), Pain Points (#F8C090)
- Content theme classifier is keyword-based (~80-85% accuracy) — do not assume perfect classification
- Sprout CSV schema is documented in @docs/schemas.md — validate column names before processing
