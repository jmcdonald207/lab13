# Lab 20 checkout

## Technical cold run and fix

Codex found the missing root README during the initial GitHub review and added the [root entry point](../README.md). The original classroom baseline ran in roughly 1.22 seconds after the files were acquired. The updated synthetic-data baseline and its stress were rerun with `python -B run.py` and `python -B run.py --equity-return 7`. [Visible output](output/results.md)

Human partner cold run, elapsed time, rerun and code walkthrough are pending. For the walkthrough, trace `evaluate` in [run.py](run.py) and `search_portfolio` in [portfolio.py](portfolio.py).

## Changed-input record and reflection

The AI-assisted demo is documented in validation. The student-authored prediction, its pre-run commit, partner discussion, and reflection are pending. The official Project 2 page and Week 12 list were unavailable.

## Committee decision line

Pilot the screen for research and reject a live allocation until real adjusted-close data and the applicable mandate are verified and the committee accepts the allocation's sensitivity to the equity estimate.
