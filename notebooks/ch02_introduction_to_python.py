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
        # Chapter 2: Introduction to Python / Python入門

        **原著**: *Analyzing Baseball Data with R, 3rd ed.* Chapter 2 (Introduction to R)
        **原著URL**: https://beanumber.github.io/abdwr3e/ch02-intro-r.html

        ## R → Python / polars 対応表

        | R                                      | Python / polars                              |
        |----------------------------------------|----------------------------------------------|
        | `c(1, 2, 3)`                           | `[1, 2, 3]`                                  |
        | `data.frame(x=1:5, y=...)`             | `pl.DataFrame({"x": range(1,6), "y": ...})`  |
        | `dplyr::filter(df, x > 3)`             | `df.filter(pl.col("x") > 3)`                 |
        | `dplyr::mutate(df, z = x + y)`         | `df.with_columns((pl.col("x") + pl.col("y")).alias("z"))` |
        | `dplyr::group_by(df, g) |> summarise` | `df.group_by("g").agg(...)`                  |
        | `dplyr::arrange(df, desc(x))`          | `df.sort("x", descending=True)`              |
        | `tidyr::pivot_longer()`                | `df.unpivot()`                               |
        | `tidyr::pivot_wider()`                 | `df.pivot()`                                 |
        """
    )
    return


@app.cell
def _():
    import polars as pl
    import altair as alt
    import marimo as mo
    return alt, mo, pl


@app.cell
def _(mo):
    mo.md("## 基本的なデータ操作")
    return


@app.cell
def _(pl):
    # R: data.frame(x = 1:5, y = c(2.3, 4.5, 1.2, 3.8, 5.1))
    df = pl.DataFrame({"x": range(1, 6), "y": [2.3, 4.5, 1.2, 3.8, 5.1]})
    df
    return (df,)


@app.cell
def _(df, pl):
    # R: dplyr::mutate(df, z = x * y) |> dplyr::filter(z > 5)
    result = df.with_columns(
        (pl.col("x") * pl.col("y")).alias("z")
    ).filter(pl.col("z") > 5)
    result
    return (result,)


@app.cell
def _(mo):
    mo.md("## TODO: R との対応コードを章に沿って追加")
    return


if __name__ == "__main__":
    app.run()
