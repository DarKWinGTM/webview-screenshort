# Phase 020 Darkwingtm Runtime Authority Wording Patch

## 0) Document Control

> **Current Version:** 1.0
> **Status:** Implemented - Pending Review
> **Target Design:** [../design/design.md](../design/design.md) v2.35.0
> **Target Phase:** [../phase/phase-020-darkwingtm-runtime-authority-wording.md](../phase/phase-020-darkwingtm-runtime-authority-wording.md)
> **Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e
> **Full history:** [../changelog/changelog.md](../changelog/changelog.md)

---

## 1) Context

This patch captures the wording correction needed after the runtime authority mismatch became visible in practice. The repo had drifted toward teaching the repo-local marketplace label as if it were the preferred installed identity for this environment.

## 2) Analysis

Risk level: Low

This is a wording and contract-clarity patch. The underlying plugin package remains the same; the change is to stop misleading operators about which marketplace label should be used for the maintained local runtime lifecycle in this environment.

---

## 3) Change Items

### Change Item 1
- **Target location:** `README.md`, `design/design.md`, `phase/phase-003-install-and-lifecycle-validation.md`, `phase/SUMMARY.md`
- **Change type:** replacement

**Before**
```text
Standalone repo-local marketplace usage was described too close to the default installed runtime lifecycle, and `@darkwingtm` read like compatibility-only residue.
```

**After**
```text
Standalone repo-local marketplace usage is described as source-side validation/cutover support, while the maintained local runtime authority label for this environment is explicitly `webview-screenshort@darkwingtm`.
```

### Change Item 2
- **Target location:** `TODO.md`, `changelog/changelog.md`, package metadata
- **Change type:** replacement

**Before**
```text
The runtime-authority wording correction was not yet recorded as its own governed cleanup slice.
```

**After**
```text
The runtime-authority wording correction is recorded as the 2.35.0 governed cleanup slice.
```

---

## 4) Verification

- [x] checked README/design/phase/TODO/changelog wording in the current authority scope
- [x] checked local installed runtime state currently uses `webview-screenshort@darkwingtm`
- [x] `claude plugins validate /home/node/workplace/AWCLOUD/TEMPLATE/PLUGIN/webview-screenshort` succeeds

---

## 5) Rollback Approach

If the wording split proves confusing, roll back only the wording edits and keep the underlying runtime install state unchanged. Do not reintroduce a docs posture that blurs code/release authority with installed runtime authority again.
