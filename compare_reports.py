#!/usr/bin/env python3
"""
Compare two persisted webview capture reports and emit structured metadata for
report-to-report visual review workflows.
"""

import argparse
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPORT_SCHEMA = "webview-screenshort.capture-report/v1"
BUNDLE_SCHEMA = "webview-screenshort.evidence-bundle/v1"


@dataclass
class ComparedImage:
    report_label: str
    device: str
    image_path: str
    width: Optional[int]
    height: Optional[int]


@dataclass
class ImageDiff:
    success: bool
    left_image: str
    right_image: str
    same_size: bool
    left_width: int
    left_height: int
    right_width: int
    right_height: int
    diff_pixels: int
    diff_ratio: float
    bounding_box: Optional[Tuple[int, int, int, int]]
    diff_image_path: Optional[str]
    error: Optional[str] = None


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
    diff: Optional[ImageDiff] = None


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

    if payload.get("bundle_schema") == BUNDLE_SCHEMA:
        result = payload.get("result")
        if not isinstance(result, dict):
            raise SystemExit(f"Missing `result` object in {source_path}")
        return BUNDLE_SCHEMA, result

    raise SystemExit(
        f"Unsupported capture source in {source_path}: report_schema={payload.get('report_schema')} bundle_schema={payload.get('bundle_schema')}"
    )


def resolve_image_path(image_path: Any, report_path: Path) -> str:
    path = Path(str(image_path or "")).expanduser()
    if not path.is_absolute():
        path = (report_path.parent / path).resolve()
    return str(path)


def collect_images(result: Dict[str, Any], report_label: str, report_path: Path) -> List[ComparedImage]:
    result_type = result.get("capture_set")
    if result_type == "responsive":
        images = []
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


def run_diff_helper(diff_helper: Path, left_image: str, right_image: str, diff_output: Optional[Path]) -> ImageDiff:
    cmd = [
        sys.executable,
        str(diff_helper),
        left_image,
        right_image,
        "--output-format",
        "json",
    ]
    if diff_output:
        diff_output.parent.mkdir(parents=True, exist_ok=True)
        cmd.extend(["--diff-output", str(diff_output)])

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        try:
            payload = json.loads(result.stdout)
            return ImageDiff(**payload)
        except Exception:
            return ImageDiff(
                success=False,
                left_image=left_image,
                right_image=right_image,
                same_size=False,
                left_width=0,
                left_height=0,
                right_width=0,
                right_height=0,
                diff_pixels=0,
                diff_ratio=0.0,
                bounding_box=None,
                diff_image_path=None,
                error=result.stderr.strip() or "diff helper failed",
            )

    payload = json.loads(result.stdout)
    return ImageDiff(**payload)


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


def enrich_pairs_with_diff(pairs: List[ComparisonPair], diff_dir: Optional[Path]) -> None:
    diff_helper = Path(__file__).with_name("diff_images.py")
    for pair in pairs:
        diff_output = None
        if diff_dir:
            diff_output = diff_dir / f"{pair.device}_diff.png"
        pair.diff = run_diff_helper(diff_helper, pair.left.image_path, pair.right.image_path, diff_output)
        pair.classification, pair.classification_reason = classify_pair(pair)


def build_comparison_result_from_paths(left_path: Path, right_path: Path, diff_dir: Optional[Path] = None) -> dict:
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
        enrich_pairs_with_diff(pairs, diff_dir)

    failed_pairs = [pair.device for pair in pairs if not pair.diff or not pair.diff.success]
    if failed_pairs:
        warnings.append(
            "Diff analysis failed for device pair(s): " + ", ".join(failed_pairs) + "."
        )

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
        left_result_type=str(left_payload.get("result_type") or ("evidence_bundle" if left_source_schema == BUNDLE_SCHEMA else "unknown")),
        right_result_type=str(right_payload.get("result_type") or ("evidence_bundle" if right_source_schema == BUNDLE_SCHEMA else "unknown")),
        compatible=success,
        comparison_mode=mode,
        pairs=pairs,
        classification_summary=build_classification_summary(pairs),
        warnings=warnings,
        error=error,
    )
    return asdict(result)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare two persisted webview capture reports")
    parser.add_argument("left_report", help="Path to the first capture report")
    parser.add_argument("right_report", help="Path to the second capture report")
    parser.add_argument("--output-format", choices=["text", "json"], default="json")
    parser.add_argument("--diff-dir", help="Optional directory for generated diff images")
    args = parser.parse_args()

    left_path = Path(args.left_report).expanduser()
    right_path = Path(args.right_report).expanduser()

    diff_dir = Path(args.diff_dir).expanduser() if args.diff_dir else None
    result_payload = build_comparison_result_from_paths(left_path, right_path, diff_dir)

    if args.output_format == "json":
        print(json.dumps(result_payload, ensure_ascii=False))
        sys.exit(0 if result_payload.get("success") else 1)

    print(f"Comparison mode: {result_payload['comparison_mode']}")
    print(f"Pairs: {len(result_payload['pairs'])}")
    for pair in result_payload["pairs"]:
        print(f"- {pair['device']}: {pair['left']['image_path']} ↔ {pair['right']['image_path']}")
        print(f"  classification={pair['classification']} reason={pair['classification_reason']}")
        diff = pair.get("diff")
        if diff:
            print(f"  diff_pixels={diff['diff_pixels']} diff_ratio={diff['diff_ratio']:.6f}")
            if diff.get("bounding_box"):
                print(f"  bbox={diff['bounding_box']}")
            if diff.get("diff_image_path"):
                print(f"  diff_image={diff['diff_image_path']}")
    for warning in result_payload["warnings"]:
        print(f"⚠️ {warning}")
    if result_payload.get("error"):
        print(f"❌ {result_payload['error']}")
    sys.exit(0 if result_payload.get("success") else 1)


if __name__ == "__main__":
    main()
