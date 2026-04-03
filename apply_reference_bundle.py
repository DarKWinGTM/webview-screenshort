#!/usr/bin/env python3
"""
Apply a saved reference bundle to a current report and emit a new compare session.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

BUNDLE_SCHEMA = "webview-screenshort.reference-bundle/v1"
SESSION_SCHEMA = "webview-screenshort.compare-session/v1"


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as file_obj:
        return json.load(file_obj)


def resolve_report_path(raw_path: str, bundle_path: Path) -> Path:
    path = Path(raw_path).expanduser()
    if not path.is_absolute():
        path = (bundle_path.parent / path).resolve()
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply a reference bundle to a current report")
    parser.add_argument("--bundle", required=True, help="Path to reference bundle JSON")
    parser.add_argument("--current-report", required=True, help="Path to current capture report")
    parser.add_argument("--comparison-json", required=True, help="Output path for compare_reports JSON")
    parser.add_argument("--session-output", required=True, help="Output path for compare-session JSON")
    parser.add_argument("--session-name", required=True, help="Name for the new compare session")
    parser.add_argument("--current-label", default="actual")
    parser.add_argument("--diff-dir", help="Optional diff image output directory for compare_reports")
    args = parser.parse_args()

    bundle_path = Path(args.bundle).expanduser()
    bundle = load_json(bundle_path)
    if bundle.get("bundle_schema") != BUNDLE_SCHEMA:
        raise SystemExit(f"Unsupported bundle schema: {bundle.get('bundle_schema')}")

    session = bundle.get("session") or {}
    if session.get("session_schema") != SESSION_SCHEMA:
        raise SystemExit("Reference bundle does not contain a valid compare session")

    left_report = bundle.get("bundled_reference_report_path") or bundle.get("reference_report_path") or session.get("left", {}).get("report_path")
    if not left_report:
        raise SystemExit("Reference bundle is missing the reference report path")
    left_report_path = resolve_report_path(left_report, bundle_path)

    comparison_json_path = Path(args.comparison_json).expanduser()
    comparison_json_path.parent.mkdir(parents=True, exist_ok=True)

    compare_helper = Path(__file__).with_name("compare_reports.py")
    compare_cmd = [
        sys.executable,
        str(compare_helper),
        str(left_report_path),
        str(Path(args.current_report).expanduser()),
        "--output-format",
        "json",
    ]
    if args.diff_dir:
        compare_cmd.extend(["--diff-dir", str(Path(args.diff_dir).expanduser())])
    result = subprocess.run(compare_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or "compare_reports.py failed")
    comparison_json_path.write_text(result.stdout, encoding="utf-8")

    compare_session_helper = Path(__file__).with_name("compare_session.py")
    session_output_path = Path(args.session_output).expanduser()
    session_output_path.parent.mkdir(parents=True, exist_ok=True)
    session_cmd = [
        sys.executable,
        str(compare_session_helper),
        "--name",
        args.session_name,
        "--left-report",
        str(left_report_path),
        "--right-report",
        str(Path(args.current_report).expanduser()),
        "--left-label",
        bundle.get("reference_label") or "expected",
        "--right-label",
        args.current_label,
        "--comparison-json",
        str(comparison_json_path),
        "--output",
        str(session_output_path),
    ]
    session_result = subprocess.run(session_cmd, capture_output=True, text=True)
    if session_result.returncode != 0:
        raise SystemExit(session_result.stderr.strip() or "compare_session.py failed")

    session_payload = json.loads(session_result.stdout)
    session_payload["bundle_path"] = str(bundle_path)
    session_payload["reference_report_path"] = str(left_report_path)
    session_payload["current_report_path"] = str(Path(args.current_report).expanduser())
    if args.diff_dir:
        session_payload["diff_dir"] = str(Path(args.diff_dir).expanduser())

    print(json.dumps(session_payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
