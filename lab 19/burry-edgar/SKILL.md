---
name: burry-edgar
description: Apply the Lab 19 Burry cash-conversion and liabilities screen and write a separate skeptical memo from printed SEC evidence.
---

Read-only philosophy reference: https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/michael_burry.md. Emphasize earnings backed by cash, hidden obligations, skepticism, and a bear case. Classroom rules override upstream price targets, forecasts, holdings, confidence scores, and estimation instructions.

From lab 19 run `python panel.py TICKER` or add `--facts PATH` for saved SEC companyfacts. Shared edgar.py preserves all Lab 18 source and calculation rules: exact 10-K, five latest fiscal ends, latest filing wins, annual flows, tag priorities, and honest gaps. Liabilities uses the exact us-gaap:Liabilities tag; no subtraction fallback or guessed debt.

`panel.burry_checks` requires operating cash flow at least net income in every annual row, and latest liabilities/year-end equity no more than two. Every-year checks need all five complete annual pairs; missing inputs mean not known. Nonpositive or absent equity makes the ratio not known. A latest-year check needs only the latest row; never mistake it for an every-year rule.

Read printed output and write `output/TICKER_Burry_memo.md`, labelled AI simulation, not the real investor's opinion. Choose own the business, watch it, or pass independently of check count. Use only printed numbers. Describe cash evidence, a supported bear case, unresolved footnotes or earnings quality, and evidence that would change your verdict. Passing checks cannot establish clean accounting or value; do not allege fraud without evidence. Audit using `panel.audit`, review units and meaning, and bind .sha256 to `edgar.fingerprint(report)`. Preserve unknowns even when other investors pass.
