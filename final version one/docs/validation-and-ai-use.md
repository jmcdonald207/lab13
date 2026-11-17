# Validation and AI use

## Data and model checks

The saved November 17, 2026 run uses monthly Yahoo Finance adjusted closes for SGOV, IEF, BND, and VT from October 2021 through October 2026. The downloader requires 61 valid month-end prices per fund to compute 60 monthly returns. The model searches fully invested, long-only portfolios on a five-percentage-point weight grid. It checks a 6.50% expected annual return hurdle and a 3.00% eligible reserve minimum under the SGOV eligibility assumption. The historical vendor adjustment vintage is unavailable, so the data supports retrospective research. [Sources](../data/sources.md) · [Point-in-time data card](../data/data-card.md) · [Lab known-answer tests](../../test_portfolio.py)

| Saved run | VT weight | Expected annual return | Annual volatility | Eligible reserves | Modeled verdict |
|---|---:|---:|---:|---:|---:|
| Full 60 returns | 45% | 6.83% | 6.74% | 55% | PASS |
| Recent 36 returns | 15% | 6.85% | 1.77% | 85% | PASS |
| Full 60 returns with VT estimate at 9.55% | 50% | 6.67% | 7.48% | 50% | PASS |

The shorter window moves VT weight by 30 percentage points. The full-window estimate stress increases VT weight by five percentage points and annual volatility by 0.74 percentage points. These results support a research pilot, with live allocation deferred until the committee confirms SGOV eligibility and agrees on how to handle window sensitivity. Pause the pilot if either window fails the modeled rules or the data checks fail. [Saved CLI results](../output/results.md) · [Decision memo](decision-memo.md)

## AI use and verification

Codex assisted with implementation and documentation, downloaded the four price series, and ran the CLI outputs recorded on November 17, 2026. Codex used the saved output to check the baseline rule verdicts. The 9.55% override was an AI-assisted stress. Independent browser and partner cold-run evidence and verification of a point-in-time signal are pending. Codex added and ran the separate sensitivity replay below. [Original validation notes](../VALIDATION.md) · [Partner checkout](../CHECKOUT.md)

## Cost, reserve eligibility, and sample-end sensitivity

Run `python validate_project.py` from the Project 2 folder. Each scenario changes one input relative to the same baseline. [Runner](../validate_project.py) · [Executed output](../output/validation-stresses.md)

| Scenario | VT weight | Expected annual return | Annual volatility | Eligible reserves | Modeled verdict |
|---|---:|---:|---:|---:|---:|
| Add 50 basis points of annual portfolio drag | 50% | 6.67% net | 7.48% | 50% | PASS |
| Exclude SGOV from reserves with no eligible substitute | — | — | — | — | FAIL, no qualifying mix |
| End the sample in April 2026, six months earlier | 40% | 6.65% | 6.24% | 60% | PASS |

The illustrative cost stress uses a uniform drag across all sleeves. Excluding SGOV leaves every candidate below the reserve minimum, so pause the pilot if the committee rules SGOV ineligible and no substitute is approved. The earlier sample end tests sensitivity to the observation cutoff using current adjusted closes. A verified historical point-in-time signal still requires vintage evidence.

## Locked Changed-Input Record

| Field | Status |
|---|---|
| Input | VT expected annual return, full estimation window, other settings fixed |
| Baseline and proposed override | Default full-window estimate displayed as 10.55% → 6.50% annual return |
| Saved baseline | 45% VT, 55% SGOV, 6.74% annual volatility, 6.83% expected annual return (PASS), 55% eligible reserves (PASS under the SGOV assumption) |
| Human-authored pre-run prediction | Draft exists. Reconcile the directions and state the predicted verdict for each rule and the expected decision effect with AI closed. |
| Pre-run commit | Pending a completed prediction committed and pushed before the chosen run |
| Changed output and comparison | Pending the run after the prediction is locked. Record actual weights, return, volatility, each verdict, what matched, and the effect on the pilot. |

[Prediction draft](../lockedPredictionsNoAI) · [Saved baseline](../output/results.md)
