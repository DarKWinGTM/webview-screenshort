#!/usr/bin/env python3
"""
List and summarize saved reference bundle artifacts.
"""

import argparse
import json
from pathlib import Path

BUNDLE_SCHEMA = "webview-screenshort.reference-bundle/v1"


def load_bundle(path: Path):
    with open(path, "r", encoding="utf-8") as file_obj:
        payload = json.load(file_obj)
    if payload.get("bundle_schema") != BUNDLE_SCHEMA:
        return None
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="List reference bundle artifacts")
    parser.add_argument("directory", help="Directory containing reference-bundle JSON files")
    parser.add_argument("--output-format", choices=["json", "text"], default="json")
    args = parser.parse_args()

    base_dir = Path(args.directory).expanduser()
    bundles = []
    for path in sorted(base_dir.glob("*.json")):
        payload = load_bundle(path)
        if not payload:
            continue
        session = payload.get("session", {})
        comparison = session.get("comparison", {})
        bundles.append(
            {
                "path": str(path),
                "name": payload.get("name"),
                "generated_at": payload.get("generated_at"),
                "reference_label": payload.get("reference_label"),
                "session_name": session.get("name"),
                "comparison_mode": comparison.get("comparison_mode"),
                "pair_count": len(comparison.get("pairs", [])),
                "success": comparison.get("success"),
            }
        )

    result = {
        "bundle_schema": BUNDLE_SCHEMA,
        "directory": str(base_dir),
        "count": len(bundles),
        "bundles": bundles,
    }

    if args.output_format == "json":
        print(json.dumps(result, ensure_ascii=False))
        return

    print(f"count={result['count']}")
    for bundle in bundles:
        print(f"- {bundle['name']} [{bundle['reference_label']}] ({bundle['comparison_mode']}) {bundle['path']}")


if __name__ == "__main__":
    main()
