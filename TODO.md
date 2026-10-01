# Global TODO

<!-- Add items here. Format: - [ ] task (project/context) -->
- [x] HS to DS disclaimer 공유 (2026-09-30)
- [ ] 맥 세팅 시 `crimson/scripts/setup-claude-md.sh` 실행해서 `~/.claude/CLAUDE.md` 생성 (crimson)
- [x] 사무실 PC에서 `~/.claude/CLAUDE.md` 기존 내용 확인 — 비어있으면 `setup-claude-md.ps1` 실행, 다른 내용 있으면 crimson 포인터 한 줄만 수동 추가 (crimson)
- [x] 운전면허 갱신 신청 (2026-09-30 완료)
- [ ] 2026-10-31 로컬라이즈 프로젝트 FU — 학교 rigor & 학교별 합격률
- [x] (10-01) 아이디에이션 09-30 누락 구간 ~09:30~11:30(c01 조각: %TEMP% 아래 v1033_chunks/c01_570.wav) 1분 단위 재전사 후 `meetings/ideation/2026-09-30.md` 보강 — 나머지는 10-01 완료(로컬 md, HS & CAO·Creative Quality bar·수요일 웨비나 미참석자 페이지 인용 보강) (meetings)
- [x] (10-01 오후) 아이디에이션 "수요일 웨비나 미참석자 → 다시 초대" FU — 발표자와 가설 발송 수단 이메일→메시지 수정, 9/2·9/8·9/16 이벤트 안내 메시지 오픈율 확인 (Notion 페이지 3️⃣ 가설 아래 체크박스) https://app.notion.com/p/3b464dfd498f80d98969e2f08f1ca5b6
- [x] (10-01 재부팅 후) Digital Weekly 09-30 화자 구분 재전사 — 10-01 완료(vibe-server HTTP API, 결과 `%TEMP%\dw0930_diar.json`). 이름 매핑은 사용자 판단으로 보류 (meetings)
- [ ] (10-01) office PC Vibe 정리 — ✅ GPU 해결(드라이버 617.14, `--gpu-device 0 --threads 6`, 2분 42초, meetings/CLAUDE.md 기록). 남은 것: 녹음 Documents 저장 원인, 1분 튕김 원인 — 이하 원래 메모: NVIDIA GPU 미인식(Intel UHD만, 1분 전사 ≈ 80초) 드라이버 확인 — 10-01 확인: GTX 1660 Ti Max-Q, 드라이버 442.94(2020년)로 매우 구버전 → 최신 드라이버 설치(관리자 권한, 사용자) 후 `--gpu-device` 지정 테스트. CPU는 i7-10750H 6코어라 `--threads 6`으로 올릴 것, 녹음이 Documents로 저장 안 된 원인, 11:00 60초 녹음 정체(→ 10-01 사용자 확인: Digital Weekly 시작 녹음이 1분 만에 튕긴 것, 11:02:58 재시작 — 튕긴 원인은 미확인), 결과를 `meetings/CLAUDE.md`에 기록 (meetings)
- [ ] (10-01) 스쿨 타임라인용 웨비나 캘린더 제작하기
- [x] (10-01) Quality Bar 템플릿 7개 dbTodos 등록 (사용자 완료)
- [x] (10-01) 수요일 웨비나 미참석자 재초대 FU (사용자 완료)

## 도메인별 TODO

여기는 전역 항목만 담는다. 도메인별 세부 TODO는 각 폴더에서 따로 관리한다 (2026-09-26 확정, 이유는 `context/CLAUDE.md` 관련 세션 기록 참고):

- `onboarding/TODO.md`
- `writing/TODO.md`
- `ideate/TODO.md`
