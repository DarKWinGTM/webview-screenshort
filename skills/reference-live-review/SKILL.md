---
name: reference-live-review
description: Capture a fresh live screenshot report from a URL, apply a saved reference bundle to it automatically, and emit an expected/actual compare session. Use this when a reusable baseline should be checked against the current live page in one flow.
argument-hint: --bundle <bundle.json> --url <live-url> --current-report <current-report.json> --comparison-json <comparison.json> --session-output <session.json> --session-name <session-name> [--mode viewport|fullpage] [--device desktop|tablet|mobile] [--capture-set responsive] [--wait] [--engine auto|headless|aws] [--diff-dir <dir>]
allowed-tools: Bash, Read
---

# Reference Live Review Skill

Use this skill when a saved expected baseline should be replayed against the current live page automatically instead of requiring a separately captured current report first.

## Workflow

1. Parse `$ARGUMENTS`.
2. Run the higher-level helper:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/reference_live_bundle.py" $ARGUMENTS
   ```
3. Read the returned JSON payload.
4. Read the fresh current report from `current_report_path`.
5. Read the emitted compare session from `session_output_path`.
6. Read the referenced screenshot evidence from the capture payload and the compare-session comparison pairs.
7. Continue with expected/actual frontend review using the fresh live capture as evidence.

## Output expectations
- exact bundle path used
- exact current report path produced from the live URL
- exact comparison/session artifact paths
- exact screenshot paths used for the fresh live run
- concise expected/actual findings from the new baseline replay
- next useful UI/UX follow-up step
