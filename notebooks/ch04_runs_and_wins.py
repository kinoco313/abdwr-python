import marimo

__generated_with = "0.23.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    # Chapter 4: The Relation Between Runs and Wins / 得点と勝利の関係

    **原著**: *Analyzing Baseball Data with R, 3rd ed.* Chapter 4

    **原著URL**: https://beanumber.github.io/abdwr3e/04-pythagoras.html

    ## この章でできること

    - 得点（RS）と失点（RA）だけからチームの勝率を予測する **ピタゴラス勝率** を計算できる
    - 得失点差と勝率の間に強い線形関係があることを、散布図と回帰直線で確認できる
    - **単回帰モデル** を使って「何点の得失点差で1勝が増えるか」を推定できる
    - 残差（予測との誤差）を分析して、"勝負強さ"や"運"で勝ちすぎたチームを特定できる
    - ピタゴラス勝率の指数（1.83 vs 2.0 vs 最適値）を比較して、モデルの当てはまりを評価できる

    ## 概要

    本章で使う主な略語：

    | 略語 | 正式名称 | 意味 |
    |------|----------|------|
    | RS | Runs Scored | 得点 |
    | RA | Runs Allowed | 失点 |
    | RD | Run Differential | 得失点差（RS − RA） |
    | Wpct | Winning Percentage | 勝率 |

    $$W\% = \frac{RS^{1.83}}{RS^{1.83} + RA^{1.83}}$$
    """)
    return


@app.cell
def _():
    import altair as alt
    import numpy as np
    import polars as pl
    from scipy.stats import linregress

    from baseball.data import load_lahman_teams
    from baseball.utils import pythagorean_expectation

    return alt, linregress, load_lahman_teams, np, pl, pythagorean_expectation


@app.cell
def _(load_lahman_teams, pl, pythagorean_expectation):
    teams = (
        load_lahman_teams()
        .filter(pl.col("yearID") >= 1901)
        .with_columns(
            [
                (pl.col("W") / (pl.col("W") + pl.col("L"))).alias("win_pct"),
                pythagorean_expectation(pl.col("R"), pl.col("RA")).alias("pyth_pct"),
            ]
        )
    )
    teams.select(["yearID", "teamID", "W", "L", "R", "RA", "win_pct", "pyth_pct"])
    return (teams,)


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
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## ピタゴラス勝率はどれくらい外れる？ / Prediction Error Analysis

    ピタゴラス勝率はあくまで「得失点から期待される勝率」であり、実際の勝率とは一致しない。
    その誤差（実際の勝率 − ピタゴラス勝率）を**残差**と呼ぶ。

    - **残差 > 0**：予測より多く勝った ＝ 接戦に強い・ブルペンが優秀など「運やスキル」で上振れ
    - **残差 < 0**：予測より少なく勝った ＝ 大勝・大敗が多く「得点効率が悪い」状態

    残差の分布を見ることで、ピタゴラス勝率のモデルとしての精度と限界が分かる。
    """)
    return


@app.cell
def _(alt, pl, teams):
    teams_resid = teams.with_columns(
        (pl.col("win_pct") - pl.col("pyth_pct")).alias("residual")
    )

    resid_hist = (
        alt.Chart(teams_resid)
        .mark_bar()
        .encode(
            x=alt.X(
                "residual:Q", bin=alt.Bin(maxbins=40), title="残差（実際 − ピタゴラス）"
            ),
            y=alt.Y("count()", title="チーム数"),
            tooltip=["count()"],
        )
        .properties(title="ピタゴラス勝率残差の分布", width=500, height=300)
    )
    resid_hist
    return (teams_resid,)


