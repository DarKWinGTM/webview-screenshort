#!/usr/bin/env python3
"""
Persist a named compare session for expected/actual or before/after QA review.
"""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

SESSION_SCHEMA = "webview-screenshort.compare-session/v1"


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

    payload = {
        "session_schema": SESSION_SCHEMA,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "name": args.name,
        "left": {
            "label": args.left_label,
            "report_path": str(Path(args.left_report).expanduser()),
        },
        "right": {
            "label": args.right_label,
            "report_path": str(Path(args.right_report).expanduser()),
        },
        "comparison_json": str(comparison_path),
        "comparison": comparison,
    }

    with open(output_path, "w", encoding="utf-8") as file_obj:
        json.dump(payload, file_obj, ensure_ascii=False)

    print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
