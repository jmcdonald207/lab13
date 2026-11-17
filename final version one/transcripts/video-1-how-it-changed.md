# Video 1 — How it changed

Recording script. Update this file to match the spoken recording before submitting it as the final transcript.

AI assisted with the code, repository documentation, and this script. This is education, not investment advice.

The starting question was how a reserve portfolio could pursue its return objective while still covering payouts. The original mandate called for a seven-year horizon and annual rebalancing. The Project 2 screen turned part of that mandate into checks: a fully invested, long-only allocation, at least 6.50% estimated annual return, and at least 3% in the assumed eligible reserve sleeve.

The early version used classroom estimates. The final version uses Yahoo Finance adjusted closing prices for SGOV, IEF, BND, and VT, with a fixed October 2021 through October 2026 sample. Adding a recent-window comparison changed the question I would bring to the committee. On November 17, 2026, the full window selected 45% VT and the recent window selected 15%. Both passed the modeled checks. That 30-point gap is large enough to make the choice of estimation window a committee decision.

One AI-assisted output worth auditing is the claim that both windows pass despite the allocation gap. The saved output shows 6.83% and 6.85% expected return, both above 6.50%, and modeled eligible reserve weights of 55% and 85%, both above 3%. The repository records the CLI verification by Codex.

**Before recording:** Run the command yourself and describe what you actually checked and observed. Adjust the preceding paragraph to reflect your own verification.

[Original mandate](../../writing.md) · [Results](../output/results.md) · [Validation](../VALIDATION.md)
