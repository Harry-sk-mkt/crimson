# meetings/

주간 반복 회의 기록 폴더입니다. 회의 하나당 파일 하나로 저장합니다. 상위 원칙은 `.gemini/antigravity/knowledge/crimson-principles.md`를 따르고, 카테고리별 빈도와 원온원 상대방 명단은 `_index.md`가 기준입니다(명단을 이 문서에 중복해서 적지 않는다).

## 폴더 구조

- `event-review/`, `ideation/`, `growth-meeting/`, `sales-marketing/`, `case-study/`, `digital-weekly/`, `partnership/`, `crimson-global/`: 카테고리별 회의 폴더
  - `crimson-global/`: 다른 지역 Crimson 오피스(US, 싱가포르 등)와의 1:1 지식공유·벤치마킹 콜. 제목에 공통 키워드가 아직 없어 자동 매칭 규칙은 안 만들었음 — 미매칭 제목이 이런 성격이면 사용자에게 확인 (2026-10-13 "Steph (US in-person) event discussion meeting" 사례로 신설, 일회성/부정기라 `_index.md` 빈도표에는 안 넣음)
- `1on1/<이름>/`: 원온원은 상대방별 폴더 (소문자 영문 이름, 등록된 상대방은 `_index.md` 참고)

## 파일 규칙

- 회의 하나당 파일 하나: `<카테고리 폴더>/YYYY-MM-DD.md` (예: `event-review/2026-09-22.md`)
- 원온원: `1on1/<이름>/YYYY-MM-DD.md`
- 같은 날짜에 같은 폴더에서 회의가 2번 이상이면 파일명 규칙에 맞는 값이 없다. 접미사를 추측해서 붙이지 말고 사용자에게 규칙을 확인한 뒤 이 문서를 갱신한다.

## Vibe transcript 매칭 규칙

회의 녹음은 로컬 앱 Vibe로 진행한다 (Fireflies 대체, 2026-09-21부터). Vibe는 로컬 앱이라 자동 pull이 안 되므로, 사용자가 "방금 녹음했어" 등으로 전사를 요청하면 사용자에게 파일을 요청하기 전에 먼저 로컬에서 직접 찾는다 (2026-09-22 확정).

### 로컬 Vibe 녹음 찾는 법

