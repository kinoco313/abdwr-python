# CLAUDE.md — Analyzing Baseball Data with R: Python Reproduction

## Project Overview

*Analyzing Baseball Data with R (3rd ed.)* を Python (uv + marimo) で再現するプロジェクト。
全15章 + 付録3本を対象に、R のコードを Python で書き直し、日本語解説ドキュメントを整備する。

- **原著サイト**: https://beanumber.github.io/abdwr3e/
- **環境**: Docker コンテナ（Python 3.12 + uv）
- **ノートブック**: marimo（`notebooks/`）
- **解説ドキュメント**: 日本語訳マークダウン（`docs/`）

## ディレクトリ構成

```
abdwr-python/
├── notebooks/          # marimoノートブック（1ファイル = 1章）
├── docs/               # 日本語訳マークダウン
├── src/baseball/       # 再利用可能なモジュール
├── data/               # データファイル（gitignore済み）
├── Dockerfile
├── docker-compose.yml
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
- **docs/**: 対応する日本語解説マークダウン（`ch01_*.md`）
- サブフォルダを新設しない（data/ と src/ 配下を除く）

### 2. R → Python 対応方針

| R パッケージ       | Python 相当                        |
| ----------------- | ---------------------------------- |
| `Lahman`          | `pybaseball` (lahman data)         |
| `dplyr` / `tidyr` | **`polars`**（pandas 禁止）        |
| `ggplot2`         | **`altair`**（plotly 禁止）        |
| `Shiny`           | `marimo` UI elements               |
| `Quarto`          | `marimo export html`               |
| `DBI` / `RSQLite` | `duckdb`                           |
| `baseballr`       | `pybaseball`                       |

### 3. データ取得
- `pybaseball` で Lahman / Retrosheet / Statcast データを取得
- 取得済みデータは `data/` に Parquet 形式でキャッシュ
- `data/` はすべて gitignore（生データをリポジトリに含めない）

### 4. marimoの使い方
```bash
# 開発（コンテナ内）
uv run marimo edit --host 0.0.0.0 --port 2718 --no-token

# 特定ノートブックを開く
uv run marimo edit notebooks/ch01_baseball_datasets.py

# アプリとして実行
uv run marimo run notebooks/ch01_baseball_datasets.py

# ホストマシンから開く場合（docker-compose）
open http://localhost:2718
```

### 5. No Code Duplication
- 2度書いたら `src/baseball/` に切り出す
- ノートブックは `src/baseball` からインポートする

### 6. 章15（Shiny → marimo apps）の扱い
原著の Shiny アプリを `mo.ui.*` 要素で再現する。
`mo.ui.slider`, `mo.ui.dropdown`, `mo.ui.dataframe` などを活用。

## Coding Standards

### Python Style
- 型ヒントを関数に付ける
- `ruff` でフォーマット・リント
- `pathlib.Path` を使う（文字列パス禁止）
- Parquet 保存: `df.write_parquet(DATA_DIR / "file.parquet")`
- **pandas 禁止** / **plotly 禁止**（pybaseball の返り値変換用途のみ内部利用可）

### Imports
```python
from pathlib import Path

import polars as pl
import altair as alt
import marimo as mo

from baseball.data import load_lahman
```

### データハンドリング
```python
from src.baseball.data import DATA_DIR

# 取得済みならキャッシュを使う
cache = DATA_DIR / "batting.parquet"
if not cache.exists():
    df = pybaseball.batting_stats_bref(...)
    df.to_parquet(cache)
else:
    df = pd.read_parquet(cache)
```

## Workflow

1. `docs/chXX_*.md` で日本語解説を書く（原著を参照・翻訳）
2. `notebooks/chXX_*.py` で Python 再現コードを実装
3. 再利用コードは `src/baseball/` に切り出してテスト
4. `git add -A && git commit -m "add: chXX ..."` で保存

## Project-Specific Data Sources

- **Lahman Database**: 年次集計 (batting, pitching, fielding, teams)
  - 取得: `pybaseball.lahman.batting()` など
- **Retrosheet**: イベントレベルデータ（打席単位）
  - 取得: `pybaseball.retrosheet_game(year)` 
- **Statcast**: トラッキングデータ（投球・打球物理量）
  - 取得: `pybaseball.statcast(start_dt, end_dt)`
- **FanGraphs**: セイバーメトリクス指標
  - 取得: `pybaseball.batting_stats(year)` / `pybaseball.pitching_stats(year)`

## Anti-patterns to Avoid

- ❌ データファイルをコミットする
- ❌ `pip install`（`uv add` を使う）
- ❌ ノートブック間でコードをコピペする
- ❌ `import pandas as pd` をノートブックに書く（pybaseball 変換のみ許容）
- ❌ `import plotly` をノートブックに書く
- ❌ `print()` デバッグを残す（`mo.md()` で表示する）
- ❌ R のコードをコメントで残しっぱなしにする
