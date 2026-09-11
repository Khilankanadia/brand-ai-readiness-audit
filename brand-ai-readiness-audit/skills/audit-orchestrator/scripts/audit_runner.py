#!/usr/bin/env python3
"""
audit_runner.py - Main Orchestrator CLI
Coordinates execution of all 4 domain skills against a target URL or local HTML fixture.
"""

import sys
import os
import json
import argparse
import urllib.request
import urllib.error
import urllib.parse

# Ensure child skill scripts are importable
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# CURRENT_DIR is skills/audit-orchestrator/scripts
# .. is skills/audit-orchestrator
# ../.. is skills
# ../../.. is marketplace root
MARKETPLACE_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".."))

sys.path.insert(0, os.path.join(MARKETPLACE_ROOT, "skills", "crawl-render-audit", "scripts"))
sys.path.insert(0, os.path.join(MARKETPLACE_ROOT, "skills", "structured-data-audit", "scripts"))
sys.path.insert(0, os.path.join(MARKETPLACE_ROOT, "skills", "freshness-corroboration", "scripts"))
sys.path.insert(0, os.path.join(MARKETPLACE_ROOT, "skills", "engagement-audit", "scripts"))
sys.path.insert(0, os.path.join(MARKETPLACE_ROOT, "skills", "audience-personalization-audit", "scripts"))
sys.path.insert(0, os.path.join(MARKETPLACE_ROOT, "skills", "email-summary-audit", "scripts"))
sys.path.insert(0, CURRENT_DIR)

from diff_crawler import audit_crawl_render
from schema_validator import audit_structured_data
from entity_resolver import audit_freshness_entity
from orientation_analyzer import audit_engagement_friction
from personalization_analyzer import audit_audience_personalization
from email_analyzer import audit_email_summary
from compose_report import compose_final_report

def fetch_live_site(url: str, timeout: int = 10):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 BrandAIAuditor/1.0"
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            html = response.read().decode("utf-8", errors="replace")
    except Exception as e:
        html = f"<html><body><!-- Failed to fetch {url}: {str(e)} --></body></html>"

    # Try fetching robots.txt
    parsed = urllib.parse.urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    robots_content = ""
    try:
        r_req = urllib.request.Request(robots_url, headers=headers)
        with urllib.request.urlopen(r_req, timeout=5) as r_res:
            robots_content = r_res.read().decode("utf-8", errors="replace")
    except Exception:
        robots_content = ""

    return html, robots_content

def run_marketplace_audit(target: str, html_override: str = None, robots_override: str = None) -> dict:
    if html_override is not None:
        html_content = html_override
        robots_content = robots_override or ""
        site_name = target.replace("http://", "").replace("https://", "").split("/")[0] or target
    else:
        if not target.startswith("http://") and not target.startswith("https://"):
            target = "https://" + target
        site_name = urllib.parse.urlparse(target).netloc or target
        html_content, robots_content = fetch_live_site(target)

    all_raw_findings = []

    # 1. Crawl & Render Audit
    crawl_findings = audit_crawl_render(html_content, robots_content=robots_content, url=target)
    all_raw_findings.extend(crawl_findings)

    # 2. Structured Data Audit
    schema_findings = audit_structured_data(html_content, url=target)
    all_raw_findings.extend(schema_findings)

    # 3. Freshness & Entity Corroboration Audit
    entity_findings = audit_freshness_entity(html_content, url=target)
    all_raw_findings.extend(entity_findings)

    # 4. Engagement & Friction Audit
    engagement_findings = audit_engagement_friction(html_content, url=target)
    all_raw_findings.extend(engagement_findings)

    # 5. Audience Personalization & Prior Context Audit
    personalization_findings = audit_audience_personalization(html_content, url=target)
    all_raw_findings.extend(personalization_findings)

    # 6. Email Summary & Extractability Audit
    email_findings = audit_email_summary(html_content, url=target)
    all_raw_findings.extend(email_findings)

    # 7. Compose and format into final standardized report schema
    final_report = compose_final_report(site=site_name, raw_findings=all_raw_findings)
    return final_report

def main():
    parser = argparse.ArgumentParser(description="Brand AI-Readiness Audit Orchestrator")
    parser.add_argument("target_pos", nargs="?", default=None, help="Target URL, domain, or path to local HTML file")
    parser.add_argument("--site", type=str, default=None, help="Target URL or domain to audit")
    parser.add_argument("--test-fixture", "--fixture", type=str, default=None, help="Path to local HTML fixture file for offline evaluation")
    parser.add_argument("--robots-fixture", type=str, default=None, help="Path to local robots.txt fixture file")
    parser.add_argument("--out", type=str, default=None, help="Output JSON file path (optional, defaults to stdout)")

    args = parser.parse_args()

    target = args.site or args.target_pos or "example.com"
    html_content = None
    robots_content = None

    # If target is a local file path that exists, automatically treat as test fixture
    if os.path.exists(target) and os.path.isfile(target):
        with open(target, "r", encoding="utf-8", errors="replace") as f:
            html_content = f.read()
        target = os.path.basename(target)
    elif args.test_fixture and os.path.exists(args.test_fixture):
        with open(args.test_fixture, "r", encoding="utf-8", errors="replace") as f:
            html_content = f.read()

    if args.robots_fixture and os.path.exists(args.robots_fixture):
        with open(args.robots_fixture, "r", encoding="utf-8", errors="replace") as f:
            robots_content = f.read()

    report = run_marketplace_audit(target=target, html_override=html_content, robots_override=robots_content)
    output_json = json.dumps(report, indent=2)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(output_json)
        print(f"Audit report saved to {args.out}")
    else:
        print(output_json)

if __name__ == "__main__":
    main()
