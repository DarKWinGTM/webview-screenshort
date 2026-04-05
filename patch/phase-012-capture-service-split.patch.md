# Phase 012 Capture-Service Split Patch

## 0) Document Control

> **Current Version:** 1.0
> **Status:** Implemented - Pending Review
> **Target Design:** [../design/design.md](../design/design.md) v2.27.0
> **Target Phase:** [../phase/phase-012-capture-service-split.md](../phase/phase-012-capture-service-split.md)
> **Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e
> **Full history:** [../changelog/changelog.md](../changelog/changelog.md)

---

## 1) Context

This patch captures the next bounded cleanup slice after the capture-authority wave: thinning `capture_service.py` by moving obvious support responsibilities into dedicated capture modules.

## 2) Analysis

Risk level: Medium

`capture_service.py` still held too many unrelated concerns at once. The safest split is to extract the clearly separable responsibilities first — config loading, path generation, and witness derivation — while leaving engine/orchestration behavior behind the same facade until a later wave.

---

## 3) Change Items

### Change Item 1
- **Target location:** `webview_screenshort/capture/config.py`
- **Change type:** additive

**Before**
```text
Screenshot configuration defaults and env-loading logic lived inside `capture_service.py`.
```

**After**
```text
Screenshot config/env-loading logic now lives in a dedicated `capture/config.py` module.
```

### Change Item 2
- **Target location:** `webview_screenshort/capture/paths.py`
- **Change type:** additive

**Before**
```text
Output/report/bundle/path helpers and PNG validation helpers lived inside `capture_service.py`.
```

**After**
```text
Path/output helpers and PNG validation helpers now live in `capture/paths.py`.
```

### Change Item 3
- **Target location:** `webview_screenshort/capture/witnesses.py` and `capture_service.py`
- **Change type:** replacement

**Before**
```text
Witness-mode normalization, HTML/text conversion, semantic page summary logic, and richer witness collection all lived directly in `capture_service.py`.
```

**After**
```text
Witness normalization and richer witness extraction now live in `capture/witnesses.py`, while `capture_service.py` reuses them as a facade.
```

---

## 4) Verification

- [x] `python3 -m py_compile webview_screenshort/capture/config.py webview_screenshort/capture/paths.py webview_screenshort/capture/witnesses.py webview_screenshort/capture_service.py screenshot.py` succeeds
- [x] `python3 screenshot.py https://example.com --mode viewport --witness-mode frontend-default --output-format json` succeeds
- [x] `python3 screenshot.py https://example.com --capture-set responsive --mode viewport --witness-mode responsive --output-format json` succeeds
- [x] richer witness outputs are still emitted after the extraction

---

## 5) Rollback Approach

If the capture-service split proves unstable, keep the new `capture/config.py`, `capture/paths.py`, and `capture/witnesses.py` files but temporarily point `capture_service.py` back to local copies of the extracted logic. Do not delete the new modules as a first rollback step; the safer rollback is import redirection while preserving the new structure.
