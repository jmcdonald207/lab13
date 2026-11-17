# Lab 20 — Project 2 readiness

This package uses the Meridian classroom assumptions from [Lab 15](../lab15/Thursday_checkout.md). Confirm the actual Project 2 inputs and scope before treating this as the final decision.

Download or clone this repository, open `final version one` in a terminal, and run with Python 3:

```text
python run.py
```

The result prints to the terminal. The baseline needs no packages or network. The tool's `--equity-return` control takes annual percent units (for example, `8` means 8%). Read the modeled mandate verdict at the bottom.

- [Visible output](output/results.md)
- [Decision memo](docs/decision-memo.md)
- [Validation and AI use](VALIDATION.md)
- [Lab 20 checkout and partner note](CHECKOUT.md)
- [Locked Changed-Input Record](docs/locked-changed-input.md)
- [Videos and transcripts](docs/videos.md)

For browser controls, install the [Lab 15 dependencies](requirements.txt) with `python -m pip install -r requirements.txt` and launch `python -m streamlit run app.py`. Change Global equity index fund expected return (%) and compare the current and loaded answers. Use the CLI for the explicitly labeled mandate verdict.
