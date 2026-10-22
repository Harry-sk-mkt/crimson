# accepted/

합격 사례 수집 도메인입니다. 회사 Slack `accepted_class2031` 채널의 합격 공지에서 한국인으로 보이는 학생을 자동으로 모아, 한국인 케이스 마케팅에 쓸 후보를 놓치지 않게 합니다. 상위 원칙은 `../CLAUDE.md`를 따릅니다. (2026-10-21 신설, 사용자 요청)

## 흐름

1. Slack `accepted_class2031`에 합격 공지가 올라옴 (형식: 작성자 + 본문. 학생 이름은 `#client-이름-성-26-27` 태그 또는 본문 속 "Firstname Lastname")
2. Zapier: 새 메시지(공개 채널 — 트리거 `New Message Posted to Channel`, 2026-10-22 사용자 확인) → Code(Python, `korean_name_catch.py`) → 후보면 수집 시트 새 탭에 한 줄 추가
3. 사용자가 계약서·커먼앱을 열어 실제 한국인인지 확인하고 분류: **Korea Team 학생** / **다른나라 팀** (기존 시트 탭 이름과 같음)

## 위치

- 수집 시트: `[KOR] Accepted_Class of 2031` — https://docs.google.com/spreadsheets/d/1MkFKP4g7I-Fpz7koIkeP0PW86VWg71T6gF2QQTsvANU/edit
  - 기존 탭: `Korea Team 학생`(Student, High School, Strategists, SSM, University, Tier, Major, Round, Common App, Outreach Email, Print — 2행이 헤더), `다른나라 팀`(Country + 같은 칸, Outreach Email 없음), `Summary`, `국제학교 입결`
  - 자동 수집은 **새 탭 `SlackCrawl`**(2026-10-22 사용자 생성)에 쌓는다 — 1행 헤더 `날짜 | 감지 이름 | 메시지 | Slack 링크 | 분류`(분류는 사용자가 확인 후 Korea Team 학생/다른나라 팀 기입). 기존 탭은 사용자가 확인 후 옮겨 적는 곳이라 건드리지 않음
- Zap: `Accepted Korean SlackCrawl` (Zapier id 384368759, 2026-10-22 생성) — ① Slack New Message Posted to Channel(`accepted_class2031`, 계정 @h.yun (Crimson) #2, 봇 메시지 제외) → ② Code Run Python(input `text` = Slack **Text**(포맷 적용본 — `#client-...` 태그가 그대로 보임), 코드 = `korean_name_catch.py`에서 `__main__` 검증 뺀 부분) → ③ Filter `Is Candidate` (Boolean) is true → ④ Google Sheets Create Spreadsheet Row(계정 h.yun #2, `SlackCrawl`: 날짜 = Ts Time(UTC ISO), 감지 이름 = Names, 메시지 = Text, Slack 링크 = Permalink, 분류 비움, Accepted = School) → ⑤ Slack Send Private Channel Message(`kor_mkt`, 봇 이름 Zapier, Zap 링크 없음): `New Possible Korean Admit!` / `Name: {Names}` / `Accepted: {School}` / SlackCrawl 탭 링크 (2026-10-22 사용자 요청으로 Accepted 열·알림 추가)
  - 시트 열: A 날짜 · B 감지 이름 · C 메시지 · D Slack 링크 · E 분류 · F Accepted. Zapier는 열 위치로 매핑하므로 **열을 중간에 끼워 넣지 말 것**(새 열은 오른쪽 끝에 추가 후 Sheets 단계 Refresh fields)
  - 학교 추출(`school()`)은 추정값 — 합격 단어(offer/acceptance/got into 등) 뒤 from/to/at만 보고, "from Illinois"(출신지)는 건너뜀. 못 찾으면 빈칸
- 판별 코드: `korean_name_catch.py` — Zapier Code 단계에 그대로 붙여 넣는 코드 + 로컬 자체 검증(`py -I korean_name_catch.py` → `all checks passed`)

## 판별 규칙 (놓치지 않는 쪽 우선)

- 확인은 사람이 계약서·커먼앱으로 하므로 recall 우선 — Lee·Park·Lim처럼 다른 나라와 겹치는 성씨도 수집한다.
- 후보: 클라이언트 태그·본문 영문 이름 중 한국 성씨 또는 한국식 이름 음절(2음절 이상), 한글 이름(성씨로 시작하는 2~4자), 이름을 못 찾았는데 한국 단서(Korea/Seoul/:kr: 등)가 있으면 메시지 자체
- 메시지 작성자와 `@멘션`은 직원이라 대상 아님 — Zapier Slack 트리거에선 작성자는 별도 필드, 멘션은 사용자 ID로 들어와 자연히 빠짐

## 규칙

- 학생 이름·메시지 원문 등 개인정보는 저장소에 넣지 않는다. 시트에만 둔다.
- 오탐·누락 사례가 나오면 `korean_name_catch.py`의 `__main__` 검증에 예시를 추가하고 규칙을 고친다(실명 대신 형식만 같은 가상 이름).
