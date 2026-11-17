# Validation and AI use

Codex selected the illustrative tickers, generated the synthetic series, connected it to the Lab 15 optimizer, and executed both CLI commands on November 17, 2026. The full 60-return and last 36-return baseline and the single-input stress all passed the 6.50% estimated return and 3.00% reserve checks. The optimizer uses a fully invested long-only five-percentage-point grid. The baseline holds 5% SGOV, the only modeled eligible sleeve.

The stress held the full-window volatility and correlations fixed and lowered VT from 8.00% to 7.00%. VT weight rose 25 percentage points and volatility rose 3.29 percentage points. [Run output](output/results.md)

The interactive app uses the same computation. Its browser runtime has not been verified. The student-authored AI-closed prediction is pending. [Locked record](docs/locked-changed-input.md)
