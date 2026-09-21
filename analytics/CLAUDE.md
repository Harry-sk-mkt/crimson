# analytics

마케팅 퍼널/코호트, 광고 성과/ROI를 Python으로 분석하는 도메인입니다. `lead-tracker/`(Apps Script ETL)가 만든 Master/OPS 시트를 입력으로 받고, 분석 결과만 시트나 문서로 돌려줍니다. 공통 원칙은 루트 `CLAUDE.md`가 우선합니다.

## 다루는 범위

- 마케팅 퍼널/코호트 분석 (Leads → MTA → IC Funnel → SAL → 매출)
- 광고 성과/ROI (Meta, Naver, Kakao, Google 광고비와 리드/매출의 관계)
- 어트리뷰션(채널별 기여도), MMM(채널별 광고 효과 추정)

## lead-tracker와의 경계

- **데이터 수집·변환·Master 빌드는 `lead-tracker/`의 책임이다.** 여기서 재구현하지 않는다. 분석에 필요한 컬럼이 Master에 없으면 `lead-tracker/`에 요청할 사항으로 정리해서 사용자에게 알린다.
- 이 도메인은 Master 시트를 읽기만 한다. Raw/Master/OPS 시트에 직접 쓰지 않는다 (`lead-tracker`의 "Raw is Immutable / Master is Rebuildable" 원칙 유지).
- 비즈니스 규칙(Fiscal Calendar, ACQ 코호트 정의, Business Segment 분류)은 `lead-tracker/docs/`와 `marketing2-report-bizrules` 스킬이 기준이다. 분석 코드에서 다시 정의하지 않는다.

## 구조

| 경로 | 용도 | git |
|---|---|---|
| `CLAUDE.md` | 이 문서 | 추적 |
| `docs/` | 후보 레포 조사, 분석 설계, 결과 해석 | 추적 |
| `data/` | Master 시트에서 내려받은 데이터 | **제외** (`.gitignore`, 이메일 등 개인정보 포함) |
| `.venv/` | Python 가상환경 | **제외** |
| `src/config.py` | 경로, 헤더 라벨, 캠페인 접두사, 대상 월 등 설정 단일 지점 | 추적 |
| `src/load_campaign_members.py` | Salesforce 캠페인 멤버 리포트 로더와 테스트(`python load_campaign_members.py`) | 추적 |
| `src/school_aliases.py` | 학교명 매핑 보정 규칙 (사용자 확정 별칭 `USER_CONFIRMED_ALIASES`, 내가 제안한 별칭 `PROPOSED_ALIASES`, 행 병합). 기본 사전은 `data/`의 학교 목록 워크북에서 읽는다 | 추적 |
| `src/school_normalize.py` | 학교명을 대표 학교로 묶고 국내 국제학교/해외 범위를 붙인다 (`python school_normalize.py`로 테스트) | 추적 |
| `src/school_table.py` | 연도별 6~8월 국내 국제학교별 고유 Contact 표와 테스트 | 추적 |
| `src/concentration_test.py` | 학교별 감소가 우연 이상으로 몰렸는지 몬테카를로 검정과 테스트 | 추적 |
| `src/regular_retention.py` | 단골(regular) Contact 유지율, 참석자 감소의 신규/기존 분해와 테스트 | 추적 |
| `src/event_continuity.py` | 이벤트 간 연속 참석(연속성) 분석. 이벤트 일정표(`data/event_attendance_last4weeks.xlsx`)와 매칭, 테스트 포함 | 추적 |

## 데이터 출처

