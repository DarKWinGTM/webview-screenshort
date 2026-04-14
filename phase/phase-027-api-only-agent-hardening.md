# Phase 027 - API-only agent hardening

> **Summary File:** [SUMMARY.md](SUMMARY.md)
> **Phase ID:** 027
> **Status:** Implemented - Pending Review
> **Design References:** [../design/design.md](../design/design.md)
> **Patch References:** [../patch/phase-027-api-only-agent-hardening.patch.md](../patch/phase-027-api-only-agent-hardening.patch.md)

---

## Objective

Harden the active agent and skill surfaces so they stay on the API-based capture path only and explicitly ban Playwright/Chromium/local-browser probing.

## Why this phase exists

The package already runs through remote capture APIs and is intentionally not a local-browser automation tool. Even after the public-target reachability guard, agent/skill behavior could still drift into generic frontend verification habits such as probing Playwright or Chromium availability on the local machine. That behavior is out of scope for this package and adds unwanted local-browser weight. This phase locks the operator-facing behavior to the real architecture: API-based capture only.

## Action points / execution checklist

- [x] update the companion agent guidance to say directly that it must never probe Playwright/Chromium/Chrome/WebKit/Selenium/Puppeteer or any other local browser stack
- [x] update the active screenshot/review/live-replay skill surfaces to ban local browser discovery/fallback commands explicitly
- [x] sync README and design wording so the package now describes itself as API-only more directly, not only as public-target-only
- [x] sync TODO, changelog, and phase summary for the API-only hardening wave

## Verification

- checked active agent/skill docs now explicitly ban local browser probing
- checked README/design now describe the package as API-only more directly
- `claude plugins validate /home/node/workplace/AWCLOUD/TEMPLATE/PLUGIN/webview-screenshort` succeeds
- `claude plugin update "webview-screenshort@darkwingtm" --scope user` updates the installed plugin to `2.42.0`

## Exit criteria

- active operator-facing surfaces now say the package is API-only clearly enough that local browser probing is out of bounds
- the plugin no longer describes local browser discovery as a valid troubleshooting or fallback path
- installed plugin/runtime wording stays aligned with the API-only capture contract
