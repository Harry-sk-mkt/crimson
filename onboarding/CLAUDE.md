# onboarding

Tracks work on the Crimson Marketing team's Notion "⛴️ Onboarding" page (`Crimson_marketing / Onboarding`). The onboarding content itself lives in Notion, not here — this folder is a local staging area for tracking what's still missing and drafting content before it goes into Notion.

**Status: actively being built out, not yet usable for a real new hire.** See `TODO.md` for the current gap list.

## Key Notion pages

- Root: [⛴️ Onboarding](https://app.notion.com/p/3d764dfd498f803fac10d4ad656c727a)
- `db_onboarding` (D1–D4/30D checklist database): https://app.notion.com/p/3d764dfd498f80098e8fd83b439c5194
- Weekly database (W1–W4 + D30/D60/D90 Review): https://app.notion.com/p/3d764dfd498f803c83eedd9688a221e3
- Resource hub pages (Customer, Marketing Strategy, Marketing Funnel, Data & KPI, Team Playbook) are already well-written — see `TODO.md` for which ones are not.

## How to work on this

- Draft new/missing page content as markdown files in this folder first, then push into Notion via the Notion MCP tools (`notion-update-page` / `notion-create-pages`) once reviewed.
- `db_onboarding` row pages follow one frame: `## 섹션 (약 N분)` + `- [ ]` checklist, then `---` and `# 모든 태스크 완료했다면 맨 위 Completed? 체크`. Set `순서` and `예상 시간(분)` on each row. Material is taught as a lecture by Harry Yun ("Harry Yun의 [자료] 강의 듣기"), not self-reading. D1 courses end with a 1:1 with that course's owner for feedback; D2 has no 1:1s. The user sets tight task times on purpose. (2026-09-23)
- Copy-paste lists (Slack channels, tool names, etc.) follow root `crimson/CLAUDE.md` "Copy-Paste Lines": one value per block, nothing else on that line.
- When a TODO item is finished in Notion, check it off in `TODO.md` and note the date — don't delete the line, so there's a record of what's been done.
