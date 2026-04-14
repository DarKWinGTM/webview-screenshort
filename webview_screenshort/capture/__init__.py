"""Capture domain package for webview-screenshort."""

from .auth import AuthContext, build_auth_context, redact_auth_context
from .headless_api import HeadlessRenderApiClient, ResponsePayload, decode_body_from_json_payload, extract_metadata_from_json_payload
from .url_policy import BLOCKED_CAPTURE_TARGET_MESSAGE, validate_public_capture_url

__all__ = [
    "AuthContext",
    "BLOCKED_CAPTURE_TARGET_MESSAGE",
    "HeadlessRenderApiClient",
    "ResponsePayload",
    "build_auth_context",
    "decode_body_from_json_payload",
    "extract_metadata_from_json_payload",
    "redact_auth_context",
    "validate_public_capture_url",
]
