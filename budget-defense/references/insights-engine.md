# Insights Engine Reference

## Overview

Six deterministic insight generators. Every insight is derived from the formulas, not industry advice. Each surfaces only when its metric is flagged, and includes a formula explanation, root cause analysis, and actionable levers with concrete projections.

**Quick reference — jump to the section you need:**
- CPL flagged? → `## 1. CPL Insight`
- Cost Per SQL flagged? → `## 2. Cost Per SQL Insight`
- ROI flagged? → `## 3. ROI Insight`
- Rates look suspicious? → `## 4. Sanity Check`
- Revenue vs industry? → `## 5. Funnel vs Industry`
- Coverage below target? → `## 6. Coverage Insight`
- Need root cause analysis? → `## Root Cause Analysis`
- Need lever projections? → `## Lever System`
- Calibrated vs industry copy? → `## Source-Aware Copy Patterns`

**Panel tagline:** "Math-based suggestions — every lever comes from the formulas, not industry advice."

**When all metrics are in range:** "All metrics are in range. When something drifts outside the benchmarks, this panel will show which inputs to adjust to bring it back."

## Insight Priority and Deduplication

Present insights in this order:

1. **Sanity Check** (culprit tier — "is this real?")
2. **Funnel vs Industry** (culprit tier — "how does it compare?")
3. **ROI** (hero derived metric)
4. **Coverage**
5. **CPL**
6. **Cost Per SQL**

The top-ranked insight keeps its root causes. All subsequent insights drop their root causes to avoid repeating the same upstream-rate analysis across multiple cards.

## Forecast vs. Actuals Voice

The entire insights layer switches voice based on report type. Use the correct column:

| Element | Forecast (prescriptive) | Actuals (explanatory) |
|---|---|---|
| Headings | "ROI is below expectations" | "ROI came in below expectations" |
| Revenue label | "Forecast Revenue" | "Revenue" |
| Return context verb | "means" | "represented" |
| Loss phrasing | "the event is forecast to cost more than it generates" | "the event cost more than it generated" |
| Root cause section title | "What's dragging this down" | "Why" |
| Root cause action | "restoring it to X alone lifts…" | "had it hit X, the metric would have been…" |
| Root cause target label | "target X%" | "industry typical: X%" |
| Prescriptive tails | Present | Omitted |
| Levers | Full list with projections | Omitted entirely |

---

## 1. CPL Insight

**Fires when:** CPL is flagged red or yellow.

**Suppressed when:** sourced < 30% — high CPL is expected for exec dinners and pipeline-acceleration events.

### Copy Patterns

**Heading (forecast):** "Cost Per Lead is above the healthy range"
**Heading (actuals):** "Cost Per Lead came in above the healthy range"

**Explanation (forecast):** "CPL = [Event Budget] ÷ Net New Leads. To lower it, reduce the numerator or grow the denominator."
**Explanation (actuals):** "CPL = [Event Budget] ÷ Net New Leads."

**Projection example:** "10% less [Event Budget] (→ $67,500) lowers CPL to $185."

**Lever reasons:**
- boothCost: "direct numerator of CPL"
- boothVisitorRate: "more visitors → more leads (denominator)"
- leadsRate: "more leads directly (denominator)"

---

## 2. Cost Per SQL Insight

**Fires when:** Cost Per SQL is flagged red or yellow.

**Suppressed when:** sourced < 30% (same logic as CPL).

**Benchmark:** Dynamically derived at 3×–7× CPL when no template override exists.

### Copy Patterns

**Heading (forecast):** "Cost Per SQL is above the healthy range"
**Heading (actuals):** "Cost Per SQL came in above the healthy range"

**Explanation (forecast):** "Cost Per SQL = [Event Budget] ÷ SQLs. To lower it, reduce cost or raise the downstream conversion rates."
**Explanation (actuals):** "Cost Per SQL = [Event Budget] ÷ SQLs."

**Projection example:** "10% less [Event Budget] lowers Cost Per SQL to $1,250."

**Lever reasons:**
- boothCost: "direct numerator"
- mqlRate: "grows MQLs → SQLs (denominator)"
- sqlRate: "direct multiplier on SQLs (denominator)"
- leadsRate: "more leads feed the MQL→SQL chain"

---

## 3. ROI Insight

**Fires when:** ROI is flagged red or yellow.

### Copy Patterns

**Heading (forecast):** "ROI is below expectations"
**Heading (actuals):** "ROI came in below expectations"

**Explanation (forecast):** "ROI = (Forecast Revenue − [Event Budget]) ÷ [Event Budget]. To raise it, either grow forecast revenue or shrink cost."
**Explanation (actuals):** "ROI = (Revenue − [Event Budget]) ÷ [Event Budget]."

**Return context (profit, forecast):** "[X.X]× means a $[amount] profit on $[amount] spent — positive return, but below the 3× industry median (5× is best-in-class)."
**Return context (profit, actuals):** "[X.X]× represented a $[amount] profit on $[amount] spent — positive return, but below the 3× industry median (5× is best-in-class)."

