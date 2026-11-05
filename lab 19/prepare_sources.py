"""Export unaltered relevant observations from the existing Lab 18 SEC caches.

This is a source subset, not a synthetic fixture. The app never imports expected answers.
"""
import hashlib
import json
from pathlib import Path
import panel

def main():
    manifest={}
    for ticker in ('COST','JPM'):
        source=panel.ROOT.parent/'lab 18/output'/f'{ticker}_companyfacts.json'
        raw=source.read_bytes()
        facts=json.loads(raw)
        baseline=panel.build(facts,ticker)
        ends={r['fiscal_year_end'] for r in baseline['rows']}
        gaap=facts['facts']['us-gaap']
        subset={k:facts[k] for k in ('cik','entityName')}
        subset['facts']={'us-gaap':{tag:{'units':{'USD':[f for f in gaap[tag].get('units',{}).get('USD',[]) if panel.edgar.eligible(f) and f.get('end') in ends]}} for tags in panel.edgar.TAGS.values() for tag in tags if tag in gaap}}
        assert panel.build(subset,ticker)==baseline, 'Source subset must reproduce full-cache report'
        target=panel.OUT/f'{ticker}_facts.json'
        target.write_text(json.dumps(subset,indent=2),encoding='utf-8')
        manifest[ticker]={'source':str(source.relative_to(panel.ROOT.parent)), 'source_sha256':hashlib.sha256(raw).hexdigest(), 'subset_sha256':hashlib.sha256(target.read_bytes()).hexdigest(), 'url':f'https://data.sec.gov/api/xbrl/companyfacts/CIK{int(facts["cik"]):010d}.json', 'note':'Existing Lab 18 SEC cache, not a fresh network download. Unmodified observations for permitted tags and selected fiscal ends; full-cache and subset reports compared equal.'}
    (panel.OUT/'source_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')

if __name__=='__main__':
    main()
