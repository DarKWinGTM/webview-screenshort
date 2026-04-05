"""Compatibility shim for headless render API helpers."""

from .capture.headless_api import (
    HeadlessRenderApiClient,
    ResponsePayload,
    decode_body_from_json_payload,
    extract_metadata_from_json_payload,
)

__all__ = [
    "HeadlessRenderApiClient",
    "ResponsePayload",
    "decode_body_from_json_payload",
    "extract_metadata_from_json_payload",
]
