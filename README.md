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

- `<workspace-root>` = this plugin package root
- `<marketplace-root>` = the current shared local marketplace root that contains package directories plus `.claude-plugin/marketplace.json`
- `<repo-marketplace-root>` = this package root when it becomes its own standalone plugin repo with local marketplace support

## Installation and activation

### Local marketplace install in the current shared workspace
Add the shared marketplace once:

```bash
claude plugins marketplace add "/home/node/workplace/AWCLOUD/TEMPLATE/PLUGIN" --scope local
```

Install this package:

```bash
claude plugins install webview-screenshort@darkwingtm --scope local
```

### Standalone-repo local marketplace install target
When this package becomes its own repo, the intended local marketplace shape is:

```bash
claude plugins marketplace add "<repo-marketplace-root>" --scope local
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

## Current status

Verified now:
- `screenshot.py` captures live webpages successfully
- CSR-heavy page capture works when `--wait` is used
- viewport and fullpage capture both work
- the package now has plugin scaffolding with `.claude-plugin/`, `skills/`, and `agents/`
- the package installs through the shared `darkwingtm` marketplace and exposes `webview-screenshort:webview-vision-assist`
- skill/agent execution now targets `${CLAUDE_PLUGIN_ROOT}` instead of a source-workspace-only path
- `screenshot.py` now supports env-driven capture configuration and JSON result output for chaining into frontend review workflows

Checked live example:
- `https://claw-frontend-dev.nodenetwork.ovh/docs`
- viewport + wait capture succeeded
- fullpage + wait capture succeeded

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

- restart/reload lifecycle for this package is not yet closed
- visual analysis orchestration still depends on Claude reading the generated image after capture
- broader CSR validation still needs more than one checked target
- separate-repo authority cutover is not yet complete

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
