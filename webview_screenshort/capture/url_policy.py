from __future__ import annotations

import ipaddress
from urllib.parse import urlparse


BLOCKED_CAPTURE_TARGET_MESSAGE = (
    "Unsupported capture target: webview-screenshort currently supports only publicly reachable "
    "http(s) URLs. Local/private targets such as localhost, loopback addresses, and private network "
    "addresses are not reachable from the current remote capture engines. Use a public domain URL or "
    "expose the page through a public tunnel/domain before capture."
)


ALLOWED_SCHEMES = {"http", "https"}
BLOCKED_HOST_SUFFIXES = (
    ".internal",
    ".lan",
    ".local",
    ".localdomain",
    ".localhost",
    ".home",
)



def _is_blocked_ip_host(host: str) -> bool:
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        return False
    return any(
        (
            address.is_private,
            address.is_loopback,
            address.is_link_local,
            address.is_multicast,
            address.is_reserved,
            address.is_unspecified,
        )
    )



def validate_public_capture_url(url: str) -> str | None:
    parsed = urlparse(url)
    scheme = (parsed.scheme or "").lower()
    host = parsed.hostname

    if scheme not in ALLOWED_SCHEMES:
        return BLOCKED_CAPTURE_TARGET_MESSAGE
    if not host:
        return BLOCKED_CAPTURE_TARGET_MESSAGE

    normalized_host = host.rstrip(".").lower()
    if normalized_host == "localhost":
        return BLOCKED_CAPTURE_TARGET_MESSAGE
    if any(normalized_host.endswith(suffix) for suffix in BLOCKED_HOST_SUFFIXES):
        return BLOCKED_CAPTURE_TARGET_MESSAGE
    if "." not in normalized_host and not _is_blocked_ip_host(normalized_host):
        return BLOCKED_CAPTURE_TARGET_MESSAGE
    if _is_blocked_ip_host(normalized_host):
        return BLOCKED_CAPTURE_TARGET_MESSAGE

    return None


__all__ = [
    "BLOCKED_CAPTURE_TARGET_MESSAGE",
    "validate_public_capture_url",
]
