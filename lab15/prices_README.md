# Download prices outside the app

From your downloaded `lab15` folder, install the dependencies once:

```powershell
python -m pip install -r requirements.txt
```

Download your selected tickers:

```powershell
python prices.py
```

Enter your Yahoo Finance ticker symbols when prompted, separated by spaces.
The downloader saves `prices.csv` and `prices_sources.md` in the current folder.
Rerunning it replaces those output files.

It uses daily adjusted closes and takes the final available close of each
completed month. The unfinished current month is excluded. The default history
contains 61 monthly prices for 60 monthly returns. Missing prices or insufficient
history stop the download instead of filling values. To use a shorter history,
run `python prices.py --years 3`.

Then launch the app:

```powershell
python -m streamlit run app.py
```

Upload `prices.csv` in the sidebar. Select reserve eligibility for your tickers.
The downloader does not choose a portfolio or change the app's assumptions.

The unofficial yfinance library needs internet access; Yahoo can limit requests
or change availability. Data access is intended for personal study and research.
See [yfinance](https://github.com/ranaroussi/yfinance) and its
[download documentation](https://ranaroussi.github.io/yfinance/reference/api/yfinance.download.html).
