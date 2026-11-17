# Market data and mandate inputs

Yahoo Finance adjusted daily closes in USD for [SGOV](https://finance.yahoo.com/quote/SGOV/history/), [IEF](https://finance.yahoo.com/quote/IEF/history/), [BND](https://finance.yahoo.com/quote/BND/history/) and [VT](https://finance.yahoo.com/quote/VT/history/). Retrieved November 17, 2026. The fixed sample runs October 2021 through October 2026, excluding November 2026. The downloader uses Yahoo's adjusted close field, which reflects distributions and splits, and takes the last available trading-day observation in each month. It requires 61 valid observations per fund and does not fill missing months. Source revisions and later adjustment factors can change the downloaded series. [Acquisition code](../prices.py)

SGOV is the short Treasury reserve proxy, IEF provides intermediate Treasury exposure, BND provides broad bond exposure, and VT provides global equity exposure. The classroom mandate assumes only SGOV is reserve eligible, a 3% reserve minimum, and a 6.50% annual expected-return hurdle. Actual committee eligibility remains open.

Yahoo Finance asks users to avoid redistributing its information. The repository contains acquisition code and derived decision results. [Yahoo Finance data notice](https://help.yahoo.com/kb/finance/article-exchanges-data-delays-sln2310.html)
