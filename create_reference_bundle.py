#!/usr/bin/env python3
"""
Create a reusable expected-reference bundle for compare-review workflows.
"""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

BUNDLE_SCHEMA = "webview-screenshort.reference-bundle/v1"


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as file_obj:
        return json.load(file_obj)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a reference bundle from compare-session artifacts")
    parser.add_argument("--name", required=True)
    parser.add_argument("--session", required=True, help="Path to compare-session JSON")
    parser.add_argument("--output", required=True, help="Output bundle JSON path")
    parser.add_argument("--reference-label", default="expected")
    args = parser.parse_args()

    session_path = Path(args.session).expanduser()
    output_path = Path(args.output).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    session = load_json(session_path)
    payload = {
        "bundle_schema": BUNDLE_SCHEMA,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "name": args.name,
        "reference_label": args.reference_label,
        "session_path": str(session_path),
        "session": session,
    }

    with open(output_path, "w", encoding="utf-8") as file_obj:
        json.dump(payload, file_obj, ensure_ascii=False)

    print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
