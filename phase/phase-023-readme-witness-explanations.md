# Phase 023 - README witness explanations

> **Summary File:** [SUMMARY.md](SUMMARY.md)
> **Phase ID:** 023
> **Status:** Implemented - Pending Review
> **Design References:** [../design/design.md](../design/design.md)
> **Patch References:** [../patch/phase-023-readme-witness-explanations.patch.md](../patch/phase-023-readme-witness-explanations.patch.md)

---

## Objective

Expand the README so the witness layers are explained in practical frontend-review terms instead of being listed only as artifact names.

## Why this phase exists

The README capability map already showed what surfaces existed, but users still needed a clearer explanation of what screenshot, rendered HTML, rendered text, semantic page witness JSON, and prerendered HTML actually mean in practice. This phase adds that explanatory layer so operators can choose the right witness mode with less guesswork.

## Action points / execution checklist

- [x] add a witness comparison table to README
- [x] add a direct CSR/rendered-HTML explanation block in README
- [x] sync package/governance metadata for the README witness-explanation wave
- [x] add dedicated phase/patch artifacts for this README-clarity slice

## Verification

- checked README now explains the witness layers in practical terms
- checked README now clarifies that rendered HTML witness is available without overstating the package into a full browser DevTools dump
- `claude plugins validate /home/node/workplace/AWCLOUD/TEMPLATE/PLUGIN/webview-screenshort` succeeds

## Exit criteria

- a user can read README and understand what each witness artifact actually means in practice
- the rendered-HTML capability is explained clearly without overclaiming browser-internal coverage
- README reads more like an operator guide than a raw artifact list
