# Project 2 sensitivity run

From the Project 2 folder, run `python validate_project.py`. The figures below were produced using freshly downloaded Yahoo Finance adjusted closes for the model's fixed October 2021–October 2026 sample.

```text
Baseline: 60 returns through October 2026
VT expected return input: 10.55%
SGOV: 55.00%
IEF: 0.00%
BND: 0.00%
VT: 45.00%
Expected return (minimum 6.50%): 6.83%
Annual volatility: 6.74%
Eligible reserve weight (minimum 3.00%): 55.00%
Modeled mandate verdict: PASS

Cost stress: 50 basis points per year, return shown net of cost
VT expected return input: 10.55%
SGOV: 50.00%
IEF: 0.00%
BND: 0.00%
VT: 50.00%
Expected return (minimum 6.50%): 6.67%
Annual volatility: 7.48%
Eligible reserve weight (minimum 3.00%): 50.00%
Modeled mandate verdict: PASS

Reserve stress: SGOV excluded and no other sleeve qualifies
VT expected return input: 10.55%
Modeled mandate verdict: FAIL (no qualifying mix)

Sample-end stress: exclude the final six returns (end April 2026)
VT expected return input: 10.94%
SGOV: 60.00%
IEF: 0.00%
BND: 0.00%
VT: 40.00%
Expected return (minimum 6.50%): 6.65%
Annual volatility: 6.24%
Eligible reserve weight (minimum 3.00%): 60.00%
Modeled mandate verdict: PASS

Pause the pilot if a required scenario has no qualifying mix.
The sample-end stress uses today's adjusted prices and is retrospective.
```
