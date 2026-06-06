#!/usr/bin/env python3
"""
Budget Defense — Core Calculation Engine
Pure-function pipeline. Pass inputs as JSON, get full results back.

Usage:
    python calc_engine.py --json '{"attendees": 5000, ...}'
    python calc_engine.py --file inputs.json
    python calc_engine.py --compare scenario1.json scenario2.json

All rates are decimals (0.12 = 12%). All dollar amounts are raw numbers.
"""

import json
import sys
import os
import math

# Module imports
sys.path.insert(0, os.path.dirname(__file__))
from templates import (BENCHMARKS, MARKETING_INVESTMENT_PCT, TEMPLATES,
    DEFAULT_FUNNEL_LABELS, TONE_BANDS, TONES, get_template, match_template,
    get_tone_multipliers)
from helpers import _safe_div, _round_or_none, _calc_delta
from calibration import compute_calibration_stats, compute_full_calibration
from evolution import (event_evolution, diff_inputs, roll_up_child_events,
    compare_scenarios)

# Re-export everything for backward compatibility
__all__ = ["BENCHMARKS", "MARKETING_INVESTMENT_PCT", "TEMPLATES",
    "DEFAULT_FUNNEL_LABELS", "TONE_BANDS", "TONES", "get_template",
    "match_template", "get_tone_multipliers", "calculate_funnel",
    "flag_benchmarks", "root_cause_analysis", "lever_projections",
    "funnel_vs_industry", "sanity_check", "compare_scenarios",
    "run_full_analysis", "compute_calibration_stats",
    "compute_full_calibration", "event_evolution", "diff_inputs",
    "roll_up_child_events"]

# ──────────────────────────────────────────────────────────────
# Core Funnel Calculation
# ──────────────────────────────────────────────────────────────

