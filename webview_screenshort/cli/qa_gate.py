from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from ..qa.gate import build_gate_from_source


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Apply threshold policy gating on top of a QA verdict source")
    parser.add_argument("source", help="Path to a compare-session, comparison, live-replay, or verdict JSON")
    parser.add_argument("--policy-file", help="Optional JSON file containing gate policy settings")
    parser.add_argument("--policy-preset", help="Name of a built-in policy preset from support/policies/")
    parser.add_argument("--output-format", choices=["json", "text"], default="json")
    parser.add_argument("--fail-on-invalid", choices=["true", "false"], help="Override fail_on_invalid policy")
    parser.add_argument("--require-device", action="append", default=[], help="Require a device to be present; may be passed multiple times")
    parser.add_argument("--max-diff-pixels", type=int, help="Maximum allowed diff pixel count before gate fail")
    parser.add_argument("--max-diff-ratio", type=float, help="Maximum allowed diff ratio before gate fail")
    return parser


def emit_text(payload: dict) -> None:
    print(f"overall_gate_status={payload['overall_gate_status']}")
    print(f"overall_passed={str(payload['overall_passed']).lower()}")
    if payload.get("selected_policy_preset"):
        print(f"selected_policy_preset={payload['selected_policy_preset']}")
    if payload.get("missing_required_devices"):
        print(f"missing_required_devices={','.join(payload['missing_required_devices'])}")
    if payload.get("violated_rules"):
        print(f"violated_rules={','.join(payload['violated_rules'])}")
    if payload.get("mismatch_classification_summary"):
        print("mismatch_classifications=" + ",".join(
            f"{classification}:{'|'.join(devices)}" for classification, devices in payload["mismatch_classification_summary"].items()
        ))
    for device in payload.get("devices", []):
        print(
            f"- {device['device']}: verdict={device['verdict']} classification={device['classification']} gate_status={device['gate_status']} diff_pixels={device['diff_pixels']} diff_ratio={device['diff_ratio']}"
        )
    for warning in payload.get("warnings", []):
        print(f"⚠️ {warning}")
    if payload.get("error"):
        print(f"❌ {payload['error']}")


def main() -> None:
    args = build_parser().parse_args()
    result = build_gate_from_source(
        Path(args.source).expanduser(),
        args.policy_file,
        args.policy_preset,
        args.fail_on_invalid,
        args.require_device,
        args.max_diff_pixels,
        args.max_diff_ratio,
    )
    payload = asdict(result)
    if args.output_format == "json":
        print(json.dumps(payload, ensure_ascii=False))
    else:
        emit_text(payload)
    sys.exit(0 if result.overall_passed else 1)


if __name__ == "__main__":
    main()
