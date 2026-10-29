"""Run live assignment checks. Expected answers are assertions, never app data."""
import json
from datetime import date, timedelta
from pathlib import Path
from asof_app import fetch_snapshot, get_api_key, compare


def fetch_today(series_id, day):
    return fetch_snapshot(series_id, day, day, get_api_key())


def fetch_asof(series_id, cutoff, day):
    return fetch_snapshot(series_id, cutoff, day, get_api_key())


def main():
    if not get_api_key():
        raise SystemExit("Set FRED_API_KEY in the environment or Streamlit secrets before running the live audit.")
    day = date.today().isoformat()
    expected = {"BAA": ("2026-09-01", 6.47), "FEDFUNDS": ("2026-09-01", 3.75),
                "DGS10": ("2026-10-02", 5.28), "MORTGAGE30US": ("2026-10-01", 7.28)}
    report = {"download_day": day, "checks": []}
    for sid, (last, value) in expected.items():
        try:
            known = fetch_asof(sid, "2026-10-05", day)
            actual = known["values"]
            passed = not actual.empty and str(actual.index[-1].date()) == last and abs(actual.iloc[-1] - value) < 1e-9
            report["checks"].append({"series": sid, "passed": bool(passed),
                "actual_date": str(actual.index[-1].date()) if not actual.empty else None,
                "actual_value": float(actual.iloc[-1]) if not actual.empty else None,
                "url": known["url"], "requested_cutoff": known["requested_cutoff"],
                "downloaded_utc": known["downloaded_utc"]})
        except Exception as error:
            report["checks"].append({"series": sid, "passed": False, "error": str(error)})
    try:
        current = fetch_today("PAYEMS", day)
        known = fetch_asof("PAYEMS", "2025-01-15", day)
        summary, _ = compare(current["values"], known["values"])
        then = float(known["values"].loc["2024-12-01"])
        now = float(current["values"].loc["2024-12-01"])
        passed = str(known["values"].index[-1].date()) == "2024-12-01" and then == 159536 and now < then and summary["Revised shared dates"] > 0
        report["checks"].append({"series": "PAYEMS", "passed": bool(passed), "December_2024_then": then,
                                  "December_2024_today": now, "revised_count": summary["Revised shared dates"]})
    except Exception as error:
        report["checks"].append({"series": "PAYEMS", "passed": False, "error": str(error)})
    # Provisional chosen-series evidence, including last month's cutoff.
    try:
        cutoff = date.today().replace(day=1) - timedelta(days=1)
        current = fetch_today("DGS10", day)
        known = fetch_asof("DGS10", cutoff.isoformat(), day)
        summary, _ = compare(current["values"], known["values"])
        report["provisional_DGS10"] = {"cutoff": str(cutoff), "summary": summary,
            "latest_three": {str(k.date()): float(v) for k, v in current["values"].tail(3).items()},
            "downloaded_utc": current["downloaded_utc"]}
    except Exception as error:
        report["provisional_DGS10"] = {"error": str(error)}
    target = Path(__file__).with_name("live_audit.json")
    target.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print(target.read_text(encoding="utf-8"))
    raise SystemExit(0 if all(c["passed"] for c in report["checks"]) else 1)


if __name__ == "__main__":
    main()

