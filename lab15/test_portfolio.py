"""Course known-answer and deliberate-break checks. Run: python test_portfolio.py"""
import copy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import portfolio as p


class PortfolioChecks(unittest.TestCase):
    def test_known_answers(self):
        vols = [s['volatility'] for s in p.SLEEVES]
        returns = [s['expected_return'] for s in p.SLEEVES]
        p.validate_inputs(p.SLEEVES, p.CORRELATIONS, p.OBJECTIVE_RETURN)
        cov = p.covariance_matrix(vols, p.CORRELATIONS)
        cases = [
            (p.benchmark_weights(), ['0.0', '0.0', '40.0', '60.0'], '6.80', '10.46', '0.0', True),
            (p.equal_weights(4), ['25.0'] * 4, '5.20', '5.21', '50.0', False),
            (p.inverse_volatility_weights(vols), ['84.3', '6.0', '7.0', '2.6'], '3.77', '1.05', '90.3', False),
        ]
        for weights, display, ret, risk, reserve, meets in cases:
            self.assertAlmostEqual(sum(weights), 1)
            self.assertEqual([f'{w * 100:.1f}' for w in weights], display)
            result = p.expected_return(weights, returns)
            self.assertEqual(f'{result * 100:.2f}', ret)
            self.assertEqual(f'{p.portfolio_volatility(weights, cov) * 100:.2f}', risk)
            self.assertEqual(f'{p.reserve_eligible_weight(weights) * 100:.1f}', reserve)
            self.assertEqual(p.meets_objective(result, p.OBJECTIVE_RETURN), meets)

    def test_correlation_changes_risk(self):
        corr = copy.deepcopy(p.CORRELATIONS)
        corr[2][3] = corr[3][2] = 0.50
        p.validate_inputs(p.SLEEVES, corr, p.OBJECTIVE_RETURN)
        cov = p.covariance_matrix([s['volatility'] for s in p.SLEEVES], corr)
        self.assertEqual(f'{p.portfolio_volatility(p.benchmark_weights(), cov) * 100:.2f}', '11.00')
        self.assertEqual(p.CORRELATIONS[2][3], 0.25)

    def test_cli_refuses_bad_inputs(self):
        source = Path(p.__file__).read_text()
        for replacement, message in [
            ('[0.05, 0.80, 1.0, 1.3]', 'from -1 to 1'),
            ('[0.05, 0.80, 1.0, 0.50]', 'not symmetric'),
        ]:
            with tempfile.TemporaryDirectory() as folder:
                script = Path(folder) / 'portfolio.py'
                script.write_text(source.replace('[0.05, 0.80, 1.0, 0.25]', replacement))
                run = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
                self.assertNotEqual(run.returncode, 0)
                self.assertIn(message, run.stderr)


if __name__ == '__main__':
    unittest.main()

