---
name: policy-presets
description: List the built-in QA gate policy presets available in webview-screenshort. Use this when you need to discover reusable policy names before running qa-gate or reference-live-gate.
argument-hint: [--output-format json|text]
allowed-tools: Bash, Read
---

# Policy Presets Skill

Use this skill when you want to discover the built-in QA policy preset names instead of passing raw policy-file paths manually.

## Workflow

1. Parse `$ARGUMENTS`.
2. Run the helper:
   ```bash
   PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" python3 -m webview_screenshort.cli.list_policy_presets $ARGUMENTS
   ```
3. Read the returned preset list.
4. Recommend the best-fit preset name for the intended QA flow.

## Output expectations
- preset names
- preset families
- canonical selectors
- exact preset paths
- policy payloads when useful
- next useful qa-gate or reference-live-gate invocation
