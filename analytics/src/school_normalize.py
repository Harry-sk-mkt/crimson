"""학교명 자유 입력을 사용자 제공 학교 목록으로 대표 학교에 묶고, 국내 국제학교 범위 여부를 붙인다.

WHY: Salesforce의 School Name이 자유 입력이라 같은 학교가 'kis', 'KIS PANGYO', '채드', '체드윅' 등으로
흩어져 있고, 분석 대상은 국내 국제학교뿐이라 해외 학교를 걸러내야 한다. 기준은 사용자가 준 워크북의
'P1 School List'(School + Similar Name + Type)이고, 여기서 해결 안 되는 보정만 school_aliases.py에 있다.

결과 컬럼
- school: 대표 학교 이름 (못 묶으면 정규화한 원문)
- match_tier: user / list / proposed / ambiguous / unmapped / unknown
- scope: domestic(국내 국제학교) / korea_other(한국 소재인데 Type이 다름) / overseas / unclassified
"""
import re
import unicodedata

import pandas as pd

import config
import school_aliases as sa


def normalize_key(value) -> str:
    """소문자, 전각 정리(NFKC), 연속 공백 하나로."""
    if value is None or pd.isna(value):
        return ""
    s = unicodedata.normalize("NFKC", str(value)).strip().lower()
    return re.sub(r"\s+", " ", s)


def _read_school_list() -> pd.DataFrame:
    """워크북 학교 목록 -> 컬럼: school, type, country, aliases(list[str])."""
    files = sorted(config.DATA_DIR.glob(config.SCHOOL_MAP_GLOB))
    if not files:
        raise FileNotFoundError(f"{config.DATA_DIR}에 {config.SCHOOL_MAP_GLOB} 파일이 없다")
    raw = pd.read_excel(files[0], sheet_name=config.SCHOOL_MAP_SHEET, header=None)
    h = next(i for i in range(len(raw)) if (raw.iloc[i] == config.SCHOOL_MAP_HEADER_ANCHOR).any())
    labels = [str(v).strip() if pd.notna(v) else "" for v in raw.iloc[h]]
    above = raw.iloc[h - 1].tolist()
    sim_start = next(j for j, v in enumerate(above) if pd.notna(v) and str(v).strip() == config.SIMILAR_NAME_ANCHOR)
    i_school, i_type, i_country = (labels.index(c) for c in
                                   (config.SCHOOL_COL_NAME, config.SCHOOL_COL_TYPE, config.SCHOOL_COL_COUNTRY))
    rows = []
    for _, r in raw.iloc[h + 1:].iterrows():
        if pd.isna(r.iloc[i_school]):
            continue
        sims = [str(v).strip() for v in r.iloc[sim_start:] if pd.notna(v) and str(v).strip()]
        rows.append({"school": str(r.iloc[i_school]).strip(),
                     "type": r.iloc[i_type] if pd.notna(r.iloc[i_type]) else "",
                     "country": r.iloc[i_country] if pd.notna(r.iloc[i_country]) else "",
                     "aliases": sims})
    return pd.DataFrame(rows)


def _scope_of(school_type: str, country: str) -> str:
    if school_type in config.DOMESTIC_INTL_TYPES:
        return "domestic"
    if country == config.KOREA_COUNTRY_LABEL:
        return "korea_other"
    return "overseas"


def _build():
    lst = _read_school_list()
    canon = lambda name: sa.SCHOOL_MERGES.get(name, name)
    info = {}                                   # 대표 학교 -> scope
    for _, r in lst.iterrows():
        info[canon(r["school"])] = _scope_of(r["type"], r["country"])
    for name in sa.DOMESTIC_SCOPE_EXTRA_SCHOOLS:
        assert name in info, f"범위 예외 학교 '{name}'가 학교 목록에 없다"
        info[name] = "domestic"
    cands = {}                                  # 정규화 별칭 -> 후보 학교 집합
    for _, r in lst.iterrows():
        for a in [r["school"]] + r["aliases"]:
            cands.setdefault(normalize_key(a), set()).add(canon(r["school"]))
    return info, cands


SCHOOL_SCOPE, _CANDIDATES = _build()
_UNKNOWN = {normalize_key(v) for v in sa.UNKNOWN_VALUES} | {""}


def _canon(name: str) -> str:
    return sa.SCHOOL_MERGES.get(name, name)


def canonical_school(value):
    """(대표 이름, 등급, 범위) 반환."""
    key = normalize_key(value)
    if key in _UNKNOWN:
        return sa.UNKNOWN_LABEL, "unknown", "unclassified"
    if key in {normalize_key(k) for k in sa.USER_CONFIRMED_ALIASES}:
        name = _canon(next(v for k, v in sa.USER_CONFIRMED_ALIASES.items() if normalize_key(k) == key))
        return name, "user", SCHOOL_SCOPE[name]
    if key in _CANDIDATES:
        names = sorted(_CANDIDATES[key])
        scopes = {SCHOOL_SCOPE[n] for n in names}
        if len(names) == 1:
            return names[0], "list", SCHOOL_SCOPE[names[0]]
        if len(scopes) == 1:                    # 후보가 여러 개여도 범위가 같으면 범위는 확정 (예: Fayston 두 캠퍼스)
            return " / ".join(names), "list", scopes.pop()
        return " / ".join(names), "ambiguous", "unclassified"   # 국내/해외에 걸침 (예: isb, mca)
    proposed = {normalize_key(k): v for k, v in sa.PROPOSED_ALIASES.items()}
    if key in proposed:
        name = _canon(proposed[key])
        return name, "proposed", SCHOOL_SCOPE[name]
    return key, "unmapped", "unclassified"


