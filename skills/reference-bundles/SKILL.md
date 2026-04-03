---
name: reference-bundles
description: Browse saved reference bundles, create a new reference bundle from a compare session, apply a saved reference bundle to a fresh report, or route into the live-url replay flow when a baseline should be checked against the current page automatically. Use this when compare artifacts should become reusable baseline assets.
argument-hint: list <bundle-dir> | create <compare-session.json> <bundle-name> <output.json> | apply <bundle.json> <current-report.json> <session-name> <comparison.json> <session.json> | apply-live --bundle <bundle.json> --url <live-url> --current-report <current-report.json> --comparison-json <comparison.json> --session-output <session.json> --session-name <session-name>
allowed-tools: Bash, Read
---

# Reference Bundles Skill

Use this skill when webview compare artifacts should be turned into reusable baseline assets rather than handled as one-off JSON files.

## Modes

### 1) List bundles
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/list_reference_bundles.py" <bundle-dir> --output-format json
```

### 2) Create bundle
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/create_reference_bundle.py" --name <bundle-name> --session <compare-session.json> --output <bundle.json> --reference-label expected
```

### 3) Apply bundle
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/apply_reference_bundle.py" --bundle <bundle.json> --current-report <current-report.json> --comparison-json <comparison.json> --session-output <session.json> --session-name <session-name> --current-label actual --diff-dir <diff-dir>
```

### 4) Apply bundle to live URL
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/reference_live_bundle.py" --bundle <bundle.json> --url <live-url> --current-report <current-report.json> --comparison-json <comparison.json> --session-output <session.json> --session-name <session-name> --current-label actual --mode viewport --wait
```

## Output expectations
- exact input/output artifact paths
- whether the bundle list/create/apply step succeeded
- summary of bundle/session metadata when available
- exact current-report path when the live-url replay flow was used
- next useful QA step after the artifact operation
