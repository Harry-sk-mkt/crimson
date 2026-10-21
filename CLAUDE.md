# crimson

여러 도메인을 묶는 마더 프로젝트 루트입니다. 이 문서는 요청을 어느 도메인으로 보낼지와 공통 원칙을 정의합니다. 도메인별 세부 규칙은 각 폴더의 `CLAUDE.md`가 우선합니다.

## 세션 시작

- 세션 시작 시 OS(맥/윈도우)를 확인한다. 사용자가 여러 환경을 오가며 작업하므로, 환경이 바뀌었으면 경로 표기·설치된 도구·아직 못 끝낸 환경별 작업(dmg 삭제, Dock 설정 등)이 이전 환경 기준일 수 있다는 점을 감안한다.
- 최근 `context/*.md`를 확인해 직전 세션에서 넘어온 미결 사항(특히 환경 전환과 관련된 것)이 있는지 살핀다.

## 도메인 라우팅

| 요청 | 폴더 | 먼저 읽을 문서 |
|---|---|---|
| 블로그 (기획/작성/검수) | `blog/` | `blog/CLAUDE.md` |
| 코딩 (마케팅 리드 ETL, Apps Script) | `lead-tracker/` | `lead-tracker/CLAUDE.md` |
| 데이터 분석 (퍼널/코호트, 광고 성과/ROI, 어트리뷰션, MMM) | `analytics/` | `analytics/CLAUDE.md` |
| 회의 기록 (Vibe transcript 포함) | `meetings/` | `meetings/CLAUDE.md`, `meetings/_index.md` |
| 연차/캘린더 (Apps Script) | `leaves/` | `leaves/CLAUDE.md` |
| 개인 reimburse 영수증 자동 기록 (Apps Script) | `reimburse/` | `reimburse/CLAUDE.md` |
| 온보딩 (Notion 온보딩 페이지 구축) | `onboarding/` | `onboarding/CLAUDE.md`, `onboarding/TODO.md` |
| 이메일 | `email/` | 아직 구조 없음 |
| 글 작성 (Copy/Kakao Library 소재 검수·보완) | `writing/` | `writing/CLAUDE.md` |
| 아이디에이션 작성 (dbTodos Ideation 페이지 공동 작성·검토) | `ideate/` | `ideate/CLAUDE.md` |
| 웨비나/세미나 요약 (Vibe transcript 포함) | `event/` | `event/CLAUDE.md` |
| 채용 면접 전사·정리 (Vibe transcript → Notion db_recruit) | `interview/` | `interview/CLAUDE.md` |
| 외주 (번역 등 업체 견적·발주·납품) | `outsource/` (번역: `outsource/translate/`) | `outsource/CLAUDE.md` |
| 합격 사례 수집 (Slack accepted 채널 → 한국인 후보 시트) | `accepted/` | `accepted/CLAUDE.md` |
| 주요 결정 기록 (세션 종료 메모) | `context/` | `context/CLAUDE.md` |

- 도메인이 명확하면 해당 폴더의 `CLAUDE.md`를 먼저 읽고 그 규칙을 따른다.
- 도메인이 모호하거나 여러 도메인에 걸치면 추측하지 말고 사용자에게 확인한다.
- `email/`처럼 구조가 없는 도메인은 첫 실질 작업 시점에 구조를 먼저 확인하고 이 문서를 갱신한다.

## 저장소 구조

- `crimson/` 루트는 git 저장소다 (remote: `github.com/Harry-sk-mkt/crimson`). `blog/`, `lead-tracker/`, `leaves/`는 `.gitignore`로 제외돼 있어 루트 커밋에 포함되지 않는다.
- `blog/`: 별도 git 저장소 (`crimson-naver-blog`)
- `lead-tracker/`: 별도 git 저장소 (`crimson-lead-tracker`). 세션 시작/종료 절차(`scripts/start-session.sh`, Changelog 기록 등)는 그 폴더의 `CLAUDE.md`를 따른다.
- `leaves/`: 별도 git 저장소 (`mkt-leaves`). Google Apps Script(clasp) 프로젝트이며, 세션 절차는 그 폴더의 `CLAUDE.md`를 따른다.
- `interview/`: `CLAUDE.md`만 루트 저장소에서 추적하고 나머지(지원자 전사)는 `.gitignore`로 제외 — 개인정보라 로컬 전용
- `analytics/`: 루트 저장소에서 추적하지만 `analytics/data/`(리드 개인정보 포함)와 `analytics/.venv/`는 `.gitignore`로 제외. `lead-tracker/`의 Master 시트를 읽기만 하는 Python 분석 도메인
- `reimburse/`: 별도 저장소 아님, 루트 저장소에서 직접 추적하는 Apps Script(clasp) 프로젝트. push는 `reimburse/scripts/safe-clasp-push.sh`.
- `onboarding/`: 별도 저장소 아님, 루트 저장소에서 직접 추적. 실제 온보딩 콘텐츠는 Notion에 있고 이 폴더는 작업 추적/초안용.
- `meetings/`, `email/`, `writing/`, `ideate/`, `event/`, `outsource/`, `accepted/`, `context/`, `onboarding/`, `.gemini/`, `CLAUDE.md`: 루트 저장소에서 추적하는 파일
- 각 저장소의 커밋/푸시는 그 저장소 안에서 따로 한다. 루트에서 `git add`를 해도 `blog/`, `lead-tracker/`, `leaves/` 변경은 잡히지 않는다.

