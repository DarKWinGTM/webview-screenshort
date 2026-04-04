#!/usr/bin/env python3
"""
Apply threshold/policy gating on top of QA verdict artifacts.
"""

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

DEFAULT_POLICY = {
    "fail_on_invalid": True,
    "require_devices": [],
    "max_diff_pixels": None,
    "max_diff_ratio": None,
}


@dataclass
class GateDeviceResult:
    device: str
    verdict: str
    gate_status: str
    passed_gate: bool
    reason: str
    diff_pixels: Optional[int]
    diff_ratio: Optional[float]
    violated_rules: List[str]


@dataclass
class GateResult:
    success: bool
    source_path: str
    policy: Dict[str, Any]
    overall_gate_status: str
    overall_passed: bool
    violated_rules: List[str]
    missing_required_devices: List[str]
    devices: List[GateDeviceResult]
    warnings: List[str]
    error: Optional[str] = None


def load_json(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as file_obj:
        return json.load(file_obj)


def build_verdict_command(source_path: Path) -> List[str]:
    helper = Path(__file__).with_name("qa_verdict.py")
    return [sys.executable, str(helper), str(source_path), "--output-format", "json"]


def load_verdict(source_path: Path) -> Dict[str, Any]:
    import subprocess

    result = subprocess.run(build_verdict_command(source_path), capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or result.stdout.strip() or "qa_verdict.py failed")
    return json.loads(result.stdout)


def load_policy(policy_path: Optional[str]) -> Dict[str, Any]:
    if not policy_path:
        return dict(DEFAULT_POLICY)
    payload = load_json(Path(policy_path).expanduser())
    merged = dict(DEFAULT_POLICY)
    merged.update(payload)
    return merged


def evaluate_device(device: Dict[str, Any], policy: Dict[str, Any]) -> GateDeviceResult:
    violated_rules: List[str] = []
    verdict = str(device.get("verdict") or "invalid")
    diff_pixels = device.get("diff_pixels")
    diff_ratio = device.get("diff_ratio")

    if verdict == "invalid" and policy.get("fail_on_invalid", True):
        violated_rules.append("fail_on_invalid")

    max_diff_pixels = policy.get("max_diff_pixels")
    if max_diff_pixels is not None and diff_pixels is not None and diff_pixels > max_diff_pixels:
        violated_rules.append("max_diff_pixels")

    max_diff_ratio = policy.get("max_diff_ratio")
    if max_diff_ratio is not None and diff_ratio is not None and diff_ratio > max_diff_ratio:
        violated_rules.append("max_diff_ratio")

    gate_status = "pass"
    passed_gate = True
    reason = "within_policy"
    if violated_rules:
        gate_status = "fail"
        passed_gate = False
        reason = "policy_violation"

    return GateDeviceResult(
        device=str(device.get("device") or "unknown"),
        verdict=verdict,
        gate_status=gate_status,
        passed_gate=passed_gate,
        reason=reason,
        diff_pixels=diff_pixels,
        diff_ratio=diff_ratio,
        violated_rules=violated_rules,
    )


def apply_gate(verdict_payload: Dict[str, Any], policy: Dict[str, Any], source_path: Path) -> GateResult:
    devices = [evaluate_device(device, policy) for device in verdict_payload.get("devices") or []]
    present_devices = {device.device for device in devices}
    required_devices = [str(device) for device in policy.get("require_devices") or []]
    missing_required_devices = [device for device in required_devices if device not in present_devices]

    violated_rules: List[str] = []
    for device in devices:
        violated_rules.extend(f"{device.device}:{rule}" for rule in device.violated_rules)
    for device in missing_required_devices:
        violated_rules.append(f"missing_required_device:{device}")

    overall_gate_status = "pass"
    overall_passed = True
    if violated_rules:
        overall_gate_status = "fail"
        overall_passed = False

    return GateResult(
        success=True,
        source_path=str(source_path),
        policy=policy,
        overall_gate_status=overall_gate_status,
        overall_passed=overall_passed,
        violated_rules=violated_rules,
        missing_required_devices=missing_required_devices,
        devices=devices,
        warnings=list(verdict_payload.get("warnings") or []),
        error=None,
    )


def emit_text(result: GateResult) -> None:
    print(f"overall_gate_status={result.overall_gate_status}")
    print(f"overall_passed={str(result.overall_passed).lower()}")
    if result.missing_required_devices:
        print(f"missing_required_devices={','.join(result.missing_required_devices)}")
    if result.violated_rules:
        print(f"violated_rules={','.join(result.violated_rules)}")
    for device in result.devices:
        print(
            f"- {device.device}: verdict={device.verdict} gate_status={device.gate_status} diff_pixels={device.diff_pixels} diff_ratio={device.diff_ratio}"
        )
    for warning in result.warnings:
        print(f"⚠️ {warning}")
    if result.error:
        print(f"❌ {result.error}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply threshold policy gating on top of a QA verdict source")
    parser.add_argument("source", help="Path to a compare-session, comparison, live-replay, or verdict JSON")
    parser.add_argument("--policy-file", help="Optional JSON file containing gate policy settings")
    parser.add_argument("--output-format", choices=["json", "text"], default="json")
    parser.add_argument("--fail-on-invalid", choices=["true", "false"], help="Override fail_on_invalid policy")
    parser.add_argument("--require-device", action="append", default=[], help="Require a device to be present; may be passed multiple times")
    parser.add_argument("--max-diff-pixels", type=int, help="Maximum allowed diff pixel count before gate fail")
    parser.add_argument("--max-diff-ratio", type=float, help="Maximum allowed diff ratio before gate fail")
    args = parser.parse_args()

    source_path = Path(args.source).expanduser()
    payload = load_json(source_path)
    if "overall_verdict" in payload and isinstance(payload.get("devices"), list):
        verdict_payload = payload
    else:
        verdict_payload = load_verdict(source_path)

    policy = load_policy(args.policy_file)
    if args.fail_on_invalid is not None:
        policy["fail_on_invalid"] = args.fail_on_invalid == "true"
    if args.require_device:
        policy["require_devices"] = args.require_device
    if args.max_diff_pixels is not None:
        policy["max_diff_pixels"] = args.max_diff_pixels
    if args.max_diff_ratio is not None:
        policy["max_diff_ratio"] = args.max_diff_ratio

    result = apply_gate(verdict_payload, policy, source_path)

    if args.output_format == "json":
        print(json.dumps(asdict(result), ensure_ascii=False))
    else:
        emit_text(result)

    sys.exit(0 if result.overall_passed else 1)


if __name__ == "__main__":
    main()
