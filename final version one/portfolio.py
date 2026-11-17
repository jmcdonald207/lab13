"""Compare three portfolios. Run: python portfolio.py

Returns and volatilities are annual decimals (0.065 means 6.5%).
Correlation rows and columns follow SLEEVES order.
"""

# EDITABLE INPUTS: course-authored training values, not market estimates.
# Annual returns and volatilities are decimals.
SLEEVES = [
    {"name": "Bills", "expected_return": 0.035, "volatility": 0.005},
    {"name": "10-year note", "expected_return": 0.043, "volatility": 0.07},
    {"name": "Investment-grade bond fund", "expected_return": 0.05, "volatility": 0.06},
    {"name": "Global equity index fund", "expected_return": 0.08, "volatility": 0.16},
]
CORRELATIONS = [
    [1.0, 0.10, 0.05, 0.00],
    [0.10, 1.0, 0.80, -0.10],
    [0.05, 0.80, 1.0, 0.25],
    [0.00, -0.10, 0.25, 1.0],
]
# CPI estimate 2.5% + real-return objective 4.0% = 6.5%.
OBJECTIVE_RETURN = 0.025 + 0.04
# END EDITABLE INPUTS

import math


def finite_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def validate_inputs(sleeves, correlations, objective, require_four=True):
    n = len(sleeves)
    if require_four and n != 4:
        raise ValueError("Exactly four sleeves are required, in the documented order.")
    for sleeve in sleeves:
        if not finite_number(sleeve["expected_return"]):
            raise ValueError(f"Enter a finite expected return for {sleeve['name']}.")
        if not finite_number(sleeve["volatility"]) or sleeve["volatility"] <= 0:
            raise ValueError(f"Enter a positive finite volatility for {sleeve['name']}.")
    if not finite_number(objective):
        raise ValueError("Objective return must be finite.")
    if len(correlations) != n or any(len(row) != n for row in correlations):
        raise ValueError("Correlation table must have one row and column per sleeve.")
    for i in range(n):
        for j in range(n):
            value = correlations[i][j]
            if not finite_number(value) or not -1 <= value <= 1:
                raise ValueError(f"Correlation [{i + 1}, {j + 1}] must be a number from -1 to 1.")
            if value != correlations[j][i]:
                raise ValueError(f"Correlation table is not symmetric at [{i + 1}, {j + 1}].")
        if correlations[i][i] != 1:
            raise ValueError("Every diagonal correlation must equal 1.")
    # A symmetric correlation table must also describe nonnegative variances.
    factor = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            residual = correlations[i][j] - sum(factor[i][k] * factor[j][k] for k in range(j))
            if i == j:
                if residual < -1e-12:
                    raise ValueError("Correlation table is not positive semidefinite.")
                factor[i][j] = math.sqrt(max(0.0, residual))
            elif factor[j][j] > 1e-12:
                factor[i][j] = residual / factor[j][j]
            elif abs(residual) > 1e-12:
                raise ValueError("Correlation table is not positive semidefinite.")


def covariance_matrix(volatilities, correlations):
    return [[correlations[i][j] * vi * vj for j, vj in enumerate(volatilities)]
            for i, vi in enumerate(volatilities)]


def benchmark_weights():
    return [0.0, 0.0, 0.4, 0.6]


def equal_weights(count):
    return [1.0 / count] * count


def inverse_volatility_weights(volatilities):
    inverse = [1.0 / volatility for volatility in volatilities]
    total = sum(inverse)
    return [value / total for value in inverse]


def expected_return(weights, returns):
    return sum(weight * value for weight, value in zip(weights, returns))


def portfolio_volatility(weights, covariance):
    # Include every pair: off-diagonal terms capture diversification.
    variance = sum(wi * wj * covariance[i][j]
                   for i, wi in enumerate(weights) for j, wj in enumerate(weights))
    if variance < -1e-12:
        raise ValueError("Portfolio variance is negative; check the covariance inputs.")
    return math.sqrt(max(0.0, variance))


def reserve_eligible_weight(weights):
    """Requested bills-plus-note measure; not certification of Meridian eligibility."""
    return weights[0] + weights[1]


def meets_objective(portfolio_return, objective):
    return portfolio_return >= objective


