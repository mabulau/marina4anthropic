"""Budget Defense — Templates, Benchmarks, and Tone Configuration"""

# ──────────────────────────────────────────────────────────────
# Industry Benchmark Ranges (defaults — templates can override)
# ──────────────────────────────────────────────────────────────

BENCHMARKS = {
    "boothVisitorRate": {"low": 0.05, "high": 0.20, "direction": "within-range"},
    "leadsRate":        {"low": 0.35, "high": 0.60, "direction": "higher-is-better"},
    "mqlRate":          {"low": 0.25, "high": 0.40, "direction": "higher-is-better"},
    "sqlRate":          {"low": 0.40, "high": 0.70, "direction": "higher-is-better"},
    "winRate":          {"low": 0.10, "high": 0.25, "direction": "higher-is-better"},
    "cpl":              {"low": 180,  "high": 700,  "direction": "lower-is-better"},
    "costPerSql":       {"low": 540,  "high": 5000, "direction": "lower-is-better"},
    "coverage":         {"low": 1.0,  "high": float("inf"), "direction": "higher-is-better"},
    "roi":              {"low": 3.0,  "high": 5.0,  "direction": "higher-is-better"},
}

MARKETING_INVESTMENT_PCT = 0.10  # industry rule of thumb: 10% of revenue goes to marketing

# ──────────────────────────────────────────────────────────────
# Event Type Templates
# ──────────────────────────────────────────────────────────────

# Default funnel labels (used when template doesn't override)
DEFAULT_FUNNEL_LABELS = {
    "attendees": "Attendees",
    "visitors": "Booth Visitors",
    "leads": "Net New Leads",
    "mql": "MQLs",
    "sql": "SQLs",
    "deals": "Closed-Won Deals",
    "revenue": "Forecasted Revenue"
}

