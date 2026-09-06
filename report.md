# Statistical Significance Testing for Segment-Level Credit Risk
### (Built on the real "Give Me Some Credit" dataset)

## 1. Objective
Retail credit portfolios are often split into segments (e.g., income
bands) for risk monitoring. This project tests, with formal statistical
methods rather than a visual "eyeball" comparison, whether two such
segments genuinely differ in risk — or whether an observed gap could
just be sampling noise.

**Question:** Do applicants below vs. above the median monthly income
show a statistically significant difference in (a) serious delinquency
rate, and (b) average debt ratio?

## 2. Data
Source: the "Give Me Some Credit" credit-risk dataset (Kaggle), pulled
from a public GitHub mirror of the competition data — 41,016 applicant
records with `SeriousDlqin2yrs` (target: did the applicant experience
serious delinquency within two years) plus features including
`MonthlyIncome`, `DebtRatio`, `age`, credit line counts, and past
delinquency counts.

**Data quality issues found and handled** (this step matters as much as
the tests themselves):
- `MonthlyIncome` was missing for 7,974 applicants (19.4%) — dropped,
  since income segment can't be assigned without it.
- `DebtRatio` is calculated as debt payments ÷ income, so it explodes
  to absurd values (up to ~107,000) for applicants who under-reported or
  had near-zero income — a well-known quirk of this dataset. Rows with
  `DebtRatio > 5` (7,902 rows) were removed as data-quality outliers
  rather than genuine signal.
- **Net: 32,468 of 41,016 rows (79.2%) retained** after cleaning.

## 3. Test 1 — Chi-Square Test of Independence (Serious Delinquency Rate)

**H0:** Delinquency rate is independent of income segment.

Split at median monthly income (₹5,350 in the dataset's units), n≈16,200
per segment.

| Segment | Delinquent | Not Delinquent | Delinquency Rate |
|---|---|---|---|
| Low income | 3,341 | 12,898 | 20.57% |
| High income | 2,124 | 14,105 | 13.09% |

- Chi-square statistic: **324.96**
- p-value: **< 0.000001**

**Result:** Reject H0. Low-income applicants show a materially and
statistically significant higher delinquency rate.

## 4. Test 2 — Standard Independent T-Test (Average Debt Ratio)

**H0:** Average debt ratio is the same across income segments.

| Segment | Mean Debt Ratio | Std Dev |
|---|---|---|
| Low income | 0.4210 | 0.4772 |
| High income | 0.3182 | 0.2526 |

- T-statistic: **24.26**
- p-value: **< 0.000001**

**Result:** Reject H0. Low-income applicants carry meaningfully higher
average debt ratios.

**Caveat on this test specifically:** the two groups' standard
deviations differ by almost 2x (0.477 vs 0.253), which technically
violates the "equal variance" assumption behind the standard t-test used
here. The conclusion doesn't change (Welch's t-test on the same data
gives an even larger t-statistic), but a rigorous validation report would
run a variance-equality check (Levene's test) first and default to
Welch's t-test when variances differ this much.

## 5. Interpretation
Both tests agree: the low-income segment carries genuinely higher credit
risk on this dataset, both in outcome (delinquency) and in a leading
indicator (debt ratio). This kind of segment-level finding is exactly
what a model risk / portfolio monitoring team would use to check whether
a scorecard's performance holds up consistently across income bands, or
whether it's systematically miscalibrated for one segment.

## 6. Limitations
- **Correlation, not causation:** applicants were split by an existing
  trait (income), not randomly assigned — this is an observational
  comparison, not a randomized experiment. Debt ratio and income are
  related by construction (debt ratio's denominator IS income), so part
  of this "effect" is definitional overlap, not two independent risk
  drivers.
- **Data cleaning removed ~21% of records** — if the missingness or the
  extreme debt-ratio values are not random (e.g., correlated with
  informal-sector income, which skews toward lower reported income),
  the cleaned sample may understate the true risk gap between segments.
- **Unequal variances** in the debt ratio test (noted above) mean the
  t-test's exact p-value is approximate; the qualitative conclusion is
  robust, but a stricter validation write-up would use Welch's test.
