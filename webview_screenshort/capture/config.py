from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

DEFAULT_PRIMARY_API = "https://service.headless-render-api.com/screenshot"
DEFAULT_FALLBACK_API = "https://cauhib5bi3.execute-api.ap-south-1.amazonaws.com/default/screenshot"
DEFAULT_FALLBACK_CONTENT_TYPE = "text/plain;charset=UTF-8"
DEFAULT_FALLBACK_ORIGIN = "https://constellix.vercel.app"
DEFAULT_FALLBACK_REFERER = "https://constellix.vercel.app/"
DEFAULT_VIEWPORT_WIDTH = 1920
DEFAULT_VIEWPORT_HEIGHT = 1080
DEFAULT_FULLPAGE_HEIGHT = 20000
DEFAULT_PRIMARY_TIMEOUT = 45
DEFAULT_PRIMARY_WAIT_TIMEOUT = 60
DEFAULT_FALLBACK_TIMEOUT = 60
DEFAULT_HTML_TIMEOUT = 60
DEVICE_PRESETS = {
    "desktop": (1920, 1080),
    "tablet": (1024, 1366),
    "mobile": (430, 932),
}


@dataclass
class ScreenshotConfig:
    primary_api: str
    fallback_api: str
    fallback_content_type: str
    fallback_origin: str
    fallback_referer: str
    viewport_width: int
    viewport_height: int
    fullpage_height: int
    primary_timeout: int
    primary_wait_timeout: int
    fallback_timeout: int
    html_timeout: int
    output_dir: Optional[Path]
    prerender_token: str = ""


def load_positive_int(env_name: str, default: int) -> int:
    raw = os.environ.get(env_name)
    if raw is None:
        return default
    try:
        value = int(raw)
    except ValueError as exc:
        raise SystemExit(f"Invalid integer for {env_name}: {raw}") from exc
    if value <= 0:
        raise SystemExit(f"{env_name} must be > 0, got: {value}")
    return value


def load_device_preset(preset_name: Optional[str] = None) -> Optional[Tuple[int, int]]:
    name = preset_name or os.environ.get("WEBVIEW_SCREENSHORT_DEVICE_PRESET")
    if not name:
        return None
    preset = DEVICE_PRESETS.get(name.lower())
    if not preset:
        raise SystemExit(f"Unsupported WEBVIEW_SCREENSHORT_DEVICE_PRESET: {name}")
    return preset


def load_config(device_override: Optional[str] = None) -> ScreenshotConfig:
    output_dir = os.environ.get("WEBVIEW_SCREENSHORT_OUTPUT_DIR")
    preset = load_device_preset(device_override)
    viewport_width = preset[0] if preset else load_positive_int("WEBVIEW_SCREENSHORT_VIEWPORT_WIDTH", DEFAULT_VIEWPORT_WIDTH)
    viewport_height = preset[1] if preset else load_positive_int("WEBVIEW_SCREENSHORT_VIEWPORT_HEIGHT", DEFAULT_VIEWPORT_HEIGHT)
    return ScreenshotConfig(
        primary_api=os.environ.get("WEBVIEW_SCREENSHORT_PRIMARY_API", DEFAULT_PRIMARY_API),
        fallback_api=os.environ.get("WEBVIEW_SCREENSHORT_FALLBACK_API", DEFAULT_FALLBACK_API),
        fallback_content_type=os.environ.get("WEBVIEW_SCREENSHORT_FALLBACK_CONTENT_TYPE", DEFAULT_FALLBACK_CONTENT_TYPE),
        fallback_origin=os.environ.get("WEBVIEW_SCREENSHORT_FALLBACK_ORIGIN", DEFAULT_FALLBACK_ORIGIN),
        fallback_referer=os.environ.get("WEBVIEW_SCREENSHORT_FALLBACK_REFERER", DEFAULT_FALLBACK_REFERER),
        viewport_width=viewport_width,
        viewport_height=viewport_height,
        fullpage_height=load_positive_int("WEBVIEW_SCREENSHORT_FULLPAGE_HEIGHT", DEFAULT_FULLPAGE_HEIGHT),
        primary_timeout=load_positive_int("WEBVIEW_SCREENSHORT_PRIMARY_TIMEOUT", DEFAULT_PRIMARY_TIMEOUT),
        primary_wait_timeout=load_positive_int("WEBVIEW_SCREENSHORT_PRIMARY_WAIT_TIMEOUT", DEFAULT_PRIMARY_WAIT_TIMEOUT),
        fallback_timeout=load_positive_int("WEBVIEW_SCREENSHORT_FALLBACK_TIMEOUT", DEFAULT_FALLBACK_TIMEOUT),
        html_timeout=load_positive_int("WEBVIEW_SCREENSHORT_HTML_TIMEOUT", DEFAULT_HTML_TIMEOUT),
        output_dir=Path(output_dir).expanduser() if output_dir else None,
        prerender_token=os.environ.get("PRERENDER_TOKEN") or os.environ.get("WEBVIEW_SCREENSHORT_PRERENDER_TOKEN", ""),
    )


__all__ = [
    "DEVICE_PRESETS",
    "ScreenshotConfig",
    "load_config",
    "load_device_preset",
    "load_positive_int",
]
