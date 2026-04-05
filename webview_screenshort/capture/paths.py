from __future__ import annotations

from datetime import datetime
import os
from pathlib import Path
import tempfile
from typing import Optional, Tuple

from .config import ScreenshotConfig

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
WORKSPACE_OUTPUT_SUBDIR = Path(".tmp") / "webview-screenshort"
PLUGIN_CACHE_MARKER = (".claude", "plugins", "cache")


def is_plugin_cache_path(path: Path) -> bool:
    parts = path.resolve().parts
    return all(marker in parts for marker in PLUGIN_CACHE_MARKER)


def detect_workspace_base_dir() -> Optional[Path]:
    cwd = Path.cwd().resolve()
    if not is_plugin_cache_path(cwd):
        return cwd

    oldpwd = os.environ.get("OLDPWD")
    if oldpwd:
        oldpwd_path = Path(oldpwd).expanduser().resolve()
        if not is_plugin_cache_path(oldpwd_path):
            return oldpwd_path

    return None


def normalize_url(url: str) -> str:
    if not url.startswith(("http://", "https://")):
        return "https://" + url
    return url


def ensure_image_suffix(path: Path) -> Path:
    return path if path.suffix.lower() in IMAGE_SUFFIXES else path.with_suffix(".png")


def apply_suffix(path: Path, suffix: Optional[str] = None) -> Path:
    if not suffix:
        return path
    return path.with_name(f"{path.stem}_{suffix}{path.suffix}")


def ensure_json_suffix(path: Path) -> Path:
    return path if path.suffix.lower() == ".json" else path.with_suffix(".json")


def ensure_parent_dir(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def default_output_dir(config: ScreenshotConfig) -> Path:
    if config.output_dir:
        return config.output_dir

    workspace_base = detect_workspace_base_dir()
    if workspace_base is not None:
        return workspace_base / WORKSPACE_OUTPUT_SUBDIR

    return Path(tempfile.gettempdir()) / "webview-screenshort"


def generate_output_path(url: str, config: ScreenshotConfig, provided_path: Optional[str] = None, output_dir: Optional[str] = None, suffix: Optional[str] = None) -> Path:
    if provided_path:
        path = apply_suffix(ensure_image_suffix(Path(provided_path).expanduser()), suffix)
        return ensure_parent_dir(path)
    base_dir = Path(output_dir).expanduser() if output_dir else default_output_dir(config)
    base_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    domain = url.replace("https://", "").replace("http://", "").split("/")[0].replace(".", "_")
    path = base_dir / f"screenshot_{domain}_{timestamp}.png"
    return apply_suffix(path, suffix)


def generate_report_path(url: str, config: ScreenshotConfig, provided_path: Optional[str] = None, output_dir: Optional[str] = None, suffix: Optional[str] = None) -> Path:
    if provided_path:
        path = apply_suffix(ensure_json_suffix(Path(provided_path).expanduser()), suffix)
        return ensure_parent_dir(path)
    base_dir = Path(output_dir).expanduser() if output_dir else default_output_dir(config)
    base_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    domain = url.replace("https://", "").replace("http://", "").split("/")[0].replace(".", "_")
    path = base_dir / f"capture_report_{domain}_{timestamp}.json"
    return apply_suffix(path, suffix)


def generate_bundle_path(url: str, config: ScreenshotConfig, provided_path: Optional[str] = None, output_dir: Optional[str] = None, suffix: Optional[str] = None) -> Path:
    if provided_path:
        path = apply_suffix(ensure_json_suffix(Path(provided_path).expanduser()), suffix)
        return ensure_parent_dir(path)
    base_dir = Path(output_dir).expanduser() if output_dir else default_output_dir(config)
    base_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    domain = url.replace("https://", "").replace("http://", "").split("/")[0].replace(".", "_")
    path = base_dir / f"evidence_bundle_{domain}_{timestamp}.json"
    return apply_suffix(path, suffix)


def derive_neighbor_path(base_path: Path, suffix_name: str, extension: str) -> Path:
    ext = extension if extension.startswith(".") else f".{extension}"
    return base_path.with_name(f"{base_path.stem}_{suffix_name}{ext}")


def read_png_dimensions(path: Path) -> Tuple[Optional[int], Optional[int]]:
    with open(path, "rb") as file_obj:
        header = file_obj.read(24)
    if len(header) < 24 or not header.startswith(PNG_SIGNATURE):
        return None, None
    width = int.from_bytes(header[16:20], "big")
    height = int.from_bytes(header[20:24], "big")
    return width, height


def validate_png(path: Path) -> bool:
    if not path.exists() or path.stat().st_size <= 0:
        return False
    with open(path, "rb") as file_obj:
        return file_obj.read(8).startswith(PNG_SIGNATURE)


__all__ = [
    "apply_suffix",
    "default_output_dir",
    "derive_neighbor_path",
    "detect_workspace_base_dir",
    "ensure_image_suffix",
    "ensure_json_suffix",
    "ensure_parent_dir",
    "generate_bundle_path",
    "generate_output_path",
    "generate_report_path",
    "is_plugin_cache_path",
    "normalize_url",
    "read_png_dimensions",
    "validate_png",
]