def calculate_funnel(inputs: dict) -> dict:
    """
    Core funnel: attendees → visitors → leads → MQLs → SQLs → deals → revenue.
    Each stage is a multiplication.

    Required inputs:
        attendees (int), boothVisitorRate, leadsRate, mqlRate, sqlRate, winRate (all float 0-1),
        acv (float $)

    Optional inputs:
        boothCost (float $), targetRevenue (float $),
        sourcedPct (float 0-1, default 1.0), creditWeight (float 0-1, default 0.30),
        template (str), tone (str: conservative/realistic/optimistic),
        calibration (dict: from calibration.json for this category, enables calibrated tone bands)
    """
    # Apply per-rate tone multipliers (variance-weighted, not flat)
    tone = inputs.get("tone", "realistic")
    calibration = inputs.get("calibration", None)
    tone_mults = get_tone_multipliers(tone, calibration)

    attendees = inputs.get("attendees", 0)
    boothVisitorRate = inputs.get("boothVisitorRate", 0) * tone_mults.get("boothVisitorRate", 1.0)
    leadsRate = inputs.get("leadsRate", 0) * tone_mults.get("leadsRate", 1.0)
    mqlRate = inputs.get("mqlRate", 0) * tone_mults.get("mqlRate", 1.0)
    sqlRate = inputs.get("sqlRate", 0) * tone_mults.get("sqlRate", 1.0)
    winRate = inputs.get("winRate", 0) * tone_mults.get("winRate", 1.0)
    acv = inputs.get("acv", 0)

    # Input validation: catch inconsistent data before calculating
    validation_warnings = []
    raw_rates = {
        "boothVisitorRate": inputs.get("boothVisitorRate", 0),
        "leadsRate": inputs.get("leadsRate", 0),
        "mqlRate": inputs.get("mqlRate", 0),
        "sqlRate": inputs.get("sqlRate", 0),
        "winRate": inputs.get("winRate", 0),
    }
    for rate_name, rate_val in raw_rates.items():
        if rate_val > 1.0:
            validation_warnings.append({
                "field": rate_name,
                "value": rate_val,
                "issue": f"{rate_name} is {rate_val*100:.0f}% — rates should be between 0% and 100%. This will be capped at 100%."
            })
        elif rate_val < 0:
            validation_warnings.append({
                "field": rate_name,
                "value": rate_val,
                "issue": f"{rate_name} is negative ({rate_val*100:.0f}%). This will be treated as 0%."
            })
    if inputs.get("attendees", 0) < 0:
        validation_warnings.append({
            "field": "attendees", "value": inputs["attendees"],
            "issue": "Attendees is negative. This will be treated as 0."
        })
    if inputs.get("acv", 0) < 0:
        validation_warnings.append({
            "field": "acv", "value": inputs["acv"],
            "issue": "ACV is negative. Check your deal size."
        })

    # Cap rates at 1.0 and floor at 0 after tone adjustment
    boothVisitorRate = max(0, min(boothVisitorRate, 1.0))
    leadsRate = max(0, min(leadsRate, 1.0))
    mqlRate = max(0, min(mqlRate, 1.0))
    sqlRate = max(0, min(sqlRate, 1.0))
    winRate = max(0, min(winRate, 1.0))
    attendees = max(0, attendees)
    winRate = min(winRate, 1.0)

    # Funnel stages
    boothVisitors = attendees * boothVisitorRate
    netNewLeads = boothVisitors * leadsRate
    mqls = netNewLeads * mqlRate
    sqls = mqls * sqlRate
    deals = sqls * winRate
    forecastedRevenue = deals * acv

    # Cost inputs
    boothCost = inputs.get("boothCost", 0) or 0
    targetRevenue = inputs.get("targetRevenue", 0) or 0

    # Derived metrics (null-safe)
    targetBoothCost = targetRevenue * MARKETING_INVESTMENT_PCT
    estimatedBoothCost = forecastedRevenue * MARKETING_INVESTMENT_PCT

    # Use targetBoothCost as fallback when boothCost is 0
    effectiveCost = boothCost if boothCost > 0 else targetBoothCost

    roi = _safe_div(forecastedRevenue - effectiveCost, effectiveCost)
    coverage = _safe_div(forecastedRevenue, targetRevenue) if targetRevenue > 0 else None
    cpl = _safe_div(effectiveCost, netNewLeads)
    costPerSql = _safe_div(effectiveCost, sqls)
    targetGap = forecastedRevenue - targetRevenue if targetRevenue > 0 else None

    # Attribution layer
    sourcedPct = inputs.get("sourcedPct", 1.0)
    creditWeight = inputs.get("creditWeight", 0.30)

    sourcedRevenue = forecastedRevenue * sourcedPct
    influencedRevenue = forecastedRevenue * (1 - sourcedPct)
    influencedCredit = influencedRevenue * creditWeight
    creditedRevenue = sourcedRevenue + influencedCredit

    return {
        "funnel": {
            "attendees": attendees,
            "boothVisitors": round(boothVisitors, 1),
            "netNewLeads": round(netNewLeads, 1),
            "mqls": round(mqls, 1),
            "sqls": round(sqls, 1),
            "deals": round(deals, 2),
            "forecastedRevenue": round(forecastedRevenue, 2)
        },
        "rates": {
            "boothVisitorRate": round(boothVisitorRate, 4),
            "leadsRate": round(leadsRate, 4),
            "mqlRate": round(mqlRate, 4),
            "sqlRate": round(sqlRate, 4),
            "winRate": round(winRate, 4)
        },
        "costs": {
            "boothCost": boothCost,
            "effectiveCost": effectiveCost,
            "targetBoothCost": round(targetBoothCost, 2),
            "estimatedBoothCost": round(estimatedBoothCost, 2)
        },
        "derivedMetrics": {
            "roi": _round_or_none(roi, 2),
            "coverage": _round_or_none(coverage, 4),
            "cpl": _round_or_none(cpl, 2),
            "costPerSql": _round_or_none(costPerSql, 2),
            "targetGap": _round_or_none(targetGap, 2),
            "targetRevenue": targetRevenue
        },
        "attribution": {
            "sourcedPct": sourcedPct,
            "creditWeight": creditWeight,
            "sourcedRevenue": round(sourcedRevenue, 2),
            "influencedRevenue": round(influencedRevenue, 2),
            "influencedCredit": round(influencedCredit, 2),
            "creditedRevenue": round(creditedRevenue, 2)
        },
        "inputs": {
            "acv": acv,
            "tone": tone,
            "template": inputs.get("template", "booth_presence")
        },
        "validationWarnings": validation_warnings
    }


