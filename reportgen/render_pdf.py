from __future__ import annotations

from collections import Counter
from pathlib import Path

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from reportgen.models import WebsiteReviewReport


SEVERITY_ORDER = ["Critical", "High", "Medium", "Low"]


def _severity_counts(report: WebsiteReviewReport) -> dict[str, int]:
    counts = Counter(f.severity for f in report.findings)
    return {s: counts.get(s, 0) for s in SEVERITY_ORDER}


def render_pdf(report: WebsiteReviewReport, out_path: str | Path) -> Path:
    out_path = Path(out_path)
    c = canvas.Canvas(str(out_path), pagesize=LETTER)
    width, height = LETTER

    margin = 0.75 * inch
    y = height - margin

    # ---- Cover-ish header ----
    c.setFont("Helvetica-Bold", 18)
    c.drawString(margin, y, report.report.title)
    y -= 0.35 * inch

    c.setFont("Helvetica", 11)
    c.drawString(margin, y, f"Client: {report.report.client_name}")
    y -= 0.20 * inch
    c.drawString(margin, y, f"Website: {report.report.site_name} ({report.report.site_url})")
    y -= 0.20 * inch
    c.drawString(margin, y, f"Review date: {report.report.review_date}")
    y -= 0.20 * inch
    c.drawString(margin, y, f"Reviewer: {report.report.reviewer_name} — {report.report.reviewer_brand}")
    y -= 0.35 * inch

    # ---- Summary ----
    c.setFont("Helvetica-Bold", 13)
    c.drawString(margin, y, "Executive Summary")
    y -= 0.22 * inch

    c.setFont("Helvetica", 11)
    y = _draw_wrapped_text(c, report.summary.executive_summary, margin, y, width - 2 * margin, leading=14)
    y -= 0.25 * inch

    # ---- Severity counts ----
    counts = _severity_counts(report)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Findings Overview")
    y -= 0.22 * inch
    c.setFont("Helvetica", 11)
    c.drawString(margin, y, " • ".join([f"{k}: {v}" for k, v in counts.items()]))
    y -= 0.30 * inch

    # ---- Top priorities ----
    c.setFont("Helvetica-Bold", 13)
    c.drawString(margin, y, "Top Priorities")
    y -= 0.22 * inch
    c.setFont("Helvetica", 11)
    for i, p in enumerate(report.summary.top_priorities[:3], start=1):
        y = _draw_wrapped_text(c, f"{i}. {p}", margin, y, width - 2 * margin, leading=14)
        y -= 0.08 * inch

    # New page for findings
    c.showPage()
    y = height - margin

    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "Findings")
    y -= 0.30 * inch

    for f in report.findings:
        # Page break if needed
        if y < 2.0 * inch:
            c.showPage()
            y = height - margin

        c.setFont("Helvetica-Bold", 12)
        c.drawString(margin, y, f"{f.id} — {f.title}")
        y -= 0.18 * inch

        c.setFont("Helvetica", 10)
        c.drawString(margin, y, f"Category: {f.category}   |   Severity: {f.severity}   |   Effort: {f.effort}")
        y -= 0.20 * inch

        c.setFont("Helvetica-Bold", 10)
        c.drawString(margin, y, "What we found:")
        y -= 0.14 * inch
        c.setFont("Helvetica", 10)
        y = _draw_wrapped_text(c, f.what_we_found, margin, y, width - 2 * margin, leading=12)
        y -= 0.14 * inch

        c.setFont("Helvetica-Bold", 10)
        c.drawString(margin, y, "Why it matters:")
        y -= 0.14 * inch
        c.setFont("Helvetica", 10)
        y = _draw_wrapped_text(c, f.why_it_matters, margin, y, width - 2 * margin, leading=12)
        y -= 0.14 * inch

        c.setFont("Helvetica-Bold", 10)
        c.drawString(margin, y, "Recommendation:")
        y -= 0.14 * inch
        c.setFont("Helvetica", 10)
        y = _draw_wrapped_text(c, f.recommendation, margin, y, width - 2 * margin, leading=12)
        y -= 0.14 * inch

        if f.evidence:
            c.setFont("Helvetica-Bold", 10)
            c.drawString(margin, y, "Evidence:")
            y -= 0.14 * inch
            c.setFont("Helvetica", 10)
            for ev in f.evidence:
                y = _draw_wrapped_text(c, f"• {ev}", margin + 10, y, width - 2 * margin - 10, leading=12)
                y -= 0.06 * inch

        y -= 0.20 * inch  # spacing between findings

    c.save()
    return out_path


def _draw_wrapped_text(c: canvas.Canvas, text: str, x: float, y: float, max_width: float, leading: int = 14) -> float:
    """
    Draw text with simple word-wrapping. Returns the new y position after drawing.
    """
    # Basic wrap: split into words and build lines that fit max_width.
    words = (text or "").split()
    if not words:
        return y

    line = ""
    for w in words:
        test = (line + " " + w).strip()
        if c.stringWidth(test, c._fontname, c._fontsize) <= max_width:
            line = test
        else:
            c.drawString(x, y, line)
            y -= leading
            line = w

    if line:
        c.drawString(x, y, line)
        y -= leading

    return y
