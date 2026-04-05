---
name: reference-live-gate
description: Capture a fresh live page evidence set from a URL, replay a saved reference bundle, and apply threshold-aware QA gate rules in one flow. Use this when a reusable baseline should be checked against the current live page and the result should end as a policy-based gate decision.
argument-hint: --bundle <bundle.json> --url <live-url> --current-report <current-report.json> --comparison-json <comparison.json> --session-output <session.json> --session-name <session-name> --gate-output <gate.json> [--policy-preset <family/name-or-alias>] [--policy-file <policy.json>] [--mode viewport|fullpage] [--device desktop|tablet|mobile] [--capture-set responsive] [--wait] [--engine auto|headless|aws] [--witness-mode frontend-default|csr-debug|responsive|session-replay] [--header NAME:VALUE] [--origin-header Prerendercloud-Name:VALUE] [--cookie NAME=VALUE] [--cookie-file FILE] [--preloaded-state-json JSON] [--preloaded-state-file FILE] [--diff-dir <dir>] [--fail-on-invalid true|false] [--require-device desktop] [--require-device tablet] [--require-device mobile] [--max-diff-pixels <n>] [--max-diff-ratio <n>]
allowed-tools: Bash, Read
---

# Reference Live Gate Skill

Use this skill when a saved expected baseline should be replayed against the current live page and the workflow should end with a threshold-aware gate result in one run.

## Workflow

1. Parse `$ARGUMENTS`.
2. Choose a live witness mode first:
   - `frontend-default` for normal baseline replay
   - `csr-debug` when late render / hydration incompleteness is suspected
   - `responsive` when cross-breakpoint replay matters
   - `session-replay` when the operator provides headers/cookies/session material explicitly
3. Run the higher-level helper:
   ```bash
   PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" python3 -m webview_screenshort.cli.reference_live_gate $ARGUMENTS
   ```
4. Read the returned JSON payload.
5. Read the fresh current report from `live_replay.current_report_path`.
6. If richer witnesses were emitted for the live capture, read them before explaining gate failure as purely visual.
7. If semantic page witness JSON was emitted for the live capture, use it to check for missing headings/nav/forms/content-shape drift before reducing the result to screenshot delta only.
8. Read the emitted gate result from `gate_output_path`.
9. Report the policy used, violated rules, and per-device gate outcome clearly.

## Output expectations
- exact bundle path used
- exact current report path produced from the live URL
- exact comparison/session/gate artifact paths
- exact rendered HTML / rendered text witness paths when emitted for the live capture
- exact semantic page witness path when emitted for the live capture
- overall gate result
- policy used
- missing required devices
- violated rules
- next useful QA or UI follow-up step
