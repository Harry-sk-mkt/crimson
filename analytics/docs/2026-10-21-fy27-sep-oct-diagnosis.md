# FY27 9–10월 퍼포먼스 진단 (2026-10-21)

- ⚠️ 2026-10-21 정정: 표 출처는 ACQ_REP이 아니라 NewP1_REP(New P1 코호트 기준, Revenue는 딜 Created Date 기준)이다. 아래 정의·해석(특히 "코호트 아님", H2)은 다시 작성해야 한다 — `background.md` 참고.
- 입력: 사용자 제공 `Crimson_Korea_FY27_Performance_Analysis_Context.md`(Downloads, 저장소 밖). FY26·FY27 8–10월 세그먼트별 42행.
- 검산 스크립트: 세션 scratchpad `fy27_check.py`(문서 표 파싱 → 재합산·비율·YoY·채널 증감·New P1 볼륨/비율 분해).
- 사실(표·문서로 확인)과 가설을 나눠 적는다. 목표값은 받지 못해 달성률은 만들지 않았다.

## 경영진 요약

- 확인된 사실 (8+9월 합산, 10월 제외)
  - New P1 322 → 541 (+68%)
  - SAL(BOFU 제외) 184 → 125 (−32%)
  - IC Complete 88 → 46 (−48%)
  - Revenue 2.55M → 2.41M (−5%). Referral 제외하면 1.82M → 2.15M (+18%)
  - 9월 Revenue 감소 −872k 중 −562k(64%)가 Referral (561.8k → 0)
- 해석: 줄어든 곳은 마케팅 유입(New P1)이 아니라 P1 이후 단계(SAL, 상담 완료)다. 다만 원인이 리드 의도 품질인지, 세일즈 처리인지, 데이터 수집인지는 아직 구분되지 않는다.
- 다음 행동
  1. Salesforce에서 9월 IC Completed 건수 직접 확인 (하루, 9건이 실제인지)
  2. 8–9월 리드 코호트의 생성 후 21일 내 SAL·IC Booked 도달률 FY26 대비 비교
  3. FY27 월별 목표값 수령

## 1. 검산

- 42행 재합산. 문서 6절 합계 중 1건 오류: **FY27 9월 All P1은 914가 아니라 921**(51+453+40+28+313+7+29). YoY +25.2% → +26.2%.
- 나머지 합계와 증감률은 일치.
- 비율 126개 재계산: All P1% = All P1 / All Leads, New Leads% = New Leads / All Leads, New P1% = New P1 / New Leads로 모두 일치. 반올림 차이 1건(FY27 8월 Seminar 18/32 = 56.25%).

## 지표 정의 — lead-tracker 문서로 확인됨

표 구조가 lead-tracker `ACQ_REP`과 같다. 정의는 `lead-tracker/docs/ACQReportDesign.md`(2026-07-22 이후. FY26도 같은 코드로 다시 계산됨).

| 지표 | 귀속 월 | 세그먼트 기준 |
|---|---|---|
| All Leads / All P1 | MTA 터치 생성일 (리드 수가 아니라 터치 수) | 터치별 캠페인 |
| New Leads / New P1 | 리드 생성일 | 리드 first touch |
| SAL | Sales Accepted Date | `SAL Segment`(SAL 이벤트 터치 기준 — 처음에 first touch로 잘못 적었다가 코드 확인 후 정정) |
| IC Booked / IC Complete | 각 날짜 (활동 발생 월) | 리드 first touch |
| Revenue | Deal Tracker Close Date | 딜의 수동 Segment 칸 (Upsell은 Other) |

- SAL, IC, Revenue 모두 활동 발생 월 기준이고 코호트가 아니다. 따라서 같은 행의 New P1 → SAL → IC 비율은 전환율이 아니다.
- All Leads는 터치 수라 유입량 비교에서 뺐다.
- 남은 확인
  - Revenue의 Close Date가 계약일인지 매출 인식일인지 (Deal Tracker 입력 기준)
  - FY27 목표에 Referral·Upsell이 포함되는지
- 데이터 품질 주의 (문서 기록)
  - IC Booked/Complete는 사용자가 Salesforce에서 따로 내보내는 IC Funnel 리포트를 Import해야 갱신된다(2026-08-26~). 마지막 Import 이후 완료분은 빠진다. 2026-08에 같은 구조로 ACQ_REP IC Complete 7 vs Salesforce 21 사례가 있었다.
  - SAL에서 Lead Status = Nurturing 제외 조건은 아직 미구현. 두 해 같은 로직이라 수준에는 영향, YoY에는 영향이 작다.
  - 병합된 Salesforce 리드: 옛 Lead ID에 SAL 12·IC 9건이 아직 안 붙어 있다(10-20 확인). 감소폭(−45, −34)을 설명하기엔 작다.

