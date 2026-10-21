# dbTodos & daily integration (2026-10-21~)

아이디에이션(새 아이디어). Notion: https://app.notion.com/p/3ff64dfd498f819c9ec4fd6b2cd5cc62 (dbTodos, Ideation_2.3.2, Status In-writing, Host Harry, Due 2026-10-22~11-04) — 10-21 사용자 요청으로 Claude가 생성, 1️⃣ 본문·2️⃣ 5W1H 입력

## 진행

| 단계 | 상태 | 메모 |
|---|---|---|
| 문제 탐색 | 완료 | 웨비나 등록 감소·Seminar·Contact·오프닝 참석 → 사용자 기각(이유 `analytics/docs/background.md` 10-21). 이벤트 old P1 → 이미 제외 타겟팅 중. iPad 프로모 → New P1 캠페인 아님. New P1 YoY는 증가(TEMPQA_079). 워크스페이스 공유 → 반복 업무 누락 → Daily Update로 좁혀짐 |
| 1️⃣ 배경 | 확정 (10-21) | Problem: dbTodos에서 끝낸 일을 Daily에 다시 적어야 해서 기록이 빠지거나 휘발됨 |
| 2️⃣ 5W1H | 확정 | Due 2026-10-22 ~ 11-04 |
| 3️⃣~5️⃣ | 확정 (10-21) | 가설·Metrics·ICE Notion 반영. 6️⃣·7️⃣은 실험 종료 후 그로스미팅 |

## 근거 (db_Daily 10-06~10-20 평일, 공휴일 10-05·10-09, Harry 휴가 10-06~09 제외, 대상 31일)

- Completed 비어 있음 4/31 (13%), 팀원별 0~3일. 휴가 날 빈 칸(Harry 10-07·08) vs "Day off" 표기(Richard 10-14) 혼재
- 칸별 사용률: Completed 87%, In Progress 65%(Richard 1/9), Next Focus 32%, Team Notes/Blockers 0/10일, `AI summary`·`Person` 속성 0%
- In Progress 휘발 예: Harry 10-14 "9월 딜 리드 소스 변경 재요청", "Brice 미팅 일정" → 10-15 In Progress·Completed 어디에도 없음. 재기입 예: "Expo 디지털 예산 plan" 10-14·10-15 각각 수기
- 영향(사용자): Daily는 대표님께 전달 — 누락되면 관리 미흡으로 비쳐짐

## 사용자 결정

- Team Notes / Blockers 삭제(의미 없음)
- 핵심 이슈 = In Progress 휘발, 연속성 필요. dbTodos를 쓰지만 Daily 항목이 전부 dbTodos에 들어가지는 않음
- 원하는 방향: dbTodos 항목이 Done되면 Daily Completed에 자동 기록(Zapier 같은 자동화)

## 솔루션 메모 (2️⃣에서 확정)

- In Progress → dbTodos 뷰(Host=팀원, Status=In progress, Type=Daily 신규 옵션). 뷰에서 추가하면 필터값 자동 채움 — Person 필터 자동 채움은 테스트 필요
- Done → Completed 텍스트 자동 기록: Zapier(3단계라 유료, 페이지 끝에만 추가) / Make(무료 1,000회, 블록 지정 가능) / Apps Script(무료, reimburse 구조). `Reported` 체크박스로 중복 방지
- dbTodos 스키마: Tasks(title), Host(person), Status(In progress/Done 등), Type(Tasks/Holiday/Ideation/Meeting/Personal), Due

## dbTodos ↔ Daily 대조 (10-06~10-20, 2026-10-21)

- dbTodos `Type=Tasks` 중 Due가 기간 안이고 Done인 항목 8건(Host user ID → 이름은 작업 내용으로 추정: 6bbeb44e=Richard 7건, fc289842=Jennie 1건, 사용자 확인 전)
  - 같은 날 Daily Completed에 있음 2건(신규 입사자 전화 연락, 제주 CAO 캠페인 런칭), 비슷한 항목만 있음 2건(Stanford vs Harvard Recording 런칭 ↔ "11/7 웨비나 캠페인", Korean stu WB opti ↔ "10.31 WB creatives opti"), 없음 4건(SAT 웨비나 카톡 뉴스, Stanford vs Harvard opti, PIC 캠페인 리뷰 (1), SAT opti)
- 반대 방향: 같은 기간 Daily Completed 약 234줄(Harry 111·Jennie 67·Richard 40·Hanna 16, 상위 불릿 기준 수기 집계) 중 dbTodos와 연결되는 건 4~6줄(약 2%)
- 해석(내 판단): 양방향 모두 끊김. dbTodos→Daily 자동 복사만으로는 Daily의 2%만 커버 → In Progress를 dbTodos 뷰로 바꿔 "Daily에 적는 것 = dbTodos 등록"이 되게 하는 쪽이 전제

## 현재 구조 (사용자, 2026-10-21)

