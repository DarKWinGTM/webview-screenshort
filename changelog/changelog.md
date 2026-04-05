# Changelog - Webview Screenshort

> **Parent Document:** [../design/design.md](../design/design.md)
> **Current Version:** 2.22.0
> **Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e

---

## Version History (Unified)

| Version | Date | Changes | Summary |
|---------|------|---------|---------|
| 2.22.0 | 2026-04-05 | **[Started frontend-vision evidence bundle upgrade](#version-2220)** | Started the strategic refactor toward an internal runtime package, richer witness modes, rendered HTML/rendered text evidence bundles, and bounded session-replay capture. |
| 2.21.0 | 2026-04-04 | **[Added mismatch classifications](#version-2210)** | Added machine-readable mismatch classifications across compare, verdict, and gate artifacts, and fixed RGB-only diff detection so visible changes are no longer missed. |
| 2.20.0 | 2026-04-04 | **[Added named policy families](#version-2200)** | Added family/name metadata and canonical selectors so policy presets can be grouped and selected as structured names like `layout/major-shift`. |
| 2.19.0 | 2026-04-04 | **[Added semantic QA policy presets](#version-2190)** | Added multiple intent-shaped built-in policy presets so gate flows can choose smoke, layout, mobile-critical, content-tolerant, or strict behavior by name. |
| 2.18.0 | 2026-04-04 | **[Added named policy preset UX](#version-2180)** | Added preset discovery and `--policy-preset` support so gate flows can select built-in QA policies by name instead of raw path. |
| 2.17.0 | 2026-04-04 | **[Added one-step baseline gate workflow](#version-2170)** | Added `reference_live_gate.py`, a dedicated one-step gate skill, and a reusable strict policy preset so saved baselines can be replayed and gated in one run. |
| 2.16.0 | 2026-04-04 | **[Added threshold-aware QA gate layer](#version-2160)** | Added `qa_gate.py` and a dedicated gate skill so verdict artifacts can be checked against explicit policy rules instead of only summarized. |
| 2.15.0 | 2026-04-04 | **[Added automated QA verdict layer](#version-2150)** | Added `qa_verdict.py` and a dedicated verdict skill so compare/live-replay artifacts can end in reusable per-device pass/fail output instead of raw pair metadata only. |
| 2.14.1 | 2026-04-04 | **[Fixed authority/update drift after 2.14.0](#version-2141)** | Corrected the remaining install/update/doc authority drift so repo-local marketplace posture and compatibility-only `darkwingtm` wording now align cleanly. |
| 2.14.0 | 2026-04-04 | **[Added live baseline replay workflow](#version-2140)** | Added `reference_live_bundle.py`, exposed live baseline replay from a dedicated skill surface, and made saved reference bundles easier to re-run directly against current live pages. |
| 2.13.0 | 2026-04-04 | **[Added bundle-lifecycle skill surface](#version-2130)** | Added `skills/reference-bundles/SKILL.md`, lifted bundle helpers into a clearer front-door workflow surface, and made baseline artifact lifecycle operations easier to invoke directly. |
| 2.12.0 | 2026-04-04 | **[Added reference-bundle browsing](#version-2120)** | Added `list_reference_bundles.py`, introduced lightweight browsing of saved baseline bundles, and pushed the compare workflow closer to a practical reusable QA asset system. |
| 2.11.0 | 2026-04-04 | **[Added apply-reference workflow](#version-2110)** | Added `apply_reference_bundle.py`, introduced a way to replay expected/actual QA against saved reference bundles, and pushed the compare workflow closer to a reusable baseline-application system. |
| 2.10.0 | 2026-04-04 | **[Added expected-reference bundles](#version-2100)** | Added `create_reference_bundle.py`, introduced reusable expected-reference bundle artifacts, and pushed the compare workflow closer to a reusable baseline-driven QA system. |
| 2.9.0 | 2026-04-04 | **[Added compare-session history browsing](#version-290)** | Added `list_compare_sessions.py`, introduced a reusable compare-session index/history surface, and pushed compare-review closer to a practical QA archive workflow. |
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

<a id="version-2220"></a>
## Version 2.22.0: Started frontend-vision evidence bundle upgrade

**Date:** 2026-04-05
**Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e

### Changes
- Added an internal `webview_screenshort/` runtime package so capture/auth/provider/workflow logic can move out of pure top-level script sprawl.
- Refactored `screenshot.py` into a thinner wrapper that now supports richer witness modes (`visual`, `frontend-default`, `csr-debug`, `responsive`, `session-replay`).
- Added rendered HTML / rendered text witness generation plus `webview-screenshort.evidence-bundle/v1` output alongside the existing screenshot-era report model.
- Added bounded session-replay capture inputs (`--header`, `--origin-header`, `--cookie`, `--cookie-file`) with redacted auth summaries in persisted capture outputs.
- Refactored `reference_live_bundle.py` and `reference_live_gate.py` to route through reusable internal workflow helpers.
- Extended `compare_reports.py` so bundle-aware compare flows can accept `webview-screenshort.evidence-bundle/v1` artifacts in addition to screenshot-era reports.
- Extended `create_reference_bundle.py` so bundle-based compare sessions can become reusable reference bundles while preserving the reference artifact schema.
- Updated screenshot, frontend-review, reference-live-review, README, design, TODO, phase, and patch docs so the product now reads as screenshot-first but HTML-aware frontend vision instead of screenshot-only review.
- Bumped plugin and marketplace package versions to `2.22.0`.

### Validation
- `python3 -m py_compile screenshot.py compare_reports.py compare_session.py create_reference_bundle.py apply_reference_bundle.py reference_live_bundle.py reference_live_gate.py qa_verdict.py qa_gate.py policy_presets.py webview_screenshort/__init__.py webview_screenshort/auth_context.py webview_screenshort/headless_render_api.py webview_screenshort/capture_service.py webview_screenshort/workflows.py` succeeds.
- `python3 screenshot.py https://example.com --engine headless --mode viewport --witness-mode frontend-default --output-format json --report-file /tmp/webview_v222_report.json` succeeds and emits rendered HTML / rendered text witness paths.
- `python3 screenshot.py https://example.com --engine headless --mode viewport --witness-mode session-replay --header "Authorization: Bearer secret-token-value" --origin-header "Prerendercloud-Debug-User: alice" --cookie "sessionid=supersecret" --output-format json --report-file /tmp/webview_v222_auth_report.json` succeeds and persists only redacted session-replay summaries.
- `python3 screenshot.py https://example.com --engine headless --mode viewport --witness-mode csr-debug --output-format json --report-file /tmp/webview_v222_csr_report.json` succeeds and emits prerender HTML witness output.
- `claude plugins validate .` succeeds from the repo root after the metadata/runtime updates.
- `python3 reference_live_bundle.py ...` succeeds with richer witness output in the live capture payload.
- `python3 reference_live_gate.py ...` succeeds with default policy and emits a passing gate result while preserving richer live capture witnesses.
- `python3 compare_reports.py <evidence-bundle> <evidence-bundle> --output-format json` succeeds and reports `left_result_type = right_result_type = evidence_bundle`.
- `python3 create_reference_bundle.py --session <bundle-based-compare-session> ...` succeeds and preserves `reference_artifact_schema = webview-screenshort.evidence-bundle/v1`.

### Summary
The package has now started the strategic shift from a screenshot utility into a richer frontend-vision runtime that can emit screenshot plus rendered-page witnesses and prepare for authenticated page inspection without crossing into interactive login automation.

---

<a id="version-2210"></a>
## Version 2.21.0: Added mismatch classifications

**Date:** 2026-04-04
**Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e

### Changes
- Added per-pair mismatch classification fields (`classification`, `classification_reason`) plus grouped `classification_summary` output to `compare_reports.py`.
- Added classification-aware verdict output in `qa_verdict.py`, including grouped `mismatch_classification_summary` for downstream QA reuse.
- Added classification-aware gate output in `qa_gate.py` so threshold decisions preserve grouped mismatch context instead of collapsing everything into rule violations only.
- Fixed `diff_images.py` so RGB-only changes are detected via a visible difference mask even when RGBA bbox truthiness would otherwise hide them.
- Updated README, design, TODO, phase, patch, and skill wording so mismatch classifications are now part of the visible product contract.
- Bumped plugin and marketplace package versions to `2.21.0`.

### Validation
- `python3 -m py_compile diff_images.py compare_reports.py qa_verdict.py qa_gate.py` succeeds.
- `python3 compare_reports.py /tmp/webview_24_responsive_report.json /tmp/webview_gate_preset_current_report.json --output-format json --diff-dir /tmp/webview_mismatch_diffs` succeeds and emits `classification_summary`.
- `python3 qa_verdict.py /tmp/webview_gate_preset_session.json --output-format json` succeeds and emits classification-aware pass output.
- `python3 compare_reports.py /tmp/webview_24_single_report.json /tmp/webview_gate_preset_current_report_mobile.json --output-format json --diff-dir /tmp/webview_mismatch_mobile_diffs` succeeds and emits `visual_change_region`.
- `python3 qa_verdict.py /tmp/webview_mismatch_mobile_compare.json --output-format json` succeeds and emits `mismatch_classification_summary`.
- `python3 qa_gate.py /tmp/webview_mismatch_mobile_compare.json --policy-preset strict/responsive-zero-diff --output-format json` fails as expected with classification-aware gate output.
- `python3 qa_verdict.py /tmp/webview_empty_compare.json --output-format json` fails as expected with `overall_verdict = invalid` when comparison input contains no comparable pairs.

### Summary
The package now explains screenshot QA mismatches in machine-readable terms, so downstream review and automation can distinguish visible changes, size problems, dimension shifts, and diff failures instead of only seeing pass/fail state.

---

<a id="version-2200"></a>
## Version 2.20.0: Added named policy families

**Date:** 2026-04-04
**Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e

### Changes
- Added family-aware preset metadata (`family`, `name`, `selector`, `aliases`) across the built-in semantic QA policy presets.
- Updated preset discovery and gate selection so flows can use canonical selectors like `strict/responsive-zero-diff` and `layout/major-shift`, while preserving legacy alias compatibility.
- Updated README, design, TODO, and skill wording so policy presets are now grouped and explained as named families rather than a flat list only.
- Bumped plugin and marketplace package versions to `2.20.0`.

### Validation
- `python3 list_policy_presets.py --output-format json` succeeds and returns `family`, `name`, `selector`, and `aliases` for each built-in preset.
- `python3 qa_gate.py /tmp/webview_gate_preset_session.json --policy-preset strict/responsive-zero-diff --output-format json` succeeds.
- `python3 qa_gate.py /tmp/webview_gate_preset_session.json --policy-preset smoke-responsive --output-format json` succeeds through the legacy alias path.
- `python3 reference_live_gate.py --bundle /tmp/webview_reference_bundles/nodeclaw-docs-reference-v3.json --url https://claw-frontend-dev.nodenetwork.ovh/docs --current-report /tmp/webview_family_current_report.json --comparison-json /tmp/webview_family_compare.json --session-output /tmp/webview_family_session.json --session-name nodeclaw-docs-family-gate --gate-output /tmp/webview_family_gate.json --policy-preset layout/major-shift --capture-set responsive --mode viewport --wait --diff-dir /tmp/webview_family_diffs` succeeds.

### Summary
The package now gives policy presets a clearer scalable structure, so QA flows can select grouped canonical family/name presets while still accepting legacy alias names.

---

<a id="version-2190"></a>
## Version 2.19.0: Added semantic QA policy presets

**Date:** 2026-04-04
**Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e

### Changes
- Added semantic built-in policy presets: `smoke-responsive`, `layout-major-shift`, `mobile-critical`, and `content-tolerant` on top of the existing strict preset.
- Extended preset discovery so the package now exposes a more meaningful preset set for common QA intents instead of one strict preset only.
- Updated README, design, TODO, and preset-discovery wording so policy choice can follow QA intent more naturally.
- Bumped plugin and marketplace package versions to `2.19.0`.

### Validation
- `python3 list_policy_presets.py --output-format json` succeeds and returns the expanded semantic preset set.
- `python3 qa_gate.py /tmp/webview_gate_preset_session.json --policy-preset smoke-responsive --output-format json` succeeds.
- `python3 reference_live_gate.py --bundle /tmp/webview_reference_bundles/nodeclaw-docs-reference-v3.json --url https://claw-frontend-dev.nodenetwork.ovh/docs --current-report /tmp/webview_semantic_current_report.json --comparison-json /tmp/webview_semantic_compare.json --session-output /tmp/webview_semantic_session.json --session-name nodeclaw-docs-semantic-gate --gate-output /tmp/webview_semantic_gate.json --policy-preset layout-major-shift --capture-set responsive --mode viewport --wait --diff-dir /tmp/webview_semantic_diffs` succeeds.

### Summary
The package now exposes a more usable semantic preset set, so QA policy selection can follow the intent of the review instead of depending only on one strict preset or raw threshold values.

---

<a id="version-2180"></a>
## Version 2.18.0: Added named policy preset UX

**Date:** 2026-04-04
**Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e

### Changes
- Added `list_policy_presets.py` so built-in QA policy presets can be discovered directly.
- Added `skills/policy-presets/SKILL.md` so preset discovery has a dedicated front-door skill surface.
- Added `--policy-preset` support to `qa_gate.py` and `reference_live_gate.py` so built-in policies can be selected by name instead of raw file path.
- Updated README, design, TODO, and agent workflow wording so preset discovery and preset-name selection are part of the visible product surface.
- Bumped plugin and marketplace package versions to `2.18.0`.

### Validation
- `python3 list_policy_presets.py --output-format json` succeeds and returns the built-in preset list.
- `python3 qa_gate.py /tmp/webview_gate_preset_session.json --policy-preset strict-responsive-zero-diff --output-format json` succeeds.
- `python3 reference_live_gate.py --bundle /tmp/webview_reference_bundles/nodeclaw-docs-reference-v3.json --url https://claw-frontend-dev.nodenetwork.ovh/docs --current-report /tmp/webview_gate_preset2_current_report.json --comparison-json /tmp/webview_gate_preset2_compare.json --session-output /tmp/webview_gate_preset2_session.json --session-name nodeclaw-docs-live-gate-preset2 --gate-output /tmp/webview_gate_preset2_result.json --policy-preset strict-responsive-zero-diff --capture-set responsive --mode viewport --wait --diff-dir /tmp/webview_gate_preset2_diffs` succeeds.

### Summary
The package now makes policy presets easier to use in practice by letting gate flows select built-in QA policies by name rather than forcing raw policy-file paths in normal usage.

---

<a id="version-2170"></a>
## Version 2.17.0: Added one-step baseline gate workflow

**Date:** 2026-04-04
**Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e

### Changes
- Added `reference_live_gate.py` so a saved reference bundle can capture current state, replay the baseline, and apply threshold-aware QA gate rules in one flow.
- Added `skills/reference-live-gate/SKILL.md` so one-step saved-baseline + live-URL + gate evaluation has a dedicated front-door skill surface.
- Added `support/policies/strict-responsive-zero-diff.json` as a reusable strict policy preset for responsive zero-diff gating.
- Updated `skills/reference-live-review/SKILL.md`, `skills/qa-gate/SKILL.md`, and `agents/webview-vision-assist.md` so one-step baseline gating is now part of the visible workflow model.
- Updated README, design, and TODO wording so the product surface now explicitly includes one-step baseline gate usage and reusable policy presets.
- Bumped plugin and marketplace package versions to `2.17.0`.

### Validation
- `python3 -m py_compile reference_live_gate.py` succeeds.
- `python3 reference_live_gate.py --bundle /tmp/webview_reference_bundles/nodeclaw-docs-reference-v3.json --url https://claw-frontend-dev.nodenetwork.ovh/docs --current-report /tmp/webview_gate_current_report.json --comparison-json /tmp/webview_gate_compare.json --session-output /tmp/webview_gate_session.json --session-name nodeclaw-docs-live-gate --gate-output /tmp/webview_gate_result.json --policy-file /home/node/workplace/AWCLOUD/TEMPLATE/PLUGIN/webview-screenshort/support/policies/strict-responsive-zero-diff.json --capture-set responsive --mode viewport --wait --diff-dir /tmp/webview_gate_diffs` succeeds.
- the helper emits one machine-readable payload that includes both live replay output and the final gate result.

### Summary
The package now supports a true one-step saved-baseline gate flow, reducing the path from reusable baseline to policy-based QA decision into one reusable command.

---

<a id="version-2160"></a>
## Version 2.16.0: Added threshold-aware QA gate layer

**Date:** 2026-04-04
**Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e

### Changes
- Added `qa_gate.py` so compare-session, comparison, live-replay, or verdict artifacts can be checked against explicit threshold/policy rules.
- Added `skills/qa-gate/SKILL.md` so gate evaluation has a dedicated front-door skill surface.
- Updated `skills/qa-verdict/SKILL.md`, `skills/reference-live-review/SKILL.md`, `skills/compare-review/SKILL.md`, and `agents/webview-vision-assist.md` so verdict and gate layers are now part of the visible workflow.
- Updated README, design, and TODO wording so the product surface now explicitly includes threshold-aware gate evaluation on top of capture/compare/replay/verdict flows.
- Bumped plugin and marketplace package versions to `2.16.0`.

### Validation
- `python3 -m py_compile qa_gate.py` succeeds.
- `python3 qa_gate.py /tmp/webview_live_session_v3.json --require-device desktop --require-device tablet --require-device mobile --fail-on-invalid true --max-diff-ratio 0 --output-format json` succeeds.
- the helper returns a machine-readable gate result with policy, violated-rules surface, missing-device checks, and per-device gate status.

### Summary
The package now adds a true threshold-aware QA gate layer, so screenshot review can end not only with a verdict but also with a policy-based pass/fail decision.

---

<a id="version-2150"></a>
## Version 2.15.0: Added automated QA verdict layer

**Date:** 2026-04-04
**Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e

### Changes
- Added `qa_verdict.py` so compare-session, comparison, and live-replay artifacts can be converted into reusable machine-readable verdicts.
- Added `skills/qa-verdict/SKILL.md` so verdict generation has a dedicated front-door skill surface.
- Updated `skills/compare-review/SKILL.md`, `skills/reference-live-review/SKILL.md`, and `agents/webview-vision-assist.md` so compare/live-replay flows can now continue into a verdict layer directly.
- Updated README, design, and TODO wording so the product surface now explicitly includes verdict generation on top of capture/compare/replay workflows.
- Bumped plugin and marketplace package versions to `2.15.0`.

### Validation
- `python3 -m py_compile qa_verdict.py` succeeds.
- `python3 qa_verdict.py /tmp/webview_live_session_v3.json --output-format json` succeeds and returns per-device pass/fail verdicts.
- `python3 qa_verdict.py /tmp/webview_live_compare_v3.json --output-format text` succeeds and returns a concise verdict summary.

### Summary
The package now moves beyond raw compare artifacts by adding a reusable verdict layer, so screenshot QA can finish with a machine-readable outcome instead of only low-level pair metadata.

---

<a id="version-2141"></a>
## Version 2.14.1: Fixed authority/update drift after 2.14.0

**Date:** 2026-04-04
**Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e

### Changes
- Reworked `README.md` so the repo-local marketplace update path is now the primary example and the older `darkwingtm` route is clearly labeled as compatibility-only.
- Reworked `phase/phase-003-install-and-lifecycle-validation.md` so the primary lifecycle path now matches the standalone repo-local marketplace posture.
- Reworked `phase/SUMMARY.md` so TODO coordination wording matches the broader package scope instead of the older cutover-only slice.
- Bumped plugin and marketplace package versions to `2.14.1`.

### Validation
- `claude plugins validate /home/node/workplace/AWCLOUD/TEMPLATE/PLUGIN/webview-screenshort` succeeds.
- The repo-local install/update posture and compatibility-only shared-marketplace wording now point to the same authority model across README and phase docs.

### Summary
The package now presents one cleaner authority story: standalone repo-local marketplace first, shared `darkwingtm` path as checked compatibility-only context.

---

<a id="version-2140"></a>
## Version 2.14.0: Added live baseline replay workflow

**Date:** 2026-04-04
**Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e

### Changes
- Added `reference_live_bundle.py` so a saved reference bundle can capture a fresh current report from a live URL and emit a new expected/actual compare session in one flow.
- Added `skills/reference-live-review/SKILL.md` so live baseline replay has a dedicated front-door skill surface.
- Hardened `create_reference_bundle.py`, `apply_reference_bundle.py`, and `list_reference_bundles.py` so reusable baseline artifacts now carry explicit reference-side/report metadata, newer bundles carry bundled reference-report assets, and replay exposes richer metadata.
- Hardened `compare_reports.py` so non-diffable paired comparisons now fail the top-level comparison instead of being reported as successful replay runs just because device labels matched.
- Fixed `diff_images.py` so diff-pixel counting now reflects non-zero RGBA visual changes instead of relying only on alpha-channel differences.
- Hardened `agents/webview-vision-assist.md`, README, design, and TODO wording so the new live baseline replay path is reflected in the visible product surface.
- Bumped plugin and marketplace package versions to `2.14.0`.

### Validation
- `python3 -m py_compile screenshot.py compare_reports.py compare_session.py create_reference_bundle.py apply_reference_bundle.py list_reference_bundles.py diff_images.py reference_live_bundle.py` succeeds.
- `python3 create_reference_bundle.py --name nodeclaw-docs-reference-v3 --session /tmp/webview_compare_session.json --output /tmp/webview_reference_bundles/nodeclaw-docs-reference-v3.json --reference-label expected` succeeds and emits bundled reference-report assets.
- `python3 reference_live_bundle.py --bundle /tmp/webview_reference_bundles/nodeclaw-docs-reference-v3.json --url https://claw-frontend-dev.nodenetwork.ovh/docs --current-report /tmp/webview_live_current_report_v3.json --comparison-json /tmp/webview_live_compare_v3.json --session-output /tmp/webview_live_session_v3.json --session-name nodeclaw-docs-live-baseline-v3 --current-label actual --capture-set responsive --mode viewport --wait --diff-dir /tmp/webview_live_diff_outputs_v3` succeeds.
- `python3 apply_reference_bundle.py --bundle /tmp/webview_reference_bundles/nodeclaw-docs-reference-v2.json --current-report /tmp/webview_24_responsive_report.json --comparison-json /tmp/webview_apply_v2_compare.json --session-output /tmp/webview_apply_v2_session.json --session-name nodeclaw-docs-reference-v2-apply --current-label actual --diff-dir /tmp/webview_apply_v2_diffs` succeeds.
- `python3 list_reference_bundles.py /tmp/webview_reference_bundles --output-format json` now shows explicit `reference_side` and `reference_report_path` for newly created bundles, while older bundles still get useful fallback values.

### Summary
The package now moves one step closer to a real reusable frontend QA system by letting saved baselines be replayed directly against current live pages, while also making comparison success stricter and newly created baseline bundles more durable.

---

<a id="version-2130"></a>
## Version 2.13.0: Added bundle-lifecycle skill surface

**Date:** 2026-04-04
**Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e

### Changes
- Added `skills/reference-bundles/SKILL.md` so bundle listing, creation, and apply-reference work now have a dedicated front-door skill surface.
- Updated README and design guidance so baseline artifact lifecycle work is easier to invoke directly.
- Bumped plugin and marketplace package versions to `2.13.0`.

### Validation
- `python3 -m py_compile create_reference_bundle.py apply_reference_bundle.py list_reference_bundles.py` succeeds.
- the bundle lifecycle helpers remain valid and callable through the new dedicated skill surface.
- `claude plugins validate /home/node/workplace/AWCLOUD/TEMPLATE/PLUGIN/webview-screenshort` succeeds.

### Summary
The package now exposes bundle lifecycle work through a clearer front-door skill, reducing friction when users or agents need to browse, create, or apply reusable baseline artifacts.

---

<a id="version-2120"></a>
## Version 2.12.0: Added reference-bundle browsing

**Date:** 2026-04-04
**Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e

### Changes
- Added `list_reference_bundles.py` so saved reference bundles can be listed and summarized from a directory.
- Extended README and design guidance so baseline bundles are now easier to discover and reuse later.
- Bumped plugin and marketplace package versions to `2.12.0`.

### Validation
- `python3 -m py_compile list_reference_bundles.py` succeeds.
- `python3 list_reference_bundles.py /tmp/webview_reference_bundles --output-format json` succeeds.
- the helper returns a structured bundle index with name, reference label, session name, comparison mode, pair count, and success state.

### Summary
The package now supports lightweight browsing of saved baseline bundles, moving the QA workflow closer to a reusable asset system instead of path-by-path manual recall.

---

<a id="version-2110"></a>
## Version 2.11.0: Added apply-reference workflow

**Date:** 2026-04-04
**Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e

### Changes
- Added `apply_reference_bundle.py` so a saved reference bundle can be applied to a fresh report and turned into a new expected/actual compare session automatically.
- Extended README and design guidance so reference bundles are not only stored but also actively reusable in later QA runs.
- Bumped plugin and marketplace package versions to `2.11.0`.

### Validation
- `python3 -m py_compile apply_reference_bundle.py` succeeds.
- `python3 apply_reference_bundle.py --bundle /tmp/webview_reference_bundle.json --current-report /tmp/webview_24_responsive_report.json --comparison-json /tmp/webview_applied_compare.json --session-output /tmp/webview_applied_session.json --session-name nodeclaw-docs-actual-run --current-label actual` succeeds.
- the apply-reference workflow emits a fresh compare session from the saved baseline bundle plus the current report.

### Summary
The package now supports replaying expected/actual QA from saved reference bundles, moving the comparison flow closer to a reusable baseline-application system instead of static archive artifacts only.

---

<a id="version-2100"></a>
## Version 2.10.0: Added expected-reference bundles

**Date:** 2026-04-04
**Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e

### Changes
- Added `create_reference_bundle.py` so saved compare sessions can be promoted into reusable expected-reference bundle artifacts.
- Extended README and design guidance so reusable baseline bundles are now part of the intended QA workflow.
- Bumped plugin and marketplace package versions to `2.10.0`.

### Validation
- `python3 -m py_compile create_reference_bundle.py` succeeds.
- `python3 create_reference_bundle.py --name nodeclaw-docs-reference --session /tmp/webview_compare_session.json --output /tmp/webview_reference_bundle.json --reference-label expected` succeeds.
- the reference bundle persists a named baseline artifact on top of a saved compare session.

### Summary
The package now supports a reusable expected-reference layer, moving compare workflows closer to a baseline-driven QA system instead of one-off review artifacts only.

---

<a id="version-290"></a>
## Version 2.9.0: Added compare-session history browsing

**Date:** 2026-04-04
**Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e

### Changes
- Added `list_compare_sessions.py` so persisted compare-session artifacts can be listed and summarized from a directory.
- Extended the README and design guidance so compare-session history is now part of the intended QA workflow.
- Bumped plugin and marketplace package versions to `2.9.0`.

### Validation
- `python3 -m py_compile list_compare_sessions.py` succeeds.
- `python3 list_compare_sessions.py /tmp/webview_compare_sessions --output-format json` succeeds.
- the helper returns a structured index with session name, labels, comparison mode, pair count, and success state.

### Summary
The package now supports lightweight QA history browsing by turning saved compare sessions into a reusable indexable surface instead of isolated JSON artifacts only.

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
