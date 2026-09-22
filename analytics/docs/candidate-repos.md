# 후보 레포 조사 (2026-09-22)

조건: 마케팅 퍼널/코호트, 광고 성과/ROI 분석. 실행은 Python 보조 환경(A안). 입력은 `lead-tracker/` Master 시트.

## 채택 후보

| 순위 | 레포 | 용도 | 라이선스 | 확인 수준 |
|---|---|---|---|---|
| 1 | [pymc-labs/pymc-marketing](https://github.com/pymc-labs/pymc-marketing) | MMM, CLV/BTYD | Apache 2.0 | README 직접 확인. Python ≥ 3.12 필요 |
| 2 | [DavideAltomare/ChannelAttribution](https://github.com/DavideAltomare/ChannelAttribution) | 마르코프 체인 어트리뷰션 (Python/R) | 미확인 | 검색 결과만 |
| 3 | [DP6/Marketing-Attribution-Models](https://github.com/DP6/Marketing-Attribution-Models) | 규칙 기반 어트리뷰션 비교 (기준선) | 미확인 | 검색 결과만 |

MMM 대안인 [google/meridian](https://github.com/google/meridian)과 [facebookexperimental/robyn](https://github.com/facebookexperimental/robyn)은 pymc-marketing과 겹쳐서 보류했다. 하나만 고른다.

## 제외 (이미 lead-tracker에 있음)

- [tarping/ads-to-sheets](https://github.com/tarping/ads-to-sheets): 광고 수집. `lead-tracker/`의 `AD_001~007`이 Meta/Naver/Kakao/Google을 이미 처리한다. 스타 0, 커밋 6개.
- [WildH0g/UnitTestingApp](https://github.com/WildH0g/UnitTestingApp): Apps Script 테스트. 프로젝트에 `testXXXX()` 규칙, pre-commit 검사, QA 에이전트가 이미 있다.

## 참고용

- [naver/searchad-apidoc](https://github.com/naver/searchad-apidoc): Naver 검색광고 API 공식 문서.

## 채택 전 확인할 것

- 2~3번의 라이선스와 최근 커밋 일자
- Master 시트의 기간과 주 단위 데이터 양 (MMM은 일반적으로 긴 시계열과 광고비 변동이 필요하다)
- 마르코프 어트리뷰션에 필요한 터치포인트 순서 데이터가 MTA에 있는지
