from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Union

from ..schemas import EVIDENCE_BUNDLE_SCHEMA, REPORT_SCHEMA
from .config import load_config
from .models import CaptureResult, CaptureSetResult, Reporter
from .paths import generate_bundle_path, generate_report_path
from .witnesses import build_capture_set_witness_index


def load_plugin_version() -> Optional[str]:
    plugin_json_path = Path(__file__).resolve().parent.parent.parent / ".claude-plugin" / "plugin.json"
    if not plugin_json_path.exists():
        return None
    try:
        with open(plugin_json_path, "r", encoding="utf-8") as file_obj:
            return json.load(file_obj).get("version")
    except Exception:
        return None


def build_report_payload(result: Union[CaptureResult, CaptureSetResult], report_path: Path) -> Dict[str, Any]:
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


def build_evidence_bundle_payload(result: Union[CaptureResult, CaptureSetResult], bundle_path: Path) -> Dict[str, Any]:
    captures = result.captures if isinstance(result, CaptureSetResult) else [result]
    page_titles = [capture.title for capture in captures if capture.title]
    auth_summaries = [capture.auth_summary for capture in captures if capture.auth_summary]
    artifacts = []
    semantic_index = build_capture_set_witness_index(captures, "semantic_page_summary")
    acquisition_index = build_capture_set_witness_index(captures, "acquisition_summary")
    for capture in captures:
        artifacts.append(
            {
                "device": capture.device or "default",
                "screenshot_path": capture.output_path,
                "rendered_html_path": capture.rendered_html_path,
                "rendered_text_path": capture.rendered_text_path,
                "prerendered_html_path": capture.prerendered_html_path,
                "metadata_path": capture.metadata_path,
                "acquisition_path": capture.acquisition_path,
                "semantic_page_path": capture.semantic_page_path,
                "semantic_page_summary": capture.semantic_page_summary,
            }
        )
    return {
        "bundle_schema": EVIDENCE_BUNDLE_SCHEMA,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "plugin_version": load_plugin_version(),
        "bundle_path": str(bundle_path),
        "request": {
            "url": result.url,
            "mode": result.mode_requested,
            "wait": result.wait_requested,
            "engine_requested": result.engine_requested,
            "witness_mode": result.witness_mode,
            "capture_set": getattr(result, "capture_set", None),
        },
        "page": {
            "title": page_titles[0] if page_titles else None,
            "metadata": captures[0].page_metadata if captures and captures[0].page_metadata else {},
            "semantic_page_summary": captures[0].semantic_page_summary if len(captures) == 1 else {},
            "semantic_capture_index": semantic_index if len(captures) > 1 else {},
            "acquisition_capture_index": acquisition_index if len(captures) > 1 else {},
        },
        "auth": auth_summaries[0] if auth_summaries else {"has_auth_material": False},
        "artifacts": artifacts,
        "report_compat": {
            "report_path": result.report_path,
            "report_schema": REPORT_SCHEMA if result.report_path else None,
        },
        "result": asdict(result),
    }


def write_report_file(result: Union[CaptureResult, CaptureSetResult], report_path: Optional[Path]) -> Optional[str]:
    if not report_path:
        return None
    report_path.parent.mkdir(parents=True, exist_ok=True)
    data = build_report_payload(result, report_path)
    with open(report_path, "w", encoding="utf-8") as file_obj:
        json.dump(data, file_obj, ensure_ascii=False)
    return str(report_path)


def write_evidence_bundle_file(result: Union[CaptureResult, CaptureSetResult], bundle_path: Optional[Path]) -> Optional[str]:
    if not bundle_path:
        return None
    bundle_path.parent.mkdir(parents=True, exist_ok=True)
    data = build_evidence_bundle_payload(result, bundle_path)
    with open(bundle_path, "w", encoding="utf-8") as file_obj:
        json.dump(data, file_obj, ensure_ascii=False)
    return str(bundle_path)


