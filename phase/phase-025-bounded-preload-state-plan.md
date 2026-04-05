# Phase 025 - Bounded preload-state plan

> **Summary File:** [SUMMARY.md](SUMMARY.md)
> **Phase ID:** 025
> **Status:** Implemented - Pending Review
> **Design References:** [../design/design.md](../design/design.md)
> **Patch References:** [../patch/phase-025-bounded-preload-state-plan.patch.md](../patch/phase-025-bounded-preload-state-plan.patch.md)

---

## Objective

Add bounded operator-provided cookie replay plus preloaded-state replay support for authenticated rendering without assuming direct browser-storage injection by the provider.

## Why this phase exists

The current authenticated-capture model already supports request headers, origin-forwarded `Prerendercloud-*` headers, and cookies, but it does not provide a first-class way to carry origin-bootstrap state for pages that need more than cookies alone. At the same time, the checked provider/docs do not prove direct localStorage/sessionStorage injection support. This phase therefore plans a bounded replay model that forwards structured preload state to the origin and requires app-side reconstruction into `window.__PRELOADED_STATE__`.

## Action points / execution checklist

- [x] add first-class operator inputs such as `--preloaded-state-json` and `--preloaded-state-file`
- [x] extend the capture auth/session context so cookies plus preload state travel through one bounded replay model
- [x] transport preload state only through generated `Prerendercloud-*` origin-forwarded headers
- [x] require origin-side reconstruction into `window.__PRELOADED_STATE__`
- [x] persist only redacted preload/cookie summaries in reports and bundles
- [x] sanitize HTML witnesses so raw bootstrap state is not written into persisted artifacts
- [x] sync README/design/changelog/TODO after implementation validation

## Verification

- explicit preload inputs are validated and bounded
- cookies plus preload state can coexist under a safe header budget
- reports/bundles contain only redacted summaries, not raw bootstrap JSON
- focused capture with preload JSON emits redacted summary fields
- the package still does not claim direct browser storage injection or interactive login automation

## Exit criteria

- the package supports bounded cookie + preload replay for authenticated rendering
- the origin can reconstruct forwarded preload state into `window.__PRELOADED_STATE__`
- the operator-facing contract remains explicit, bounded, and redaction-safe
