# Lab 17 — Point-in-Time Audit

Was each number in your series knowable on the day you would have traded on it — and may Project 2 use it?

## Run

From the repository root, in a terminal with internet access:

```powershell
python -m pip install -r "lab 17/requirements.txt"
$env:FRED_API_KEY = "your_personal_fred_api_key"
python -m streamlit run "lab 17/asof_app.py" --browser.gatherUsageStats false
```

Run the live known-answer audit separately:

```powershell
python "lab 17/audit.py"
```

It writes `live_audit.json` beside the script and exits unsuccessfully if any required check fails. That generated file is actual download evidence; the expected answers in the audit are only comparisons, never substituted into the app. Run offline tests with `python -m unittest discover -s "lab 17" -p "test_asof.py" -v`.

## Verification status

Built with AI help on 2026-10-29. Local Python has Streamlit, pandas, NumPy and requests installed. Direct CSV download was attempted with `requests.get` against the PAYEMS ALFRED URL, but this environment returned `PermissionError: [WinError 10013] An attempt was made to access a socket in a way forbidden by its access permissions`. Therefore the four live known answers and PAYEMS probe are **not yet verified here**. No live CSV download date or passing result is invented. Offline tests use clearly synthetic data.

Set the app's date to 2026-10-05 and verify BAA: 2026-09-01 / 6.47; FEDFUNDS: 2026-09-01 / 3.75; DGS10: 2026-10-02 / 5.28; MORTGAGE30US: 2026-10-01 / 7.28. Monthly CSV dates label the month with its first day. Add PAYEMS and set 2025-01-15: the last observation should be December 2024 / 159,536; inspect that month's lower current value and the revision count. If results differ, preserve the actual downloads and investigate; do not edit the displayed values to match.

## Provisional data card — DGS10

The prework choice was not supplied or found in the repository. DGS10 is a provisional example; replace this card if the student's actual choice differs. DGS10 is already among the four default selections.

| Field | Evidence |
|---|---|
| Source and link | Board of Governors of the Federal Reserve System, H.15; distributed by [FRED](https://fred.stlouisfed.org/series/DGS10) and historical vintages by [ALFRED](https://alfred.stlouisfed.org/series?seid=DGS10) |
| Measure | Daily nominal Treasury yield at a constant ten-year maturity, interpolated from the yield curve; not a bond price or realized return |
| Units | Percent per year, not seasonally adjusted; 5.05 means 5.05%, not 505% |
| Publication lag | Short business-day lag, not zero by assumption. On 2026-10-29 the FRED page's latest measurement is 2026-10-28. [H.15](https://www.federalreserve.gov/releases/h15/) posts weekdays at 4:15 p.m., except holidays/closures. This is the source release schedule, not proof of FRED intraday arrival. |
| Revisions | A market yield is expected to have few revisions, but corrections remain possible. FRED explicitly says all data are subject to revision. The vintage-versus-current revised count remains to be measured by the live audit. |
| Retrieval date | Source webpages read by AI on 2026-10-29. CSV download attempted that date and blocked; successful CSV download date pending. The app records actual UTC download timestamps. |

Three webpage observations read by AI from FRED on 2026-10-29 and cross-checked against H.15: 2026-10-26 = 5.00%; 2026-10-27 = 4.99%; 2026-10-28 = 5.05%. These are source-page checks, not app-versus-source verification or the student's required hand check. Student: read the same three dates on FRED, compare with the downloaded app data, and record the result and date here: **pending**.

For the series exercise, set the cutoff to 2026-09-30, then today. Record the last known measurement, later observation count, and revision count at both cutoffs: **pending live access**. Later observations are newer measured periods; they do not count every newly published or restored historical value. Revisions compare nonmissing shared dates across the full history. Missing days are excluded, never forward-filled; no earlier history is inferred if ALFRED returns none.

## Project 2 call

**Quarantine DGS10 pending the live audit and confirmation of the actual prework series.** Admit only with an archived ALFRED vintage for each historical decision date and a rule that availability precedes the trade. For intraday decisions, a date-only snapshot is insufficient: establish publication/ingestion time or conservatively use a prior completed day's vintage. Admission requires the four known answers and PAYEMS probe to pass, the three manual comparisons, and the lag/revision evidence to be recorded. Reject any pipeline that substitutes today's history for historical vintages or forward-fills before first publication.

This call concerns data eligibility, not a recommendation to trade. A possible hypothesis is that Treasury yields affect equity discount rates and corporate financing conditions; the student must explain the link to their own universe.

## Fresh eyes — student and partner must complete

- Partner's actual least-trusted field (publication date, revisions, or units): **pending**.
- Partner's question about the download function: **pending**.
- Student's answer from the code: **pending**.
- Two-sentence response to the actual attack, with app or source evidence: **pending**.

Example response if publication date is challenged (preparation only, not a claimed partner exchange): “FRED on October 29 labels the latest DGS10 measurement October 28, and H.15 specifies a 4:15 p.m. weekday release. I therefore cannot treat the measurement date as the time I could trade on the published FRED value; I require a prior-day vintage or verified intraday availability.”

## Explain the code and learning notes

`fetch_snapshot` requests FRED observations with `realtime_start` and `realtime_end` both set to the requested information date. It checks that the response confirms this period, follows pagination, rejects measurements beyond the cutoff, and records the UTC retrieval time and a credential-free request URL. Current data uses the same endpoint with today’s information date. Missing values are excluded; duplicate or missing dates and infinite values are rejected. Metadata (units, frequency and seasonal adjustment) is current, not historical. Charts overlay both histories; exported differences include revisions, later observations, older additions and historical dates absent today. With an empty historical baseline, current-only dates are counted separately rather than assumed to be later publications.

A data card states meaning and availability: source, ID, units, measurement period, publication lag, revisions, vintage, and download time. The vintage and decision-date availability rule prevent leakage before a signal is computed; the download date alone cannot. “Cleaned the data” describes an operation but does not establish what a number meant or when it became knowable.

Reflection preparation: DGS10 has a short business-day lag in the source-page example, but the historical app comparison must still establish the cutoff's latest available measurement. Using today's values could give a backtest access to unpublished observations and later corrections. That overstates the information available at the time; whether performance rises or falls is empirical and cannot be claimed without a backtest.

Student's own reflection, no-screen code explanation, partner swap, and Brightspace quiz: **pending student completion**.

## Files for checkout

- [App](asof_app.py)
- [Live known-answer audit](audit.py)
- [Offline leakage and interface tests](test_asof.py)
- [Dependencies](requirements.txt)
- This Markdown file contains the provisional card, call, and remaining student work.

## Reopening, sharing, and credentials

On Windows, double-click `launch_asof.cmd` in this folder, or run the Streamlit command above. Leave the terminal running, then bookmark http://localhost:8501. Connection refused means the server has stopped or is listening on a different port. The localhost address works only on the machine running the app. Other computers need the terminal’s Network URL on an allowed local network, or a hosted deployment.

Alternatively store your key in `.streamlit/secrets.toml` under the directory from which you launch Streamlit:

```toml
FRED_API_KEY = "your_personal_fred_api_key"
```

Never commit that secrets file. The supplied `.gitignore` excludes it. Source request URLs intentionally omit API keys. For a hosted deployment, set the key in the hosting service’s secrets settings; uploading files to GitHub alone does not host a Streamlit app. FRED supplies data but does not host this application.

If all series fail, read the displayed network or HTTP error. The assistant’s restricted execution session could not reach FRED; launch from your own terminal with internet access. Live data and known-answer checks remain unverified until `audit.py` succeeds. Offline tests are synthetic and do not establish historical accuracy.

