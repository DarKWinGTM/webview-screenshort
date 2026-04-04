#!/usr/bin/env python3
"""
Generate a machine-readable QA verdict from compare-session, comparison, or
reference-live-replay artifacts.
"""

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

SESSION_SCHEMA = "webview-screenshort.compare-session/v1"
LIVE_REPLAY_WORKFLOW = "reference_live_bundle"


@dataclass
class DeviceVerdict:
    device: str
    verdict: str
    passed: bool
    reason: str
    diff_pixels: Optional[int]
    diff_ratio: Optional[float]
    width_delta: Optional[int]
    height_delta: Optional[int]
    left_image: str
    right_image: str
    diff_image_path: Optional[str]
    bounding_box: Optional[tuple[int, int, int, int]]
    warnings: List[str]


@dataclass
class VerdictResult:
    success: bool
    source_type: str
    source_path: str
    overall_verdict: str
    overall_passed: bool
    pair_count: int
    passed_devices: int
    failed_devices: int
    invalid_devices: int
    match_devices: List[str]
    mismatch_devices: List[str]
    invalid_device_names: List[str]
    warnings: List[str]
    devices: List[DeviceVerdict]
    session_name: Optional[str] = None
    left_label: Optional[str] = None
    right_label: Optional[str] = None
    error: Optional[str] = None


def load_json(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as file_obj:
        return json.load(file_obj)


def extract_source(payload: Dict[str, Any]) -> tuple[str, Optional[dict], Optional[dict], Optional[str], Optional[str], Optional[str]]:
    if payload.get("workflow") == LIVE_REPLAY_WORKFLOW:
        session = payload.get("session")
        if isinstance(session, dict):
            return (
                "live-replay",
                payload.get("capture") if isinstance(payload.get("capture"), dict) else None,
                session,
                session.get("name"),
                session.get("left", {}).get("label"),
                session.get("right", {}).get("label"),
            )

    if payload.get("session_schema") == SESSION_SCHEMA:
        return (
            "session",
            None,
            payload,
            payload.get("name"),
            payload.get("left", {}).get("label"),
            payload.get("right", {}).get("label"),
        )

    if isinstance(payload.get("pairs"), list):
        return ("comparison", None, {"comparison": payload}, None, None, None)

    raise SystemExit("Unsupported verdict source. Expected live replay, compare session, or comparison JSON.")


def build_device_verdict(pair: Dict[str, Any]) -> DeviceVerdict:
    diff = pair.get("diff") or {}
    warnings: List[str] = []
    verdict = "pass"
    reason = "no_visual_difference_detected"
    passed = True

    if not diff:
        verdict = "invalid"
        reason = "missing_diff_payload"
        passed = False
        warnings.append("Pair does not contain diff metadata.")
    elif not diff.get("success"):
        verdict = "invalid"
        reason = "diff_analysis_failed"
        passed = False
        if diff.get("error"):
            warnings.append(str(diff.get("error")))
    else:
        diff_pixels = diff.get("diff_pixels")
        diff_ratio = diff.get("diff_ratio")
        if diff_pixels or diff_ratio:
            verdict = "fail"
            reason = "visual_mismatch_detected"
            passed = False

    return DeviceVerdict(
        device=str(pair.get("device") or "unknown"),
        verdict=verdict,
        passed=passed,
        reason=reason,
        diff_pixels=diff.get("diff_pixels"),
        diff_ratio=diff.get("diff_ratio"),
        width_delta=pair.get("width_delta"),
        height_delta=pair.get("height_delta"),
        left_image=str((pair.get("left") or {}).get("image_path") or ""),
        right_image=str((pair.get("right") or {}).get("image_path") or ""),
        diff_image_path=diff.get("diff_image_path"),
        bounding_box=diff.get("bounding_box"),
        warnings=warnings,
    )


def build_verdict_from_payload(payload: Dict[str, Any], source_path: Path) -> VerdictResult:
    source_type, capture_payload, session_payload, session_name, left_label, right_label = extract_source(payload)
    comparison = (session_payload or {}).get("comparison") or {}
    pairs = comparison.get("pairs")
    if not isinstance(pairs, list):
        return VerdictResult(
            success=False,
            source_type=source_type,
            source_path=str(source_path),
            overall_verdict="invalid",
            overall_passed=False,
            pair_count=0,
            passed_devices=0,
            failed_devices=0,
            invalid_devices=0,
            match_devices=[],
            mismatch_devices=[],
            invalid_device_names=[],
            warnings=[],
            devices=[],
            session_name=session_name,
            left_label=left_label,
            right_label=right_label,
            error="Missing comparison pairs.",
        )

    devices = [build_device_verdict(pair) for pair in pairs]
    match_devices = [device.device for device in devices if device.verdict == "pass"]
    mismatch_devices = [device.device for device in devices if device.verdict == "fail"]
    invalid_device_names = [device.device for device in devices if device.verdict == "invalid"]
    warnings = list(comparison.get("warnings") or [])
    for device in devices:
        warnings.extend(device.warnings)

    overall_verdict = "pass"
    if invalid_device_names:
        overall_verdict = "invalid"
    elif mismatch_devices:
        overall_verdict = "fail"

    result = VerdictResult(
        success=True,
        source_type=source_type,
        source_path=str(source_path),
        overall_verdict=overall_verdict,
        overall_passed=overall_verdict == "pass",
        pair_count=len(devices),
        passed_devices=len(match_devices),
        failed_devices=len(mismatch_devices),
        invalid_devices=len(invalid_device_names),
        match_devices=match_devices,
        mismatch_devices=mismatch_devices,
        invalid_device_names=invalid_device_names,
        warnings=warnings,
        devices=devices,
        session_name=session_name,
        left_label=left_label,
        right_label=right_label,
        error=None,
    )
    if capture_payload is not None:
        setattr(result, "capture_success", capture_payload.get("success"))
    return result


def emit_text(result: VerdictResult) -> None:
    print(f"overall_verdict={result.overall_verdict}")
    print(f"overall_passed={str(result.overall_passed).lower()}")
    print(f"pair_count={result.pair_count}")
    if result.match_devices:
        print(f"match_devices={','.join(result.match_devices)}")
    if result.mismatch_devices:
        print(f"mismatch_devices={','.join(result.mismatch_devices)}")
    if result.invalid_device_names:
        print(f"invalid_devices={','.join(result.invalid_device_names)}")
    for device in result.devices:
        print(
            f"- {device.device}: verdict={device.verdict} diff_pixels={device.diff_pixels} diff_ratio={device.diff_ratio} reason={device.reason}"
        )
    for warning in result.warnings:
        print(f"⚠️ {warning}")
    if result.error:
        print(f"❌ {result.error}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a QA verdict from compare or live replay artifacts")
    parser.add_argument("source", help="Path to a compare-session JSON, comparison JSON, or live replay JSON")
    parser.add_argument("--output-format", choices=["json", "text"], default="json")
    args = parser.parse_args()

    source_path = Path(args.source).expanduser()
    payload = load_json(source_path)
    result = build_verdict_from_payload(payload, source_path)

    if args.output_format == "json":
        print(json.dumps(asdict(result), ensure_ascii=False))
    else:
        emit_text(result)

    sys.exit(0 if result.success else 1)


if __name__ == "__main__":
    main()
