from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from ..qa.verdicts import build_verdict_from_source


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a QA verdict from compare or live replay artifacts")
    parser.add_argument("source", help="Path to a compare-session JSON, comparison JSON, or live replay JSON")
    parser.add_argument("--output-format", choices=["json", "text"], default="json")
    return parser


def emit_text(payload: dict) -> None:
    print(f"overall_verdict={payload['overall_verdict']}")
    print(f"overall_passed={str(payload['overall_passed']).lower()}")
    print(f"pair_count={payload['pair_count']}")
    if payload.get("match_devices"):
        print(f"match_devices={','.join(payload['match_devices'])}")
    if payload.get("mismatch_devices"):
        print(f"mismatch_devices={','.join(payload['mismatch_devices'])}")
    if payload.get("invalid_device_names"):
        print(f"invalid_devices={','.join(payload['invalid_device_names'])}")
    if payload.get("mismatch_classification_summary"):
        print("mismatch_classifications=" + ",".join(
            f"{classification}:{'|'.join(devices)}" for classification, devices in payload["mismatch_classification_summary"].items()
        ))
    for device in payload.get("devices", []):
        print(
            f"- {device['device']}: verdict={device['verdict']} classification={device['classification']} diff_pixels={device['diff_pixels']} diff_ratio={device['diff_ratio']} reason={device['reason']}"
        )
    for warning in payload.get("warnings", []):
        print(f"⚠️ {warning}")
    if payload.get("error"):
        print(f"❌ {payload['error']}")


def main() -> None:
    args = build_parser().parse_args()
    result = build_verdict_from_source(Path(args.source).expanduser())
    payload = asdict(result)
    if args.output_format == "json":
        print(json.dumps(payload, ensure_ascii=False))
    else:
        emit_text(payload)
    sys.exit(0 if result.success else 1)


if __name__ == "__main__":
    main()
