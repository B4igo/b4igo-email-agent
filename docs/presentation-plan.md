# Final Presentation: Planning Document

**Project:** B4iGo Email Agent (CS Senior Capstone)
**Sponsor:** B4iGo, *Take Control of Your Digital Footprint*
**Format:** 20 min talk, 5 min sponsor / 15 min project (incl. demo)
**Style:** Assertion–Evidence (Alley / Penn State variant)
**Audience:** Mixed. Capstone faculty and classmates in the room; **B4iGo sponsor team watching via livestream.** Assume non-technical.

> Working assumptions called out at the end. Flag anything that's wrong and the plan adjusts.

---

## 1. What we want the audience to walk away with

Order of priority. Every slide should serve at least one of these.

1. **B4iGo empowers people to manage their entire digital footprint** at end-of-life or when incapacitated. Healthcare is the wedge, not the whole story.
2. **Our capstone built B4iGo's first AI data-collection agent**: the thesis describes it; we made it run.
3. **The hard problem was trust**, not parsing. Humans review every extraction before it's saved.
4. **Privacy was a design constraint, not a feature.** All AI runs locally, no user data leaves the device.
5. **It works end-to-end today**, and it extends beyond healthcare.

If a slide doesn't drive one of these home, cut or rework it.

---

## 2. Assertion–Evidence rules (apply to every slide)

Loose A–E. Visual-led, but practical:

- **Headline = one complete sentence** stating the slide's main point. ~16 words max, two lines max.
  - ❌ "Architecture Overview"
  - ✅ "Six small services turn one inbound email into a confirmed vault entry."
- **Body = visual evidence** supporting that sentence: diagram, screenshot, chart, photo. Short bullets are allowed on dense slides (architecture, quality gates, roadmap), but never as the *primary* content. Cap at four lines.
- **Speak the support, don't read the slide.** Headlines are the audience's anchor; you fill in the story.
- **One assertion per slide.** If you find yourself saying "and also…", split the slide.
- **Numbers go on slides; adjectives go in the speech.** "$266.1M annually" on the slide, "huge" in your mouth.

Discipline check before submitting the deck: skim every slide title in order and read them as a paragraph. If that paragraph tells the story, the deck is doing its job.

---

## 3. Timing & speaker plan

| Block | Time | Purpose |
|---|---|---|
| Title + team intro | 0:30 | Who we are, what's coming |
| Sponsor (Part 1) | 3:00 | Why B4iGo matters: empowering people to manage their digital footprint when they can't |
| Project framing | 2:00 | Where our capstone fits in B4iGo's bigger picture |
| How it works | 4:00 | Pipeline + AI in plain language |
| Trust + privacy | 2:00 | The two design constraints we're proudest of |
| Live demo | 4:00 | Email to vault, end to end |
| Engineering & handoff | 3:45 | Architecture, ops console, deployment readiness |
| Closing + Q&A handoff | 0:30 | Thank-yous, return to sponsor |
| **Total** | **19:45** | ~15 sec slack; the closing has natural give if needed |

> **Note on the Part 1 reduction.** Sponsor block dropped from 4:30 to 3:00 after removing the "Two Louisianas" slide (state-medical-board pitch material, not capstone-relevant). 30 seconds of the freed time went to the demo; the rest is slack. The original assignment said "5 min sponsor / 15 min project" — if the team wants to honor that target literally, stretch slides 2 and 3 (Part 1) to ~1:45 each instead of 1:15 and shrink the slack. Either is defensible.

**Speaker rotation:** 4 presenters. Rough split (adjust to team comfort):

- **Speaker A:** Title + sponsor (Part 1), closing
- **Speaker B:** Project framing + how it works
- **Speaker C:** Trust/privacy + live demo (drives the screen)
- **Speaker D:** Architecture/engineering, extensibility, Q&A lead

A clean handoff sentence between speakers is worth rehearsing: *"…and that's where Sam picks up with how we built it."*

**Stream awareness:** B4iGo is on the livestream, not in the room. Keep the camera/mic in mind during Part 1 (they wrote those slides; be accurate, attribute clearly) and during the closing thanks (address them through the camera, not the room).

---

## 4. Slide-by-slide outline

