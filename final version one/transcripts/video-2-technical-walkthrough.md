# Video 2 — Technical Walkthrough of My Financial Applications

> **Status: User-provided presentation script.** This is not yet a verified word-for-word transcript of a recording. After recording, compare it with the audio and correct any differences before submitting.

## Introduction

**[Show your GitHub repository or the first application]**

Hello, my name is Joshua McDonald, and in this video, I'll walk through five financial applications I developed throughout this course and explain how they support portfolio management, financial analysis, and investment decisions.

AI assisted with the development, testing, and documentation of these applications. This presentation is for education, not investment advice.

Each application focuses on a different part of the financial decision-making process, including portfolio optimization, sensitivity analysis, historical data verification, and fundamental company analysis.

## Application 1 — Project 2 Portfolio Screen

**[Show Project 2 Portfolio Screen — Port 8513]**

Starting with my Project 2 Portfolio Screen, this application is designed to identify the lowest-risk investment portfolio that satisfies specific financial constraints.

The model uses adjusted historical closing prices from Yahoo Finance for four ETFs: SGOV, IEF, BND, and VT.

The first interactive feature allows users to select either the full 60-month estimation window or the most recent 36 months.

The second feature allows users to manually adjust VT's expected annual return to observe how changing financial assumptions affects the optimal portfolio.

Looking at the current results, the model recommends allocating 55% to SGOV and 45% to VT, producing an expected annual return of 6.83% and annual volatility of 6.74%.

The application also checks whether the portfolio meets a minimum 6.5% expected return and a 3% reserve requirement.

In this case, the portfolio passes both modeled constraints.

However, switching to the 36-month estimation window produces a significantly different portfolio, illustrating the sensitivity of optimization models to historical assumptions.

## Application 2 — Meridian Portfolio Explorer

**[Switch to Meridian Portfolio Explorer — Port 8515]**

The second application is the Meridian Portfolio Explorer.

This application allows users to experiment more directly with financial assumptions and portfolio constraints.

On the left side, users can change the expected-return objective, adjust the minimum reserve requirement, and choose between training assumptions and uploaded financial data.

The application also allows users to change expected returns for individual investments and select which assets qualify as reserves.

One particularly useful feature is the side-by-side comparison between the portfolio calculated using current inputs and the portfolio calculated using the original loaded assumptions.

Here, both portfolios currently have an expected return of 6.51%, volatility of 9.44%, and reserve-eligible weight of 20%.

However, changing an expected-return assumption can produce a different optimal allocation.

The application measures this difference using the largest weight change, allowing users to evaluate how sensitive the recommendation is to changes in financial assumptions.

## Application 3 — Point-in-Time Rates

**[Switch to Point-in-Time Rates — Port 8517]**

The third application focuses on financial data reliability rather than portfolio optimization.

It retrieves economic data from FRED and ALFRED, including corporate bond yields, the federal funds rate, 10-year Treasury yields, and mortgage rates.

Users can select different economic indicators, add new series, and adjust the historical chart period.

The most important feature is the "As known on" date selector.

This allows users to compare economic information that was available on a historical date with information available today.

For example, an economic indicator might have been revised after its initial publication.

If an investment model uses revised information that was not available at the time, it could create misleading backtesting results.

The application also includes an as-of audit table showing observation dates, values, and validation status.

Overall, this tool demonstrates why data timing, historical availability, and revisions are important in financial modeling.

## Application 4 — Buffett Business Notebook

**[Switch to Buffett Business Notebook — Port 8518]**

The fourth application analyzes company financial statements using a Buffett-inspired investment approach.

Users can enter a stock ticker and retrieve financial information directly from SEC EDGAR.

For this demonstration, I'm using Costco.

The application displays five years of financial information, including revenue, net income, operating cash flow, capital expenditures, and shareholders' equity.

It also calculates financial ratios and owner earnings, which this application defines as operating cash flow minus total capital expenditures.

For Costco, the financial screening tests show that return on equity exceeded 15% in every reported year, owner earnings remained positive, and owner earnings increased from the first year to the last.

All three financial checks passed.

The application also includes an AI-assisted business-quality memo.

In this example, the recommendation is to watch Costco rather than immediately invest, because strong historical financial performance does not necessarily prove a lasting competitive advantage.

Another feature is the memo validation process, which checks whether numerical values used in the memo appear in the underlying financial report.

This helps identify unsupported numbers in AI-generated financial analysis, although the meaning of those numbers still requires human review.

## Application 5 — Same Facts, Different Investors

**[Switch to Same Facts, Different Investors — Port 8519]**

The fifth application examines how different investment philosophies can produce different conclusions from the same financial data.

It uses SEC financial statements and evaluates companies through three investor-inspired perspectives: Warren Buffett, Cathie Wood, and Michael Burry.

The Buffett-inspired approach focuses on profitability and consistent owner earnings.

The Cathie Wood-inspired approach emphasizes high revenue growth and research-and-development investment.

The Burry-inspired approach emphasizes cash flow and balance-sheet strength.

Using Costco as an example, the company passes all three Buffett-inspired checks and both Burry-inspired checks.

However, it fails the Cathie Wood-inspired revenue growth requirement because its annualized revenue growth of 7.51% is below the application's 15% threshold.

The research-and-development check is also marked as unknown because the required information was not found in the selected financial data.

This demonstrates that different investment strategies can interpret the same financial information differently.

The application also includes separate investment memos and checks for numerical consistency between those memos and the source reports.

## Conclusion

**[Return to GitHub or Project 2 Portfolio Screen]**

Overall, these five applications demonstrate different components of financial decision-making.

The portfolio applications identify allocations that satisfy modeled investment constraints and test their sensitivity to changing assumptions.

The Point-in-Time Rates application evaluates whether historical economic information was actually available when investment decisions would have been made.

Finally, the two company-analysis applications demonstrate how financial statements, quantitative screening rules, and AI-assisted judgments can support investment research.

One important lesson from developing these applications is that **correct financial calculations do not automatically guarantee correct investment decisions**.

Data quality, financial assumptions, model limitations, and human judgment all remain important.

Together, these applications demonstrate how Python and AI can support financial analysis while allowing users to independently examine the underlying evidence.

## Source files

[Project 2 app](../app.py) · [Meridian app](../../lab15/app.py) · [Point-in-Time app](../../lab%2017/asof_app.py) · [Buffett notebook](../../lab%2018/app.py) · [Investor panel](../../lab%2019/app.py)
