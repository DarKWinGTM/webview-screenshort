from __future__ import annotations

import argparse
import json
from pathlib import Path

from ..compare.sessions import build_compare_session_payload


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a named compare session artifact")
    parser.add_argument("--name", required=True, help="Human-friendly session name")
    parser.add_argument("--left-report", required=True)
    parser.add_argument("--right-report", required=True)
    parser.add_argument("--left-label", default="before")
    parser.add_argument("--right-label", default="after")
    parser.add_argument("--comparison-json", required=True, help="Path to compare_reports JSON output")
    parser.add_argument("--output", required=True, help="Output session JSON path")
    return parser


def main() -> None:
    args = build_parser().parse_args()
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
