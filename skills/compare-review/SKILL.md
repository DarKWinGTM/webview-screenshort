---
name: compare-review
description: Compare two previously generated capture reports and review the referenced screenshots for visible UI/layout differences. Use this for before/after, expected/actual, or regression-style frontend review.
argument-hint: <report-a.json> <report-b.json>
allowed-tools: Read
---

# Compare Review Skill

Use this skill when frontend review should compare two already-generated screenshot report artifacts instead of taking a fresh capture first.

## Workflow

1. Parse `$ARGUMENTS`.
   - first positional arg = report A path
   - second positional arg = report B path

2. Read both JSON report files.

3. Confirm that each report is a valid `webview-screenshort.capture-report/v1` artifact.

4. Extract the referenced screenshot paths.
   - for focused captures: `result.output_path`
   - for responsive capture sets: each `result.captures[].output_path`

5. Read the referenced image files.

6. Compare the screenshots and summarize:
   - layout differences
   - spacing or hierarchy changes
   - responsive regressions
   - missing/added panels, cards, or nav blocks
   - obvious before/after wins or regressions

7. Keep the output evidence-first and mention which report/image paths were compared.

## Output expectations
- exact report paths used
- exact screenshot paths used
- visible differences grouped clearly
- concise judgment about improvement, regression, or mixed result
