from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


@dataclass
class AuthContext:
    request_headers: Dict[str, str] = field(default_factory=dict)
    origin_forward_headers: Dict[str, str] = field(default_factory=dict)
    cookies: Dict[str, str] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)

    def has_auth_material(self) -> bool:
        return bool(self.request_headers or self.origin_forward_headers or self.cookies)


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


def _cookie_header(cookies: Dict[str, str]) -> Optional[str]:
    if not cookies:
        return None
    return "; ".join(f"{name}={value}" for name, value in cookies.items())


def build_auth_context(
    headers: Optional[Iterable[str]] = None,
    origin_headers: Optional[Iterable[str]] = None,
    cookies: Optional[Iterable[str]] = None,
    cookie_file: Optional[str] = None,
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

    if context.origin_forward_headers:
        context.warnings.append(
            "Origin-Header-Whitelist forwarding is documented only for Prerendercloud-* header names and disables the 5-minute server cache."
        )

    return context


def redact_auth_context(context: AuthContext) -> Dict[str, object]:
    return {
        "has_auth_material": context.has_auth_material(),
        "request_header_names": sorted(context.request_headers.keys()),
        "origin_forward_header_names": sorted(context.origin_forward_headers.keys()),
        "cookie_names": sorted(context.cookies.keys()),
        "warnings": list(context.warnings),
    }


__all__ = [
    "AuthContext",
    "build_auth_context",
    "redact_auth_context",
]
