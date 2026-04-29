# CLAUDE.md — Analyzing Baseball Data with R: Python Reproduction

## Project Overview

*Analyzing Baseball Data with R (3rd ed.)* を Python (uv + marimo) で再現するプロジェクト。
全15章 + 付録3本を対象に、R のコードを Python で書き直し、日本語解説ドキュメントを整備する。

- **原著サイト**: https://beanumber.github.io/abdwr3e/
- **環境**: Python 3.12 + uv（ローカル）
- **ノートブック**: marimo（`notebooks/`）
- **解説ドキュメント**: marimo エクスポート HTML（`docs/`）

## 出版ビジョン

このリポジトリは将来的に入門書として出版されることを目指している。

**想定読者**:
- Python でモダンなデータ分析を学びたい人
- 大学教養レベル（統計検定2級相当）の統計学を学びたい人
- 野球が好きで、セイバーメトリクスに興味がある人

**執筆スタンス**:
- 初学者が「？」となりそうな概念は、教科書的な定義より「このデータでは何を意味するか」をそのセルの変数名で具体的に説明する
- 専門用語は日常語で直感的に言い換えてから導入する（例：「説明できる」→「連動している」）
- 数式を出すなら直後に日本語の直感的解釈を添える
- 各章の冒頭に「この章でできること」を箇条書きで示す

## ディレクトリ構成

```
abdwr-python/
├── notebooks/          # marimoノートブック（1ファイル = 1章、ch01_*.py の命名）
├── docs/               # marimoエクスポートHTML（ch01_*.html の命名）
├── src/baseball/       # 再利用可能なモジュール
│   ├── data.py         # データ取得・キャッシュ関数
│   └── utils.py        # 汎用ユーティリティ
├── data/               # データファイル（gitignore済み、Parquetキャッシュ）
└── pyproject.toml
```

## Core Technology

### marimo（Jupyter の代わりに）
- Pure Python ファイル → Git フレンドリー
- リアクティブ実行 → hidden state なし
- 組み込み UI 要素 → Shiny 相当をネイティブに実現

### uv（pip の代わりに）
- 高速・再現性の高いパッケージ管理
- `uv run` で仮想環境を意識せず実行

## Project Rules

### 1. ファイル組織
- **notebooks/**: 探索・レポート専用（`ch01_*.py` の命名）
- **src/baseball/**: 再利用コードはすべてモジュールへ
- **docs/**: marimo エクスポート HTML（`ch01_*.html`）
- サブフォルダを新設しない（data/ と src/ 配下を除く）

### 2. R → Python 対応方針

| R パッケージ       | Python 相当                        |
| ----------------- | ---------------------------------- |
| `Lahman`          | `lahman` パッケージ                |
| `dplyr` / `tidyr` | **`polars`**（pandas 禁止）        |
| `ggplot2`         | **`altair`**（plotly 禁止）        |
| `Shiny`           | `marimo` UI elements               |
| `Quarto`          | `marimo export html`               |
| `DBI` / `RSQLite` | `duckdb`                           |
| `baseballr`       | `pybaseball`                       |

### 3. データ取得
- `lahman` パッケージで Lahman データを取得
- `pybaseball` で Retrosheet / Statcast / FanGraphs データを取得
- 取得済みデータは `data/` に Parquet 形式でキャッシュ（`src/baseball/data.py` の `_cached()` を使う）
- `data/` はすべて gitignore（生データをリポジトリに含めない）

### 4. marimoの使い方
```bash
# 開発
uv run marimo edit notebooks/ch01_baseball_datasets.py

# 全ノートブックをまとめて開く
uv run marimo edit --host 0.0.0.0 --port 2718 --no-token

# HTMLエクスポート（docs/へ）
uv run marimo export html notebooks/ch01_baseball_datasets.py -o docs/ch01_baseball_datasets.html
```

### 5. No Code Duplication
- 2度書いたら `src/baseball/` に切り出す
- ノートブックは `src/baseball` からインポートする

### 6. 章15（Shiny → marimo apps）の扱い
原著の Shiny アプリを `mo.ui.*` 要素で再現する。
`mo.ui.slider`, `mo.ui.dropdown`, `mo.ui.dataframe` などを活用。

### 7. ノートブックの記述スタイル
- 概要セクション（冒頭の `mo.md()`）に、その章で使う略語の一覧表を入れる
- 例：RS（Runs Scored: 得点）、RA（Runs Allowed: 失点）、RD（Run Differential: 得失点差）
- 略語は本文中の**初出箇所**でも `略語（正式名称）` の形で併記する
- import は各セルに分散させず、冒頭の imports セルに集約する

## Coding Standards

### Python Style
- 型ヒントを関数に付ける
- `ruff` でフォーマット・リント
- `pathlib.Path` を使う（文字列パス禁止）
- Parquet 保存: `df.write_parquet(DATA_DIR / "file.parquet")`
- **pandas 禁止** / **plotly 禁止**（pybaseball / lahman の返り値変換用途のみ内部利用可）

### Imports
```python
from pathlib import Path

import polars as pl
import altair as alt
import marimo as mo

from baseball.data import load_lahman_batting
```

### データハンドリング
`src/baseball/data.py` の `_cached()` ヘルパーを使う。新しいデータソースを追加する場合は同ファイルに関数を追加する。

```python
# src/baseball/data.py のパターン
def load_lahman_batting() -> pl.DataFrame:
    import lahman
    return _cached("lahman_batting", lambda: _from_pybaseball(lahman.batting))

# ノートブックからの使い方
from baseball.data import load_lahman_batting
batting = load_lahman_batting()
```

## Workflow

1. `notebooks/chXX_*.py` で Python 再現コードを実装（marimo）
2. 再利用コードは `src/baseball/` に切り出してテスト
3. `uv run marimo export html notebooks/chXX_*.py -o docs/chXX_*.html` でHTMLエクスポート
4. `git add -A && git commit -m "add: chXX ..."` で保存

## Project-Specific Data Sources

- **Lahman Database**: 年次集計 (batting, pitching, fielding, teams)
  - 取得: `from baseball.data import load_lahman_batting` など
- **Retrosheet**: イベントレベルデータ（打席単位）
  - 取得: `pybaseball.retrosheet_game(year)`
- **Statcast**: トラッキングデータ（投球・打球物理量）
  - 取得: `pybaseball.statcast(start_dt, end_dt)`
- **FanGraphs**: セイバーメトリクス指標
  - 取得: `from baseball.data import load_fangraphs_batting`

## Anti-patterns to Avoid

- ❌ データファイルをコミットする
- ❌ `pip install`（`uv add` を使う）
- ❌ ノートブック間でコードをコピペする
- ❌ `import pandas as pd` をノートブックに書く（pybaseball / lahman 変換のみ許容）
- ❌ `import plotly` をノートブックに書く
- ❌ `print()` デバッグを残す（`mo.md()` で表示する）
- ❌ R のコードをコメントで残しっぱなしにする
- ❌ `mo.ui.dataframe()` / `mo.ui.table()` でデータフレームを表示する（静的 HTML エクスポートで動かないため）。データフレームはセルの最終式として変数名で参照する（例: `df` や `df.head(10)`）
- ❌ `from src.baseball.data import` と書く（正しくは `from baseball.data import`）