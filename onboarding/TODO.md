# Onboarding page — TODO

Source: full review of the Notion "⛴️ Onboarding" page tree, 2026-09-21. Page is under active construction — this list is the gap inventory from that review, not a complaint about finished work.

## Quick fixes (links already have a destination, just not wired up)

- [ ] Hyperlink the "회사/비즈니스" resource card to the existing "Company and Business" page.
- [ ] Hyperlink the "용어집" resource card to the existing "📚 Internal Glossary 용어집" page (it has a live `db_Voca` database already).
- [ ] Hyperlink "[온보딩 체크리스트 →]" under "나의 온보딩" to the `db_onboarding` database.
- [ ] Add D60 Review and D90 Review links under "💫 Pit-stop" (pages exist in the Weekly database but aren't surfaced on the root page — only D30 is linked).

## Content to write (pages currently blank or near-empty)

- [ ] **Company and Business** — currently just a bare bookmark to an external presentation. Add 1–2 native paragraphs on the actual revenue model. Can lean on content already written in Marketing Strategy / Data & KPI.
- [ ] **Korea Market** — currently one unrecognized embed block, no real text.
- [ ] **Channel Playbook** — currently fully blank.
- [ ] Every row's detail page in `db_onboarding` (17 items, all blank) — at minimum add: one-line description of the task, a link to the relevant resource page, and fill the `Person` property (schema supports it, unused so far).
- [ ] **W2_Kick Off, W3_Own, W4_Boss it** — _(2026-09-23: the program is now 2 weeks, so W3/W4 go away — see "2-week program" below)_ still literal placeholder templates (`[주제]`, `[자료 1]`, blank underscores). W1_Understand has its goal filled in but everything else in it is still placeholder too.
- [ ] **D30 / D60 / D90 Review pages** — completely blank, not even the template applied.

## Structural gaps (not just missing content — missing sections)

- [ ] Accounts & tool-access checklist: Slack invite + channel list, Google Workspace, Notion permissions, CRM/Salesforce access, ad platform access (Meta/Google/Naver), building/key-card access. Nothing like this exists yet anywhere in the tree.
- [ ] Security/compliance section (data handling, MFA, confidentiality) — currently only a generic link to the general HR policy hub.
- [ ] "Who's Who" — currently only 5 named people (manager, 2 buddies, accounting, campaign execution). No broader team directory/org chart.
- [ ] Communication norms — only "#General" is mentioned. No Slack etiquette, meeting norms, response-time expectations.
- [ ] Defined 1:1 cadence with calendar links (manager, professional buddy, personal buddy) — currently just prose ("a time that suits you both").
- [ ] "How to ask for help" routed by topic (Salesforce, ad platforms, Notion access) — currently only generic IT/HR email aliases.
- [ ] FAQ section — doesn't exist anywhere in the tree.
- [ ] Reconcile the two disconnected "Day 30" processes: the generic "Onboarding Checklist" page's day-30 panel (interview-panel questions, scorecard) vs. the blank `D30 Review` page — right now they don't reference each other.

## Already good — don't touch without reason

Customer, Marketing Strategy, Marketing Funnel, Data & KPI, and Team/Quality Bar Playbook pages are genuinely well-written and detailed. Reuse/cross-link their content rather than rewriting.

## Full review

See conversation from 2026-09-21 for the complete category-by-category writeup (Overview & First Impressions / Critical Gaps / Actionable Recommendations) if more context is needed on any item above.

## Added 2026-09-23 (from `2026-09-23-analysis.md`)

- [ ] Rename or relink the "🛫 마케팅 퍼널" card — it points to role/Segment Ownership content, while the funnel stages live on Marketing Strategy.
- ~~Unify `db_onboarding` `Week` options (D1–D4) with the Weekly database (W1–W4)~~ — dropped 2026-09-23: D1–D4 really do mean day 1–4 (user confirmed).
- [ ] Decide whether to keep the `Field` property. It's a topic tag (Business/Market/Customer/Team/Strategy/Marketing/Practice/Review), but the only board view doesn't show it, and nobody on the team knows what it's for. Delete it, or fill the 4 empty rows and show it in the view.
- [ ] Merge the overlapping Growth/Ideation rows ("Growth and Ideation" D1 vs "Growth Meeting" D2 / "Ideation Meeting" D3).
- [ ] Rebalance D1: 7 items on day 1 (company, market, customer, team, Tech setup, …) is too much for one day. D3 has 2 items and D4 has 1.

### 2-week program (decided 2026-09-23 — Notion not changed yet)

- [ ] Restructure the Weekly database from W1–W4 to W1–W2. Decide what happens to W3_Own / W4_Boss it (delete them, or fold their "own a project" goal into W2).
- [ ] Decide how D1–D4 (the first 4 days) and the rest of the 2 weeks (days 5–10) relate. Right now the checklist only covers day 1–4 plus 30D.
- [ ] Decide whether the D30/D60/D90 reviews stay after a 2-week program, and update the root "💫 Pit-stop" text to match.
- [ ] Update `onboarding/CLAUDE.md` "Key Notion pages" descriptions (they still say W1–W4) after the Notion restructure.

### Missing content to write (from the 9 completion goals)

Goals with no supporting content yet. Company and Business, Korea Market, and Channel Playbook are already listed above.
- [ ] **Existing-campaign analysis practice**: a real past campaign + its data + questions to answer. Supports "기존 캠페인의 성과를 분석할 수 있다". The `기존 캠페인 분석` row is blank.
- [ ] **Mini campaign brief assignment**: template + evaluation criteria for `미니 캠페인 기획`. Could build on Customer page §07 (Customer Message practice).
- [ ] **Independent project definition**: what "프로젝트 독립 운영" (D4) means concretely: scope, owner, what "done" looks like.
- [ ] Check the 3 API-unreadable embeds (root alias, Korea Market, School & App Timeline) in the Notion UI with new-hire permissions.

### Quest checklist (from 2026-09-23 Socratic review)

The real gap is not "every blank", it's the missing execution layer: what to do today, how long it takes, and what counts as done.
- [x] Add `순서`, `예상 시간(분)`, `완료 기준` properties to `db_onboarding`; board view sorted by `순서` and shows `예상 시간(분)` on cards (2026-09-23)
- [x] Fill D1's 7 rows with order, time, and a done-criteria checklist inside each page (2026-09-23; D1 total 390 min). Open: Company and Business / Korea Market source pages are still bookmark/embed only, so "자료 읽기" there depends on content that may not exist yet
- [x] D1 switched to lecture format (Harry Yun) + per-course 1:1 feedback; 1:1s moved out of Tech SETUP (2026-09-23)
- [x] D2 6 rows filled (lecture + practice, no 1:1 — all run by Harry) and D3 order set; `SSM meet-up` row added to D3 (2026-09-23)
- [ ] D2 Growth Meeting `예상 시간(분)` — user will fill
- [ ] Channel lecture material not made yet (채널별 역할 이해 marked "자료 미제작")
- [ ] Fill D3 (미니 캠페인 기획, Ideation Meeting) and D4 pages in the same format
- [ ] Walk through D1 (buddy or self), measure real time, adjust, then extend the same format to the full 10 days
