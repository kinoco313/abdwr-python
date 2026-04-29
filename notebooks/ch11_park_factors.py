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
        # Chapter 11: Park Factors / 球場補正係数

        **原著**: *Analyzing Baseball Data with R, 3rd ed.* Chapter 11
        **原著URL**: https://beanumber.github.io/abdwr3e/11-sql.html

        ## 概要
        - DuckDB を使ったプレイバイプレイデータの SQL 集計
        - 球場補正係数（Park Factor）の計算
        - 球場特性の可視化
        """
    )
    return


@app.cell
def _():
    import altair as alt
    import duckdb
    import polars as pl

    from baseball.data import DATA_DIR, load_lahman_teams

    return DATA_DIR, alt, duckdb, load_lahman_teams, pl


@app.cell
def _(duckdb, load_lahman_teams, mo):
    con = duckdb.connect()
    teams = load_lahman_teams()
    con.register("teams", teams)
    result = con.execute("""
        SELECT yearID, teamID, park, R, RA, G
        FROM teams
        WHERE yearID >= 2010
        ORDER BY yearID, teamID
    """).pl()
    mo.ui.dataframe(result.to_pandas(), page_size=10)
    return con, result, teams


@app.cell
def _(mo):
    mo.md("## TODO: Retrosheet PBP を DuckDB で集計して球場補正係数を計算・可視化")
    return


if __name__ == "__main__":
    app.run()