## 2. 전체 비교 (FY26 → FY27)

10월은 기준일 미확정이라 부분 월이다. YoY로 해석하지 않는다.

| 지표 | 8월 | 9월 | 10월 (부분) | 8+9월 |
|---|---|---|---|---|
| New Leads | 742 → 876 (+18%) | 711 → 597 (−16%) | 551 → 322 | 1,453 → 1,473 (+1%) |
| New P1 | 173 → 324 (+87%) | 149 → 217 (+46%) | 119 → 113 | 322 → 541 (+68%) |
| New P1 % | 23.3% → 37.0% | 21.0% → 36.3% | 21.6% → 35.1% | 22.2% → 36.7% |
| SAL | 133 → 268 (+102%) | 141 → 96 (−32%) | 126 → 76 | 274 → 364 (+33%) |
| SAL (BOFU 제외) | 92 → 83 (−10%) | 92 → 42 (−54%) | 74 → 43 | 184 → 125 (−32%) |
| IC Booked | 56 → 54 (−4%) | 57 → 45 (−21%) | 46 → 21 | 113 → 99 (−12%) |
| IC Complete | 45 → 37 (−18%) | 43 → 9 (−79%) | 39 → 11 | 88 → 46 (−48%) |
| Revenue | 0.94M → 1.67M (+79%) | 1.61M → 0.74M (−54%) | 1.05M → 0.35M | 2.55M → 2.41M (−5%) |
| Revenue (Referral 제외) | 0.77M → 1.41M (+83%) | 1.05M → 0.74M (−30%) | 0.77M → 0.18M | 1.82M → 2.15M (+18%) |

- 10월 민감도(참고용, 결론에 쓰지 않음): 표가 10/20까지라고 가정하고 31/20로 단순 환산하면 New Leads −9%, New P1 +47%, SAL −7%, IC Booked −29%, IC Complete −56%. IC는 시차가 있어 선형 환산이 맞지 않는다.
- 8·9월 New P1과 10월 Search New P1(4)이 10/21 `TEMPQA_079` ACQ_Summary 덤프(10월 1~20일분)와 같다. 그래서 이 표도 10/20 전후 추출일 가능성이 있다. 확인 필요.

## 3. 채널별 변화와 기여도 (8+9월 합산)

| 채널 | New Leads | New P1 | SAL | IC Booked | IC Complete | Revenue |
|---|---|---|---|---|---|---|
| Seminar | 103 → 28 (−75) | 54 → 11 (−43) | 21 → 4 (−17) | 17 → 12 (−5) | 15 → 6 (−9) | 414k → 429k (+15k) |
| Webinar | 471 → 418 (−53) | 143 → 209 (+66) | 94 → 45 (−49) | 39 → 32 (−7) | 30 → 15 (−15) | 539k → 757k (+218k) |
| BOFU | 80 → 221 (+141) | 17 → 28 (+11) | 90 → 239 (+149) | 4 → 7 (+3) | 2 → 2 (0) | 0 → 131k (+131k) |
| Search | 75 → 70 (−5) | 27 → 29 (+2) | 29 → 37 (+8) | 18 → 24 (+6) | 11 → 8 (−3) | 213k → 440k (+226k) |
| Content | 696 → 712 (+16) | 73 → 249 (+176) | 33 → 27 (−6) | 20 → 15 (−5) | 16 → 8 (−8) | 453k → 221k (−232k) |
| Referral | 12 → 10 (−2) | 3 → 7 (+4) | 0 → 0 | 13 → 6 (−7) | 11 → 6 (−5) | 725k → 256k (−469k) |
| Other | 16 → 14 (−2) | 5 → 8 (+3) | 7 → 12 (+5) | 2 → 3 (+1) | 3 → 1 (−2) | 201k → 175k (−26k) |
| **합계** | +20 | +219 | +90 | −14 | −42 | −136k |

