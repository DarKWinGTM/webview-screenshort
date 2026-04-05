# Phase 010 - Package reorganization

> **Summary File:** [SUMMARY.md](SUMMARY.md)
> **Phase ID:** 010
> **Status:** Implemented - Pending Review
> **Design References:** [../design/design.md](../design/design.md)
> **Patch References:** [../patch/phase-010-package-reorganization.patch.md](../patch/phase-010-package-reorganization.patch.md)

---

## Objective

Reorganize the Python codebase into clearer package-internal domains so compare, QA, reference, and CLI logic no longer live only as a flat root-script pile.

## Why this phase exists

The package already had a useful internal runtime boundary for capture, but too much reusable logic still lived in root-level scripts. That made the repo look tactical, blurred the difference between CLI entrypoints and reusable library code, and allowed package-internal modules such as `webview_screenshort/workflows.py` to import root scripts directly. This phase moves the codebase toward a more professional Python project layout while preserving current root command compatibility.

## Action points / execution checklist

- [x] add package-internal domains for compare, QA, references, CLI adapters, and shared schemas
- [x] move compare/diff/session logic behind package-internal modules
- [x] move QA verdict/gate/policy logic behind package-internal modules
- [x] move reference-bundle and live replay orchestration behind package-internal modules
- [x] convert root Python commands into compatibility-thin wrappers over package CLI adapters
- [x] remove root-script imports from `webview_screenshort/workflows.py`
- [x] reduce direct script-to-script subprocess coupling where in-process module reuse now exists
- [x] keep `screenshot.py` as the main capture entrypoint rather than folding unrelated utilities into it
- [x] sync docs/version metadata for the package-organization wave

## Verification

- `python3 -m py_compile` succeeds across the root wrappers and newly added package modules
- `python3 compare_reports.py /tmp/webview_semantic_focus_report.json /tmp/webview_semantic_focus_report.json --output-format json` succeeds
- `python3 compare_session.py --name wrapper-check ...` succeeds
- `python3 create_reference_bundle.py --name wrapper-check ...` succeeds
- `python3 apply_reference_bundle.py --bundle /tmp/webview_wrapper_bundle.json ...` succeeds
- `python3 qa_verdict.py /tmp/webview_wrapper_apply_session.json --output-format json` succeeds
- `python3 qa_gate.py /tmp/webview_wrapper_apply_session.json --policy-preset strict/responsive-zero-diff --output-format json` returns the expected policy result for the checked artifact shape
- `python3 list_policy_presets.py --output-format json`, `python3 list_compare_sessions.py /tmp --output-format json`, and `python3 list_reference_bundles.py /tmp --output-format json` all succeed after robust non-artifact skipping
- `claude plugins validate /home/node/workplace/AWCLOUD/TEMPLATE/PLUGIN/webview-screenshort` succeeds

## Exit criteria

- root Python commands are visibly thinner and act as stable command surfaces
- package-internal modules depend on package modules instead of importing root scripts directly
- compare / QA / reference logic is grouped by role rather than scattered as mixed top-level scripts
- the codebase reads more like a professional Python package while preserving current command compatibility
