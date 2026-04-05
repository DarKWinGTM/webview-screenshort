from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from ..schemas import REFERENCE_LIVE_BUNDLE_WORKFLOW, SESSION_SCHEMA


@dataclass
class DeviceVerdict:
    device: str
    verdict: str
    passed: bool
    reason: str
    classification: str
    classification_reason: str
    semantic_classification: Optional[str]
    semantic_reason: Optional[str]
    semantic_details: Optional[Dict[str, Any]]
    diff_pixels: Optional[int]
    diff_ratio: Optional[float]
    width_delta: Optional[int]
    height_delta: Optional[int]
    left_image: str
    right_image: str
    diff_image_path: Optional[str]
    bounding_box: Optional[Tuple[int, int, int, int]]
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
    mismatch_classification_summary: Dict[str, List[str]]
    semantic_mismatch_classification_summary: Dict[str, List[str]]
    warnings: List[str]
    devices: List[DeviceVerdict]
    session_name: Optional[str] = None
    left_label: Optional[str] = None
    right_label: Optional[str] = None
    error: Optional[str] = None


def load_json(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as file_obj:
        return json.load(file_obj)


def extract_source(payload: Dict[str, Any]) -> Tuple[str, Optional[dict], Optional[dict], Optional[str], Optional[str], Optional[str]]:
    if payload.get("workflow") == REFERENCE_LIVE_BUNDLE_WORKFLOW:
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


def infer_pair_classification(pair: Dict[str, Any]) -> Tuple[str, str]:
    diff = pair.get("diff")
    if not isinstance(diff, dict) or not diff:
        return "invalid_diff_payload", "missing_diff_payload"
    if not diff.get("success"):
        if diff.get("same_size") is False:
            return "size_mismatch", "images_are_not_same_size"
        return "diff_error", "diff_analysis_failed"
    width_delta = pair.get("width_delta")
    height_delta = pair.get("height_delta")
    if width_delta or height_delta:
        return "dimension_shift", "reported_image_dimensions_changed"
    if diff.get("diff_pixels"):
        if diff.get("bounding_box"):
            return "visual_change_region", "non_zero_diff_pixels_with_bounding_box"
        return "visual_change", "non_zero_diff_pixels_detected"
    return "exact_match", "no_visual_difference_detected"


def build_device_verdict(pair: Dict[str, Any]) -> DeviceVerdict:
    diff = pair.get("diff") or {}
    warnings: List[str] = []
    classification = str(pair.get("classification") or "").strip()
    classification_reason = str(pair.get("classification_reason") or "").strip()
    if not classification or not classification_reason:
        classification, classification_reason = infer_pair_classification(pair)
    verdict = "pass"
    reason = "no_visual_difference_detected"
    passed = True

    if classification in {"invalid_diff_payload", "diff_error", "size_mismatch"}:
        verdict = "invalid"
        reason = classification_reason
        passed = False
        if not diff:
            warnings.append("Pair does not contain diff metadata.")
        if diff.get("error"):
            warnings.append(str(diff.get("error")))
    elif classification in {"dimension_shift", "visual_change", "visual_change_region"}:
        verdict = "fail"
        reason = classification_reason
        passed = False

    return DeviceVerdict(
        device=str(pair.get("device") or "unknown"),
        verdict=verdict,
        passed=passed,
        reason=reason,
        classification=classification,
        classification_reason=classification_reason,
        semantic_classification=pair.get("semantic_classification"),
        semantic_reason=pair.get("semantic_reason"),
        semantic_details=pair.get("semantic_details"),
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
    if not isinstance(pairs, list) or not pairs:
        upstream_error = str(comparison.get("error") or "Missing comparison pairs.")
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
            mismatch_classification_summary={},
            semantic_mismatch_classification_summary={},
            warnings=list(comparison.get("warnings") or []),
            devices=[],
            session_name=session_name,
            left_label=left_label,
            right_label=right_label,
            error=upstream_error,
        )

    devices = [build_device_verdict(pair) for pair in pairs]
    match_devices = [device.device for device in devices if device.verdict == "pass"]
    mismatch_devices = [device.device for device in devices if device.verdict == "fail"]
    invalid_device_names = [device.device for device in devices if device.verdict == "invalid"]
    mismatch_classification_summary: Dict[str, List[str]] = {}
    semantic_mismatch_classification_summary: Dict[str, List[str]] = {}
    for device in devices:
        if device.verdict != "pass":
            mismatch_classification_summary.setdefault(device.classification, []).append(device.device)
        semantic_classification = device.semantic_classification or "semantic_unavailable"
        if semantic_classification != "semantic_match":
            semantic_mismatch_classification_summary.setdefault(semantic_classification, []).append(device.device)
    mismatch_classification_summary = dict(sorted(mismatch_classification_summary.items()))
    semantic_mismatch_classification_summary = dict(sorted(semantic_mismatch_classification_summary.items()))
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
        mismatch_classification_summary=mismatch_classification_summary,
        semantic_mismatch_classification_summary=semantic_mismatch_classification_summary,
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


def build_verdict_from_source(source_path: Path) -> VerdictResult:
    payload = load_json(source_path)
    return build_verdict_from_payload(payload, source_path)


def verdict_to_payload(result: VerdictResult) -> Dict[str, Any]:
    return asdict(result)
