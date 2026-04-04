---
name: qa-verdict
description: Turn compare-session, comparison, or reference-live-replay artifacts into a machine-readable visual QA verdict with per-device pass/fail/invalid summaries. Use this when screenshot QA should end in a reusable verdict instead of raw comparison JSON only.
argument-hint: <compare-session.json|comparison.json|live-replay.json> [--output-format json|text]
allowed-tools: Bash, Read
---

# QA Verdict Skill

Use this skill when frontend screenshot QA should end with a concise verdict layer rather than only raw pair metadata.

## Workflow

1. Parse `$ARGUMENTS`.
2. Run the helper:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/qa_verdict.py" $ARGUMENTS
   ```
3. Read the returned verdict payload.
4. If needed, read the referenced compare-session/live-replay artifact for deeper evidence.
5. Report the per-device outcome clearly.

## Output expectations
- overall verdict: `pass`, `fail`, or `invalid`
- per-device verdicts for desktop/tablet/mobile or focused captures
- machine-readable match/mismatch/invalid lists
- concise reason for each failed or invalid pair
- next useful QA or UI follow-up step