- 녹음은 `~/Documents/Vibe/Record-<날짜>-<시각>-.../` 폴더에 저장되고, 그 안의 `transcript.vibe.json`에 `segments` 배열로 전사 내용이 들어있다.
- "방금" 녹음은 `createdAt`/폴더 타임스탬프가 가장 최근인 것을 고른다. 여러 개가 비슷한 시각이면 사용자에게 확인한다.
- **앱이 튕겼을 때(맥)**: `~/Documents/Vibe`에 새 폴더가 없어도 녹음은 `$TMPDIR/vibe_temp_<YYYY-MM-DD>/<YYYY-MM-DD HH-MM-SS>.wav`(16kHz mono)에 남아 있을 수 있다. 임시 폴더라 재부팅 시 지워질 수 있으므로 먼저 `~/Documents/Vibe/Record-<타임스탬프>-recovered/audio.wav`로 복사한 뒤 아래 CLI로 전사한다. 크래시 로그는 `~/Library/Logs/DiagnosticReports/vibe-*.ips` (2026-10-12 66분 녹음 후 SIGABRT 크래시에서 확인). **Windows(office)도 같다**: 임시 녹음은 `%TEMP%\vibe_temp_<YYYY-MM-DD>\<YYYY-MM-DD HH-MM-SS>.wav`(16kHz 변환본), 앱 로그는 `%APPDATA%\github.com.thewh1teagle.vibe\log_<YYYY-MM-DD>.txt`(`WAV file path`, `Merging WAV files`, ffmpeg 명령이 찍힘). 2026-10-14 Digital Weekly: Zoom 종료 2초 뒤 헤드셋 스트림 오류(`StreamInvalidated`) → 녹음 정지 시 앱이 꺼졌지만 변환본은 정상이었다.
- `segments`가 빈 배열이면 아직 전사가 실행되지 않은 것이다 (녹음 종료와 전사 실행은 별개 단계). 이 경우 사용자에게 앱에서 눌러달라고 요청하지 말고, 아래 옵션으로 `vibe-server`를 직접 돌린다 (2026-09-22 확정):
  ```
  /Applications/vibe.app/Contents/MacOS/vibe-server transcribe <model> <audio.wav> --language ko --beam-size 5 --best-of 5 --temperature 0.4 --threads 4
  ```
  **Windows(office)**: 2026-09-30 winget(`Thewh1teagle.vibe` 3.2.2)으로 설치 — 실행 파일은 `C:\Users\Harry\AppData\Local\vibe\vibe-server.exe`, 같은 폴더에 `ffmpeg.exe`도 있다. 모델: `C:\Users\Harry\AppData\Local\github.com.thewh1teagle.vibe\ggml-large-v3-turbo.bin` (맥과 같은 large-v3-turbo). 설정: `C:\Users\Harry\AppData\Roaming\github.com.thewh1teagle.vibe\app_config.json` — `transcription.modelOptions`가 생겼지만 `lang: en`(Digital Weekly 때 바꾼 값)이라 그대로 따오지 말고, CLI에는 맥과 같은 옵션(`--language ko --beam-size 5 --best-of 5 --temperature 0.4`)을 직접 넣는다. 앱 `model.path`는 `ggml-large-v3-turbo.bin`이다. 2026-10-12에 MD5가 같은 복사본 `ggml-model_63xfoh8w.bin`(1.5GB)을 삭제하고 경로를 원본으로 바꿨다. 같은 날 녹음 단축키(`recording.shortcutEnabled`)는 오입력으로 녹음이 멈추는 일을 막으려고 껐고, 회의 감지는 켜둔 상태다. 백업 파일은 `app_config.json.bak-20261012`. **office GPU (2026-10-01 확인)**: 드라이버 617.14 업데이트 후 Vulkan 장치 0 = GTX 1660 Ti, 1 = Intel UHD → CLI에 `--gpu-device 0 --threads 6`(i7-10750H 6코어)을 추가한다. 2분 파일 기준 CPU 약 160초 → GPU 42초(모델 로드 포함). `-v`를 붙이면 텍스트가 `[_TT_..]` 토큰과 섞여 나오므로 결과 추출용으로는 빼고 돌린다. **화자 구분(2026-10-01 확인)**: `transcribe` CLI엔 옵션이 없지만 HTTP 서버 모드로 된다 — `vibe-server serve --port 8765 --exit-with-parent false` → `POST /v1/models/load` JSON `{"path":"<모델>","gpu_device":0}` → `POST /v1/audio/transcriptions` multipart `file=@<wav>`, `language`, `response_format=verbose_json`, `diarize_model=C:/Users/Harry/AppData/Local/github.com.thewh1teagle.vibe/diar_streaming_sortformer_4spk-v2.q8_0.gguf`, `beam_size=5`, `best_of=5`, `temperature=0.4`, `n_threads=6`. 각 segment에 `speaker`(0부터, 최대 4명) 필드가 붙는다. 31분 영어 회의 GPU 약 6.5분. 끝나면 서버 프로세스를 종료한다. 화자 이름 매핑은 사용자가 요청할 때만 한다. 녹음 저장 폴더는 `C:\Users\Harry\OneDrive\Documents\Vibe\`다. 이 PC는 Windows "문서" 폴더 자체가 OneDrive로 리디렉션돼 있어서 `~/Documents\Vibe`는 없다 — 저장이 안 된 게 아니라 위치가 다른 것이다(2026-10-12 확인). 시스템 오디오(Zoom 상대방) 녹음은 Record 화면에서 스피커 옵션을 켜야 한다 — Windows 동작은 테스트 후 기록.
  **Windows(home, `underline_desk`, 사용자 `mrhar`)**: winget으로 설치 — 실행 파일 `C:\Users\mrhar\AppData\Local\vibe\vibe-server.exe`, 같은 폴더에 `ffmpeg.exe`도 있음. 모델: `C:\Users\mrhar\AppData\Local\github.com.thewh1teagle.vibe\ggml-large-v3-turbo.bin`. 정상 녹음 저장 폴더는 `C:\Users\mrhar\OneDrive\Documents\Vibe\`(이 PC도 문서 폴더가 OneDrive 리디렉션). **앱이 튕겼을 때**: 맥과 동일하게 `C:\Users\mrhar\AppData\Local\Temp\vibe_temp_<YYYY-MM-DD>\<YYYY-MM-DD HH-MM-SS>.wav`에 원본이 남아 있다 (2026-10-13 확인). GPU 옵션(`--gpu-device`)은 아직 테스트 안 함 — 이 세션은 CPU(`--threads 4`)로 돌렸고 32분 파일 10분 청크 기준 각 조각 전사에 수 분 소요. ffmpeg가 이 PC에도 있어서(비디 설치 폴더) `-f segment -segment_time <N> -c copy`로 쪼개는 방식이 맥의 Python `wave` 모듈 방식보다 간단하게 된다.
  `<model>`은 `transcript.vibe.json`의 `modelPath` 값을 그대로 쓴다. `beam-size`/`best-of`/`temperature`/`threads` 값은 `~/Library/Application Support/github.com.thewh1teagle.vibe/app_config.json`의 `transcription.modelOptions`를 그대로 따온 것 — Vibe 앱이 실제로 검증해서 쓰는 값이다. 녹음이 길면(수십 분 이상) 시간이 걸리므로 백그라운드로 실행하고 완료를 기다린다.
- **맥에서 긴 녹음은 처음부터 10분 청크로 나눠 전사한다** (2026-10-12 확인): 66분 파일을 통째로 돌리자 모델 로드 전 Metal(GPU) `waitUntilCompleted`에서 CPU 0%로 멈춘 채 14분간 진행이 없었다. 10분 청크는 각 약 100초에 정상 완료. 진행 여부는 stdout이 끝날 때까지 비어 있으므로 CPU/메모리(`ps -o pcpu,rss`)로 확인하고, 청크마다 타임아웃(`perl -e 'alarm 600; exec @ARGV' ...`)을 건다.
- `--word-timestamps` 옵션은 쓰지 않는다. 단어 단위로 쪼개면서 한글 멀티바이트 문자가 깨진다 (예: "제주도" → "제주■", 2026-09-22 확인). 세그먼트 단위 타임스탬프만으로 충분하다.
- 옵션 없이(기본값 temperature=0 그리디) 돌리면 긴 녹음(70분+)에서 같은 문구를 수백 번 반복하는 hallucination loop가 발생할 수 있다 (2026-09-22 확인, "스탠포드에 합격시킨" 반복). 위 앱 기본값 옵션을 반드시 쓴다. 그래도 반복 루프가 보이면 결과를 그대로 쓰지 말고 사용자에게 알린다.
- **반복 탐지는 두 방식을 병행한다** (2026-09-29 확인): ① 연속 동일 문자열 정규식 — 같은 구절이 바로 이어서 반복되는 경우. ② 인접 문장 유사도(Python `difflib`) 비교 — 문단 하나가 통째로 뒤에서 다시 등장하는 echo형 hallucination은 ①로 못 잡음(chunk_00에서 실제 발견). 두 방식 다 써서 교차 확인한다. 그래도 둘 다 놓치는 echo가 있으므로(2026-10-19 Hanna 1:1 chunk_02, 짧은 문장이 섞인 문단 반복) 저장 전에 전문을 한 번 직접 읽어서 확인한다.
- **hallucination loop 발생 시 분할 재전사로 해결한다** (2026-09-22 72분 파일, 2026-09-23 15분 파일에서 두 번 확인 — 앱 권장 옵션을 써도 발생 가능): `audio.wav`를 Python `wave` 모듈로 10분 단위 청크로 나눠(이 환경엔 ffmpeg 없음) 각각 따로 전사한다. 특정 청크에서도 반복이 나오면 그 청크만 2분 단위로 더 쪼개 재시도하고, 2분에서도 남으면 1분, 그래도 남으면 20~40초까지 재귀적으로 계속 더 쪼갠다 (2026-09-29 확인 — 2분까지만으로는 안 잡히는 경우가 있었음). 결과를 합쳐서 문장 단위 줄바꿈으로 정리한다.
- 짧은 조각(2분)으로 전사하면 조각 끝에 실제 발화가 아닌 " 감사합니다."가 붙어 나올 수 있다. 합칠 때 조각 끝의 이 문구는 지운다 (2026-10-21 아이디에이션, 5조각 중 3조각에서 확인).
- **재귀 분할에도 한계가 있다 — 끝까지 깨지면 전사 포기하고 사용자에게 알린다** (2026-10-13 확인): 10분→2분→20~30초까지 쪼개도 매번 다른 무의미한 내용(완전히 다른 단어)으로 깨지는 구간은 모델 컨텍스트 문제가 아니라 원음 자체 품질 문제(겹치는 발화, 마이크 노이즈 등)일 가능성이 높다. 이 경우 더 쪼개봐야 소용없으므로 20~30초에서 멈추고, 해당 구간을 `[전사 불가]`로 표시한 뒤 사용자에게 알린다 — 여러 조각에서 서로 다른 그럴듯한 내용이 나왔다고 해서 아무거나 골라 짜맞추지 않는다. 통화 종료 후 이어지는 무음/잡음 구간도 매번 다른 무의미한 한국어로 전사되는 식으로 나타나므로, 같은 패턴이면 실제 발화가 아닐 가능성을 의심한다.
- **결정은 전사가 아니라 사용자 노트·발언이 기준이다** (2026-10-01 사용자 확정): Notion에 사용자가 직접 쓴 노트(예: "Indigo WB - again X")와 전사가 다르면 노트를 결정으로 쓰고, 전사로 반대 결론을 내리거나 사용자에게 "전사로는 ~로 들린다"며 결론을 뒤집으려 하지 않는다. whisper는 "not" 같은 부정어를 자주 빠뜨린다(Digital Weekly 09-30: 사용자는 "not again", 전사는 "good enough to do again"). 노트에 없는 결정만 전사에서 가져온다.
- 전사 결과는 문장 부호(`.`, `?`, `!`) 기준으로 한 문장씩 줄바꿈해서 저장한다 (로컬 md, Notion 둘 다). whisper 출력은 문장 사이 마침표는 있지만 줄바꿈이 없어 벽처럼 읽혀 가독성이 떨어진다 (2026-09-22 사용자 피드백). 이 포맷팅은 2026-09-22 이후 새로 만드는 회의록부터 적용 — 그 이전 파일은 소급 수정하지 않는다.
- Vibe 3.2.2는 화자 구분(diarization)을 지원한다(최대 4명, 결과는 Speaker 번호뿐). 앱은 설정 `transcription.recognizeSpeakers`로 켜고, CLI는 위 Windows 항목의 HTTP 서버 방식을 쓴다(2026-10-01 확인). 화자 번호에 이름을 임의로 추정해 붙이지 않는다.
- 회의 제목은 Vibe가 자동으로 저장하지 않는다 (폴더명은 `Record-<타임스탬프>`일 뿐). 제목은 사용자가 말해준 것을 사용하고, 그 **제목**의 키워드로 저장 위치를 결정한다. 위에서부터 순서대로 검사하고 처음 맞는 규칙을 적용한다.

| 순서 | 제목 키워드 | 저장 위치 | 추가 규칙 |
|---|---|---|---|
| 1 | `1:1` 또는 `1on1` 포함 | `1on1/<이름>/` | 참석자 이름으로 `<이름>` 폴더 매칭 (본인 제외한 상대방) |
| 2 | `이벤트 리뷰` 포함 | `event-review/` | - |
| 3 | `아이디에이션` 포함 | `ideation/` | - |
| 4 | `그로스` 포함 | `growth-meeting/` | - |
| 5 | `세일즈` 또는 `마케팅` 포함 | `sales-marketing/` | - |
| 6 | `케이스 스터디` 포함 | `case-study/` | 일회성/부정기 회의 — `_index.md` 빈도표에는 넣지 않는다 (2026-09-23 확정) |
| 7 | `Digital Weekly` 또는 `Weekly Digital` 포함 | `digital-weekly/` | 본사 퍼포먼스팀과의 주간 회의, **영어** — 전사 시 `--language en` (2026-10-01 확정) |
| 8 | `파트너십` 포함 | `partnership/` | 외부 파트너사 미팅(예: SC Bank) — 일회성/부정기, `_index.md` 빈도표에는 넣지 않는다 (2026-10-15 확정) |

- 파일명은 회의 날짜 기준 `YYYY-MM-DD.md`.
- 영문 표기(`1:1`, `1on1`)는 대소문자를 구분하지 않고 매칭한다. 그 외 한국어 키워드는 부분 문자열 일치 기준이다.

## Notion 페이지 생성 (Vibe → Notion)

사용자가 Vibe transcript(파일/텍스트)를 전달하며 "정리해줘"라고 요청하면 위 매칭 규칙으로 분류하고, **로컬 md와 Notion 페이지를 둘 다** 만든다. 자동 실행은 하지 않는다. 매칭 순서는 위 표와 같다.

| 매칭 | Notion DB (data source) | 속성 | 템플릿 |
|---|---|---|---|
| 1on1 | `dbInCorpMeeting` (`collection://cf42335d-5a19-429b-b1b6-54baa385b667`) | Name=`<이름> 1:1`, Tags=`Inter-corp Meeting`, Date, Person=사용자 본인 | `one-on-one` (`31864dfd-498f-8045-8c31-c753b06acb20`) |
| 이벤트 리뷰 | `dbInCorpMeeting` | Name=회의 제목, Tags=`Team`, Date, Person=사용자 본인 | 없음 |
| 아이디에이션 | 새 페이지 만들지 않음 — 아래 "아이디에이션 원문 보강" 참고 | - | - |
| 그로스 | `dbGm` (`collection://9658cdef-98f7-40fb-8ee6-645e816b6176`) | Name=회의 제목, Tags=`Meeting`, Date | `GM_temp.2.0.0.` (`39564dfd-498f-80ad-a45e-fbf1dc76436e`) |
| 세일즈/마케팅 | `dbInCorpMeeting` | Name=회의 제목, Tags=`Team`, Date, Person=사용자 본인 | 없음 |
| 케이스 스터디 | `db_CaseStudies` (`collection://3e464dfd-498f-80b7-a419-000bd09f5f59`) — 새 페이지 만들지 않음. 사용자가 미팅 중 직접 쓴 메모 페이지가 이 DB에 있으므로 그 페이지를 찾아 보강한다 (2026-09-23 사용자 확정). 요약은 회의록(요약/논의/결정/액션)이 아니라 **세미나 슬라이드에 바로 쓸 수 있는 학생 케이스 정리**로 쓴다: 한 줄 요약 → 세미나 메시지 → 학업 지표 → 합류 전후 → 활동별(시작·동기→성장→임팩트→Crimson 역할) → 에세이 → 공개 시 가릴 것 → 확인 필요. 출처 태그(`[담당 선생님 이름]`, `[메모]`) 표기. 기준 예시: "Brice NYU", "Scarlett Dental" 페이지. 쓰기 전에 `case-study/review-patterns.md`(사용자 교정 패턴)를 먼저 읽고, 올린 직후 `case-study/snapshots/`에 Claude 작성분 스냅샷을 남긴다 (학생 정보 포함이라 `.gitignore` 처리된 로컬 전용 폴더 — 만든 컴퓨터에서만 비교 가능, 2026-09-23 사용자 결정) | Name, Tags(US 대학 multi-select, US News 2027 Top 20 + NYU 랭킹순), Date, Person | 없음 |
| Digital Weekly | Global meeting DB (`collection://4042786a-52c5-4bf2-88f9-e9f4cd2e966d`, 페이지 `🌎 Global meeting` 안) — 새 페이지 만들지 않음. 회의 중 사용자가 만든 `Weekly Digital Marketing Call (MM/DD)` 페이지(템플릿 "Weekly digital")를 찾아 기존 노트 아래에 추가한다. 그로스미팅식 인용 보강이 **아니라** 회의 내용 요약 + 액션 아이템으로 정리하고, **의사결정 중 Cut(중단·제외)/Add(신규·추가)된 항목은 별도 섹션으로 따로 기록**한다 (2026-10-01 사용자 확정). 기존 노트·표(Weekly Digital Tracker, PLAN)는 건드리지 않는다. 추가 섹션 제목은 `## 회의 내용` (뒤에 "(Vibe 전사 정리)" 같은 출처 표기 붙이지 않음, 2026-10-01 사용자 지시). **네이밍 규칙(자동화 기준, 2026-10-01 확인)**: 제목은 `Weekly Digital Marketing Call (MM/DD)` — 회의 날짜, 월·일 두 자리 0 채움(2025-10 이후, 예: `(09/30)`). 그 이전 페이지는 `(9/30)`, `(11/6)`처럼 0 없이 썼고, 제목에 연도가 없어 `(9/30)`(2025)와 `(09/30)`(2026)가 공존한다 → 페이지를 찾을 땐 제목만으로 고르지 말고 **`Date` 속성 = 회의 날짜**로 확정한다. 제목에 연도는 넣지 않는다 — 연도 구분은 `Date`로 충분 (2026-10-01 사용자 확정) | 기존 유지 | 없음 |
| 파트너십 | `dbInCorpMeeting` — 사용자가 미팅 중 쓴 파트너사 이름 페이지(예: `SC Bank`, Tags=`Inter-corp Meeting`)가 같은 날짜로 있으면 새로 만들지 않고 그로스미팅과 같은 방식(라벨 없는 `> "인용문"`, 기존 내용 유지)으로 원문 보강한다. 제목에 "파트너십"이 없으므로 Date=회의 날짜로 찾는다 (2026-10-15 사용자 확정) | 기존 유지 | 없음 |
| 그 외 미매칭 | `dbInCorpMeeting` | Name=회의 제목, Tags=`Team`, Date, Person=사용자 본인 | 없음 |

