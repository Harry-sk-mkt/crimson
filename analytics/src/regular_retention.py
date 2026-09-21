"""단골(regular) Contact 유지율과 참석자 감소의 신규/기존 분해.

WHY: 사용자는 "주기적으로 웨비나에 오던 Contact(regular)가 알 수 없는 이유로 빠져나갔다"고 본다.
이 가설은 '전년 6~8월에 참석한 사람이 올해 6~8월에도 참석했는가(유지율)'로 직접 시험할 수 있다.
또 참석자 감소가 유지율 하락 때문인지 신규 유입 감소 때문인지 나누어 어느 쪽이 더 큰지 본다.
주의: '신규'는 전년 6~8월 참석 기록이 없는 사람이다. 다른 달이나 그 이전 해에 참석한 사람이 섞여 있다.
"""
import pandas as pd

import config
from load_campaign_members import load_all


def prepare(df: pd.DataFrame, korea_only: bool = False) -> pd.DataFrame:
    d = df[df["campaign_month"].isin(config.TARGET_MONTHS)]
    d = d[~d["Campaign Name"].isin(config.EXCLUDED_CAMPAIGNS)]
    if korea_only:
        d = d[d["Country"] == config.KOREA_RESIDENT_LABEL]
    return d


def attended_counts(d: pd.DataFrame) -> pd.DataFrame:
    """연도별, 이메일별로 참석한 서로 다른 캠페인 수."""
    a = d[d["Member Status"] == "Attended"].drop_duplicates(["campaign_year", "Email", "Campaign Name"])
    return a.groupby(["campaign_year", "Email"]).size().rename("n").reset_index()


def attendees(counts: pd.DataFrame, year: int, min_times: int = 1) -> set:
    return set(counts[(counts["campaign_year"] == year) & (counts["n"] >= min_times)]["Email"])


def retention(counts: pd.DataFrame, y0: int, y1: int, min_times: int = 1):
    """(돌아온 사람 수, 전년 그룹 크기). 돌아옴 = 다음 해에 1회 이상 참석."""
    base = attendees(counts, y0, min_times)
    return len(base & attendees(counts, y1, 1)), len(base)


def new_vs_returning(counts: pd.DataFrame, y0: int, y1: int):
    """(y1 참석자 중 전년 참석자, 신규)."""
    cur, prev = attendees(counts, y1), attendees(counts, y0)
    return len(cur & prev), len(cur - prev)


# ---- 테스트: 기대값과 실제값 비교 ----
def _toy():
    rows = []
    def add(y, email, camp, status="Attended", month=7, country="South Korea"):
        rows.append({"campaign_year": y, "campaign_month": month, "Email": email, "Campaign Name": camp,
                     "Member Status": status, "Country": country})
    # 2024: a는 2회, b는 1회, c는 등록만(불참)
    add(2024, "a", "W1"); add(2024, "a", "W2"); add(2024, "b", "W1"); add(2024, "c", "W1", "No Show")
    # 2025: a 돌아옴, b 안 옴, d 신규, 같은 캠페인 중복 행은 1회로
    add(2025, "a", "X1"); add(2025, "a", "X1"); add(2025, "d", "X1")
    return pd.DataFrame(rows)


def test_retention_toy():
    c = attended_counts(prepare(_toy()))
    assert retention(c, 2024, 2025, 1) == (1, 2)       # a, b 중 a만
    assert retention(c, 2024, 2025, 2) == (1, 1)       # 2회 이상은 a만이고 돌아옴


def test_new_vs_returning_toy():
    c = attended_counts(prepare(_toy()))
    assert new_vs_returning(c, 2024, 2025) == (1, 1)   # 2025 참석 a(전년 참석), d(신규)


def test_duplicate_rows_count_once():
    c = attended_counts(prepare(_toy()))
    assert int(c[(c.campaign_year == 2025) & (c.Email == "a")]["n"].iloc[0]) == 1


def test_excluded_campaign_removed():
    df = _toy()
    df = pd.concat([df, pd.DataFrame([{"campaign_year": 2025, "campaign_month": 7, "Email": "z",
                                       "Campaign Name": config.EXCLUDED_CAMPAIGNS[0], "Member Status": "Attended",
                                       "Country": "South Korea"}])])
    assert "z" not in attendees(attended_counts(prepare(df)), 2025)


def test_korea_only_filter():
    df = pd.concat([_toy(), pd.DataFrame([{"campaign_year": 2025, "campaign_month": 7, "Email": "us",
                                           "Campaign Name": "X1", "Member Status": "Attended", "Country": "United States of America"}])])
    assert "us" in attendees(attended_counts(prepare(df)), 2025)
    assert "us" not in attendees(attended_counts(prepare(df, korea_only=True)), 2025)


def test_real_data_partition_holds():
    # 실제 데이터에서도 '돌아온 사람 + 신규 = 그 해 참석자'가 성립해야 한다
    c = attended_counts(prepare(load_all()))
    for y0, y1 in ((2024, 2025), (2025, 2026)):
        r, n = new_vs_returning(c, y0, y1)
        assert r + n == len(attendees(c, y1))


if __name__ == "__main__":
    for t in [v for k, v in sorted(globals().items()) if k.startswith("test_")]:
        t()
    print("모든 테스트 통과")
    for title, ko in (("2025-08-23 제외", False), ("2025-08-23 제외 + 한국 거주만", True)):
        c = attended_counts(prepare(load_all(), korea_only=ko))
        print(f"\n[{title}]")
        for y0, y1 in ((2024, 2025), (2025, 2026)):
            parts = []
            for k in (1, 2, 3):
                r, n = retention(c, y0, y1, k)
                parts.append(f">={k}회 {r}/{n} ({r / n * 100:.0f}%)")
            ret, new = new_vs_returning(c, y0, y1)
            print(f"  {y0}->{y1} 유지: " + " | ".join(parts) + f" || {y1} 참석 {ret + new} = 돌아온 {ret} + 신규 {new}")
