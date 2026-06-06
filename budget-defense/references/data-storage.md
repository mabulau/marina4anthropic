# Data Storage Reference

## Directory Structure

All data lives in `/budget-defense/` within the Cowork Project (or the working directory if not in Cowork). The planner owns their data — it's inspectable, backupable, and version-controllable.

```
/budget-defense/
├── settings.json        — Company-wide config (set once, editable anytime)
├── events.json          — Event history (the system of record)
├── scenarios.json       — Saved scenarios with overrides
├── calibration.json     — Per-category learning state
└── templates.json       — Custom/override templates (planner-defined)
```

## settings.json

Company-wide configuration. Set during first activation.

```json
{
  "salesCycle": {
    "defaultMonths": 4,
    "overrides": {
      "webinar": 2,
      "workshop": 3,
      "executive_dinner": 9,
      "sales_presentation": 6,
      "customer_event": 3
    }
  },
  "defaultCreditWeight": 0.30,
  "globalOverrides": {},
  "notifications": {
    "channel": "slack",
    "destination": "#events-ops",
    "enabled": true
  },
  "lastOpened": "2026-05-20T14:30:00Z",
  "createdAt": "2026-03-15T10:00:00Z"
}
```

### Fields

| Field | Purpose |
|---|---|
| salesCycle.defaultMonths | Company-wide average sales cycle |
| salesCycle.overrides | Per-event-type sales cycle overrides |
| defaultCreditWeight | Default credit weight for influenced revenue |
| globalOverrides | Any benchmark or attribution overrides applied company-wide |
| notifications.channel | email, slack, or teams |
| notifications.destination | Email address, Slack channel, or Teams channel |
| lastOpened | Drives the "X updates since MM/DD/YYYY" counter |

## events.json

Event history with composite keys. This is the system of record.

```json
{
  "events": {
    "AWS re:Invent 2025|2025-12-01": {
      "identity": {
        "name": "AWS re:Invent 2025",
        "date": "2025-12-01",
        "endDate": "2025-12-05",
        "eventType": "conference_presentation",
        "category": "Trade show"
      },
      "inputs": {
        "attendees": 60000,
        "boothVisitorRate": 0.08,
        "leadsRate": 0.50,
        "mqlRate": 0.35,
        "sqlRate": 0.50,
        "winRate": 0.05,
        "acv": 85000,
        "boothCost": 250000,
        "targetRevenue": 2000000
      },
      "attribution": {
        "sourcedPct": 0.75,
        "creditWeight": 0.30
      },
      "outputs": {
        "forecastedRevenue": 1785000,
        "roi": 6.14,
        "coverage": 0.8925,
        "cpl": 104.17,
        "costPerSql": 595.24,
        "targetGap": -215000
      },
      "benchmarkFlags": {
        "boothVisitorRate": "green",
        "leadsRate": "green",
        "roi": "green",
        "coverage": "yellow"
      },
      "reportType": "forecast",
      "source": "master_doc",
      "timestamps": {
        "created": "2025-09-15T10:00:00Z",
        "lastUpdated": "2025-11-20T16:30:00Z"
      }
    }
  }
}
```

### Composite Key Format

`{event name}|{start date}` — e.g., `"AWS re:Invent 2025|2025-12-01"`

This ensures uniqueness: the same event name in different years creates separate entries.

### Event Entry Fields

| Field Group | Contents |
|---|---|
| identity | name, date, endDate, eventType (template key), category |
| inputs | All funnel inputs (attendees, rates, ACV, cost, target) |
| attribution | sourcedPct, creditWeight |
| outputs | All calculated outputs (revenue, ROI, coverage, CPL, etc.) |
| benchmarkFlags | Green/yellow/red for each metric at time of calculation |
| reportType | "forecast" or "actuals" |
| source | "master_doc", "manual", or "override" |
| timestamps | created, lastUpdated |

## scenarios.json

