"""Biostatistics against published reference values and constructed data."""
import math
import warnings

import numpy as np
import pandas as pd
import pytest
from scipy import stats as st

from osteoquant.stats.core import (adjust_pvalues, agreement_summary, anova_oneway, bland_altman,
                                   bootstrap_ci, check_pseudoreplication, compare_two_groups, describe,
                                   hedges_g, icc, learning_curve_fit, lins_ccc, missing_data_summary,
                                   mixed_model_longitudinal, sample_size_icc, sample_size_two_groups)
from osteoquant.stats.core import test_retest as retest

# Shrout & Fleiss (1979) Table 2: 6 targets x 4 judges.
SF = np.array([[9, 2, 5, 8], [6, 1, 3, 2], [8, 4, 6, 8], [7, 1, 2, 6], [10, 5, 6, 9], [6, 2, 4, 7]], float)

# Published values (Shrout & Fleiss 1979 point estimates; 95 % CIs as reported by R psych::ICC for
# the same data, which implements the Shrout-Fleiss / McGraw-Wong F-based intervals).
SF_REF = {
    "1,1": (0.17, -0.133, 0.72),
    "2,1": (0.29, 0.019, 0.76),
    "3,1": (0.71, 0.342, 0.95),
    "2,k": (0.62, 0.071, 0.93),
    "3,k": (0.91, 0.676, 0.99),
}


@pytest.mark.parametrize("form", sorted(SF_REF))
def test_icc_matches_shrout_fleiss(form):
    r = icc(SF, form)
    est, lo, hi = SF_REF[form]
    assert round(r["icc"], 2) == pytest.approx(est, abs=0.006)
    assert r["ci95_low"] == pytest.approx(lo, abs=0.006)
    assert r["ci95_high"] == pytest.approx(hi, abs=0.006)
    assert r["n"] == 6 and r["k"] == 4 and r["form"] == form


def test_icc_perfect_agreement_and_degenerate_inputs():
    Y = np.c_[np.arange(10.0), np.arange(10.0)]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        r = icc(Y, "2,1")
        assert r["icc"] == pytest.approx(1.0)
        assert r["interpretation_koo_li"] == "excellent"
        z = icc(np.ones((5, 3)), "2,1")                 # zero variance: undefined, NOT "excellent"
    assert math.isnan(z["icc"]) and z["interpretation_koo_li"] == "undefined"
    assert math.isnan(icc(np.ones((1, 3)))["icc"])
    with pytest.raises(ValueError):
        icc(SF, "9,9")


def test_icc_rater_offset_lowers_absolute_not_consistency():
    rng = np.random.default_rng(1)
    t = rng.normal(0, 1, 30)
    Y = np.c_[t + rng.normal(0, 0.1, 30), t + 2 + rng.normal(0, 0.1, 30)]   # systematic +2 offset
    assert icc(Y, "3,1")["icc"] > 0.95
    assert icc(Y, "2,1")["icc"] < 0.5


def test_icc_is_invariant_to_rater_and_subject_permutation():
    rng = np.random.default_rng(3)
    for form in ("1,1", "2,1", "3,1"):
        a = icc(SF, form)["icc"]
        assert icc(SF[:, rng.permutation(4)], form)["icc"] == pytest.approx(a)
        assert icc(SF[rng.permutation(6)], form)["icc"] == pytest.approx(a)


def test_bland_altman_constructed():
    a = np.arange(1.0, 11.0)
    d = np.array([0.5, -0.5] * 5)                       # mean 0, sd known
    b = a + 1.0 + d
    r = bland_altman(a, b)
    sd = np.std(d, ddof=1)
    assert r["bias"] == pytest.approx(1.0) and r["sd_diff"] == pytest.approx(sd)
    assert r["loa_low"] == pytest.approx(1 - 1.96 * sd) and r["loa_high"] == pytest.approx(1 + 1.96 * sd)
    t = st.t.ppf(0.975, 9)
    assert r["bias_ci95"][0] == pytest.approx(1 - t * sd / math.sqrt(10))
    assert r["loa_high_ci95"][1] == pytest.approx(1 + 1.96 * sd + t * sd * math.sqrt(3 / 10))
    assert abs(r["proportional_bias_slope"]) < 0.1


