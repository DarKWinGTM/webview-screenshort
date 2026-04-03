---
name: screenshot
description: Capture a real rendered screenshot of a webpage for frontend-development visual review. Use this when Claude needs visual evidence from a live page, especially CSR/SPA pages, before giving layout, UX, UI, or docs-page feedback.
argument-hint: <url> [--mode fullpage|viewport] [--device desktop|tablet|mobile] [--capture-set responsive] [--report-file FILE] [--wait] [--engine auto|headless|aws] [--output FILE] [--output-format json]
allowed-tools: Bash, Read
---

# Screenshot Skill

Capture a webpage screenshot from `$ARGUMENTS` so Claude can inspect the real rendered UI.

## What this skill is for
Use it when frontend work needs visual evidence from the real page, for example:
- layout review
- UX/UI inspection
- CSR/hydration verification
- docs page visual checks
- dashboard/page-state comparison before recommending changes

## Execution Steps

1. Parse arguments from `$ARGUMENTS`.
   - first positional arg = URL
   - optional flags: `--mode`, `--device`, `--capture-set`, `--report-file`, `--wait`, `--engine`, `--output`, `--output-format`

2. Run the screenshot engine from this installed plugin package:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/screenshot.py" $ARGUMENTS
   ```

3. Prefer adding `--output-format json` when the result will feed a follow-on review workflow.

4. If the task needs one-shot responsive review, prefer `--capture-set responsive` so the tool returns one machine-readable JSON payload with desktop, tablet, and mobile results together.

5. If capture succeeds:
   - report the exact screenshot file path
   - if `--report-file` was used, report the exact JSON report path
   - if `--capture-set responsive` was used, report the per-device screenshot paths and viewport metadata
   - if the user wants visual review, read the image file next and continue from the screenshot evidence

6. If capture fails:
   - report the error clearly
   - suggest a narrower retry such as `--wait`, `--mode viewport`, or `--engine headless`

## Default Behavior
- Engine: `auto`
- Mode: `fullpage`
- Wait: off by default; turn on for CSR / SPA pages

## Recommended Usage
```bash
/screenshot https://example.com --wait --mode viewport
/screenshot https://example.com/docs --wait --mode fullpage --output-format json --report-file /tmp/example_capture.json
/screenshot https://example.com --capture-set responsive --wait --mode viewport --output-format json --report-file /tmp/example_responsive.json
/screenshot https://example.com --device mobile --wait --mode viewport --output-format json
/screenshot https://example.com --device tablet --wait --mode viewport --output-format json
```
