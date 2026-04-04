#!/usr/bin/env python3
"""
List built-in QA policy presets for webview-screenshort.
"""

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="List built-in QA policy presets")
    parser.add_argument("--output-format", choices=["json", "text"], default="json")
    args = parser.parse_args()

    base_dir = Path(__file__).parent / "support" / "policies"
    if not base_dir.exists():
        raise SystemExit(f"Policy preset directory not found: {base_dir}")

    presets = []
    for path in sorted(base_dir.glob("*.json")):
        with open(path, "r", encoding="utf-8") as file_obj:
            payload = json.load(file_obj)
        presets.append(
            {
                "name": path.stem,
                "path": str(path),
                "policy": payload,
            }
        )

    if not presets:
        raise SystemExit(f"No built-in policy presets found in: {base_dir}")

    result = {
        "policy_preset_count": len(presets),
        "directory": str(base_dir),
        "presets": presets,
    }

    if args.output_format == "json":
        print(json.dumps(result, ensure_ascii=False))
        return

    print(f"count={result['policy_preset_count']}")
    for preset in presets:
        print(f"- {preset['name']} -> {preset['path']}")


if __name__ == "__main__":
    main()