TEMPLATES = {
    "booth_presence": {
        "name": "Booth Presence",
        "description": "Trade show booth walk-ups. Highest sourced attribution.",
        "hosted": False,
        "sourcedPct": 0.75,
        "creditWeight": 0.30,
        "benchmarkOverrides": {"winRate": {"low": 0.02, "high": 0.10}},
        "funnelLabels": {
            "attendees": "Attendees",
            "visitors": "Booth Visitors",
            "leads": "Net New Leads",
            "mql": "MQLs",
            "sql": "SQLs",
            "deals": "Closed-Won Deals",
            "revenue": "Forecasted Revenue"
        },
        "cplSuppressed": False,
        "categoryKeywords": ["trade show", "expo", "exhibit", "booth"]
    },
    "sales_presentation": {
        "name": "Sales Presentation",
        "description": "1:1 or small-group demos. Mostly influenced.",
        "hosted": True,
        "sourcedPct": 0.25,
        "creditWeight": 0.30,
        "benchmarkOverrides": {"winRate": {"low": 0.15, "high": 0.30}},
        "funnelLabels": {
            "attendees": "Invitees",
            "visitors": "Attendees",
            "leads": "Prospects",
            "mql": "Qualified Prospects",
            "sql": "Sales-Ready",
            "deals": "Closed-Won Deals",
            "revenue": "Forecasted Revenue"
        },
        "cplSuppressed": True,
        "categoryKeywords": ["demo", "presentation", "sales meeting"]
    },
    "webinar": {
        "name": "Webinar",
        "description": "Online presentation. Mixed audience.",
        "hosted": True,
        "sourcedPct": 0.55,
        "creditWeight": 0.30,
        "benchmarkOverrides": {},
        "funnelLabels": {
            "attendees": "Registrants",
            "visitors": "Live Attendees",
            "leads": "Engaged Leads",
            "mql": "MQLs",
            "sql": "SQLs",
            "deals": "Closed-Won Deals",
            "revenue": "Forecasted Revenue"
        },
        "cplSuppressed": False,
        "categoryKeywords": ["webinar", "virtual", "online"]
    },
    "conference_presentation": {
        "name": "Conference Presentation",
        "description": "Keynote or breakout session.",
        "hosted": False,
        "sourcedPct": 0.75,
        "creditWeight": 0.30,
        "benchmarkOverrides": {"winRate": {"low": 0.02, "high": 0.10}},
        "funnelLabels": {
            "attendees": "Session Attendees",
            "visitors": "Engaged Attendees",
            "leads": "Net New Leads",
            "mql": "MQLs",
            "sql": "SQLs",
            "deals": "Closed-Won Deals",
            "revenue": "Forecasted Revenue"
        },
        "cplSuppressed": False,
        "categoryKeywords": ["conference", "summit", "keynote", "breakout", "speaking"]
    },
    "executive_dinner": {
        "name": "Executive Dinner",
        "description": "Curated high-touch event. Mostly influenced.",
        "hosted": True,
        "sourcedPct": 0.30,
        "creditWeight": 0.30,
        "benchmarkOverrides": {"cpl": {"low": 1000, "high": 6000}},
        "funnelLabels": {
            "attendees": "Invited Executives",
            "visitors": "Confirmed Attendees",
            "leads": "Engaged Contacts",
            "mql": "Qualified Opportunities",
            "sql": "Sales-Ready Opportunities",
            "deals": "Closed-Won Deals",
            "revenue": "Forecasted Revenue"
        },
        "cplSuppressed": False,
        "categoryKeywords": ["dinner", "roundtable", "executive", "intimate"]
    },
    "workshop": {
        "name": "Workshop",
        "description": "Interactive hands-on session. 50/50 sourced/influenced.",
        "hosted": True,
        "sourcedPct": 0.50,
        "creditWeight": 0.30,
        "benchmarkOverrides": {},
        "funnelLabels": {
            "attendees": "Registrants",
            "visitors": "Participants",
            "leads": "Net New Leads",
            "mql": "MQLs",
            "sql": "SQLs",
            "deals": "Closed-Won Deals",
            "revenue": "Forecasted Revenue"
        },
        "cplSuppressed": False,
        "categoryKeywords": ["workshop", "training", "hands-on", "lab"]
    },
    "customer_event": {
        "name": "Customer Event",
        "description": "Existing-customer expansion/upsell/renewal. 0% sourced.",
        "hosted": True,
        "sourcedPct": 0.00,
        "creditWeight": 0.30,
        "benchmarkOverrides": {
            "boothVisitorRate": {"low": 0.60, "high": 0.90, "direction": "within-range"},
            "winRate": {"low": 0.20, "high": 0.50}
        },
        "funnelLabels": {
            "attendees": "Invited Customers",
            "visitors": "RSVP Attendees",
            "leads": "Engaged Customers",
            "mql": "Expansion Opportunities",
            "sql": "Qualified Opportunities",
            "deals": "Closed Deals",
            "revenue": "Expansion Revenue"
        },
        "cplSuppressed": True,
        "categoryKeywords": ["customer", "user conference", "advisory", "appreciation"]
    }
}


def get_template(template_key: str, custom_templates: dict = None) -> dict:
    """
    Get a template by key. Checks custom templates first (from settings/templates.json),
    then falls back to built-in defaults. This allows planners to add or override templates.
    """
    if custom_templates and template_key in custom_templates:
        # Merge custom over defaults so partial overrides work
        base = TEMPLATES.get(template_key, {}).copy()
        base.update(custom_templates[template_key])
        return base
    return TEMPLATES.get(template_key, TEMPLATES["booth_presence"])