# ──────────────────────────────────────────────────────────────
# Benchmark Flagging
# ──────────────────────────────────────────────────────────────

def flag_benchmarks(results: dict, template_key: str = "booth_presence") -> dict:
    """
    Evaluate each metric against its benchmark range. Returns flags dict.
    Yellow = within 10% buffer zone of the edge. Red = outside range. Green = healthy.
    NaN/None values flag red.
    """
    template = TEMPLATES.get(template_key, TEMPLATES["booth_presence"])
    overrides = template.get("benchmarkOverrides", {})

    flags = {}

    # Rate metrics
    rate_metrics = {
        "boothVisitorRate": results["rates"]["boothVisitorRate"],
        "leadsRate": results["rates"]["leadsRate"],
        "mqlRate": results["rates"]["mqlRate"],
        "sqlRate": results["rates"]["sqlRate"],
        "winRate": results["rates"]["winRate"],
    }

    for metric, value in rate_metrics.items():
        bench = overrides.get(metric, BENCHMARKS.get(metric))
        if bench:
            flags[metric] = _evaluate_flag(value, bench)

    # Derived metrics
    derived = {
        "cpl": results["derivedMetrics"]["cpl"],
        "costPerSql": results["derivedMetrics"]["costPerSql"],
        "roi": results["derivedMetrics"]["roi"],
        "coverage": results["derivedMetrics"]["coverage"],
    }

    # Dynamic cost per SQL benchmark: 3x-7x CPL when no template override
    # (matches benchmark table: $540-$5,000 ≈ 3×-7× of $180-$700 CPL range)
    if "costPerSql" not in overrides and results["derivedMetrics"]["cpl"] is not None:
        cpl_val = results["derivedMetrics"]["cpl"]
        cpl_bench = overrides.get("cpl", BENCHMARKS["cpl"])
        derived_cps_low = cpl_bench["low"] * 3
        derived_cps_high = cpl_bench["high"] * 7
        overrides_with_cps = {**overrides, "costPerSql": {
            "low": derived_cps_low, "high": derived_cps_high, "direction": "lower-is-better"
        }}
    else:
        overrides_with_cps = overrides

    for metric, value in derived.items():
        bench = overrides_with_cps.get(metric, BENCHMARKS.get(metric))
        if bench:
            flags[metric] = _evaluate_flag(value, bench)

    # CPL suppression for heavily influenced programs (sourced < 30%)
    sourced_pct = results["attribution"]["sourcedPct"]
    if sourced_pct < 0.30:
        if flags.get("cpl", {}).get("flag") == "red":
            flags["cpl"]["flag"] = "suppressed"
            flags["cpl"]["reason"] = f"Suppressed: sourced at {sourced_pct*100:.0f}% — high CPL is expected for influenced programs"
        if flags.get("costPerSql", {}).get("flag") == "red":
            flags["costPerSql"]["flag"] = "suppressed"
            flags["costPerSql"]["reason"] = f"Suppressed: sourced at {sourced_pct*100:.0f}%"

    return flags


