#!/usr/bin/env python3
"""
Hybrid Screenshot Tool
Usage: python screenshot.py <url> [--output FILE] [--output-dir DIR]
                           [--device {desktop,tablet,mobile}]
                           [--capture-set {responsive}]
                           [--report-file FILE]
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
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Tuple, Union

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg"}
RESPONSIVE_CAPTURE_SET = ("desktop", "tablet", "mobile")
REPORT_SCHEMA = "webview-screenshort.capture-report/v1"

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
    device: Optional[str] = None
    report_path: Optional[str] = None
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
    captures: List[CaptureResult]
    successful_captures: int
    failed_captures: int
    report_path: Optional[str] = None
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
    return Path(__file__).parent / "screenshot"


def generate_output_path(
    url: str,
    config: ScreenshotConfig,
    provided_path: Optional[str] = None,
    output_dir: Optional[str] = None,
    suffix: Optional[str] = None,
) -> Path:
    if provided_path:
        path = apply_suffix(ensure_image_suffix(Path(provided_path).expanduser()), suffix)
        return ensure_parent_dir(path)

    base_dir = Path(output_dir).expanduser() if output_dir else default_output_dir(config)
    base_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    domain = url.replace("https://", "").replace("http://", "").split("/")[0].replace(".", "_")
    path = base_dir / f"screenshot_{domain}_{timestamp}.png"
    return apply_suffix(path, suffix)


def generate_report_path(
    url: str,
    config: ScreenshotConfig,
    provided_path: Optional[str] = None,
    output_dir: Optional[str] = None,
    suffix: Optional[str] = None,
) -> Path:
    if provided_path:
        path = apply_suffix(ensure_json_suffix(Path(provided_path).expanduser()), suffix)
        return ensure_parent_dir(path)

    base_dir = Path(output_dir).expanduser() if output_dir else default_output_dir(config)
    base_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    domain = url.replace("https://", "").replace("http://", "").split("/")[0].replace(".", "_")
    path = base_dir / f"capture_report_{domain}_{timestamp}.json"
    return apply_suffix(path, suffix)


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


def capture_label(device: Optional[str] = None) -> str:
    return f"[{device}] " if device else ""


def capture_primary(
    url: str,
    output_path: Path,
    config: ScreenshotConfig,
    mode: str,
    wait: bool,
    reporter: Reporter,
    label: str = "",
) -> Tuple[bool, List[str], Optional[str], str, bool]:
    reporter.log(f"{label}Attempting Primary API (Headless): {config.primary_api}")
    reporter.log(f"{label}Mode: {mode}, Wait: {wait}")

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
        reporter.log(f"{label}✅ Primary API Success")
        return True, [], None, mode, wait

    if output_path.exists():
        output_path.unlink()
    return False, [], "Primary API returned invalid data", mode, wait


def capture_fallback(
    url: str,
    output_path: Path,
    config: ScreenshotConfig,
    mode: str,
    wait: bool,
    reporter: Reporter,
    label: str = "",
) -> Tuple[bool, List[str], Optional[str], str, bool]:
    reporter.log(f"{label}Attempting Fallback API (AWS): {config.fallback_api}")

    warnings = []
    if mode == "fullpage":
        warnings.append("AWS fallback does not support explicit fullpage mode; result is best-effort only.")
        reporter.log(f"{label}⚠️ Note: AWS engine does not support explicit 'fullpage' mode settings.")
    if wait:
        warnings.append("AWS fallback does not support explicit wait mode; extra wait is ignored.")
        reporter.log(f"{label}⚠️ Note: AWS engine does not support explicit 'wait' settings.")

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
        message = data.get("message", "Unknown error") if isinstance(data, dict) else "Unknown error"
        return False, warnings, f"Fallback API response missing screenshot: {message}", "best-effort", False

    try:
        img_data = base64.b64decode(data["screenshot"])
        with open(output_path, "wb") as file_obj:
            file_obj.write(img_data)
    except Exception as exc:
        return False, warnings, f"Fallback API write error: {exc}", "best-effort", False

    if validate_png(output_path):
        reporter.log(f"{label}✅ Fallback API Success")
        return True, warnings, None, "best-effort", False

    if output_path.exists():
        output_path.unlink()
    return False, warnings, "Fallback API produced invalid PNG data", "best-effort", False


def execute_capture(
    url: str,
    output_path: Path,
    config: ScreenshotConfig,
    engine: str,
    mode: str,
    wait: bool,
    reporter: Reporter,
    device: Optional[str] = None,
) -> CaptureResult:
    label = capture_label(device)
    reporter.log(f"{label}Target: {url}")
    reporter.log(f"{label}Output: {output_path}")
    reporter.log(f"{label}Engine: {engine}")
    reporter.log(f"{label}Mode:   {mode}")
    reporter.log(f"{label}Wait:   {wait}")
    reporter.log(f"{label}Viewport: {config.viewport_width}x{config.viewport_height}")

    success = False
    warnings: List[str] = []
    error: Optional[str] = None
    engine_used: Optional[str] = None
    mode_effective: Optional[str] = mode
    wait_effective = wait

    if engine == "headless":
        success, warnings, error, mode_effective, wait_effective = capture_primary(
            url, output_path, config, mode, wait, reporter, label
        )
        engine_used = "headless"

    elif engine == "aws":
        success, warnings, error, mode_effective, wait_effective = capture_fallback(
            url, output_path, config, mode, wait, reporter, label
        )
        engine_used = "aws"

    else:
        success, warnings, error, mode_effective, wait_effective = capture_primary(
            url, output_path, config, mode, wait, reporter, label
        )
        engine_used = "headless"
        if not success:
            primary_error = error
            reporter.log(f"{label}🔄 Switching to Fallback Strategy...")
            (
                fallback_success,
                fallback_warnings,
                fallback_error,
                fallback_mode_effective,
                fallback_wait_effective,
            ) = capture_fallback(url, output_path, config, mode, wait, reporter, label)
            warnings.extend(fallback_warnings)
            if fallback_success:
                success = True
                engine_used = "aws"
                mode_effective = fallback_mode_effective
                wait_effective = fallback_wait_effective
                error = None
                warnings.insert(0, "Primary headless capture failed; fallback AWS engine was used.")
            else:
                error = f"Primary: {primary_error}; Fallback: {fallback_error or 'unknown error'}"

    file_size = output_path.stat().st_size if success and output_path.exists() else None
    image_width, image_height = read_png_dimensions(output_path) if success and output_path.exists() else (None, None)

    return CaptureResult(
        success=success,
        url=url,
        output_path=str(output_path),
        engine_requested=engine,
        engine_used=engine_used,
        mode_requested=mode,
        mode_effective=mode_effective,
        wait_requested=wait,
        wait_effective=wait_effective,
        viewport_width=config.viewport_width,
        viewport_height=config.viewport_height,
        file_size_bytes=file_size,
        image_width=image_width,
        image_height=image_height,
        device=device,
        warnings=warnings,
        error=error,
    )


def run_responsive_capture_set(url: str, args: argparse.Namespace, reporter: Reporter) -> CaptureSetResult:
    captures: List[CaptureResult] = []
    report_base_path = generate_report_path(
        url,
        load_config(),
        provided_path=args.report_file,
        output_dir=args.output_dir,
    ) if args.report_file else None
    for device_name in RESPONSIVE_CAPTURE_SET:
        config = load_config(device_name)
        output_path = generate_output_path(
            url,
            config,
            provided_path=args.output,
            output_dir=args.output_dir,
            suffix=device_name,
        )
        capture_result = execute_capture(
            url=url,
            output_path=output_path,
            config=config,
            engine=args.engine,
            mode=args.mode,
            wait=args.wait,
            reporter=reporter,
            device=device_name,
        )
        capture_result.report_path = write_report_file(
            capture_result,
            apply_suffix(report_base_path, device_name) if report_base_path else None,
        )
        captures.append(capture_result)

    successful_captures = sum(1 for capture in captures if capture.success)
    failed_captures = len(captures) - successful_captures
    warnings: List[str] = []
    error: Optional[str] = None

    if failed_captures:
        error = "One or more responsive captures failed. Check the per-device errors in `captures`."
        warnings.append("Responsive capture set is partially complete.")

    result = CaptureSetResult(
        success=failed_captures == 0,
        url=url,
        capture_set="responsive",
        engine_requested=args.engine,
        mode_requested=args.mode,
        wait_requested=args.wait,
        captures=captures,
        successful_captures=successful_captures,
        failed_captures=failed_captures,
        warnings=warnings,
        error=error,
    )
    result.report_path = write_report_file(result, report_base_path)
    return result


def load_plugin_version() -> Optional[str]:
    plugin_json_path = Path(__file__).parent / ".claude-plugin" / "plugin.json"
    if not plugin_json_path.exists():
        return None
    try:
        with open(plugin_json_path, "r", encoding="utf-8") as file_obj:
            return json.load(file_obj).get("version")
    except Exception:
        return None


def build_report_payload(result: Union[CaptureResult, CaptureSetResult], report_path: Path) -> dict:
    result_payload = asdict(result)
    result_payload["report_path"] = str(report_path)
    return {
        "report_schema": REPORT_SCHEMA,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "plugin_version": load_plugin_version(),
        "result_type": "capture_set" if isinstance(result, CaptureSetResult) else "capture",
        "report_path": str(report_path),
        "result": result_payload,
    }


def write_report_file(result: Union[CaptureResult, CaptureSetResult], report_path: Optional[Path]) -> Optional[str]:
    if not report_path:
        return None
    ensure_parent_dir(report_path)
    data = build_report_payload(result, report_path)
    with open(report_path, "w", encoding="utf-8") as file_obj:
        json.dump(data, file_obj, ensure_ascii=False)
    return str(report_path)


def emit_single_capture_text(result: CaptureResult, reporter: Reporter) -> None:
    if result.success:
        reporter.log(f"Screenshot saved: {result.output_path}")
        if result.file_size_bytes is not None:
            reporter.log(f"Size: {result.file_size_bytes:,} bytes")
        if result.image_width and result.image_height:
            reporter.log(f"Dimensions: {result.image_width}x{result.image_height}")
        if result.report_path:
            reporter.log(f"Report: {result.report_path}")
        if result.warnings:
            for warning in result.warnings:
                reporter.log(f"⚠️ {warning}")
        return

    if result.warnings:
        for warning in result.warnings:
            reporter.log(f"⚠️ {warning}")
    reporter.log(f"❌ Screenshot capture failed: {result.error}")


def emit_capture_set_text(result: CaptureSetResult, reporter: Reporter) -> None:
    reporter.log(
        f"Responsive capture set complete: {result.successful_captures}/{len(result.captures)} capture(s) succeeded"
    )
    for capture in result.captures:
        status = "✅" if capture.success else "❌"
        reporter.log(f"{status} {capture.device}: {capture.output_path}")
        if capture.file_size_bytes is not None:
            reporter.log(f"   Size: {capture.file_size_bytes:,} bytes")
        if capture.image_width and capture.image_height:
            reporter.log(f"   Dimensions: {capture.image_width}x{capture.image_height}")
        if capture.warnings:
            for warning in capture.warnings:
                reporter.log(f"   ⚠️ {warning}")
        if capture.report_path:
            reporter.log(f"   Report: {capture.report_path}")
        if capture.error:
            reporter.log(f"   Error: {capture.error}")

    if result.report_path:
        reporter.log(f"Capture-set report: {result.report_path}")
    if result.warnings:
        for warning in result.warnings:
            reporter.log(f"⚠️ {warning}")
    if result.error:
        reporter.log(f"❌ Capture set failed: {result.error}")


def emit_result(result: Union[CaptureResult, CaptureSetResult], output_format: str, reporter: Reporter) -> None:
    if output_format == "json":
        print(json.dumps(asdict(result), ensure_ascii=False))
        return

    if isinstance(result, CaptureSetResult):
        emit_capture_set_text(result, reporter)
        return

    emit_single_capture_text(result, reporter)


def main() -> None:
    parser = argparse.ArgumentParser(description="Hybrid Screenshot Tool")
    parser.add_argument("url", help="URL to capture")
    parser.add_argument("--output", "-o", help="Output file path or base file path when using --capture-set")
    parser.add_argument("--output-dir", help="Output directory for generated screenshots")
    parser.add_argument("--device", choices=["desktop", "tablet", "mobile"], help="Viewport preset override for focused frontend review")
    parser.add_argument("--capture-set", choices=["responsive"], help="Capture a predefined multi-device screenshot set in one run")
    parser.add_argument("--report-file", help="Write machine-readable capture metadata to a JSON report file")
    parser.add_argument("--engine", "-e", choices=["auto", "headless", "aws"], default="auto", help="Select screenshot engine (default: auto)")
    parser.add_argument("--mode", "-m", choices=["viewport", "fullpage"], default="fullpage", help="Capture mode: 'viewport' or 'fullpage' (default: fullpage)")
    parser.add_argument("--wait", "-w", action="store_true", help="Wait extra time for dynamic content (Headless engine only)")
    parser.add_argument("--output-format", choices=["text", "json"], default="text", help="Result output format (default: text)")
    args = parser.parse_args()

    if args.capture_set and args.device:
        raise SystemExit("--capture-set cannot be combined with --device. Use either one device or one capture set.")

    reporter = Reporter(args.output_format)
    url = normalize_url(args.url)

    if args.capture_set == "responsive":
        result: Union[CaptureResult, CaptureSetResult] = run_responsive_capture_set(url, args, reporter)
    else:
        config = load_config(args.device)
        output_path = generate_output_path(url, config, args.output, args.output_dir)
        result = execute_capture(
            url=url,
            output_path=output_path,
            config=config,
            engine=args.engine,
            mode=args.mode,
            wait=args.wait,
            reporter=reporter,
            device=args.device,
        )
        result.report_path = write_report_file(
            result,
            generate_report_path(url, config, args.report_file, args.output_dir) if args.report_file else None,
        )

    emit_result(result, args.output_format, reporter)
    sys.exit(0 if result.success else 1)


if __name__ == "__main__":
    main()
