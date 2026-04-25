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
        # Chapter 3: Graphics / データ可視化

        **原著**: *Analyzing Baseball Data with R, 3rd ed.* Chapter 3
        **原著URL**: https://beanumber.github.io/abdwr3e/ch03-graphics.html

        ## ggplot2 → altair 対応表

        | ggplot2                    | altair                                          |
        |----------------------------|-------------------------------------------------|
        | `geom_point()`             | `.mark_point()`                                 |
        | `geom_line()`              | `.mark_line()`                                  |
        | `geom_bar(stat="identity")`| `.mark_bar()`                                   |
        | `geom_histogram()`         | `.mark_bar()` + `alt.X(bin=True)`               |
        | `geom_smooth(method="lm")` | `transform_regression()`                        |
        | `facet_wrap(~var)`         | `.facet("var", columns=3)`                      |
        | `aes(color=var)`           | `color="var:N"`                                 |
        | `theme_minimal()`          | `.properties()` + `alt.themes`                  |
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
    from src.baseball.data import load_lahman_batting
    return Path, alt, load_lahman_batting, mo, pl, sys


@app.cell
def _(alt, load_lahman_batting, pl):
    batting = load_lahman_batting()
    season_hr = (
        batting.group_by("yearID")
        .agg(pl.col("HR").sum())
        .sort("yearID")
    )
    chart_hr = (
        alt.Chart(season_hr)
        .mark_line()
        .encode(
            x=alt.X("yearID:Q", title="年"),
            y=alt.Y("HR:Q", title="本塁打数"),
        )
        .properties(title="MLB 年間本塁打数の推移", width=600, height=300)
    )
    chart_hr
    return batting, chart_hr, season_hr


@app.cell
def _(mo):
    mo.md("## TODO: 各種 ggplot2 グラフを altair で再現（散布図・ヒストグラム・ファセット等）")
    return


if __name__ == "__main__":
    app.run()