def emit_single_capture_text(result: CaptureResult, reporter: Reporter) -> None:
    if result.success:
        reporter.log(f"Screenshot saved: {result.output_path}")
        if result.file_size_bytes is not None:
            reporter.log(f"Size: {result.file_size_bytes:,} bytes")
        if result.image_width and result.image_height:
            reporter.log(f"Dimensions: {result.image_width}x{result.image_height}")
        if result.rendered_html_path:
            reporter.log(f"Rendered HTML: {result.rendered_html_path}")
        if result.rendered_text_path:
            reporter.log(f"Rendered text: {result.rendered_text_path}")
        if result.prerendered_html_path:
            reporter.log(f"Prerendered HTML: {result.prerendered_html_path}")
        if result.metadata_path:
            reporter.log(f"Metadata witness: {result.metadata_path}")
        if result.acquisition_path:
            reporter.log(f"Acquisition witness: {result.acquisition_path}")
        if result.semantic_page_path:
            reporter.log(f"Semantic page witness: {result.semantic_page_path}")
        if result.report_path:
            reporter.log(f"Report: {result.report_path}")
        if result.bundle_path:
            reporter.log(f"Evidence bundle: {result.bundle_path}")
        if result.warnings:
            for warning in result.warnings:
                reporter.log(f"⚠️ {warning}")
        return
    if result.warnings:
        for warning in result.warnings:
            reporter.log(f"⚠️ {warning}")
    reporter.log(f"❌ Screenshot capture failed: {result.error}")


def emit_capture_set_text(result: CaptureSetResult, reporter: Reporter) -> None:
    reporter.log(f"Responsive capture set complete: {result.successful_captures}/{len(result.captures)} capture(s) succeeded")
    for capture in result.captures:
        status = "✅" if capture.success else "❌"
        reporter.log(f"{status} {capture.device}: {capture.output_path}")
        if capture.file_size_bytes is not None:
            reporter.log(f"   Size: {capture.file_size_bytes:,} bytes")
        if capture.image_width and capture.image_height:
            reporter.log(f"   Dimensions: {capture.image_width}x{capture.image_height}")
        if capture.rendered_html_path:
            reporter.log(f"   Rendered HTML: {capture.rendered_html_path}")
        if capture.rendered_text_path:
            reporter.log(f"   Rendered text: {capture.rendered_text_path}")
        if capture.prerendered_html_path:
            reporter.log(f"   Prerendered HTML: {capture.prerendered_html_path}")
        if capture.metadata_path:
            reporter.log(f"   Metadata witness: {capture.metadata_path}")
        if capture.acquisition_path:
            reporter.log(f"   Acquisition witness: {capture.acquisition_path}")
        if capture.semantic_page_path:
            reporter.log(f"   Semantic page witness: {capture.semantic_page_path}")
        if capture.warnings:
            for warning in capture.warnings:
                reporter.log(f"   ⚠️ {warning}")
        if capture.report_path:
            reporter.log(f"   Report: {capture.report_path}")
        if capture.error:
            reporter.log(f"   Error: {capture.error}")
    if result.acquisition_path:
        reporter.log(f"Capture-set acquisition witness: {result.acquisition_path}")
    if result.semantic_page_path:
        reporter.log(f"Capture-set semantic witness: {result.semantic_page_path}")
    if result.report_path:
        reporter.log(f"Capture-set report: {result.report_path}")
    if result.bundle_path:
        reporter.log(f"Evidence bundle: {result.bundle_path}")
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


def finalize_capture_artifacts(args: Any, url: str, result: Union[CaptureResult, CaptureSetResult]) -> Union[CaptureResult, CaptureSetResult]:
    if isinstance(result, CaptureSetResult):
        pass
    else:
        config = load_config(getattr(args, "device", None))
        report_file = getattr(args, "report_file", None)
        output_dir = getattr(args, "output_dir", None)
        result.report_path = write_report_file(result, generate_report_path(url, config, report_file, output_dir) if report_file else None)

    bundle_file = getattr(args, "bundle_file", None)
    output_dir = getattr(args, "output_dir", None)
    if bundle_file:
        config = load_config(getattr(args, "device", None))
        bundle_path = generate_bundle_path(url, config, bundle_file, output_dir)
    elif getattr(args, "witness_mode", "visual") != "visual":
        config = load_config(getattr(args, "device", None))
        bundle_path = generate_bundle_path(url, config, None, output_dir)
    else:
        bundle_path = None
    bundle_written = write_evidence_bundle_file(result, bundle_path)
    result.bundle_path = bundle_written
    return result


__all__ = [
    "build_evidence_bundle_payload",
    "build_report_payload",
    "emit_result",
    "emit_capture_set_text",
    "emit_single_capture_text",
    "finalize_capture_artifacts",
    "load_plugin_version",
    "write_evidence_bundle_file",
    "write_report_file",
]
