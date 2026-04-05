#!/usr/bin/env python3
"""
Generate simple image-diff metadata between two screenshots.
"""

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional, Tuple

from PIL import Image, ImageChops


def build_difference_mask(diff: Image.Image) -> Image.Image:
    rgb_mask = diff.convert("RGB").convert("L")
    alpha_mask = diff.getchannel("A")
    return ImageChops.lighter(rgb_mask, alpha_mask)


def build_visible_diff_image(diff: Image.Image, mask: Image.Image) -> Image.Image:
    rgb = diff.convert("RGB")
    if not rgb.getbbox():
        rgb = Image.merge("RGB", (mask, mask, mask))
    alpha = mask.point(lambda value: 255 if value else 0)
    return Image.merge("RGBA", (*rgb.split(), alpha))


@dataclass
class ImageDiffResult:
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


def load_image(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def main() -> None:
    parser = argparse.ArgumentParser(description="Diff two images and emit structured metadata")
    parser.add_argument("left_image")
    parser.add_argument("right_image")
    parser.add_argument("--diff-output", help="Optional output path for visual diff image")
    parser.add_argument("--output-format", choices=["json", "text"], default="json")
    args = parser.parse_args()

    left_path = Path(args.left_image).expanduser()
    right_path = Path(args.right_image).expanduser()

    try:
        left = load_image(left_path)
        right = load_image(right_path)
    except Exception as exc:
        result = ImageDiffResult(
            success=False,
            left_image=str(left_path),
            right_image=str(right_path),
            same_size=False,
            left_width=0,
            left_height=0,
            right_width=0,
            right_height=0,
            diff_pixels=0,
            diff_ratio=0.0,
            bounding_box=None,
            diff_image_path=None,
            error=str(exc),
        )
        print(json.dumps(asdict(result), ensure_ascii=False) if args.output_format == "json" else f"❌ {exc}")
        sys.exit(1)

    left_width, left_height = left.size
    right_width, right_height = right.size
    same_size = left.size == right.size

    if not same_size:
        result = ImageDiffResult(
            success=False,
            left_image=str(left_path),
            right_image=str(right_path),
            same_size=False,
            left_width=left_width,
            left_height=left_height,
            right_width=right_width,
            right_height=right_height,
            diff_pixels=0,
            diff_ratio=0.0,
            bounding_box=None,
            diff_image_path=None,
            error="Images must be the same size for diff analysis.",
        )
        print(json.dumps(asdict(result), ensure_ascii=False) if args.output_format == "json" else result.error)
        sys.exit(1)

    diff = ImageChops.difference(left, right)
    diff_mask = build_difference_mask(diff)
    bbox = diff_mask.getbbox()
    diff_pixels = 0
    if bbox:
        diff_pixels = sum(diff_mask.histogram()[1:])
    total_pixels = left_width * left_height
    diff_ratio = diff_pixels / total_pixels if total_pixels else 0.0

    diff_output_path = None
    if args.diff_output:
        output_path = Path(args.diff_output).expanduser()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        build_visible_diff_image(diff, diff_mask).save(output_path)
        diff_output_path = str(output_path)

    result = ImageDiffResult(
        success=True,
        left_image=str(left_path),
        right_image=str(right_path),
        same_size=True,
        left_width=left_width,
        left_height=left_height,
        right_width=right_width,
        right_height=right_height,
        diff_pixels=diff_pixels,
        diff_ratio=diff_ratio,
        bounding_box=bbox,
        diff_image_path=diff_output_path,
    )

    if args.output_format == "json":
        print(json.dumps(asdict(result), ensure_ascii=False))
    else:
        print(f"same_size={result.same_size} diff_pixels={result.diff_pixels} diff_ratio={result.diff_ratio:.6f}")
        if result.bounding_box:
            print(f"bbox={result.bounding_box}")
        if result.diff_image_path:
            print(f"diff_image={result.diff_image_path}")


if __name__ == "__main__":
    main()
