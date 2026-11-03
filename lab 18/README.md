# Lab 18 — code computes, the model judges

This project downloads SEC companyfacts and implements the classroom rules. No FAskills installation, paid feeds, price data, or expected-answer values are used by the app.

## Run from the repository root

```powershell
python -m pip install -r "lab 18/requirements.txt"
Set-Location "lab 18"
$env:SEC_USER_AGENT = 'jmcdonald207 mcdon207@purdue.edu'
python edgar.py COST
python edgar.py JPM
python verify_live.py
python -m streamlit run app.py
```

Change the contact to your own name and email if you reuse this project. SEC responses and derived reports are saved under `output`. Raw responses remain local and are not included as fabricated sample data. Each derived JSON row records tag, period, filing date, and accession. The text report prints both millions and raw dollars. The app displays the saved snapshot until refreshed.

## Skill discovery

The self-contained authored skill is `buffett-edgar/SKILL.md`, with its script in `buffett-edgar/scripts`. Codex scans `.agents/skills` from its working directory up toward the repository root. The GitHub project also includes a discoverable copy at `lab 18/.agents/skills/buffett-edgar`; launch Codex with **lab 18 as its working directory** to discover it. Local installation in this managed session was blocked by its filesystem policy; the authored copy remains directly readable here. See [official Codex skills documentation](https://learn.chatgpt.com/docs/build-skills).

## My request to the AI

> Use buffett-edgar on COST and JPM. Download only SEC EDGAR facts with my contact in the User-Agent. Apply the specified annual periods, tag priorities, latest-filing selection, and missing-data rules. Print the table, tags and computed checks. Read the printed results and write a short Buffett-inspired business-quality memo, choosing own the business, watch it, or pass, using only printed numbers. Explicitly identify unknowns. Save and audit each memo, then run the Streamlit app and the COST/JPM probes. Never force SEC facts to match the handout.

The model writes the memo after running the report; the app does not silently generate a verdict from check statuses. Then bind the reviewed memo:

```powershell
python edgar.py --audit output/COST_memo.md --report output/COST.json --bind-memo
python edgar.py --audit output/JPM_memo.md --report output/JPM.json --bind-memo
```

The included memos are explicitly **pending live data**. They contain no invented financial numbers. They must be rewritten after downloading the reports. A hash detects reports changed after review. The numeric audit accepts equivalent comma/decimal formatting, checks every occurrence, and lists unprinted numeric tokens. It cannot prove correct meaning or units; a printed number could still be misused in a sentence.

## Proof and classroom activities

`python -m unittest -v test_edgar.py` tests synthetic inputs: classroom arithmetic, changing an input changes outputs, missing capex, nonpositive equity, latest annual 10-K wins, tag fallback, and the actual Streamlit memo editor rejecting 40.0%. These tests do **not** prove the live COST or JPM answers. `expected_cost.csv` is the supplied classroom answer, read only by tests and `verify_live.py`. The live verifier reports differences without changing any data. A live JPM result is not forced to have missing capex if SEC actually supplies a permitted tag.

For the hand-number probe, enter `ROE 40.0%.` in COST's memo editor. The app must flag it if the printed report lacks that number. For the fresh-chat comparison, ask a separate browser AI without the skill: “Is Costco a Buffett business? Give its ROE for the last five years.” Record its answer and sources, then compare fiscal dates, equity denominator, and filing vintage. This human exercise has not been performed for you.

For the no-screen partner discussion: owner earnings can be computed from cash flow and capital spending; whether competitive advantages will endure requires judgment. For the code explanation, open `year_row` in `buffett-edgar/scripts/edgar.py`: it selects facts and provenance, keeps absent values as `None`, calculates ROE only with positive equity, and subtracts capex only when both inputs exist. `display_value` turns absent values into the required labels. No missing value becomes zero.

At minute twenty, open Brightspace → Quizzes → Lab 18 yourself. Add your own trust decision in the app under the memo; it saves to `output/TICKER_decision.md`. Suggested starting point, to accept or change: “I trust the computed screen more than the verdict, because historical returns and cash flow do not by themselves prove a durable moat.” This is a draft, not a statement of your personal opinion.

## Verification status in this session

The script's live SEC download was attempted and blocked by the managed environment's outbound socket policy (WinError 10013). The web tool could not retrieve companyfacts either. Therefore live COST/JPM values, exact handout agreement, the completed company memos, and the expected chart trends remain unverified. Do not submit the synthetic tests as live proof. Run the commands above on a network-enabled machine, then ask Codex to write the final memos from the printed reports.

## Sources and scope

- [SEC ticker mapping](https://www.sec.gov/files/company_tickers.json)
- [SEC companyfacts API documentation](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)
- [FAskills Buffett reference page, read only](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/warren_buffett.md)
- [Streamlit chart documentation](https://docs.streamlit.io/develop/api-reference/charts/st.line_chart)

The Buffett reference emphasizes durable competitive advantages, understandable economics, management, and owner earnings. Its valuation, price-target, and maintenance-capex estimation instructions are excluded by this assignment. Here owner earnings is strictly operating cash flow minus total capital spending. ROE uses year-end equity. Liabilities/equity is not part of the requested output and is not calculated. Fiscal flows must span 350–380 days, accommodating standard 52/53-week years; transition short years are not treated as annual flows. Only exact `10-K` forms qualify, not amendments or quarterly filings.
