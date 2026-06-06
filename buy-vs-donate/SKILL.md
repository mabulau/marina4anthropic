---
name: buy-vs-donate
description: "Buy-vs-rent calculator for trade show, conference, and event equipment with IRS MACRS depreciation and charitable donation tax savings. Use this skill whenever the user asks whether it's cheaper to buy and donate equipment or rent it, compares buying vs renting equipment for trade shows, conferences, galas, summits, workshops, or any event type, asks about tax savings from donating used equipment, mentions MACRS depreciation on event assets, asks about the buy-use-donate strategy for event materials, wants to calculate charitable deduction value for donated equipment, or asks about buying equipment and donating it to a nonprofit. Also trigger when the user asks about IRS §170 deductions for donated property, adjusted basis vs FMV for charitable contributions, or wants to model the net cost of purchasing equipment that will later be donated to a nonprofit. This skill contains the authoritative MACRS tables, FMV condition multipliers, and IRS threshold rules — do not guess or approximate these values."
---

# Buy vs. Donate Calculator Skill

## What This Skill Does

Compares the total cost of **renting** trade show / event equipment against the net cost of **buying it, using it, then donating it** to a 501(c)(3) nonprofit — factoring in IRS MACRS depreciation, FMV estimates, charitable deduction rules, and tax savings.

The calculator doesn't just answer "which is cheaper?" — it proactively models optimization scenarios so the user can see how changing their plan affects the outcome.

## When to Use

- User asks "should I buy or rent [equipment] for my trade show?"
- User wants to know the tax benefit of donating used equipment
- User mentions buy-use-donate, buy vs rent, or MACRS depreciation for event assets
- User wants to calculate charitable deduction value for donated property
- User provides a purchase price and rental price and wants a comparison

## Behavior When Inputs Are Missing

**Do NOT interrogate the user for every field.** Instead:

1. Use whatever the user provided plus reasonable defaults for everything else
2. Build the interactive calculator immediately (they can adjust via sliders)
3. **Always include the Optimization Scenarios section** (see below) — this is where the real value is

The goal is: user says "I'm looking at $3,000 AV gear, rental is $1,500/show, we have 3 shows" → they immediately get a working calculator AND scenario analysis showing event scaling, and condition impact.

## When Renting Wins

**If the user's scenario clearly favors renting, say so directly.** Don't twist the output into a buy-donate pitch. The calculator should be honest:
- Show the comparison as-is (renting cheaper by $X)
- The event scaling table naturally shows where the tipping point is (if one exists)
- If even at 6+ events renting is cheaper, say: "At these rates, renting is the better financial option."
- Don't force the buy-donate conclusion — the user's trust in the tool depends on it being honest when the answer isn't what they hoped for

## Required Inputs

Use defaults in parentheses if not provided:

| Input | Description | Default |
|---|---|---|
| **Equipment category** | Electronics, Furniture, Sports, Clothing, Fabric/Linens, Flowers | Furniture |
| **Purchase price** | What the equipment costs to buy | (required) |
| **Rental cost per event** | Average cost to rent per show/event (actual costs vary) | (required) |
| **Number of events** | How many shows/events before donation | 3 |
| **Months held before donation** | Time between purchase and donation | 12 |
| **Condition at donation** | excellent, good, fair, poor | good |
| **Entity type** | C-Corp or Pass-through/Individual | C-Corp |

**Tax rate handling:**
- **C-Corp** → use 21% (fixed federal rate, IRC §11)
- **Pass-through / Individual** → default to 24%, let them adjust via slider
- Always show a help note: "Confirm your applicable rate with your accounting team before relying on these estimates."

## Output

Produce a **React (.jsx) artifact** with an interactive calculator that supports both single-item and multi-item (cart) mode. The artifact must include:

