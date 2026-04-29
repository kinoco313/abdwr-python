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
        # Chapter 15: Interactive Apps with marimo / marimoインタラクティブアプリ

        **原著**: *Analyzing Baseball Data with R, 3rd ed.* Chapter 15 (Shiny)
        **原著URL**: https://beanumber.github.io/abdwr3e/15-shiny.html

        ## Shiny → marimo UI 対応表

        | Shiny                | marimo                          |
        |----------------------|---------------------------------|
        | `sliderInput()`      | `mo.ui.slider()`                |
        | `selectInput()`      | `mo.ui.dropdown()`              |
        | `checkboxInput()`    | `mo.ui.checkbox()`              |
        | `textInput()`        | `mo.ui.text()`                  |
        | `renderTable()`      | `mo.ui.dataframe()`             |
        | `renderPlot()`       | altair チャートを直接返す       |
        | `server` / `ui` 分離 | 不要（リアクティブ自動伝播）    |
        """
    )
    return


@app.cell
def _():
    import altair as alt
    import polars as pl

    from baseball.data import load_lahman_batting

    return alt, load_lahman_batting, pl


@app.cell
def _(mo):
    year_range = mo.ui.range_slider(
        start=1900,
        stop=2023,
        value=[2000, 2023],
        step=1,
        label="対象年度",
    )
    stat_select = mo.ui.dropdown(
        options={"本塁打": "HR", "安打": "H", "打点": "RBI", "盗塁": "SB"},
        value="HR",
        label="統計指標",
    )
    mo.hstack([year_range, stat_select])
    return stat_select, year_range


@app.cell
def _(alt, load_lahman_batting, mo, pl, stat_select, year_range):
    batting = load_lahman_batting()
    stat_col = stat_select.value
    season = (
        batting.filter(
            pl.col("yearID").is_between(year_range.value[0], year_range.value[1])
        )
        .group_by("yearID")
        .agg(pl.col(stat_col).sum())
        .sort("yearID")
    )
    chart = (
        alt.Chart(season)
        .mark_bar()
        .encode(
            x=alt.X("yearID:Q", title="年"),
            y=alt.Y(f"{stat_col}:Q", title=stat_select.label),
        )
        .properties(
            title=f"MLB 年間{stat_select.label} ({year_range.value[0]}–{year_range.value[1]})",
            width=600,
            height=350,
        )
    )
    mo.vstack([chart])
    return batting, chart, season, stat_col


@app.cell
def _(mo):
    mo.md("## TODO: 原著の Shiny サンプルアプリを marimo UI で再現")
    return


if __name__ == "__main__":
    app.run()
