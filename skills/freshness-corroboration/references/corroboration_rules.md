# Entity Corroboration & Freshness Heuristics

AI models require cross-web grounding to avoid halluncinating details about a brand.

## Key Disambiguation Anchors
1. **`sameAs` in Schema.org**: Links the brand’s domain to external authoritative knowledge hubs:
   - `https://www.wikidata.org/wiki/Q...` (Highest entity resolution weight in LLM pre-training & retrieval)
   - `https://en.wikipedia.org/wiki/...`
   - `https://www.crunchbase.com/organization/...`
   - `https://github.com/...` / `https://www.linkedin.com/company/...`
2. **Canonical Tag Consistency**:
   - Every primary page should define `<link rel="canonical" href="...">`.
3. **Temporal Freshness Indicators**:
   - Current footer copyright year within 1 year of audit time.
   - `datePublished` and `dateModified` Schema markup on articles/documentation.
