/**
 * ==========================================================
 * reimburse
 * 영수증 OCR 텍스트 파싱 + 정산 주기 계산 (순수 함수 — GAS/Node 공용)
 *
 * Responsibility
 * Drive/Sheet API를 부르지 않는다. Node에서 tests/parse.test.js로 검증한다.
 *
 * Version
 * v1.6.0
 *
 * Change Log
 * v1.6.0 (2026-10-19)
 * - 재파싱 9건 실측 보정: 금액 'KRW' 인식, 강한 라벨('총 결제금액')은 다음 줄 '금액원'도 인정,
 *   결제처 별칭(aliases)·'영수증' 다음 줄 규칙, 앱 화면 글자(TALK/과거 주문 내역 등) 제외
 * v1.5.0 (2026-10-19)
 * - buildDescription 추가 (B열 초안 'YYMMDD 결제처'), buildFileName = B열 + 확장자 (사용자 기존 형식)
 * v1.4.0 (2026-10-19)
 * - 결제처: 시각·숫자뿐인 줄(스크린샷 상태바) 건너뜀, '판매자/사업자…' 이후 잘라냄 (첫 실행 9건 실측)
 * v1.3.0 (2026-10-19)
 * - CARD_MAP 키에 '*' 와일드카드 허용 (끝자리까지 가려진 카드: 국민쿠팡 '806*')
 * v1.2.0 (2026-10-19)
 * - 실제 카드사 앱 영수증(폴바셋) 기준 보정: 결제처 = 같은 줄 라벨 값 또는 첫 줄,
 *   카드번호 '.' 가림 인식, 영문 카드사 이름, 금액은 라벨 다음 줄 값을 쓰지 않음
 * v1.1.0 (2026-10-19)
 * - periodFolderName 추가 (주기별 영수증 폴더 이름)
 * v1.0.0 (2026-10-19)
 * - 최초 구현
 * ==========================================================
 */

// WHY: 영수증마다 금액 라벨이 다르다. 앞쪽일수록 "실제 결제액"에 가까운 라벨이라 우선한다.
var AMOUNT_LABELS = [
  /결\s*제\s*금\s*액/, /승\s*인\s*금\s*액/, /받\s*을\s*금\s*액/, /청\s*구\s*금\s*액/,
  /총\s*결\s*제/, /합\s*계/, /총\s*액/, /total/i, /금\s*액/
];
var CARD_ISSUERS = ['삼성', '국민', 'KB', '신한', '현대', '롯데', '하나', '우리', '농협', 'NH', 'BC', '카카오', '토스'];
// WHY: 카드사 앱 영수증은 카드사 이름이 영문으로만 찍히기도 한다 (예: 'Samsung Card').
var CARD_ISSUERS_EN = { Samsung: '삼성', Shinhan: '신한', Hyundai: '현대', Lotte: '롯데', Hana: '하나', Woori: '우리', Kookmin: '국민' };
// 결제처로 쓰지 않는 줄: 영수증 제목, 앱 화면 글자, 라벨 (2026-10-19 실측 — 쿠팡이츠 스크린샷, 해외 승인 영수증)
var TITLE_LINES = /^(카드\s*매출\s*전표|영수증|매출\s*전표|신용\s*카드|거래\s*명세|이용\s*내역|authorization confirmation|(?:talk|x|\|+|준비중)$|과거 주문 내역|주문\s*번호|카드\s*번호|카드\s*종류|account number)/i;
// 이 라벨이면 값이 다음 줄에 와도 믿는다 (다음 줄이 '금액원' 형태일 때만). '이용금액' 같은 약한 라벨은 제외.
var STRONG_AMOUNT_LABEL = /결\s*제\s*금\s*액|승\s*인\s*금\s*액|합\s*계\s*금\s*액|총\s*결\s*제/;
var WON_LINE = /^(\d{1,3}(?:,\d{3})+|\d+)\s*(원|KRW)$/i;
var MONEY_RE = /\d{1,3}(?:,\d{3})+|\d{4,}/g;

function pad2(n) { return (n < 10 ? '0' : '') + n; }

function validYmd(y, m, d) {
  return m >= 1 && m <= 12 && d >= 1 && d <= 31 && y >= 2000 && y <= 2099;
}

