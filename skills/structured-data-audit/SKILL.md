---
name: structured-data-audit
description: Validates Schema.org JSON-LD and Microdata markup completeness, verifies whether core brand and product facts are stated in plain unambiguous text, and inspects OpenGraph metadata for AI quotation readiness.
license: Apache-2.0
allowed-tools: [read_url, run_command]
---

# Structured Data & Fact Extractability Audit (Discoverability: Appendix B & C)

## When to use
Use this skill when auditing how easily AI assistants and search engines can parse, quote, and extract explicit, high-confidence facts (organization identity, product offerings, pricing, FAQs, author credentials) from a webpage.

## Inputs
- `url` (string, required): The target website URL.
- `html_content` (string, optional): Raw HTML for inspection.

## Procedure
1. **JSON-LD & Microdata Extraction**:
   - Locate and parse all `<script type="application/ld+json">` elements.
   - Extract declared `@type` (e.g., `Organization`, `Product`, `Article`, `LocalBusiness`, `FAQPage`, `SoftwareApplication`).
2. **Schema Completeness & Property Validation**:
   - Check whether mandatory properties are populated with non-placeholder values:
     - `Organization`: `name`, `url`, `logo`, `description`, `sameAs`.
     - `Product`: `name`, `description`, `offers` (with `price`, `priceCurrency`), `brand`.
     - `FAQPage`: `mainEntity` array with `Question` and `AcceptedAnswer`.
   - Flag empty schemas, schema validation errors, or total absence of structured data.
3. **Plain-Text Quotability Cross-Check**:
   - Verify that core facts (company name, primary value proposition, pricing) appear in clean semantic HTML tags (`<h1>`, `<h2>`, `<p>`) without obfuscation.
4. **Social & Search Meta Tag Quality**:
   - Check for `meta[name="description"]`, `og:title`, `og:description`, `og:image`.
   - Flag generic/boilerplate meta descriptions (e.g., "Home", "Welcome to our website", strings $< 30$ chars).
5. **Actionable Code Snippet Generation**:
   - Provide a copy-paste JSON-LD script snippet in `suggested_action` tailored to the detected page context.

## Output
Returns a JSON array of findings adhering to the standard schema:
```json
[
  {
    "id": "F-DATA-001",
    "title": "Missing JSON-LD Structured Data",
    "severity": "high",
    "evidence": "0 JSON-LD or Microdata blocks found on the page. AI answer engines cannot extract authoritative structured facts.",
    "suggested_action": {
      "summary": "Embed Schema.org Organization and Product JSON-LD in the HTML <head>.",
      "priority": "high"
    }
  }
]
```
