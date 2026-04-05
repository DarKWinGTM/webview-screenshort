# Webview Screenshort - Phase Summary

> **Current Version:** 2.40.1
> **Target Design:** [../design/design.md](../design/design.md) v2.40.1
> **Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e
> **Status:** Implemented - Pending Review
> **Full history:** [../changelog/changelog.md](../changelog/changelog.md)

---

## Context

This phase workspace tracks the conversion of `webview-screenshort` from an older project-local skill utility into a governed plugin package for frontend-development visual workflows.

---

## Source-Input Extraction Summary

| Phase | Phase File | Design Source | Patch Source | Derived Execution Work | Target Outcome |
|---|---|---|---|---|---|
| 001 | `phase-001-convert-to-plugin-package.md` | `design/design.md` active package model | `../patch/phase-001-convert-to-plugin-package.patch.md` | Convert old project-local layout into governed plugin package structure | Package has standard plugin layout |
| 002 | `phase-002-validate-csr-screenshot-workflow.md` | `design/design.md` CSR support model | `../patch/phase-002-validate-csr-screenshot-workflow.patch.md` | Validate real CSR capture, responsive presets, and frontend-vision use case | Real CSR page capture and responsive review support are evidence-backed |
| 003 | `phase-003-install-and-lifecycle-validation.md` | `design/design.md` runtime contract | `none` | Validate plugin install, skill visibility, and runtime lifecycle | Package works as installed plugin |
| 004 | `phase-004-separate-repo-cutover.md` | `design/design.md` plus package-local marketplace cutover posture | `../patch/phase-004-separate-repo-cutover.patch.md` | Prepare authority migration from the shared workspace into a standalone `webview-screenshort` repo | Package can cut over to its own repo without duplicate authority |
| 005 | `phase-005-live-baseline-replay.md` | `design/design.md` live baseline replay and reusable baseline model | `../patch/phase-005-live-baseline-replay.patch.md` | Add saved-bundle + live-URL replay as a first-class frontend QA workflow | Reusable baselines can be replayed directly against current live pages in one flow |
| 006 | `phase-006-mismatch-classification.md` | `design/design.md` compare/verdict/gate mismatch classification model | `../patch/phase-006-mismatch-classification.patch.md` | Add machine-readable mismatch classifications across compare, verdict, and gate layers | QA artifacts explain why devices failed, not only which devices failed |
| 007 | `phase-007-frontend-vision-evidence-bundle.md` | `design/design.md` frontend-vision upgrade model, session-replay capture boundary, and strategic runtime refactor direction | `../patch/phase-007-frontend-vision-evidence-bundle.patch.md` | Start the strategic runtime refactor, add richer witness modes, emit rendered HTML/rendered text evidence bundles, and prepare logged-in-state capture via bounded session context | The package becomes screenshot-first but HTML-aware, with a clearer internal architecture and richer frontend evidence output |
| 008 | `phase-008-metadata-and-acquisition-witnesses.md` | `design/design.md` richer witness model and bounded provider-capability truth | `../patch/phase-008-metadata-and-acquisition-witnesses.patch.md` | Add acquisition-summary and provider-returned metadata witnesses so capture outputs explain how richer artifacts were obtained | The package exposes more machine-readable frontend truth without pretending it already has full browser console/network tracing |
| 009 | `phase-009-semantic-page-witness.md` | `design/design.md` semantic page witness model and richer frontend structure understanding | `../patch/phase-009-semantic-page-witness.patch.md` | Add a rendered-HTML-derived semantic page witness and preserve it across bundle/replay flows | The package can summarize page structure in machine-readable form without forcing reviewers to reread full raw HTML every time |
| 010 | `phase-010-package-reorganization.md` | `design/design.md` package-organization model and internal domain separation | `../patch/phase-010-package-reorganization.patch.md` | Reorganize compare / QA / reference flows into package-internal domains and keep root commands compatibility-thin | The package reads more like a professional Python project instead of a flat root-script pile |
| 011 | `phase-011-capture-domain-authority.md` | `design/design.md` capture-domain authority split and compatibility-shim posture | `../patch/phase-011-capture-domain-authority.patch.md` | Move auth-context and headless-render-api ownership under `capture/` while preserving old import paths as shims | The capture side starts to match the newer package-domain structure without breaking current flows |
| 012 | `phase-012-capture-service-split.md` | `design/design.md` deeper capture-service split and facade-boundary cleanup | `../patch/phase-012-capture-service-split.patch.md` | Start moving config/path/witness responsibilities out of `capture_service.py` into dedicated capture modules | The largest remaining capture monolith becomes thinner while preserving current capture behavior |
| 013 | `phase-013-capture-authority-surface.md` | `design/design.md` capture authority-surface promotion and consumer migration | `../patch/phase-013-capture-authority-surface.patch.md` | Extract capture models/engines/reporting/runtime modules and start moving consumers onto `capture.service` | The capture package becomes more authoritative while `capture_service.py` remains a compatibility facade |
| 014 | `phase-014-capture-facade-cleanup.md` | `design/design.md` capture authority consolidation and legacy-facade cleanup | `../patch/phase-014-capture-facade-cleanup.patch.md` | Reduce `capture_service.py` to a true compatibility facade now that `capture.service` is the active authority surface | The capture package finishes this refactor stretch with one clearer active authority and one explicit legacy shim |
| 015 | `phase-015-semantic-aware-qa.md` | `design/design.md` semantic-aware QA companion model | `../patch/phase-015-semantic-aware-qa.patch.md` | Add semantic companion classification summaries to compare, verdict, and gate artifacts | The package can now preserve semantic structure drift as machine-readable QA context instead of relying only on visual mismatch summaries |
| 016 | `phase-016-semantic-gate-rules.md` | `design/design.md` semantic-aware gate policy model | `../patch/phase-016-semantic-gate-rules.patch.md` | Add semantic-aware gate rule keys so policy evaluation can explicitly fail on semantic drift | Semantic companion output now affects policy evaluation rather than only being carried as summary context |
| 017 | `phase-017-semantic-policy-granularity.md` | `design/design.md` finer semantic gate policy model | `../patch/phase-017-semantic-policy-granularity.patch.md` | Add finer semantic gate rule granularity for title/headings/structure/link/button/form/input drift | Semantic-aware gate presets can now express more precise frontend QA intent instead of only class-level semantic drift |
| 018 | `phase-018-wrapper-retirement-governance-contract.md` | `design/design.md` active command/authority contract after wrapper retirement | `../patch/phase-018-wrapper-retirement-governance-contract.patch.md` | Normalize governance/docs after wrapper retirement so active package CLI execution and retired-wrapper placement are described consistently | The cleanup closes with one current-state command contract, one active capture authority surface, and one explicit retirement location for old wrappers |
| 019 | `phase-019-release-blocker-fixes.md` | `design/design.md` higher-level review-skill witness-mode contract and generated-artifact hygiene | `../patch/phase-019-release-blocker-fixes.patch.md` | Fix release blockers before publish by preserving explicit witness-mode choice and ignoring generated runtime evidence outputs by default | The release surface no longer silently overrides operator witness-mode selection and no longer treats timestamped screenshot-side evidence outputs as normal tracked content |
| 020 | `phase-020-darkwingtm-runtime-authority-wording.md` | `design/design.md` runtime-authority wording split between source/release authority and maintained local runtime authority | `../patch/phase-020-darkwingtm-runtime-authority-wording.patch.md` | Realign install/update wording so this environment keeps `webview-screenshort@darkwingtm` as the maintained runtime label while the standalone repo remains the code/release source | The docs stop blurring code/release authority with installed runtime authority and now match the real operating model for this environment |
| 021 | `phase-021-prototype-retirement.md` | `design/design.md` final strategic package-structure cleanup with no retained prototype wrapper layer | `../patch/phase-021-prototype-retirement.patch.md` | Remove the retained `prototype/` wrapper area and normalize active docs/governance around the direct package CLI structure only | The package becomes more fully strategic: one active structure, no retained prototype execution layer, and no active-state docs that still lean on prototype retirement storage |
| 022 | `phase-022-readme-capability-map.md` | `design/design.md` operator-facing capability visibility for the current package surface | `../patch/phase-022-readme-capability-map.patch.md` | Add a complete current capability map to README so users can see capture/review/compare/baseline/QA surfaces and artifact outputs in one place | The package becomes easier to understand operationally because the active capability set is visible from one README section instead of being scattered across many skill and doc files |
| 023 | `phase-023-readme-witness-explanations.md` | `design/design.md` operator-facing witness clarity for screenshot/rendered HTML/rendered text/semantic/prerender outputs | `../patch/phase-023-readme-witness-explanations.patch.md` | Expand README so the witness layers are explained in practical frontend-review terms instead of only being listed as artifact names | Users can understand what each witness means, when to use it, and what the rendered-HTML capability can and cannot provide |
| 024 | `phase-024-output-path-policy.md` | `design/design.md` output-path precedence for workspace-friendly artifact placement | `../patch/phase-024-output-path-policy.patch.md` | Move the default no-override output policy away from package/plugin-cache paths toward workspace-local temp/artifact placement, with OS tmp only as fallback | The package becomes safer for installed-plugin usage and more compatible with workspace-limited MCP/image-analysis flows when no explicit output path is provided |
| 025 | `phase-025-bounded-preload-state-plan.md` | `design/design.md` bounded preload-state + cookie replay model for authenticated rendering | `../patch/phase-025-bounded-preload-state-plan.patch.md` | Add bounded authenticated-rendering replay around cookies plus origin-side `window.__PRELOADED_STATE__` reconstruction | The package now has an implemented bounded replay model with explicit limits, redaction, and origin-bootstrap semantics instead of only a planned contract |

