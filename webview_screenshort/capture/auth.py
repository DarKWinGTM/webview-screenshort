from __future__ import annotations

import base64
import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

PRELOADED_STATE_VERSION = "1"
PRELOADED_STATE_ENCODING = "base64url-json"
PRELOADED_STATE_HEADER_PREFIX = "Prerendercloud-Preloaded-State"
PRELOADED_STATE_CHUNK_BYTES = 1024
PRELOADED_STATE_MAX_RAW_BYTES = 3072
PRELOADED_STATE_MAX_CHUNKS = 4
FORWARDED_HEADER_BUDGET_BYTES = 6144


@dataclass
class PreloadedStateContext:
    source_kind: str
    top_level_keys: List[str]
    raw_bytes: int
    encoded_bytes: int
    chunk_count: int
    sha256: str
    estimated_forwarded_header_bytes: int
    origin_forward_headers: Dict[str, str] = field(default_factory=dict)


@dataclass
class AuthContext:
    request_headers: Dict[str, str] = field(default_factory=dict)
    origin_forward_headers: Dict[str, str] = field(default_factory=dict)
    cookies: Dict[str, str] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    manual_origin_forward_header_names: List[str] = field(default_factory=list)
    preloaded_state: Optional[PreloadedStateContext] = None

    def has_auth_material(self) -> bool:
        return bool(self.request_headers or self.origin_forward_headers or self.cookies or self.preloaded_state)


def _split_header(value: str) -> Tuple[str, str]:
    if ":" in value:
        name, raw_value = value.split(":", 1)
    elif "=" in value:
        name, raw_value = value.split("=", 1)
    else:
        raise ValueError(f"Invalid header format: {value}")
    name = name.strip()
    raw_value = raw_value.strip()
    if not name:
        raise ValueError(f"Header name is empty: {value}")
    return name, raw_value


def _parse_cookie_pair(value: str) -> Tuple[str, str]:
    if "=" not in value:
        raise ValueError(f"Invalid cookie format: {value}")
    name, raw_value = value.split("=", 1)
    name = name.strip()
    raw_value = raw_value.strip()
    if not name:
        raise ValueError(f"Cookie name is empty: {value}")
    return name, raw_value


def _read_cookie_file(path: Path) -> Dict[str, str]:
    text = path.read_text(encoding="utf-8")
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        cookies: Dict[str, str] = {}
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            name, value = _parse_cookie_pair(line)
            cookies[name] = value
        return cookies

    if isinstance(payload, dict):
        return {str(name): str(value) for name, value in payload.items()}
    if isinstance(payload, list):
        cookies: Dict[str, str] = {}
        for item in payload:
            if not isinstance(item, dict):
                continue
            name = str(item.get("name") or "").strip()
            value = str(item.get("value") or "")
            if name:
                cookies[name] = value
        return cookies
    raise ValueError(f"Unsupported cookie file structure: {path}")


