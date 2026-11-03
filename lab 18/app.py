import json
import os
from pathlib import Path

import pandas as pd
import streamlit as st
import edgar

OUT = Path(__file__).parent / 'output'
st.set_page_config(page_title='Buffett business notebook', layout='wide')
st.title('Buffett business notebook')
st.caption('data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.')
ticker = st.text_input('Ticker', 'COST').strip().upper()
if not edgar.re.fullmatch(r'[A-Z0-9.-]{1,15}', ticker):
    st.error('Enter a valid ticker.')
    st.stop()
agent = st.text_input('SEC User-Agent: name and email', os.environ.get('SEC_USER_AGENT', edgar.DEFAULT_AGENT))
if st.button('Download SEC facts', type='primary'):
    try:
        with st.spinner('Reading SEC annual filings…'):
            report, facts = edgar.load_company(ticker, agent)
            edgar.save(report, facts, OUT)
    except Exception as exc:
        st.error(f'SEC download failed: {exc}')
path = OUT / f'{ticker}.json'
if not path.exists():
    st.info('Download SEC facts to begin. No estimated values are prefilled.')
    st.stop()
report = json.loads(path.read_text(encoding='utf-8'))
st.subheader(report.get('entity') or ticker)
st.caption('Saved SEC snapshot. Refresh with Download SEC facts. USD millions except ROE (%).')
records = [{'Fiscal year end': r['fiscal_year_end'], **{k: (v / 1_000_000 if v is not None and k != 'roe_percent' else v) for k, v in r['values'].items()}} for r in report['rows']]
frame = pd.DataFrame(records)
if not frame.empty:
    st.line_chart(frame.set_index('Fiscal year end')[['owner_earnings', 'net_income']], y_label='USD millions')
    shown = pd.DataFrame([{'Fiscal year end': r['fiscal_year_end'], **{k: edgar.display_value(k, v) for k, v in r['values'].items()}} for r in report['rows']])
    st.dataframe(shown, hide_index=True)
else:
    st.warning('No qualifying annual periods found.')
st.table(pd.DataFrame(report['checks'].items(), columns=['Check', 'Result']))
with st.expander('XBRL tags and filing provenance'):
    st.json([{'fiscal_year_end': r['fiscal_year_end'], 'sources': r['sources']} for r in report['rows']])
st.download_button('Download printed report', edgar.render(report), file_name=f'{ticker}_report.txt')
st.subheader('Business-quality memo')
memo_path = OUT / f'{ticker}_memo.md'
saved = memo_path.read_text(encoding='utf-8') if memo_path.exists() else ''
memo = st.text_area('Memo editor — try adding 40.0% to test the audit', saved, height=240, key=f'memo_{ticker}_{edgar.fingerprint(report)}')
if memo:
    st.markdown(memo)
    flags = edgar.audit(memo, report)
    if flags:
        st.error('Numbers absent from the printed report: ' + ', '.join(flags))
    else:
        st.success('All numeric tokens occur in the printed report. Review their meaning and units too.')
    binding = memo_path.with_suffix('.sha256')
    if memo != saved or not binding.exists() or binding.read_text(encoding='utf-8').strip() != edgar.fingerprint(report):
        st.warning('Edited, unbound, or stale memo: ask Codex to review against this report before binding.')
    st.download_button('Download memo', memo, file_name=memo_path.name)
else:
    st.info(f'Ask Codex to use buffett-edgar on {ticker} and save output/{ticker}_memo.md. The model writes the judgment after reading the report.')
decision_path = OUT / f'{ticker}_decision.md'
decision = st.text_input('Your decision: do you trust the verdict, and why?', decision_path.read_text(encoding='utf-8') if decision_path.exists() else '', key=f'decision_{ticker}')
if st.button('Save my decision'):
    decision_path.write_text(decision + '\n', encoding='utf-8')
    st.success('Decision saved.')
