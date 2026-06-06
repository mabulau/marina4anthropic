# Master Event Record — Schema Reference

This document defines the data model that powers both the KBYG generator and the Budget Defense skill, plus other event operations tools. A single master event record serves as the **consolidated operational record** for each event — the single place where all event-related data comes together so the skills don't have to query six different systems. Individual source systems (Salesforce for pipeline, CVENT for registration, carrier APIs for shipping) remain authoritative for their own data; the master record aggregates them into one operational view. The KBYG skill reads from it to generate staff briefings. The Budget Defense skill reads from it for ROI forecasting, post-event analysis, and calibration.

**Architecture:** One record per event. Staff profiles are a connected layer that accumulates across events. Market intelligence (competitors, partners, customers) is tracked per event with historical continuity. Event classification fields (type, category, tier) are set once and shared across all skills that read the record.

---

## Data Sources

When connected, pull data from these systems automatically:

| Source | What It Provides |
|---|---|
| Airtable / Google Sheets / Notion | Event record fields, staff assignments, calendars, budgets |
| Google Calendar / Outlook | Hosted/sponsored event schedules, meeting room bookings, debrief meetings |
| Google Drive / Shared Docs | Travel policy docs, product messaging docs, talking points, design asset files, post-event reports |
| Salesforce | Campaign details, lead capture config, pipeline data, follow-up workflows |
| CVENT / Event Platform (Splash, Bizzabo, etc.) | Registration data, attendee lists, session RSVPs, check-in data, session attendance |
| Slack | Event channels, intel sharing, real-time coordination |
| CRM / Contact Directory | Staff contact info, roles, expertise areas |
| Carrier APIs (UPS, FedEx, DHL) | Shipping tracking, delivery status |

When a source is not connected, the skill falls back to manual input or inserts specific placeholders.

---

## Section A: Event Record

These fields map directly to the 10 KBYG sections and provide the data the skill needs to generate the document.

**Event Record Header** (planner-facing metadata, visible at the top of every event record)
- Event status (planning / confirmed / active / post-event / closed)
- Event owner (primary planner)
- Budget owner
- Last updated
- Open issues or blockers

### A1. Event Overview
- Event name
- Event dates (start, end, move-in, move-out)
- Venue name, city, country
- Event format (in-person / virtual / hybrid)
- Event type (trade show / conference / webinar / workshop / executive dinner / customer event / sales presentation / other) — maps to Budget Defense template for ROI analysis
- Event category (hosted / third-party) — hosted means you organized it and control the guest list; third-party means you're attending someone else's event. Affects whether the attendee lever appears in ROI insights. The same event type (e.g., executive dinner) can be either.
- Participation level (booth / sponsorship / speaking / attending only / multiple — specify)
- Event tier (Tier 1 / Tier 2 / Tier 3)
- Conference size (estimated total attendance)
- Type of attendees (technical / executive / mixed / academic / industry-specific — note primary and secondary)
- Area of knowledge or focus (AI, cloud, healthcare IT, fintech, etc.)
- Why we're attending (strategic context — what this event means for our broader business and market position)
- Event goals (pipeline generation / brand awareness / customer engagement / recruiting / partnership development / product launch — can be multiple, each with its own owner and strategy)
- KPIs per goal (e.g., pipeline goal: X leads, $Y influenced pipeline; brand goal: Z impressions, N media mentions)
- Sponsorship package and what's included

### A2. Our Presence & Design Assets

