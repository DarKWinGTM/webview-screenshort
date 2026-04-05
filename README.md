# Webview Screenshort

> **Current Version:** 2.35.0

A governed frontend-development screenshot plugin package for capturing real rendered webpages and giving Claude visual plus semantic page evidence during UI, UX, and layout work.

---

## Purpose

This package exists to help frontend development use real page vision instead of source-only guessing.

It is meant for workflows where Claude should:
- capture the real rendered page
- inspect the screenshot as visual evidence
- inspect semantic page witness JSON as structure evidence derived from rendered HTML
- help with layout, spacing, hierarchy, UX, and UI decisions
- verify CSR/SPA rendering before recommending frontend changes

---

## Path notation

- `<repo-root>` = this standalone repo root and the preferred public source-side path for install commands
- `<workspace-root>` = the current local working copy of the same package

## Installation and activation

### Maintained local runtime authority
This package now has its own standalone GitHub repo at:
- `https://github.com/DarKWinGTM/webview-screenshort`

But in this maintained local runtime environment, the install/update authority label stays:
- `webview-screenshort@darkwingtm`

Use this for the normal local runtime lifecycle:

```bash
claude plugins install webview-screenshort@darkwingtm --scope local
claude plugins update webview-screenshort@darkwingtm --scope local
```

Why this exact shape matters:
- `claude plugins update webview-screenshort --scope local` may fail because the installed local plugin is keyed by `plugin@marketplace`
- this environment preserves `@darkwingtm` as the stable runtime authority label for the plugin
- the standalone repo remains the source of truth for code and releases, but not the preferred installed label for this local runtime

Optional reload:

```bash
/reload-plugins
```

Check installed state:

```bash
claude plugins list
claude agents
```

### Repo-local validation path
If you want to validate the standalone repo/package surface directly from the repo root, that package-local marketplace manifest still works as a source-side validation/cutover path:

```bash
git clone https://github.com/DarKWinGTM/webview-screenshort.git
cd webview-screenshort
claude plugins marketplace add ./ --scope local
claude plugins install webview-screenshort@webview-screenshort --scope local
```

Checked local validation from the repo root:
- `claude plugins marketplace add ./ --scope local` succeeds
- `claude plugins install webview-screenshort@webview-screenshort --scope local` succeeds
- `claude agents` shows `webview-screenshort:webview-vision-assist`

## Current status

