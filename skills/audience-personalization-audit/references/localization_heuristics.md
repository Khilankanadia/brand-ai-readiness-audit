# Audience Personalization & Localization Heuristics

> **Appendix E Reference Guide — Adobe University Hackathon 2026**

## Overview
AI search assistants (e.g. ChatGPT, Claude, Perplexity) personalize answers based on user location, language, and implicit demographic context. Without explicit language and regional targeting tags, AI models may mix up regional product offerings, return wrong currencies, or serve non-localized copy.

## Key Inspection Rules

### 1. HTML Root `lang` Attribute
- **Requirement**: The root `<html>` tag must declare an ISO 639-1 language code (e.g. `<html lang="en">` or `<html lang="fr-CA">`).
- **Impact**: Without `lang`, natural language processing models must infer the document language heuristically, increasing error rates on bilingual or code-mixed pages.

### 2. Explicit `hreflang` Regional Targeting
- **Requirement**: Multi-regional or international sites must provide `<link rel="alternate" hreflang="...">` tags in the `<head>`.
- **Example**:
  ```html
  <link rel="alternate" hreflang="en-us" href="https://example.com/us/" />
  <link rel="alternate" hreflang="en-gb" href="https://example.com/uk/" />
  <link rel="alternate" hreflang="x-default" href="https://example.com/" />
  ```

### 3. OpenGraph Regional Locale (`og:locale`)
- **Requirement**: Declare `<meta property="og:locale" content="en_US">` alongside alternate locales (`og:locale:alternate`).
- **Impact**: Grounding OpenGraph metadata ensures conversational AI assistants route social citation cards to the correct locale.