Each entry: **headline** (the assertion, exact wording), **visual** (the evidence), **speaker notes** (~50-80 words covering what the presenter actually says).

### Part 1: Sponsor (3 minutes, 3 slides)

#### Slide 1: Title
- **Headline:** *B4iGo Hybrid Authority Agent AI Prototype*
- **Subhead (small, under the title):** Senior Capstone, Computer Science, Louisiana Tech University
- **Visual:** B4iGo logo (top) + project title large in the middle + team names and roles in a clean row underneath. Optional: a faint pipeline silhouette or vault-wheel watermark behind the title for visual interest, but keep it subtle so the project name carries.
- **Speaker (~30s):** Open with the project name as the sponsor coined it: *"B4iGo Hybrid Authority Agent AI Prototype."* Introduce the team by name, then the structure: a few minutes on the sponsor and the problem they're solving, then the bulk of the talk on this prototype.

#### Slide 2: The everyday problem
- **Headline:** *Our digital lives have grown six-fold in a decade — and most of us have no plan for what happens to them when we can't manage them ourselves.*
- **Visual — "Scattered footprint":** A single grayed silhouette of a person at center. Around them, ~12 small flat icons drifting outward in all directions, drawn from the breadth of a digital life: envelope (email), credit card (banking), key (passwords), insurance card, calendar (subscriptions), ID badge (licenses), file folder (will/legal), lock (accounts), photo (legacy), pill bottle (healthcare), prescription pad, contract scroll (testament). All icons in one accent color. Two stat callouts pinned in opposite corners: top-right *"6× growth in 10 years"*, bottom-left *"30+ accounts per adult"*. No icon labels, no legend. The visual point: digital life is sprawling and uncoordinated.
- **Tools:** Lucide or Phosphor icons (both free, MIT-licensed) dropped into a Figma/Keynote canvas. Single fill color so the eye doesn't have to parse meaning per icon.
- **Speaker (~1:15):** Walk through two relatable scenarios. *"A parent passes — and the family has to track down bank accounts, subscriptions, the will, the social media legacy, all across a dozen services with no master list."* Or: *"A parent has a stroke — and the family doesn't know which medications they take, where the advance directive lives, or who the trusted contact is."* The data exists. It's just unreachable when it matters most.

#### Slide 3: B4iGo's answer
- **Headline:** *B4iGo is your digital agent — it acts on your wishes when you can't speak for yourself.*
- **Visual — "The flip":** Two stacked panels separated by a thin horizontal rule.
  - **Top, labeled "Today":** A cluster of institutional icons at center (hospital, bank, insurance card, social media, subscription provider, government building). ~6 small individual figures around the edges, each with arrows reaching *inward* trying to coordinate across them. One-line caption beneath: *"Your data lives in dozens of institutions. Coordinating it is on you."*
  - **Bottom, labeled "B4iGo":** A single individual icon at center, with a small vault symbol. ~6 small icons around the edges representing the people and institutions who might need access (family, doctor, lawyer, executor, hospital, EMS), each with arrows reaching *outward from the individual*. One-line caption beneath: *"You hold your data. The agent releases it on your terms."*

  The arrows reverse direction between panels. That single visual difference is the entire point of the slide.
- **Speaker (~1:15):** Contrast institution-centric storage (your bank, hospital, insurer each hold a slice) with individual-centric storage (you hold the slice; you decide who sees what, when). Mention briefly that the agent supports three release conditions from the thesis: *immediate*, *at a future date*, or *upon a critical event* like a medical emergency or death. Then set up the project section: *"and an agent can't act on your wishes without a way to know your wishes — which is where we come in."*

### Part 2: Project (~16 minutes, 12 slides + demo)

