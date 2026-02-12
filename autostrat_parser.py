"""
Autostrat PDF-to-JSON Parser
=============================
Reads PDF exports (from Google Slides) of autostrat.ai reports,
extracts text via pdftotext, and outputs structured JSON matching
the templates in data/autostrat/{report_type}/.

Usage:
    from autostrat_parser import parse_all_pdfs
    results = parse_all_pdfs()  # scans data/autostrat/pdfs/
"""

from __future__ import annotations

import json
import os
import re
import subprocess

BASE_DIR = os.path.dirname(__file__)
AUTOSTRAT_DIR = os.path.join(BASE_DIR, "data", "autostrat")
PDF_DIR = os.path.join(AUTOSTRAT_DIR, "pdfs")

# Map title line to report type directory
REPORT_TYPE_MAP = {
    "tiktok hashtag analysis presentation": "tiktok_hashtags",
    "tiktok hashtag search analysis presentation": "tiktok_hashtags",
    "tiktok profile analysis presentation": "tiktok_profiles",
    "instagram profile analysis presentation": "instagram_profiles",
    "instagram profile presentation": "instagram_profiles",
    "instagram hashtag analysis presentation": "instagram_hashtags",
    "instagram hashtag search analysis presentation": "instagram_hashtags",
    "tiktok keyword analysis presentation": "tiktok_keywords",
    "tiktok keywords analysis presentation": "tiktok_keywords",
    "tiktok keyword search analysis presentation": "tiktok_keywords",
    "tiktok keywords search analysis presentation": "tiktok_keywords",
    "google news analysis presentation": "google_news",
    "google news presentation": "google_news",
}

