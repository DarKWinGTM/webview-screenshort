# Responsive Review Workflow

Use this workflow when frontend review should compare the same page across desktop, tablet, and mobile captures.

This workflow expects a publicly reachable `http(s)` page URL. It is not designed for `localhost`, `127.0.0.1`, or private/local network targets in the current remote-engine architecture.

## Recommended sequence
1. Capture the page with `--capture-set responsive --output-format json` when one combined workflow result is preferred.
2. Read the JSON result and collect each entry from `captures[]`:
   - `device`
   - `output_path`
   - `viewport_width`
   - `viewport_height`
   - `engine_used`
3. Read each image file.
4. Compare:
   - content hierarchy
   - sidebar/nav behavior
   - text density
   - card stacking
   - overflow/cropping risk
   - spacing and readability
5. Summarize which issues are desktop-only, tablet-only, mobile-only, or cross-device.

## Suggested commands
```bash
/screenshot https://example.com --capture-set responsive --wait --mode viewport --output-format json
```
