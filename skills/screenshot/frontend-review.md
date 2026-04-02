# Frontend Review Workflow

## When to use
Use this screenshot skill before giving UI/UX/layout feedback when the real rendered page matters more than source code guesses.

## Suggested sequence
1. Capture the target URL.
2. Confirm the screenshot file path.
3. Read the image.
4. Analyze visual evidence.
5. Only then recommend UI/UX/layout changes.

## What to look for
- visual hierarchy
- spacing rhythm
- card density
- content readability
- sidebar/nav balance
- responsive-looking constraints visible in desktop capture
- obvious CSR loading issues or half-rendered sections

## Typical commands
```bash
/screenshot https://example.com --wait --mode viewport
/screenshot https://example.com/docs --wait --mode fullpage
```
