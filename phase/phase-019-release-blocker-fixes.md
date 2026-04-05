# Phase 019 - Release blocker fixes

> **Summary File:** [SUMMARY.md](SUMMARY.md)
> **Phase ID:** 019
> **Status:** Implemented - Pending Review
> **Design References:** [../design/design.md](../design/design.md)
> **Patch References:** [../patch/phase-019-release-blocker-fixes.patch.md](../patch/phase-019-release-blocker-fixes.patch.md)

---

## Objective

Fix the remaining release blockers before publish by preserving explicit operator witness-mode choice on higher-level review skills and keeping generated screenshot-side evidence outputs out of the tracked release surface by default.

## Why this phase exists

The package cleanup was structurally complete, but the checked release surface still had two practical blockers. First, the higher-level `frontend-review` and `responsive-review` skills hard-appended default witness modes, which meant an explicit operator-provided `--witness-mode` could be silently overridden. Second, timestamped JSON/HTML/TXT artifacts under `screenshot/` were still unignored, which made local runtime evidence too easy to drag into the release diff. This phase closes both blockers before publish.

## Action points / execution checklist

- [x] fix `frontend-review` so it only injects `frontend-default` when the operator did not already provide `--witness-mode`
- [x] fix `responsive-review` so it only injects `responsive` when the operator did not already provide `--witness-mode`
- [x] extend `.gitignore` so generated screenshot-side JSON/HTML/TXT evidence outputs stay local by default
- [x] bump package/governance metadata for the blocker-fix wave
- [x] sync README/design/TODO/phase wording for the blocker-fix wave
- [x] verify the checked release surface no longer carries those two blockers

## Verification

- checked `skills/frontend-review/SKILL.md` and `skills/responsive-review/SKILL.md` now preserve an explicit operator-provided `--witness-mode`
- checked `.gitignore` now ignores generated `screenshot/*.json`, `screenshot/*.html`, and `screenshot/*.txt` outputs in addition to PNG files
- `python3 -m py_compile /home/node/workplace/AWCLOUD/TEMPLATE/PLUGIN/webview-screenshort/webview_screenshort/cli/screenshot.py` succeeds
- `claude plugins validate /home/node/workplace/AWCLOUD/TEMPLATE/PLUGIN/webview-screenshort` succeeds

## Exit criteria

- higher-level review skills no longer silently override explicit witness-mode choice
- generated local screenshot/evidence outputs are ignored by default
- the checked release surface is cleaner and more trustworthy for commit/tagging