@app.cell
def _(mo, pl, teams_resid):
    top_over = (
        teams_resid.sort("residual", descending=True)
        .select(
            ["yearID", "teamID", "W", "L", "R", "RA", "win_pct", "pyth_pct", "residual"]
        )
        .head(10)
    )
    top_under = (
        teams_resid.sort("residual")
        .select(
            ["yearID", "teamID", "W", "L", "R", "RA", "win_pct", "pyth_pct", "residual"]
        )
        .head(10)
    )

    mo.vstack(
        [
            mo.md("### オーバーパフォーマンス上位10チーム"),
            top_over.with_columns(
                [
                    pl.col("win_pct").round(3),
                    pl.col("pyth_pct").round(3),
                    pl.col("residual").round(3),
                ]
            ),
            mo.md("### アンダーパフォーマンス上位10チーム"),
            top_under.with_columns(
                [
                    pl.col("win_pct").round(3),
                    pl.col("pyth_pct").round(3),
                    pl.col("residual").round(3),
                ]
            ),
        ]
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 得失点差と勝率の線形回帰 / Linear Regression: Run Differential → Win Pct

    得失点差（RD: Run Differential = RS − RA）と勝率（win_pct）の間には強い線形関係がある。

    係数から「何得失点差で勝率が 1/162 上がるか（= 1勝増えるか）」を推定できる。
    """)
    return


@app.cell
def _(alt, pl, teams):
    teams_rd = teams.with_columns((pl.col("R") - pl.col("RA")).alias("run_diff"))

    rd_chart = (
        alt.Chart(teams_rd)
        .mark_point(opacity=0.3, size=20)
        .encode(
            x=alt.X("run_diff:Q", title="得失点差 (RS − RA)"),
            y=alt.Y("win_pct:Q", title="勝率"),
            tooltip=["yearID:Q", "teamID:N", "win_pct:Q", "run_diff:Q"],
        )
        .properties(title="得失点差 vs 勝率", width=500, height=400)
    )
    rd_chart + rd_chart.transform_regression("run_diff", "win_pct").mark_line(
        color="red"
    )
    return (teams_rd,)


@app.cell
def _(linregress, mo, teams_rd):
    rd = teams_rd["run_diff"].to_numpy()
    wpct = teams_rd["win_pct"].to_numpy()
    slope, intercept, r_value, p_value, std_err = linregress(rd, wpct)

    # 1勝 = 162試合中1試合増 = 勝率 1/162 の増加
    runs_per_win = (1 / 162) / slope

    r_sq = r_value**2
    mo.md(f"""
    ### 回帰結果

    | 指標 | 値 |
    |------|-----|
    | 切片（intercept） | {intercept:.4f} |
    | 傾き（slope） | {slope:.5f} |
    | **決定係数 R²** | **{r_sq:.4f}** |
    | p値 | {p_value:.2e} |
    | **1勝増やすのに必要な得失点差** | **{runs_per_win:.1f} 点** |

    → 得失点差が約 **{runs_per_win:.1f} 点**多くなると、勝率が1勝分（≒1/162）増える計算になる。

    #### 決定係数 R²（R-squared）とは

    単回帰では **R² = 相関係数²** が成り立つ（`r_value` の二乗がそのまま R²）。

    つまり R² は、「得失点差と勝率がどれだけ連動しているか」を 0〜1 で表した値。

    - **0** → 得失点差が高くても低くても勝率はバラバラ（まったく連動していない）
    - **1** → 得失点差が大きいチームほど必ず勝率も高い（完全に連動している）

    今回: 相関係数 r = {r_value:.4f}、R² = {r_sq:.4f}
    → 得失点差と勝率は非常に強く連動しており、{r_sq * 100:.0f}% の連動を線形関係で捉えられている。
    """)
    return intercept, slope


@app.cell
def _(mo):
    mo.md(r"""
    ## ピタゴラス勝率の予測精度は年によって変わる？ / Prediction Accuracy by Season

    残差の絶対値の平均（MAE: Mean Absolute Error）をシーズンごとに集計する。
    MAE が大きい年は「得失点と勝率がズレやすかった年」、小さい年は「ピタゴラス勝率がよく当たった年」を意味する。

    運や打線の集中度など、年ごとの傾向の違いが見えてくる。
    """)
    return


@app.cell
def _(alt, pl, teams_resid):
    yearly_resid = (
        teams_resid.filter(pl.col("yearID") >= 2001)
        .group_by("yearID")
        .agg(
            [
                pl.col("residual").mean().alias("mean_resid"),
                pl.col("residual").abs().mean().alias("mae_resid"),
            ]
        )
        .sort("yearID")
    )

    base = alt.Chart(yearly_resid).encode(x=alt.X("yearID:O", title="シーズン"))

    mae_line = base.mark_line(point=True, color="steelblue").encode(
        y=alt.Y("mae_resid:Q", title="残差の絶対平均（MAE）"),
        tooltip=["yearID:O", "mae_resid:Q"],
    )

    mae_line.properties(
        title="年次別 ピタゴラス勝率残差の絶対平均",
        width=600,
        height=300,
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## ピタゴラス指数の最適化 / Finding the Optimal Pythagorean Exponent

    Bill James が最初に提案した指数は **2** だったが、実際のデータに合う最適な指数は異なる。

    W/L と R/RA の関係式を対数変換すると線形になる性質を使う：

    $$\log\!\left(\frac{W}{L}\right) \approx k \cdot \log\!\left(\frac{R}{RA}\right)$$

    切片なしの線形回帰で $k$ を推定する。
    """)
    return