// 반환: 'YYYY-MM-DD' 또는 null. 문자열로 다뤄 타임존 변환 문제를 피한다.
function parseDate(text) {
  var patterns = [
    /(20\d{2})\s*[.\-\/년]\s*(\d{1,2})\s*[.\-\/월]\s*(\d{1,2})/g,
    /(?:^|[^\d])(\d{2})[.\-\/](\d{2})[.\-\/](\d{2})(?!\d)/g
  ];
  for (var i = 0; i < patterns.length; i++) {
    var re = patterns[i], m;
    while ((m = re.exec(text)) !== null) {
      var y = Number(m[1]), mo = Number(m[2]), d = Number(m[3]);
      if (y < 100) y += 2000;
      if (validYmd(y, mo, d)) return y + '-' + pad2(mo) + '-' + pad2(d);
    }
  }
  return null;
}

function moneyIn(line) {
  var found = line.match(MONEY_RE);
  return found ? Number(found[found.length - 1].replace(/,/g, '')) : null;
}

// 라벨과 같은 줄의 숫자 → 없으면 '원'/'₩'이 붙은 숫자 중 최댓값.
// WHY: OCR이 표 형태 영수증을 열 단위로 읽어 라벨 다음 줄에 다른 값(승인번호 등)이 오는 경우가 있어
// "라벨 다음 줄" 값은 쓰지 않는다 (2026-10-19 폴바셋 영수증 실측).
function parseAmount(text) {
  var lines = text.split(/\r?\n/);
  for (var k = 0; k < AMOUNT_LABELS.length; k++) {
    for (var i = 0; i < lines.length; i++) {
      if (!AMOUNT_LABELS[k].test(lines[i])) continue;
      var v = moneyIn(lines[i].replace(AMOUNT_LABELS[k], ''));
      if (v !== null) return v;
      // 쿠팡이츠: '총 결제금액' 다음 줄 '31,900원' (주문금액 35,900보다 우선해야 함)
      var next = (lines[i + 1] || '').trim();
      if (STRONG_AMOUNT_LABEL.test(lines[i]) && WON_LINE.test(next)) return moneyIn(next);
    }
  }
  var best = null, m;
  var wonRe = /₩\s*(\d{1,3}(?:,\d{3})+|\d+)|(\d{1,3}(?:,\d{3})+|\d+)\s*(?:원|KRW)/gi;
  while ((m = wonRe.exec(text)) !== null) {
    var n = Number((m[1] || m[2]).replace(/,/g, ''));
    if (best === null || n > best) best = n;
  }
  return best;
}

// WHY: 쇼핑몰 영수증은 '쿠팡(주) 판매자 사업자등록번호 120-88-…'처럼 상호 뒤에 부가 정보가 붙는다.
function cleanMerchant(s) {
  return s.replace(/\s*(판매자|사업자|대표자|전화|주소|TEL)[\s\S]*$/i, '').trim().slice(0, 30);
}

function isMerchantCandidate(line) {
  return line && !TITLE_LINES.test(line) && !/^[\d\s:.,\-\/%()원₩]+$/.test(line) && cleanMerchant(line).length >= 2;
}

// 우선순위: ① 별칭(aliases 키가 본문에 있으면 그 이름) ② 같은 줄 '가맹점명: 값'
// ③ '영수증' 다음 줄 (쿠팡이츠) ④ 제목·앱 글자·숫자뿐인 줄을 건너뛴 첫 줄 (카드사 앱 영수증은 맨 위가 가맹점명)
function parseMerchant(text, aliases) {
  for (var key in (aliases || {})) {
    if (text.toUpperCase().indexOf(key.toUpperCase()) !== -1) return aliases[key];
  }
  var m = text.match(/(?:가맹점명|상호명|상호|매장명)[ \t]*[:：]?[ \t]+([^\r\n]+)/);
  if (m) return cleanMerchant(m[1]);
  var lines = text.split(/\r?\n/).map(function (l) { return l.trim(); });
  for (var i = 0; i < lines.length - 1; i++) {
    if (lines[i] === '영수증' && isMerchantCandidate(lines[i + 1])) return cleanMerchant(lines[i + 1]);
  }
  for (var j = 0; j < lines.length; j++) {
    if (isMerchantCandidate(lines[j])) return cleanMerchant(lines[j]);
  }
  return '';
}

