"""Internal runtime package for webview-screenshort."""

from .auth_context import AuthContext, build_auth_context, redact_auth_context
from .capture_service import (
    CaptureResult,
    CaptureSetResult,
    capture_from_args,
    emit_result,
    generate_bundle_path,
    generate_report_path,
    generate_output_path,
    run_capture,
    run_responsive_capture_set,
    write_evidence_bundle_file,
    write_report_file,
)

__all__ = [
    "AuthContext",
    "CaptureResult",
    "CaptureSetResult",
    "build_auth_context",
    "capture_from_args",
    "emit_result",
    "generate_bundle_path",
    "generate_output_path",
    "generate_report_path",
    "redact_auth_context",
    "run_capture",
    "run_responsive_capture_set",
    "write_evidence_bundle_file",
    "write_report_file",
]
