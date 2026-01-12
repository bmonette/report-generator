from __future__ import annotations

import json
from pathlib import Path

from reportgen.models import (
    Appendix,
    Finding,
    NextSteps,
    ReportMeta,
    Screenshot,
    Summary,
    WebsiteReviewReport,
)


def load_report(path: str | Path) -> WebsiteReviewReport:
    path = Path(path)
    data = json.loads(path.read_text(encoding="utf-8"))

    meta = ReportMeta(**data["report"])
    summary = Summary(**data["summary"])

    findings = [Finding(**f) for f in data.get("findings", [])]

    next_steps_data = data.get("next_steps")
    next_steps = NextSteps(**next_steps_data) if next_steps_data else None

    appendix_data = data.get("appendix")
    appendix = None
    if appendix_data and appendix_data.get("screenshots"):
        shots = [Screenshot(**s) for s in appendix_data["screenshots"]]
        appendix = Appendix(screenshots=shots)

    return WebsiteReviewReport(
        report=meta,
        summary=summary,
        highlights=data.get("highlights", []),
        risks=data.get("risks", []),
        findings=findings,
        next_steps=next_steps,
        appendix=appendix,
    )
