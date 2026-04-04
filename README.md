# Webview Screenshort

A governed frontend-development screenshot plugin package for capturing real rendered webpages and giving Claude visual evidence during UI, UX, and layout work.

---

## Purpose

This package exists to help frontend development use real page vision instead of source-only guessing.

It is meant for workflows where Claude should:
- capture the real rendered page
- inspect the screenshot as visual evidence
- help with layout, spacing, hierarchy, UX, and UI decisions
- verify CSR/SPA rendering before recommending frontend changes

---

## Path notation

- `<repo-root>` = this standalone repo root and the preferred public source-side path for install commands
- `<workspace-root>` = the current local working copy of the same package

## Installation and activation

### Recommended public install path
This package now has its own standalone GitHub repo at:
- `https://github.com/DarKWinGTM/webview-screenshort`

Clone once, then run the install from the repo root:

```bash
git clone https://github.com/DarKWinGTM/webview-screenshort.git
cd webview-screenshort
claude plugins marketplace add ./ --scope local
claude plugins install webview-screenshort@webview-screenshort --scope local
```

Optional reload:

```bash
/reload-plugins
```

Check installed state:

```bash
claude plugins list
claude agents
```

Checked local validation from the repo root:
- `claude plugins marketplace add ./ --scope local` succeeds
- `claude plugins install webview-screenshort@webview-screenshort --scope local` succeeds
- `claude agents` shows `webview-screenshort:webview-vision-assist`

### Update an installed plugin

If the plugin was installed from this standalone repo-local marketplace, update it by using the installed identifier shape `plugin@marketplace`:

```bash
claude plugins update webview-screenshort@webview-screenshort --scope local
```

If you still have an older local install through the shared compatibility marketplace, the installed identifier may instead be `webview-screenshort@darkwingtm`:

```bash
claude plugins update webview-screenshort@darkwingtm --scope local
```

Why this exact shape matters:
- `claude plugins update webview-screenshort --scope local` may fail because the installed local plugin is keyed by `plugin@marketplace`
- the explicit `plugin@marketplace` form matches the installed identifier shown in `claude plugins list`

### Local development compatibility note

The same package may still be referenced through the shared local `darkwingtm` marketplace during workspace development, but that route is no longer package authority. The standalone repo is now the intended source of truth, and any remaining shared-workspace usage should be treated as temporary local compatibility only.

## Current status

Verified now:
- `screenshot.py` captures live webpages successfully
- CSR-heavy page capture works when `--wait` is used
- viewport and fullpage capture both work
- mobile and tablet viewport presets now work for responsive frontend review
- the package now has plugin scaffolding with `.claude-plugin/`, `skills/`, and `agents/`
- the package installs through its own repo-root marketplace manifest and exposes `webview-screenshort:webview-vision-assist`
- skill/agent execution now targets `${CLAUDE_PLUGIN_ROOT}` instead of a source-workspace-only path
- `screenshot.py` now supports env-driven capture configuration, JSON result output, schema-stamped persisted report-file output, and one-run responsive capture-set output for chaining into frontend review workflows
- `compare_reports.py` now validates persisted reports and emits structured pair metadata for report-to-report comparison workflows
- `diff_images.py` now adds optional image-diff metrics and diff-image outputs for richer compare-review workflows
- `compare_session.py` now persists named compare-session artifacts with expected/actual-style labels for later QA review
- `list_compare_sessions.py` now lists and summarizes persisted compare-session artifacts for practical QA history browsing
- `create_reference_bundle.py` now builds reusable expected-reference bundle artifacts on top of saved compare sessions
- `apply_reference_bundle.py` now applies a saved reference bundle to a current report and emits a fresh expected/actual compare session automatically
- `reference_live_bundle.py` now captures a fresh current report from a live URL and replays a saved baseline in one flow
- `qa_verdict.py` now turns compare-session, comparison, or live-replay artifacts into machine-readable pass/fail/invalid QA verdicts
- `qa_gate.py` now applies threshold/policy rules on top of verdict artifacts so screenshot QA can produce reusable gate results
- `list_reference_bundles.py` now lists and summarizes saved reference bundles for practical baseline browsing
- `skills/reference-bundles/SKILL.md` now exposes bundle lifecycle work through a dedicated front-door skill surface
- `skills/reference-live-review/SKILL.md` now exposes saved-baseline replay against a live URL from one front door
- `skills/qa-verdict/SKILL.md` now exposes a reusable verdict layer for compare/live-replay artifacts
- `skills/qa-gate/SKILL.md` now exposes a threshold-aware gate layer for policy-based QA pass/fail decisions
- reference bundles now carry explicit reference-side/report metadata instead of relying only on implicit left-side session interpretation
- newly created reference bundles now include a bundled reference report payload plus copied baseline images so replay is less fragile if the original temp report disappears
- `compare_reports.py` now treats non-diffable paired comparisons as failed instead of silently reporting success just because device labels matched
- `diff_images.py` now counts non-zero RGBA diff pixels directly so visual differences are measured more honestly when screenshot colors change without alpha changes
- `webview-vision-assist` now routes more clearly between focused review, responsive review, compare review, bundle-lifecycle paths, and live baseline replay paths
- public-repo install posture is now validated from the standalone repo root