def test_bland_altman_proportional_bias_and_log():
    a = np.linspace(1, 10, 20)
    b = 1.2 * a
    r = bland_altman(a, b)
    assert r["proportional_bias_slope"] == pytest.approx(0.2 / 1.1, rel=1e-6)
    lg = bland_altman(a, b, log=True)
    assert lg["log_scale"] and lg["bias"] == pytest.approx(math.log(1.2)) and lg["sd_diff"] == pytest.approx(0, abs=1e-12)
    one = bland_altman([1.0], [2.0])
    assert one["n"] == 1 and math.isnan(one["sd_diff"]) and "proportional_bias_slope" not in one


def test_hedges_g_known_value_and_symmetry():
    a, b = [2, 3, 4, 5], [1, 2, 3, 4]
    r = hedges_g(a, b)
    d = 1 / np.std([1, 2, 3, 4], ddof=1)
    J = 1 - 3 / (4 * 8 - 9)
    assert r["d"] == pytest.approx(d) and r["g"] == pytest.approx(d * J)
    assert hedges_g(b, a)["g"] == pytest.approx(-r["g"])
    assert r["ci95_low"] < r["g"] < r["ci95_high"]
    assert math.isnan(hedges_g([1], [1, 2])["g"])
    assert math.isnan(hedges_g([1, 1], [1, 1])["g"])


def test_adjust_pvalues_matches_statsmodels():
    from statsmodels.stats.multitest import multipletests
    p = [0.01, 0.04, 0.03, 0.005, 0.2, 0.5, 0.0001]
    for ours, theirs in (("holm", "holm"), ("bonferroni", "bonferroni"), ("bh", "fdr_bh"), ("fdr_bh", "fdr_bh")):
        assert np.allclose(adjust_pvalues(p, ours), multipletests(p, method=theirs)[1])
    with pytest.raises(ValueError):
        adjust_pvalues(p, "nope")
    assert adjust_pvalues([], "holm") == []


def test_describe_filters_missing_and_reports_ci():
    r = describe([1, 2, 3, None, float("nan"), float("inf")])
    assert r["n"] == 3 and r["mean"] == 2.0 and r["sd"] == 1.0
    t = st.t.ppf(0.975, 2)
    assert r["ci95_high"] == pytest.approx(2 + t / math.sqrt(3))
    assert describe([]) == {"n": 0}
    assert "sd" not in describe([5.0])
    assert math.isnan(describe([-1.0, 1.0])["cv"])


def test_bootstrap_ci_contains_mean_and_is_deterministic():
    x = np.random.default_rng(0).normal(10, 1, 50)
    lo, hi = bootstrap_ci(x, n_boot=500)
    assert lo < x.mean() < hi
    assert bootstrap_ci(x, n_boot=500) == (lo, hi)
    assert all(math.isnan(v) for v in bootstrap_ci([1.0]))


def test_compare_two_groups_unpaired_and_paired():
    a = [10.0, 11.0, 12.0, 13.0, 14.0, 15.0]
    b = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    r = compare_two_groups(a, b)
    assert r["mean_diff"] == 9.0 and r["welch_t"]["p"] < 1e-4 and "caution" not in r
    assert r["mann_whitney"]["p"] == pytest.approx(st.mannwhitneyu(a, b, alternative="two-sided").pvalue)
    p = compare_two_groups([1.0, 2, 3], [1.5, 2.7, 3.2], paired=True)
    assert "t_test" in p and "caution" in p
    same = compare_two_groups([1.0, 2.0, 3.0], [1.0, 2.0, 3.0], paired=True)   # zero differences
    assert same["wilcoxon"] is None or math.isnan(same["wilcoxon"]["p"]) or same["wilcoxon"]["p"] == 1.0


