"""Offline leakage and UI checks. Fixtures are synthetic, not claimed live evidence."""
import unittest
from unittest.mock import patch
from datetime import date
import requests
from streamlit.testing.v1 import AppTest
from asof_app import parse_csv, compare, fetch_asof


class AuditTests(unittest.TestCase):
    def test_missing_revisions_and_later_observations(self):
        known = parse_csv("DATE,X_20250115\n2024-11-01,100\n2024-12-01,110\n2025-01-01,.\n")
        current = parse_csv("observation_date,X\n2024-11-01,99\n2024-12-01,110\n2025-01-01,120\n")
        summary, revisions = compare(current, known)
        self.assertEqual(summary["Later observations"], 1)
        self.assertEqual(summary["Revised shared dates"], 1)
        self.assertEqual(summary["Value known then"], 110)
        self.assertEqual(len(revisions), 1)

    def test_real_vintage_request(self):
        fetch_asof.clear()
        with patch("asof_app.download", return_value={"values": parse_csv("DATE,X\n2024-12-01,10\n2025-02-01,20\n")}) as mocked:
            result = fetch_asof("PAYEMS", "2025-01-15", date.today().isoformat())
            self.assertIn("alfredgraph.csv", mocked.call_args.args[0])
            self.assertEqual(mocked.call_args.args[1]["vintage_date"], "2025-01-15")
            self.assertEqual(len(result["values"]), 1)
        fetch_asof.clear()

    def test_empty_vintage(self):
        current = parse_csv("DATE,X\n2024-12-01,10\n")
        summary, _ = compare(current, current.iloc[:0])
        self.assertIsNone(summary["Value known then"])
        self.assertEqual(summary["Later observations"], 1)

    def test_ui_and_bad_id_isolation(self):
        def fake_download(url, params):
            if params["id"] == "UNKNOWN":
                raise requests.HTTPError("Unknown ID")
            return {"values": parse_csv("DATE,X\n2024-12-01,10\n2025-01-01,11\n"),
                    "url": url, "downloaded_utc": "synthetic offline test"}
        with patch("asof_app.requests.get") as get:
            get.return_value.text = "DATE,X\n2024-12-01,10\n2025-01-01,11\n"
            get.return_value.url = "https://example.test/fixture"
            app = AppTest.from_file(str(__import__('pathlib').Path(__file__).with_name('asof_app.py'))).run(timeout=30)
            self.assertEqual(len(app.exception), 0)
            self.assertEqual(len(app.dataframe), 5)
            get.side_effect = requests.HTTPError("Unknown ID")
            app.sidebar.text_input[0].set_value("UNKNOWN").run(timeout=30)
            self.assertEqual(len(app.exception), 0)
            self.assertTrue(any("UNKNOWN" in item.value for item in app.error))
            self.assertEqual(len(app.dataframe), 5)


if __name__ == "__main__":
    unittest.main()

