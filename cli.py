from __future__ import annotations

import argparse
from pathlib import Path

from reportgen.load import load_report
from reportgen.render_pdf import render_pdf


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a Website Review PDF report from JSON.")
    parser.add_argument("json_path", help="Path to the input JSON file (e.g., sample_review.json)")
    parser.add_argument("--out", default="website_review_report.pdf", help="Output PDF path")
    args = parser.parse_args()

    report = load_report(args.json_path)
    out_path = render_pdf(report, Path(args.out))
    print(f"✅ Generated: {out_path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