### Cart Functionality
The calculator supports adding multiple items to an "event cart" for aggregate comparison:
- **Item editor** (left sidebar): category, optional label, purchase price, avg rental, condition → "Add to Event" button
- **Cart list**: shows all added items with category icon, label, per-item cost/rental/deduction, and a remove button
- **Shared settings**: number of events, months before donation, and tax entity apply to all items (you're donating everything at the same time from the same entity)
- **Per-item MACRS**: each item gets its own depreciation calculation based on its category (5-year electronics vs 7-year furniture)
- **Aggregate results**: total purchase, total rental, total deduction, total tax savings, net savings across all items
- **Per-item breakdown table**: shows each item's cost, adjusted basis, FMV, deduction, and tax saved
- **IRS threshold flags apply to the aggregate deduction total** — a $400 chair and $300 monitor individually don't trigger Form 8283, but together at $700 combined they do

When the cart is empty, show a placeholder prompting the user to add items. When items are added, show the full results.

If the user provides just one item, the calculator works the same way — they add it, see results. The cart just enables the multi-item workflow naturally.

### Section 1: Core Comparison
1. Side-by-side: **Rent Every Event** vs **Buy → Use → Donate**
2. MACRS depreciation breakdown (original cost → adjusted basis → FMV → deduction)
3. Net savings (or loss) hero card
4. IRS compliance threshold flags ($250/$500/$5,000/$10,000) — applied to the **aggregate** deduction across all cart items
5. Entity type toggle with help note about confirming with accounting

### Section 2: Optimization Scenarios (ALWAYS INCLUDE)

This is what makes the skill useful beyond a simple calculator. Show these scenarios below the core comparison:

#### a) Incremental Value Narrative
Don't show an abstract "breakeven" number. Instead, tell the story in terms the user relates to — what happens at each event count:

- If buy-donate wins at their current plan: "At [N-1] events, you'd save [X]. Adding just one more event bumps your savings to [Y]."
- If renting is still cheaper: "At [N] events, renting is cheaper by [X]. Adding [M] more events would tip the balance — at [N+M] events, you'd save [Y]."
- Always close with: "Your buy-donate cost stays fixed at [net cost] — rental costs add up with each event. These projections use your average rate of [rental]/event."

**Critical: never claim "every additional event saves exactly [rental]."** Rental costs vary by venue, city, show duration, labor rules, and equipment availability. The user entered a single average rate. The buy-donate side IS fixed — but the rent side is an estimate per event that will vary in practice. Always qualify projections with "at this average rate" or "based on your estimated rental rate."

#### b) Event Scaling Table
Show a small table with 1 through max(userEvents + 3, 6) events:

| Events | Rent Total | Buy-Donate Net | Savings |
|--------|-----------|----------------|---------|
| 1      | $1,500    | $2,698         | −$1,198 |
| 2      | $3,000    | $2,698         | $302    |
| 3      | $4,500    | $2,698         | $1,802  |
| ...    | ...       | ...            | ...     |

The buy-donate column stays constant. The rent column grows. This makes the scaling argument visual and intuitive.

#### c) Condition Impact
Frame as actionable advice, not just data:
- If current condition is below excellent: "Keeping your materials in excellent shape could add **$X** to your savings."
- If excellent: "You're at the highest deduction. Letting condition slip to fair would cost you **$X**."
- Show all four condition levels with the delta from the user's current choice, but lead with the actionable upside/downside.

#### d) Timing Insight (honest, not always positive)
For **depreciable property** (Electronics, Furniture, Sports): more months = more MACRS depreciation = lower adjusted basis = lower deduction cap. Surface this honestly:
- "Holding 12 more months adds X% MACRS depreciation, which *lowers* your adjusted basis to $Y and caps your deduction at $Y instead of $Z."
- This is counterintuitive — most people assume holding longer is always better. For §1245 property it's not.

For **non-depreciable property** (Clothing, Fabric/Linens, Flowers): more months = lower FMV (age decline), which directly reduces the deduction. Also not always positive.

**Never fabricate a "hold longer = save more" claim.** Run the actual math both ways and report what happens.

### Section 3: IRS Forms & Resources
Link to relevant IRS resources:
- [Form 8283](https://www.irs.gov/forms-pubs/about-form-8283) — Noncash Charitable Contributions (required for deductions >$500)
- [Publication 946](https://www.irs.gov/publications/p946) — How to Depreciate Property (MACRS tables)
- [Publication 561](https://www.irs.gov/publications/p561) — Determining the Value of Donated Property
- [Publication 526](https://www.irs.gov/publications/p526) — Charitable Contributions

**No branding.** The calculator should be clean and neutral — no product names, company names, or logos.

## Math Engine

### IRS Constants (2026)

```
Corporate tax rate (C-Corp):   21% federal (IRC §11 — fixed)
Individual rates:              10–37% marginal (brackets vary)
Corporate charitable limit:    10% of taxable income (C-corps)
Individual charitable limit:   60% of AGI (cash), 30% of AGI (property)

Thresholds:
  $250+    → Written acknowledgment required
  $500+    → Form 8283 Section A required
  $5,000+  → Qualified appraisal + Form 8283 Section B required
  $10,000+ → $500 filing fee + Form 8283-V required
```

### MACRS Depreciation Tables

IRS Publication 946, Table A-1 — 200% Declining Balance, Half-Year Convention.

```
3-year: [0.3333, 0.4445, 0.1481, 0.0741]
5-year: [0.2000, 0.3200, 0.1920, 0.1152, 0.1152, 0.0576]
7-year: [0.1429, 0.2449, 0.1749, 0.1249, 0.0893, 0.0892, 0.0893, 0.0446]
```

### Category → MACRS Recovery Period

```
Electronics:    5-year  (computers, AV, phones, displays)
Furniture:      7-year  (desks, chairs, tables, fixtures)
Sports:         7-year  (equipment, default class)
Clothing:       null    (non-depreciable — use FMV only)
Fabric/Linens:  null    (non-depreciable — use FMV only)
Flowers:        null    (perishable — use FMV at donation)
```

### FMV Condition Multipliers

Platform estimates — not from IRS Pub 561. Verify against actual resale prices.

```
excellent: 0.80
good:      0.60
fair:      0.40
poor:      0.20
```

### Calculation Steps

#### Step 1: MACRS Depreciation (for depreciable categories only)

```javascript
function calculateMACRS(cost, life, months) {
  const rates = MACRS_RATES[life];
  const yearsCompleted = Math.floor(months / 12);
  let accumulated = 0;
  for (let yr = 0; yr < Math.min(yearsCompleted, rates.length); yr++) {
    accumulated += rates[yr] * cost;
  }
  accumulated = Math.min(accumulated, cost);
  const adjustedBasis = Math.max(cost - accumulated, 0);
  return { adjustedBasis, accumulated };
}
```

Rates already incorporate the half-year convention. Only apply complete recovery years — no partial-year interpolation.

#### Step 2: FMV Estimate

Annual decline rates are platform estimates — not IRS figures. They approximate real secondary-market behavior (Electronics lose value fastest, Furniture slowest) but are not sourced from Pub 561 or any IRS publication. Verify against actual resale prices.

```javascript
const conditionMultiplier = FMV_CONDITION[condition];
// Platform estimates — not IRS figures:
const annualDecline = category === 'Electronics' ? 0.30  // ~30%/yr (AV, displays depreciate quickly in resale)
  : category === 'Sports' ? 0.15                         // ~15%/yr
  : category === 'Furniture' ? 0.10                       // ~10%/yr
  : 0.08;                                                 // ~8%/yr default
const ageFactor = Math.max(0.10, 1 - (months / 12) * annualDecline);
const fmv = cost * conditionMultiplier * ageFactor;
```

#### Step 3: Deduction Value

For **depreciable property** (Electronics, Furniture, Sports — all §1245 ordinary income property):

```
deduction = min(FMV, adjustedBasis)
```

This applies regardless of holding period, but for different reasons:
- **Short-term (≤12 months):** IRC §170(e)(1)(A) — deduction reduced by the amount that would be short-term capital gain.
- **Long-term (>12 months):** IRC §170(e)(1)(B)(i) — deduction reduced by ordinary income that would be recognized on sale. For §1245 property, MACRS depreciation recapture under §1245(a) converts gain up to accumulated depreciation into ordinary income, which limits the deduction to adjusted basis even for long-term holds.

The result is the same either way: `min(FMV, adjustedBasis)`. The calculator gets the right answer — this note is for anyone who asks *why*.

For **non-depreciable property** (Clothing, Fabric/Linens, Flowers):

```
deduction = FMV
```

#### Step 4: Tax Savings

```
taxSavings = deduction × (taxRate / 100)
```

#### Step 5: Core Comparison

```
Rent total     = rentalCostPerShow × numberOfShows
Buy-donate net = purchasePrice - taxSavings
Net savings    = rentTotal - buyDonateNet
```

#### Step 6: Incremental Event Analysis

For each event count from 1 to max(userEvents + 3, 6):
```
rent_at_N    = rentalCostPerEvent × N
savings_at_N = rent_at_N - buyDonateNet
```

buyDonateNet is constant. Rent is projected using the user's average rate — always note that actual rental costs vary by event. The insight is that the buy-donate side is locked in while rental costs accumulate, but don't overstate the precision of the rental projection.

#### Step 7: Condition Sensitivity

Run the full calc at each condition level (excellent, good, fair, poor) and show the delta vs. the user's chosen condition.

#### Step 8: Timing Sensitivity

Run the full calc at the user's months AND at user's months + 12. Compare deduction values. For §1245 property, if the deduction drops (because basis drops faster than FMV), say so clearly.

### IRS Threshold Flags

After calculating deduction value, flag:
- **$250+**: "Written acknowledgment from nonprofit required"
- **$500+**: "IRS Form 8283 Section A must be filed"
- **$5,000+**: "Qualified appraisal by qualified appraiser required + Form 8283 Section B"
- **$10,000+**: "$500 filing fee required with Form 8283-V"

### Legal Disclaimer

Every output MUST include this disclaimer (no product or company names):

> This calculator provides estimates based on IRS MACRS tables (Publication 946) and is not tax advice. It is not provided by a tax advisor, CPA firm, law firm, or qualified appraiser. Users are solely responsible for determining the accuracy of information they provide and the value of deductions claimed on their tax returns. All depreciation calculations and FMV estimates are approximations only. Consult a qualified tax professional before making decisions based on these figures.

## Design Notes

- Clean, neutral design — no branding, logos, or product names
- Color palette: primary green `#2D5A27`, background `#F7F6F3`, card white `#FFF`, border `#DDD8CD`, muted text `#7A756A`
- Font stack: DM Sans for body, JetBrains Mono for numbers
- Cards with subtle borders, no heavy shadows
- Green for buy-donate column, red/warm for rent column
- Highlight the net savings prominently
- Entity type toggle with "?" help note about confirming with accounting
- Optimization scenarios section should feel like a natural extension, not a separate tool
- IRS resources section at the bottom with clickable links
- For §1245 depreciable property, always show the "lesser of FMV or adjusted basis" rule regardless of holding period

## Critical Accuracy Rules

1. **Never fabricate MACRS rates.** Use only the tables above.
2. **Never skip the §1245 basis cap for depreciable property.** The deduction for Electronics, Furniture, and Sports is ALWAYS min(FMV, adjustedBasis) regardless of holding period.
3. **Never claim this is tax advice.** Always include the disclaimer.
4. **Never omit IRS threshold flags.** They are compliance-critical. Include all four: $250, $500, $5,000, and $10,000.
5. **FMV multipliers AND annual decline rates are platform estimates, not IRS figures.** Always note this.
6. **Never fabricate "hold longer = save more" claims.** Run the math both ways and report honestly. For §1245 property, holding longer often reduces the deduction.
7. **Always include the optimization scenarios.** They're the primary value of this skill over a basic calculator.
8. **If renting wins, say so.** Don't force the buy-donate conclusion. The tool's credibility depends on honesty.