## 공통 원칙

- **Session-Start Git Sync Check**: 트리거는 "대화 시작" 그 자체다(= 세션 시작, 용어 통일) — 첫 메시지가 순수 질문이라도 첫 응답 전에, 작업할 저장소의 `git fetch` 후 divergence(ahead/behind)와 `git worktree list`를 확인한다. behind만 있고 로컬 변경이 없으면 확인 없이 `git pull`(fast-forward)까지 진행하고, uncommitted 변경이 있거나 ahead/behind가 동시에 있으면 pull하지 않고 먼저 알린다. `scripts/start-session.sh`가 있는 저장소(`lead-tracker/`, `leaves/`)는 그 스크립트로 대신한다. (lead-tracker 2026-07-24 divergence·2026-09-02 오래된 정보로 답변한 사고에서 도입, 2026-09-23 전 도메인 공통으로 승격)
- **Real-Time Decision/Change Log**: 세션 종료 멘트를 기다리지 않고, 의미 있는 결정이나 코드/파일 변경이 생길 때마다 그 즉시 도메인별 기록 위치(`lead-tracker/`는 `docs/Changelog.md`, 루트 저장소는 `context/` — 파일/헤더 형식은 `context/CLAUDE.md` 참고)에 남긴다. 커밋은 로그 작성과 별도로 묶어서 진행해도 되지만, 로그 자체는 절대 세션 끝까지 미루지 않는다. (배경: 기존엔 "오늘은 여기까지" 같은 종료멘트가 유일한 트리거라 종료멘트 없이 세션이 끊기면 그 세션 내용이 통째로 안 남는 gap이 있었음 — 2026-09-24 사용자 확인 후 도입)
- **Session-End Commit & Push (Pre-Authorized)**: 사용자가 "오늘은 여기까지" 류의 종료멘트를 하면, 실제 파일 변경이 있었을 때만(Real-Time Decision/Change Log로 이미 기록된 내용 포함) 커밋한 뒤 별도 확인 없이 `git push`까지 진행한다. main이 아니라 머신별 세션 브랜치로 push한다 — 아래 Multi-Machine Session Branching 참고. 순수 Q&A 세션은 skip. 각 저장소에서 따로 커밋/push한다(`blog/`는 자체 `CLAUDE.md` 절차를 따른다). (lead-tracker 2026-07-29 push 누락으로 다른 장소에서 작업을 못 받은 사고에서 도입, 2026-09-22 루트 적용, 2026-09-23 전 도메인 공통으로 승격)
- **Multi-Machine Session Branching**: office/mac/home 세 곳을 오가며 작업하므로, 세션 커밋은 main에 직접 하지 않고 위치별 브랜치(`session/office`, `session/mac`, `session/home`)에 커밋·push한다.
  - **세션 시작 순서**: (1) main을 `git pull`로 최신화 → (2) 아래 표에서 `hostname` 결과로 위치를 판별 → (3) 그 위치의 `session/<위치>` 브랜치로 checkout(없으면 최신 main 기준으로 새로 생성, 있으면 main이 앞서 있을 때 fast-forward로 반영) → 작업 시작. 작업할 저장소마다(루트, `lead-tracker/` 등) 각각 적용한다.
  - **위치 판별 표** — 표에 없는 컴퓨터면 추측하지 말고 사용자에게 office/mac/home 중 어디인지 물은 뒤, 그 `hostname`을 이 표에 추가한다.

    | 위치 | hostname | 브랜치 |
    |---|---|---|
    | office | `DESKTOP-BMRK5VF` (Windows) | `session/office` |
    | mac | `MacBook-Air-od-Harry.local` | `session/mac` |
    | home | `underline_desk` | `session/home` |

  - **main 병합 — 언제**: 저장소마다(루트, `lead-tracker/` 등) 각각 판단한다.
    - **세션 종료 push 시 자동 병합 (Pre-Authorized)**: 내 세션 브랜치를 push한 뒤 `git fetch`. 조건 두 가지가 모두 맞으면 확인 없이 main을 내 브랜치로 fast-forward하고 push한다. ① 다른 위치 브랜치(`origin/session/*`)에 main에 없는 커밋이 없다. ② main에 내 브랜치에 없는 커밋이 없다. 그다음 다른 세션 브랜치도 main 위치로 맞춘다. 하나라도 어긋나면 병합하지 않고, 다음 세션 시작 때 묻는 쪽으로 넘긴다.
    - **세션 시작 시 병합 제안**: Git Sync Check 때 다른 위치 브랜치에 main에 없는 커밋이 있으면 "병합할까요?"(위치별 커밋 수 포함)라고 한 줄만 묻는다. 승인을 받은 뒤에만 아래 절차로 병합한다. 다른 위치 세션이 끝났는지도 이때 확인한다.
    - 위 두 경우 외에는 사용자가 명시적으로 요청할 때만 병합한다. 위치 무관.
  - **main 병합 — 절차** (2026-09-29~10-19 병합 관행을 정리):
    1. `git fetch` 후 각 `session/*`가 main보다 몇 커밋 앞서 있는지 보고한다. 끝나지 않은 위치 세션은 push된 커밋까지만 병합한다.
    2. main에서 fast-forward가 되는 브랜치를 먼저 반영하고, 나머지는 merge commit으로 합친다. 한 브랜치의 커밋이 이미 다른 브랜치에 들어 있으면 따로 병합하지 않는다.
    3. 충돌: `context/*.md`의 같은 날짜 파일은 양쪽 내용을 모두 살려 시간순으로 합친다. `TODO.md`는 양쪽에서 추가한 항목을 모두 살리고, 같은 항목이 서로 다르게 바뀌었으면 사용자에게 확인한다. `CLAUDE.md`와 코드는 자동 병합이 안 되면 사용자에게 확인한다.
    4. main을 push한 뒤 모든 세션 브랜치를 main 위치로 맞춘다. force push는 금지한다. 거부되면 병합 중에 새 커밋이 올라온 것이니 멈추고 알린다.
    5. `context/<오늘>.md`에 `## main 병합 — Claude Code (위치)` 섹션(순서, 충돌 파일, 해결 방식)을 쓰고 INDEX에 한 줄 추가한다. 자동 병합도 기록한다.
  - (2026-09-28 맥/데스크탑 동시 세션 충돌 방지 위해 도입, 같은 날 office/mac/home 3곳 + hostname 자동 판별 + 병합 위치 무관으로 확장 — 사용자 확정. 기존 `session/desktop`은 `session/office`로 이름 변경)
