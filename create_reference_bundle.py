#!/usr/bin/env python3
"""
Create a reusable expected-reference bundle for compare-review workflows.
"""

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

BUNDLE_SCHEMA = "webview-screenshort.reference-bundle/v1"
SESSION_SCHEMA = "webview-screenshort.compare-session/v1"


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


def rewrite_report_image_paths(report_payload: dict, source_report_path: Path, asset_dir: Path) -> dict:
    result = report_payload.get("result") or {}
    if report_payload.get("result_type") == "capture_set":
        for capture in result.get("captures", []):
            output_path = capture.get("output_path")
            if not output_path:
                continue
            source_image = Path(output_path).expanduser()
            if not source_image.is_absolute():
                source_image = (source_report_path.parent / source_image).resolve()
            target_image = asset_dir / source_image.name
            target_image.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_image, target_image)
            capture["output_path"] = relativize_if_possible(target_image, asset_dir)
        return report_payload

    output_path = result.get("output_path")
    if output_path:
        source_image = Path(output_path).expanduser()
        if not source_image.is_absolute():
            source_image = (source_report_path.parent / source_image).resolve()
        target_image = asset_dir / source_image.name
        target_image.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_image, target_image)
        result["output_path"] = relativize_if_possible(target_image, asset_dir)
    return report_payload


def load_and_bundle_reference_report(reference_report_path: Path, output_path: Path, bundle_name: str) -> tuple[dict, str]:
    report_payload = load_json(reference_report_path)
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
