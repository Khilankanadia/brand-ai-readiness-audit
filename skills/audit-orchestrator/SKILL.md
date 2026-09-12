---
name: audit-orchestrator
description: Designated entrypoint skill that coordinates all discovery and engagement audit skills, merges findings, resolves duplicates, computes deterministic severity summaries, and outputs the final standardized JSON audit report.
license: Apache-2.0
allowed-tools: [read_url, run_command]
---

# Brand AI-Readiness Audit Orchestrator (Entrypoint)

## When to use
Use this designated entrypoint skill to run a complete, end-to-end Brand AI Discoverability and On-Site Engagement audit on any given website domain or URL.

## Inputs
- `url` (string, required): The target website URL to audit (e.g., `https://example.com`).
- `html_content` (string, optional): Raw HTML string for offline/fixture audit execution.
- `robots_content` (string, optional): Content of `robots.txt` for sandboxed crawl evaluation.

## Procedure
1. **Initialize Audit Session**:
   - Record target URL and generation timestamp (`audited_at` in ISO 8601 UTC format).
2. **Execute Domain Audits in Sequence**:
   - Run `crawl-render-audit` to detect crawl barriers, JS render gaps, AI crawler blocks, and `llms.txt`.
   - Run `structured-data-audit` to validate Schema.org JSON-LD syntax, schema completeness, and meta tags.
   - Run `freshness-corroboration` to inspect `sameAs` entity links, canonical URLs, and copyright freshness.
   - Run `engagement-audit` to inspect above-the-fold orientation, navigation cognitive load, and trust signals.
   - Run `audience-personalization-audit` to inspect `hreflang` tags, `og:locale`, and HTML `lang` attributes.
   - Run `email-summary-audit` to inspect text-to-image ratios and image `alt` text fallbacks.
3. **Merge & De-duplicate Findings**:
   - Combine all findings from child skills.
   - Suppress redundant or overlapping findings using multi-signal corroboration rules.
   - Ensure sequential finding IDs (`F-001`, `F-002`, ...).
4. **Compute Summary Statistics**:
   - Automatically tally severity counts (`critical`, `high`, `medium`, `low`, `total_findings`).
5. **Ensure Proactive Improvement Recommendations**:
   - Guarantee that at least one actionable proactive suggestion (e.g. `llms.txt`, FAQPage Schema, Wikidata grounding) is present in the final output.
6. **Emit Standardized Audit Report**:
   - Output the final report strictly adhering to the contest schema.

## Output
Emits a single JSON audit report:
```json
{
  "site": "example.com",
  "audited_at": "2026-09-20T14:32:00Z",
  "summary": {
    "total_findings": 4,
    "critical": 1,
    "high": 1,
    "medium": 1
  },
  "findings": [
    {
      "id": "F-001",
      "title": "No JSON-LD structured data on product pages",
      "severity": "high",
      "evidence": "Crawled 12 product pages; 0/12 contain schema.org markup.",
      "suggested_action": {
        "summary": "Add Product/Offer JSON-LD to every product page.",
        "priority": "high"
      }
    }
  ]
}
```
