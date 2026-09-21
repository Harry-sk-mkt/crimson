# Glossary

`crimson` 마더 프로젝트 전반에서 쓰이는 용어 모음입니다. 도메인별 세부 용어는 각 도메인 문서가 우선하며, 여기서는 여러 도메인이 공유하거나 마더 프로젝트 레벨에서 알아야 할 용어만 다룹니다. 살아있는 문서로, 새 도메인 작업이 진행되며 계속 채워집니다.

## 공통

- **크림슨 (crimson)**: 이 마더 프로젝트 전체를 가리키는 이름. 하위 도메인: `blog`, `lead-tracker`, `meetings`, `email`, `decisions`.
- **도메인 (domain)**: `crimson/` 아래 각 하위 폴더 하나. 독립된 레포이거나(예: `blog`, `lead-tracker`) 아직 구조가 없는 신규 영역(예: `meetings`)일 수 있음.
- **마더 프로젝트 (mother project)**: 여러 도메인을 상위에서 묶는 `crimson/` 자체. 개별 도메인의 세부 구현에는 관여하지 않고, 공통 원칙([[crimson-principles]])과 라우팅([[domain-routing]])만 관리.

## lead-tracker 도메인 (crimson-lead-tracker에서 이관)

- **Raw**: Import 단계에서 저장되는 원본 데이터. 수정 금지, 불변.
- **Master**: Raw로부터 Business Logic을 적용해 재생성되는 데이터. 언제든 재생성 가능.
- **Leads_OPS**: Master 이후 운영 레이어.
- **REP (예: ACQ_REP, FY_REP)**: FY 선택 + Generate 체크박스로 화면을 재작성하는 리포트 시트.

## blog 도메인 (crimson-naver-blog에서 이관)

- (TBD — blog 도메인 고유 용어는 `blog/CLAUDE.md` 및 관련 문서에서 이관 필요, 아직 정리 전)

## meetings / email / decisions 도메인

- (TBD — 아직 도메인 구조가 정의되지 않아 고유 용어 없음)