**Return context (loss, forecast):** "[X.X]× means a $[amount] loss on $[amount] spent — the event is forecast to cost more than it generates."
**Return context (loss, actuals):** "[X.X]× represented a $[amount] loss on $[amount] spent — the event cost more than it generated."

**Cost projection:** "10% less [Event Budget] (→ $[amount]) lifts ROI from [X.X]× to [X.X]×."
**ACV projection:** "10% more [Avg Deal Value] (→ $[amount]) lifts ROI to [X.X]× and revenue to $[amount]."

**Lever reasons:**
- boothCost: "both numerator and denominator — biggest lever"
- acv: "linear multiplier on forecast revenue"
- rates (all): "compounds into forecast revenue"
- attendees: "scales the whole funnel"

---

## 4. Sanity Check

**Fires when:** Any of three triggers hit. Calm tone. Fires as a 'culprit' tier (ranks above effect-level insights).

### Copy Patterns

**Heading (forecast):** "Worth a sanity check"
**Heading (actuals):** "A few things to double-check"

**Explanation (forecast):** "Some of these inputs are outside what's typical. You're either set up for a strong event, or one of these is a hopeful guess rather than a measured value — worth double-checking before treating the forecast as decided."
**Explanation (actuals):** "These inputs landed outside what's typical. Worth a second look before sharing this as actuals."

### Triggers

**Trigger 1 — Rate above industry high:**
"[Rate Name] at [X]% is well above the typical [low]–[high]% range"

**Trigger 2 — Coverage exceeds 150%:**
"Forecast revenue ($[amount]) is [X.X]× the [Revenue Target] ($[amount]) — either the target is outdated, or one or more conversion rates are more optimistic than they look"

**Trigger 3 — Sourced override exceeds template default by >20pp:**
"You've set sourced revenue at [X]% for [a Template Name] — that's well above the typical [low]–[high]% for this event type. Be ready to defend the lift to finance"

**Trigger 4 — Derived metric at extreme value:**
- ROI > 15×: "ROI at [X.X]× is exceptionally high (5× is best-in-class). Double-check that your cost and conversion rates are accurate before sharing this forecast"
- CPL below 25% of industry low: "CPL at $[X] is unusually low for B2B events (industry starts at $[low]). Verify your lead count and budget figures"
- Cost Per SQL below $100: "Cost Per SQL at $[X] is unusually low. Verify your SQL count — this typically indicates a data quality issue rather than exceptional performance"

---

## 5. Funnel vs Industry

**Fires when:** Spread between forecasted revenue and industry rule-of-thumb exceeds 15%.

**Industry rule of thumb:** expectedRevenue = eventCost / marketingInvestmentPct (10%)

Fires as a 'culprit' tier.

### Copy Patterns

**Heading (outperforming, forecast):** "Your funnel is significantly outperforming industry average expectations"
**Heading (outperforming, actuals):** "Excellent — your funnel beat industry average expectations by [X]%"
**Heading (underperforming, forecast):** "Your funnel is forecasting [X]% below industry average expectations"
**Heading (underperforming, actuals):** "Your funnel came in [X]% below industry average expectations"

**Explanation (outperforming):** "Industry rule of thumb says a $[cost] budget should generate around $[expected] in revenue. Your funnel is forecasting $[actual] — that's [X.X]× what industry expects. [tail]"
**Explanation (underperforming):** "Industry rule of thumb says a $[cost] budget should generate around $[expected]. Your funnel is forecasting only $[actual]. [tail]"

### Tails (appended to explanation)

**With top driver, outperforming:** "The biggest lift is coming from [Rate] at [X]% (industry [low]–[high]%) — [above the industry high / in the upper half of the typical range]."
**With top driver, underperforming:** "The biggest drag is [Rate] at [X]% (industry [low]–[high]%) — [below the industry low / in the lower half of the typical range]."
**No drivers, outperforming:** "Your conversion rates are doing real work here."
**No drivers, underperforming:** "Several rates are sitting toward the lower half of their industry ranges; small lifts add up multiplicatively across the funnel."

**Return context (outperforming):** "Strongest rates: [Rate X% (industry low–high%), Rate X%, …]"
**Return context (underperforming):** "Weakest rates: [Rate X% (industry low–high%), Rate X%, …]"

---

## 6. Coverage Insight

**Fires when:** Coverage is below 100%.

### Copy Patterns

**Heading (forecast):** "Coverage is below 100% of your revenue target"
**Heading (actuals):** "Coverage came in below 100% of your revenue target"

**Explanation (forecast):** "Coverage = Forecast Revenue ÷ [Revenue Target]. To close the gap, grow forecast revenue (or revisit the target if it was too aggressive)."
**Explanation (actuals):** "Coverage = Revenue ÷ [Revenue Target]."

