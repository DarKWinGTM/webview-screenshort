# Webview Screenshort - Phase Summary

> **Current Version:** 2.20.0
> **Target Design:** [../design/design.md](../design/design.md) v2.20.0
> **Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e
> **Status:** Implemented - Pending Review
> **Full history:** [../changelog/changelog.md](../changelog/changelog.md)

---

## Context

This phase workspace tracks the conversion of `webview-screenshort` from an older project-local skill utility into a governed plugin package for frontend-development visual workflows.

---

## Source-Input Extraction Summary

| Phase | Phase File | Design Source | Patch Source | Derived Execution Work | Target Outcome |
|---|---|---|---|---|---|
| 001 | `phase-001-convert-to-plugin-package.md` | `design/design.md` active package model | `../patch/phase-001-convert-to-plugin-package.patch.md` | Convert old project-local layout into governed plugin package structure | Package has standard plugin layout |
| 002 | `phase-002-validate-csr-screenshot-workflow.md` | `design/design.md` CSR support model | `../patch/phase-002-validate-csr-screenshot-workflow.patch.md` | Validate real CSR capture, responsive presets, and frontend-vision use case | Real CSR page capture and responsive review support are evidence-backed |
| 003 | `phase-003-install-and-lifecycle-validation.md` | `design/design.md` runtime contract | `none` | Validate plugin install, skill visibility, and runtime lifecycle | Package works as installed plugin |
| 004 | `phase-004-separate-repo-cutover.md` | `design/design.md` plus package-local marketplace cutover posture | `../patch/phase-004-separate-repo-cutover.patch.md` | Prepare authority migration from the shared workspace into a standalone `webview-screenshort` repo | Package can cut over to its own repo without duplicate authority |
| 005 | `phase-005-live-baseline-replay.md` | `design/design.md` live baseline replay and reusable baseline model | `../patch/phase-005-live-baseline-replay.patch.md` | Add saved-bundle + live-URL replay as a first-class frontend QA workflow | Reusable baselines can be replayed directly against current live pages in one flow |

---

## Phase Map

| Phase | Status | File | Objective |
|---|---|---|---|
| 001 | Implemented - Pending Review | `phase-001-convert-to-plugin-package.md` | Convert the old utility into governed plugin package structure |
| 002 | Implemented - Pending Review | `phase-002-validate-csr-screenshot-workflow.md` | Validate real CSR capture and responsive frontend review workflows |
| 003 | Implemented - Pending Review | `phase-003-install-and-lifecycle-validation.md` | Validate install/lifecycle through plugin flow |
| 004 | Implemented - Pending Review | `phase-004-separate-repo-cutover.md` | Finalize standalone repo authority and retire shared-workspace authority posture |
| 005 | Implemented - Pending Review | `phase-005-live-baseline-replay.md` | Add saved-bundle + live-URL replay as a first-class reusable frontend QA workflow |

---

## Global TODO / Changelog Coordination

- `TODO.md` should track the active package work and shipped execution history clearly, not only the earlier cutover slice.
- `changelog/changelog.md` should record shipped plugin-structure, CSR-validation, repo-root install-normalization, responsive capture-set workflow, report-file/review-skill workflow, compare-review/report-schema workflow, structured compare-helper outcomes, diff-assisted compare outcomes, named compare-session outcomes, compare-session history outcomes, expected-reference bundle outcomes, apply-reference workflow outcomes, reference-bundle browsing outcomes, bundle-lifecycle skill-surface outcomes, live baseline replay outcomes, qa-verdict outcomes, qa-gate outcomes, one-step baseline gate outcomes, semantic preset outcomes, policy-family outcomes, repo-local marketplace install outcomes, and agent-orchestration hardening outcomes only.
- `design/design.md` remains the authority for frontend-vision intent, plugin boundaries, and standalone-repo install posture.

---

## Final Verification

- package reorganized into governed plugin layout
- real CSR docs page capture verified in viewport and fullpage modes
- stale project-local skill path identified and removed
- frontend-vision workflow intent is now explicit in docs and skill surfaces
- package validates and installs through its standalone repo-root marketplace manifest
- installed agent visibility is confirmed
- standalone repo now acts as the package authority at the public documentation/source-of-truth level
- shared `darkwingtm` marketplace usage is now scoped as local compatibility context rather than public default install authority
- installed runtime invocation now uses `${CLAUDE_PLUGIN_ROOT}`
- engine now supports env-driven configuration and JSON result output
- responsive mobile and tablet presets are validated on a second frontend target
- responsive desktop/tablet/mobile multi-capture workflow is validated on the NodeNetwork docs page
- one-run responsive capture-set workflow now returns combined desktop/tablet/mobile machine-readable results
- focused and responsive capture flows can now persist report-file artifacts for later re-reading
- dedicated `frontend-review` and `responsive-review` skill surfaces now sit above the lower-level screenshot engine
- compare-review can now compare two persisted report artifacts for regression-style visual checks
- persisted report artifacts now carry explicit schema/version metadata for reuse
- `compare_reports.py` now emits structured image-pair metadata for expected/actual and before/after review
- `diff_images.py` now emits diff metrics and optional diff images for compare workflows
- `compare_session.py` now persists named expected/actual compare sessions for later QA review
- `list_compare_sessions.py` now exposes saved compare-session history for lightweight QA browsing
- `create_reference_bundle.py` now promotes saved compare sessions into reusable expected-reference bundles
- `apply_reference_bundle.py` now replays a saved baseline against a fresh report to emit a new expected/actual session
- `list_reference_bundles.py` now exposes saved baseline bundles for lightweight QA browsing
- `skills/reference-bundles/SKILL.md` now exposes bundle listing, creation, and apply-reference work from one front door
- `reference_live_bundle.py` now captures a fresh current report from a live URL and replays a saved baseline automatically
- `skills/reference-live-review/SKILL.md` now exposes saved-baseline replay against a live URL from one front door
- `qa_verdict.py` now turns compare/live-replay artifacts into reusable machine-readable verdicts
- `qa_gate.py` now applies threshold-aware policy rules on top of verdict artifacts
- `reference_live_gate.py` now captures current state, replays a saved baseline, and applies gate policy in one flow
- reusable policy presets now exist under `support/policies/`
- policy presets now carry family-aware metadata with canonical selectors and legacy aliases
- reference bundles now carry explicit `reference_side` and `reference_report_path` metadata for more reliable replay
- repo-local marketplace path now installs `webview-screenshort@webview-screenshort` directly from the standalone repo root
- `webview-vision-assist` now routes more explicitly between focused review, responsive review, compare-review, bundle-lifecycle, live baseline replay, verdict, gate, one-step baseline gate, and preset-discovery entrypoints

---
