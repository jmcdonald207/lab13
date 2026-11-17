# Lab 20 — Project 2 readiness

From this folder, run the baseline with Python 3.10 or newer. It needs no packages or network.

```text
python run.py
```

The command prints allocation, annual return and volatility, eligible reserve weight, and mandate verdict for both the full and recent windows. The modeled mandate requires at least 6.50% expected annual return and 3.00% in SGOV, with a fully invested long-only allocation. These are classroom assumptions.

- [Fund universe and synthetic data provenance](data/sources.md)
- [Visible output](output/results.md)
- [Decision memo](docs/decision-memo.md)
- [Validation and AI use](VALIDATION.md)
- [Lab checkout](CHECKOUT.md)
- [Locked Changed-Input Record](docs/locked-changed-input.md)
- [Videos and transcripts](docs/videos.md)

For the interactive view, run `python -m pip install -r requirements.txt` and `python -m streamlit run app.py`. Change **VT expected return (%)** and read the verdict. The CLI equivalent is `python run.py --equity-return 7`.