**Booth**
- Booth number, hall, floor location
- Booth layout overview (planner-populated — general description and layout image/link)
- AV setup (screens, monitors, audio, power — what's provided vs. what we bring)
- Demo stations (what's running at each)
- Branded spaces or activations within the booth
- Booth hours
- Booth rules (food/drink policy, storage, security, after-hours access, exhibitor guidelines)
- Booth shift schedule and how to swap or change your shift

**Meeting Spaces**
- Room IDs and names
- Capacity per room
- Hours of availability
- Booking process (who to contact, how to reserve, lead time required)
- AV setup per room (projector, screen sharing, conference call capability, whiteboard)
- Catering available? (yes/no — details)

**War Room / Local Office**
- Location (address or venue room number)
- Access instructions
- Available for (team-only storage, calls, decompression — specify)
- Hours
- AV and connectivity setup

**Design Assets**
- Signage and banners (item, description, dimensions, placement)
- Digital screen content (demo loops, presentations, video reels — what runs where)
- Printed materials (brochures, sell sheets, one-pagers, case studies — with quantities)
- Swag and giveaways (items, quantities, storage location, distribution guidance)
- Branded items (tablecloths, podium wraps, lanyards, badge holders)
- Asset status per item (new / reused / updated)
- Design file locations
- Vendor who produced each asset

### A3. Travel & Logistics
- Hotel name, address, rate, group code, booking link, reservation deadline
- Airport and ground transportation guidance
- Team arrival date and time
- HR travel guidelines (per diem, credit card policy, insurance, expense reporting process and deadline)
- Dress code
- Weather / packing notes
- Travel tips (local restaurants and coffee near venue, neighborhood safety notes, things to do if you have downtime, power adapter needs for international, time zone reminders)

### A4. Event Calendar
- Company-hosted events (sub-records: name, date, time, venue, lead, capacity, description, dress code, registration link)
- Company-sponsored events (sub-records: name, date, time, venue, sponsorship details, staff responsibilities)
- Company in the program (sub-records: session name, date, time, room, speaker, topic)
- Highlighted partner events (sub-records: name, date, time, venue, why it matters, who should attend)
- Highlighted industry-relevant sessions (sub-records: name, date, time, room, what to listen for)
- Highlighted C-suite / executive events (sub-records: name, date, time, venue, who's attending)
- Registration links and deadlines
- Run of show document link

### A5. Company Updates & Talking Points
- Product updates (list)
- Department updates (list)
- Key talking points (3–5 themes)
- Highlights to reference (awards, press, wins)
- Messaging boundaries (embargoed items, sensitive topics, and who to redirect those conversations to)

**Staff Social Media & Amplification**
- Whether staff are expected to post (yes / encouraged / optional)
- Key hashtags (event official + company)
- Content themes to amplify from the company's social accounts
- What not to post (consistent with messaging boundaries above)
- Approval process for live posts (who to run things by before posting)
- Tag/mention guidelines (company handles, event handles)
- Full social media plan: see B5

### A6. Event Tech

Tools and access staff need before arriving on-site.

- Event app (name, download links, what it's used for)
- Badge scanning / lead capture tool (name, app link, credentials distribution)
- Lead capture office hours (when and where to get help on-site)
- Lead capture training (quick-start guide, video walkthrough, or live session — date/time/link)
- Meeting scheduling tool
- Internal comms channel (Slack channel name and link)
- WiFi details (network name, password, backup option)

### A6b. Lead Qualification

How we define, score, and route leads captured at this event.

- MQL definition for this event (with examples) — carries through to the Budget Defense skill for ROI analysis
- SQL definition for this event (with examples)
- Lead scoring criteria (hot / warm / cool — with behavioral signals for each)
- Salesforce campaign hierarchy and member status per campaign
- Lead routing and follow-up ownership (who owns hot leads? warm leads?)

### A7. What to Watch For
- What to look for (booth designs, messaging themes, traffic patterns, product demos, audience reactions — across competitors, partners, and the broader market)
- What to photograph (interesting booth setups, signage, crowd shots, swag, activations — with notes on where/why)
- What to listen for (announcements, product launches, positioning shifts, customer sentiment about specific topics the company cares about)
- Photo and notes sharing channel or folder
- Priority sessions to observe
- Booths and activations to observe (competitors, partners, customers, interesting newcomers)
- Observation reporting channel and deadline

### A8. Post-Event Reporting
- Reporting expectations per attendee
- Submission deadline
- Reporting format and tool
- Debrief meeting date and time
- Lead follow-up timeline (hot, warm, cool)
- Salesforce campaign link (see A6 for campaign hierarchy and member status)

### A9. Staff Attending & Speaker Support
- Staff roster (name, role, expertise area, professional contact, booth shifts)
- Who to pull in for specific conversation types
- Professional headshot/portrait service — Tier 1 events only (voluntary, available dates/times/location at venue)

**Speaker Support**
- Speaker assignments and session details (session name, date, time, room, audience size)
- Deck review status (design review, copy review, final approval — with dates)
- Practice/rehearsal schedule (date, time, location or virtual link)
- Handler needed? (yes/no — handler name, phone, role during session)
- AV requirements per session
- Speaker prep materials (talking points, Q&A prep, audience context)

### A10. Key Contacts
- Event planner(s) (name, phone, email)
- Staff leading specific events
- Staff with other event roles
- Vendor/partner contacts (AV, catering, booth builder)
- Venue emergency contact
- Internal emergency contact

---

## Section B: Operational & Tracking Fields

These fields are used by the event planner for management and tracking. They do not appear in the KBYG but power planning, approvals, and reporting.

### B1. Event Status & Management

Core status fields (event status, owner, budget owner, last updated, open issues) are in the **Event Record Header** above Section A so planners see them immediately alongside the event data. B1 tracks the detailed operational checklists behind that status.

- Key deadlines checklist:
  - Registration deadline
  - Hotel block cutoff
  - Shipping deadline
  - Content submission due dates
  - Sponsorship deliverables due dates
  - Speaker prep deadlines
  - Design asset production deadlines
- Internal approval status (budget approved / content approved / staffing confirmed / shipping confirmed / design approved)
- Notes and open issues

### B2. Budget & Contracts
- Approved budget
- Spent to date
- Remaining budget
- Sponsorship cost
- Vendor contracts (vendor name, service, amount, payment status, payment deadline)
- Invoice tracking

### B3. Shipping & Inventory

**Shipping Plan**
- Shipping method: advance warehouse / direct to show / both
- Advance warehouse: delivery start date, delivery end date, warehouse address, receiving hours
- Direct to show: delivery start date, delivery end date, venue receiving dock address and contact
- Advance warehouse label (show-provided template — attach when ready)
- Direct to show label (show-provided template — attach when ready)

**Items Manifest** (what's going and where)

Each item:
- Item name and description
- Category (booth material / swag / tech / printed materials / branded items / other)
- Quantity
- Shipping method for this item (advance warehouse / direct to show)
- Returning after event? (yes / no / donate / dispose)

**Logistics Details** (per shipment, not per item)
- Box/crate count and dimensions per shipment
- Total weight per shipment
- Carrier and tracking number
- Special handling instructions (fragile, temperature-sensitive, etc.)
- Customs documentation (for international)

**Return Shipping**
- Return shipping plan (carrier, pickup date, destination)
- Return carrier and tracking numbers
- Items not returning (disposed, donated, left with venue — note reason)

### B4. Design Asset Production Tracking
- Asset name
- Type (signage / banner / digital content / print / swag / branded item)
- Status (requested / in design / in review / approved / in production / delivered)
- Designer or vendor assigned
- Review and approval dates
- File location (design files, print-ready files)
- Reusable for future events? (yes / no / with updates)
- Notes (special instructions, print specs, material requirements)

### B5. Communications Plan

**Pre-Event Communications**
- ICP definition for this event (who are we trying to reach?)
- Invite lists (source, segment, size)
- Email copies per event (invite, reminder, last chance, day-of, post-event follow-up)
- Communications cadence (timeline: when each send goes out)
- Landing page / registration page (URL, tracking parameters)

**On-Site Asset Production**
- Daily capture plan (B-roll video, booth shots, crowd shots, product demos, session recordings)
- Headshot and portrait service (voluntary — available for staff who want updated professional photos)
- Production team or assigned staff
- Asset delivery timeline (same-day turnaround? next-day?)
- Where assets are stored and shared (drive folder, DAM, Slack channel)
- Long-term content captures (partner interviews, customer testimonials, site visits, executive conversations — planned in advance with participants)

**Social Media Plan**
- This is the company's/product's social media plan for the event — not just staff guidance
- Platforms active during event (LinkedIn, X, Instagram, etc.)
- Posting cadence (pre-event, live during event, post-event)
- Content themes per day
- Approval workflow for live posts
- Hashtags (event official + company)
- Staff-specific: tag/mention guidelines (company handles, event handles)
- Staff-specific: see A5 for social amplification guidance (what to post, what to amplify, approval process)

**Tracking & Metrics**
- Specific URLs and UTM parameters per campaign
- Tracking links per channel (email, social, paid)
- Website pages to monitor (landing pages, product pages, pricing page)
- Google Search Console data to watch (brand searches, product searches during event window)
- Metrics dashboard link

---

## Section C: Event Intelligence Layer

Historical and competitive data that makes the event program smarter over time. This data accumulates across events and informs future planning.

### C1. Historical Participation

Track our presence at this event in previous years. Each year is a sub-record:

- Year
- Participation level (booth size, sponsorship tier, speaking slots)
- Staff count
- Presentations delivered (titles, speakers, audience size, attendance)
- Design assets used (what was produced, what was reused, what was retired)
- Lead metrics (total captured, MQLs, SQLs, pipeline influenced)
- Meetings held
- Budget spent
- ROI achieved
- Notable outcomes or learnings
- What worked well
- What we'd change

This allows year-over-year comparison and data-driven decisions about whether to increase, maintain, or reduce investment at this event.

### C2. Market Presence Analysis

Track competitor, partner, and customer presence at this event. Each entity is a sub-record with yearly entries:

**Current Year (pre-event intelligence)**
- Entity name and type (competitor / partner / customer / newcomer)
- Confirmed attending? (yes / no / unknown)
- Expected participation level (booth size, sponsorship tier, speaking slots)
- Known announcements or launches expected
- Key staff attending (if known)

**Current Year (captured during event — from on-site observation reports)**
- Actual booth size, location, and design notes
- Messaging themes and positioning
- Demo approaches and featured products
- Booth traffic observations
- Swag and giveaways
- Staff count and engagement style
- Any announcements made
- Photos captured (linked)

**Previous Years (historical records)**
- Same fields as above, organized by year
- Year-over-year changes in their presence (growing, shrinking, repositioning)

### C3. Post-Event Actuals & ROI

**Sales & Pipeline Metrics**
- Total leads captured
- MQLs generated
- SQLs generated
- Opportunities created
- Pipeline influenced
- Closed-won revenue attributed
- Meetings held (on-site)
- Demos delivered
- Event ROI (revenue / cost)

**Digital Marketing Metrics**
- Email campaign performance (sends, open rate, click rate, conversions)
- Social media metrics (impressions, engagement, follower growth, top-performing posts)
- Website / microsite traffic (sessions, unique visitors, page views, conversion rate)
- Content downloads or gated asset engagement
- Hashtag performance

**Traditional Media Metrics**
- Press mentions (publication, date, reach)
- Media appearances and interviews (outlet, date, topic)
- Analyst mentions or coverage
- Speaking session media coverage

**Local & Community Impact**
- Donations made (amount, recipient)
- Volunteer hours contributed
- Tax-deductible items or contributions
- Environmental impact considerations (carbon offset, waste reduction, sustainable sourcing)
- Community partnerships or engagement

---

## Section D: Staff Event Profiles (Connected Layer)

Staff profiles are **not per-event** — they are persistent records per person that accumulate across all events. The master event record references staff profiles when assigning people to an event.

### D1. Staff Profile Record

Each staff member has a profile containing:

**Identity & Expertise**
- Name, title, department
- Professional contact (work phone, work email)
- Areas of expertise (technical / product, sales / pipeline, partnerships / biz dev, executive engagement, press / analyst relations, domain-specific knowledge areas)
- Languages spoken
- Certifications or specializations relevant to events

**Event History**
- Events attended (list with dates, event name, tier, role played)
- Total events attended (count)
- Event types experienced (trade shows, conferences, executive dinners, regional meetups, etc.)

**Speaking History**
- Sessions delivered (event name, session title, date, audience size, attendance count)
- Topics spoken on
- Speaking feedback or ratings (if captured)
- Panels participated in

**Lead Generation Track Record**
- Leads captured per event (total, MQL, SQL)
- Average lead quality score across events
- Pipeline influenced from their leads (if trackable)
- Conversion rate of their captured leads (lead → opportunity)

**Booth & On-Site Performance**
- Booth shifts worked (count across events)
- Demos delivered per event
- Qualitative notes from event planners (e.g., "excellent with technical audiences," "strong at qualifying enterprise leads," "great energy, keeps booth engaged during slow periods")

**Strengths & Best Use**
- Best audience type (technical, executive, mixed)
- Best event format (large conferences, intimate dinners, panels, booth)
- Best event size (large-scale 10K+, mid-size 1K–10K, small <1K)
- Any limitations or preferences noted

### D2. Using Staff Profiles for Event Staffing

When staffing a new event, the skill can query staff profiles to recommend:

- **Booth staff:** Match expertise areas to expected attendee type. Prioritize staff with strong lead generation history at similar events.
- **Speakers:** Match topic expertise and speaking history to session opportunities. Consider audience size experience.
- **Meeting staff:** Match seniority and expertise to the type of meetings expected (executive, technical, partnership).
- **Observation leads:** Staff with strong observation and market intel history.
- **Event leads:** Staff with experience managing similar event types and tiers.

Example query: "This is a Tier 1 technical conference with 5,000 attendees focused on AI infrastructure. Recommend booth staff."

The skill would surface staff who have expertise in relevant technical areas, have attended Tier 1 events before, have strong lead generation metrics at technical conferences, and have positive planner notes about technical audience engagement.

---

## Schema Notes

- **Minimum viable record:** Only Section A1 (Event Overview) fields are required to create a record. Everything else can be populated over time.
- **Progressive enrichment:** A record starts sparse during early planning and fills in as the event approaches. Post-event fields are completed after the event closes.
- **Linking:** Staff profiles (Section D) are linked to event records but maintained independently. A staff member's profile persists and grows regardless of which events they're assigned to.
- **Historical records:** When an event repeats annually, create a new record per year but link to previous years for historical comparison (Section C1).
- **Data format:** This schema is tool-agnostic. It can be implemented in Airtable, Google Sheets, Notion, a database, or any structured data system. Both the KBYG skill and the Budget Defense skill read from whatever format the data lives in.
