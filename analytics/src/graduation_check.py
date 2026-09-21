"""졸업이 6~8월 Contact 감소를 설명하는지 확인한다.

WHY: 사용자 가설은 '졸업해서 더 이상 정보가 필요 없어진 사람들이 빠졌다'이다. 멤버 리포트의 학년 필드는
사람당 값 하나이고 해마다 올라가지 않아서, 그 사람이 처음 데이터에 나온 해의 학년으로 보고 해마다 +1 한
'추정 학년'으로 졸업 예상자를 나눈다. 졸업 예상자와 재학 중인 학생의 재참석률이 연도별로 어떻게 달라졌는지,
그리고 졸업 구성 변화만으로 잃은 재참석자가 얼마나 설명되는지를 계산한다.
주의: 추정이다. 실제 졸업연도 필드가 있으면 그것으로 대체해야 한다.
"""
import re

import numpy as np
import pandas as pd

import config
import regular_retention as rr
from load_campaign_members import load_all

_GRADE_RE = re.compile(r"^(?:grade\s*)?(\d{1,2})\s*(?:학년)?(?:\s*[\(/].*)?$")


def parse_grade(value):
    """'9', 'Grade 11', '10학년', 'grade 11 (高校2年生)', 'grade 9/ year 10' -> 정수 학년. 그 외(졸업연도 2030, Year N, 1900 등)는 NaN."""
    if value is None or pd.isna(value):
        return np.nan
    s = str(value).strip().lower()
    if s.startswith("year"):
        return np.nan
    m = _GRADE_RE.match(s)
    if not m:
        return np.nan
    n = int(m.group(1))
    return n if config.GRADE_MIN <= n <= config.GRADE_MAX else np.nan


def grade_group(n) -> str:
    if pd.isna(n):
        return "missing"
    if n <= 8:
        return "<=8"
    if n == 9:
        return "9"
    return "10-11" if n <= 11 else "12+"


def summer_members(df: pd.DataFrame) -> pd.DataFrame:
    """6~8월 전체 멤버(모든 상태). 학년과 첫 등장 연도는 미국 공동 이벤트를 포함한 이 집합에서 정한다."""
    return df[df["campaign_month"].isin(config.TARGET_MONTHS)]


def person_grade(members: pd.DataFrame) -> pd.Series:
    """이메일별 파싱된 학년의 최빈값 (없으면 NaN)."""
    g = members[config.GRADE_COLUMN].map(parse_grade)
    return g.groupby(members["Email"]).agg(lambda s: s.dropna().mode().iloc[0] if s.dropna().size else np.nan)


def first_seen_year(members: pd.DataFrame) -> pd.Series:
    return members.groupby("Email")["campaign_year"].min()


def status_next_summer(email, y0, pg, first) -> str:
    """y0 여름의 추정 학년로 다음 여름 전 졸업 여부를 분류: graduated / in_school / missing."""
    g0 = pg.get(email, np.nan)
    if pd.isna(g0):
        return "missing"
    est = g0 + (y0 - first[email])
    return "graduated" if est >= config.GRADUATION_EST_GRADE else "in_school"


def retention_by_status(counts, pg, first, y0, y1) -> dict:
    """{'graduated': (돌아온 수, 전년 참석자 수), 'in_school': ..., 'missing': ...}"""
    back = rr.attendees(counts, y1)
    out = {k: [0, 0] for k in ("graduated", "in_school", "missing")}
    for e in rr.attendees(counts, y0):
        k = status_next_summer(e, y0, pg, first)
        out[k][1] += 1
        out[k][0] += e in back
    return {k: tuple(v) for k, v in out.items()}


def composition_expected(prev: dict, now: dict) -> float:
    """전년 전환(prev)의 그룹별 재참석률을 올해 그룹 구성(now)에 적용한 기대 재참석자 수.
    학년 정보 없음은 전년 전체 재참석률을 쓴다."""
    tot_k = sum(k for k, _ in prev.values())
    tot_n = sum(n for _, n in prev.values())
    overall = tot_k / tot_n
    exp = 0.0
    for grp, (_, n_now) in now.items():
        k0, n0 = prev[grp]
        rate = overall if grp == "missing" or n0 == 0 else k0 / n0
        exp += rate * n_now
    return exp


