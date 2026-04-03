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
from typing import Any, Dict, List, Optional

REPORT_SCHEMA = "webview-screenshort.capture-report/v1"


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
    bounding_box: Optional[tuple[int, int, int, int]]
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
    warnings: List[str]
    error: Optional[str] = None


def load_json(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as file_obj:
        return json.load(file_obj)


def require_valid_report(payload: Dict[str, Any], report_path: Path) -> Dict[str, Any]:
    if payload.get("report_schema") != REPORT_SCHEMA:
        raise SystemExit(f"Unsupported report schema in {report_path}: {payload.get('report_schema')}")
    result = payload.get("result")
    if not isinstance(result, dict):
        raise SystemExit(f"Missing `result` object in {report_path}")
    return result


def collect_images(result: Dict[str, Any], report_label: str) -> List[ComparedImage]:
    result_type = result.get("capture_set")
    if result_type == "responsive":
        images = []
        for capture in result.get("captures", []):
            images.append(
                ComparedImage(
                    report_label=report_label,
                    device=str(capture.get("device") or "unknown"),
                    image_path=str(capture.get("output_path")),
                    width=capture.get("image_width"),
                    height=capture.get("image_height"),
                )
            )
        return images

    return [
        ComparedImage(
            report_label=report_label,
            device=str(result.get("device") or "default"),
            image_path=str(result.get("output_path")),
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


def enrich_pairs_with_diff(pairs: List[ComparisonPair], diff_dir: Optional[Path]) -> None:
    diff_helper = Path(__file__).with_name("diff_images.py")
    for pair in pairs:
        diff_output = None
        if diff_dir:
            diff_output = diff_dir / f"{pair.device}_diff.png"
        pair.diff = run_diff_helper(diff_helper, pair.left.image_path, pair.right.image_path, diff_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare two persisted webview capture reports")
    parser.add_argument("left_report", help="Path to the first capture report")
    parser.add_argument("right_report", help="Path to the second capture report")
    parser.add_argument("--output-format", choices=["text", "json"], default="json")
    parser.add_argument("--diff-dir", help="Optional directory for generated diff images")
    args = parser.parse_args()

    left_path = Path(args.left_report).expanduser()
    right_path = Path(args.right_report).expanduser()

    left_payload = load_json(left_path)
    right_payload = load_json(right_path)
    left_result = require_valid_report(left_payload, left_path)
    right_result = require_valid_report(right_payload, right_path)

    left_images = collect_images(left_result, "left")
    right_images = collect_images(right_result, "right")
    pairs = build_pairs(left_images, right_images)
    warnings: List[str] = []

    if not pairs:
        warnings.append("No shared device/image pairs were found between the two reports.")

    mode = determine_mode(left_result, right_result)
    if mode == "mixed":
        warnings.append("Reports represent different capture shapes; only shared device labels were paired.")

    diff_dir = Path(args.diff_dir).expanduser() if args.diff_dir else None
    if pairs:
        enrich_pairs_with_diff(pairs, diff_dir)

    result = ComparisonResult(
        success=bool(pairs),
        left_report=str(left_path),
        right_report=str(right_path),
        report_schema=REPORT_SCHEMA,
        left_result_type=str(left_payload.get("result_type") or "unknown"),
        right_result_type=str(right_payload.get("result_type") or "unknown"),
        compatible=bool(pairs),
        comparison_mode=mode,
        pairs=pairs,
        warnings=warnings,
        error=None if pairs else "No comparable image pairs found.",
    )

    if args.output_format == "json":
        print(json.dumps(asdict(result), ensure_ascii=False))
        sys.exit(0 if result.success else 1)

    print(f"Comparison mode: {result.comparison_mode}")
    print(f"Pairs: {len(result.pairs)}")
    for pair in result.pairs:
        print(f"- {pair.device}: {pair.left.image_path} ↔ {pair.right.image_path}")
        if pair.diff:
            print(f"  diff_pixels={pair.diff.diff_pixels} diff_ratio={pair.diff.diff_ratio:.6f}")
            if pair.diff.bounding_box:
                print(f"  bbox={pair.diff.bounding_box}")
            if pair.diff.diff_image_path:
                print(f"  diff_image={pair.diff.diff_image_path}")
    for warning in result.warnings:
        print(f"⚠️ {warning}")
    if result.error:
        print(f"❌ {result.error}")
    sys.exit(0 if result.success else 1)


if __name__ == "__main__":
    main()
