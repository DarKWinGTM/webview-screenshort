from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

from dataclasses import asdict

from compare_reports import build_comparison_result_from_paths
from compare_session import build_compare_session_payload
from create_reference_bundle import BUNDLE_SCHEMA
from qa_gate import apply_gate, load_policy
from qa_verdict import build_verdict_from_payload
from .capture_service import capture_from_args


def _load_json(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as file_obj:
        return json.load(file_obj)


def _resolve_report_path(raw_path: str, bundle_path: Path) -> Path:
    path = Path(raw_path).expanduser()
    if not path.is_absolute():
        path = (bundle_path.parent / path).resolve()
    return path


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
    bundle = _load_json(bundle_path)
    if bundle.get("bundle_schema") != BUNDLE_SCHEMA:
        raise SystemExit(f"Unsupported bundle schema: {bundle.get('bundle_schema')}")

    session = bundle.get("session") or {}
    left_report = (
        bundle.get("bundled_reference_report_path")
        or bundle.get("reference_report_path")
        or session.get("left", {}).get("report_path")
    )
    if not left_report:
        raise SystemExit("Reference bundle is missing the reference report path")
    left_report_path = _resolve_report_path(left_report, bundle_path)

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


def reference_live_bundle(*, args: Any) -> Dict[str, Any]:
    bundle_path = Path(args.bundle).expanduser()
    current_report_path = Path(args.current_report).expanduser()
    current_report_path.parent.mkdir(parents=True, exist_ok=True)
    if not getattr(args, "report_file", None):
        args.report_file = str(current_report_path)

    capture_result = capture_from_args(args)
    report_path = capture_result.report_path
    if not report_path:
        raise SystemExit("Capture output did not include a report_path")
    capture_payload = asdict(capture_result)

    session_payload = apply_reference_bundle(
        bundle_path=bundle_path,
        current_report_path=Path(report_path).expanduser(),
        comparison_json_path=Path(args.comparison_json).expanduser(),
        session_output_path=Path(args.session_output).expanduser(),
        session_name=args.session_name,
        current_label=args.current_label,
        diff_dir=Path(args.diff_dir).expanduser() if args.diff_dir else None,
    )

    return {
        "workflow": "reference_live_bundle",
        "bundle_path": str(bundle_path),
        "url": args.url,
        "capture": capture_payload,
        "session": session_payload,
        "current_report_path": str(Path(report_path).expanduser()),
        "comparison_json_path": str(Path(args.comparison_json).expanduser()),
        "session_output_path": str(Path(args.session_output).expanduser()),
    }


def reference_live_gate(*, args: Any) -> Dict[str, Any]:
    live_payload = reference_live_bundle(args=args)
    source_path = Path(args.session_output).expanduser()
    session_payload = json.loads(source_path.read_text(encoding="utf-8"))
    verdict = build_verdict_from_payload(session_payload, source_path)
    policy, selected_policy_preset = load_policy(args.policy_file, args.policy_preset)
    if args.fail_on_invalid is not None:
        policy["fail_on_invalid"] = args.fail_on_invalid == "true"
    if args.require_device:
        policy["require_devices"] = args.require_device
    if args.max_diff_pixels is not None:
        policy["max_diff_pixels"] = args.max_diff_pixels
    if args.max_diff_ratio is not None:
        policy["max_diff_ratio"] = args.max_diff_ratio
    gate_result = apply_gate(asdict(verdict), policy, source_path, selected_policy_preset)
    gate_payload = asdict(gate_result)
    gate_output_path = Path(args.gate_output).expanduser()
    gate_output_path.parent.mkdir(parents=True, exist_ok=True)
    gate_output_path.write_text(json.dumps(gate_payload, ensure_ascii=False), encoding="utf-8")
    return {
        "workflow": "reference_live_gate",
        "bundle_path": str(Path(args.bundle).expanduser()),
        "url": args.url,
        "live_replay": live_payload,
        "gate": gate_payload,
        "gate_output_path": str(gate_output_path),
    }
