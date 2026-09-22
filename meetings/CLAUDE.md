# meetings/

주간 반복 회의 기록 폴더입니다. 회의 하나당 파일 하나로 저장합니다. 상위 원칙은 `.gemini/antigravity/knowledge/crimson-principles.md`를 따르고, 카테고리별 빈도와 원온원 상대방 명단은 `_index.md`가 기준입니다(명단을 이 문서에 중복해서 적지 않는다).

## 폴더 구조

- `event-review/`, `ideation/`, `growth-meeting/`: 카테고리별 회의 폴더
- `1on1/<이름>/`: 원온원은 상대방별 폴더 (소문자 영문 이름, 등록된 상대방은 `_index.md` 참고)

## 파일 규칙

- 회의 하나당 파일 하나: `<카테고리 폴더>/YYYY-MM-DD.md` (예: `event-review/2026-09-22.md`)
- 원온원: `1on1/<이름>/YYYY-MM-DD.md`
- 같은 날짜에 같은 폴더에서 회의가 2번 이상이면 파일명 규칙에 맞는 값이 없다. 접미사를 추측해서 붙이지 말고 사용자에게 규칙을 확인한 뒤 이 문서를 갱신한다.

## Vibe transcript 매칭 규칙

회의 녹음은 로컬 앱 Vibe로 진행한다 (Fireflies 대체, 2026-09-21부터). Vibe는 로컬 앱이라 자동 pull이 안 되므로, 사용자가 Vibe에서 만든 transcript 파일/텍스트를 직접 전달하면 **회의 제목**의 키워드로 저장 위치를 결정한다. 위에서부터 순서대로 검사하고 처음 맞는 규칙을 적용한다.

| 순서 | 제목 키워드 | 저장 위치 | 추가 규칙 |
|---|---|---|---|
| 1 | `1:1` 또는 `1on1` 포함 | `1on1/<이름>/` | 참석자 이름으로 `<이름>` 폴더 매칭 (본인 제외한 상대방) |
| 2 | `이벤트 리뷰` 포함 | `event-review/` | - |
| 3 | `아이디에이션` 포함 | `ideation/` | - |
| 4 | `그로스` 포함 | `growth-meeting/` | - |

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
| 그 외 미매칭 | `dbInCorpMeeting` | Name=회의 제목, Tags=`Team`, Date, Person=사용자 본인 | 없음 |

- 본문은 해당 DB 템플릿의 구조(제목/항목)에 transcript 내용을 채워 넣는다. `create-pages`는 `template_id`와 `content`를 같이 못 쓰므로, 템플릿 페이지를 fetch해 구조를 복제한 content로 만든다. 템플릿이 없는 노트는 요약 / 주요 논의 / 결정 / 액션 아이템 구조로 쓴다.
- `dbTodos`의 Status, Due, Priority 등 위에 적지 않은 속성은 사용자가 정하기 전까지 비워둔다.
- Vibe는 봇 없는 로컬 녹음이라 화자 이름이 자동으로 붙지 않는다. 1on1 상대방 이름이 화자 라벨(Speaker 1/2)로만 나오면 임의로 붙이지 않고 사용자에게 확인한다.
- Notion 페이지를 만들기 전에 같은 날짜·같은 Name의 페이지가 이미 있는지 검색하고, 있으면 새로 만들지 않고 사용자에게 확인한다.

## 미매칭 처리 (No Assumptions)

아래 경우에는 임의로 분류하거나 새 폴더를 만들지 않고 사용자에게 먼저 확인한다.

- 어떤 키워드에도 맞지 않는 제목: Notion은 위 표대로 `dbInCorpMeeting`에 넣지만, **로컬 md 저장 위치**는 정해진 폴더가 없으므로 사용자에게 확인한다.
- 1on1인데 참석자가 `_index.md`에 등록된 상대방과 일치하지 않는 경우 (신규 팀원 폴더가 생기기 전까지는 그 사람의 1on1도 여기에 해당). 이 경우 Notion 페이지도 이름 확인 후에 만든다.

## 갱신 절차

- 원온원 상대방이 확정/변경되면 `1on1/<이름>/` 폴더를 만들고 `_index.md`의 명단 표를 갱신한다.
- 카테고리나 키워드가 바뀌면 이 문서의 매칭 표와 `_index.md`의 빈도표를 함께 갱신한다.
