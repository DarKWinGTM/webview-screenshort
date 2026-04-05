# Phase 010 Package Reorganization Patch

## 0) Document Control

> **Current Version:** 1.0
> **Status:** Implemented - Pending Review
> **Target Design:** [../design/design.md](../design/design.md) v2.25.0
> **Target Phase:** [../phase/phase-010-package-reorganization.md](../phase/phase-010-package-reorganization.md)
> **Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e
> **Full history:** [../changelog/changelog.md](../changelog/changelog.md)

---

## 1) Context

This patch captures the next bounded structural wave: turning the repo from a root-script-heavy layout into a more professional package-oriented Python project while preserving the existing command surface.

## 2) Analysis

Risk level: Medium

The main risk is compatibility drift: root commands, import paths, and JSON/output behaviors are already part of the package contract. The refactor therefore must preserve the existing command names and keep compatibility surfaces in place while moving real implementation into internal package domains.

---

## 3) Change Items

### Change Item 1
- **Target location:** `webview_screenshort/compare/`, `webview_screenshort/qa/`, `webview_screenshort/references/`, `webview_screenshort/cli/`, `webview_screenshort/schemas.py`
- **Change type:** additive

**Before**
```text
Reusable comparison, QA, and reference logic mostly lived in root-level scripts, and shared schema strings were duplicated across several files.
```

**After**
```text
The codebase now has package-internal domains for compare, QA, references, CLI adapters, and shared schema constants.
```

### Change Item 2
- **Target location:** root Python command files such as `compare_reports.py`, `qa_verdict.py`, `qa_gate.py`, `create_reference_bundle.py`, `apply_reference_bundle.py`, `reference_live_bundle.py`, `reference_live_gate.py`, and listing commands
- **Change type:** replacement

**Before**
```text
Root Python commands mixed CLI argument handling with reusable implementation logic.
```

**After**
```text
Root Python commands now act as compatibility-thin wrappers that delegate parser/main behavior to package-internal CLI adapters.
```

### Change Item 3
- **Target location:** `webview_screenshort/workflows.py` and cross-flow coupling points
- **Change type:** replacement

**Before**
```text
The internal workflow module imported root scripts directly, and several flows used script-to-script subprocess chaining even though the logic was library-like.
```

**After**
```text
The internal workflow surface now depends on package domains, and direct subprocess coupling has been reduced where in-process module reuse now exists.
```

---

## 4) Verification

- [x] `python3 -m py_compile` succeeds across the root wrappers and new package modules
- [x] `python3 compare_reports.py /tmp/webview_semantic_focus_report.json /tmp/webview_semantic_focus_report.json --output-format json` succeeds
- [x] `python3 compare_session.py --name wrapper-check ...` succeeds
- [x] `python3 create_reference_bundle.py --name wrapper-check ...` succeeds
- [x] `python3 apply_reference_bundle.py --bundle /tmp/webview_wrapper_bundle.json ...` succeeds
- [x] `python3 qa_verdict.py /tmp/webview_wrapper_apply_session.json --output-format json` succeeds
- [x] listing wrappers now skip invalid/non-dict JSON artifacts robustly
- [x] `claude plugins validate /home/node/workplace/AWCLOUD/TEMPLATE/PLUGIN/webview-screenshort` succeeds

---

## 5) Rollback Approach

If the package-organization wave proves unstable, keep the new domain files as reference targets but restore the root command files to their previous mixed implementations. Do not roll back by deleting the new package structure blindly; the safer rollback is to preserve the new modules and re-point wrappers/imports incrementally if compatibility issues appear.
