---
globs: ["clients/**/*.py", "client_context.py"]
---
# Multi-Tenant Client Rules
- ClientConfig is defined in clients/_schema.py — all new fields go there
- Every client's client.py must export get_config() -> ClientConfig
- Brand handle mappings (BRAND_MAP) must exactly match Sprout CSV "Profile" column values
- Never put client-specific constants in config.py — that file is shared-only
- When adding a ClientConfig field, add it with a sensible default so existing clients don't break
- Reference @docs/schemas.md for the full ClientConfig field reference
- Reference @docs/onboarding-client.md for the new client setup checklist