def search_portfolio(sleeves, correlations, objective, reserve_minimum, reserve_eligible):
    """Exhaust every long-only 5-percentage-point mix; return best or None.

    Eligibility is a sequence of booleans in sleeve order. Ties retain the
    first mix visited. All rates and weights are decimals.
    """
    validate_inputs(sleeves, correlations, objective, require_four=False)
    n = len(sleeves)
    if not n or len(reserve_eligible) != n:
        raise ValueError("Provide one reserve eligibility flag per asset.")
    if not finite_number(reserve_minimum) or not 0 <= reserve_minimum <= 1:
        raise ValueError("Reserve minimum must be between 0 and 1.")
    returns = [s['expected_return'] for s in sleeves]
    covariance = covariance_matrix([s['volatility'] for s in sleeves], correlations)
    best = None

    def visit(prefix, remaining):
        nonlocal best
        if len(prefix) < n - 1:
            for units in range(remaining + 1):
                visit(prefix + [units], remaining - units)
            return
        weights = [units / 20 for units in prefix + [remaining]]
        result = expected_return(weights, returns)
        reserve = sum(w for w, eligible in zip(weights, reserve_eligible) if eligible)
        if result + 1e-12 < objective or reserve + 1e-12 < reserve_minimum:
            return
        volatility = portfolio_volatility(weights, covariance)
        if best is None or volatility < best['volatility']:
            best = dict(weights=weights, expected_return=result,
                        volatility=volatility, reserve_eligible_weight=reserve)

    visit([], 20)
    return best


def search(sleeves, correlations, objective, reserve_eligible, reserve_minimum):
    """Compatibility entry point for the existing Lab 15 search tests."""
    result = search_portfolio(sleeves, correlations, objective, reserve_minimum, reserve_eligible)
    if result is not None:
        result = dict(result, reserve_weight=result['reserve_eligible_weight'])
    return result


def estimate_from_csv(source, last_36_months=False):
    """Read monthly prices (date, then tickers); return sleeves, correlations.

    Use sample standard deviations and arithmetic mean monthly returns.
    The window is applied to returns, so 36 returns require 37 prices.
    """
    import pandas as pd

    prices = pd.read_csv(source)
    if prices.shape[1] < 2 or len(prices) < 3:
        raise ValueError("CSV needs a date column, at least one ticker, and at least three price rows.")
    dates = pd.to_datetime(prices.iloc[:, 0], errors='raise')
    months = dates.dt.to_period('M')
    if dates.isna().any() or months.duplicated().any() or not months.is_monotonic_increasing:
        raise ValueError("Dates must be oldest first, with one row per month.")
    if any(b.ordinal - a.ordinal != 1 for a, b in zip(months, months[1:])):
        raise ValueError("Prices must cover consecutive months without gaps.")
    values = prices.iloc[:, 1:].apply(pd.to_numeric, errors='raise')
    if values.isna().any().any() or not all(math.isfinite(float(v)) and v > 0 for v in values.to_numpy().flat):
        raise ValueError("All prices must be positive finite numbers without missing values.")
    returns = values.pct_change(fill_method=None).iloc[1:]
    if last_36_months:
        returns = returns.tail(36)
    means = returns.mean() * 12
    volatilities = returns.std(ddof=1) * math.sqrt(12)
    sleeves = [dict(name=str(ticker), expected_return=float(means[ticker]),
                    volatility=float(volatilities[ticker])) for ticker in values.columns]
    correlations = returns.corr().values.tolist()
    validate_inputs(sleeves, correlations, 0.0, require_four=False)
    return sleeves, correlations


def main():
    validate_inputs(SLEEVES, CORRELATIONS, OBJECTIVE_RETURN)
    returns = [sleeve["expected_return"] for sleeve in SLEEVES]
    volatilities = [sleeve["volatility"] for sleeve in SLEEVES]
    covariance = covariance_matrix(volatilities, CORRELATIONS)
    portfolios = {
        "Benchmark": benchmark_weights(),
        "Equal weight": equal_weights(len(SLEEVES)),
        "Inverse volatility": inverse_volatility_weights(volatilities),
    }
    print(f"Expected-return objective: {OBJECTIVE_RETURN:.2%}")
    print("Inputs are course-authored training values; volatility is annual standard deviation.")
    for name, weights in portfolios.items():
        result = expected_return(weights, returns)
        print(f"\n{name}")
        for sleeve, weight in zip(SLEEVES, weights):
            print(f"  {sleeve['name']}: {weight:.1%}")
        print(f"  Expected return: {result:.2%}")
        print(f"  Volatility: {portfolio_volatility(weights, covariance):.2%}")
        print(f"  Reserve-eligible weight (bills + 10-year note): {reserve_eligible_weight(weights):.1%}")
        print(f"  Expected return meets objective: {'Yes' if meets_objective(result, OBJECTIVE_RETURN) else 'No'}")


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        raise SystemExit(f"Input error: {error}")