- 본문은 해당 DB 템플릿의 구조(제목/항목)에 transcript 내용을 채워 넣는다. `create-pages`는 `template_id`와 `content`를 같이 못 쓰므로, 템플릿 페이지를 fetch해 구조를 복제한 content로 만든다. 템플릿이 없는 노트는 요약 / 주요 논의 / 결정 / 액션 아이템 구조로 쓴다.
- **Tags는 절대 비워두지 않는다**: `dbInCorpMeeting`/`dbGm` 보기(view)는 Tags로 걸러져서, Tags가 비면 페이지가 있어도 목록에 안 보인다. 페이지를 만든 직후 fetch로 Tags가 위 표 값대로 들어갔는지 확인한다 (2026-09-29 세일즈마케팅 미팅 페이지가 Tags 누락으로 안 보인 사고, 사용자 확정).
- `dbTodos`의 Status, Due, Priority 등 위에 적지 않은 속성은 사용자가 정하기 전까지 비워둔다.
- Vibe는 봇 없는 로컬 녹음이라 화자 이름이 자동으로 붙지 않는다. 1on1 상대방 이름이 화자 라벨(Speaker 1/2)로만 나오면 임의로 붙이지 않고 사용자에게 확인한다.
- Notion 페이지를 만들기 전에 같은 날짜·같은 Name의 페이지가 이미 있는지 검색하고, 있으면 새로 만들지 않고 사용자에게 확인한다.

