# Synthetic Project 2 results

Run November 17, 2026. Price dates January 2021 to January 2026 are simulated.

| Measure | All 60 returns | Last 36 returns | All 60 with VT stressed |
|---|---:|---:|---:|
| VT annual return input | 8.00% | 7.00% | 7.00% |
| SGOV | 5.00% | 5.00% | 5.00% |
| IEF | 10.00% | 0.00% | 0.00% |
| BND | 30.00% | 15.00% | 15.00% |
| VT | 55.00% | 80.00% | 80.00% |
| Expected annual return | 6.51% | 6.52% | 6.53% |
| Annual volatility | 7.60% | 10.95% | 10.89% |
| Eligible reserves | 5.00% | 5.00% | 5.00% |
| Modeled mandate verdict | PASS | PASS | PASS |

Baseline command is `python run.py`. Stress command is `python run.py --equity-return 7`. The recent window already estimates 7.00% for VT and reproduces the recent-window verdict under the override.