def _evaluate_flag(value, bench: dict) -> dict:
    """Evaluate a single metric against its benchmark range."""
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return {"flag": "red", "value": None, "low": bench["low"], "high": bench["high"],
                "reason": "No data"}

    direction = bench.get("direction", "higher-is-better")
    low, high = bench["low"], bench["high"]
    buffer = 0.10  # 10% yellow zone

    if direction == "higher-is-better":
        if value >= low:
            return {"flag": "green", "value": value, "low": low, "high": high}
        elif value >= low * (1 - buffer):
            return {"flag": "yellow", "value": value, "low": low, "high": high,
                    "reason": f"Near lower edge ({value:.4f} vs {low:.4f})"}
        else:
            return {"flag": "red", "value": value, "low": low, "high": high,
                    "reason": f"Below range ({value:.4f} < {low:.4f})"}

    elif direction == "lower-is-better":
        if value <= high:
            return {"flag": "green", "value": value, "low": low, "high": high}
        elif value <= high * (1 + buffer):
            return {"flag": "yellow", "value": value, "low": low, "high": high,
                    "reason": f"Near upper edge (${value:,.0f} vs ${high:,.0f})"}
        else:
            return {"flag": "red", "value": value, "low": low, "high": high,
                    "reason": f"Above range (${value:,.0f} > ${high:,.0f})"}

    elif direction == "within-range":
        if low <= value <= high:
            return {"flag": "green", "value": value, "low": low, "high": high}
        elif value < low:
            if value >= low * (1 - buffer):
                return {"flag": "yellow", "value": value, "low": low, "high": high,
                        "reason": f"Near lower edge"}
            return {"flag": "red", "value": value, "low": low, "high": high,
                    "reason": f"Below range ({value:.4f} < {low:.4f})"}
        else:  # value > high
            if value <= high * (1 + buffer):
                return {"flag": "yellow", "value": value, "low": low, "high": high,
                        "reason": f"Near upper edge"}
            return {"flag": "red", "value": value, "low": low, "high": high,
                    "reason": f"Above range ({value:.4f} > {high:.4f})"}

    return {"flag": "green", "value": value, "low": low, "high": high}


# ──────────────────────────────────────────────────────────────
# Root Cause Analysis
# ──────────────────────────────────────────────────────────────

def root_cause_analysis(results: dict, flags: dict, metric_key: str,
                        template_key: str = "booth_presence") -> list:
    """
    For a derived metric (ROI, coverage, CPL, costPerSql), identify every upstream
    rate that's out of range in the HARMFUL direction. Project what the metric would
    be if that single rate were restored to its nearest industry edge. Sort by impact.

    Returns list of dicts: [{rate, currentValue, targetValue, currentMetric, projectedMetric, lift}]
    """
    template = TEMPLATES.get(template_key, TEMPLATES["booth_presence"])
    overrides = template.get("benchmarkOverrides", {})

    rate_keys = ["boothVisitorRate", "leadsRate", "mqlRate", "sqlRate", "winRate"]
    causes = []

    for rate_key in rate_keys:
        flag = flags.get(rate_key, {})
        if flag.get("flag") not in ("red", "yellow"):
            continue

        bench = overrides.get(rate_key, BENCHMARKS.get(rate_key, {}))
        direction = bench.get("direction", "higher-is-better")
        current_val = results["rates"][rate_key]
        low, high = bench["low"], bench["high"]

        # Determine if this rate is out of range in the HARMFUL direction
        # for the parent metric
        if direction == "higher-is-better" and current_val < low:
            target_val = low  # restore to lower edge
        elif direction == "lower-is-better" and current_val > high:
            target_val = high
        elif direction == "within-range":
            if current_val < low:
                target_val = low
            elif current_val > high:
                target_val = high
            else:
                continue
        else:
            continue  # rate is out of range in the GOOD direction — skip

        # Project: recalculate with this one rate changed
        projected_inputs = {
            "attendees": results["funnel"]["attendees"],
            "boothVisitorRate": results["rates"]["boothVisitorRate"],
            "leadsRate": results["rates"]["leadsRate"],
            "mqlRate": results["rates"]["mqlRate"],
            "sqlRate": results["rates"]["sqlRate"],
            "winRate": results["rates"]["winRate"],
            "acv": results["inputs"]["acv"],
            "boothCost": results["costs"]["boothCost"],
            "targetRevenue": results["derivedMetrics"]["targetRevenue"],
            "sourcedPct": results["attribution"]["sourcedPct"],
            "creditWeight": results["attribution"]["creditWeight"],
            "tone": "realistic"  # projections always at 1.0x
        }
        projected_inputs[rate_key] = target_val
        projected = calculate_funnel(projected_inputs)

        current_metric = results["derivedMetrics"].get(metric_key)
        projected_metric = projected["derivedMetrics"].get(metric_key)

        if current_metric is None or projected_metric is None:
            continue

        # For within-range rates like boothVisitorRate, check that restoring
        # the rate actually IMPROVES the parent metric, not worsens it
        metric_direction = BENCHMARKS.get(metric_key, {}).get("direction", "higher-is-better")
        if metric_direction == "higher-is-better" and projected_metric <= current_metric:
            continue
        if metric_direction == "lower-is-better" and projected_metric >= current_metric:
            continue

        lift = projected_metric - current_metric
        causes.append({
            "rate": rate_key,
            "currentValue": current_val,
            "targetValue": target_val,
            "currentMetric": current_metric,
            "projectedMetric": projected_metric,
            "lift": abs(lift)
        })

    # Sort by impact magnitude (largest lift first)
    causes.sort(key=lambda x: x["lift"], reverse=True)
    return causes


