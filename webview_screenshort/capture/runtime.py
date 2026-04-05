from __future__ import annotations

from pathlib import Path
from typing import Any, List, Optional, Tuple, Union

from .auth import AuthContext, build_auth_context, redact_auth_context
from .config import ScreenshotConfig, load_config
from .engines import capture_fallback, capture_primary
from .models import CaptureResult, CaptureSetResult, Reporter, capture_label, empty_html_witnesses
from .paths import generate_output_path, generate_report_path, read_png_dimensions
from .witnesses import build_capture_set_witness_index, collect_html_witnesses, normalize_witness_mode, write_capture_set_witness_file

RESPONSIVE_CAPTURE_SET = ("desktop", "tablet", "mobile")


def execute_capture(url: str, output_path: Path, config: ScreenshotConfig, engine: str, mode: str, wait: bool, reporter: Reporter, device: Optional[str] = None, witness_mode: str = "visual", auth_context: Optional[AuthContext] = None) -> CaptureResult:
    witness_mode = normalize_witness_mode(witness_mode)
    label = capture_label(device)
    reporter.log(f"{label}Target: {url}")
    reporter.log(f"{label}Output: {output_path}")
    reporter.log(f"{label}Engine: {engine}")
    reporter.log(f"{label}Mode:   {mode}")
    reporter.log(f"{label}Wait:   {wait}")
    reporter.log(f"{label}Witness mode: {witness_mode}")
    reporter.log(f"{label}Viewport: {config.viewport_width}x{config.viewport_height}")

    success = False
    warnings: List[str] = []
    error: Optional[str] = None
    engine_used: Optional[str] = None
    mode_effective: Optional[str] = mode
    wait_effective = wait

    if engine == "headless":
        success, warnings, error, mode_effective, wait_effective = capture_primary(url, output_path, config, mode, wait, reporter, label, auth_context)
        engine_used = "headless"
    elif engine == "aws":
        success, warnings, error, mode_effective, wait_effective = capture_fallback(url, output_path, config, mode, wait, reporter, label, auth_context)
        engine_used = "aws"
    else:
        success, warnings, error, mode_effective, wait_effective = capture_primary(url, output_path, config, mode, wait, reporter, label, auth_context)
        engine_used = "headless"
        if not success:
            primary_error = error
            reporter.log(f"{label}🔄 Switching to Fallback Strategy...")
            fallback_success, fallback_warnings, fallback_error, fallback_mode_effective, fallback_wait_effective = capture_fallback(url, output_path, config, mode, wait, reporter, label, auth_context)
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

    html_witnesses = empty_html_witnesses()
    if success:
        html_witnesses = collect_html_witnesses(
            url=url,
            config=config,
            wait=wait,
            witness_mode=witness_mode,
            output_path=output_path,
            auth_context=auth_context,
            warnings=warnings,
        )

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
        witness_mode=witness_mode,
        file_size_bytes=file_size,
        image_width=image_width,
        image_height=image_height,
        device=device,
        rendered_html_path=html_witnesses["rendered_html_path"],
        rendered_text_path=html_witnesses["rendered_text_path"],
        prerendered_html_path=html_witnesses["prerendered_html_path"],
        metadata_path=html_witnesses["metadata_path"],
        acquisition_path=html_witnesses["acquisition_path"],
        semantic_page_path=html_witnesses["semantic_page_path"],
        title=html_witnesses["title"],
        page_metadata=html_witnesses["page_metadata"],
        acquisition_summary=html_witnesses["acquisition_summary"],
        semantic_page_summary=html_witnesses["semantic_page_summary"],
        auth_summary=redact_auth_context(auth_context) if auth_context else None,
        warnings=warnings,
        error=error,
    )


def run_capture(url: str, args: Any, reporter: Reporter) -> CaptureResult:
    config = load_config(args.device)
    output_path = generate_output_path(url, config, args.output, args.output_dir)
    auth_context = build_auth_context(
        headers=getattr(args, "header", None),
        origin_headers=getattr(args, "origin_header", None),
        cookies=getattr(args, "cookie", None),
        cookie_file=getattr(args, "cookie_file", None),
        preloaded_state_json=getattr(args, "preloaded_state_json", None),
        preloaded_state_file=getattr(args, "preloaded_state_file", None),
    )
    return execute_capture(
        url=url,
        output_path=output_path,
        config=config,
        engine=args.engine,
        mode=args.mode,
        wait=args.wait,
        reporter=reporter,
        device=args.device,
        witness_mode=normalize_witness_mode(getattr(args, "witness_mode", "visual")),
        auth_context=auth_context,
    )


def run_responsive_capture_set(url: str, args: Any, reporter: Reporter) -> CaptureSetResult:
    captures: List[CaptureResult] = []
    shared_config = load_config()
    report_base_path = generate_report_path(url, shared_config, provided_path=args.report_file, output_dir=args.output_dir) if args.report_file else None
    witness_base_path = report_base_path or generate_report_path(url, shared_config, None, args.output_dir)

    from .reporting import write_report_file

    for device_name in RESPONSIVE_CAPTURE_SET:
        config = load_config(device_name)
        output_path = generate_output_path(url, config, provided_path=args.output, output_dir=args.output_dir, suffix=device_name)
        auth_context = build_auth_context(
            headers=getattr(args, "header", None),
            origin_headers=getattr(args, "origin_header", None),
            cookies=getattr(args, "cookie", None),
            cookie_file=getattr(args, "cookie_file", None),
            preloaded_state_json=getattr(args, "preloaded_state_json", None),
            preloaded_state_file=getattr(args, "preloaded_state_file", None),
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
            witness_mode=normalize_witness_mode(getattr(args, "witness_mode", "frontend-default")),
            auth_context=auth_context,
        )
        capture_result.report_path = write_report_file(capture_result, generate_report_path(url, shared_config, provided_path=args.report_file, output_dir=args.output_dir, suffix=device_name) if report_base_path else None)
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
        witness_mode=normalize_witness_mode(getattr(args, "witness_mode", "frontend-default")),
        captures=captures,
        successful_captures=successful_captures,
        failed_captures=failed_captures,
        warnings=warnings,
        error=error,
    )
    result.acquisition_path = write_capture_set_witness_file(witness_base_path, "capture_set_acquisition", build_capture_set_witness_index(captures, "acquisition_summary"))
    result.semantic_page_path = write_capture_set_witness_file(witness_base_path, "capture_set_semantic", build_capture_set_witness_index(captures, "semantic_page_summary"))
    result.report_path = write_report_file(result, report_base_path)
    return result


__all__ = [
    "RESPONSIVE_CAPTURE_SET",
    "execute_capture",
    "run_capture",
    "run_responsive_capture_set",
]