Saved scenarios linked to event names. A scenario is a snapshot of inputs with overrides and settings.

```json
{
  "scenarios": {
    "AWS re:Invent 2026 - Conservative": {
      "identity": {
        "name": "AWS re:Invent 2026 - Conservative",
        "linkedEvent": "AWS re:Invent 2026",
        "eventType": "conference_presentation"
      },
      "inputOverrides": {
        "attendees": 65000,
        "boothCost": 275000,
        "targetRevenue": 2500000
      },
      "tone": "conservative",
      "attribution": {
        "sourcedPct": 0.75,
        "creditWeight": 0.30
      },
      "templateUsed": "conference_presentation",
      "timestamps": {
        "created": "2026-04-10T09:00:00Z",
        "lastUpdated": "2026-04-10T09:00:00Z"
      }
    }
  }
}
```

### Scenario Fields

| Field | Purpose |
|---|---|
| identity.name | Scenario name (planner chooses) |
| identity.linkedEvent | Which event this scenario is for |
| identity.eventType | Template key |
| inputOverrides | Only the fields that differ from the base data |
| tone | conservative / realistic / optimistic |
| attribution | Sourced % and credit weight for this scenario |
| templateUsed | Which template was applied |

## calibration.json

Per-category learning state. Updated by the recurring task when new event data arrives.

```json
{
  "categories": {
    "booth_presence": {
      "eventCount": 12,
      "calibrationStatus": "calibrated",
      "statusLabel": "calibrated, 12 events",
      "runningAverages": {
        "boothVisitorRate": 0.14,
        "leadsRate": 0.42,
        "mqlRate": 0.32,
        "sqlRate": 0.58,
        "winRate": 0.07,
        "cpl": 320,
        "costPerSql": 1800,
        "roi": 4.2
      },
      "varianceRanges": {
        "boothVisitorRate": { "min": 0.08, "max": 0.22 },
        "leadsRate": { "min": 0.35, "max": 0.52 },
        "roi": { "min": 2.1, "max": 7.8 }
      },
      "adaptiveThresholds": {
        "varianceBandPct": 0.15,
        "absoluteFloors": {
          "revenue": 50000,
          "leads": 100,
          "roi": 1.0
        }
      },
      "lastRecalibration": "2026-04-01T12:00:00Z"
    },
    "executive_dinner": {
      "eventCount": 3,
      "calibrationStatus": "learning",
      "statusLabel": "learning 3/5",
      "runningAverages": {
        "boothVisitorRate": 0.72,
        "winRate": 0.28
      },
      "varianceRanges": {},
      "adaptiveThresholds": {
        "varianceBandPct": 0.30
      },
      "lastRecalibration": null
    }
  }
}
```

### Calibration Fields

| Field | Purpose |
|---|---|
| eventCount | How many events in this category |
| calibrationStatus | "learning" (< 5 events) or "calibrated" (≥ 5) |
| statusLabel | Human-readable status for display |
| runningAverages | Current averages per metric |
| varianceRanges | Min/max observed per metric (established at event 5) |
| adaptiveThresholds | Current variance bands and absolute impact floors |
| lastRecalibration | When averages were last recalculated |

## templates.json

Custom templates defined by the planner. These take priority over built-in templates in `match_template()`. Planners can add entirely new templates or override properties of existing ones.

```json
{
  "field_marketing": {
    "name": "Field Marketing Event",
    "description": "Regional field events with mixed format.",
    "hosted": true,
    "sourcedPct": 0.60,
    "creditWeight": 0.30,
    "benchmarkOverrides": {},
    "funnelLabels": {
      "attendees": "Invitees",
      "visitors": "Attendees",
      "leads": "Net New Leads",
      "mql": "MQLs",
      "sql": "SQLs",
      "deals": "Closed-Won Deals",
      "revenue": "Forecasted Revenue"
    },
    "cplSuppressed": false,
    "categoryKeywords": ["field", "regional", "roadshow"]
  }
}
```

