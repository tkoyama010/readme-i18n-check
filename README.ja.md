# readme-i18n-check

[![Tests](https://github.com/tkoyama010/readme-i18n-check/actions/workflows/test.yml/badge.svg)](https://github.com/tkoyama010/readme-i18n-check/actions/workflows/test.yml)
[![README i18n Check](https://github.com/tkoyama010/readme-i18n-check/actions/workflows/readme-i18n-check.yml/badge.svg)](https://github.com/tkoyama010/readme-i18n-check/actions/workflows/readme-i18n-check.yml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/tkoyama010/readme-i18n-check/main.svg)](https://results.pre-commit.ci/latest/github/tkoyama010/readme-i18n-check/main)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

<p align="center">
  <a href="README.md">English</a> |
  <a href="README.ja.md">日本語</a>
</p>

ゼロ依存のREADME多言語化ドリフト検出ツール: GitHubネイティブのローカライズREADMEに対する構造パリティ + 古い翻訳の検出。

Python標準ライブラリのみ — サードパーティの実行時依存関係なし。pre-commitフックとGitHub Actionの両方で動作します。

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

多言語README（例: `README.md`、`README.ja.md`、`README.zh_CN.md`）を持つプロジェクトは2つのドリフト問題に直面します:

1. **構造ドリフト** — 翻訳にセクションが欠落したり追加されたり、見出しが英語のREADMEから逸脱したりする。
2. **コンテンツドリフト** — 英語のREADMEが更新されたが翻訳が更新されておらず、古いままになる。

このツールは両方をCIとpre-commitで自動的に検出し、レビュアーの目に頼るのではなくドリフトを表面化させます。

## Install

Python 3.9以上以外のインストールは不要です。パッケージはサードパーティの依存関係を使用しません（Python標準ライブラリのみ）。

## Usage

### Pre-commit Hook

`.pre-commit-config.yaml` に以下を追加してください:

```yaml
repos:
  - repo: https://github.com/tkoyama010/readme-i18n-check
    rev: v0.1.0  # 最新のタグを使用してください
    hooks:
      - id: check-readme-i18n
```

pre-commitフックは構造パリティチェックのみ（`--no-stale-check`）を実行し、ステージされた変更に対する偽陽性を回避します。

### GitHub Action

ワークフローに以下を追加してください:

```yaml
steps:
  - uses: actions/checkout@v4
    with:
      fetch-depth: 0  # 古い翻訳の検出に必要です

  - uses: tkoyama010/readme-i18n-check@v0.1.0
    with:
      # allowlist: .github/readme-i18n-allowlist  # 任意
      # no-stale-check: 'false'                   # デフォルト: false
      # repo-root: .                               # デフォルト: 自動検出
```

### Command Line

```bash
python -m check_readme_i18n [OPTIONS]
```

オプション:

- `--allowlist FILE` — 古い翻訳チェックから除外するファイル名をリストしたファイル（1行1ファイル名、`#`コメント可能）
- `--no-stale-check` — 古い翻訳（gitコミット日付）チェックをスキップ
- `--repo-root PATH` — リポジトリルート（省略時はgitで自動検出）

終了コード: 0 = 成功、1 = ドリフト検出、2 = 設定エラー。

## Checks

### Structural Parity

`README.md` と各 `README.<lang>.md` から見出しレベル（H1-H6）を抽出します。リストは数と位置ごとのレベルが一致する必要があります。見出しの*テキスト*は異なる（翻訳されている）ことを許容しつつ、欠落、追加、再構築されたセクションを検出します。

### Stale Translation

各ローカライズREADMEのgitコミットタイムスタンプを `README.md` と比較します。翻訳の最終コミットが英語READMEの最新変更より前の場合、古い翻訳としてフラグが立てられます。GitHub Actionsのチェックアウトで `fetch-depth: 0` が必要です。

### Allowlist

古い翻訳チェックから除外するファイル名をリストしたファイル。1行1ファイル名、`#`コメント可能。英語READMEの変更が表面的（例: バッジURL）で翻訳の更新が不要な場合に使用します。

allowlistファイルの例:

```
# 翻訳更新が不要な表面的な変更
README.ja.md
```

## Contributing

貢献を歓迎します！[GitHub](https://github.com/tkoyama010/readme-i18n-check/issues) でissueまたはプルリクエストを開いてください。

## License

[MIT](LICENSE) © Tetsuo Koyama
