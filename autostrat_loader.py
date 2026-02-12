"""
Autostrat Intelligence Report Loader
=====================================
Loads parsed JSON reports from data/autostrat/ subdirectories
and provides query functions for the dashboard pages.
"""

from __future__ import annotations

import json
import os
from typing import Any, Optional

from config import REFERENCE_BRANDS

BASE_DIR = os.path.dirname(__file__)
AUTOSTRAT_DIR = os.path.join(BASE_DIR, "data", "autostrat")

REPORT_TYPES = [
    "instagram_profiles",
    "tiktok_profiles",
    "instagram_hashtags",
    "tiktok_hashtags",
    "tiktok_keywords",
    "google_news",
]

REPORT_TYPE_LABELS = {
    "instagram_profiles": "Instagram Profiles",
    "tiktok_profiles": "TikTok Profiles",
    "instagram_hashtags": "Instagram Hashtags",
    "tiktok_hashtags": "TikTok Hashtags",
    "tiktok_keywords": "TikTok Keywords",
    "google_news": "Google News",
}

# Profile report types (per-brand)
PROFILE_TYPES = ["instagram_profiles", "tiktok_profiles"]

# Conversation/trend report types (per-hashtag/keyword)
CONVERSATION_TYPES = ["instagram_hashtags", "tiktok_hashtags", "tiktok_keywords"]