## 1on1 원문 보강 (실시간 노트 + Vibe transcript → 기존 dbInCorpMeeting 1on1 페이지)

1on1도 그로스미팅과 같은 패턴이다 — 회의 중 사용자가 `one-on-one` 템플릿 기반 페이지(질문별 `##` 섹션, 체크박스)에 실시간으로 노트를 직접 입력해둔다. 회의가 끝나고 "처리해줘" 등으로 요청하면, 로컬 md 저장과 별개로 Notion 페이지도 확인한다 — 같은 날짜·이름의 페이지가 이미 있으면 새로 만들지 않고, 아래 그로스미팅과 동일한 방식(라벨 없는 `> "인용문"` blockquote, 기존 내용 삭제/이동 금지, 편집 후 재fetch 확인)으로 각 질문 섹션 바로 아래에 transcript 발췌를 보강한다. `## 퇴사` 같은 민감한 메모 섹션이 있을 수 있으니 손대지 않는다 (2026-09-28 Richard/Jennie 1:1에서 확인, 사용자 확정).

## 그로스미팅 원문 보강 (실시간 노트 + Vibe transcript → 기존 dbGm 페이지)

그로스미팅은 회의 중 사용자가 `dbGm` 페이지에 실시간으로 구조화된 노트(가설/실험 카드, Weekly 1:1 표 등)를 직접 입력한다. 회의가 끝나고 Vibe transcript를 전달하며 "확인해서 채워달라"고 하면, 이미 적힌 내용은 그대로 두고 다음만 한다.

