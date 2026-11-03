"""Synthetic selection/arithmetic tests; these are NOT live SEC verification."""
import copy
import csv
import json
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import patch

import edgar

HERE = Path(__file__).parent


def fixture():
    facts = {'entityName': 'SYNTHETIC classroom fixture, not SEC data', 'facts': {'us-gaap': {}}}
    with (HERE / 'expected_cost.csv').open(newline='', encoding='utf-8') as f:
        for index, row in enumerate(csv.DictReader(f)):
            end = row['fiscal_year_end']
            start = (date.fromisoformat(end) - timedelta(days=364)).isoformat()
            for metric, tags in edgar.TAGS.items():
                fact = {'end': end, 'val': int(row[metric]) * 1_000_000, 'filed': end[:4] + '-10-20', 'form': '10-K', 'accn': str(index)}
                if metric in edgar.FLOW:
                    fact['start'] = start
                facts['facts']['us-gaap'].setdefault(tags[0], {'units': {'USD': []}})['units']['USD'].append(fact)
    return facts


class ArithmeticTests(unittest.TestCase):
    def test_classroom_arithmetic(self):
        report = edgar.build(fixture(), 'TEST')
        self.assertEqual(len(report['rows']), 5)
        self.assertEqual(list(report['checks'].values()), ['pass'] * 3)
        self.assertEqual([r['values']['owner_earnings'] for r in report['rows']], [3501e6, 6745e6, 6629e6, 7837e6, 9382e6])
        self.assertEqual([edgar.display_value('roe_percent', r['values']['roe_percent']) for r in report['rows']], ['28.3', '25.1', '31.2', '27.8', '25.8'])

    def test_changed_inputs_change_outputs(self):
        facts = fixture()
        facts['facts']['us-gaap']['NetCashProvidedByUsedInOperatingActivities']['units']['USD'][-1]['val'] += 1234567
        report = edgar.build(facts, 'TEST')
        self.assertEqual(report['rows'][-1]['values']['owner_earnings'], 9382e6 + 1234567)

    def test_missing_capex_is_not_zero(self):
        facts = fixture()
        del facts['facts']['us-gaap']['PaymentsToAcquirePropertyPlantAndEquipment']
        report = edgar.build(facts, 'TEST')
        for row in report['rows']:
            self.assertIsNone(row['values']['capital_spending'])
            self.assertIsNone(row['values']['owner_earnings'])
        self.assertEqual(list(report['checks'].values())[1:], ['not known', 'not known'])
        self.assertIn('not found', edgar.render(report))

    def test_latest_annual_10k_wins(self):
        facts = fixture()
        fs = facts['facts']['us-gaap']['NetIncomeLoss']['units']['USD']
        replacement = {**fs[0], 'filed': '2025-10-20', 'accn': 'revised', 'val': 123e6}
        fs.extend([replacement, {**replacement, 'form': '10-Q', 'filed': '2025-11-20', 'val': 999e6},
                   {**replacement, 'start': '2022-06-01', 'filed': '2025-12-20', 'val': 888e6}])
        row = edgar.build(facts, 'TEST')['rows'][0]
        self.assertEqual(row['values']['net_income'], 123e6)
        self.assertEqual(row['sources']['net_income']['filed'], '2025-10-20')

    def test_fallback_and_priority(self):
        gaap = fixture()['facts']['us-gaap']
        gaap['Revenues'] = copy.deepcopy(gaap['RevenueFromContractWithCustomerExcludingAssessedTax'])
        gaap['Revenues']['units']['USD'][0]['val'] = 1
        self.assertEqual(edgar.year_row(gaap, '2022-08-28')['values']['revenue'], 226954e6)
        del gaap['RevenueFromContractWithCustomerExcludingAssessedTax']
        self.assertEqual(edgar.year_row(gaap, '2022-08-28')['values']['revenue'], 1)

    def test_nonpositive_equity_and_missing_income(self):
        gaap = fixture()['facts']['us-gaap']
        for value in (0, -1):
            gaap['StockholdersEquity']['units']['USD'][0]['val'] = value
            self.assertIsNone(edgar.year_row(gaap, '2022-08-28')['values']['roe_percent'])
        del gaap['NetIncomeLoss']
        self.assertIsNone(edgar.year_row(gaap, '2022-08-28')['values']['roe_percent'])

    def test_audit(self):
        report = edgar.build(fixture(), 'TEST')
        self.assertEqual(edgar.audit('ROE 28.3%; owner earnings $3,501 million.', report), [])
        self.assertEqual(edgar.audit('ROE 40.0%. Again 40.0%.', report), ['40.0', '40.0'])

    def test_app_number_probe(self):
        from streamlit.testing.v1 import AppTest
        # Temporary synthetic snapshot: never installed as a runtime COST result.
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp)
            report = edgar.build(fixture(), 'COST')
            (out / 'COST.json').write_text(json.dumps(report), encoding='utf-8')
            original_read = Path.read_text
            original_exists = Path.exists
            def mapped(p):
                return out / p.name if p.parent == HERE / 'output' else p
            with patch.object(Path, 'read_text', lambda p, *a, **kw: original_read(mapped(p), *a, **kw)), patch.object(Path, 'exists', lambda p: original_exists(mapped(p))):
                app = AppTest.from_file(str(HERE / 'app.py')).run(timeout=20)
                self.assertEqual(len(app.exception), 0)
                app.text_area[0].input('ROE 40.0%.').run()
                self.assertTrue(any('40.0' in error.value for error in app.error))


if __name__ == '__main__':
    unittest.main()
