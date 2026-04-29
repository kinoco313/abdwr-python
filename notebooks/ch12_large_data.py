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
        # Chapter 12: Working with Large Data / 大規模データ処理

        **原著**: *Analyzing Baseball Data with R, 3rd ed.* Chapter 12
        **原著URL**: https://beanumber.github.io/abdwr3e/12-large.html

        ## 概要
        - Polars による高速データ処理（lazy evaluation）
        - DuckDB による SQL クエリ
        - Parquet フォーマットの活用
        - Statcast 複数年データの効率的な処理
        """
    )
    return


@app.cell
def _():
    import altair as alt
    import duckdb
    import polars as pl

    from baseball.data import DATA_DIR

    return DATA_DIR, alt, duckdb, pl


@app.cell
def _(mo):
    mo.md(
        """
        ## Polars Lazy Evaluation

        ```python
        # Lazy frame: 実行計画を最適化してから実行
        result = (
            pl.scan_parquet(DATA_DIR / "statcast_*.parquet")
            .filter(pl.col("events").is_not_null())
            .group_by(["game_year", "player_name"])
            .agg([
                pl.col("launch_speed").mean().alias("avg_exit_velo"),
                pl.col("home_run").sum(),
            ])
            .collect()
        )
        ```
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        "## TODO: 複数年 Statcast データを Polars LazyFrame + DuckDB で処理する例を実装"
    )
    return


if __name__ == "__main__":
    app.run()
