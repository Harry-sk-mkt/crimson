# crimson

여러 도메인을 묶는 마더 프로젝트 루트입니다. 이 문서는 요청을 어느 도메인으로 보낼지와 공통 원칙을 정의합니다. 도메인별 세부 규칙은 각 폴더의 `CLAUDE.md`가 우선합니다.

## 도메인 라우팅

| 요청 | 폴더 | 먼저 읽을 문서 |
|---|---|---|
| 블로그 (기획/작성/검수) | `blog/` | `blog/CLAUDE.md` |
| 코딩 (마케팅 리드 ETL, Apps Script) | `lead-tracker/` | `lead-tracker/CLAUDE.md` |
| 회의 기록 (Fireflies transcript 포함) | `meetings/` | `meetings/CLAUDE.md`, `meetings/_index.md` |
| 연차/캘린더 (Apps Script) | `leaves/` | `leaves/CLAUDE.md` |
| 이메일 | `email/` | 아직 구조 없음 |
| 주요 결정 기록 | `decisions/` | 아직 구조 없음 |

- 도메인이 명확하면 해당 폴더의 `CLAUDE.md`를 먼저 읽고 그 규칙을 따른다.
- 도메인이 모호하거나 여러 도메인에 걸치면 추측하지 말고 사용자에게 확인한다.
- `email/`, `decisions/`처럼 구조가 없는 도메인은 첫 실질 작업 시점에 구조를 먼저 확인하고 이 문서를 갱신한다.

## 저장소 구조

- `crimson/` 루트는 git 저장소다 (remote: `github.com/Harry-sk-mkt/crimson`). `blog/`, `lead-tracker/`, `leaves/`는 `.gitignore`로 제외돼 있어 루트 커밋에 포함되지 않는다.
- `blog/`: 별도 git 저장소 (`crimson-naver-blog`)
- `lead-tracker/`: 별도 git 저장소 (`crimson-lead-tracker`). 세션 시작/종료 절차(`scripts/start-session.sh`, Changelog 기록 등)는 그 폴더의 `CLAUDE.md`를 따른다.
- `leaves/`: 별도 git 저장소 (`mkt-leaves`). Google Apps Script(clasp) 프로젝트이며, 세션 절차는 그 폴더의 `CLAUDE.md`를 따른다.
- `meetings/`, `email/`, `decisions/`, `.gemini/`, `mcp_config.json`, `CLAUDE.md`: 루트 저장소에서 추적하는 파일
- 각 저장소의 커밋/푸시는 그 저장소 안에서 따로 한다. 루트에서 `git add`를 해도 `blog/`, `lead-tracker/`, `leaves/` 변경은 잡히지 않는다.

## 공통 원칙

- **No Assumptions**: 파일/시트 이름, 스키마, 기존 구조를 추측하지 않는다. 모르면 질문한다.
- **Configuration Centralized**: 설정값은 도메인별 단일 설정 지점에만 둔다. 하드코딩 금지.
- **TDD**: 함수를 만들거나 고칠 때 WHY 주석과 기대값 비교 테스트를 함께 작성하고, 테스트 통과 전에는 완료로 보지 않는다.
- **Backward Compatibility**: 파일명, 함수명, 시그니처, 기존 산출물은 승인 없이 바꾸지 않는다.

각 원칙의 상세 설명은 `.gemini/antigravity/knowledge/crimson-principles.md`, 용어는 같은 폴더의 `glossary.md`, 라우팅 배경은 `domain-routing.md`를 참고한다. 도메인 규칙이 이 원칙과 충돌하면 사용자에게 먼저 확인한다.

## 외부 연동

- `mcp_config.json`: Fireflies MCP 서버 설정. 회의 transcript pull은 `meetings/CLAUDE.md`의 매칭 규칙을 따른다.
