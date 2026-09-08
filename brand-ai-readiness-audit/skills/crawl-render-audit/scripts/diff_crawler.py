#!/usr/bin/env python3
"""
diff_crawler.py - Crawlability & JS-Render Difference Auditor
Inspects raw HTML vs rendered structures, robots.txt AI bot policies, llms.txt, and trapped text.
"""

import sys
import re
import urllib.parse
from html.parser import HTMLParser

AI_BOTS = [
    "GPTBot",
    "ClaudeBot",
    "PerplexityBot",
    "Google-Extended",
    "Amazonbot",
    "Bytespider",
    "cohere-ai",
    "Applebot-Extended"
]

class HTMLContentExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_chunks = []
        self.images_without_alt = 0
        self.total_images = 0
        self.canvas_count = 0
        self.has_empty_spa_root = False
        self.scripts_count = 0
        self.meta_robots = []
        self._current_tag = None

    def handle_starttag(self, tag, attrs):
        self._current_tag = tag
        attr_dict = dict(attrs)

        if tag == "img":
            self.total_images += 1
            alt = attr_dict.get("alt", "").strip()
            if not alt:
                self.images_without_alt += 1

        elif tag == "canvas":
            self.canvas_count += 1

        elif tag == "meta":
            name = attr_dict.get("name", "").lower()
            if name in ["robots", "googlebot", "bingbot"]:
                content = attr_dict.get("content", "")
                self.meta_robots.append((name, content))

        elif tag == "div":
            div_id = attr_dict.get("id", "").lower()
            if div_id in ["root", "app", "__next", "__nuxt"]:
                # Checked later if content is injected
                pass

        elif tag == "script":
            self.scripts_count += 1

    def handle_data(self, data):
        cleaned = data.strip()
        if cleaned and self._current_tag not in ["script", "style", "noscript"]:
            self.text_chunks.append(cleaned)

