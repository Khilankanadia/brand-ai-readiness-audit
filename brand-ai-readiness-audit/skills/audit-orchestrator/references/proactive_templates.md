# Proactive Recommendations Library

The rubric explicitly rewards proactive improvements that strengthen discoverability or engagement even where no defect was found.

## 1. `/llms.txt` Standard Template
Provide AI agents with structured, high-density documentation at domain root:
```markdown
# [Brand Name]

> [One sentence brand mission & core capability]

## Documentation
- [API Reference](https://example.com/docs/api): Complete OpenAPI 3.0 specification
- [Pricing](https://example.com/pricing): Breakdown of plans and quotas

## Key Products
- [Product Alpha](https://example.com/products/alpha): AI-powered workflow optimizer
```

## 2. FAQPage Schema for Direct Answer Grounding
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How does [Product] integrate with existing workflows?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Product] provides native webhooks and REST APIs supported in Python, JS, and Go."
      }
    }
  ]
}
```

## 3. High-Intent Quick-Action CTA Design
- Above-the-fold button with explicit action verb: `"Deploy Instant Sandbox"` or `"Read Interactive Docs"`.
