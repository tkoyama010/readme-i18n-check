# readme-i18n-check

[![Tests](https://github.com/tkoyama010/readme-i18n-check/actions/workflows/test.yml/badge.svg)](https://github.com/tkoyama010/readme-i18n-check/actions/workflows/test.yml)
[![README i18n Check](https://github.com/tkoyama010/readme-i18n-check/actions/workflows/readme-i18n-check.yml/badge.svg)](https://github.com/tkoyama010/readme-i18n-check/actions/workflows/readme-i18n-check.yml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/tkoyama010/readme-i18n-check/main.svg)](https://results.pre-commit.ci/latest/github/tkoyama010/readme-i18n-check/main)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **日本語**: [README.ja.md](README.ja.md)

Zero-dependency README i18n drift-detection: structural parity + stale-translation check for GitHub-native localized READMEs.

Python stdlib only — no third-party runtime dependencies. Works as both a pre-commit hook and a GitHub Action.

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Background](#background)
- [Install](#install)
- [Usage](#usage)
  - [Pre-commit Hook](#pre-commit-hook)
  - [GitHub Action](#github-action)
  - [Command Line](#command-line)
- [Checks](#checks)
  - [Structural Parity](#structural-parity)
  - [Stale Translation](#stale-translation)
  - [Allowlist](#allowlist)
- [Contributing](#contributing)
- [License](#license)

## Background

Projects with multilingual READMEs (e.g. `README.md`, `README.ja.md`, `README.zh_CN.md`) face two drift problems:

1. **Structural drift** — a translation is missing or adds sections, or headings diverge from the English README.
2. **Content drift** — the English README is updated but a translation is not, leaving it stale.

This tool detects both automatically, in CI and pre-commit, so drift is surfaced rather than left to reviewer vigilance.

## Install

No installation is needed beyond Python 3.9+. The package uses zero third-party dependencies (Python stdlib only).

## Usage

### Pre-commit Hook

Add this to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/tkoyama010/readme-i18n-check
    rev: v0.1.0  # Use the latest tag
    hooks:
      - id: check-readme-i18n
```

The pre-commit hook runs the structural-parity check only (`--no-stale-check`) to avoid false positives on staged changes.

### GitHub Action

Add this to your workflow:

```yaml
steps:
  - uses: actions/checkout@v4
    with:
      fetch-depth: 0  # Required for stale-translation check

  - uses: tkoyama010/readme-i18n-check@v0.1.0
    with:
      # allowlist: .github/readme-i18n-allowlist  # optional
      # no-stale-check: 'false'                   # default: false
      # repo-root: .                               # default: auto-detect
```

### Command Line

```bash
python -m check_readme_i18n [OPTIONS]
```

Options:

- `--allowlist FILE` — file listing filenames exempt from stale checks (one per line, `#` comments allowed)
- `--no-stale-check` — skip the stale-translation (git commit date) check
- `--repo-root PATH` — repository root (auto-detected via git if omitted)

Exit codes: 0 = pass, 1 = drift detected, 2 = configuration error.

## Checks

### Structural Parity

Heading levels (H1-H6) are extracted from `README.md` and each `README.<lang>.md`. The lists must match in count and per-position level. This catches missing, extra, or restructured sections while allowing heading *text* to differ (it is translated).

### Stale Translation

The git commit timestamp of each localized README is compared against `README.md`. If the translation's last commit predates the English README's latest change, it is flagged as stale. Requires `fetch-depth: 0` in GitHub Actions checkout.

### Allowlist

A file listing filenames exempt from the stale check. One filename per line, `#` comments allowed. Use this when an English README change is cosmetic (e.g. a badge URL) and does not require translation updates.

Example allowlist file:

```
# Cosmetic changes that don't need translation updates
README.ja.md
```

## Contributing

Contributions are welcome! Please open an issue or pull request on [GitHub](https://github.com/tkoyama010/readme-i18n-check/issues).

## License

[MIT](LICENSE) © Tetsuo Koyama
