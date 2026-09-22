"""연도별 웨비나 볼륨과 웨비나당 Contact 볼륨.

WHY: 전체 Contact 수는 2025에 늘었다가 2026에 줄었는데, 웨비나 수도 해마다 늘었다(6 -> 13 -> 18).
전체 합계만 보면 2025는 증가로 보이지만 웨비나당으로 보면 이미 줄고 있었다. '2026에 감소 폭이 더 깊어졌다'는
서술은 웨비나당 볼륨으로 봐야 정확하다. 미국 공동 이벤트(사용자 기준 제외 대상) 포함/제외 두 버전을 함께 낸다.
등록 = Registration Error를 뺀 멤버, 이메일x캠페인 중복 제거. 월은 캠페인명의 WB-YYYY-MM 기준.
"""
import pandas as pd

import config
from load_campaign_members import load_all


def volume_table(df: pd.DataFrame, exclude_campaigns: bool = False) -> pd.DataFrame:
    d = df[df["campaign_month"].isin(config.TARGET_MONTHS)]
    if exclude_campaigns:
        d = d[~d["Campaign Name"].isin(config.EXCLUDED_CAMPAIGNS)]
    d = d.drop_duplicates(["campaign_year", "Email", "Campaign Name"])
    reg = d[d["Member Status"] != "Registration Error"]
    g = reg.groupby("campaign_year")
    out = pd.DataFrame({"webinars": g["Campaign Name"].nunique(), "contact_regs": g.size(),
                        "unique_contacts": g["Email"].nunique()})
    out["attended"] = d[d["Member Status"] == "Attended"].groupby("campaign_year").size()
    out["attended"] = out["attended"].fillna(0).astype(int)
    out["regs_per_webinar"] = out["contact_regs"] / out["webinars"]
    out["attended_per_webinar"] = out["attended"] / out["webinars"]
    return out


def pct_changes(out: pd.DataFrame, col: str) -> dict:
    """(뒤 해 / 앞 해 - 1) 비율. 키: '2025 vs 2024', '2026 vs 2025', '2026 vs 2024'."""
    v = out[col]
    return {"2025 vs 2024": v[2025] / v[2024] - 1, "2026 vs 2025": v[2026] / v[2025] - 1,
            "2026 vs 2024": v[2026] / v[2024] - 1}


# ---- 테스트: 기대값과 실제값 비교 ----
def _toy():
    rows = []
    def add(y, e, camp, status):
        rows.append({"campaign_year": y, "campaign_month": 7, "Email": e, "Campaign Name": camp, "Member Status": status})
    add(2024, "a", "A1", "Attended"); add(2024, "b", "A1", "No Show")
    add(2025, "a", "B1", "Attended"); add(2025, "a", "B1", "Attended")      # 중복 행은 1건
    add(2025, "c", "B2", "Attended"); add(2025, "d", "B2", "Registration Error")   # 오류는 등록에서 제외
    add(2026, "a", "C1", "Attended")
    return pd.DataFrame(rows)


def test_volume_toy():
    v = volume_table(_toy())
    assert v.loc[2024, ["webinars", "contact_regs", "unique_contacts", "attended"]].tolist() == [1, 2, 2, 1]
    assert v.loc[2025, ["webinars", "contact_regs", "unique_contacts", "attended"]].tolist() == [2, 2, 2, 2]
    assert v.loc[2025, "regs_per_webinar"] == 1.0


def test_pct_changes_toy():
    v = volume_table(_toy())
    ch = pct_changes(v, "regs_per_webinar")           # 2024: 2/1=2, 2025: 2/2=1, 2026: 1/1=1
    assert abs(ch["2025 vs 2024"] - (-0.5)) < 1e-9 and abs(ch["2026 vs 2025"]) < 1e-9


def test_excluded_campaign_toy():
    df = _toy()
    df.loc[len(df)] = {"campaign_year": 2025, "campaign_month": 7, "Email": "z",
                       "Campaign Name": config.EXCLUDED_CAMPAIGNS[0], "Member Status": "Attended"}
    assert volume_table(df).loc[2025, "webinars"] == 3
    assert volume_table(df, exclude_campaigns=True).loc[2025, "webinars"] == 2


def test_real_data_regression():
    # 2026-09-22 임시 계산으로 확인한 값과 같아야 한다 (리포트가 바뀌면 이 값도 검토 대상)
    v = volume_table(load_all())
    assert v["webinars"].tolist() == [6, 13, 18]
    assert v["contact_regs"].tolist() == [470, 853, 529]
    assert v["unique_contacts"].tolist() == [283, 362, 231]
    assert v["attended"].tolist() == [240, 567, 283]
    x = volume_table(load_all(), exclude_campaigns=True)
    assert x["webinars"].tolist() == [6, 12, 18]
    assert x["contact_regs"].tolist() == [470, 768, 529]
    assert x["attended"].tolist() == [240, 519, 283]


def test_real_data_drop_deepens_in_2026():
    # 사용자 서술의 근거: 웨비나당 등록이 2025에 줄고 2026에 더 크게 준다
    ch = pct_changes(volume_table(load_all()), "regs_per_webinar")
    assert ch["2025 vs 2024"] < 0 and ch["2026 vs 2025"] < ch["2025 vs 2024"]


if __name__ == "__main__":
    for t in [v for k, v in sorted(globals().items()) if k.startswith("test_")]:
        t()
    print("모든 테스트 통과")
    for title, ex in (("전체 6~8월 웨비나", False), ("2025-08-23 미국 공동 이벤트 제외", True)):
        v = volume_table(load_all(), exclude_campaigns=ex)
        print(f"\n[{title}]")
        print(v.round(1).to_string())
        for col in ("regs_per_webinar", "attended_per_webinar"):
            ch = pct_changes(v, col)
            print(f"  {col}: " + " | ".join(f"{k} {x * 100:+.0f}%" for k, x in ch.items()))
