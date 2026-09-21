"""연도별 6~8월 국내 국제학교별 고유 Contact 표.

WHY: 'Contact 감소가 특정 국내 국제학교에 몰렸는지, 전반적인지'를 보려면 같은 학교를 하나로 묶고
해외 학교를 걸러낸 학교별 집계가 필요하다. 연도 안에서 같은 이메일은 1명으로 센다(여러 웨비나 중복 제거).
"""
import pandas as pd

import config
import school_normalize
from load_campaign_members import load_all

# 한 사람이 여러 웨비나에서 다른 학교명을 적었을 때, 더 확실한 매핑의 행을 남긴다
TIER_RANK = {"user": 0, "list": 0, "proposed": 1, "ambiguous": 2, "unmapped": 3, "unknown": 4}


def unique_contacts() -> pd.DataFrame:
    d = load_all()
    d = d[d["campaign_month"].isin(config.TARGET_MONTHS)]
    d = school_normalize.apply(d)
    d["_rank"] = d["match_tier"].map(TIER_RANK)
    d = d.sort_values("_rank").drop_duplicates(["campaign_year", "Email"])
    return d.drop(columns="_rank")


def coverage(d: pd.DataFrame) -> pd.DataFrame:
    """범위별 고유 Contact 수 (국내 국제학교 / 한국 소재 다른 Type / 해외 / 분류불가)."""
    return d.pivot_table(index="scope", columns="campaign_year", values="Email", aggfunc="size", fill_value=0)


def school_table(d: pd.DataFrame) -> pd.DataFrame:
    dom = d[d["scope"] == "domestic"]
    yrs = sorted(d["campaign_year"].unique())
    p = dom.pivot_table(index="school", columns="campaign_year", values="Email", aggfunc="size", fill_value=0)
    for y in yrs:
        if y not in p.columns:
            p[y] = 0
    prop = dom[dom["match_tier"] == "proposed"].pivot_table(
        index="school", columns="campaign_year", values="Email", aggfunc="size", fill_value=0).reindex(p.index, fill_value=0)
    p["total"] = p[yrs].sum(axis=1)
    p["proposed_incl"] = prop.sum(axis=1)   # 합계 중 내가 제안한 별칭(확인 전)으로 묶인 수
    p["d_25_26"] = p[2026] - p[2025]
    return p


# ---- 테스트 ----
def test_scope_sums_match_unique_contacts():
    d = unique_contacts()
    c = coverage(d)
    for y, n in d.groupby("campaign_year").size().items():
        assert c[y].sum() == n, f"{y}: 범위별 합 {c[y].sum()} != 고유 연락처 {n}"


def test_school_table_sums_match_domestic_scope():
    d = unique_contacts()
    p = school_table(d)
    c = coverage(d)
    for y in (2024, 2025, 2026):
        assert p[y].sum() == c.loc["domestic", y], f"{y}: 학교별 합 != domestic 범위 합"


def test_no_duplicate_email_within_year():
    d = unique_contacts()
    assert not d.duplicated(["campaign_year", "Email"]).any()


if __name__ == "__main__":
    test_scope_sums_match_unique_contacts()
    test_school_table_sums_match_domestic_scope()
    test_no_duplicate_email_within_year()
    print("모든 테스트 통과")
