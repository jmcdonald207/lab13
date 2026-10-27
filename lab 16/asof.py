"""Lab 15: point-in-time provenance gate (Python standard library only)."""

from datetime import date
from decimal import Decimal


# Editable inputs: row, ticker, month measured, published on, price.
DECISION_DATE = "2026-03-31"
TABLE = [
    (1, "AAA", "2026-01", "2026-02-10", "101.0"),
    (2, "AAA", "2026-02", "2026-03-10", "104.0"),
    (3, "AAA", "2026-03", "2026-04-10", "109.0"),
    (4, "AAA", "2026-02", "2026-03-25", "103.0"),
    (5, "BBB", "2026-01", "2026-02-10", "98.0"),
    (6, "BBB", "2026-02", "2026-03-10", "97.0"),
    (7, "BBB", "2026-02", "2026-03-10", "97.0"),
    (8, "BBB", "2026-03", "2026-04-10", "92.0"),
    (9, "CCC", "2026-01", "2026-02-10", "110.0"),
    (10, "CCC", "2026-02", "2026-04-05", "112.0"),
    (11, "", "2026-02", "2026-03-10", "99.0"),
    (12, "CCC", "2026-02", "2026-03-10", "111.0"),
]


def parse_table(table):
    return [dict(row=n, ticker=t.strip(), month=date.fromisoformat(m + "-01"),
                 published=date.fromisoformat(p), price=Decimal(str(v)))
            for n, t, m, p, v in table]


def latest_publications(rows):
    """Rule 4: caller first limits rows to publications allowed at the cutoff."""
    latest = {}
    for row in rows:
        key = (row["ticker"], row["month"])
        if key not in latest or row["published"] > latest[key]["published"]:
            latest[key] = row
        elif (row["published"] == latest[key]["published"]
              and row["price"] != latest[key]["price"]):
            raise ValueError(f"Conflicting prices for {key} on {row['published']}")
    kept = {row["row"] for row in latest.values()}
    return ([row for row in rows if row["row"] in kept],
            [row["row"] for row in rows if row["row"] not in kept])


def filter_asof(rows, decision_date):
    funnel = []
    admitted = [r for r in rows if r["ticker"]]
    funnel.append(("Quarantined: no ticker", [r["row"] for r in rows if not r["ticker"]]))

    seen, unique, duplicates = set(), [], []
    for row in admitted:
        # Source row number is provenance, not part of a duplicate's content.
        key = (row["ticker"], row["month"], row["published"], row["price"])
        if key in seen:
            duplicates.append(row["row"])
        else:
            seen.add(key)
            unique.append(row)
    funnel.append(("Exact duplicate", duplicates))

    eligible = [r for r in unique if r["published"] <= decision_date]
    funnel.append(("Published after decision date",
                   [r["row"] for r in unique if r["published"] > decision_date]))
    panel, replaced = latest_publications(eligible)
    funnel.append(("Older vintage replaced by a revision", replaced))
    # Naive comparison uses the same identity/duplicate gate, but no date gate.
    naive, _ = latest_publications(unique)
    return panel, naive, funnel


def signals(panel):
    result = {}
    for ticker in sorted({r["ticker"] for r in panel}):
        history = sorted((r for r in panel if r["ticker"] == ticker),
                         key=lambda r: r["month"])
        latest = history[-1]
        month = latest["month"]
        previous_month = date(month.year - (month.month == 1),
                              12 if month.month == 1 else month.month - 1, 1)
        previous = next((r for r in history if r["month"] == previous_month), None)
        change = None if previous is None else (latest["price"] / previous["price"] - 1) * 100
        result[ticker] = (month, change)
    return result


def main():
    cutoff = date.fromisoformat(DECISION_DATE)
    panel, naive, funnel = filter_asof(parse_table(TABLE), cutoff)
    print(f"Decision date: {cutoff}\n\nRow funnel")
    for label, removed in funnel:
        print(f"{label}: {len(removed)}; rows {', '.join(map(str, removed)) or 'none'}")
    print(f"As-of panel: {len(panel)}; rows {', '.join(str(r['row']) for r in panel)}")
    print("\nRow Ticker Month   Published  Price")
    for r in panel:
        print(f"{r['row']:>3} {r['ticker']:6} {r['month']:%Y-%m} {r['published']} {r['price']}")
    for label, data in (("As-of", panel), ("Naive", naive)):
        print(f"\n{label} signals")
        for ticker, (month, change) in signals(data).items():
            value = "unavailable (no previous calendar month)" if change is None else f"{change:+.2f}%"
            print(f"{ticker}: {value} ({month:%B %Y})")


if __name__ == "__main__":
    main()
