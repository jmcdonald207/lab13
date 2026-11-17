"""Read the fixed Project 2 sample from Yahoo Finance adjusted daily closes."""
from datetime import date, datetime, timezone
from json import load
import math
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from functools import lru_cache

TICKERS = ("SGOV", "IEF", "BND", "VT")
START = date(2021, 10, 1)
END = date(2026, 11, 1)
MONTHS = tuple(f"{START.year + (START.month - 1 + i) // 12:04d}-"
               f"{(START.month - 1 + i) % 12 + 1:02d}" for i in range(61))


def monthly_prices(ticker):
    def epoch(day):
        return int(datetime(day.year, day.month, day.day, tzinfo=timezone.utc).timestamp())

    query = urlencode(dict(period1=epoch(START), period2=epoch(END), interval="1d"))
    endpoint = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?{query}"
    request = Request(endpoint, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=30) as response:
        result = load(response)["chart"]["result"][0]

    closes = result["indicators"]["adjclose"][0]["adjclose"]
    # US regular-session daily timestamps fall on the same UTC calendar day.
    month_ends = {}
    for timestamp, close in sorted(zip(result["timestamp"], closes, strict=True)):
        month = datetime.fromtimestamp(timestamp, timezone.utc).strftime("%Y-%m")
        month_ends[month] = close
    if any(month not in month_ends or month_ends[month] is None
           or not math.isfinite(month_ends[month]) or month_ends[month] <= 0
           for month in MONTHS):
        raise ValueError(f"{ticker}: missing or invalid final close in the fixed window")
    return tuple(month_ends[month] for month in MONTHS)


@lru_cache(maxsize=1)
def load_prices():
    return tuple(monthly_prices(ticker) for ticker in TICKERS)
