---
name: audience-personalization-audit
description: Audits a website for localization and personalization tagging (e.g., hreflang, og:locale) to ensure AI assistants can tailor context based on user demographics and location.
license: Apache-2.0
allowed-tools: [read_url, run_command]
---

# Audience Personalization & Prior Context Audit (Discoverability: Appendix E)

## When to use
Use this skill to determine if a brand's website provides sufficient explicit metadata (language/region targeting, audience specification) that allows an AI assistant to confidently personalize its answer for specific users based on their location, language, or stated preferences.

## Inputs
- `url` (string, required): The target website URL.
- `html_content` (string, optional): Raw HTML for inspection.

## Procedure
1. **Localization Extraction**:
   - Check the HTML `<head>` for `<link rel="alternate" hreflang="...">` tags.
   - Check the `<html>` tag for the `lang` attribute.
   - Check for `<meta property="og:locale">`.
2. **Analysis**:
   - If a global brand lacks `hreflang` or basic localization tagging, flag as an issue, since an AI assistant may mix up regional product offerings or pricing when tailoring an answer to a non-US user.
   - If the `html` tag lacks a `lang` attribute, flag it as a fundamental context failure.
3. **Actionable Code Snippet Generation**:
   - Provide concrete suggestions for injecting `hreflang` mappings or `og:locale` to ensure the assistant knows exactly which demographic the page serves.

## Output
Returns a JSON array of findings adhering to the standard schema:
```json
[
  {
    "id": "F-PERSONALIZE-001",
    "title": "Missing Explicit Language/Region Targeting",
    "severity": "medium",
    "evidence": "No `hreflang` tags or `og:locale` properties found. AI assistants cannot accurately route regional users to localized context.",
    "suggested_action": {
      "summary": "Implement <link rel=\"alternate\" hreflang=\"...\"> tags for all supported regions in the <head>.",
      "priority": "medium"
    }
  }
]
```
