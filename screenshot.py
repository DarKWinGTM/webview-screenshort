#!/usr/bin/env python3
"""
Hybrid Screenshot Tool
Usage: python screenshot.py <url> [--output FILE] [--output-dir DIR]
                            [--engine {auto,headless,aws}]
                            [--mode {viewport,fullpage}]
                            [--wait]
                            [--output-format {text,json}]

Strategy:
1. auto: Try Primary (Headless) -> Fallback to AWS
2. headless: Force Headless Render API
3. aws: Force AWS API

Modes:
- viewport: Capture standard visible area
- fullpage: Capture long-page content using tall viewport simulation

Environment overrides:
- WEBVIEW_SCREENSHORT_PRIMARY_API
- WEBVIEW_SCREENSHORT_FALLBACK_API
- WEBVIEW_SCREENSHORT_FALLBACK_CONTENT_TYPE
- WEBVIEW_SCREENSHORT_FALLBACK_ORIGIN
- WEBVIEW_SCREENSHORT_FALLBACK_REFERER
- WEBVIEW_SCREENSHORT_VIEWPORT_WIDTH
- WEBVIEW_SCREENSHORT_VIEWPORT_HEIGHT
- WEBVIEW_SCREENSHORT_FULLPAGE_HEIGHT
- WEBVIEW_SCREENSHORT_PRIMARY_TIMEOUT
- WEBVIEW_SCREENSHORT_PRIMARY_WAIT_TIMEOUT
- WEBVIEW_SCREENSHORT_FALLBACK_TIMEOUT
- WEBVIEW_SCREENSHORT_OUTPUT_DIR
- WEBVIEW_SCREENSHORT_DEVICE_PRESET
"""

import argparse
import base64
import json
import os
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg"}

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
    output_dir: Optional[Path]


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
    file_size_bytes: Optional[int] = None
    image_width: Optional[int] = None
    image_height: Optional[int] = None
    warnings: List[str] = field(default_factory=list)
    error: Optional[str] = None


class Reporter:
    def __init__(self, output_format: str):
        self.output_format = output_format

    def log(self, message: str) -> None:
        if self.output_format == "json":
            print(message, file=sys.stderr)
        else:
            print(message)


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


def load_device_preset() -> Optional[Tuple[int, int]]:
    preset_name = os.environ.get("WEBVIEW_SCREENSHORT_DEVICE_PRESET")
    if not preset_name:
        return None
    preset = DEVICE_PRESETS.get(preset_name.lower())
    if not preset:
        raise SystemExit(f"Unsupported WEBVIEW_SCREENSHORT_DEVICE_PRESET: {preset_name}")
    return preset


def load_config() -> ScreenshotConfig:
    output_dir = os.environ.get("WEBVIEW_SCREENSHORT_OUTPUT_DIR")
    preset = load_device_preset()
    viewport_width = preset[0] if preset else load_positive_int("WEBVIEW_SCREENSHORT_VIEWPORT_WIDTH", DEFAULT_VIEWPORT_WIDTH)
    viewport_height = preset[1] if preset else load_positive_int("WEBVIEW_SCREENSHORT_VIEWPORT_HEIGHT", DEFAULT_VIEWPORT_HEIGHT)
    return ScreenshotConfig(
        primary_api=os.environ.get("WEBVIEW_SCREENSHORT_PRIMARY_API", DEFAULT_PRIMARY_API),
        fallback_api=os.environ.get("WEBVIEW_SCREENSHORT_FALLBACK_API", DEFAULT_FALLBACK_API),
        fallback_content_type=os.environ.get(
            "WEBVIEW_SCREENSHORT_FALLBACK_CONTENT_TYPE", DEFAULT_FALLBACK_CONTENT_TYPE
        ),
        fallback_origin=os.environ.get("WEBVIEW_SCREENSHORT_FALLBACK_ORIGIN", DEFAULT_FALLBACK_ORIGIN),
        fallback_referer=os.environ.get("WEBVIEW_SCREENSHORT_FALLBACK_REFERER", DEFAULT_FALLBACK_REFERER),
        viewport_width=viewport_width,
        viewport_height=viewport_height,
        fullpage_height=load_positive_int("WEBVIEW_SCREENSHORT_FULLPAGE_HEIGHT", DEFAULT_FULLPAGE_HEIGHT),
        primary_timeout=load_positive_int("WEBVIEW_SCREENSHORT_PRIMARY_TIMEOUT", DEFAULT_PRIMARY_TIMEOUT),
        primary_wait_timeout=load_positive_int(
            "WEBVIEW_SCREENSHORT_PRIMARY_WAIT_TIMEOUT", DEFAULT_PRIMARY_WAIT_TIMEOUT
        ),
        fallback_timeout=load_positive_int("WEBVIEW_SCREENSHORT_FALLBACK_TIMEOUT", DEFAULT_FALLBACK_TIMEOUT),
        output_dir=Path(output_dir).expanduser() if output_dir else None,
    )


