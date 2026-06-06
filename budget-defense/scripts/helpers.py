"""Budget Defense — Shared Helper Functions"""

import math


def _safe_div(numerator, denominator):
    """Division that returns None instead of raising ZeroDivisionError."""
    if denominator is None or denominator == 0:
        return None
    try:
        result = numerator / denominator
        if math.isnan(result) or math.isinf(result):
            return None
        return result
    except (TypeError, ZeroDivisionError):
        return None


def _round_or_none(val, digits):
    if val is None:
        return None
    try:
        return round(val, digits)
    except (TypeError, ValueError):
        return None


def _calc_delta(val_a, val_b, precision=2):
    """
    Calculate delta between two values, handling zero-crossing safely.
    Returns absolute delta + direction instead of misleading percentages
    when the baseline is zero or negative, or when values cross zero.
    """
    delta = round(val_b - val_a, precision)
    result = {
        "a": val_a,
        "b": val_b,
        "delta": delta,
        "direction": "up" if delta > 0 else ("down" if delta < 0 else "flat")
    }

    crosses_zero = (val_a < 0 and val_b > 0) or (val_a > 0 and val_b < 0)
    if val_a != 0 and not crosses_zero:
        result["pctChange"] = round((val_b - val_a) / abs(val_a) * 100, 1)
    else:
        result["pctChange"] = None
        if crosses_zero:
            result["note"] = "crosses zero — percentage not meaningful"

    return result
