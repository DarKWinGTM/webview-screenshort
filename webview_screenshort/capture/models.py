from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from .config import ScreenshotConfig


@dataclass
class CaptureResult:
    success: bool
    url: str
    output_path: str
    engine_requested: str
    engine_used: Optional[str]
    mode_requested: str
    mode_effective: Optional[str]
    wait_requested: bool
    wait_effective: bool
    viewport_width: int
    viewport_height: int
    witness_mode: str = "visual"
    file_size_bytes: Optional[int] = None
    image_width: Optional[int] = None
    image_height: Optional[int] = None
    device: Optional[str] = None
    report_path: Optional[str] = None
    bundle_path: Optional[str] = None
    rendered_html_path: Optional[str] = None
    rendered_text_path: Optional[str] = None
    prerendered_html_path: Optional[str] = None
    metadata_path: Optional[str] = None
    acquisition_path: Optional[str] = None
    semantic_page_path: Optional[str] = None
    title: Optional[str] = None
    page_metadata: Optional[Dict[str, Any]] = None
    acquisition_summary: Optional[Dict[str, Any]] = None
    semantic_page_summary: Optional[Dict[str, Any]] = None
    auth_summary: Optional[Dict[str, Any]] = None
    warnings: List[str] = field(default_factory=list)
    error: Optional[str] = None


@dataclass
class CaptureSetResult:
    success: bool
    url: str
    capture_set: str
    engine_requested: str
    mode_requested: str
    wait_requested: bool
    witness_mode: str
    captures: List[CaptureResult]
    successful_captures: int
    failed_captures: int
    report_path: Optional[str] = None
    bundle_path: Optional[str] = None
    acquisition_path: Optional[str] = None
    semantic_page_path: Optional[str] = None
    warnings: List[str] = field(default_factory=list)
    error: Optional[str] = None


class Reporter:
    def __init__(self, output_format: str):
        self.output_format = output_format

    def log(self, message: str) -> None:
        if self.output_format == "json":
            print(message, file=__import__("sys").stderr)
        else:
            print(message)


def capture_label(device: Optional[str] = None) -> str:
    return f"[{device}] " if device else ""


def empty_html_witnesses() -> Dict[str, Any]:
    return {
        "rendered_html_path": None,
        "rendered_text_path": None,
        "prerendered_html_path": None,
        "metadata_path": None,
        "acquisition_path": None,
        "semantic_page_path": None,
        "title": None,
        "page_metadata": {},
        "acquisition_summary": {},
        "semantic_page_summary": {},
    }


__all__ = [
    "CaptureResult",
    "CaptureSetResult",
    "Reporter",
    "ScreenshotConfig",
    "capture_label",
    "empty_html_witnesses",
]
