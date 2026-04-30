# Analyzing Baseball Data with R — Python Reproduction

*Analyzing Baseball Data with R (3rd ed.)* の内容を Python (uv + marimo) で再現するプロジェクト。

- **原著**: https://beanumber.github.io/abdwr3e/
- **言語変換**: R → Python
- **ノートブック**: [marimo](https://marimo.io)
- **パッケージ管理**: [uv](https://docs.astral.sh/uv/)

## Quick Start

```bash
uv run marimo edit notebooks/ch01_baseball_datasets.py
```

## Structure

| ディレクトリ | 内容 |
| ----------- | ---- |
| `notebooks/` | marimoノートブック（1ファイル = 1章） |
| `docs/` | HTMLエクスポート（GitHub Pages で公開） |
| `src/baseball/` | 再利用モジュール |
| `data/` | データキャッシュ（gitignore済み） |

## Chapters

公開済みの章は **Published** 列のリンクから閲覧できます。

| # | 原著タイトル | Python ノートブック | Published |
|---|------------|-------------------|-----------|
| 1 | The Baseball Datasets | `ch01_baseball_datasets.py` | [→ 公開ページ](https://kinoco313.github.io/abdwr-python/ch01_baseball_datasets.html) |
| 4 | The Relation Between Runs and Wins | `ch04_runs_and_wins.py` | [→ 公開ページ](https://kinoco313.github.io/abdwr-python/ch04_runs_and_wins.html) |
