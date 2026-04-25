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
        # Chapter 14: Scientific Presentation with marimo / marimoによるレポート作成

        **原著**: *Analyzing Baseball Data with R, 3rd ed.* Chapter 14 (Quarto)
        **原著URL**: https://beanumber.github.io/abdwr3e/ch14-quarto.html

        ## 概要
        原著では Quarto を使った科学的レポート作成を扱う。
        Python 版では `marimo export` でノートブックを HTML / WASM に変換する。

        ```bash
        # HTML エクスポート
        uv run marimo export html notebooks/ch14_scientific_presentation.py -o report.html

        # WASM（ブラウザで動くインタラクティブレポート）
        uv run marimo export html-wasm notebooks/ch14_scientific_presentation.py -o report_wasm.html
        ```
        """
    )
    return


@app.cell
def _():
    import polars as pl
    import altair as alt
    from baseball.data import load_lahman_teams
    from baseball.utils import pythagorean_expectation
    return alt, load_lahman_teams, pl, pythagorean_expectation


@app.cell
def _(mo):
    mo.callout(
        mo.md("このノートブックは `marimo export html` でそのまま HTML レポートに変換できます。"),
        kind="info",
    )
    return


@app.cell
def _(load_lahman_teams, mo, pl, pythagorean_expectation):
    teams = (
        load_lahman_teams()
        .filter(pl.col("yearID") >= 2010)
        .with_columns([
            (pl.col("W") / (pl.col("W") + pl.col("L"))).alias("win_pct"),
            pythagorean_expectation(pl.col("R"), pl.col("RA")).alias("pyth_pct"),
        ])
        .select(["yearID", "teamID", "W", "L", "R", "RA", "win_pct", "pyth_pct"])
        .sort(["yearID", "teamID"])
    )
    mo.stat(label="対象チーム数", value=str(teams.height))
    return (teams,)


@app.cell
def _(mo):
    mo.md("## TODO: 分析レポートのサンプルを追加（LaTeX数式・図・表を組み合わせた例）")
    return


if __name__ == "__main__":
    app.run()
