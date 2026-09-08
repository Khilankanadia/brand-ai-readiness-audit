# Schema.org Specification Matrix for AI Answer Engines

AI assistants rely on explicit entities to distinguish brands and avoid confabulation.

| @type | Mandatory Properties | AI Quotation Benefit |
| :--- | :--- | :--- |
| **Organization** | `name`, `url`, `logo`, `description`, `sameAs` | Prevents entity confusion, links brand to verified knowledge bases. |
| **Product** | `name`, `description`, `offers`, `brand` | Directly grounds pricing, availability, and product capabilities. |
| **Offer** | `price`, `priceCurrency`, `availability` | Enables assistants to answer *"How much does X cost?"* deterministically. |
| **FAQPage** | `mainEntity` (List of `Question` + `Answer`) | Direct source for instant chat completions and cited Q&A snippets. |
| **SoftwareApplication** | `name`, `applicationCategory`, `operatingSystem` | Surfaces technical compatibility and category classification. |
| **Article** / **BlogPosting** | `headline`, `author`, `datePublished` | Ensures timestamped content is recognized as current and authoritative. |
