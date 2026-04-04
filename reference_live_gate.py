#!/usr/bin/env python3
"""
Capture a fresh live screenshot report, replay a saved baseline, and apply QA gate
policy in one flow.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Capture a live current report, replay a saved baseline, and apply QA gate policy"
    )
    parser.add_argument("--bundle", required=True, help="Path to reference bundle JSON")
    parser.add_argument("--url", required=True, help="Live URL to capture before applying the baseline")
    parser.add_argument("--current-report", required=True, help="Output path for the fresh current capture report")
    parser.add_argument("--comparison-json", required=True, help="Output path for compare_reports JSON")
    parser.add_argument("--session-output", required=True, help="Output path for compare-session JSON")
    parser.add_argument("--session-name", required=True, help="Name for the emitted expected/actual compare session")
    parser.add_argument("--gate-output", required=True, help="Output path for QA gate JSON")
    parser.add_argument("--policy-file", help="Optional policy preset JSON for QA gate evaluation")
    parser.add_argument("--current-label", default="actual")
    parser.add_argument("--output", help="Optional screenshot output path or base path for responsive capture set")
    parser.add_argument("--output-dir", help="Optional output directory for generated screenshots")
    parser.add_argument("--device", choices=["desktop", "tablet", "mobile"], help="Optional focused device preset")
    parser.add_argument("--capture-set", choices=["responsive"], help="Optional responsive capture-set mode")
    parser.add_argument("--engine", choices=["auto", "headless", "aws"], default="auto")
    parser.add_argument("--mode", choices=["viewport", "fullpage"], default="viewport")
    parser.add_argument("--wait", action="store_true")
    parser.add_argument("--diff-dir", help="Optional diff image output directory for comparison enrichment")
    parser.add_argument("--fail-on-invalid", choices=["true", "false"], help="Override fail_on_invalid policy")
    parser.add_argument("--require-device", action="append", default=[], help="Require a device; may be passed multiple times")
    parser.add_argument("--max-diff-pixels", type=int, help="Maximum allowed diff pixel count before gate fail")
    parser.add_argument("--max-diff-ratio", type=float, help="Maximum allowed diff ratio before gate fail")
    args = parser.parse_args()

    live_helper = Path(__file__).with_name("reference_live_bundle.py")
    live_cmd = [
        sys.executable,
        str(live_helper),
        "--bundle",
        args.bundle,
        "--url",
        args.url,
        "--current-report",
        args.current_report,
        "--comparison-json",
        args.comparison_json,
        "--session-output",
        args.session_output,
        "--session-name",
        args.session_name,
        "--current-label",
        args.current_label,
        "--mode",
        args.mode,
        "--engine",
        args.engine,
    ]
    if args.wait:
        live_cmd.append("--wait")
    if args.output:
        live_cmd.extend(["--output", args.output])
    if args.output_dir:
        live_cmd.extend(["--output-dir", args.output_dir])
    if args.device:
        live_cmd.extend(["--device", args.device])
    if args.capture_set:
        live_cmd.extend(["--capture-set", args.capture_set])
    if args.diff_dir:
        live_cmd.extend(["--diff-dir", args.diff_dir])

    live_result = subprocess.run(live_cmd, capture_output=True, text=True)
    if live_result.returncode != 0:
        raise SystemExit(live_result.stderr.strip() or live_result.stdout.strip() or "reference_live_bundle.py failed")
    live_payload = json.loads(live_result.stdout)

    gate_helper = Path(__file__).with_name("qa_gate.py")
    gate_cmd = [
        sys.executable,
        str(gate_helper),
        args.session_output,
        "--output-format",
        "json",
    ]
    if args.policy_file:
        gate_cmd.extend(["--policy-file", args.policy_file])
    if args.fail_on_invalid is not None:
        gate_cmd.extend(["--fail-on-invalid", args.fail_on_invalid])
    for device in args.require_device:
        gate_cmd.extend(["--require-device", device])
    if args.max_diff_pixels is not None:
        gate_cmd.extend(["--max-diff-pixels", str(args.max_diff_pixels)])
    if args.max_diff_ratio is not None:
        gate_cmd.extend(["--max-diff-ratio", str(args.max_diff_ratio)])

    gate_result = subprocess.run(gate_cmd, capture_output=True, text=True)
    if gate_result.returncode not in (0, 1):
        raise SystemExit(gate_result.stderr.strip() or gate_result.stdout.strip() or "qa_gate.py failed")
    gate_payload = json.loads(gate_result.stdout)

    gate_output_path = Path(args.gate_output).expanduser()
    gate_output_path.parent.mkdir(parents=True, exist_ok=True)
    gate_output_path.write_text(json.dumps(gate_payload, ensure_ascii=False), encoding="utf-8")

    output_payload = {
        "workflow": "reference_live_gate",
        "bundle_path": str(Path(args.bundle).expanduser()),
        "url": args.url,
        "live_replay": live_payload,
        "gate": gate_payload,
        "gate_output_path": str(gate_output_path),
    }
    print(json.dumps(output_payload, ensure_ascii=False))
    sys.exit(0 if gate_payload.get("overall_passed") else 1)


if __name__ == "__main__":
    main()
