"""Offline regression tests; run with python -m unittest -v test_asof."""
from datetime import date, timedelta
import unittest
from unittest.mock import patch, Mock

import pandas as pd
import requests
from pathlib import Path
from streamlit.testing.v1 import AppTest

import asof_app as app


def series(dates, values):
    return pd.Series(values, index=pd.to_datetime(dates), dtype=float)


class AsOfTests(unittest.TestCase):
    def test_ui_and_bad_id_isolation(self):
        def fake_api(endpoint, params, api_key):
            if params["series_id"] == "UNKNOWN":
                raise app.FredDownloadError("FRED request failed (HTTP 400). Check series ID.")
            if endpoint == "series":
                return {"seriess": [{"id": params["series_id"], "title": "Synthetic fixture",
                                    "units": "Percent", "frequency": "Daily", "seasonal_adjustment": "NSA"}]}
            return {"realtime_start": params["realtime_start"], "realtime_end": params["realtime_end"],
                    "count": 1, "observations": [{"date": "2020-01-01", "value": "2"}]}
        app.fetch_metadata.clear()
        app.fetch_snapshot.clear()
        def fake_get(url, params, timeout):
            response = Mock(ok=True)
            response.json.return_value = fake_api(url.rsplit("/fred/", 1)[1], params, params["api_key"])
            return response
        try:
            with patch.dict("os.environ", {"FRED_API_KEY": "synthetic-key"}), patch("requests.get", side_effect=fake_get):
                ui = AppTest.from_file(str(Path(__file__).with_name("asof_app.py"))).run(timeout=30)
                self.assertEqual(len(ui.exception), 0)
                self.assertEqual(len(ui.dataframe), 5)
                ui.sidebar.text_input[0].set_value("UNKNOWN").run(timeout=30)
                self.assertEqual(len(ui.exception), 0)
                self.assertTrue(any("UNKNOWN" in item.value for item in ui.error))
                self.assertEqual(len(ui.dataframe), 5)
        finally:
            app.fetch_metadata.clear()
            app.fetch_snapshot.clear()

    def test_csv_validation(self):
        good = app.parse_csv("DATE,BAA\n2020-01-01,2\n2020-01-02,.\n", "BAA")
        self.assertEqual(len(good), 1)
        for text in ["DATE,OTHER\n2020-01-01,2\n", "DATE,BAA\n,2\n",
                     "DATE,BAA\n2020-01-01,inf\n", "DATE,BAA\n2020-01-01,2\n2020-01-01,3\n",
                     "<html>Error</html>", "DATE,BAA\nnot-a-date,2\n"]:
            with self.subTest(text=text), self.assertRaises(ValueError):
                app.parse_csv(text, "BAA")

    def test_all_difference_types(self):
        known = series(["2020-01-02", "2020-01-03"], [2, 3])
        current = series(["2020-01-01", "2020-01-02", "2020-01-04"], [1, 2.5, 4])
        counts, changes = app.compare(current, known)
        self.assertEqual(counts["Revised shared dates"], 1)
        self.assertEqual(counts["Older observations added"], 1)
        self.assertEqual(counts["Later observations"], 1)
        self.assertEqual(counts["Historical dates absent today"], 1)
        self.assertEqual(len(changes), 4)

    def test_empty_and_unchanged(self):
        empty = series([], [])
        current = series(["2020-01-01"], [1])
        counts, changes = app.compare(current, empty)
        self.assertEqual(counts["Current-only dates without historical baseline"], 1)
        self.assertEqual(counts["Later observations"], 0)
        self.assertIsNone(counts["Value known then"])
        self.assertEqual(len(changes), 1)
        self.assertTrue(app.compare(current, current)[1].empty)
        self.assertTrue(app.compare(empty, empty)[1].empty)

    def test_identifier(self):
        self.assertEqual(app.validate_id(" baa "), "BAA")
        with self.assertRaises(ValueError):
            app.validate_id("BAA&x=1")

    def test_future_cutoff(self):
        with self.assertRaises(ValueError):
            app.fetch_snapshot.__wrapped__("BAA", (date.today() + timedelta(days=1)).isoformat(), "test", "secret")

    def test_historical_request_and_pagination(self):
        def page(offset):
            return {"realtime_start": "2020-01-03", "realtime_end": "2020-01-03", "count": 2,
                    "observations": [{"date": f"2020-01-0{offset + 1}", "value": str(offset + 2)}]}
        with patch.object(app, "api_json", side_effect=[page(0), page(1)]) as get:
            snapshot = app.fetch_snapshot.__wrapped__("BAA", "2020-01-03", "test", "secret")
        self.assertEqual(len(snapshot["values"]), 2)
        params = get.call_args.args[1]
        self.assertEqual(params["realtime_start"], "2020-01-03")
        self.assertEqual(params["realtime_end"], "2020-01-03")
        self.assertEqual(params["offset"], 1)
        self.assertNotIn("secret", snapshot["url"])
        self.assertNotIn("api_key", snapshot["url"])

    def test_wrong_vintage_rejected(self):
        with patch.object(app, "api_json", return_value={"realtime_start": "2025-01-01"}):
            with self.assertRaises(ValueError):
                app.fetch_snapshot.__wrapped__("BAA", "2020-01-03", "test", "secret")

    def test_http_error_does_not_disclose_key(self):
        with patch.object(app.requests, "get") as get:
            get.return_value.ok = False
            get.return_value.status_code = 400
            with self.assertRaisesRegex(ValueError, "HTTP 400"):
                app.api_json("series", {}, "secret")

    def test_network_error_has_actionable_message_without_key(self):
        with patch.object(app.requests, "get", side_effect=requests.ConnectionError("url?api_key=secret")):
            with self.assertRaises(app.FredDownloadError) as caught:
                app.api_json("series", {}, "secret")
        self.assertIn("Cannot connect", str(caught.exception))
        self.assertNotIn("secret", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
