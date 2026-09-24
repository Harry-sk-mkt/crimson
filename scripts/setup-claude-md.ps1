# 새 환경(윈도우)에서 ~/.claude/CLAUDE.md 세션 규칙 포인터를 만든다.
# 이 스크립트가 있는 위치(crimson\scripts\)를 기준으로 projects 경로를 자동 계산하므로
# OneDrive 동기화 경로가 PC마다 달라도 그대로 동작한다.
# 새 PC에서는 세션 규칙이 아직 없어 자동 실행이 불가능하므로 최초 1회는 수동 실행 필요.

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectsDir = Split-Path -Parent (Split-Path -Parent $ScriptDir)
$TargetDir = Join-Path $HOME ".claude"
$Target = Join-Path $TargetDir "CLAUDE.md"

New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null

$Template = @'
# Session rules

- 세션 시작 시 cwd와 무관하게 항상 `{0}\crimson\CLAUDE.md`를 먼저 읽고, 그 안의 세션 시작/진행중/종료 규칙(Git Sync Check, Real-Time Decision/Change Log, Session-End Commit & Push, Summary Format, Notion Daily Update 등)을 따른다. cwd가 `crimson\` 하위가 아니어도 마찬가지 — 원래 crimson 하위에서만 자동 로드되던 걸 놓쳐서 세션 종료 규칙이 통째로 안 적용된 사고(2026-09-24)가 있었음.
- At the start of a session, or whenever the user asks what to work on next (e.g. "뭐부터 해야하지"), check `{0}\crimson\TODO.md` (git-tracked, syncs across machines) first before proposing next steps.
- When the user says "기록해줘" (or similar) without specifying where, default to appending it as an item to `{0}\crimson\TODO.md`. Only use long-term memory, a task list, or a project file instead if the content clearly isn't a to-do (e.g. it's a preference, decision log, or project-specific note).
'@

$Content = $Template -f $ProjectsDir

Set-Content -Path $Target -Value $Content -Encoding utf8

Write-Host "Wrote $Target (pointing to $ProjectsDir\crimson)"
