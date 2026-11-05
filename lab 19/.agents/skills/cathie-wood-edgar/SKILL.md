---
name: cathie-wood-edgar
description: Apply the Lab 19 Cathie Wood growth and R&D screen to SEC facts and write a separate evidence-based innovation memo.
---

Read-only philosophy reference: https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/cathie_wood.md. Use innovation, reinvestment, and long-term adoption questions. Classroom rules override the upstream predictions, price targets, holdings, confidence scores, and estimates.

From lab 19 run `python panel.py TICKER`; or add `--facts PATH` for saved SEC companyfacts. The shared edgar.py preserves Lab 18 tag priorities, latest-filed annual 10-K selection, five fiscal dates, 350–380-day flows, year-end equity, and missing inputs. Added tags are Liabilities (instant) and ResearchAndDevelopmentExpense (annual flow). Do not fill missing R&D with zero or infer innovation from its absence.

The checks run in `panel.cathie_checks`: revenue growth `(last / first)^(1/4) - 1` must meet the threshold in this skill's `rules.json` (default 15 percent); latest R&D/revenue must be at least 5 percent. Missing endpoints, fewer than five annual dates, invalid revenue denominators, or missing R&D produce not known. Probe by changing rules.json to 5 and rerunning; restore 15 if keeping the assigned growth definition. A CLI `--growth-threshold 5` produces a separate probe report without replacing the baseline.

Read the printed report before writing `output/TICKER_Cathie_Wood_memo.md`. Label AI simulation, not the real investor's opinion. Choose own the business, watch it, or pass, separately from the mechanical check count. Use only printed numbers; identify unknown innovation economics and evidence that would change your verdict. Do not assert actual trades or innovation leadership from ratios. Under the memo record the retained growth threshold and reason. Audit with `panel.audit`; after reviewing meaning and units, bind a .sha256 file to `edgar.fingerprint(report)`. The app audits all three memos including edits and warns if bindings are stale.
