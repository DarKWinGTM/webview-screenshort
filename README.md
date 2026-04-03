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

### Checked local development note

The same package is also currently validated through the shared local `darkwingtm` marketplace during workspace development. That shared-marketplace route is a checked local development path, not the public default install story for this repo.

## Current status

Verified now:
- `screenshot.py` captures live webpages successfully
- CSR-heavy page capture works when `--wait` is used
- viewport and fullpage capture both work
- mobile and tablet viewport presets now work for responsive frontend review
- the package now has plugin scaffolding with `.claude-plugin/`, `skills/`, and `agents/`
- the package installs through its own repo-root marketplace manifest and exposes `webview-screenshort:webview-vision-assist`
- skill/agent execution now targets `${CLAUDE_PLUGIN_ROOT}` instead of a source-workspace-only path
- `screenshot.py` now supports env-driven capture configuration and JSON result output for chaining into frontend review workflows
- public-repo install posture is now validated from the standalone repo root

Checked live examples:
- `https://claw-frontend-dev.nodenetwork.ovh/docs`
  - viewport + wait capture succeeded
  - fullpage + wait capture succeeded
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
  screenshot.py
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
- visual analysis orchestration still depends on Claude reading the generated image after capture
- broader CSR validation still needs more than one checked target
- public-repo wording polish is still in progress outside the now-validated repo-root install path

---

## Recommended usage model

### For focused capture
- `/screenshot <url> --wait --mode viewport`
- `/screenshot <url> --wait --mode fullpage`

### For frontend review
1. capture first
2. read the image
3. analyze the visible layout/UI from the screenshot
4. only then suggest code or design changes

### For responsive frontend review
1. capture desktop, tablet, and mobile variants with `--output-format json`
2. read each result and image
3. compare hierarchy, overflow, spacing, stacking, and readability across breakpoints
4. summarize which issues are desktop-only, tablet-only, mobile-only, or cross-device
