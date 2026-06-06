---
name: kbyg-generator
description: "Generate 'Know Before You Go' (KBYG) internal staff briefing documents for conferences, trade shows, partner events, sponsored activations, hosted dinners, meetups, workshops, and speaking engagements. Use this skill whenever the user mentions KBYG, 'know before you go', event briefing, staff event guide, conference prep document, event staff guide, or asks to create a document that prepares staff to attend an event. Also trigger when someone says they need to brief their team before a conference, create an internal event guide, or prepare attendees. Produces .docx, .md, or .pptx output with tiered section recommendations (Tier 1 / Tier 2 / Tier 3) that the planner can override."
---

# Know Before You Go (KBYG) Generator

## What This Skill Does

Generates internal staff briefing documents — **Know Before You Go (KBYG)** guides — for conferences and events. A KBYG is NOT an event playbook or operational plan for the planner. It is a **concise, scannable guide that helps every staff member attending the event show up prepared.**

The guiding principle: **keep it as light as possible so people actually read it.**

## When to Use

- User needs to create a KBYG / event briefing / staff guide for an upcoming event
- User wants to brief their team before a conference, trade show, or partner event
- User is preparing internal documentation for event attendees

## Data Sources & Integration

This skill can pull event data from connected sources to pre-populate the KBYG instead of requiring manual input for every field. When a data source is available, use it. When it's not, fall back to asking the user or inserting placeholders.

### Ideal Architecture: Master Event Record

The most efficient workflow is a **single structured event record** (in Airtable, Google Sheets, Notion, or similar) that serves as the consolidated operational record for every event. The KBYG skill reads from this record. Other tools — post-event reports, status updates, ROI analysis, staffing recommendations — also read from it. One record, many outputs.

See `references/master-event-schema.md` for the full schema, including the event intelligence layer (historical participation, competitor analysis, post-event metrics) and staff event profiles.

### Event Folder

All event-related information — logistics, travel, design assets, talking points, staff assignments, images — should live in a single shared folder named after the event. The skill pulls from this folder. Ask the user to point to the folder location (Google Drive, Dropbox, shared network, etc.) and the skill will read what it needs.

If no event folder exists, the skill falls back to manual input or connected tools.

### Connected Tools

Before gathering inputs manually, the skill checks what connectors are available in the current environment using `tool_search`. If any connected tools could contain event data (calendars, file storage, project management, CRM, messaging, etc.), the skill offers to pull from them:

> "I see you have [connected tools] available. Would you like me to check those for event data, or would you prefer to provide the details manually?"

The skill makes no assumptions about which tools are in use or where data lives. It works with whatever is connected — or with no connectors at all (fully manual input).

### Fallback Behavior

For any data that isn't available from a connected source or the event folder:
- Ask the user directly during input gathering
- If the user doesn't have the info yet, insert a specific placeholder: `**[PLANNER: Add hotel block details and booking link]**`
- Never leave a section empty — always include either real data, user-provided input, or a clear placeholder

## Step 1: Gather Inputs

Check connected data sources first (see above). Then ask the user for anything still missing.

