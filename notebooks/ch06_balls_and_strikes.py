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
        # Chapter 6: Balls and Strikes Effects / ボール・ストライク効果

        **原著**: *Analyzing Baseball Data with R, 3rd ed.* Chapter 6
        **原著URL**: https://beanumber.github.io/abdwr3e/ch06-balls-strikes.html

        ## 概要
        - カウント別打者有利度の定量化
        - ストライクゾーンのヒートマップ可視化
        - Statcast の `plate_x` / `plate_z` を使った分析
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
    from src.baseball.data import load_statcast
    return Path, alt, load_statcast, mo, pl, sys


@app.cell
def _(mo):
    mo.md(
        """
        ## TODO
        1. `load_statcast()` でシーズンデータを取得
        2. `plate_x` / `plate_z` でストライクゾーンヒートマップを作成
        3. カウント別の期待値差を altair で可視化

        ```python
        # ストライクゾーンヒートマップ例
        alt.Chart(pitches).mark_rect().encode(
            x=alt.X("plate_x:Q", bin=alt.Bin(step=0.25)),
            y=alt.Y("plate_z:Q", bin=alt.Bin(step=0.25)),
            color=alt.Color("mean(is_strike):Q", scale=alt.Scale(scheme="reds")),
        )
        ```
        """
    )
    return


if __name__ == "__main__":
    app.run()
