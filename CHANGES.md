# Repo Fixes — Change Log

Three corrected Python files are ready to drop into `budget-defense/scripts/`:
**templates.py, evolution.py, calibration.py** (calc_engine.py and helpers.py need no changes).
The markdown edits below can be applied in GitHub’s web editor.

-----

## 1. BUG FIX (highest priority) — calibration key mismatch

**Problem:** `compute_calibration_stats()` writes variance ranges as `low`/`high`,
but `data-storage.md` documents the calibration.json schema as `min`/`max` (and the
`get_tone_multipliers` docstring agreed with the docs). Any calibration.json written
in the documented format made calibrated tone bands silently no-op (multiplier 1.0) —
the “learns from your own data” feature did nothing.

**Code fix (in patched templates.py):** `get_tone_multipliers` now reads `low`/`high`
as canonical and accepts `min`/`max` as legacy aliases, and its docstring shows the
correct shape. Verified: both formats now produce real calibrated multipliers.

**Doc fix — in `references/data-storage.md`, calibration.json example:**

FIND:
“boothVisitorRate”: { “min”: 0.08, “max”: 0.22 },
“leadsRate”: { “min”: 0.35, “max”: 0.52 },
“roi”: { “min”: 2.1, “max”: 7.8 }
REPLACE WITH:
“boothVisitorRate”: { “low”: 0.08, “high”: 0.22 },
“leadsRate”: { “low”: 0.35, “high”: 0.52 },
“roi”: { “low”: 2.1, “high”: 7.8 }

Also in the Calibration Fields table:
FIND:    Min/max observed per metric (established at event 5)
REPLACE: Low/high observed per metric (established at event 5)

-----

## 2. budget-defense/SKILL.md — Scenario Engine contradicts the tone system

The SKILL.md describes the legacy flat multipliers, contradicting math-engine.md,
templates-and-benchmarks.md, and the code (per-stage variance bands). This undersells
your differentiator in the one file every reviewer reads.

FIND:

- Apply tones: Conservative (0.75×), Realistic (1.0×), Optimistic (1.25×) — multiplied against all rates

REPLACE WITH:

- Apply tones (conservative / realistic / optimistic) using per-stage variance bands — upstream rates swing more than downstream rates (booth visitor ±35%, win rate ±10%). Once a category is calibrated (5+ events), the planner’s own historical variance replaces the fixed bands. See `references/templates-and-benchmarks.md`.

-----

## 3. data-storage.md — example output disagrees with the engine

The engine flags coverage 0.8925 **red** (yellow buffer cuts off at 0.90 for
higher-is-better metrics). The example claims yellow.

In the events.json example, FIND:
“coverage”: “yellow”
REPLACE: “coverage”: “red”

In the plain-text export example, FIND:
Coverage:  89.3% ⚠️
REPLACE:
Coverage:  89.3% ❌

(Alternative: change the example’s targetRevenue so coverage lands in the yellow
band — but the one-word fix is simpler.)

-----

## 4. evolution.py (in patched file)

- Removed the duplicate local `_calc_delta` that shadowed the helpers import.
- `event_evolution()`’s `category` parameter now filters on `identity.category`
  (the human-readable field, case-insensitive, with eventType fallback) instead of
  duplicating the `template_key` filter. Filtering by “Trade show” now works.

## 5. calibration.py (in patched file)

- Removed the orphaned “Evolution Chart Data” section header at end of file.

-----

## 6. buy-vs-donate/SKILL.md — surface the deduction caps you already cite

The IRS constants list the 10%-of-taxable-income (C-corp) and 30%-of-AGI (property)
limits, but Step 4 (`taxSavings = deduction × rate`) never applies or flags them, so
large donations can overstate savings. Add after Step 4:

ADD:
**Deduction limit flag:** The calculator cannot know the user’s taxable income or AGI,
so it does not cap the deduction — but when the aggregate deduction is large, append:
“Note: charitable deductions are limited to 10% of taxable income for C-corps (30% of
AGI for property donated by individuals). Amounts above the limit carry forward up to
five years. If this deduction is large relative to your income, the first-year tax
savings shown here may overstate the benefit — confirm with your tax team.”

And add to Critical Accuracy Rules:
9. **Flag the deduction limits on large donations.** First-year savings may be
deferred by the 10%/30% caps; never present capped-out savings as immediate.

-----

## 7. README.md — fix the contradiction and name the system

a) The README says kbyg-generator’s contents are “a single self-contained SKILL.md” —
but the SKILL.md references `references/master-event-schema.md`, `references/sections.md`,
and `references/test-cases.md`. Either commit those files under kbyg-generator/references/
(recommended — the schema is the portfolio’s best artifact) and update the “Inside:” line:

REPLACE the kbyg “Inside:” line WITH:
*Inside:* `SKILL.md` and a `references/` folder (section templates, the master event
schema that connects all three skills, and three tiered test cases).

b) ADD a section (suggested placement: right after “The Skills”):

## How the skills connect

These aren’t three separate tools — they share one data model. The **master event
record** (`kbyg-generator/references/master-event-schema.md`) is the source of truth:

- **kbyg-generator** reads Sections A and D (event details, staff profiles) to build
  the briefing document.
- **budget-defense** consumes and writes back Section C3 (post-event actuals: leads,
  MQLs, SQLs, pipeline, ROI) — every event analyzed feeds its calibration loop.
- **buy-vs-donate** outputs land in Section C3’s local & community impact fields
  (donations made, tax-deductible contributions), so donation strategy shows up in
  the same ROI picture finance sees.

One schema, many outputs: brief the team before the event, defend the budget after
it, and make the buy/rent/donate call in between — all against the same record.

-----

## 8. Optional — kbyg test-case/sample alignment (verify against your latest)

In the versions reviewed: Test Case 1 says booth images were provided and “embedded
with captions,” but sample-output-tier1.md shows [PLANNER: Embed…] placeholders; the
input says 15 staff with full roster provided, but the sample lists 7 plus a
placeholder for “remaining 8.” Either adjust the test-case input (images/roster
partially available) or the sample (show all 15, embed-image notes). Also replace
“(702) XXX-XXXX” with a proper **[PLANNER: Add venue security number]** placeholder.