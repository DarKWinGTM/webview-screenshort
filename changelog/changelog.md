# Changelog - Webview Screenshort

> **Parent Document:** [../design/design.md](../design/design.md)
> **Current Version:** 2.8.0
> **Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e

---

## Version History (Unified)

| Version | Date | Changes | Summary |
|---------|------|---------|---------|
| 2.8.0 | 2026-04-04 | **[Added named compare sessions](#version-280)** | Added `compare_session.py`, introduced reusable expected/actual compare-session artifacts, and moved compare-review closer to a durable QA workflow rather than one-off terminal output. |
| 2.7.0 | 2026-04-03 | **[Added diff-assisted compare evidence](#version-270)** | Added `diff_images.py`, upgraded report comparison to include diff metrics and generated diff images, and pushed compare-review closer to a practical expected/actual QA workflow. |
| 2.6.0 | 2026-04-03 | **[Hardened agent orchestration flow](#version-260)** | Updated `webview-vision-assist` so it routes more explicitly between focused review, responsive review, and compare-review paths, reducing ambiguity at the product entry layer. |
| 2.5.0 | 2026-04-03 | **[Added structured compare helper flow](#version-250)** | Added `compare_reports.py`, upgraded compare-review to use structured pair metadata, and pushed the package closer to a reusable expected/actual visual QA surface. |
| 2.4.0 | 2026-04-03 | **[Added compare-review workflow and hardened report schema](#version-240)** | Added a report-to-report comparison skill, hardened persisted report artifacts with explicit schema metadata, and pushed the package closer to a reusable frontend regression-review surface. |
| 2.3.0 | 2026-04-03 | **[Added review-skill and report-file workflow surfaces](#version-230)** | Added persisted report-file output, introduced dedicated `frontend-review` and `responsive-review` skills, and tightened the screenshot workflow so structured metadata can be re-read more directly in follow-on review flows. |
| 2.2.0 | 2026-04-03 | **[Added one-run responsive capture-set workflow](#version-220)** | Added first-class responsive capture-set support to `screenshot.py`, returned combined machine-readable desktop/tablet/mobile results from one run, and synced the frontend-review docs around the stronger responsive workflow. |
| 2.1.0 | 2026-04-03 | **[Normalized public install docs to repo-root marketplace guidance](#version-210)** | Reworked the public install story around repo-root local marketplace usage, validated `./`-based install from the standalone repo root, and kept the shared `darkwingtm` route scoped as local workspace development context. |
| 2.0.0 | 2026-04-03 | **[Plugin package and CSR frontend-vision validation](#version-200)** | Refactored the old project-local screenshot skill into a governed plugin package, added a frontend-review workflow surface, and verified real CSR capture against the NodeNetwork docs page. |
| 1.8 | 2026-02-07 | **[Project-Local Skill Implementation](#version-18)** | Implemented the older project-local screenshot skill model. |

---

<a id="version-280"></a>
## Version 2.8.0: Added named compare sessions

**Date:** 2026-04-04
**Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e

### Changes
- Added `compare_session.py` so compare workflows can persist a named compare-session artifact for later QA review.
- Added expected/actual-style labels to the session artifact model.
- Updated compare-review guidance and package docs so reusable compare sessions are now part of the intended QA workflow.
- Bumped plugin and marketplace package versions to `2.8.0`.

### Validation
- `python3 -m py_compile compare_session.py` succeeds.
- `python3 compare_session.py --name "nodeclaw-docs-regression" --left-report /tmp/webview_24_responsive_report.json --right-report /tmp/webview_24_responsive_report.json --left-label expected --right-label actual --comparison-json /tmp/webview_compare_diff.json --output /tmp/webview_compare_session.json` succeeds.
- the compare-session artifact persists the named expected/actual review state plus the structured comparison payload.

### Summary
The package now supports a more durable QA workflow by persisting named compare sessions instead of forcing every expected/actual review to live only in one-off comparison output.

---

<a id="version-270"></a>
## Version 2.7.0: Added diff-assisted compare evidence

**Date:** 2026-04-03
**Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e

### Changes
- Added `diff_images.py` so compare workflows can compute image-diff metrics and optionally write visual diff images.
- Upgraded `compare_reports.py` so comparison pairs now include diff metadata rather than only pairing information.
- Updated README and design wording so compare-review now explicitly covers diff-assisted expected/actual workflows.
- Bumped plugin and marketplace package versions to `2.7.0`.

### Validation
- `python3 -m py_compile compare_reports.py diff_images.py` succeeds.
- `python3 compare_reports.py /tmp/webview_24_responsive_report.json /tmp/webview_24_responsive_report.json --diff-dir /tmp/webview_diff_outputs --output-format json` succeeds.
- diff image files are generated for desktop, tablet, and mobile pairs.

### Summary
The package now exposes richer comparison evidence by pairing persisted reports with diff metrics and optional diff images, making compare-review more useful for expected/actual QA work.

---

<a id="version-260"></a>
## Version 2.6.0: Hardened agent orchestration flow

**Date:** 2026-04-03
**Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e

### Changes
- Updated `agents/webview-vision-assist.md` so the agent now classifies work into focused review, responsive review, or compare-review paths before acting.
- Made the agent prefer higher-level installed review surfaces where appropriate instead of treating everything like raw capture work.
- Updated README wording so the stronger orchestration behavior is reflected in the package overview.
- Bumped plugin and marketplace package versions to `2.6.0`.

### Validation
- `claude agents` still shows `webview-screenshort:webview-vision-assist` after package update.
- `claude plugins update webview-screenshort@darkwingtm --scope local` succeeds for the updated package.
- the runtime package remains validated through `claude plugins validate`.

### Summary
The package now has a clearer orchestration front door, reducing ambiguity about which review surface should be used for focused, responsive, or comparison-oriented frontend work.

---

<a id="version-250"></a>
## Version 2.5.0: Added structured compare helper flow

**Date:** 2026-04-03
**Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e

### Changes
- Added `compare_reports.py` to validate two persisted capture reports and emit structured comparison-pair metadata.
- Upgraded `skills/compare-review/SKILL.md` so it now uses the installed comparison helper rather than only manual report reading.
- Updated README and design guidance to describe the stronger expected/actual and regression-style review flow.
- Bumped plugin and marketplace package versions to `2.5.0`.

### Validation
- `python3 -m py_compile screenshot.py compare_reports.py` succeeds.
- `python3 compare_reports.py /tmp/webview_24_responsive_report.json /tmp/webview_24_responsive_report.json --output-format json` succeeds.
- the comparison helper returns structured device-pair metadata for current report artifacts.

### Summary
The package now has a clearer expected/actual comparison layer by pairing persisted report artifacts through a dedicated helper rather than leaving compare-review as a purely manual interpretation surface.

---

<a id="version-240"></a>
## Version 2.4.0: Added compare-review workflow and hardened report schema

**Date:** 2026-04-03
**Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e

### Changes
- Hardened persisted report artifacts with explicit `report_schema`, `generated_at`, `plugin_version`, and `result_type` metadata.
- Added `skills/compare-review/SKILL.md` so the package can compare two previously generated capture reports for before/after or regression-style review.
- Updated README and design guidance to expose compare-review as part of the product surface.
- Bumped plugin and marketplace package versions to `2.4.0`.

### Validation
- `python3 -m py_compile screenshot.py` succeeds.
- `python3 screenshot.py https://claw-frontend-dev.nodenetwork.ovh/docs --capture-set responsive --mode viewport --wait --output-format json --report-file /tmp/webview_24_responsive_report.json` succeeds.
- `python3 screenshot.py https://developer.mozilla.org/en-US/docs/Web/JavaScript --device mobile --mode viewport --wait --output-format json --report-file /tmp/webview_24_single_report.json` succeeds.
- the persisted report file now includes `webview-screenshort.capture-report/v1` schema metadata.

### Summary
The package now supports a stronger reusable frontend-review workflow by standardizing report artifacts and adding a compare-review surface for regression-style visual checks.

---

<a id="version-230"></a>
## Version 2.3.0: Added review-skill and report-file workflow surfaces

**Date:** 2026-04-03
**Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e

### Changes
- Added `--report-file` to `screenshot.py` so capture metadata can be persisted to JSON for later reading and chaining.
- Added report-file support for both focused captures and responsive capture sets.
- Added `skills/frontend-review/SKILL.md` as a direct capture-then-review surface.
- Added `skills/responsive-review/SKILL.md` as a direct responsive capture-then-review surface.
- Updated README, design, and screenshot skill guidance so the package now exposes stronger product-facing review entrypoints instead of only lower-level capture primitives.
- Bumped plugin and marketplace package versions to `2.3.0`.

### Validation
- `python3 -m py_compile screenshot.py` succeeds.
- `python3 screenshot.py https://claw-frontend-dev.nodenetwork.ovh/docs --capture-set responsive --mode viewport --wait --output-format json --report-file /tmp/webview_responsive_report.json` succeeds.
- `python3 screenshot.py https://developer.mozilla.org/en-US/docs/Web/JavaScript --device mobile --mode viewport --wait --output-format json --report-file /tmp/webview_single_report.json` succeeds.
- both responsive and focused flows now write re-readable JSON report artifacts.

### Summary
The package now moves one step closer to a true frontend-review product surface by persisting capture metadata and exposing dedicated review skills on top of the screenshot engine.

---

<a id="version-220"></a>
## Version 2.2.0: Added one-run responsive capture-set workflow

**Date:** 2026-04-03
**Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e

### Changes
- Added `--capture-set responsive` to `screenshot.py` so one invocation can produce desktop, tablet, and mobile captures together.
- Added combined JSON result output for responsive capture sets with per-device `captures[]` metadata.
- Added per-device output naming so responsive capture-set runs produce stable desktop/tablet/mobile image paths in one batch.
- Updated skill, workflow, agent, and README guidance so responsive frontend review now prefers one machine-readable responsive run instead of three manual commands.
- Bumped plugin and marketplace package versions to `2.2.0` for install/update visibility.

### Validation
- `python3 -m py_compile screenshot.py` succeeds.
- `python3 screenshot.py https://claw-frontend-dev.nodenetwork.ovh/docs --capture-set responsive --mode viewport --wait --output-format json` succeeds.
- The responsive capture-set run returns 3 successful captures with desktop/tablet/mobile metadata and image paths.

### Summary
The package now reduces responsive-review workflow friction by producing a full desktop/tablet/mobile capture set plus machine-readable metadata in one run.

---

<a id="version-210"></a>
## Version 2.1.0: Normalized public install docs to repo-root marketplace guidance

**Date:** 2026-04-03
**Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e

### Changes
- Reworked `README.md` so the public install path now starts from the standalone repo root instead of the shared `TEMPLATE/PLUGIN` workspace path.
- Reworked cutover/governance wording so the standalone repo is now package authority and shared-workspace usage is treated only as local compatibility context.
- Replaced source-side public install examples with repo-root guidance using:
  - `claude plugins marketplace add ./ --scope local`
  - `claude plugins install webview-screenshort@webview-screenshort --scope local`
- Kept the shared `darkwingtm` marketplace route documented only as a checked local development note rather than the public default install story.
- Added repo-root install validation evidence to the package-level public readiness story.

### Validation
- `claude plugins marketplace add ./ --scope local` succeeds from the repo root.
- `claude plugins install webview-screenshort@webview-screenshort --scope local` succeeds from the repo root.
- `claude agents` shows `webview-screenshort:webview-vision-assist` after repo-root install.

### Summary
The package now treats the standalone repo as its active authority, teaches a portable public install story from that repo root, and keeps the shared `darkwingtm` route only as scoped local compatibility context.

---

<a id="version-200"></a>
## Version 2.0.0: Plugin package and CSR frontend-vision validation

**Date:** 2026-04-03
**Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e

### Changes
- Moved the old project-local skill file into plugin-standard `skills/screenshot/SKILL.md`.
- Added `.claude-plugin/plugin.json` for plugin packaging.
- Added package-local `.claude-plugin/marketplace.json` so this package can later cut over into its own standalone repo-local marketplace root.
- Added `agents/webview-vision-assist.md` as the optional visual-review companion agent.
- Added focused skill workflow files for frontend review.
- Reorganized the package into governed plugin layout with `design/`, `changelog/`, `phase/`, and `patch/` directories.
- Verified screenshot capture against `https://claw-frontend-dev.nodenetwork.ovh/docs` in both viewport and fullpage modes using `--wait`.
- Confirmed that the old hardcoded project-local skill path in `SKILL.md` was stale and replaced it with the current package path.
- Added the package to the shared `darkwingtm` marketplace and verified install plus agent visibility.
- Switched runtime invocation to `${CLAUDE_PLUGIN_ROOT}` for installed-plugin portability.
- Refactored `screenshot.py` to support env-driven endpoints/timeouts and machine-readable JSON result output.
- Added mobile and tablet device presets for responsive frontend review.
- Verified a second frontend docs target (`https://developer.mozilla.org/en-US/docs/Web/JavaScript`) in desktop/mobile/tablet viewport capture with structured JSON output.
- Validated a responsive multi-capture workflow on `https://claw-frontend-dev.nodenetwork.ovh/docs` across desktop, tablet, and mobile presets.
- Verified that the installed package remains visible from a fresh CLI process, closing the current restart-time lifecycle check.

### Summary
The package is now moving from an old project-local screenshot utility toward a governed frontend-vision plugin package with real CSR capture evidence.

---

<a id="version-18"></a>
## Version 1.8: Project-Local Skill Implementation

**Date:** 2026-02-07
**Session:** project-local skill implementation

### Changes
- Created `./.claude/skills/screenshot/SKILL.md`
- Changed from global to project-local path
- Enhanced SKILL.md with examples and default behavior description
- Added `Read` in addition to `Bash` for result reporting

### Summary
Completed the older skill implementation using project-local `.claude/` layout.
