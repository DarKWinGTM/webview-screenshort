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
- [x] Completed standalone-repo cutover and retired shared-workspace authority from the public package posture.

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
- [x] Validate workflow on at least one more CSR-heavy frontend target.
- [x] Add mobile and tablet viewport presets for frontend responsive review.
- [x] Add responsive multi-capture workflow guidance for desktop/tablet/mobile review.
- [x] Add one-run responsive capture-set support with combined machine-readable output for desktop/tablet/mobile review.
- [x] Add persisted report-file output plus direct `frontend-review` / `responsive-review` skill surfaces.
- [x] Validate `/reload-plugins` and restart-time visibility for the installed package.

---

## 📜 History

| Date | Changes |
|------|---------|
| 2026-04-03 | Added persisted report-file output to `screenshot.py`, added direct `frontend-review` and `responsive-review` skills, validated both responsive and focused report-file flows, and bumped the plugin/marketplace package versions to `2.3.0`. |
| 2026-04-03 | Added one-run responsive capture-set support to `screenshot.py`, validated combined desktop/tablet/mobile JSON output against the NodeNetwork docs page, synced the responsive-review docs/agent workflow, and bumped the plugin/marketplace package versions to `2.2.0`. |
| 2026-04-03 | Normalized public install docs to the standalone repo root, validated `claude plugins marketplace add ./ --scope local` plus `claude plugins install webview-screenshort@webview-screenshort --scope local` from the repo root in an isolated HOME, and kept the shared `darkwingtm` path scoped as checked local workspace-development context. |
| 2026-04-03 | Refactored the old project-local screenshot skill into governed plugin layout, added a frontend-vision workflow surface, verified real CSR capture against the NodeNetwork docs page, added the package to the shared `darkwingtm` marketplace, verified installed agent/skill surfaces, made runtime execution plugin-root portable, added config-driven plus structured JSON output support in `screenshot.py`, closed current lifecycle checks, validated responsive mobile/tablet presets against a second frontend target (MDN JavaScript docs), and validated a responsive multi-capture desktop/tablet/mobile workflow against the NodeNetwork docs page. |
| 2026-01-28 | Initial TODO created |
