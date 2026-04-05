#!/usr/bin/env python3
"""
Hybrid Screenshot Tool
Usage: python screenshot.py <url> [--output FILE] [--output-dir DIR]
                           [--device {desktop,tablet,mobile}]
                           [--capture-set {responsive}]
                           [--report-file FILE]
                           [--bundle-file FILE]
                           [--engine {auto,headless,aws}]
                           [--mode {viewport,fullpage}]
                           [--wait]
                           [--witness-mode {visual,frontend-default,csr-debug,responsive,session-replay}]
                           [--header NAME:VALUE]
                           [--origin-header Prerendercloud-Name:VALUE]
                           [--cookie NAME=VALUE]
                           [--cookie-file FILE]
                           [--output-format {text,json}]
"""

import argparse
import json
import sys
from dataclasses import asdict

from webview_screenshort.capture_service import Reporter, capture_from_args, emit_result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Hybrid Screenshot Tool")
    parser.add_argument("url", help="URL to capture")
    parser.add_argument("--output", "-o", help="Output file path or base file path when using --capture-set")
    parser.add_argument("--output-dir", help="Output directory for generated screenshots")
    parser.add_argument("--device", choices=["desktop", "tablet", "mobile"], help="Viewport preset override for focused frontend review")
    parser.add_argument("--capture-set", choices=["responsive"], help="Capture a predefined multi-device screenshot set in one run")
    parser.add_argument("--report-file", help="Write machine-readable capture metadata to a JSON report file")
    parser.add_argument("--bundle-file", help="Write a machine-readable evidence bundle JSON file")
    parser.add_argument("--engine", "-e", choices=["auto", "headless", "aws"], default="auto", help="Select screenshot engine (default: auto)")
    parser.add_argument("--mode", "-m", choices=["viewport", "fullpage"], default="fullpage", help="Capture mode: 'viewport' or 'fullpage' (default: fullpage)")
    parser.add_argument("--wait", "-w", action="store_true", help="Wait extra time for dynamic content (Headless engine only)")
    parser.add_argument(
        "--witness-mode",
        choices=["visual", "frontend-default", "csr-debug", "responsive", "session-replay", "auth-frontend"],
        default="visual",
        help="Select the evidence mode to capture (default: visual)",
    )
    parser.add_argument("--header", action="append", default=[], help="Forward a request header as NAME:VALUE")
    parser.add_argument(
        "--origin-header",
        action="append",
        default=[],
        help="Forward a Prerendercloud-* header to the origin as NAME:VALUE",
    )
    parser.add_argument("--cookie", action="append", default=[], help="Forward a cookie as NAME=VALUE")
    parser.add_argument("--cookie-file", help="Load cookies from a JSON or newline-separated file")
    parser.add_argument("--output-format", choices=["text", "json"], default="text", help="Result output format (default: text)")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.capture_set and args.device:
        raise SystemExit("--capture-set cannot be combined with --device. Use either one device or one capture set.")
    if args.capture_set == "responsive" and args.witness_mode == "visual":
        args.witness_mode = "responsive"

    reporter = Reporter(args.output_format)
    result = capture_from_args(args)

    if args.output_format == "json":
        print(json.dumps(asdict(result), ensure_ascii=False))
    else:
        emit_result(result, args.output_format, reporter)
    sys.exit(0 if result.success else 1)


if __name__ == "__main__":
    main()
