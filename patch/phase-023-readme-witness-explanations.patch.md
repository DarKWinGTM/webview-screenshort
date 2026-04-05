# Phase 023 README Witness Explanations Patch

## 0) Document Control

> **Current Version:** 1.0
> **Status:** Implemented - Pending Review
> **Target Design:** [../design/design.md](../design/design.md) v2.38.0
> **Target Phase:** [../phase/phase-023-readme-witness-explanations.md](../phase/phase-023-readme-witness-explanations.md)
> **Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e
> **Full history:** [../changelog/changelog.md](../changelog/changelog.md)

---

## 1) Context

This patch captures the README witness-clarity wave: improving operator understanding of the package by explaining what each witness type means in practice.

## 2) Analysis

Risk level: Low

This is a README clarity patch. The package already emitted these artifacts, but a user-facing explanation of their meaning reduces confusion about screenshot-only versus rendered-page witness capabilities and keeps the README aligned with the real scope of the tool.

---

## 3) Change Items

### Change Item 1
- **Target location:** `README.md`
- **Change type:** replacement

**Before**
```text
README listed the artifact types, but users still had to infer what screenshot, rendered HTML, rendered text, semantic page witness JSON, and prerendered HTML meant in practice.
```

**After**
```text
README now includes a witness comparison table plus a direct CSR/rendered-HTML explanation block describing what each witness means, when it is useful, and what it is not.
```

### Change Item 2
- **Target location:** package/governance metadata and README documentation sync files
- **Change type:** replacement

**Before**
```text
The witness-clarity improvement was not yet tracked as its own governed documentation wave.
```

**After**
```text
The witness-clarity improvement is tracked as the 2.38.0 README documentation wave.
```

---

## 4) Verification

- [x] checked README now explains the witness layers in practical terms
- [x] checked README now explains rendered HTML capability without overstating it into full browser-internal coverage
- [x] `claude plugins validate /home/node/workplace/AWCLOUD/TEMPLATE/PLUGIN/webview-screenshort` succeeds

---

## 5) Rollback Approach

If the new README explanation feels too detailed, reduce the prose while keeping a compact witness table. Do not revert to a README that only names artifact files without explaining what they mean for operators.
