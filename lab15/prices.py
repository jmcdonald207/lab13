"""Download monthly adjusted prices outside Streamlit. Run: python prices.py

Yahoo Finance data via the unofficial yfinance library, for personal study.
No portfolio tickers are selected for you. Only completed months are saved.
"""
import argparse
from datetime import date
from pathlib import Path
import math


def download_prices(tickers, years=5, output="prices.csv"):
    """Save date-first prices, oldest first, plus a source record.

    Fetch daily adjusted closes and take each month's final available close.
    Include one extra monthly price so five years supplies 60 monthly returns.
    Fail on missing history rather than filling prices or changing the universe.
    """
    import pandas as pd
    import yfinance as yf
    from portfolio import estimate_from_csv

    tickers = list(dict.fromkeys(t.strip().upper() for t in tickers if t.strip()))
    if not 1 <= len(tickers) <= 6:
        raise ValueError("Enter one to six distinct Yahoo Finance tickers.")
    if not isinstance(years, int) or years < 1:
        raise ValueError("Years must be a positive whole number.")
    end = pd.Timestamp(date.today()).replace(day=1)
    start = end - pd.DateOffset(years=years, months=1)
    raw = yf.download(tickers, start=start.date().isoformat(),
                      end=end.date().isoformat(), interval="1d", auto_adjust=True,
                      group_by="column", multi_level_index=True,
                      progress=False, threads=False, timeout=30)
    if raw is None or raw.empty:
        raise ValueError("Yahoo returned no prices. Check the tickers and connection, then try again.")
    closes = raw["Close"]
    if isinstance(closes, pd.Series):
        closes = closes.to_frame(tickers[0])
    closes = closes.reindex(columns=tickers).sort_index()
    closes.index = pd.to_datetime(closes.index).tz_localize(None)
    monthly = closes.resample("ME").last()
    expected_months = pd.period_range(start=start, end=end - pd.Timedelta(days=1), freq="M")
    monthly.index = monthly.index.to_period("M")
    monthly = monthly.reindex(expected_months)
    bad = [ticker for ticker in tickers if not all(
        pd.notna(v) and math.isfinite(float(v)) and v > 0 for v in monthly[ticker])]
    if bad:
        raise ValueError("Missing or invalid monthly prices for: " + ", ".join(bad) +
                         ". Choose tickers with the full history or request fewer years.")
    monthly.index = monthly.index.to_timestamp(how="start")
    monthly.index.name = "date"
    csv_text = monthly.to_csv(date_format="%Y-%m-%d")
    # Reuse the app's estimator to verify the generated CSV before saving it.
    from io import StringIO
    estimate_from_csv(StringIO(csv_text))
    destination = Path(output).resolve()
    destination.write_text(csv_text, encoding="utf-8")
    record = destination.with_name(destination.stem + "_sources.md")
    record.write_text(
        "# Price download record\n\n"
        f"Downloaded: {date.today().isoformat()}\n\n"
        "Source: Yahoo Finance through yfinance. Daily dividend/split-adjusted "
        "closes, taking the final available close of each completed month.\n\n"
        f"Months: {monthly.index[0]:%Y-%m} to {monthly.index[-1]:%Y-%m}; "
        f"{len(monthly)} prices and {len(monthly) - 1} monthly returns.\n\n"
        + "\n".join(f"- {ticker}: https://finance.yahoo.com/quote/{ticker}/history/" for ticker in tickers)
        + "\n", encoding="utf-8")
    return destination, record, len(monthly)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tickers", nargs="*", help="Yahoo ticker symbols, separated by spaces")
    parser.add_argument("--years", type=int, default=5, help="Years of monthly returns (default: 5)")
    parser.add_argument("--output", default="prices.csv", help="Output CSV path")
    args = parser.parse_args()
    tickers = args.tickers or input("Enter your Yahoo Finance tickers, separated by spaces: ").replace(",", " ").split()
    try:
        destination, record, count = download_prices(tickers, args.years, args.output)
    except ImportError:
        parser.exit(1, "Install dependencies first: python -m pip install -r requirements.txt\n")
    except Exception as error:
        parser.exit(1, f"Download failed: {error}\n")
    print(f"Saved {destination} ({count} monthly prices, {count - 1} returns).")
    print(f"Source record: {record}")
    print("Upload the CSV in the Streamlit app's sidebar.")


if __name__ == "__main__":
    main()
