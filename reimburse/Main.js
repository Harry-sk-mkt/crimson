/**
 * ==========================================================
 * reimburse
 * Drive 영수증 폴더 → OCR → 정산 주기 탭에 한 줄씩 기록 + 설명 입력 후 파일명 정리
 *
 * Responsibility
 * - runProcessReceipts(): 매일 트리거로 실행. 새 파일 기록 → 파일명 정리 순서.
 * - 파싱 로직은 Parse.js (Node 테스트 대상), 설정은 Config.js.
 *
 * Version
 * v1.7.0
 *
 * Change Log
 * v1.7.0 (2026-10-19)
 * - E열 영수증을 Drive 파일 스마트 칩으로 기록 (Sheets API chipRuns), 동기화 기록은 J열
 * v1.6.0 (2026-10-19)
 * - runReparseUndescribed(): C를 직접 고친 줄(C ≠ B)은 건너뜀
 * v1.5.0 (2026-10-19)
 * - A열이 Date로 저장되는 경우 처리(cellYmd) — 재파싱 때 B·C·파일명이 깨지던 버그 수정, A열 형식 mm-dd-yyyy
 * v1.4.0 (2026-10-19)
 * - 파서에 CONFIG.MERCHANT_ALIASES 전달
 * v1.3.0 (2026-10-19)
 * - B·C에 'YYMMDD 결제처' 초안 자동 입력 (사용자 기존 형식), 파일명을 항상 B + 확장자로 동기화
 * - runReparseUndescribed(): 대상 = 계정과목(G)이 빈 줄, B·C도 다시 채움
 * v1.2.0 (2026-10-19)
 * - runReparseUndescribed() 추가: 파싱 규칙 수정 후 B가 빈 줄의 C·D·F를 다시 채움 + OCR 원문 로그
 * v1.1.0 (2026-10-19)
 * - 기록한 영수증을 주기별 폴더(예: 1020-1119 FY26)로 이동, 없으면 생성
 * v1.0.0 (2026-10-19)
 * - 최초 구현
 * ==========================================================
 */

function runProcessReceipts() {
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(30000)) { console.log('다른 실행이 진행 중 — 건너뜀'); return; }
  try {
    var ss = SpreadsheetApp.openById(CONFIG.SHEET_ID);
    var added = recordNewReceipts(ss);
    var renamed = renameDescribedReceipts(ss);
    console.log('기록 ' + added + '건, 파일명 정리 ' + renamed + '건');
  } finally {
    lock.releaseLock();
  }
}

// 매일 CONFIG.DAILY_TRIGGER_HOUR시 실행 트리거 등록 (기존 것은 지우고 1개만 유지)
function runInstallDailyTrigger() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'runProcessReceipts') ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('runProcessReceipts').timeBased().everyDays(1).atHour(CONFIG.DAILY_TRIGGER_HOUR).create();
  console.log('트리거 등록: 매일 ' + CONFIG.DAILY_TRIGGER_HOUR + '시');
}

// 파싱 튜닝용: 폴더의 가장 최근 영수증 OCR 원문과 파싱 결과를 로그로 출력 (시트는 안 건드림)
function runDumpLatestOcr() {
  var files = receiptFiles(), latest = null;
  files.forEach(function (f) { if (!latest || f.getDateCreated() > latest.getDateCreated()) latest = f; });
  if (!latest) { console.log('영수증 파일 없음'); return; }
  var text = ocrText(latest);
  console.log(latest.getName() + '\n---\n' + text + '\n---\n' + JSON.stringify(parseReceiptText(text, CONFIG.CARD_MAP, CONFIG.MERCHANT_ALIASES)));
}

// 파싱 규칙을 고친 뒤 이미 기록된 줄에 다시 적용: 계정과목(G)이 비어 있고 C가 B와 같은(= 손대지 않은) 줄만
// OCR을 다시 해서 B·C·D·F를 덮어쓴다. 날짜(A)·탭은 그대로 둔다.
// 각 파일 OCR 원문을 로그로 남긴다.
function runReparseUndescribed() {
  var ss = SpreadsheetApp.openById(CONFIG.SHEET_ID), count = 0;
  ss.getSheets().forEach(function (sh) {
    var last = sh.getLastRow();
    if (last <= CONFIG.HEADER_ROW) return;
    var values = sh.getRange(CONFIG.HEADER_ROW + 1, 1, last - CONFIG.HEADER_ROW, CONFIG.HEADERS.length).getValues();
    values.forEach(function (v, i) {
      var fileId = v[CONFIG.COL.FILE_ID - 1];
      if (!fileId || String(v[CONFIG.COL.ACCOUNT - 1]).trim()) return;
      // 자동 초안은 C = B. 사용자가 C를 고친 줄은 다시 읽지 않는다 (2026-10-19 사용자 C 수정분 보호)
      if (String(v[CONFIG.COL.DETAIL - 1]) !== String(v[CONFIG.COL.DESC - 1])) return;
      var r = CONFIG.HEADER_ROW + 1 + i, file = DriveApp.getFileById(fileId);
      var text = '';
      try { text = ocrText(file); } catch (e) { console.log('OCR 실패: ' + file.getName() + ' — ' + e); }
      var p = parseReceiptText(text, CONFIG.CARD_MAP, CONFIG.MERCHANT_ALIASES);
      console.log(file.getName() + '\n---\n' + text + '\n---\n' + JSON.stringify(p));
      var desc = buildDescription(cellYmd(v[CONFIG.COL.DATE - 1]), p.merchant);
      sh.getRange(r, CONFIG.COL.DESC, 1, 2).setValues([[desc, desc]]);
      sh.getRange(r, CONFIG.COL.AMOUNT).setValue(p.amount === null ? '' : p.amount)
        .setBackground(p.amount === null ? CONFIG.MISSING_COLOR : null);
      sh.getRange(r, CONFIG.COL.CARD).setValue(p.card).setBackground(p.card ? null : CONFIG.MISSING_COLOR);
      count++;
    });
  });
  console.log('다시 읽은 줄 ' + count + '건, 파일명 정리 ' + renameDescribedReceipts(ss) + '건');
}