// key의 '*'는 어떤 문자와도 맞는다 ('806*' ↔ '806*', '8061'). 나머지는 글자 그대로 비교.
function cardKeyMatches(key, tail) {
  if (key.length !== tail.length) return false;
  for (var i = 0; i < key.length; i++) {
    if (key[i] !== '*' && key[i] !== tail[i]) return false;
  }
  return true;
}

// cardMap: { '끝4자리': '라벨' }. 마스킹된 카드번호 끝 4자리 → 라벨, 없으면 카드사 이름.
function parseCard(text, cardMap) {
  // 가림 문자는 *, x, . 모두 쓰이고 끝자리까지 가리는 카드도 있다 (예: '5188-31..-....-5050', '....-806*')
  var masked = text.match(/[\d*xX.]{4}[-\s]?[\d*xX.]{2,4}[-\s]?[\d*xX.]{2,4}[-\s]?[\d*xX.]{3,4}/g) || [];
  for (var i = 0; i < masked.length; i++) {
    if (!/[*xX.]/.test(masked[i]) || !/\d{2}/.test(masked[i])) continue;
    var tail = masked[i].replace(/[-\s]/g, '').slice(-4);
    for (var key in (cardMap || {})) {
      if (cardKeyMatches(key, tail)) return cardMap[key];
    }
  }
  for (var j = 0; j < CARD_ISSUERS.length; j++) {
    if (text.indexOf(CARD_ISSUERS[j]) !== -1) return CARD_ISSUERS[j];
  }
  for (var en in CARD_ISSUERS_EN) {
    if (new RegExp(en, 'i').test(text)) return CARD_ISSUERS_EN[en];
  }
  return '';
}

function parseReceiptText(text, cardMap, aliases) {
  text = text || '';
  return {
    date: parseDate(text),
    amount: parseAmount(text),
    merchant: parseMerchant(text, aliases),
    card: parseCard(text, cardMap)
  };
}

// 'YYYY-MM-DD' → 정산 주기 {start, end} ('YYYY-MM-DD'). startDay=20이면 20일~다음달 19일.
function periodFor(ymd, startDay) {
  var p = ymd.split('-').map(Number), y = p[0], m = p[1];
  if (p[2] < startDay) { m -= 1; if (m === 0) { m = 12; y -= 1; } }
  var ey = m === 12 ? y + 1 : y, em = m === 12 ? 1 : m + 1;
  return { start: y + '-' + pad2(m) + '-' + pad2(startDay), end: ey + '-' + pad2(em) + '-' + pad2(startDay - 1) };
}

// 기존 xlsx 탭 이름 형식: '0920-1019Y26 Heesang Yun' (연도 = 시작일 기준)
function periodTabName(ymd, startDay, name) {
  var pr = periodFor(ymd, startDay), s = pr.start.split('-'), e = pr.end.split('-');
  return s[1] + s[2] + '-' + e[1] + e[2] + 'Y' + s[0].slice(2) + ' ' + name;
}

// 기존 주기별 영수증 폴더 형식: '0920-1019 FY26' (연도 = 시작일 기준)
function periodFolderName(ymd, startDay) {
  var pr = periodFor(ymd, startDay), s = pr.start.split('-'), e = pr.end.split('-');
  return s[1] + s[2] + '-' + e[1] + e[2] + ' FY' + s[0].slice(2);
}

function toMDY(ymd) { var p = ymd.split('-'); return p[1] + '-' + p[2] + '-' + p[0]; }

// 기존 xlsx B열 형식: '260908 SNM meeting lunch' — 영수증에선 목적을 알 수 없어 결제처로 초안을 만든다.
function buildDescription(ymd, merchant) {
  var p = ymd.split('-');
  return (p[0].slice(2) + p[1] + p[2] + ' ' + (merchant || '영수증')).trim();
}

// 기존 영수증 파일명 형식 = B열 + 확장자: '260908 SNM meeting lunch.jpg'
function buildFileName(description, ext) {
  var safe = String(description).replace(/[\\\/:*?"<>|]/g, ' ').replace(/\s+/g, ' ').trim();
  return safe + (ext ? '.' + ext : '');
}

if (typeof module !== 'undefined') {
  module.exports = { parseDate: parseDate, parseAmount: parseAmount, parseMerchant: parseMerchant,
    parseCard: parseCard, parseReceiptText: parseReceiptText, periodFor: periodFor,
    periodTabName: periodTabName, periodFolderName: periodFolderName, toMDY: toMDY, buildDescription: buildDescription, buildFileName: buildFileName };
}
