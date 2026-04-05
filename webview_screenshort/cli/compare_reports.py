from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from ..compare.reports import build_comparison_result_from_paths


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compare two persisted webview capture reports")
    parser.add_argument("left_report", help="Path to the first capture report")
    parser.add_argument("right_report", help="Path to the second capture report")
    parser.add_argument("--output-format", choices=["text", "json"], default="json")
    parser.add_argument("--diff-dir", help="Optional directory for generated diff images")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    left_path = Path(args.left_report).expanduser()
    right_path = Path(args.right_report).expanduser()
    diff_dir = Path(args.diff_dir).expanduser() if args.diff_dir else None
    result_payload = build_comparison_result_from_paths(left_path, right_path, diff_dir)

    if args.output_format == "json":
        print(json.dumps(result_payload, ensure_ascii=False))
        sys.exit(0 if result_payload.get("success") else 1)

    print(f"Comparison mode: {result_payload['comparison_mode']}")
    print(f"Pairs: {len(result_payload['pairs'])}")
    for pair in result_payload["pairs"]:
        print(f"- {pair['device']}: {pair['left']['image_path']} ↔ {pair['right']['image_path']}")
        print(f"  classification={pair['classification']} reason={pair['classification_reason']}")
        diff = pair.get("diff")
        if diff:
            print(f"  diff_pixels={diff['diff_pixels']} diff_ratio={diff['diff_ratio']:.6f}")
            if diff.get("bounding_box"):
                print(f"  bbox={diff['bounding_box']}")
            if diff.get("diff_image_path"):
                print(f"  diff_image={diff['diff_image_path']}")
    for warning in result_payload["warnings"]:
        print(f"⚠️ {warning}")
    if result_payload.get("error"):
        print(f"❌ {result_payload['error']}")
    sys.exit(0 if result_payload.get("success") else 1)


if __name__ == "__main__":
    main()
