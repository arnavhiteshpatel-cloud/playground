"""Biostatistics for preclinical imaging studies.

Unit of analysis = the animal/specimen. Functions that accept long-format data require an
explicit ``subject`` column; ``check_pseudoreplication`` refuses analyses where the number of
rows per subject per condition exceeds 1 unless a repeated-measures/mixed model is used.

ICC forms follow McGraw & Wong (1996) and Shrout & Fleiss (1979) as summarised by
Koo & Li (2016, J Chiropr Med 15:155; DOI 10.1016/j.jcm.2016.02.012):
  ICC(1,1)  one-way random, single measure
  ICC(2,1)  two-way random, absolute agreement, single measure   <- default for method/rater agreement
  ICC(3,1)  two-way mixed, consistency, single measure
  ICC(2,k), ICC(3,k) average measures
95% CIs use the F-distribution formulas from McGraw & Wong (1996).
"""
from __future__ import annotations

import math
import warnings

import numpy as np
from scipy import stats as st


# ----------------------------------------------------------------------------- descriptive
def describe(x) -> dict:
    x = np.asarray([v for v in x if v is not None and np.isfinite(v)], float)
    n = len(x)
    if n == 0:
        return {"n": 0}
    out = {"n": n, "mean": float(x.mean()), "median": float(np.median(x)),
           "min": float(x.min()), "max": float(x.max())}
    if n > 1:
        sd = float(x.std(ddof=1))
        se = sd / math.sqrt(n)
        t = st.t.ppf(0.975, n - 1)
        out.update({"sd": sd, "se": se, "ci95_low": out["mean"] - t * se, "ci95_high": out["mean"] + t * se,
                    "cv": sd / out["mean"] if out["mean"] else float("nan"),
                    "q1": float(np.percentile(x, 25)), "q3": float(np.percentile(x, 75))})
    return out


def bootstrap_ci(x, fn=np.mean, n_boot=5000, alpha=0.05, seed=0):
    rng = np.random.default_rng(seed)
    x = np.asarray(x, float)
    if len(x) < 2:
        return (float("nan"), float("nan"))
    b = np.array([fn(rng.choice(x, len(x), replace=True)) for _ in range(n_boot)])
    return float(np.percentile(b, 100 * alpha / 2)), float(np.percentile(b, 100 * (1 - alpha / 2)))


# ----------------------------------------------------------------------------- effect sizes
def hedges_g(a, b) -> dict:
    a, b = np.asarray(a, float), np.asarray(b, float)
    na, nb = len(a), len(b)
    if na < 2 or nb < 2:
        return {"g": float("nan")}
    sp = math.sqrt(((na - 1) * a.var(ddof=1) + (nb - 1) * b.var(ddof=1)) / (na + nb - 2))
    d = (a.mean() - b.mean()) / sp if sp > 0 else float("nan")
    J = 1 - 3 / (4 * (na + nb) - 9)
    g = d * J
    se = math.sqrt((na + nb) / (na * nb) + g ** 2 / (2 * (na + nb)))
    return {"g": g, "ci95_low": g - 1.96 * se, "ci95_high": g + 1.96 * se, "d": d}


