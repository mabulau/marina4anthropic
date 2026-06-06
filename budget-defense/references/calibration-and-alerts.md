# Calibration & Alerts Reference

## Calibration Loop

The system learns from accumulated event data. Each event category (mapped from templates) maintains its own calibration state.

### How It Works

**Events 1–4 (learning phase):**
- The system is collecting data. Status shows "learning 3/5" (or whatever the count is).
- Industry benchmarks are the primary reference. The system calculates using defaults.
- Each event's actual rates are recorded for future calibration.

**Event 5 (first calibration):**
- The system has enough data to establish baseline averages AND natural variance ranges.
- Running averages are calculated for every metric across all 5 events.
- Natural variance range = the spread observed in those 5 events (min to max for each metric).
- Status changes to "calibrated, 5 events."
- The planner is actively notified that their baseline has been established.

**Events 6+ (ongoing recalibration):**
- After every 5th event (event 10, 15, 20...), running averages are recalculated.
- Between recalibrations, new events update the running totals but don't trigger a full recalculation.
- The planner is actively notified each time a recalibration occurs.

### Calibration Status Display

Always show the planner where each category stands:
- **Pre-calibration:** "learning 3/5" — transparent about how much data the system has
- **Calibrated:** "calibrated, 12 events" — planner knows how much trust to put in the numbers
- **Just recalibrated:** "recalibrated at 15 events — baseline updated" — planner knows averages shifted

### What Gets Calibrated

Per category, the system tracks running averages for:
- Booth visitor rate
- Leads rate
- MQL rate
- SQL rate
- Win rate
- CPL
- Cost per SQL
- ROI

The averaging method adapts to sample size using `compute_calibration_stats()`:

| Events | Central Tendency | Variance Range | Rationale |
|---|---|---|---|
| 1–4 | Simple mean (pre-calibration) | N/A | Not enough data for robust stats |
| 5–9 | Median | Min–Max | Outlier protection at small samples |
| 10+ | Trimmed mean (drop top/bottom 10%) | P25–P75 (interquartile range) | More data, can trim while keeping information |

**Divergence check:** The system always computes both the robust average (median or trimmed mean) and the simple mean. If they diverge by more than 15%, it flags the planner: "Your average ROI is 3.8× (median), but the simple mean is 12.9× — one or two strong outliers are pulling the average up." This transparency lets the planner decide which number to defend.

**Why this matters for tone bands:** The variance range feeds directly into the per-stage tone multipliers. At 5–9 events, conservative tone uses the historical min and optimistic uses the max. At 10+ events, conservative uses P25 and optimistic uses P75 — representing where performance "usually" falls, not where it fell that one time. This prevents one bad event from forever anchoring the conservative scenario.

Once calibrated, these averages can replace or supplement industry benchmarks for that category. The planner always sees both: "Your average booth visitor rate for trade shows: 14% (industry: 5–20%)."

## Adaptive Alert Thresholds

Rather than flat percentage thresholds, alert sensitivity scales with context:

### Event Size Bands

| Event Size | Variance Band | Rationale |
|---|---|---|
| Small (< 200 attendees) | ±30% | Intimate dinners, roundtables — high natural fluctuation |
| Medium (200–2,000) | ±20% | Regional events, workshops |
| Large (2,000–10,000) | ±15% | Major conferences |
| Very Large (10,000+) | ±10% | Flagship events — small % = large absolute numbers |

### Absolute Impact Floor

Even when a percentage change looks mild, catch significant absolute shifts:
- Revenue shift > $50,000
- Lead count shift > 100
- ROI shift > 1.0×

If an absolute floor is breached, the alert fires regardless of percentage.

### Post-Calibration (5+ events)

Once a category is calibrated from real data, variance bands become genuinely adaptive:
- Use the natural variance range from the first 5 events as the baseline band
- Tighten or widen based on observed consistency (if all 5 events had similar rates, the band is narrow; if they varied widely, the band stays wide)

## Big Jump Alerts

When a new event's data would shift a category average significantly beyond its variance band, the system flags it for review before incorporating.

### How It Works

1. New event data arrives (from master doc or planner input)
2. System calculates what the category average would be WITH this new data
3. Compares the shift to the current variance band
4. If the shift exceeds the band → **Big Jump Alert**

### Alert Content

The alert includes:
- Which metric jumped and by how much
- Current category average vs. what it would become
- Whether this looks like an outlier or a genuine shift
- Action required: planner confirms or rejects before the data affects calibration averages

### Why This Matters

Without this guardrail, a single exceptional event (or data entry error) could silently skew all future projections for that category. The planner reviews before the data is incorporated.

## Sales Cycle Guardrail

Revenue attribution takes time. A trade show in March might not close deals until July. If the system processes actuals from a recent event, the revenue numbers are likely incomplete.

### Configuration

Set during first activation in `settings.json`:

**Company-wide default:** e.g., 4 months

**Per-event-type overrides:**
| Event Type | Typical Sales Cycle | Rationale |
|---|---|---|
| Webinar | 2 months | Digital leads move faster |
| Trade Show | 4 months | Standard B2B cycle |
| Conference | 4 months | |
| Workshop | 3 months | Hands-on engagement accelerates |
| Executive Dinner | 9 months | High-value deals take longer |
| Customer Event | 3 months | Existing relationship shortens cycle |
| Sales Presentation | 6 months | Enterprise sales cycles |

### How It Fires

When processing a new event with actuals:
1. Check the event date against today
2. Look up the applicable sales cycle (event-type override, or company default)
3. If `today - eventDate < salesCycleLength` → **Sales Cycle Alert**

### Alert Content

The alert contextualizes without hiding:
- "This event was [X] weeks ago. Your typical sales cycle for [event type] is [Y] months. Revenue attribution is likely incomplete — [Z]% of the sales cycle has elapsed."
- The numbers are still shown, but the planner knows not to make decisions off them yet
- Suggest revisiting after the full sales cycle has passed

## Cowork Recurring Task Behavior

In a Cowork environment, these alerts are delivered via the recurring task:

### Passive Updates (no interruption)
- New event data within normal parameters
- Updates to `events.json` and recalculated metrics
- Summary surfaced next time planner opens the skill: "3 updates since 05/14/2026"

### Active Alerts (immediate notification)
- Big jump detected → notify before incorporating
- Category recalibration at 5th event → notify that baseline changed
- Sales cycle guardrail fires → notify that revenue data is premature

### Notification Channels

Configured during first activation. Options:
- Email
- Slack message
- Teams message

The alert is concise: what changed, why it matters, what action is needed. Include a link or prompt to open the skill for full details.

## Processing Logic for New Event Data

When the system receives new event data (from file trigger or manual activation):

```
1. Extract composite key: event name + date
2. If key doesn't exist → new event
   a. Create entry in events.json
   b. Run full calculations
   c. Check calibration: has category hit 5th event? → recalibrate + notify
   d. Evaluate big jump: would this shift averages beyond variance band? → alert
   e. Check sales cycle: is event too recent? → warn
3. If key exists and data changed → updated event
   a. Diff incoming vs. saved values
   b. Update entry in events.json
   c. Recalculate
   d. Re-evaluate alerts (big jump, sales cycle)
4. If key exists and no changes → skip
```
