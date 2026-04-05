# Webview Screenshort - TODO

> **Last Updated:** 2026-04-05

---

## ✅ Completed

- [x] Baseline screenshot CLI exists (`screenshot.py`).
- [x] Reorganized the package into governed plugin layout.
- [x] Added plugin metadata under `.claude-plugin/plugin.json`.
- [x] Replaced the stale project-local skill path with the current package path.
- [x] Verified real CSR capture against `https://claw-frontend-dev.nodenetwork.ovh/docs` in viewport and fullpage modes using `--wait`.
- [x] Added a frontend-review workflow surface through `skills/screenshot/` plus `agents/webview-vision-assist.md`.
- [x] Completed standalone-repo cutover and retired shared-workspace authority from the public package posture.
- [x] Normalized the active command contract and governance docs around package CLI module execution after root-wrapper retirement.
- [x] Fixed higher-level review skills so an explicit `--witness-mode` is preserved instead of being silently overridden by hard-appended defaults.
- [x] Ignored generated screenshot-side JSON/HTML/TXT evidence outputs so local runtime artifacts do not pollute release diffs by default.

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
- [x] Add compare-session history browsing so saved QA artifacts can be listed and reused more easily.
- [x] Add expected-reference bundles so saved compare sessions can be promoted into reusable QA baselines.
- [x] Add apply-reference workflow so saved baselines can be replayed against fresh reports automatically.
- [x] Add reference-bundle browsing so saved baseline artifacts can be listed and reused more easily.
- [x] Add a dedicated bundle-lifecycle skill surface so baseline artifacts can be listed, created, and applied from one front door.
- [x] Add reference-bundle apply/browse ergonomics so repo-local baseline workflows can be reused with less path hunting.
- [x] Add live baseline replay so a saved reference bundle can capture a fresh current report from a URL and emit a new expected/actual compare session automatically.
- [x] Harden reference-bundle metadata so reusable baselines carry explicit reference-side/report information.
- [x] Add a QA verdict layer so compare/live-replay artifacts can end in reusable machine-readable pass/fail output instead of raw pair metadata only.
- [x] Add a QA gate layer so verdict artifacts can be checked against explicit required-device and diff-threshold policy rules.
- [x] Add a one-step baseline gate workflow so saved bundle + live URL + policy evaluation can finish in one run.
- [x] Add reusable gate policy presets so common threshold rules do not need to be retyped every time.
- [x] Add policy preset discovery so built-in gate policies can be selected by name instead of raw file paths.
- [x] Add multiple semantic policy presets so common QA goals can be selected by intent rather than one strict preset only.
- [x] Add named policy families so semantic presets can be grouped and selected by canonical family/name selectors.
- [x] Add machine-readable mismatch classifications so compare/verdict/gate artifacts explain why a device failed, not only that it failed.
- [x] Harden `webview-vision-assist` so it routes more clearly between focused, responsive, compare-review, live baseline replay, verdict-generation, gate-evaluation, one-step baseline-gate, and preset-discovery paths.
- [x] Validate `/reload-plugins` and restart-time visibility for the installed package.
- [x] Start strategic runtime refactor with an internal `webview_screenshort/` package instead of keeping orchestration only in top-level scripts.
- [x] Add richer witness modes so capture can emit screenshot-only, screenshot + rendered HTML/text, CSR-debug, responsive, and session-replay flows.
- [x] Add rendered HTML / rendered text evidence bundle output on top of the screenshot-era report model.
- [x] Add bounded session-replay inputs (`--header`, `--origin-header`, `--cookie`, `--cookie-file`) for logged-in-state capture planning/execution.
- [x] Upgrade skill and agent wording so routing is witness-mode-aware rather than screenshot-only by default.
- [x] Add semantic page witness output so rendered HTML can produce a reusable structure summary artifact.
- [x] Preserve semantic/acquisition witness indexes in responsive capture-set outputs and evidence bundles.
- [x] Reorganize compare / QA / reference logic into package-internal domains instead of leaving them only as root scripts.
- [x] Convert root Python commands into compatibility-thin wrappers over package-internal CLI adapters.
- [x] Remove root-script imports from `webview_screenshort/workflows.py` so internal package modules depend on package modules only.
- [x] Remove direct script-to-script subprocess coupling where in-process module reuse now exists.
- [x] Move auth-context authority into `webview_screenshort/capture/auth.py` while preserving `auth_context.py` as a compatibility shim.
- [x] Move headless-render-api authority into `webview_screenshort/capture/headless_api.py` while preserving `headless_render_api.py` as a compatibility shim.
- [x] Start splitting `capture_service.py` by moving config/path/witness responsibilities into `webview_screenshort/capture/` modules.
- [x] Extract capture models, engines, reporting, and runtime modules under `webview_screenshort/capture/`.
- [x] Move key consumers to import through `webview_screenshort/capture/service.py` as the newer capture authority surface.
- [x] Reduce `capture_service.py` to an explicit compatibility facade instead of leaving duplicate capture implementation there.
- [x] Add semantic companion classification summaries to compare / verdict / gate artifacts.
- [x] Add semantic-aware gate policy keys so gate presets can fail on semantic drift explicitly.
- [x] Add finer semantic gate rule granularity for title/headings/structure/link/button/form/input drift.
- [x] Migrate the active command contract to `PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" python3 -m webview_screenshort.cli.<tool>`.
- [x] Retire root wrapper scripts from the active root structure into `prototype/root-wrappers/`.

