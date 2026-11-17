"""Compare allocations using the real adjusted-close prices."""
import argparse
from math import sqrt
from statistics import correlation, mean, stdev

if __package__:
    from .portfolio import search_portfolio
    from .prices import TICKERS, load_prices
else:
    from portfolio import search_portfolio
    from prices import TICKERS, load_prices

OBJECTIVE = 0.065
RESERVE_MINIMUM = 0.03
RESERVE_ELIGIBLE = (True, False, False, False)


def evaluate(months=None, equity_return=None):
    prices = load_prices()
    returns = [[end / start - 1 for start, end in zip(series, series[1:])]
               for series in prices]
    if months is not None:
        returns = [series[-months:] for series in returns]
    sleeves = [
        dict(name=ticker, expected_return=12 * mean(series),
             volatility=sqrt(12) * stdev(series))
        for ticker, series in zip(TICKERS, returns)
    ]
    if equity_return is not None:
        sleeves[-1]["expected_return"] = equity_return / 100
    correlations = [[1.0 if i == j else correlation(returns[min(i, j)], returns[max(i, j)])
                     for j in range(len(returns))] for i in range(len(returns))]
    return sleeves, search_portfolio(sleeves, correlations, OBJECTIVE,
                                     RESERVE_MINIMUM, RESERVE_ELIGIBLE)


def report(sleeves, result):
    lines = [f"VT expected return input: {sleeves[-1]['expected_return']:.2%}"]
    if result is None:
        return "\n".join(lines + ["Modeled mandate verdict: FAIL (no qualifying mix)"])
    lines.extend(f"{sleeve['name']}: {weight:.2%}"
                 for sleeve, weight in zip(sleeves, result["weights"]))
    lines.extend([
        f"Expected return (minimum 6.50%): {result['expected_return']:.2%}",
        f"Annual volatility: {result['volatility']:.2%}",
        f"Eligible reserve weight (minimum 3.00%): {result['reserve_eligible_weight']:.2%}",
        "Modeled mandate verdict: PASS",
    ])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--equity-return", type=float, help="Override VT annual return in percent")
    args = parser.parse_args()
    print("Yahoo Finance adjusted closes | Oct 2021 to Oct 2026")
    for title, months in (("All 60 monthly returns", None), ("Last 36 monthly returns", 36)):
        print(f"\n{title}\n{report(*evaluate(months, args.equity_return))}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, IndexError, TypeError) as error:
        raise SystemExit(f"Could not complete the portfolio run: {error}") from error
