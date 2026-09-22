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
- [ ] **W2_Kick Off, W3_Own, W4_Boss it** — still literal placeholder templates (`[주제]`, `[자료 1]`, blank underscores). W1_Understand has its goal filled in but everything else in it is still placeholder too.
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
- [ ] Unify `db_onboarding` `Week` options (D1–D4) with the Weekly database (W1–W4) — confirm first that D meant "week".
- [ ] Fill empty `Field` on 4 rows (Growth and Ideation, 좋은 팀원 이해, Growth Meeting, Ideation Meeting); reconsider Tech SETUP = Business; merge the overlapping Growth/Ideation rows.
- [ ] Check the 3 API-unreadable embeds (root alias, Korea Market, School & App Timeline) in the Notion UI with new-hire permissions.
