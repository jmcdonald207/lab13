"""Three classroom screens on identical SEC facts; no expected values in runtime."""
import argparse
import json
import math
from pathlib import Path
import edgar

ROOT = Path(__file__).parent
OUT = ROOT / 'output'
edgar.TAGS.update(liabilities=['Liabilities'], research_and_development=['ResearchAndDevelopmentExpense'])
edgar.FLOW.add('research_and_development')

def threshold():
    """The skill owns its growth design choice; editing its JSON changes code behavior."""
    return json.loads((ROOT / 'cathie-wood-edgar/rules.json').read_text())['growth_threshold_percent']

def status(value, predicate):
    return 'not known' if value is None else ('pass' if predicate(value) else 'fail')

def cathie_checks(report, growth_threshold=None):
    """Missing/invalid inputs remain unknown; never replace absent R&D with zero."""
    limit = threshold() if growth_threshold is None else growth_threshold
    growth = report['revenue_growth_percent']
    latest = report['rows'][-1]['values'] if report['rows'] else {}
    rd = latest.get('rd_percent')
    return {f'Revenue growth >= {limit:g}% a year, first to last': status(growth, lambda v: v >= limit),
            'R&D >= 5% of revenue, latest year': status(rd, lambda v: v >= 5)}

def burry_checks(report):
    rows = report['rows']
    pairs = [(r['values']['operating_cash_flow'], r['values']['net_income']) for r in rows]
    cash = None if len(pairs) != 5 or any(a is None or b is None for a,b in pairs) else all(a >= b for a,b in pairs)
    ratio = rows[-1]['values']['liabilities_equity'] if rows else None
    return {'Operating cash flow >= net income every year': status(cash, bool),
            'Liabilities <= twice equity, latest year': status(ratio, lambda v: v <= 2)}

def build(facts, ticker, growth_threshold=None):
    report = edgar.build(facts, ticker)
    for row in report['rows']:
        v = row['values']
        v['rd_percent'] = v['research_and_development'] / v['revenue'] * 100 if v['research_and_development'] is not None and v['revenue'] is not None and v['revenue'] > 0 else None
        v['liabilities_equity'] = v['liabilities'] / v['equity'] if v['liabilities'] is not None and v['equity'] is not None and v['equity'] > 0 else None
        row['sources']['rd_percent'] = {'tag': 'derived: ResearchAndDevelopmentExpense / revenue * 100'}
        row['sources']['liabilities_equity'] = {'tag': 'derived: Liabilities / StockholdersEquity'}
    revenues = [r['values']['revenue'] for r in report['rows']]
    report['revenue_growth_percent'] = ((revenues[-1]/revenues[0])**(1/4)-1)*100 if len(revenues)==5 and revenues[0] is not None and revenues[-1] is not None and revenues[0]>0 and revenues[-1]>=0 else None
    report['growth_threshold_percent'] = threshold() if growth_threshold is None else growth_threshold
    report['panel'] = {'Buffett': report['checks'], 'Cathie Wood': cathie_checks(report, growth_threshold), 'Burry': burry_checks(report)}
    return report

def display(metric, value):
    if metric in ('rd_percent', 'liabilities_equity'):
        return 'not known' if value is None else f'{value:.2f}'
    return edgar.display_value(metric, value)

def render(report):
    lines = [f"{report['ticker']} | {report['entity']}", 'SEC EDGAR annual 10-K facts. Amounts USD millions; ROE and R&D percent; liabilities/equity multiple.']
    for row in report['rows']:
        for metric,value in row['values'].items():
            raw = f' (USD {value:,})' if value is not None and metric not in ('roe_percent','rd_percent','liabilities_equity') else ''
            lines.append(f"{row['fiscal_year_end']} | {metric} | {display(metric,value)}{raw} | {row['sources'][metric]['tag']}")
    growth = report['revenue_growth_percent']
    lines.append('Revenue growth a year = (last / first)^(1/4) - 1: ' + ('not known' if growth is None else f'{growth:.2f}%'))
    lines.append(f"Cathie Wood growth threshold kept: {report['growth_threshold_percent']:g}%")
    for investor, checks in report['panel'].items():
        lines.extend(f'{investor} | {check} | {result}' for check,result in checks.items())
        lines.append(f'{investor}: {list(checks.values()).count("pass")} of {len(checks)} pass')
    return '\n'.join(lines)+'\n'

def audit(memo, report):
    allowed = {v for _,v in edgar.numeric_tokens(render(report))}
    return [token for token,value in edgar.numeric_tokens(memo) if value not in allowed]

def audit_all(memos, report):
    return {name:audit(memo,report) for name,memo in memos.items()}

def memo_path(ticker, investor):
    return OUT / f'{ticker}_{investor.replace(" ", "_")}_memo.md'

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('ticker')
    p.add_argument('--facts', type=Path)
    p.add_argument('--growth-threshold', type=float)
    args = p.parse_args()
    if args.growth_threshold is not None and (not math.isfinite(args.growth_threshold) or args.growth_threshold < 0):
        p.error('growth threshold must be finite and nonnegative')
    ticker = args.ticker.strip().upper()
    if not edgar.re.fullmatch(r'[A-Z0-9.-]{1,15}',ticker):
        p.error('invalid ticker')
    facts = json.loads(args.facts.read_text(encoding='utf-8')) if args.facts else edgar.load_company(ticker,edgar.os.environ.get('SEC_USER_AGENT',edgar.DEFAULT_AGENT))[1]
    report = build(facts,ticker,args.growth_threshold)
    OUT.mkdir(exist_ok=True)
    suffix = '' if args.growth_threshold is None else f'_probe_{args.growth_threshold:g}'
    (OUT / f'{ticker}{suffix}.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    (OUT / f'{ticker}{suffix}_report.txt').write_text(render(report),encoding='utf-8')
    print(render(report))

if __name__ == '__main__':
    main()
