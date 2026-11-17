# Project 2 point-in-time data card

| Field | Definition and control |
|---|---|
| Measure | Yahoo Finance daily adjusted closing prices in USD for SGOV, IEF, BND, and VT, reflecting distributions and splits. |
| As-of and acquisition | The report uses a November 17, 2026 download. The fixed observation window is October 2021 through October 2026. November prices and later observations are excluded. |
| Month selection | Keep the final available trading-day adjusted close per calendar month. Require 61 positive, finite observations per ticker. Stop on missing or invalid month-end prices. |
| Transformations | Compute consecutive month-to-month simple returns. Annualize the arithmetic mean by multiplying by 12 and sample standard deviation by multiplying by the square root of 12. Use monthly correlations. The recent window takes the final 36 returns. |
| Availability rule | For a committee analysis as of a stated date, use only completed months with observations already published by that date and an adjustment vintage available at that date. The downloader enforces the observation window. The provider does not supply historical publication or revision vintages through this workflow. |
| Revisions and intended use | Later vendor corrections and corporate-action adjustments may alter observations. Treat this download as a retrospective sample for a research pilot. A historical backtest or live decision requires a date-stamped source vintage and a documented availability rule. |
| Licensing and privacy | The project publishes acquisition code and derived results. Vendor price files remain with the provider. The route uses public fund symbols and requires no user credentials or personal data. |

[Source notes](sources.md) · [Download code](../prices.py) · [Lab 16 timing example](../../lab%2016/Lab15_checkout.md) · [Lab 17 vintage audit](../../lab%2017/README.md)
