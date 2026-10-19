// node reimburse/tests/parse.test.js — Parse.js 기대값 비교 테스트
var assert = require('assert');
var P = require('../Parse.js');

var cardReceipt = [
  '카드매출전표',
  '가맹점명 : 스타벅스 압구정점',
  '가맹점번호 12345678',
  '거래일시 2026/10/17 12:31:05',
  '카드번호 5310-12**-****-3456',
  '삼성카드',
  '공급가액 9,091',
  '부가세 909',
  '합계 10,000',
  '승인금액',
  '10,000원'
].join('\n');

var r = P.parseReceiptText(cardReceipt, { '3456': '삼성kt' });
assert.strictEqual(r.date, '2026-10-17');
assert.strictEqual(r.amount, 10000);          // 승인금액(다음 줄) 우선, 합계보다 앞
assert.strictEqual(r.merchant, '스타벅스 압구정점'); // 가맹점번호 줄은 무시
assert.strictEqual(r.card, '삼성kt');          // 끝4자리 매핑

var app = P.parseReceiptText('쿠팡\n주문일 2026.09.04\n결제금액 27,300원\nKB국민카드', {});
assert.strictEqual(app.date, '2026-09-04');
assert.strictEqual(app.amount, 27300);
assert.strictEqual(app.card, '국민');          // 매핑 없으면 카드사 이름

// 실측: 삼성카드 앱 영수증 OCR (2026-10-19 runDumpLatestOcr). 라벨·값이 열 단위로 흩어져 나온다.
var samsungApp = ['폴바셋 종각역점', '14,100원', '카드종류', '개인/신용카드', '카드번호', '5188-31..-....-5050',
  '거래일자', '26.10.15 12:33', '일시불/할부', '승인번호', '이용금액', '부가세', '일시불', '13477132', '12,818원',
  '1,282', '봉사료', '0원', '컵 보증금', '0원', '가맹점정보', '가맹점명', '사업자등록번호', '폴바셋 종각역점',
  '2118895935', '가맹점번호', 'Samsung Card'].join('\n');
assert.deepStrictEqual(P.parseReceiptText(samsungApp, {}),
  { date: '2026-10-15', amount: 14100, merchant: '폴바셋 종각역점', card: '삼성' });
assert.strictEqual(P.parseReceiptText(samsungApp, { '5050': '삼성kt' }).card, '삼성kt');

// 실측(첫 실행 9건): 스크린샷 상태바 시각, 쇼핑몰 판매자 정보
assert.strictEqual(P.parseMerchant('19:52\n\n주문 상세\n결제금액 35,900원'), '주문 상세');
assert.strictEqual(P.parseMerchant('쿠팡(주) 판매자 사업자등록번호 120-88-00767'), '쿠팡(주)');
assert.strictEqual(P.parseMerchant('(주)유니씨앤씨 판매자 사업자등록번호 106-86-09'), '(주)유니씨앤씨');
assert.strictEqual(P.parseMerchant('상호 : 오만복 대표자 김OO'), '오만복');

// 실측(재파싱 로그): 해외 승인 영수증 — KRW 금액, 맨 윗줄 제목, 별칭
var anthropic = ['Authorization confirmation', '카드번호', '5188-31..-....-5010', 'Account number', '현지이용금액',
  'Authorization amount', '승인일자(년/월/일)', '승인번호', '가맹점명', 'Merchant', 'name', '35,000KRW', '25.36 USD',
  '26.09.21', '135882', 'ANTHROPIC* CLAUDE SUB SAN FR', 'ANCISCO USA', 'Samsung Card'].join('\n');
assert.deepStrictEqual(P.parseReceiptText(anthropic, { '5010': '삼성iD' }, { ANTHROPIC: 'Anthropic 구독료' }),
  { date: '2026-09-21', amount: 35000, merchant: 'Anthropic 구독료', card: '삼성iD' });

