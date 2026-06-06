---
name: budget-defense
description: "Event ROI intelligence system — calculates, benchmarks, and defends event marketing spend. Use this skill whenever the user mentions ROI, budget defense, event ROI, trade show ROI, funnel forecasting, CPL, cost per lead, cost per SQL, booth cost analysis, marketing attribution, sourced vs influenced revenue, or wants to forecast, analyze, compare, or defend the ROI of conferences, trade shows, webinars, executive dinners, workshops, customer events, or any event type. Also trigger for scenarios (conservative/realistic/optimistic), side-by-side comparisons, funnel health checks, forecasted revenue calculations, budget defense documents, or post-event actuals analysis. Reads event data from Airtable, spreadsheets, or master event documents."
---

# Budget Defense Skill — Event ROI Intelligence

## What This Skill Does

A persistent, learning event ROI system that combines a deterministic math engine with accumulating event data. It starts smart (industry benchmarks + event type presets) and gets smarter with every event the planner adds.

**Core loop:** Read event data → run funnel math → flag benchmarks → generate insights → save state → learn over time.

The skill produces three kinds of output:
1. **Interactive analysis** — funnel walkthrough, benchmark flags, insights with root causes and levers (in-conversation)
2. **Exportable reports** — PDF or plain text with full formatting, ready for finance or executives
3. **Scenario comparisons** — side-by-side deltas between conservative/realistic/optimistic or between two events

## When to Use

- Planner wants to forecast ROI for an upcoming event
- Planner has post-event actuals and wants to analyze results
- Planner needs a budget defense document for finance/leadership
- Planner wants to compare scenarios or events
- Planner asks about benchmarks, CPL, cost per SQL, conversion rates, or funnel health
- Planner wants to set up the system for the first time (first activation flow)
- Data arrives from the master event document and needs processing

## Data Fallback Chain

For any calculation, use the best available data in this order:
1. **Actual data** from the master event document (Airtable, spreadsheet, or uploaded file)
2. **Saved scenarios** matching that specific event's name
3. **Saved scenarios** for that event type/category
4. **Calibrated averages** from the planner's own event history (if 5+ events in this category)
5. **Standard benchmarks** (industry defaults from `references/templates-and-benchmarks.md`)

Specificity cascades down. A scenario saved from "AWS re:Invent 2025" is more useful for planning "AWS re:Invent 2026" than a generic trade show scenario. The planner's own historical data always takes priority over industry benchmarks — their rates reflect their company's actual funnel performance, not an industry average.