def test_anova_and_kruskal():
    r = anova_oneway({"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]})
    f, p = st.f_oneway([1, 2, 3], [4, 5, 6], [7, 8, 9])
    assert r["F"] == pytest.approx(f) and r["p"] == pytest.approx(p) and r["groups"]["b"]["mean"] == 5


def test_lins_ccc_implementation_variant():
    # Implementation uses n-1 (sample) moments; Lin (1989) defines population (1/n) moments.
    # Documented as ambiguity QA-OBS-02; both agree for perfect agreement and as n grows.
    assert lins_ccc([1, 2, 3], [1, 2, 3]) == pytest.approx(1.0)
    assert lins_ccc([1, 2, 3], [2, 3, 4]) == pytest.approx(2 / 3)
    x = np.random.default_rng(0).normal(0, 1, 5000)
    y = x + 0.3
    sx2, sy2, sxy = x.var(), y.var(), np.cov(x, y, ddof=0)[0, 1]
    lin = 2 * sxy / (sx2 + sy2 + 0.09)
    assert lins_ccc(x, y) == pytest.approx(lin, rel=1e-3)


def test_agreement_summary_and_retest():
    t = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    m = t * 1.1
    r = agreement_summary(t, m)
    assert r["mae"] == pytest.approx(0.3) and r["mean_rel_error"] == pytest.approx(0.1)
    assert r["pearson_r"] == pytest.approx(1.0) and r["spearman_rho"] == pytest.approx(1.0)
    assert r["bland_altman"]["bias"] == pytest.approx(0.3)
    small = agreement_summary([1.0, 2.0], [1.0, 2.0])
    assert math.isnan(small["ccc"])
    tr = retest([1.0, 2.0, 3.0], [1.5, 2.5, 3.5])
    assert tr["Sw"] == pytest.approx(math.sqrt(0.25 / 2)) and tr["RC"] == pytest.approx(2.77 * tr["Sw"])


def test_pseudoreplication_detection():
    df = pd.DataFrame({"animal": [1, 1, 2, 2], "group": ["a", "a", "b", "b"], "v": [1, 2, 3, 4]})
    r = check_pseudoreplication(df, "animal", ["group"])
    assert r["pseudoreplication_risk"] and r["max_rows_per_subject_condition"] == 2 and r["n_subjects"] == 2
    ok = check_pseudoreplication(df.drop_duplicates("animal"), "animal", ["group"])
    assert not ok["pseudoreplication_risk"]
    empty = check_pseudoreplication(df.iloc[:0], "animal", ["group"])
    assert empty["max_rows_per_subject_condition"] == 0


def test_mixed_model_recovers_slope_and_refuses_small_n():
    rng = np.random.default_rng(0)
    rows = []
    for s in range(12):
        g = "T" if s % 2 else "C"
        b0 = rng.normal(0, 0.5)
        for t in (0, 4, 8, 12):
            rows.append({"y": 1 + b0 + (0.3 if g == "T" else 0.1) * t + rng.normal(0, 0.05), "grp": g,
                         "week": t, "animal": s})
    df = pd.DataFrame(rows)
    r = mixed_model_longitudinal(df, "y", "grp", "week", "animal")
    assert r["n_subjects"] == 12 and r["n_obs"] == 48
    assert r["params"]["week"] == pytest.approx(0.1, abs=0.02)
    assert r["params"]["C(grp)[T.T]:week"] == pytest.approx(0.2, abs=0.03)
    assert "error" in mixed_model_longitudinal(df[df.animal < 3], "y", "grp", "week", "animal")


def test_missing_data_summary():
    df = pd.DataFrame({"a": [1, None, 3], "s": ["x", "y", "z"]})
    r = missing_data_summary(df, "s", ["a"])
    assert r["a"] == {"n_missing": 1, "frac_missing": pytest.approx(1 / 3), "subjects_affected": ["y"]}


def test_learning_curve_fit_recovers_asymptote():
    n = np.array([1, 2, 4, 8, 16, 32])
    y = 0.9 - 0.5 * n ** -0.7
    r = learning_curve_fit(n, y)
    assert r["asymptote"] == pytest.approx(0.9, abs=0.01) and r["c"] == pytest.approx(0.7, abs=0.05)
    assert "error" in learning_curve_fit([1, 2], [0.1, 0.2])


def test_sample_size_formulas():
    # two-sample t, d = 1, alpha .05, power .8: normal approximation 15.7 -> 16 (+1) = 17 per group
    assert sample_size_two_groups(1.0, 1.0) == 17
    assert sample_size_two_groups(0.5, 1.0) > sample_size_two_groups(1.0, 1.0)
    # Walter, Eliasziw & Donner (1998): rho0 .6 vs rho1 .8, k=2 -> 39 subjects
    assert sample_size_icc(0.6, 0.8, k=2) == 39
    assert sample_size_icc(0.6, 0.8, k=3) < 39
