---
name: qa-gate
description: Apply threshold and policy rules on top of compare/live-replay verdicts so screenshot QA can produce a reusable pass/fail gate result. Use this when verdict output should be checked against explicit acceptance thresholds.
argument-hint: <compare-session.json|comparison.json|live-replay.json|verdict.json> [--policy-preset <family/name-or-alias>] [--policy-file <policy.json>] [--fail-on-invalid true|false] [--require-device desktop] [--require-device tablet] [--require-device mobile] [--max-diff-pixels <n>] [--max-diff-ratio <n>] [--output-format json|text]
allowed-tools: Bash, Read
---

# QA Gate Skill

Use this skill when screenshot QA should end in a threshold-aware gate result instead of only a verdict summary.

## Workflow

1. Parse `$ARGUMENTS`.
2. Run the helper:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/qa_gate.py" $ARGUMENTS
   ```
3. Read the returned gate payload.
4. Report the violated rules and failing devices clearly.
5. If the source still needs live baseline replay first, prefer `/reference-live-gate` instead of chaining `/reference-live-review` + `/qa-gate` manually.

## Output expectations
- overall gate result: `pass` or `fail`
- policy used
- missing required devices
- violated rules
- per-device gate status
- next useful QA or UI follow-up step
