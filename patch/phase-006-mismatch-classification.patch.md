# Phase 006 Mismatch Classification Patch

## 0) Document Control

> **Current Version:** 1.0
> **Status:** Implemented - Pending Review
> **Target Design:** [../design/design.md](../design/design.md) v2.21.0
> **Target Phase:** [../phase/phase-006-mismatch-classification.md](../phase/phase-006-mismatch-classification.md)
> **Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e
> **Full history:** [../changelog/changelog.md](../changelog/changelog.md)

---

## 1) Context

This patch captures the before/after surface for making screenshot QA artifacts explain why mismatches happened, not only whether they happened.

## 2) Analysis

Risk level: Medium

The package already had strong artifact reuse, but compare, verdict, and gate outputs still collapsed too much meaning into pass/fail/invalid. That left automation and operators with extra interpretation work. At the same time, diff detection still had a blind spot for RGB-only changes because the older RGBA bbox path could miss visible color drift when alpha remained zero.

---

## 3) Change Items

### Change Item 1
- **Target location:** `compare_reports.py`
- **Change type:** replacement

**Before**
```text
The compare helper emitted pair metadata plus diff metrics, but it did not classify the reason for each mismatch beyond raw numeric diff values.
```

**After**
```text
The compare helper now emits per-pair `classification` and `classification_reason` fields plus a grouped `classification_summary` so downstream flows can distinguish exact matches, visible-region changes, dimension shifts, size mismatches, and diff errors.
```

### Change Item 2
- **Target location:** `qa_verdict.py` and `qa_gate.py`
- **Change type:** replacement

**Before**
```text
Verdict and gate outputs reported pass/fail/invalid state and policy violations, but they did not preserve grouped mismatch classes for later QA reasoning.
```

**After**
```text
Verdict and gate outputs now carry per-device classification values and grouped mismatch classification summaries so reusable QA artifacts explain why failures happened.
```

### Change Item 3
- **Target location:** `diff_images.py`
- **Change type:** replacement

**Before**
```text
RGB-only visual changes could still be missed because diff detection relied on RGBA bbox truthiness in a way Pillow could report as empty when alpha stayed zero.
```

**After**
```text
Diff detection now builds a visible difference mask from RGB plus alpha channels, counts changed pixels from that mask, and saves a classification-friendly diff image so RGB-only changes are detected reliably.
```

---

## 4) Verification

- [x] `python3 -m py_compile diff_images.py compare_reports.py qa_verdict.py qa_gate.py` succeeds
- [x] `python3 compare_reports.py /tmp/webview_24_responsive_report.json /tmp/webview_gate_preset_current_report.json --output-format json --diff-dir /tmp/webview_mismatch_diffs` succeeds and emits `classification_summary`
- [x] `python3 qa_verdict.py /tmp/webview_gate_preset_session.json --output-format json` succeeds and now emits classification-aware pass output
- [x] `python3 compare_reports.py /tmp/webview_24_single_report.json /tmp/webview_gate_preset_current_report_mobile.json --output-format json --diff-dir /tmp/webview_mismatch_mobile_diffs` succeeds and emits `visual_change_region`
- [x] `python3 qa_verdict.py /tmp/webview_mismatch_mobile_compare.json --output-format json` succeeds and emits `mismatch_classification_summary`
- [x] `python3 qa_gate.py /tmp/webview_mismatch_mobile_compare.json --policy-preset strict/responsive-zero-diff --output-format json` fails as expected with classification-aware gate output
- [x] `python3 qa_verdict.py /tmp/webview_empty_compare.json --output-format json` fails as expected with `overall_verdict = invalid` when comparison input contains no comparable pairs

---

## 5) Rollback Approach

If the classification model proves too noisy, keep the compare/verdict/gate artifact layering but narrow the classification vocabulary instead of removing the entire structured-mismatch path. The diff-detection fix should remain even if classification labels are later simplified, because it closes a real evidence bug rather than only adding surface detail.
