# meetings/

주간 반복 회의 기록 폴더입니다. 회의 하나당 파일 하나로 저장합니다. 상위 원칙은 `.gemini/antigravity/knowledge/crimson-principles.md`를 따르고, 카테고리별 빈도와 원온원 상대방 명단은 `_index.md`가 기준입니다(명단을 이 문서에 중복해서 적지 않는다).

## 폴더 구조

- `event-review/`, `ideation/`, `growth-meeting/`, `sales-marketing/`: 카테고리별 회의 폴더
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
- `segments`가 빈 배열이면 아직 전사가 실행되지 않은 것이다 (녹음 종료와 전사 실행은 별개 단계). 이 경우 사용자에게 앱에서 눌러달라고 요청하지 말고, 아래 옵션으로 `vibe-server`를 직접 돌린다 (2026-09-22 확정):
  ```
  /Applications/vibe.app/Contents/MacOS/vibe-server transcribe <model> <audio.wav> --language ko --beam-size 5 --best-of 5 --temperature 0.4 --threads 4
  ```
  `<model>`은 `transcript.vibe.json`의 `modelPath` 값을 그대로 쓴다. `beam-size`/`best-of`/`temperature`/`threads` 값은 `~/Library/Application Support/github.com.thewh1teagle.vibe/app_config.json`의 `transcription.modelOptions`를 그대로 따온 것 — Vibe 앱이 실제로 검증해서 쓰는 값이다. 녹음이 길면(수십 분 이상) 시간이 걸리므로 백그라운드로 실행하고 완료를 기다린다.
- `--word-timestamps` 옵션은 쓰지 않는다. 단어 단위로 쪼개면서 한글 멀티바이트 문자가 깨진다 (예: "제주도" → "제주■", 2026-09-22 확인). 세그먼트 단위 타임스탬프만으로 충분하다.
- 옵션 없이(기본값 temperature=0 그리디) 돌리면 긴 녹음(70분+)에서 같은 문구를 수백 번 반복하는 hallucination loop가 발생할 수 있다 (2026-09-22 확인, "스탠포드에 합격시킨" 반복). 위 앱 기본값 옵션을 반드시 쓴다. 그래도 반복 루프가 보이면 결과를 그대로 쓰지 말고 사용자에게 알린다.
- 전사 결과는 문장 부호(`.`, `?`, `!`) 기준으로 한 문장씩 줄바꿈해서 저장한다 (로컬 md, Notion 둘 다). whisper 출력은 문장 사이 마침표는 있지만 줄바꿈이 없어 벽처럼 읽혀 가독성이 떨어진다 (2026-09-22 사용자 피드백). 이 포맷팅은 2026-09-22 이후 새로 만드는 회의록부터 적용 — 그 이전 파일은 소급 수정하지 않는다.
- Vibe/whisper.cpp는 화자 분리(diarization) 기능이 없다. 봇 없는 로컬 마이크 녹음이라 "누가 말했는지"를 아예 구분하지 못하므로, 화자 라벨을 임의로 추정해 붙이지 않는다. 화자 구분이 필요하면 별도 diarization 도구(예: pyannote) 도입이 필요하다는 걸 사용자에게 알리고, 요청 없이 먼저 진행하지 않는다.
- 회의 제목은 Vibe가 자동으로 저장하지 않는다 (폴더명은 `Record-<타임스탬프>`일 뿐). 제목은 사용자가 말해준 것을 사용하고, 그 **제목**의 키워드로 저장 위치를 결정한다. 위에서부터 순서대로 검사하고 처음 맞는 규칙을 적용한다.

| 순서 | 제목 키워드 | 저장 위치 | 추가 규칙 |
|---|---|---|---|
| 1 | `1:1` 또는 `1on1` 포함 | `1on1/<이름>/` | 참석자 이름으로 `<이름>` 폴더 매칭 (본인 제외한 상대방) |
| 2 | `이벤트 리뷰` 포함 | `event-review/` | - |
| 3 | `아이디에이션` 포함 | `ideation/` | - |
| 4 | `그로스` 포함 | `growth-meeting/` | - |
| 5 | `세일즈` 또는 `마케팅` 포함 | `sales-marketing/` | - |

- 파일명은 회의 날짜 기준 `YYYY-MM-DD.md`.
- 영문 표기(`1:1`, `1on1`)는 대소문자를 구분하지 않고 매칭한다. 그 외 한국어 키워드는 부분 문자열 일치 기준이다.

## Notion 페이지 생성 (Vibe → Notion)

사용자가 Vibe transcript(파일/텍스트)를 전달하며 "정리해줘"라고 요청하면 위 매칭 규칙으로 분류하고, **로컬 md와 Notion 페이지를 둘 다** 만든다. 자동 실행은 하지 않는다. 매칭 순서는 위 표와 같다.

