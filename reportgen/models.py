from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Screenshot:
    caption: str
    path: str


@dataclass
class Finding:
    id: str
    category: str
    severity: str   # Critical | High | Medium | Low
    effort: str     # Low | Medium | High
    title: str
    what_we_found: str
    why_it_matters: str
    recommendation: str
    evidence: List[str] = field(default_factory=list)


@dataclass
class ReportMeta:
    title: str
    client_name: str
    site_name: str
    site_url: str
    review_date: str
    reviewer_name: str
    reviewer_brand: str


@dataclass
class Summary:
    executive_summary: str
    top_priorities: List[str] = field(default_factory=list)


@dataclass
class NextSteps:
    proposed_plan: List[str] = field(default_factory=list)
    optional_addons: List[str] = field(default_factory=list)


@dataclass
class Appendix:
    screenshots: List[Screenshot] = field(default_factory=list)


@dataclass
class WebsiteReviewReport:
    report: ReportMeta
    summary: Summary
    highlights: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    findings: List[Finding] = field(default_factory=list)
    next_steps: Optional[NextSteps] = None
    appendix: Optional[Appendix] = None