---

## Phase Map

| Phase | Status | File | Objective |
|---|---|---|---|
| 001 | Implemented - Pending Review | `phase-001-convert-to-plugin-package.md` | Convert the old utility into governed plugin package structure |
| 002 | Implemented - Pending Review | `phase-002-validate-csr-screenshot-workflow.md` | Validate real CSR capture and responsive frontend review workflows |
| 003 | Implemented - Pending Review | `phase-003-install-and-lifecycle-validation.md` | Validate install/lifecycle through plugin flow |
| 004 | Implemented - Pending Review | `phase-004-separate-repo-cutover.md` | Finalize standalone repo authority and retire shared-workspace authority posture |
| 005 | Implemented - Pending Review | `phase-005-live-baseline-replay.md` | Add saved-bundle + live-URL replay as a first-class reusable frontend QA workflow |
| 006 | Implemented - Pending Review | `phase-006-mismatch-classification.md` | Add machine-readable mismatch classifications across compare, verdict, and gate workflows |
| 007 | Implemented - Pending Review | `phase-007-frontend-vision-evidence-bundle.md` | Start the strategic frontend-vision upgrade with internal runtime modules, richer witness modes, evidence bundles, and bounded session-replay capture |
| 008 | Implemented - Pending Review | `phase-008-metadata-and-acquisition-witnesses.md` | Add metadata/acquisition witness artifacts so richer capture outputs explain provider-returned page truth more clearly |
| 009 | Implemented - Pending Review | `phase-009-semantic-page-witness.md` | Add semantic page witness artifacts so richer capture outputs summarize page structure in machine-readable form |
| 010 | Implemented - Pending Review | `phase-010-package-reorganization.md` | Reorganize package-internal domains so root commands become compatibility-thin wrappers instead of mixed implementation files |
| 011 | Implemented - Pending Review | `phase-011-capture-domain-authority.md` | Move auth/headless capture authority under `capture/` while preserving legacy import paths as shims |
| 012 | Implemented - Pending Review | `phase-012-capture-service-split.md` | Start splitting `capture_service.py` so config/path/witness responsibilities leave the monolith |
| 013 | Implemented - Pending Review | `phase-013-capture-authority-surface.md` | Extract capture runtime modules further and migrate key consumers onto `capture.service` |
| 014 | Implemented - Pending Review | `phase-014-capture-facade-cleanup.md` | Reduce `capture_service.py` to a true compatibility facade now that `capture.service` is the active authority surface |
| 015 | Implemented - Pending Review | `phase-015-semantic-aware-qa.md` | Add semantic companion classification summaries to compare, verdict, and gate artifacts |
| 016 | Implemented - Pending Review | `phase-016-semantic-gate-rules.md` | Add semantic-aware gate rule keys so policy evaluation can explicitly fail on semantic drift |
| 017 | Implemented - Pending Review | `phase-017-semantic-policy-granularity.md` | Add finer semantic gate rule granularity for title/headings/structure/link/button/form/input drift |
| 018 | Implemented - Pending Review | `phase-018-wrapper-retirement-governance-contract.md` | Normalize governance/docs after wrapper retirement so active package CLI execution and retired-wrapper placement are described consistently |
| 019 | Implemented - Pending Review | `phase-019-release-blocker-fixes.md` | Preserve explicit witness-mode choice in review skills and ignore generated screenshot-side runtime artifacts by default |
| 020 | Implemented - Pending Review | `phase-020-darkwingtm-runtime-authority-wording.md` | Realign install/update wording so this environment keeps `webview-screenshort@darkwingtm` as the maintained runtime label |
| 021 | Implemented - Pending Review | `phase-021-prototype-retirement.md` | Remove the retained `prototype/` wrapper area and normalize the package around the direct strategic structure only |
| 022 | Implemented - Pending Review | `phase-022-readme-capability-map.md` | Add a complete current capability map to README so the package surfaces and artifacts are visible in one place |
| 023 | Implemented - Pending Review | `phase-023-readme-witness-explanations.md` | Expand README so the witness layers are explained in practical frontend-review terms |
| 024 | Implemented - Pending Review | `phase-024-output-path-policy.md` | Move the default no-override output policy toward workspace-local temp/artifact placement instead of package/plugin-cache defaults |
| 025 | Implemented - Pending Review | `phase-025-bounded-preload-state-plan.md` | Add bounded cookie + preloaded-state replay support without assuming direct browser-storage injection |

