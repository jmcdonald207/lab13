"""Reproduce the classroom reserve portfolio screen."""
import argparse
from copy import deepcopy

from portfolio import CORRELATIONS, OBJECTIVE_RETURN, SLEEVES, search_portfolio

RESERVE_MINIMUM = 0.03
RESERVE_ELIGIBLE = (True, True, False, False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--equity-return", type=float, default=8.0,
                        help="Annual expected equity return in percent (default: 8)")
    args = parser.parse_args()
    sleeves = deepcopy(SLEEVES)
    sleeves[-1]["expected_return"] = args.equity_return / 100
    result = search_portfolio(sleeves, CORRELATIONS, OBJECTIVE_RETURN,
                              RESERVE_MINIMUM, RESERVE_ELIGIBLE)

    print(f"Equity expected return input: {args.equity_return:.2f}%")
    print(f"Expected-return objective: {OBJECTIVE_RETURN:.2%}")
    print(f"Reserve-eligible minimum: {RESERVE_MINIMUM:.2%}")
    if result is None:
        print("Modeled mandate verdict: FAIL (no qualifying grid mix)")
    else:
        for sleeve, weight in zip(sleeves, result["weights"]):
            print(f"{sleeve['name']}: {weight:.2%}")
        print(f"Expected return: {result['expected_return']:.2%}")
        print(f"Annual volatility: {result['volatility']:.2%}")
        print(f"Reserve-eligible weight: {result['reserve_eligible_weight']:.2%}")
        print("Modeled mandate verdict: PASS (expected return and reserve only)")
    print("Full mandate review: unresolved")


if __name__ == "__main__":
    main()
