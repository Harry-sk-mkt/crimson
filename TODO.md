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
- [ ] (10-01) 스쿨 타임라인용 웨비나 캘린더 제작하기
- [x] (10-01) Quality Bar 템플릿 7개 dbTodos 등록 (사용자 완료)
- [x] (10-01) 수요일 웨비나 미참석자 재초대 FU (사용자 완료)
- [x] (10-12) office PC Vibe — 중복 모델 삭제, `model.path`를 원본으로 변경, 녹음 단축키 끔(회의 감지는 유지). 1분 튕김 원인은 미확정으로 종결: 재발하면 Vibe를 재시작하기 전에 당일 로그 확인 (meetings)
- [x] (10-12 사용자 확인: 백업 시트 생성됨, 숨김 처리) Events_OPS Manual 백업 생성 확인 — 실행 중인 tail이 끝난 뒤 `EVENTS_007_ManualBackup.js`의 `runPreviewRestoreEventsManualFromBackup()` 실행. "복원할 빈칸 없음"이면 완료, "백업 없음"이면 `runAcceptEventsManualAsBackup()` 실행. 다음 자동 실행이 메일 권한 오류로 실패하지 않는지도 확인 (lead-tracker)
- [x] (10-13 아침) 10-07 버전 복원으로 Master에서 빠진 Leads 61행·MTA 143행+ 복구 — 실행 중인 파이프라인 없는지 확인 후 순서대로: `MASTER_004_MasterBuild.js` `rebuildLeadsMaster()` → `rebuildMTAMaster()` → `MASTER_002_PipelineAsync.js` `runLeadsPipelineTail()` → `runMTAPipelineTail()` → `TEMPQA_071_MasterRawGapAfterRestore.js` `runDiagnoseMasterRawGapAfterRestore()`로 "누락 없음" 확인 (lead-tracker) — 2026-10-13 완료(LEADS·MTA 누락 없음)
- [ ] lead-tracker 그림자 diff 확대 원인 확인 (10-13 복구 후 Target 72건·FY_REP 677건, 실제 출력 영향 없음)
- [ ] lead-tracker `rebuildMTAMaster()` 26분(30분 한도 근접) — 중복 삭제를 시트 행 삭제 대신 메모리 처리로 단축 검토 (코드 수정, 승인 필요)
- [ ] (10-14) lead-tracker Target 재산출 시뮬레이션 실행 — `TEMPQA_072_TargetRecalcSimulation.js` `runSimulateTargetRecalc()` 로그 검토: [1] FY26 재계산이 현재 목표와 일치하는지 먼저 확인 → 12개월 기준 세그먼트 목표·3627 현실성·CPNP1 비교 후 Target_Engine 반영 여부 결정
- [ ] (10-12) office PC Vibe — 다음에 앱을 열 때 모델이 정상 선택돼 있는지, 녹음·전사가 되는지 확인 (meetings)
- [ ] (10-14) lead-tracker Events_OPS 쓰기 검증 첫 동작 확인 — 다음 Revenue 실행(17:09~) 로그에 `[Events_OPS 쓰기 검증] 정상` 줄이 찍히는지. `⚠️ … 덜 남음`이 찍히면 쓰기 단계 유실 확정(재쓰기 결과 줄도 같이 확인). Event Date·Time 유실 3차(10-13 23:11 쓰기 직후) 원인 추적용 (lead-tracker)
- [ ] (10-14) 블로그 10/6 발행본 확인 — Notion 10-06 행(`옥스브리지 마감 9일 전! 제출 전 형식 점검 체크리스트`) 본문이 UCAT 글(10-09와 같은 초안)로 들어가 있음. 사용자 추정: 네이버에선 직접 작성했고 Notion으로 안 옮겼을 가능성 → 네이버 10/6 실제 글 확인 후 Notion 본문 교체 여부 결정. 10/8 글 CTA 앞 고정 두 단락 누락도 같이 확인 (blog)
- [ ] (10-14) Expo(1월) 디지털 예산 내부 논의 후 본사 performance팀에 공유 — **2026-10-23(금) 전까지 plan 확정**. 본사는 Meta 약 40k 가정, Naver 유료 + Meta(PMax·Demand Gen 없음), 트래픽 8주 + 리드젠 6주 제안 (Digital Weekly 10-14, `meetings/digital-weekly/2026-10-14.md`)

## 도메인별 TODO

여기는 전역 항목만 담는다. 도메인별 세부 TODO는 각 폴더에서 따로 관리한다 (2026-09-26 확정, 이유는 `context/CLAUDE.md` 관련 세션 기록 참고):

- `onboarding/TODO.md`
- `writing/TODO.md`
- `ideate/TODO.md`
