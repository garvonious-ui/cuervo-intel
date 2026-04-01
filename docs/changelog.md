# Changelog

## 2026-04-01 — Session 0 (Baseline)
- Project restructured to follow Claude Code Project Structure Guide
- Created docs/ directory with architecture.md, schemas.md, build-plan.md, changelog.md, design-system.md, page-specs.md, onboarding-client.md
- Rewrote CLAUDE.md from 180 lines → ~88 lines (lean index pointing to docs/)
- Added .claude/commands/ (start, checkpoint, wrap, status)
- Added .claude/rules/ (pages.md, clients.md, data-layer.md)
- Absorbed HANDOFF.md content into docs/ files and removed it
- Cleaned up fully-merged Claude Code branches (cool-dubinsky, elegant-hypatia, jolly-poitras)
- Flagged claude/reverent-borg for manual review (1 unmerged Strategy page commit, will conflict)

### Historical Summary (pre-structure, 293 commits)
- Initial build: single-client Cuervo competitive dashboard
- Refactored to multi-tenant architecture (March 2026)
- Added Devils Reserve as second client
- 5 dashboard pages: Brand Performance, Competitive Landscape, Strategy, Inspiration & Explorer, Conversation Intel
- Autostrat PDF/PPTX parser and qualitative intelligence system
- Sprout Social CSV import with AI content classifiers
- Excel report export
- Deployed on Streamlit Community Cloud