Verified now:
- screenshot capture works through the package CLI module surface
- CSR-heavy page capture works when `--wait` is used
- viewport and fullpage capture both work
- mobile and tablet viewport presets now work for responsive frontend review
- the package now has plugin scaffolding with `.claude-plugin/`, `skills/`, and `agents/`
- the package validates through its own repo-root marketplace manifest and exposes `webview-screenshort:webview-vision-assist`
- the maintained local runtime authority label in this environment remains `webview-screenshort@darkwingtm`
- skill/agent execution now targets `${CLAUDE_PLUGIN_ROOT}` instead of a source-workspace-only path
- the runtime now has an internal `webview_screenshort/` package so root scripts no longer need to remain the only place where orchestration logic lives
- richer capture output now includes acquisition witness JSON so the package can report how scrape/prerender witnesses were obtained in machine-readable form
- the package CLI screenshot module now supports env-driven capture configuration, JSON result output, schema-stamped persisted report-file output, one-run responsive capture-set output, richer witness modes, optional evidence-bundle output, acquisition witness JSON output, semantic page witness JSON output, and capture-set semantic/acquisition witness indexes for chaining into frontend review workflows
- the package CLI compare module now validates persisted screenshot reports and evidence bundles, emits structured pair metadata, and classifies each compared device as `exact_match`, `visual_change_region`, `dimension_shift`, `size_mismatch`, or `diff_error`
- the package CLI diff module now adds optional image-diff metrics and diff-image outputs for richer compare-review workflows
- the package CLI compare-session module now persists named compare-session artifacts with expected/actual-style labels for later QA review
- the package CLI compare-session listing module now lists and summarizes persisted compare-session artifacts for practical QA history browsing
- the package CLI reference-bundle creation module now builds reusable expected-reference bundle artifacts on top of saved compare sessions, including bundle-based compare sessions sourced from richer evidence bundles
- the package CLI apply-reference module now applies a saved reference bundle to a current report and emits a fresh expected/actual compare session automatically
- the package CLI live replay module now captures a fresh current report from a live URL and replays a saved baseline in one flow
- the package CLI verdict module now turns compare-session, comparison, or live-replay artifacts into machine-readable pass/fail/invalid QA verdicts with mismatch classification summaries
- the package CLI gate module now applies threshold/policy rules on top of verdict artifacts so screenshot QA can produce reusable gate results while preserving mismatch classification summaries
- the package CLI live gate module now captures a live current report, replays a saved baseline, and applies gate policy in one flow
- the package CLI preset-discovery module now lists the built-in gate policy presets that can be selected by name
- the package now ships multiple semantic QA policy presets for smoke, layout, mobile-critical, content-tolerant, and strict responsive review
- policy presets now carry family/name metadata so gate flows can use selectors like `layout/major-shift` in addition to legacy aliases like `layout-major-shift`
- the package CLI reference-bundle listing module now lists and summarizes saved reference bundles for practical baseline browsing
- `skills/reference-bundles/SKILL.md` now exposes bundle lifecycle work through a dedicated front-door skill surface
- `skills/reference-live-review/SKILL.md` now exposes saved-baseline replay against a live URL from one front door
- `skills/frontend-review/SKILL.md` and `skills/responsive-review/SKILL.md` now treat semantic page witness output as part of richer frontend evidence, not only rendered HTML/text
- `skills/qa-verdict/SKILL.md` now exposes a reusable verdict layer for compare/live-replay artifacts
- `skills/qa-gate/SKILL.md` now exposes a threshold-aware gate layer for policy-based QA pass/fail decisions
- `skills/reference-live-gate/SKILL.md` now exposes a one-step saved-baseline + live-URL + gate workflow
- `skills/policy-presets/SKILL.md` now exposes preset discovery so policy names can be chosen without raw path hunting
- reference bundles now carry explicit reference-side/report metadata instead of relying only on implicit left-side session interpretation
- newly created reference bundles now include a bundled reference report payload plus copied baseline images so replay is less fragile if the original temp report disappears
- `compare_reports.py` now treats non-diffable paired comparisons as failed instead of silently reporting success just because device labels matched
- `diff_images.py` now counts non-zero RGBA diff pixels directly so visual differences are measured more honestly when screenshot colors change without alpha changes
- `webview-vision-assist` now routes more clearly between focused review, responsive review, compare review, bundle-lifecycle paths, and live baseline replay paths
- semantic page witness JSON is now emitted from rendered HTML where available, and responsive capture-set output now preserves capture-set semantic/acquisition witness indexes
- the codebase now has internal package domains for compare, QA, references, CLI adapters, and shared schemas instead of keeping those flows only as root-script implementations
- package CLI modules under `webview_screenshort/cli/` now own parser/main behavior and the active programmable command surface, while the retired root wrappers live under `prototype/root-wrappers/` for compatibility reference only
- higher-level review skills preserve an explicit operator-provided `--witness-mode` instead of silently overriding it with a hard-appended default
- generated timestamped files under `screenshot/` are local evidence outputs, not package authority artifacts that should be tracked by default
- `webview_screenshort/workflows.py` no longer imports root scripts directly, so the package boundary is cleaner than before
- auth-context parsing and headless-render-api integration now live under `webview_screenshort/capture/`, while the older `auth_context.py` and `headless_render_api.py` paths remain as compatibility shims
- config/path/witness responsibilities moved out of `capture_service.py` into `webview_screenshort/capture/config.py`, `capture/paths.py`, and `capture/witnesses.py`
- capture models, engines, reporting, and runtime orchestration now also live under `webview_screenshort/capture/`
- key consumers such as package exports, screenshot CLI, and live replay now import through `webview_screenshort/capture/service.py`, which acts as the newer capture authority surface
- `capture_service.py` now remains only as a compatibility facade instead of duplicating the active capture implementation
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
  webview_screenshort/
    __init__.py
    schemas.py
    auth_context.py
    headless_render_api.py
    capture_service.py
    workflows.py
    capture/
      __init__.py
      auth.py
      headless_api.py
      config.py
      paths.py
      witnesses.py
      models.py
      engines.py
      reporting.py
      runtime.py
      service.py
    compare/
      __init__.py
      diffing.py
      reports.py
      sessions.py
      listings.py
    qa/
      __init__.py
      policies.py
      verdicts.py
      gate.py
    references/
      __init__.py
      bundles.py
      live.py
    cli/
      __init__.py
      screenshot.py
      compare_reports.py
      diff_images.py
      compare_session.py
      create_reference_bundle.py
      apply_reference_bundle.py
      qa_verdict.py
      qa_gate.py
      reference_live_bundle.py
      reference_live_gate.py
      list_compare_sessions.py
      list_reference_bundles.py
      list_policy_presets.py
  prototype/
    policy_presets.py
    root-wrappers/
      screenshot.py
      compare_reports.py
      diff_images.py
      compare_session.py
      create_reference_bundle.py
      apply_reference_bundle.py
      qa_verdict.py
      qa_gate.py
      reference_live_bundle.py
      reference_live_gate.py
      list_compare_sessions.py
      list_reference_bundles.py
      list_policy_presets.py
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

