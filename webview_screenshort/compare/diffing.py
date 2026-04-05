from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Optional, Tuple

from PIL import Image, ImageChops


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


def load_image(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def diff_images(left_path: Path, right_path: Path, diff_output: Optional[Path] = None) -> ImageDiffResult:
    try:
        left = load_image(left_path)
        right = load_image(right_path)
    except Exception as exc:
        return ImageDiffResult(
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

    left_width, left_height = left.size
    right_width, right_height = right.size
    same_size = left.size == right.size
    if not same_size:
        return ImageDiffResult(
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

    diff = ImageChops.difference(left, right)
    diff_mask = build_difference_mask(diff)
    bbox = diff_mask.getbbox()
    diff_pixels = sum(diff_mask.histogram()[1:]) if bbox else 0
    total_pixels = left_width * left_height
    diff_ratio = diff_pixels / total_pixels if total_pixels else 0.0

    diff_output_path = None
    if diff_output:
        diff_output.parent.mkdir(parents=True, exist_ok=True)
        build_visible_diff_image(diff, diff_mask).save(diff_output)
        diff_output_path = str(diff_output)

    return ImageDiffResult(
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


def diff_images_payload(left_path: Path, right_path: Path, diff_output: Optional[Path] = None) -> Dict[str, object]:
    return asdict(diff_images(left_path, right_path, diff_output))