---

## Global TODO / Changelog Coordination

- `TODO.md` should track the active package work and shipped execution history clearly, not only the earlier cutover slice.
- `changelog/changelog.md` should record shipped plugin-structure, CSR-validation, repo-root install-normalization, responsive capture-set workflow, report-file/review-skill workflow, compare-review/report-schema workflow, structured compare-helper outcomes, diff-assisted compare outcomes, named compare-session outcomes, compare-session history outcomes, expected-reference bundle outcomes, apply-reference workflow outcomes, reference-bundle browsing outcomes, bundle-lifecycle skill-surface outcomes, live baseline replay outcomes, qa-verdict outcomes, qa-gate outcomes, one-step baseline gate outcomes, semantic preset outcomes, policy-family outcomes, mismatch-classification outcomes, repo-local marketplace install outcomes, agent-orchestration hardening outcomes, strategic runtime-package extraction, richer witness-mode output, evidence-bundle output, bounded session-replay capture outcomes, metadata/acquisition witness outcomes, semantic page witness outcomes, package-reorganization outcomes, capture-domain authority outcomes, capture-service split outcomes, capture authority-surface outcomes, capture facade cleanup outcomes, semantic-aware QA outcomes, semantic-aware gate-rule outcomes, and semantic-policy-granularity outcomes only.
- `design/design.md` remains the authority for frontend-vision intent, plugin boundaries, standalone-repo install posture, richer witness modes, semantic page witness boundaries, package-domain organization boundaries, capture-domain authority boundaries, and session-replay capture boundaries.

