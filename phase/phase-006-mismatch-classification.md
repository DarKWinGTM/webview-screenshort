# Phase 006 - Mismatch classification

> **Summary File:** [SUMMARY.md](SUMMARY.md)
> **Phase ID:** 006
> **Status:** Implemented - Pending Review
> **Design References:** [../design/design.md](../design/design.md)
> **Patch References:** [../patch/phase-006-mismatch-classification.patch.md](../patch/phase-006-mismatch-classification.patch.md)

---

## Objective

Add machine-readable mismatch classifications across compare, verdict, and gate workflows so frontend QA artifacts explain why a device failed instead of only reporting pass/fail.

## Why this phase exists

The package already had reusable compare sessions, verdicts, and threshold-aware gate outputs, but failure reporting still stopped too early at generic pass/fail/invalid labels. That made downstream automation and human review less informative because callers still had to infer whether a failure came from visible change, dimension drift, diff-tool failure, or non-comparable images. This phase closes that product gap and also hardens diff detection so RGB-only changes are no longer missed when alpha stays zero.

## Action points / execution checklist

- [x] add pair-level mismatch classifications to `compare_reports.py`
- [x] carry classification fields and grouped mismatch summaries into `qa_verdict.py`
- [x] preserve mismatch classification summaries into `qa_gate.py`
- [x] update workflow skill surfaces so classification-aware outputs are part of the visible product contract
- [x] fix diff detection so RGB-only differences are detected even when Pillow reports no RGBA bbox
- [x] validate classification output on a real responsive expected/actual workflow
- [x] validate a forced mismatch sample so verdict and gate outputs show non-pass classifications correctly
- [x] validate that verdict generation treats empty/no-pairs comparison input as invalid instead of pass

## Verification

- `compare_reports.py` emits `classification` / `classification_reason` per pair plus `classification_summary`
- `qa_verdict.py` emits `classification`, `classification_reason`, and `mismatch_classification_summary`
- `qa_gate.py` preserves `mismatch_classification_summary` and per-device classification values
- `diff_images.py` detects RGB-only visual changes without depending on RGBA bbox truthiness alone

## Exit criteria

- compare artifacts explain why each device matched or failed
- verdict artifacts group failures by mismatch class rather than device name only
- gate artifacts preserve classification context alongside policy violations
- docs and governance surfaces describe the classification-aware QA model honestly
- version/package metadata are ready for release and install update