| 매칭 | Notion DB (data source) | 속성 | 템플릿 |
|---|---|---|---|
| 1on1 | `dbInCorpMeeting` (`collection://cf42335d-5a19-429b-b1b6-54baa385b667`) | Name=`<이름> 1:1`, Tags=`Inter-corp Meeting`, Date, Person=사용자 본인 | `one-on-one` (`31864dfd-498f-8045-8c31-c753b06acb20`) |
| 이벤트 리뷰 | `dbInCorpMeeting` | Name=회의 제목, Tags=`Team`, Date, Person=사용자 본인 | 없음 |
| 아이디에이션 | `dbTodos` (`collection://2907cc28-daa4-4494-9ab6-ad4a6dd0a3dd`) | Tasks(제목)=회의 제목, Type=`Ideation` | `Ideation_2.3.2` (`bc1b4f40-f720-4891-8318-1ae1ce11c254`) |
| 그로스 | `dbGm` (`collection://9658cdef-98f7-40fb-8ee6-645e816b6176`) | Name=회의 제목, Tags=`Meeting`, Date | `GM_temp.2.0.0.` (`39564dfd-498f-80ad-a45e-fbf1dc76436e`) |
| 세일즈/마케팅 | `dbInCorpMeeting` | Name=회의 제목, Tags=`Team`, Date, Person=사용자 본인 | 없음 |
| 그 외 미매칭 | `dbInCorpMeeting` | Name=회의 제목, Tags=`Team`, Date, Person=사용자 본인 | 없음 |

- 본문은 해당 DB 템플릿의 구조(제목/항목)에 transcript 내용을 채워 넣는다. `create-pages`는 `template_id`와 `content`를 같이 못 쓰므로, 템플릿 페이지를 fetch해 구조를 복제한 content로 만든다. 템플릿이 없는 노트는 요약 / 주요 논의 / 결정 / 액션 아이템 구조로 쓴다.
- `dbTodos`의 Status, Due, Priority 등 위에 적지 않은 속성은 사용자가 정하기 전까지 비워둔다.
- Vibe는 봇 없는 로컬 녹음이라 화자 이름이 자동으로 붙지 않는다. 1on1 상대방 이름이 화자 라벨(Speaker 1/2)로만 나오면 임의로 붙이지 않고 사용자에게 확인한다.
- Notion 페이지를 만들기 전에 같은 날짜·같은 Name의 페이지가 이미 있는지 검색하고, 있으면 새로 만들지 않고 사용자에게 확인한다.

## 그로스미팅 원문 보강 (실시간 노트 + Vibe transcript → 기존 dbGm 페이지)

그로스미팅은 회의 중 사용자가 `dbGm` 페이지에 실시간으로 구조화된 노트(가설/실험 카드, Weekly 1:1 표 등)를 직접 입력한다. 회의가 끝나고 Vibe transcript를 전달하며 "확인해서 채워달라"고 하면, 이미 적힌 내용은 그대로 두고 다음만 한다.

- **적힌 내용 중 누락된 것**: 관련 항목(불릿) 바로 아래에 `> "인용문"` 형태로 원문 발췌를 덧붙인다. **라벨/접두사(예: "0922 그로스미팅 원문 — ...")는 붙이지 않는다** — 인용부호로 시작하는 순수 blockquote만 쓴다 (2026-09-22 확정).
- **아예 적혀있지 않은 내용**: 가장 가까운 관련 섹션 아래에 같은 `> "인용문"` 형태로 추가한다. 마땅한 섹션이 없으면 2️⃣/3️⃣ 경계(예비 결과 점검 소제목 바로 아래)처럼 일반 논의 항목이 모이는 위치에 넣는다.
- **주의**: 기존 내용을 삭제하거나 옮기지 않는다. quote 텍스트 편집(`notion-update-page`의 `update_content`)은 노션이 저장 시 일부 오탈자를 자동으로 다듬을 수 있어, 짧은 앞/뒤 조각만으로 긴 구간을 지우려 하면 중간 원문이 파편으로 남는 사고가 날 수 있다 — 삭제/치환할 때는 항상 **전체 문구를 정확히** old_str/new_str에 넣고, 편집 직후 반드시 다시 fetch해서 결과를 확인한다.
- **완료 처리**: 노트 작성(위 보강 포함)이 다 끝나면 해당 `dbGm` 페이지의 `Tags` 속성을 `Meeting`에서 `Archive`로 바꾼다 (2026-09-22 확정).

## 미매칭 처리 (No Assumptions)

아래 경우에는 임의로 분류하거나 새 폴더를 만들지 않고 사용자에게 먼저 확인한다.

- 어떤 키워드에도 맞지 않는 제목: Notion은 위 표대로 `dbInCorpMeeting`에 넣지만, **로컬 md 저장 위치**는 정해진 폴더가 없으므로 사용자에게 확인한다.
- 1on1인데 참석자가 `_index.md`에 등록된 상대방과 일치하지 않는 경우 (신규 팀원 폴더가 생기기 전까지는 그 사람의 1on1도 여기에 해당). 이 경우 Notion 페이지도 이름 확인 후에 만든다.

## 갱신 절차

- 원온원 상대방이 확정/변경되면 `1on1/<이름>/` 폴더를 만들고 `_index.md`의 명단 표를 갱신한다.
- 카테고리나 키워드가 바뀌면 이 문서의 매칭 표와 `_index.md`의 빈도표를 함께 갱신한다.
