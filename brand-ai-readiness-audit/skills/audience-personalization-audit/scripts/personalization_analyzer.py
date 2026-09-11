#!/usr/bin/env python3
import re
from typing import List, Dict, Any

def audit_audience_personalization(html_content: str, url: str) -> List[Dict[str, Any]]:
    findings = []
    
    if not html_content:
        return findings

    html_lower = html_content.lower()

    # Check 1: HTML lang attribute
    lang_match = re.search(r'<html[^>]*lang=["\']([^"\']+)["\']', html_lower)
    if not lang_match:
        findings.append({
            "id": "F-PERSONALIZE-001",
            "title": "Missing HTML Language Declaration",
            "severity": "medium",
            "evidence": "The root <html> element does not declare a lang attribute, so the page does not explicitly identify its primary language in machine-readable HTML metadata.",
            "suggested_action": {
                "summary": "Declare the page's primary language using the HTML lang attribute, e.g. <html lang=\"en\">.",
                "priority": "medium"
            }
        })

    # Check 2: Conditional hreflang check for localization
    hreflang_tags = re.findall(r'<link[^>]*hreflang=["\'][^"\']+["\'][^>]*>', html_lower)
    
    # Heuristic to detect if the page actually has multiple regional/language versions
    has_lang_path = bool(re.search(r'href=["\']/[a-z]{2}(?:-[a-z]{2})?/["\']', html_lower))
    has_lang_subdomain = bool(re.search(r'href=["\']https?://[a-z]{2}\.[^"\']+["\']', html_lower))
    has_lang_text = bool(re.search(r'>\s*(english|español|français|deutsch|italiano|português|日本語|中文|select region|choose language)\s*<', html_lower))
    
    is_multi_regional = has_lang_path or has_lang_subdomain or has_lang_text

    if is_multi_regional and not hreflang_tags:
        findings.append({
            "id": "F-PERSONALIZE-002",
            "title": "Missing Explicit Language/Region Targeting (hreflang)",
            "severity": "low",
            "evidence": "The page contains indications of multiple language or regional versions (e.g., language selector links), but 0 `hreflang` tags were detected. AI assistants lack explicit metadata to map users to the correct localized content.",
            "suggested_action": {
                "summary": "Implement <link rel=\"alternate\" hreflang=\"...\"> tags for all supported regions to explicitly link localized versions.",
                "priority": "low"
            }
        })

    return findings
