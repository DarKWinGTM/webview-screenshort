#!/usr/bin/env python3
"""
Persist a named compare session for expected/actual or before/after QA review.
"""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

SESSION_SCHEMA = "webview-screenshort.compare-session/v1"


def build_compare_session_payload(
    *,
    name: str,
    left_report: Path,
    right_report: Path,
    left_label: str,
    right_label: str,
    comparison_json_path: Path,
    comparison: dict,
) -> dict:
    return {
        "session_schema": SESSION_SCHEMA,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "name": name,
        "left": {
            "label": left_label,
            "report_path": str(left_report.expanduser()),
        },
        "right": {
            "label": right_label,
            "report_path": str(right_report.expanduser()),
        },
        "comparison_json": str(comparison_json_path),
        "comparison": comparison,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a named compare session artifact")
    parser.add_argument("--name", required=True, help="Human-friendly session name")
    parser.add_argument("--left-report", required=True)
    parser.add_argument("--right-report", required=True)
    parser.add_argument("--left-label", default="before")
    parser.add_argument("--right-label", default="after")
    parser.add_argument("--comparison-json", required=True, help="Path to compare_reports JSON output")
    parser.add_argument("--output", required=True, help="Output session JSON path")
    args = parser.parse_args()

    comparison_path = Path(args.comparison_json).expanduser()
    output_path = Path(args.output).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(comparison_path, "r", encoding="utf-8") as file_obj:
        comparison = json.load(file_obj)

    payload = build_compare_session_payload(
        name=args.name,
        left_report=Path(args.left_report),
        right_report=Path(args.right_report),
        left_label=args.left_label,
        right_label=args.right_label,
        comparison_json_path=comparison_path,
        comparison=comparison,
    )

    with open(output_path, "w", encoding="utf-8") as file_obj:
        json.dump(payload, file_obj, ensure_ascii=False)

    print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
