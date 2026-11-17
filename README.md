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

## Run any of the five websites

Download or clone this repository and open a terminal at its root. Use Python 3.10 or newer and an internet connection. For each website you want to open, use a fresh terminal at the repository root and follow its row.

| Website | Change to this folder | Install dependencies | Start the app | Open on your computer |
|---|---|---|---|---|
| [Project 2 Portfolio Screen](final%20version%20one/README.md) | `cd "final version one"` | `python -m pip install -r requirements.txt` | `python -m streamlit run app.py --server.port 8513` | [Port 8513](http://127.0.0.1:8513) |
| [Meridian Portfolio Explorer](lab15/Thursday_checkout.md) | `cd lab15` | `python -m pip install -r requirements.txt` | `python -m streamlit run app.py --server.port 8515` | [Port 8515](http://127.0.0.1:8515) |
| [Point-in-Time Rates](lab%2017/README.md) | `cd "lab 17"` | `python -m pip install -r requirements.txt` | `python -m streamlit run asof_app.py --server.port 8517` | [Port 8517](http://127.0.0.1:8517) |
| [Buffett Business Notebook](lab%2018/README.md) | `cd "lab 18"` | `python -m pip install -r requirements.txt` | `python -m streamlit run app.py --server.port 8518` | [Port 8518](http://127.0.0.1:8518) |
| [Same Facts, Different Investors](lab%2019/README.md) | `cd "lab 19"` | `python -m pip install -r requirements.txt` | `python -m streamlit run app.py --server.port 8519` | [Port 8519](http://127.0.0.1:8519) |

Keep each terminal running while you use its app. These ports are local to the reader's computer. Run the commands before opening the matching link.

Lab 17 needs a personal `FRED_API_KEY` for live rates. Keep it in the environment or Streamlit secrets. For live SEC requests in Labs 18 and 19, enter your own contact information in the **SEC User-Agent** field. [Lab 17 setup](lab%2017/README.md) · [Lab 18 setup](lab%2018/README.md) · [Lab 19 setup](lab%2019/README.md)

### Share browser-only links

For access without a local Python setup, deploy from branch `main` using the app's repository-relative entry point. For example, Project 2 uses `final version one/app.py` and Lab 17 uses `lab 17/asof_app.py`. After deployment, place the verified hosted URL next to the matching app. Configure the FRED key in the hosting platform's secrets. If access needs to be restricted, verify who can open the hosted site before sharing. Streamlit Community Cloud supports one private app at a time. [Deploy an app](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy) · [Share an app](https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app)

## Earlier lab work

- [Lab 13 mandate checker](mandate.py) and [statement classifications](writing.md)
- [Lab 14 checkout](Tuesday_checkout.md) and [Lab 15 portfolio stability](lab15/Thursday_checkout.md)
- [Lab 16 provenance gate](lab%2016/Lab15_checkout.md) and [Lab 17 point-in-time audit](lab%2017/README.md)
- [Lab 18 investor analysis](lab%2018/README.md) and [Lab 19 investor panel](lab%2019/CHECKOUT.md)
