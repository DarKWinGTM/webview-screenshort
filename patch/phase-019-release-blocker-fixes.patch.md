# Phase 019 Release Blocker Fixes Patch

## 0) Document Control

> **Current Version:** 1.0
> **Status:** Implemented - Pending Review
> **Target Design:** [../design/design.md](../design/design.md) v2.34.0
> **Target Phase:** [../phase/phase-019-release-blocker-fixes.md](../phase/phase-019-release-blocker-fixes.md)
> **Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e
> **Full history:** [../changelog/changelog.md](../changelog/changelog.md)

---

## 1) Context

This patch captures the bounded blocker-fix wave that had to land before commit/push/release. The package structure was already in good shape, but the checked release surface still had one command-contract problem and one release-hygiene problem.

## 2) Analysis

Risk level: Low

These fixes are narrow and release-oriented. The skill fix preserves explicit operator intent instead of changing the underlying screenshot CLI contract, and the ignore fix reduces accidental release pollution from local timestamped evidence outputs. Both changes are safer than shipping the blockers forward.

---

## 3) Change Items

### Change Item 1
- **Target location:** `skills/frontend-review/SKILL.md`, `skills/responsive-review/SKILL.md`
- **Change type:** replacement

**Before**
```text
The higher-level review skills hard-appended default `--witness-mode` flags, so an explicit operator-provided witness-mode selection could be silently overridden.
```

**After**
```text
The higher-level review skills now add their default witness mode only when the operator did not already provide `--witness-mode`.
```

### Change Item 2
- **Target location:** `.gitignore`
- **Change type:** replacement

**Before**
```text
Only `screenshot/*.png` was ignored, so generated JSON/HTML/TXT evidence outputs under `screenshot/` could still pollute the release diff.
```

**After**
```text
Generated `screenshot/*.json`, `screenshot/*.html`, and `screenshot/*.txt` outputs are now ignored by default alongside PNG files.
```

### Change Item 3
- **Target location:** package/governance metadata (`.claude-plugin/*.json`, README/design/TODO/phase/changelog)
- **Change type:** replacement

**Before**
```text
The checked docs and package metadata ended at 2.33.0 before the blocker-fix wave was recorded.
```

**After**
```text
The checked docs and package metadata now reflect 2.34.0 for the release-blocker fix wave.
```

---

## 4) Verification

- [x] checked `skills/frontend-review/SKILL.md` and `skills/responsive-review/SKILL.md` for explicit witness-mode preservation
- [x] checked `.gitignore` for generated screenshot-side artifact coverage
- [x] `python3 -m py_compile /home/node/workplace/AWCLOUD/TEMPLATE/PLUGIN/webview-screenshort/webview_screenshort/cli/screenshot.py` succeeds
- [x] `claude plugins validate /home/node/workplace/AWCLOUD/TEMPLATE/PLUGIN/webview-screenshort` succeeds

---

## 5) Rollback Approach

If either blocker fix proves undesirable, roll back the specific skill-shell logic or ignore entries while keeping the broader package reorganization and wrapper-retirement cleanup intact. Do not undo the underlying package CLI contract just to reverse these narrow release-surface fixes.