def audit_crawl_render(html_content: str, robots_content: str = "", url: str = "https://example.com"):
    findings = []
    
    # 1. Parse HTML
    parser = HTMLContentExtractor()
    try:
        parser.feed(html_content)
    except Exception:
        pass

    raw_text = " ".join(parser.text_chunks)
    word_count = len(raw_text.split())

    # 2. Check for SPA / JS-Only Rendering Gaps
    spa_patterns = [
        r'<div\s+id=["\'](?:root|app|__next|__nuxt)["\']\s*>\s*</div>',
        r'window\.__INITIAL_STATE__\s*=',
        r'<noscript>.*?(?:enable\s+javascript|requires\s+javascript).*?</noscript>'
    ]
    is_spa_empty = False
    for pat in spa_patterns:
        if re.search(pat, html_content, re.IGNORECASE | re.DOTALL):
            if word_count < 60:
                is_spa_empty = True
                break

    # Look for pricing / core product data in script tags but absent from raw rendered text
    js_locked_pricing = False
    price_in_scripts = re.search(r'["\'](?:price|amount|cost)["\']\s*:\s*["\']?\$?\d+(?:\.\d{2})?["\']?', html_content, re.IGNORECASE)
    price_in_text = re.search(r'\$\d+(?:\.\d{2})?', raw_text)
    if price_in_scripts and not price_in_text:
        js_locked_pricing = True

    if is_spa_empty:
        findings.append({
            "id": "F-CRAWL-001",
            "title": "Client-Side Render Gap: Core Content Empty in Raw HTML",
            "severity": "critical",
            "evidence": f"Raw HTML contains only {word_count} visible words. Page relies on client-side JS hydration (<div id='root'>), leaving search and AI crawlers with near-blank snapshots.",
            "suggested_action": {
                "summary": "Implement Server-Side Rendering (SSR) or Static Site Generation (SSG) so full semantic HTML is delivered on initial GET requests.",
                "priority": "critical"
            }
        })
    elif js_locked_pricing:
        findings.append({
            "id": "F-CRAWL-002",
            "title": "Critical Value/Pricing Data Locked in Client JavaScript",
            "severity": "high",
            "evidence": "Pricing or feature definitions detected inside client script bundles/data objects, but not present in server-rendered plain text.",
            "suggested_action": {
                "summary": "Render key product, pricing, and feature specifications directly in server-rendered HTML markup with accompanying Schema.org/Offer markup.",
                "priority": "high"
            }
        })

    # 3. Check Meta Robots restrictions
    for name, content in parser.meta_robots:
        if "noindex" in content.lower():
            findings.append({
                "id": "F-CRAWL-003",
                "title": "Meta Robots Restricts Crawler Indexing",
                "severity": "critical",
                "evidence": f"Found <meta name='{name}' content='{content}'> preventing automated indexing and citation.",
                "suggested_action": {
                    "summary": "Remove 'noindex' directive from public brand and documentation pages.",
                    "priority": "critical"
                }
            })

    # 4. Robots.txt Analysis for AI Bots
    if robots_content:
        disallowed_ai_bots = []
        # Parse blocks by User-agent
        blocks = re.split(r'(?i)User-agent:\s*', robots_content)
        for block in blocks:
            if not block.strip():
                continue
            lines = [l.strip() for l in block.splitlines() if l.strip() and not l.strip().startswith('#')]
            if not lines:
                continue
            ua = lines[0]
            matched_bot = next((b for b in AI_BOTS if b.lower() == ua.lower() or b.lower() in ua.lower()), None)
            if matched_bot:
                # Check directives under this bot
                has_root_disallow = False
                has_root_allow = False
                for line in lines[1:]:
                    if re.match(r'(?i)Disallow:\s*(?:/\s*$|/\*|\s*$)', line):
                        # Disallow: / or Disallow: /*
                        if not re.match(r'(?i)Disallow:\s*$', line): # empty disallow means allowed
                            has_root_disallow = True
                    elif re.match(r'(?i)Allow:\s*(?:/\s*$|/\*)', line):
                        has_root_allow = True
                
                if has_root_disallow and not has_root_allow:
                    disallowed_ai_bots.append(matched_bot)

        if disallowed_ai_bots:
            findings.append({
                "id": "F-CRAWL-004",
                "title": "AI Assistant Crawlers Explicitly Blocked in robots.txt",
                "severity": "high",
                "evidence": f"robots.txt explicitly disallows AI assistant crawlers ({', '.join(disallowed_ai_bots)}) from root access. AI assistants will fail to fetch live content during real-time retrieval.",
                "suggested_action": {
                    "summary": f"Grant selective crawl access in robots.txt to AI search agents ({', '.join(disallowed_ai_bots[:3])}) for public content directories.",
                    "priority": "high"
                }
            })

    # 5. Non-text trapped facts
    if parser.total_images > 0 and (parser.images_without_alt / parser.total_images) > 0.4:
        findings.append({
            "id": "F-CRAWL-005",
            "title": "High Ratio of Images Missing Text Alternatives (Alt Tags)",
            "severity": "medium",
            "evidence": f"{parser.images_without_alt} out of {parser.total_images} images ({(parser.images_without_alt/parser.total_images)*100:.1f}%) lack alt attributes, locking visual facts from non-multimodal crawlers.",
            "suggested_action": {
                "summary": "Provide descriptive, factual alt text for all infographic, product, and diagram images.",
                "priority": "medium"
            }
        })

    # 6. Proactive llms.txt Suggestion
    # In live mode or audit mode, check/suggest llms.txt
    if "llms.txt" not in html_content.lower():
        findings.append({
            "id": "F-CRAWL-P01",
            "title": "Proactive Opportunity: Publish /llms.txt for AI Search Engines",
            "severity": "low",
            "evidence": "Website has not published a standardized /llms.txt file describing high-level architecture and concise documentation for LLM ingestion.",
            "suggested_action": {
                "summary": "Create and host a markdown /llms.txt file at domain root outlining the brand's core mission, product catalog, and direct API/documentation links.",
                "priority": "low"
            }
        })

    return findings

if __name__ == "__main__":
    import json
    # Simple CLI test interface
    sample_html = sys.stdin.read() if not sys.stdin.isatty() else "<html><body><h1>Sample</h1></body></html>"
    results = audit_crawl_render(sample_html)
    print(json.dumps(results, indent=2))
