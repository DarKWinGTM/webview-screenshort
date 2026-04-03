# Phase 004 Separate Repo Cutover Patch

## 0) Document Control

> **Current Version:** 1.0
> **Status:** Implemented - Pending Review
> **Target Design:** [../design/design.md](../design/design.md)
> **Target Phase:** [../phase/phase-004-separate-repo-cutover.md](../phase/phase-004-separate-repo-cutover.md)
> **Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e
> **Full history:** [../changelog/changelog.md](../changelog/changelog.md)

---

## 1) Context

This patch defines the before/after cutover surface for moving `webview-screenshort` from the shared local plugin workspace into its own standalone GitHub repo authority.

## 2) Analysis

Risk level: Medium

The package now has portable runtime invocation and structured output, but it still assumes the shared workspace marketplace for the current install story. Cutover must make the standalone repo the only long-term source of truth.

---

## 3) Change Items

### Change Item 1
- **Target location:** standalone repo-local marketplace support
- **Change type:** additive

**Before**
```text
The package only documents the shared local marketplace root under TEMPLATE/PLUGIN.
```

**After**
```text
The package includes its own `.claude-plugin/marketplace.json` so the repo can be used as its own local marketplace root after cutover.
```

### Change Item 2
- **Target location:** authority posture
- **Change type:** replacement

**Before**
```text
The shared TEMPLATE/PLUGIN workspace remains the active authority context for this package.
```

**After**
```text
The standalone GitHub repo becomes the source of truth, and the shared workspace copy is retired as long-term authority.
```

---

## 4) Verification

- [ ] standalone repo exists and is pushed
- [ ] repo-local marketplace manifest validates
- [ ] package install can target the standalone repo root
- [ ] shared-workspace authority is explicitly retired

---

## 5) Rollback Approach

If cutover fails, keep one clear authority baseline and revert to the shared workspace temporarily rather than letting both sides drift.
