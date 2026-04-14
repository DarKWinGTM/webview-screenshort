---
name: frontend-review
description: Capture one real rendered webpage, read the screenshot, and continue with frontend UI/UX/layout review. Prefer a richer witness bundle (screenshot + rendered HTML + rendered text + semantic page witness) when CSR/frontend-development context needs more than an image alone.
argument-hint: <public-url> [--mode fullpage|viewport] [--device desktop|tablet|mobile] [--wait] [--engine auto|headless|aws] [--witness-mode frontend-default|csr-debug|session-replay] [--header NAME:VALUE] [--origin-header Prerendercloud-Name:VALUE] [--cookie NAME=VALUE] [--cookie-file FILE] [--preloaded-state-json JSON] [--preloaded-state-file FILE]
allowed-tools: Bash, Read
---

# Frontend Review Skill

Use this skill when the goal is not just to capture a page, but to continue directly into evidence-first frontend review.

This workflow is for publicly reachable http(s) pages only. It is not designed for `localhost`, `127.0.0.1`, or private/local network targets because the current capture engines use remote services.

This workflow must stay on the API-based package path. It must never probe or depend on Playwright, Chromium, Chrome, WebKit, Selenium, Puppeteer, or any other local browser stack.

## Workflow

1. Parse `$ARGUMENTS`.
   - first positional arg = publicly reachable http(s) URL
   - optional flags: `--mode`, `--device`, `--wait`, `--engine`

2. Never run local browser discovery or fallback commands such as Playwright imports, Chromium lookup, or Chrome availability probes.

3. Default to a richer witness mode for frontend-development review:
   - `frontend-default` for normal real-page review
   - `csr-debug` when CSR/hydration incompleteness is suspected
   - `session-replay` when the user provides headers/cookies/session material explicitly, optionally paired with bounded preload-state replay for an origin that reconstructs `window.__PRELOADED_STATE__`

4. Run the installed capture engine and force machine-readable output plus a persisted report file:
   ```bash
   report_file="$(mktemp /tmp/webview_frontend_review_XXXXXX.json)" && extra_witness_args="" && case " $ARGUMENTS " in *" --witness-mode "*) ;; *) extra_witness_args="--witness-mode frontend-default" ;; esac && PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" python3 -m webview_screenshort.cli.screenshot $ARGUMENTS $extra_witness_args --output-format json --report-file "$report_file"
   ```

5. Read the JSON report file from the returned `report_path`.

6. If capture succeeded, read the image file at `output_path`.

7. If rendered HTML / rendered text witnesses were emitted, read them too before concluding on CSR/content issues.

8. If semantic page witness JSON was emitted, read it too so title/headings/links/forms/page-shape can be understood quickly before rereading raw HTML.

9. Continue with visual review using the screenshot as evidence. Focus on:
   - layout balance
   - spacing and hierarchy
   - readability
   - navigation/sidebar behavior
   - obvious CSR/hydration rendering problems
   - visible UI/UX issues worth fixing before code suggestions

10. Only then recommend frontend changes.

## Output expectations
- exact screenshot path
- exact report path
- exact rendered HTML / rendered text paths when emitted
- exact semantic page witness path when emitted
- capture metadata
- visible layout / UX / UI findings
- concise next fixes based on the screenshot evidence plus any richer witnesses that were available