def apply(df: pd.DataFrame, col: str = "School Name") -> pd.DataFrame:
    out = df.copy()
    res = out[col].map(canonical_school)
    out["school"] = res.map(lambda r: r[0])
    out["match_tier"] = res.map(lambda r: r[1])
    out["scope"] = res.map(lambda r: r[2])
    return out


# ---- 테스트: 기대값과 실제값 비교 ----
def test_list_has_domestic_schools():
    n = sum(1 for s in SCHOOL_SCOPE.values() if s == "domestic")
    # 워크북 Type=국제_국내 40개에서 KIS 두 행을 하나로 합쳐 39, 사용자 승인 예외 3개 추가 = 42
    assert n == 42, f"국내 국제학교 수 {n} != 42"


def test_kis_rules_from_user():
    pangyo = "Korea International School PANGYO"
    assert canonical_school("KIS") == (pangyo, "user", "domestic")
    assert canonical_school("Korea International School")[0] == pangyo      # 합쳐진 행
    assert canonical_school("kis pangyo")[0] == pangyo
    assert canonical_school("KISJ")[0] == "Korea International School Jeju"
    assert canonical_school("kis  jeju")[0] == "Korea International School Jeju"   # 공백 두 칸


def test_list_similar_names():
    assert canonical_school("채드")[0] == "Chadwick International School"
    assert canonical_school("체드윅")[0] == "Chadwick International School"
    assert canonical_school("NLCS")[0] == "North London Collegiate School Jeju"


def test_user_confirmed_abbreviations():
    assert canonical_school("BHA") == ("Branksome Hall Asia", "user", "domestic")
    assert canonical_school("SSI")[0] == "Seoul Scholars International"
    assert canonical_school("kkfs")[0] == "korea kent foreign school"
    # 워크북 Similar Name의 DIS(Dominican Taipei)보다 사용자 정정(대구)이 우선
    assert canonical_school("DIS") == ("Daegu International School", "user", "domestic")
    assert canonical_school("채드윅")[1] == "user"
    assert canonical_school("sis")[1] == "user"


def test_scope_extra_schools_are_domestic():
    assert canonical_school("sja")[2] == "domestic"
    assert canonical_school("Dwight school seoul")[2] == "domestic"
    assert canonical_school("Korean Minjok Leadership Academy")[2] == "domestic"


def test_second_round_confirmed_aliases():
    assert canonical_school("NL")[0] == "North London Collegiate School Jeju"
    assert canonical_school("BIS") == ("International School of Busan", "user", "domestic")
    assert canonical_school("민사고")[0] == canonical_school("민사")[0] == "Korean Minjok Leadership Academy"
    assert canonical_school("Fayston Preparatory of Suji")[0] == "Fayston Preparatory School of Suji"


def test_proposed_tier_is_flagged_when_used():
    # 제안 별칭이 없으면 이 등급은 나오지 않는다. 등급 로직은 임시 항목으로 검증
    sa.PROPOSED_ALIASES["zz test school"] = "Seoul International School"
    try:
        assert canonical_school("zz test school") == ("Seoul International School", "proposed", "domestic")
    finally:
        del sa.PROPOSED_ALIASES["zz test school"]


def test_ambiguous_across_domestic_and_overseas():
    name, tier, scope = canonical_school("isb")
    assert (tier, scope) == ("ambiguous", "unclassified")


def test_overseas_and_unknown_and_unmapped():
    assert canonical_school("Choate")[2] in ("unclassified",)     # 목록에 없으면 미분류
    assert canonical_school(None) == (sa.UNKNOWN_LABEL, "unknown", "unclassified")
    assert canonical_school("미정")[1] == "unknown"


def test_proposed_targets_exist_in_list():
    for k, v in {**sa.USER_CONFIRMED_ALIASES, **sa.PROPOSED_ALIASES}.items():
        assert _canon(v) in SCHOOL_SCOPE, f"별칭 '{k}'의 대상 '{v}'가 학교 목록에 없다"


def test_apply_preserves_row_count():
    df = pd.DataFrame({"School Name": ["kis", "KIS", None, "채드", "zzz"]})
    out = apply(df)
    assert len(out) == len(df)
    assert out["scope"].tolist() == ["domestic", "domestic", "unclassified", "domestic", "unclassified"]


if __name__ == "__main__":
    for t in [v for k, v in sorted(globals().items()) if k.startswith("test_")]:
        t()
    print("모든 테스트 통과")
