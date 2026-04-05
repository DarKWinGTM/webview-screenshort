---
name: reference-live-review
description: Capture a fresh live page evidence set from a URL, apply a saved reference bundle to it automatically, and emit an expected/actual compare session. Use this when a reusable baseline should be checked against the current live page in one flow.
argument-hint: --bundle <bundle.json> --url <live-url> --current-report <current-report.json> --comparison-json <comparison.json> --session-output <session.json> --session-name <session-name> [--mode viewport|fullpage] [--device desktop|tablet|mobile] [--capture-set responsive] [--wait] [--engine auto|headless|aws] [--witness-mode frontend-default|csr-debug|session-replay|responsive] [--header NAME:VALUE] [--origin-header Prerendercloud-Name:VALUE] [--cookie NAME=VALUE] [--cookie-file FILE] [--diff-dir <dir>]
allowed-tools: Bash, Read
---

# Reference Live Review Skill

Use this skill when a saved expected baseline should be replayed against the current live page automatically instead of requiring a separately captured current report first.

## Workflow

1. Parse `$ARGUMENTS`.
2. Run the higher-level helper:
   ```bash
   PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" python3 -m webview_screenshort.cli.reference_live_bundle $ARGUMENTS
   ```
3. Read the returned JSON payload.
4. Read the fresh current report from `current_report_path`.
5. Read the emitted compare session from `session_output_path`.
6. Read the referenced screenshot evidence from the capture payload and the compare-session comparison pairs.
7. If rendered HTML / rendered text witnesses were emitted for the fresh live capture, read them too before concluding on CSR/content drift.
8. If semantic page witness JSON was emitted for the fresh live capture, read it too before concluding that the drift is only visual.
9. Continue with expected/actual frontend review using the fresh live capture as evidence.
9. If the workflow should end in a reusable machine-readable verdict, run:
   ```bash
   PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" python3 -m webview_screenshort.cli.qa_verdict <live-replay.json> --output-format json
   ```
10. If the workflow should end in a threshold-aware gate result directly, prefer `/reference-live-gate` instead of chaining verdict + gate manually.

## Output expectations
- exact bundle path used
- exact current report path produced from the live URL
- exact comparison/session artifact paths
- exact screenshot paths used for the fresh live run
- exact rendered HTML / rendered text paths when emitted for the live capture
- exact semantic page witness path when emitted for the live capture
- concise expected/actual findings from the new baseline replay
- next useful UI/UX follow-up step
