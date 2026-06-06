# marina4anthropic

# Claude Skills for Event Marketing

Three Agent Skills built for Claude, each focused on a real part of event-marketing work: defending a budget, deciding whether to buy or rent, and getting a team ready before an event. Every Skill is a `SKILL.md` that tells Claude when and how to use it, along with any supporting references and scripts.

*(Built and shared as part of my application to Anthropic.)*

## The Skills

### `budget-defense` — event ROI intelligence

An ROI engine for event marketers with a calibration loop that learns from a user's own conversion rates as their event history grows. It applies thresholds tied to event size and holds off on recalibrating while a sales cycle is still open and the funnel data may still be incomplete. Results are mathematically generated and deterministic, and grow more precise over time. It is also portable enough to run mid-event, so a user may adjust strategy the moment an event is not tracking to goal.

*Inside:* `SKILL.md`, a `references/` folder (math, calibration and alerts, insights, data storage, templates and benchmarks), and a `scripts/` folder (calculation, calibration, and evolution logic).

### `buy-vs-donate` — cost calculator

A calculator that weighs renting event items against buying, using, and donating them to a nonprofit for the tax write-off. It runs the real tax math across categories as different as AV gear, furniture, and flowers, handles a whole cart of items at once, and shows how the numbers move as the user adds events, changes an item's condition, or holds it longer before donating.

*Inside:* a single `SKILL.md`.

### `kbyg-generator` — pre-event staff document

A generator for the "Know Before You Go," an internal pre-event document that shares the information staff need before an event. It builds ten standard sections and scales their depth by event tier. The sections adapt for in-person, virtual, or hybrid events, and the output can be a Word document, Markdown, or a slide deck.

*Inside:* `SKILL.md` plus a `references/` folder (master event schema, section guide, test cases, and a Tier 1 sample output).

## Trying them

These run on Claude's Skills feature.

- **To read:** open any `SKILL.md` to see exactly how the Skill instructs Claude — no download needed.
- **To run:** add a skill folder to Claude through the Skills interface, then ask Claude about something the Skill covers. Each `SKILL.md` opens with the phrases and topics that trigger it.

A note on paths: references such as `/mnt/skills/public/...` and `/mnt/user-data/outputs/` point to Claude's Skills runtime, not to anything on a local machine.