### Command contract
The active programmable command surface is now the package CLI module layer:
- `PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" python3 -m webview_screenshort.cli.screenshot ...`
- `PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" python3 -m webview_screenshort.cli.compare_reports ...`
- `PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" python3 -m webview_screenshort.cli.qa_gate ...`

Why this matters:
- the package CLI module layer is now the intended stable execution surface
- the older root wrapper scripts have been removed from the active root structure and moved under `prototype/root-wrappers/` for retirement/compatibility reference only

It should let Claude:
1. capture a page
2. return the local screenshot path
3. optionally emit rendered HTML and rendered text witnesses when the selected witness mode requires them
4. optionally emit semantic page witness JSON when rendered HTML is available
5. optionally emit an evidence bundle artifact for richer workflows
6. continue analysis from real rendered evidence instead of source-only guessing

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
- semantic page witness is currently a lightweight HTML-derived summary and does not yet model deeper DOM semantics or visual salience
- `capture/auth.py` and `capture/headless_api.py` now own those domains directly, config/path/witness extraction is in place, and `capture.service` is the active authority surface, while `capture_service.py` remains only as a legacy compatibility facade for older imports
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
3. if richer witnesses were emitted, read rendered HTML / rendered text and semantic page witness JSON too
4. analyze the visible layout/UI and rendered content together
5. use semantic page witness to understand title/headings/links/forms/page-shape faster before dropping into raw HTML
6. only then suggest code or design changes

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
- semantic page witness output is especially useful here for spotting missing headings/nav/forms/content-shape changes without re-reading full raw HTML first
- compare/verdict/gate artifacts now preserve semantic companion classifications so this structure drift can remain machine-readable downstream

### For reusable QA verdict output
- `/qa-verdict /path/to/compare-session-or-live-replay.json --output-format json`
- use this surface when compare/live-replay artifacts should end in a reusable per-device verdict instead of raw pair metadata only
- the verdict layer now returns overall `pass` / `fail` / `invalid` state plus per-device reasons, match/mismatch lists, grouped visual mismatch classifications, and grouped semantic companion classifications

### For threshold-aware QA gate output
- `/qa-gate /path/to/compare-session-or-live-replay.json --policy-preset strict-responsive-zero-diff --output-format json`
- use this surface when verdict artifacts should be checked against explicit acceptance rules rather than only summarized
- the gate layer now returns overall gate status, violated rules, missing required devices, per-device gate results, propagated visual mismatch classifications, and propagated semantic companion classifications
- built-in semantic gate policy keys such as `fail_on_semantic_missing`, `fail_on_semantic_structure_change`, `fail_on_semantic_content_change`, `fail_on_semantic_any_change`, `fail_on_title_change`, `fail_on_missing_headings`, `fail_on_structure_flags_change`, `fail_on_missing_links`, `fail_on_missing_buttons`, `fail_on_form_count_change`, and `fail_on_missing_inputs` can now participate in policy evaluation

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
