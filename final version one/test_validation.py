"""Offline known-answer checks for the Project 2 mandate search."""
import unittest
from math import hypot
from unittest.mock import patch

from portfolio import search_portfolio
from run import evaluate, report


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.sleeves = [
            {"name": "SGOV", "expected_return": 0.04, "volatility": 0.01},
            {"name": "VT", "expected_return": 0.09, "volatility": 0.16},
        ]
        self.correlations = [[1, 0], [0, 1]]

    def test_lowest_volatility_mix_at_exact_return_boundary(self):
        # Half equity earns exactly 6.5%. Every lower equity grid weight fails.
        result = search_portfolio(self.sleeves, self.correlations, 0.065, 0.03, (True, False))
        self.assertEqual(result["weights"], [0.5, 0.5])
        self.assertAlmostEqual(result["expected_return"], 0.065)
        self.assertAlmostEqual(result["volatility"], hypot(0.005, 0.08))
        self.assertAlmostEqual(result["reserve_eligible_weight"], 0.5)

    def test_cost_drag_requires_more_equity(self):
        # With a 0.5% drag, the first qualifying equity grid weight is 60%.
        net_sleeves = [dict(sleeve, expected_return=sleeve["expected_return"] - 0.005)
                       for sleeve in self.sleeves]
        result = search_portfolio(net_sleeves, self.correlations, 0.065, 0.03, (True, False))
        self.assertEqual(result["weights"], [0.4, 0.6])
        self.assertAlmostEqual(result["expected_return"], 0.065)

    def test_no_eligible_reserve_stops_search(self):
        result = search_portfolio(self.sleeves, self.correlations, 0.065, 0.03, (False, False))
        self.assertIsNone(result)
        self.assertIn("FAIL (no qualifying mix)", report(self.sleeves, result))

    def test_sample_cutoff_excludes_future_price_jump(self):
        # Four prices imply returns of 10%, 0%, and 100%. The last is held back.
        prices = tuple((100, 110, 110, 220) for _ in range(4))
        with patch("run.load_prices", return_value=prices):
            full, _ = evaluate()
            cutoff, _ = evaluate(months_held_back=1)
        self.assertAlmostEqual(full[-1]["expected_return"], 4.4)
        self.assertAlmostEqual(cutoff[-1]["expected_return"], 0.6)


if __name__ == "__main__":
    unittest.main()
