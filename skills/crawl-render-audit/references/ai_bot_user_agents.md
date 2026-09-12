# AI Assistant Crawler User-Agents Reference

Modern AI assistants retrieve live citations and ground answers using dedicated search/crawler user-agents. Blocking these in `robots.txt` directly prevents AI apps from citing the brand.

| Bot Name | Operator | Primary Role | Default Behavior |
| :--- | :--- | :--- | :--- |
| **GPTBot** | OpenAI | Training data collection & direct ChatGPT search browsing | Respects standard robots.txt |
| **ClaudeBot** | Anthropic | Training & search retrieval for Claude | Respects standard robots.txt |
| **PerplexityBot** | Perplexity AI | Real-time live web indexing for answer grounding | Respects standard robots.txt |
| **Google-Extended** | Google | Gemini & Vertex AI data collection | Does not block Google Search, only AI use |
| **Amazonbot** | Amazon | Alexa & Amazon Q assistant retrieval | Respects standard robots.txt |
| **Bytespider** | ByteDance | Doubao / AI Assistant ingestion | High crawl rate; requires rate limiting |

## Recommended `robots.txt` Directive for Brands
```txt
User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /
```
