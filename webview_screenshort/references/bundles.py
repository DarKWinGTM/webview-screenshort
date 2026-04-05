from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from ..compare.reports import build_comparison_result_from_paths
from ..compare.sessions import build_compare_session_payload
from ..schemas import EVIDENCE_BUNDLE_SCHEMA, REFERENCE_BUNDLE_SCHEMA, REPORT_SCHEMA, SESSION_SCHEMA


def load_json(path: Path) -> Dict[str, Any]:
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


def resolve_report_path(raw_path: str, bundle_path: Path) -> Path:
    path = Path(raw_path).expanduser()
    if not path.is_absolute():
        path = (bundle_path.parent / path).resolve()
    return path


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


def rewrite_report_image_paths(report_payload: Dict[str, Any], source_report_path: Path, asset_dir: Path) -> Dict[str, Any]:
    result = report_payload.get("result") or {}
    witness_fields = [
        "output_path",
        "rendered_html_path",
        "rendered_text_path",
        "prerendered_html_path",
        "metadata_path",
        "acquisition_path",
        "semantic_page_path",
        "bundle_path",
    ]
    if report_payload.get("result_type") == "capture_set":
        for capture in result.get("captures", []):
            for field in witness_fields:
                raw_path = capture.get(field)
                if raw_path:
                    capture[field] = _copy_if_present(raw_path, source_report_path, asset_dir)
        for field in ("acquisition_path", "semantic_page_path"):
            raw_path = result.get(field)
            if raw_path:
                result[field] = _copy_if_present(raw_path, source_report_path, asset_dir)
        return report_payload

    for field in witness_fields:
        raw_path = result.get(field)
        if raw_path:
            result[field] = _copy_if_present(raw_path, source_report_path, asset_dir)
    return report_payload


def load_and_bundle_reference_report(reference_report_path: Path, output_path: Path, bundle_name: str) -> Tuple[Dict[str, Any], str]:
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


def create_reference_bundle_payload(
    *,
    name: str,
    session_path: Path,
    output_path: Path,
    reference_label: str,
) -> Dict[str, Any]:
    session = load_json(session_path)
    if session.get("session_schema") != SESSION_SCHEMA:
        raise SystemExit(f"Unsupported compare-session schema: {session.get('session_schema')}")

    reference_report_path_raw = session.get("left", {}).get("report_path")
    if not reference_report_path_raw:
        raise SystemExit("Compare session is missing the left/reference report path")

    reference_report_path = Path(reference_report_path_raw).expanduser()
    bundled_reference_report, bundled_reference_report_path = load_and_bundle_reference_report(reference_report_path, output_path, name)
    return {
        "bundle_schema": REFERENCE_BUNDLE_SCHEMA,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "name": name,
        "reference_label": reference_label,
        "reference_side": "left",
        "reference_session_label": session.get("left", {}).get("label") or reference_label,
        "reference_report_path": str(reference_report_path),
        "reference_artifact_schema": bundled_reference_report.get("report_schema") or bundled_reference_report.get("bundle_schema"),
        "bundled_reference_report_path": bundled_reference_report_path,
        "bundled_reference_report": bundled_reference_report,
        "comparison_mode": session.get("comparison", {}).get("comparison_mode"),
        "session_path": str(session_path),
        "session": session,
    }


def write_reference_bundle(
    *,
    name: str,
    session_path: Path,
    output_path: Path,
    reference_label: str,
) -> Dict[str, Any]:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = create_reference_bundle_payload(
        name=name,
        session_path=session_path,
        output_path=output_path,
        reference_label=reference_label,
    )
    with open(output_path, "w", encoding="utf-8") as file_obj:
        json.dump(payload, file_obj, ensure_ascii=False)
    return payload


def apply_reference_bundle(
    *,
    bundle_path: Path,
    current_report_path: Path,
    comparison_json_path: Path,
    session_output_path: Path,
    session_name: str,
    current_label: str,
    diff_dir: Optional[Path] = None,
) -> Dict[str, Any]:
    bundle = load_json(bundle_path)
    if bundle.get("bundle_schema") != REFERENCE_BUNDLE_SCHEMA:
        raise SystemExit(f"Unsupported bundle schema: {bundle.get('bundle_schema')}")

    session = bundle.get("session") or {}
    left_report = bundle.get("bundled_reference_report_path") or bundle.get("reference_report_path") or session.get("left", {}).get("report_path")
    if not left_report:
        raise SystemExit("Reference bundle is missing the reference report path")
    left_report_path = resolve_report_path(left_report, bundle_path)

    comparison_json_path.parent.mkdir(parents=True, exist_ok=True)
    comparison = build_comparison_result_from_paths(left_report_path, current_report_path, diff_dir)
    comparison_json_path.write_text(json.dumps(comparison, ensure_ascii=False), encoding="utf-8")

    session_output_path.parent.mkdir(parents=True, exist_ok=True)
    session_payload = build_compare_session_payload(
        name=session_name,
        left_report=left_report_path,
        right_report=current_report_path,
        left_label=bundle.get("reference_label") or "expected",
        right_label=current_label,
        comparison_json_path=comparison_json_path,
        comparison=comparison,
    )
    session_output_path.write_text(json.dumps(session_payload, ensure_ascii=False), encoding="utf-8")
    session_payload["bundle_path"] = str(bundle_path)
    session_payload["reference_report_path"] = str(left_report_path)
    session_payload["current_report_path"] = str(current_report_path)
    if diff_dir:
        session_payload["diff_dir"] = str(diff_dir)
    return session_payload


def load_reference_bundle(path: Path) -> Optional[Dict[str, Any]]:
    try:
        payload = load_json(path)
    except Exception:
        return None
    if not isinstance(payload, dict):
        return None
    if payload.get("bundle_schema") != REFERENCE_BUNDLE_SCHEMA:
        return None
    return payload


def list_reference_bundles_payload(directory: Path) -> Dict[str, Any]:
    base_dir = directory.expanduser()
    bundles = []
    for path in sorted(base_dir.glob("*.json")):
        payload = load_reference_bundle(path)
        if not payload:
            continue
        session = payload.get("session", {})
        comparison = session.get("comparison", {})
        bundles.append(
            {
                "path": str(path),
                "name": payload.get("name"),
                "generated_at": payload.get("generated_at"),
                "reference_label": payload.get("reference_label"),
                "reference_side": payload.get("reference_side") or "left",
                "reference_report_path": payload.get("reference_report_path") or session.get("left", {}).get("report_path"),
                "session_name": session.get("name"),
                "comparison_mode": payload.get("comparison_mode") or comparison.get("comparison_mode"),
                "pair_count": len(comparison.get("pairs", [])),
                "success": comparison.get("success"),
            }
        )
    return {
        "bundle_schema": REFERENCE_BUNDLE_SCHEMA,
        "directory": str(base_dir),
        "count": len(bundles),
        "bundles": bundles,
    }
