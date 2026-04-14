# Phase 026 - Public target reachability guard

> **Summary File:** [SUMMARY.md](SUMMARY.md)
> **Phase ID:** 026
> **Status:** Implemented - Pending Review
> **Design References:** [../design/design.md](../design/design.md)
> **Patch References:** [../patch/phase-026-public-target-reachability-guard.patch.md](../patch/phase-026-public-target-reachability-guard.patch.md)

---

## Objective

Reject localhost/private/local network targets before remote engine execution and lock the package contract to publicly reachable `http(s)` page URLs only.

## Why this phase exists

The checked runtime architecture uses remote capture engines, so local/private targets such as `localhost`, loopback hosts, and RFC1918/private network addresses are not actually reachable from the rendering side. Before this phase, those targets could flow into the engine layer and then fail later with confusing provider-side errors. This phase makes the product truth explicit: the package is a public-web evidence tool in the current architecture, not a localhost/private-network capture tool.

## Action points / execution checklist

- [x] add a capture-domain URL policy helper for publicly reachable target validation
- [x] reject localhost, loopback, private-network, and other non-public-style targets before engine execution begins
- [x] return a direct contract error instead of surfacing downstream remote-engine errors for blocked targets
- [x] update screenshot/live-replay/live-gate CLI help text to say publicly reachable `http(s)` URL explicitly
- [x] sync README, design, active skills, companion agent, changelog, TODO, and phase summary to the public-target-only contract

## Verification

- `python3 -m py_compile /home/node/workplace/AWCLOUD/TEMPLATE/PLUGIN/webview-screenshort/webview_screenshort/capture/url_policy.py /home/node/workplace/AWCLOUD/TEMPLATE/PLUGIN/webview-screenshort/webview_screenshort/capture/service.py /home/node/workplace/AWCLOUD/TEMPLATE/PLUGIN/webview-screenshort/webview_screenshort/cli/screenshot.py /home/node/workplace/AWCLOUD/TEMPLATE/PLUGIN/webview-screenshort/webview_screenshort/cli/reference_live_bundle.py /home/node/workplace/AWCLOUD/TEMPLATE/PLUGIN/webview-screenshort/webview_screenshort/cli/reference_live_gate.py` succeeds
- a direct capture probe against `http://127.0.0.1:5174` now fails fast with the public-target contract message before remote engine execution
- `claude plugins validate /home/node/workplace/AWCLOUD/TEMPLATE/PLUGIN/webview-screenshort` succeeds

## Exit criteria

- localhost/private/local network targets no longer fall through into remote engine execution
- the package now reports the public-web-only contract directly at the capture entrypoint
- operator-facing docs and installed skill/agent surfaces all describe the same public-target-only behavior
