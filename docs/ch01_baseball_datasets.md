# 第1章: 野球データセット入門

**原著**: Chapter 1 — The Baseball Datasets
**原著URL**: https://beanumber.github.io/abdwr3e/ch01-bball.html
**対応ノートブック**: [ch01_baseball_datasets.py](../notebooks/ch01_baseball_datasets.py)

---

## この章の目的

野球データ分析の基礎として、主要なデータソースを知ることが最初の一歩となる。
本章では以下の4つのデータソースを紹介し、Python (pybaseball) でそれぞれを取得・確認する。

---

## 1. Lahman Database

### 概要

Sean Lahman が構築・公開している、最も広く使われる野球統計データベース。
1871年から現在まで、MLB 全選手のシーズン集計データを収録している。

- **粒度**: 選手 × シーズン × チーム（途中移籍で複数行になる場合あり）
- **テーブル**: batting, pitching, fielding, teams, people など多数

### Python での取得

```python
from baseball.data import load_lahman_batting, load_lahman_people

batting = load_lahman_batting()   # → polars DataFrame
people  = load_lahman_people()    # → 選手プロフィール
```

`pybaseball.lahman.batting()` を内部で呼び出し、Parquet にキャッシュして返す。

### batting テーブルの主要列

| 列 | 型 | 説明 |
|---|---|---|
| `playerID` | str | 選手固有 ID（Lahman 形式） |
| `yearID` | int | シーズン年 |
| `teamID` | str | チーム略称 |
| `G` | int | 試合数 |
| `AB` | int | 打数 |
| `H` | int | 安打 |
| `2B` | int | 二塁打 |
| `3B` | int | 三塁打 |
| `HR` | int | 本塁打 |
| `RBI` | int | 打点 |
| `SB` | int | 盗塁 |
| `BB` | int | 四球 |
| `SO` | int | 三振 |

### R との対応

```r
# R: Lahman パッケージ
library(Lahman)
data(Batting)
```

```python
# Python: pybaseball
from baseball.data import load_lahman_batting
batting = load_lahman_batting()
```

---

## 2. FanGraphs

### 概要

セイバーメトリクス指標を充実させた統計サイト。
wRC+、FIP、WAR など、Lahman にはない高度な分析指標が揃っており、現代の野球分析で広く参照される。

- **粒度**: 選手 × シーズン
- **期間**: 2002年〜現在

### Python での取得

```python
from baseball.data import load_fangraphs_batting

fg_2023 = load_fangraphs_batting(2023)
fg_range = load_fangraphs_batting(2015, 2023)  # 複数年
```

### 主要な指標

| 指標 | 説明 | 平均値の目安 |
|---|---|---|
| `wRC+` | 球場・時代補正済みの得点創出力 | 100 = リーグ平均 |
| `wOBA` | 重み付き出塁率 | 約 0.320 |
| `OBP` | 出塁率 | 約 0.320 |
| `SLG` | 長打率 | 約 0.410 |
| `BB%` | 四球率 | 約 8–9% |
| `K%` | 三振率 | 約 22–24% |
| `WAR` | Wins Above Replacement | 2.0 = 平均的なレギュラー |
| `FIP` | 守備無関係防御率（投手） | — |

### R との対応

```r
# R: baseballr パッケージ
library(baseballr)
fg_batter_leaders(2023, 2023)
```

```python
# Python
from baseball.data import load_fangraphs_batting
fg = load_fangraphs_batting(2023)
```

---

## 3. Statcast

### 概要

2015年から MLB 全球場に設置されたカメラ＆レーダーによるトラッキングシステム。
全投球・全打球の物理量をピッチ単位で記録する。データ量が多いため、特定期間を指定して取得する。

- **粒度**: 1投球
- **期間**: 2015年〜現在
- **データ量**: 1日あたり約 2,000〜5,000 行

### Python での取得

```python
from baseball.data import load_statcast

# 1日分（サンプル）
sc = load_statcast("2023-07-04", "2023-07-04")

# 1週間分
sc_week = load_statcast("2023-07-01", "2023-07-07")
```

### 主要な列

| 列 | 説明 |
|---|---|
| `player_name` | 投手名 |
| `batter` | 打者 MLBAM ID |
| `pitch_type` | 球種（FF=4シーム、SL=スライダー、CH=チェンジアップ、CU=カーブ、SI=シンカー、FC=カット） |
| `release_speed` | 球速 (mph) |
| `release_spin_rate` | 回転数 (rpm) |
| `pfx_x`, `pfx_z` | 変化量（横・縦、インチ） |
| `launch_speed` | 打球初速 (mph) |
| `launch_angle` | 打球角度 (°) |
| `hit_distance_sc` | 打球飛距離 (ft) |
| `events` | 打席結果（`home_run`, `strikeout`, `single` など） |
| `description` | 投球結果（`swinging_strike`, `called_strike`, `ball` など） |

### バレルゾーン

打球初速と打球角度の組み合わせで「バレル（barrel）」ゾーンが定義される。
おおよそ **打球角度 25–35°、打球初速 98 mph 以上** がバレル領域にあたる。

### R との対応

```r
# R: baseballr パッケージ
library(baseballr)
statcast_search("2023-07-04", "2023-07-04")
```

```python
# Python
from baseball.data import load_statcast
sc = load_statcast("2023-07-04", "2023-07-04")
```

---

## 4. Retrosheet

### 概要

Retrosheet は 1871 年から現在までの全試合の詳細記録を無料公開している非営利組織。
pybaseball では試合ログ（game logs）として取得できる。

- **粒度**: 1試合
- **期間**: 1871年〜現在

### Python での取得

```python
import pybaseball
import polars as pl

# 2023年の全試合ログ
gl = pybaseball.retrosheet_game(2023)
gl_pl = pl.from_pandas(gl)
```

> Retrosheet のゲームログには、両チームの安打・得点・エラー数など、試合単位の集計が含まれる。

---

## データソースの使い分け

| 分析の目的 | 推奨データソース |
|---|---|
| 選手の長期トレンド（キャリア統計） | Lahman |
| 選手比較・ランキング（現代指標） | FanGraphs |
| 投球・打球の物理的特性 | Statcast |
| 試合の勝敗・球場別比較 | Retrosheet ゲームログ |

---

## 参考: データ取得ユーティリティ

すべてのロード関数は `src/baseball/data.py` に集約されており、
**Parquet キャッシュ**により2回目以降の読み込みは高速。

```python
from baseball.data import (
    load_lahman_batting,
    load_lahman_pitching,
    load_lahman_teams,
    load_lahman_people,
    load_fangraphs_batting,
    load_statcast,
)
```

データは `data/` ディレクトリに `.parquet` 形式で保存される（gitignore 済み）。
