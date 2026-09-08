#!/usr/bin/env python3
"""
entity_resolver.py - Entity Disambiguation & Freshness Auditor
Checks sameAs links, canonical tags, copyright staleness, and knowledge graph grounding.
"""

import sys
import json
import re
import datetime

CURRENT_YEAR = datetime.date.today().year

def audit_freshness_entity(html_content: str, url: str = "https://example.com"):
    findings = []
    
    # 1. Check Canonical Tag
    has_canonical = bool(re.search(r'<link\s+[^>]*rel=["\']canonical["\'][^>]*>', html_content, re.IGNORECASE))
    if not has_canonical:
        findings.append({
            "id": "F-ENT-001",
            "title": "Missing Canonical URL Declaration",
            "severity": "medium",
            "evidence": "No <link rel='canonical'> found. AI crawlers may index duplicate paths or staging URLs inconsistently.",
            "suggested_action": {
                "summary": f"Add `<link rel='canonical' href='{url}'>` to the <head> of every primary page.",
                "priority": "medium"
            }
        })

    # 2. Check sameAs in JSON-LD
    same_as_matches = re.findall(r'["\']sameAs["\']\s*:\s*(\[[^\]]*\]|"[^"]*")', html_content)
    has_authoritative_same_as = False
    if same_as_matches:
        combined = " ".join(same_as_matches).lower()
        if any(kb in combined for kb in ["wikidata.org", "wikipedia.org", "crunchbase.com", "linkedin.com", "github.com", "x.com", "twitter.com"]):
            has_authoritative_same_as = True

    if not has_authoritative_same_as:
        findings.append({
            "id": "F-ENT-002",
            "title": "Unanchored Entity: Missing sameAs Authority Links",
            "severity": "medium",
            "evidence": "No verified sameAs links to Wikidata, Crunchbase, Wikipedia, or official social profiles found in structured data. Increases entity confusion with homonyms.",
            "suggested_action": {
                "summary": "Populate the `sameAs` array in Organization schema with URLs to Wikidata, Crunchbase, LinkedIn, and official repositories.",
                "priority": "medium"
            }
        })

    # 3. Check Copyright & Content Staleness
    copyright_match = re.search(r'(?:©|&copy;|copyright)\s*(?:20\d\d\s*[-–]\s*)?(20\d\d)', html_content, re.IGNORECASE)
    if copyright_match:
        year = int(copyright_match.group(1))
        if CURRENT_YEAR - year >= 2:
            findings.append({
                "id": "F-ENT-003",
                "title": f"Stale Copyright Year Detected ({year})",
                "severity": "medium",
                "evidence": f"Copyright notice indicates {year} (over {CURRENT_YEAR - year} years outdated). AI models lower freshness ranking when temporal signals appear obsolete.",
                "suggested_action": {
                    "summary": f"Update the site footer copyright notice to {CURRENT_YEAR} and verify publication/modified date headers.",
                    "priority": "medium"
                }
            })

    # 4. Proactive Knowledge Graph Disambiguation Suggestion
    findings.append({
        "id": "F-ENT-P01",
        "title": "Proactive Opportunity: Claim and Anchor Wikidata Entity ID",
        "severity": "low",
        "evidence": "Linking directly to a Wikidata item (Q-ID) in Schema.org provides an unambiguous persistent identifier across all major LLM knowledge graphs.",
        "suggested_action": {
            "summary": "Create or claim a Wikidata entry for the organization and reference its Q-ID in the JSON-LD `@id` attribute.",
            "priority": "low"
        }
    })

    return findings

if __name__ == "__main__":
    sample = sys.stdin.read() if not sys.stdin.isatty() else "<html><body><p>© 2020 Acme Corp</p></body></html>"
    print(json.dumps(audit_freshness_entity(sample), indent=2))
