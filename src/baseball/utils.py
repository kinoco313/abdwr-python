"""Common baseball analytics utilities."""

import polars as pl


def run_expectancy_matrix(pbp: pl.DataFrame) -> pl.DataFrame:
    """Compute 24-state run expectancy matrix from play-by-play data.

    Args:
        pbp: Play-by-play DataFrame with columns:
             base_state (str), outs (int), runs_scored_after (float)
    Returns:
        DataFrame with columns base_state, outs, mean_runs.
    """
    return (
        pbp.group_by(["base_state", "outs"])
        .agg(pl.col("runs_scored_after").mean().alias("mean_runs"))
        .sort(["outs", "base_state"])
    )


def linear_weights(pbp: pl.DataFrame, events: list[str]) -> pl.DataFrame:
    """Estimate linear weights (wOBA components) from play-by-play data."""
    return (
        pbp.filter(pl.col("event").is_in(events))
        .group_by("event")
        .agg(pl.col("run_value").mean().alias("linear_weight"))
        .sort("linear_weight", descending=True)
    )


def pythagorean_expectation(
    runs_scored: pl.Series | pl.Expr,
    runs_allowed: pl.Series | pl.Expr,
    exp: float = 1.83,
) -> pl.Series | pl.Expr:
    """Bill James Pythagorean Win Expectation."""
    rs_exp = runs_scored**exp
    ra_exp = runs_allowed**exp
    return rs_exp / (rs_exp + ra_exp)
