# Phase 022 README Capability Map Patch

## 0) Document Control

> **Current Version:** 1.0
> **Status:** Implemented - Pending Review
> **Target Design:** [../design/design.md](../design/design.md) v2.37.0
> **Target Phase:** [../phase/phase-022-readme-capability-map.md](../phase/phase-022-readme-capability-map.md)
> **Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e
> **Full history:** [../changelog/changelog.md](../changelog/changelog.md)

---

## 1) Context

This patch captures the README capability-documentation wave: making the current package ability set visible in one place instead of leaving it spread across multiple skill and governance documents.

## 2) Analysis

Risk level: Low

This is a documentation-clarity patch. The main value is operator understanding: the package now has enough surfaces that a compact README capability map reduces search cost and helps new users see the whole active toolkit faster.

---

## 3) Change Items

### Change Item 1
- **Target location:** `README.md`
- **Change type:** replacement

**Before**
```text
README described many capabilities in prose, but the full active package surface and artifact set were still spread across multiple sections and workflow docs.
```

**After**
```text
README now includes a compact capability map plus output/artifact table covering the current package surface in one place.
```

### Change Item 2
- **Target location:** package/governance metadata and phase/changelog sync files
- **Change type:** replacement

**Before**
```text
The capability-documentation slice was not yet tracked as its own governed wave.
```

**After**
```text
The README capability-documentation slice is tracked as the 2.37.0 governed documentation wave.
```

---

## 4) Verification

- [x] checked README capability section now summarizes the active package surface in one place
- [x] checked the capability section includes both operational surfaces and artifact outputs
- [x] `claude plugins validate /home/node/workplace/AWCLOUD/TEMPLATE/PLUGIN/webview-screenshort` succeeds

---

## 5) Rollback Approach

If the README capability section proves too dense, reduce the table size while keeping one unified capability section. Do not revert to scattering the current capability set entirely across multiple workflow files again.
