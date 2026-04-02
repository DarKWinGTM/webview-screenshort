# Phase 001 Convert to Plugin Package Patch

## 0) Document Control

> **Current Version:** 1.0
> **Status:** Implemented - Pending Review
> **Target Design:** [../design/design.md](../design/design.md) v2.0.0
> **Target Phase:** [../phase/phase-001-convert-to-plugin-package.md](../phase/phase-001-convert-to-plugin-package.md)
> **Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e
> **Full history:** [../changelog/changelog.md](../changelog/changelog.md)

---

## 1) Context

This patch captures the conversion from the older project-local screenshot utility layout into a governed plugin package.

## 2) Analysis

Risk level: Medium

The old utility had working screenshot behavior, but its skill wiring used a stale absolute path and non-standard package layout. Converting to standard plugin layout reduces authority drift and makes future install validation possible.

---

## 3) Change Items

### Change Item 1
- **Target location:** package directory structure
- **Change type:** restructuring

**Before**
```text
webview-screenshort/
  .claude/skills/screenshot/SKILL.md
  design.md
  changelog.md
  screenshot.py
```

**After**
```text
webview-screenshort/
  .claude-plugin/plugin.json
  agents/webview-vision-assist.md
  skills/screenshot/SKILL.md
  skills/screenshot/overview.md
  skills/screenshot/frontend-review.md
  design/design.md
  changelog/changelog.md
  phase/
  patch/
  screenshot.py
```

### Change Item 2
- **Target location:** `skills/screenshot/SKILL.md`
- **Change type:** replacement

**Before**
```text
The skill file invoked a stale absolute path under /home/node/workplace/AWCLOUD/CLAUDE/claude-code-webview-screenshort/screenshot.py.
```

**After**
```text
The skill file now invokes the installed plugin-local script path through `${CLAUDE_PLUGIN_ROOT}/screenshot.py` instead of a stale source-workspace-only path.
```

---

## 4) Verification

- [x] plugin metadata exists
- [x] legacy design/changelog/skill files moved into governed locations
- [x] stale skill path removed
- [x] package now has standard plugin surfaces

---

## 5) Rollback Approach

If this direction proves wrong, keep one governed package and revert structure there rather than restoring a second non-governed project-local skill path.
