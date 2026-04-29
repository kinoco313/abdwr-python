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
        # Chapter 9: Simulation / シミュレーション

        **原著**: *Analyzing Baseball Data with R, 3rd ed.* Chapter 9
        **原著URL**: https://beanumber.github.io/abdwr3e/09-simulation.html

        ## 概要
        - モンテカルロシミュレーションによるゲーム結果予測
        - ハーフイニングのシミュレーション
        - シーズン成績のシミュレーション
        """
    )
    return


@app.cell
def _():
    import polars as pl
    import altair as alt
    import numpy as np
    from scipy import stats
    return alt, np, pl, stats


@app.cell
def _(mo):
    n_sim = mo.ui.slider(start=1000, stop=50000, step=1000, value=10000, label="シミュレーション回数")
    n_sim
    return (n_sim,)


@app.cell
def _(alt, mo, np, n_sim, pl):
    rng = np.random.default_rng(42)
    # 簡易ハーフイニングシミュレーション: 打率.260 の打者9人
    ba = 0.260
    results = []
    for _ in range(n_sim.value):
        outs = runs = 0
        while outs < 3:
            if rng.random() < ba:
                runs += 1
            else:
                outs += 1
        results.append(runs)

    sim_df = pl.DataFrame({"runs": results})
    chart = (
        alt.Chart(sim_df)
        .mark_bar()
        .encode(
            x=alt.X("runs:Q", bin=alt.Bin(step=1), title="得点"),
            y=alt.Y("count()", title="頻度"),
        )
        .properties(title=f"ハーフイニング得点分布 (n={n_sim.value:,})", width=500, height=300)
    )
    mo.vstack([mo.md(f"平均得点: **{sim_df['runs'].mean():.3f}**"), chart])
    return ba, chart, outs, results, rng, runs, sim_df


@app.cell
def _(mo):
    mo.md("## TODO: 実際の打席確率を使ったより精緻なシミュレーターを実装")
    return


if __name__ == "__main__":
    app.run()
