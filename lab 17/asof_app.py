"""Compare current FRED observations with a documented historical information set.

Run: streamlit run asof_app.py
Set FRED_API_KEY in the environment or Streamlit secrets.
"""
from datetime import date, datetime, timezone
from io import StringIO
import os
import re

import numpy as np
import pandas as pd
import requests
import streamlit as st

SERIES = {
    "BAA": "Moody's Baa corporate bond yield",
    "FEDFUNDS": "Federal funds rate",
    "DGS10": "10-year Treasury yield",
    "MORTGAGE30US": "30-year mortgage rate",
}
API = "https://api.stlouisfed.org/fred"


class FredDownloadError(ValueError):
    """A user-facing download error that never includes credential-bearing URLs."""


def get_api_key():
    key = os.environ.get("FRED_API_KEY", "").strip()
    if not key:
        try:
            key = st.secrets.get("FRED_API_KEY", "").strip()
        except (FileNotFoundError, st.errors.StreamlitSecretNotFoundError):
            pass
    return key


def validate_id(series_id):
    series_id = series_id.strip().upper()
    if not re.fullmatch(r"[A-Z0-9_]+", series_id):
        raise ValueError("Use a FRED series ID containing letters, digits or underscores.")
    return series_id


def clean_values(dates, values):
    dates = pd.to_datetime(dates, errors="raise")
    values = pd.to_numeric(values, errors="raise")
    if pd.isna(dates).any():
        raise ValueError("Download has missing observation dates.")
    if np.isinf(np.asarray(values, dtype=float)).any():
        raise ValueError("Download has infinite observation values.")
    result = pd.Series(np.asarray(values, dtype=float), index=pd.DatetimeIndex(dates), name="value")
    if result.index.has_duplicates:
        raise ValueError("Download has duplicate observation dates.")
    return result.dropna().sort_index()


def parse_csv(text, expected_id=None):
    frame = pd.read_csv(StringIO(text), na_values=["."])
    if len(frame.columns) != 2:
        raise ValueError("Expected a date column and one series column.")
    if expected_id and frame.columns[1] != validate_id(expected_id):
        raise ValueError("Download returned an unexpected series column.")
    return clean_values(frame.iloc[:, 0], frame.iloc[:, 1])


def api_json(endpoint, params, api_key):
    try:
        response = requests.get(f"{API}/{endpoint}",
                                params={**params, "api_key": api_key.strip(), "file_type": "json"}, timeout=30)
    except requests.Timeout:
        raise FredDownloadError("FRED timed out. Try Refresh downloads shortly.") from None
    except requests.ConnectionError:
        raise FredDownloadError(
            "Cannot connect to api.stlouisfed.org. Check your network or firewall. "
            "If this app was launched by the assistant, stop it and run "
            "python -m streamlit run asof_app.py --browser.gatherUsageStats false "
            "from your own terminal; the assistant's session blocks outbound downloads."
        ) from None
    except requests.RequestException:
        raise FredDownloadError("FRED network request failed. Check your connection and retry.") from None
    # Do not expose response.url or requests exception messages: they contain the API key.
    if not response.ok:
        hints = {400: "Check your API key, series ID and requested date.",
                 401: "Check your FRED API key.", 403: "FRED denied access. Check your API key and network.",
                 429: "FRED's request limit was reached. Wait before refreshing."}
        raise FredDownloadError(f"FRED request failed (HTTP {response.status_code}). "
                                + hints.get(response.status_code, "Try again later."))
    payload = response.json()
    if "error_message" in payload:
            raise FredDownloadError("FRED rejected the request. Check your API key and series ID.")
    return payload


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_metadata(series_id, download_day, _api_key):
    payload = api_json("series", {"series_id": validate_id(series_id)}, _api_key)
    items = payload.get("seriess", [])
    if len(items) != 1 or items[0].get("id") != series_id:
        raise ValueError("Unexpected series metadata response.")
    return items[0]


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_snapshot(series_id, vintage_date, download_day, _api_key):
    series_id = validate_id(series_id)
    cutoff = date.fromisoformat(vintage_date)
    if cutoff > date.today():
        raise ValueError("An as-known date cannot be in the future.")
    params = {"series_id": series_id, "realtime_start": cutoff.isoformat(),
              "realtime_end": cutoff.isoformat(), "observation_end": cutoff.isoformat(),
              "limit": 100000, "offset": 0}
    observations = []
    while True:
        payload = api_json("series/observations", params, _api_key)
        if (payload.get("realtime_start") != cutoff.isoformat()
                or payload.get("realtime_end") != cutoff.isoformat()):
            raise ValueError("FRED returned a different real-time period than requested.")
        page = payload.get("observations")
        if not isinstance(page, list):
            raise ValueError("Missing observations in FRED response.")
        observations.extend(page)
        count = int(payload["count"])
        if len(observations) >= count:
            break
        if not page:
            raise ValueError("Incomplete paginated FRED response.")
        params["offset"] = len(observations)
    values = clean_values([row["date"] for row in observations],
                          [np.nan if row["value"] == "." else row["value"] for row in observations])
    if (values.index > pd.Timestamp(cutoff)).any():
        raise ValueError("FRED returned observations beyond the requested cutoff.")
    public_params = {k: v for k, v in params.items() if k != "offset"}
    url = requests.Request("GET", f"{API}/series/observations", params=public_params).prepare().url
    return {"values": values, "url": url,
            "downloaded_utc": datetime.now(timezone.utc).isoformat(),
            "requested_cutoff": cutoff.isoformat()}


