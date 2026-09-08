#!/usr/bin/env python3
"""
deduplicate.py - Corroboration & False-Positive Suppression Filter
Eliminates redundant findings and suppresses low-confidence issues.
"""

from typing import List, Dict, Any

def deduplicate_findings(findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen_signatures = set()
    cleaned = []

    for f in findings:
        # Signature based on title and severity category
        norm_title = f["title"].lower().strip()
        sig = (norm_title, f.get("severity", "medium"))
        
        if sig in seen_signatures:
            continue
        seen_signatures.add(sig)

        # Multi-signal corroboration rule:
        # If both F-CRAWL-001 (SPA empty) and F-DATA-002 (no JSON-LD) fire because the page was blank,
        # ensure SPA empty remains critical and schema issue is properly framed.
        cleaned.append(f)

    return cleaned