function receiptFiles() {
  var since = new Date(CONFIG.SINCE + 'T00:00:00+09:00');
  var it = DriveApp.getFolderById(CONFIG.FOLDER_ID).getFiles(), out = [];
  while (it.hasNext()) {
    var f = it.next(), mime = f.getMimeType();
    if ((mime.indexOf('image/') === 0 || mime === 'application/pdf') && f.getDateCreated() >= since) out.push(f);
  }
  return out;
}

// WHY: Drive가 이미지/PDF를 Google Docs로 변환할 때 OCR을 해준다 — 외부 API·키 없이 work 계정만으로 됨.
function ocrText(file) {
  var doc = Drive.Files.copy({ name: 'ocr-tmp ' + file.getName(), mimeType: MimeType.GOOGLE_DOCS },
    file.getId(), { ocrLanguage: CONFIG.OCR_LANGUAGE });
  try {
    return DocumentApp.openById(doc.id).getBody().getText();
  } finally {
    Drive.Files.remove(doc.id);
  }
}

function knownFileIds(ss) {
  var ids = {};
  ss.getSheets().forEach(function (sh) {
    var last = sh.getLastRow();
    if (last <= CONFIG.HEADER_ROW) return;
    sh.getRange(CONFIG.HEADER_ROW + 1, CONFIG.COL.FILE_ID, last - CONFIG.HEADER_ROW, 1).getValues()
      .forEach(function (r) { if (r[0]) ids[r[0]] = true; });
  });
  return ids;
}

function getOrCreateTab(ss, name) {
  var sh = ss.getSheetByName(name);
  if (sh) return sh;
  sh = ss.insertSheet(name, 0);
  sh.getRange(1, 1).setValue(name).setFontWeight('bold');
  sh.getRange(CONFIG.HEADER_ROW, 1, 1, CONFIG.HEADERS.length).setValues([CONFIG.HEADERS]).setFontWeight('bold');
  sh.getRange('A:A').setNumberFormat('mm-dd-yyyy');   // xlsx와 같은 표시 형식 (값은 Date로 저장됨 — cellYmd 참고)
  sh.getRange('D:D').setNumberFormat('#,##0');
  sh.setFrozenRows(CONFIG.HEADER_ROW);
  return sh;
}

function getOrCreatePeriodFolder(name) {
  var parent = DriveApp.getFolderById(CONFIG.PERIOD_PARENT_ID), it = parent.getFoldersByName(name);
  return it.hasNext() ? it.next() : parent.createFolder(name);
}

function recordNewReceipts(ss) {
  var known = knownFileIds(ss), tz = Session.getScriptTimeZone(), count = 0;
  receiptFiles().forEach(function (f) {
    if (known[f.getId()]) return;
    var text = '';
    try { text = ocrText(f); } catch (e) { console.log('OCR 실패: ' + f.getName() + ' — ' + e); }
    var p = parseReceiptText(text, CONFIG.CARD_MAP, CONFIG.MERCHANT_ALIASES);
    // 영수증에서 날짜를 못 읽으면 업로드 날짜로 대신하고 노란색 표시
    var ymd = p.date || Utilities.formatDate(f.getDateCreated(), tz, 'yyyy-MM-dd');
    var sh = getOrCreateTab(ss, periodTabName(ymd, CONFIG.PERIOD_START_DAY, CONFIG.NAME));
    var row = CONFIG.HEADERS.map(function () { return ''; });
    // B·C 초안 = 'YYMMDD 결제처' (기존 xlsx도 C는 대부분 B와 같다). 필요하면 B를 목적으로 고친다.
    var desc = buildDescription(ymd, p.merchant);
    row[CONFIG.COL.DATE - 1] = toMDY(ymd);
    row[CONFIG.COL.DESC - 1] = desc;
    row[CONFIG.COL.DETAIL - 1] = desc;
    row[CONFIG.COL.AMOUNT - 1] = p.amount === null ? '' : p.amount;
    row[CONFIG.COL.CARD - 1] = p.card;
    row[CONFIG.COL.LOCATION - 1] = CONFIG.LOCATION;
    row[CONFIG.COL.FILE_ID - 1] = f.getId();
    sh.appendRow(row);
    var r = sh.getLastRow();
    if (!p.date) sh.getRange(r, CONFIG.COL.DATE).setBackground(CONFIG.MISSING_COLOR);
    if (!p.merchant) sh.getRange(r, CONFIG.COL.DESC, 1, 2).setBackground(CONFIG.MISSING_COLOR);
    if (p.amount === null) sh.getRange(r, CONFIG.COL.AMOUNT).setBackground(CONFIG.MISSING_COLOR);
    if (!p.card) sh.getRange(r, CONFIG.COL.CARD).setBackground(CONFIG.MISSING_COLOR);
    // 기록 후 주기 폴더로 이동 → 받은편지함에는 미처리 파일만 남는다
    f.moveTo(getOrCreatePeriodFolder(periodFolderName(ymd, CONFIG.PERIOD_START_DAY)));
    known[f.getId()] = true;
    count++;
  });
  return count;
}