@app.cell
def _(mo, np, pl, teams):
    teams_log = teams.filter(
        (pl.col("W") > 0) & (pl.col("L") > 0) & (pl.col("R") > 0) & (pl.col("RA") > 0)
    ).with_columns(
        [
            (pl.col("W") / pl.col("L")).log().alias("log_w_ratio"),
            (pl.col("R") / pl.col("RA")).log().alias("log_r_ratio"),
        ]
    )

    log_r = teams_log["log_r_ratio"].to_numpy()
    log_w = teams_log["log_w_ratio"].to_numpy()
    # 切片なし線形回帰: k = Σ(x*y) / Σ(x²)
    k_opt = float(np.dot(log_r, log_w) / np.dot(log_r, log_r))

    mo.md(f"""
    ### 推定結果

    | 指数 | 値 | 出典 |
    |------|-----|------|
    | Bill James オリジナル | 2.00 | 経験則 |
    | 本書推奨値 | 1.83 | 後続研究 |
    | **データから推定（1901年以降）** | **{k_opt:.3f}** | 本分析 |

    → 実測値は **約 {k_opt:.2f}** で、オリジナルの 2 より小さい。
    現代野球のデータでは **1.82〜1.83** 付近に収束することが多い。
    """)
    return (k_opt,)


@app.cell
def _(mo):
    mo.md(r"""
    ## 線形モデル vs ピタゴラスモデルの精度比較 / Model Comparison: RMSE

    2つのモデルの予測誤差（RMSE: Root Mean Square Error、二乗平均平方根誤差）を比較する。

    $$\text{RMSE} = \sqrt{\frac{1}{N}\sum_{i}(\hat{Wpct}_i - Wpct_i)^2}$$

    - RMSE が小さい → 予測が実際の勝率に近い
    - 68% の誤差が ±1×RMSE 以内、95% が ±2×RMSE 以内（正規分布の場合）
    """)
    return


