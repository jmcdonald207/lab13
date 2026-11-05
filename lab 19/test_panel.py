import copy
import json
import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest
import panel

class PanelTests(unittest.TestCase):
    def setUp(self):
        self.cost=panel.build(json.loads((panel.OUT/'COST_facts.json').read_text()),'COST')
        self.assertEqual(self.cost,json.loads((panel.OUT/'COST.json').read_text()))

    def test_known_answer_from_saved_report(self):
        r=self.cost
        self.assertEqual([x['fiscal_year_end'] for x in r['rows']],['2022-08-28','2023-09-03','2024-09-01','2025-08-31','2026-08-30'])
        self.assertEqual(round(r['revenue_growth_percent'],2),7.51)
        self.assertEqual([round(x['values']['liabilities_equity'],2) for x in r['rows']],[2.11,1.75,1.96,1.64,1.49])
        self.assertEqual(list(r['panel']['Buffett'].values()),['pass']*3)
        self.assertEqual(list(r['panel']['Cathie Wood'].values()),['fail','not known'])
        self.assertEqual(list(r['panel']['Burry'].values()),['pass']*2)
        self.assertTrue(all(x['values']['research_and_development'] is None for x in r['rows']))

    def test_probe_and_missing_inputs(self):
        self.assertEqual(list(panel.cathie_checks(self.cost,5).values()),['pass','not known'])
        r=copy.deepcopy(self.cost)
        r['revenue_growth_percent']=None
        self.assertEqual(list(panel.cathie_checks(r).values()),['not known']*2)
        r['rows'][0]['values']['operating_cash_flow']=None
        r['rows'][-1]['values']['liabilities_equity']=None
        self.assertEqual(list(panel.burry_checks(r).values()),['not known']*2)

    def test_boundary_is_inclusive(self):
        r=copy.deepcopy(self.cost)
        r['revenue_growth_percent']=15
        r['rows'][-1]['values']['rd_percent']=5
        self.assertEqual(list(panel.cathie_checks(r).values()),['pass']*2)
        for row in r['rows']:
            row['values']['operating_cash_flow']=row['values']['net_income']
        r['rows'][-1]['values']['liabilities_equity']=2
        self.assertEqual(list(panel.burry_checks(r).values()),['pass']*2)

    def test_source_gaps_and_denominators(self):
        facts=json.loads((panel.OUT/'COST_facts.json').read_text())
        del facts['facts']['us-gaap']['RevenueFromContractWithCustomerExcludingAssessedTax']
        facts['facts']['us-gaap'].pop('Revenues',None)
        r=panel.build(facts,'COST')
        self.assertIsNone(r['revenue_growth_percent'])
        self.assertEqual(list(r['panel']['Cathie Wood'].values()),['not known']*2)
        facts=json.loads((panel.OUT/'COST_facts.json').read_text())
        for fact in facts['facts']['us-gaap']['StockholdersEquity']['units']['USD']:
            fact['val']=0
        r=panel.build(facts,'COST')
        self.assertIsNone(r['rows'][-1]['values']['liabilities_equity'])
        self.assertEqual(list(r['panel']['Burry'].values())[-1],'not known')
        for ticker in ('COST','JPM'):
            r=panel.build(json.loads((panel.OUT/f'{ticker}_facts.json').read_text()),ticker)
            self.assertEqual(r,json.loads((panel.OUT/f'{ticker}.json').read_text()))

    def test_every_memo_and_injected_numbers(self):
        for ticker in ('COST','JPM'):
            r=json.loads((panel.OUT/f'{ticker}.json').read_text())
            memos={i:panel.memo_path(ticker,i).read_text(encoding='utf-8') for i in r['panel']}
            self.assertFalse(any(panel.audit_all(memos,r).values()))
            for investor in memos:
                edited=dict(memos)
                edited[investor]+=' Unsupported 987654321.123%.'
                self.assertEqual(panel.audit_all(edited,r)[investor],['987654321.123'])

    def test_app_and_live_editor_audit(self):
        app=AppTest.from_file(str(panel.ROOT/'app.py')).run(timeout=20)
        self.assertFalse(app.exception)
        self.assertEqual(len(app.text_area),3)
        for index in range(3):
            app.text_area[index].set_value('Unsupported 987654321.123%.').run()
            self.assertTrue(any('987654321.123' in x.value for x in app.error))
        app.text_input[0].set_value('JPM').run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.text_area),3)

if __name__=='__main__':
    unittest.main()