// A열 값 → 'YYYY-MM-DD'. WHY: Sheets가 'MM-DD-YYYY' 문자열을 Date로 자동 변환해 저장한다
// (2026-10-19 실측 — 문자열로만 처리하다 B·C·파일명이 'definedMon Sep 21…'로 깨짐). Date·문자열 둘 다 받는다.
function cellYmd(v) {
  if (v instanceof Date) return Utilities.formatDate(v, Session.getScriptTimeZone(), 'yyyy-MM-dd');
  var p = String(v).split('-');   // 'MM-DD-YYYY'
  if (p.length !== 3) throw new Error('A열 날짜 형식 아님: ' + v);
  return p[2] + '-' + p[0] + '-' + p[1];
}

function extOf(name) {
  var m = String(name).match(/\.([A-Za-z0-9]{2,5})$/);
  return m ? m[1].toLowerCase() : '';
}

// 파일명을 항상 'B열.확장자'로 맞추고 E열에 Drive 파일 칩으로 넣는다 (사용자 요청: 링크는 칩 형태).
// J열(CHIP_NAME)이 원하는 파일명과 같으면 이미 끝난 줄 → Drive 호출 없이 건너뜀. B를 고치면 다시 처리된다.
function renameDescribedReceipts(ss) {
  var count = 0, requests = [];
  ss.getSheets().forEach(function (sh) {
    var last = sh.getLastRow();
    if (last <= CONFIG.HEADER_ROW) return;
    var headerCell = sh.getRange(CONFIG.HEADER_ROW, CONFIG.COL.CHIP_NAME);   // 예전 탭엔 J 헤더가 없음
    if (!headerCell.getValue()) headerCell.setValue(CONFIG.HEADERS[CONFIG.COL.CHIP_NAME - 1]).setFontWeight('bold');
    var range = sh.getRange(CONFIG.HEADER_ROW + 1, 1, last - CONFIG.HEADER_ROW, CONFIG.HEADERS.length);
    range.getValues().forEach(function (v, i) {
      var desc = String(v[CONFIG.COL.DESC - 1]).trim(), fileId = v[CONFIG.COL.FILE_ID - 1];
      var synced = String(v[CONFIG.COL.CHIP_NAME - 1]);
      if (!desc || !fileId) return;
      if (synced && synced === buildFileName(desc, extOf(synced))) return;
      var file = DriveApp.getFileById(fileId);
      var name = buildFileName(desc, extOf(file.getName()));
      if (file.getName() !== name) file.setName(name);
      var r = CONFIG.HEADER_ROW + 1 + i;
      requests.push(fileChipRequest(sh.getSheetId(), r, CONFIG.COL.RECEIPT, file.getUrl()));
      sh.getRange(r, CONFIG.COL.CHIP_NAME).setValue(name);
      count++;
    });
  });
  if (requests.length) Sheets.Spreadsheets.batchUpdate({ requests: requests }, ss.getId());
  return count;
}

// WHY: SpreadsheetApp엔 스마트 칩 쓰기가 없다. Sheets API는 문자열의 '@' 자리를 chipRuns로 칩으로 바꾼다.
// 칩은 Drive 파일 제목을 그대로 보여주므로 파일명(= B.확장자)이 곧 E열 표시값이 된다.
function fileChipRequest(sheetId, row, col, url) {
  return {
    updateCells: {
      range: { sheetId: sheetId, startRowIndex: row - 1, endRowIndex: row, startColumnIndex: col - 1, endColumnIndex: col },
      rows: [{ values: [{ userEnteredValue: { stringValue: '@' }, chipRuns: [{ startIndex: 0, chip: { richLinkProperties: { uri: url } } }] }] }],
      fields: 'userEnteredValue,chipRuns'
    }
  };
}
