from __future__ import annotations

import argparse
import json
from pathlib import Path

from ..references.bundles import apply_reference_bundle


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Apply a reference bundle to a current report")
    parser.add_argument("--bundle", required=True, help="Path to reference bundle JSON")
    parser.add_argument("--current-report", required=True, help="Path to current capture report")
    parser.add_argument("--comparison-json", required=True, help="Output path for compare_reports JSON")
    parser.add_argument("--session-output", required=True, help="Output path for compare-session JSON")
    parser.add_argument("--session-name", required=True, help="Name for the new compare session")
    parser.add_argument("--current-label", default="actual")
    parser.add_argument("--diff-dir", help="Optional diff image output directory for compare_reports")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    payload = apply_reference_bundle(
        bundle_path=Path(args.bundle).expanduser(),
        current_report_path=Path(args.current_report).expanduser(),
        comparison_json_path=Path(args.comparison_json).expanduser(),
        session_output_path=Path(args.session_output).expanduser(),
        session_name=args.session_name,
        current_label=args.current_label,
        diff_dir=Path(args.diff_dir).expanduser() if args.diff_dir else None,
    )
    print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
