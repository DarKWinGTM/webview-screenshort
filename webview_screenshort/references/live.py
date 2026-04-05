from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict

from ..capture.service import capture_from_args
from ..qa.gate import apply_gate, load_policy
from ..qa.verdicts import build_verdict_from_payload
from ..schemas import REFERENCE_LIVE_BUNDLE_WORKFLOW, REFERENCE_LIVE_GATE_WORKFLOW
from .bundles import apply_reference_bundle


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
        "workflow": REFERENCE_LIVE_BUNDLE_WORKFLOW,
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
        "workflow": REFERENCE_LIVE_GATE_WORKFLOW,
        "bundle_path": str(Path(args.bundle).expanduser()),
        "url": args.url,
        "live_replay": live_payload,
        "gate": gate_payload,
        "gate_output_path": str(gate_output_path),
    }
