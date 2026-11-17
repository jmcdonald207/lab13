# Lab 13 and later labs

Codex assisted with repository review, implementation, testing, and documentation. The analysis and committee decision are the project author's. **education, not investment advice**.

## Project 2 — Portfolio mandate screen

The current app is in [final version one](final%20version%20one/README.md). From the repository root, run the following with Python 3.10 or newer and an internet connection.

```powershell
cd "final version one"
python -m pip install -r requirements.txt
python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8513
```

Open [localhost:8513](http://127.0.0.1:8513) while Streamlit is running. Switch between full and recent estimation windows or change VT's expected return to see the modeled allocation and verdict.

The saved full window selected **45% VT**. The recent window selected **15% VT**. Both cleared the modeled return and reserve rules. The committee memo proposes a research pilot and defers live allocation until the committee resolves SGOV reserve eligibility and allocation sensitivity.

- [Decision memo](final%20version%20one/docs/decision-memo.md) and [submission manifest](final%20version%20one/MANIFEST.md)
- [Saved baseline results](final%20version%20one/output/results.md) and [sensitivity results](final%20version%20one/output/validation-stresses.md)
- [Validation and AI use](final%20version%20one/docs/validation-and-ai-use.md) and [Lab 20 checkout](final%20version%20one/CHECKOUT.md)

## Earlier lab work

- [Lab 13 mandate checker](mandate.py) and [statement classifications](writing.md)
- [Lab 14 checkout](Tuesday_checkout.md) and [Lab 15 portfolio stability](lab15/Thursday_checkout.md)
- [Lab 16 provenance gate](lab%2016/Lab15_checkout.md) and [Lab 17 point-in-time audit](lab%2017/README.md)
- [Lab 18 investor analysis](lab%2018/README.md) and [Lab 19 investor panel](lab%2019/CHECKOUT.md)
