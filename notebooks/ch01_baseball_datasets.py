import marimo

__generated_with = "0.23.3"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    # Chapter 1: The Baseball Datasets / 野球データセット入門

    **原著**: *Analyzing Baseball Data with R, 3rd ed.* Chapter 1

    **原著URL**: https://beanumber.github.io/abdwr3e/01-datasets.html

    ## 概要
    野球データの主要ソースを紹介し、Python (pybaseball) で取得する方法を示す。

    | データソース | 粒度 | 期間 | 特徴 |
    |---|---|---|---|
    | **Lahman Database** | シーズン集計 | 1871年〜現在 | 打撃・投球・守備・チーム |
    | **Retrosheet** | 試合ログ | 1871年〜現在 | 1試合単位の詳細記録 |
    | **Statcast** | 投球トラッキング | 2015年〜現在 | 球速・回転数・打球角度 |
    | **FanGraphs** | シーズン集計 | 2002年〜現在 | wRC+, FIP, WAR などの指標 |
    """)
    return


@app.cell
def _():
    import polars as pl
    import altair as alt
    from baseball.data import (
        load_lahman_batting,
        load_statcast,
    )

    return alt, load_lahman_batting, load_statcast, pl


@app.cell
def _(mo):
    mo.md("""
    ## 1. Lahman Database

    最も歴史の深い野球統計データベース。1871年から現在まで、MLB 全選手の
    シーズン集計データを収録。`batting` テーブルの主要列を確認する。

    | 列 | 説明 |
    |---|---|
    | `playerID` | 選手固有ID（lahman形式） |
    | `yearID` | シーズン年 |
    | `teamID` | チームID |
    | `G` | 試合数 |
    | `AB` | 打数 |
    | `H` | 安打 |
    | `HR` | 本塁打 |
    | `RBI` | 打点 |
    | `BB` | 四球 |
    | `SO` | 三振 |
    """)
    return


@app.cell
def _(load_lahman_batting, mo):
    batting = load_lahman_batting()
    latest_year = batting["yearID"].max()
    season_games = batting.filter(batting["yearID"] == latest_year)["G"].max()
    qualifying_ab = int(season_games * 2.7)
    mo.ui.dataframe(batting.tail(20), page_size=10)
    return batting, latest_year, qualifying_ab


@app.cell
def _(batting, mo):
    mo.md(f"""
    **行数**: {batting.height:,}  |  **列数**: {batting.width}
    （1シーズン × 1チーム × 1選手 = 1行）
    """)
    return


@app.cell
def _(batting, latest_year, mo):
    mo.md(f"### 本塁打上位10名（{latest_year}年）")
    top_hr = (
        batting
        .filter(batting["yearID"] == latest_year)
        .sort("HR", descending=True)
        .head(10)
        .select(["playerID", "teamID", "G", "AB", "H", "HR", "RBI", "BB", "SO"])
    )
    mo.ui.dataframe(top_hr)
    return


@app.cell
def _(alt, batting, pl):
    # シーズン総本塁打数の推移（1960年〜）
    hr_trend = (
        batting
        .filter(batting["yearID"] >= 1960)
        .group_by("yearID")
        .agg(pl.col("HR").sum().alias("pl_HR"))
        .sort("yearID")
    )
    chart_hr = (
        alt.Chart(hr_trend)
        .mark_line(point=True)
        .encode(
            x=alt.X("yearID:Q", title="シーズン"),
            y=alt.Y("pl_HR:Q", title="総本塁打数"),
            tooltip=["yearID", "pl_HR"],
        )
        .properties(title="MLB シーズン総本塁打数の推移（1960年〜）", width=640, height=300)
    )
    chart_hr
    return


@app.cell
def _(batting, latest_year, mo, pl, qualifying_ab):
    batting_avg = (
        batting
        .filter((batting["yearID"] == latest_year) & (batting["AB"] >= qualifying_ab))
        .with_columns(
            (pl.col("H") / pl.col("AB")).alias("AVG")
        )
        .sort("AVG", descending=True)
        .head(10)
        .select(["playerID", "teamID", "AB", "H", "HR", "AVG"])
    )

    mo.ui.dataframe(batting_avg)
    return


@app.cell
def _(mo):
    mo.md("""
    ## 2. FanGraphs（現在アクセス不可）

    原著では FanGraphs から wRC+・wOBA・WAR などのセイバーメトリクス指標を取得している。
    ただし 2025年時点で `pybaseball.batting_stats()` が FanGraphs の
    `leaders-legacy.aspx` エンドポイントから **HTTP 403** を受け取るため利用不可。
    pybaseball 2.2.7 が最新版だが未修正。

    代替として Lahman の生データから OBP・SLG・OPS を自前計算する。

    | 指標 | 計算式 |
    |---|---|
    | `OBP` | (H + BB + HBP) / (AB + BB + HBP + SF) |
    | `SLG` | (1B + 2×2B + 3×3B + 4×HR) / AB　※ 1B = H − 2B − 3B − HR |
    | `OPS` | OBP + SLG |
    """)
    return


@app.cell
def _(batting, latest_year, mo, pl, qualifying_ab):
    ops_stats = (
        batting
        .filter((batting["yearID"] == latest_year) & (pl.col("AB") >= qualifying_ab))
        .with_columns([
            ((pl.col("H") + pl.col("BB") + pl.col("HBP").fill_null(0))
             / (pl.col("AB") + pl.col("BB") + pl.col("HBP").fill_null(0) + pl.col("SF").fill_null(0)))
            .alias("OBP"),
            # SLG = Total Bases / AB
            # H で全ヒットを1塁分計上済みなので追加塁数だけ足す
            # (2B:+1, 3B:+2, HR:+3) ≡ 1B + 2×2B + 3×3B + 4×HR を展開した形
            ((pl.col("H") + pl.col("2B") + 2 * pl.col("3B") + 3 * pl.col("HR"))
             / pl.col("AB"))
            .alias("SLG"),
        ])
        .with_columns((pl.col("OBP") + pl.col("SLG")).alias("OPS"))
        .sort("OPS", descending=True)
        .head(20)
        .select(["playerID", "teamID", "AB", "H", "HR", "OBP", "SLG", "OPS"])
    )
    mo.ui.dataframe(ops_stats, page_size=10)
    return (ops_stats,)


@app.cell
def _(alt, ops_stats):
    # OBP vs SLG の散布図（HR でカラー）
    scatter_ops = (
        alt.Chart(ops_stats)
        .mark_circle(size=80, opacity=0.7)
        .encode(
            x=alt.X("OBP:Q", title="出塁率 (OBP)", scale=alt.Scale(zero=False)),
            y=alt.Y("SLG:Q", title="長打率 (SLG)", scale=alt.Scale(zero=False)),
            color=alt.Color("HR:Q", scale=alt.Scale(scheme="orangered"), title="本塁打"),
            tooltip=["playerID", "teamID", "OBP", "SLG", "OPS", "HR"],
        )
        .properties(title="出塁率 vs 長打率（規定打席以上）", width=520, height=360)
        .interactive()
    )
    scatter_ops
    return


@app.cell
def _(mo):
    mo.md("""
    ## 3. Statcast

    2015年から MLB 全球場に設置されたトラッキングシステム。
    投球・打球の物理量をピッチ単位で記録する。

    | 列 | 説明 |
    |---|---|
    | `pitch_type` | 球種（FF=4シーム、SL=スライダー、CH=チェンジアップ…） |
    | `release_speed` | 球速 (mph) |
    | `release_spin_rate` | 回転数 (rpm) |
    | `launch_speed` | 打球初速 (mph) |
    | `launch_angle` | 打球角度 (°) |
    | `hit_distance_sc` | 打球距離 (ft) |
    | `events` | 打席結果（home_run, strikeout, …） |

    > **注意**: Statcast は1日分でも数千行あるため、サンプルとして1日を取得する。
    """)
    return


@app.cell
def _(load_statcast, mo):
    statcast = load_statcast("2023-07-04", "2023-07-04")
    mo.ui.dataframe(
        statcast.select([
            "player_name", "pitch_type", "release_speed", "release_spin_rate",
            "launch_speed", "launch_angle", "events",
        ])
        .drop_nulls(subset=["pitch_type"])
        .head(20),
        page_size=10,
    )
    return (statcast,)


@app.cell
def _(mo, statcast):
    mo.md(f"""
    **行数（投球数）**: {statcast.height:,}  |  **列数**: {statcast.width}
    """)
    return


@app.cell
def _(alt, pl, statcast):
    # 球種別 球速分布
    sc_pitch = (
        statcast
        .filter(
            pl.col("pitch_type").is_not_null()
            & pl.col("release_speed").is_not_null()
        )
        .filter(pl.col("pitch_type").is_in(["FF", "SL", "CH", "CU", "SI", "FC"]))
    )
    chart_speed = (
        alt.Chart(sc_pitch.select(["pitch_type", "release_speed"]))
        .mark_boxplot()
        .encode(
            x=alt.X("pitch_type:N", title="球種"),
            y=alt.Y("release_speed:Q", title="球速 (mph)", scale=alt.Scale(zero=False)),
            color="pitch_type:N",
        )
        .properties(title="球種別 球速分布（2023-07-04）", width=500, height=300)
    )
    chart_speed
    return


@app.cell
def _(alt, pl, statcast):
    # 打球: launch_speed vs launch_angle（本塁打のみ強調）
    hits = statcast.filter(
        pl.col("launch_speed").is_not_null()
        & pl.col("launch_angle").is_not_null()
    ).with_columns(
        pl.when(pl.col("events") == "home_run")
        .then(pl.lit("本塁打"))
        .otherwise(pl.lit("その他"))
        .alias("is_hr")
    )
    chart_la = (
        alt.Chart(hits.select(["player_name", "events", "launch_speed", "launch_angle", "is_hr"]))
        .mark_circle(opacity=0.5, size=30)
        .encode(
            x=alt.X("launch_speed:Q", title="打球初速 (mph)"),
            y=alt.Y("launch_angle:Q", title="打球角度 (°)"),
            color=alt.Color("is_hr:N", scale=alt.Scale(
                domain=["本塁打", "その他"],
                range=["#e74c3c", "#aaa"],
            )),
            tooltip=["player_name", "events", "launch_speed", "launch_angle"],
        )
        .properties(title="打球初速 vs 打球角度（2023-07-04）", width=580, height=350)
        .interactive()
    )
    chart_la
    return


@app.cell
def _(mo):
    mo.md("""
    ## まとめ

    | データソース | 取得関数 | 用途 |
    |---|---|---|
    | Lahman batting | `load_lahman_batting()` | 選手の長期トレンド分析 |
    | Lahman people | `load_lahman_people()` | 選手名・生年月日 |
    | FanGraphs | `load_fangraphs_batting(year)` | 高度なセイバーメトリクス指標 |
    | Statcast | `load_statcast(start, end)` | 投球・打球の物理量分析 |

    次章以降では、これらのデータを組み合わせてより深い分析を行う。
    """)
    return


if __name__ == "__main__":
    app.run()
