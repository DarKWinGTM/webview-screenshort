from __future__ import annotations

import json
import re
from html import unescape
from pathlib import Path
from typing import Any, Dict, List, Optional

from .auth import AuthContext
from .config import ScreenshotConfig
from .headless_api import HeadlessRenderApiClient, ResponsePayload, decode_body_from_json_payload, extract_metadata_from_json_payload
from .paths import derive_neighbor_path, ensure_parent_dir

WITNESS_MODE_ALIASES = {
    "auth-frontend": "session-replay",
}
SCRIPT_STYLE_RE = re.compile(r"<(script|style|noscript)\b[^>]*>[\s\S]*?</\1>", re.IGNORECASE)
TAG_RE = re.compile(r"<[^>]+>")
WHITESPACE_RE = re.compile(r"\s+")


def normalize_witness_mode(value: str) -> str:
    normalized = str(value or "visual").strip() or "visual"
    return WITNESS_MODE_ALIASES.get(normalized, normalized)


def html_to_text(html: str) -> str:
    text = SCRIPT_STYLE_RE.sub(" ", html)
    text = TAG_RE.sub(" ", text)
    text = unescape(text)
    text = WHITESPACE_RE.sub(" ", text).strip()
    return text


def extract_title_from_html(html: str) -> Optional[str]:
    match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    if not match:
        return None
    return WHITESPACE_RE.sub(" ", unescape(match.group(1))).strip() or None


def _extract_tag_texts(html: str, tag_name: str, limit: int = 12) -> List[str]:
    pattern = re.compile(fr"<{tag_name}[^>]*>(.*?)</{tag_name}>", re.IGNORECASE | re.DOTALL)
    values: List[str] = []
    for match in pattern.finditer(html):
        value = html_to_text(match.group(1))
        if value:
            values.append(value)
        if len(values) >= limit:
            break
    return values


def _extract_anchor_texts(html: str, limit: int = 20) -> List[str]:
    pattern = re.compile(r"<a\b[^>]*>(.*?)</a>", re.IGNORECASE | re.DOTALL)
    values: List[str] = []
    for match in pattern.finditer(html):
        value = html_to_text(match.group(1))
        if value:
            values.append(value)
        if len(values) >= limit:
            break
    return values


def _extract_input_names(html: str, limit: int = 20) -> List[str]:
    pattern = re.compile(r"<input\b[^>]*(?:name|id)=['\"]([^'\"]+)['\"][^>]*>", re.IGNORECASE)
    values: List[str] = []
    for match in pattern.finditer(html):
        values.append(match.group(1).strip())
        if len(values) >= limit:
            break
    return values