# ──────────────────────────────────────────────────────────────
# Lever Projections
# ──────────────────────────────────────────────────────────────

def lever_projections(results: dict, template_key: str = "booth_presence") -> dict:
    """
    For each adjustable lever, project what a 10% improvement would do.
    Returns projections grouped by direct and upstream levers.
    """
    base = results.copy()
    projections = {"direct": [], "upstream": []}

    # Direct levers: boothCost (decrease), ACV (increase), targetRevenue (adjust)
    if results["costs"]["boothCost"] > 0:
        new_cost = results["costs"]["boothCost"] * 0.90
        new_roi = _safe_div(results["funnel"]["forecastedRevenue"] - new_cost, new_cost)
        new_cpl = _safe_div(new_cost, results["funnel"]["netNewLeads"])
        new_cps = _safe_div(new_cost, results["funnel"]["sqls"])
        projections["direct"].append({
            "lever": "boothCost",
            "direction": "decrease",
            "change": "10% less",
            "newValue": round(new_cost, 2),
            "effects": {
                "roi": {"from": results["derivedMetrics"]["roi"], "to": _round_or_none(new_roi, 2)},
                "cpl": {"from": results["derivedMetrics"]["cpl"], "to": _round_or_none(new_cpl, 2)},
                "costPerSql": {"from": results["derivedMetrics"]["costPerSql"], "to": _round_or_none(new_cps, 2)}
            },
            "reason": "both numerator and denominator — biggest lever"
        })

    if results["inputs"]["acv"] > 0:
        new_acv = results["inputs"]["acv"] * 1.10
        new_rev = (results["funnel"]["deals"]) * new_acv
        new_cost = results["costs"]["effectiveCost"]
        new_roi = _safe_div(new_rev - new_cost, new_cost)
        new_cov = _safe_div(new_rev, results["derivedMetrics"]["targetRevenue"]) if results["derivedMetrics"]["targetRevenue"] else None
        projections["direct"].append({
            "lever": "acv",
            "direction": "increase",
            "change": "10% more",
            "newValue": round(new_acv, 2),
            "effects": {
                "forecastedRevenue": {"from": results["funnel"]["forecastedRevenue"], "to": round(new_rev, 2)},
                "roi": {"from": results["derivedMetrics"]["roi"], "to": _round_or_none(new_roi, 2)},
                "coverage": {"from": results["derivedMetrics"]["coverage"], "to": _round_or_none(new_cov, 4)}
            },
            "reason": "linear multiplier on forecast revenue"
        })

    # Upstream levers: each rate
    for rate_key in ["boothVisitorRate", "leadsRate", "mqlRate", "sqlRate", "winRate"]:
        current = results["rates"][rate_key]
        if current <= 0:
            continue
        new_rate = min(current * 1.10, 1.0)
        proj_inputs = {
            "attendees": results["funnel"]["attendees"],
            "boothVisitorRate": results["rates"]["boothVisitorRate"],
            "leadsRate": results["rates"]["leadsRate"],
            "mqlRate": results["rates"]["mqlRate"],
            "sqlRate": results["rates"]["sqlRate"],
            "winRate": results["rates"]["winRate"],
            "acv": results["inputs"]["acv"],
            "boothCost": results["costs"]["boothCost"],
            "targetRevenue": results["derivedMetrics"]["targetRevenue"],
            "sourcedPct": results["attribution"]["sourcedPct"],
            "creditWeight": results["attribution"]["creditWeight"],
            "tone": "realistic"
        }
        proj_inputs[rate_key] = new_rate
        proj = calculate_funnel(proj_inputs)

        projections["upstream"].append({
            "lever": rate_key,
            "direction": "increase",
            "change": "10% more",
            "currentValue": current,
            "newValue": round(new_rate, 4),
            "effects": {
                "forecastedRevenue": {
                    "from": results["funnel"]["forecastedRevenue"],
                    "to": proj["funnel"]["forecastedRevenue"]
                },
                "roi": {
                    "from": results["derivedMetrics"]["roi"],
                    "to": proj["derivedMetrics"]["roi"]
                }
            },
            "reason": "compounds into forecast revenue"
        })

    # Attendee lever: only for hosted/owned events where the planner controls attendance.
    # Uses the template's "hosted" property instead of a separate list.
    template = TEMPLATES.get(template_key, TEMPLATES["booth_presence"])
    is_hosted = template.get("hosted", False)
    if is_hosted and results["funnel"]["attendees"] > 0:
        new_attendees = round(results["funnel"]["attendees"] * 1.25)  # 25% more for hosted
        proj_inputs = {
            "attendees": new_attendees,
            "boothVisitorRate": results["rates"]["boothVisitorRate"],
            "leadsRate": results["rates"]["leadsRate"],
            "mqlRate": results["rates"]["mqlRate"],
            "sqlRate": results["rates"]["sqlRate"],
            "winRate": results["rates"]["winRate"],
            "acv": results["inputs"]["acv"],
            "boothCost": results["costs"]["boothCost"],
            "targetRevenue": results["derivedMetrics"]["targetRevenue"],
            "sourcedPct": results["attribution"]["sourcedPct"],
            "creditWeight": results["attribution"]["creditWeight"],
            "tone": "realistic"
        }
        proj = calculate_funnel(proj_inputs)
        projections["upstream"].append({
            "lever": "attendees",
            "direction": "increase",
            "change": "25% more",
            "currentValue": results["funnel"]["attendees"],
            "newValue": new_attendees,
            "effects": {
                "forecastedRevenue": {
                    "from": results["funnel"]["forecastedRevenue"],
                    "to": proj["funnel"]["forecastedRevenue"]
                },
                "roi": {
                    "from": results["derivedMetrics"]["roi"],
                    "to": proj["derivedMetrics"]["roi"]
                }
            },
            "reason": "scales the whole funnel (you control the invite list)"
        })

    return projections


