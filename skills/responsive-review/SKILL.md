---
name: responsive-review
description: Capture one page across desktop, tablet, and mobile, then continue with cross-breakpoint screenshot-based frontend review. Use this when responsive behavior is the main review target.
argument-hint: <url> [--mode viewport|fullpage] [--wait] [--engine auto|headless|aws]
allowed-tools: Bash, Read
---

# Responsive Review Skill

Use this skill when Claude should capture the same page across the core breakpoints and continue into responsive frontend review.

## Workflow

1. Parse `$ARGUMENTS`.
   - first positional arg = URL
   - optional flags: `--mode`, `--wait`, `--engine`

2. Run the installed screenshot engine with one responsive capture set and persist a machine-readable report file:
   ```bash
   report_file="$(mktemp /tmp/webview_responsive_review_XXXXXX.json)" && python3 "${CLAUDE_PLUGIN_ROOT}/screenshot.py" $ARGUMENTS --capture-set responsive --output-format json --report-file "$report_file"
   ```

3. Read the JSON report file from the returned `report_path`.

4. If capture succeeded, read each image file from `captures[].output_path`.

5. Continue with responsive review using the images as evidence. Compare:
   - content hierarchy
   - overflow / cropping risk
   - card stacking
   - sidebar or nav behavior
   - readability and spacing density
   - issues that are desktop-only, tablet-only, mobile-only, or cross-device

6. Only then recommend frontend changes.

## Output expectations
- exact capture-set report path
- per-device screenshot paths
- per-device viewport metadata
- cross-breakpoint findings
- concise recommended fixes based on the screenshot evidence
