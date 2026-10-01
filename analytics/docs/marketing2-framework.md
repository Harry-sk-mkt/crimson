# Marketing 2.0 Framework — 소스 문서 요약

`C:\Users\mrhar\Downloads\Marketing 2.0 Docs-20261001T082534Z-1-001\Marketing 2.0 Docs\`에서 받은 신규 운영 프레임워크 문서 세트를 콘텍스트화한 기록이다 (2026-10-01). 9월 성과 리뷰 + FY27 리뷰의 평가 기준이 되는 문서라 먼저 읽고 정리했다.

## 소스 파일

| 파일 | 내용 | 비고 |
|---|---|---|
| `0. Marketing 2.0 Master.docx` | 전체 통합본 (Background~Review Framework + Appendix A~J) | 가장 포괄적. 본문은 13.5M(after-tax), Appendix는 14.03M(부가세 적용 추정) 표기 — 13.5M이 기준 (아래 참고) |
| `1. Model Context.docx` | Master 1장과 거의 동일 내용의 더 정리된 버전 | 14.03M(부가세 적용 추정) 표기 |
| `2. Data Architecture.docx` | Master 2장과 동일 | ADR 번호(ADR-001~006) 부여된 버전 |
| `3. A Day in Marketing 2.0.docx` / `.pptx` | 팀원 입장에서 Weekly/Monthly/Quarterly 운영 흐름 | Master 3장과 동일 |
| `4. Program Framework.docx` | Program 정의, Brief 템플릿 | Master 4장과 동일 |
| `5. Segment Framework.docx` | Segment 정의, KPI, 전략 | Master 5장과 동일 |
| `6. Target Framework.docx` | Target Cascade, 배분 로직, P1 Value 공식 | Master 6장과 동일 |
| `7. Attribution Framework.docx` | FTA 규칙, Re-attribution | Master 7장과 동일 |
| `8. Performance Framework.docx` | 개인 성과 평가 공식 | Master 8장보다 더 구체적 — `Individual Contribution = Program P1 × Program P1 Value` 명시 |
| `Data Stream Revised.docx` | MTA Log / Master Lead Database 2-layer 설계, Salesforce Export 운영 절차 | Master에 없는 **별도 문서**. lead-tracker ACQ/New P1 설계와 거의 동일 개념 (아래 참고) |
| `TBD) Planning Framework.docx` | FY/Quarterly Planning 절차, Capacity Planning | Master에 없는 **별도 문서**, FY27 Planning 근거 |
| `Marketing 2.0 Worksheet.xlsx` | 숫자만 있는 작은 표 (Priority별 Revenue 등으로 추정) | 헤더 라벨 없음 — 해석 보류, 아래 참고 |
| `Intro slides/260707 Sales and marketing.pptx` | 텍스트 추출 안 됨(이미지/SmartArt 위주로 추정) | 미확인 |
| `Intro slides/260708 digital share.pptx` | Master 요약 슬라이드. 14.03M 표기 | |
| `Intro slides/3. A_Day_in_Marketing_2.0.pdf`, `Marketing_2.0_Blueprint.pdf` | PDF, 로컬에 pdftoppm(poppler) 없어 렌더링 못 함 | 필요시 poppler 설치 후 재확인 |

## 핵심 문제의식 (Why Marketing 2.0)

1. **Revenue 중심 평가의 한계**: Revenue는 Sales/상담품질/시장상황 영향을 받아 Marketing이 직접 통제 불가 → 캠페인 품질 평가 어려움.
2. **Source of Truth 분리**: Marketo(Log 기준, 재참여도 New Lead로 집계)와 Salesforce(최초 Lead 기준)의 New Lead 수가 다름. → Marketing 2.0은 지표별 SoT를 명시적으로 고정(아래 표).
3. **Program 단위 성과 추적 불가**: 기존엔 Registration/New Leads/Revenue 상위 퍼널만 봐서 "어떤 Webinar가 좋은 P1을 만들었는지" 등을 알 수 없었음.

## Source of Truth 매핑

| KPI | SoT |
|---|---|
| Registration | Marketo |
| New Leads | Marketo |
| P1 (NL P1) | Salesforce |
| IC Booked/Complete | Salesforce |
| Opportunity / Revenue | Salesforce |

## Program / Segment / Target 계층

- **Layer**: Company → Portfolio → Segment → Program → Campaign
- **Segment = Event / eBook / PTC / Others** (역할이 다름 → 동일 KPI로 평가 금지)
  - Event: Primary Demand Engine (Webinar+Seminar, 가장 안정적 Revenue)
  - eBook: Pipeline Builder (New Lead 최다, Long Nurturing, 평균 Deal Size 최대)
  - PTC(Search/Consult): Demand Capture (구매 Intent·Deal Rate 최고)
- **Program**: 하나의 Offer + 하나의 Landing Page + 하나의 Conversion Goal. Audience/Creative/Budget/Bid 변경은 Program이 아니라 Campaign Optimization.
- **Primary KPI by Layer**: Portfolio=Revenue/ROAS, Segment=P1, Program=P1, Campaign=P1/CPL. **Program은 Revenue를 KPI로 쓰지 않음.**
- **Program Ownership**: Program마다 Primary Owner 1명(성과 책임) + Secondary Owner(QA/운영 지원, 성과 책임 없음).

## Attribution (FTA)

- First Touch Attribution 기본: 최초 Lead를 만든 Program이 이후 전체 Revenue를 귀속받음.
- Re-attribution 규칙: Marketo Activity Log 기준 **최근 활동 후 6개월 이상 비활성**이면 다음 활동을 새 First Touch로 인정.
- Referral은 Portfolio Revenue엔 포함하되 Program/Segment 비교에서는 제외(별도 관리).
- Program 종료 ≠ Attribution 종료 (Lifetime Revenue 계속 귀속).

## Data Stream 설계 (`Data Stream Revised.docx`)

- 리드는 **Lead Attribute(P1 등)**와 **Sales Funnel(SAL→IC Request→IC Booked→IC Complete→Won)** 두 축을 동시에 가짐.
- 데이터는 2-layer: **MTA Log**(이메일 중복 가능, 터치포인트 전부 기록) + **Master Lead Database**(이메일 PK, 1행/리드, Sales Funnel 상태).
- 운영 루틴: Salesforce에서 All Leads/New Leads/SAL Report를 주기적으로 export → MTA Log/Master Lead DB 갱신, IC 이후는 수동 체크.
- Dashboard 2종: **Acquisition Summary**(월별, All Leads/New P1/Existing P1/P1 Rate) + **New P1 Pipeline**(Cohort, Lead Created Month 기준 장기 Conversion 추적).
- → **lead-tracker의 ACQReportDesign / NewP1ReportDesign과 개념이 거의 1:1 대응**으로 보인다. 실제 구현이 이 설계와 얼마나 일치하는지는 비교 안 함 (다음 분석 때 확인 필요).

## Planning Framework (`TBD) Planning Framework.docx`)

- 순서: Revenue Target → Portfolio Plan → Segment Plan → Program Plan → Campaign Plan.
- **Required P1이 Program 개수를 결정** (Revenue나 균등배분이 아님).
- Program Capacity Planning 예시: Webinar 48 / Seminar 15 / eBook 30 / PTC 3 (FY27, 예시로 보임 — 확정 수치인지 미확인).
- Resource Planning: Owner Capacity(담당 Program 수)를 Program 배정보다 먼저 확인.
- Budget 우선순위: Event > PTC > eBook > Others.

## FY26 Baseline

| KPI | FY26 |
|---|---|
| Revenue | NZD 10.79M |
| Deals | 143 |
| IC Complete | 371 |
| IC Booked | 575 |
| P1 | 2,272 |
| New Leads | 8,326 |

Segment: Event NL 2,878 / Deals 53 / Revenue 3.53M · eBook NL 3,927 / Deals 20 / Revenue 2.06M · PTC NL 262 / Deals 35 / Revenue 2.17M · Others NL 1,259 / Deals 28 / Revenue 1.19M.

Referral(FY27부터 별도 관리): Leads 54 / Deals 34 / Revenue 1.84M.

## FY27 Target — Revenue 숫자 3종 (2026-10-01 사용자 설명으로 정리)

| 표기 | 의미 (사용자) |
|---|---|
| **NZD 13.5M** | **After-tax target.** 실제 추적할 FY27 Revenue Target은 이 값. |
| **NZD 15M** | 매출총액 (세전/gross). |
| NZD 14.03M / 14M | 13.5M에 부가세(1.1배수)를 적용한 값으로 추정 — 사용자도 "일 것"이라는 추정이라 정확한 산출식은 미확정. |

- 산술 확인: 13.5 × 1.1 = 14.85, 13.5 ÷ 0.9 = 15.0 → "매출총액 15M"은 13.5M을 0.9로 나눈 값과 일치(10% 공제 구조로 보임). 14.03M은 13.5×1.1(14.85)과도, 13.5/0.9(15.0)와도 정확히 들어맞지 않아 **정확한 산출 근거는 아직 불명확** — 중요하지 않으면 넘어가고, 필요하면 원 작성자에게 확인.
- **앞으로 분석/리뷰에서는 13.5M을 FY27 Revenue Target(after-tax)으로 사용.** 15M(매출총액)은 별도 라벨로 구분, 14.03M은 특별한 지시 없으면 쓰지 않음.
- Appendix C의 역산 전환 테이블(Deals 186 / IC Complete 482 / IC Booked 748 / New Leads 10,824)은 Master 본문과 Appendix 모두 같은 값이라 Revenue 표기가 13.5M이든 14.03M이든 이 운영 캐스케이드 자체는 영향 없음 — 13.5M 기준으로 봐도 무방.
- P1은 "전환율 유지 역산값 3,021"과 "Segment 배분 합계 Operational Target 3,200"이 공존. **2026-10-01 사용자**: 둘 중 하나를 고르는 문제가 아니라, P1을 매주 관리하기 시작하면 실제 집계되는 P1과 설계 당시(FY26 Baseline 기준 역산) P1이 맞는지 대조해서 재산정해야 함. **지금 당장 할 일은 아니고 TODO로만 남김** (`TODO.md`).

### Segment별 FY27 P1 Target (일관됨, 불일치 없음)

| Segment | FY27 P1 |
|---|---|
| Event | 1,200 |
| eBook | 1,350 |
| PTC | 200 |
| Others | 450 |
| **Total** | **3,200** |

## KPI Value 공식

- `Current P1 Value = Current Cycle Revenue ÷ Current Cycle Generated P1`
- `Previous P1 Value = Previous Revenue ÷ Previous FY Generated P1` (Current/Previous 분리 계산)
- `Individual Contribution = Program P1 × Program P1 Value` (Primary Owner 기준, Secondary는 성과 산정 제외)
- `CPL = Spend ÷ P1` (이름은 CPL이지만 정의는 Cost per **P1**, Cost per Lead 아님 — Appendix Glossary 기준)
- `ROAS = Revenue ÷ Spend`

## Review Cadence (운영 캘린더)

| Cycle | Scope | 주요 KPI | 산출물 |
|---|---|---|---|
| Weekly (Growth Meeting) | Live Program | P1, CPL | Budget/Creative/Audience 조정, Pause/Scale |
| Monthly (Segment Business Review) | Segment 전체(Live+Off) | Segment P1, P1 Rate | Program Ranking, Resource 재배분 |
| Quarterly (QBR) | Portfolio | Revenue, ROAS | 투자 의사결정, 예산 계획 |
| Annual (FY Planning & Calibration) | Lifetime Program | Revenue Contribution, Program Asset Value | FY Planning, Target 설정 |

**9월 성과 리뷰는 이 중 Monthly(Segment Business Review) 레벨로 보인다** — Segment P1 / Program Ranking / Target Achievement가 중심 지표.

## Open Items (문서 자체에 명시된 미정 항목)

- P1 분류 정확도 지속 관리 Owner/프로세스 미정.
- Segment별 Off 판단 NLP1 3개월 이동평균 Threshold 미정 (FY27 운영 데이터 축적 후 확정 예정).
- 인수인계 시 트랙커 검수 체크리스트 미표준화.
- 복수 Segment/Program 겸임 시 기여도 가중치 기준 미정.

## 해석 보류 (내가 확인 못한 것)

- `Marketing 2.0 Worksheet.xlsx`: B~E열(4개 지표) × 10행 숫자 테이블. 마지막 행(B10~E10)이 817,810.06 / 2,169,030.38 / 77,376.96 / 572,268.35로 Master의 "New Lead Priority별 Revenue(SGD)" 표(Others/P1/P2/P3)와 정확히 일치 — **이 워크시트는 그 표의 원본 계산 시트로 보임**. 다만 헤더 셀(행1~2)에 텍스트가 없어 B~E 열이 어느 Priority에 대응하는지, A/G열 숫자(4~12)가 무엇인지는 확인 못함.
- `260707 Sales and marketing.pptx`: 텍스트 추출 결과 비어 있음(이미지/SmartArt 추정). 필요시 PowerPoint로 직접 열어 확인 필요.
- 두 PDF(`3. A_Day_in_Marketing_2.0.pdf`, `Marketing_2.0_Blueprint.pdf`): 로컬에 poppler 없어 페이지 렌더링 못 함 — 대응하는 docx/pptx 텍스트는 이미 추출됨.
- lead-tracker의 기존 `BusinessSegmentClassification.md`(333줄), `FYReportDesign.md`, `NewP1ReportDesign.md`(235줄), `FiscalCalendarRule.md`가 이 프레임워크와 Segment/FY/P1 정의를 공유하는 것으로 보이나, 실제 구현이 이 새 프레임워크와 일치하는지는 아직 대조 안 함.

## 다음 액션 제안

1. ~~FY27 Revenue Target 13.5M vs 14.03M~~ → 해결 (13.5M after-tax가 기준, 2026-10-01 사용자 확정). **P1 Operational Target(3,021 vs 3,200)은 TODO로 보류** — P1 Weekly 관리 시작 후 실제 집계와 설계 당시 수치 대조해서 재산정 (`TODO.md` 참고, 지금 하지 않음).
2. 9월 성과 리뷰의 정확한 범위(Segment Business Review 포맷을 따를지, 어떤 KPI를 볼지) 확인.
3. lead-tracker Master 시트가 이 Source of Truth 매핑(Registration/New Lead=Marketo, P1 이후=Salesforce)과 Attribution 규칙(FTA, 6개월 재귀속)을 실제로 반영하고 있는지 대조 — 9월 수치 신뢰도에 직결됨.
