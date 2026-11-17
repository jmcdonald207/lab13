# Input provenance

The tickers are used as labels for four illustrative sleeves. Codex generated the price series on November 17, 2026. No market data was downloaded. The dates identify synthetic periods.

| Ticker | Fund | Modeled role | Reserve eligible |
|---|---|---|---|
| SGOV | iShares 0–3 Month Treasury Bond ETF | Short Treasury reserve proxy | Yes, classroom assumption |
| IEF | iShares 7–10 Year Treasury Bond ETF | Intermediate Treasury exposure | No |
| BND | Vanguard Total Bond Market ETF | Broad investment-grade bond exposure | No |
| VT | Vanguard Total World Stock ETF | Global equity exposure | No |

Each series starts at 100 in January 2021. For the next 60 months, the previous price is multiplied by one plus a synthetic monthly return. The return is the modeled annual drift divided by 12 plus a sine wave with phase 0.4 radians. Annual drifts are 3.5%, 4.3%, 5.0%, and 9.5% for VT's first 24 returns and 7.0% thereafter. In ticker order, wave amplitudes are 0.0015, 0.022, 0.017 and 0.055, with respective periods of 3, 4, 6 and 12 months. The file rounds prices to eight decimals.
