---
name: freshness-corroboration
description: Evaluates brand entity ambiguity, verifies cross-web identity anchors (Wikidata, Wikipedia, Crunchbase, official social links via sameAs), and audits on-page freshness and staleness signals (copyright years, outdated versions).
license: Apache-2.0
allowed-tools: [web_search, read_url, run_command]
---

# Freshness & Entity Corroboration Audit (Discoverability: Appendix D)

## When to use
Use this skill when auditing why an AI assistant confuses a brand with homonyms/generic terms, doubts factual claims due to lack of cross-web consensus, or considers information stale.

## Inputs
- `url` (string, required): The target website URL.
- `html_content` (string, optional): Raw HTML for inspection.

## Procedure
1. **Entity Ambiguity & Identity Anchors**:
   - Check if the site establishes authoritative identity disambiguation via Schema `sameAs` links pointing to trusted knowledge bases (Wikidata, Wikipedia, Crunchbase, GitHub, official social profiles).
   - Check canonical URL specification (`<link rel="canonical">`).
2. **On-Page Staleness Detection**:
   - Extract copyright notices in the footer/page (e.g., `© 2019`, `© 2021`). Compare against the current year.
   - Look for outdated framing (e.g., referencing expired years as "upcoming", legacy product versions).
3. **Cross-Web Consensus Assessment**:
   - Verify that core claims (brand name, HQ, founding year) are unambiguously stated and match external authority references.
4. **Output Emission**:
   - Return structured findings list with `id`, `title`, `severity`, `evidence`, and actionable `suggested_action`.

## Output
Returns a JSON array of findings adhering to the standard schema:
```json
[
  {
    "id": "F-ENT-001",
    "title": "Missing sameAs Knowledge Graph Identity Anchors",
    "severity": "medium",
    "evidence": "No sameAs links to Wikidata, Crunchbase, or official LinkedIn/GitHub profiles found in JSON-LD.",
    "suggested_action": {
      "summary": "Add sameAs array in Organization JSON-LD linking to verified external profiles.",
      "priority": "medium"
    }
  }
]
```
