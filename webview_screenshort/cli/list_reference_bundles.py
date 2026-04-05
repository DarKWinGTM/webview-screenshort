from __future__ import annotations

import argparse
import json
from pathlib import Path

from ..references.bundles import list_reference_bundles_payload


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="List reference bundle artifacts")
    parser.add_argument("directory", help="Directory containing reference-bundle JSON files")
    parser.add_argument("--output-format", choices=["json", "text"], default="json")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    result = list_reference_bundles_payload(Path(args.directory))
    if args.output_format == "json":
        print(json.dumps(result, ensure_ascii=False))
        return
    print(f"count={result['count']}")
    for bundle in result["bundles"]:
        print(f"- {bundle['name']} [{bundle['reference_label']}] ({bundle['comparison_mode']}) {bundle['path']}")


if __name__ == "__main__":
    main()
