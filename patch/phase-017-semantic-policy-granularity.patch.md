# Phase 017 Semantic Policy Granularity Patch

## 0) Document Control

> **Current Version:** 1.0
> **Status:** Implemented - Pending Review
> **Target Design:** [../design/design.md](../design/design.md) v2.32.0
> **Target Phase:** [../phase/phase-017-semantic-policy-granularity.md](../phase/phase-017-semantic-policy-granularity.md)
> **Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e
> **Full history:** [../changelog/changelog.md](../changelog/changelog.md)

---

## 1) Context

This patch captures the next semantic QA refinement wave: moving from broad semantic gate classes toward more precise semantic gate rules that better match real frontend QA intent.

## 2) Analysis

Risk level: Medium

The semantic layer remains bounded and evidence-driven. The safest way to increase policy expressiveness is to re-use the already emitted `semantic_details` structure instead of inventing a new deeper semantic engine. That keeps the implementation grounded in existing checked evidence.

---

## 3) Change Items

### Change Item 1
- **Target location:** `webview_screenshort/qa/gate.py`
- **Change type:** replacement

**Before**
```text
Semantic-aware gate policy could only fail on broad classes such as semantic missing, semantic structure change, semantic content change, or any semantic change.
```

**After**
```text
Semantic-aware gate policy can now also fail on title change, missing headings, structure-flag change, missing links/buttons, form-count change, and missing inputs.
```

### Change Item 2
- **Target location:** relevant built-in presets under `support/policies/*.json`
- **Change type:** replacement

**Before**
```text
Built-in semantic-aware presets expressed only broad semantic gate classes.
```

**After**
```text
Built-in semantic-aware presets now express more specific frontend QA expectations where appropriate.
```

---

## 4) Verification

- [x] `python3 -m py_compile webview_screenshort/qa/gate.py` succeeds
- [x] `python3 list_policy_presets.py --output-format json` exposes the finer semantic rule keys in relevant built-in presets
- [x] `python3 qa_gate.py /tmp/webview_semantic_qa_session.json --policy-preset strict/responsive-zero-diff --output-format json` returns gate policy payload including the finer semantic rule keys
- [x] the checked example still fails for its real required-device reason instead of due to an implementation error

---

## 5) Rollback Approach

If the finer semantic granularity proves noisy, keep the broad semantic gate rules and remove only the newer fine-grained rule keys from policy evaluation and presets. The rollback surface is the granularity layer, not the whole semantic-aware QA stack.