- **Session-End Summary Format**: 세션 종료 시 채팅에 보여주는 "오늘 한 일" 요약은 모든 도메인 공통으로 **개조식**으로 쓴다 — `-` 불릿, 한 줄에 한 작업, 명사형 종결(`~완료`, `~수정`, `~삽입`, `~확인`), 서술형 문장(`~했습니다`)·부연 설명·파일 경로 나열 금지. 커밋/push/Changelog 기록 같은 절차 자체는 불릿으로 넣지 않는다. 예: `- 온보딩 Notion 페이지 보완 분석 완료`, `- 주별 캐시 단계에 구간별 시간 로그 삽입` (2026-09-23 사용자 확정)
- **Session-End dbTodos Update (2026-10-22~, 기존 Notion Daily Update 대체)**: 사용자가 종료멘트를 하면, 실제 파일 변경이 있었을 때만(순수 Q&A 세션은 skip — 위 커밋 규칙과 동일 조건) Notion `dbTodos`(`collection://2907cc28-daa4-4494-9ab6-ad4a6dd0a3dd`)에 그 세션의 업무를 기록한다. Daily 페이지(`db_Daily`)에는 더 이상 직접 쓰지 않는다 — 발송 Zap이 dbTodos로 Daily를 만들기 때문에 직접 쓰면 중복·덮어쓰기가 생김 (아이디에이션 "dbTodos & daily integration", `ideate/2026-10-21-dbtodos-daily-integration.md`, 2026-10-21 사용자 확정).
  1. 먼저 `Host = Harry`, `Status = In progress` 항목을 조회해, 이번 세션에 끝낸 일이 그중에 있으면 새로 만들지 않고 그 항목을 `Done` + `Done date = 오늘`로 바꾼다.
  2. 목록에 없던 끝낸 일은 Session-End Summary Format 불릿 **한 줄당 한 항목**으로 새로 만든다: `Tasks` = 개조식 한 줄, `Host` = Harry, `Type` = `Tasks`(회의 전사·참석은 `Meeting`), `Status` = `Done`, `Done date` = 오늘, `Due` = 오늘. `Select`는 아이디어 전용이라 비운다.
  3. 다음 날로 넘어가는 일(기존 🚧 In Progress)은 `Status = In progress`로 만든다. 같은 일이 이미 In progress로 있으면 새로 만들지 않는다.
  4. 반복 업무(`Repeat`)도 끝나면 `Done`으로 바꾼다 — 캘린더에서 다음 주로 옮기지 않는다(다음 회차는 Repeat가 자동 생성).
  - `Done date` 속성이 아직 없으면(10-22 구축 전) 그 칸만 비우고 기록한 뒤, 구축 후 채운다.
  - 이전 규칙(2026-09-24~10-21, 이력): `db_Daily`에서 Date가 오늘인 페이지의 `🧑 Harry` 섹션 `✅ Completed:`에 Summary 불릿을, 다음 날로 넘어가는 일은 `🚧 In Progress:`에 append. 오늘 페이지가 없으면 기본 템플릿(Daily Summary Mkt)으로 생성하고 Harry 외 팀원 섹션은 "Day off"로 둠.
