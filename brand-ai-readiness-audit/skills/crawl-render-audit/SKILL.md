---
name: crawl-render-audit
description: Audits a target website for crawlability, client-side JS rendering gaps, robots.txt restrictions (especially against AI crawlers like GPTBot, ClaudeBot, PerplexityBot), llms.txt availability, and non-text trapped content.
license: Apache-2.0
allowed-tools: [read_url, run_command]
---

# Crawl & Render Audit (Discoverability: Appendix A & C)

## When to use
Use this skill when auditing why an AI assistant or search crawler cannot access, parse, or index key brand facts on a website due to crawl barriers, JS-only content rendering, or crawler-specific access blocks.

## Inputs
- `url` (string, required): The target website URL or domain (e.g. `https://example.com`).
- `html_content` (string, optional): Pre-fetched raw HTML for offline/fixture testing.
- `robots_content` (string, optional): Pre-fetched `robots.txt` content for sandboxed checks.

## Procedure
1. **Robots.txt & AI Crawler Access Inspection**:
   - Fetch or simulate `robots.txt` from the domain root.
   - Evaluate general search engine access (`Googlebot`, `Bingbot`).
   - Specifically check for disallow rules targeting known AI assistant user agents: `GPTBot`, `ClaudeBot`, `PerplexityBot`, `Google-Extended`, `Amazonbot`, `Bytespider`.
   - Flag any rule that blocks AI crawlers from accessing core brand, product, or pricing pages.
2. **`llms.txt` Discovery Check**:
   - Check whether `/llms.txt` or `/llms-full.txt` is published at the root domain.
   - If missing, generate a proactive improvement suggestion with a recommended `llms.txt` structure.
3. **HTTP vs JS-Rendered Differential Analysis**:
   - Inspect raw server-rendered HTML versus client-side hydration signals (`<div id="root">`, `<div id="__next">` with empty markup, client-rendered script bundles).
   - Detect if critical information (e.g., pricing, features, company description) is absent from raw HTML and only visible after client-side script execution.
4. **Non-Text Content Traps**:
   - Scan for images missing descriptive `alt` tags, embedded PDFs, canvas elements, or SVG-only text that prevent text extraction.
5. **Output Emission**:
   - Return structured findings list with `id`, `title`, `severity`, `evidence`, and actionable `suggested_action`.

## Output
Returns a JSON array of findings adhering to the standard schema:
```json
[
  {
    "id": "F-CRAWL-001",
    "title": "AI Assistant Crawler Blocked in robots.txt",
    "severity": "critical",
    "evidence": "robots.txt explicitly disallows GPTBot and ClaudeBot from accessing /products and /pricing.",
    "suggested_action": {
      "summary": "Update robots.txt to allow GPTBot and ClaudeBot crawl access to public landing pages.",
      "priority": "critical"
    }
  }
]
```
