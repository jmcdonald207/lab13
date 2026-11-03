"""Compare downloaded reports with classroom expectations; never alter results."""
import csv
import json
from pathlib import Path
import edgar

HERE = Path(__file__).parent


def verify():
    discrepancies = []
    for ticker in ('COST', 'JPM'):
        path = HERE / 'output' / f'{ticker}.json'
        if not path.exists():
            discrepancies.append(f'{ticker}: live report unavailable; run python edgar.py {ticker}')
            continue
        report = json.loads(path.read_text(encoding='utf-8'))
        if ticker == 'COST':
            rows = {r['fiscal_year_end']: r for r in report['rows']}
            with (HERE / 'expected_cost.csv').open(newline='', encoding='utf-8') as f:
                for expected in csv.DictReader(f):
                    end = expected.pop('fiscal_year_end')
                    if end not in rows:
                        discrepancies.append(f'COST: expected fiscal year {end} absent from downloaded report')
                        continue
                    for metric, value in expected.items():
                        actual = edgar.display_value(metric, rows[end]['values'][metric]).replace(',', '')
                        if actual != value:
                            discrepancies.append(f'COST {end} {metric}: SEC={actual}; classroom={value}')
            for name, status in report['checks'].items():
                if status != 'pass':
                    discrepancies.append(f'COST {name}: {status}; expected pass')
        else:
            if len(report['rows']) != 5:
                discrepancies.append('JPM: fewer than five annual rows')
            for row in report['rows']:
                for metric in ('capital_spending', 'owner_earnings'):
                    if row['values'][metric] is not None:
                        discrepancies.append(f"JPM {row['fiscal_year_end']} {metric}: found in SEC; differs from classroom expectation")
            for name, status in report['checks'].items():
                if name.startswith('Owner') and status != 'not known':
                    discrepancies.append(f'JPM {name}: {status}; expected not known')
    return discrepancies


if __name__ == '__main__':
    differences = verify()
    print('\n'.join(differences) if differences else 'All live COST and JPM classroom checks match.')
    raise SystemExit(bool(differences))
