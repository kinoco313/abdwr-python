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
        # Chapter 13: Home Run Hitting / ホームラン打撃分析

        **原著**: *Analyzing Baseball Data with R, 3rd ed.* Chapter 13
        **原著URL**: https://beanumber.github.io/abdwr3e/ch13-home-runs.html

        ## 概要
        - Statcast の打球データ（`launch_speed` / `launch_angle`）
        - ホームラン確率と打球特性の関係
        - Spray Chart（打球方向の分布マップ）
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
        1. `load_statcast()` で打球イベントを取得
        2. `launch_speed` × `launch_angle` の散布図（HR/非HRで色分け）
        3. Spray Chart: `hc_x` / `hc_y` で打球方向を可視化

        ```python
        # Spray Chart 例
        alt.Chart(batted_balls).mark_point(opacity=0.3).encode(
            x=alt.X("hc_x:Q", scale=alt.Scale(domain=[0, 250])),
            y=alt.Y("hc_y:Q", scale=alt.Scale(domain=[0, 250], reverse=True)),
            color=alt.Color("events:N"),
        ).properties(width=400, height=400)
        ```
        """
    )
    return


if __name__ == "__main__":
    app.run()
