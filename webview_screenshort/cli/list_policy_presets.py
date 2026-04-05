from __future__ import annotations

import argparse
import json

from ..qa.policies import list_policy_presets_payload


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="List built-in QA policy presets")
    parser.add_argument("--output-format", choices=["json", "text"], default="json")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    result = list_policy_presets_payload()
    if args.output_format == "json":
        print(json.dumps(result, ensure_ascii=False))
        return
    print(f"count={result['policy_preset_count']}")
    for preset in result["presets"]:
        print(f"- {preset['selector']} -> {preset['path']}")


if __name__ == "__main__":
    main()
