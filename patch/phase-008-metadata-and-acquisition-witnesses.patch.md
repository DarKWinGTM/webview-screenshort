# Phase 008 Metadata and Acquisition Witnesses Patch

## 0) Document Control

> **Current Version:** 1.0
> **Status:** Implemented - Pending Review
> **Target Design:** [../design/design.md](../design/design.md) v2.23.0
> **Target Phase:** [../phase/phase-008-metadata-and-acquisition-witnesses.md](../phase/phase-008-metadata-and-acquisition-witnesses.md)
> **Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e
> **Full history:** [../changelog/changelog.md](../changelog/changelog.md)

---

## 1) Context

This patch captures the next bounded frontend-vision wave: preserving machine-readable acquisition truth and provider-returned metadata alongside screenshot and HTML witnesses.

## 2) Analysis

Risk level: Medium

The package already emits richer witness artifacts, but it still under-explained how those artifacts were acquired. Users need a clearer machine-readable witness for scrape/prerender success state and provider-returned metadata without pretending the system has full browser console or network tracing.

---

## 3) Change Items

### Change Item 1
- **Target location:** `webview_screenshort/headless_render_api.py` and `webview_screenshort/capture_service.py`
- **Change type:** additive

**Before**
```text
Capture flows extracted rendered HTML/text but dropped most acquisition details except warnings and final success/failure state.
```

**After**
```text
Capture flows now preserve acquisition summaries (status code, content type, JSON-payload presence, error state) for scrape/prerender witness calls.
```

### Change Item 2
- **Target location:** `CaptureResult`, evidence bundle payload, and text output surfaces
- **Change type:** replacement

**Before**
```text
Output surfaces focused on screenshot, rendered HTML, rendered text, and bundle/report paths only.
```

**After**
```text
Output surfaces now include metadata/acquisition witness paths and machine-readable acquisition summaries when available.
```

### Change Item 3
- **Target location:** governance/docs/version metadata
- **Change type:** replacement

**Before**
```text
The richer-witness model stopped at screenshot + HTML/text, leaving provider-returned metadata/acquisition truth under-documented.
```

**After**
```text
Docs, phase, patch, changelog, and package versions now describe the metadata/acquisition witness layer explicitly and keep its scope bounded to checked provider capabilities.
```

---

## 4) Verification

- [x] `python3 -m py_compile webview_screenshort/headless_render_api.py webview_screenshort/capture_service.py screenshot.py` succeeds
- [x] `python3 screenshot.py https://headless-render-api.com/docs --engine headless --mode viewport --witness-mode frontend-default --output-format json --report-file /tmp/webview_v223_report.json` succeeds
- [x] the returned capture includes `acquisition_path`
- [x] the returned capture includes `acquisition_summary.scrape`
- [x] plugin validation still succeeds after the witness-layer metadata additions

---

## 5) Rollback Approach

If acquisition/metadata witnesses prove noisy, keep the screenshot and HTML/text witness layer intact and drop only the extra metadata/acquisition artifact files. Do not blur this rollback into a claim that console/network witnesses were ever shipped; this phase is intentionally bounded to provider-returned metadata and acquisition truth only.
