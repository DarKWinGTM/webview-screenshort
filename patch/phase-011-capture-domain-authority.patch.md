# Phase 011 Capture-Domain Authority Patch

## 0) Document Control

> **Current Version:** 1.0
> **Status:** Implemented - Pending Review
> **Target Design:** [../design/design.md](../design/design.md) v2.26.0
> **Target Phase:** [../phase/phase-011-capture-domain-authority.md](../phase/phase-011-capture-domain-authority.md)
> **Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e
> **Full history:** [../changelog/changelog.md](../changelog/changelog.md)

---

## 1) Context

This patch captures the next bounded cleanup slice after the package-reorganization wave: moving clear capture subdomains into `webview_screenshort/capture/` while preserving old import paths as compatibility shims.

## 2) Analysis

Risk level: Low to Medium

The logic moved in this slice is well-bounded and already had obvious domain ownership: auth/session parsing and headless-render-api integration. The main compatibility risk is import-path drift, so the old files should remain as explicit shims instead of being removed immediately.

---

## 3) Change Items

### Change Item 1
- **Target location:** `webview_screenshort/capture/auth.py` and `webview_screenshort/auth_context.py`
- **Change type:** replacement

**Before**
```text
Auth-context implementation authority lived in `webview_screenshort/auth_context.py`.
```

**After**
```text
Auth-context implementation authority now lives in `webview_screenshort/capture/auth.py`, while `webview_screenshort/auth_context.py` remains as a compatibility shim.
```

### Change Item 2
- **Target location:** `webview_screenshort/capture/headless_api.py` and `webview_screenshort/headless_render_api.py`
- **Change type:** replacement

**Before**
```text
Headless-render-api implementation authority lived in `webview_screenshort/headless_render_api.py`.
```

**After**
```text
Headless-render-api implementation authority now lives in `webview_screenshort/capture/headless_api.py`, while `webview_screenshort/headless_render_api.py` remains as a compatibility shim.
```

### Change Item 3
- **Target location:** `webview_screenshort/capture_service.py` and `webview_screenshort/__init__.py`
- **Change type:** replacement

**Before**
```text
The capture service and package exports still pointed at the older top-level package authority paths.
```

**After**
```text
The capture service and package exports now import from the newer capture-domain authority paths first.
```

---

## 4) Verification

- [x] `python3 -m py_compile webview_screenshort/capture/auth.py webview_screenshort/capture/headless_api.py webview_screenshort/auth_context.py webview_screenshort/headless_render_api.py webview_screenshort/capture_service.py webview_screenshort/__init__.py screenshot.py` succeeds
- [x] `python3 screenshot.py https://example.com --mode viewport --witness-mode frontend-default --output-format json` succeeds
- [x] the checked screenshot flow still emits richer witness artifacts after the authority shift

---

## 5) Rollback Approach

If the new capture authority split proves unstable, keep the new `capture/` files but re-point imports temporarily back through the older top-level package files. Do not delete the new capture-domain files as a first rollback step; the safer rollback is import redirection while preserving the new structure.
