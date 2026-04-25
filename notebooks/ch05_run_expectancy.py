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
        # Chapter 5: Value of Plays Using Run Expectancy / 期待得点による打撃価値

        **原著**: *Analyzing Baseball Data with R, 3rd ed.* Chapter 5
        **原著URL**: https://beanumber.github.io/abdwr3e/ch05-run-expectancy.html

        ## 概要
        - 24状態（塁状況 × アウト数）の期待得点マトリックス
        - 各プレイのラン・バリュー計算
        - 線形重み（Linear Weights）の推定

        24状態 = 塁状況 8通り × アウト数 3通り
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
    from src.baseball.utils import run_expectancy_matrix
    return Path, alt, mo, pl, run_expectancy_matrix, sys


@app.cell
def _(mo):
    mo.md(
        """
        ## TODO
        1. Retrosheet PBP データを取得して期待得点マトリックスを構築
        2. ヒット・四球・三振などのラン・バリューを計算
        3. `run_expectancy_matrix()` でヒートマップ可視化

        ```python
        # ヒートマップ例
        alt.Chart(re_matrix).mark_rect().encode(
            x="outs:O",
            y="base_state:N",
            color=alt.Color("mean_runs:Q", scale=alt.Scale(scheme="blues")),
        )
        ```
        """
    )
    return


if __name__ == "__main__":
    app.run()
