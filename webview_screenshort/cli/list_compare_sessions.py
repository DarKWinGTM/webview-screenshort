from __future__ import annotations

import argparse
import json
from pathlib import Path

from ..compare.listings import list_compare_sessions_payload


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="List compare session artifacts")
    parser.add_argument("directory", help="Directory containing compare-session JSON files")
    parser.add_argument("--output-format", choices=["json", "text"], default="json")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    result = list_compare_sessions_payload(Path(args.directory))
    if args.output_format == "json":
        print(json.dumps(result, ensure_ascii=False))
        return
    print(f"count={result['count']}")
    for session in result["sessions"]:
        print(f"- {session['name']} ({session['left_label']} -> {session['right_label']}) [{session['comparison_mode']}] {session['path']}")


if __name__ == "__main__":
    main()