#### Slide 4: Where our capstone fits
- **Headline:** *B4iGo's thesis envisions AI agents that collect data on the user's behalf. We built the first working one.*
- **Visual — "Inbox to vault":** Left side: a stylized inbox icon with three or four envelope shapes stacked inside. Center: a single right-pointing arrow labeled *"B4iGo agent"* in small text. Right side: a stylized vault/safe icon as a 3×3 grid of nine unlabeled tiles (one per envisioned domain in the thesis). Two tiles (Healthcare and Legal) are filled in the accent color; the other seven are pale gray. Caption below the grid: *"Nine envisioned domains. Two lit up today. Seven within reach."*
- **Speaker (~1:00):** Anchor it in the thesis if you want to: *"AI Agents will collect input that can then be codified into the user's digital footprint portfolio."* That's exactly what we built. Three years after the thesis was written, the agent it imagines runs on the demo laptop. Manual data entry is the #1 reason users abandon platforms like this, especially older or less tech-savvy users (Sarah, in the thesis's persona work). Our agent reads what they already get and proposes structured entries; they stay in the driver's seat.

#### Slide 5: Why this is harder than it sounds
- **Headline:** *A doctor's appointment email is structured information, trapped in unstructured prose.*
- **Visual:** Two-column mockup. Left: a realistic appointment-reminder email. Right: the structured fields we want: `provider`, `date`, `time`, `location`, `preparation_notes`. Arrows from prose to fields.
- **Speaker (~1:00):** Humans read the email and "just know" the appointment is Tuesday at 10. Software has to learn that. Every clinic writes these emails differently. That's the problem we set out to solve.

#### Slide 6: How it works, end to end
- **Headline:** *Six small services move an email from inbox to vault in under thirty seconds.*
- **Visual:** Pipeline diagram. Stylized boxes left-to-right: **Email Provider → Account Manager → Scheduler → AI Service → Confirmation Queue → Vault**. Use icons (envelope, gear, brain, checkmark, lock). Reuse `docs/diagrams/b4igo-email-agent.png` as the base, but simplify text.
- **Speaker (~2:00):** Walk left to right at a layperson's level. *"We connect to the user's existing email (Gmail, IMAP). A scheduler checks for new mail. The AI reads each one. Anything actionable — health, legal, personal — gets queued for the user to review. They tap accept, and it lands in their vault."* No jargon, no port numbers.

#### Slide 7: The AI, in plain language
- **Headline:** *A small model decides what kind of email it is; a larger one extracts the facts.*
- **Visual:** Two-stage diagram. Stage 1: an email going into a "classifier" labeled with five buckets (Health, Legal, Personal, Education, Other). Stage 2: the email plus the bucket going into a "parser" that outputs a JSON-looking card with example fields. Show one real example: an appointment email becoming `{"provider": "Dr. Patel", "date": "...", "location": "..."}`.
- **Speaker (~2:00):** Explain the two-step trick without saying "reranker." *"First, we ask: is this even a healthcare email? That's a quick yes/no across categories. Then, only the right kind of email goes to the slower step that actually pulls out the facts."* This is also where you mention this is the AI work the team is most proud of.