def load_report(report_type: str, filename: str) -> Optional[dict]:
    """Load a single JSON report. Returns None if not found."""
    path = os.path.join(AUTOSTRAT_DIR, report_type, filename)
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def load_all_reports(report_type: str) -> dict[str, dict]:
    """Load all non-template JSON files from a report type directory.

    Returns {identifier: report_data} where identifier is the filename stem.
    """
    report_dir = os.path.join(AUTOSTRAT_DIR, report_type)
    if not os.path.isdir(report_dir):
        return {}

    reports = {}
    for filename in sorted(os.listdir(report_dir)):
        if not filename.endswith(".json") or filename.startswith("_"):
            continue
        filepath = os.path.join(report_dir, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            identifier = os.path.splitext(filename)[0]
            reports[identifier] = data
        except (json.JSONDecodeError, OSError):
            continue

    return reports


def load_all_autostrat() -> dict[str, dict[str, dict]]:
    """Load all autostrat reports across all report types.

    Returns {report_type: {identifier: report_data}}.
    """
    all_data = {}
    for rt in REPORT_TYPES:
        all_data[rt] = load_all_reports(rt)
    return all_data


def has_autostrat_data(autostrat: dict) -> bool:
    """Check if any autostrat reports are loaded."""
    return any(len(reports) > 0 for reports in autostrat.values())


def is_reference_brand(identifier: str) -> bool:
    """Check if an autostrat profile identifier is a reference/inspiration brand."""
    return identifier.lower() in [rb.lower() for rb in REFERENCE_BRANDS]


def get_available_identifiers(autostrat: dict, report_type: str) -> list[str]:
    """Get list of identifiers (brand names, hashtags, etc.) for a report type."""
    return list(autostrat.get(report_type, {}).keys())


def get_competitor_identifiers(autostrat: dict, report_type: str) -> list[str]:
    """Get identifiers for a report type, excluding reference/inspiration brands."""
    return [i for i in get_available_identifiers(autostrat, report_type)
            if not is_reference_brand(i)]


def get_reference_profiles(autostrat: dict) -> dict[str, dict]:
    """Get all profile reports for reference/inspiration brands.

    Returns {key: {report_type, identifier, report}} across both platforms.
    """
    results = {}
    for rt in PROFILE_TYPES:
        for identifier, report in autostrat.get(rt, {}).items():
            if is_reference_brand(identifier):
                results[f"{rt}:{identifier}"] = {
                    "report_type": rt,
                    "identifier": identifier,
                    "report": report,
                }
    return results


def get_report(autostrat: dict, report_type: str, identifier: str) -> Optional[dict]:
    """Get a specific report by type and identifier."""
    return autostrat.get(report_type, {}).get(identifier)


def get_section_across_reports(
    autostrat: dict, report_type: str, section_key: str
) -> dict[str, Any]:
    """Extract a specific section from all reports of a given type.

    Returns {identifier: section_data}.
    """
    result = {}
    for identifier, report in autostrat.get(report_type, {}).items():
        if section_key in report:
            result[identifier] = report[section_key]
    return result


def get_all_audience_profiles(
    autostrat: dict, exclude_reference: bool = False
) -> list[dict]:
    """Get all audience profiles across all report types.

    Returns list of {source_type, identifier, audience_profile}.
    When exclude_reference=True, skips reference/inspiration brand profiles.
    """
    profiles = []
    for rt in REPORT_TYPES:
        for identifier, report in autostrat.get(rt, {}).items():
            if exclude_reference and rt in PROFILE_TYPES and is_reference_brand(identifier):
                continue
            if "audience_profile" in report:
                ap = report["audience_profile"]
                if any(ap.get(k) for k in ["needs", "objections", "desires", "pain_points"]):
                    profiles.append({
                        "source_type": rt,
                        "source_label": REPORT_TYPE_LABELS.get(rt, rt),
                        "identifier": identifier,
                        "audience_profile": ap,
                    })
    return profiles


def get_all_how_to_win(
    autostrat: dict, exclude_reference: bool = False
) -> list[dict]:
    """Get all How to Win sections across all report types.

    Returns list of {source_type, identifier, how_to_win}.
    When exclude_reference=True, skips reference/inspiration brand profiles.
    """
    results = []
    for rt in REPORT_TYPES:
        for identifier, report in autostrat.get(rt, {}).items():
            if exclude_reference and rt in PROFILE_TYPES and is_reference_brand(identifier):
                continue
            if "how_to_win" in report:
                hw = report["how_to_win"]
                if hw.get("territories") or hw.get("summary"):
                    results.append({
                        "source_type": rt,
                        "source_label": REPORT_TYPE_LABELS.get(rt, rt),
                        "identifier": identifier,
                        "how_to_win": hw,
                    })
    return results


def get_all_brand_mentions(autostrat: dict) -> list[dict]:
    """Get all brand mentions across hashtag/keyword reports.

    Returns flat list of {source_type, source_identifier, brand, context, sentiment, ...}.
    """
    mentions = []
    for rt in CONVERSATION_TYPES + ["google_news"]:
        for identifier, report in autostrat.get(rt, {}).items():
            for mention in report.get("brand_mentions", []):
                mentions.append({
                    "source_type": rt,
                    "source_label": REPORT_TYPE_LABELS.get(rt, rt),
                    "source_identifier": identifier,
                    **mention,
                })
    return mentions


def get_all_content_trends(autostrat: dict) -> list[dict]:
    """Get all content trends across reports.

    Returns list of {source_type, source_identifier, trend, description}.
    """
    trends = []
    for rt in CONVERSATION_TYPES:
        for identifier, report in autostrat.get(rt, {}).items():
            for trend in report.get("content_trends", []):
                trends.append({
                    "source_type": rt,
                    "source_label": REPORT_TYPE_LABELS.get(rt, rt),
                    "source_identifier": identifier,
                    **trend,
                })
    return trends


def get_all_creator_archetypes(autostrat: dict) -> list[dict]:
    """Get all creator archetypes across reports.

    Returns list of {source_type, source_identifier, archetype, description, appeal, examples}.
    """
    archetypes = []
    for rt in CONVERSATION_TYPES:
        for identifier, report in autostrat.get(rt, {}).items():
            for arch in report.get("creator_archetypes", []):
                archetypes.append({
                    "source_type": rt,
                    "source_label": REPORT_TYPE_LABELS.get(rt, rt),
                    "source_identifier": identifier,
                    **arch,
                })
    return archetypes


def get_all_strategic_actions(autostrat: dict) -> list[dict]:
    """Get strategic actions and opportunities from hashtag analysis reports.

    Returns list of {source_identifier, key_findings, opportunities, gaps, actions}.
    """
    results = []
    for rt in CONVERSATION_TYPES:
        for identifier, report in autostrat.get(rt, {}).items():
            ha = report.get("hashtag_analysis", {})
            if any(ha.get(k) for k in ["key_findings", "opportunities",
                                        "gaps_risks_unmet_needs", "strategic_actions"]):
                results.append({
                    "source_type": rt,
                    "source_label": REPORT_TYPE_LABELS.get(rt, rt),
                    "source_identifier": identifier,
                    "key_findings": ha.get("key_findings", []),
                    "opportunities": ha.get("opportunities", []),
                    "gaps_risks_unmet_needs": ha.get("gaps_risks_unmet_needs", []),
                    "strategic_actions": ha.get("strategic_actions", []),
                })
    return results


def get_all_sponsorship_suggestions(
    autostrat: dict, exclude_reference: bool = False
) -> list[dict]:
    """Get all future sponsorship suggestions from profile reports.

    Returns list of {source_type, identifier, suggestions: [...]}.
    When exclude_reference=True, skips reference/inspiration brand profiles.
    """
    results = []
    for rt in PROFILE_TYPES:
        for identifier, report in autostrat.get(rt, {}).items():
            if exclude_reference and is_reference_brand(identifier):
                continue
            suggestions = report.get("future_sponsorship_suggestions", [])
            if suggestions:
                results.append({
                    "source_type": rt,
                    "source_label": REPORT_TYPE_LABELS.get(rt, rt),
                    "identifier": identifier,
                    "suggestions": suggestions,
                })
    return results


def get_report_counts(autostrat: dict) -> dict[str, int]:
    """Get count of reports per type."""
    return {rt: len(reports) for rt, reports in autostrat.items()}
