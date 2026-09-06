"""
analysis.py
Statistical Significance Testing for Segment-Level Credit Risk
-- built on the real "Give Me Some Credit" dataset --

Question: Do applicants below vs. above the median monthly income show a
statistically significant difference in (a) serious delinquency rate, and
(b) average debt ratio?
"""

import pandas as pd
from scipy import stats

df = pd.read_csv("credit-data-clean.csv")

# --- Split into two segments by median income ---------------------------
median_income = df["MonthlyIncome"].median()
group_low = df[df["MonthlyIncome"] <= median_income]
group_high = df[df["MonthlyIncome"] > median_income]

print(f"Median monthly income split point: {median_income:,.0f}")
print(f"Low-income group  n = {len(group_low)}")
print(f"High-income group n = {len(group_high)}\n")

# =========================================================================
# TEST 1: Chi-Square Test of Independence (Serious Delinquency Rate)
# =========================================================================
n1, n2 = len(group_low), len(group_high)
x1, x2 = group_low["SeriousDlqin2yrs"].sum(), group_high["SeriousDlqin2yrs"].sum()

contingency_table = pd.DataFrame({
    "Delinquent": [x1, x2],
    "Not Delinquent": [n1 - x1, n2 - x2]
}, index=["Low Income", "High Income"])

chi2_stat, p_value_chi2, dof, expected = stats.chi2_contingency(contingency_table, correction=False)

print("=== TEST 1: Chi-Square Test of Independence (Serious Delinquency) ===")
print("Observed:")
print(contingency_table)
print("\nExpected under H0 (no relationship):")
print(pd.DataFrame(expected, columns=["Delinquent", "Not Delinquent"],
                    index=["Low Income", "High Income"]).round(1))
print(f"\nLow-income delinquency rate:  {x1/n1:.4f}")
print(f"High-income delinquency rate: {x2/n2:.4f}")
print(f"Chi-square statistic: {chi2_stat:.3f}")
print(f"p-value:              {p_value_chi2:.6f}")
print(f"Reject H0?             {'YES' if p_value_chi2 < 0.05 else 'NO'}\n")

# =========================================================================
# TEST 2: Standard Independent T-Test (equal variances) on Debt Ratio
# =========================================================================
t_stat, p_value_t = stats.ttest_ind(
    group_low["DebtRatio"], group_high["DebtRatio"], equal_var=True
)
mean1, mean2 = group_low["DebtRatio"].mean(), group_high["DebtRatio"].mean()
std1, std2 = group_low["DebtRatio"].std(), group_high["DebtRatio"].std()

print("=== TEST 2: Standard Independent T-Test (Avg. Debt Ratio) ===")
print(f"Low-income mean debt ratio:  {mean1:.4f} (sd={std1:.4f})")
print(f"High-income mean debt ratio: {mean2:.4f} (sd={std2:.4f})")
print(f"T-statistic:                 {t_stat:.3f}")
print(f"p-value:                     {p_value_t:.6f}")
print(f"Reject H0?                   {'YES' if p_value_t < 0.05 else 'NO'}\n")

results = pd.DataFrame({
    "metric": [
        "n_low", "n_high", "delinquency_rate_low", "delinquency_rate_high",
        "chi2_statistic", "p_value_chi2",
        "mean_debt_ratio_low", "mean_debt_ratio_high",
        "t_statistic", "p_value_ttest"
    ],
    "value": [
        n1, n2, round(x1/n1, 4), round(x2/n2, 4),
        round(chi2_stat, 3), round(p_value_chi2, 6),
        round(mean1, 4), round(mean2, 4),
        round(t_stat, 3), round(p_value_t, 6)
    ]
})
results.to_csv("results_summary.csv", index=False)
print("Saved results_summary.csv")
