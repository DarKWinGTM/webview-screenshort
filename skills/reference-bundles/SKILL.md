---
name: reference-bundles
description: Browse saved reference bundles, create a new reference bundle from a compare session, apply a saved reference bundle to a fresh report, or route into the live-url replay flow when a baseline should be checked against the current page automatically. Use this when compare artifacts should become reusable baseline assets and the current page may need richer witness capture, not screenshot-only replay.
argument-hint: list <bundle-dir> | create <compare-session.json> <bundle-name> <output.json> | apply <bundle.json> <current-report.json> <session-name> <comparison.json> <session.json> | apply-live --bundle <bundle.json> --url <live-url> --current-report <current-report.json> --comparison-json <comparison.json> --session-output <session.json> --session-name <session-name> [--witness-mode frontend-default|csr-debug|responsive|session-replay] [--header NAME:VALUE] [--origin-header Prerendercloud-Name:VALUE] [--cookie NAME=VALUE] [--cookie-file FILE] [--preloaded-state-json JSON] [--preloaded-state-file FILE]
allowed-tools: Bash, Read
---

# Reference Bundles Skill

Use this skill when webview compare artifacts should be turned into reusable baseline assets rather than handled as one-off JSON files.

## Modes

### 1) List bundles
```bash
PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" python3 -m webview_screenshort.cli.list_reference_bundles <bundle-dir> --output-format json
```

### 2) Create bundle
```bash
PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" python3 -m webview_screenshort.cli.create_reference_bundle --name <bundle-name> --session <compare-session.json> --output <bundle.json> --reference-label expected
```

### 3) Apply bundle
```bash
PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" python3 -m webview_screenshort.cli.apply_reference_bundle --bundle <bundle.json> --current-report <current-report.json> --comparison-json <comparison.json> --session-output <session.json> --session-name <session-name> --current-label actual --diff-dir <diff-dir>
```

### 4) Apply bundle to live URL
```bash
PYTHONPATH="${CLAUDE_PLUGIN_ROOT}" python3 -m webview_screenshort.cli.reference_live_bundle --bundle <bundle.json> --url <live-url> --current-report <current-report.json> --comparison-json <comparison.json> --session-output <session.json> --session-name <session-name> --current-label actual --mode viewport --wait
```

## Output expectations
- exact input/output artifact paths
- whether the bundle list/create/apply step succeeded
- summary of bundle/session metadata when available
- exact current-report path when the live-url replay flow was used
- next useful QA step after the artifact operation
