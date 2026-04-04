# Webview Screenshort

## 0) Document Control

> **Parent Scope:** TEMPLATE / PLUGIN / webview-screenshort
> **Current Version:** 2.17.0
> **Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e (2026-04-03)

---

## 1) Goal

Provide a governed standalone-repo plugin package that captures real rendered webpages so Claude can use screenshots as visual evidence during frontend development.

The target is not only a raw screenshot CLI.
The target is a frontend-development vision workflow where Claude can:
- capture a live page
- verify CSR/SPA rendering state
- inspect real layout and UI output
- use screenshot evidence before recommending frontend changes

---

## 2) Active package model

The intended package model is:
- `.claude-plugin/plugin.json` = plugin metadata
- `.claude-plugin/marketplace.json` = standalone repo-local marketplace manifest for cutover and local install from this package root
- `skills/screenshot/SKILL.md` = primary runtime entrypoint for focused capture
- `skills/screenshot/*.md` = focused frontend vision workflow guidance
- `skills/frontend-review/SKILL.md` = direct capture-then-review skill surface
- `skills/responsive-review/SKILL.md` = direct cross-breakpoint capture-then-review skill surface
- `skills/compare-review/SKILL.md` = report-to-report comparison and regression-review skill surface
- `skills/reference-bundles/SKILL.md` = bundle lifecycle surface for listing, creating, and applying reusable baseline artifacts
- `skills/reference-live-review/SKILL.md` = live baseline replay surface for saved expected bundles plus fresh live URLs
- `skills/qa-verdict/SKILL.md` = verdict surface that turns compare/live-replay artifacts into reusable QA outcomes
- `skills/qa-gate/SKILL.md` = threshold-aware gate surface that applies policy rules on top of verdict artifacts
- `skills/reference-live-gate/SKILL.md` = one-step gate surface for saved baseline + live URL + policy evaluation
- `agents/webview-vision-assist.md` = optional visual-review companion agent
- `screenshot.py` = execution engine with focused capture plus one-run responsive capture-set support
- `compare_reports.py` = report comparison helper for expected/actual and before/after review workflows
- `qa_verdict.py` = verdict helper for per-device pass/fail/invalid output on top of compare/live-replay artifacts
- `qa_gate.py` = gate helper for policy/threshold checks on top of verdict output
- `reference_live_gate.py` = one-step helper that captures a live current report, replays a saved baseline, and evaluates the result against gate policy
- `diff_images.py` = image-diff helper for richer compare-review evidence
- `compare_session.py` = named compare-session helper for reusable expected/actual QA artifacts
- `list_compare_sessions.py` = compare-session index/history helper for reusable QA browsing
- `create_reference_bundle.py` = expected-reference bundle helper for reusable baseline artifacts
- `apply_reference_bundle.py` = apply-reference helper for re-running expected/actual QA against fresh reports
- `reference_live_bundle.py` = higher-level helper that captures a fresh current report from a live URL and applies a saved bundle automatically
- `list_reference_bundles.py` = reference-bundle browser helper for reusable baseline discovery
- `screenshot/` = generated screenshots and checked local artifacts
- `design/changelog/TODO/phase/patch` = governance authority at the standalone repo root

---

## 3) Runtime contract

### 3.1 Primary execution path
The skill should remain the main runtime surface.

Why:
- screenshot capture is a tooling action
- the user often wants a direct command
- capture should happen before analysis
- installed plugin execution should resolve through `${CLAUDE_PLUGIN_ROOT}` rather than a source-workspace-only path

### 3.2 Companion agent path
An optional agent can help when the task is not just “take a screenshot” but “use screenshots to review the frontend visually.”

That agent should:
- trigger screenshot capture first
- prefer visual evidence before advice
- support layout / UX / UI review workflows

---

## 4) Frontend vision workflow

The intended frontend-development workflow is:

```text
Need visual frontend review
  → capture the page
  → use --wait when CSR/SPA rendering is likely
  → choose viewport or fullpage
  → choose desktop / tablet / mobile preset when focused responsive review matters
  → prefer `--capture-set responsive` when the same page should be checked across all three breakpoints in one run
  → prefer JSON result output for workflow chaining
  → persist a report file when a later step should re-read structured capture metadata directly
  → save screenshot locally
  → read the image
  → when comparing states, re-read two report files and compare the referenced screenshots through structured pair metadata
  → persist a named compare session when the expected/actual review should remain reusable later
  → list or reopen saved compare sessions when QA history should be reused
  → create a reference bundle when a saved expected state should become a reusable baseline
  → apply a saved reference bundle when a fresh actual state should be checked against that baseline automatically
  → replay a saved reference bundle directly against a live URL when the current actual report should be captured on demand in the same flow
  → browse saved reference bundles when the reusable baseline set should be discoverable later
  → generate a machine-readable QA verdict when compare/live-replay output should become reusable pass/fail evidence
  → apply threshold-aware gate rules when explicit acceptance policy should decide pass/fail
  → run one-step baseline gate flow when capture + replay + policy evaluation should finish in one workflow
  → analyze layout / UX / UI from the screenshot
  → then recommend code or design changes
```

