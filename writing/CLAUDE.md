# writing/

글 작성 도메인입니다 (2026-09-23 생성). 블로그는 `blog/`, 회의 transcript 정리는 `meetings/`가 맡으므로 여기서 다루지 않습니다.

## 하는 일

### 1. 외부 배포 소재 검수·보완

이미 쓴 외부 배포용 카피를 검수하고 보완합니다. 소재는 Notion에 있습니다.

| 라이브러리 | DB (data source) | 주요 속성 |
|---|---|---|
| [Copy Library](https://app.notion.com/p/3c364dfd498f8077be3cce74858c346b) | `db_copy` (`collection://3c364dfd-498f-805c-aa5b-000bcb110b8a`) | Name, Segment(Content/Seminar/Webinar/BOFU/Search), Person, `isReviewed`, Launch, Marketo, LG (UTM), LP, Feed, Landscape, Storyblok |
| [Kakao Library](https://app.notion.com/p/19064dfd498f802fbfd5d5650b0c50e7) | `dbKakao` (`collection://19064dfd-498f-80ac-8e28-000b1e6078de`) | Name, For(Webinar/Seminar/BOFU), Type(TY/Ads/News/Final Reminder/SMS), SentAt, Person |

`dbKakao`에는 Type별 템플릿이 있습니다 (TY message, Seminar/Webinar Final reminder, Seminar/Webinar Ads, Seminar/Webinar news, 모두 v.0.0.1.). Kakao는 형태가 아직 정의되지 않았으므로 Copy를 먼저 구축한 뒤 다룬다 (2026-09-23 사용자 확정).

**Copy 검수 흐름 (사용자 작업 방식, 2026-09-23 확인)**: 사용자가 소재를 읽고 수정한 뒤, 원래 내용은 페이지 안 `legacy` 토글에 넣고 본문에는 배포할 버전만 남긴 다음 `isReviewed`를 체크한다. 일부 페이지는 토글 이름이 `before review`다.

**검수 기준**: Quality Bar(Creative & funnel)를 먼저 적용한다. 애매한 표현은 규칙으로 모두 나열하거나 예외 처리할 수 없으므로, legacy와 최종본의 차이를 학습해서 판단한다. 학습 결과는 `copy-review-patterns.md`에 쌓는다. 새로 `isReviewed`가 체크된 페이지에 legacy 토글이 있으면 비교해서 이 파일을 갱신한다.

### 2. Ideation 작성

아이디에이션 문서를 작성합니다. 회의 transcript를 정리하는 일은 `meetings/`, 아이디어 문서 자체를 쓰는 일은 여기입니다.

- 위치: `dbTodos` (`collection://2907cc28-daa4-4494-9ab6-ad4a6dd0a3dd`), Type=`Ideation`
- 템플릿: `Ideation_2.3.2` (`bc1b4f40-f720-4891-8318-1ae1ce11c254`). 7단계: 1 아이디어 배경(현상 및 문제), 2 아이디어 설명(5W1H), 3 가설, 4 검증(Metrics), 5 평가(ICE System), 6 실행(Practice), 7 보고(Report)

## 아직 정하지 않은 것

첫 실질 작업 때 사용자에게 확인하고 이 문서를 갱신합니다. 추측해서 정하지 않습니다.

- Claude가 검수할 때 제안을 어디에 남기는지 (페이지 본문 직접 수정 + legacy 토글, 코멘트, 로컬 md 초안 등)
- legacy 토글 없이 `isReviewed`가 체크된 페이지의 의미 (수정 없이 통과인지, legacy를 지운 것인지)
- Ideation 초안을 로컬 md로 먼저 쓸지, Notion에 바로 쓸지
