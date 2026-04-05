# Phase 017 - Semantic policy granularity

> **Summary File:** [SUMMARY.md](SUMMARY.md)
> **Phase ID:** 017
> **Status:** Implemented - Pending Review
> **Design References:** [../design/design.md](../design/design.md)
> **Patch References:** [../patch/phase-017-semantic-policy-granularity.patch.md](../patch/phase-017-semantic-policy-granularity.patch.md)

---

## Objective

Add finer semantic gate rule granularity so semantic-aware policies can target title/headings/structure/link/button/form/input drift more precisely than the current class-level semantic change rules.

## Why this phase exists

The semantic-aware gate rule wave made semantic drift policy-visible, but the rules were still broad. This phase adds more specific semantic controls so the policy layer can express practical frontend QA intent more precisely, such as caring strongly about headings, structure flags, or form/input disappearance while staying tolerant of other content drift.

## Action points / execution checklist

- [x] extend gate policy defaults with finer semantic rule keys
- [x] map finer semantic rule keys onto `semantic_details` from compare output
- [x] extend relevant built-in presets with more precise semantic rule choices
- [x] verify preset discovery and gate output still expose the finer semantic keys correctly
- [x] sync docs/version metadata for the semantic policy granularity wave

## Verification

- `python3 -m py_compile webview_screenshort/qa/gate.py` succeeds
- `python3 list_policy_presets.py --output-format json` exposes the finer semantic rule keys in relevant built-in presets
- `python3 qa_gate.py /tmp/webview_semantic_qa_session.json --policy-preset strict/responsive-zero-diff --output-format json` returns gate policy payload including the finer semantic rule keys
- the checked example still fails for its real required-device reason instead of due to an implementation error

## Exit criteria

- semantic-aware gate policy can express more specific frontend QA intent than only broad semantic-change classes
- built-in presets can distinguish stricter and more tolerant semantic expectations more clearly
