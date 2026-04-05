from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Dict

from ..schemas import SESSION_SCHEMA


def build_compare_session_payload(
    *,
    name: str,
    left_report: Path,
    right_report: Path,
    left_label: str,
    right_label: str,
    comparison_json_path: Path,
    comparison: Dict,
) -> Dict:
    return {
        "session_schema": SESSION_SCHEMA,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "name": name,
        "left": {
            "label": left_label,
            "report_path": str(left_report.expanduser()),
        },
        "right": {
            "label": right_label,
            "report_path": str(right_report.expanduser()),
        },
        "comparison_json": str(comparison_json_path),
        "comparison": comparison,
    }
