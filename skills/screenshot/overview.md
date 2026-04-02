# Screenshot Frontend Workflow

This skill is for frontend-development visual work.

Use it when Claude needs to see the real rendered page so it can help with:
- layout balance
- spacing and hierarchy
- UX/UI inspection
- CSR/hydration visibility
- docs-page or dashboard visual review

Recommended capture defaults:
- use `--wait` for CSR / SPA pages
- use `--mode viewport` for focused above-the-fold review
- use `--mode fullpage` for docs, settings pages, and long flows

After capture, Claude should read the image file and continue with visual analysis if needed.
