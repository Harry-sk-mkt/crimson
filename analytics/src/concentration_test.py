"""학교별 감소가 '특정 학교에 몰렸다'고 볼 만큼 우연 이상인지 검정한다.

WHY: 표본이 작으면(학교당 연 1~18명) 우연만으로도 어떤 학교는 크게 줄고 어떤 학교는 는다.
'여섯 학교에 몰려 있다'는 관찰은 결과를 본 뒤 고른 학교라 그 자체로는 증거가 아니다.
귀무가설: 두 해의 학교별 분포가 같고, 전체 인원만 다르다. 이 가정으로 두 해를 다시 뽑아
(몬테카를로) 우리가 본 것만큼 학교별 차이가 벌어질 확률을 잰다. 고르는 절차(상위 k개)까지
시뮬레이션에 똑같이 넣어 사후 선택 편향을 반영한다.
"""
import numpy as np
import pandas as pd

import school_table

RNG_SEED = 20260922
N_SIM = 20000
TOP_K = 6


def _stats(a: np.ndarray, b: np.ndarray, k: int):
    """a, b: 학교별 인원(앞 해, 뒤 해). 반환 (카이제곱, 상위 k개 감소 합)."""
    na, nb = a.sum(), b.sum()
    tot = a + b
    exp_b = tot * nb / (na + nb)
    exp_a = tot * na / (na + nb)
    m = tot > 0
    chi2 = (((a - exp_a) ** 2)[m] / exp_a[m]).sum() + (((b - exp_b) ** 2)[m] / exp_b[m]).sum()
    drop = exp_b - b                       # 기대보다 덜 나온 인원 (양수 = 비례 대비 감소)
    top_drop = np.sort(drop)[::-1][:k].sum()
    return chi2, top_drop


def concentration_pvalues(a, b, k=TOP_K, n_sim=N_SIM, seed=RNG_SEED):
    a, b = np.asarray(a, float), np.asarray(b, float)
    obs_chi2, obs_top = _stats(a, b, k)
    rng = np.random.default_rng(seed)
    tot = a + b
    p = tot / tot.sum()
    na, nb = int(a.sum()), int(b.sum())
    sa = rng.multinomial(na, p, size=n_sim)
    sb = rng.multinomial(nb, p, size=n_sim)
    sims = [_stats(sa[i], sb[i], k) for i in range(n_sim)]
    chi = np.array([s[0] for s in sims]); top = np.array([s[1] for s in sims])
    return {"chi2": obs_chi2, "p_chi2": float((chi >= obs_chi2).mean()),
            "top_drop": obs_top, "p_top": float((top >= obs_top).mean()),
            "sim_top_median": float(np.median(top))}


def domestic_counts() -> pd.DataFrame:
    return school_table.school_table(school_table.unique_contacts())


# ---- 테스트: 기대값과 실제값 비교 ----
def test_identical_distribution_is_not_significant():
    a = np.array([20, 15, 10, 5, 5, 5]); b = a * 2 // 1   # 모든 학교가 똑같이 2배
    r = concentration_pvalues(a, b, k=2, n_sim=2000)
    assert r["p_chi2"] > 0.5 and r["p_top"] > 0.2, r


def test_concentrated_drop_is_significant():
    a = np.array([40, 40, 10, 10]); b = np.array([5, 40, 10, 10])   # 한 학교만 크게 감소
    r = concentration_pvalues(a, b, k=1, n_sim=2000)
    assert r["p_top"] < 0.01 and r["p_chi2"] < 0.01, r


if __name__ == "__main__":
    test_identical_distribution_is_not_significant()
    test_concentrated_drop_is_significant()
    print("모든 테스트 통과")
