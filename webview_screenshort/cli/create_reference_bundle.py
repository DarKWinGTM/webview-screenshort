from __future__ import annotations

import argparse
import json
from pathlib import Path

from ..references.bundles import write_reference_bundle


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a reference bundle from compare-session artifacts")
    parser.add_argument("--name", required=True)
    parser.add_argument("--session", required=True, help="Path to compare-session JSON")
    parser.add_argument("--output", required=True, help="Output bundle JSON path")
    parser.add_argument("--reference-label", default="expected")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    payload = write_reference_bundle(
        name=args.name,
        session_path=Path(args.session).expanduser(),
        output_path=Path(args.output).expanduser(),
        reference_label=args.reference_label,
    )
    print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