def compare(current, known):
    last = known.index[-1] if not known.empty else None
    common = pd.concat([known.rename("then"), current.rename("today")], axis=1, join="inner").dropna()
    revised = ~np.isclose(common["then"], common["today"], rtol=0, atol=1e-9)
    added = current.index.difference(known.index)
    later = added[added > last] if last is not None else added
    older_added = added[added <= last] if last is not None else added[:0]
    removed = known.index.difference(current.index)
    differences = pd.concat([known.rename("then"), current.rename("today")], axis=1, sort=True)
    differences["Change"] = "Unchanged"
    differences.loc[common.index[revised], "Change"] = "Revised"
    differences.loc[later, "Change"] = "Later observation" if last is not None else "Current only; no historical baseline"
    differences.loc[older_added, "Change"] = "Older observation added"
    differences.loc[removed, "Change"] = "Absent from current"
    return {
        "Last measured date known then": last,
        "Value known then": float(known.iloc[-1]) if not known.empty else None,
        "Last measured date today": current.index[-1] if not current.empty else None,
        "Value today": float(current.iloc[-1]) if not current.empty else None,
        "Later observations": len(later) if last is not None else 0,
        "Current-only dates without historical baseline": len(added) if last is None else 0,
        "Older observations added": len(older_added),
        "Historical dates absent today": len(removed),
        "Shared dates": len(common), "Revised shared dates": int(revised.sum()),
    }, differences.loc[differences["Change"] != "Unchanged"]


def main():
    st.set_page_config(page_title="Point-in-Time Rates", layout="wide")
    today = date.today()
    st.title("Point-in-Time Rates")
    st.caption("FRED and ALFRED, Federal Reserve Bank of St. Louis. Built with AI help; a learning demonstration, not investment advice.")
    api_key = get_api_key()
    if not api_key:
        st.info("Set FRED_API_KEY in your environment or Streamlit secrets, then restart the app. Get a key at https://fred.stlouisfed.org/docs/api/api_key.html")
        return
    selected = st.sidebar.multiselect("Series", list(SERIES), default=list(SERIES))
    extra = st.sidebar.text_input("Add a FRED series ID", placeholder="PAYEMS")
    if extra.strip():
        try:
            extra = validate_id(extra)
            if extra not in selected:
                selected.append(extra)
        except ValueError as error:
            st.sidebar.error(str(error))
    start = st.sidebar.date_input("Chart start date", date(2020, 1, 1))
    cutoff = st.sidebar.date_input("As known on", today, max_value=today)
    if st.sidebar.button("Refresh downloads"):
        fetch_snapshot.clear()
        fetch_metadata.clear()
    st.info("Observation dates label the period measured, not publication time. Counts cover full histories; chart start changes charts only. Date-level vintages cannot establish availability before an intraday trade. Metadata shown is current. API downloads can be cached for up to one hour.")
    rows = []
    for series_id in selected:
        st.subheader(series_id)
        row = {"Series ID": series_id, "Series": f"https://fred.stlouisfed.org/series/{series_id}",
               "Requested cutoff": cutoff.isoformat(), "Current snapshot date": today.isoformat()}
        try:
            metadata = fetch_metadata(series_id, today.isoformat(), api_key)
            st.caption(f"{metadata['title']} · {metadata['units']} · {metadata['frequency']} · {metadata['seasonal_adjustment']}")
            current = fetch_snapshot(series_id, today.isoformat(), today.isoformat(), api_key)
            known = fetch_snapshot(series_id, cutoff.isoformat(), today.isoformat(), api_key)
            summary, differences = compare(current["values"], known["values"])
            plotted = pd.concat([current["values"].rename("Today"), known["values"].rename(f"Known on {cutoff}")], axis=1).loc[pd.Timestamp(start):]
            if plotted.empty:
                st.warning("No observations at or after the chart start date.")
            else:
                st.line_chart(plotted)
            status = "OK"
            if current["values"].empty:
                status = "No current observations"
            elif known["values"].empty:
                status = "No historical observations available"
            elif not summary["Shared dates"]:
                status = "No shared observation dates"
            st.write(f"Comparison status: {status}")
            last = summary["Last measured date known then"]
            st.write(f"Last measured date known on {cutoff}: {last.date() if last is not None else 'None'}")
            st.caption(f"Current download: {current['downloaded_utc']} · Vintage download: {known['downloaded_utc']}")
            row.update({"Status": status, "Title": metadata["title"], "Units": metadata["units"],
                        "Frequency": metadata["frequency"], "Seasonal adjustment": metadata["seasonal_adjustment"],
                        "Current downloaded UTC": current["downloaded_utc"],
                        "Vintage downloaded UTC": known["downloaded_utc"],
                        "Current source URL": current["url"], "Vintage source URL": known["url"], **summary})
            with st.expander("Source requests and changed observations"):
                st.caption("Source URLs omit credentials; add your API key to reproduce requests.")
                st.write(current["url"], known["url"])
                st.dataframe(differences, width="stretch")
                st.download_button("Download differences CSV", differences.to_csv(index_label="Observation date"),
                                   file_name=f"{series_id}_{cutoff}_differences.csv", key=series_id)
        except FredDownloadError as error:
            row["Status"] = str(error)
            st.error(f"{series_id}: {row['Status']}")
        except requests.RequestException:
            row["Status"] = "Network request failed; retry the download."
            st.error(f"{series_id}: {row['Status']}")
        except (ValueError, KeyError, TypeError) as error:
            row["Status"] = f"Invalid data or request ({type(error).__name__})"
            st.error(f"{series_id}: {row['Status']}")
        rows.append(row)
    if rows:
        table = pd.DataFrame(rows)
        st.subheader("As-of audit")
        st.dataframe(table, hide_index=True, width="stretch",
                     column_config={"Series": st.column_config.LinkColumn("Series", display_text=r"/series/(.*)$")})
        st.download_button("Download audit table", table.to_csv(index=False), "asof_audit.csv")


if __name__ == "__main__":
    main()
