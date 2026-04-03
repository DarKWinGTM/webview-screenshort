---
name: frontend-review
description: Capture one real rendered webpage, read the screenshot, and continue with screenshot-based frontend UI/UX/layout review. Use this when Claude should not stop at capture-only output.
argument-hint: <url> [--mode fullpage|viewport] [--device desktop|tablet|mobile] [--wait] [--engine auto|headless|aws]
allowed-tools: Bash, Read
---

# Frontend Review Skill

Use this skill when the goal is not just to capture a page, but to continue directly into evidence-first frontend review.

## Workflow

1. Parse `$ARGUMENTS`.
   - first positional arg = URL
   - optional flags: `--mode`, `--device`, `--wait`, `--engine`

2. Run the installed screenshot engine and force machine-readable output plus a persisted report file:
   ```bash
   report_file="$(mktemp /tmp/webview_frontend_review_XXXXXX.json)" && python3 "${CLAUDE_PLUGIN_ROOT}/screenshot.py" $ARGUMENTS --output-format json --report-file "$report_file"
   ```

3. Read the JSON report file from the returned `report_path`.

4. If capture succeeded, read the image file at `output_path`.

5. Continue with visual review using the screenshot as evidence. Focus on:
   - layout balance
   - spacing and hierarchy
   - readability
   - navigation/sidebar behavior
   - obvious CSR/hydration rendering problems
   - visible UI/UX issues worth fixing before code suggestions

6. Only then recommend frontend changes.

## Output expectations
- exact screenshot path
- exact report path
- capture metadata
- visible layout / UX / UI findings
- concise next fixes based on the screenshot evidence
