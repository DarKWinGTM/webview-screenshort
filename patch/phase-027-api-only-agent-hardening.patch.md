# Phase 027 API-Only Agent Hardening Patch

## 0) Document Control

> **Current Version:** 1.0
> **Status:** Implemented - Pending Review
> **Target Design:** [../design/design.md](../design/design.md) v2.42.0
> **Target Phase:** [../phase/phase-027-api-only-agent-hardening.md](../phase/phase-027-api-only-agent-hardening.md)
> **Session:** d7dcb67a-20d7-48df-bbbd-a3f0247649ee
> **Full history:** [../changelog/changelog.md](../changelog/changelog.md)

---

## 1) Context

This patch captures the API-only hardening wave: make the active agent and skill surfaces state directly that the package must stay on the API-based capture flow and must not drift into local browser probing.

## 2) Analysis

Risk level: Low

This is an operator-surface hardening patch. It does not change the capture engine implementation itself; it changes the documented execution contract so the agent/skill layer stops improvising generic local-browser verification moves that do not belong to this package.

---

## 3) Change Items

### Change Item 1
- **Target location:** `agents/webview-vision-assist.md`, active screenshot/review/live-replay skills
- **Change type:** replacement

**Before**
```text
The active operator-facing surfaces described the public-target URL contract, but they did not yet ban Playwright/Chromium/local-browser probing explicitly enough.
```

**After**
```text
The active operator-facing surfaces now say directly that the package must stay on the API-based capture path and must never probe Playwright, Chromium, Chrome, WebKit, Selenium, Puppeteer, or other local browser tooling.
```

### Change Item 2
- **Target location:** README/design/TODO/changelog/phase wording
- **Change type:** replacement

**Before**
```text
The governance/docs described the package as remote-engine/public-target-only, but the API-only execution contract was still too implicit.
```

**After**
```text
The governance/docs now describe the package as API-only more directly, so the real execution contract is visible from both the code-facing and operator-facing layers.
```

---

## 4) Verification

- [x] checked active agent/skill docs now explicitly ban local browser probing
- [x] checked README/design now describe the package as API-only more directly
- [x] `claude plugins validate /home/node/workplace/AWCLOUD/TEMPLATE/PLUGIN/webview-screenshort` succeeds
- [x] the installed user-scope plugin updates to `2.42.0`

---

## 5) Rollback Approach

If the wording is later refined, keep the API-only contract intact. Do not revert to vague operator guidance that leaves room for Playwright/Chromium/local-browser probing to reappear as an ad hoc fallback behavior.
