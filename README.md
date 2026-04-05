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
- the runtime now has an internal `webview_screenshort/` package so root scripts no longer need to remain the only place where orchestration logic lives
- richer capture output now includes acquisition witness JSON so the package can report how scrape/prerender witnesses were obtained in machine-readable form
- `screenshot.py` now supports env-driven capture configuration, JSON result output, schema-stamped persisted report-file output, one-run responsive capture-set output, richer witness modes, optional evidence-bundle output, and acquisition witness JSON output for chaining into frontend review workflows
- `compare_reports.py` now validates persisted screenshot reports and evidence bundles, emits structured pair metadata, and classifies each compared device as `exact_match`, `visual_change_region`, `dimension_shift`, `size_mismatch`, or `diff_error`
- `diff_images.py` now adds optional image-diff metrics and diff-image outputs for richer compare-review workflows
- `compare_session.py` now persists named compare-session artifacts with expected/actual-style labels for later QA review
- `list_compare_sessions.py` now lists and summarizes persisted compare-session artifacts for practical QA history browsing
- `create_reference_bundle.py` now builds reusable expected-reference bundle artifacts on top of saved compare sessions, including bundle-based compare sessions sourced from richer evidence bundles
- `apply_reference_bundle.py` now applies a saved reference bundle to a current report and emits a fresh expected/actual compare session automatically
- `reference_live_bundle.py` now captures a fresh current report from a live URL and replays a saved baseline in one flow
- `qa_verdict.py` now turns compare-session, comparison, or live-replay artifacts into machine-readable pass/fail/invalid QA verdicts with mismatch classification summaries
- `qa_gate.py` now applies threshold/policy rules on top of verdict artifacts so screenshot QA can produce reusable gate results while preserving mismatch classification summaries
- `reference_live_gate.py` now captures a live current report, replays a saved baseline, and applies gate policy in one flow
- `list_policy_presets.py` now lists the built-in gate policy presets that can be selected by name
- the package now ships multiple semantic QA policy presets for smoke, layout, mobile-critical, content-tolerant, and strict responsive review
- policy presets now carry family/name metadata so gate flows can use selectors like `layout/major-shift` in addition to legacy aliases like `layout-major-shift`
- `list_reference_bundles.py` now lists and summarizes saved reference bundles for practical baseline browsing
- `skills/reference-bundles/SKILL.md` now exposes bundle lifecycle work through a dedicated front-door skill surface
- `skills/reference-live-review/SKILL.md` now exposes saved-baseline replay against a live URL from one front door
- `skills/qa-verdict/SKILL.md` now exposes a reusable verdict layer for compare/live-replay artifacts
- `skills/qa-gate/SKILL.md` now exposes a threshold-aware gate layer for policy-based QA pass/fail decisions
- `skills/reference-live-gate/SKILL.md` now exposes a one-step saved-baseline + live-URL + gate workflow
- `skills/policy-presets/SKILL.md` now exposes preset discovery so policy names can be chosen without raw path hunting
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
    reference-live-gate/
      SKILL.md
    policy-presets/
      SKILL.md
  screenshot.py
  compare_reports.py
  qa_verdict.py
  qa_gate.py
  reference_live_gate.py
  webview_screenshort/
    __init__.py
    auth_context.py
    headless_render_api.py
    capture_service.py
    workflows.py
  list_policy_presets.py
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
The main runtime path should still be the screenshot skill, but it should now behave like a frontend-evidence front door rather than a screenshot-only command.

It should let Claude:
1. capture a page
2. return the local screenshot path
3. optionally emit rendered HTML and rendered text witnesses when the selected witness mode requires them
4. optionally emit an evidence bundle artifact for richer workflows
5. continue analysis from real rendered evidence instead of source-only guessing

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
- compare/verdict/gate workflows are still screenshot-era first-class flows and need broader bundle-aware continuity review
- logged-in-state capture is operator-provided only; the package replays existing session context and does not automate interactive login
- metadata/acquisition witnesses are provider-bounded truth only; they are not full browser console or network tracing
- headless-render-api documentation supports origin forwarding only through `Prerendercloud-*` header names plus `Origin-Header-Whitelist`, so authenticated capture needs a bounded forwarding contract rather than assuming arbitrary header pass-through to origin
- broader CSR validation still needs more than the two currently checked public docs targets
- public-repo wording polish is still in progress outside the now-validated repo-root install path

---

## Recommended usage model

