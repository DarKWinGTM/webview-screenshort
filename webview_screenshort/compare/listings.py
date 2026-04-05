from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

from ..schemas import SESSION_SCHEMA


def load_session(path: Path) -> Optional[Dict[str, Any]]:
    try:
        with open(path, "r", encoding="utf-8") as file_obj:
            payload = json.load(file_obj)
    except Exception:
        return None
    if not isinstance(payload, dict):
        return None
    if payload.get("session_schema") != SESSION_SCHEMA:
        return None
    return payload


def list_compare_sessions_payload(directory: Path) -> Dict[str, Any]:
    base_dir = directory.expanduser()
    sessions = []
    for path in sorted(base_dir.glob("*.json")):
        payload = load_session(path)
        if not payload:
            continue
        comparison = payload.get("comparison", {})
        sessions.append(
            {
                "path": str(path),
                "name": payload.get("name"),
                "generated_at": payload.get("generated_at"),
                "left_label": payload.get("left", {}).get("label"),
                "right_label": payload.get("right", {}).get("label"),
                "comparison_mode": comparison.get("comparison_mode"),
                "pair_count": len(comparison.get("pairs", [])),
                "success": comparison.get("success"),
            }
        )
    return {
        "session_schema": SESSION_SCHEMA,
        "directory": str(base_dir),
        "count": len(sessions),
        "sessions": sessions,
    }
