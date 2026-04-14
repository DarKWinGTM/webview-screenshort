---
name: responsive-review
description: Capture one page across desktop, tablet, and mobile, then continue with cross-breakpoint frontend review. Prefer richer witness bundles so responsive review can use screenshot plus rendered HTML/rendered text and semantic page witness output where useful.
argument-hint: <public-url> [--mode viewport|fullpage] [--wait] [--engine auto|headless|aws] [--witness-mode responsive|frontend-default|csr-debug|session-replay] [--header NAME:VALUE] [--origin-header Prerendercloud-Name:VALUE] [--cookie NAME=VALUE] [--cookie-file FILE] [--preloaded-state-json JSON] [--preloaded-state-file FILE]
allowed-tools: Bash, Read
---

# Responsive Review Skill

Use this skill when Claude should capture the same page across the core breakpoints and continue into responsive frontend review.

This workflow is for publicly reachable http(s) pages only. It is not designed for `localhost`, `127.0.0.1`, or private/local network targets because the current capture engines use remote services.

## Workflow

1. Parse `$ARGUMENTS`.
   - first positional arg = publicly reachable http(s) URL
   - optional flags: `--mode`, `--wait`, `--engine`

2. Prefer `--witness-mode responsive` so the capture run can emit richer responsive witnesses rather than screenshots only.

3. Run the installed screenshot engine with one responsive capture set and persist a machine-readable report file:
   ```bash
   report_file="$(mktemp /tmp/webview_responsive_review_XXXXXX.json)" && extra_witness_args="" && case " $ARGUMENTS " in *" --witness-mode "*) ;; *) extra_witness_args="--witness-mode responsive" ;; esac && PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" python3 -m webview_screenshort.cli.screenshot $ARGUMENTS --capture-set responsive $extra_witness_args --output-format json --report-file "$report_file"
   ```

4. Read the JSON report file from the returned `report_path`.

5. If capture succeeded, read each image file from `captures[].output_path`.

6. If rendered HTML / rendered text witnesses were emitted for each responsive capture, read them too before concluding on content or CSR differences.

7. If semantic page witnesses were emitted for each responsive capture, read them too so heading/nav/form/content-shape drift across breakpoints is easier to spot.

8. Continue with responsive review using the images as evidence. Compare:
   - content hierarchy
   - overflow / cropping risk
   - card stacking
   - sidebar or nav behavior
   - readability and spacing density
   - issues that are desktop-only, tablet-only, mobile-only, or cross-device

9. Only then recommend frontend changes.

## Output expectations
- exact capture-set report path
- exact evidence bundle path when emitted
- per-device screenshot paths
- per-device rendered HTML / rendered text paths when emitted
- per-device semantic page witness paths when emitted
- per-device viewport metadata
- cross-breakpoint findings
- concise recommended fixes based on the screenshot evidence plus any richer responsive witnesses that were available