#### Slide 8: The user is always in the loop
- **Headline:** *Nothing reaches your vault until you review and confirm it.*
- **Visual:** Screenshot of the confirmation card in the frontend, with extracted fields editable and accept/reject buttons clearly visible. Annotate with a red circle around the "edit" capability.
- **Speaker (~1:00):** This is intentional. AI gets things wrong. Our system never silently writes anything. The user (or a trusted helper, like an adult child or caregiver — both anticipated in B4iGo's persona work) sees what was extracted, can correct a typo, and chooses what to keep. That's the trust contract.

#### Slide 9: Privacy was a constraint, not a feature
- **Headline:** *Every word of every email is processed locally. Your data never leaves the device.*
- **Visual:** Split graphic. Left side: traditional cloud-AI flow with a red ✗ over an arrow leaving the device. Right side: our flow, with the AI running on the device, green ✓. Small Ollama logo for the technical audience.
- **Speaker (~1:00):** Healthcare data + cloud LLMs = a HIPAA conversation we don't want to have, and the same logic applies to financial records, legal documents, anything you wouldn't post publicly. Running locally is harder (the model has to be smaller and slower), but it means a user on shared rural internet doesn't have to trust an outside server with anything they've stored.

#### Slide 10: Live demo
- **Headline:** *Watch one email become a vault entry, start to finish.*
- **Visual:** The live screen. Have the admin panel and the frontend tiled side by side beforehand. Backup: a pre-recorded 60-second screen capture of the same flow (in case Ollama is cold or the network is bad).
- **Speaker (~4:00):** Narrate three beats:
  1. *Trigger.* Admin panel sends a real-looking appointment email.
  2. *Pipeline lights up.* Point out each stage going green as the email moves through.
  3. *Confirmation.* Flip to the frontend, show the extracted fields, edit one to prove it's editable, hit accept. *"And it's now in the vault."*

  Don't narrate every container. Narrate what a user would experience.

#### Slide 11: Built to scale, not just to demo
- **Headline:** *Six independent services connected by message queues. Each can be scaled, restarted, or upgraded without touching the others.*
- **Visual:** Architecture diagram from slide 6, re-annotated: small "scale up" arrows on the AI service and the scheduler; the Redis queue highlighted as the decoupling seam between mail-pulling and AI inference. Beneath the diagram, a thin row of quality stamps (`black` / `mypy` / `pre-commit` / `e2e`) as a credibility footer.
- **Speaker (~1:00):** This is the architecture pride point. Speaker D should own it. Walk the decision: *"We could have built one big app. We didn't, because email volume is bursty and AI inference is the slow step, so the AI service can scale independently of the part that pulls mail."* Name the queue as the seam: if the AI service goes down, mail isn't lost; it sits in Redis. Close with one beat of engineering rigor (pre-commit hooks, end-to-end test on every change) so the architecture story isn't a hand-wave.

#### Slide 12: Two of nine domains today, the rest within reach
- **Headline:** *Two of B4iGo's nine envisioned domains run today. The rest are a schema and a prompt away.*
- **Visual:** The 3×3 vault tile grid from slide 4, but now showing the pipeline below it — three icons (stethoscope / scales / calendar) feeding into the same architecture, with the lit-up tiles above and pale tiles labeled with thesis domains (financial records, will & testament, accounts/passwords, legacy docs, communications, memorial plans, life story).
- **Speaker (~1:00):** This was a design call, not a side effect. From day one we built a multi-domain pipeline because the thesis is multi-domain. Adding the next one, say financial records or will & testament, is one new Pydantic schema and one prompt template. The pipeline doesn't change. That matters because B4iGo's full vision is much bigger than healthcare, and what we built doesn't have to be rebuilt to follow.

#### Slide 13: B4iGo gets the agent and the tools to run it
- **Headline:** *We didn't just build the agent — we built the ops console B4iGo needs to deploy, validate, and maintain it.*
- **Visual:** Annotated screenshot of the admin panel (capture from the running demo stack). Four callouts pointing to the four panel sections, each with a one-line label:
  - **Demo Actions** — "Send canned scenarios for QA, demos, or onboarding."
  - **E2E Test** — "One synthetic email; live stage-by-stage verification."
  - **Pipeline Trace** — "Combined log stream from every service in one window."
  - **AI Playground** — "Run text or attachments through the AI in dry-run mode."
- **Speaker (~1:00):** Shipping a microservice stack without ops tooling would be irresponsible. So we built the admin panel: one console for everything B4iGo's team needs after we're gone. Send a test email through any scenario for support, demos, or onboarding. Run an end-to-end pipeline check after every code change to verify nothing regressed. Stream live logs from every service in one place when something breaks. Experiment with the AI in dry-run mode without touching the real queue. This is what makes the agent maintainable, not just runnable.

#### Slide 14: Built to be handed off
- **Headline:** *One command brings the stack up; the docs walk through every component; quality gates run on every change.*
- **Visual:** Three-column layout with three large icons in the accent color:
  - **Deploy** (container icon) — "9 containers, one command: `./setup.sh -d`."
  - **Document** (folder icon) — "README + per-service docs + architecture diagrams + vault integration spec."
  - **Verify** (gear icon) — "Pre-commit hooks, mypy, end-to-end test on every change."
- **Speaker (~0:45):** Code without a handoff plan dies. B4iGo needs to be able to pick this up after we graduate. Three things make that possible. One: the entire nine-container stack comes up with a single command, no manual configuration. Two: documentation covers the README, every service's API, the architecture, and the vault integration. Three: code quality is enforced by pre-commit hooks and an end-to-end test that runs on every commit. Whoever picks this up next can find their footing in an afternoon.

#### Slide 15: Closing
- **Headline:** *We didn't build a vault. We built the AI agent that fills it.*
- **Visual:** B4iGo logo + team photo or names + sponsor thank-you line.
- **Speaker (~0:30):** Restate the through-line: B4iGo's thesis describes an AI agent that collects data on the user's behalf. Three years on, we built one. It reads emails, fills the vault, and keeps the user in control, with privacy and consent baked in. Thank the B4iGo team, and open the floor to in-room questions.

---

## 5. Demo plan

A live demo is the most memorable 4 minutes of the talk and the most likely to fail. Treat it like a test you've already taken.

**Setup checklist (run 30 min before the talk starts):**
- `cd demo && ./setup.sh -d`. Full stack up.
- Confirm Ollama is warm: send one email through the admin panel's E2E test and watch it complete.
- Pre-load the admin panel and the frontend in two browser tabs, sized side-by-side.
- Pre-log in to the frontend as `user` / `password`.
- Clear any lingering confirmations from the queue so the demo starts clean.

**The three demo beats** (rehearse these as a unit):
1. **Trigger.** Click a scenario in the admin panel. *"This is what an appointment reminder looks like in a real inbox."*
2. **Pipeline.** Switch to the pipeline trace. *"Watch each stage light up: pull, classify, parse, queue."* ~10–15 seconds.
3. **Review.** Switch to the frontend. *"Here's what the user sees. They can edit anything before it's saved."* Edit one field on stage to prove it's editable. Hit accept. *"And it's in the vault."*

**Backup plan:** A 60-second screen recording of the same flow on the demo laptop. If Ollama is cold or anything stalls past 5 seconds of silence, switch to the recording without apology and keep narrating. Do not debug live.

**What NOT to demo:** the IMAP login flow, the OAuth flow, the admin panel's deep ops features. Tempting; eats time; doesn't add to the story.

---

## 6. Q&A preparation

Anticipated questions, ranked by likelihood. Each presenter should have a one-sentence answer ready.

| Q | Short answer |
|---|---|
| Why local AI instead of GPT-4 / Claude? | Privacy exposure across health, legal, and financial data; cost at scale; and the users we serve often have unreliable internet. |
| What model? How big? | `qwen3:8b` for extraction, a small reranker for classification. Both run under Ollama on commodity hardware. |
| How accurate is the extraction? | We measured against canned scenarios; production-grade accuracy needs a labeled corpus we didn't have time to build. |
| What about hallucinations? | The confirmation step is the safety net: any wrong field is one tap away from being corrected or rejected. |
| Why email and not direct provider integration (FHIR, etc.)? | Email is what people already get, regardless of tech sophistication. FHIR is a future integration, not a starting point. |
| Did you build the vault? | No. B4iGo's vault API is the destination. We built the ingest pipeline that feeds it. |
| How does this connect to B4iGo's broader vision? | The thesis describes nine domains and an AI Agent layer. We built the agent. Two domains run today; adding the others (financial, will, legacy, EoL actions) is a schema and a prompt template per domain. |
| What's left on the roadmap? / What would you do with another semester? | Production hardening (real WSGI runner, OAuth at scale) and the remaining seven thesis domains — financial records, will & testament, legacy documents, EoL actions, memorial plans, life story. The architecture is ready; per-domain work is a Pydantic schema and a prompt template. |
| Who owns the data while it's in transit? | Stays on the user's machine end to end. Service-to-service traffic is on localhost in the demo. |
| How do trusted helpers and caregivers fit in? | The thesis explicitly calls for proxy access (adult children, executors, professional caregivers). Out of scope for this capstone, but the architecture is compatible: the consumer of confirmations is just whatever vault identity is logged in. |
| Cost to deploy? | Negligible. Open-source stack, runs on the user's existing device or a cheap VPS. |
| What's the line between this and a Gmail filter? | Gmail filters route email. We extract structured records and put them under user control inside their B4iGo vault. |

If a question goes off-script, the cleanest move is *"great question, let's take that offline"* rather than guessing on stage.

---

## 7. Visuals to gather or create

We are building all our own visuals. Sponsor decks are not being reused (they were authored for a state medical board audience and are too text-dense for this format).

What exists and is reusable from the repo:

- `docs/diagrams/b4igo-email-agent.png`: full architecture; will need simplification for slide 6.
- `docs/diagrams/AI_Runtime.drawio.png`: basis for slide 7.

What needs to be created:

- **Slide 2:** "scattered footprint" (silhouette + drifting icons + two stat callouts).
- **Slide 3:** "the flip" (two stacked panels with reversed arrow direction).
- **Slide 4:** inbox-to-vault arrow with vault tile grid.
- **Slide 5:** side-by-side prose-vs-fields illustration. Strongest single visual in the deck; worth investing time.
- **Slide 8:** annotated screenshot of the confirmation UI. Capture from the running demo stack.
- **Slide 9:** cloud-vs-local privacy split graphic.
- **Slide 10 (backup):** 60s pre-recorded demo capture.
- **Slide 11:** scaling-arrows annotation on the slide-6 architecture diagram, plus a thin row of quality stamps.
- **Slide 13:** annotated screenshot of the admin panel UI; four callouts to feature areas. Capture from the running demo stack.
- **Slide 14:** three-column "deploy / document / verify" graphic with three large icons.

**Design tips (apply across the deck):**
- One accent color across all slides (suggest B4iGo blue or LA Tech red, pick one and stick with it). Everything else in grayscale.
- Free icon sets: Lucide, Phosphor, Heroicons. All MIT-licensed, all consistent line weights, all easy to drop into Figma / Keynote / PowerPoint.
- Pass the "1-second test": glance at the slide; the audience should grok the point before they finish reading the headline.
- No text on the visual itself unless it's a number or a one-word label.
- Whitespace is doing work. Resist filling it.

---

## 8. Decisions locked in

- **4 presenters.** Speakers A / B / C / D as in §3.
- **Live demo is primary.** Pre-recorded fallback only if the stack stalls past five seconds of dead air.
- **B4iGo on livestream, not in the room.** Part 1 should respect that the people who wrote those slides are listening; reuse their visuals, attribute, don't paraphrase loosely. Closing thanks goes to the camera.
- **Loose A–E.** Declarative headlines and visual-led slides; light bullet support is OK on the architecture, quality, and roadmap slides (§2 reflects this).
- **Architecture is the team's collective pride point** (per Speaker D). Slide 11 leads with scalable microservices and queues; slides 13 and 14 close the engineering arc with the ops console and handoff readiness. Quality gates stay as a credibility footer on slide 11 rather than the main message. Each presenter should still feel free to lean into the part *they* built when they have the floor.
- **No "Two Louisianas" slide.** Removed as state-medical-board pitch material; not relevant to the capstone audience.

## 9. Things to avoid saying

A few traps worth pre-empting. All are easy to walk into in Q&A:

1. **"HIPAA-compliant."** Local AI helps, but compliance is an audit, not a tech choice. Say *privacy-respecting* or *patient data stays local*.
2. **Specific accuracy percentages.** We tested against canned scenarios, not a labeled corpus. If pushed: *"we measured against our scenario set; production-grade benchmarking is on the roadmap."*
3. **"Production-ready."** The README is honest that Flask's dev server fronts the services. Say *demo-stable*, and let the Q&A roadmap question carry the production-hardening details.
4. **Live OAuth or account-linking demo.** Gmail's consent screens are slow and brittle. The story is the email-to-vault flow, not the plumbing.
5. **Deep dives on SIWE / Web3 auth.** It's an unusual choice for healthcare and can derail Q&A toward *"why crypto?"* If asked, one sentence: *"B4iGo's identity model uses wallet-signed sign-in; we adopted it to stay compatible with the rest of their stack."*
6. **Sponsor figures you can't source.** If anyone asks where B4iGo's market-sizing or savings figures come from, defer to B4iGo's published deck rather than improvise.
7. **Port numbers, env vars, terminal output on stage.** Loses the non-technical half of the audience. Save for Q&A.
8. **"We solved healthcare data."** Underselling is fine; oversell will be the first thing remembered, especially with the sponsor on the stream.

---

*v3: Two Louisianas removed, slides renumbered. Next pass: produce the actual deck slide by slide.*