# ──────────────────────────────────────────────────────────────
# Funnel vs Industry Comparison
# ──────────────────────────────────────────────────────────────

def funnel_vs_industry(results: dict, template_key: str = "booth_presence") -> dict:
    """
    Compare forecasted revenue against the industry rule-of-thumb:
    expectedRevenue = eventCost / marketingInvestmentPct.
    Returns spread and driver analysis when spread exceeds 15%.
    """
    cost = results["costs"]["effectiveCost"]
    if cost <= 0:
        return {"fires": False, "reason": "No cost data"}

    expected = cost / MARKETING_INVESTMENT_PCT
    actual = results["funnel"]["forecastedRevenue"]

    if expected <= 0:
        return {"fires": False, "reason": "Expected revenue is zero"}

    spread = (actual - expected) / expected
    fires = abs(spread) > 0.15

    if not fires:
        return {"fires": False, "spread": round(spread, 4)}

    # Find top driver: rate with largest deviation from industry midpoint
    template = TEMPLATES.get(template_key, TEMPLATES["booth_presence"])
    overrides = template.get("benchmarkOverrides", {})
    drivers = []

    for rate_key in ["boothVisitorRate", "leadsRate", "mqlRate", "sqlRate", "winRate"]:
        bench = overrides.get(rate_key, BENCHMARKS.get(rate_key, {}))
        mid = (bench["low"] + bench["high"]) / 2
        val = results["rates"][rate_key]
        deviation = (val - mid) / mid if mid > 0 else 0
        drivers.append({
            "rate": rate_key,
            "value": val,
            "low": bench["low"],
            "high": bench["high"],
            "deviation": deviation,
            "position": "above" if val > bench["high"] else ("below" if val < bench["low"] else "in-range")
        })

    drivers.sort(key=lambda x: abs(x["deviation"]), reverse=True)

    return {
        "fires": True,
        "direction": "outperforming" if spread > 0 else "underperforming",
        "spread": round(spread, 4),
        "spreadPct": round(abs(spread) * 100, 1),
        "expectedRevenue": round(expected, 2),
        "actualRevenue": round(actual, 2),
        "ratio": round(actual / expected, 2) if expected > 0 else None,
        "topDriver": drivers[0] if drivers else None,
        "allDrivers": drivers
    }


