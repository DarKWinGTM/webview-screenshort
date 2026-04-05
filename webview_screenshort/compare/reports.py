from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from ..schemas import EVIDENCE_BUNDLE_SCHEMA, REPORT_SCHEMA
from .diffing import ImageDiffResult, diff_images
from .semantic import extract_semantic_summary, summarize_semantic_difference


@dataclass
class ComparedImage:
    report_label: str
    device: str
    image_path: str
    width: Optional[int]
    height: Optional[int]


@dataclass
class ComparisonPair:
    pair_key: str
    device: str
    left: ComparedImage
    right: ComparedImage
    width_delta: Optional[int]
    height_delta: Optional[int]
    classification: str
    classification_reason: str
    semantic_classification: Optional[str] = None
    semantic_reason: Optional[str] = None
    semantic_details: Optional[Dict[str, Any]] = None
    diff: Optional[ImageDiffResult] = None


@dataclass
class ComparisonResult:
    success: bool
    left_report: str
    right_report: str
    report_schema: str
    left_result_type: str
    right_result_type: str
    compatible: bool
    comparison_mode: str
    pairs: List[ComparisonPair]
    classification_summary: Dict[str, List[str]]
    semantic_classification_summary: Dict[str, List[str]]
    warnings: List[str]
    error: Optional[str] = None


