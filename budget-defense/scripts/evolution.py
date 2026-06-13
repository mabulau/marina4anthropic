"""Budget Defense — Evolution Charts, Diff View, Parent/Child Events"""

import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from templates import BENCHMARKS, get_template
from helpers import _safe_div, _round_or_none, _calc_delta

def compare_scenarios(scenario_a: dict, scenario_b: dict) -> dict:
    """
    Compare two full result sets side by side. Returns deltas for all metrics.
    Uses absolute delta + direction for metrics that can cross zero (targetGap, ROI).
    """
    deltas = {}

    # Funnel deltas
    for key in scenario_a.get("funnel", {}):
        val_a = scenario_a["funnel"].get(key, 0) or 0
        val_b = scenario_b["funnel"].get(key, 0) or 0
        deltas[f"funnel.{key}"] = _calc_delta(val_a, val_b)

    # Derived metric deltas
    for key in scenario_a.get("derivedMetrics", {}):
        val_a = scenario_a["derivedMetrics"].get(key)
        val_b = scenario_b["derivedMetrics"].get(key)
        if val_a is not None and val_b is not None:
            deltas[f"derived.{key}"] = _calc_delta(val_a, val_b)

    # Rate deltas
    for key in scenario_a.get("rates", {}):
        val_a = scenario_a["rates"].get(key, 0)
        val_b = scenario_b["rates"].get(key, 0)
        deltas[f"rate.{key}"] = _calc_delta(val_a, val_b, precision=4)

    return deltas


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

    # Only show percentage change when it's meaningful:
    # - baseline is not zero
    # - values don't cross zero (sign change makes % misleading)
    crosses_zero = (val_a < 0 and val_b > 0) or (val_a > 0 and val_b < 0)
    if val_a != 0 and not crosses_zero:
        result["pctChange"] = round((val_b - val_a) / abs(val_a) * 100, 1)
    else:
        result["pctChange"] = None
        if crosses_zero:
            result["note"] = "crosses zero — percentage not meaningful"

    return result


# ──────────────────────────────────────────────────────────────
# Helpers

def event_evolution(events: list, metric: str = "roi", category: str = None,
                    year: int = None, template_key: str = None) -> dict:
    """
    Produce time-series data for the evolution chart from event history.
    Filters by category, year, and/or template. Returns chronological list
    with benchmark context.

    events: list of event dicts from events.json (each has identity, inputs, outputs)
    metric: which metric to chart (roi, coverage, cpl, costPerSql, boothVisitorRate, etc.)
    category: filter by template/event type
    year: filter by year
    template_key: filter by specific template
    """
    filtered = events

    if category:
        filtered = [e for e in filtered
                    if e.get("identity", {}).get("eventType", "") == category]
    if template_key:
        filtered = [e for e in filtered
                    if e.get("identity", {}).get("eventType", "") == template_key]
    if year:
        filtered = [e for e in filtered
                    if str(year) in e.get("identity", {}).get("date", "")]

    # Sort chronologically
    filtered.sort(key=lambda e: e.get("identity", {}).get("date", ""))

    if not filtered:
        return {"fires": False, "reason": "No events match the filter", "eventCount": 0}

    # Extract metric values
    points = []
    values = []
    for event in filtered:
        val = None
        outputs = event.get("outputs", {})
        inputs_data = event.get("inputs", {})

        # Check outputs first (derived metrics), then inputs (rates)
        if metric in outputs:
            val = outputs[metric]
        elif metric in inputs_data:
            val = inputs_data[metric]

        if val is not None:
            values.append(val)
            points.append({
                "name": event["identity"]["name"],
                "date": event["identity"]["date"],
                "value": val,
                "reportType": event.get("reportType", "unknown")
            })

    if len(points) < 1:
        return {"fires": False, "reason": f"No data for metric '{metric}'", "eventCount": 0}

    # Compute stats
    avg = sum(values) / len(values)
    min_val = min(values)
    max_val = max(values)

    # Get benchmark range for this metric
    bench = BENCHMARKS.get(metric, {})
    bench_low = bench.get("low")
    bench_high = bench.get("high")

    # Flag each point
    for p in points:
        if bench_low is not None and bench_high is not None:
            if bench.get("direction") == "lower-is-better":
                p["flag"] = "green" if p["value"] <= bench_high else (
                    "yellow" if p["value"] <= bench_high * 1.1 else "red")
            elif bench.get("direction") == "within-range":
                p["flag"] = "green" if bench_low <= p["value"] <= bench_high else "red"
            else:  # higher-is-better
                p["flag"] = "green" if p["value"] >= bench_low else (
                    "yellow" if p["value"] >= bench_low * 0.9 else "red")
        else:
            p["flag"] = "neutral"

    # Determine trend (simple: compare first half avg to second half avg)
    if len(values) >= 4:
        mid = len(values) // 2
        first_half = sum(values[:mid]) / mid
        second_half = sum(values[mid:]) / (len(values) - mid)
        trend = "improving" if second_half > first_half else (
            "declining" if second_half < first_half else "flat")
        trend_pct = round((second_half - first_half) / abs(first_half) * 100, 1) if first_half != 0 else None
    else:
        trend = None
        trend_pct = None

    return {
        "fires": True,
        "metric": metric,
        "eventCount": len(points),
        "points": points,
        "stats": {
            "average": round(avg, 2),
            "min": round(min_val, 2),
            "max": round(max_val, 2),
            "trend": trend,
            "trendPct": trend_pct
        },
        "benchmark": {
            "low": bench_low,
            "high": bench_high,
            "direction": bench.get("direction")
        },
        "canShowTrend": len(points) >= 3,
        "canShowComparison": len(points) >= 2
    }