def registered_by_grade(members: pd.DataFrame, pg: pd.Series) -> pd.DataFrame:
    """연도별 등록 Contact(고유 이메일)의 학년 그룹 분포."""
    u = members.drop_duplicates(["campaign_year", "Email"]).copy()
    u["g"] = u["Email"].map(pg).map(grade_group)
    return u.pivot_table(index="g", columns="campaign_year", values="Email", aggfunc="size",
                         fill_value=0).reindex(config.GRADE_GROUPS, fill_value=0)


def new_attendee_grades(counts, pg, y0, y1) -> dict:
    """y1 참석자 중 y0 6~8월 참석 기록이 없는 신규의 학년 그룹 분포."""
    new = rr.attendees(counts, y1) - rr.attendees(counts, y0)
    s = pd.Series([grade_group(pg.get(e, np.nan)) for e in new]).value_counts()
    return {g: int(s.get(g, 0)) for g in config.GRADE_GROUPS}


# ---- 테스트: 기대값과 실제값 비교 ----
def test_parse_grade():
    assert parse_grade("9") == 9 and parse_grade(" 12 ") == 12
    assert parse_grade("Grade 11") == 11 and parse_grade("10학년") == 10
    assert parse_grade("grade 11 (高校2年生)") == 11 and parse_grade("grade 9/ year 10") == 9
    for bad in ("2030", "2027년", "1900", "year 9", "other", "e.g. 2024", "28", None, np.nan, "1"):
        assert pd.isna(parse_grade(bad)), bad


def test_grade_group():
    assert [grade_group(x) for x in (np.nan, 8, 9, 10, 11, 12, 13)] == ["missing", "<=8", "9", "10-11", "10-11", "12+", "12+"]


def _toy():
    rows = []
    def add(y, e, grade, camp="W", status="Attended", month=7):
        rows.append({"campaign_year": y, "campaign_month": month, "Email": e, "Campaign Name": camp,
                     "Member Status": status, "Country": "South Korea", config.GRADE_COLUMN: grade})
    add(2024, "a", "12"); add(2024, "b", "10"); add(2024, "c", "10"); add(2024, "d", None)
    add(2025, "b", "10"); add(2025, "e", "9")                       # b만 돌아옴, e는 신규
    return pd.DataFrame(rows)


def test_status_and_retention_toy():
    df = _toy()
    m = summer_members(df)
    pg, first = person_grade(m), first_seen_year(m)
    assert status_next_summer("a", 2024, pg, first) == "graduated"     # 12학년 -> 졸업 예상
    assert status_next_summer("b", 2024, pg, first) == "in_school"
    assert status_next_summer("d", 2024, pg, first) == "missing"
    c = rr.attended_counts(rr.prepare(df))
    assert retention_by_status(c, pg, first, 2024, 2025) == {"graduated": (0, 1), "in_school": (1, 2), "missing": (0, 1)}


def test_entry_year_adjustment():
    # 2024에 11학년으로 처음 나온 사람은 2025 여름에는 12학년으로 추정되어 다음 여름 전 졸업 예상
    df = pd.DataFrame([
        {"campaign_year": 2024, "campaign_month": 7, "Email": "x", "Campaign Name": "W", "Member Status": "Attended",
         "Country": "South Korea", config.GRADE_COLUMN: "11"},
        {"campaign_year": 2025, "campaign_month": 7, "Email": "x", "Campaign Name": "W", "Member Status": "Attended",
         "Country": "South Korea", config.GRADE_COLUMN: "11"}])
    m = summer_members(df)
    pg, first = person_grade(m), first_seen_year(m)
    assert status_next_summer("x", 2024, pg, first) == "in_school"
    assert status_next_summer("x", 2025, pg, first) == "graduated"


def test_composition_expected_toy():
    prev = {"graduated": (2, 10), "in_school": (40, 100), "missing": (1, 10)}      # 전체 43/120
    now = {"graduated": (0, 20), "in_school": (0, 80), "missing": (0, 10)}
    exp = composition_expected(prev, now)
    assert abs(exp - (0.2 * 20 + 0.4 * 80 + (43 / 120) * 10)) < 1e-9


def test_registered_and_new_toy():
    df = _toy()
    m = summer_members(df)
    pg = person_grade(m)
    t = registered_by_grade(m, pg)
    assert t.loc["12+", 2024] == 1 and t.loc["10-11", 2024] == 2 and t.loc["missing", 2024] == 1 and t.loc["9", 2025] == 1
    c = rr.attended_counts(rr.prepare(df))
    assert new_attendee_grades(c, pg, 2024, 2025) == {"<=8": 0, "9": 1, "10-11": 0, "12+": 0, "missing": 0}


