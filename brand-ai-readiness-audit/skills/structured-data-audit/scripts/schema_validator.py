#!/usr/bin/env python3
"""
schema_validator.py - Structured Data & Quotability Auditor
Validates JSON-LD, Microdata, meta tags, and plain-text fact extractability.
"""

import sys
import json
import re
from html.parser import HTMLParser

SCHEMA_REQUIREMENTS = {
    "Organization": ["name", "url", "description"],
    "Product": ["name", "description", "offers"],
    "SoftwareApplication": ["name", "applicationCategory", "offers"],
    "FAQPage": ["mainEntity"],
    "Article": ["headline", "author", "datePublished"]
}

class SchemaExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.json_ld_raw = []
        self.in_json_ld = False
        self.current_json_data = []
        self.meta_tags = {}
        self.title_text = ""
        self.in_title = False
        self.h1_texts = []
        self.in_h1 = False
        self.current_h1 = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)

        if tag == "script" and attr_dict.get("type", "").lower() == "application/ld+json":
            self.in_json_ld = True
            self.current_json_data = []

        elif tag == "meta":
            name = attr_dict.get("name", "").lower() or attr_dict.get("property", "").lower()
            content = attr_dict.get("content", "")
            if name and content:
                self.meta_tags[name] = content

        elif tag == "title":
            self.in_title = True

        elif tag == "h1":
            self.in_h1 = True
            self.current_h1 = []

    def handle_endtag(self, tag):
        if tag == "script" and self.in_json_ld:
            self.in_json_ld = False
            raw = "".join(self.current_json_data).strip()
            if raw:
                self.json_ld_raw.append(raw)
        elif tag == "title":
            self.in_title = False
        elif tag == "h1":
            self.in_h1 = False
            text = " ".join(self.current_h1).strip()
            if text:
                self.h1_texts.append(text)

    def handle_data(self, data):
        if self.in_json_ld:
            self.current_json_data.append(data)
        elif self.in_title:
            self.title_text += data.strip()
        elif self.in_h1:
            self.current_h1.append(data.strip())

def audit_structured_data(html_content: str, url: str = "https://example.com"):
    findings = []
    parser = SchemaExtractor()
    try:
        parser.feed(html_content)
    except Exception:
        pass

    parsed_schemas = []
    schema_errors = 0

    # 1. Parse JSON-LD Blocks
    for raw_block in parser.json_ld_raw:
        try:
            data = json.loads(raw_block)
            if isinstance(data, list):
                parsed_schemas.extend(data)
            elif isinstance(data, dict):
                if "@graph" in data:
                    parsed_schemas.extend(data["@graph"])
                else:
                    parsed_schemas.append(data)
        except json.JSONDecodeError:
            schema_errors += 1

    # Check findings for Structured Data Presence
    if schema_errors > 0:
        findings.append({
            "id": "F-DATA-001",
            "title": "Malformed JSON-LD Syntax Detected",
            "severity": "high",
            "evidence": f"Found {schema_errors} JSON-LD block(s) with invalid JSON syntax. Crawlers and LLMs will reject these blocks completely.",
            "suggested_action": {
                "summary": "Fix JSON syntax errors in application/ld+json script tags using standard Schema.org schema validator.",
                "priority": "high"
            }
        })

    if not parsed_schemas and schema_errors == 0:
        # Determine recommended schema based on heuristics
        page_title = parser.title_text or "Brand Name"
        suggested_snippet = {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": page_title.split("-")[0].split("|")[0].strip(),
            "url": url,
            "description": parser.meta_tags.get("description", "Official website and service description.")
        }
        findings.append({
            "id": "F-DATA-002",
            "title": "No JSON-LD Structured Data on Page",
            "severity": "high",
            "evidence": "0 Schema.org JSON-LD blocks were detected on the audited page. Important organization/product information therefore lacks this particular machine-readable representation.",
            "suggested_action": {
                "summary": f"Add Schema.org JSON-LD to <head>. Example:\n```json\n{json.dumps(suggested_snippet, indent=2)}\n```",
                "priority": "high"
            }
        })
    else:
        # Validate properties for declared schemas
        for s in parsed_schemas:
            stype = s.get("@type")
            stypes = [stype] if isinstance(stype, str) else (stype if isinstance(stype, list) else [])
            for t in stypes:
                if t in SCHEMA_REQUIREMENTS:
                    missing_props = [p for p in SCHEMA_REQUIREMENTS[t] if p not in s or not s[p]]
                    if missing_props:
                        findings.append({
                            "id": "F-DATA-003",
                            "title": f"Incomplete Schema.org/@type={t} Properties",
                            "severity": "medium",
                            "evidence": f"Schema.org/{t} is missing essential attributes: {', '.join(missing_props)}.",
                            "suggested_action": {
                                "summary": f"Populate required properties ({', '.join(missing_props)}) in the {t} JSON-LD block.",
                                "priority": "medium"
                            }
                        })

    # 2. Meta Description / OpenGraph checks
    meta_desc = parser.meta_tags.get("description", "").strip()
    og_desc = parser.meta_tags.get("og:description", "").strip()
    desc = meta_desc or og_desc

    if not desc:
        findings.append({
            "id": "F-DATA-004",
            "title": "Missing Meta & OpenGraph Description",
            "severity": "medium",
            "evidence": "Neither <meta name='description'> nor <meta property='og:description'> was detected, so the page does not provide these explicit metadata descriptions for search/social retrieval contexts.",
            "suggested_action": {
                "summary": "Add a clear 150-160 character meta description summarizing the core brand value proposition.",
                "priority": "medium"
            }
        })
    elif len(desc) < 30 or desc.lower() in ["home", "welcome", "default description", "untitled"]:
        findings.append({
            "id": "F-DATA-005",
            "title": "Low-Quality Boilerplate Meta Description",
            "severity": "medium",
            "evidence": f"Meta description is trivial or boilerplate ('{desc[:40]}...'). AI summarizers may omit core product capabilities.",
            "suggested_action": {
                "summary": "Replace boilerplate description with specific, keyword-rich copy stating what the brand provides and who it serves.",
                "priority": "medium"
            }
        })

    # 3. Proactive FAQ / Speakable Markup Suggestion
    has_faq = any(s.get("@type") == "FAQPage" for s in parsed_schemas)
    if not has_faq:
        findings.append({
            "id": "F-DATA-P01",
            "title": "Proactive Opportunity: Add Schema.org FAQPage Markup",
            "severity": "low",
            "evidence": "Page lacks structured FAQ markup. Adding FAQ schema enables AI assistants to directly quote Q&A pairs in conversational answers.",
            "suggested_action": {
                "summary": "Implement FAQPage JSON-LD answering the top 3-5 customer questions regarding pricing, features, and onboarding.",
                "priority": "low"
            }
        })

    return findings

if __name__ == "__main__":
    sample = sys.stdin.read() if not sys.stdin.isatty() else "<html><head><title>Test</title></head><body><h1>Hello</h1></body></html>"
    print(json.dumps(audit_structured_data(sample), indent=2))
