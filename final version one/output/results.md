# Real adjusted-close portfolio results

Downloaded and run November 17, 2026. Fixed sample October 2021 through October 2026. The recent return window uses the final 36 monthly returns.

| Measure | Full 60 | Recent 36 | Full 60 at 9.55% VT | Recent 36 at 9.55% VT |
|---|---:|---:|---:|---:|
| VT annual return input | 10.55% | 20.69% | 9.55% | 9.55% |
| SGOV | 55% | 85% | 50% | 55% |
| IEF | 0% | 0% | 0% | 0% |
| BND | 0% | 0% | 0% | 5% |
| VT | 45% | 15% | 50% | 40% |
| Expected annual return | 6.83% | 6.85% | 6.67% | 6.52% |
| Annual volatility | 6.74% | 1.77% | 7.48% | 4.80% |
| Eligible reserve | 55% | 85% | 50% | 55% |
| Modeled verdict | PASS | PASS | PASS | PASS |

Run `python run.py` for the baseline and `python run.py --equity-return 9.55` for the AI-assisted stress replay. [Data source and definitions](../data/sources.md)
