# Phase 015 Semantic-Aware QA Patch

## 0) Document Control

> **Current Version:** 1.0
> **Status:** Implemented - Pending Review
> **Target Design:** [../design/design.md](../design/design.md) v2.30.0
> **Target Phase:** [../phase/phase-015-semantic-aware-qa.md](../phase/phase-015-semantic-aware-qa.md)
> **Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e
> **Full history:** [../changelog/changelog.md](../changelog/changelog.md)

---

## 1) Context

This patch captures the next bounded product-value wave after the package cleanup stretch: making semantic page witness output visible inside downstream QA artifacts instead of leaving it as a standalone sidecar only.

## 2) Analysis

Risk level: Medium

The package should keep screenshot diff as the primary QA signal. The semantic layer in this wave is companion evidence only. The safest implementation is therefore to preserve semantic structure drift as additional machine-readable context rather than letting it directly replace or override visual diff policy behavior.

---

## 3) Change Items

### Change Item 1
- **Target location:** `webview_screenshort/compare/semantic.py` and `compare/reports.py`
- **Change type:** additive

**Before**
```text
Semantic page witness JSON existed, but compare output did not summarize semantic drift between the two sides.
```

**After**
```text
Compare output now carries pair-level semantic companion classifications and grouped semantic classification summary output.
```

### Change Item 2
- **Target location:** `webview_screenshort/qa/verdicts.py` and `qa/gate.py`
- **Change type:** replacement

**Before**
```text
Verdict and gate output preserved only visual mismatch classification summaries.
```

**After**
```text
Verdict and gate output now also preserve semantic companion classification summaries alongside the visual mismatch summary.
```

---

## 4) Verification

- [x] `python3 -m py_compile webview_screenshort/compare/semantic.py webview_screenshort/compare/reports.py webview_screenshort/qa/verdicts.py webview_screenshort/qa/gate.py` succeeds
- [x] `python3 compare_reports.py /tmp/webview_semantic_focus_report.json /tmp/webview_semantic_focus_report.json --output-format json` emits `semantic_classification_summary`
- [x] `python3 qa_verdict.py /tmp/webview_semantic_qa_session.json --output-format json` emits `semantic_mismatch_classification_summary`
- [x] `python3 qa_gate.py /tmp/webview_semantic_qa_session.json --policy-preset strict/responsive-zero-diff --output-format json` preserves semantic companion summary in gate output

---

## 5) Rollback Approach

If semantic-aware QA output proves noisy, keep semantic witness generation intact but remove only the downstream semantic companion classification layer. Do not roll back by claiming the semantic witness feature itself was invalid; the rollback surface is the compare/verdict/gate companion integration only.