**ACV projection:** "10% more [Avg Deal Value] lifts forecast revenue to $[amount] and coverage to [X]%."

**Ambitious target context (when all rates are already healthy, forecast only):**
- For hosted/owned events (customer_event, workshop, executive_dinner): "Your conversion rates are already within industry typical ranges. The gap to target won't close by tuning rates alone — to lift forecast revenue, grow [Attendees] or [Avg Deal Value]. If those aren't movable, your [Revenue Target] may be more aggressive than this funnel can deliver."
- For third-party events (booth_presence, conference_presentation, webinar, sales_presentation): "Your conversion rates are already within industry typical ranges. The gap to target won't close by tuning rates alone — to lift forecast revenue, grow [Avg Deal Value]. If that's not movable, your [Revenue Target] may be more aggressive than this funnel can deliver."

The difference: attendees is only a lever the planner controls for events they host. At a third-party trade show or conference, total attendance is set by the organizer — telling the planner to "grow attendees from 12,000 to 20,000" is not actionable.

**Lever reasons:**
- acv: "linear multiplier on forecast revenue"
- rates: "compounds into forecast revenue"
- attendees: "scales the whole funnel" — **only surface for hosted/owned event templates** (customer_event, workshop, executive_dinner)
- targetRevenue: "direct denominator — only adjust if the target was unrealistic"

---

## Root Cause Analysis (applies to ROI, coverage, CPL, cost per SQL)

For derived metrics, the system identifies every upstream rate currently out of range in the harmful direction, projects what the metric would be if that single rate were restored to its nearest industry edge, and sorts by impact magnitude.

### Copy Patterns

**Section title (forecast):** "What's dragging this down"
**Section title (actuals):** "Why"

**Root cause line (forecast):** "[Rate Name] is at [X.X]% (target [X]%) — restoring it to [X]% alone lifts the metric from [baseline] to [projected]."
**Root cause line (actuals):** "[Rate Name] came in at [X.X]% (industry typical: [X]%) — had it hit [X]%, the metric would have been [projected] instead of [baseline]."

### Rules

- Only rates out of range in the harmful direction are surfaced
- Rates out of range in the GOOD direction are propping the metric up — skip them
- If restoring a rate to its edge would actually LOWER the parent metric, skip it
- The calc engine's `root_cause_analysis()` function handles all of this

---

## Lever System (forecast mode only)

Each insight lists levers in two tiers:

**Direct:** Appears in the formula (boothCost, ACV, targetRevenue)
**Upstream:** Compounds through the funnel (rates, attendees)

Each lever includes:
- Direction (increase/decrease)
- Mathematical rationale
- Concrete projection where possible

### Attendee Lever Suppression

The attendees lever is only actionable for events the planner hosts or controls:

**Show attendees as a lever for:** customer_event, workshop, executive_dinner — the planner sets the invite list and controls turnout.

**Suppress attendees as a lever for:** booth_presence, conference_presentation, webinar, sales_presentation — total attendance is set by the event organizer, not the planner. Suggesting "increase attendees from 12,000 to 20,000" at a third-party trade show is not actionable advice.

When attendees is suppressed, the lever projections function should skip it entirely — don't show it with a caveat, just omit it. The planner's controllable levers at third-party events are: booth visitor rate (booth design, location, engagement tactics), conversion rates (lead qualification, follow-up process), ACV (deal targeting), and cost (negotiation, scope).

In actuals mode, levers are omitted entirely — you can't change inputs after the fact.

The calc engine's `lever_projections()` function computes all projections. Pass the template key so it can suppress attendees for non-hosted templates.

---

## Source-Aware Copy Patterns

All copy patterns throughout the insights engine should adapt based on whether the benchmark reference is industry data or the planner's own calibrated data:

### When using industry benchmarks (pre-calibration, < 5 events in category)

- Rate references: "[Rate] at X% (industry [low]–[high]%)"
- ROI context: "below the 3× industry median (5× is best-in-class)"
- Funnel vs industry: "Industry rule of thumb says..."
- Root cause target label: "target X%"
- Range label in funnel visualization: "Typical range"

### When using planner's calibrated data (5+ events in category)

- Rate references: "[Rate] at X% (your typical [low]–[high]%)"
- ROI context: "below your [X.X]× average across [N] events"
- Funnel vs expected: "Your historical data for [category] events suggests a $[cost] budget typically generates around $[expected]"
- Root cause target label: "your average X%"
- Range label in funnel visualization: "Your range"

### When both are available (show both, planner's data primary)

- Rate references: "[Rate] at X% (your typical [low]–[high]%, industry [low]–[high]%)"
- The funnel visualization shows both: dashed bracket for planner's range, triangle markers for industry edges
- Insights lead with the planner's data but note where industry differs significantly

The planner's own data is always more relevant than industry averages because it reflects their company's actual funnel performance, sales cycle, deal size, and market position. Industry benchmarks remain useful as a second reference point — especially for event types the planner has limited history with.
