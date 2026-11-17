"""Replay independent cost, reserve-eligibility, and sample-end stresses."""
from run import evaluate, report


def main():
    cases = (
        ("Baseline: 60 returns through October 2026", {}),
        ("Cost stress: 50 basis points per year, return shown net of cost",
         {"annual_cost": 0.005}),
        ("Reserve stress: SGOV excluded and no other sleeve qualifies",
         {"reserve_eligible": (False, False, False, False)}),
        ("Sample-end stress: exclude the final six returns (end April 2026)",
         {"months_held_back": 6}),
    )
    for title, overrides in cases:
        print(f"\n{title}\n{report(*evaluate(**overrides))}")
    print("\nPause the pilot if a required scenario has no qualifying mix.")
    print("The sample-end stress uses today's adjusted prices and is retrospective.")


if __name__ == "__main__":
    main()
