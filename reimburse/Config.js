/**
 * ==========================================================
 * reimburse
 * 전역 설정값 — ID/이름/열 위치는 이 파일에서만 관리한다.
 *
 * Version
 * v1.4.0
 *
 * Change Log
 * v1.4.0 (2026-10-19)
 * - CHIP_NAME 열(J) 추가 — E열 영수증을 Drive 파일 칩으로 쓰기 위한 동기화 기록
 * v1.3.0 (2026-10-19)
 * - MERCHANT_ALIASES 추가 (ANTHROPIC → 'Anthropic 구독료')
 * v1.2.0 (2026-10-19)
 * - CARD_MAP: 5050 삼성KT, 5010 삼성iD, 806* 국민쿠팡 (사용자 확인)
 * v1.1.0 (2026-10-19)
 * - PERIOD_PARENT_ID 추가 (처리한 영수증을 주기별 폴더로 이동)
 * v1.0.0 (2026-10-19)
 * - 최초 구현
 * ==========================================================
 */

var CONFIG = {
  FOLDER_ID: '13E5vPt8B9_4p82EMd6CPQ2ee0ptXDHIe',        // Drive "Reimburse" (카드사 앱 → 여기로 공유, 받은편지함)
  PERIOD_PARENT_ID: '1BhKsyW45qwW0hyycpz184pQ4btzhxsap', // "88_윤희상_Heesang Yun_Reimbursements" — 주기별 폴더(0920-1019 FY26 등)가 있는 곳
  SHEET_ID: '1sM0VKjFexy2zU-gh4FGH9k3mXxqkIoN2ILnpQdfTQn4', // "Reimburse Staging (자동 기록)"
  NAME: 'Heesang Yun',            // 탭 이름 접미사 (xlsx 탭 형식과 동일)
  LOCATION: 'Korea',
  PERIOD_START_DAY: 20,           // 정산 주기 20일~다음달 19일
  SINCE: '2026-10-01',            // 이 날짜 이전에 올라온 파일은 무시 (폴더에 2024년 파일 있음)
  OCR_LANGUAGE: 'ko',
  DAILY_TRIGGER_HOUR: 9,
  // 카드번호 끝 4자리 → xlsx F열 라벨 (예: '1234': '삼성kt'). 비우면 카드사 이름만 들어간다.
  CARD_MAP: { '5050': '삼성KT', '5010': '삼성iD', '806*': '국민쿠팡' },  // '*' = 영수증에서 가려진 자리
  // 영수증 본문에 키가 있으면 결제처를 이 이름으로 (반복 결제, 기존 xlsx 이름 기준). 대소문자 무시.
  MERCHANT_ALIASES: { ANTHROPIC: 'Anthropic 구독료' },
  // xlsx 최근 탭(0920-1019Y26) 열 순서. FILE_ID·CHIP_NAME은 내부용 — 붙여넣기 대상 아님.
  // CHIP_NAME = E열 칩을 마지막으로 쓸 때의 파일명. B가 바뀌면 달라져서 이름 변경 + 칩 재작성.
  HEADERS: ['Date', 'Description', 'detailed description', 'Amount', '영수증', '카드', '계정과목', 'Location', 'fileId (붙여넣기 제외)', '칩 파일명 (붙여넣기 제외)'],
  COL: { DATE: 1, DESC: 2, DETAIL: 3, AMOUNT: 4, RECEIPT: 5, CARD: 6, ACCOUNT: 7, LOCATION: 8, FILE_ID: 9, CHIP_NAME: 10 },
  HEADER_ROW: 2,                  // 1행 = 탭 제목, 2행 = 헤더
  MISSING_COLOR: '#fff2cc'        // OCR로 못 채운 칸 표시
};
