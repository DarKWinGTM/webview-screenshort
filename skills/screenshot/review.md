# Screenshot Review Flow

Use this workflow when Claude should both capture the page and immediately continue with screenshot-based frontend review.

## Recommended sequence
1. Capture the page with the screenshot skill using `--output-format json`.
2. If responsive review matters across the full breakpoint set, prefer `--capture-set responsive`; otherwise choose one of `--device desktop`, `--device tablet`, or `--device mobile`.
3. Read the JSON result and confirm:
   - `success`
   - `output_path`
   - `engine_used`
   - `mode_effective`
   - `wait_effective`
   - `viewport_width`
   - `viewport_height`
4. Read the image file at `output_path`, or each `captures[].output_path` when a responsive capture set was used.
5. Analyze layout, spacing, hierarchy, readability, and visible UX/UI issues.
6. Only then recommend frontend changes.

## Why this matters
This keeps frontend review evidence-first instead of code-first guessing.
