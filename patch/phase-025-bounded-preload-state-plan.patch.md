# Phase 025 Bounded Preload-State Plan Patch

## 0) Document Control

> **Current Version:** 1.0
> **Status:** Implemented - Pending Review
> **Target Design:** [../design/design.md](../design/design.md) v2.40.0
> **Target Phase:** [../phase/phase-025-bounded-preload-state-plan.md](../phase/phase-025-bounded-preload-state-plan.md)
> **Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e
> **Full history:** [../changelog/changelog.md](../changelog/changelog.md)

---

## 1) Context

This patch captures the authenticated-rendering wave for cookies plus bounded preload-state replay. The goal is to improve stateful rendering support without pretending the provider can inject browser storage directly.

## 2) Analysis

Risk level: Medium

The feature touches authenticated rendering, provider forwarding constraints, persisted artifacts, and app-side cooperation. The safest direction is to preserve the current cookie/header replay model, extend it with bounded structured preload input, and keep the whole system explicit about redaction, header budgets, and origin-side reconstruction requirements.

---

## 3) Change Items

### Change Item 1
- **Target location:** capture CLI/auth/runtime/provider transport flow
- **Change type:** replacement

**Before**
```text
Authenticated rendering replay was limited to request headers, forwarded `Prerendercloud-*` headers, and cookies.
```

**After**
```text
Authenticated rendering replay now supports cookies plus bounded operator-provided preload state, transported to the origin through generated `Prerendercloud-*` headers.
```

### Change Item 2
- **Target location:** witness/report/bundle persistence
- **Change type:** replacement

**Before**
```text
The package did not yet define how bootstrap state should be redacted/sanitized if it became part of authenticated rendering.
```

**After**
```text
The package now persists only redacted preload/cookie summaries and sanitized witness HTML, never raw bootstrap secrets/state.
```

---

## 4) Verification

- [x] preload input validation rejects invalid dual-input usage, non-object JSON, and oversize payloads
- [x] generated `Prerendercloud-*` preload headers are chunked and budget-checked
- [x] reports/bundles contain redacted preload/cookie summaries rather than raw bootstrap JSON
- [x] focused capture with preload JSON emits redacted summary fields
- [x] the package still does not claim direct `localStorage` / `sessionStorage` injection

---

## 5) Rollback Approach

If the bounded preload-state implementation proves too brittle, keep cookies/headers as the supported replay model and remove only the preload-specific inputs/transport. Do not weaken the boundary language by pretending direct browser-storage injection is supported when it is not verified.