def load_json(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as file_obj:
        return json.load(file_obj)


def require_valid_capture_source(payload: Dict[str, Any], source_path: Path) -> Tuple[str, Dict[str, Any]]:
    if payload.get("report_schema") == REPORT_SCHEMA:
        result = payload.get("result")
        if not isinstance(result, dict):
            raise SystemExit(f"Missing `result` object in {source_path}")
        return REPORT_SCHEMA, result
    if payload.get("bundle_schema") == EVIDENCE_BUNDLE_SCHEMA:
        result = payload.get("result")
        if not isinstance(result, dict):
            raise SystemExit(f"Missing `result` object in {source_path}")
        return EVIDENCE_BUNDLE_SCHEMA, result
    raise SystemExit(
        f"Unsupported capture source in {source_path}: report_schema={payload.get('report_schema')} bundle_schema={payload.get('bundle_schema')}"
    )


def resolve_image_path(image_path: Any, report_path: Path) -> str:
    path = Path(str(image_path or "")).expanduser()
    if not path.is_absolute():
        path = (report_path.parent / path).resolve()
    return str(path)


def collect_images(result: Dict[str, Any], report_label: str, report_path: Path) -> List[ComparedImage]:
    if result.get("capture_set") == "responsive":
        images: List[ComparedImage] = []
        for capture in result.get("captures", []):
            images.append(
                ComparedImage(
                    report_label=report_label,
                    device=str(capture.get("device") or "unknown"),
                    image_path=resolve_image_path(capture.get("output_path"), report_path),
                    width=capture.get("image_width"),
                    height=capture.get("image_height"),
                )
            )
        return images
    return [
        ComparedImage(
            report_label=report_label,
            device=str(result.get("device") or "default"),
            image_path=resolve_image_path(result.get("output_path"), report_path),
            width=result.get("image_width"),
            height=result.get("image_height"),
        )
    ]


def index_by_device(images: List[ComparedImage]) -> Dict[str, ComparedImage]:
    return {image.device: image for image in images}


def build_pairs(left_images: List[ComparedImage], right_images: List[ComparedImage]) -> List[ComparisonPair]:
    left_by_device = index_by_device(left_images)
    right_by_device = index_by_device(right_images)
    shared_devices = sorted(set(left_by_device) & set(right_by_device))
    pairs: List[ComparisonPair] = []
    for device in shared_devices:
        left = left_by_device[device]
        right = right_by_device[device]
        width_delta = None if left.width is None or right.width is None else right.width - left.width
        height_delta = None if left.height is None or right.height is None else right.height - left.height
        pairs.append(
            ComparisonPair(
                pair_key=f"{left.report_label}-vs-{right.report_label}:{device}",
                device=device,
                left=left,
                right=right,
                width_delta=width_delta,
                height_delta=height_delta,
                classification="awaiting_diff",
                classification_reason="diff_not_run_yet",
            )
        )
    return pairs


def determine_mode(left_result: Dict[str, Any], right_result: Dict[str, Any]) -> str:
    left_is_set = left_result.get("capture_set") == "responsive"
    right_is_set = right_result.get("capture_set") == "responsive"
    if left_is_set and right_is_set:
        return "responsive-set"
    if not left_is_set and not right_is_set:
        return "focused-capture"
    return "mixed"


def classify_pair(pair: ComparisonPair) -> Tuple[str, str]:
    diff = pair.diff
    if not diff:
        return "invalid_diff_payload", "missing_diff_payload"
    if not diff.success:
        if not diff.same_size:
            return "size_mismatch", "images_are_not_same_size"
        return "diff_error", "diff_analysis_failed"
    if pair.width_delta or pair.height_delta:
        return "dimension_shift", "reported_image_dimensions_changed"
    if diff.diff_pixels:
        if diff.bounding_box:
            return "visual_change_region", "non_zero_diff_pixels_with_bounding_box"
        return "visual_change", "non_zero_diff_pixels_detected"
    return "exact_match", "no_visual_difference_detected"


def build_classification_summary(pairs: List[ComparisonPair]) -> Dict[str, List[str]]:
    summary: Dict[str, List[str]] = {}
    for pair in pairs:
        summary.setdefault(pair.classification, []).append(pair.device)
    return dict(sorted(summary.items()))


def build_semantic_classification_summary(pairs: List[ComparisonPair]) -> Dict[str, List[str]]:
    summary: Dict[str, List[str]] = {}
    for pair in pairs:
        classification = pair.semantic_classification or "semantic_unavailable"
        summary.setdefault(classification, []).append(pair.device)
    return dict(sorted(summary.items()))


def enrich_pairs_with_diff(
    pairs: List[ComparisonPair],
    diff_dir: Optional[Path],
    left_result: Dict[str, Any],
    right_result: Dict[str, Any],
    left_path: Path,
    right_path: Path,
) -> None:
    for pair in pairs:
        diff_output = diff_dir / f"{pair.device}_diff.png" if diff_dir else None
        pair.diff = diff_images(Path(pair.left.image_path), Path(pair.right.image_path), diff_output)
        pair.classification, pair.classification_reason = classify_pair(pair)
        left_semantic = extract_semantic_summary(left_result, left_path, pair.device)
        right_semantic = extract_semantic_summary(right_result, right_path, pair.device)
        pair.semantic_classification, pair.semantic_reason, pair.semantic_details = summarize_semantic_difference(left_semantic, right_semantic)


def build_comparison_result_from_paths(left_path: Path, right_path: Path, diff_dir: Optional[Path] = None) -> Dict[str, Any]:
    left_payload = load_json(left_path)
    right_payload = load_json(right_path)
    left_source_schema, left_result = require_valid_capture_source(left_payload, left_path)
    right_source_schema, right_result = require_valid_capture_source(right_payload, right_path)

    left_images = collect_images(left_result, "left", left_path)
    right_images = collect_images(right_result, "right", right_path)
    pairs = build_pairs(left_images, right_images)
    warnings: List[str] = []

    if not pairs:
        warnings.append("No shared device/image pairs were found between the two reports.")

    mode = determine_mode(left_result, right_result)
    if mode == "mixed":
        warnings.append("Reports represent different capture shapes; only shared device labels were paired.")

    if pairs:
        enrich_pairs_with_diff(pairs, diff_dir, left_result, right_result, left_path, right_path)

    failed_pairs = [pair.device for pair in pairs if not pair.diff or not pair.diff.success]
    if failed_pairs:
        warnings.append("Diff analysis failed for device pair(s): " + ", ".join(failed_pairs) + ".")

    success = bool(pairs) and not failed_pairs
    error = None
    if not pairs:
        error = "No comparable image pairs found."
    elif failed_pairs:
        error = "Diff analysis failed for device pair(s): " + ", ".join(failed_pairs) + "."

    result = ComparisonResult(
        success=success,
        left_report=str(left_path),
        right_report=str(right_path),
        report_schema=REPORT_SCHEMA,
        left_result_type=str(left_payload.get("result_type") or ("evidence_bundle" if left_source_schema == EVIDENCE_BUNDLE_SCHEMA else "unknown")),
        right_result_type=str(right_payload.get("result_type") or ("evidence_bundle" if right_source_schema == EVIDENCE_BUNDLE_SCHEMA else "unknown")),
        compatible=success,
        comparison_mode=mode,
        pairs=pairs,
        classification_summary=build_classification_summary(pairs),
        semantic_classification_summary=build_semantic_classification_summary(pairs),
        warnings=warnings,
        error=error,
    )
    return asdict(result)
