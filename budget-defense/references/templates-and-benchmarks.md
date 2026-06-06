# Templates & Benchmarks Reference

## Industry Benchmark Ranges (Defaults)

These are the baseline ranges. Templates can override any range for their event type.

| Metric | Low | High | Direction | Notes |
|---|---|---|---|---|
| Booth Visit Rate | 5% | 20% | Within-range | Too high = implausible, too low = empty booth |
| Leads Rate | 35% | 60% | Higher is better | |
| MQL Rate | 25% | 40% | Higher is better | |
| SQL Rate | 40% | 70% | Higher is better | |
| Win Rate (blended) | 10% | 25% | Higher is better | Templates override: sourced 2–10%, influenced 15–30% |
| CPL | $180 | $700 | Lower is better | B2B event-sourced leads |
| Cost Per SQL | $540 | $5,000 | Lower is better | Dynamically derived: 3×–7× CPL when no override |
| Coverage | 100% | ∞ | Higher is better | Aim for 100%+ |
| ROI | 3× | 5× | Higher is better | 3× industry median, 5× best-in-class |

## Benchmark Flag Evaluation

Flags evaluate to three colors:
- **Green** — metric is within the healthy range
- **Yellow** — metric is within a 10% buffer zone near the edge (warning)
- **Red** — metric is outside the range in the harmful direction

NaN/null values always flag red.

### Within-Range Metrics (booth visitor rate)

Both extremes are concerning. Below low = empty booth. Above high = implausible traffic or data quality issue. Green only when between low and high.

### CPL Suppression

CPL (and Cost Per SQL) insights are suppressed when the event is heavily influenced (sourced < 30%). High CPL is expected for executive dinners and pipeline-acceleration events — flagging it red would be a false alarm. The flag shows "suppressed" with an explanation instead.

## Event Type Templates

