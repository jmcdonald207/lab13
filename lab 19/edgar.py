"""Deterministic SEC 10-K lab. No paid services or price data."""
import argparse
import hashlib
import json
import os
import re
import time
from datetime import date
from decimal import Decimal
from pathlib import Path
from urllib.request import Request, urlopen

TAGS = {
    'revenue': ['RevenueFromContractWithCustomerExcludingAssessedTax', 'Revenues'],
    'net_income': ['NetIncomeLoss'],
    'operating_cash_flow': ['NetCashProvidedByUsedInOperatingActivities'],
    'capital_spending': ['PaymentsToAcquirePropertyPlantAndEquipment', 'PaymentsToAcquireProductiveAssets'],
    'equity': ['StockholdersEquity'],
}
FLOW = set(TAGS) - {'equity'}
NUMBER = re.compile(r'(?<![\w])[-+−]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:[eE][-+]?\d+)?(?![\w])')
DEFAULT_AGENT = 'jmcdonald207 mcdon207@purdue.edu'


def fetch(url, agent):
    if not re.search(r'\S+@\S+\.\S+', agent) or len(agent.split()) < 2:
        raise ValueError('SEC User-Agent must contain your name and email.')
    for attempt in range(3):
        try:
            time.sleep(.2)
            with urlopen(Request(url, headers={'User-Agent': agent, 'Accept': 'application/json'}), timeout=45) as response:
                return json.load(response)
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)


def annual(f):
    try:
        return 350 <= (date.fromisoformat(f['end']) - date.fromisoformat(f['start'])).days <= 380
    except (KeyError, ValueError):
        return False


def eligible(f):
    return f.get('form') == '10-K' and f.get('filed', '9999') <= date.today().isoformat()


def select(gaap, metric, end):
    for tag in TAGS[metric]:
        candidates = [f for f in gaap.get(tag, {}).get('units', {}).get('USD', [])
                      if eligible(f) and f.get('end') == end
                      and (annual(f) if metric in FLOW else 'start' not in f)]
        if candidates:
            f = max(candidates, key=lambda x: (x['filed'], x['accn'], x.get('start', '')))
            return f['val'], {'tag': 'us-gaap:' + tag, **{k: f.get(k) for k in ('start', 'end', 'filed', 'accn', 'form')}}
    return None, {'tag': 'not found', 'attempted_tags': TAGS[metric]}


def year_row(gaap, end):
    """One row: select source facts first, then calculate only with present inputs."""
    row = {'fiscal_year_end': end, 'values': {}, 'sources': {}}
    for metric in TAGS:
        value, source = select(gaap, metric, end)
        row['values'][metric] = value
        row['sources'][metric] = source
    v = row['values']
    v['roe_percent'] = v['net_income'] / v['equity'] * 100 if v['net_income'] is not None and v['equity'] is not None and v['equity'] > 0 else None
    v['owner_earnings'] = v['operating_cash_flow'] - v['capital_spending'] if v['operating_cash_flow'] is not None and v['capital_spending'] is not None else None
    row['sources']['roe_percent'] = {'tag': 'derived: NetIncomeLoss / StockholdersEquity * 100'}
    row['sources']['owner_earnings'] = {'tag': 'derived: ' + row['sources']['operating_cash_flow']['tag'] + ' - ' + row['sources']['capital_spending']['tag']}
    return row


def build(facts, ticker):
    gaap = facts.get('facts', {}).get('us-gaap', {})
    # A comparative fact's fy is the filing's year, not necessarily the fact's year.
    # Each accession's latest annual flow end identifies its fiscal year end.
    filing_ends = {}
    for metric in FLOW:
        for tag in TAGS[metric]:
            for f in gaap.get(tag, {}).get('units', {}).get('USD', []):
                if eligible(f) and annual(f):
                    filing_ends[f['accn']] = max(filing_ends.get(f['accn'], ''), f['end'])
    ends = sorted(set(filing_ends.values()))[-5:]
    rows = [year_row(gaap, end) for end in ends]
    def check(metric, predicate):
        values = [r['values'][metric] for r in rows]
        return 'not known' if len(values) != 5 or any(v is None for v in values) else ('pass' if predicate(values) else 'fail')
    return {'ticker': ticker, 'entity': facts.get('entityName'), 'cik': facts.get('cik'), 'rows': rows,
            'checks': {'ROE >= 15% every year': check('roe_percent', lambda vs: all(v >= 15 for v in vs)),
                       'Owner earnings positive every year': check('owner_earnings', lambda vs: all(v > 0 for v in vs)),
                       'Owner earnings grew first to last': check('owner_earnings', lambda vs: vs[-1] > vs[0])}}


