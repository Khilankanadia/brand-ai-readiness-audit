#!/usr/bin/env python3
"""
orientation_analyzer.py - On-Site Engagement & Friction Auditor
Evaluates above-the-fold orientation, navigation cognitive load, breadcrumbs, and trust anchors.
"""

import sys
import json
import re
from html.parser import HTMLParser

class EngagementExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1_list = []
        self.in_h1 = False
        self.curr_h1 = []
        self.nav_links_count = 0
        self.in_nav = False
        self.has_breadcrumbs = False
        self.links = []
        self.curr_link_href = None
        self.curr_link_text = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag == "h1":
            self.in_h1 = True
            self.curr_h1 = []
        elif tag == "nav":
            self.in_nav = True
            aria_label = attr_dict.get("aria-label", "").lower()
            if "breadcrumb" in aria_label:
                self.has_breadcrumbs = True
        elif tag == "a":
            self.curr_link_href = attr_dict.get("href", "")
            self.curr_link_text = []
            if self.in_nav:
                self.nav_links_count += 1
            if "breadcrumb" in attr_dict.get("class", "").lower() or "breadcrumb" in attr_dict.get("rel", "").lower():
                self.has_breadcrumbs = True

    def handle_endtag(self, tag):
        if tag == "h1":
            self.in_h1 = False
            text = " ".join(self.curr_h1).strip()
            if text:
                self.h1_list.append(text)
        elif tag == "nav":
            self.in_nav = False
        elif tag == "a":
            text = " ".join(self.curr_link_text).strip()
            if self.curr_link_href:
                self.links.append((self.curr_link_href, text))

    def handle_data(self, data):
        if self.in_h1:
            self.curr_h1.append(data.strip())
        elif self.curr_link_href is not None:
            self.curr_link_text.append(data.strip())

def audit_engagement_friction(html_content: str, url: str = "https://example.com"):
    findings = []
    parser = EngagementExtractor()
    try:
        parser.feed(html_content)
    except Exception:
        pass

    # 1. Orientation / H1 Check
    if not parser.h1_list:
        findings.append({
            "id": "F-ENG-001",
            "title": "Missing Above-the-Fold H1 Value Proposition",
            "severity": "medium",
            "evidence": "No <h1> element was detected on the page. The page therefore lacks a conventional primary heading that explicitly identifies its main subject or purpose.",
            "suggested_action": {
                "summary": "Introduce a clear, prominent <h1> tag above the fold articulating what the product or organization does.",
                "priority": "medium"
            }
        })
    else:
        h1_text = parser.h1_list[0]
        vague_terms = ["welcome", "hello", "the future", "revolutionize", "home", "untitled"]
        if len(h1_text.split()) < 2 or any(h1_text.lower() == v for v in vague_terms):
            findings.append({
                "id": "F-ENG-002",
                "title": "Vague or Generic H1 Tagline",
                "severity": "medium",
                "evidence": f"Heading 1 is too brief or generic ('{h1_text}'), failing to convey clear product category or benefits to visitors.",
                "suggested_action": {
                    "summary": "Rewrite the primary <h1> into a descriptive statement (e.g. '[Product] is the [Category] for [Audience]').",
                    "priority": "medium"
                }
            })

    # 2. Navigation Complexity / Cognitive Load
    if parser.nav_links_count > 12:
        findings.append({
            "id": "F-ENG-003",
            "title": "Overcrowded Primary Navigation Menu",
            "severity": "medium",
            "evidence": f"Found {parser.nav_links_count} top-level navigation links in primary <nav>. Excess menu options increase cognitive friction and bounce rates.",
            "suggested_action": {
                "summary": "Streamline main navigation to 5-7 core priority categories and move secondary utility links into dropdowns or footer.",
                "priority": "medium"
            }
        })

    # 3. Trust & Contact Signal Verification
    all_links_str = " ".join([f"{href} {text}".lower() for href, text in parser.links])
    has_contact = any(k in all_links_str for k in ["contact", "support", "help", "mailto:"])
    has_about = any(k in all_links_str for k in ["about", "team", "story", "company"])

    if not has_contact and not has_about:
        findings.append({
            "id": "F-ENG-004",
            "title": "Absence of Transparent Trust & Contact Links",
            "severity": "medium",
            "evidence": "No discernible 'Contact Us', 'Support', or 'About' links found in navigation or footer. Lowers user conversion confidence.",
            "suggested_action": {
                "summary": "Place clear 'About Us' and 'Contact' links in the persistent header and footer navigation.",
                "priority": "medium"
            }
        })

    # 4. Proactive Engagement Enhancer: Quick-Start / Interactive CTA
    findings.append({
        "id": "F-ENG-P01",
        "title": "Proactive Opportunity: Add Sticky Interactive CTA / Quick Start",
        "severity": "low",
        "evidence": "Visitors arriving from AI citations seek immediate answers or interactive trial paths. A clear single primary CTA accelerates time-to-value.",
        "suggested_action": {
            "summary": "Add a prominent primary Call-to-Action button ('Get Started Free' or 'Try Live Demo') visible above the fold.",
            "priority": "low"
        }
    })

    return findings

if __name__ == "__main__":
    sample = sys.stdin.read() if not sys.stdin.isatty() else "<html><body><h1>Acme AI</h1><nav><a href='/'>Home</a></nav></body></html>"
    print(json.dumps(audit_engagement_friction(sample), indent=2))
