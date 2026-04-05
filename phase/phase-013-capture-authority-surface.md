# Phase 013 - Capture authority surface

> **Summary File:** [SUMMARY.md](SUMMARY.md)
> **Phase ID:** 013
> **Status:** Implemented - Pending Review
> **Design References:** [../design/design.md](../design/design.md)
> **Patch References:** [../patch/phase-013-capture-authority-surface.patch.md](../patch/phase-013-capture-authority-surface.patch.md)

---

## Objective

Extract additional capture runtime modules and start moving key consumers onto `webview_screenshort/capture/service.py` as the newer capture authority surface.

## Why this phase exists

After the first capture-service split, `capture_service.py` was thinner but still remained the practical authority for many consumers. This phase adds the next runtime-oriented modules — models, engines, reporting, and runtime orchestration — and starts shifting key consumers to the newer `capture.service` surface while preserving the old `capture_service.py` path as a compatibility facade.

## Action points / execution checklist

- [x] add `webview_screenshort/capture/models.py`
- [x] add `webview_screenshort/capture/engines.py`
- [x] add `webview_screenshort/capture/reporting.py`
- [x] add `webview_screenshort/capture/runtime.py`
- [x] promote `webview_screenshort/capture/service.py` into a richer authority surface instead of a trivial wildcard shim
- [x] update key consumers (`__init__.py`, screenshot CLI, live replay) to import through `capture.service`
- [x] verify focused screenshot and live replay flows after the consumer migration
- [x] sync docs/version metadata for the capture authority-surface wave

## Verification

- `python3 -m py_compile webview_screenshort/capture/models.py webview_screenshort/capture/engines.py webview_screenshort/capture/reporting.py webview_screenshort/capture/runtime.py webview_screenshort/capture/service.py webview_screenshort/__init__.py webview_screenshort/cli/screenshot.py webview_screenshort/references/live.py screenshot.py reference_live_bundle.py reference_live_gate.py` succeeds
- `python3 screenshot.py https://example.com --mode viewport --witness-mode frontend-default --output-format json` succeeds
- `python3 reference_live_bundle.py --bundle /tmp/webview_wrapper_bundle.json --url https://example.com ... --output-format json` succeeds
- the checked screenshot and live replay flows still work after the authority-surface migration

## Exit criteria

- the capture package has explicit modules for models, engines, reporting, and runtime orchestration
- key consumers import through `capture.service` instead of pointing only at `capture_service.py`
- `capture_service.py` remains available as a compatibility facade while the newer capture package becomes more authoritative
