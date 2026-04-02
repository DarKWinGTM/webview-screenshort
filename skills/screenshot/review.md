# Screenshot Review Flow

Use this workflow when Claude should both capture the page and immediately continue with screenshot-based frontend review.

## Recommended sequence
1. Capture the page with the screenshot skill using `--output-format json`.
2. Read the JSON result and confirm:
   - `success`
   - `output_path`
   - `engine_used`
   - `mode_effective`
   - `wait_effective`
3. Read the image file at `output_path`.
4. Analyze layout, spacing, hierarchy, readability, and visible UX/UI issues.
5. Only then recommend frontend changes.

## Why this matters
This keeps frontend review evidence-first instead of code-first guessing.
