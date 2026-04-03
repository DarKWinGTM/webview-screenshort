# Phase 004 - Separate repo cutover

> **Summary File:** [SUMMARY.md](SUMMARY.md)
> **Phase ID:** 004
> **Status:** Implemented - Pending Review
> **Design References:** [../design/design.md](../design/design.md)
> **Patch References:** [../patch/phase-004-separate-repo-cutover.patch.md](../patch/phase-004-separate-repo-cutover.patch.md)

---

## Objective

Finalize `webview-screenshort` as its own standalone GitHub repo authority without leaving duplicate public install posture behind in the shared workspace.

## Action points / execution checklist
- [x] validate `/reload-plugins` and restart visibility
- [x] validate one more CSR-heavy target
- [x] create/push `DarKWinGTM/webview-screenshort`
- [x] validate repo-root local marketplace install from `./`
- [ ] switch authority from shared workspace to standalone repo
- [ ] retire shared-workspace authority cleanly
