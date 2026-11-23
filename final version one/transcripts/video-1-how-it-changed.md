# Video 1 — How My Project Changed (Edition A to Edition B)

> **Status: User-provided presentation script.** This is not yet a verified word-for-word transcript of a recording. After recording, compare it with the audio and correct any differences before submitting.

## Slide 1 — Project title and portfolio management application

Hello, my name is Joshua McDonald, and in this video, I'll explain how my portfolio management project developed from Edition A to Edition B, including how I used artificial intelligence to help improve the application.

AI assisted with the development of my code, documentation, and testing. This presentation is for education, not investment advice.

## Slide 2 — Edition A: Original Portfolio Model

Starting with Edition A, my goal was to develop a tool that could evaluate different investment portfolios and determine whether they satisfied an investment mandate.

The original mandate included a seven-year investment horizon, a return objective of inflation plus four percent, and requirements for liquidity and reserve holdings.

My earlier model used classroom assumptions for four investment categories: Treasury bills, Treasury notes, investment-grade bonds, and global equities.

I compared three approaches: a traditional 60/40 benchmark, an equally weighted portfolio, and an inverse-volatility portfolio.

For example, the 60/40 benchmark produced an expected annual return of 6.8 percent and annual volatility of 10.46 percent. Although it met the return objective, it did not satisfy the required reserve allocation.

The main limitation of this version was that it relied on hypothetical financial assumptions rather than actual market data.

## Slide 3 — Edition B: Improved Application

In Edition B, I expanded the project into a more realistic portfolio optimization tool.

Instead of using only classroom assumptions, the application retrieves historical adjusted closing prices for four exchange-traded funds: SGOV, IEF, BND, and VT.

The program uses these prices to estimate returns, volatility, and correlations before searching for the lowest-volatility portfolio that satisfies the modeled financial requirements.

I also added an interactive Streamlit application that allows users to change the estimation window and expected return assumptions.

## Slide 4 — Comparison of 60-Month and 36-Month Results

One of the most interesting results came from comparing different historical periods.

Using the full 60-month window, the model recommended allocating 45 percent to VT, which represents global equities.

However, when I shortened the estimation window to 36 months, the recommended equity allocation dropped to only 15 percent.

Both portfolios passed the modeled return and reserve requirements, despite having substantially different allocations.

This demonstrated a major limitation of optimization models: even when the calculations are mathematically correct, changes in financial assumptions can produce very different investment recommendations.

## Slide 5 — How AI Helped and What I Learned

AI helped me develop the Python application, organize the repository, document the financial assumptions, and implement validation tests.

However, AI-generated code and explanations should not automatically be trusted. The results still need to be checked against the underlying assumptions, financial formulas, and investment requirements.

The most important lesson from developing Edition B was that an application producing a passing result does not necessarily mean the investment decision is appropriate.

My final recommendation was therefore to continue testing the application through a research pilot rather than immediately investing real money.

Overall, Edition B improved the project by making it more interactive, more closely connected to market data, and more useful for financial decision-making.

Thank you.

## Source files

[Original mandate](../../writing.md) · [Original baseline](../../Tuesday_checkout.md) · [Project 2 results](../output/results.md)
