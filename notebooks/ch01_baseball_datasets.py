import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
        # Chapter 1: The Baseball Datasets / 野球データセット入門

        **原著**: *Analyzing Baseball Data with R, 3rd ed.* Chapter 1
        **原著URL**: https://beanumber.github.io/abdwr3e/ch01-bball.html

        ## 概要
        野球データの主要ソースを紹介し、Python (pybaseball) で取得する方法を示す。

        - **Lahman Database**: 年次集計データ（1871年〜現在）
        - **Retrosheet**: イベントレベルのプレイバイプレイデータ
        - **Statcast**: 物理トラッキングデータ（2015年〜）
        - **FanGraphs**: セイバーメトリクス指標
        """
    )
    return


@app.cell
def _():
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path("..").resolve()))
    import polars as pl
    import altair as alt
    import marimo as mo
    from src.baseball.data import load_lahman_batting, load_lahman_teams
    return Path, alt, load_lahman_batting, load_lahman_teams, mo, pl, sys


@app.cell
def _(mo):
    mo.md("## Lahman Database — batting テーブル")
    return


@app.cell
def _(load_lahman_batting, mo):
    batting = load_lahman_batting()
    mo.ui.dataframe(batting.tail(10).to_pandas(), page_size=10)
    return (batting,)


@app.cell
def _(batting, mo):
    mo.md(f"**行数**: {batting.height:,}  |  **列数**: {batting.width}")
    return


@app.cell
def _(mo):
    mo.md("## TODO: Retrosheet / Statcast の取得例を追加")
    return


if __name__ == "__main__":
    app.run()
