# Lab 20 — Project 2 readiness

AI assisted with repository review, implementation and documentation. **education, not investment advice**.

From this folder, run with Python 3.10 or newer and internet access. The CLI uses the standard library.

```text
python run.py
```

The tool downloads real adjusted closes for SGOV, IEF, BND and VT for a fixed October 2021–October 2026 sample, then prints the full and recent window allocations and modeled mandate verdicts. If Yahoo is unavailable or observations are missing, the run stops with an error.

- [Submission manifest](MANIFEST.md)
- [Studio must-fix list](docs/studio.md)
- [Point-in-time data card](data/data-card.md)
- [Input source and definitions](data/sources.md)
- [Visible results](output/results.md)
- [Decision memo](docs/decision-memo.md)
- [Validation and AI use](VALIDATION.md)
- [Lab checkout](CHECKOUT.md)
- [Locked Changed-Input Record](docs/locked-changed-input.md)
- [Videos and transcripts](docs/videos.md)

For the interactive view, install with `python -m pip install -r requirements.txt` and launch with `python -m streamlit run app.py`. Select the window, change **VT expected return (%)**, and read the verdict. The CLI stress is `python run.py --equity-return 9.55`.
