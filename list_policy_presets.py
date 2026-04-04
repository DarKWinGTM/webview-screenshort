#!/usr/bin/env python3
"""
List built-in QA policy presets for webview-screenshort.
"""

import argparse
import json

from policy_presets import list_policy_preset_records, policy_preset_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="List built-in QA policy presets")
    parser.add_argument("--output-format", choices=["json", "text"], default="json")
    args = parser.parse_args()

    records = list_policy_preset_records()
    result = {
        "policy_preset_count": len(records),
        "directory": str(policy_preset_dir()),
        "presets": records,
    }

    if args.output_format == "json":
        print(json.dumps(result, ensure_ascii=False))
        return

    print(f"count={result['policy_preset_count']}")
    for preset in records:
        print(f"- {preset['selector']} -> {preset['path']}")


if __name__ == "__main__":
    main()
