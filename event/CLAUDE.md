# event/

웨비나·세미나 내용 요약 폴더입니다. 웨비나/세미나 하나당 파일 하나로 저장합니다. 상위 원칙은 `../CLAUDE.md`를 따릅니다.

## 파일 규칙

- `event/YYYY-MM-DD.md` (예: `event/2026-09-30.md`)
- 같은 날짜에 웨비나/세미나가 2번 이상이면 파일명 규칙에 맞는 값이 없다. 접미사를 추측해서 붙이지 말고 사용자에게 확인한 뒤 이 문서를 갱신한다.

## 입력 소스 (Vibe transcript)

녹음/전사는 `meetings/`와 동일하게 로컬 앱 Vibe를 쓴다. 녹음 찾는 법, hallucination loop 대응, 문장 단위 줄바꿈 포맷, 화자 분리 안 됨 등은 `meetings/CLAUDE.md`의 "로컬 Vibe 녹음 찾는 법" 섹션과 동일하게 적용한다 (여기서 중복 서술하지 않음).

## Notion 페이지 생성 (Vibe → Notion)

사용자가 transcript(파일/텍스트)를 전달하며 "정리해줘"라고 요청하면 **로컬 md와 Notion 페이지를 둘 다** 만든다. 자동 실행은 하지 않는다.

- DB: `dbWebinar` (`collection://e600e8af-6fb9-4804-9994-40c047da38fb`), 상위 페이지 `Crimson_marketing / Events`
- 속성: `Title`=웨비나/세미나 제목, `Date`, `EventType`=`Webinar` 또는 `Seminar` (select), `Person`=사용자 본인
- `EventType` 판단: 제목에 "웨비나"/"세미나" 키워드가 있으면 그대로 매칭. 애매하거나 둘 다 없으면 추측하지 말고 사용자에게 확인한다.
- 템플릿 없음(빈 페이지) — 본문은 요약 / 주요 논의 / 결정 / 액션 아이템 구조로 쓴다.
- Notion 페이지를 만들기 전에 같은 날짜·같은 Title의 페이지가 이미 있는지 검색하고, 있으면 새로 만들지 않고 사용자에게 확인한다.

## 갱신 절차

- 카테고리나 Notion 스키마(`dbWebinar` 속성)가 바뀌면 이 문서를 함께 갱신한다.
