# Phase 021 Prototype Retirement Patch

## 0) Document Control

> **Current Version:** 1.0
> **Status:** Implemented - Pending Review
> **Target Design:** [../design/design.md](../design/design.md) v2.36.0
> **Target Phase:** [../phase/phase-021-prototype-retirement.md](../phase/phase-021-prototype-retirement.md)
> **Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e
> **Full history:** [../changelog/changelog.md](../changelog/changelog.md)

---

## 1) Context

This patch captures the final strategic cleanup wave after the active command surface had already moved to package CLI modules: removing the retained `prototype/` wrapper area so the repo no longer carries a prototype execution layer at all.

## 2) Analysis

Risk level: Low to Medium

The main risk is hidden dependency on the retained wrapper files. The checked scope already showed active skills/agents using package CLI modules directly and no active Python imports from `prototype`, so the safer strategic move is to remove the leftover wrapper storage and then normalize docs to stop describing it as part of the package story.

---

## 3) Change Items

### Change Item 1
- **Target location:** `prototype/`
- **Change type:** deletion

**Before**
```text
The repo still retained `prototype/root-wrappers/` and `prototype/policy_presets.py` as historical compatibility/reference artifacts.
```

**After**
```text
The retained `prototype/` wrapper area is removed entirely.
```

### Change Item 2
- **Target location:** `README.md`, `design/design.md`, `phase/SUMMARY.md`, `TODO.md`, `changelog/changelog.md`
- **Change type:** replacement

**Before**
```text
Active-state docs still described `prototype/root-wrappers/` as the retirement/reference location for old wrappers.
```

**After**
```text
Active-state docs now describe the package as a direct strategic structure with package CLI modules as the active command surface and no retained prototype wrapper layer.
```

---

## 4) Verification

- [x] checked active skills/agents still route through `webview_screenshort.cli.*`
- [x] checked Python grep scope does not show active imports from `prototype`
- [x] `claude plugins validate /home/node/workplace/AWCLOUD/TEMPLATE/PLUGIN/webview-screenshort` succeeds
- [x] checked the `prototype/` directory is removed from the repo working tree

---

## 5) Rollback Approach

If hidden dependency on the removed prototype files appears, restore only the specific missing artifact long enough to migrate that dependency properly. Do not restore the whole prototype retirement area by default; the strategic target is one direct package structure with no retained wrapper layer.