- **적힌 내용 중 누락된 것**: 관련 항목(불릿) 바로 아래에 `> "인용문"` 형태로 원문 발췌를 덧붙인다. **라벨/접두사(예: "0922 그로스미팅 원문 — ...")는 붙이지 않는다** — 인용부호로 시작하는 순수 blockquote만 쓴다 (2026-09-22 확정).
- **아예 적혀있지 않은 내용**: 가장 가까운 관련 섹션 아래에 같은 `> "인용문"` 형태로 추가한다. 마땅한 섹션이 없으면 2️⃣/3️⃣ 경계(예비 결과 점검 소제목 바로 아래)처럼 일반 논의 항목이 모이는 위치에 넣는다.
- **주의**: 기존 내용을 삭제하거나 옮기지 않는다. quote 텍스트 편집(`notion-update-page`의 `update_content`)은 노션이 저장 시 일부 오탈자를 자동으로 다듬을 수 있어, 짧은 앞/뒤 조각만으로 긴 구간을 지우려 하면 중간 원문이 파편으로 남는 사고가 날 수 있다 — 삭제/치환할 때는 항상 **전체 문구를 정확히** old_str/new_str에 넣고, 편집 직후 반드시 다시 fetch해서 결과를 확인한다.
- **완료 처리**: 노트 작성(위 보강 포함)이 다 끝나면 해당 `dbGm` 페이지의 `Tags` 속성을 `Meeting`에서 `Archive`로 바꾼다 (2026-09-22 확정).