def compare_two_groups(a, b, paired=False) -> dict:
    """Welch t-test (or paired t) + Mann–Whitney/Wilcoxon + Hedges g. Small n -> report both."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    out = {"n_a": len(a), "n_b": len(b), "mean_diff": float(a.mean() - b.mean())}
    if paired:
        out["t_test"] = dict(zip(("t", "p"), map(float, st.ttest_rel(a, b))))
        try:
            out["wilcoxon"] = dict(zip(("W", "p"), map(float, st.wilcoxon(a, b))))
        except ValueError:
            out["wilcoxon"] = None
    else:
        out["welch_t"] = dict(zip(("t", "p"), map(float, st.ttest_ind(a, b, equal_var=False))))
        out["mann_whitney"] = dict(zip(("U", "p"), map(float, st.mannwhitneyu(a, b, alternative="two-sided"))))
    out["hedges_g"] = hedges_g(a, b)
    if min(len(a), len(b)) < 5:
        out["caution"] = "n<5 per group: p-values unstable; emphasise effect sizes and CIs"
    return out


def adjust_pvalues(p, method="holm") -> list[float]:
    p = np.asarray(p, float)
    m = len(p)
    order = np.argsort(p)
    adj = np.empty(m)
    if method == "bonferroni":
        adj = np.minimum(p * m, 1)
    elif method == "holm":
        run = 0.0
        for i, k in enumerate(order):
            run = max(run, (m - i) * p[k])
            adj[k] = min(run, 1)
    elif method in ("bh", "fdr_bh"):
        run = 1.0
        for i in range(m - 1, -1, -1):
            k = order[i]
            run = min(run, p[k] * m / (i + 1))
            adj[k] = run
    else:
        raise ValueError(method)
    return adj.tolist()


def anova_oneway(groups: dict) -> dict:
    vals = [np.asarray(v, float) for v in groups.values()]
    f, p = st.f_oneway(*vals)
    h, pk = st.kruskal(*vals)
    return {"F": float(f), "p": float(p), "kruskal_H": float(h), "kruskal_p": float(pk),
            "groups": {k: describe(v) for k, v in groups.items()}}


# ----------------------------------------------------------------------------- agreement
def icc(Y, form="2,1") -> dict:
    """ICC from an n_subjects × k_raters matrix (no missing values)."""
    Y = np.asarray(Y, float)
    n, k = Y.shape
    if n < 2 or k < 2:
        return {"icc": float("nan"), "form": form}
    gm = Y.mean()
    ssr = k * ((Y.mean(1) - gm) ** 2).sum()
    ssc = n * ((Y.mean(0) - gm) ** 2).sum()
    sst = ((Y - gm) ** 2).sum()
    sse = sst - ssr - ssc
    msr = ssr / (n - 1)
    msc = ssc / (k - 1)
    mse = sse / ((n - 1) * (k - 1))
    msw = (ssc + sse) / (n * (k - 1))
    a = 0.05
    if form == "1,1":
        v = (msr - msw) / (msr + (k - 1) * msw)
        F = msr / msw
        df1, df2 = n - 1, n * (k - 1)
        fl, fu = F / st.f.ppf(1 - a / 2, df1, df2), F * st.f.ppf(1 - a / 2, df2, df1)
        lo, hi = (fl - 1) / (fl + k - 1), (fu - 1) / (fu + k - 1)
    elif form in ("2,1", "2,k"):
        if form == "2,1":
            v = (msr - mse) / (msr + (k - 1) * mse + k * (msc - mse) / n)
        else:
            v = (msr - mse) / (msr + (msc - mse) / n)
        # McGraw & Wong CI for absolute agreement
        Fj = msc / mse
        vn = (k - 1) * (n - 1) * (k * v * Fj + n * (1 + (k - 1) * v) - k * v) ** 2
        vd = (n - 1) * k ** 2 * v ** 2 * Fj ** 2 + (n * (1 + (k - 1) * v) - k * v) ** 2
        nu = vn / vd if vd > 0 else n - 1
        Fs = st.f.ppf(1 - a / 2, n - 1, nu)
        Fs2 = st.f.ppf(1 - a / 2, nu, n - 1)
        lo = n * (msr - Fs * mse) / (Fs * (k * msc + (k * n - k - n) * mse) + n * msr)
        hi = n * (Fs2 * msr - mse) / (k * msc + (k * n - k - n) * mse + n * Fs2 * msr)
        if form == "2,k":
            lo, hi = lo * k / (1 + lo * (k - 1)), hi * k / (1 + hi * (k - 1))
    elif form in ("3,1", "3,k"):
        F = msr / mse
        df1, df2 = n - 1, (n - 1) * (k - 1)
        fl, fu = F / st.f.ppf(1 - a / 2, df1, df2), F * st.f.ppf(1 - a / 2, df2, df1)
        if form == "3,1":
            v = (msr - mse) / (msr + (k - 1) * mse)
            lo, hi = (fl - 1) / (fl + k - 1), (fu - 1) / (fu + k - 1)
        else:
            v = (msr - mse) / msr
            lo, hi = 1 - 1 / fl, 1 - 1 / fu
    else:
        raise ValueError(form)
    interp = ("poor" if v < 0.5 else "moderate" if v < 0.75 else "good" if v < 0.9 else "excellent")
    return {"icc": float(v), "ci95_low": float(lo), "ci95_high": float(hi), "form": form, "n": n, "k": k,
            "interpretation_koo_li": interp,
            "note": "Koo & Li 2016 interpretation applied to the CI, not just the point estimate"}


def bland_altman(a, b, log=False) -> dict:
    """Bland–Altman limits of agreement (b − a). Proportional bias via regression of diff on mean."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    if log:
        a, b = np.log(a), np.log(b)
    d = b - a
    m = (a + b) / 2
    n = len(d)
    bias = float(d.mean())
    sd = float(d.std(ddof=1)) if n > 1 else float("nan")
    t = st.t.ppf(0.975, n - 1) if n > 1 else float("nan")
    se_bias = sd / math.sqrt(n) if n > 1 else float("nan")
    se_loa = sd * math.sqrt(3 / n) if n > 1 else float("nan")
    out = {"n": n, "bias": bias, "sd_diff": sd, "loa_low": bias - 1.96 * sd, "loa_high": bias + 1.96 * sd,
           "bias_ci95": [bias - t * se_bias, bias + t * se_bias],
           "loa_low_ci95": [bias - 1.96 * sd - t * se_loa, bias - 1.96 * sd + t * se_loa],
           "loa_high_ci95": [bias + 1.96 * sd - t * se_loa, bias + 1.96 * sd + t * se_loa],
           "log_scale": log}
    if n > 2:
        sl = st.linregress(m, d)
        out["proportional_bias_slope"] = float(sl.slope)
        out["proportional_bias_p"] = float(sl.pvalue)
    return out