def match_template(event_type: str = "", event_format: str = "", event_category: str = "",
                   custom_templates: dict = None) -> str:
    """
    Match an event to the best template using type, format, and category fields.
    Category refines the match: a 'Conference' with 'Customer engagement' category
    maps to customer_event, not conference_presentation.
    Custom templates are checked first for keyword matches (planner's templates take priority).

    Returns the template key.
    """
    event_type_lower = (event_type or "").lower()
    event_format_lower = (event_format or "").lower()
    event_category_lower = (event_category or "").lower()

    # Category-first overrides: these take priority regardless of type
    if "customer" in event_category_lower:
        return "customer_event"

    # Format-specific overrides
    if event_format_lower in ("dinner", "roundtable"):
        return "executive_dinner"

    # Check custom templates FIRST for keyword matches (planner's templates take priority)
    if custom_templates:
        for key, tmpl in custom_templates.items():
            keywords = tmpl.get("categoryKeywords", [])
            for kw in keywords:
                if kw in event_type_lower or kw in event_format_lower:
                    return key

    # Then check built-in templates
    for key, tmpl in TEMPLATES.items():
        keywords = tmpl.get("categoryKeywords", [])
        for kw in keywords:
            if kw in event_type_lower or kw in event_format_lower:
                return key

    # Default
    return "booth_presence"

# ──────────────────────────────────────────────────────────────
# Scenario Tone Bands (per-stage variance)
# ──────────────────────────────────────────────────────────────
# Upstream rates vary more than downstream rates. Booth visitor rate
# swings with booth location and floor traffic; win rate is structural.
# These fixed bands are used pre-calibration. Post-calibration (5+ events),
# the planner's own variance range replaces these.

TONE_BANDS = {
    "conservative": {
        "boothVisitorRate": 0.65,   # -35% — high variance (booth location, traffic)
        "leadsRate":        0.78,   # -22% — medium-high (staff quality, qualification)
        "mqlRate":          0.82,   # -18% — medium (follow-up speed, ICP fit)
        "sqlRate":          0.88,   # -12% — medium-low (sales capacity)
        "winRate":          0.90,   # -10% — low (structural: product, pricing)
    },
    "realistic": {
        "boothVisitorRate": 1.0,
        "leadsRate":        1.0,
        "mqlRate":          1.0,
        "sqlRate":          1.0,
        "winRate":          1.0,
    },
    "optimistic": {
        "boothVisitorRate": 1.35,   # +35%
        "leadsRate":        1.22,   # +22%
        "mqlRate":          1.18,   # +18%
        "sqlRate":          1.12,   # +12%
        "winRate":          1.10,   # +10%
    }
}

# Legacy flat multipliers (kept for backward compatibility)
TONES = {
    "conservative": 0.75,
    "realistic": 1.0,
    "optimistic": 1.25
}


def get_tone_multipliers(tone: str, calibration: dict = None) -> dict:
    """
    Get per-rate tone multipliers. Hybrid approach:
    - Pre-calibration: uses fixed TONE_BANDS based on natural variance by stage
    - Post-calibration: uses the planner's own observed variance range

    calibration: dict from calibration.json for this event category, or None.
        Expected shape: {"varianceRanges": {"boothVisitorRate": {"min": 0.08, "max": 0.22}, ...},
                         "runningAverages": {"boothVisitorRate": 0.14, ...}}
    """
    if tone == "realistic":
        return {k: 1.0 for k in ["boothVisitorRate", "leadsRate", "mqlRate", "sqlRate", "winRate"]}

    # Post-calibration: use planner's own variance
    if calibration and calibration.get("varianceRanges"):
        ranges = calibration["varianceRanges"]
        averages = calibration.get("runningAverages", {})
        multipliers = {}

        for rate_key in ["boothVisitorRate", "leadsRate", "mqlRate", "sqlRate", "winRate"]:
            r = ranges.get(rate_key, {})
            avg = averages.get(rate_key)

            if r and avg and avg > 0:
                if tone == "conservative":
                    # Conservative = ratio of historical low to average
                    multipliers[rate_key] = r.get("low", avg) / avg
                elif tone == "optimistic":
                    # Optimistic = ratio of historical high to average
                    multipliers[rate_key] = r.get("high", avg) / avg
                else:
                    multipliers[rate_key] = 1.0
            else:
                # Fall back to fixed bands for rates without calibration data
                multipliers[rate_key] = TONE_BANDS.get(tone, TONE_BANDS["realistic"]).get(rate_key, 1.0)

        return multipliers

    # Pre-calibration: use fixed bands
    return TONE_BANDS.get(tone, TONE_BANDS["realistic"]).copy()
