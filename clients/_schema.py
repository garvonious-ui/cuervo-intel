"""
Client Configuration Schema
============================
Defines the ClientConfig dataclass that every client module must produce.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class ClientConfig:
    """Complete configuration for a single client dashboard."""

    # ── Identity ──
    client_id: str                          # URL slug: "cuervo", "conejos"
    client_name: str                        # Display name: "Jose Cuervo Social Intelligence"
    hero_brand: str                         # Primary brand for self-audit: "Jose Cuervo"
    agency_name: str                        # "Poplife"
    industry: str                           # "tequila", "mezcal", etc.

    # ── Brands ──
    brands: list[str] = field(default_factory=list)
    brand_order: list[str] = field(default_factory=list)
    brand_colors: dict[str, str] = field(default_factory=dict)
    brand_map: dict[str, str] = field(default_factory=dict)          # Sprout handle normalization
    fallback_followers: dict[str, int] = field(default_factory=dict)

    # ── Reference / Inspiration Brands ──
    reference_brands: list[str] = field(default_factory=list)
    reference_brand_labels: dict[str, str] = field(default_factory=dict)

    # ── Autostrat Config ──
    brand_hashtags: dict[str, str] = field(default_factory=dict)     # identifier -> display name
    hero_hashtag_ids: set[str] = field(default_factory=set)          # hero brand's hashtag identifiers
    category_hashtags: dict[str, str] = field(default_factory=dict)
    hero_news_id: str = ""                                             # Google News report identifier

    # ── Strategy Frameworks ──
    pillar_map: dict[str, list[str]] = field(default_factory=dict)
    pillar_targets: dict[str, int] = field(default_factory=dict)
    pillar_colors: dict[str, str] = field(default_factory=dict)
    pillar_descriptions: dict[str, str] = field(default_factory=dict)
    content_mix_map: dict[str, list[str]] = field(default_factory=dict)
    content_mix_targets: dict[str, int] = field(default_factory=dict)
    content_mix_colors: dict[str, str] = field(default_factory=dict)
    kpi_targets: dict[str, Any] = field(default_factory=dict)       # SOCIAL_BRIEF_TARGETS equivalent
    cadence_targets: dict[str, dict] = field(default_factory=dict)
    ig_format_mix: dict[str, dict] = field(default_factory=dict)
    platform_roles: dict[str, dict] = field(default_factory=dict)
    content_source_mix: dict[str, int] = field(default_factory=dict)
    monthly_ramp: dict[str, dict] = field(default_factory=dict)
    testing_roadmap: dict[str, dict] = field(default_factory=dict)
    cultural_calendar: dict[str, dict] = field(default_factory=dict)
    sku_strategy: dict[str, dict] = field(default_factory=dict)
    execution_engines: dict[str, str] = field(default_factory=dict)
    creator_archetypes: dict[str, str] = field(default_factory=dict)
    voice_principles: list[tuple[str, str]] = field(default_factory=list)
    gen_z_leaders: list[str] = field(default_factory=list)

    # ── Sprout Import Config ──
    creator_program_signals: list[str] = field(default_factory=list)
    theme_keywords: dict[str, list[str]] | None = None   # Override defaults if set
    tone_keywords: dict[str, list[str]] | None = None

    # ── Demo Data ──
    brand_profiles: dict[str, dict] = field(default_factory=dict)
    hashtag_pools: dict[str, list[str]] = field(default_factory=dict)

    # ── Theming / CSS ──
    primary_color: str = "#F8C090"
    background_color: str = "#F3EDE6"
    dark_color: str = "#333333"
    accent_color: str = "#2ea3f2"
    custom_css: str = ""

    # ── Assets ──
    logo_path: str = ""
    favicon_path: str = ""
    app_logo_path: str = ""

    # ── Page Copy ──
    page_title: str = "Social Intelligence Dashboard"
    home_title: str = "Social Media Intelligence"
    home_subtitle_template: str = "Competitive analysis across {n} {industry} brands on Instagram & TikTok"
    page_headers: dict[str, str] = field(default_factory=dict)
    page_captions: dict[str, str] = field(default_factory=dict)
    nav_table: str = ""
    excel_filename: str = "intelligence_report.xlsx"
    highlight_fill_color: str = "#FDEBD6"

    # ── Narrative Copy (per-page text blocks) ──
    narrative: dict[str, Any] = field(default_factory=dict)

    # ── Feature Flags ──
    themes_ready: bool = True   # False = hide content theme / source mix sections until manual tagging is done

    # ── Data Paths (resolved at load time by client_context.py) ──
    data_dir: str = ""
    sprout_dir: str = ""
    autostrat_dir: str = ""
    sprout_output_dir: str = ""