### 1. Booth Presence
- **Use for:** Trade show booth walk-ups, expos, exhibit halls
- **Attribution:** 75% sourced / 25% influenced
- **Credit weight:** 30%
- **Win rate override:** 2–10% (sourced first-touch range — much lower than blended)
- **CPL suppressed:** No
- **Hosted:** No (planner doesn't control total attendance)
- **Funnel labels:** Attendees → Booth Visitors → Net New Leads → MQLs → SQLs → Closed-Won Deals → Forecasted Revenue
- **Rate explainers (use when onboarding the planner):**
  - Booth visitor rate: "% of total conference attendees who stopped at your booth — driven by booth location, signage, and floor traffic"
  - Leads rate: "% of booth visitors who became a net new contact in your CRM — depends on badge scanning discipline and qualification bar"
  - MQL rate: "% of new leads that marketing qualifies as worth pursuing — based on ICP fit and engagement signals"
  - SQL rate: "% of MQLs that sales accepts as genuine opportunities — depends on sales follow-up speed and capacity"
  - Win rate: "% of SQLs that close — for sourced first-touch leads from trade shows, expect 2–10% (lower than blended pipeline)"

### 2. Sales Presentation
- **Use for:** 1:1 or small-group demos, product showcases
- **Attribution:** 25% sourced / 75% influenced
- **Credit weight:** 30%
- **Win rate override:** 15–30% (influenced range — higher because leads are warmer)
- **CPL suppressed:** Yes (sourced < 30%)
- **Hosted:** Yes
- **Funnel labels:** Invitees → Attendees → Prospects → Qualified Prospects → Sales-Ready → Closed-Won Deals → Forecasted Revenue
- **Rate explainers:**
  - Attendee rate: "% of invitees who actually showed up — depends on invite quality and scheduling"
  - Leads rate: "% of attendees who became a qualified prospect — most demos produce warm leads, expect high conversion"
  - MQL rate: "% of prospects that marketing deems qualified — typically high for demos since attendees self-selected"
  - SQL rate: "% that sales accepts — pre-qualified audience means high acceptance"
  - Win rate: "% of sales-ready prospects that close — influenced deals close at 15–30% (warmer than cold leads)"

### 3. Webinar
- **Use for:** Online presentations, virtual events
- **Attribution:** 55% sourced / 45% influenced
- **Credit weight:** 30%
- **Benchmark overrides:** None (uses all defaults)
- **CPL suppressed:** No
- **Hosted:** Yes
- **Funnel labels:** Registrants → Live Attendees → Engaged Leads → MQLs → SQLs → Closed-Won Deals → Forecasted Revenue
- **Rate explainers:**
  - Live attendee rate: "% of registrants who actually joined the live session — industry average is 40–50% for webinars"
  - Leads rate: "% of attendees who engaged enough to qualify as a lead — stayed 15+ minutes, asked questions, downloaded content"
  - MQL rate: "% of engaged leads that fit your ICP — webinars attract a mixed audience, so qualification filters matter"
  - SQL rate: "% of MQLs that sales accepts — depends on how targeted the webinar topic was"
  - Win rate: "% of SQLs that close — blended range since webinars produce both new and nurtured leads"

### 4. Conference Presentation
- **Use for:** Keynotes, breakout sessions, panel participation
- **Attribution:** 75% sourced / 25% influenced
- **Credit weight:** 30%
- **Win rate override:** 2–10% (same as booth presence — sourced first-touch)
- **CPL suppressed:** No
- **Hosted:** No
- **Funnel labels:** Session Attendees → Engaged Attendees → Net New Leads → MQLs → SQLs → Closed-Won Deals → Forecasted Revenue
- **Rate explainers:**
  - Engaged attendee rate: "% of session attendees who engaged with your team afterward — visited the booth, scanned a QR code, approached the speaker"
  - Leads rate: "% of engaged attendees who became net new leads — depends on how strong the CTA was in the presentation"
  - MQL rate: "% of leads that marketing qualifies — conference leads are often early-stage, so expect standard conversion"
  - SQL rate: "% of MQLs that sales accepts — similar to booth presence since these are sourced first-touch"
  - Win rate: "% of SQLs that close — sourced first-touch range (2–10%)"

### 5. Executive Dinner
- **Use for:** Curated high-touch events, intimate roundtables
- **Attribution:** 30% sourced / 70% influenced
- **Credit weight:** 30%
- **CPL override:** $1,000–$6,000 (ceiling lifted — boutique dinners naturally run high CPL without it signaling inefficiency)
- **CPL suppressed:** No (range is lifted instead of suppressed)
- **Hosted:** Yes
- **Funnel labels:** Invited Executives → Confirmed Attendees → Engaged Contacts → Qualified Opportunities → Sales-Ready Opportunities → Closed-Won Deals → Forecasted Revenue
- **Rate explainers:**
  - Confirmed attendee rate: "% of invited executives who RSVP'd yes and attended — high-touch invites typically see 60–80% confirmation"
  - Leads rate: "% of attendees who became an active opportunity or deepened an existing one — at intimate dinners, nearly every attendee is a lead"
  - MQL rate: "% of contacts that marketing qualifies — these are pre-vetted executives, so expect high qualification"
  - SQL rate: "% that sales accepts as genuine pipeline — high for curated events since attendees were handpicked"
  - Win rate: "% of sales-ready opportunities that close — mostly influenced (not first-touch), so expect 15–30%"

### 6. Workshop
- **Use for:** Interactive hands-on sessions, training events
- **Attribution:** 50% sourced / 50% influenced
- **Credit weight:** 30%
- **Benchmark overrides:** None (uses all defaults)
- **CPL suppressed:** No
- **Hosted:** Yes
- **Funnel labels:** Registrants → Participants → Net New Leads → MQLs → SQLs → Closed-Won Deals → Forecasted Revenue
- **Rate explainers:**
  - Participant rate: "% of registrants who attended and participated — workshops have higher show rates than webinars because of the hands-on commitment"
  - Leads rate: "% of participants who became leads — active participation usually means high conversion"
  - MQL rate: "% of leads that marketing qualifies — workshops attract a self-selected audience with real interest"
  - SQL rate: "% of MQLs that sales accepts — 50/50 sourced/influenced mix means standard conversion"
  - Win rate: "% of SQLs that close — blended range since workshops produce both new and nurtured leads"

### 7. Customer Event
- **Use for:** Existing-customer expansion, upsell, renewal events
- **Attribution:** 0% sourced / 100% influenced (by definition — these are existing customers)
- **Credit weight:** 30%
- **Benchmark overrides:**
  - Engagement rate → 60–90% (RSVP attendance rate for invited customers)
  - Win rate → 20–50% (upsell/expansion win rate — higher than net-new)
- **CPL suppressed:** Yes (0% sourced)
- **Hosted:** Yes
- **Funnel labels:** Invited Customers → RSVP Attendees → Engaged Customers → Expansion Opportunities → Qualified Opportunities → Closed Deals → Expansion Revenue
- **Rate explainers:**
  - RSVP rate: "% of invited customers who attended — existing relationships drive high turnout (60–90%)"
  - Engagement rate: "% of attendees who engaged in expansion conversations — product roadmap sessions, 1:1 meetings, upsell demos"
  - Expansion opportunity rate: "% of engaged customers with a real expansion, upsell, or renewal opportunity"
  - Qualification rate: "% of opportunities that are qualified and in active sales cycle"
  - Win rate: "% of qualified opportunities that close — existing customers close at 20–50% (much higher than net-new)"

## Scenario Tones (Per-Stage Variance Bands)

Three tones adjust conversion rates before calculation. Rather than a flat multiplier on all rates, each stage has its own variance band based on how much it naturally fluctuates event-to-event. Upstream rates (booth visitor rate) vary more than downstream rates (win rate), so the tone system reflects that.

### Pre-Calibration (fixed bands, based on natural variance by stage)

| Rate | Conservative | Realistic | Optimistic | Why |
|---|---|---|---|---|
| Booth visitor rate | 0.65× (−35%) | 1.0× | 1.35× (+35%) | High variance — booth location, floor traffic, competing sessions |
| Leads rate | 0.78× (−22%) | 1.0× | 1.22× (+22%) | Medium-high — staff quality, qualification bar |
| MQL rate | 0.82× (−18%) | 1.0× | 1.18× (+18%) | Medium — follow-up speed, ICP fit |
| SQL rate | 0.88× (−12%) | 1.0× | 1.12× (+12%) | Medium-low — sales capacity, qualification rigor |
| Win rate | 0.90× (−10%) | 1.0× | 1.10× (+10%) | Low — structural (product, pricing, competition) |

This produces a tighter, more defensible range than a flat 0.75×/1.25× on everything. The conservative scenario doesn't catastrophize the win rate (which barely moves event-to-event), and the optimistic scenario doesn't over-inflate it.

### Post-Calibration (planner's own variance, 5+ events in category)

Once the planner has enough event history, the fixed bands are replaced by their own observed variance:
- **Conservative** = each rate at the planner's historical low (or P25 at 10+ events)
- **Optimistic** = each rate at the planner's historical high (or P75 at 10+ events)
- **Realistic** = 1.0× (no adjustment)

This means "conservative" answers "what if every rate hit the low end of what I've historically seen?" and "optimistic" answers "what if every rate hit the high end?" — a genuinely defensible range backed by real data.

The switchover happens automatically via `get_tone_multipliers()` in the calc engine. If calibration data is passed, it uses the planner's variance. If not, it uses the fixed bands above.

Rates are capped at 1.0 and floored at 0 after tone adjustment. The planner can run all three tones and compare side by side to show leadership a range of outcomes.

## Template Selection Logic

When the planner doesn't specify a template, infer from available data:

1. If they name the event type → map directly
2. If Airtable `Event Type` field is populated → use the mapping table in `math-engine.md`
3. If `Event Category` includes customer-focused terms → customer_event
4. If `Event Format` is "Dinner" or "Roundtable" → executive_dinner
5. Default → booth_presence (most common B2B event type)

Always tell the planner which template was selected and offer to change it.
