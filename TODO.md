# Global TODO

<!-- Add items here. Format: - [ ] task (project/context) -->
- [x] HS to DS disclaimer 공유 (2026-09-30)
- [ ] 맥 세팅 시 `crimson/scripts/setup-claude-md.sh` 실행해서 `~/.claude/CLAUDE.md` 생성 (crimson)
- [x] 사무실 PC에서 `~/.claude/CLAUDE.md` 기존 내용 확인 — 비어있으면 `setup-claude-md.ps1` 실행, 다른 내용 있으면 crimson 포인터 한 줄만 수동 추가 (crimson)
- [x] 운전면허 갱신 신청 (2026-09-30 완료)
- [x] 2026-10-31 로컬라이즈 프로젝트 FU — 학교 rigor & 학교별 합격률 (2026-10-12 사용자 계산 완료)
- [ ] Marketing 2.0 P1 타겟(3,021 역산 vs 3,200 Segment 배분) 조정 — P1 Weekly 관리 시작 후 실제 집계 P1과 설계 당시 P1(FY26 Baseline 2,272 등)을 대조해서 재산정. 지금 당장은 아님 (analytics, 2026-10-01)
- [x] 2026-10-08(목) 발표 준비 (2026-10-06 사용자 보고: 10-06(화) → 10-08(목)로 연기, 2026-10-12 사용자 완료 확인) — 내일(2026-10-02) 오전부터 시작. 구성: Funnel / Revenue by Segment / Webinar Stats / IC 구성(P1·P2·P3 비중, Complete·Deal도 동일 비중 breakdown). 핵심 검증 포인트: Marketing 2.0 논리("New P1이 늘어야 Revenue가 는다")가 실제 데이터로 맞는지 확인. 2025·2026 8/9/10월 퍼널·이벤트 데이터 정리본 사용 (analytics, 2026-10-01)
- [x] (10-01) 아이디에이션 09-30 누락 구간 ~09:30~11:30(c01 조각: %TEMP% 아래 v1033_chunks/c01_570.wav) 1분 단위 재전사 후 `meetings/ideation/2026-09-30.md` 보강 — 나머지는 10-01 완료(로컬 md, HS & CAO·Creative Quality bar·수요일 웨비나 미참석자 페이지 인용 보강) (meetings)
- [x] (10-01 오후) 아이디에이션 "수요일 웨비나 미참석자 → 다시 초대" FU — 발표자와 가설 발송 수단 이메일→메시지 수정, 9/2·9/8·9/16 이벤트 안내 메시지 오픈율 확인 (Notion 페이지 3️⃣ 가설 아래 체크박스) https://app.notion.com/p/3b464dfd498f80d98969e2f08f1ca5b6
- [x] (10-01 재부팅 후) Digital Weekly 09-30 화자 구분 재전사 — 10-01 완료(vibe-server HTTP API, 결과 `%TEMP%\dw0930_diar.json`). 이름 매핑은 사용자 판단으로 보류 (meetings)
- [x] (10-01) office PC Vibe 정리 (10-12 종결) — ✅ GPU 해결(드라이버 617.14, `--gpu-device 0 --threads 6`, 2분 42초, meetings/CLAUDE.md 기록). ✅ 저장 위치(10-12): 문서 폴더가 OneDrive로 리디렉션된 것뿐, 정상 저장. 남은 것: 1분 튕김 원인(10-12: 정지 26초 뒤 11:01:16에 앱에서 모델 복사본이 생성됨 → 사용자가 앱 설정을 만지던 중 녹음이 멈췄을 가능성, 사용자 기억 확인 대기), 중복 모델 1.5GB 정리 여부 — 이하 원래 메모: NVIDIA GPU 미인식(Intel UHD만, 1분 전사 ≈ 80초) 드라이버 확인 — 10-01 확인: GTX 1660 Ti Max-Q, 드라이버 442.94(2020년)로 매우 구버전 → 최신 드라이버 설치(관리자 권한, 사용자) 후 `--gpu-device` 지정 테스트. CPU는 i7-10750H 6코어라 `--threads 6`으로 올릴 것, 녹음이 Documents로 저장 안 된 원인, 11:00 60초 녹음 정체(→ 10-01 사용자 확인: Digital Weekly 시작 녹음이 1분 만에 튕긴 것, 11:02:58 재시작 — 튕긴 원인은 미확인), 결과를 `meetings/CLAUDE.md`에 기록 (meetings)
- [x] (10-01) 스쿨 타임라인용 웨비나 캘린더 제작하기 — 10-19 완료: 원본 Google Sheet `12 Month Marketing Execution Plan SK`의 `Topic Timeline` 탭(사용자 재정리)이 최종본, 규칙 점검 통과. 분류 규칙은 `event/webinar-calendar/build.py` CATS (event)
- [ ] (10-19) FY27 탭을 Topic Timeline 탭에 맞추기 — 사용자 직접 진행 (event)
- [x] (10-01) Quality Bar 템플릿 7개 dbTodos 등록 (사용자 완료)
- [x] (10-01) 수요일 웨비나 미참석자 재초대 FU (사용자 완료)
- [x] (10-12) office PC Vibe — 중복 모델 삭제, `model.path`를 원본으로 변경, 녹음 단축키 끔(회의 감지는 유지). 1분 튕김 원인은 미확정으로 종결: 재발하면 Vibe를 재시작하기 전에 당일 로그 확인 (meetings)
- [x] (10-12 사용자 확인: 백업 시트 생성됨, 숨김 처리) Events_OPS Manual 백업 생성 확인 — 실행 중인 tail이 끝난 뒤 `EVENTS_007_ManualBackup.js`의 `runPreviewRestoreEventsManualFromBackup()` 실행. "복원할 빈칸 없음"이면 완료, "백업 없음"이면 `runAcceptEventsManualAsBackup()` 실행. 다음 자동 실행이 메일 권한 오류로 실패하지 않는지도 확인 (lead-tracker)
- [x] (10-13 아침) 10-07 버전 복원으로 Master에서 빠진 Leads 61행·MTA 143행+ 복구 — 실행 중인 파이프라인 없는지 확인 후 순서대로: `MASTER_004_MasterBuild.js` `rebuildLeadsMaster()` → `rebuildMTAMaster()` → `MASTER_002_PipelineAsync.js` `runLeadsPipelineTail()` → `runMTAPipelineTail()` → `TEMPQA_071_MasterRawGapAfterRestore.js` `runDiagnoseMasterRawGapAfterRestore()`로 "누락 없음" 확인 (lead-tracker) — 2026-10-13 완료(LEADS·MTA 누락 없음)
- [ ] lead-tracker 그림자 diff 확대 원인 확인 (10-13 복구 후 Target 72건·FY_REP 677건, 실제 출력 영향 없음 / 10-16 16:55 Target 75건·FY_REP 691건, 예: FY27 OCT Content newLeads full 111 vs incremental 23)
- [ ] lead-tracker `rebuildMTAMaster()` 26분(30분 한도 근접) — 중복 삭제를 시트 행 삭제 대신 메모리 처리로 단축 검토 (코드 수정, 승인 필요)
- [x] (10-15 종결: 현재 구조·3627 유지, 사용자 확정) (10-14) lead-tracker Target 재산출 시뮬레이션 실행 — `TEMPQA_072_TargetRecalcSimulation.js` `runSimulateTargetRecalc()` 로그 검토: [1] FY26 재계산이 현재 목표와 일치하는지 먼저 확인 → 12개월 기준 세그먼트 목표·3627 현실성·CPNP1 비교 후 Target_Engine 반영 여부 결정
- [ ] (10-12) office PC Vibe — 다음에 앱을 열 때 모델이 정상 선택돼 있는지, 녹음·전사가 되는지 확인 (meetings)
- [x] (10-15 사용자 완료) (10-14) Amanda Margareth(Delta) 답장 — 1월 Expo 세부 정보 문의 + Delta 대표자 참석이 필요하면 지금부터 준비하겠다는 메시지(10-14 5:50 PM). Expo 일정·Delta 참석 필요 여부 정리해서 회신 (event)
- [x] (10-15 완료: `event/2026-10-14.md` + Notion "본 웨비나" 섹션) (10-15) 10-14 저녁 웨비나 녹음 전사 — Vibe 녹음 폴더(`OneDrive\Documents\Vibe\`) 확인, 앱이 꺼졌으면 `%TEMP%\vibe_temp_2026-10-14\` 변환본 복구. 저장 위치·Notion 정리 방식은 사용자 확인 (event/meetings)
- [x] (10-14 17:09·17:40 두 번 `정상` 확인) (10-14) lead-tracker Events_OPS 쓰기 검증 첫 동작 확인 — 다음 Revenue 실행(17:09~) 로그에 `[Events_OPS 쓰기 검증] 정상` 줄이 찍히는지. `⚠️ … 덜 남음`이 찍히면 쓰기 단계 유실 확정(재쓰기 결과 줄도 같이 확인). Event Date·Time 유실 3차(10-13 23:11 쓰기 직후) 원인 추적용 (lead-tracker)
- [x] (10-15 사용자 완료: 10/6 Notion 본문 교체, 10/8 CTA 고정 단락 확인) (10-14) 블로그 10/6 발행본 확인 — Notion 10-06 행(`옥스브리지 마감 9일 전! 제출 전 형식 점검 체크리스트`) 본문이 UCAT 글(10-09와 같은 초안)로 들어가 있음. 사용자 추정: 네이버에선 직접 작성했고 Notion으로 안 옮겼을 가능성 → 네이버 10/6 실제 글 확인 후 Notion 본문 교체 여부 결정. 10/8 글 CTA 앞 고정 두 단락 누락도 같이 확인 (blog)
- [x] (10-16 Richard에게 이관) (10-14) Expo(1월) 디지털 예산 내부 논의 후 본사 performance팀에 공유 — **2026-10-23(금) 전까지 plan 확정**. 본사는 Meta 약 40k 가정, Naver 유료 + Meta(PMax·Demand Gen 없음), 트래픽 8주 + 리드젠 6주 제안 (Digital Weekly 10-14, `meetings/digital-weekly/2026-10-14.md`)
- [ ] (2027-01 엑스포 후) lead-tracker FY27 New P1 총목표 3627 재점검 — 10-15 시뮬레이션 기준 연말 예상 3324(시즌성)/2894(3개월 속도), 부족분 거의 Seminar(목표 880 vs 예상 46~55). 엑스포로 Seminar가 메워졌는지 `TEMPQA_072_TargetRecalcSimulation.js` `runSimulateTargetRecalc()` 재실행으로 확인 (lead-tracker)
- [ ] (10-16) lead-tracker Events_OPS 유실 5차(10-16 15:13 쓰기 직후, 복원 완료) 후속 — 쓰기 전 필터 제거 + 즉시 메일 배포(`EVENTS_005_Write.js` v1.7.0). 다음 유실 메일이 오면 그 실행 로그의 `[Events_OPS 필터]` 줄로 필터 원인 판별 → 확정되면 BOFU/Content/Search/Leads_OPS 쓰기에도 같은 수정. 실무자에게 15:13 전후 Events_OPS 필터 사용 여부 확인 (lead-tracker)
- [ ] (10-15) lead-tracker Events_OPS 유실 재발 시 — 가드 메일이 오면 첫 가드 실행 **직전** Revenue 실행 로그의 `[쓰기 진단]` 줄 확보 → 원인 판단·수정. 복원은 `runPreviewRestoreEventsManualFromBackup()` → `runRestoreEventsManualFromBackup()` → `runRevenuePipelineTail()` (10-15 11:11 쓰기 직후 375→4 확정, lead-tracker)
- [ ] (10-17) 이벤트 참가패턴 분석 — Notion 웨비나 DB 페이지 내부 데이터 긁어와서 분석 (analytics)

- [x] (10-19) 블로그 리서치 10건(10/23~11/02 발행분) 방식 결정 — 10-20 A안 확정, 10/23·25·26·27 4건 Claude 리서치 완료·push (blog)
- [ ] (10-26 오전 Gemini 초기화 후) 블로그 리서치 남은 6건(10/28·29·30·31·11/01·11/02) Gemini flash-low로 처리 — 10/28분은 10/27 07:00 D-1 루틴 전까지 필요. 실행 전 agy 모델 목록에 flash-low보다 낮은 모델이 있는지 확인(10-19 flash-low 4회로 주간 한도 소진, 10-20 사용자: "더 낮은 모델 써야 할 듯") (blog)
- [x] (10-19) 블로그 11/01 "마감 직전 제출 오류 대비" 글 — 10-20 10/30 글과 발행일 교체(제출 오류 → 10/30, 대회/경시대회 → 11/01), 10/28은 에세이 내용 오류·10/30은 기술 오류로 앵글 분리 (blog). 10/24 중복 건은 10-20 "ED 제출 후 인터뷰 연락이 오면 — 11월 일정과 준비 순서"로 앵글 변경 완료
- [x] (10-22 Zoom) 채용 스크리닝 질문지 점검 — 10-20 사용자 완료(불필요 질문 제거)
- [x] (10-20 아침) 블로그 d1 루틴 Step 2.5 첫 실행 확인 — 10-20 07:13 실행, Harry 🚧에 10/23·25·26·27 4건 정상 기록 확인 (blog)
- [ ] (10-22 목 12:00·14:00) 채용 Zoom 스크리닝 2건 — 질문지는 Notion db_recruit 페이지, 끝나면 녹화 전사·Q&A 정리 (interview)

## 도메인별 TODO

여기는 전역 항목만 담는다. 도메인별 세부 TODO는 각 폴더에서 따로 관리한다 (2026-09-26 확정, 이유는 `context/CLAUDE.md` 관련 세션 기록 참고):

- `onboarding/TODO.md`
- `writing/TODO.md`
- `ideate/TODO.md`
