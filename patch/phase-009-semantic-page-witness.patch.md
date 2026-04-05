# Phase 009 Semantic Page Witness Patch

## 0) Document Control

> **Current Version:** 1.0
> **Status:** Implemented - Pending Review
> **Target Design:** [../design/design.md](../design/design.md) v2.24.0
> **Target Phase:** [../phase/phase-009-semantic-page-witness.md](../phase/phase-009-semantic-page-witness.md)
> **Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e
> **Full history:** [../changelog/changelog.md](../changelog/changelog.md)

---

## 1) Context

This patch captures the next bounded frontend-vision wave: turning rendered HTML into a reusable semantic page witness so frontend review can understand page structure faster than rereading full raw HTML.

## 2) Analysis

Risk level: Medium

The package already emits richer witness artifacts, but structure understanding still depended too heavily on raw HTML or screenshots alone. The change should stay bounded to checked rendered HTML truth and avoid claiming deeper DOM semantics, OCR, or visual salience analysis that the runtime does not actually compute.

---

## 3) Change Items

### Change Item 1
- **Target location:** `webview_screenshort/capture_service.py`
- **Change type:** additive

**Before**
```text
Richer capture could emit screenshot, rendered HTML, rendered text, metadata, and acquisition witnesses, but there was no compact machine-readable page-structure summary.
```

**After**
```text
Richer capture now derives semantic page witness JSON from rendered HTML and exposes title, headings, links, buttons, forms, and page-shape markers in a reusable summary artifact.
```

### Change Item 2
- **Target location:** evidence bundle output, responsive capture-set output, and `create_reference_bundle.py`
- **Change type:** replacement

**Before**
```text
Bundle and replay flows preserved screenshot/HTML/text witness paths, but semantic page witness continuity was not part of the artifact chain.
```

**After**
```text
Bundle and replay flows now preserve semantic page witness paths/summaries, and reference-bundle creation copies semantic witness artifacts when they exist in the source report.
```

### Change Item 3
- **Target location:** README, design, skill surfaces, phase summary, TODO, and changelog
- **Change type:** replacement

**Before**
```text
Docs described richer witness modes around screenshot, rendered HTML/text, metadata, and acquisition truth only.
```

**After**
```text
Docs now describe semantic page witness as a first-class lightweight structure-summary witness while keeping its scope bounded to rendered-HTML-derived truth.
```

---

## 4) Verification

- [x] `python3 -m py_compile webview_screenshort/capture_service.py create_reference_bundle.py screenshot.py` succeeds
- [x] `python3 screenshot.py https://example.com --mode viewport --witness-mode frontend-default --output-format json` succeeds
- [x] the returned capture includes `semantic_page_path`
- [x] the returned capture includes a non-empty `semantic_page_summary`
- [x] the emitted evidence bundle now includes semantic witness references

---

## 5) Rollback Approach

If semantic page witness output proves noisy, keep screenshot/rendered HTML/rendered text capture intact and remove only the semantic summary layer. Do not blur rollback into a claim that the package ever shipped deeper DOM-semantic or visual-semantic understanding; this phase is intentionally limited to lightweight rendered-HTML-derived structure summaries.
