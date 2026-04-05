# Phase 015 - Semantic-aware QA

> **Summary File:** [SUMMARY.md](SUMMARY.md)
> **Phase ID:** 015
> **Status:** Implemented - Pending Review
> **Design References:** [../design/design.md](../design/design.md)
> **Patch References:** [../patch/phase-015-semantic-aware-qa.patch.md](../patch/phase-015-semantic-aware-qa.patch.md)

---

## Objective

Add semantic companion classification summaries to compare, verdict, and gate artifacts so semantic page witness output becomes reusable downstream QA context rather than a standalone side artifact only.

## Why this phase exists

The package already emitted semantic page witness JSON, but downstream QA layers still judged pages almost entirely through screenshot-era visual diff logic. This phase keeps visual diff as the primary decision path while preserving semantic witness comparisons as machine-readable companion evidence for missing headings, links, buttons, forms, and page-structure drift.

## Action points / execution checklist

- [x] add semantic witness comparison helpers under `webview_screenshort/compare/`
- [x] extend compare pairs with semantic companion classification fields
- [x] add grouped semantic classification summary to comparison output
- [x] propagate semantic companion classifications into verdict output
- [x] propagate semantic companion classifications into gate output
- [x] verify semantic-aware compare/verdict/gate flow against checked artifacts
- [x] sync docs/version metadata for the semantic-aware QA wave

## Verification

- `python3 -m py_compile webview_screenshort/compare/semantic.py webview_screenshort/compare/reports.py webview_screenshort/qa/verdicts.py webview_screenshort/qa/gate.py` succeeds
- `python3 compare_reports.py /tmp/webview_semantic_focus_report.json /tmp/webview_semantic_focus_report.json --output-format json` emits `semantic_classification_summary`
- `python3 qa_verdict.py /tmp/webview_semantic_qa_session.json --output-format json` emits `semantic_mismatch_classification_summary`
- `python3 qa_gate.py /tmp/webview_semantic_qa_session.json --policy-preset strict/responsive-zero-diff --output-format json` preserves semantic companion summary in gate output

## Exit criteria

- semantic page witness is no longer only a side artifact; compare/verdict/gate can carry its summarized drift context downstream
- visual diff remains the primary QA signal, but semantic structure drift becomes reusable machine-readable companion evidence
