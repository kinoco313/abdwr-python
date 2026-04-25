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
        # Chapter 8: Career Trajectories / キャリア軌跡

        **原著**: *Analyzing Baseball Data with R, 3rd ed.* Chapter 8
        **原著URL**: https://beanumber.github.io/abdwr3e/ch08-career-trajectories.html

        ## 概要
        - 年齢と成績の関係（Age Curve）
        - Delta Method によるキャリア軌跡の推定
        - ピーク年齢の分析
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
    import statsmodels.formula.api as smf
    from src.baseball.data import load_lahman_batting
    return Path, alt, load_lahman_batting, mo, pl, smf, sys


@app.cell
def _(load_lahman_batting, pl):
    batting = (
        load_lahman_batting()
        .filter(pl.col("AB") >= 100)
        .select(["playerID", "yearID", "age", "H", "AB"])
        .with_columns(
            (pl.col("H") / pl.col("AB")).alias("avg")
        )
    )
    batting.head()
    return (batting,)


@app.cell
def _(mo):
    mo.md("## TODO: Delta Method で年齢カーブを推定して altair で可視化")
    return


if __name__ == "__main__":
    app.run()
