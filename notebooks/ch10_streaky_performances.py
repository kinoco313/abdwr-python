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
        # Chapter 10: Exploring Streaky Performances / 連続パフォーマンス分析

        **原著**: *Analyzing Baseball Data with R, 3rd ed.* Chapter 10
        **原著URL**: https://beanumber.github.io/abdwr3e/10-streak.html

        ## 概要
        - 連続安打・無安打の統計的検定
        - ランダムウォークとの比較
        - Joe DiMaggio の 56 試合連続安打の確率評価
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
def _(mo, np, pl):
    # 打率 .325 の打者でランダムシミュレーション
    rng = np.random.default_rng(42)
    ba = 0.325
    n_games = 162
    n_trials = 10_000

    max_streaks = []
    for _ in range(n_trials):
        hits = rng.random(n_games) < ba
        streak = cur = 0
        for h in hits:
            cur = cur + 1 if h else 0
            streak = max(streak, cur)
        max_streaks.append(streak)

    streak_df = pl.DataFrame({"max_streak": max_streaks})
    mo.md(f"平均最長連続安打: **{streak_df['max_streak'].mean():.1f}** 試合  |  中央値: **{streak_df['max_streak'].median():.0f}**")
    return ba, cur, h, hits, max_streaks, n_games, n_trials, rng, streak, streak_df


@app.cell
def _(alt, streak_df):
    alt.Chart(streak_df).mark_bar().encode(
        x=alt.X("max_streak:Q", bin=alt.Bin(step=1), title="最長連続安打数"),
        y=alt.Y("count()", title="頻度"),
    ).properties(title="シーズン最長連続安打分布（シミュレーション）", width=500, height=300)
    return


@app.cell
def _(mo):
    mo.md("## TODO: 実際の打者データで連続記録のランダム性を検定")
    return


if __name__ == "__main__":
    app.run()
