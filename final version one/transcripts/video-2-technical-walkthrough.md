# Video 2 — Technical walkthrough

Recording script. Update this file to match the spoken recording before submitting it as the final transcript.

AI assisted with the code, repository documentation, and this script. This is education, not investment advice.

Start in the submission folder with `python run.py`. The downloader requests daily adjusted closes in US dollars and keeps each completed month's last available trading observation. It requires 61 monthly observations per fund and stops on missing or invalid prices. The data is a November 17, 2026 retrieval for October 2021 through October 2026. The provider can revise adjusted prices, so these results support retrospective research.

In `run.py`, each monthly simple return is the new adjusted price divided by the previous adjusted price, minus one. The code multiplies the monthly arithmetic mean by 12 and the monthly sample standard deviation by the square root of 12. It combines the volatilities and monthly correlations into a covariance matrix. The recent window uses the final 36 monthly returns.

In `search_portfolio`, the engine enumerates long-only mixes in five-percentage-point increments that sum to 100%. It filters by the 6.50% return hurdle and the 3% reserve minimum, then selects the lowest-volatility eligible mix. SGOV is the only modeled qualifying reserve sleeve.

The documented stress run used `python run.py --equity-return 9.55`. In the full window, the revised VT estimate moved VT weight from 45% to 50% and annual volatility from 6.74% to 7.48%. The stressed allocation returned an estimated 6.67%, held 50% modeled eligible reserves, and still passed. The run checks how sensitive the allocation is to one return estimate.

[Downloader](../prices.py) · [CLI](../run.py) · [Engine](../portfolio.py) · [Recorded results](../output/results.md)
