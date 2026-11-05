"""Audit each saved memo and bind it to the reviewed printed report."""
import json
import panel

def main():
    summary={}
    for ticker in ('COST','JPM'):
        report=json.loads((panel.OUT/f'{ticker}.json').read_text())
        summary[ticker]={}
        for investor in report['panel']:
            path=panel.memo_path(ticker,investor)
            flags=panel.audit(path.read_text(encoding='utf-8'),report)
            summary[ticker][investor]=flags
            if flags:
                raise ValueError(f'{ticker} {investor}: {flags}')
            path.with_suffix('.sha256').write_text(panel.edgar.fingerprint(report),encoding='utf-8')
    (panel.OUT/'memo_audit.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    main()
