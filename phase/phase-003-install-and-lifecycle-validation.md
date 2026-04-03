# Phase 003 - Install and lifecycle validation

> **Summary File:** [SUMMARY.md](SUMMARY.md)
> **Phase ID:** 003
> **Status:** In Progress
> **Design References:** [../design/design.md](../design/design.md)
> **Patch References:** none

---

## Objective

Validate the package through the shared plugin install path and confirm runtime lifecycle behavior.

## Checked current state

- plugin manifest validates
- marketplace manifest validates
- `webview-screenshort@darkwingtm` installs in local scope
- `claude agents` shows `webview-screenshort:webview-vision-assist`

## Action points / execution checklist
- [x] validate plugin manifest
- [x] add package to shared local marketplace if needed
- [x] install package from marketplace
- [x] confirm installed skill/package surfaces
- [x] confirm agent visibility
- [x] confirm reload/restart behavior for the current installed package path
