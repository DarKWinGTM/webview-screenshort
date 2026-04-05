#!/usr/bin/env python3
"""
Create a reusable expected-reference bundle for compare-review workflows.
"""

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Tuple

BUNDLE_SCHEMA = "webview-screenshort.reference-bundle/v1"
SESSION_SCHEMA = "webview-screenshort.compare-session/v1"
REPORT_SCHEMA = "webview-screenshort.capture-report/v1"
EVIDENCE_BUNDLE_SCHEMA = "webview-screenshort.evidence-bundle/v1"


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as file_obj:
        return json.load(file_obj)


def sanitize_name(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in ("-", "_") else "-" for ch in value).strip("-") or "bundle"


def bundle_asset_dir(output_path: Path, bundle_name: str) -> Path:
    return output_path.parent / f"{sanitize_name(bundle_name)}_assets"


def relativize_if_possible(path: Path, base_dir: Path) -> str:
    try:
        return str(path.relative_to(base_dir))
    except ValueError:
        return str(path)


def _copy_if_present(raw_path: str, source_report_path: Path, asset_dir: Path) -> str:
    source_path = Path(raw_path).expanduser()
    if not source_path.is_absolute():
        source_path = (source_report_path.parent / source_path).resolve()
    if not source_path.exists():
        return raw_path
    target_path = asset_dir / source_path.name
    target_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, target_path)
    return relativize_if_possible(target_path, asset_dir)


def rewrite_report_image_paths(report_payload: dict, source_report_path: Path, asset_dir: Path) -> dict:
    result = report_payload.get("result") or {}
    witness_fields = [
        "output_path",
        "rendered_html_path",
        "rendered_text_path",
        "prerendered_html_path",
        "bundle_path",
    ]
    if report_payload.get("result_type") == "capture_set":
        for capture in result.get("captures", []):
            for field in witness_fields:
                raw_path = capture.get(field)
                if not raw_path:
                    continue
                capture[field] = _copy_if_present(raw_path, source_report_path, asset_dir)
        return report_payload

    for field in witness_fields:
        raw_path = result.get(field)
        if not raw_path:
            continue
        result[field] = _copy_if_present(raw_path, source_report_path, asset_dir)
    return report_payload


def load_and_bundle_reference_report(reference_report_path: Path, output_path: Path, bundle_name: str) -> Tuple[dict, str]:
    report_payload = load_json(reference_report_path)
    source_schema = report_payload.get("report_schema") or report_payload.get("bundle_schema")
    if source_schema not in {REPORT_SCHEMA, EVIDENCE_BUNDLE_SCHEMA}:
        raise SystemExit(f"Unsupported reference artifact schema: {source_schema}")
    assets_dir = bundle_asset_dir(output_path, bundle_name)
    bundled_report_path = assets_dir / reference_report_path.name
    bundled_report_path.parent.mkdir(parents=True, exist_ok=True)
    bundled_payload = rewrite_report_image_paths(report_payload, reference_report_path, assets_dir)
    with open(bundled_report_path, "w", encoding="utf-8") as file_obj:
        json.dump(bundled_payload, file_obj, ensure_ascii=False)
    return bundled_payload, relativize_if_possible(bundled_report_path, output_path.parent)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a reference bundle from compare-session artifacts")
    parser.add_argument("--name", required=True)
    parser.add_argument("--session", required=True, help="Path to compare-session JSON")
    parser.add_argument("--output", required=True, help="Output bundle JSON path")
    parser.add_argument("--reference-label", default="expected")
    args = parser.parse_args()

    session_path = Path(args.session).expanduser()
    output_path = Path(args.output).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    session = load_json(session_path)
    if session.get("session_schema") != SESSION_SCHEMA:
        raise SystemExit(f"Unsupported compare-session schema: {session.get('session_schema')}")

    reference_report_path = session.get("left", {}).get("report_path")
    if not reference_report_path:
        raise SystemExit("Compare session is missing the left/reference report path")

    reference_report_path = Path(reference_report_path).expanduser()
    bundled_reference_report, bundled_reference_report_path = load_and_bundle_reference_report(
        reference_report_path,
        output_path,
        args.name,
    )

    payload = {
        "bundle_schema": BUNDLE_SCHEMA,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "name": args.name,
        "reference_label": args.reference_label,
        "reference_side": "left",
        "reference_session_label": session.get("left", {}).get("label") or args.reference_label,
        "reference_report_path": str(reference_report_path),
        "reference_artifact_schema": bundled_reference_report.get("report_schema") or bundled_reference_report.get("bundle_schema"),
        "bundled_reference_report_path": bundled_reference_report_path,
        "bundled_reference_report": bundled_reference_report,
        "comparison_mode": session.get("comparison", {}).get("comparison_mode"),
        "session_path": str(session_path),
        "session": session,
    }

    with open(output_path, "w", encoding="utf-8") as file_obj:
        json.dump(payload, file_obj, ensure_ascii=False)

    print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
