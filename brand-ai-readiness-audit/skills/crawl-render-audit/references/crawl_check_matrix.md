# Crawlability & JS-Render Failure Modes Matrix

| Code | Failure Mode | Severity | Detection Mechanism | Resolution |
| :--- | :--- | :--- | :--- | :--- |
| **F-CRAWL-001** | Client-Side Render Gap (SPA Root) | **Critical** | Raw HTML word count $< 60$ with `<div id="root">` placeholder. | Migrate to SSR/SSG (Next.js, Astro, Remix). |
| **F-CRAWL-002** | JS-Locked Pricing/Specs | **High** | Price/specs found in JS bundles but missing in plain HTML DOM. | Render critical specs server-side. |
| **F-CRAWL-003** | `noindex` Directives | **Critical** | Meta tag or header `X-Robots-Tag: noindex`. | Remove `noindex` on public landing pages. |
| **F-CRAWL-004** | Blocked AI Bot Agents | **High** | Disallow rules for `GPTBot`, `ClaudeBot`, `PerplexityBot`. | Grant explicit allow directives in `robots.txt`. |
| **F-CRAWL-005** | Missing Alt Text | **Medium** | Ratio of missing alt attributes $> 40\%$. | Add descriptive alt text to all informative media. |
| **F-CRAWL-P01** | Missing `/llms.txt` | **Low (Proactive)** | 404 or absence of `/llms.txt` standard file. | Author and publish `/llms.txt`. |