# ──────────────────────────────────────────────────────────────
# Input Diff (before/after comparison)
# ──────────────────────────────────────────────────────────────

def diff_inputs(before: dict, after: dict) -> dict:
    """
    Compare two analysis results and produce a diff showing what changed.
    Returns changed inputs, changed outputs, and the delta for each.
    Used when the planner adjusts rates and wants to see the impact.
    """
    diff = {
        "inputChanges": [],
        "outputChanges": [],
        "funnelChanges": []
    }

    # Compare rates
    for key in before.get("rates", {}):
        val_a = before["rates"].get(key, 0)
        val_b = after["rates"].get(key, 0)
        if abs(val_b - val_a) > 0.0001:
            diff["inputChanges"].append({
                "field": key,
                "from": val_a,
                "to": val_b,
                "delta": round(val_b - val_a, 4),
                "pctChange": round((val_b - val_a) / val_a * 100, 1) if val_a != 0 else None
            })

    # Compare funnel stages
    for key in before.get("funnel", {}):
        val_a = before["funnel"].get(key, 0)
        val_b = after["funnel"].get(key, 0)
        if abs(val_b - val_a) > 0.01:
            diff["funnelChanges"].append({
                "stage": key,
                "from": val_a,
                "to": val_b,
                "delta": round(val_b - val_a, 2),
                "pctChange": round((val_b - val_a) / val_a * 100, 1) if val_a != 0 else None
            })

    # Compare derived metrics
    for key in before.get("derivedMetrics", {}):
        val_a = before["derivedMetrics"].get(key)
        val_b = after["derivedMetrics"].get(key)
        if val_a is not None and val_b is not None and abs(val_b - val_a) > 0.01:
            diff["outputChanges"].append(_calc_delta(val_a, val_b) | {
                "metric": key
            })

    return diff


# ──────────────────────────────────────────────────────────────
# Parent/Child Event Support
# ──────────────────────────────────────────────────────────────

def roll_up_child_events(children: list) -> dict:
    """
    Roll up multiple child event results into a parent event summary.
    Use when a single conference has multiple activations (booth + dinner + session).

    children: list of dicts, each with {results: calculate_funnel output, template_key: str}

    Returns a combined summary with:
    - Total cost, total forecasted revenue, combined ROI
    - Per-child breakdown
    - Attribution-weighted credited revenue
    """
    total_cost = 0
    total_revenue = 0
    total_credited = 0
    total_leads = 0
    total_sqls = 0
    child_summaries = []

    for child in children:
        r = child["results"]
        template_key = child.get("template_key", "booth_presence")
        template = get_template(template_key)

        cost = r["costs"]["effectiveCost"]
        rev = r["funnel"]["forecastedRevenue"]
        credited = r["attribution"]["creditedRevenue"]
        leads = r["funnel"]["netNewLeads"]
        sqls = r["funnel"]["sqls"]

        total_cost += cost
        total_revenue += rev
        total_credited += credited
        total_leads += leads
        total_sqls += sqls

        child_summaries.append({
            "name": child.get("name", template.get("name", template_key)),
            "template": template_key,
            "templateName": template.get("name"),
            "cost": round(cost, 2),
            "forecastedRevenue": round(rev, 2),
            "creditedRevenue": round(credited, 2),
            "leads": round(leads, 1),
            "sqls": round(sqls, 1),
            "roi": _round_or_none(_safe_div(rev - cost, cost), 2)
        })

    combined_roi = _safe_div(total_revenue - total_cost, total_cost)
    combined_cpl = _safe_div(total_cost, total_leads)
    combined_cps = _safe_div(total_cost, total_sqls)

    return {
        "parentSummary": {
            "totalCost": round(total_cost, 2),
            "totalForecastedRevenue": round(total_revenue, 2),
            "totalCreditedRevenue": round(total_credited, 2),
            "combinedROI": _round_or_none(combined_roi, 2),
            "combinedCPL": _round_or_none(combined_cpl, 2),
            "combinedCostPerSQL": _round_or_none(combined_cps, 2),
            "totalLeads": round(total_leads, 1),
            "totalSQLs": round(total_sqls, 1),
            "childCount": len(children)
        },
        "children": child_summaries
    }