def normalize_url(url: str) -> str:
    if not url.startswith(("http://", "https://")):
        return "https://" + url
    return url


def ensure_image_suffix(path: Path) -> Path:
    return path if path.suffix.lower() in IMAGE_SUFFIXES else path.with_suffix(".png")


def default_output_dir(config: ScreenshotConfig) -> Path:
    if config.output_dir:
        return config.output_dir
    return Path(__file__).parent / "screenshot"


def generate_output_path(url: str, config: ScreenshotConfig, provided_path: Optional[str] = None, output_dir: Optional[str] = None) -> Path:
    if provided_path:
        path = ensure_image_suffix(Path(provided_path).expanduser())
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    base_dir = Path(output_dir).expanduser() if output_dir else default_output_dir(config)
    base_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    domain = url.replace("https://", "").replace("http://", "").split("/")[0].replace(".", "_")
    return base_dir / f"screenshot_{domain}_{timestamp}.png"


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


def capture_primary(url: str, output_path: Path, config: ScreenshotConfig, mode: str, wait: bool, reporter: Reporter) -> Tuple[bool, List[str], Optional[str], str, bool]:
    reporter.log(f"Attempting Primary API (Headless): {config.primary_api}")
    reporter.log(f"Mode: {mode}, Wait: {wait}")

    target_api = f"{config.primary_api.rstrip('/')}/{url}"
    height = str(config.fullpage_height if mode == "fullpage" else config.viewport_height)
    timeout = config.primary_wait_timeout if wait else config.primary_timeout

    cmd = [
        "curl", "-sS", "--compressed", "--max-time", str(timeout),
        "-H", f"prerender-viewport-width: {config.viewport_width}",
        "-H", f"prerender-viewport-height: {height}",
        "-H", f"prerender-device-width: {config.viewport_width}",
        "-H", f"prerender-device-height: {height}",
    ]

    if wait:
        cmd.extend(["-H", "prerender-wait-extra-long: true"])

    cmd.extend([target_api, "-o", str(output_path)])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except Exception as exc:
        return False, [], f"Primary API exception: {exc}", mode, wait

    if result.returncode != 0:
        stderr = result.stderr.strip() or "curl exited with non-zero status"
        return False, [], f"Primary API curl error: {stderr}", mode, wait

    if validate_png(output_path):
        reporter.log("✅ Primary API Success")
        return True, [], None, mode, wait

    if output_path.exists():
        output_path.unlink()
    return False, [], "Primary API returned invalid data", mode, wait


def capture_fallback(url: str, output_path: Path, config: ScreenshotConfig, mode: str, wait: bool, reporter: Reporter) -> Tuple[bool, List[str], Optional[str], str, bool]:
    reporter.log(f"Attempting Fallback API (AWS): {config.fallback_api}")

    warnings = []
    if mode == "fullpage":
        warnings.append("AWS fallback does not support explicit fullpage mode; result is best-effort only.")
        reporter.log("⚠️ Note: AWS engine does not support explicit 'fullpage' mode settings.")
    if wait:
        warnings.append("AWS fallback does not support explicit wait mode; extra wait is ignored.")
        reporter.log("⚠️ Note: AWS engine does not support explicit 'wait' settings.")

    payload = json.dumps({"url": url}, separators=(",", ":"))
    cmd = [
        "curl", "-sS", "--max-time", str(config.fallback_timeout),
        config.fallback_api,
        "-H", f"content-type: {config.fallback_content_type}",
        "-H", f"origin: {config.fallback_origin}",
        "-H", f"referer: {config.fallback_referer}",
        "--data-raw", payload,
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=config.fallback_timeout)
    except Exception as exc:
        return False, warnings, f"Fallback API exception: {exc}", "best-effort", False

    if result.returncode != 0:
        stderr = result.stderr.strip() or "curl exited with non-zero status"
        return False, warnings, f"Fallback API curl error: {stderr}", "best-effort", False

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return False, warnings, "Fallback API returned invalid JSON", "best-effort", False

    if "screenshot" not in data:
        return False, warnings, f"Fallback API response missing screenshot: {data.get('message', 'Unknown error')}", "best-effort", False

    try:
        img_data = base64.b64decode(data["screenshot"])
        with open(output_path, "wb") as file_obj:
            file_obj.write(img_data)
    except Exception as exc:
        return False, warnings, f"Fallback API write error: {exc}", "best-effort", False

    if validate_png(output_path):
        reporter.log("✅ Fallback API Success")
        return True, warnings, None, "best-effort", False

    if output_path.exists():
        output_path.unlink()
    return False, warnings, "Fallback API produced invalid PNG data", "best-effort", False


