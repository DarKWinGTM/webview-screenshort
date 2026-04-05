# Phase 016 - Semantic gate rules

> **Summary File:** [SUMMARY.md](SUMMARY.md)
> **Phase ID:** 016
> **Status:** Implemented - Pending Review
> **Design References:** [../design/design.md](../design/design.md)
> **Patch References:** [../patch/phase-016-semantic-gate-rules.patch.md](../patch/phase-016-semantic-gate-rules.patch.md)

---

## Objective

Add semantic-aware gate policy keys so policy evaluation can explicitly fail on semantic drift instead of only carrying semantic summary context forward.

## Why this phase exists

The previous semantic-aware QA wave preserved semantic companion classifications in compare/verdict/gate output, but policy decisions still did not act on them. This phase makes semantic drift policy-visible by adding optional semantic-aware rule keys and wiring them into gate evaluation and built-in presets.

## Action points / execution checklist

- [x] add semantic-aware gate policy keys to the gate default policy model
- [x] make device-level gate evaluation fail on configured semantic conditions
- [x] extend built-in policy presets with semantic-aware rule keys where appropriate
- [x] verify policy preset discovery and gate output still behave correctly with the new semantic keys
- [x] sync docs/version metadata for the semantic gate rule wave

## Verification

- `python3 -m py_compile webview_screenshort/qa/gate.py webview_screenshort/qa/policies.py` succeeds
- `python3 list_policy_presets.py --output-format json` now exposes semantic-aware gate keys in the relevant built-in presets
- `python3 qa_gate.py /tmp/webview_semantic_qa_session.json --policy-preset strict/responsive-zero-diff --output-format json` returns gate output that includes the semantic-aware policy keys
- the checked example still fails for its real required-device reason rather than due to an implementation error

## Exit criteria

- semantic companion output is no longer only summary context; gate policy can explicitly fail on semantic drift when configured
- built-in policy presets can express semantic-aware QA intent instead of only visual diff thresholds