- New P1 +219 중 Content가 +176(80%), Webinar가 +66을 차지한다. Seminar는 −43(세미나 캠페인 미런칭, `analytics/docs/background.md`).
- Content의 New P1 증가는 리드 수가 아니라 P1 비율에서 나왔다. 볼륨/비율로 분해하면 8월 +112 중 +102, 9월 +64 중 +71이 비율 효과다(Content New P1 %: 11.6% → 35.9%, 9.5% → 33.7%).
- 비BOFU SAL −59 중 Webinar가 −49(83%)다. Webinar는 New P1 +66인데 SAL은 −49로 반대 방향이다.
- IC Complete −42: Webinar −15, Seminar −9, Content −8, Referral −5.
- BOFU는 SAL이 90 → 239로 늘었지만 IC Booked는 4 → 7이다. 두 해 모두 BOFU SAL은 거의 상담으로 이어지지 않는다. 전체 SAL이 BOFU 때문에 부풀려지므로 SAL은 BOFU를 빼고 본다.
- Revenue: Referral −469k가 전체 감소 −136k보다 크다. 비Referral은 +333k. Content −232k는 FY26 9월 452k 한 달에 몰려 있어 일회성 여부를 확인해야 한다.
- 10월(부분)
  - Content New Leads 308 → 155(−153)는 전체 −229의 67%다.
  - Search New Leads 27 → 7, New P1 12 → 4. 네이버 결제 중단 약 10일이 있었다(10/17께 카드 변경 후 재개, 10/21 Digital Weekly).

## 4. 월별 집계와 코호트 전환 구분

- 이 표로 말할 수 있는 것: 그 달에 몇 건이 생성·수락·예약·완료·계약됐나.
- 말할 수 없는 것: 9월 New P1 217명 중 몇 명이 SAL이나 IC가 됐나. 9월 SAL 96건에는 이전 달 리드와 수년 전 리드가 섞여 있다. 예를 들어 FY27 8월 Seminar는 New Leads 0인데 IC Booked 7, Revenue 344k다.
- 그래서 New P1 대비 SAL 같은 비율은 만들지 않았다.
- 코호트로 볼 때는 관찰 기간을 맞춘다. 10/21 기준 9/30 생성 리드는 21일밖에 안 지났다. FY26·FY27 모두 "생성 후 21일 내" 도달률로 맞추고, 8월 코호트는 60일까지 본다.
- 월별 집계로도 쓸 수 있는 신호: 2개월 합산은 월 경계 시차를 일부 흡수한다. 합산해도 비BOFU SAL −32%, IC Complete −48%라 월 경계 이동만으로는 설명이 어렵다(해석).

## 5. 원인 가설 3개 (단정하지 않음, 동시에 참일 수 있음)

### H1. P1 이후 수락(SAL) 단계 손실 — 리드 의도 품질 또는 세일즈 처리

- 관찰: 8+9월 비BOFU New P1 305 → 513(+68%), 비BOFU SAL 184 → 125(−32%). Webinar New P1 +66 / SAL −49, Content New P1 +176 / SAL −6.
- 증거 수준: 중간. 월별 집계라 코호트 전환은 아직 확인하지 않았다.
- 하위 가설
  - (a) P1 판정은 늘었지만 상담 의도가 약한 리드다. Content P1 비율이 3배가 됐는데, 타깃팅 변화(hyperlocal ebook 등) 때문인지 P1 판정 기준 변화 때문인지 모른다 → 마케팅 쪽.
  - (b) 세일즈 연락·수락 처리가 늘어난 P1을 못 따라갔다 → 세일즈 쪽.
  - (c) SAL 정의나 프로세스가 바뀌었다.
- 반증 조건
  - 21일 코호트 SAL률이 FY26와 비슷하면 H1을 기각한다(월 시차 문제).
  - 첫 연락 시간·연락 시도율은 FY26 수준인데 응답률만 낮으면 (a)다.
  - 미연락 비율이 높으면 (b)다.
- 필요 데이터: 리드 단위 생성일, Priority, Sales Accepted Date, 첫 연락 활동 일시, 연락 횟수, Owner, Lead Status. FY27 P1 판정 기준의 변경 이력.
- 의사결정 영향: (a)면 Content/Webinar 증액·cap을 New P1이 아니라 SAL·IC 기준으로 다시 평가한다. (b)면 세일즈 배정과 SLA를 고친다.

### H2. IC Complete 급감(9월 43 → 9) — 실제 상담 완료 감소 또는 데이터 수집 누락

- 관찰: 9월 IC Booked는 −21%인데 Complete는 −79%다. 9월 Search는 Booked 12 / Complete 0, Seminar는 Complete 0.
- 증거 수준: 낮음~중간. 실제 감소인지부터 확인되지 않았다.
- 데이터 쪽 근거
  - IC Complete는 수동 IC Funnel Import에 의존한다.
  - 2026-08에 같은 구조로 과소집계된 사례가 있다(7 vs 21).
  - export 필드명이 "IC Completed Date (Pre-Conversion)"이다. 전환된 리드에서도 값이 유지되는지 확인해야 한다(확인 항목, 추정 아님).
