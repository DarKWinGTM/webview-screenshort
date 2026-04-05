# Phase 012 - Capture-service split

> **Summary File:** [SUMMARY.md](SUMMARY.md)
> **Phase ID:** 012
> **Status:** Implemented - Pending Review
> **Design References:** [../design/design.md](../design/design.md)
> **Patch References:** [../patch/phase-012-capture-service-split.patch.md](../patch/phase-012-capture-service-split.patch.md)

---

## Objective

Start thinning `capture_service.py` by moving config, path, and witness responsibilities into dedicated capture-domain modules while preserving the current capture facade behavior.

## Why this phase exists

After moving auth-context and headless-render-api authority into `capture/`, the biggest remaining monolith was still `capture_service.py`. This phase starts a safer split by extracting clear non-engine responsibilities first: config loading, output/path generation, and richer witness extraction. That reduces structural sprawl without forcing a risky all-at-once rewrite of capture orchestration.

## Action points / execution checklist

- [x] add `webview_screenshort/capture/config.py` for screenshot config/env loading
- [x] add `webview_screenshort/capture/paths.py` for output/report/bundle/path helpers
- [x] add `webview_screenshort/capture/witnesses.py` for witness normalization, HTML/text conversion, semantic summary building, and richer witness emission
- [x] update `capture_service.py` to import and reuse those modules instead of owning all three responsibility groups directly
- [x] keep `capture_service.py` as the active facade so current CLI and package imports still work unchanged
- [x] verify focused and responsive screenshot flows after the extraction
- [x] sync docs/version metadata for the capture-service split wave

## Verification

- `python3 -m py_compile webview_screenshort/capture/config.py webview_screenshort/capture/paths.py webview_screenshort/capture/witnesses.py webview_screenshort/capture_service.py screenshot.py` succeeds
- `python3 screenshot.py https://example.com --mode viewport --witness-mode frontend-default --output-format json` succeeds
- `python3 screenshot.py https://example.com --capture-set responsive --mode viewport --witness-mode responsive --output-format json` succeeds
- the checked capture flows still emit richer witness artifacts after the split

## Exit criteria

- `capture_service.py` is thinner than before and clearly delegates config/path/witness work into capture-domain modules
- the screenshot command still behaves the same from the user side
- the capture side moves closer to a professional package structure without breaking current flows