# ──────────────────────────────────────────────────────────────
# Sanity Check
# ──────────────────────────────────────────────────────────────

def sanity_check(results: dict, flags: dict, template_key: str = "booth_presence") -> list:
    """
    Sanity check triggers. Returns list of triggered checks.
    Catches: rates above industry high, excessive coverage, sourced overrides,
    and absurdly high derived metrics that would otherwise flag green.
    """
    template = TEMPLATES.get(template_key, TEMPLATES["booth_presence"])
    overrides = template.get("benchmarkOverrides", {})
    checks = []

    # Trigger 1: rate above industry high
    for rate_key in ["boothVisitorRate", "leadsRate", "mqlRate", "sqlRate", "winRate"]:
        bench = overrides.get(rate_key, BENCHMARKS.get(rate_key, {}))
        val = results["rates"][rate_key]
        if val > bench.get("high", 1.0):
            checks.append({
                "trigger": "rate_above_high",
                "rate": rate_key,
                "value": val,
                "high": bench["high"],
                "low": bench.get("low", 0)
            })

    # Trigger 2: coverage >150%
    cov = results["derivedMetrics"]["coverage"]
    target = results["derivedMetrics"]["targetRevenue"]
    if cov is not None and cov > 1.5 and target > 0:
        checks.append({
            "trigger": "coverage_excessive",
            "coverage": cov,
            "forecastedRevenue": results["funnel"]["forecastedRevenue"],
            "targetRevenue": target
        })

    # Trigger 3: sourced override >20pp above template default
    actual_sourced = results["attribution"]["sourcedPct"]
    default_sourced = template.get("sourcedPct", 1.0)
    if actual_sourced - default_sourced > 0.20:
        checks.append({
            "trigger": "sourced_override_high",
            "actual": actual_sourced,
            "default": default_sourced,
            "templateName": template["name"]
        })

    # Trigger 4: absurdly high derived metrics
    # ROI > 15× is almost certainly a data entry error (5× is best-in-class)
    roi = results["derivedMetrics"]["roi"]
    if roi is not None and roi > 15.0:
        checks.append({
            "trigger": "derived_metric_extreme",
            "metric": "roi",
            "value": roi,
            "threshold": 15.0,
            "benchmarkHigh": BENCHMARKS["roi"]["high"]
        })

    # CPL below $50 for B2B is suspiciously cheap — likely a data issue
    cpl = results["derivedMetrics"]["cpl"]
    cpl_bench = overrides.get("cpl", BENCHMARKS["cpl"])
    if cpl is not None and cpl > 0 and cpl < cpl_bench["low"] * 0.25:
        checks.append({
            "trigger": "derived_metric_extreme",
            "metric": "cpl",
            "value": cpl,
            "threshold": cpl_bench["low"] * 0.25,
            "benchmarkLow": cpl_bench["low"]
        })

    # Cost Per SQL below $100 is suspicious
    cps = results["derivedMetrics"]["costPerSql"]
    if cps is not None and cps > 0 and cps < 100:
        checks.append({
            "trigger": "derived_metric_extreme",
            "metric": "costPerSql",
            "value": cps,
            "threshold": 100
        })

    return checks


