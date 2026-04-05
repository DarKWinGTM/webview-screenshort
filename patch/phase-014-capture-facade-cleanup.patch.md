# Phase 014 Capture Facade Cleanup Patch

## 0) Document Control

> **Current Version:** 1.0
> **Status:** Implemented - Pending Review
> **Target Design:** [../design/design.md](../design/design.md) v2.29.0
> **Target Phase:** [../phase/phase-014-capture-facade-cleanup.md](../phase/phase-014-capture-facade-cleanup.md)
> **Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e
> **Full history:** [../changelog/changelog.md](../changelog/changelog.md)

---

## 1) Context

This patch captures the final cleanup slice in the current capture refactor stretch: removing the remaining duplicate authority from `capture_service.py` by turning it into an explicit compatibility facade.

## 2) Analysis

Risk level: Low to Medium

By this point the newer `capture.service` surface was already in use by key consumers, so keeping the old implementation duplicated in `capture_service.py` mainly increased maintenance risk and authority ambiguity. The safer consolidation move is to keep the old file name but make it a pure re-export facade.

---

## 3) Change Items

### Change Item 1
- **Target location:** `webview_screenshort/capture_service.py`
- **Change type:** replacement

**Before**
```text
`capture_service.py` still contained substantial capture implementation alongside the newer `capture.service` authority surface.
```

**After**
```text
`capture_service.py` now acts as a compatibility facade that re-exports the capture authority surface instead of duplicating the implementation.
```

### Change Item 2
- **Target location:** key capture consumers
- **Change type:** replacement

**Before**
```text
The newer authority surface existed, but the old file still looked like a second implementation authority.
```

**After**
```text
The newer `capture.service` surface is now the practical active authority, while the old path remains only for compatibility.
```

---

## 4) Verification

- [x] `python3 -m py_compile webview_screenshort/capture_service.py webview_screenshort/capture/service.py webview_screenshort/__init__.py webview_screenshort/cli/screenshot.py webview_screenshort/references/live.py screenshot.py reference_live_bundle.py reference_live_gate.py` succeeds
- [x] `python3 screenshot.py https://example.com --mode viewport --witness-mode frontend-default --output-format json` succeeds
- [x] `python3 reference_live_bundle.py --bundle /tmp/webview_wrapper_bundle.json --url https://example.com ... --output-format json` succeeds
- [x] `claude plugins validate /home/node/workplace/AWCLOUD/TEMPLATE/PLUGIN/webview-screenshort` succeeds

---

## 5) Rollback Approach

If this final facade cleanup causes compatibility trouble, the rollback should restore selected imports or targeted compatibility exports, not restore a second full implementation inside `capture_service.py`. The main goal is to preserve one active authority surface.