def build_semantic_page_summary(html: str, *, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    lowered = html.lower()
    semantic = {
        "title": extract_title_from_html(html),
        "headings": {
            "h1": _extract_tag_texts(html, "h1", 5),
            "h2": _extract_tag_texts(html, "h2", 8),
            "h3": _extract_tag_texts(html, "h3", 10),
        },
        "buttons": _extract_tag_texts(html, "button", 12),
        "links": _extract_anchor_texts(html, 20),
        "forms": {
            "count": lowered.count("<form"),
            "inputs": _extract_input_names(html, 20),
        },
        "structure": {
            "has_header": "<header" in lowered,
            "has_nav": "<nav" in lowered,
            "has_main": "<main" in lowered,
            "has_footer": "<footer" in lowered,
            "has_aside": "<aside" in lowered,
            "section_count": lowered.count("<section"),
            "article_count": lowered.count("<article"),
            "table_count": lowered.count("<table"),
            "list_count": lowered.count("<ul") + lowered.count("<ol"),
        },
    }
    if metadata:
        semantic["provider_metadata_keys"] = sorted(metadata.keys())
    return semantic


def response_summary(response: ResponsePayload, source: str) -> Dict[str, Any]:
    return {
        "source": source,
        "ok": response.ok,
        "status_code": response.status_code,
        "content_type": response.content_type,
        "has_json_payload": isinstance(response.json_payload, dict),
        "error": response.error,
    }


def write_json_file(path: Path, payload: Dict[str, Any]) -> str:
    ensure_parent_dir(path)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return str(path)


def write_text_file(path: Path, content: str) -> str:
    ensure_parent_dir(path)
    path.write_text(content, encoding="utf-8")
    return str(path)


def build_capture_set_witness_index(captures: List[Any], field_name: str) -> Dict[str, Any]:
    index: Dict[str, Any] = {}
    for capture in captures:
        value = getattr(capture, field_name, None)
        if value:
            index[capture.device or "default"] = value
    return index


def write_capture_set_witness_file(base_path: Path, suffix_name: str, payload: Dict[str, Any]) -> Optional[str]:
    if not payload:
        return None
    return write_json_file(derive_neighbor_path(base_path, suffix_name, "json"), payload)


def collect_html_witnesses(
    *,
    url: str,
    config: ScreenshotConfig,
    wait: bool,
    witness_mode: str,
    output_path: Path,
    auth_context: Optional[AuthContext],
    warnings: List[str],
) -> Dict[str, Any]:
    client = HeadlessRenderApiClient(config.prerender_token)
    rendered_html_path: Optional[str] = None
    rendered_text_path: Optional[str] = None
    prerendered_html_path: Optional[str] = None
    metadata_path: Optional[str] = None
    acquisition_path: Optional[str] = None
    semantic_page_path: Optional[str] = None
    title: Optional[str] = None
    page_metadata: Dict[str, Any] = {}
    acquisition_summary: Dict[str, Any] = {}
    semantic_page_summary: Dict[str, Any] = {}

    if witness_mode == "visual":
        return {
            "rendered_html_path": None,
            "rendered_text_path": None,
            "prerendered_html_path": None,
            "metadata_path": None,
            "acquisition_path": None,
            "semantic_page_path": None,
            "title": None,
            "page_metadata": {},
            "acquisition_summary": {},
            "semantic_page_summary": {},
        }

    scrape_response = client.scrape(
        url=url,
        timeout_sec=config.html_timeout,
        wait=wait,
        device_width=config.viewport_width,
        device_height=config.fullpage_height if witness_mode in {"csr-debug", "frontend-default", "session-replay"} else config.viewport_height,
        with_metadata=True,
        with_screenshot=False,
        auth=auth_context,
    )
    acquisition_summary["scrape"] = response_summary(scrape_response, "scrape")
    page_metadata.update(extract_metadata_from_json_payload(scrape_response.json_payload))
    if scrape_response.ok:
        rendered_html = decode_body_from_json_payload(scrape_response.json_payload) or scrape_response.body_text
        if rendered_html:
            rendered_html_path = write_text_file(derive_neighbor_path(output_path, "rendered", "html"), rendered_html)
            rendered_text = html_to_text(rendered_html)
            rendered_text_path = write_text_file(derive_neighbor_path(output_path, "rendered", "txt"), rendered_text)
            title = extract_title_from_html(rendered_html)
        else:
            warnings.append("Scrape witness returned no HTML body.")
    else:
        warnings.append(f"Rendered HTML witness failed: {scrape_response.error or 'unknown error'}")

    if witness_mode == "csr-debug":
        prerender_response = client.prerender(
            url=url,
            timeout_sec=config.html_timeout,
            wait=wait,
            device_width=config.viewport_width,
            device_height=config.fullpage_height,
            with_metadata=True,
            with_screenshot=False,
            auth=auth_context,
        )
        acquisition_summary["prerender"] = response_summary(prerender_response, "prerender")
        prerender_meta = extract_metadata_from_json_payload(prerender_response.json_payload)
        if prerender_meta:
            page_metadata["prerender"] = prerender_meta
        if prerender_response.ok:
            prerender_html = decode_body_from_json_payload(prerender_response.json_payload) or prerender_response.body_text
            if prerender_html:
                prerendered_html_path = write_text_file(derive_neighbor_path(output_path, "prerendered", "html"), prerender_html)
                title = title or extract_title_from_html(prerender_html)
            else:
                warnings.append("Prerender HTML witness returned no serialized HTML body.")
        else:
            warnings.append(f"Prerender HTML witness failed: {prerender_response.error or 'unknown error'}")

    semantic_source_html = None
    if prerendered_html_path and Path(prerendered_html_path).exists():
        semantic_source_html = Path(prerendered_html_path).read_text(encoding="utf-8")
    elif rendered_html_path and Path(rendered_html_path).exists():
        semantic_source_html = Path(rendered_html_path).read_text(encoding="utf-8")

    if semantic_source_html:
        semantic_page_summary = build_semantic_page_summary(semantic_source_html, metadata=page_metadata)
        semantic_page_path = write_json_file(derive_neighbor_path(output_path, "semantic", "json"), semantic_page_summary)

    if page_metadata:
        metadata_path = write_json_file(derive_neighbor_path(output_path, "metadata", "json"), page_metadata)
    if acquisition_summary:
        acquisition_path = write_json_file(derive_neighbor_path(output_path, "acquisition", "json"), acquisition_summary)

    return {
        "rendered_html_path": rendered_html_path,
        "rendered_text_path": rendered_text_path,
        "prerendered_html_path": prerendered_html_path,
        "metadata_path": metadata_path,
        "acquisition_path": acquisition_path,
        "semantic_page_path": semantic_page_path,
        "title": title,
        "page_metadata": page_metadata,
        "acquisition_summary": acquisition_summary,
        "semantic_page_summary": semantic_page_summary,
    }


__all__ = [
    "build_capture_set_witness_index",
    "build_semantic_page_summary",
    "collect_html_witnesses",
    "extract_title_from_html",
    "html_to_text",
    "normalize_witness_mode",
    "response_summary",
    "write_capture_set_witness_file",
    "write_json_file",
    "write_text_file",
]