# ──────────────────────────────────────────────────────────────
# ──────────────────────────────────────────────────────────────
# CLI Interface
# ──────────────────────────────────────────────────────────────

def run_full_analysis(inputs: dict) -> dict:
    """Run the complete analysis pipeline and return all results."""
    template_key = inputs.get("template", "booth_presence")

    results = calculate_funnel(inputs)
    flags = flag_benchmarks(results, template_key)
    sanity = sanity_check(results, flags, template_key)
    fvi = funnel_vs_industry(results, template_key)

    # Root causes for flagged derived metrics
    root_causes = {}
    for metric in ["roi", "coverage", "cpl", "costPerSql"]:
        flag = flags.get(metric, {})
        if flag.get("flag") in ("red", "yellow"):
            root_causes[metric] = root_cause_analysis(results, flags, metric, template_key)

    levers = lever_projections(results, template_key)

    template = get_template(template_key)

    return {
        "results": results,
        "flags": flags,
        "sanityChecks": sanity,
        "funnelVsIndustry": fvi,
        "rootCauses": root_causes,
        "leverProjections": levers,
        "template": template_key,
        "templateName": template.get("name", template_key),
        "templateHosted": template.get("hosted", False),
        "funnelLabels": template.get("funnelLabels", DEFAULT_FUNNEL_LABELS)
    }


# ──────────────────────────────────────────────────────────────
# Calibration Statistics (adaptive averaging)
# ──────────────────────────────────────────────────────────────


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python calc_engine.py --json '{...}' | --file input.json | --compare a.json b.json")
        sys.exit(1)

    if sys.argv[1] == "--json":
        inputs = json.loads(sys.argv[2])
        output = run_full_analysis(inputs)
        print(json.dumps(output, indent=2, default=str))

    elif sys.argv[1] == "--file":
        with open(sys.argv[2]) as f:
            inputs = json.load(f)
        output = run_full_analysis(inputs)
        print(json.dumps(output, indent=2, default=str))

    elif sys.argv[1] == "--compare":
        with open(sys.argv[2]) as f:
            inputs_a = json.load(f)
        with open(sys.argv[3]) as f:
            inputs_b = json.load(f)
        results_a = calculate_funnel(inputs_a)
        results_b = calculate_funnel(inputs_b)
        deltas = compare_scenarios(results_a, results_b)
        print(json.dumps(deltas, indent=2, default=str))

    else:
        print(f"Unknown flag: {sys.argv[1]}")
        sys.exit(1)
