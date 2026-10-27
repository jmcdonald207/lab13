# Lab 15: point-in-time checkout

Question: On the day you would have traded, what did this data actually say, and how much of what you see now came later?

Run the standard-library-only program from this folder:

```text
python asof.py
```

Inputs are editable at the top of [asof.py](asof.py). These are fictional course data. The saved decision date is 2026-03-31.

## Verified known answer

| Gate, in order | Count excluded | Source rows |
|---|---:|---|
| Quarantine missing ticker | 1 | 11 |
| Remove exact duplicate | 1 | 7 |
| Remove publications after March 31 | 3 | 3, 8, 10 |
| Replace older publication | 1 | 2 |
| Remaining panel | 6 | 1, 4, 5, 6, 9, 12 |

The duplicate comparison excludes the source row number; otherwise rows 6 and 7 would never count as duplicates. Publication on the decision date is allowed.

| Fund | As of March 31 | Naive latest data |
|---|---|---|
| AAA | +1.98% (February) | +5.83% (March) |
| BBB | -1.02% (February) | -5.15% (March) |
| CCC | +0.91% (February) | +1.82% (February, revised) |

Executed assertions verified every excluded row, all six panel rows, and all six rounded signals. A second calculation at 2026-04-15 verified exact equality of the as-of and naive signals for all tickers. The saved input remains March 31. This automated verification does not claim a partner exercise was completed.

## Sanity check

Yield = (100 / price - 1) * 100 percent.

| Row | Fund | Month | Price | Yield | Breaks the training assumptions |
|---|---|---|---:|---:|---|
| 1 | AAA | January | 101.0 | -0.99% | Negative yield |
| 4 | AAA | February | 103.0 | -2.91% | Negative yield |
| 5 | BBB | January | 98.0 | +2.04% | Nothing |
| 6 | BBB | February | 97.0 | +3.09% | Nothing |
| 9 | CCC | January | 110.0 | -9.09% | Negative yield; above BBB and AAA |
| 12 | CCC | February | 111.0 | -9.91% | Negative yield; above BBB and AAA |

A fifth, separate sanity rule would quarantine prices above 100 under this exercise's nonnegative-yield assumption, catching rows 1, 4, 9 and 12. A credit-order check would also flag CCC above safer funds at the same maturity and month. Negative yields can exist outside this fictional exercise; provenance alone establishes neither economic validity nor truth.

## Code explanation and learning notes

In `latest_publications`, `key` groups records by ticker and month measured. The dictionary retains one record per key. An unseen key is added; a later publication replaces the stored record. The caller has already excluded publications after the cutoff. The retained source row numbers determine the panel and which older rows were removed. Conflicting prices at the same publication date raise an error rather than silently choosing one.

`signals` sorts each ticker's months and compares the latest with the previous calendar month. It prints unavailable if that month is missing. The naive calculation uses the same missing-ticker and duplicate gates but allows all publication dates before selecting revisions.

Look-ahead bias means letting a historical decision use information that arrived later. The month measured is event time; the publication date is when the number became available. A revision measures the same month but becomes available on a new publication date.

AAA's +5.83% is 109 / 103 - 1: March's price of 109 was published April 10. On March 31 the latest knowable return was February's 103 / 101 - 1 = +1.98%. Row 4's March 25 revision was already knowable; retaining row 2 instead would incorrectly give +2.97%.

Rule 3 prevents future publications entering the backtest; rule 4 makes the admitted February value correct. A naive backtest would claim AAA gained 5.83%, BBB lost 5.15%, and CCC gained 1.82% using values unavailable on the decision date. The future data improves some signals and worsens others; either direction is leakage.

## Student checkout still to complete

- Explain measurement month versus publication date to your partner without a screen.
- Explain rule 4 line by line, answer your partner's question, and swap files for the later-date run.
- Quiz, answer before asking AI for an explanation: Why must `filter_asof` exclude future publications before calling `latest_publications`? Use AAA rows 2 and 4 and CCC rows 10 and 12 in your answer.
- Add your own reflection and submit GitHub links to this Markdown file and `asof.py`. Files are submitted in the `lab 16` folder of `jmcdonald207/lab13`.
