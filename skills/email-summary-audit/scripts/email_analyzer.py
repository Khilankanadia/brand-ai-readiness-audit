#!/usr/bin/env python3
import re
from html.parser import HTMLParser
from typing import List, Dict, Any

class EmailContentExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_content = []
        self.images = []
        self.in_script_or_style = False

    def handle_starttag(self, tag, attrs):
        if tag in ["script", "style", "noscript"]:
            self.in_script_or_style = True
        elif tag == "img":
            attr_dict = dict(attrs)
            self.images.append({
                "src": attr_dict.get("src", ""),
                "alt": attr_dict.get("alt", None)
            })

    def handle_endtag(self, tag):
        if tag in ["script", "style", "noscript"]:
            self.in_script_or_style = False

    def handle_data(self, data):
        if not self.in_script_or_style:
            stripped = data.strip()
            if stripped:
                self.text_content.append(stripped)

def audit_email_summary(html_content: str, url: str) -> List[Dict[str, Any]]:
    findings = []
    
    if not html_content:
        return findings

    parser = EmailContentExtractor()
    try:
        parser.feed(html_content)
    except Exception:
        pass

    full_text = " ".join(parser.text_content)
    word_count = len(re.findall(r'\b\w+\b', full_text))
    image_count = len(parser.images)

    # Check 1: Text to Image Ratio (F-EMAIL-001)
    if image_count > 0 and word_count < 50:
        findings.append({
            "id": "F-EMAIL-001",
            "title": "Low Plain-Text to Image Ratio",
            "severity": "high",
            "evidence": f"The page contains {image_count} images but only {word_count} words of visible plain text. Core messages locked inside images lack this machine-readable text representation.",
            "suggested_action": {
                "summary": "Move critical claims, offers, and calls-to-action into plain HTML text outside of images.",
                "priority": "high"
            }
        })

    # Check 2: Missing Image Alt Text (F-EMAIL-002)
    images_missing_alt = [img for img in parser.images if img["alt"] is None or img["alt"].strip() == ""]
    
    if image_count > 0 and len(images_missing_alt) > 0:
        # Only flag if a significant portion of images are missing alt text, or if there's very little text anyway.
        # For simplicity, if any image is missing alt text and it might be an important email/page
        findings.append({
            "id": "F-EMAIL-002",
            "title": "Missing Image Alt Text Fallbacks",
            "severity": "medium",
            "evidence": f"{len(images_missing_alt)} out of {image_count} `<img>` elements lack descriptive `alt` attributes. The page therefore fails to provide a machine-readable text fallback for this visual content.",
            "suggested_action": {
                "summary": "Add comprehensive, descriptive `alt` text to all non-decorative images carrying key brand messages.",
                "priority": "medium"
            }
        })

    return findings