def display_value(metric, value):
    if value is None:
        return 'not known' if metric == 'roe_percent' else 'not found'
    return f'{value:.1f}' if metric == 'roe_percent' else f'{value / 1_000_000:,.3f}'.rstrip('0').rstrip('.')


def render(report):
    lines = [f"{report['ticker']} | {report['entity']}", 'Data: SEC EDGAR. Amounts in USD millions; ROE in percent.',
             'Fiscal year end | Metric | Value | XBRL tag / derivation']
    for row in report['rows']:
        for metric, value in row['values'].items():
            raw = '' if value is None or metric == 'roe_percent' else f' (USD {value:,})'
            lines.append(f"{row['fiscal_year_end']} | {metric} | {display_value(metric, value)}{raw} | {row['sources'][metric]['tag']}")
    lines.extend(f'{name}: {status}' for name, status in report['checks'].items())
    return '\n'.join(lines) + '\n'


def numeric_tokens(text):
    return [(m.group(), Decimal(m.group().replace(',', '').replace('−', '-'))) for m in NUMBER.finditer(text)]


def audit(memo, report):
    allowed = {v for _, v in numeric_tokens(render(report))}
    return [token for token, value in numeric_tokens(memo) if value not in allowed]


def fingerprint(report):
    return hashlib.sha256(json.dumps(report, sort_keys=True).encode()).hexdigest()


def load_company(ticker, agent):
    ticker = ticker.strip().upper()
    if not re.fullmatch(r'[A-Z0-9.-]{1,15}', ticker):
        raise ValueError('Invalid ticker.')
    mapping = fetch('https://www.sec.gov/files/company_tickers.json', agent)
    company = next((v for v in mapping.values() if v['ticker'].upper() == ticker), None)
    if company is None:
        raise ValueError('Ticker not found in SEC mapping.')
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{int(company['cik_str']):010d}.json"
    facts = fetch(url, agent)
    return build(facts, ticker), facts


def save(report, facts, out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    ticker = report['ticker']
    (out / f'{ticker}.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    (out / f'{ticker}_companyfacts.json').write_text(json.dumps(facts), encoding='utf-8')
    (out / f'{ticker}_report.txt').write_text(render(report), encoding='utf-8')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('ticker', nargs='?', default='COST')
    p.add_argument('--out', type=Path, default=Path.cwd() / 'output')
    p.add_argument('--facts', type=Path, help='Offline SEC companyfacts JSON')
    p.add_argument('--audit', type=Path)
    p.add_argument('--report', type=Path)
    p.add_argument('--bind-memo', action='store_true')
    args = p.parse_args()
    if args.audit:
        report = json.loads(args.report.read_text(encoding='utf-8'))
        flags = audit(args.audit.read_text(encoding='utf-8'), report)
        print(json.dumps({'unsupported_numbers': flags}, indent=2))
        if flags:
            raise SystemExit(1)
        if args.bind_memo:
            args.audit.with_suffix('.sha256').write_text(fingerprint(report), encoding='utf-8')
        return
    ticker = args.ticker.upper().strip()
    if args.facts:
        facts = json.loads(args.facts.read_text(encoding='utf-8'))
        report = build(facts, ticker)
    else:
        report, facts = load_company(ticker, os.environ.get('SEC_USER_AGENT', DEFAULT_AGENT))
    save(report, facts, args.out)
    print(render(report))


if __name__ == '__main__':
    main()
