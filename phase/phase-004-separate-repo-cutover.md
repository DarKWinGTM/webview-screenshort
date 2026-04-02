# Phase 004 - Separate repo cutover

> **Summary File:** [SUMMARY.md](SUMMARY.md)
> **Phase ID:** 004
> **Status:** Pending
> **Design References:** [../design/design.md](../design/design.md)
> **Patch References:** none

---

## Objective

Prepare `webview-screenshort` to become its own standalone GitHub repo without leaving duplicate authority behind in the shared workspace.

## Action points / execution checklist
- [ ] validate `/reload-plugins` and restart visibility
- [ ] validate one more CSR-heavy target
- [ ] create/push `DarKWinGTM/webview-screenshort`
- [ ] switch authority from shared workspace to standalone repo
- [ ] retire shared-workspace authority cleanly
