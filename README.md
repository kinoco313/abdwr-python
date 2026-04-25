# Analyzing Baseball Data with R — Python Reproduction

*Analyzing Baseball Data with R (3rd ed.)* の内容を Python (uv + marimo) で再現するプロジェクト。

- **原著**: https://beanumber.github.io/abdwr3e/
- **言語変換**: R → Python
- **ノートブック**: [marimo](https://marimo.io)
- **パッケージ管理**: [uv](https://docs.astral.sh/uv/)

## Quick Start

```bash
# Docker で起動
docker compose up

# ブラウザで開く
open http://localhost:2718
```

```bash
# ローカルで起動（uv インストール済みの場合）
uv run marimo edit notebooks/ch01_baseball_datasets.py
```

## Structure

| ディレクトリ | 内容 |
| ----------- | ---- |
| `notebooks/` | marimoノートブック（1ファイル = 1章） |
| `docs/` | 日本語解説マークダウン |
| `src/baseball/` | 再利用モジュール |
| `data/` | データキャッシュ（gitignore済み） |

## Chapters

| # | 原著タイトル | Python ノートブック |
|---|------------|-------------------|
| 1 | The Baseball Datasets | `ch01_baseball_datasets.py` |
| 2 | Introduction to R | `ch02_introduction_to_python.py` |
| 3 | Graphics | `ch03_graphics.py` |
| 4 | The Relation Between Runs and Wins | `ch04_runs_and_wins.py` |
| 5 | Value of Plays Using Run Expectancy | `ch05_run_expectancy.py` |
| 6 | Balls and Strikes Effects | `ch06_balls_and_strikes.py` |
| 7 | Catcher Framing | `ch07_catcher_framing.py` |
| 8 | Career Trajectories | `ch08_career_trajectories.py` |
| 9 | Simulation | `ch09_simulation.py` |
| 10 | Exploring Streaky Performances | `ch10_streaky_performances.py` |
| 11 | Using a Database to Compute Park Factors | `ch11_park_factors.py` |
| 12 | Working with Large Data | `ch12_large_data.py` |
| 13 | Home Run Hitting | `ch13_home_run_hitting.py` |
| 14 | Making a Scientific Presentation | `ch14_scientific_presentation.py` |
| 15 | Interactive Apps (marimo) | `ch15_marimo_apps.py` |
