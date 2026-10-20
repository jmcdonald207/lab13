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


def validate_inputs(sleeves, correlations, objective):
    n = len(sleeves)
    if n != 4:
        raise ValueError("Exactly four sleeves are required, in the documented order.")
    for sleeve in sleeves:
        if not finite_number(sleeve["expected_return"]):
            raise ValueError(f"Enter a finite expected return for {sleeve['name']}.")
        if not finite_number(sleeve["volatility"]) or sleeve["volatility"] <= 0:
            raise ValueError(f"Enter a positive finite volatility for {sleeve['name']}.")
    if not finite_number(objective):
        raise ValueError("Objective return must be finite.")
    if len(correlations) != n or any(len(row) != n for row in correlations):
        raise ValueError("Correlation table must have four rows and four columns.")
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
