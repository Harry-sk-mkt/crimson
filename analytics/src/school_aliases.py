"""학교명 매핑 보정 규칙. 기본 사전은 사용자 제공 워크북(config.SCHOOL_MAP_*)에서 읽고,
여기에는 워크북만으로 해결되지 않는 보정만 둔다 (설정 중앙화).

우선순위: user(사용자 확정) > list(워크북의 School/Similar Name) > proposed(내가 제안, 확인 전).
"""

# 워크북에서 서로 다른 행으로 나뉜 것을 하나의 학교로 합친다: {합쳐질 행 이름: 대표 행 이름}
# 근거: 'kis'만 적혀 있으면 판교라고 사용자가 확정 (2026-09-22, docs/background.md)
SCHOOL_MERGES = {
    "Korea International School": "Korea International School PANGYO",
}

# 사용자가 확정한 별칭: {정규화된 별칭: 워크북 School 이름} (2026-09-22, docs/background.md)
USER_CONFIRMED_ALIASES = {
    # 'kis'만 적혀 있으면 판교, 제주는 kisj / kis jeju
    "kis": "Korea International School PANGYO",
    "kisj": "Korea International School Jeju",
    "kis jeju": "Korea International School Jeju",
    # 약어 확정. 'dis'는 워크북 Similar Name에는 Dominican Taipei로 되어 있으나 사용자가 대구로 정정
    "bha": "Branksome Hall Asia",
    "ssi": "Seoul Scholars International",
    "kkfs": "korea kent foreign school",
    "dis": "Daegu International School",
    # 사용자가 "응"으로 승인한 기존 제안 별칭 (해석은 docs/background.md 참고)
    "채드윅": "Chadwick International School",
    "chadwick": "Chadwick International School",
    "kis 판교": "Korea International School PANGYO",
    "kis판교": "Korea International School PANGYO",
    "제주kis": "Korea International School Jeju",
    "sis": "Seoul International School",
    "yiss": "Yongsan International School of Seoul",
    "sfs": "Seoul Foreign School",
    "sja": "St. Johnsbury Academy Jeju",
    "청심국제고": "Cheongshim International Academy",
    "nlcs jeju": "North London Collegiate School Jeju",
    # 2026-09-22 추가 확정
    "nl": "North London Collegiate School Jeju",
    "bis": "International School of Busan",           # 사용자: busan international. 목록에서 해당하는 학교
    "민사고": "Korean Minjok Leadership Academy",
    "민사": "Korean Minjok Leadership Academy",
    "fayston preparatory of suji": "Fayston Preparatory School of Suji",
}

# 내가 제안한 별칭 (사용자 확인 전). 확인되면 위로 옮기거나 지운다.
PROPOSED_ALIASES = {
}

# 한국 소재이지만 워크북 Type이 국제_국내가 아닌데 국내 국제학교 범위에 넣기로 한 학교 (사용자 승인 2026-09-22)
DOMESTIC_SCOPE_EXTRA_SCHOOLS = [
    "St. Johnsbury Academy Jeju",             # Type: Boarding
    "Dwight school seoul",                    # Type: 국제_해외
    "Korean Minjok Leadership Academy",       # Type: 국내 학교 (국제학교는 아니지만 사용자 승인으로 포함)
]

UNKNOWN_LABEL = "(미입력)"
UNKNOWN_VALUES = ["미정", "?", "-", "n/a", "na", "none"]