### Template Fields

| Field | Required | Purpose |
|---|---|---|
| name | Yes | Display name |
| description | Yes | One-line description |
| hosted | Yes | Does the planner control attendance? (affects attendee lever) |
| sourcedPct | Yes | Default sourced attribution (0-1) |
| creditWeight | Yes | Default credit weight for influenced revenue (0-1) |
| benchmarkOverrides | No | Override any benchmark range for this template |
| funnelLabels | Yes | Labels for each funnel stage (attendees, visitors, leads, mql, sql, deals, revenue) |
| cplSuppressed | No | Whether CPL insight is suppressed (auto-set when sourcedPct < 0.30) |
| categoryKeywords | Yes | Keywords for template matching from Airtable fields |

To override a built-in template, use the same key (e.g., `"booth_presence"`) — the custom version merges over the default.

## Export Formats

### PDF Export

Full report with:
- Event name, date, template used, report type (forecast/actuals)
- Complete funnel with counts at each stage
- Derived metrics with benchmark flags (colored indicators)
- Attribution breakdown (if not 100% sourced)
- All fired insights in full: heading, explanation, return context, root causes, levers with projections
- Generated-on timestamp

Style with inline CSS so the output survives PDF rendering. No external stylesheets.

### Plain Text Export

Copy-friendly text dump for pasting into emails, Slack, or documents:

```
EVENT: AWS re:Invent 2025 | Dec 1-5, 2025
TYPE: Conference Presentation | REPORT: Forecast
───────────────────────────────────
FUNNEL
  Attendees:        60,000
  Booth Visitors:    4,800 (8.0%)
  Net New Leads:     2,400 (50.0%)
  MQLs:                840 (35.0%)
  SQLs:                420 (50.0%)
  Deals:              21.0 (5.0%)
  Forecast Revenue: $1,785,000
───────────────────────────────────
METRICS
  ROI:       6.1× ✅
  Coverage:  89.3% ⚠️
  CPL:       $104 ✅
  Cost/SQL:  $595 ✅
───────────────────────────────────
ATTRIBUTION
  Sourced (75%):    $1,338,750
  Influenced (25%): $446,250
  Credited (30%):   $1,472,625
───────────────────────────────────
INSIGHTS
  [insights in full text form]
───────────────────────────────────
Generated: May 20, 2026
```

### Scenario Comparison Export

Side-by-side with delta highlighting:

```
COMPARISON: Conservative vs Optimistic
──────────────────────────────────────────────
                    Conservative  Optimistic   Δ
Forecast Revenue    $1,003,594    $1,742,969   +$739,375 (+73.6%)
ROI                 3.01×         5.97×        +2.96×
Coverage            50.2%         87.1%        +36.9pp
CPL                 $298          $172         -$126 (-42.3%)
──────────────────────────────────────────────
```

## First Activation — Cowork Setup Flow

When running inside a Cowork Project:

1. **Create data directory:** `/budget-defense/` with the four JSON files initialized empty
2. **Create recurring task:** File event trigger watching the master event document
   - Cowork's native event-driven automation fires when the watched file changes
   - Not timer-based — event-driven
3. **Configure notifications:** Ask planner for channel preference (email/Slack/Teams)
4. **Initial scan:** Read master doc, populate `events.json`, run calculations for all existing events
5. **Set settings:** Sales cycle defaults, credit weight, any global overrides

### Recurring Task Behavior

The task maintains awareness across runs (Cowork context persistence):
- References previous outputs
- Tracks what changed since last execution
- Accumulates calibration data without starting fresh

### Fallback (no Cowork)

If not in a Cowork environment, or if the master doc isn't watchable:
- Same logic runs on each manual activation
- Planner opens the skill → skill checks master doc → processes any changes
- All the same checks apply (composite key matching, calibration, alerts)
