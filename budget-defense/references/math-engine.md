# Math Engine Reference

## Funnel Pipeline

Each stage is a multiplication. The full chain:

```
attendees × boothVisitorRate × leadsRate × mqlRate × sqlRate × winRate × ACV = forecasted revenue
```

Intermediate stages:
- boothVisitors = attendees × boothVisitorRate
- netNewLeads = boothVisitors × leadsRate
- MQLs = netNewLeads × mqlRate
- SQLs = MQLs × sqlRate
- deals = SQLs × winRate
- forecastedRevenue = deals × ACV

## Derived Metrics

| Metric | Formula | Null Safety |
|---|---|---|
| ROI | (forecastedRevenue − boothCost) / boothCost | Falls back to targetBoothCost when boothCost is blank/0 |
| Conversion Coverage | forecastedRevenue / targetRevenue × 100 | None when targetRevenue is 0 |
| CPL | boothCost / netNewLeads | None when leads = 0 |
| Cost Per SQL | boothCost / SQLs | None when SQLs = 0 |
| Target Gap | forecastedRevenue − targetRevenue | None when targetRevenue is 0 |
| Target Booth Cost | targetRevenue × marketingInvestmentPct (10%) | Always computable |
| Estimated Booth Cost | forecastedRevenue × marketingInvestmentPct (10%) | Always computable |

When boothCost is blank or 0, the engine uses targetBoothCost as the effective cost to avoid division by zero. NaN is returned for undefined ratios so the UI can show "—" instead of misleading zeros.

## Attribution Layer

Revenue splits into sourced (event as first touch) and influenced (event was one of several touches):

```
sourcedRevenue = forecastedRevenue × sourcedPct
influencedRevenue = forecastedRevenue × (1 − sourcedPct)
influencedCredit = influencedRevenue × creditWeight
creditedRevenue = sourcedRevenue + influencedCredit
```

The attribution layer does NOT change core engine math. ROI, coverage, and target gap stay based on full forecasted revenue. Attribution lets the planner defend a specific claim level to finance.

**Defaults:**
- sourcedPct: 100% (unless template overrides)
- creditWeight: 30% (mid-point of the 25–50% range most multi-touch models land in)

**Cross-event attribution limitation:** The attribution layer handles sourced vs. influenced within a single event. It does NOT deduplicate prospects across events. If a prospect visits your booth at Cloud Expo in May and attends your executive dinner in June, both events independently claim their share of the revenue when that prospect closes. The parent/child roll-up (`roll_up_child_events`) has the same characteristic — it sums revenue across children assuming independent funnels.

This is a known simplification. True cross-event deduplication requires CRM-level prospect tracking (mapping individual contacts to event touchpoints), which is outside the scope of this system. The planner should be aware that summing credited revenue across their full event portfolio may overcount total attributed revenue. To mitigate: use the credited revenue figure (which applies the credit weight to influenced revenue) rather than full forecasted revenue when aggregating across events. The credit weight exists precisely to discount the portion of revenue that multiple events may be claiming.

## Scenario Tones

Three tones adjust rates before calculation using per-stage variance bands (not a flat multiplier). Upstream rates get larger swings than downstream rates because they naturally vary more event-to-event. See `references/templates-and-benchmarks.md` for the full variance table.

Pre-calibration: fixed per-stage bands (booth ±35%, leads ±22%, MQL ±18%, SQL ±12%, win ±10%).
Post-calibration (5+ events): the planner's own historical low/high per rate replaces the fixed bands.

Rates are capped at 1.0 and floored at 0 after tone adjustment.

## Running the Engine

Always use the script for calculations:

```bash
python scripts/calc_engine.py --json '{"attendees": 5000, "boothVisitorRate": 0.12, ...}'
python scripts/calc_engine.py --file inputs.json
python scripts/calc_engine.py --compare scenario_a.json scenario_b.json
```

The `run_full_analysis()` function returns the complete analysis: funnel results, flags, sanity checks, funnel vs industry, root causes, and lever projections.

### Required Input Fields

| Field | Type | Notes |
|---|---|---|
| attendees | int | Total conference attendees |
| boothVisitorRate | float 0–1 | % who visit the booth |
| leadsRate | float 0–1 | % of visitors who become net new leads |
| mqlRate | float 0–1 | % of leads that become MQLs |
| sqlRate | float 0–1 | % of MQLs that become SQLs |
| winRate | float 0–1 | % of SQLs that close |
| acv | float $ | Average contract value |

### Optional Input Fields

| Field | Type | Default | Notes |
|---|---|---|---|
| boothCost | float $ | 0 | Falls back to targetBoothCost |
| targetRevenue | float $ | 0 | For coverage calculation |
| sourcedPct | float 0–1 | 1.0 | Template overrides |
| creditWeight | float 0–1 | 0.30 | Influenced revenue credit |
| template | string | "booth_presence" | Template key |
| tone | string | "realistic" | conservative/realistic/optimistic |

## Airtable Field Mapping

When reading event data from the Airtable Events table (Base 1):

| Airtable Field | Engine Input | Notes |
|---|---|---|
| `Event Name` | event identity (composite key) | Combined with date for unique ID |
| `Event Start Date` | event identity (composite key) | |
| `Expected Number of Attendees` | attendees | |
| `Estimated Budget` | boothCost (forecast mode) | |
| `Actual Budget` | boothCost (actuals mode) | Use when event is past |
| `Event Type` | → template selection | See mapping below |
| `Event Format` | → template selection (secondary) | Used when Event Type is ambiguous |
| `Event Category` | → attribution hints | "Sales / pipeline generation" → higher sourced |

### Event Type → Template Mapping

| Airtable Event Type | Template Key | Notes |
|---|---|---|
| Trade show | booth_presence | |
| Conference | conference_presentation | |
| Summit | conference_presentation | |
| Workshop | workshop | |
| Webinar | webinar | |
| Developer event | conference_presentation | Tech audience, sourced-heavy |
| Regional meetup | booth_presence | Smaller scale but same model |
| Partner Event | booth_presence | Default; planner can override |
| Other | booth_presence | Default; planner should specify |

When `Event Format` provides more detail:
- Dinner → executive_dinner
- Roundtable → executive_dinner
- Expo → booth_presence

If `Event Category` includes "Customer" focus → customer_event template.

### Fields NOT in Airtable (planner provides or defaults apply)

The Airtable Events table stores event identity, logistics, and budget — but not funnel conversion rates. These come from:

1. **Template defaults** — each template has standard rate ranges
2. **Saved scenarios** — if this event was analyzed before, use saved rates
3. **Calibrated averages** — if the category has 5+ events, use learned rates
4. **Planner input** — the planner provides rates conversationally
5. **Industry benchmarks** — last resort fallback

The planner always provides or confirms: ACV, target revenue, and any rate they have actual data for.
