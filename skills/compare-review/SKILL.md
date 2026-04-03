---
name: compare-review
description: Compare two previously generated capture reports and review the referenced screenshots for visible UI/layout differences. Use this for before/after, expected/actual, or regression-style frontend review.
argument-hint: <report-a.json> <report-b.json>
allowed-tools: Bash, Read
---

# Compare Review Skill

Use this skill when frontend review should compare two already-generated screenshot report artifacts instead of taking a fresh capture first.

## Workflow

1. Parse `$ARGUMENTS`.
   - first positional arg = report A path
   - second positional arg = report B path

2. Run the installed comparison helper to validate the two reports and emit structured comparison metadata:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/compare_reports.py" $ARGUMENTS --output-format json
   ```

3. Read both JSON report files.

4. Confirm that each report is a valid `webview-screenshort.capture-report/v1` artifact.

5. Read the helper output and extract the referenced screenshot pairs.

6. Read the referenced image files.

7. Compare the screenshots and summarize:
   - layout differences
   - spacing or hierarchy changes
   - responsive regressions
   - missing/added panels, cards, or nav blocks
   - obvious before/after wins or regressions

7. Keep the output evidence-first and mention which report/image paths were compared.

## Output expectations
- exact report paths used
- exact screenshot paths used
- structured pair metadata from the helper output
- visible differences grouped clearly
- concise judgment about improvement, regression, or mixed result