When displaying funnel results, show the benchmark reference point (either the planner's saved average or the industry midpoint) on each funnel bar so the planner can see at a glance whether their rate is above or below the reference.

## Overrides

The planner can override specific data points conversationally:
- "Update SQL rate to 45% for this scenario"
- "Swap in actuals: 11,200 attendees, 9% booth visit rate, $78.5K cost"

Accept partial overrides against whatever the current data source is (master doc, saved scenario, or defaults) without requiring the planner to re-enter everything. Overrides persist when the scenario is saved. Unsaved overrides are session-only.

## First Activation Flow

On first use, run this setup:

1. Ask the planner to point to their master event document (Airtable base, spreadsheet, or upload). Check connected tools first via `tool_search` — if Airtable, Google Sheets, or file access is available, offer to pull from it.
2. Create the `/budget-defense/` data directory (see `references/data-storage.md` for structure).
3. If running in Cowork: create a recurring task with a file event trigger watching the master document for modifications. This is the primary data pipeline.
4. Scan the master doc for existing events, populate `events.json`, and run initial calculations.
5. Ask for company-wide settings: default sales cycle length (e.g., 4 months), notification preferences (email/Slack/Teams), and any global overrides. Save to `settings.json`.

If the master document isn't in a watchable format, fall back to checking the document on each manual activation.

## Reading Event Data from Airtable / Spreadsheets

The master event document maps to the calculation engine like this:

| Master Doc Field | Calculation Engine Input |
|---|---|
| Expected Number of Attendees | attendees |
| Estimated Budget / Actual Budget | boothCost |
| Event Type + Event Format | → selects template (see templates reference) |
| Event Category | → informs attribution defaults |

Fields the master doc likely does NOT contain (planner provides or defaults apply):
- Booth visitor rate, leads rate, MQL rate, SQL rate, win rate → use template defaults or planner input
- ACV (average contract value) → planner provides
- Target revenue → planner provides
- Sourced % and credit weight → template defaults, planner can override

When reading from the Airtable base, map the `Event Type` field to the closest template:
- "Trade show" or "Expo" → Booth Presence
- "Conference" or "Summit" → Conference Presentation
- "Workshop" → Workshop
- "Webinar" → Webinar
- "Dinner" or "Roundtable" → Executive Dinner
- "Partner Event" with sales focus → Sales Presentation
- Events with "customer" in category → Customer Event

## Core Workflow

### Step 1: Identify the Event and Mode

Determine:
- **Which event?** — by name, or new scenario
- **Forecast or actuals?** — is the event upcoming (forecast, prescriptive voice) or past (actuals, explanatory voice)?
- **Which template?** — use `match_template(event_type, event_format, event_category)` from the calc engine. Category overrides type: a "Conference" with "Customer engagement" category maps to customer_event, not conference_presentation. Tell the planner which template was selected and offer to change it.
- **Parent or standalone?** — if the event has multiple activations (booth + dinner + session at the same conference), ask whether to analyze them separately or as children of a parent event. Use `roll_up_child_events()` for the parent summary.

### Step 2: Gather Inputs

Collect funnel inputs. For each, check the fallback chain — use the best available data and tell the planner what source you're using.

**First-event guidance:** When the planner has no saved data for this event or event type, proactively fill industry midpoints and explain what each rate means:

"Since this is your first [template name] analysis, I'll start with industry midpoints:
- [Funnel label for visitors]: [midpoint]% — [one-sentence explanation of what this rate measures]
- [Funnel label for leads]: [midpoint]% — [explanation]
- ... (all rates)

Adjust any rate you have better data for. If you're not sure, these are reasonable starting points."

Use the template's funnel labels (from `funnelLabels`), not generic "booth visitor rate" language. A webinar should say "Live Attendees" not "Booth Visitors."

**Funnel inputs (in order, using template labels):**
- Attendees
- Visitor/engagement rate (%)
- Leads rate (%)
- MQL rate (%)
- SQL rate (%)
- Win rate (%)
- ACV (average contract value, $)

**Cost and target inputs:**
- Event budget ($)
- Target revenue ($)

**Attribution inputs (template provides defaults):**
- Sourced % (what % of revenue is first-touch sourced to this event)
- Credit weight (for influenced revenue, default 30%)

### Step 2b: Diff View (when adjusting inputs)

When the planner changes inputs on an existing analysis ("what if booth visitor rate were 15%?"), always show a before/after comparison using `diff_inputs()`. The planner needs to see the delta, not just the new numbers:

"Changing booth visitor rate from 9% → 15% and MQL rate from 32% → 36%:
- Forecast revenue: $183,306 → $343,699 (+$160,393, +87.5%)
- ROI: 0.05× → 0.96× (↑)
- Coverage: 12.2% → 22.9% (+10.7pp)"

Show only what changed. Don't re-render the entire dashboard unless the planner asks.

### Step 3: Run Calculations

Execute the calculation engine. Read `references/math-engine.md` for the full formula reference and run `scripts/calc_engine.py` for deterministic results.

The engine computes:
- Full funnel: attendees → booth visitors → net new leads → MQLs → SQLs → deals → forecasted revenue
- Derived metrics: ROI, conversion coverage, CPL, cost per SQL, target gap
- Attribution split: sourced revenue, influenced revenue, credited revenue
- Benchmark flags: green/yellow/red for each metric

### Step 4: Generate Insights

Read `references/insights-engine.md` for the six deterministic insight generators. Each fires only when its metric is flagged, and includes:
- Heading (forecast vs. actuals voice)
- Explanation with formula
- Root cause analysis (which upstream rates are dragging the metric down)
- Levers with concrete projections (forecast mode only)

**Priority order:** sanityCheck → funnelVsIndustry → ROI → coverage → CPL → costPerSql

The top-ranked insight keeps its root causes. All others drop theirs to avoid repetition.

### Step 5: Present Results

Present the full analysis conversationally:
1. **Funnel summary** — each stage with counts and rates
2. **Derived metrics** — ROI, coverage, CPL, cost per SQL with benchmark flags
3. **Attribution** — sourced vs. influenced breakdown (if not 100% sourced)
4. **Insights panel** — fired insights in priority order
5. **Offer next steps:** save scenario, export report, compare scenarios, adjust inputs

### Step 6: Save State

When the planner saves a scenario:
- Write to `events.json` with composite key (event name + date)
- Write to `scenarios.json` with all overrides and settings
- Check calibration state — has a category hit its 5th event? See `references/calibration-and-alerts.md`

## Report Modes

### Forecast Report
- Prescriptive voice: "To raise ROI, either grow forecast revenue or shrink cost"
- Full root causes with "What's dragging this down" section
- Full levers with projections: "10% less Event Budget lifts ROI from 2.1× to 2.4×"
- Revenue labeled "Forecast Revenue"

### Actuals Report
- Explanatory voice: "ROI came in below expectations"
- Root causes with "Why" section: "Had it hit X%, the metric would have been Y"
- No levers — you can't change inputs after the fact
- Revenue labeled "Revenue"

## Exports

Read `references/data-storage.md` for export format details.

- **PDF** — Full report with funnel, metrics, flags, and insights. Styled with inline CSS.
- **Plain text** — Copy-friendly for pasting into emails, Slack, or documents.
- **Scenario comparison** — Side-by-side with delta highlighting.

## Calibration and Learning

Read `references/calibration-and-alerts.md` for the full calibration system.

Key concepts:
- Events 1–5 in each category establish baseline averages and natural variance
- After every 5th event, the system recalibrates running averages
- Adaptive alert thresholds scale with event size (small events get wider bands)
- Big jump alerts flag outliers before they skew projections
- Sales cycle guardrail warns when revenue attribution is likely incomplete

## Scenario Engine

The planner can:
- Save scenarios linked to event names with all overrides
- Apply tones: Conservative (0.75×), Realistic (1.0×), Optimistic (1.25×) — multiplied against all rates
- Compare two scenarios side by side with delta highlighting
- Search/filter saved scenarios by event type, region, budget range

### Three-Way Tone Comparison

When the planner asks to compare all three tones, run the calc engine three times with the same inputs but different tones. Present as a three-column layout:

| Metric | Conservative | Realistic | Optimistic |
|---|---|---|---|
| Forecast Revenue | $X | $Y | $Z |
| ROI | X× | Y× | Z× |

Show the delta from conservative to optimistic as a range: "Revenue range: $X – $Z (Δ $N)". This gives the planner a defensible range to present to finance rather than a single point estimate.

### Parent/Child Events

When an event has multiple activations (e.g., a booth + executive dinner + speaking session at the same conference), the planner can analyze each as a child event and see a rolled-up parent summary using `roll_up_child_events()`:

- Each child runs through the full analysis pipeline with its own template
- The parent summary shows: combined cost, combined revenue, combined ROI, combined CPL, combined Cost/SQL
- The per-child breakdown shows each activation's contribution

This solves the "we spent $210K total at SaaS World — what was the combined ROI?" question that the single-event model can't answer.

### Event Evolution

Show performance trends across events using `event_evolution()`. Fires from "show me my past events," "how have my trade shows been trending," or the "Past events" action card.

**With 3+ events:** Vertical bar chart with chronological events, industry range band, planner's average line, and trend direction. Filterable by metric (ROI, coverage, CPL, booth visit %, etc.) and by year.

**With 2 events:** Side-by-side comparison using `compare_scenarios()`. "You have 2 [category] events. Here they are compared — I need 3+ to show a trend."

**With 1 event:** Show the single event's metrics with industry context. "You have 1 [category] event so far. After 2 more, I can show trends."

**With 0 events in filter:** "No events match that filter. You have [N] events total — try [suggest broader filter]."

### Scenario Discovery

When the planner opens the skill or starts working on an event, proactively check `scenarios.json` and `events.json` for relevant saved data before starting fresh:

1. **On any event reference:** Look for saved scenarios matching that event name (or previous years of the same event). If found, surface them: "I found 3 saved scenarios for re:Invent (Conservative, Realistic, Optimistic — last updated April 10) and actuals from re:Invent 2025. Want to start from one of those, or build fresh?"

2. **On "show me my scenarios" / "what do I have saved":** List all saved scenarios from `scenarios.json` — show name, linked event, tone, template, and last-updated date. Group by event name. If there are many, offer to filter by event type, date range, or search term.

3. **On "list my events" / "what events do I have data for":** List all events from `events.json` — show name, date, type, report mode (forecast/actuals), and key metrics (ROI, coverage). Sort by date descending.

4. **On first activation with existing data:** After scanning the master doc, tell the planner exactly what was found: "I found 12 events in your master document. 8 are past events (actuals available), 4 are upcoming (forecast mode). I've populated the event history. Want to see a summary?"

The planner should never have to guess what's saved or wonder what a scenario is called. The skill always shows what's available before asking for new input.

## Reference Files

Load these as needed — don't read all at once:

| File | When to Read |
|---|---|
| `references/math-engine.md` | Before running any calculations |
| `references/templates-and-benchmarks.md` | When selecting a template or checking benchmark ranges |
| `references/insights-engine.md` | When generating the insights panel |
| `references/calibration-and-alerts.md` | When processing new event data or checking calibration state |
| `references/data-storage.md` | During first activation, when saving/loading data, or exporting |

## Script

| Script | What It Does |
|---|---|
| `scripts/calc_engine.py` | Pure-function calculation pipeline — pass inputs, get outputs. Deterministic. |

Run the script for all calculations to ensure consistency. Don't calculate by hand.

## Output Format Guidance

The skill produces three kinds of output depending on the request:

### Visual Dashboard (default for full analysis)

Use inline visual widgets for full event analysis. Split across two widgets to avoid rendering timeouts:

**Widget 1 — Financial summary (top half):**
1. Event name + metadata line (template, mode, tone, calibration status)
2. ROI hero — large centered number with colored bar (green ≥3×, yellow 1–3×, red <1×) and context line
3. Two-column budget/revenue cards:
   - Left: revenue target, industry-standard budget, your event budget (stacked)
   - Right: forecast revenue with attribution badge, coverage, vs-target gap
4. Natural language summary — one sentence connecting budget, forecast, target, and bottleneck
5. Secondary metrics row — CPL, cost per SQL, credited revenue, deals (4-column grid)

**Widget 2 — Funnel + actions (bottom half):**
1. Funnel bars — full-width tracks, colored fill proportional to rate, percentage anchored at right edge
2. Dual range markers on each bar:
   - Dashed bracket with tick marks = planner's range (when calibrated, 5+ events)
   - Small triangles below = industry range (always visible)
   - Legend explaining both
   - Pre-calibration: only industry triangles show, legend says "Typical range"
3. Forecast revenue row at bottom of funnel
4. "What would you like to do next?" card grid (6 cards: view insights, adjust inputs, compare tones, past events, compare events, export report)

**Insights panel (separate, on request):**
- Insight cards in priority order (sanityCheck → funnelVsIndustry → ROI → coverage → CPL → costPerSql)
- Each card: rank tag (culprit/effect), heading, explanation, context box, root causes (top card only), levers with projections
- Green metrics get a one-line confirmation at bottom
- "What next?" card grid at bottom

**Evolution chart (on request, requires 3+ events in category):**
- Vertical bar chart showing metric trend across events in a category
- Industry range as horizontal band, planner's average as reference line
- Filterable by event type, date range, metric
- Fires from: "show me my past events", "how have my trade shows been trending", "past events" action card

### Conversational Text (for quick lookups)

Use plain text for single-metric checks, quick comparisons, or when the planner asks a specific question. Default to the fuller format and let the planner ask for less, not the other way around.

**Quick check examples (text only):**
- "What's my CPL for this event?" → "CPL is $338 (green, industry range $180–$700)."
- "Is my ROI healthy?" → "ROI is 1.5× — positive return but below the 3× industry median. The main drag is low booth visitor rate (9%, lower end of 5–20%). Reducing budget by 10% or lifting visitor rate to 12.5% would each push ROI closer to 2×."
- "What template should I use for a webinar?" → "Webinar template — 55% sourced, standard benchmarks, funnel labels: Registrants → Live Attendees → Engaged Leads → MQLs → SQLs."

**Full analysis examples (visual dashboard):**
- "Run an ROI forecast for SaaS World" → full dashboard (two widgets)
- "How's my event looking?" → full dashboard (ambiguous = default to full)
- "Analyze this event" → full dashboard
- "Compare conservative and optimistic" → three-way comparison table
- "Show me my past trade shows" → evolution chart
- "What changed if I bump visitor rate to 15%?" → diff view (text, not full dashboard)

### Exports (PDF and plain text)

See `references/data-storage.md` for export format specifications. When the planner clicks "Export report," tell them what they'll get before generating: "You'll get a styled PDF with the full funnel, all metrics with benchmark flags, the attribution breakdown, and every fired insight with root causes and levers — ready to send to finance."

Exports include the full analysis: funnel, metrics, flags, attribution, and all fired insights with complete formatting.

## Runtime Environment

The skill works in two environments with different automation capabilities:

### In Cowork (full automation)
- File event trigger watches the master event document for changes
- Recurring task processes new data automatically (passive updates, active alerts)
- Notifications via email/Slack/Teams for big jumps, recalibrations, sales cycle warnings
- Context persistence across runs — the recurring task remembers previous outputs
- Data directory `/budget-defense/` lives in the project folder

### In Claude.ai (manual activation)
- Same calculation logic, same insights, same output formats
- No file watching — the planner triggers analysis by opening the skill or uploading data
- No background notifications — alerts surface when the planner asks for analysis
- Data persists via the JSON files if the planner saves them, but there's no automatic pipeline
- The skill should be explicit: "I've saved this to events.json. Next time you open me, I'll pick up where we left off."

The core analysis is identical in both environments. The difference is whether data flows in automatically (Cowork) or the planner brings it manually (Claude.ai).
