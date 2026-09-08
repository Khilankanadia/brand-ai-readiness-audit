# Deterministic Severity Scoring Rubric & Confidence Rules

This reference defines the deterministic classification of findings across all audit skills to guarantee consistency and minimize false positives.

## Severity Levels

| Severity | Definition & Impact | Example Defect |
| :--- | :--- | :--- |
| **`critical`** | Complete AI Invisibility / Unreachability. Crawlers or assistants cannot access or parse core page substance. | Server returns blank HTML due to pure client-side SPA rendering; `noindex` tag present. |
| **`high`** | Severe Extractability Failure. Crucial facts (pricing, product type, business entity) cannot be grounded with confidence. | Core pricing locked exclusively inside JS scripts; no Schema.org JSON-LD; AI bot explicitly blocked. |
| **`medium`** | Structural Weakness or Grounding Degradation. Information exists but requires heuristic parsing, or entity lacks cross-web anchors. | Missing `sameAs` entity links; outdated copyright year ($> 2$ years); overcrowded navigation menu ($> 12$ links). |
| **`low`** | Proactive Optimization Opportunity. No explicit defect exists, but implementing modern AI protocols will boost visibility and citations. | Missing `/llms.txt`; adding `FAQPage` schema; adding sticky trial CTA. |

## Multi-Signal Confidence Suppression Rules
1. **Plain-Text Grounding Suppression**: If Schema.org markup is missing but the company name and value proposition are clearly stated in semantic `<h1>` and `<p>` tags, severity is capped at `high` and does not escalate to `critical`.
2. **Deterministic Thresholds**: All thresholds (word counts $< 60$, nav links $> 12$, copyright gap $\ge 2$ years) are strict constants, avoiding non-deterministic grading variance.
