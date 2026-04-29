"""Data loading utilities with Parquet caching."""

from pathlib import Path
from typing import Callable

import polars as pl

DATA_DIR = Path(__file__).parent.parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)


def _cached(name: str, fetch_fn: Callable[[], pl.DataFrame]) -> pl.DataFrame:
    path = DATA_DIR / f"{name}.parquet"
    if path.exists():
        return pl.read_parquet(path)
    df = fetch_fn()
    df.write_parquet(path)
    return df


def _from_pybaseball(fetch_fn: Callable) -> pl.DataFrame:
    """Call a pybaseball function (returns pandas) and convert to polars."""
    import pandas as pd  # pybaseball requires pandas internally

    df_pd: pd.DataFrame = fetch_fn()
    return pl.from_pandas(df_pd)


def load_lahman_batting() -> pl.DataFrame:
    import lahman

    return _cached("lahman_batting", lambda: _from_pybaseball(lahman.batting))


def load_lahman_pitching() -> pl.DataFrame:
    import lahman

    return _cached("lahman_pitching", lambda: _from_pybaseball(lahman.pitching))


def load_lahman_teams() -> pl.DataFrame:
    import lahman

    return _cached("lahman_teams", lambda: _from_pybaseball(lahman.teams))


def load_lahman_people() -> pl.DataFrame:
    import lahman

    return _cached("lahman_people", lambda: _from_pybaseball(lahman.people))


def load_fangraphs_batting(
    start_season: int, end_season: int | None = None
) -> pl.DataFrame:
    import pybaseball

    end = end_season or start_season
    name = f"fangraphs_batting_{start_season}_{end}"
    return _cached(
        name,
        lambda: _from_pybaseball(lambda: pybaseball.batting_stats(start_season, end)),
    )


def load_statcast(start_dt: str, end_dt: str) -> pl.DataFrame:
    import pybaseball

    name = f"statcast_{start_dt}_{end_dt}".replace("-", "")
    return _cached(
        name, lambda: _from_pybaseball(lambda: pybaseball.statcast(start_dt, end_dt))
    )
