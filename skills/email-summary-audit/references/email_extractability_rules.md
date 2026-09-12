# Email & Content Summary Extractability Rules

> **Appendix F Reference Guide — Adobe University Hackathon 2026**

## Overview
AI inbox summarizers (such as Apple Intelligence Mail summaries) and web content summarizers build summaries from readable plain text. When critical message substance is locked inside images or buried in low-value disclaimer filler, the summary fails to extract the core brand proposition.

## Key Inspection Rules

### 1. Plain-Text to Image Ratio
- **Rule**: Pages/emails containing images MUST maintain a minimum text-to-image ratio (> 50 words of visible text per key promotional image).
- **Risk**: Image-heavy marketing layouts with under 50 words of plain text result in blank or truncated AI summaries.

### 2. Descriptive Alt Text Fallbacks
- **Rule**: All `<img>` tags must supply descriptive, factual `alt` attributes.
- **Requirement**: Alt text must state the actual offer, product name, or data shown in the graphic (e.g. `alt="50% off all enterprise plans through Sept 30"` rather than `alt="banner.jpg"` or empty `alt=""`).

### 3. Core Substance vs Low-Value Filler
- **Rule**: Core promotional value propositions should appear above low-value legal disclaimers or footer navigation.
