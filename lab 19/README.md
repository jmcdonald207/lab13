# Lab 19: same facts, three investor perspectives

Question: When three investors' skills read the same 10-K facts, where do they agree, where do they split — and would you trust the panel?

This extends Lab 18 with two FAskills-inspired skills, a shared deterministic panel, separate AI-authored memos, and a Streamlit app. Lab 18 remains unchanged. All three read the same facts and printed report; the investor checks are Python functions, and the memos are reviewed judgments, not automatic check-count verdicts. This is a sequential skill panel, not independent models or a claim that real investors endorsed these views.

## Run

```powershell
cd "lab 19"
python -m pip install -r requirements.txt
python panel.py COST --facts output/COST_facts.json
python panel.py JPM --facts output/JPM_facts.json
python panel.py COST --facts output/COST_facts.json --growth-threshold 5
python review_memos.py
python -m unittest -v test_panel.py
python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8520
```

Open http://127.0.0.1:8520 and leave the process running. The app opens COST by default, loads saved reports without internet, retains the Lab 18 chart, table, source provenance, memo editing and downloads, numeric audit, stale-memo binding warning, SEC refresh, and personal decision field. It adds the panel table and three verdict/memo columns. Replace the ticker with JPM for the selected company's run. To refresh live data use `python panel.py COST` or `python panel.py JPM`, with SEC_USER_AGENT set to your name and email; then rewrite/review memos before binding them again.

The included `output/*_facts.json` files are subsets of the existing Lab 18 SEC companyfacts caches. Observations are retained without changing their values; `prepare_sources.py` exports them and verifies identical reports against the full source caches. The source manifest records both hashes and SEC URLs. They are saved source snapshots, not newly downloaded facts. Fiscal period, tag, filing date, and accession are preserved in the derived reports. Missing R&D and capex stay missing. There is no handout answer input in runtime code.

## My request to the AI

> Preserve my Lab 18 Buffett skill and app behavior. Extend the same five annual 10-K facts with Liabilities and ResearchAndDevelopmentExpense. Build Cathie Wood and Burry skills from the FAskills philosophy pages using the assignment's exact checks in Python. Calculate revenue CAGR as (last/first)^(1/4)-1. Each skill must read the printed report and write its own labelled AI-simulation memo and verdict using printed numbers only. Display investor × check statuses, three verdicts and memos side by side, and audit all edited memos for unprinted numbers. Preserve unknown inputs, source tags, and filing provenance. Reproduce COST without forcing the expected answer; save the 5% threshold probe separately. Select a fund with a verified largest holding, run that company, and write evidence-based bull/bear arguments and a conditional screening decision. Do not claim partner or quiz activities were completed.

## Known answer and probe

The computed COST run gives Buffett 3 of 3; Cathie Wood growth fails at 7.51% and R&D is not known; Burry 2 of 2 with latest liabilities/equity 1.49. The five ratio values round to 2.11, 1.75, 1.96, 1.64, 1.49. R&D expense is not found in every year. See [printed report](output/COST_report.txt) and the automated known-answer assertions in `test_panel.py`.

The saved [5% probe](output/COST_probe_5_report.txt) passes Wood's growth check while R&D stays not known. The baseline keeps 15% to preserve the assigned high-growth definition rather than tune it to admit COST. To perform the probe by editing the skill itself, change `cathie-wood-edgar/rules.json` from 15 to 5, rerun COST, observe the check, then restore 15 and rerun. The CLI override uses the same check function but saves a separate report. Re-review baseline memos after any report change.

## Selected fund and company

With permission to choose a fund, the final choice is Fidelity MSCI Financials ETF (FNCL). [Fidelity's holdings page](https://research2.fidelity.com/fidelity/screeners/etf/public/etfholdings.asp?sortBy=Symbol&sortDir=asc&symbol=FNCL&view=Holdings), read on November 5, 2026, shows JPMorgan Chase (JPM) first at 10.48%, ahead of Berkshire Hathaway at 8.37%, with holdings dated August 31, 2026. This is a selected fund for this lab, not a claim about previously submitted Project 2 choices. JPM files 10-Ks, so no next-largest-company exception is needed.

VOO/NVDA was initially considered. Its SEC download failed in the managed process; the final FNCL/JPM selection uses the already available Lab 18 source cache and is explicitly documented. It does not claim NVDA lacks a 10-K. See [checkout](CHECKOUT.md) for JPM's panel, bull/bear, and a draft decision.

## Code to explain

Open `cathie_checks` in `panel.py`. `limit` reads the skill threshold unless a probe override is supplied. `growth` reads the computed CAGR. `latest` safely obtains the latest annual values or an empty dictionary. `rd` reads the R&D ratio; absence returns None. Each `status` call returns not known when the value is None; otherwise its inclusive comparison produces pass or fail. A missing input never becomes zero. `build` computes CAGR only with five annual rows and valid endpoints; it computes R&D intensity only with observed expense and positive revenue. Do not round before comparing thresholds.

The numeric flag scans every numeric occurrence in every memo editor against the shared printed report. Try `987654321.123%` independently in each memo; each must trigger the flag. Matching numeric occurrence cannot validate meaning, units, or an inference; those still require review. Missing memos and stale bindings produce separate warnings.

## Sources

- [FAskills Cathie Wood](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/cathie_wood.md): innovation, reinvestment, and adoption lens. The classroom growth/R&D cutoffs are assignment rules, not claims of her actual screening method.
- [FAskills Burry](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/michael_burry.md): cash-backed earnings, balance-sheet skepticism, and bear cases. The classroom cutoffs are assignment rules.
- [FAskills Buffett](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/warren_buffett.md): business durability, stewardship, and owner earnings.
- [SEC EDGAR API](https://www.sec.gov/search-filings/edgar-application-programming-interfaces): companyfacts and source context.
- [Streamlit columns](https://docs.streamlit.io/develop/api-reference/layout/st.columns): three side-by-side memo containers.

FAskills is a read-only philosophy reference, not installed or executed. Its predictions, price targets, paid integrations, alternative formulas, and numeric confidence scores are excluded by the classroom rules. Skills are also discoverable under `.agents/skills` when Codex starts in this folder.
