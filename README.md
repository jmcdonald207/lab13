# Lab 13 and later labs

Codex assisted with repository review, implementation, testing, and documentation. The analysis and committee decision are the project author's. **education, not investment advice**.

## One website — five portfolio and finance tools

All five applications now run inside **one Streamlit website** with a sidebar menu. Download or clone the repository, open a terminal at the repository root, and use Python 3.10 or newer with an internet connection.

```powershell
python -m pip install -r requirements.txt
python -m streamlit run dashboard.py --server.port 8513
```

Open **[the unified dashboard at localhost:8513](http://127.0.0.1:8513)**. In the sidebar, choose which tool to view:

| Page in the one website | What it does | Supporting documentation |
|---|---|---|
| **Project 2 Portfolio Screen** | Portfolio mandate, full and recent windows, VT estimate control | [Project 2 README](final%20version%20one/README.md) |
| **Meridian Portfolio Explorer** | Portfolio optimization and scenario inputs | [Lab 15 checkout](lab15/Thursday_checkout.md) |
| **Point-in-Time Rates** | FRED/ALFRED historical-vintage comparisons | [Lab 17 README](lab%2017/README.md) |
| **Buffett Business Notebook** | SEC financial facts and business-quality screening | [Lab 18 README](lab%2018/README.md) |
| **Same Facts, Different Investors** | Compare investor-style screens using SEC filings | [Lab 19 README](lab%2019/README.md) |

Only **one terminal and one local port** are needed. The underlying files and existing independent launch commands remain available. The site is local to your computer until deployed; localhost is **not a public website URL**.

### Project 2 decision evidence

The saved full-window result selected **45% VT** and the recent window selected **15% VT**. Both cleared the modeled return and reserve rules. The committee memo proposes a research pilot, deferring live allocation until SGOV reserve eligibility and allocation sensitivity are resolved.

- [Decision memo](final%20version%20one/docs/decision-memo.md) and [submission manifest](final%20version%20one/MANIFEST.md)
- [Saved results](final%20version%20one/output/results.md) and [sensitivity results](final%20version%20one/output/validation-stresses.md)
- [Validation and AI use](final%20version%20one/docs/validation-and-ai-use.md) and [Lab 20 checkout](final%20version%20one/CHECKOUT.md)

### External data and deployment

Point-in-Time Rates requires your own `FRED_API_KEY` in the environment or Streamlit secrets. For live SEC requests, enter your contact information in the SEC User-Agent field in Labs 18 and 19. Project 2 uses Yahoo Finance prices and requires network access. Individual pages can still display saved results or errors when providers are unavailable.

For a **shareable public link** without requiring visitors to install Python, deploy the repository on Streamlit Community Cloud using `dashboard.py` as the entry point on branch `main`, then configure secrets as needed. A hosted URL does not exist until you deploy it and verify it works. [Deployment guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)

## Earlier lab work

- [Lab 13 mandate checker](mandate.py) and [statement classifications](writing.md)
- [Lab 14 checkout](Tuesday_checkout.md) and [Lab 15 portfolio stability](lab15/Thursday_checkout.md)
- [Lab 16 provenance gate](lab%2016/Lab15_checkout.md) and [Lab 17 point-in-time audit](lab%2017/README.md)
- [Lab 18 investor analysis](lab%2018/README.md) and [Lab 19 investor panel](lab%2019/CHECKOUT.md)
