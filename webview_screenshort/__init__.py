"""Internal runtime package for webview-screenshort."""

from .capture.auth import AuthContext, build_auth_context, redact_auth_context
from .capture.service import (
    CaptureResult,
    CaptureSetResult,
    Reporter,
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
from .compare.reports import build_comparison_result_from_paths
from .compare.sessions import build_compare_session_payload
from .qa.gate import apply_gate, load_policy
from .qa.policies import list_policy_preset_records, resolve_policy_preset_record
from .qa.verdicts import build_verdict_from_payload
from .references.bundles import apply_reference_bundle, write_reference_bundle
from .references.live import reference_live_bundle, reference_live_gate

__all__ = [
    "AuthContext",
    "CaptureResult",
    "CaptureSetResult",
    "Reporter",
    "apply_gate",
    "apply_reference_bundle",
    "build_auth_context",
    "build_comparison_result_from_paths",
    "build_compare_session_payload",
    "build_verdict_from_payload",
    "capture_from_args",
    "emit_result",
    "generate_bundle_path",
    "generate_output_path",
    "generate_report_path",
    "list_policy_preset_records",
    "load_policy",
    "redact_auth_context",
    "reference_live_bundle",
    "reference_live_gate",
    "resolve_policy_preset_record",
    "run_capture",
    "run_responsive_capture_set",
    "write_evidence_bundle_file",
    "write_reference_bundle",
    "write_report_file",
]
