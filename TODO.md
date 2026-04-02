# Webview Screenshort - TODO

> **Last Updated:** 2026-04-03

---

## ✅ Completed

- [x] Baseline screenshot CLI exists (`screenshot.py`).
- [x] Reorganized the package into governed plugin layout.
- [x] Added plugin metadata under `.claude-plugin/plugin.json`.
- [x] Replaced the stale project-local skill path with the current package path.
- [x] Verified real CSR capture against `https://claw-frontend-dev.nodenetwork.ovh/docs` in viewport and fullpage modes using `--wait`.
- [x] Added a frontend-review workflow surface through `skills/screenshot/` plus `agents/webview-vision-assist.md`.

---

## 📋 Tasks To Do

### Current Plugin Execution
- [x] Validate `claude plugins validate <workspace-root>` for this package.
- [x] Add the package to the shared `darkwingtm` local marketplace and install it.
- [x] Validate skill/package surfaces after install.
- [x] Validate agent visibility after install.

### Code Improvements
- [x] Move hardcoded API endpoints in `screenshot.py` to env/config resolution.
- [x] Add configurable timeout handling instead of fixed values only.
- [x] Add a clearer machine-readable success output mode for follow-on skill workflows.

### Frontend Vision Workflow
- [x] Add a higher-level review skill flow that captures first and then guides screenshot-based UI analysis.
- [ ] Validate workflow on at least one more CSR-heavy frontend target.
- [ ] Validate `/reload-plugins` and restart-time visibility for the installed package.
- [ ] Complete separate-repo cutover and retire shared-workspace authority once the standalone repo becomes the source of truth.

---

## 📜 History

| Date | Changes |
|------|---------|
| 2026-04-03 | Refactored the old project-local screenshot skill into governed plugin layout, added a frontend-vision workflow surface, verified real CSR capture against the NodeNetwork docs page, added the package to the shared `darkwingtm` marketplace, verified installed agent/skill surfaces, made runtime execution plugin-root portable, and added config-driven plus structured JSON output support in `screenshot.py`. |
| 2026-01-28 | Initial TODO created |
