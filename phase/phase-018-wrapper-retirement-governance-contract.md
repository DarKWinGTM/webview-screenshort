# Phase 018 - Wrapper-retirement governance contract

> **Summary File:** [SUMMARY.md](SUMMARY.md)
> **Phase ID:** 018
> **Status:** Implemented - Pending Review
> **Design References:** [../design/design.md](../design/design.md)
> **Patch References:** [../patch/phase-018-wrapper-retirement-governance-contract.patch.md](../patch/phase-018-wrapper-retirement-governance-contract.patch.md)

---

## Objective

Normalize the active command and governance contract after root-wrapper retirement so current docs consistently describe package CLI module execution, retired-wrapper placement, and the active capture authority surface.

## Why this phase exists

The cleanup had already moved the old root wrappers out of the active root structure, and skills/agents were already invoking package CLI modules directly. The remaining drift was documentary: some current-state docs still sounded transitional, still described wrapper retirement as pending, or still framed `capture.service` as merely the newer authority instead of the active one. This phase closes that last cleanup gap so the governance layer matches the real package state.

## Action points / execution checklist

- [x] bump design/phase/changelog/plugin metadata to the wrapper-retirement governance-sync version
- [x] normalize README wording around active package CLI modules and retired-wrapper placement
- [x] normalize design wording around active command contract, active capture authority, and retired-wrapper location
- [x] update TODO and phase summary so the cleanup appears as completed current-state contract, not a pending transition
- [x] add a dedicated changelog entry for the governance-contract normalization wave
- [x] verify the checked governance scope no longer carries the wrapper-retirement wording drift

## Verification

- checked `README.md`, `design/design.md`, `TODO.md`, `phase/SUMMARY.md`, and `changelog/changelog.md` and normalized the active-state wording in that scope
- `claude plugins validate /home/node/workplace/AWCLOUD/TEMPLATE/PLUGIN/webview-screenshort` succeeds
- checked current docs now align on `PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" python3 -m webview_screenshort.cli.<tool>` as the active programmable contract
- checked current docs now align on retired root wrappers living under `prototype/root-wrappers/` for compatibility reference only

## Exit criteria

- current-state docs describe one active programmable command surface
- current-state docs describe `capture.service` as the active capture authority surface
- retired wrapper placement is documented as completed cleanup, not as future work
- package governance reads as post-cleanup reality instead of mid-migration wording
