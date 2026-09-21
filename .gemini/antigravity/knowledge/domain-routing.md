# Domain Routing

`crimson` 마더 프로젝트는 여러 도메인 폴더로 구성됩니다. 요청이 들어왔을 때 어느 도메인으로 라우팅해야 하는지에 대한 참고 문서입니다. 상위 작업 원칙은 [[crimson-principles]] 참고.

## blog/

- 실체: `crimson-naver-blog` 레포 (git remote: `github.com/Harry-sk-mkt/crimson-naver-blog`)
- 성격: 네이버 블로그 콘텐츠 기획/작성/검수 파이프라인
- 에이전트(`.claude/agents/`, 11개): `writer`, `researcher`, `pillar-planner`, `quarterly-planner`, `weekly-topic-planner`, `edit-learner`, `revision-verifier`, `style-guard`, `title-pattern-learner`, `data-analyst`, `notion-bridge`
- 라우팅 신호: "블로그", "포스팅", "네이버", "타이틀", "썸네일", "콘텐츠 캘린더", "주제 기획" 등
- 세부 규칙: `blog/CLAUDE.md` 참고 (이 문서가 상위 원칙에 우선하지 않음)

## lead-tracker/

- 실체: `crimson-lead-tracker` 레포 (Google Apps Script 기반)
- 성격: 마케팅 리드 ETL 파이프라인 (`CSV → Import(Raw) → Master Build → Master → Leads_OPS → Reports`)
- 라우팅 신호: "리드", "Master", "Leads_OPS", "리포트(ACQ/NewP1/Target/S&M/FY REP)", "MTA", "IC Funnel", "Salesforce export" 등
- 세부 규칙: `lead-tracker/CLAUDE.md` 및 `lead-tracker/docs/` 전체 (Staged ETL, Config 중앙화, 세션 시작/종료 절차 등 이 도메인 고유 규칙 다수 포함)

## meetings/

- 실체: TBD — 아직 콘텐츠/구조 미정
- 성격 추정: 회의 준비/기록 관련 도메인일 것으로 예상되나, 확정된 범위 없음
- 이 도메인 요청이 들어오면 구조를 추측하지 말고 먼저 사용자에게 확인 ([[crimson-principles]]의 No Assumptions 원칙 적용)

## email/

- 실체: TBD — 아직 콘텐츠/구조 미정
- 성격 추정: 이메일 작성/추적 관련 도메인일 것으로 예상되나, 확정된 범위 없음
- 이 도메인 요청이 들어오면 구조를 추측하지 말고 먼저 사용자에게 확인

## decisions/

- 실체: TBD — 아직 콘텐츠/구조 미정
- 성격 추정: 의사결정 로그(ADR류)일 것으로 예상되나, 확정된 범위 없음
- 이 도메인 요청이 들어오면 구조를 추측하지 말고 먼저 사용자에게 확인

## 라우팅 원칙

1. 요청의 키워드/맥락으로 도메인을 먼저 식별한다.
2. 도메인이 명확하면 해당 폴더의 `CLAUDE.md`/문서를 먼저 읽고 그 도메인의 세부 규칙을 따른다.
3. 도메인이 모호하거나 여러 도메인에 걸치면, 추측하지 말고 사용자에게 확인한다.
4. `meetings/`, `email/`, `decisions/`처럼 아직 구조가 없는 도메인은 첫 실질 작업 시점에 이 문서를 갱신한다.
