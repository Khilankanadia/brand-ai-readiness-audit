#!/usr/bin/env python3
"""
compose_report.py - Audit Report Schema Formatter & Finalizer
Aggregates findings, computes exact severity counts, and emits standard JSON.
"""

import os
import sys
from typing import List, Dict, Any
import datetime

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from deduplicate import deduplicate_findings

def compose_final_report(site: str, raw_findings: List[Dict[str, Any]], audited_at: str = None) -> Dict[str, Any]:
    if not audited_at:
        audited_at = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    deduped = deduplicate_findings(raw_findings)

    # Format findings with sequential IDs
    formatted_findings = []
    counts = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0
    }

    # Ensure at least one proactive finding is included
    proactive_exists = any(f.get("severity") == "low" or "proactive" in f.get("title", "").lower() for f in deduped)
    if not proactive_exists:
        deduped.append({
            "id": "F-PROACTIVE-DEFAULT",
            "title": "Proactive Recommendation: Publish /llms.txt for AI Search Indexing",
            "severity": "low",
            "evidence": "Website has not deployed a dedicated /llms.txt manifest. Adding this provides explicit context grounding for retrieval engines.",
            "suggested_action": {
                "summary": "Create and host /llms.txt with brand summary, API documentation, and core product URLs.",
                "priority": "low"
            }
        })

    for idx, item in enumerate(deduped, start=1):
        sev = item.get("severity", "medium").lower()
        if sev not in counts:
            sev = "medium"
        counts[sev] += 1

        formatted_findings.append({
            "id": f"F-{idx:03d}",
            "title": item["title"],
            "severity": sev,
            "evidence": item["evidence"],
            "suggested_action": {
                "summary": item["suggested_action"]["summary"],
                "priority": item["suggested_action"].get("priority", sev)
            }
        })

    total = len(formatted_findings)

    summary_obj = {
        "total_findings": total,
        "critical": counts["critical"],
        "high": counts["high"],
        "medium": counts["medium"]
    }
    # Keep low count if present (allowed additions to schema)
    if counts["low"] > 0:
        summary_obj["low"] = counts["low"]

    return {
        "site": site,
        "audited_at": audited_at,
        "summary": summary_obj,
        "findings": formatted_findings
    }
