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

3. If the review should be preserved as a reusable QA artifact, persist a named compare session after the comparison step:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/compare_session.py" --name "session-name" --left-report <report-a.json> --right-report <report-b.json> --comparison-json <comparison.json> --output <session.json>
   ```

4. Read both JSON report files.

5. Confirm that each report is a valid `webview-screenshort.capture-report/v1` artifact.

6. Read the helper output and extract the referenced screenshot pairs.

7. Read the referenced image files.

8. Compare the screenshots and summarize:
   - layout differences
   - spacing or hierarchy changes
   - responsive regressions
   - missing/added panels, cards, or nav blocks
   - obvious before/after wins or regressions

9. If the review should end in a reusable machine-readable verdict rather than raw comparison metadata only, run:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/qa_verdict.py" <comparison-or-session.json> --output-format json
   ```

10. Keep the output evidence-first and mention which report/image paths were compared.

## Output expectations
- exact report paths used
- exact screenshot paths used
- structured pair metadata from the helper output
- visible differences grouped clearly
- concise judgment about improvement, regression, or mixed result