- `data/[KOR] Priority 1  Striker.xlsx`: 사용자가 내려받은 학교명 매핑 워크북. `P1 School List` 시트를 학교 목록으로 쓴다. 다른 시트에는 이메일/전화번호가 있다 (`docs/context.md`).
- `data/Campaigns with Campaign Members-<연도>년.xlsx`: 사용자가 Salesforce에서 직접 내보낸 리포트 (2026-09-22, `lead-tracker/`에는 없는 데이터). 웨비나 캠페인 `WB-YYYY-MM-KOR-MOFU-Core*`(5~8월)의 멤버 중 Member Type = Contact. Contact는 예전에 한 번이라도 상담을 받은 적이 있는 리드다. 이번 웨비나로 전환되는 것이 아니다 (`docs/context.md` 참고).
- 리포트가 Member Type/Status로 그룹지어 값이 첫 행에만 있고 Total 행이 있다. 로더가 이를 처리하고 리포트 Total과 대조한다.
- **한계**: 리포트가 "All active campaigns"만 포함하고, 월은 캠페인명(`WB-YYYY-MM`) 기준이라 실제 웨비나 개최일과 다를 수 있다 (예: `WB-2024-08 ... (9/11)`). 2024년에만 `Invited`/`Registered` 상태가 있어 연도 간 상태 비교에 주의.

## 컨텍스트 기록 규칙

사용자가 알려주는 용어 정의, 데이터의 의미, 분석 목적, 비즈니스 배경, 그리고 내 해석에 대한 정정은 **그 자리에서 `docs/context.md`에 기록한다** (2026-09-22 사용자 요청으로 도입).

- **즉시 기록**: 답변을 이어가기 전에 먼저 적는다. 세션이 끝나면 대화 내용은 사라지므로 나중에 몰아서 적지 않는다.
- **날짜 표기**: 각 항목에 사용자가 알려준 날짜를 적는다. 사용자가 말한 것과 내가 추론한 것을 섞지 않는다. 추론은 "사용자 확인 전"으로 따로 표기한다.
- **정정은 덮어쓰지 않는다**: 이전 해석이 틀렸다면 항목을 지우지 않고 "정정:" 줄로 남겨 무엇이 왜 바뀌었는지 보이게 한다.
- **분석 전에 읽는다**: 이 도메인의 작업을 시작할 때 `docs/context.md`를 먼저 읽고, 그 정의를 코드 주석과 결과 설명에 반영한다.
- **범위**: 개인정보(이름, 이메일 등)는 적지 않는다. 다른 도메인에도 같은 기록이 필요해지면 사용자에게 확인하고 루트 `CLAUDE.md`로 올린다.

## 원칙

- **개인정보 보호**: 리드 데이터에는 이메일 등 개인정보가 있다. `data/` 밖에 데이터를 저장하거나 커밋하지 않는다. 문서나 결과물에 실제 이메일/이름을 남기지 않는다.
- **No Assumptions**: 시트 이름, 컬럼, 기간, 세그먼트 정의를 추측하지 않는다. 모르면 질문한다.
- **Configuration Centralized**: 시트 ID, 컬럼명, 기간 같은 설정값은 단일 설정 파일에만 둔다. 파일이 생기면 이 문서에 위치를 적는다.
- **TDD**: 함수에 WHY 주석과 기대값 비교 테스트를 함께 작성하고, 테스트 통과 전에는 완료로 보지 않는다.
- **결과 해석의 한계 명시**: 모델 결과는 표본 기간, 데이터 양, 가정을 함께 적는다. MMM 같은 추정 결과를 확정 사실처럼 쓰지 않는다.

## 후보 레포

`docs/candidate-repos.md` 참고. 채택 전 라이선스와 최근 관리 상태를 확인한다.

## 미해결 항목

- **Python 버전**: 로컬은 3.9.13인데 pymc-marketing은 3.12 이상이 필요하다 (2026-09-22 README 기준). 채택 시 `.venv`를 3.12 이상으로 만들어야 한다. 아직 설치하지 않았다.
- **데이터 접근 방식**: Master 시트를 어떻게 내려받을지(Sheets API, CSV export 등)는 미정.
- **분석 데이터 양**: Master의 기간(주 수)이 MMM에 충분한지 아직 확인하지 않았다.
- **첫 분석 주제**: 미정. 코드 구조는 그때 확정한다.