## 그로스미팅 준비 (회의 전, 사용자 요청 시)

트리거: 사용자가 "그로스미팅 준비하자" 류로 요청하면 아래 1~5를 순서대로 진행한다 (2026-10-20 사용자 확정 — "다음 주부터 그로스미팅 준비하자고 하면 지금 한 것처럼 진행").

2026-10-20 사용자가 정한 순서:

1. 지난주 `dbGm` 페이지 "예비 결과 점검" 섹션 중 Host=Harry인 실험을 오늘 페이지 같은 섹션으로 옮긴다 — `## 제목` + 가설 + 진행 불릿만, 지난주 `> "인용문"`은 옮기지 않는다.
2. 아이디어 페이지(`dbTodos`) `Due` 종료일이 오늘 이전이면 "최종점검_완료된 실험" 아래 "실험 결과" 쪽으로 옮긴다 — `### 제목` + 기울임 가설 + 불릿 + 결과 한 줄 + `→ 채택/기각`. **단, 판정할 표본이 부족하면(예: copy.lib return%는 n≥30 필요) Due가 지나도 예비에 남기고 "n=30까지 관찰 지속"처럼 적는다.**
3. 완료로 옮긴 실험은 아이디어 페이지 6️⃣ `Pratice`(행: 실행 기간 / 집행 / 지표값)와 7️⃣ `Report`(결과정리 / 도출된결론 / 교란가능성)를 채운다. 지표 정의는 `ideate/CLAUDE.md` "지표 정의" 참고.
4. 이전 미팅에서 채택/기각이 이미 결정된 실험은 결과(6️⃣·7️⃣)를 기록한 뒤 아이디어 페이지 `Status`를 채택 → `Successful`, 기각 → `Failed`로 바꾼다 (2026-10-20 사용자 확정, HS & CAO·Weekly 1:1 첫 적용).
5. 오늘 페이지 4️⃣ `Best Contributor Calc.`의 Harry 행을 채운다 (2026-10-20 사용자 정의):
   - 공급성 = 지난주 아이디에이션 회의에서 Harry가 낸 아이디어 수 (`meetings/ideation/<날짜>.md` 발표 목록 → 각 페이지 Host 확인)
   - 실행성 = 이번 주 그로스미팅에서 완료된(채택/기각 결정) 실험 수 — 이전 주에 결정돼 이번 주엔 결과 기록·Status 변경만 한 실험(4번)은 결정된 주 계산에 이미 들어가 있으므로 넣지 않는다
   - 부당성 = Harry 아이디어 중 `Re-ideation`으로 넘어간 수
   - 건전성 = 완료된 실험 중 기각된 수

