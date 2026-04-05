# Phase 020 - Darkwingtm runtime authority wording

> **Summary File:** [SUMMARY.md](SUMMARY.md)
> **Phase ID:** 020
> **Status:** Implemented - Pending Review
> **Design References:** [../design/design.md](../design/design.md)
> **Patch References:** [../patch/phase-020-darkwingtm-runtime-authority-wording.patch.md](../patch/phase-020-darkwingtm-runtime-authority-wording.patch.md)

---

## Objective

Realign install/update authority wording so this environment clearly uses `webview-screenshort@darkwingtm` as the maintained runtime label while keeping the standalone repo as the code/release source of truth.

## Why this phase exists

The package docs had normalized too far toward the standalone repo-local marketplace label, which made the repo read as if `webview-screenshort@webview-screenshort` were also the preferred installed identity for this environment. That wording drift created real operator confusion. This phase restores the actual operating contract: repo authority for code/releases, `@darkwingtm` authority for the maintained local runtime label.

## Action points / execution checklist

- [x] update README install/update wording to prefer `webview-screenshort@darkwingtm`
- [x] update design/install lifecycle wording to separate repo validation from local runtime authority
- [x] update phase summary and phase-003 install/lifecycle wording to match the maintained runtime label
- [x] record the wording correction in TODO/changelog and bump metadata to 2.35.0
- [x] verify checked local runtime state still uses `webview-screenshort@darkwingtm`

## Verification

- checked `README.md`, `design/design.md`, `phase/phase-003-install-and-lifecycle-validation.md`, `phase/SUMMARY.md`, `TODO.md`, and `changelog/changelog.md`
- checked local installed runtime state currently uses `webview-screenshort@darkwingtm`
- `claude plugins validate /home/node/workplace/AWCLOUD/TEMPLATE/PLUGIN/webview-screenshort` succeeds

## Exit criteria

- current-state docs distinguish code/release authority from installed runtime authority
- current-state docs prefer `webview-screenshort@darkwingtm` for the maintained local runtime lifecycle in this environment
- standalone repo-local marketplace usage is framed as source-side validation/cutover support instead of the preferred runtime label here