def lins_ccc(a, b) -> float:
    a, b = np.asarray(a, float), np.asarray(b, float)
    sxy = np.cov(a, b, ddof=1)[0, 1]
    return float(2 * sxy / (a.var(ddof=1) + b.var(ddof=1) + (a.mean() - b.mean()) ** 2))


def agreement_summary(truth, measured) -> dict:
    t, m = np.asarray(truth, float), np.asarray(measured, float)
    err = m - t
    rel = err / np.where(t != 0, t, np.nan)
    return {"n": len(t), "mae": float(np.abs(err).mean()), "rmse": float(np.sqrt((err ** 2).mean())),
            "mean_rel_error": float(np.nanmean(rel)), "mean_abs_rel_error": float(np.nanmean(np.abs(rel))),
            "pearson_r": float(st.pearsonr(t, m)[0]) if len(t) > 2 else float("nan"),
            "spearman_rho": float(st.spearmanr(t, m)[0]) if len(t) > 2 else float("nan"),
            "ccc": lins_ccc(t, m) if len(t) > 2 else float("nan"),
            "icc_2_1": icc(np.c_[t, m], "2,1"), "bland_altman": bland_altman(t, m)}


def test_retest(run1, run2) -> dict:
    """Repeatability: within-subject SD (Sw), repeatability coefficient RC = 2.77·Sw, ICC(2,1)."""
    a, b = np.asarray(run1, float), np.asarray(run2, float)
    sw = math.sqrt(((a - b) ** 2).mean() / 2)
    return {"Sw": sw, "RC": 2.77 * sw, "CV_within": sw / float(np.mean((a + b) / 2)),
            "icc_2_1": icc(np.c_[a, b], "2,1")}