---

## 📜 History

| Date | Changes |
|------|---------|
| 2026-04-05 | Fixed release blockers before publish: higher-level review skills now preserve an explicit operator-provided `--witness-mode`, generated `screenshot/*.json|*.html|*.txt` runtime outputs are now ignored by default, and the package version moved to `2.34.0`. |
| 2026-04-05 | Normalized the active command/gov-doc contract after wrapper retirement: package CLI modules are now the active programmable surface, `capture.service` is described as the active capture authority, retired wrappers stay under `prototype/root-wrappers/` for compatibility reference only, and the package version moved to `2.33.0`. |
| 2026-04-05 | Retired root wrapper scripts from the active root structure: the active command contract now runs through `PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" python3 -m webview_screenshort.cli.<tool>`, retired wrappers moved under `prototype/root-wrappers/`, and the package cleanup can now close without a root-script pile remaining in the active surface. |
| 2026-04-05 | Added finer semantic gate rule granularity: built-in semantic gate policies can now target title/headings/structure/link/button/form/input drift more explicitly, and the package version moved to `2.32.0`. |
| 2026-04-05 | Added semantic-aware gate rules: built-in gate presets and gate policy evaluation can now fail on semantic drift such as missing semantic witness or semantic structure/content changes, and the package version moved to `2.31.0`. |
| 2026-04-05 | Added semantic-aware QA companion output: compare/verdict/gate artifacts now preserve semantic companion classifications on top of visual diff classifications, and the package version moved to `2.30.0`. |
| 2026-04-05 | Finalized the capture authority surface: capture models/engines/reporting/runtime modules now exist under `webview_screenshort/capture/`, key consumers use `capture.service`, `capture_service.py` is now a compatibility facade, and the package version moved to `2.29.0`. |
| 2026-04-05 | Extracted capture runtime modules further: models/engines/reporting/runtime now live under `webview_screenshort/capture/`, key consumers import through `capture.service`, and the package version moved to `2.28.0`. |
| 2026-04-05 | Started the deeper capture-service split: config/path/witness responsibilities now have dedicated `capture/` modules, `capture_service.py` now reuses them as a facade, and the package version moved to `2.27.0`. |
| 2026-04-05 | Deepened the capture-domain split: auth-context and headless-render-api authority now live under `webview_screenshort/capture/`, legacy import paths remain as compatibility shims, and the package version moved to `2.26.0`. |
| 2026-04-05 | Reorganized the Python package structure: compare / QA / reference logic now lives behind package-internal domains, root commands are compatibility-thin wrappers over internal CLI adapters, `workflows.py` no longer imports root scripts directly, direct script-to-script subprocess coupling was reduced through module reuse, and the package version moved to `2.25.0`. |
| 2026-04-05 | Added semantic page witness output on top of the richer frontend-vision stack: rendered HTML can now emit machine-readable page-structure JSON, responsive capture-set outputs now preserve semantic/acquisition witness indexes, reference-bundle creation now copies semantic witness artifacts when present, and the package version moved to `2.24.0`. |
| 2026-04-05 | Added metadata and acquisition witness output on top of the frontend-vision upgrade: richer capture runs now preserve scrape/prerender acquisition summaries in machine-readable form, and the package version moved to `2.23.0`. |
| 2026-04-05 | Started the strategic frontend-vision upgrade: added an internal `webview_screenshort/` runtime package, moved capture/replay/gate logic toward reusable modules, added richer witness modes plus evidence-bundle output with rendered HTML / rendered text artifacts, added bounded session-replay inputs for logged-in-state capture, and upgraded skill/agent routing/docs toward screenshot-first but HTML-aware frontend vision. |
| 2026-04-04 | Added machine-readable mismatch classifications (`exact_match`, `visual_change_region`, `dimension_shift`, `size_mismatch`, `diff_error`) across compare/verdict/gate artifacts, fixed RGBA diff detection so RGB-only changes are no longer missed, validated both responsive and forced-mismatch workflows, and bumped the plugin/marketplace package versions to `2.21.0`. |
| 2026-04-04 | Added named policy family metadata (`family`, `name`, `selector`, `aliases`) across the semantic presets, validated canonical family/name selectors plus legacy aliases against the checked NodeClaw docs workflow, and bumped the plugin/marketplace package versions to `2.20.0`. |
| 2026-04-04 | Added semantic policy presets (`smoke-responsive`, `layout-major-shift`, `mobile-critical`, `content-tolerant`) on top of the strict preset, validated semantic preset selection against the checked NodeClaw docs workflow, and bumped the plugin/marketplace package versions to `2.19.0`. |
| 2026-04-04 | Added `list_policy_presets.py`, added `skills/policy-presets/SKILL.md`, added `--policy-preset` support to `qa_gate.py` and `reference_live_gate.py`, validated named preset selection against the checked NodeClaw docs workflow, and bumped the plugin/marketplace package versions to `2.18.0`. |
| 2026-04-04 | Added `reference_live_gate.py`, added `skills/reference-live-gate/SKILL.md`, added `support/policies/strict-responsive-zero-diff.json`, validated one-step saved-baseline + live-URL + gate evaluation against the checked NodeClaw docs workflow, and bumped the plugin/marketplace package versions to `2.17.0`. |
| 2026-04-04 | Added `qa_gate.py`, added `skills/qa-gate/SKILL.md`, validated threshold-aware gate evaluation against the checked live replay/session artifacts, and bumped the plugin/marketplace package versions to `2.16.0`. |
| 2026-04-04 | Added `qa_verdict.py`, added `skills/qa-verdict/SKILL.md`, validated reusable pass/fail verdict generation against the checked live replay/session artifacts, and bumped the plugin/marketplace package versions to `2.15.0`. |
| 2026-04-04 | Fixed remaining authority/update drift after `2.14.0` so README and phase docs now point to repo-local marketplace update/install posture first, keep `darkwingtm` explicitly compatibility-only, and bumped the plugin/marketplace package versions to `2.14.1`. |
| 2026-04-04 | Added `reference_live_bundle.py`, added `skills/reference-live-review/SKILL.md`, hardened bundle metadata with explicit reference-side/report fields, made newly created bundles self-contained with bundled baseline report assets, fixed RGBA diff-pixel counting, tightened compare success semantics so non-diffable pairs fail replay, validated live baseline replay against the NodeClaw docs page, and bumped the plugin/marketplace package versions to `2.14.0`. |
| 2026-04-04 | Added `skills/reference-bundles/SKILL.md`, lifted bundle lifecycle operations into a dedicated front-door skill surface, registered the repo-local `webview-screenshort` marketplace, installed `webview-screenshort@webview-screenshort`, and shipped the `2.13.0` bundle-lifecycle wave. |
| 2026-04-04 | Added `list_reference_bundles.py`, validated reference-bundle browsing against saved baseline artifacts, and bumped the plugin/marketplace package versions to `2.12.0`. |
| 2026-04-04 | Added `apply_reference_bundle.py`, validated replaying a saved reference bundle against a fresh report, and bumped the plugin/marketplace package versions to `2.11.0`. |
| 2026-04-04 | Added `create_reference_bundle.py`, validated reusable expected-reference bundle artifacts, and bumped the plugin/marketplace package versions to `2.10.0`. |
| 2026-04-04 | Added `list_compare_sessions.py`, validated compare-session history browsing against saved QA artifacts, and bumped the plugin/marketplace package versions to `2.9.0`. |
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
