# Changelog - Webview Screenshort

> **Parent Document:** [../design/design.md](../design/design.md)
> **Current Version:** 2.0.0
> **Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e

---

## Version History (Unified)

| Version | Date | Changes | Summary |
|---------|------|---------|---------|
| 2.0.0 | 2026-04-03 | **[Plugin package and CSR frontend-vision validation](#version-200)** | Refactored the old project-local screenshot skill into a governed plugin package, added a frontend-review workflow surface, and verified real CSR capture against the NodeNetwork docs page. |
| 1.8 | 2026-02-07 | **[Project-Local Skill Implementation](#version-18)** | Implemented the older project-local screenshot skill model. |

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
