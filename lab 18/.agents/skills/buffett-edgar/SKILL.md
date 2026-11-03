---
name: buffett-edgar
description: Screen a ticker using five years of SEC 10-K facts, computed Buffett checks, and a short business-quality memo without prices. Use for the Buffett EDGAR lab or repeatable company-quality screening.
---

Use only keyless SEC EDGAR for numbers. Never install FAskills or use its paid data. The classroom reference is https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/warren_buffett.md (read only); use its emphasis on understandable economics, durable advantages, and stewardship. The lab rules override its price analysis and estimation instructions.

From the lab folder run `python buffett-edgar/scripts/edgar.py COST`, substituting the requested ticker. Set SEC_USER_AGENT to the user's real name and email; the bundled default is the repository owner's connected GitHub identity and email. All arithmetic belongs in the script.

Rules: 10-K only; last five fiscal-year-end dates; one-year flows (including 52/53-week years); latest filing wins for the same period; revenue tags RevenueFromContractWithCustomerExcludingAssessedTax then Revenues; net income NetIncomeLoss; cash flow NetCashProvidedByUsedInOperatingActivities; capex PaymentsToAcquirePropertyPlantAndEquipment then PaymentsToAcquireProductiveAssets; equity StockholdersEquity. Missing values print `not found`. ROE is net income / year-end equity; nonpositive equity yields `not known`. Owner earnings is operating cash flow minus capex. A check with missing inputs is `not known`. No estimates or forced known-answer matches.

Read the printed report and write `output/TICKER_memo.md` yourself in a Buffett-inspired first-person voice, explicitly labelled AI simulation, not Buffett's actual opinion. Choose own the business, watch it, or pass. Judge the business only, not price. Use only printed numbers, with no mental arithmetic. Discuss durable advantage, predictability, and stewardship only to the extent supported; numeric screens alone cannot establish them. For missing owner earnings explicitly say you cannot judge owner earnings.

Apply the reference's business-ownership questions in a short memo: what does the historical record support; what remains unknown about understandable economics, competitive durability, and management; what evidence would change the verdict? Distinguish observed results from your interpretation. With only this numeric report, explicitly leave unsupported qualitative claims unresolved. Passing checks do not automatically mean own the business; failing or unavailable checks do not automatically mean pass. Do not invent a moat, management facts, confidence scores, or forecasts to complete the reference's output template.

The classroom calculation is a cash-flow proxy, not the reference's estimate of distributable earnings using maintenance spending. Do not import its alternative formula, valuation template, price targets, projected growth, news, holdings, or data integrations. Use the local rules even if the upstream reference changes. Reference reviewed: `financial-researcher/experts/warren_buffett.md`, Git blob `7409039b40f5858f34f5ac5aad676338ac2b495e`.

Run `python buffett-edgar/scripts/edgar.py --audit output/TICKER_memo.md --report output/TICKER.json --bind-memo`. Fix unsupported numbers, then review the meaning and units manually. Numeric occurrence alone does not validate a claim. The hash binds the memo to the reviewed report.

Run `python -m streamlit run app.py`. The app loads saved reports, fetches fresh facts, plots both series, shows tags and provenance, and audits memo edits. Keep classroom expected values only in tests, never as runtime financial data. Explain disagreements honestly. Ask the student to supply their personal decision; do not impersonate it.
