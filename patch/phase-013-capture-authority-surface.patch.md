# Phase 013 Capture Authority Surface Patch

## 0) Document Control

> **Current Version:** 1.0
> **Status:** Implemented - Pending Review
> **Target Design:** [../design/design.md](../design/design.md) v2.28.0
> **Target Phase:** [../phase/phase-013-capture-authority-surface.md](../phase/phase-013-capture-authority-surface.md)
> **Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e
> **Full history:** [../changelog/changelog.md](../changelog/changelog.md)

---

## 1) Context

This patch captures the next bounded capture cleanup slice after the first `capture_service.py` split: promoting `capture.service` into a stronger authority surface and migrating key consumers onto it.

## 2) Analysis

Risk level: Medium

The goal here is not to delete `capture_service.py` yet. The safer move is to make the newer capture package authoritative first, then let the older path remain as a compatibility facade. That reduces risk while still improving structure and import direction.

---

## 3) Change Items

### Change Item 1
- **Target location:** `webview_screenshort/capture/models.py`, `capture/engines.py`, `capture/reporting.py`, `capture/runtime.py`
- **Change type:** additive

**Before**
```text
The newer capture package had config/path/witness modules, but models/engines/reporting/runtime orchestration still lived mostly in `capture_service.py`.
```

**After**
```text
The capture package now has explicit modules for models, engines, reporting, and runtime orchestration.
```

### Change Item 2
- **Target location:** `webview_screenshort/capture/service.py`
- **Change type:** replacement

**Before**
```text
`capture/service.py` was only a trivial wildcard compatibility shim over `capture_service.py`.
```

**After**
```text
`capture/service.py` now acts as a richer authority surface that exposes the newer capture modules together and keeps `capture_from_args()` as the package-facing entry path.
```

### Change Item 3
- **Target location:** `webview_screenshort/__init__.py`, `webview_screenshort/cli/screenshot.py`, `webview_screenshort/references/live.py`
- **Change type:** replacement

**Before**
```text
Key consumers still imported from `capture_service.py` directly.
```

**After**
```text
Key consumers now import through `capture.service`, while `capture_service.py` remains as a compatibility facade.
```

---

## 4) Verification

- [x] `python3 -m py_compile webview_screenshort/capture/models.py webview_screenshort/capture/engines.py webview_screenshort/capture/reporting.py webview_screenshort/capture/runtime.py webview_screenshort/capture/service.py webview_screenshort/__init__.py webview_screenshort/cli/screenshot.py webview_screenshort/references/live.py screenshot.py reference_live_bundle.py reference_live_gate.py` succeeds
- [x] `python3 screenshot.py https://example.com --mode viewport --witness-mode frontend-default --output-format json` succeeds
- [x] `python3 reference_live_bundle.py --bundle /tmp/webview_wrapper_bundle.json --url https://example.com ... --output-format json` succeeds

---

## 5) Rollback Approach

If the authority-surface promotion proves unstable, keep the new capture modules but temporarily re-point the affected consumers back to `capture_service.py`. Do not delete the new modules as a first rollback step; the safer rollback is import redirection while preserving the new package structure.
