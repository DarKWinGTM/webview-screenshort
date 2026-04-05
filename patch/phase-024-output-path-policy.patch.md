# Phase 024 Output Path Policy Patch

## 0) Document Control

> **Current Version:** 1.0
> **Status:** Implemented - Pending Review
> **Target Design:** [../design/design.md](../design/design.md) v2.39.0
> **Target Phase:** [../phase/phase-024-output-path-policy.md](../phase/phase-024-output-path-policy.md)
> **Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e
> **Full history:** [../changelog/changelog.md](../changelog/changelog.md)

---

## 1) Context

This patch captures the planned output-path policy wave: replacing package/plugin-cache default output with a workspace-friendly default chain that works better with downstream MCP/image-analysis constraints.

## 2) Analysis

Risk level: Medium

The change touches an operational default rather than a pure additive feature, so the safest path is to preserve all explicit caller overrides first and only change the no-override default behavior. The main goal is interoperability: installed-plugin paths should not quietly push artifacts into plugin cache when downstream tools need workspace-local files.

---

## 3) Change Items

### Change Item 1
- **Target location:** `webview_screenshort/capture/paths.py`, related config/runtime callers
- **Change type:** replacement

**Before**
```text
If the caller does not provide an explicit path and no env override is set, output defaults to the package-side `screenshot/` directory.
```

**After**
```text
If the caller does not provide an explicit path and no env override is set, output should default to a workspace-local temp/artifact directory, with OS tmp only as fallback.
```

### Change Item 2
- **Target location:** README/design/TODO/changelog governance wording
- **Change type:** replacement

**Before**
```text
The docs explain the current output artifacts, but the safer planned default-path policy is not yet visible as a governed next wave.
```

**After**
```text
The docs record the planned output-path policy so the next implementation wave has explicit authority and rationale.
```

---

## 4) Verification target

- [ ] explicit caller paths still win
- [ ] env override still wins next
- [ ] workspace-local temp/artifact dir becomes the default no-override base path
- [ ] OS tmp is used only as fallback
- [ ] downstream workspace-only MCP/image-analysis flows can consume default artifacts more reliably

---

## 5) Rollback Approach

If the policy implementation proves disruptive, keep explicit/env override behavior intact and temporarily restore the previous default while a narrower workspace-detection strategy is introduced. Do not remove the new policy authority without replacing it with an equally clear output contract.
