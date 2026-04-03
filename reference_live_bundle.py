#!/usr/bin/env python3
"""
Capture a fresh live screenshot report from a URL and apply a saved reference bundle to it.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

BUNDLE_SCHEMA = "webview-screenshort.reference-bundle/v1"


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as file_obj:
        return json.load(file_obj)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Capture a live current report and apply a saved reference bundle automatically"
    )
    parser.add_argument("--bundle", required=True, help="Path to reference bundle JSON")
    parser.add_argument("--url", required=True, help="Live URL to capture before applying the bundle")
    parser.add_argument("--current-report", required=True, help="Output path for the fresh current capture report")
    parser.add_argument("--comparison-json", required=True, help="Output path for compare_reports JSON")
    parser.add_argument("--session-output", required=True, help="Output path for compare-session JSON")
    parser.add_argument("--session-name", required=True, help="Name for the emitted expected/actual compare session")
    parser.add_argument("--current-label", default="actual")
    parser.add_argument("--output", help="Optional screenshot output path or base path for responsive capture set")
    parser.add_argument("--output-dir", help="Optional output directory for generated screenshots")
    parser.add_argument("--device", choices=["desktop", "tablet", "mobile"], help="Optional focused device preset")
    parser.add_argument("--capture-set", choices=["responsive"], help="Optional responsive capture-set mode")
    parser.add_argument("--engine", choices=["auto", "headless", "aws"], default="auto")
    parser.add_argument("--mode", choices=["viewport", "fullpage"], default="viewport")
    parser.add_argument("--wait", action="store_true")
    parser.add_argument("--diff-dir", help="Optional diff image output directory for comparison enrichment")
    args = parser.parse_args()

    bundle_path = Path(args.bundle).expanduser()
    bundle = load_json(bundle_path)
    if bundle.get("bundle_schema") != BUNDLE_SCHEMA:
        raise SystemExit(f"Unsupported bundle schema: {bundle.get('bundle_schema')}")

    current_report_path = Path(args.current_report).expanduser()
    current_report_path.parent.mkdir(parents=True, exist_ok=True)

    screenshot_helper = Path(__file__).with_name("screenshot.py")
    capture_cmd = [
        sys.executable,
        str(screenshot_helper),
        args.url,
        "--mode",
        args.mode,
        "--engine",
        args.engine,
        "--output-format",
        "json",
        "--report-file",
        str(current_report_path),
    ]
    if args.wait:
        capture_cmd.append("--wait")
    if args.output:
        capture_cmd.extend(["--output", args.output])
    if args.output_dir:
        capture_cmd.extend(["--output-dir", args.output_dir])
    if args.device:
        capture_cmd.extend(["--device", args.device])
    if args.capture_set:
        capture_cmd.extend(["--capture-set", args.capture_set])

    capture_result = subprocess.run(capture_cmd, capture_output=True, text=True)
    if capture_result.returncode != 0:
        raise SystemExit(capture_result.stderr.strip() or capture_result.stdout.strip() or "screenshot.py failed")

    capture_payload = json.loads(capture_result.stdout)
    report_path = capture_payload.get("report_path") or capture_payload.get("result", {}).get("report_path")
    if not report_path:
        raise SystemExit("Capture output did not include a report_path")

    apply_helper = Path(__file__).with_name("apply_reference_bundle.py")
    apply_cmd = [
        sys.executable,
        str(apply_helper),
        "--bundle",
        str(bundle_path),
        "--current-report",
        str(Path(report_path).expanduser()),
        "--comparison-json",
        str(Path(args.comparison_json).expanduser()),
        "--session-output",
        str(Path(args.session_output).expanduser()),
        "--session-name",
        args.session_name,
        "--current-label",
        args.current_label,
    ]
    if args.diff_dir:
        apply_cmd.extend(["--diff-dir", args.diff_dir])

    apply_result = subprocess.run(apply_cmd, capture_output=True, text=True)
    if apply_result.returncode != 0:
        raise SystemExit(apply_result.stderr.strip() or apply_result.stdout.strip() or "apply_reference_bundle.py failed")

    session_payload = json.loads(apply_result.stdout)
    output_payload = {
        "workflow": "reference_live_bundle",
        "bundle_path": str(bundle_path),
        "url": args.url,
        "capture": capture_payload,
        "session": session_payload,
        "current_report_path": str(Path(report_path).expanduser()),
        "comparison_json_path": str(Path(args.comparison_json).expanduser()),
        "session_output_path": str(Path(args.session_output).expanduser()),
    }
    print(json.dumps(output_payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
