# Phase 008 - Metadata and acquisition witnesses

> **Summary File:** [SUMMARY.md](SUMMARY.md)
> **Phase ID:** 008
> **Status:** Implemented - Pending Review
> **Design References:** [../design/design.md](../design/design.md)
> **Patch References:** [../patch/phase-008-metadata-and-acquisition-witnesses.patch.md](../patch/phase-008-metadata-and-acquisition-witnesses.patch.md)

---

## Objective

Extend the frontend-vision runtime so capture outputs include more structured, non-visual truth: acquisition summaries for scrape/prerender steps and provider-returned metadata/links when available.

## Why this phase exists

The package already emits screenshots, rendered HTML, and rendered text, but frontend debugging still needs more context about how those witnesses were acquired. Without acquisition/metadata witnesses, the user sees the page state but has less machine-readable visibility into whether scrape/prerender succeeded cleanly, what content type came back, and whether metadata/links were exposed by the provider.

## Action points / execution checklist

- [x] add acquisition-summary recording for scrape/prerender witness calls
- [x] persist acquisition witness JSON artifacts beside capture outputs
- [x] expose metadata witness fields in the capture model when provider metadata exists
- [x] surface metadata/acquisition paths in text output and evidence bundle artifacts
- [x] keep runtime changes bounded to checked provider capabilities rather than inventing console/network features the provider docs do not promise
- [x] sync docs/version metadata for the new witness layer

## Verification

- `python3 -m py_compile webview_screenshort/headless_render_api.py webview_screenshort/capture_service.py screenshot.py` succeeds
- `python3 screenshot.py https://headless-render-api.com/docs --engine headless --mode viewport --witness-mode frontend-default --output-format json --report-file /tmp/webview_v223_report.json` succeeds
- the returned capture now includes `acquisition_path`
- the returned capture now includes `acquisition_summary.scrape`
- the emitted evidence bundle now carries acquisition witness references
- plugin validation still succeeds after the witness-layer metadata additions

## Exit criteria

- the package exposes acquisition truth in machine-readable form instead of only final capture artifacts
- capture outputs surface metadata/acquisition witness paths when available
- docs describe these witnesses honestly as checked provider outputs, not full browser-devtools/network tracing
