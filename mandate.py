"""Check reserve mandates. Run with: python mandate.py"""

# EDITABLE INPUTS
# Add one row per holding. Use the same issuer for every security of a company.
# issuer_type must be "company", "cash", "us_treasury", or "diversified_fund".
# Example row format (replace with your actual holdings):
# {"holding": "Example bond", "issuer": "Example Co", "business_days_to_redeem": 2,
#  "reserve_eligible": True, "issuer_type": "company"}
HOLDINGS = []

# Percent weights, keyed by holding name. Include every holding, even at zero.
CANDIDATES = {
    "A": {},
    "B": {},
    "C": {},
}
RESERVE_SIZE = 100  # USD millions
QUARTERLY_DISTRIBUTION = 0.75  # USD millions
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW = 5  # business days
MINIMUM_LIQUID_SHARE = 90  # percent
ISSUER_LIMIT = 8  # percent
# END EDITABLE INPUTS

from decimal import Decimal, InvalidOperation


def number(value):
    result = Decimal(str(value))
    if not result.is_finite():
        raise ValueError("Numeric inputs must be finite.")
    return result


def main():
    reserve_size = number(RESERVE_SIZE)
    if reserve_size <= 0:
        raise ValueError("RESERVE_SIZE must be positive.")
    reserve_minimum = (
        number(QUARTERS_TO_COVER) * number(QUARTERLY_DISTRIBUTION)
        / reserve_size * 100
    )
    print(f"Reserve minimum: {reserve_minimum:.1f}%")

    if not HOLDINGS or any(not weights for weights in CANDIDATES.values()):
        raise ValueError(
            "Missing holdings table and/or candidate weights. "
            "Fill in HOLDINGS and CANDIDATES at the top of this file."
        )
    holdings = {}
    issuer_types = {}
    allowed_types = {"company", "cash", "us_treasury", "diversified_fund"}
    for row in HOLDINGS:
        name = row["holding"]
        issuer = row["issuer"].strip().casefold()
        kind = row["issuer_type"]
        if not name or name in holdings or not issuer:
            raise ValueError("Holding names must be unique and issuers nonempty.")
        if kind not in allowed_types:
            raise ValueError(f"Invalid issuer_type for {name}.")
        if issuer in issuer_types and issuer_types[issuer] != kind:
            raise ValueError(f"Conflicting issuer types for {row['issuer']}.")
        issuer_types[issuer] = kind
        days = number(row["business_days_to_redeem"])
        if days < 0 or type(row["reserve_eligible"]) is not bool:
            raise ValueError(f"Invalid redemption days or eligibility for {name}.")
        holdings[name] = (issuer, kind, days, row["reserve_eligible"])

    for candidate, raw_weights in CANDIDATES.items():
        if set(raw_weights) != set(holdings):
            raise ValueError(f"Candidate {candidate} must specify every holding exactly.")
        weights = {name: number(value) for name, value in raw_weights.items()}
        eligible = Decimal(0)
        liquid = Decimal(0)
        companies = {}
        for name, weight in weights.items():
            issuer, kind, days, is_eligible = holdings[name]
            if is_eligible:
                eligible += weight
            if days <= number(LIQUIDITY_WINDOW):
                liquid += weight
            if kind == "company":
                companies[issuer] = companies.get(issuer, Decimal(0)) + weight
        total = sum(weights.values(), Decimal(0))
        lowest = min(weights.values())
        largest = max(companies.values(), default=Decimal(0))
        checks = [
            ("Weights sum to 100", total, total == 100),
            ("Lowest weight (long-only)", lowest, lowest >= 0),
            ("Reserve-eligible weight", eligible, eligible >= reserve_minimum),
            ("Weight redeemable within window", liquid,
             liquid >= number(MINIMUM_LIQUID_SHARE)),
            ("Largest single company", largest, largest <= number(ISSUER_LIMIT)),
        ]
        print(f"\nCandidate {candidate}")
        for label, value, passed in checks:
            print(f"  {label}: {value:.1f}% — {'pass' if passed else 'FAIL'}")
        print("  Calendar-year loss rule: requires CIO clarification")
        failures = sum(not passed for _, _, passed in checks)
        print("  passes every checkable rule" if failures == 0
              else f"  fails {failures} rule(s)")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, TypeError, InvalidOperation) as error:
        raise SystemExit(f"Input error: {error}")