@app.cell
def _(intercept, k_opt, mo, np, pl, pythagorean_expectation, slope, teams_rd):
    teams_cmp = teams_rd.with_columns(
        [
            (pl.col("win_pct") - (intercept + slope * pl.col("run_diff"))).alias(
                "resid_linear"
            ),
            (
                pl.col("win_pct")
                - pythagorean_expectation(pl.col("R"), pl.col("RA"), exp=2.0)
            ).alias("resid_pyth2"),
            (
                pl.col("win_pct")
                - pythagorean_expectation(pl.col("R"), pl.col("RA"), exp=k_opt)
            ).alias("resid_pyth_opt"),
        ]
    )

    def rmse(col: str) -> float:
        return float(np.sqrt(teams_cmp[col].pow(2).mean()))

    rmse_linear = rmse("resid_linear")
    rmse_pyth2 = rmse("resid_pyth2")
    rmse_opt = rmse("resid_pyth_opt")

    n = len(teams_cmp)
    within1_linear = int((teams_cmp["resid_linear"].abs() < rmse_linear).sum())
    within2_linear = int((teams_cmp["resid_linear"].abs() < 2 * rmse_linear).sum())

    mo.md(f"""
    ### RMSE 比較

    | モデル | RMSE | ±1×RMSE 以内 | ±2×RMSE 以内 |
    |--------|------|-------------|-------------|
    | 線形回帰（RD → Wpct） | {rmse_linear:.4f} | {within1_linear / n:.1%} | {within2_linear / n:.1%} |
    | ピタゴラス（k=2.00） | {rmse_pyth2:.4f} | — | — |
    | ピタゴラス（k={k_opt:.2f}） | {rmse_opt:.4f} | — | — |

    → 精度はほぼ同等。しかしピタゴラスモデルは **勝率が必ず 0〜1 に収まる** という
    理論的に望ましい性質があるため、実用上はピタゴラスが好まれる。
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 1勝に必要な得失点差 / How Many Runs for a Win?

    「失点 $RA$ を固定したまま、得点 $RS$ をほんの少し増やしたとき、勝率はどれだけ上がるか」を計算すると、
    1勝増やすのに必要な追加得点（IR/W: Incremental Runs per Win）が求まる。

    数学的には $W\%$ を $RS$ で偏微分すると $\dfrac{dW\%}{dRS} = \dfrac{\Delta 勝率}{\Delta RS}$、
    つまり「RSを1増やしたら勝率がいくつ上がるか」が得られる。
    知りたいのはその逆、「勝率を1勝分上げるのにRSがいくつ必要か」＝ $\dfrac{\Delta RS}{\Delta 勝率}$ なので、逆数を取る。

    Ralph Caola（2003）の公式：

    $$\frac{IR}{W} = \frac{1}{dW\%/dRS} = \frac{(RS^2 + RA^2)^2}{2 \cdot RS \cdot RA^2}$$

    ここで $RS$, $RA$ は**1試合あたりの**得点・失点。
    """)
    return


@app.cell
def _(mo, np, pl):
    def ir_per_win(rs: float, ra: float) -> float:
        return (rs**2 + ra**2) ** 2 / (2 * rs * ra**2)

    rs_vals = np.arange(3.0, 6.5, 0.5)
    ra_vals = np.arange(3.0, 6.5, 0.5)

    ir_table = pl.DataFrame(
        [
            {"RS/G": rs, "RA/G": ra, "IR/W": round(ir_per_win(rs, ra), 1)}
            for rs in rs_vals
            for ra in ra_vals
        ]
    )

    mo.vstack(
        [
            mo.md(r"""
        ### 1勝に必要な得失点差（試合あたり RS/RA 別）

        現代 MLB の平均的な得点環境（RS ≈ RA ≈ 4.5〜5.0）では、
        約 **10 得失点差** で 1 勝増える（「10点ルール」の理論的根拠）。

        **直感に反する点**: RS/G が低いチーム（得点力が低いチーム）ほど IR/W が小さくなる。
        つまり「得点力が低いチームほど、少ない追加得点で1勝増やせる」。

        これはピタゴラス勝率の式 $W\% = RS^2 / (RS^2 + RA^2)$ の性質によるもので、
        RS が大きくなるほど「1点追加したときの勝率の上がり幅」が小さくなる。

        RA=5.0 で固定した場合の例：

        | RS/G | ピタゴラス勝率 | RS/G を +0.5 したときの勝率増加 |
        |------|--------------|-------------------------------|
        | 4.5 | 44.8% | +5.2pt（4.5 → 5.0）|
        | 5.0 | 50.0% | +4.8pt（5.0 → 5.5）|
        | 5.5 | 54.8% | +4.4pt（5.5 → 6.0）|

        RS/G が低い領域では同じ得点上乗せでも勝率が大きく上がる。
        RS/G が高くなるにつれてその上がり幅が小さくなるため、1勝に必要な追加点（IR/W）が増える。
        """),
            ir_table,
        ]
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
