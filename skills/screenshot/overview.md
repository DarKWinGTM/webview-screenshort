# Screenshot Frontend Workflow

This skill is for frontend-development visual work.

Use it when Claude needs to see the real rendered page so it can help with:

Target contract:
- use publicly reachable `http(s)` page URLs
- do not use `localhost`, `127.0.0.1`, loopback, or private/local network targets in the current remote-engine architecture
- layout balance
- spacing and hierarchy
- UX/UI inspection
- CSR/hydration visibility
- docs-page or dashboard visual review

Recommended capture defaults:
- use `--wait` for CSR / SPA pages
- use `--mode viewport` for focused above-the-fold review
- use `--mode fullpage` for docs, settings pages, and long flows
- use `--capture-set responsive` when frontend review should inspect the same page across desktop, tablet, and mobile in one run
- use one of `--device mobile` or `--device tablet` when only one breakpoint needs focused inspection
- use `--output-format json` when the screenshot result should feed a follow-on review workflow

After capture, Claude should read the image file and continue with visual analysis if needed.