Checked live examples:
- `https://claw-frontend-dev.nodenetwork.ovh/docs`
  - viewport + wait capture succeeded
  - fullpage + wait capture succeeded
  - one-run responsive capture-set + wait succeeded
- `https://developer.mozilla.org/en-US/docs/Web/JavaScript`
  - viewport + wait capture succeeded
  - mobile preset + wait capture succeeded
  - tablet preset + wait capture succeeded

---

## Plugin surfaces

```text
webview-screenshort/
  README.md
  TODO.md
  .claude-plugin/
    plugin.json
  agents/
    webview-vision-assist.md
  skills/
    screenshot/
      SKILL.md
      overview.md
      frontend-review.md
    frontend-review/
      SKILL.md
    responsive-review/
      SKILL.md
    compare-review/
      SKILL.md
    reference-bundles/
      SKILL.md
    reference-live-review/
      SKILL.md
    qa-verdict/
      SKILL.md
    qa-gate/
      SKILL.md
  screenshot.py
  compare_reports.py
  qa_verdict.py
  qa_gate.py
  diff_images.py
  compare_session.py
  list_compare_sessions.py
  create_reference_bundle.py
  apply_reference_bundle.py
  reference_live_bundle.py
  list_reference_bundles.py
  screenshot/
  design/
    design.md
  changelog/
    changelog.md
  phase/
  patch/
```

---

## What this package should do

### Skill role
The main runtime path should be the screenshot skill.

It should let Claude:
1. capture a page
2. return the local image path
3. read the screenshot image
4. continue visual analysis from real evidence

### Agent role
The companion agent should help when the user wants a visual frontend-review workflow rather than only a one-shot slash command.

---

## Frontend-development use cases

Use this package when the goal is to inspect:
- actual layout balance
- spacing and visual hierarchy
- docs page readability
- dashboard structure
- rendered component density
- CSR / hydration state
- whether a frontend change improved or harmed the visible page

---

## Current limitations

- restart/reload lifecycle is now validated for the current installed package path
- visual analysis orchestration still depends on Claude reading the generated image after capture, even though responsive desktop/tablet/mobile capture can now be produced in one machine-readable run
- broader CSR validation still needs more than the two currently checked public docs targets
- public-repo wording polish is still in progress outside the now-validated repo-root install path

---

## Recommended usage model

### For focused capture
- `/screenshot <url> --wait --mode viewport`
- `/screenshot <url> --wait --mode fullpage`
- `/screenshot <url> --capture-set responsive --wait --mode viewport --output-format json`
- `/screenshot <url> --wait --mode viewport --output-format json --report-file /tmp/capture.json`

### For frontend review
- `/frontend-review <url> --wait --mode viewport`
1. capture first
2. read the image
3. analyze the visible layout/UI from the screenshot
4. only then suggest code or design changes

### For responsive frontend review
- `/responsive-review <url> --wait --mode viewport`

### For before/after or regression review
- `/compare-review /path/to/report-a.json /path/to/report-b.json`
- compare two `webview-screenshort.capture-report/v1` artifacts and inspect the paired screenshots
- use diff-assisted compare flow when you want image-diff metrics and generated diff images in addition to pair metadata
- persist a named compare session when QA work should be saved as an expected/actual or before/after artifact

### For bundle lifecycle work
- `/reference-bundles list /path/to/bundles`
- `/reference-bundles create /path/to/compare-session.json bundle-name /path/to/bundle.json`
- `/reference-bundles apply /path/to/bundle.json /path/to/current-report.json session-name /path/to/comparison.json /path/to/session.json`
- optional diff enrichment now flows through `--diff-dir` on the helper layer when compare images should also be written during baseline replay
- use this surface when saved QA artifacts should be browsed, turned into reusable baselines, or replayed against fresh actual reports
- browse saved reference bundles when baseline assets should be reused without remembering exact paths

### For saved baseline replay against a live URL
- `/reference-live-review --bundle /path/to/bundle.json --url https://example.com/page --current-report /tmp/current.json --comparison-json /tmp/compare.json --session-output /tmp/session.json --session-name current-vs-expected --capture-set responsive --mode viewport --wait --diff-dir /tmp/diffs`
- use this surface when the baseline already exists but the current live page still needs to be captured first
- the flow now captures a fresh current report, applies the bundle automatically, and emits a new expected/actual compare session in one run

### For reusable QA verdict output
- `/qa-verdict /path/to/compare-session-or-live-replay.json --output-format json`
- use this surface when compare/live-replay artifacts should end in a reusable per-device verdict instead of raw pair metadata only
- the verdict layer now returns overall `pass` / `fail` / `invalid` state plus per-device reasons and match/mismatch lists

### For threshold-aware QA gate output
- `/qa-gate /path/to/compare-session-or-live-replay.json --require-device desktop --require-device tablet --require-device mobile --fail-on-invalid true --max-diff-ratio 0 --output-format json`
- use this surface when verdict artifacts should be checked against explicit acceptance rules rather than only summarized
- the gate layer now returns overall gate status, violated rules, missing required devices, and per-device gate results

Or manually:
1. capture one responsive set with `--capture-set responsive --output-format json`
2. read the combined JSON result plus each generated image from `captures[].output_path`
3. compare hierarchy, overflow, spacing, stacking, and readability across breakpoints
4. summarize which issues are desktop-only, tablet-only, mobile-only, or cross-device
