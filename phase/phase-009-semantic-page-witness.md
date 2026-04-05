# Phase 009 - Semantic page witness

> **Summary File:** [SUMMARY.md](SUMMARY.md)
> **Phase ID:** 009
> **Status:** Implemented - Pending Review
> **Design References:** [../design/design.md](../design/design.md)
> **Patch References:** [../patch/phase-009-semantic-page-witness.patch.md](../patch/phase-009-semantic-page-witness.patch.md)

---

## Objective

Add a first-class semantic page witness layer so rendered HTML can produce a reusable machine-readable page-structure summary for frontend review, responsive review, and baseline-replay workflows.

## Why this phase exists

The package already emits screenshots, rendered HTML, rendered text, acquisition summaries, and provider-returned metadata, but a reviewer still has to read full raw HTML to understand basic page shape. This phase adds a lighter structure-summary witness so frontend review can quickly see title, headings, links, buttons, forms, and major page-shape markers without pretending the runtime already has full browser-devtools semantics.

## Action points / execution checklist

- [x] add semantic page witness generation from rendered HTML
- [x] persist semantic witness JSON beside focused capture outputs
- [x] expose semantic witness path and summary in the capture result model
- [x] preserve semantic witness paths inside evidence bundle artifacts
- [x] preserve semantic/acquisition witness indexes for responsive capture-set output
- [x] make reference-bundle creation copy semantic witness artifacts when source reports contain them
- [x] update screenshot / frontend-review / responsive-review / agent wording so semantic page witness is treated as richer structure evidence
- [x] sync design, README, TODO, phase summary, patch, and changelog for the semantic witness wave

## Verification

- `python3 -m py_compile webview_screenshort/capture_service.py create_reference_bundle.py screenshot.py` succeeds
- `python3 screenshot.py https://example.com --mode viewport --witness-mode frontend-default --output-format json` succeeds
- the returned capture now includes `semantic_page_path`
- the returned capture now includes a non-empty `semantic_page_summary` for the checked page
- the emitted evidence bundle now carries `semantic_page_path` and `semantic_page_summary`
- responsive capture-set output now preserves capture-set semantic/acquisition witness index paths when richer witnesses are emitted

## Exit criteria

- semantic page witness becomes a first-class frontend evidence artifact instead of an implicit future idea
- focused capture output can point to machine-readable page-structure JSON when rendered HTML exists
- evidence bundles and responsive capture-set flows preserve semantic witness references instead of dropping structure understanding back to raw HTML only
- docs describe semantic witness honestly as lightweight rendered-HTML-derived structure truth rather than full DOM or visual-semantic analysis
