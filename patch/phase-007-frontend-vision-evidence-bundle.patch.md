# Phase 007 Frontend Vision Evidence Bundle Patch

## 0) Document Control

> **Current Version:** 1.0
> **Status:** Implemented - Pending Review
> **Target Design:** [../design/design.md](../design/design.md) v2.22.0
> **Target Phase:** [../phase/phase-007-frontend-vision-evidence-bundle.md](../phase/phase-007-frontend-vision-evidence-bundle.md)
> **Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e
> **Full history:** [../changelog/changelog.md](../changelog/changelog.md)

---

## 1) Context

This patch captures the strategic shift from screenshot-only runtime scripts toward a reusable frontend-vision runtime package with richer witnesses and bounded session-replay capture.

## 2) Analysis

Risk level: Medium-High

The package already has strong screenshot QA workflows, but the runtime implementation is still fragmented across top-level scripts and subprocess chains. At the same time, frontend-development workflows now need richer witnesses than images alone, especially for CSR pages and authenticated pages where rendered HTML / rendered text can provide stronger evidence than screenshot-only review.

---

## 3) Change Items

### Change Item 1
- **Target location:** `webview_screenshort/`
- **Change type:** additive

**Before**
```text
Most runtime/orchestration logic lived directly in top-level scripts.
```

**After**
```text
A reusable internal Python package owns auth context, headless-render-api integration, capture service logic, and higher-level workflow orchestration.
```

### Change Item 2
- **Target location:** `screenshot.py`
- **Change type:** replacement

**Before**
```text
The main screenshot CLI owned screenshot capture logic directly and only emitted screenshot/report artifacts.
```

**After**
```text
The screenshot CLI becomes a thinner wrapper that can request richer witness modes and emit screenshot/report/evidence-bundle outputs through the internal runtime package.
```

### Change Item 3
- **Target location:** runtime capture artifacts
- **Change type:** additive

**Before**
```text
The package only had screenshot-first capture artifacts plus screenshot-era compatibility reports.
```

**After**
```text
The runtime can now emit richer evidence artifacts including rendered HTML, rendered text, and a new `webview-screenshort.evidence-bundle/v1` payload alongside the existing screenshot report model.
```

### Change Item 4
- **Target location:** session-replay capture inputs and routing docs
- **Change type:** additive

**Before**
```text
Authenticated page capture had no explicit operator-facing contract.
```

**After**
```text
The package now introduces bounded auth-context inputs (`--header`, `--origin-header`, `--cookie`, `--cookie-file`) and documents that authenticated capture is operator-provided rather than interactive login automation.
```

### Change Item 5
- **Target location:** `reference_live_bundle.py`, `reference_live_gate.py`, `compare_reports.py`, `create_reference_bundle.py`, skills, and agent routing docs
- **Change type:** replacement

**Before**
```text
Live replay/gate flows were screenshot-first, compare/reference-bundle flows assumed screenshot-era report inputs only, and routing prose did not explicitly choose witness modes.
```

**After**
```text
Live replay/gate wrappers now route through reusable internal workflows, compare/reference-bundle flows can accept richer evidence-bundle sources, and the screenshot/agent/review surfaces describe witness-mode-aware frontend vision with session-replay wording instead of screenshot-only assumptions.
```

---

## 4) Verification

- [x] `python3 -m py_compile screenshot.py compare_reports.py compare_session.py create_reference_bundle.py apply_reference_bundle.py reference_live_bundle.py reference_live_gate.py qa_verdict.py qa_gate.py policy_presets.py webview_screenshort/__init__.py webview_screenshort/auth_context.py webview_screenshort/headless_render_api.py webview_screenshort/capture_service.py webview_screenshort/workflows.py` succeeds
- [x] `python3 screenshot.py https://example.com --engine headless --mode viewport --witness-mode frontend-default --output-format json --report-file /tmp/webview_v222_report.json` succeeds and emits rendered HTML / rendered text witness paths
- [x] `python3 screenshot.py https://example.com --engine headless --mode viewport --witness-mode csr-debug --output-format json --report-file /tmp/webview_v222_csr_report.json` succeeds and emits richer CSR witness artifacts
- [x] `python3 screenshot.py https://example.com --engine headless --mode viewport --witness-mode session-replay --header "Authorization: Bearer secret-token-value" --origin-header "Prerendercloud-Debug-User: alice" --cookie "sessionid=supersecret" --output-format json --report-file /tmp/webview_v222_auth_report.json` succeeds and persists redacted session-replay summaries only
- [x] `python3 reference_live_bundle.py ...` still succeeds after the internal workflow refactor
- [x] `python3 reference_live_gate.py ...` still succeeds after the internal workflow refactor
- [x] existing screenshot-era compare/verdict/gate flows remain usable
- [x] persisted auth summaries are redacted and do not store raw secret values

---

## 5) Rollback Approach

If the richer-witness refactor proves unstable, keep the internal package extraction but narrow runtime output back to screenshot/report compatibility first. Do not roll back the strategic package boundary unless the wrapper/core split itself proves harmful. If session-replay capture is noisy, keep the runtime redaction contract and disable only the exposed auth-input surface until a narrower provider-backed contract is ready.
