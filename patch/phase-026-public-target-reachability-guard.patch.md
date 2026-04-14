# Phase 026 Public Target Reachability Guard Patch

## 0) Document Control

> **Current Version:** 1.0
> **Status:** Implemented - Pending Review
> **Target Design:** [../design/design.md](../design/design.md) v2.41.0
> **Target Phase:** [../phase/phase-026-public-target-reachability-guard.md](../phase/phase-026-public-target-reachability-guard.md)
> **Session:** d7dcb67a-20d7-48df-bbbd-a3f0247649ee
> **Full history:** [../changelog/changelog.md](../changelog/changelog.md)

---

## 1) Context

This patch captures the public-target-contract wave: make the package reject localhost/private/local network targets before remote capture begins so the runtime behavior matches the real remote-engine architecture.

## 2) Analysis

Risk level: Medium

The code change is small, but it changes user-visible behavior from late remote-engine failure to early explicit contract rejection. That is the correct direction because the old behavior hid the real product boundary. The safest implementation path is to add one capture-entrypoint validator, keep the failure message direct, and sync every operator-facing surface to the same public-target-only contract.

---

## 3) Change Items

### Change Item 1
- **Target location:** `webview_screenshort/capture/service.py`, `webview_screenshort/capture/url_policy.py`
- **Change type:** replacement

**Before**
```text
Capture entrypoints accepted local/private-style targets and let them fall through into the remote engine layer, where failures later appeared as provider-side screenshot errors.
```

**After**
```text
Capture entrypoints now validate target reachability first and reject localhost/private/local network targets with a direct public-target contract message before remote engine execution begins.
```

### Change Item 2
- **Target location:** CLI help text plus active README/skill/agent/design surfaces
- **Change type:** replacement

**Before**
```text
Operator-facing wording described URL capture broadly enough that localhost/private targets could look like valid inputs even though the architecture used remote engines only.
```

**After**
```text
Operator-facing wording now states publicly reachable `http(s)` URL explicitly and explains that localhost/private/local network targets are out of scope for the current remote-engine architecture.
```

---

## 4) Verification

- [x] compile validation succeeds for the URL-policy, capture-service, and affected CLI modules
- [x] a localhost probe now fails fast with the public-target contract message
- [x] plugin validation succeeds after the contract/docs sync

---

## 5) Rollback Approach

If the target guard proves too strict, narrow the hostname policy carefully while preserving the core public-target contract. Do not roll back to the old behavior where unreachable local/private targets fall through into remote engine execution and fail with misleading downstream errors.