- 회의 중 다른 팀원이 같은 페이지를 동시에 편집하므로 편집 직전 다시 fetch하고, 다른 사람 섹션은 건드리지 않는다.

## 아이디에이션 원문 보강 (Vibe transcript → 기존 dbTodos 페이지)

아이디에이션 회의는 참석자가 각자 아이디어 1개씩 발표하고, 아이디어 페이지는 발표자가 `dbTodos`(`collection://2907cc28-daa4-4494-9ab6-ad4a6dd0a3dd`, Type=`Ideation`)에 미리 만들어 둔다. 새 페이지를 만들지 않는다 (2026-09-23 확정).

- **페이지 찾기**: Type=`Ideation`이면서 Status=`Brief`인 페이지를 먼저 본다. **생성일로 자르지 말고 Brief 전체를 조회한다** — 발표자가 예전(한 달 전)에 만든 페이지를 재사용하는 경우가 있다 (2026-10-01: "수요일 웨비나 미참석자 → 다시 초대"가 08월 생성·Brief였는데 최근 생성순 상위만 봐서 놓침). transcript의 아이디어가 Brief에 없으면 최근 생성된 Ideation 페이지에서 찾아보고, 거기에도 없으면 사용자에게 알린다 (2026-09-23 사례: 9학년 리서치 소재 페이지가 `On-track_IDEA` 상태였음). 회의 중에 Status가 바로 바뀌기도 하므로(2026-10-15 "BOFU - first touch 보안"이 회의 중 `Need-to-FIX`로 변경), Brief 수가 transcript의 발표 수보다 적으면 Type=`Ideation` 전체를 Due 내림차순으로 조회해 회의 날짜 전후 Due 페이지를 확인한다.
- **빠진 내용 판단**: 본문뿐 아니라 인라인 DB(5W1H, Metrics, ICE System)에 이미 적힌 값도 대조한다. 이미 적힌 내용은 넣지 않는다.
- **넣는 위치**: 1️⃣ 아이디어 배경 섹션 맨 아래(2️⃣ 콜아웃 바로 위)에 모은다.
- **형식·주의**: 그로스미팅과 같다 — 라벨 없이 `> "인용문"` blockquote만, transcript 원문 그대로 인용한다. 편집 후 다시 fetch해서 확인한다.
- 화자 구분이 없으므로 발언자 이름은 붙이지 않는다. 인신·건강 관련 잡담은 넣지 않는다.

## 미매칭 처리 (No Assumptions)

아래 경우에는 임의로 분류하거나 새 폴더를 만들지 않고 사용자에게 먼저 확인한다.

- 어떤 키워드에도 맞지 않는 제목: Notion은 위 표대로 `dbInCorpMeeting`에 넣지만, **로컬 md 저장 위치**는 정해진 폴더가 없으므로 사용자에게 확인한다.
- 1on1인데 참석자가 `_index.md`에 등록된 상대방과 일치하지 않는 경우 (신규 팀원 폴더가 생기기 전까지는 그 사람의 1on1도 여기에 해당). 이 경우 Notion 페이지도 이름 확인 후에 만든다.

## 갱신 절차

- 원온원 상대방이 확정/변경되면 `1on1/<이름>/` 폴더를 만들고 `_index.md`의 명단 표를 갱신한다.
- 카테고리나 키워드가 바뀌면 이 문서의 매칭 표와 `_index.md`의 빈도표를 함께 갱신한다.
