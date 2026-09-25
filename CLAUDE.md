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
| 온보딩 (Notion 온보딩 페이지 구축) | `onboarding/` | `onboarding/CLAUDE.md`, `onboarding/TODO.md` |
| 이메일 | `email/` | 아직 구조 없음 |
| 글 작성 (Copy/Kakao Library 소재 검수·보완, Ideation 작성) | `writing/` | `writing/CLAUDE.md` |
| 주요 결정 기록 (세션 종료 메모) | `context/` | `context/CLAUDE.md` |

- 도메인이 명확하면 해당 폴더의 `CLAUDE.md`를 먼저 읽고 그 규칙을 따른다.
- 도메인이 모호하거나 여러 도메인에 걸치면 추측하지 말고 사용자에게 확인한다.
- `email/`처럼 구조가 없는 도메인은 첫 실질 작업 시점에 구조를 먼저 확인하고 이 문서를 갱신한다.

## 저장소 구조

- `crimson/` 루트는 git 저장소다 (remote: `github.com/Harry-sk-mkt/crimson`). `blog/`, `lead-tracker/`, `leaves/`는 `.gitignore`로 제외돼 있어 루트 커밋에 포함되지 않는다.
- `blog/`: 별도 git 저장소 (`crimson-naver-blog`)
- `lead-tracker/`: 별도 git 저장소 (`crimson-lead-tracker`). 세션 시작/종료 절차(`scripts/start-session.sh`, Changelog 기록 등)는 그 폴더의 `CLAUDE.md`를 따른다.
- `leaves/`: 별도 git 저장소 (`mkt-leaves`). Google Apps Script(clasp) 프로젝트이며, 세션 절차는 그 폴더의 `CLAUDE.md`를 따른다.
- `analytics/`: 루트 저장소에서 추적하지만 `analytics/data/`(리드 개인정보 포함)와 `analytics/.venv/`는 `.gitignore`로 제외. `lead-tracker/`의 Master 시트를 읽기만 하는 Python 분석 도메인
- `onboarding/`: 별도 저장소 아님, 루트 저장소에서 직접 추적. 실제 온보딩 콘텐츠는 Notion에 있고 이 폴더는 작업 추적/초안용.
- `meetings/`, `email/`, `writing/`, `context/`, `onboarding/`, `.gemini/`, `CLAUDE.md`: 루트 저장소에서 추적하는 파일
- 각 저장소의 커밋/푸시는 그 저장소 안에서 따로 한다. 루트에서 `git add`를 해도 `blog/`, `lead-tracker/`, `leaves/` 변경은 잡히지 않는다.

## 공통 원칙

