# Phase 003 - Install and lifecycle validation

> **Summary File:** [SUMMARY.md](SUMMARY.md)
> **Phase ID:** 003
> **Status:** Implemented - Pending Review
> **Design References:** [../design/design.md](../design/design.md)
> **Patch References:** none

---

## Objective

Validate the package through the maintained installed plugin flow for this environment, while also confirming the standalone repo-local marketplace manifest still validates from the repo root.

## Checked current state

- plugin manifest validates
- marketplace manifest validates
- `webview-screenshort@darkwingtm` is the maintained local runtime authority label in this environment
- the standalone repo-local marketplace manifest still validates from the repo root when needed for package-side checks
- `claude agents` shows `webview-screenshort:webview-vision-assist`

## Action points / execution checklist
- [x] validate plugin manifest
- [x] add package to shared local marketplace if needed
- [x] install package from marketplace
- [x] confirm installed skill/package surfaces
- [x] confirm agent visibility
- [x] confirm reload/restart behavior for the current installed package path