def test_real_data_regression():
    # 2026-09-22 임시 계산으로 확인한 값과 같아야 한다 (리포트가 바뀌면 이 값도 검토 대상)
    df = load_all()
    m = summer_members(df)
    pg, first = person_grade(m), first_seen_year(m)
    c = rr.attended_counts(rr.prepare(df))
    assert retention_by_status(c, pg, first, 2024, 2025) == {"graduated": (4, 21), "in_school": (60, 146), "missing": (1, 1)}
    assert retention_by_status(c, pg, first, 2025, 2026) == {"graduated": (9, 44), "in_school": (40, 165), "missing": (2, 28)}
    t = registered_by_grade(m, pg)
    assert t[2024].tolist() == [29, 63, 156, 35, 3]
    assert t[2025].tolist() == [57, 88, 154, 20, 44]
    assert t[2026].tolist() == [42, 48, 66, 6, 69]
    assert new_attendee_grades(c, pg, 2025, 2026) == {"<=8": 18, "9": 21, "10-11": 21, "12+": 2, "missing": 41}


def test_real_data_graduation_does_not_explain_drop():
    # 졸업 예상자의 재참석률은 두 해 모두 비슷하고, 재학생의 재참석률이 크게 떨어졌다. 구성 효과는 작다.
    df = load_all()
    m = summer_members(df)
    pg, first = person_grade(m), first_seen_year(m)
    c = rr.attended_counts(rr.prepare(df))
    r1, r2 = retention_by_status(c, pg, first, 2024, 2025), retention_by_status(c, pg, first, 2025, 2026)
    rate = lambda t: t[0] / t[1]
    assert abs(rate(r1["graduated"]) - rate(r2["graduated"])) < 0.05
    assert rate(r1["in_school"]) - rate(r2["in_school"]) > 0.10
    overall_prev = sum(k for k, _ in r1.values()) / sum(n for _, n in r1.values())
    naive = overall_prev * sum(n for _, n in r2.values())
    adjusted = composition_expected(r1, r2)
    actual = sum(k for k, _ in r2.values())
    assert (naive - adjusted) < 0.25 * (naive - actual)     # 구성 변화가 잃은 재참석자의 1/4 미만


if __name__ == "__main__":
    for t in [v for k, v in sorted(globals().items()) if k.startswith("test_")]:
        t()
    print("모든 테스트 통과")
    df = load_all()
    m = summer_members(df)
    pg, first = person_grade(m), first_seen_year(m)
    c = rr.attended_counts(rr.prepare(df))
    print("\n[연도별 등록 Contact(고유) 학년 그룹]")
    print(registered_by_grade(m, pg).to_string())
    res = {}
    for y0, y1 in ((2024, 2025), (2025, 2026)):
        res[(y0, y1)] = retention_by_status(c, pg, first, y0, y1)
        print(f"\n[{y0}->{y1}] 전년 참석자의 다음 해 재참석 (추정 학년 기준)")
        for k, (b, n) in res[(y0, y1)].items():
            print(f"  {k}: {b}/{n} ({b / n * 100:.0f}%)" if n else f"  {k}: -")
    r1, r2 = res[(2024, 2025)], res[(2025, 2026)]
    overall_prev = sum(k for k, _ in r1.values()) / sum(n for _, n in r1.values())
    n_now = sum(n for _, n in r2.values())
    naive, adjusted, actual = overall_prev * n_now, composition_expected(r1, r2), sum(k for k, _ in r2.values())
    print(f"\n2025 참석자 {n_now}명에 2024->25 재참석률 적용: 전체 비율 기준 기대 {naive:.0f}명, 졸업/재학 구성 반영 기대 {adjusted:.0f}명, 실제 {actual}명")
    print(f"  잃은 재참석자 {naive - actual:.0f}명 중 구성 변화로 설명되는 것: 약 {naive - adjusted:.0f}명")
    print("\n[신규 참석자 학년 그룹]")
    for y0, y1 in ((2024, 2025), (2025, 2026)):
        print(f"  {y1}: {new_attendee_grades(c, pg, y0, y1)}")
