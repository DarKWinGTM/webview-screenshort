#!/usr/bin/env python3
"""
List and summarize named compare session artifacts.
"""

import argparse
import json
from pathlib import Path

SESSION_SCHEMA = "webview-screenshort.compare-session/v1"


def load_session(path: Path):
    with open(path, "r", encoding="utf-8") as file_obj:
        payload = json.load(file_obj)
    if payload.get("session_schema") != SESSION_SCHEMA:
        return None
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="List compare session artifacts")
    parser.add_argument("directory", help="Directory containing compare-session JSON files")
    parser.add_argument("--output-format", choices=["json", "text"], default="json")
    args = parser.parse_args()

    base_dir = Path(args.directory).expanduser()
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

    result = {
        "session_schema": SESSION_SCHEMA,
        "directory": str(base_dir),
        "count": len(sessions),
        "sessions": sessions,
    }

    if args.output_format == "json":
        print(json.dumps(result, ensure_ascii=False))
        return

    print(f"count={result['count']}")
    for session in sessions:
        print(f"- {session['name']} ({session['left_label']} -> {session['right_label']}) [{session['comparison_mode']}] {session['path']}")


if __name__ == "__main__":
    main()