### For focused capture
- `/screenshot <url> --wait --mode viewport`
- `/screenshot <url> --wait --mode fullpage`
- `/screenshot <url> --wait --mode viewport --witness-mode frontend-default --output-format json --report-file /tmp/capture.json`
- `/screenshot <url> --wait --mode viewport --witness-mode csr-debug --bundle-file /tmp/evidence.json --output-format json`
- `/screenshot <url> --capture-set responsive --wait --mode viewport --witness-mode responsive --output-format json`

### For frontend review
- `/frontend-review <url> --wait --mode viewport`
1. capture first
2. read the screenshot
3. if richer witnesses were emitted, read rendered HTML / rendered text too
4. analyze the visible layout/UI and rendered content together
5. only then suggest code or design changes

### For responsive frontend review
- `/responsive-review <url> --wait --mode viewport`

### For before/after or regression review
- `/compare-review /path/to/report-a.json /path/to/report-b.json`
- compare two `webview-screenshort.capture-report/v1` artifacts and inspect the paired screenshots
- use diff-assisted compare flow when you want image-diff metrics, generated diff images, and pair-level mismatch classifications in addition to pair metadata
- persist a named compare session when QA work should be saved as an expected/actual or before/after artifact

### For bundle lifecycle work
- `/reference-bundles list /path/to/bundles`
- `/reference-bundles create /path/to/compare-session.json bundle-name /path/to/bundle.json`
- `/reference-bundles apply /path/to/bundle.json /path/to/current-report.json session-name /path/to/comparison.json /path/to/session.json`
- optional diff enrichment now flows through `--diff-dir` on the helper layer when compare images should also be written during baseline replay
- use this surface when saved QA artifacts should be browsed, turned into reusable baselines, or replayed against fresh actual reports
- browse saved reference bundles when baseline assets should be reused without remembering exact paths

### For saved baseline replay against a live URL
- `/reference-live-review --bundle /path/to/bundle.json --url https://example.com/page --current-report /tmp/current.json --comparison-json /tmp/compare.json --session-output /tmp/session.json --session-name current-vs-expected --capture-set responsive --mode viewport --wait --witness-mode responsive --diff-dir /tmp/diffs`
- use this surface when the baseline already exists but the current live page still needs to be captured first
- the flow now captures a fresh current report, applies the bundle automatically, and emits a new expected/actual compare session in one run
- when richer witnesses were emitted for the fresh live capture, they should be inspected before deciding whether the baseline drift is visual-only or also semantic/CSR-related

### For reusable QA verdict output
- `/qa-verdict /path/to/compare-session-or-live-replay.json --output-format json`
- use this surface when compare/live-replay artifacts should end in a reusable per-device verdict instead of raw pair metadata only
- the verdict layer now returns overall `pass` / `fail` / `invalid` state plus per-device reasons, match/mismatch lists, and grouped mismatch classifications

### For threshold-aware QA gate output
- `/qa-gate /path/to/compare-session-or-live-replay.json --policy-preset strict-responsive-zero-diff --output-format json`
- use this surface when verdict artifacts should be checked against explicit acceptance rules rather than only summarized
- the gate layer now returns overall gate status, violated rules, missing required devices, per-device gate results, and propagated mismatch classifications

### For built-in policy preset discovery
- `/policy-presets --output-format json`
- use this surface when you want to discover reusable built-in policy names before running `/qa-gate` or `/reference-live-gate`
- preset-name selection now lets QA flows avoid raw `support/policies/*.json` path hunting in normal usage
- current semantic presets include:
  - `strict/responsive-zero-diff`
  - `smoke/responsive`
  - `layout/major-shift`
  - `mobile/critical`
  - `content/tolerant`
- legacy alias names such as `strict-responsive-zero-diff` and `layout-major-shift` still work for compatibility

### For one-step saved baseline gate against a live URL
- `/reference-live-gate --bundle /path/to/bundle.json --url https://example.com/page --current-report /tmp/current.json --comparison-json /tmp/compare.json --session-output /tmp/session.json --session-name current-vs-expected --gate-output /tmp/gate.json --policy-preset strict/responsive-zero-diff --capture-set responsive --mode viewport --wait --witness-mode responsive --diff-dir /tmp/diffs`
- use this surface when the whole flow should finish in one run: capture current state, replay saved baseline, and apply policy gate
- the package now includes a reusable strict responsive zero-diff preset under `support/policies/strict-responsive-zero-diff.json`
- authenticated pages can also be captured in this flow when the operator provides headers/cookies/session material explicitly

Or manually:
1. capture one responsive set with `--capture-set responsive --output-format json`
2. read the combined JSON result plus each generated image from `captures[].output_path`
3. compare hierarchy, overflow, spacing, stacking, and readability across breakpoints
4. summarize which issues are desktop-only, tablet-only, mobile-only, or cross-device
