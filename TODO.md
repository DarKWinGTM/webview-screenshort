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
- [x] Add compare-review skill support plus hardened report-schema metadata for reusable regression-style review.
- [x] Add a structured comparison helper so report-to-report review has reusable pair metadata instead of only manual interpretation.
- [x] Add diff-assisted compare evidence so compare-review can surface diff metrics and generated diff images.
- [x] Add named compare sessions so expected/actual review state can be persisted as a reusable artifact.
- [x] Harden `webview-vision-assist` so it routes more clearly between focused, responsive, and compare-review paths.
- [x] Validate `/reload-plugins` and restart-time visibility for the installed package.

---

## 📜 History

| Date | Changes |
|------|---------|
| 2026-04-04 | Added `compare_session.py`, validated reusable expected/actual compare-session artifacts, and bumped the plugin/marketplace package versions to `2.8.0`. |
| 2026-04-03 | Added `diff_images.py`, upgraded compare-report output with diff metrics and generated diff images, and bumped the plugin/marketplace package versions to `2.7.0`. |
| 2026-04-03 | Hardened `webview-vision-assist` so it routes more clearly between focused, responsive, and compare-review surfaces, and bumped the plugin/marketplace package versions to `2.6.0`. |
| 2026-04-03 | Added `compare_reports.py`, upgraded compare-review to use structured report pairing, validated the helper output against persisted responsive reports, and bumped the plugin/marketplace package versions to `2.5.0`. |
| 2026-04-03 | Hardened persisted report artifacts with explicit schema metadata, added `compare-review`, validated the new report format on focused and responsive flows, and bumped the plugin/marketplace package versions to `2.4.0`. |
| 2026-04-03 | Added persisted report-file output to `screenshot.py`, added direct `frontend-review` and `responsive-review` skills, validated both responsive and focused report-file flows, and bumped the plugin/marketplace package versions to `2.3.0`. |
| 2026-04-03 | Added one-run responsive capture-set support to `screenshot.py`, validated combined desktop/tablet/mobile JSON output against the NodeNetwork docs page, synced the responsive-review docs/agent workflow, and bumped the plugin/marketplace package versions to `2.2.0`. |
| 2026-04-03 | Normalized public install docs to the standalone repo root, validated `claude plugins marketplace add ./ --scope local` plus `claude plugins install webview-screenshort@webview-screenshort --scope local` from the repo root in an isolated HOME, and kept the shared `darkwingtm` path scoped as checked local workspace-development context. |
| 2026-04-03 | Refactored the old project-local screenshot skill into governed plugin layout, added a frontend-vision workflow surface, verified real CSR capture against the NodeNetwork docs page, added the package to the shared `darkwingtm` marketplace, verified installed agent/skill surfaces, made runtime execution plugin-root portable, added config-driven plus structured JSON output support in `screenshot.py`, closed current lifecycle checks, validated responsive mobile/tablet presets against a second frontend target (MDN JavaScript docs), and validated a responsive multi-capture desktop/tablet/mobile workflow against the NodeNetwork docs page. |
| 2026-01-28 | Initial TODO created |
