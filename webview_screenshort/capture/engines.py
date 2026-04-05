from __future__ import annotations

import base64
import json
import subprocess
from pathlib import Path
from typing import List, Optional, Tuple

from .auth import AuthContext
from .config import ScreenshotConfig
from .models import Reporter
from .paths import validate_png


def build_fallback_request_headers(config: ScreenshotConfig, auth_context: Optional[AuthContext]) -> List[str]:
    headers = [
        "-H", f"content-type: {config.fallback_content_type}",
        "-H", f"origin: {config.fallback_origin}",
        "-H", f"referer: {config.fallback_referer}",
    ]
    if auth_context:
        for name, value in auth_context.request_headers.items():
            headers.extend(["-H", f"{name}: {value}"])
        if auth_context.origin_forward_headers:
            headers.extend(["-H", f"Origin-Header-Whitelist: {', '.join(sorted(auth_context.origin_forward_headers.keys()))}"])
            for name, value in auth_context.origin_forward_headers.items():
                headers.extend(["-H", f"{name}: {value}"])
    return headers


def capture_primary(url: str, output_path: Path, config: ScreenshotConfig, mode: str, wait: bool, reporter: Reporter, label: str = "", auth_context: Optional[AuthContext] = None) -> Tuple[bool, List[str], Optional[str], str, bool]:
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
    if config.prerender_token:
        cmd.extend(["-H", f"X-Prerender-Token: {config.prerender_token}"])
    if wait:
        cmd.extend(["-H", "prerender-wait-extra-long: true"])
    if auth_context:
        for name, value in auth_context.request_headers.items():
            cmd.extend(["-H", f"{name}: {value}"])
        if auth_context.origin_forward_headers:
            cmd.extend(["-H", f"Origin-Header-Whitelist: {', '.join(sorted(auth_context.origin_forward_headers.keys()))}"])
            for name, value in auth_context.origin_forward_headers.items():
                cmd.extend(["-H", f"{name}: {value}"])
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


def capture_fallback(url: str, output_path: Path, config: ScreenshotConfig, mode: str, wait: bool, reporter: Reporter, label: str = "", auth_context: Optional[AuthContext] = None) -> Tuple[bool, List[str], Optional[str], str, bool]:
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
        *build_fallback_request_headers(config, auth_context),
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


__all__ = [
    "build_fallback_request_headers",
    "capture_fallback",
    "capture_primary",
]
