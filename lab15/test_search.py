"""Run: python -m unittest test_portfolio test_search -v"""
import copy
import unittest
import portfolio as p


class SearchChecks(unittest.TestCase):
    def run_search(self, sleeves=None, correlations=None, objective=0.065):
        return p.search(sleeves or p.SLEEVES, correlations or p.CORRELATIONS,
                        objective, [True, True, False, False], 0.03)

    def check_answer(self, result, weights, ret, risk):
        self.assertEqual([round(w * 100) for w in result["weights"]], weights)
        self.assertEqual(f'{result["expected_return"] * 100:.2f}', ret)
        self.assertEqual(f'{result["volatility"] * 100:.2f}', risk)
        self.assertGreaterEqual(result["reserve_weight"], 0.03)

    def test_meridian_and_one_point_change(self):
        baseline = self.run_search()
        self.check_answer(baseline, [0, 20, 25, 55], "6.51", "9.44")
        sleeves = copy.deepcopy(p.SLEEVES)
        sleeves[3]["expected_return"] = 0.07
        stressed = self.run_search(sleeves=sleeves)
        self.check_answer(stressed, [0, 10, 10, 80], "6.53", "12.94")
        self.assertAlmostEqual(max(abs(a - b) for a, b in
                                   zip(baseline["weights"], stressed["weights"])), 0.25)

    def test_engine_correlation_change(self):
        corr = copy.deepcopy(p.CORRELATIONS)
        corr[2][3] = corr[3][2] = 0.50
        self.check_answer(self.run_search(correlations=corr), [0, 40, 0, 60], "6.52", "9.73")

    def test_infeasible(self):
        self.assertIsNone(self.run_search(objective=0.20))
        self.assertIsNone(p.search(p.SLEEVES, p.CORRELATIONS, 0.065,
                                  [False] * 4, 0.03))

    def test_three_and_six_assets(self):
        for count in (3, 6):
            sleeves = [dict(name=str(i), expected_return=0.05, volatility=0.1)
                       for i in range(count)]
            corr = [[float(i == j) for j in range(count)] for i in range(count)]
            result = p.search(sleeves, corr, 0.05, [False] * count, 0)
            self.assertAlmostEqual(sum(result["weights"]), 1)
            self.assertTrue(all(abs(w * 20 - round(w * 20)) < 1e-10
                                for w in result["weights"]))


if __name__ == "__main__":
    unittest.main()
