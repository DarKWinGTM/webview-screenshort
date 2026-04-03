# Phase 005 Live Baseline Replay Patch

## 0) Document Control

> **Current Version:** 1.0
> **Status:** Implemented - Pending Review
> **Target Design:** [../design/design.md](../design/design.md) v2.14.0
> **Target Phase:** [../phase/phase-005-live-baseline-replay.md](../phase/phase-005-live-baseline-replay.md)
> **Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e
> **Full history:** [../changelog/changelog.md](../changelog/changelog.md)

---

## 1) Context

This patch captures the before/after surface for turning saved reference bundles into a practical live replay workflow against current frontend URLs.

## 2) Analysis

Risk level: Medium

The package already had reusable baseline artifacts, but it still left too much orchestration burden on the caller. A live replay layer should reuse the existing screenshot, compare, and compare-session helpers instead of inventing a second QA stack. At the same time, baseline metadata needs to be less implicit so bundle replay stays reliable even when sessions are revisited later.

---

## 3) Change Items

### Change Item 1
- **Target location:** `reference_live_bundle.py` plus `skills/reference-live-review/SKILL.md`
- **Change type:** additive

**Before**
```text
A saved reference bundle could only be replayed if the caller first captured the current report separately, then passed that current-report path into apply-reference manually.
```

**After**
```text
A higher-level helper plus a dedicated skill surface now let the caller start from a saved bundle and a live URL, capture the fresh current report automatically, and emit a new expected/actual compare session in one flow.
```

### Change Item 2
- **Target location:** reference bundle schema and listing/apply helpers
- **Change type:** replacement

**Before**
```text
Reference bundles relied mostly on the embedded compare-session shape and implicit left-side interpretation. Bundle listings exposed only limited metadata for baseline identity.
```

**After**
```text
Reference bundles now carry explicit `reference_side`, `reference_session_label`, `reference_report_path`, and `comparison_mode` metadata, while bundle listing and apply-reference logic preserve fallback behavior for older bundles.
```

### Change Item 3
- **Target location:** diff and agent workflow behavior
- **Change type:** replacement

**Before**
```text
Diff-pixel counting relied on alpha-channel differences only, and agent routing did not yet include saved-bundle + live-URL replay as a first-class path.
```

**After**
```text
Diff-pixel counting now measures non-zero RGBA differences directly, and the agent/runtime skill surfaces now route live baseline replay explicitly.
```

---

## 4) Verification

- [x] `python3 -m py_compile screenshot.py compare_reports.py compare_session.py create_reference_bundle.py apply_reference_bundle.py list_reference_bundles.py diff_images.py reference_live_bundle.py` succeeds
- [x] `python3 reference_live_bundle.py --bundle /tmp/webview_reference_bundles/nodeclaw-docs-reference-v2.json --url https://claw-frontend-dev.nodenetwork.ovh/docs --current-report /tmp/webview_live_current_report.json --comparison-json /tmp/webview_live_compare.json --session-output /tmp/webview_live_session.json --session-name nodeclaw-docs-live-baseline --current-label actual --capture-set responsive --mode viewport --wait --diff-dir /tmp/webview_live_diff_outputs` succeeds
- [x] `python3 apply_reference_bundle.py --bundle /tmp/webview_reference_bundles/nodeclaw-docs-reference-v2.json --current-report /tmp/webview_24_responsive_report.json --comparison-json /tmp/webview_apply_v2_compare.json --session-output /tmp/webview_apply_v2_session.json --session-name nodeclaw-docs-reference-v2-apply --current-label actual --diff-dir /tmp/webview_apply_v2_diffs` succeeds
- [x] `python3 list_reference_bundles.py /tmp/webview_reference_bundles --output-format json` now shows explicit reference metadata for new bundles and fallback values for old bundles

---

## 5) Rollback Approach

If the live replay surface proves confusing or too heavy, keep the existing lower-level apply-reference workflow as the stable baseline, remove or narrow the new live helper/skill layer, and preserve the explicit bundle metadata hardening because it improves replay clarity even without the higher-level orchestration surface.
