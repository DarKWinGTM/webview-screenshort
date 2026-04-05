# Phase 018 Wrapper-Retirement Governance Contract Patch

## 0) Document Control

> **Current Version:** 1.0
> **Status:** Implemented - Pending Review
> **Target Design:** [../design/design.md](../design/design.md) v2.33.0
> **Target Phase:** [../phase/phase-018-wrapper-retirement-governance-contract.md](../phase/phase-018-wrapper-retirement-governance-contract.md)
> **Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e
> **Full history:** [../changelog/changelog.md](../changelog/changelog.md)

---

## 1) Context

This patch captures the final documentation/governance cleanup after the root-wrapper retirement wave. The code cleanup was already done, but the authority docs still needed to stop sounding transitional.

## 2) Analysis

Risk level: Low

This is a governance-normalization patch, not a behavior-change patch. The main risk is wording drift: if current-state docs keep transitional phrasing after cleanup is already complete, later readers can mistake compatibility-reference artifacts for active structure. The safe fix is to normalize the active contract explicitly and keep the historical wrapper-retirement entry as history only.

---

## 3) Change Items

### Change Item 1
- **Target location:** `README.md`, `design/design.md`, `phase/SUMMARY.md`, `TODO.md`, `changelog/changelog.md`
- **Change type:** replacement

**Before**
```text
Current-state docs still mixed completed cleanup with transitional wording, such as root-wrapper retirement still sounding pending or `capture.service` still sounding only newer instead of active.
```

**After**
```text
Current-state docs now describe package CLI modules as the active programmable command surface, `capture.service` as the active authority surface, and `prototype/root-wrappers/` as the completed retirement location for old wrappers.
```

### Change Item 2
- **Target location:** `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `design/design.md`, `phase/SUMMARY.md`, `changelog/changelog.md`
- **Change type:** replacement

**Before**
```text
Governance and package metadata still reflected version 2.32.0, which ended before the wrapper-retirement doc normalization wave was recorded as its own completed slice.
```

**After**
```text
Governance and package metadata now reflect version 2.33.0 for the wrapper-retirement governance-contract normalization wave.
```

---

## 4) Verification

- [x] checked `README.md`, `design/design.md`, `TODO.md`, `phase/SUMMARY.md`, and `changelog/changelog.md` in the normalized governance scope
- [x] `claude plugins validate /home/node/workplace/AWCLOUD/TEMPLATE/PLUGIN/webview-screenshort` succeeds
- [x] checked active-state docs now align on package CLI module execution and retired-wrapper placement

---

## 5) Rollback Approach

If the wording normalization proves too aggressive, roll back only the affected governance phrasing while keeping the physical wrapper retirement and package CLI execution contract intact. Do not roll back by restoring the retired wrappers into the active root structure.