- 운영 쪽 가능성: 노쇼·취소 증가, 예약 후 완료가 10월 이후로 밀림, 상담 인력 변화.
- 반증 조건
  - Salesforce에서 IC Completed Date가 2026-09인 리드 수가 9건 근처면 데이터 문제를 기각하고 운영 문제로 본다.
  - 크게 많으면 수집 문제다. 이 경우 진단 표 숫자부터 다시 만든다.
- 필요 데이터: Salesforce IC 리포트(Booked/Completed Date, 상태, 담당자), 마지막 IC Funnel Import 일시.
- 의사결정 영향: 하루면 확인되고, 결과에 따라 "상담 단계가 무너졌다"는 메시지 자체가 바뀐다 → 최우선.
- **업데이트 (2026-10-21, 사용자 Salesforce 확인)**
  - 9월 IC Complete는 Salesforce 전체 33건, P1만 9건이다. 표의 9는 P1 수와 같다.
  - 하지만 ACQ_REP 코드는 IC Complete를 Priority 필터 없이 센다. 그래서 왜 9가 나왔는지는 아직 설명되지 않는다. 표가 33 중 24건을 놓쳤거나 다른 기준으로 추출됐다.
  - 전체 기준(33)으로 보면 FY26 9월 43 → 33(−23%)이다. 단, FY26 43이 같은 기준인지는 미확인이다. "−79%"는 기준이 섞인 수치일 수 있어 경영진 보고에 쓰지 않는다.
  - P1 기준으로는 9건(27%)뿐이다. New P1이 68% 늘었는데 P1 상담 완료가 적다는 점은 H1(P1 이후 단계 손실)과 같은 방향이다.
  - 다음: Salesforce 33건 Lead ID 목록과 Leads_OPS를 대조한다(빠진 24건이 Leads_OPS에 없는지, 날짜가 비었는지). FY26 9월도 Salesforce 전체·P1 수를 같은 방식으로 뽑는다.

### H3. 매출 감소는 Referral 공백과 과거 파이프라인 소진의 시차이며, 9–10월 상담 감소가 11월 이후 매출 위험으로 이어짐

- 관찰
  - 8+9월 Revenue −136k 중 Referral이 −469k, Referral 제외 +333k(+18%).
  - 10월(부분) −706k: Search −223k, Webinar −159k, Referral −126k, Seminar −120k.
  - 10/21 Digital Weekly 본사 발언: 10월 목표 800k에 파이프라인 예정 딜 없음(목표 기준 미확인).
- 증거 수준: Referral 비중은 표로 확인된 사실이다. 시차라는 원인은 가설이다.
- 반증 조건
  - Deal 건수는 비슷한데 평균 계약금액만 떨어졌으면 시차가 아니라 단가·상품 믹스 문제다.
  - Close된 딜의 리드 생성일이 대부분 FY27이면 시차 가설이 약해진다.
- 필요 데이터: Deal Tracker의 Close Date, Amount, Segment, Referral/Upsell 구분, 딜 리드의 생성일. open pipeline 단계와 예상 Close Date.
- 의사결정 영향: Referral을 목표·리포트에서 분리할지 정하고, 11–12월 매출을 예측한다.

## 6. Salesforce 추출 필드와 보고서 설계

필드(라벨 기준. "확인"은 필드 존재 여부를 확인해야 하는 것)

| 객체 | 필드 |
|---|---|
| Lead | Lead ID, Create Date, Lead Priority, Lead Status, Lead Owner, First MKT UTM Campaign, Sales Accepted Date, IC Booked Date, IC Completed Date (Pre-Conversion), Sales Funnel Stage, Converted Date(확인), 미전환·Disqualify 사유(확인), 학교·학년(P1 판정 근거) |
| Activity (Task/Event) | 관련 Lead ID, 생성 일시, 유형(전화/메시지), 결과 — 연결/미응답(확인), 담당자 |
| IC | 예약 일시, 상담 일시, 상태 — 완료/노쇼/취소/재예약(어디에 기록되는지 확인), 상담 담당자 |
| Opportunity | Opportunity ID, Lead/Contact ID, Created Date, Close Date, Stage, Amount, Lost Reason, Referral/Upsell 구분 |

보고서 4개

- **R1 코호트 퍼널**
  - 대상: Lead Create Date 2025-08-01~10-31, 2026-08-01~10-20. 리드 한 줄당 한 행.
  - 컬럼: Priority, First MKT UTM Campaign, Sales Accepted Date, IC Booked/Completed, Won.
  - 산출: 생성 후 7/14/21일(9월 코호트 최대), 30/60일(8월 코호트) 안에 SAL·IC Booked·IC Complete에 도달한 비율. FY별·세그먼트별.
