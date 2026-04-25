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
        # Chapter 4: The Relation Between Runs and Wins / 得点と勝利の関係

        **原著**: *Analyzing Baseball Data with R, 3rd ed.* Chapter 4
        **原著URL**: https://beanumber.github.io/abdwr3e/ch04-runs-wins.html

        ## 概要
        - ピタゴラス勝率（Pythagorean Win Expectation）
        - 得点・失点から予測勝率を計算
        - 線形回帰による得点と勝利の関係

        $$W\% = \frac{RS^{1.83}}{RS^{1.83} + RA^{1.83}}$$
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
    from src.baseball.data import load_lahman_teams
    from src.baseball.utils import pythagorean_expectation
    return Path, alt, load_lahman_teams, mo, pl, pythagorean_expectation, sys


@app.cell
def _(load_lahman_teams, pl, pythagorean_expectation):
    teams = (
        load_lahman_teams()
        .filter(pl.col("yearID") >= 1901)
        .with_columns([
            (pl.col("W") / (pl.col("W") + pl.col("L"))).alias("win_pct"),
        ])
    )
    win_pct = teams["win_pct"]
    r_col = teams["R"]
    ra_col = teams["RA"]
    teams = teams.with_columns(
        pythagorean_expectation(r_col, ra_col).alias("pyth_pct")
    )
    teams.select(["yearID", "teamID", "W", "L", "R", "RA", "win_pct", "pyth_pct"])
    return ra_col, r_col, teams, win_pct


@app.cell
def _(alt, teams):
    chart = (
        alt.Chart(teams)
        .mark_point(opacity=0.4)
        .encode(
            x=alt.X("pyth_pct:Q", title="ピタゴラス勝率", scale=alt.Scale(zero=False)),
            y=alt.Y("win_pct:Q", title="実際の勝率", scale=alt.Scale(zero=False)),
            tooltip=["yearID:Q", "teamID:N", "win_pct:Q", "pyth_pct:Q"],
        )
        .properties(title="ピタゴラス勝率 vs 実際の勝率", width=500, height=400)
    )
    chart + chart.transform_regression("pyth_pct", "win_pct").mark_line(color="red")
    return (chart,)


@app.cell
def _(mo):
    mo.md("## TODO: 残差分析・オーバーパフォーマンスチーム特定を追加")
    return


if __name__ == "__main__":
    app.run()
