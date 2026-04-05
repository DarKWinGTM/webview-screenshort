# Phase 024 - Output path policy

> **Summary File:** [SUMMARY.md](SUMMARY.md)
> **Phase ID:** 024
> **Status:** Implemented - Pending Review
> **Design References:** [../design/design.md](../design/design.md)
> **Patch References:** [../patch/phase-024-output-path-policy.patch.md](../patch/phase-024-output-path-policy.patch.md)

---

## Objective

Move the default no-override output policy away from package/plugin-cache paths toward workspace-local temp/artifact placement, with OS tmp only as fallback.

## Why this phase exists

The current checked output-path behavior still defaults unguided capture output into the package-side `screenshot/` directory. That works for source-side package development, but it becomes awkward when the package is running from an installed plugin path and downstream tools only accept files inside the current workspace. This phase establishes the next intended path policy before implementation so the output contract can become safer and more interoperable.

## Action points / execution checklist

- [x] preserve explicit caller paths as highest-priority output control (`--output`, `--output-dir`, `--report-file`, `--bundle-file`)
- [x] preserve `WEBVIEW_SCREENSHORT_OUTPUT_DIR` as the next override layer
- [x] add a workspace-local temp/artifact default when no explicit path or env override is provided
- [x] use OS tmp only as fallback when a workspace-local path is unavailable or unwritable
- [x] keep sibling artifacts together under the same derived base path
- [x] sync README/design/changelog/TODO after implementation validation

## Verification

- `python3 -m py_compile /home/node/workplace/AWCLOUD/TEMPLATE/PLUGIN/webview-screenshort/webview_screenshort/capture/paths.py` succeeds
- source-tree probing now resolves `/home/node/workplace/AWCLOUD/CLAUDE/.tmp/webview-screenshort` from normal workspace execution and from plugin-cache-style execution when a usable prior workspace path is available
- source-tree capture smoke test now emits default artifacts under `/home/node/workplace/AWCLOUD/CLAUDE/.tmp/webview-screenshort` instead of package/plugin-cache paths
- `claude plugins validate /home/node/workplace/AWCLOUD/TEMPLATE/PLUGIN/webview-screenshort` succeeds

## Exit criteria

- the output-path precedence is `explicit path > env override > workspace-local temp/artifact dir > OS tmp fallback`
- the package no longer defaults unguided output into plugin cache paths first
- artifact sibling files remain colocated predictably under the chosen base path