**Required inputs (must have these to generate):**
- Event name *
- Event dates *
- Event format * (in-person / virtual / hybrid) — determines which sections are relevant (e.g., A2 booth sections are skipped for virtual events)
- Event type * (trade show / conference / webinar / workshop / executive dinner / customer event / sales presentation / other)
- Event category * (hosted — you organized it, control the guest list | third-party — attending someone else's event)
- Participation level * (booth | sponsorship | speaking | attending only | multiple — specify)
- Event tier * (Tier 1 = major/flagship | Tier 2 = significant investment | Tier 3 = small/regional/low investment)

Event type and category align with the Budget Defense skill's template system. When both skills read from the same master event record, the planner classifies the event once and both skills pick it up. Event type maps to a Budget Defense template (e.g., "executive dinner" → executive_dinner template). Event category determines whether the planner controls attendance (affects ROI lever analysis).

**Optional inputs (prompt for these, accept what's available):**
- Venue / city
- Conference size (estimated total attendance)
- Type of attendees (technical / executive / mixed / academic / industry-specific)
- Area of knowledge or focus
- Company goals and KPIs for this event
- Booth (number, hall, layout overview and location, layout image or rendering)
- Meeting spaces (room IDs, capacity, hours, booking process, AV)
- War room or local office details
- Design assets and booth materials (signage, banners, screens, printed materials, swag — with photos and placement notes)
- Venue or floor map images
- Hotel and travel details
- HR travel policy details (per diem, credit card policy, insurance, expense reporting)
- Event calendar (hosted events, sponsored events, program sessions, partner/industry/C-suite highlighted sessions)
- Product updates or key messaging
- Department updates or highlights
- Staff social amplification guidance (hashtags, what to amplify, approval process)
- Lead capture tool, office hours, and training details
- Lead qualification criteria (MQL/SQL definitions with examples, scoring) — these carry through to the Budget Defense skill
- Event tech stack (event app, meeting scheduling tool, WiFi, Slack channel)
- Salesforce campaign hierarchy and member status
- Staff roster (names, roles, expertise, shifts)
- Speaker support details (deck status, rehearsal schedule, handler)
- Post-event reporting expectations and deadlines
- Key contacts (event planner, staff leads, emergency)
- Any special instructions or notes

## Step 2: Determine Sections

A KBYG has 10 sections. Every section is always generated, but the **depth and detail** varies by tier. The planner can override any recommendation — if they say "include full observation guide for this Tier 3 event," do it.

Read the section templates in `references/sections.md` for the full structure of each section.

| Section | Tier 1 (Flagship) | Tier 2 (Significant) | Tier 3 (Small/Regional) |
|---|---|---|---|
| 1. Event Overview | Full context + format + strategic goals + event goals with KPIs + audience profile | Standard context + format + event goals + KPIs | Brief — name, format, dates, goals, why we're there |
| 2. Our Presence & Design Assets | Full — Booth (number, layout, AV, demos, hours, rules, shifts) + Meeting Spaces (rooms, booking, AV) + War Room/Local Office + all design assets | Standard — Booth + Meeting Spaces + key materials | Light — where to find us + key materials |
| 3. Travel & Logistics | Full — flights, hotel, HR travel policy, per diem, insurance, expense reporting | Standard — hotel, travel basics, expense reporting | Light — travel basics, expense reporting |
| 4. Event Calendar | Full — all hosted, sponsored, program, and highlighted events (partner, industry, C-suite) with registration and run of show | Standard — hosted + program + key highlighted events | Light — key sessions to attend |
| 5. Company Updates & Talking Points | Full — product updates, department updates, key messaging, highlights, messaging boundaries, staff social amplification guidance | Standard — key product updates, talking points, messaging boundaries, social basics | Light — one-paragraph update + boundaries |
| 6. Event Tech & Lead Qualification | Full — event app, lead capture tool, office hours, training, WiFi/access, plus MQL/SQL definitions, scoring, Salesforce campaign info, lead routing | Standard — lead capture + training + event app + MQL/SQL + scoring | Light — lead capture tool + office hours + basic qualification |
| 7. What to Watch For | Full — photo guidance, observation priorities, market observations, what to listen for, reporting | Standard — photo guidance, key things to look for | Brief reminder — capture photos, note highlights |
| 8. Post-Event Reporting | Full — expectations, deadlines, format, metrics, debrief meeting, lead follow-up | Standard — expectations and deadline | Light — brief reminder |
| 9. Staff & Speaker Support | Full — roster, expertise, shifts, who to pull in for what + speaker prep (deck status, rehearsal, handler) + headshot service (Tier 1 only — voluntary) | Standard — roster with name, role, contact + speaker assignments | Light — who's attending + planner contact |
| 10. Key Contacts | Full — planners, staff leads, task owners, vendors, emergency | Standard — planner + key leads + emergency | Planner + emergency contact |

## Step 3: Generate the Document

### Output format

Ask the user: **"Would you like this as a Word document (.docx), Markdown (.md), or a presentation deck (.pptx)?"**

- For `.docx`: Read `/mnt/skills/public/docx/SKILL.md` and follow those instructions for document creation.
- For `.md`: Generate a clean markdown file with clear heading hierarchy.
- For `.pptx`: Read `/mnt/skills/public/pptx/SKILL.md` and follow those instructions. Structure as one section per slide. Keep slides minimal — title, key bullets, and any relevant images only. This format is useful for teams that present the KBYG in an all-hands or pre-event team meeting.

### Virtual and hybrid event adaptation

When event format is **virtual** or **hybrid**, adapt these sections:

- **Section 2 (Our Presence):** Replace Booth with "Virtual Setup" (platform, login credentials, virtual background, audio/video check guidance). Skip Meeting Spaces and War Room unless the company has a physical hub location for a hybrid event.
- **Section 3 (Travel):** Skip for fully virtual. For hybrid, include travel details only for staff attending in person.
- **Section 7 (What to Watch For):** Adapt to virtual context — what to watch in the chat, which sessions to attend live vs. watch recording, how to share observations asynchronously.
- **Shipping (B3):** Not applicable for fully virtual events.

### Formatting guidance

The KBYG assembles and organizes data from the master event record and event folder. It does not rewrite or reinterpret source material. Format the data for scannability:

- **Bold** key info: dates, deadlines, locations, names
- Use bullet points — no one reads paragraphs in a KBYG
- Keep sections short and structured with clear headers
- Embed images where provided (booth layout, floor maps, design asset photos) with brief captions noting placement
- Link everything — registration links, hotel booking, shared folders, event app downloads
- Version and date the document so staff know they have the latest

### Document structure

Start the document with:
- **Document title:** "[Event Name] — Know Before You Go"
- **Event dates and venue** prominently displayed
- **Version date**

Then generate Section 1 (Event Overview) using the event data — assemble name, type, audience, participation level, and goals directly from the source record. Do not compose or rewrite this section — present the data clearly.

Then generate each remaining section based on the tier depth and available inputs. For any information the user didn't provide, include a clearly marked placeholder:

```
**[PLANNER: Add hotel block details and booking link]**
```

These placeholders should be specific about what's needed, not generic "TBD" markers.

End the document with:
- A "Questions?" line pointing to the main event planner contact
- Document version date

### Section-by-section guidance

Refer to `references/sections.md` for detailed content guidance on each section.

## Step 4: Present and Iterate

After generating, tell the user:
- Which tier was applied
- Which sections were populated vs. have placeholders
- Which data was pulled from connected sources vs. manually provided
- Offer to adjust tier depth for any section, add/remove sections, or fill in placeholders if they have more info

Save the final document to `/mnt/user-data/outputs/` and present it to the user.

## Test Cases

See `references/test-cases.md` for three validation scenarios (Tier 1, Tier 2, Tier 3) with expected inputs and output guidance.