# Section headings used as text delimiters (order matters for splitting)
SECTION_HEADINGS = [
    "Executive Summary",
    "Audience Profile",
    "Snapshot",
    "Creator Summary",
    "Hashtag Analysis",
    "Interesting Conversations",
    "Conversation Map",
    "Content Trends",
    "Brand Mentions",
    "In-Market Campaigns",
    "How to Win With This Audience",
    "Creator Archetypes",
    "Sponsorship Analysis",
    "Future Sponsorship Suggestions",
    "Engagement Analysis",
    "Posting Analysis",
    "Summary Statistics - By Post Type",
    "Summary Statistics - All Posts",
    "Summary Statistics",
    "Most / Least Liked",
    "Most / Least Comments",
    "Most / Least Engaged",
    "News Analysis",
    "Top Stories",
    "Competitor Coverage",
    "Trending Narratives",
    "Strategic Implications",
    "Appendix",
]


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a PDF using pdftotext."""
    result = subprocess.run(
        ["pdftotext", pdf_path, "-"],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        raise RuntimeError(f"pdftotext failed on {pdf_path}: {result.stderr}")
    return result.stdout


def detect_report_type(text: str) -> tuple[str, str, str]:
    """Detect report type, identifier, and date from the first lines of text.

    Returns (report_type_dir, identifier, date_str).
    """
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    if len(lines) < 3:
        raise ValueError("PDF text too short to detect report type")

    identifier = lines[0].strip("'").strip()
    # Handle cases like "entrapranure's TikTok Profile Analysis"
    if "'s " in identifier:
        identifier = identifier.split("'s ")[0]

    # Find the report type line
    report_type_dir = None
    for line in lines[:5]:
        key = line.strip().lower()
        if key in REPORT_TYPE_MAP:
            report_type_dir = REPORT_TYPE_MAP[key]
            break

    if not report_type_dir:
        # Try partial matching
        for line in lines[:5]:
            key = line.strip().lower()
            for pattern, rtype in REPORT_TYPE_MAP.items():
                if pattern in key or key in pattern:
                    report_type_dir = rtype
                    break
            if report_type_dir:
                break

    if not report_type_dir:
        raise ValueError(f"Could not detect report type from first lines: {lines[:5]}")

    # Find date (look for date-like patterns)
    date_str = ""
    for line in lines[:8]:
        # Match "January 06, 2026" or "2025-07-04" or "December 10, 2025"
        m = re.search(r'(\d{4}-\d{2}-\d{2})', line)
        if m:
            date_str = m.group(1)
            break
        m = re.search(r'(\w+ \d{1,2},?\s*\d{4})', line)
        if m:
            date_str = m.group(1)
            break

    return report_type_dir, identifier, date_str


def split_into_sections(text: str) -> dict[str, str]:
    """Split text into named sections using heading delimiters."""
    sections = {}
    # Remove the boilerplate "How to use this deck" section
    boilerplate_end = text.find("Autostrat Team")
    if boilerplate_end > 0:
        # Find the next line break after boilerplate
        next_nl = text.find("\n", boilerplate_end)
        if next_nl > 0:
            text = text[:text.find("How to use this deck")] + text[next_nl:]

    # Build a list of (position, heading_name) for all headings found
    found = []
    for heading in SECTION_HEADINGS:
        # Use word-boundary matching to avoid partial matches
        pattern = re.escape(heading)
        for m in re.finditer(pattern, text):
            found.append((m.start(), heading, m.end()))

    # Sort by position
    found.sort(key=lambda x: x[0])

    # Deduplicate — if same heading appears multiple times, keep first before Appendix
    # and any after Appendix separately
    appendix_pos = None
    for pos, name, end in found:
        if name == "Appendix":
            appendix_pos = pos
            break

    # Extract sections
    for i, (pos, name, end) in enumerate(found):
        # Skip duplicate headings that appear in the appendix
        if appendix_pos and pos > appendix_pos and name != "Appendix":
            # Store as appendix subsection
            next_pos = found[i + 1][0] if i + 1 < len(found) else len(text)
            key = f"appendix_{name}"
            sections[key] = text[end:next_pos].strip()
            continue

        next_pos = found[i + 1][0] if i + 1 < len(found) else len(text)
        section_text = text[end:next_pos].strip()
        sections[name] = section_text

    return sections


def parse_number(s: str) -> int | float:
    """Parse a number string, handling commas and percentages."""
    s = s.strip().replace(",", "").replace("%", "").strip()
    try:
        if "." in s:
            return float(s)
        return int(s)
    except (ValueError, TypeError):
        return 0


def parse_nopd(text: str) -> dict:
    """Parse Needs/Objections/Desires/Pain Points from audience profile text."""
    result = {"summary": "", "needs": [], "objections": [], "desires": [], "pain_points": []}

    # Split on the NOPD labels
    parts = re.split(r'\n(NEEDS|OBJECTIONS|DESIRES|PAIN POINTS)\n', text)

    if parts:
        result["summary"] = parts[0].strip()

    current_key = None
    key_map = {
        "NEEDS": "needs",
        "OBJECTIONS": "objections",
        "DESIRES": "desires",
        "PAIN POINTS": "pain_points",
    }

    for part in parts[1:]:
        part = part.strip()
        if part in key_map:
            current_key = key_map[part]
        elif current_key:
            # Split into individual items on double newlines or clear paragraph breaks
            items = re.split(r'\n\n+', part)
            for item in items:
                item = item.strip()
                if item and len(item) > 5:
                    result[current_key].append(item)

    return result


def parse_snapshot(text: str) -> dict:
    """Parse snapshot metrics (followers, following, avg likes, etc.).

    The PDF text groups labels together then values together:
      Followers / Following / 1624521 / 1999
      Avg Likes / Avg Comments / Avg Engagement Rate / 101,198 / 1,019 / 6 %
    So we collect label positions and value positions, then match in order.
    """
    snapshot = {
        "followers": 0, "following": 0,
        "avg_likes": 0, "avg_comments": 0, "avg_engagement_rate": 0
    }

    lines = [ln.strip() for ln in text.split("\n")]

    # Pass 1: Collect the ordered labels we care about and the pure-number lines
    label_order = []
    LABEL_MAP = {
        "followers": "followers",
        "following": "following",
        "avg likes": "avg_likes",
        "avg comments": "avg_comments",
        "avg engagement rate": "avg_engagement_rate",
    }

    # Find the two groups: first group (followers/following), second group (avg*)
    group1_labels = []  # followers, following
    group1_values = []
    group2_labels = []  # avg likes, avg comments, avg engagement rate
    group2_values = []

    in_group1 = False
    in_group2 = False
    past_group1_labels = False
    past_group2_labels = False

    for line in lines:
        low = line.lower()
        if not line:
            continue

        if low == "followers":
            in_group1 = True
            group1_labels.append("followers")
        elif low == "following" and in_group1:
            group1_labels.append("following")
            past_group1_labels = True
        elif past_group1_labels and not in_group2 and re.match(r'^[\d,]+\.?\d*\s*%?$', line):
            group1_values.append(parse_number(line))
            if len(group1_values) >= len(group1_labels):
                past_group1_labels = False
        elif low == "avg likes":
            in_group2 = True
            group2_labels.append("avg_likes")
        elif "avg comments" in low and in_group2:
            group2_labels.append("avg_comments")
        elif "avg engagement rate" in low and in_group2:
            group2_labels.append("avg_engagement_rate")
            past_group2_labels = True
        elif past_group2_labels and re.match(r'^[\d,]+\.?\d*\s*%?$', line):
            group2_values.append(parse_number(line))
            if len(group2_values) >= len(group2_labels):
                break

    # Map values to labels
    for i, label in enumerate(group1_labels):
        if i < len(group1_values):
            snapshot[label] = group1_values[i]

    for i, label in enumerate(group2_labels):
        if i < len(group2_values):
            snapshot[label] = group2_values[i]

    return snapshot


def parse_creator_summary(text: str) -> dict:
    """Parse creator summary section."""
    result = {
        "search_purpose": "",
        "topline": "",
        "what_it_means": "",
        "common_themes": [],
        "what_hits": "",
        "what_misses": "",
    }

    # Split by known sub-headings
    sub_headings = ["Search Purpose", "Topline", "What it Means for You",
                    "What it Means", "Common Themes and Topics",
                    "Common Themes", "What Hits", "What Misses"]

    parts = {}
    current = "preamble"
    current_text = []

    for line in text.split("\n"):
        stripped = line.strip()
        matched = False
        for heading in sub_headings:
            if stripped == heading:
                parts[current] = "\n".join(current_text).strip()
                current = heading
                current_text = []
                matched = True
                break
        if not matched:
            current_text.append(line)

    parts[current] = "\n".join(current_text).strip()

    result["search_purpose"] = parts.get("Search Purpose", "")
    result["topline"] = parts.get("Topline", parts.get("preamble", ""))
    result["what_it_means"] = parts.get("What it Means for You",
                                         parts.get("What it Means", ""))
    themes_text = parts.get("Common Themes and Topics",
                            parts.get("Common Themes", ""))
    if themes_text:
        result["common_themes"] = [t.strip() for t in re.split(r'\n\n+', themes_text)
                                   if t.strip() and len(t.strip()) > 5]
    result["what_hits"] = parts.get("What Hits", "")
    result["what_misses"] = parts.get("What Misses", "")

    return result


def parse_how_to_win(text: str) -> dict:
    """Parse How to Win section.

    Structure: summary, "Audience Verbatims" label, Territory 1-5 text,
    then actual verbatim quotes after the last territory.
    """
    result = {"summary": "", "territories": [], "audience_verbatims": []}

    # Split on Territory markers
    territory_pattern = r'Territory \d+'
    parts = re.split(territory_pattern, text)

    if parts:
        first = parts[0].strip()
        # Remove "Audience Verbatims" label from summary
        verbatim_marker = "Audience Verbatims"
        if verbatim_marker in first:
            idx = first.index(verbatim_marker)
            result["summary"] = first[:idx].strip()
        else:
            result["summary"] = first

    # Parse territories — each part between Territory N markers
    for part in parts[1:]:
        part = part.strip()
        if part and len(part) > 10:
            paras = re.split(r'\n\n+', part)
            if paras:
                result["territories"].append(paras[0].strip())

    # Verbatims come AFTER the last territory text
    # Find the last territory's end position, then grab everything after
    last_territory_match = None
    for m in re.finditer(territory_pattern, text):
        last_territory_match = m

    if last_territory_match:
        after_last = text[last_territory_match.end():].strip()
        # Skip the territory text (first paragraph) to get to verbatims
        paras = re.split(r'\n\n+', after_last)
        # First para is the territory text; remaining are verbatims
        for para in paras[1:]:
            para = para.strip()
            if para and len(para) > 8:
                # Split multi-line quotes into individual verbatims
                for line in para.split("\n"):
                    line = line.strip()
                    if line and len(line) > 8:
                        result["audience_verbatims"].append(line)

    return result


def parse_sponsorships(text: str) -> dict:
    """Parse sponsorship analysis section."""
    result = {
        "summary": "",
        "integration_summary": "",
        "categories": [],
        "companies": [],
    }

    sub_headings = ["Sponsorship Summary", "Current Categories",
                    "Integration Summary", "Current Companies"]
    parts = {}
    current = "preamble"
    current_text = []

    for line in text.split("\n"):
        stripped = line.strip()
        matched = False
        for heading in sub_headings:
            if stripped == heading:
                parts[current] = "\n".join(current_text).strip()
                current = heading
                current_text = []
                matched = True
                break
        if not matched:
            current_text.append(line)
    parts[current] = "\n".join(current_text).strip()

    result["summary"] = parts.get("Sponsorship Summary", parts.get("preamble", ""))
    result["integration_summary"] = parts.get("Integration Summary", "")

    cats = parts.get("Current Categories", "")
    if cats:
        result["categories"] = [c.strip() for c in cats.split("\n")
                                if c.strip() and 2 < len(c.strip()) < 40
                                and not c.strip().endswith(".")]

    comps = parts.get("Current Companies", "")
    if comps:
        result["companies"] = [c.strip() for c in comps.split("\n")
                               if c.strip() and 1 < len(c.strip()) < 40
                               and not c.strip().endswith(".")]

    return result


def parse_future_sponsorships(text: str) -> list[dict]:
    """Parse future sponsorship suggestions."""
    suggestions = []

    # Look for category names followed by "Why it Works" and "How to Activate"
    # The structure is: summary paragraph, then category blocks
    lines = text.split("\n")
    summary_end = 0

    # Find where categories start (look for "Why it Works" pattern)
    for i, line in enumerate(lines):
        if "Why it Works" in line or "Why it works" in line:
            summary_end = i
            break

    # Parse the section before "Why it Works" for category names
    pre_text = "\n".join(lines[:summary_end])
    # Categories are typically short phrases (2-5 words) on their own lines
    potential_cats = []
    for line in lines[:summary_end]:
        stripped = line.strip()
        if stripped and 5 < len(stripped) < 60 and not stripped.endswith("."):
            potential_cats.append(stripped)

    # Build suggestions with available data
    # This is a best-effort parse — the PDF format makes precise extraction hard
    current_cat = None
    why_text = []
    how_text = []
    in_why = False
    in_how = False

    for line in lines:
        stripped = line.strip()
        if "Why it Works" in stripped or "Why it works" in stripped:
            if current_cat and (why_text or how_text):
                suggestions.append({
                    "category": current_cat,
                    "why_it_works": " ".join(why_text).strip(),
                    "how_to_activate": [h for h in how_text if h],
                })
                why_text = []
                how_text = []
            in_why = True
            in_how = False
            continue
        if "How to Activate" in stripped or "How to activate" in stripped:
            in_why = False
            in_how = True
            continue

        if in_why and stripped:
            why_text.append(stripped)
        elif in_how and stripped:
            how_text.append(stripped)
        elif stripped and not in_why and not in_how and len(stripped) > 3:
            # Might be a category name
            if len(stripped) < 60 and stripped not in ["Why it Works", "How to Activate"]:
                if current_cat and (why_text or how_text):
                    suggestions.append({
                        "category": current_cat,
                        "why_it_works": " ".join(why_text).strip(),
                        "how_to_activate": [h for h in how_text if h],
                    })
                    why_text = []
                    how_text = []
                current_cat = stripped

    # Don't forget the last one
    if current_cat and (why_text or how_text):
        suggestions.append({
            "category": current_cat,
            "why_it_works": " ".join(why_text).strip(),
            "how_to_activate": [h for h in how_text if h],
        })

    return suggestions


def parse_content_trends(text: str) -> list[dict]:
    """Parse content trends section."""
    trends = []
    # Trends come as title + description paragraphs
    paragraphs = re.split(r'\n\n+', text)
    i = 0
    while i < len(paragraphs):
        para = paragraphs[i].strip()
        if not para:
            i += 1
            continue
        # Short lines are likely titles, longer ones are descriptions
        if len(para) < 80 and i + 1 < len(paragraphs):
            trends.append({
                "trend": para,
                "description": paragraphs[i + 1].strip(),
            })
            i += 2
        else:
            # Might be a combined title+description
            lines = para.split("\n")
            if len(lines) >= 2:
                trends.append({
                    "trend": lines[0].strip(),
                    "description": " ".join(lines[1:]).strip(),
                })
            i += 1

    return trends


def parse_creator_archetypes(text: str) -> list[dict]:
    """Parse creator archetypes section."""
    archetypes = []

    # Look for "The ..." patterns as archetype names
    # Pattern: "The ASMR Mechanic", "The Relatable DIYer", etc.
    the_pattern = r'(The [A-Z][^\n]{3,40})'
    matches = list(re.finditer(the_pattern, text))

    if not matches:
        # Try splitting on "Appeal" markers
        parts = re.split(r'\nAppeal\n', text)
        for part in parts:
            part = part.strip()
            if part and len(part) > 20:
                lines = [ln.strip() for ln in part.split("\n") if ln.strip()]
                if lines:
                    archetypes.append({
                        "archetype": lines[0],
                        "description": " ".join(lines[1:3]) if len(lines) > 1 else "",
                        "appeal": "",
                        "examples": [],
                    })
        return archetypes

    for i, m in enumerate(matches):
        name = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end].strip()

        arch = {"archetype": name, "description": "", "appeal": "", "examples": []}

        # Look for Appeal and Examples sub-sections
        if "Appeal" in block:
            parts = block.split("Appeal")
            arch["description"] = parts[0].strip()
            if len(parts) > 1:
                rest = parts[1]
                if "Examples" in rest:
                    appeal_part, examples_part = rest.split("Examples", 1)
                    arch["appeal"] = appeal_part.strip()
                    arch["examples"] = [ex.strip() for ex in examples_part.strip().split("\n")
                                        if ex.strip() and len(ex.strip()) > 5]
                else:
                    arch["appeal"] = rest.strip()
        else:
            arch["description"] = block

        archetypes.append(arch)

    return archetypes


def parse_brand_mentions(text: str) -> list[dict]:
    """Parse brand mentions section."""
    mentions = []

    # Look for brand name headers followed by context/sentiment/verbatims
    # Split on patterns like "Context\n" and "Sentiment\n"
    sub_headings = ["Context", "Reception", "Sentiment", "Verbatims"]

    # First try to find brand name blocks
    current_brand = None
    current_data = {"brand": "", "context": "", "sentiment": "", "reception": "", "verbatims": []}
    current_field = None

    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped:
            continue

        if stripped in sub_headings:
            current_field = stripped.lower()
            continue

        # Check if this is a brand name (short, capitalized, not a sentence)
        if (len(stripped) < 30 and not stripped.endswith(".")
                and stripped[0].isupper() and current_field is None):
            if current_brand and current_data.get("context"):
                mentions.append(dict(current_data))
            current_brand = stripped
            current_data = {"brand": stripped, "context": "", "sentiment": "",
                            "reception": "", "verbatims": []}
            current_field = None
            continue

        if current_field == "context":
            current_data["context"] += " " + stripped
        elif current_field == "sentiment":
            current_data["sentiment"] += " " + stripped
        elif current_field == "reception":
            current_data["reception"] += " " + stripped
        elif current_field == "verbatims":
            current_data["verbatims"].append(stripped)
        elif current_brand and not current_field:
            # Probably part of the brand description
            current_data["context"] += " " + stripped

    if current_brand and current_data.get("context"):
        mentions.append(dict(current_data))

    # Clean up
    for m in mentions:
        m["context"] = m["context"].strip()
        m["sentiment"] = m["sentiment"].strip()
        m["reception"] = m["reception"].strip()

    return mentions


def parse_hashtag_analysis(text: str) -> dict:
    """Parse hashtag analysis section with findings/opportunities/gaps/actions."""
    result = {
        "summary": "",
        "related_hashtags": [],
        "key_findings": [],
        "opportunities": [],
        "gaps_risks_unmet_needs": [],
        "strategic_actions": [],
    }

    # Split on sub-section headings
    sections = {}
    sub_headings = ["Summary", "Analysis", "Key Findings", "Opportunities",
                    "Gaps, Risks or Unmet Needs", "Strategic Actions",
                    "Themes", "Engagement\nTactics", "Sentiment", "Motivations"]

    # Find Key Findings, Opportunities, Gaps, and Strategic Actions
    for heading in ["Key Findings", "Opportunities",
                    "Gaps, Risks or Unmet Needs", "Strategic Actions"]:
        idx = text.find(heading)
        if idx >= 0:
            # Get text between this heading and the next
            end_idx = len(text)
            for other in ["Key Findings", "Opportunities",
                          "Gaps, Risks or Unmet Needs", "Strategic Actions",
                          "Interesting Conversations", "Content Trends"]:
                if other == heading:
                    continue
                other_idx = text.find(other, idx + len(heading))
                if other_idx > idx and other_idx < end_idx:
                    end_idx = other_idx

            section_text = text[idx + len(heading):end_idx].strip()
            items = [item.strip() for item in re.split(r'\n\n+', section_text)
                     if item.strip() and len(item.strip()) > 10]

            key_map = {
                "Key Findings": "key_findings",
                "Opportunities": "opportunities",
                "Gaps, Risks or Unmet Needs": "gaps_risks_unmet_needs",
                "Strategic Actions": "strategic_actions",
            }
            if heading in key_map:
                result[key_map[heading]] = items

    # Get summary (text before first sub-heading)
    first_heading_pos = len(text)
    for heading in ["Key Findings", "Opportunities", "Gaps, Risks or Unmet Needs"]:
        pos = text.find(heading)
        if 0 <= pos < first_heading_pos:
            first_heading_pos = pos

    if first_heading_pos > 0:
        result["summary"] = text[:first_heading_pos].strip()

    return result


def parse_interesting_conversations(text: str) -> list[dict]:
    """Parse interesting conversations section."""
    conversations = []

    # Look for "Conversation N" patterns
    conv_pattern = r'Conversation \d+'
    parts = re.split(conv_pattern, text)

    # First part is the summary
    summary = parts[0].strip() if parts else ""

    for part in parts[1:]:
        part = part.strip()
        if not part:
            continue
        # First line is title, rest is description
        lines = [ln.strip() for ln in part.split("\n") if ln.strip()]
        if lines:
            conversations.append({
                "title": lines[0],
                "description": " ".join(lines[1:]) if len(lines) > 1 else "",
            })

    return conversations


def parse_conversation_map(text: str) -> dict:
    """Parse conversation map section."""
    result = {
        "summary": "",
        "relationship_analysis": "",
        "overarching_patterns": [],
        "action_opportunities": [],
    }

    sub_headings = {
        "Conversation Map Analysis": None,
        "Relationship Analysis": "relationship_analysis",
        "Overarching Patterns": "overarching_patterns",
        "Conversation Action Opportunities": "action_opportunities",
    }

    current_key = "summary"
    current_text = []

    for line in text.split("\n"):
        stripped = line.strip()
        matched = False
        for heading, key in sub_headings.items():
            if stripped == heading:
                # Save current
                if current_key == "summary":
                    result["summary"] = "\n".join(current_text).strip()
                elif current_key in ("relationship_analysis",):
                    result[current_key] = "\n".join(current_text).strip()
                elif current_key in ("overarching_patterns", "action_opportunities"):
                    items = [t.strip() for t in "\n".join(current_text).strip().split("\n\n")
                             if t.strip() and len(t.strip()) > 10]
                    result[current_key] = items

                current_key = key or "summary"
                current_text = []
                matched = True
                break
        if not matched:
            current_text.append(line)

    # Save last section
    if current_key and current_text:
        text_joined = "\n".join(current_text).strip()
        if current_key in ("overarching_patterns", "action_opportunities"):
            result[current_key] = [t.strip() for t in text_joined.split("\n\n")
                                   if t.strip() and len(t.strip()) > 10]
        elif current_key in result and isinstance(result.get(current_key), str):
            result[current_key] = text_joined

    return result


def parse_in_market_campaigns(text: str) -> list[dict]:
    """Parse in-market campaigns section."""
    campaigns = []
    # Similar to content trends — title + description pairs
    paragraphs = re.split(r'\n\n+', text)
    i = 0
    while i < len(paragraphs):
        para = paragraphs[i].strip()
        if not para:
            i += 1
            continue
        if len(para) < 80 and i + 1 < len(paragraphs):
            campaigns.append({
                "campaign": para,
                "description": paragraphs[i + 1].strip(),
            })
            i += 2
        else:
            lines = para.split("\n")
            if len(lines) >= 2:
                campaigns.append({
                    "campaign": lines[0].strip(),
                    "description": " ".join(lines[1:]).strip(),
                })
            i += 1
    return campaigns


def parse_executive_summary(text: str) -> dict:
    """Parse executive summary section."""
    result = {"overview": "", "key_insights": [], "search_term": "", "search_purpose": ""}

    # Look for "What You Searched" and "Why You're Searching"
    if "What You Searched" in text:
        parts = text.split("What You Searched")
        if len(parts) > 1:
            rest = parts[1]
            if "Why You're Searching" in rest:
                search_part, purpose_part = rest.split("Why You're Searching", 1)
                result["search_term"] = search_part.strip().split("\n")[0].strip()
                result["search_purpose"] = purpose_part.strip().split("\n\n")[0].strip()
            else:
                result["search_term"] = rest.strip().split("\n")[0].strip()

    # Key insights are the titled blocks after the search info
    # They appear as short title + longer description
    paragraphs = re.split(r'\n\n+', text)
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        # Skip the search metadata
        if any(x in para for x in ["What You Searched", "Why You're Searching"]):
            continue
        if len(para) > 30:
            result["key_insights"].append(para)

    if result["key_insights"]:
        result["overview"] = result["key_insights"][0]

    return result


def parse_top_posts(text: str) -> dict:
    """Parse a Most/Least section for top posts."""
    result = {"caption": "", "engagement_rate": 0, "likes": 0, "comments": 0, "link": ""}

    lines = text.split("\n")
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "Caption":
            # Next lines contain the caption
            caption_lines = []
            for j in range(i + 1, min(i + 5, len(lines))):
                if lines[j].strip() and lines[j].strip() not in [
                    "Engagement Rate", "Likes Count", "Comment Count", "Link"
                ]:
                    caption_lines.append(lines[j].strip())
                else:
                    break
            result["caption"] = " ".join(caption_lines)
        elif stripped == "Engagement Rate":
            for j in range(i + 1, min(i + 3, len(lines))):
                m = re.search(r'[\d,.]+', lines[j])
                if m:
                    result["engagement_rate"] = parse_number(m.group())
                    break
        elif stripped == "Likes Count":
            for j in range(i + 1, min(i + 3, len(lines))):
                m = re.search(r'[\d,]+', lines[j])
                if m:
                    result["likes"] = parse_number(m.group())
                    break
        elif stripped == "Comment Count":
            for j in range(i + 1, min(i + 3, len(lines))):
                m = re.search(r'[\d,]+', lines[j])
                if m:
                    result["comments"] = parse_number(m.group())
                    break
        elif "tiktok.com" in stripped or "instagram.com" in stripped:
            result["link"] = stripped

    return result


def parse_statistics(text: str) -> dict:
    """Parse summary statistics section."""
    stats = {
        "all_posts": {
            "min_views": 0, "max_views": 0, "median_views": 0, "avg_views": 0,
            "min_likes": 0, "max_likes": 0, "median_likes": 0, "avg_likes": 0,
            "min_comments": 0, "max_comments": 0, "median_comments": 0, "avg_comments": 0,
        }
    }

    lines = text.split("\n")
    # Look for labeled number patterns
    for i, line in enumerate(lines):
        stripped = line.strip()
        label_map = {
            "Min Views": "min_views", "Max Views": "max_views",
            "Median Views": "median_views", "Avg Views": "avg_views",
            "Min Likes": "min_likes", "Max Likes": "max_likes",
            "Median Likes": "median_likes", "Avg Likes": "avg_likes",
            "Min Comments": "min_comments", "Max Comments": "max_comments",
            "Median Comments": "median_comments", "Avg Comments": "avg_comments",
        }
        for label, key in label_map.items():
            if stripped == label:
                for j in range(i + 1, min(i + 3, len(lines))):
                    m = re.search(r'[\d,]+\.?\d*', lines[j])
                    if m:
                        stats["all_posts"][key] = parse_number(m.group())
                        break

    return stats


# ── Main Parsers per Report Type ──────────────────────────────────────

def parse_tiktok_hashtag(sections: dict, identifier: str, date_str: str) -> dict:
    """Build JSON for a TikTok hashtag analysis report."""
    report = {
        "report_type": "tiktok_hashtag",
        "hashtag": identifier,
        "report_date": date_str,
    }

    if "Executive Summary" in sections:
        report["executive_summary"] = parse_executive_summary(sections["Executive Summary"])

    if "Audience Profile" in sections:
        report["audience_profile"] = parse_nopd(sections["Audience Profile"])

    if "Hashtag Analysis" in sections:
        report["hashtag_analysis"] = parse_hashtag_analysis(sections["Hashtag Analysis"])

    if "Interesting Conversations" in sections:
        convs = parse_interesting_conversations(sections["Interesting Conversations"])
        report["interesting_conversations"] = convs

    if "Conversation Map" in sections:
        report["conversation_map"] = parse_conversation_map(sections["Conversation Map"])

    if "Content Trends" in sections:
        report["content_trends"] = parse_content_trends(sections["Content Trends"])

    if "Brand Mentions" in sections:
        report["brand_mentions"] = parse_brand_mentions(sections["Brand Mentions"])

    if "In-Market Campaigns" in sections:
        report["in_market_campaigns"] = parse_in_market_campaigns(
            sections["In-Market Campaigns"])

    if "How to Win With This Audience" in sections:
        report["how_to_win"] = parse_how_to_win(
            sections["How to Win With This Audience"])

    if "Creator Archetypes" in sections:
        report["creator_archetypes"] = parse_creator_archetypes(
            sections["Creator Archetypes"])

    return report


def parse_tiktok_profile(sections: dict, identifier: str, date_str: str) -> dict:
    """Build JSON for a TikTok profile analysis report."""
    report = {
        "report_type": "tiktok_profile",
        "username": identifier,
        "report_date": date_str,
    }

    if "Audience Profile" in sections:
        report["audience_profile"] = parse_nopd(sections["Audience Profile"])

    if "Snapshot" in sections:
        report["snapshot"] = parse_snapshot(sections["Snapshot"])

    if "Creator Summary" in sections:
        report["creator_summary"] = parse_creator_summary(sections["Creator Summary"])

    if "Sponsorship Analysis" in sections:
        report["sponsorships"] = parse_sponsorships(sections["Sponsorship Analysis"])

    if "Future Sponsorship Suggestions" in sections:
        report["future_sponsorship_suggestions"] = parse_future_sponsorships(
            sections["Future Sponsorship Suggestions"])

    if "Engagement Analysis" in sections:
        report["engagement_analysis"] = {"summary": sections["Engagement Analysis"].strip()}

    if "Summary Statistics" in sections:
        report["statistics"] = parse_statistics(sections["Summary Statistics"])
    elif "Summary Statistics - All Posts" in sections:
        report["statistics"] = parse_statistics(sections["Summary Statistics - All Posts"])

    if "Posting Analysis" in sections:
        report["posting_analysis"] = {"summary": sections["Posting Analysis"].strip()}

    if "How to Win With This Audience" in sections:
        report["how_to_win"] = parse_how_to_win(
            sections["How to Win With This Audience"])

    # Top posts
    top_posts = {}
    if "Most / Least Liked" in sections:
        text = sections["Most / Least Liked"]
        if "Most Liked" in text:
            most_part = text.split("Least Liked")[0] if "Least Liked" in text else text
            top_posts["most_liked"] = parse_top_posts(most_part)
        if "Least Liked" in text:
            least_part = text.split("Least Liked")[1]
            top_posts["least_liked"] = parse_top_posts(least_part)

    if "Most / Least Engaged" in sections:
        text = sections["Most / Least Engaged"]
        if "Most Engaged" in text:
            most_part = text.split("Least Engaged")[0] if "Least Engaged" in text else text
            top_posts["most_engaged"] = parse_top_posts(most_part)
        if "Least Engaged" in text:
            least_part = text.split("Least Engaged")[1]
            top_posts["least_engaged"] = parse_top_posts(least_part)

    if top_posts:
        report["top_posts"] = top_posts

    return report


def parse_instagram_profile(sections: dict, identifier: str, date_str: str) -> dict:
    """Build JSON for an Instagram profile analysis report."""
    report = {
        "report_type": "instagram_profile",
        "username": identifier,
        "report_date": date_str,
    }

    if "Snapshot" in sections:
        report["snapshot"] = parse_snapshot(sections["Snapshot"])

    if "Creator Summary" in sections:
        report["creator_summary"] = parse_creator_summary(sections["Creator Summary"])

    if "Audience Profile" in sections:
        report["audience_profile"] = parse_nopd(sections["Audience Profile"])

    if "Sponsorship Analysis" in sections:
        report["sponsorships"] = parse_sponsorships(sections["Sponsorship Analysis"])

    if "Future Sponsorship Suggestions" in sections:
        report["future_sponsorship_suggestions"] = parse_future_sponsorships(
            sections["Future Sponsorship Suggestions"])

    if "Summary Statistics - All Posts" in sections:
        report["statistics"] = parse_statistics(sections["Summary Statistics - All Posts"])
    elif "Summary Statistics" in sections:
        report["statistics"] = parse_statistics(sections["Summary Statistics"])

    if "Engagement Analysis" in sections:
        report["engagement_analysis"] = {"summary": sections["Engagement Analysis"].strip()}

    if "Posting Analysis" in sections:
        report["posting_analysis"] = {"summary": sections["Posting Analysis"].strip()}

    if "How to Win With This Audience" in sections:
        report["how_to_win"] = parse_how_to_win(
            sections["How to Win With This Audience"])

    # Top posts
    top_posts = {}
    if "Most / Least Liked" in sections:
        text = sections["Most / Least Liked"]
        if "Most Liked" in text:
            most_part = text.split("Least Liked")[0] if "Least Liked" in text else text
            top_posts["most_liked"] = parse_top_posts(most_part)
    if "Most / Least Engaged" in sections:
        text = sections["Most / Least Engaged"]
        if "Least Engaged" in text:
            least_part = text.split("Least Engaged")[1]
            top_posts["least_engaged"] = parse_top_posts(least_part)
    if top_posts:
        report["top_posts"] = top_posts

    return report


def parse_instagram_hashtag(sections: dict, identifier: str, date_str: str) -> dict:
    """Build JSON for an Instagram hashtag analysis report."""
    # Very similar to TikTok hashtag but without conversation map and in-market campaigns
    report = {
        "report_type": "instagram_hashtag",
        "hashtag": identifier,
        "report_date": date_str,
    }

    if "Executive Summary" in sections:
        report["executive_summary"] = parse_executive_summary(sections["Executive Summary"])

    if "Audience Profile" in sections:
        report["audience_profile"] = parse_nopd(sections["Audience Profile"])

    if "Hashtag Analysis" in sections:
        report["hashtag_analysis"] = parse_hashtag_analysis(sections["Hashtag Analysis"])

    if "Content Trends" in sections:
        report["content_trends"] = parse_content_trends(sections["Content Trends"])

    if "Brand Mentions" in sections:
        report["brand_mentions"] = parse_brand_mentions(sections["Brand Mentions"])

    if "Creator Archetypes" in sections:
        report["creator_archetypes"] = parse_creator_archetypes(
            sections["Creator Archetypes"])

    if "How to Win With This Audience" in sections:
        report["how_to_win"] = parse_how_to_win(
            sections["How to Win With This Audience"])

    return report


def parse_tiktok_keywords(sections: dict, identifier: str, date_str: str) -> dict:
    """Build JSON for a TikTok keyword analysis report."""
    report = {
        "report_type": "tiktok_keywords",
        "keyword": identifier,
        "report_date": date_str,
    }

    if "Executive Summary" in sections:
        report["executive_summary"] = parse_executive_summary(sections["Executive Summary"])

    if "Audience Profile" in sections:
        report["audience_profile"] = parse_nopd(sections["Audience Profile"])

    if "Content Trends" in sections:
        report["content_trends"] = parse_content_trends(sections["Content Trends"])

    if "Brand Mentions" in sections:
        report["brand_mentions"] = parse_brand_mentions(sections["Brand Mentions"])

    if "Creator Archetypes" in sections:
        report["creator_archetypes"] = parse_creator_archetypes(
            sections["Creator Archetypes"])

    if "How to Win With This Audience" in sections:
        report["how_to_win"] = parse_how_to_win(
            sections["How to Win With This Audience"])

    return report


def parse_google_news(sections: dict, identifier: str, date_str: str) -> dict:
    """Build JSON for a Google News analysis report."""
    report = {
        "report_type": "google_news",
        "search_query": identifier,
        "report_date": date_str,
    }

    if "Executive Summary" in sections:
        report["executive_summary"] = parse_executive_summary(sections["Executive Summary"])

    if "News Analysis" in sections:
        report["news_analysis"] = {"summary": sections["News Analysis"].strip()}

    if "Brand Mentions" in sections:
        report["brand_mentions"] = parse_brand_mentions(sections["Brand Mentions"])

    if "Trending Narratives" in sections:
        report["trending_narratives"] = parse_content_trends(sections["Trending Narratives"])

    if "Strategic Implications" in sections:
        text = sections["Strategic Implications"].strip()
        report["strategic_implications"] = {"summary": text, "action_items": []}

    return report


# ── Dispatch ──────────────────────────────────────────────────────────

PARSERS = {
    "tiktok_hashtags": parse_tiktok_hashtag,
    "tiktok_profiles": parse_tiktok_profile,
    "instagram_profiles": parse_instagram_profile,
    "instagram_hashtags": parse_instagram_hashtag,
    "tiktok_keywords": parse_tiktok_keywords,
    "google_news": parse_google_news,
}


def parse_pdf(pdf_path: str) -> tuple[str, str, dict]:
    """Parse a single PDF file into structured JSON.

    Returns (report_type_dir, identifier, report_dict).
    """
    text = extract_text_from_pdf(pdf_path)
    report_type_dir, identifier, date_str = detect_report_type(text)
    sections = split_into_sections(text)

    parser_func = PARSERS.get(report_type_dir)
    if not parser_func:
        raise ValueError(f"No parser for report type: {report_type_dir}")

    report = parser_func(sections, identifier, date_str)
    return report_type_dir, identifier, report


def parse_and_save_pdf(pdf_path: str) -> str:
    """Parse a PDF and save the JSON output to the correct directory.

    Returns the output JSON file path.
    """
    report_type_dir, identifier, report = parse_pdf(pdf_path)

    # Create safe filename from identifier
    safe_name = re.sub(r'[^\w\-]', '_', identifier.lower()).strip('_')
    output_dir = os.path.join(AUTOSTRAT_DIR, report_type_dir)
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{safe_name}.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    return output_path


def parse_all_pdfs(pdf_dir: str = None) -> list[dict]:
    """Parse all PDFs in the given directory.

    Returns list of {pdf: str, output: str, report_type: str, identifier: str, error: str|None}.
    """
    if pdf_dir is None:
        pdf_dir = PDF_DIR

    if not os.path.isdir(pdf_dir):
        return []

    results = []
    for filename in sorted(os.listdir(pdf_dir)):
        if not filename.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(pdf_dir, filename)
        try:
            report_type_dir, identifier, report = parse_pdf(pdf_path)
            safe_name = re.sub(r'[^\w\-]', '_', identifier.lower()).strip('_')
            output_dir = os.path.join(AUTOSTRAT_DIR, report_type_dir)
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"{safe_name}.json")

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)

            results.append({
                "pdf": filename,
                "output": output_path,
                "report_type": report_type_dir,
                "identifier": identifier,
                "error": None,
            })
        except Exception as e:
            results.append({
                "pdf": filename,
                "output": None,
                "report_type": None,
                "identifier": None,
                "error": str(e),
            })

    return results