- **R2 SAL 처리**
  - 대상: R1의 P1 리드.
  - 추가 컬럼: 첫 활동 일시, 활동 수, Owner, Lead Status.
  - 산출: 첫 연락까지 시간 중앙값, 미연락 비율, 담당자별 리드 수.
- **R3 IC 활동**
  - 대상: IC Booked Date 또는 IC Completed Date가 2025·2026년 8–10월인 리드. 상태 포함.
  - 산출: ACQ_REP IC 값 대사, 예약→완료 소요일, 노쇼율.
- **R4 딜·파이프라인**
  - 대상: Close Date가 2025·2026년 8–10월인 Won 딜과 현재 open opportunity.
  - 컬럼: Amount, Segment, Referral/Upsell 구분, 리드 생성일.
  - 산출: 딜 수, 평균 금액, 리드 생성 FY별 매출 분해, 11–12월 예상 Close.
- R1~R3는 lead-tracker에 이미 있는 IC Funnel·SAL export에 컬럼만 추가하면 되는지 먼저 확인한다(analytics는 lead-tracker 데이터를 다시 구현하지 않음).

## 7. 10영업일 계획 (10/22 목 ~ 11/4 수)

본사 담당자가 10/29~11/3 부재다(10/21 Digital Weekly).

마케팅

| 일정 | 할 일 | 산출 |
|---|---|---|
| D1 (10/22) | 표 추출일, 마지막 IC Funnel·SAL Import 일시 확인. Salesforce 9월 IC Completed 건수 대사. 목표값 요청 | H2 데이터 문제 여부 |
| D2–3 | R1: 21일 창 SAL·IC Booked 도달률, FY26 vs FY27, Content·Webinar 우선 | H1 기각/유지 |
| D4–5 | Content P1 비율 상승을 캠페인별로 분해. 21일 SAL률이 낮은 캠페인 목록 | (a) 검증 |
| D6–8 | 결과가 (a)면 증액·cap 판단에 SAL률 조건 추가(10/21 증액 결정과 연결). Seminar 캠페인(10/21 런칭)·네이버 학습 회복 모니터링 | 예산 규칙 초안 |
| D9–10 | 주간 리포트에 21일 코호트 SAL·IC 지표 추가 제안(lead-tracker NewP1_REP 활용 검토). 경영진 보고 | 보고서 |

세일즈 (마케팅이 요청하고 담당자는 세일즈가 지정)

| 일정 | 할 일 | 산출 |
|---|---|---|
| D1–2 | SAL 운영 정의와 FY27 변경점(배정 규칙, 자동 SAL, Nurturing 처리, 인력) 공유 | H1 (c) 확인 |
| D2–4 | 8–9월 P1 리드 첫 연락 시간·미연락 비율, 담당자별 배정량(R2) | H1 (b) 확인 |
| D3–5 | 9월 IC Booked 45건 상태(완료/노쇼/취소/재예약) | H2 운영 쪽 확인 |
| D5–7 | 9–10월 상담 완료 건의 미계약 사유, open pipeline 11–12월 예상 Close | H3 |
| D8–10 | 검증된 병목 1–2개만 개선 시작(예: P1 첫 연락 SLA, 노쇼 리마인드). 기준값은 FY26 같은 창 코호트 값 | 주간 모니터링 |

공동 리뷰(D10) 지표: 21일 SAL률, 예약→완료율, 딜 수, 매출(Referral 분리).

## 8. 지금 확인할 질문 (중요도 순)

1. Salesforce에서 IC Completed Date가 2026년 9월인 리드는 몇 건인가? IC Funnel·SAL export를 마지막으로 Import한 날짜는?
2. 이 표의 추출 시점(10월은 며칠까지)은? ACQ_REP에서 뽑았다면 마지막 Import 일시는?
3. FY27 월별 목표(Revenue, New P1, 가능하면 SAL·IC)와 Referral·Upsell 포함 여부는? ACQ_REP AH–AK 열 Target 값을 써도 되는가?
4. FY27에 P1 판정 기준(학교 리스트 등)이나 SAL 운영 규칙(배정, 자동 SAL, Nurturing, 인력)이 바뀌었나?
5. FY26/FY27 8–10월 Deal 건수, 평균 계약금액, 현재 open pipeline의 예상 Close는? Deal Tracker로 뽑을 수 있나?
