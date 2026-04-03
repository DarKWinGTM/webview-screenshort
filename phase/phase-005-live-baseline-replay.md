# Phase 005 - Live baseline replay

> **Summary File:** [SUMMARY.md](SUMMARY.md)
> **Phase ID:** 005
> **Status:** Implemented - Pending Review
> **Design References:** [../design/design.md](../design/design.md)
> **Patch References:** [../patch/phase-005-live-baseline-replay.patch.md](../patch/phase-005-live-baseline-replay.patch.md)

---

## Objective

Add a higher-level reference-QA workflow that starts from a saved reference bundle plus a live URL, captures a fresh current report automatically, and emits a new expected/actual compare session in one run.

## Why this phase exists

The package already supported reusable baseline bundles and report-based apply-reference flows, but it still required the caller to capture the current report separately before replaying a saved baseline. That left a product gap between reusable baseline storage and practical live frontend QA. This phase closes that gap and also hardens baseline metadata so replay no longer depends only on implicit session-left conventions.

## Action points / execution checklist

- [x] add a higher-level helper that captures a fresh current report from a live URL and applies a saved bundle automatically
- [x] add a dedicated skill surface for live baseline replay
- [x] extend bundle metadata with explicit reference-side and reference-report fields
- [x] extend apply-reference flow with optional diff-dir support and richer emitted metadata
- [x] harden bundle listing so old bundles still display useful fallback metadata
- [x] fix diff-pixel counting so RGBA visual changes are measured more honestly
- [x] update agent orchestration guidance for the new live baseline replay path
- [x] validate the live replay flow against the NodeClaw docs page

## Verification

- `reference_live_bundle.py` can capture a fresh current report from a live URL and emit a new compare session in one run
- `skills/reference-live-review/SKILL.md` exposes the new workflow clearly
- `create_reference_bundle.py` emits explicit `reference_side` and `reference_report_path`
- `apply_reference_bundle.py` accepts `--diff-dir` and emits richer replay metadata
- `list_reference_bundles.py` keeps useful fallback behavior for older bundles that predate the new explicit fields
- `diff_images.py` counts non-zero RGBA diff pixels directly

## Exit criteria

- saved reference bundle + live URL replay works in one step
- legacy bundles still list and replay cleanly enough
- docs and governance surfaces describe the new workflow honestly
- version/package metadata are ready for release and install update
