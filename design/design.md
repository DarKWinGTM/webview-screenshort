# Webview Screenshort

## 0) Document Control

> **Parent Scope:** TEMPLATE / PLUGIN / webview-screenshort
> **Current Version:** 2.0.0
> **Session:** dd0bf4af-a66b-4b07-bb9d-a90a0e57b54e (2026-04-03)

---

## 1) Goal

Provide a governed plugin package that captures real rendered webpages so Claude can use screenshots as visual evidence during frontend development.

The target is not only a raw screenshot CLI.
The target is a frontend-development vision workflow where Claude can:
- capture a live page
- verify CSR/SPA rendering state
- inspect real layout and UI output
- use screenshot evidence before recommending frontend changes

---

## 2) Active package model

The intended package model is:
- `.claude-plugin/plugin.json` = plugin metadata
- `.claude-plugin/marketplace.json` = standalone repo-local marketplace manifest for cutover and local install from this package root
- `skills/screenshot/SKILL.md` = primary runtime entrypoint
- `skills/screenshot/*.md` = focused frontend vision workflow guidance
- `agents/webview-vision-assist.md` = optional visual-review companion agent
- `screenshot.py` = execution engine
- `screenshot/` = generated screenshots and checked local artifacts
- `design/changelog/TODO/phase/patch` = governance authority

---

## 3) Runtime contract

### 3.1 Primary execution path
The skill should remain the main runtime surface.

Why:
- screenshot capture is a tooling action
- the user often wants a direct command
- capture should happen before analysis
- installed plugin execution should resolve through `${CLAUDE_PLUGIN_ROOT}` rather than a source-workspace-only path

### 3.2 Companion agent path
An optional agent can help when the task is not just “take a screenshot” but “use screenshots to review the frontend visually.”

That agent should:
- trigger screenshot capture first
- prefer visual evidence before advice
- support layout / UX / UI review workflows

---

## 4) Frontend vision workflow

The intended frontend-development workflow is:

```text
Need visual frontend review
  → capture the page
  → use --wait when CSR/SPA rendering is likely
  → choose viewport or fullpage
  → prefer JSON result output for workflow chaining
  → save screenshot locally
  → read the image
  → analyze layout / UX / UI from the screenshot
  → then recommend code or design changes
```

---

## 5) CSR support model

CSR support is considered sufficient when:
- a page that depends on client-side rendering still produces a meaningful rendered screenshot
- `--wait` improves post-hydration capture when needed
- viewport and fullpage modes both preserve useful frontend-review evidence

Checked local verification now shows:
- `https://claw-frontend-dev.nodenetwork.ovh/docs` renders successfully in viewport mode with `--wait`
- the same page also renders successfully in fullpage mode with `--wait`

This is evidence that the current engine can already support at least one real CSR-heavy docs page workflow.

---

## 6) Design boundaries

### What this package is
- screenshot capture for frontend development
- visual evidence generation for Claude review
- CSR-aware webpage capture with optional wait behavior
- a future plugin skill that fits local marketplace install workflows

### What this package is not
- a full browser automation suite
- a DOM testing framework
- a generic backend tool
- a replacement for deeper UI analysis tools; it is the visual input step

---

## 7) Current limitations

- current workflow still relies on Claude reading the generated image after capture instead of a fully bundled multi-step visual-analysis pipeline
- plugin install lifecycle for this package is now validated through the shared local marketplace, but reload/restart lifecycle is still not yet closed
- broader CSR validation still needs more than one checked target

---

## 8) Acceptance criteria

This package is considered successful for the current wave when:
- it has proper plugin package structure
- the screenshot skill works from the installed plugin path through `${CLAUDE_PLUGIN_ROOT}`
- the stale path from the old project-local skill model is removed
- real CSR pages can be captured successfully
- the package clearly supports frontend visual review workflows
- `screenshot.py` supports late-bound config for endpoints/timeouts
- `screenshot.py` supports machine-readable JSON output for workflow chaining
- governance docs describe the real current state rather than the older project-local skill state
