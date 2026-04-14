"""Capture-domain authority surface for capture orchestration and compatibility exports."""

from __future__ import annotations

from typing import Any, Union

from .auth import AuthContext, build_auth_context, redact_auth_context
from .config import ScreenshotConfig, load_config
from .engines import build_fallback_request_headers, capture_fallback, capture_primary
from .models import CaptureResult, CaptureSetResult, Reporter
from .paths import (
    apply_suffix,
    default_output_dir,
    derive_neighbor_path,
    ensure_image_suffix,
    ensure_json_suffix,
    ensure_parent_dir,
    generate_bundle_path,
    generate_output_path,
    generate_report_path,
    normalize_url,
    read_png_dimensions,
    validate_png,
)
from .reporting import (
    build_evidence_bundle_payload,
    build_report_payload,
    emit_capture_set_text,
    emit_result,
    emit_single_capture_text,
    finalize_capture_artifacts,
    load_plugin_version,
    write_evidence_bundle_file,
    write_report_file,
)
from .runtime import RESPONSIVE_CAPTURE_SET, execute_capture, run_capture, run_responsive_capture_set
from .url_policy import validate_public_capture_url
from .witnesses import (
    build_capture_set_witness_index,
    build_semantic_page_summary,
    collect_html_witnesses,
    extract_title_from_html,
    html_to_text,
    normalize_witness_mode,
    response_summary,
    write_capture_set_witness_file,
    write_json_file,
    write_text_file,
)


def build_blocked_capture_result(args: Any, url: str, error: str) -> CaptureResult:
    config = load_config(getattr(args, "device", None))
    output_path = generate_output_path(url, config, getattr(args, "output", None), getattr(args, "output_dir", None))
    return CaptureResult(
        success=False,
        url=url,
        output_path=str(output_path),
        engine_requested=args.engine,
        engine_used=None,
        mode_requested=args.mode,
        mode_effective=None,
        wait_requested=args.wait,
        wait_effective=False,
        viewport_width=config.viewport_width,
        viewport_height=config.viewport_height,
        witness_mode=normalize_witness_mode(getattr(args, "witness_mode", "visual")),
        warnings=["Capture request was rejected before remote engine execution."],
        error=error,
    )



def build_blocked_capture_set_result(args: Any, url: str, error: str) -> CaptureSetResult:
    captures = []
    for device_name in RESPONSIVE_CAPTURE_SET:
        config = load_config(device_name)
        output_path = generate_output_path(
            url,
            config,
            provided_path=getattr(args, "output", None),
            output_dir=getattr(args, "output_dir", None),
            suffix=device_name,
        )
        captures.append(
            CaptureResult(
                success=False,
                url=url,
                output_path=str(output_path),
                engine_requested=args.engine,
                engine_used=None,
                mode_requested=args.mode,
                mode_effective=None,
                wait_requested=args.wait,
                wait_effective=False,
                viewport_width=config.viewport_width,
                viewport_height=config.viewport_height,
                witness_mode=normalize_witness_mode(getattr(args, "witness_mode", "frontend-default")),
                device=device_name,
                warnings=["Capture request was rejected before remote engine execution."],
                error=error,
            )
        )
    return CaptureSetResult(
        success=False,
        url=url,
        capture_set="responsive",
        engine_requested=args.engine,
        mode_requested=args.mode,
        wait_requested=args.wait,
        witness_mode=normalize_witness_mode(getattr(args, "witness_mode", "frontend-default")),
        captures=captures,
        successful_captures=0,
        failed_captures=len(captures),
        warnings=["Capture request was rejected before remote engine execution."],
        error=error,
    )



def capture_from_args(args: Any) -> Union[CaptureResult, CaptureSetResult]:
    reporter = Reporter(args.output_format)
    url = normalize_url(args.url)
    target_error = validate_public_capture_url(url)
    if target_error:
        if args.capture_set == "responsive":
            result: Union[CaptureResult, CaptureSetResult] = build_blocked_capture_set_result(args, url, target_error)
        else:
            result = build_blocked_capture_result(args, url, target_error)
    elif args.capture_set == "responsive":
        result = run_responsive_capture_set(url, args, reporter)
    else:
        result = run_capture(url, args, reporter)
    return finalize_capture_artifacts(args, url, result)


__all__ = [
    "AuthContext",
    "CaptureResult",
    "CaptureSetResult",
    "RESPONSIVE_CAPTURE_SET",
    "Reporter",
    "ScreenshotConfig",
    "apply_suffix",
    "build_auth_context",
    "build_capture_set_witness_index",
    "build_evidence_bundle_payload",
    "build_fallback_request_headers",
    "build_report_payload",
    "build_semantic_page_summary",
    "capture_fallback",
    "capture_from_args",
    "capture_primary",
    "collect_html_witnesses",
    "default_output_dir",
    "derive_neighbor_path",
    "emit_capture_set_text",
    "emit_result",
    "emit_single_capture_text",
    "ensure_image_suffix",
    "ensure_json_suffix",
    "ensure_parent_dir",
    "execute_capture",
    "extract_title_from_html",
    "finalize_capture_artifacts",
    "generate_bundle_path",
    "generate_output_path",
    "generate_report_path",
    "html_to_text",
    "load_config",
    "load_plugin_version",
    "normalize_url",
    "normalize_witness_mode",
    "read_png_dimensions",
    "redact_auth_context",
    "response_summary",
    "run_capture",
    "run_responsive_capture_set",
    "validate_png",
    "write_capture_set_witness_file",
    "write_evidence_bundle_file",
    "write_json_file",
    "write_report_file",
    "write_text_file",
]
