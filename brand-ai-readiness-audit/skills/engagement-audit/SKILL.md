---
name: engagement-audit
description: Audits on-site user orientation, above-the-fold value clarity (5-second rule), navigation hierarchy, breadcrumbs and context retention, and trust/friction signals to prevent visitor bounce.
license: Apache-2.0
allowed-tools: [read_url, run_command]
---

# On-Site Engagement & Friction Audit (On-Site Half)

## When to use
Use this skill when auditing why visitors arriving at a website fail to engage, bounce quickly, or lose orientation due to confusing hero banners, cluttered navigation, missing breadcrumbs, or absent contact/trust signals.

## Inputs
- `url` (string, required): The target website URL.
- `html_content` (string, optional): Raw HTML for inspection.

## Procedure
1. **Above-the-Fold Orientation Check (5-Second Rule)**:
   - Check for a clear, descriptive `<h1>` tag within the hero/header.
   - Verify that the `<h1>` contains meaningful descriptive words rather than vague buzzwords (e.g., "Welcome", "The Future is Now").
   - Check for an accompanying descriptive subtitle or tagline (`<p>`, `<h2>`).
2. **Navigation Hierarchy & Complexity**:
   - Count top-level navigation links in `<nav>` or `<header>`.
   - Flag excessive nav links ($> 10$ top-level items without grouping) causing cognitive overload.
3. **Context Retention & Breadcrumbs**:
   - Check for breadcrumbs (`<nav aria-label="breadcrumb">` or Schema `BreadcrumbList`) on deep or multi-level pages.
   - Check for a consistent home/brand logo linking back to root (`href="/"`).
4. **Friction & Trust Signals**:
   - Check for presence of essential trust pages: "About", "Contact", "Privacy", "Terms".
   - Flag missing contact channels or dead-end layouts.
5. **Output Emission**:
   - Return structured findings list with `id`, `title`, `severity`, `evidence`, and actionable `suggested_action`.

## Output
Returns a JSON array of findings adhering to the standard schema:
```json
[
  {
    "id": "F-ENG-001",
    "title": "Missing or Weak Above-the-Fold H1 Heading",
    "severity": "high",
    "evidence": "No <h1> element found on the landing page. First-time visitors cannot immediately discern the site's primary purpose.",
    "suggested_action": {
      "summary": "Add a prominent <h1> with a direct, benefit-focused value proposition above the fold.",
      "priority": "high"
    }
  }
]
```