def _read_preloaded_state_file(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    payload = json.loads(text)
    if not isinstance(payload, dict):
        raise ValueError(f"Preloaded state file must contain a JSON object: {path}")
    return payload


def _cookie_header(cookies: Dict[str, str]) -> Optional[str]:
    if not cookies:
        return None
    return "; ".join(f"{name}={value}" for name, value in cookies.items())


def _estimate_header_bytes(headers: Dict[str, str]) -> int:
    total = 0
    for name, value in headers.items():
        total += len(name.encode("utf-8")) + len(str(value).encode("utf-8")) + 4
    return total


def _encode_preloaded_state(payload: Dict[str, Any]) -> Tuple[bytes, str, str]:
    canonical = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")
    encoded = base64.urlsafe_b64encode(canonical).decode("ascii").rstrip("=")
    digest = hashlib.sha256(canonical).hexdigest()
    return canonical, encoded, digest


def _chunk_encoded_state(encoded: str) -> List[str]:
    return [encoded[i:i + PRELOADED_STATE_CHUNK_BYTES] for i in range(0, len(encoded), PRELOADED_STATE_CHUNK_BYTES)]


def _build_preloaded_state_context(
    payload: Dict[str, Any],
    *,
    source_kind: str,
    existing_request_headers: Dict[str, str],
    existing_origin_headers: Dict[str, str],
) -> PreloadedStateContext:
    canonical, encoded, digest = _encode_preloaded_state(payload)
    raw_bytes = len(canonical)
    if raw_bytes > PRELOADED_STATE_MAX_RAW_BYTES:
        raise ValueError(
            f"Preloaded state is too large: {raw_bytes} bytes (max {PRELOADED_STATE_MAX_RAW_BYTES})"
        )

    chunks = _chunk_encoded_state(encoded)
    if len(chunks) > PRELOADED_STATE_MAX_CHUNKS:
        raise ValueError(
            f"Preloaded state requires {len(chunks)} chunks (max {PRELOADED_STATE_MAX_CHUNKS}); reduce the payload size"
        )

    generated_headers: Dict[str, str] = {
        f"{PRELOADED_STATE_HEADER_PREFIX}-Version": PRELOADED_STATE_VERSION,
        f"{PRELOADED_STATE_HEADER_PREFIX}-Encoding": PRELOADED_STATE_ENCODING,
        f"{PRELOADED_STATE_HEADER_PREFIX}-Sha256": digest,
        f"{PRELOADED_STATE_HEADER_PREFIX}-Chunks": str(len(chunks)),
    }
    for index, chunk in enumerate(chunks, start=1):
        generated_headers[f"{PRELOADED_STATE_HEADER_PREFIX}-{index:02d}"] = chunk

    conflicts = sorted(set(existing_origin_headers) & set(generated_headers))
    if conflicts:
        raise ValueError(
            "Preloaded state generated origin headers conflict with operator-provided headers: " + ", ".join(conflicts)
        )

    estimated_bytes = _estimate_header_bytes(existing_request_headers) + _estimate_header_bytes({**existing_origin_headers, **generated_headers})
    if estimated_bytes > FORWARDED_HEADER_BUDGET_BYTES:
        raise ValueError(
            f"Combined forwarded header budget too large: {estimated_bytes} bytes (max {FORWARDED_HEADER_BUDGET_BYTES})"
        )

    return PreloadedStateContext(
        source_kind=source_kind,
        top_level_keys=sorted(str(key) for key in payload.keys()),
        raw_bytes=raw_bytes,
        encoded_bytes=len(encoded.encode("utf-8")),
        chunk_count=len(chunks),
        sha256=digest,
        estimated_forwarded_header_bytes=estimated_bytes,
        origin_forward_headers=generated_headers,
    )


def _load_preloaded_state(
    preloaded_state_json: Optional[str],
    preloaded_state_file: Optional[str],
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    if preloaded_state_json and preloaded_state_file:
        raise ValueError("Use either --preloaded-state-json or --preloaded-state-file, not both")
    if preloaded_state_json:
        payload = json.loads(preloaded_state_json)
        if not isinstance(payload, dict):
            raise ValueError("Preloaded state JSON must be a JSON object")
        return payload, "inline_json"
    if preloaded_state_file:
        return _read_preloaded_state_file(Path(preloaded_state_file).expanduser()), "file"
    return None, None


def build_auth_context(
    headers: Optional[Iterable[str]] = None,
    origin_headers: Optional[Iterable[str]] = None,
    cookies: Optional[Iterable[str]] = None,
    cookie_file: Optional[str] = None,
    preloaded_state_json: Optional[str] = None,
    preloaded_state_file: Optional[str] = None,
) -> AuthContext:
    context = AuthContext()

    for raw in headers or []:
        name, value = _split_header(raw)
        context.request_headers[name] = value

    for raw in origin_headers or []:
        name, value = _split_header(raw)
        if not name.lower().startswith("prerendercloud-"):
            raise ValueError(
                f"Origin-forwarded headers must start with 'Prerendercloud-': {name}"
            )
        context.origin_forward_headers[name] = value
        context.manual_origin_forward_header_names.append(name)

    for raw in cookies or []:
        name, value = _parse_cookie_pair(raw)
        context.cookies[name] = value

    if cookie_file:
        file_cookies = _read_cookie_file(Path(cookie_file).expanduser())
        context.cookies.update(file_cookies)

    cookie_header = _cookie_header(context.cookies)
    if cookie_header:
        context.request_headers.setdefault("Cookie", cookie_header)
        context.warnings.append(
            "Cookie forwarding to authenticated pages is best-effort and depends on target-site and renderer behavior."
        )

    preload_payload, preload_source_kind = _load_preloaded_state(preloaded_state_json, preloaded_state_file)
    if preload_payload is not None and preload_source_kind is not None:
        preload_context = _build_preloaded_state_context(
            preload_payload,
            source_kind=preload_source_kind,
            existing_request_headers=context.request_headers,
            existing_origin_headers=context.origin_forward_headers,
        )
        context.preloaded_state = preload_context
        context.origin_forward_headers.update(preload_context.origin_forward_headers)
        context.warnings.append(
            "Preloaded state replay is bounded origin-bootstrap input only; the target app must reconstruct it and emit window.__PRELOADED_STATE__."
        )
        context.warnings.append(
            "Preloaded state replay does not imply direct browser localStorage/sessionStorage injection by the provider."
        )

    if context.origin_forward_headers:
        context.warnings.append(
            "Origin-Header-Whitelist forwarding is documented only for Prerendercloud-* header names and disables the 5-minute server cache."
        )

    return context


def redact_auth_context(context: AuthContext) -> Dict[str, object]:
    redacted = {
        "has_auth_material": context.has_auth_material(),
        "request_header_names": sorted(context.request_headers.keys()),
        "origin_forward_header_names": sorted(context.origin_forward_headers.keys()),
        "manual_origin_forward_header_names": sorted(context.manual_origin_forward_header_names),
        "cookie_names": sorted(context.cookies.keys()),
        "warnings": list(context.warnings),
    }
    if context.preloaded_state:
        redacted.update(
            {
                "has_preloaded_state": True,
                "preloaded_state_source_kind": context.preloaded_state.source_kind,
                "preloaded_state_transport": "origin_header",
                "preloaded_state_top_level_keys": list(context.preloaded_state.top_level_keys),
                "preloaded_state_raw_bytes": context.preloaded_state.raw_bytes,
                "preloaded_state_encoded_bytes": context.preloaded_state.encoded_bytes,
                "preloaded_state_chunk_count": context.preloaded_state.chunk_count,
                "preloaded_state_sha256_prefix": context.preloaded_state.sha256[:12],
                "estimated_forwarded_header_bytes": context.preloaded_state.estimated_forwarded_header_bytes,
            }
        )
    else:
        redacted["has_preloaded_state"] = False
    return redacted


__all__ = [
    "AuthContext",
    "PreloadedStateContext",
    "build_auth_context",
    "redact_auth_context",
]