def emit_result(result: CaptureResult, output_format: str, reporter: Reporter) -> None:
    if output_format == "json":
        print(json.dumps(asdict(result), ensure_ascii=False))
        return

    if result.success:
        reporter.log(f"Screenshot saved: {result.output_path}")
        if result.file_size_bytes is not None:
            reporter.log(f"Size: {result.file_size_bytes:,} bytes")
        if result.image_width and result.image_height:
            reporter.log(f"Dimensions: {result.image_width}x{result.image_height}")
        if result.warnings:
            for warning in result.warnings:
                reporter.log(f"⚠️ {warning}")
    else:
        if result.warnings:
            for warning in result.warnings:
                reporter.log(f"⚠️ {warning}")
        reporter.log(f"❌ Screenshot capture failed: {result.error}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Hybrid Screenshot Tool")
    parser.add_argument("url", help="URL to capture")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--output-dir", help="Output directory for generated screenshots")
    parser.add_argument("--device", choices=["desktop", "tablet", "mobile"], help="Viewport preset override for frontend review")
    parser.add_argument("--engine", "-e", choices=["auto", "headless", "aws"], default="auto", help="Select screenshot engine (default: auto)")
    parser.add_argument("--mode", "-m", choices=["viewport", "fullpage"], default="fullpage", help="Capture mode: 'viewport' or 'fullpage' (default: fullpage)")
    parser.add_argument("--wait", "-w", action="store_true", help="Wait extra time for dynamic content (Headless engine only)")
    parser.add_argument("--output-format", choices=["text", "json"], default="text", help="Result output format (default: text)")
    args = parser.parse_args()

    if args.device:
        os.environ["WEBVIEW_SCREENSHORT_DEVICE_PRESET"] = args.device

    config = load_config()
    reporter = Reporter(args.output_format)

    url = normalize_url(args.url)
    output_path = generate_output_path(url, config, args.output, args.output_dir)

    reporter.log(f"Target: {url}")
    reporter.log(f"Output: {output_path}")
    reporter.log(f"Engine: {args.engine}")
    reporter.log(f"Mode:   {args.mode}")
    reporter.log(f"Wait:   {args.wait}")
    reporter.log(f"Viewport: {config.viewport_width}x{config.viewport_height}")

    success = False
    warnings: List[str] = []
    error: Optional[str] = None
    engine_used: Optional[str] = None
    mode_effective: Optional[str] = args.mode
    wait_effective = args.wait

    if args.engine == "headless":
        success, warnings, error, mode_effective, wait_effective = capture_primary(url, output_path, config, args.mode, args.wait, reporter)
        engine_used = "headless"

    elif args.engine == "aws":
        success, warnings, error, mode_effective, wait_effective = capture_fallback(url, output_path, config, args.mode, args.wait, reporter)
        engine_used = "aws"

    else:
        success, warnings, error, mode_effective, wait_effective = capture_primary(url, output_path, config, args.mode, args.wait, reporter)
        engine_used = "headless"
        if not success:
            reporter.log("🔄 Switching to Fallback Strategy...")
            fallback_success, fallback_warnings, fallback_error, fallback_mode_effective, fallback_wait_effective = capture_fallback(url, output_path, config, args.mode, args.wait, reporter)
            success = fallback_success
            warnings.extend(fallback_warnings)
            error = fallback_error if fallback_success else fallback_error or error
            engine_used = "aws" if fallback_success else engine_used
            mode_effective = fallback_mode_effective if fallback_success else mode_effective
            wait_effective = fallback_wait_effective if fallback_success else wait_effective

    file_size = output_path.stat().st_size if success and output_path.exists() else None
    image_width, image_height = read_png_dimensions(output_path) if success and output_path.exists() else (None, None)

    result = CaptureResult(
        success=success,
        url=url,
        output_path=str(output_path),
        engine_requested=args.engine,
        engine_used=engine_used,
        mode_requested=args.mode,
        mode_effective=mode_effective,
        wait_requested=args.wait,
        wait_effective=wait_effective,
        viewport_width=config.viewport_width,
        viewport_height=config.viewport_height,
        file_size_bytes=file_size,
        image_width=image_width,
        image_height=image_height,
        warnings=warnings,
        error=error,
    )

    emit_result(result, args.output_format, reporter)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
