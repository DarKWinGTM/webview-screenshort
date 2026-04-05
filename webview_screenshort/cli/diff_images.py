from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from ..compare.diffing import diff_images


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Diff two images and emit structured metadata")
    parser.add_argument("left_image")
    parser.add_argument("right_image")
    parser.add_argument("--diff-output", help="Optional output path for visual diff image")
    parser.add_argument("--output-format", choices=["json", "text"], default="json")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    result = diff_images(
        Path(args.left_image).expanduser(),
        Path(args.right_image).expanduser(),
        Path(args.diff_output).expanduser() if args.diff_output else None,
    )
    payload = {
        "success": result.success,
        "left_image": result.left_image,
        "right_image": result.right_image,
        "same_size": result.same_size,
        "left_width": result.left_width,
        "left_height": result.left_height,
        "right_width": result.right_width,
        "right_height": result.right_height,
        "diff_pixels": result.diff_pixels,
        "diff_ratio": result.diff_ratio,
        "bounding_box": result.bounding_box,
        "diff_image_path": result.diff_image_path,
        "error": result.error,
    }

    if args.output_format == "json":
        print(json.dumps(payload, ensure_ascii=False))
    else:
        if not result.success and result.error:
            print(result.error)
        else:
            print(f"same_size={result.same_size} diff_pixels={result.diff_pixels} diff_ratio={result.diff_ratio:.6f}")
            if result.bounding_box:
                print(f"bbox={result.bounding_box}")
            if result.diff_image_path:
                print(f"diff_image={result.diff_image_path}")

    sys.exit(0 if result.success else 1)


if __name__ == "__main__":
    main()