---

## 5) CSR support model

CSR support is considered sufficient when:
- a page that depends on client-side rendering still produces a meaningful rendered screenshot
- `--wait` improves post-hydration capture when needed
- viewport and fullpage modes both preserve useful frontend-review evidence

Checked local verification now shows:
- `https://claw-frontend-dev.nodenetwork.ovh/docs` renders successfully in viewport mode with `--wait`
- the same page also renders successfully in fullpage mode with `--wait`
- `https://developer.mozilla.org/en-US/docs/Web/JavaScript` renders successfully in viewport mode with `--wait`
- the same MDN page also renders successfully with `--device mobile` and `--device tablet` presets using structured JSON output

This is evidence that the current engine can already support more than one real frontend docs workflow and can now contribute to responsive frontend review, not only desktop capture.

Checked baseline-replay validation now also shows:
- a saved reference bundle can now carry explicit `reference_side` and `reference_report_path` metadata instead of relying only on implicit left-side session interpretation
- newly created reference bundles now include a bundled reference report payload plus copied baseline images so replay does not depend only on the original external report path surviving
- `apply_reference_bundle.py` now supports optional diff-output enrichment while replaying a saved baseline against a current report
- `compare_reports.py` now fails the top-level comparison when paired diff analysis fails instead of silently blessing non-diffable comparisons
- `reference_live_bundle.py` can capture a fresh responsive current report from a live URL and emit a new expected/actual compare session in one run

Checked responsive review validation now also shows:
- `https://claw-frontend-dev.nodenetwork.ovh/docs` captures successfully in desktop, tablet, and mobile viewport presets
- the same page also captures successfully through one responsive capture-set run that returns combined JSON metadata plus per-device image outputs
- the package can therefore support same-page cross-breakpoint review rather than only one-off single captures

---

## 6) Design boundaries

### What this package is
- screenshot capture for frontend development
- visual evidence generation for Claude review
- CSR-aware webpage capture with optional wait behavior
- a standalone plugin skill that now supports repo-root local marketplace install workflows

### What this package is not
- a full browser automation suite
- a DOM testing framework
- a generic backend tool
- a replacement for deeper UI analysis tools; it is the visual input step

---

## 7) Current limitations

- current workflow still relies on Claude reading the generated image after capture instead of a fully bundled tool-native visual-analysis pipeline, even though report files, review skills, compare-review entrypoints, helper-generated pair metadata, diff images, named compare sessions, compare-session history browsing, reference bundles, apply-reference workflows, live bundle replay, verdict generation, gate evaluation, one-step baseline gating, and reference-bundle browsing now reduce the manual handoff surface
- plugin install lifecycle for this package is now validated from the standalone repo root through its package-local marketplace manifest, while the shared `darkwingtm` route remains only temporary checked local compatibility context
- broader CSR validation still needs more than the two currently checked public docs targets

---

## 8) Acceptance criteria

This package is considered successful for the current wave when:
- it has proper plugin package structure
- the screenshot skill works from the installed plugin path through `${CLAUDE_PLUGIN_ROOT}`
- the stale path from the old project-local skill model is removed
- real CSR pages can be captured successfully
- the package clearly supports frontend visual review workflows
- `screenshot.py` supports late-bound config for endpoints/timeouts
- `screenshot.py` supports machine-readable JSON output and persisted report-file output for workflow chaining
- `compare_reports.py` supports structured report-to-report pairing for expected/actual and regression-style review
- `screenshot.py` supports one-run responsive capture-set output for desktop/tablet/mobile review
- `screenshot.py` supports mobile and tablet viewport presets for responsive review
- saved reference bundles carry explicit reference-side/report metadata for more reliable replay
- newly created reference bundles store a bundled reference report payload and copied baseline images instead of depending only on the original external report path
- the package can replay a saved baseline directly against a live URL without requiring the caller to capture the current report separately first
- compare/live-replay artifacts can now be converted into reusable machine-readable verdicts with per-device pass/fail/invalid output
- threshold-aware gate policy can now be applied on top of verdict artifacts with required-device and diff-threshold rules
- one-step baseline gate flow can now capture current state, replay a saved baseline, and apply policy evaluation in one run
- a reusable strict responsive zero-diff policy preset now exists for immediate gate reuse
- non-diffable paired comparisons are now treated as failed instead of being reported as successful replay sessions
- governance docs describe the real current state rather than the older project-local skill state
