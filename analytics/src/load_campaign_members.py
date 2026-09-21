"""Salesforce 'Campaigns with Campaign Members' 리포트 xlsx를 멤버 단위 DataFrame으로 읽는다.

WHY: 이 리포트는 Member Type/Status로 그룹 지어 내보내서 값이 그룹 첫 행에만 있고,
위에 제목/필터, 아래에 Subtotal/Total 행이 섞여 있다. 그대로 읽으면 Member Type/Status가 대부분
비고 합계 행이 멤버로 세어진다. 리포트 자체 Total과 대조해 파싱이 정확한지 검증한다.
"""
import re
from pathlib import Path

import pandas as pd

import config


def _find_header_row(raw: pd.DataFrame) -> int:
    for i in range(len(raw)):
        if (raw.iloc[i] == config.HEADER_ANCHOR).any():
            return i
    raise ValueError(f"헤더 라벨 '{config.HEADER_ANCHOR}'을 찾지 못했다")


def _clean_label(v) -> str:
    # 정렬 화살표(' ↑')와 공백을 떼서 라벨 비교가 가능하게 한다
    return re.sub(r"[↑↓]", "", str(v)).strip()


def report_total(raw: pd.DataFrame) -> int:
    """리포트 하단 'Total' 행의 건수."""
    for i in range(len(raw)):
        row = raw.iloc[i].tolist()
        if "Total" in row:
            nums = [v for v in row if isinstance(v, (int, float)) and not pd.isna(v)]
            return int(nums[0])
    raise ValueError("Total 행을 찾지 못했다")


def load_file(path: Path) -> pd.DataFrame:
    raw = pd.read_excel(path, sheet_name=0, header=None)
    h = _find_header_row(raw)
    labels = [_clean_label(v) if pd.notna(v) else f"_col{j}" for j, v in enumerate(raw.iloc[h])]
    df = raw.iloc[h + 1:].copy()
    df.columns = labels
    df[config.GROUPED_COLUMNS] = df[config.GROUPED_COLUMNS].ffill()
    df = df[df[config.HEADER_ANCHOR].astype(str).str.startswith(config.CAMPAIGN_PREFIX)].copy()
    ym = df[config.HEADER_ANCHOR].str.extract(config.CAMPAIGN_YM_PATTERN)
    df["campaign_year"] = ym[0].astype(int)
    df["campaign_month"] = ym[1].astype(int)
    df["source_file"] = path.name
    df.attrs["report_total"] = report_total(raw)
    return df.drop(columns=[c for c in df.columns if c.startswith("_col")]).reset_index(drop=True)


def load_all() -> pd.DataFrame:
    files = sorted(config.DATA_DIR.glob(config.CAMPAIGN_MEMBER_GLOB))
    if not files:
        raise FileNotFoundError(f"{config.DATA_DIR}에 {config.CAMPAIGN_MEMBER_GLOB} 파일이 없다")
    return pd.concat([load_file(f) for f in files], ignore_index=True)


# ---- 테스트: 기대값(리포트 Total)과 실제값(파싱 행 수) 비교 ----
def test_row_count_matches_report_total():
    for f in sorted(config.DATA_DIR.glob(config.CAMPAIGN_MEMBER_GLOB)):
        df = load_file(f)
        expected = df.attrs["report_total"]
        assert len(df) == expected, f"{f.name}: 파싱 {len(df)}행 != 리포트 Total {expected}"


def test_grouped_columns_are_filled():
    df = load_all()
    for col in config.GROUPED_COLUMNS:
        assert df[col].notna().all(), f"{col}에 빈 값이 남았다"


def test_only_contact_members():
    # 리포트 필터가 'Member Type equals Contact'라 다른 값이 있으면 필터 변경 신호
    assert set(load_all()["Member Type"].unique()) == {"Contact"}


if __name__ == "__main__":
    test_row_count_matches_report_total()
    test_grouped_columns_are_filled()
    test_only_contact_members()
    print("모든 테스트 통과")
