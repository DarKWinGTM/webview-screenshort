---
name: screenshot
description: Capture a real rendered webpage for frontend-development review. Default to screenshot evidence, but support richer witness modes such as rendered HTML and rendered text when CSR/debug context needs more than an image alone.
argument-hint: <public-url> [--mode fullpage|viewport] [--device desktop|tablet|mobile] [--capture-set responsive] [--report-file FILE] [--bundle-file FILE] [--wait] [--engine auto|headless|aws] [--witness-mode visual|frontend-default|csr-debug|responsive|session-replay] [--header NAME:VALUE] [--origin-header Prerendercloud-Name:VALUE] [--cookie NAME=VALUE] [--cookie-file FILE] [--preloaded-state-json JSON] [--preloaded-state-file FILE] [--output FILE] [--output-format json]
allowed-tools: Bash, Read
---

# Screenshot Skill

Capture a webpage screenshot from `$ARGUMENTS` so Claude can inspect the real rendered UI.

This skill is for publicly reachable http(s) pages only. It is not designed for `localhost`, `127.0.0.1`, or private/local network targets because the current capture engines run through remote services.

This skill must stay on the API-based package path. It must never probe or depend on Playwright, Chromium, Chrome, WebKit, Selenium, Puppeteer, or any other local browser stack.

## What this skill is for
Use it when frontend work needs real page evidence, for example:
- layout review
- UX/UI inspection
- CSR/hydration verification
- docs page visual checks
- dashboard/page-state comparison before recommending changes
- rendered HTML / rendered text witness capture when screenshot-only evidence is not enough
- logged-in-state capture when the user can provide headers/cookies/session material explicitly

## Execution Steps

1. Parse arguments from `$ARGUMENTS`.
   - first positional arg = publicly reachable http(s) URL
   - optional flags: `--mode`, `--device`, `--capture-set`, `--report-file`, `--bundle-file`, `--wait`, `--engine`, `--witness-mode`, `--header`, `--origin-header`, `--cookie`, `--cookie-file`, `--preloaded-state-json`, `--preloaded-state-file`, `--output`, `--output-format`

2. Choose the witness mode intentionally:
   - `visual` = screenshot-first only
   - `frontend-default` = screenshot + rendered HTML + rendered text + semantic page witness
   - `csr-debug` = screenshot + rendered HTML + prerender HTML + semantic page witness when CSR timing/debug needs deeper witnesses
   - `responsive` = richer witness bundle across desktop/tablet/mobile, including semantic page witnesses per device
   - `session-replay` = richer witness bundle plus user-provided auth context and optional bounded origin-bootstrap preload replay

3. Do not run local browser discovery or fallback commands such as Playwright imports, Chromium lookup, or Chrome availability probes.

4. Run the capture engine from this installed plugin package:
   ```bash
   PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" python3 -m webview_screenshort.cli.screenshot $ARGUMENTS
   ```

5. Prefer adding `--output-format json` when the result will feed a follow-on review workflow.

6. Prefer `--report-file` when compatibility with current compare/replay flows matters.

7. Prefer `--bundle-file` or a non-`visual` witness mode when the task needs more than screenshots alone.

8. If the task needs one-shot responsive review, prefer `--capture-set responsive` so the tool returns one machine-readable payload with desktop, tablet, and mobile results together.

9. If the page requires login and the user can provide session material, use explicit `--header`, `--origin-header`, `--cookie`, `--cookie-file`, `--preloaded-state-json`, or `--preloaded-state-file` inputs. Treat authenticated capture as operator-provided, not as an interactive login workflow.

10. Use bounded preloaded-state replay only when the origin/app is prepared to reconstruct forwarded preload headers into `window.__PRELOADED_STATE__`. Do not treat this as direct browser `localStorage` / `sessionStorage` injection.

11. If capture succeeds:
   - report the exact screenshot file path
   - if `--report-file` was used, report the exact JSON report path
   - if an evidence bundle was emitted, report the exact bundle path
   - if rendered HTML / rendered text witnesses were emitted, report their exact paths
   - if semantic page witnesses were emitted, report their exact JSON path or per-device semantic witness paths
   - if `--capture-set responsive` was used, report the per-device screenshot paths and viewport metadata
   - if the user wants visual review, read the image file next and continue from the screenshot evidence

12. If capture fails:
   - report the error clearly
   - if the target was rejected because it is `localhost`, loopback, or private/local network scope, explain that this package currently supports only publicly reachable http(s) pages and suggest using a public domain or tunnel first
   - otherwise suggest a narrower retry such as `--wait`, `--mode viewport`, `--engine headless`, or a richer witness mode when CSR timing is the likely cause

## Default Behavior
- Engine: `auto`
- Mode: `fullpage`
- Witness mode: `visual`
- Wait: off by default; turn on for CSR / SPA pages

## Recommended Usage
```bash
/screenshot https://example.com --wait --mode viewport
/screenshot https://example.com/docs --wait --mode fullpage --witness-mode frontend-default --output-format json --report-file /tmp/example_capture.json
/screenshot https://example.com/app --wait --mode viewport --witness-mode csr-debug --output-format json --bundle-file /tmp/example_bundle.json
/screenshot https://example.com --capture-set responsive --wait --mode viewport --witness-mode responsive --output-format json --report-file /tmp/example_responsive.json
/screenshot https://example.com/private --wait --mode viewport --witness-mode session-replay --cookie-file /tmp/session.json --output-format json
/screenshot https://example.com/private --wait --mode viewport --witness-mode session-replay --cookie "nodeclaw_session=..." --preloaded-state-json '{"locale":"th","cookieNoticeAcknowledged":true}' --output-format json
```
