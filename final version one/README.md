# Project 2 — Portfolio mandate screen

Codex assisted with repository review, implementation, testing, and documentation. The analysis and committee decision are the project author's. **education, not investment advice**.

## Open the Streamlit app

From the repository root, use Python 3.10 or newer and an internet connection.

```powershell
cd "final version one"
python -m pip install -r requirements.txt
python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8513
```

Open [localhost:8513](http://127.0.0.1:8513) if the browser does not open automatically. Keep the terminal running. Select **All 60 months** or **Last 36 months**, change **VT expected return (%)** if desired, and read the allocation, risk, and modeled verdict. The app was verified with both windows using Streamlit's app testing interface and live Yahoo Finance data. An independent partner cold run is tracked in the checkout.

## What it does

The screen uses monthly adjusted closes for SGOV, IEF, BND, and VT from October 2021 through October 2026. It searches fully invested, long-only portfolios in five-percentage-point increments for the lowest modeled volatility subject to a **6.50% expected annual return hurdle** and **3.00% eligible reserves**, assuming SGOV qualifies. The fixed sample is retrospective. Historical vendor adjustment vintages are unavailable in this workflow.

| Run | VT | Expected annual return | Annual volatility | Modeled verdict |
|---|---:|---:|---:|---|
| Full window | 45% | 6.83% | 6.74% | PASS |
| Recent window | 15% | 6.85% | 1.77% | PASS |
| Full window with 0.50% annual cost | 50% | 6.67% net | 7.48% | PASS |
| SGOV ineligible with no substitute | — | — | — | FAIL |
| Sample ends six months earlier | 40% | 6.65% | 6.24% | PASS |

The committee memo proposes a research pilot and defers live allocation pending an SGOV eligibility decision and a rule for handling allocation sensitivity across windows.

## Reproduce and review

Run these commands from this folder. The tests run offline. The other commands download prices.

```powershell
python run.py
python validate_project.py
python -m unittest -v test_validation
```

- [Decision memo](docs/decision-memo.md) and [submission manifest](MANIFEST.md)
- [Sources](data/sources.md) and [data card](data/data-card.md)
- [Saved baseline and VT estimate stress](output/results.md) and [cost, reserve, and date stresses](output/validation-stresses.md)
- [Validation and AI use](docs/validation-and-ai-use.md), [locked prediction draft](lockedPredictionsNoAI), and [partner checkout](CHECKOUT.md)
- [Studio notes](docs/studio.md) and [video and transcript index](docs/videos.md)

The current app shows the constrained portfolio. The same-data baseline comparison, historical point-in-time signal evidence, completed locked input record, and partner cold run are tracked as open in the submission docs.
