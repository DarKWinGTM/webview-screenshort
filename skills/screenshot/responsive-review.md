# Responsive Review Workflow

Use this workflow when frontend review should compare the same page across desktop, tablet, and mobile captures.

## Recommended sequence
1. Capture desktop, tablet, and mobile screenshots with `--output-format json`.
2. Read each JSON result and collect:
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
/screenshot https://example.com --device desktop --wait --mode viewport --output-format json
/screenshot https://example.com --device tablet --wait --mode viewport --output-format json
/screenshot https://example.com --device mobile --wait --mode viewport --output-format json
```
