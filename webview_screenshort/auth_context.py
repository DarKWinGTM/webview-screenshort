"""Compatibility shim for auth-context helpers."""

from .capture.auth import AuthContext, build_auth_context, redact_auth_context

__all__ = [
    "AuthContext",
    "build_auth_context",
    "redact_auth_context",
]
