# Phase 022 - README capability map

> **Summary File:** [SUMMARY.md](SUMMARY.md)
> **Phase ID:** 022
> **Status:** Implemented - Pending Review
> **Design References:** [../design/design.md](../design/design.md)
> **Patch References:** [../patch/phase-022-readme-capability-map.patch.md](../patch/phase-022-readme-capability-map.patch.md)

---

## Objective

Add a complete current capability map to README so the package surfaces and artifact outputs are visible in one place.

## Why this phase exists

The package had grown into a broader frontend evidence/review/QA toolkit, but the capability picture was still scattered across skill files, the design doc, and workflow-specific sections. That made it harder for an operator to understand the full current capability set quickly. This phase adds one README section that shows the active surfaces, major flows, and emitted artifact types clearly.

## Action points / execution checklist

- [x] add a compact README capability matrix for the main operational surfaces
- [x] add an output/artifact table for the current reusable artifacts
- [x] add a boundary block so users can quickly see what the package does not try to do
- [x] sync package/governance metadata for the README capability-documentation wave
- [x] add dedicated phase/patch artifacts for this documentation slice

## Verification

- checked the README now shows the active capability set in one section
- checked the capability section includes capture, review, compare, baseline, verdict, gate, preset, and session-replay surfaces
- `claude plugins validate /home/node/workplace/AWCLOUD/TEMPLATE/PLUGIN/webview-screenshort` succeeds

## Exit criteria

- a user can scan README and understand the current package capabilities without reading multiple scattered workflow docs first
- major surfaces and artifact outputs are visible in one place
- the README remains aligned with the active strategic package structure