# ----------------------------------------------------------------------------- study-level designs
def check_pseudoreplication(df, subject_col, condition_cols) -> dict:
    """Detect >1 row per subject per condition (e.g. voxel-, slice- or ROI-level rows)."""
    g = df.groupby([subject_col] + list(condition_cols)).size()
    mx = int(g.max()) if len(g) else 0
    return {"max_rows_per_subject_condition": mx, "pseudoreplication_risk": mx > 1,
            "n_subjects": int(df[subject_col].nunique())}


def mixed_model_longitudinal(df, outcome, group_col, time_col, subject_col) -> dict:
    """Linear mixed model outcome ~ group * time + (1 | subject) (statsmodels MixedLM, REML).
    Appropriate for repeated measures with missing timepoints (MAR). Small n -> unstable."""
    import statsmodels.formula.api as smf
    d = df[[outcome, group_col, time_col, subject_col]].dropna()
    if d[subject_col].nunique() < 4:
        return {"error": "fewer than 4 subjects; mixed model not estimable reliably"}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        md = smf.mixedlm(f"{outcome} ~ C({group_col}) * {time_col}", d, groups=d[subject_col])
        fit = md.fit(reml=True)
    res = {"n_obs": int(len(d)), "n_subjects": int(d[subject_col].nunique()),
           "converged": bool(fit.converged), "params": {k: float(v) for k, v in fit.params.items()},
           "pvalues": {k: float(v) for k, v in fit.pvalues.items()},
           "conf_int": {k: [float(a), float(b)] for k, (a, b) in fit.conf_int().iterrows()},
           "random_effect_var": float(fit.cov_re.iloc[0, 0]) if fit.cov_re.size else float("nan"),
           "method": "statsmodels MixedLM REML; random intercept per subject"}
    return res


def missing_data_summary(df, subject_col, expected_cols) -> dict:
    out = {}
    for c in expected_cols:
        miss = df[c].isna()
        out[c] = {"n_missing": int(miss.sum()), "frac_missing": float(miss.mean()),
                  "subjects_affected": sorted(map(str, df.loc[miss, subject_col].unique()))}
    return out


def learning_curve_fit(n_labels, scores) -> dict:
    """Fit score = a − b·n^(−c) (inverse power law) to learning-curve points; extrapolate."""
    from scipy.optimize import curve_fit
    n = np.asarray(n_labels, float)
    y = np.asarray(scores, float)
    ok = n > 0
    n, y = n[ok], y[ok]
    if len(n) < 3:
        return {"error": "need >=3 points"}
    f = lambda x, a, b, c: a - b * np.power(x, -c)  # noqa: E731
    try:
        p, _ = curve_fit(f, n, y, p0=[y.max(), max(y.max() - y.min(), 0.01), 0.5], maxfev=20000,
                         bounds=([0, 0, 0], [1.5, 10, 5]))
    except Exception as e:  # pragma: no cover
        return {"error": str(e)}
    return {"asymptote": float(p[0]), "b": float(p[1]), "c": float(p[2]),
            "pred_at": {int(k): float(f(k, *p)) for k in (1, 3, 5, 10, 20, 50)}}


def sample_size_two_groups(delta, sd, alpha=0.05, power=0.8) -> int:
    """Per-group n for a two-sided two-sample t-test (normal approximation + 1)."""
    za, zb = st.norm.ppf(1 - alpha / 2), st.norm.ppf(power)
    return int(math.ceil(2 * ((za + zb) * sd / delta) ** 2)) + 1


def sample_size_icc(rho0, rho1, k=2, alpha=0.05, power=0.8) -> int:
    """Walter, Eliasziw & Donner (1998) approximation: n subjects to show ICC > rho0 when true is rho1."""
    za, zb = st.norm.ppf(1 - alpha), st.norm.ppf(power)
    c0 = (1 + k * rho0 / (1 - rho0))
    c1 = (1 + k * rho1 / (1 - rho1))
    return int(math.ceil(1 + 2 * (za + zb) ** 2 * k / ((math.log(c1 / c0)) ** 2 * (k - 1))))