- Daily Update에 적은 내용이 매일 19:00 Zapier로 대표님 Slack DM 발송. Zapier 플랜은 미확인 — 2️⃣ How 도구 선택 때 확인
- 1️⃣ 배경 확정(현재 구조 → 두 기록 단절 → Daily 누락·휘발 → 영향 → 원인 → Problem)
- 2️⃣ 결정(사용자, 10-21): 실험 기간 2026-10-22 ~ 11-04(평일 10일), 대상 Harry·Richard·Hanna(Jennie 오프보딩으로 제외), 도구 Zapier(유료, 월 100k 중 45k 사용). 기존 19:00 DM Zap의 Notion 읽기 방식 확인 대기

## 기존 Daily 발송 Zap 구조 (사용자 화면, 2026-10-21)

1. 트리거(스케줄로 추정)
2. Formatter Date/Time: 트리거 시각 UTC → Asia/Seoul, `YYYY-MM-DDTHH:mm:ssZ`
3. Notion Find Data Source Items: db_Daily, Date equals 2단계 값, 여러 개면 first
4. Code by Zapier (Python): 입력 `text`(본문 Markdown, 칩 출처 미확인) → Slack 형식(제목·굵게·불릿·링크 변환, 빈 `-` 줄 삭제)
5. Slack Send Channel Message → #daily-updates (bot)
6. Slack Send Direct Message → 대표님, Schedule At 9 pm KST

- 시사점: 인라인 DB 뷰는 Markdown에 안 실림 → 4단계 앞에 dbTodos In progress 조회 + Code에서 팀원별 삽입 필요. 신규 Zap(Done→Completed)은 2·3단계 재사용. 10-22 오전 #daily-updates 전용 복제 Zap으로 사전 테스트

## 방향 전환 (사용자, 2026-10-21)

- 솔루션 단순화: Daily에는 아무도 직접 쓰지 않고 dbTodos 하나만 사용(습관 변화 수용). 기존 발송 Zap이 발송 시 dbTodos 조회 → 오늘 Done = Completed, In progress = In Progress로 메시지 생성 + Daily 페이지 기록. 새 Zap·템플릿 뷰·블록 끼워넣기 불필요. dbTodos에 `Done date` 속성 + Notion 자동화로 완료일 기록
- 배경 축 변경: "dbTodos vs Daily 대조 → 한 일의 약 2%만 dbTodos에 기록". Problem = "한 일의 대부분이 dbTodos에 기록되지 않아 업무 기록이 Daily에서 휘발됨". Notion 1️⃣·5W1H 반영 완료
- Type 규칙(10-21): 업무=Tasks, 회의=Meeting. Holiday는 안 씀(사용자) → 휴가는 Leave 2.0 시트(https://docs.google.com/spreadsheets/d/1NE2s8IekoPEoksKgmtZbnDN3SajmV_byABVbUQlvZXo/edit, leaves 바인딩) Personal Sheet 탭 `Harry`·`Richard`·`Hanna`(+`Jennie`)에서 오늘 Date 행 조회 → 종일 "Day off", 시간 단위 "(연차 14-18시)", 대휴적립 무시. 5W1H How ①~⑧로 반영
- 3️⃣ 가설(사용자 확정, Notion 반영): 팀원별 기록율(1인 1일 dbTodos 기록 건수 ÷ 기존 Daily 항목 수) 80% 이상. 기준값 Harry 15.9·Richard 4.4·Hanna 3.2건/1인1일(합계 167줄 ÷ 21인일 = 8.0). "Daily 중 dbTodos 비율"은 새 구조에서 무조건 100%라 지표로 안 씀
- 4️⃣ Metrics(사용자 확정, Notion 반영): 지표 = 팀원별 기록율 / 검증 = 팀원별 80% 이상 채택 / 수집 = dbTodos Host별 Created time 10/22~11/04 Tasks·Meeting 건수 ÷ 근무일(Leave 2.0 종일 휴가 제외)
- 5️⃣ ICE(Notion 반영): Impact 8(지표=기록율 기준 2%→80%+), Confidence 4(목표 환산 3명 합계 하루 약 19건 vs 현재 dbTodos 하루 0.8건, 20배+ 습관 변화), Ease 143,000원(천 원 미만 버림, 원값 143,541) = 구축 4.5h(Done date 0.5·발송 Zap 수정 2·Leave 조회 0.5·템플릿 0.25·테스트 1·안내 0.25) × 시급 31,898원(연봉 8,000만 ÷ 2,508h). 광고비 없는 아이디어의 Ease 규칙을 `ideate/CLAUDE.md`에 추가
- 반복 업무(사용자, 10-21): Repeat 항목은 Done 시 다음 회차가 생기는데, 현재는 캘린더 뷰에서 다음 주로 옮기는 식으로 씀 → Done이 안 돼 새 구조에서 보고·집계 누락. 규칙 "반복 업무도 끝나면 Done" How ②에 추가, 4️⃣ 수집 기준을 Created time → Done date로 변경(기준값이 Completed 줄 수라 끝낸 일 기준이 맞음)
- ICE 완료로 Status In-writing → Brief (10-21, 사용자 규칙)
