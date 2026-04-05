"""Comparison and diff helpers for webview-screenshort."""

from .diffing import ImageDiffResult, diff_images, diff_images_payload
from .reports import build_comparison_result_from_paths
from .sessions import build_compare_session_payload

__all__ = [
    "ImageDiffResult",
    "build_comparison_result_from_paths",
    "build_compare_session_payload",
    "diff_images",
    "diff_images_payload",
]
