from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def _load_json_file(path: Path) -> Optional[Dict[str, Any]]:
    try:
        with open(path, "r", encoding="utf-8") as file_obj:
            payload = json.load(file_obj)
    except Exception:
        return None
    return payload if isinstance(payload, dict) else None


def resolve_artifact_path(raw_path: Any, report_path: Path) -> Optional[Path]:
    if not raw_path:
        return None
    path = Path(str(raw_path)).expanduser()
    if not path.is_absolute():
        path = (report_path.parent / path).resolve()
    return path


def extract_semantic_summary(result: Dict[str, Any], report_path: Path, device: Optional[str]) -> Dict[str, Any]:
    if result.get("capture_set") == "responsive":
        captures = result.get("captures") or []
        for capture in captures:
            if str(capture.get("device") or "unknown") != str(device or "default"):
                continue
            if isinstance(capture.get("semantic_page_summary"), dict):
                return capture["semantic_page_summary"]
            semantic_path = resolve_artifact_path(capture.get("semantic_page_path"), report_path)
            if semantic_path:
                loaded = _load_json_file(semantic_path)
                if loaded:
                    return loaded
        return {}

    if isinstance(result.get("semantic_page_summary"), dict):
        return result["semantic_page_summary"]
    semantic_path = resolve_artifact_path(result.get("semantic_page_path"), report_path)
    if semantic_path:
        loaded = _load_json_file(semantic_path)
        if loaded:
            return loaded
    return {}


def _semantic_structure(summary: Dict[str, Any]) -> Dict[str, Any]:
    structure = summary.get("structure")
    return structure if isinstance(structure, dict) else {}


def _semantic_headings(summary: Dict[str, Any]) -> Dict[str, List[str]]:
    headings = summary.get("headings")
    if not isinstance(headings, dict):
        return {}
    normalized: Dict[str, List[str]] = {}
    for key, value in headings.items():
        if isinstance(value, list):
            normalized[str(key)] = [str(item) for item in value if str(item).strip()]
    return normalized


def summarize_semantic_difference(left_summary: Dict[str, Any], right_summary: Dict[str, Any]) -> Tuple[str, str, Dict[str, Any]]:
    if not left_summary and not right_summary:
        return "semantic_unavailable", "semantic_witness_missing_on_both_sides", {}
    if not left_summary or not right_summary:
        return "semantic_missing", "semantic_witness_missing_on_one_side", {
            "left_present": bool(left_summary),
            "right_present": bool(right_summary),
        }

    details: Dict[str, Any] = {}
    if (left_summary.get("title") or "") != (right_summary.get("title") or ""):
        details["title_changed"] = {
            "left": left_summary.get("title"),
            "right": right_summary.get("title"),
        }

    left_links = set(str(item) for item in left_summary.get("links") or [])
    right_links = set(str(item) for item in right_summary.get("links") or [])
    missing_links = sorted(left_links - right_links)
    added_links = sorted(right_links - left_links)
    if missing_links:
        details["missing_links"] = missing_links[:10]
    if added_links:
        details["added_links"] = added_links[:10]

    left_buttons = set(str(item) for item in left_summary.get("buttons") or [])
    right_buttons = set(str(item) for item in right_summary.get("buttons") or [])
    missing_buttons = sorted(left_buttons - right_buttons)
    added_buttons = sorted(right_buttons - left_buttons)
    if missing_buttons:
        details["missing_buttons"] = missing_buttons[:10]
    if added_buttons:
        details["added_buttons"] = added_buttons[:10]

    left_forms = left_summary.get("forms") or {}
    right_forms = right_summary.get("forms") or {}
    left_form_count = int(left_forms.get("count") or 0)
    right_form_count = int(right_forms.get("count") or 0)
    if left_form_count != right_form_count:
        details["form_count_changed"] = {
            "left": left_form_count,
            "right": right_form_count,
        }
    left_inputs = set(str(item) for item in left_forms.get("inputs") or [])
    right_inputs = set(str(item) for item in right_forms.get("inputs") or [])
    missing_inputs = sorted(left_inputs - right_inputs)
    added_inputs = sorted(right_inputs - left_inputs)
    if missing_inputs:
        details["missing_inputs"] = missing_inputs[:10]
    if added_inputs:
        details["added_inputs"] = added_inputs[:10]

    left_headings = _semantic_headings(left_summary)
    right_headings = _semantic_headings(right_summary)
    missing_heading_groups: Dict[str, List[str]] = {}
    added_heading_groups: Dict[str, List[str]] = {}
    for level in sorted(set(left_headings) | set(right_headings)):
        left_values = set(left_headings.get(level, []))
        right_values = set(right_headings.get(level, []))
        missing = sorted(left_values - right_values)
        added = sorted(right_values - left_values)
        if missing:
            missing_heading_groups[level] = missing[:10]
        if added:
            added_heading_groups[level] = added[:10]
    if missing_heading_groups:
        details["missing_headings"] = missing_heading_groups
    if added_heading_groups:
        details["added_headings"] = added_heading_groups

    left_structure = _semantic_structure(left_summary)
    right_structure = _semantic_structure(right_summary)
    changed_flags: Dict[str, Dict[str, Any]] = {}
    for key in sorted(set(left_structure) | set(right_structure)):
        if left_structure.get(key) != right_structure.get(key):
            changed_flags[key] = {
                "left": left_structure.get(key),
                "right": right_structure.get(key),
            }
    if changed_flags:
        details["structure_changes"] = changed_flags

    if not details:
        return "semantic_match", "semantic_witnesses_match", {}

    if any(key in details for key in [
        "missing_headings",
        "missing_links",
        "missing_buttons",
        "missing_inputs",
        "structure_changes",
        "form_count_changed",
    ]):
        return "semantic_structure_change", "semantic_structure_changed", details

    return "semantic_content_change", "semantic_content_changed", details


__all__ = [
    "extract_semantic_summary",
    "summarize_semantic_difference",
]
