---
name: email-summary-audit
description: Audits a page/email for content extractability, focusing on text-to-image ratios and missing image alt text to ensure AI summarizers do not drop the core message.
license: Apache-2.0
allowed-tools: [read_url, run_command]
---

# Email Summary & Extractability Audit (Discoverability: Appendix F)

## When to use
Use this skill to determine why an AI assistant or inbox summarizer (like Apple Mail Intelligence) might drop important content. It checks whether critical claims are locked inside images rather than semantic HTML text, and whether non-decorative images provide machine-readable fallbacks.

## Inputs
- `url` (string, required): The target website or email web-view URL.
- `html_content` (string, optional): Raw HTML for inspection.

## Procedure
1. **Text-to-Image Extractability**:
   - Parse the HTML to count `<img>` tags and extract all visible plain text.
   - If the HTML contains multiple images but very little plain text (< 50 words), flag this as an extractability failure.
2. **Missing Alt Text Fallback**:
   - Inspect all `<img>` tags for the `alt` attribute.
   - Flag if significant images completely lack `alt` text or have empty `alt` attributes, preventing AI summarizers from understanding the visual intent.
3. **Actionable Code Snippet Generation**:
   - Provide concrete suggestions for moving critical copy into plain HTML text and adding descriptive `alt` text.

## Output
Returns a JSON array of findings adhering to the standard schema:
```json
[
  {
    "id": "F-EMAIL-001",
    "title": "Low Plain-Text to Image Ratio",
    "severity": "high",
    "evidence": "The page contains 5 images but only 12 words of visible plain text. Core messages locked inside images lack this machine-readable text representation.",
    "suggested_action": {
      "summary": "Move critical claims, offers, and calls-to-action into plain HTML text outside of images.",
      "priority": "high"
    }
  }
]
```
