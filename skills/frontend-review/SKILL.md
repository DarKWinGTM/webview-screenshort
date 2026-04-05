---
name: frontend-review
description: Capture one real rendered webpage, read the screenshot, and continue with frontend UI/UX/layout review. Prefer a richer witness bundle (screenshot + rendered HTML + rendered text) when CSR/frontend-development context needs more than an image alone.
argument-hint: <url> [--mode fullpage|viewport] [--device desktop|tablet|mobile] [--wait] [--engine auto|headless|aws] [--witness-mode frontend-default|csr-debug|session-replay] [--header NAME:VALUE] [--origin-header Prerendercloud-Name:VALUE] [--cookie NAME=VALUE] [--cookie-file FILE]
allowed-tools: Bash, Read
---

# Frontend Review Skill

Use this skill when the goal is not just to capture a page, but to continue directly into evidence-first frontend review.

## Workflow

1. Parse `$ARGUMENTS`.
   - first positional arg = URL
   - optional flags: `--mode`, `--device`, `--wait`, `--engine`

2. Default to a richer witness mode for frontend-development review:
   - `frontend-default` for normal real-page review
   - `csr-debug` when CSR/hydration incompleteness is suspected
   - `session-replay` when the user provides headers/cookies/session material explicitly

3. Run the installed capture engine and force machine-readable output plus a persisted report file:
   ```bash
   report_file="$(mktemp /tmp/webview_frontend_review_XXXXXX.json)" && python3 "${CLAUDE_PLUGIN_ROOT}/screenshot.py" $ARGUMENTS --witness-mode frontend-default --output-format json --report-file "$report_file"
   ```

4. Read the JSON report file from the returned `report_path`.

5. If capture succeeded, read the image file at `output_path`.

6. If rendered HTML / rendered text witnesses were emitted, read them too before concluding on CSR/content issues.

7. Continue with visual review using the screenshot as evidence. Focus on:
   - layout balance
   - spacing and hierarchy
   - readability
   - navigation/sidebar behavior
   - obvious CSR/hydration rendering problems
   - visible UI/UX issues worth fixing before code suggestions

8. Only then recommend frontend changes.

## Output expectations
- exact screenshot path
- exact report path
- exact rendered HTML / rendered text paths when emitted
- capture metadata
- visible layout / UX / UI findings
- concise next fixes based on the screenshot evidence plus any richer witnesses that were available
