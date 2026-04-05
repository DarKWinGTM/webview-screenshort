from __future__ import annotations

import base64
import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Dict, Optional

from .auth import AuthContext

JSON_DICT = Dict[str, Any]


@dataclass
class ResponsePayload:
    ok: bool
    status_code: Optional[int]
    content_type: str
    body_bytes: bytes
    body_text: str
    json_payload: Optional[Dict[str, Any]]
    error: Optional[str] = None


class HeadlessRenderApiClient:
    def __init__(self, token: Optional[str] = None):
        self.token = token or ""

    def _build_headers(
        self,
        auth: Optional[AuthContext],
        *,
        wait: bool = False,
        device_width: Optional[int] = None,
        device_height: Optional[int] = None,
        viewport_width: Optional[int] = None,
        viewport_height: Optional[int] = None,
        screenshot_format: Optional[str] = None,
        with_metadata: bool = False,
        with_screenshot: bool = False,
        block_cookies: bool = False,
    ) -> Dict[str, str]:
        headers: Dict[str, str] = {
            "Accept-Encoding": "identity",
        }
        if self.token:
            headers["X-Prerender-Token"] = self.token
        if wait:
            headers["Prerender-Wait-Extra-Long"] = "true"
        if block_cookies:
            headers["Prerender-Block-Cookies"] = "true"
        if device_width is not None:
            headers["Prerender-Device-Width"] = str(device_width)
        if device_height is not None:
            headers["Prerender-Device-Height"] = str(device_height)
        if viewport_width is not None:
            headers["Prerender-Viewport-Width"] = str(viewport_width)
        if viewport_height is not None:
            headers["Prerender-Viewport-Height"] = str(viewport_height)
        if screenshot_format:
            headers["Prerender-Screenshot-Format"] = screenshot_format
        if with_metadata:
            headers["Prerender-With-Metadata"] = "true"
        if with_screenshot:
            headers["Prerender-With-Screenshot"] = "true"
        if auth:
            headers.update(auth.request_headers)
            if auth.origin_forward_headers:
                headers["Origin-Header-Whitelist"] = ", ".join(sorted(auth.origin_forward_headers.keys()))
                headers.update(auth.origin_forward_headers)
        return headers

    def _request(self, url: str, headers: Dict[str, str], timeout_sec: int) -> ResponsePayload:
        request = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(request, timeout=timeout_sec) as response:
                body_bytes = response.read()
                content_type = response.headers.get("content-type", "")
                body_text = body_bytes.decode("utf-8", "replace")
                json_payload = None
                if "json" in content_type.lower():
                    try:
                        json_payload = json.loads(body_text)
                    except json.JSONDecodeError:
                        json_payload = None
                return ResponsePayload(
                    ok=True,
                    status_code=response.status,
                    content_type=content_type,
                    body_bytes=body_bytes,
                    body_text=body_text,
                    json_payload=json_payload,
                )
        except urllib.error.HTTPError as error:
            body_bytes = error.read()
            content_type = error.headers.get("content-type", "")
            body_text = body_bytes.decode("utf-8", "replace")
            json_payload = None
            if "json" in content_type.lower():
                try:
                    json_payload = json.loads(body_text)
                except json.JSONDecodeError:
                    json_payload = None
            return ResponsePayload(
                ok=False,
                status_code=error.code,
                content_type=content_type,
                body_bytes=body_bytes,
                body_text=body_text,
                json_payload=json_payload,
                error=f"HTTP {error.code}",
            )
        except Exception as error:
            return ResponsePayload(
                ok=False,
                status_code=None,
                content_type="",
                body_bytes=b"",
                body_text="",
                json_payload=None,
                error=str(error),
            )

    def screenshot(
        self,
        *,
        url: str,
        timeout_sec: int,
        wait: bool,
        device_width: int,
        device_height: int,
        viewport_width: int,
        viewport_height: int,
        auth: Optional[AuthContext] = None,
    ) -> ResponsePayload:
        endpoint = f"https://service.headless-render-api.com/screenshot/{url}"
        headers = self._build_headers(
            auth,
            wait=wait,
            device_width=device_width,
            device_height=device_height,
            viewport_width=viewport_width,
            viewport_height=viewport_height,
        )
        return self._request(endpoint, headers, timeout_sec)

    def scrape(
        self,
        *,
        url: str,
        timeout_sec: int,
        wait: bool,
        device_width: int,
        device_height: int,
        with_metadata: bool = True,
        with_screenshot: bool = False,
        auth: Optional[AuthContext] = None,
        block_cookies: bool = False,
    ) -> ResponsePayload:
        endpoint = f"https://service.headless-render-api.com/scrape/{url}"
        headers = self._build_headers(
            auth,
            wait=wait,
            device_width=device_width,
            device_height=device_height,
            with_metadata=with_metadata,
            with_screenshot=with_screenshot,
            block_cookies=block_cookies,
        )
        return self._request(endpoint, headers, timeout_sec)

    def prerender(
        self,
        *,
        url: str,
        timeout_sec: int,
        wait: bool,
        device_width: int,
        device_height: int,
        with_metadata: bool = True,
        with_screenshot: bool = False,
        auth: Optional[AuthContext] = None,
        block_cookies: bool = False,
    ) -> ResponsePayload:
        endpoint = f"https://service.headless-render-api.com/{url}"
        headers = self._build_headers(
            auth,
            wait=wait,
            device_width=device_width,
            device_height=device_height,
            with_metadata=with_metadata,
            with_screenshot=with_screenshot,
            block_cookies=block_cookies,
        )
        return self._request(endpoint, headers, timeout_sec)


def decode_body_from_json_payload(payload: Optional[JSON_DICT]) -> str:
    if not isinstance(payload, dict):
        return ""
    raw_body = payload.get("body")
    if isinstance(raw_body, str):
        try:
            return base64.b64decode(raw_body).decode("utf-8", "replace")
        except Exception:
            return raw_body
    return ""


def extract_metadata_from_json_payload(payload: Optional[JSON_DICT]) -> JSON_DICT:
    if not isinstance(payload, dict):
        return {}
    result: JSON_DICT = {}
    meta = payload.get("meta")
    links = payload.get("links")
    if isinstance(meta, dict):
        result["meta"] = meta
    if isinstance(links, list):
        result["links"] = links
    return result


__all__ = [
    "HeadlessRenderApiClient",
    "ResponsePayload",
    "decode_body_from_json_payload",
    "extract_metadata_from_json_payload",
]