- **Session-Start Git Sync Check**: 트리거는 "세션 시작" 그 자체다 — 첫 메시지가 순수 질문이라도 첫 응답 전에, 작업할 저장소의 `git fetch` 후 divergence(ahead/behind)와 `git worktree list`를 확인한다. behind만 있고 로컬 변경이 없으면 확인 없이 `git pull`(fast-forward)까지 진행하고, uncommitted 변경이 있거나 ahead/behind가 동시에 있으면 pull하지 않고 먼저 알린다. `scripts/start-session.sh`가 있는 저장소(`lead-tracker/`, `leaves/`)는 그 스크립트로 대신한다. (lead-tracker 2026-07-24 divergence·2026-09-02 오래된 정보로 답변한 사고에서 도입, 2026-09-23 전 도메인 공통으로 승격)
- **Real-Time Decision/Change Log**: 세션 종료 멘트를 기다리지 않고, 의미 있는 결정이나 코드/파일 변경이 생길 때마다 그 즉시 도메인별 기록 위치(`lead-tracker/`는 `docs/Changelog.md`, 루트 저장소는 `context/` — 파일/헤더 형식은 `context/CLAUDE.md` 참고)에 남긴다. 커밋은 로그 작성과 별도로 묶어서 진행해도 되지만, 로그 자체는 절대 세션 끝까지 미루지 않는다. (배경: 기존엔 "오늘은 여기까지" 같은 종료멘트가 유일한 트리거라 종료멘트 없이 세션이 끊기면 그 세션 내용이 통째로 안 남는 gap이 있었음 — 2026-09-24 사용자 확인 후 도입)
- **Session-End Commit & Push (Pre-Authorized)**: 사용자가 "오늘은 여기까지" 류의 종료멘트를 하면, 실제 파일 변경이 있었을 때만(Real-Time Decision/Change Log로 이미 기록된 내용 포함) 커밋한 뒤 별도 확인 없이 `git push`까지 진행한다. 순수 Q&A 세션은 skip. 각 저장소에서 따로 커밋/push한다(`blog/`는 자체 `CLAUDE.md` 절차를 따른다). (lead-tracker 2026-07-29 push 누락으로 다른 장소에서 작업을 못 받은 사고에서 도입, 2026-09-22 루트 적용, 2026-09-23 전 도메인 공통으로 승격)
- **Session-End Summary Format**: 세션 종료 시 채팅에 보여주는 "오늘 한 일" 요약은 모든 도메인 공통으로 **개조식**으로 쓴다 — `-` 불릿, 한 줄에 한 작업, 명사형 종결(`~완료`, `~수정`, `~삽입`, `~확인`), 서술형 문장(`~했습니다`)·부연 설명·파일 경로 나열 금지. 커밋/push/Changelog 기록 같은 절차 자체는 불릿으로 넣지 않는다. 예: `- 온보딩 Notion 페이지 보완 분석 완료`, `- 주별 캐시 단계에 구간별 시간 로그 삽입` (2026-09-23 사용자 확정)
- **Session-End Notion Daily Update**: 사용자가 종료멘트를 하면, 실제 파일 변경이 있었을 때만(순수 Q&A 세션은 skip — 위 커밋 규칙과 동일 조건) Notion `Crimson_marketing / Daily Summary / db_Daily`에서 **Date 속성이 오늘 날짜인 페이지**를 찾아 `🧑 Harry` 섹션의 `✅ Completed:` 불릿 목록에 그 세션의 Session-End Summary Format 불릿을 그대로 추가한다. 기존에 그날 이미 적힌 불릿은 덮어쓰지 않고 이어서 추가(append)한다 — 하루에 여러 세션이 있을 수 있음. 기존에 있던 페이지의 Jennie/Richard 섹션은 건드리지 않는다. **오늘 날짜 페이지가 아직 없으면 `db_Daily`의 기본 템플릿(Daily Summary Mkt)으로 새로 생성하고 Date 속성을 오늘로 설정한 뒤 위와 동일하게 기록한다 — 이때는 템플릿 기본값이 남아있는 Jennie/Richard 섹션 기존 내용을 지우고 각각 "Day off"로 남긴다(신규 생성 시에만 적용, 기존 페이지는 그대로 둠).** (2026-09-24 사용자 확정, Jennie/Richard "Day off" 처리는 같은 날 추가)
- **Copy-Paste Lines**: 복사해서 쓰는 값(채널명, 명령어, 경로, ID, 검색어 등)은 한 줄(Notion은 한 블록)에 값 하나만 둔다 — 한 번에 딱 그 값만 복사할 수 있어야 효율적이기 때문. 여러 값을 쉼표·공백으로 한 줄에 몰지 않는다. 이모지·라벨·설명(🔒, "(담당자)" 등)은 같은 줄에 있어도 된다. Notion·문서·채팅 모든 출력에 적용 (2026-09-23 사용자 확정).
- **No Assumptions**: 파일/시트 이름, 스키마, 기존 구조를 추측하지 않는다. 모르면 질문한다.
- **Configuration Centralized**: 설정값은 도메인별 단일 설정 지점에만 둔다. 하드코딩 금지.
- **TDD**: 함수를 만들거나 고칠 때 WHY 주석과 기대값 비교 테스트를 함께 작성하고, 테스트 통과 전에는 완료로 보지 않는다.
- **Backward Compatibility**: 파일명, 함수명, 시그니처, 기존 산출물은 승인 없이 바꾸지 않는다.

### Apps Script(clasp) 도메인 공통 (`lead-tracker/`, `leaves/`)

- **함수 실행 요청 시 파일명 + 함수명 명시**: `clasp run-function` 미도입이라 사용자가 편집기에서 직접 Run 한다. 예: "`MASTER_003_MTAFunnelSync.js`의 `runSyncMTAFunnelToOPS()` 실행해주세요".
- **Test/Run 함수명은 `_`로 끝내지 않는다**: `_` 접미사 함수는 편집기 Run 드롭다운에서 숨겨진다. `testXXXX()`, `runXXXX()`를 쓸 때마다 이름 끝을 확인한다.
- **`clasp push`는 묻지 않고 실행하되 반드시 `scripts/safe-clasp-push.sh`로**: worktree가 2개 이상이면 확인을 받는다(2026-07-29 worktree 덮어쓰기 사고). "생략해도 됨"이 아니다 — 함수 실행을 요청하기 직전에 push했는지 확인한다(2026-08-06 push 누락으로 옛 코드가 실행된 사고).
- `clasp deploy` 등 도메인별 추가 경계는 각 폴더의 `CLAUDE.md`를 따른다.

각 원칙의 상세 설명은 `.gemini/antigravity/knowledge/crimson-principles.md`, 용어는 같은 폴더의 `glossary.md`, 라우팅 배경은 `domain-routing.md`를 참고한다. 도메인 규칙이 이 원칙과 충돌하면 사용자에게 먼저 확인한다.

## 외부 연동

- 회의 녹음/전사는 로컬 앱 Vibe를 사용한다 (Fireflies 대체, 2026-09-21부터). MCP 자동 연동은 없고, 사용자가 Vibe에서 만든 transcript 파일/텍스트를 직접 전달한다. 처리 규칙은 `meetings/CLAUDE.md`를 따른다.
