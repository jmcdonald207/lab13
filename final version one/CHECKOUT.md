# Lab 20 checkout

## Cold run

Reviewer was Codex acting as a technical partner. The first repository-only failure was the missing root README, confirmed by the GitHub contents API. Attempting a clone in this shell also failed because Git was unavailable. Codex retrieved the source through GitHub and ran the packaged files in a new temporary folder.

- Command executed: `python -B run.py` (the flag disables bytecode files).
- Elapsed time: about 1.22 seconds for the baseline process, excluding acquisition and setup.
- Result: terminal output and [saved decision numbers](output/results.md).
- Fix: a [root README](../README.md) now directs a reader to this folder's one-command baseline. Technical rerun produced the expected output. Human partner cold run and rerun are pending.

## Changed input

The previously documented stress is available for inspection. The student's new [locked prediction and rerun](docs/locked-changed-input.md) are pending.

## Explain the code and reflect

Use `search_portfolio` in [portfolio.py](portfolio.py), then trace how it calls `expected_return` and `portfolio_volatility`. Student walkthrough, partner question and answer, and swap are pending.

The technical cold check found that the repository lacked a root entry point. The student's reflection on what the partner found and what to leave alone before the deadline is pending. The Week 12 must-fix list and the full Project 2 page were unavailable.

## Committee decision line

Pilot the Meridian portfolio screen for research only, and reject a live allocation if the full mandate review remains unresolved or the committee finds the stressed 80% equity weight and 12.94% annual volatility unacceptable.