- **Copy-Paste Lines**: 복사해서 쓰는 값(채널명, 명령어, 경로, ID, 검색어 등)은 한 줄(Notion은 한 블록)에 값 하나만 둔다 — 한 번에 딱 그 값만 복사할 수 있어야 효율적이기 때문. 여러 값을 쉼표·공백으로 한 줄에 몰지 않는다. 이모지·라벨·설명(🔒, "(담당자)" 등)은 같은 줄에 있어도 된다. Notion·문서·채팅 모든 출력에 적용 (2026-09-23 사용자 확정).
- **No Assumptions**: 파일/시트 이름, 스키마, 기존 구조를 추측하지 않는다. 모르면 질문한다.
- **Configuration Centralized**: 설정값은 도메인별 단일 설정 지점에만 둔다. 하드코딩 금지.
- **TDD**: 함수를 만들거나 고칠 때 WHY 주석과 기대값 비교 테스트를 함께 작성하고, 테스트 통과 전에는 완료로 보지 않는다.
- **Backward Compatibility**: 파일명, 함수명, 시그니처, 기존 산출물은 승인 없이 바꾸지 않는다.

### Apps Script(clasp) 도메인 공통 (`lead-tracker/`, `leaves/`, `reimburse/`)

- **함수 실행 요청 시 파일명 + 함수명 명시**: `clasp run-function` 미도입이라 사용자가 편집기에서 직접 Run 한다. 예: "`MASTER_003_MTAFunnelSync.js`의 `runSyncMTAFunnelToOPS()` 실행해주세요".
- **Test/Run 함수명은 `_`로 끝내지 않는다**: `_` 접미사 함수는 편집기 Run 드롭다운에서 숨겨진다. `testXXXX()`, `runXXXX()`를 쓸 때마다 이름 끝을 확인한다.
- **`clasp push`는 묻지 않고 실행하되 반드시 `scripts/safe-clasp-push.sh`로**: worktree가 2개 이상이면 확인을 받는다(2026-07-29 worktree 덮어쓰기 사고). "생략해도 됨"이 아니다 — 함수 실행을 요청하기 직전에 push했는지 확인한다(2026-08-06 push 누락으로 옛 코드가 실행된 사고).
- `clasp deploy` 등 도메인별 추가 경계는 각 폴더의 `CLAUDE.md`를 따른다.

각 원칙의 상세 설명은 `.gemini/antigravity/knowledge/crimson-principles.md`, 용어는 같은 폴더의 `glossary.md`, 라우팅 배경은 `domain-routing.md`를 참고한다. 도메인 규칙이 이 원칙과 충돌하면 사용자에게 먼저 확인한다.

## 외부 연동

- 회의 녹음/전사는 로컬 앱 Vibe를 사용한다 (Fireflies 대체, 2026-09-21부터). MCP 자동 연동은 없고, 사용자가 Vibe에서 만든 transcript 파일/텍스트를 직접 전달한다. 처리 규칙은 `meetings/CLAUDE.md`를 따른다.
