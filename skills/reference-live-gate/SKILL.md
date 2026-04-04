---
name: reference-live-gate
description: Capture a fresh live screenshot report from a URL, replay a saved reference bundle, and apply threshold-aware QA gate rules in one flow. Use this when a reusable baseline should be checked against the current live page and the result should end as a policy-based gate decision.
argument-hint: --bundle <bundle.json> --url <live-url> --current-report <current-report.json> --comparison-json <comparison.json> --session-output <session.json> --session-name <session-name> --gate-output <gate.json> [--policy-preset <family/name-or-alias>] [--policy-file <policy.json>] [--mode viewport|fullpage] [--device desktop|tablet|mobile] [--capture-set responsive] [--wait] [--engine auto|headless|aws] [--diff-dir <dir>] [--fail-on-invalid true|false] [--require-device desktop] [--require-device tablet] [--require-device mobile] [--max-diff-pixels <n>] [--max-diff-ratio <n>]
allowed-tools: Bash, Read
---

# Reference Live Gate Skill

Use this skill when a saved expected baseline should be replayed against the current live page and the workflow should end with a threshold-aware gate result in one run.

## Workflow

1. Parse `$ARGUMENTS`.
2. Run the higher-level helper:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/reference_live_gate.py" $ARGUMENTS
   ```
3. Read the returned JSON payload.
4. Read the fresh current report from `live_replay.current_report_path`.
5. Read the emitted gate result from `gate_output_path`.
6. Report the policy used, violated rules, and per-device gate outcome clearly.

## Output expectations
- exact bundle path used
- exact current report path produced from the live URL
- exact comparison/session/gate artifact paths
- overall gate result
- policy used
- missing required devices
- violated rules
- next useful QA or UI follow-up step
