#!/usr/bin/env python3
"""
deduplicate.py - Corroboration & False-Positive Suppression Filter
Eliminates redundant findings, consolidates cross-skill signals, and suppresses low-confidence issues.
"""

from typing import List, Dict, Any

def deduplicate_findings(findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if not findings:
        return []

    # 1. First-pass title normalization deduplication
    seen_titles = set()
    first_pass = []

    has_spa_empty = any(f.get("id") == "F-CRAWL-001" or "client-side render gap" in f.get("title", "").lower() for f in findings)
    has_crawl_alt = any(f.get("id") == "F-CRAWL-005" for f in findings)

    for f in findings:
        norm_title = f.get("title", "").lower().strip()
        fid = f.get("id", "")

        # Cross-skill consolidation: if crawl-render-audit already flagged missing alt text (F-CRAWL-005),
        # suppress duplicate email-summary-audit alt text finding (F-EMAIL-002).
        if fid == "F-EMAIL-002" and has_crawl_alt:
            continue

        if norm_title in seen_titles:
            continue
        seen_titles.add(norm_title)

        # Multi-signal corroboration rule for Empty SPA Shells:
        # If F-CRAWL-001 (SPA Empty) fired, reframe secondary downstream missing-element warnings
        # to explicitly indicate they are downstream symptoms of the client-side hydration gap.
        if has_spa_empty:
            if fid in ["F-DATA-002", "F-ENG-001"]:
                f = dict(f)
                f["evidence"] = f["evidence"] + " (Note: This finding is a direct downstream symptom of the raw HTML client-side rendering gap detected in F-CRAWL-001.)"
                f["severity"] = "medium"

        first_pass.append(f)

    return first_pass
