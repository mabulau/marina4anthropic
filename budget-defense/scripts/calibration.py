"""Budget Defense — Calibration Statistics and Learning Loop"""

import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from templates import BENCHMARKS

def compute_calibration_stats(values: list) -> dict:
    if not values or len(values) < 1:
        return {"fires": False, "reason": "No data"}

    n = len(values)
    sorted_vals = sorted(values)
    simple_mean = sum(values) / n

    if n < 5:
        return {
            "fires": True,
            "method": "simple_mean",
            "methodLabel": "average (pre-calibration)",
            "eventCount": n,
            "robustAverage": round(simple_mean, 4),
            "simpleMean": round(simple_mean, 4),
            "varianceRange": {
                "low": round(min(values), 4),
                "high": round(max(values), 4),
                "method": "min_max"
            },
            "divergence": None,
            "divergenceFlag": False
        }

    if n <= 9:
        if n % 2 == 0:
            median = (sorted_vals[n // 2 - 1] + sorted_vals[n // 2]) / 2
        else:
            median = sorted_vals[n // 2]

        robust_avg = median
        method = "median"
        method_label = f"median ({n} events)"
        var_low = sorted_vals[0]
        var_high = sorted_vals[-1]
        var_method = "min_max"

    else:
        trim_count = max(1, round(n * 0.10))
        trimmed = sorted_vals[trim_count:-trim_count] if trim_count < n // 2 else sorted_vals
        robust_avg = sum(trimmed) / len(trimmed)
        method = "trimmed_mean"
        method_label = f"trimmed mean, {n} events (dropped {trim_count} outliers each end)"

        p25_idx = max(0, round(n * 0.25) - 1)
        p75_idx = min(n - 1, round(n * 0.75) - 1)
        var_low = sorted_vals[p25_idx]
        var_high = sorted_vals[p75_idx]
        var_method = "iqr_p25_p75"

    if robust_avg != 0:
        divergence_pct = abs(simple_mean - robust_avg) / abs(robust_avg) * 100
    else:
        divergence_pct = 0

    divergence_flag = divergence_pct > 15

    return {
        "fires": True,
        "method": method,
        "methodLabel": method_label,
        "eventCount": n,
        "robustAverage": round(robust_avg, 4),
        "simpleMean": round(simple_mean, 4),
        "varianceRange": {
            "low": round(var_low, 4),
            "high": round(var_high, 4),
            "method": var_method
        },
        "divergence": {
            "pct": round(divergence_pct, 1),
            "flag": divergence_flag,
            "direction": "above" if simple_mean > robust_avg else "below"
        },
        "divergenceFlag": divergence_flag
    }


def compute_full_calibration(events: list, category: str) -> dict:
    rate_keys = ["boothVisitorRate", "leadsRate", "mqlRate", "sqlRate", "winRate"]
    metric_keys = ["roi", "coverage", "cpl", "costPerSql"]

    n = len(events)
    if n < 1:
        return {
            "eventCount": 0,
            "calibrationStatus": "no_data",
            "statusLabel": "no events",
            "runningAverages": {},
            "varianceRanges": {},
            "simpleMeans": {},
            "divergenceFlags": {},
            "adaptiveThresholds": {},
            "lastRecalibration": None
        }

    running_avgs = {}
    simple_means = {}
    variance_ranges = {}
    divergence_flags = {}

    for key in rate_keys:
        values = [e.get("inputs", {}).get(key) for e in events]
        values = [v for v in values if v is not None]
        if values:
            stats = compute_calibration_stats(values)
            running_avgs[key] = stats["robustAverage"]
            simple_means[key] = stats["simpleMean"]
            variance_ranges[key] = stats["varianceRange"]
            if stats["divergenceFlag"]:
                divergence_flags[key] = stats["divergence"]

    for key in metric_keys:
        values = [e.get("outputs", {}).get(key) for e in events]
        values = [v for v in values if v is not None]
        if values:
            stats = compute_calibration_stats(values)
            running_avgs[key] = stats["robustAverage"]
            simple_means[key] = stats["simpleMean"]
            variance_ranges[key] = stats["varianceRange"]
            if stats["divergenceFlag"]:
                divergence_flags[key] = stats["divergence"]

    if n >= 5:
        cal_status = "calibrated"
        status_label = f"calibrated, {n} events"
    else:
        cal_status = "learning"
        status_label = f"learning {n}/5"

    avg_attendees = 0
    att_values = [e.get("inputs", {}).get("attendees", 0) for e in events]
    if att_values:
        avg_attendees = sum(att_values) / len(att_values)

    if avg_attendees < 200:
        band_pct = 0.30
    elif avg_attendees < 2000:
        band_pct = 0.20
    elif avg_attendees < 10000:
        band_pct = 0.15
    else:
        band_pct = 0.10

    return {
        "eventCount": n,
        "calibrationStatus": cal_status,
        "statusLabel": status_label,
        "runningAverages": running_avgs,
        "simpleMeans": simple_means,
        "varianceRanges": variance_ranges,
        "divergenceFlags": divergence_flags,
        "adaptiveThresholds": {
            "varianceBandPct": band_pct,
            "avgAttendees": round(avg_attendees),
            "absoluteFloors": {
                "revenue": 50000,
                "leads": 100,
                "roi": 1.0
            }
        },
        "method": "median" if n <= 9 else "trimmed_mean",
        "lastRecalibration": None
    }
