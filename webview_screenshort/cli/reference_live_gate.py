from __future__ import annotations

import argparse
import json
import sys

from ..references.live import reference_live_gate


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Capture a live current report, replay a saved baseline, and apply QA gate policy")
    parser.add_argument("--bundle", required=True, help="Path to reference bundle JSON")
    parser.add_argument("--url", required=True, help="Publicly reachable live URL to capture before applying the baseline")
    parser.add_argument("--current-report", required=True, help="Output path for the fresh current capture report")
    parser.add_argument("--comparison-json", required=True, help="Output path for compare_reports JSON")
    parser.add_argument("--session-output", required=True, help="Output path for compare-session JSON")
    parser.add_argument("--session-name", required=True, help="Name for the emitted expected/actual compare session")
    parser.add_argument("--gate-output", required=True, help="Output path for QA gate JSON")
    parser.add_argument("--policy-file", help="Optional policy preset JSON for QA gate evaluation")
    parser.add_argument("--policy-preset", help="Name of a built-in policy preset from support/policies/")
    parser.add_argument("--current-label", default="actual")
    parser.add_argument("--output", help="Optional screenshot output path or base path for responsive capture set")
    parser.add_argument("--output-dir", help="Optional output directory for generated screenshots")
    parser.add_argument("--device", choices=["desktop", "tablet", "mobile"], help="Optional focused device preset")
    parser.add_argument("--capture-set", choices=["responsive"], help="Optional responsive capture-set mode")
    parser.add_argument("--engine", choices=["auto", "headless", "aws"], default="auto")
    parser.add_argument("--mode", choices=["viewport", "fullpage"], default="viewport")
    parser.add_argument("--wait", action="store_true")
    parser.add_argument("--diff-dir", help="Optional diff image output directory for comparison enrichment")
    parser.add_argument("--fail-on-invalid", choices=["true", "false"], help="Override fail_on_invalid policy")
    parser.add_argument("--require-device", action="append", default=[], help="Require a device; may be passed multiple times")
    parser.add_argument("--max-diff-pixels", type=int, help="Maximum allowed diff pixel count before gate fail")
    parser.add_argument("--max-diff-ratio", type=float, help="Maximum allowed diff ratio before gate fail")
    parser.add_argument(
        "--witness-mode",
        choices=["visual", "frontend-default", "csr-debug", "responsive", "session-replay", "auth-frontend"],
        default="frontend-default",
    )
    parser.add_argument("--header", action="append", default=[], help="Forward a request header as NAME:VALUE")
    parser.add_argument("--origin-header", action="append", default=[], help="Forward a Prerendercloud-* header to the origin as NAME:VALUE")
    parser.add_argument("--cookie", action="append", default=[], help="Forward a cookie as NAME=VALUE")
    parser.add_argument("--cookie-file", help="Load cookies from a JSON or newline-separated file")
    parser.add_argument("--preloaded-state-json", help="Forward bounded preloaded state as an inline JSON object for origin-side bootstrap reconstruction")
    parser.add_argument("--preloaded-state-file", help="Load bounded preloaded state from a JSON file for origin-side bootstrap reconstruction")
    parser.add_argument("--bundle-file", help="Optional evidence bundle output path for the live capture")
    parser.add_argument("--output-format", choices=["json"], default="json")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    payload = reference_live_gate(args=args)
    print(json.dumps(payload, ensure_ascii=False))
    sys.exit(0 if payload["gate"].get("overall_passed") else 1)


if __name__ == "__main__":
    main()