---

## Final Verification

- package reorganized into governed plugin layout
- real CSR docs page capture verified in viewport and fullpage modes
- stale project-local skill path identified and removed
- frontend-vision workflow intent is now explicit in docs and skill surfaces
- package validates through its standalone repo-root marketplace manifest
- installed agent visibility is confirmed
- standalone repo now acts as the package source/release authority
- the maintained local runtime install/update authority label in this environment remains `webview-screenshort@darkwingtm`
- installed runtime invocation now uses `${CLAUDE_PLUGIN_ROOT}`
- engine now supports env-driven configuration and JSON result output
- responsive mobile and tablet presets are validated on a second frontend target
- responsive desktop/tablet/mobile multi-capture workflow is validated on the NodeNetwork docs page
- one-run responsive capture-set workflow now returns combined desktop/tablet/mobile machine-readable results
- focused and responsive capture flows can now persist report-file artifacts for later re-reading
- dedicated `frontend-review` and `responsive-review` skill surfaces now sit above the lower-level screenshot engine
- compare-review can now compare two persisted report artifacts for regression-style visual checks
- persisted report artifacts now carry explicit schema/version metadata for reuse
- `compare_reports.py` now emits structured image-pair metadata for expected/actual and before/after review
- `diff_images.py` now emits diff metrics and optional diff images for compare workflows
- `compare_session.py` now persists named expected/actual compare sessions for later QA review
- `list_compare_sessions.py` now exposes saved compare-session history for lightweight QA browsing
- `create_reference_bundle.py` now promotes saved compare sessions into reusable expected-reference bundles
- `apply_reference_bundle.py` now replays a saved baseline against a fresh report to emit a new expected/actual session
- `list_reference_bundles.py` now exposes saved baseline bundles for lightweight QA browsing
- `skills/reference-bundles/SKILL.md` now exposes bundle listing, creation, and apply-reference work from one front door
- `reference_live_bundle.py` now captures a fresh current report from a live URL and replays a saved baseline automatically
- `skills/reference-live-review/SKILL.md` now exposes saved-baseline replay against a live URL from one front door
- `qa_verdict.py` now turns compare/live-replay artifacts into reusable machine-readable verdicts
- `qa_gate.py` now applies threshold-aware policy rules on top of verdict artifacts
- compare, verdict, and gate artifacts now emit machine-readable mismatch classifications so failures explain why they happened, not only which device failed
- `reference_live_gate.py` now captures current state, replays a saved baseline, and applies gate policy in one flow
- reusable policy presets now exist under `support/policies/`
- policy presets now carry family-aware metadata with canonical selectors and legacy aliases
- reference bundles now carry explicit `reference_side` and `reference_report_path` metadata for more reliable replay
- repo-local marketplace validation path now remains available from the standalone repo root when source-side package checks are needed
- the maintained local runtime install/update authority label in this environment remains `webview-screenshort@darkwingtm`
- `webview-vision-assist` now routes more explicitly between focused review, responsive review, compare-review, bundle-lifecycle, live baseline replay, verdict, gate, one-step baseline gate, and preset-discovery entrypoints
- the runtime now has an internal `webview_screenshort/` package so capture/auth/provider/workflow logic no longer has to remain only in top-level scripts
- richer witness modes now exist for screenshot-only, screenshot + rendered HTML/text, CSR-debug, responsive, and session-replay capture flows
- the runtime can now emit `webview-screenshort.evidence-bundle/v1` artifacts with screenshot plus rendered-page witness paths
- compare flows can now accept `webview-screenshort.evidence-bundle/v1` artifacts instead of only screenshot-era capture reports
- reference-bundle creation can now preserve `reference_artifact_schema` when the source compare session came from richer evidence bundles
- logged-in-state capture now has bounded operator-facing inputs for headers/cookies/session material with redacted auth summaries in persisted outputs
- semantic page witness JSON can now be emitted from rendered HTML and preserved in richer capture/evidence outputs
- responsive capture-set output now preserves capture-set semantic/acquisition witness indexes for cross-device frontend review
- reference-bundle creation now copies semantic/acquisition/metadata witness artifacts when the source report already carries them
- compare / QA / reference logic now lives behind package-internal domains instead of staying only as root-script implementations
- package CLI modules now own the active programmable command surface directly, with no retained prototype-wrapper layer left in the package structure
- `webview_screenshort/workflows.py` no longer imports root scripts directly and now acts as a package-internal compatibility surface
- direct script-to-script subprocess coupling has been reduced where compare, QA, and reference flows now reuse package modules in-process
- auth-context and headless-render-api ownership now live under `webview_screenshort/capture/` while legacy import paths remain as compatibility shims
- config/path/witness responsibilities have now started moving out of `capture_service.py` into `webview_screenshort/capture/config.py`, `capture/paths.py`, and `capture/witnesses.py`
- additional capture runtime modules now exist for models, engines, reporting, and runtime orchestration under `webview_screenshort/capture/`
- key consumers such as package exports, screenshot CLI, and live replay now import through `capture.service` as the newer capture authority surface
- `capture_service.py` now acts as a true compatibility facade instead of continuing to duplicate the remaining capture implementation
- the active command/gov-doc contract is now normalized around `PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" python3 -m webview_screenshort.cli.<tool>` with no prototype retirement layer remaining in the package structure
- compare, verdict, and gate artifacts now preserve semantic companion classification summaries on top of visual mismatch summaries
- gate policy can now explicitly fail on semantic drift through semantic-aware policy keys such as missing semantic witness or semantic structure/content change
- semantic gate policy can now target finer-grained drift such as title change, missing headings, structure-flag change, missing links/buttons, form-count change, and missing inputs
- active skill and agent command guidance now points at package CLI module execution instead of root wrapper filenames
- the retained prototype wrapper area has been removed, so the package now exposes only the direct strategic structure in both code and governance docs
- higher-level review skills now preserve an explicit operator-provided `--witness-mode` instead of silently overriding it with a default
- generated timestamped files under `screenshot/` now stay ignored by default so local runtime evidence does not pollute the package release surface
- default no-override output now prefers a workspace-local temp/artifact path and uses OS tmp only as fallback when no usable workspace path can be determined
- bounded preload-state replay now exists alongside cookies through generated `Prerendercloud-*` headers, with redacted summaries and no direct browser-storage injection claim

---
