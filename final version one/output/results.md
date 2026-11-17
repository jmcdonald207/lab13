# Meridian classroom results

Reproduced November 17, 2026, using course-authored training assumptions. Percentages are annual where applicable. This is a classroom model with no market-data as-of date.

| Decision measure | Baseline | Existing Lab 15 stress replay |
|---|---:|---:|
| Equity return input | 8.00% | 7.00% |
| Bills | 0.00% | 0.00% |
| 10-year note | 20.00% | 10.00% |
| Investment-grade bond fund | 25.00% | 10.00% |
| Global equity index fund | 55.00% | 80.00% |
| Expected return, minimum 6.50% | 6.51% | 6.53% |
| Annual volatility | 9.44% | 12.94% |
| Reserve-eligible weight, minimum 3.00% | 20.00% | 10.00% |
| Modeled mandate verdict | PASS | PASS |
| Full mandate review | Unresolved | Unresolved |

Baseline command: `python run.py`. Existing stress replay command: `python run.py --equity-return 7`.

Equity weight increases by 25 percentage points and annual volatility by 3.50 percentage points. The model selects a different allocation to clear the same return hurdle when equity's expected return falls.
