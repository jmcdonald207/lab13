# Video 3 — Investment Committee Presentation

> **Status: User-provided presentation script.** This is not yet a verified word-for-word transcript of a recording. After recording, compare it with the audio and correct any differences before submitting.

## Slide 1 — Investment Recommendation

Good afternoon. My name is Joshua McDonald, and today I'll present the results of my portfolio optimization application and my recommendation to the investment committee.

AI assisted with the development, testing, and documentation of this project. This presentation is for education, not investment advice.

My recommendation is to **approve continued research and testing of the application, but defer live investment** until several important uncertainties have been resolved.

## Slide 2 — Investment Objectives and Constraints

The original investment mandate establishes a seven-year investment horizon, annual rebalancing, and a return objective of inflation plus four percent.

For this project, I used a 6.5% expected annual return hurdle and a 3% minimum reserve requirement, representing $3 million in liquid reserves for a $100 million portfolio.

The application analyzes four ETFs: SGOV, IEF, BND, and VT.

Its goal is to identify the lowest-volatility portfolio that meets the modeled return and reserve requirements.

## Slide 3 — Financial Results

Looking at the results from my GitHub repository, the application produced two significantly different investment allocations.

Using the full 60-month estimation window, the model recommended **55% SGOV and 45% VT**, producing an expected annual return of 6.83% and annual volatility of 6.74%.

However, shortening the window to 36 months changed the recommendation to **85% SGOV and 15% VT**, with an expected return of 6.85% and volatility of 1.77%.

Both portfolios passed the modeled requirements, but the 30-percentage-point difference in equity exposure shows how sensitive the results are to historical assumptions.

## Slide 4 — Risks and Sensitivity Analysis

I also tested how the application responded to changes in financial assumptions.

Adding 0.5% in annual investment costs increased the recommended VT allocation from 45% to 50%, while the portfolio continued to pass the modeled requirements.

However, when SGOV was excluded from eligible reserves, the application could no longer identify a qualifying portfolio.

Additionally, the original mandate's calendar-year loss requirement has not been fully evaluated.

These limitations suggest that the model is useful for research but is not ready to support actual investment decisions.

## Slide 5 — Committee Recommendation

Based on these findings, I recommend approving a research pilot rather than immediately implementing the portfolio.

During the pilot, the portfolio analyst should monitor allocations, expected returns, reserve requirements, and mandate compliance monthly.

If either estimation window fails the modeled constraints or the data validation process fails, the pilot should be paused.

Before approving live investment, the committee should confirm SGOV's reserve eligibility, establish a consistent allocation methodology, and address the calendar-year loss constraint.

**Overall, my recommendation is to continue researching the application while withholding authorization for live investment.**

Thank you for your time.

## Source files

[Decision memo](../docs/decision-memo.md) · [Saved results](../output/results.md) · [Validation](../docs/validation-and-ai-use.md)
