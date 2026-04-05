# Phase 007 - Frontend vision evidence bundle

> **Summary File:** [SUMMARY.md](SUMMARY.md)
> **Phase ID:** 007
> **Status:** Implemented - Pending Review
> **Design References:** [../design/design.md](../design/design.md)
> **Patch References:** [../patch/phase-007-frontend-vision-evidence-bundle.patch.md](../patch/phase-007-frontend-vision-evidence-bundle.patch.md)

---

## Objective

Start the strategic frontend-vision upgrade by moving runtime logic into an internal reusable package, adding richer witness modes beyond screenshot-only capture, emitting rendered HTML / rendered text evidence bundles, and preparing bounded session-replay capture for login-required pages.

## Why this phase exists

The package already works as a screenshot-first frontend QA tool, but the runtime is still too tactical: many top-level scripts shell into one another, richer witnesses are missing, and logged-in-state capture via existing session context has no bounded operator-facing contract. This phase starts the shift from screenshot utility to HTML-aware frontend vision platform while preserving the current screenshot-era review flows.

## Action points / execution checklist

- [x] add an internal `webview_screenshort/` package for reusable runtime logic
- [x] convert `screenshot.py` into a thinner wrapper over the internal runtime package
- [x] add richer witness modes (`visual`, `frontend-default`, `csr-debug`, `responsive`, `session-replay`)
- [x] emit rendered HTML / rendered text artifacts when witness mode requires them
- [x] add a new `webview-screenshort.evidence-bundle/v1` artifact alongside the existing screenshot report model
- [x] add bounded auth-context inputs (`--header`, `--origin-header`, `--cookie`, `--cookie-file`)
- [x] refactor live replay / gate orchestration to use reusable internal workflows instead of only script-to-script subprocess chaining
- [x] make compare/reference-bundle flows accept richer evidence-bundle sources instead of only screenshot-era report assumptions
- [x] upgrade screenshot / frontend-review / reference-live-review / agent wording so routing is witness-mode-aware and session-replay terminology is clearer
- [x] validate richer witness output and session-replay capture behavior end-to-end
- [x] sync changelog/release metadata after verification

## Verification

- `python3 -m py_compile screenshot.py compare_reports.py compare_session.py create_reference_bundle.py apply_reference_bundle.py reference_live_bundle.py reference_live_gate.py qa_verdict.py qa_gate.py policy_presets.py webview_screenshort/__init__.py webview_screenshort/auth_context.py webview_screenshort/headless_render_api.py webview_screenshort/capture_service.py webview_screenshort/workflows.py` succeeds
- `python3 screenshot.py https://example.com --engine headless --mode viewport --witness-mode frontend-default --output-format json --report-file /tmp/webview_v222_report.json` succeeds and emits screenshot plus rendered HTML / rendered text paths
- `python3 screenshot.py https://example.com --engine headless --mode viewport --witness-mode session-replay --header "Authorization: Bearer secret-token-value" --origin-header "Prerendercloud-Debug-User: alice" --cookie "sessionid=supersecret" --output-format json --report-file /tmp/webview_v222_auth_report.json` succeeds and persists only redacted auth summaries
- `python3 screenshot.py https://example.com --engine headless --mode viewport --witness-mode csr-debug --output-format json --report-file /tmp/webview_v222_csr_report.json` succeeds and emits screenshot plus rendered/prerender HTML witness paths
- `claude plugins validate .` succeeds from the repo root after the package metadata/runtime updates
- `reference_live_bundle.py` and `reference_live_gate.py` still emit usable machine-readable workflow payloads after the internal refactor
- `compare_reports.py` now accepts `webview-screenshort.evidence-bundle/v1` artifacts as compare inputs
- `create_reference_bundle.py` now accepts bundle-based compare sessions and preserves `reference_artifact_schema`
- compare/verdict/gate screenshot-era compatibility remains intact for existing report/session/bundle artifacts
- auth-context inputs are redacted in persisted artifacts and are not written back as raw secrets

## Exit criteria

- the package has a reusable internal runtime package instead of relying only on top-level script sprawl
- screenshot capture remains intact while richer witness modes become first-class
- rendered HTML and rendered text are emitted as evidence artifacts when requested
- logged-in-state capture has a bounded operator-provided session/context contract
- docs and routing surfaces describe witness-mode-aware frontend vision honestly
