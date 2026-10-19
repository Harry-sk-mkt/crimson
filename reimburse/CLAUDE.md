# reimburse

개인 카드 reimburse 영수증 자동 기록 (Google Apps Script, clasp). 2026-10-19 시작.

## 흐름

1. 카드사 앱에서 영수증을 Drive `Reimburse` 폴더로 바로 공유한다 (파일명은 아무거나).
2. `runProcessReceipts()`가 매일 실행되며 새 파일을 Drive OCR로 읽고, `Reimburse Staging (자동 기록)` 시트의 정산 주기 탭(20일~19일, 예: `0920-1019Y26 Heesang Yun`)에 한 줄씩 기록한다. 날짜·금액·결제처(C열)·카드·Location이 채워지고, 못 읽은 칸은 노란색으로 표시된다. 기록한 파일은 회계 공유 폴더 `88_윤희상_Heesang Yun_Reimbursements` 아래 주기별 폴더(`1020-1119 FY26` 형식, 없으면 생성)로 옮긴다 — `Reimburse`(받은편지함)엔 미처리 파일만 남는다.
3. B(Description)·C(detailed description)에는 `YYMMDD 결제처` 초안이 들어간다 (사용자 기존 xlsx 형식: B = `260908 SNM meeting lunch`, C는 대부분 B와 같음). 사용자는 필요하면 B를 목적으로 고치고 G(계정과목)를 채운다. 파일명은 항상 `B.확장자`로 동기화되고 E(영수증)에 Drive 파일 스마트 칩으로 기록된다(Sheets API `chipRuns`, 동기화 기록은 J열 — 붙여넣기 제외).
4. 정산 주기 마감 때 사용자가 해당 탭의 A~H열을 회계 소유 xlsx(`윤희상 Heesang Yun_Reimbursements.xlsx`)에 붙여넣는다. I열(fileId)은 중복 방지용이라 붙여넣지 않는다.

## 왜 이렇게 했나

- Slack API는 앱 설치 권한 문제로 안 쓴다. Slack `#1-reimburse`는 혼자 모아두는 용도였어서 Drive 직접 공유로 대체.
- Google Form은 카드사 앱 → 폼 공유가 안 돼서 이중 작업이라 버림.
- 회계 xlsx는 Apps Script가 직접 못 쓰고 소유자가 회계라 덮어쓰지 않는다. 월말 붙여넣기 1회는 사용자 승인.

## 파일

- `Config.js` — 폴더·시트 ID, 이름, 열 순서, 카드 끝4자리 매핑(`CARD_MAP`, 비어 있음)
- `Parse.js` — OCR 텍스트 파싱·정산 주기 계산 (순수 함수, `node tests/parse.test.js`로 테스트)
- `Main.js` — Drive/Sheet 연동, 트리거

## 실행 함수 (편집기에서 Run)

- `Main.js`의 `runProcessReceipts()` — 수동 1회 실행
- `Main.js`의 `runInstallDailyTrigger()` — 매일 9시 트리거 등록 (1회만)
- `Main.js`의 `runDumpLatestOcr()` — 받은편지함 최근 영수증 OCR 원문 확인 (파싱 튜닝용, 시트 안 건드림)
- `Main.js`의 `runReparseUndescribed()` — 파싱 규칙 수정 후 G(계정과목)가 비어 있고 C가 B와 같은(손대지 않은) 줄의 B·C·D·F를 다시 채움 + OCR 원문 로그

## 규칙

- push는 `bash scripts/safe-clasp-push.sh` (테스트 통과해야 push). 루트 `CLAUDE.md` Apps Script 공통 규칙을 따른다.
- 이 폴더는 루트 저장소에서 추적한다. 영수증·금액 데이터는 코드에 넣지 않는다.
