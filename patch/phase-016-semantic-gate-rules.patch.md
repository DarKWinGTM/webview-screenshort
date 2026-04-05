# Phase 016 Semantic Gate Rules Patch

## 0) Document Control

> **Current Version:** 1.0
> **Status:** Implemented - Pending Review
> **Target Design:** [../design/design.md](../design/design.md) v2.31.0
> **Target Phase:** [../phase/phase-016-semantic-gate-rules.md](../phase/phase-016-semantic-gate-rules.md)
> **Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e
> **Full history:** [../changelog/changelog.md](../changelog/changelog.md)

---

## 1) Context

This patch captures the next bounded product-value wave after semantic-aware QA summary propagation: letting semantic drift participate in gate policy evaluation directly.

## 2) Analysis

Risk level: Medium

Semantic witness remains a bounded companion signal, not a deep semantic engine. The safest policy step is to expose explicit optional rule keys such as fail-on-semantic-missing or fail-on-semantic-structure-change instead of replacing visual diff thresholds entirely.

---

## 3) Change Items

### Change Item 1
- **Target location:** `webview_screenshort/qa/gate.py`
- **Change type:** replacement

**Before**
```text
Gate policy evaluation knew only visual diff thresholds, invalid verdict rules, and required-device rules.
```

**After**
```text
Gate policy evaluation now also supports semantic-aware rule keys that can fail on semantic missing, semantic structure change, semantic content change, or any semantic change.
```

### Change Item 2
- **Target location:** `support/policies/*.json`
- **Change type:** replacement

**Before**
```text
Built-in policy presets expressed only visual diff and device requirements.
```

**After**
```text
Relevant built-in policy presets now also express semantic-aware gate intent where appropriate.
```

---

## 4) Verification

- [x] `python3 -m py_compile webview_screenshort/qa/gate.py webview_screenshort/qa/policies.py` succeeds
- [x] `python3 list_policy_presets.py --output-format json` exposes semantic-aware policy keys in relevant built-in presets
- [x] `python3 qa_gate.py /tmp/webview_semantic_qa_session.json --policy-preset strict/responsive-zero-diff --output-format json` returns gate output with semantic-aware policy keys present
- [x] the checked example still fails for its real required-device reason instead of due to an implementation error

---

## 5) Rollback Approach

If semantic-aware gate rules prove too strict or noisy, keep semantic-aware summaries in compare/verdict/gate output but remove or relax the semantic rule keys from policy evaluation. The rollback surface is the policy layer, not the semantic companion output layer itself.
