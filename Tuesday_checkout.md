# Tuesday risk engine checkout

Inputs are course-authored training values, not market estimates. CPI is a labelled 2.5% estimate; CPI + 4% gives the 6.5% expected-return objective.

Run from this folder:

```text
python portfolio.py
python test_portfolio.py
python mandate.py
```

Weights below follow bills / 10-year note / IG bonds / equity.

| Portfolio | Weights (%) | Return (%) | Volatility (%) | Reserve (%) | Meets 6.5%? |
|---|---|---:|---:|---:|---|
| Benchmark | 0.0 / 0.0 / 40.0 / 60.0 | 6.80 | 10.46 | 0.0 | Yes |
| Equal weight | 25.0 / 25.0 / 25.0 / 25.0 | 5.20 | 5.21 | 50.0 | No |
| Inverse volatility | 84.3 / 6.0 / 7.0 / 2.6 | 3.77 | 1.05 | 90.3 | No |

Rounded inverse-volatility weights total 99.9%; calculations use full precision.

## Verification

The test file checks every displayed known answer. It changes both IG–equity correlations to 0.50 in a copy and checks benchmark volatility of 11.00%. Temporary script copies verify that the command refuses 1.3 and an asymmetric table. The submitted inputs retain 0.25.

The first Lab 13 rerun printed `Input error: Missing holdings table and/or candidate weights. Fill in HOLDINGS and CANDIDATES at the top of this file.` Original A–C holdings and allocations were absent, so their verdicts cannot be reproduced. Candidate E now uses the supplied four sleeves and reserve eligibility. Redemption days (one for Treasuries, two for funds) are labelled training assumptions. Existing mandate thresholds are retained.

Candidate E fails the reserve rule: 0.0% eligible against the checker's 3.0% minimum. It meets the return objective but fails the mandate. The other baselines miss the return objective. No baseline satisfies all stated requirements. The calendar-year loss rule remains unresolved in the original checker.

## Explain diversification

Portfolio return is the weighted sum of sleeve returns. Covariance entry i,j is correlation i,j times volatility i times volatility j. Portfolio variance sums weight i times weight j times covariance i,j over every pair. The square root converts variance into volatility. Both i,j and j,i are included, giving the factor of two in the two-asset formula.

Benchmark by hand, using decimal units:

```text
variance = (0.4 × 0.06)^2 + (0.6 × 0.16)^2
         + 2 × 0.4 × 0.6 × 0.25 × 0.06 × 0.16
         = 0.010944
volatility = sqrt(0.010944) = 0.1046136 = 10.46%
```

Correlation below +1 lowers the cross term relative to perfectly correlated assets. Imperfectly synchronized movements can make a combination less risky than either holding, but do not guarantee that outcome. This benchmark is less risky than equity alone and more risky than IG bonds alone. Omitting covariance gives 9.90%, the assignment's classic error.

Inverse volatility puts most weight in bills because their volatility is only 0.5%; their reciprocal volatility is much larger than the other sleeves'. This method targets neither the return objective nor mandate compliance.

A possible CIO discussion starts with the benchmark: it meets the return objective but exposes the reserve shortfall. Compare the other baselines to show the return–risk tradeoff. This is a discussion prompt, not a claim about the student's personal reflection.

## Student work still required

- Partner explanation, swap-and-break exercise, and personal reflection.
- Quiz: in `portfolio_volatility`, why does the sum loop over both i and j? Answer before requesting an explanation.
- Thursday: select three to six funds for your own mandate, verify five years of monthly adjusted closes, and record ticker, name, role, source, and download date here. Your own mandate and fund selections were not supplied; no prices or source records have been invented.
- GitHub submission files: [portfolio.py](https://github.com/jmcdonald207/lab13/blob/main/portfolio.py), [mandate.py](https://github.com/jmcdonald207/lab13/blob/main/mandate.py), [test_portfolio.py](https://github.com/jmcdonald207/lab13/blob/main/test_portfolio.py), and [these notes](https://github.com/jmcdonald207/lab13/blob/main/Tuesday_checkout.md).
