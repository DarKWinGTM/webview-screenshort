# Phase 014 - Capture facade cleanup

> **Summary File:** [SUMMARY.md](SUMMARY.md)
> **Phase ID:** 014
> **Status:** Implemented - Pending Review
> **Design References:** [../design/design.md](../design/design.md)
> **Patch References:** [../patch/phase-014-capture-facade-cleanup.patch.md](../patch/phase-014-capture-facade-cleanup.patch.md)

---

## Objective

Reduce `capture_service.py` to a true compatibility facade now that `webview_screenshort/capture/service.py` is the newer active authority surface.

## Why this phase exists

The previous waves established a newer capture authority surface and migrated key consumers onto it, but `capture_service.py` still duplicated substantial implementation. That left two practical authorities alive at once. This phase resolves that drift by turning `capture_service.py` into an explicit compatibility facade instead of a second implementation host.

## Action points / execution checklist

- [x] replace duplicated capture implementation inside `capture_service.py` with explicit re-exports from `capture.service`
- [x] keep legacy import names available from `capture_service.py`
- [x] verify key consumer flows after the facade cleanup
- [x] sync docs/version metadata for the capture facade cleanup wave

## Verification

- `python3 -m py_compile webview_screenshort/capture_service.py webview_screenshort/capture/service.py webview_screenshort/__init__.py webview_screenshort/cli/screenshot.py webview_screenshort/references/live.py screenshot.py reference_live_bundle.py reference_live_gate.py` succeeds
- `python3 screenshot.py https://example.com --mode viewport --witness-mode frontend-default --output-format json` succeeds
- `python3 reference_live_bundle.py --bundle /tmp/webview_wrapper_bundle.json --url https://example.com ... --output-format json` succeeds
- `claude plugins validate /home/node/workplace/AWCLOUD/TEMPLATE/PLUGIN/webview-screenshort` succeeds

## Exit criteria

- `capture.service` is the active authority surface for capture consumers
- `capture_service.py` remains available only as a compatibility facade
- the capture side no longer carries two competing implementation authorities for the same responsibilities
