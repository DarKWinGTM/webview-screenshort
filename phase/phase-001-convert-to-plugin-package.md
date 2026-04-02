# Phase 001 - Convert to plugin package

> **Summary File:** [SUMMARY.md](SUMMARY.md)
> **Phase ID:** 001
> **Status:** Implemented - Pending Review
> **Design References:** [../design/design.md](../design/design.md)
> **Patch References:** [../patch/phase-001-convert-to-plugin-package.patch.md](../patch/phase-001-convert-to-plugin-package.patch.md)

---

## Objective

Convert the older project-local screenshot utility into a governed plugin package structure.

## Action points / execution checklist
- [x] create `.claude-plugin/`
- [x] create `skills/`, `agents/`, `design/`, `changelog/`, `phase/`, and `patch/`
- [x] move legacy design/changelog/skill files into plugin-standard locations
- [x] add plugin metadata
- [x] replace stale skill path

## Verification
- standard plugin directories now exist
- old project-local `.claude/skills` path is retired
- skill and agent surfaces exist inside the package
