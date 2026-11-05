import json
import os
import pandas as pd
import streamlit as st
import panel

st.set_page_config(page_title='Investor panel', layout='wide')
st.title('Same facts, different investors')
st.caption('AI simulations of investor perspectives. SEC EDGAR facts; classroom business screens.')
ticker = st.text_input('Ticker', 'COST').strip().upper()
if not panel.edgar.re.fullmatch(r'[A-Z0-9.-]{1,15}', ticker):
    st.error('Enter a valid ticker.')
    st.stop()
agent = st.text_input('SEC User-Agent: name and email', os.environ.get('SEC_USER_AGENT', panel.edgar.DEFAULT_AGENT))
if st.button('Reload saved reports — no internet needed'):
    st.rerun()
if st.button('Download SEC facts', type='primary'):
    try:
        _, facts = panel.edgar.load_company(ticker, agent)
        report = panel.build(facts,ticker)
        panel.OUT.mkdir(exist_ok=True)
        (panel.OUT / f'{ticker}.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
        (panel.OUT / f'{ticker}_report.txt').write_text(panel.render(report),encoding='utf-8')
    except Exception as exc:
        st.error(f'SEC download failed: {exc}')
        st.info('Run python panel.py TICKER in normal PowerShell, then reload saved reports.')
path = panel.OUT / f'{ticker}.json'
if not path.exists():
    st.info('No saved company report. Download facts to begin; gaps are never estimated.')
    st.stop()
report = json.loads(path.read_text(encoding='utf-8'))
st.subheader(report['entity'])
st.caption('Saved snapshot. Download to refresh. USD millions except percentage and ratio columns.')
if report['growth_threshold_percent'] != panel.threshold():
    st.warning('Skill threshold changed: rerun panel.py to recompute this snapshot and review memos.')
rows = report['rows']
if rows:
    frame = pd.DataFrame([{'Fiscal year end': r['fiscal_year_end'], **{k:r['values'][k]/1_000_000 if r['values'][k] is not None else None for k in ('owner_earnings','net_income')}} for r in rows])
    st.line_chart(frame.set_index('Fiscal year end'),y_label='USD millions')
    st.dataframe(pd.DataFrame([{'Fiscal year end':r['fiscal_year_end'],**{k:panel.display(k,v) for k,v in r['values'].items()}} for r in rows]),hide_index=True)
growth = report['revenue_growth_percent']
st.write('Revenue growth a year: '+('not known' if growth is None else f'{growth:.2f}%'))
st.table(pd.DataFrame([{'Investor':name,'Check':check,'Result':result} for name,checks in report['panel'].items() for check,result in checks.items()]))
st.caption('Owner earnings = operating cash flow minus total capital spending. ROE uses year-end equity. Screens do not prove a moat, innovation, clean accounting, or a fair price.')
with st.expander('Tags and filing provenance'):
    st.json([{'fiscal_year_end':r['fiscal_year_end'],'sources':r['sources']} for r in rows])
st.download_button('Download printed report',panel.render(report),file_name=f'{ticker}_report.txt')
edited = {}
for column,(investor,checks) in zip(st.columns(3), report['panel'].items()):
    with column:
        st.subheader(investor)
        st.write(f'{list(checks.values()).count("pass")} of {len(checks)} checks pass')
        memo_path = panel.memo_path(ticker,investor)
        saved = memo_path.read_text(encoding='utf-8') if memo_path.exists() else ''
        memo = st.text_area(f'{investor} verdict and memo',saved,height=300,key=f'{ticker}_{investor}_{panel.edgar.fingerprint(report)}')
        edited[investor] = memo
        if memo:
            st.markdown(memo)
            binding = memo_path.with_suffix('.sha256')
            if memo != saved or not binding.exists() or binding.read_text().strip() != panel.edgar.fingerprint(report):
                st.warning('Edited, unbound, or stale memo: review against printed report.')
            st.download_button(f'Download {investor} memo',memo,file_name=memo_path.name)
        else:
            st.info('Ask the investor skill to read the printed report and write its own verdict and memo.')
        if investor == 'Cathie Wood':
            st.caption(f'Threshold kept: {report["growth_threshold_percent"]:g}%; retain the assigned high-growth screen. The saved COST 5% probe passes growth; R&D stays not known.')
flags = panel.audit_all(edited,report)
if any(flags.values()):
    st.error('Unprinted-number flag across all memos: '+str({k:v for k,v in flags.items() if v}))
else:
    st.success('Unprinted-number flag: clear across all entered memos. Check meaning and units manually.')
if any(not m.strip() for m in edited.values()):
    st.warning('Panel incomplete: an investor memo is missing.')
decision_path = panel.OUT / f'{ticker}_decision.md'
decision = st.text_input('Your decision and condition',decision_path.read_text(encoding='utf-8') if decision_path.exists() else '')
if st.button('Save my decision'):
    decision_path.write_text(decision+'\n',encoding='utf-8')
    st.success('Decision saved.')
