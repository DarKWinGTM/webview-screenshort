# Phase 011 - Capture-domain authority

> **Summary File:** [SUMMARY.md](SUMMARY.md)
> **Phase ID:** 011
> **Status:** Implemented - Pending Review
> **Design References:** [../design/design.md](../design/design.md)
> **Patch References:** [../patch/phase-011-capture-domain-authority.patch.md](../patch/phase-011-capture-domain-authority.patch.md)

---

## Objective

Move auth-context and headless-render-api ownership under `webview_screenshort/capture/` so the capture side starts to match the newer package-domain structure without breaking existing import paths.

## Why this phase exists

The package-organization wave established compare, QA, reference, and CLI domains, but the capture side still relied on older top-level package files as the main authority. This phase starts the next cleanup step by moving two clear capture subdomains into `capture/` while keeping the old paths as compatibility shims.

## Action points / execution checklist

- [x] move auth-context implementation authority into `webview_screenshort/capture/auth.py`
- [x] move headless-render-api implementation authority into `webview_screenshort/capture/headless_api.py`
- [x] turn `webview_screenshort/auth_context.py` into a compatibility shim
- [x] turn `webview_screenshort/headless_render_api.py` into a compatibility shim
- [x] update `capture_service.py` and package exports to import from `capture/` authority paths
- [x] verify that focused screenshot capture still works after the authority shift
- [x] sync docs/version metadata for the capture-domain authority wave

## Verification

- `python3 -m py_compile webview_screenshort/capture/auth.py webview_screenshort/capture/headless_api.py webview_screenshort/auth_context.py webview_screenshort/headless_render_api.py webview_screenshort/capture_service.py webview_screenshort/__init__.py screenshot.py` succeeds
- `python3 screenshot.py https://example.com --mode viewport --witness-mode frontend-default --output-format json` succeeds
- the checked screenshot flow still emits rendered HTML/text, acquisition witness, and semantic witness output after the capture authority shift

## Exit criteria

- auth-context and headless-render-api implementation authority live under `webview_screenshort/capture/`
- legacy import paths remain usable as compatibility shims
- the capture side is structurally closer to the newer package-domain model without disrupting existing flows
