"""analytics 설정 단일 지점. 경로/헤더 라벨/캠페인 필터 같은 값은 여기에만 둔다."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

# Salesforce 'Campaigns with Campaign Members' 리포트 내보내기 파일명 패턴
CAMPAIGN_MEMBER_GLOB = "Campaigns with Campaign Members-*.xlsx"

# 리포트는 위에 제목/필터 설명이 있고 헤더 행 위치가 고정이라는 보장이 없어서,
# 이 라벨이 있는 행을 헤더로 찾는다 (컬럼 인덱스를 추측하지 않는다).
HEADER_ANCHOR = "Campaign Name"

# 리포트가 그룹으로 묶어 첫 행에만 값을 채우는 컬럼 (아래로 채워야 하는 컬럼)
GROUPED_COLUMNS = ["Member Type", "Member Status"]

# 멤버 행 판별: 캠페인명이 이 접두사로 시작
CAMPAIGN_PREFIX = "WB-"
CAMPAIGN_YM_PATTERN = r"WB-(\d{4})-(\d{2})"

# 분석 대상 월 (사용자 요청: 6~8월). 필터에는 5월도 있어 기준선으로 남긴다.
TARGET_MONTHS = (6, 7, 8)

# ---- 학교명 매핑 파일 (사용자 제공 'Priority 1 Striker' 워크북) ----
SCHOOL_MAP_GLOB = "*Striker*.xlsx"
SCHOOL_MAP_SHEET = "P1 School List"
SCHOOL_MAP_HEADER_ANCHOR = "Type"        # 이 라벨이 있는 행이 헤더
SCHOOL_COL_TYPE = "Type"
SCHOOL_COL_NAME = "School"
SCHOOL_COL_COUNTRY = "나라"
SIMILAR_NAME_ANCHOR = "Similar Name"     # 헤더 윗행에 있는 라벨. 이 칸부터 오른쪽 끝까지가 이름 변형

# 분석 범위: 국내 국제학교 (사용자 확정 2026-09-22)
DOMESTIC_INTL_TYPES = ("국제_국내",)
KOREA_COUNTRY_LABEL = "한국"             # 나라가 한국인데 Type이 위와 다른 학교는 별도 집계

# ---- 분석에서 제외하는 캠페인 (사용자 확정) ----
# 2025-08-23 이벤트: 미국 팀과 공동 집행이라 리드 대부분이 미국 리드, 국내 해석에 유의미하지 않다 (2026-09-22, docs/background.md)
EXCLUDED_CAMPAIGNS = ("WB-2025-07-KOR-MOFU-Core EC for Each Year of High School",)
KOREA_RESIDENT_LABEL = "South Korea"     # 멤버 Country 값. 한국 거주자만 보는 민감도 분석용

# ---- 이벤트 일정 (연속 참석 분석용) ----
# 사용자 제공 '최근 4주간 이벤트 참석률.xlsx'를 ASCII 이름으로 복사해 둔 파일 (원본은 Downloads에 남아 있음)
EVENT_CALENDAR_FILE = DATA_DIR / "event_attendance_last4weeks.xlsx"
EVENT_CALENDAR_SHEET = "2025"            # 이 시트 오른쪽에 2025와 2026 이벤트 일정/이름이 함께 있다
EVENT_DATE_HEADER = "이벤트 일정"
EVENT_NAME_HEADER = "이벤트 이름"

# 같은 주제를 라이브+레코딩으로 낸 경우, 레코딩을 라이브와 한 이벤트로 본다 (FY27부터의 방식, 사용자 확인)
MERGED_INTO = {
    "WB-2026-07-KOR-MOFU-Core EC for Each Year of High School (Recording)":
        "WB-2026-07-KOR-MOFU-Core EC for Each Year of High School",
}
# Contact 멤버가 이 수보다 적은 이벤트는 연속성 분석에서 뺀다 (2025-08-02 이벤트는 4행뿐). 내 판단이며 사용자 확인 전.
MIN_EVENT_MEMBERS = 10
WEEKLY_MAX_GAP_DAYS = 7                   # 이 일수 이하로 붙어 있는 이벤트 쌍을 '주간 연속'으로 본다

# ---- 학년/졸업 분석 ----
GRADE_COLUMN = "School Year/Grade Level"
GRADE_MIN, GRADE_MAX = 2, 13              # 이 범위의 정수 학년만 인정 (그 밖은 졸업연도 등 다른 형식이라 제외)
# 그 사람이 이 데이터에 처음 나온 해의 학년으로 보고 해마다 +1 한 추정 학년이 이 값 이상이면,
# 다음 여름 전에 졸업한 것으로 본다 (학년 필드가 해마다 갱신되지 않아서 필요한 가정, docs/2026-09-22-graduation-check.md)
GRADUATION_EST_GRADE = 12
GRADE_GROUPS = ("<=8", "9", "10-11", "12+", "missing")
