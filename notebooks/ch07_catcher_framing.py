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
        # Chapter 7: Catcher Framing / キャッチャーフレーミング

        **原著**: *Analyzing Baseball Data with R, 3rd ed.* Chapter 7
        **原著URL**: https://beanumber.github.io/abdwr3e/ch07-catcher-framing.html

        ## 概要
        キャッチャーのフレーミング（ボールをストライクに見せる）能力の定量化。

        - ロジスティック回帰によるストライク確率モデル
        - フレーミング価値（Framing Runs）の計算
        - キャッチャーランキング
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
    from sklearn.linear_model import LogisticRegression
    from src.baseball.data import load_statcast
    return LogisticRegression, Path, alt, load_statcast, mo, pl, sys


@app.cell
def _(mo):
    mo.md(
        """
        ## TODO
        1. Statcast データを取得してボーダーライン投球を抽出
        2. ロジスティック回帰でストライク確率を推定
        3. 捕手ごとの Expected Strikes vs Actual Strikes を集計
        4. フレーミングランキングを altair の棒グラフで表示
        """
    )
    return


if __name__ == "__main__":
    app.run()