// 실측: 쿠팡이츠 스크린샷 — 상태바·앱 글자, 주문금액(35,900) 대신 총 결제금액(31,900)
var eats = ['19:52', 'TALK', '과거 주문 내역', 'X', '준비중', '영수증', '스타벅스 압구정로점', '주문번호: 2N39W5',
  '2026-10-12 13:03', '23,500원', '3,000원', '주문금액', '배달비', '할인금액', '35,900원', '0원', '-4,000원',
  '와우 카드(KB) 결제', '31,900원', '총 결제금액', '31,900원', '와우 카드(KB) 498761******806* 결제완료'].join('\n');
assert.deepStrictEqual(P.parseReceiptText(eats, { '806*': '국민쿠팡' }, {}),
  { date: '2026-10-12', amount: 31900, merchant: '스타벅스 압구정로점', card: '국민쿠팡' });
var eats2 = ['18:19', '과거 주문 내역', 'X', '영수증', '주문번호: 05NA8G', '2026-10-14 17:15', '501 99', '준비중',
  '싸이버거 단품', '6,000원', '주문금액', '20,900원', '총 결제금액', '20,900원'].join('\n');
assert.strictEqual(P.parseMerchant(eats2, {}), '싸이버거 단품');   // 가게 이름이 화면에 없음 → 첫 메뉴
assert.strictEqual(P.parseAmount(eats2), 20900);
assert.strictEqual(P.parseMerchant('Xerox 강남점\n1,000원', {}), 'Xerox 강남점');   // 'X'는 한 글자 줄만 제외

var cards = { '5050': '삼성KT', '5010': '삼성iD', '806*': '국민쿠팡' };
assert.strictEqual(P.parseCard('카드번호 9430-12**-****-806*\nKB국민카드', cards), '국민쿠팡'); // 끝자리 가림
assert.strictEqual(P.parseCard('5188-31..-....-5010', cards), '삼성iD');
assert.strictEqual(P.parseCard('5188-31..-....-5099\nSamsung Card', cards), '삼성');            // 미등록 → 카드사
assert.strictEqual(P.parseCard('거래일자 26.10.15 12:33', cards), '');                            // 날짜 오인 없음

assert.strictEqual(P.parseDate('2026년 8월 20일'), '2026-08-20');
assert.strictEqual(P.parseDate('일시 26.09.11 13:00'), '2026-09-11');
assert.strictEqual(P.parseDate('전화 02-1234-5678'), null);
assert.strictEqual(P.parseAmount('택시비 15,000원\n팁 2,000원'), 15000); // 라벨 없으면 원 붙은 최댓값
assert.strictEqual(P.parseAmount('영수증'), null);
assert.deepStrictEqual(P.parseReceiptText(''), { date: null, amount: null, merchant: '', card: '' });

assert.deepStrictEqual(P.periodFor('2026-10-19', 20), { start: '2026-09-20', end: '2026-10-19' });
assert.deepStrictEqual(P.periodFor('2026-10-20', 20), { start: '2026-10-20', end: '2026-11-19' });
assert.deepStrictEqual(P.periodFor('2027-01-05', 20), { start: '2026-12-20', end: '2027-01-19' });
assert.strictEqual(P.periodTabName('2026-10-01', 20, 'Heesang Yun'), '0920-1019Y26 Heesang Yun');
assert.strictEqual(P.periodFolderName('2026-10-01', 20), '0920-1019 FY26');
assert.strictEqual(P.periodFolderName('2027-01-05', 20), '1220-0119 FY26');
assert.strictEqual(P.toMDY('2026-09-04'), '09-04-2026');
assert.strictEqual(P.buildDescription('2026-10-15', '폴바셋 종각역점'), '261015 폴바셋 종각역점');
assert.strictEqual(P.buildDescription('2026-10-15', ''), '261015 영수증');
assert.strictEqual(P.buildFileName('260908 SNM meeting/lunch', 'jpg'), '260908 SNM meeting lunch.jpg');

console.log('parse.test.js: all passed');
