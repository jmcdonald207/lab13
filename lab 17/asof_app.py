"""Lab 17: compare current FRED data with a genuine ALFRED vintage."""
from datetime import date, datetime, timezone
from io import StringIO
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


def validate_id(series_id):
    series_id = series_id.strip().upper()
    if not re.fullmatch(r"[A-Z0-9_]+", series_id):
        raise ValueError("Use a FRED series ID containing letters, digits or underscores.")
    return series_id


def parse_csv(text):
    frame = pd.read_csv(StringIO(text), na_values=["."])
    if len(frame.columns) != 2:
        raise ValueError("Expected a date column and one series column, not an error page.")
    dates = pd.to_datetime(frame.iloc[:, 0], errors="raise")
    values = pd.to_numeric(frame.iloc[:, 1], errors="raise")
    result = pd.Series(values.to_numpy(), index=pd.DatetimeIndex(dates), name="value")
    result = result.dropna().sort_index()
    if result.index.has_duplicates:
        raise ValueError("Download has duplicate observation dates.")
    return result


def download(url, params):
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return {
        "values": parse_csv(response.text),
        "url": response.url,
        "downloaded_utc": datetime.now(timezone.utc).isoformat(),
    }


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_today(series_id, download_day):
    """One current CSV request per series per cache entry; day prevents stale overnight data."""
    return download("https://fred.stlouisfed.org/graph/fredgraph.csv",
                    {"id": validate_id(series_id)})


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_asof(series_id, vintage_date, download_day):
    """Ask ALFRED for the vintage, rather than truncating today's revised history."""
    series_id = validate_id(series_id)
    cutoff = date.fromisoformat(vintage_date)
    if cutoff > date.today():
        raise ValueError("An as-known date cannot be in the future.")
    snapshot = download("https://alfred.stlouisfed.org/graph/alfredgraph.csv",
                        {"id": series_id, "vintage_date": cutoff.isoformat()})
    # Observation date is an extra sanity gate, not a substitute for vintage_date.
    snapshot["values"] = snapshot["values"].loc[:pd.Timestamp(cutoff)]
    return snapshot


def compare(current, known):
    """Counts use the full downloaded histories, independent of the chart start."""
    last_known = known.index[-1] if not known.empty else None
    common = pd.concat([known.rename("then"), current.rename("today")], axis=1,
                       join="inner").dropna()
    revised = ~np.isclose(common["then"], common["today"], rtol=0, atol=1e-9)
    return {
        "Last measured date known then": last_known,
        "Value known then": float(known.iloc[-1]) if not known.empty else None,
        "Last measured date today": current.index[-1] if not current.empty else None,
        "Value today": float(current.iloc[-1]) if not current.empty else None,
        "Later observations": int((current.index > last_known).sum()) if last_known is not None else len(current),
        "Revised shared dates": int(revised.sum()),
    }, common.loc[revised]


def main():
    st.set_page_config(page_title="Point-in-Time Rates", layout="wide")
    today = date.today()
    st.title("Point-in-Time Rates")
    st.caption(f"Data from FRED and ALFRED, Federal Reserve Bank of St. Louis; downloads requested today ({today}). Built with AI help; a learning demonstration, not investment advice.")
    selected = st.sidebar.multiselect("Series", list(SERIES), default=list(SERIES),
                                     format_func=lambda x: f"{x} — {SERIES[x]}")
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
        fetch_today.clear()
        fetch_asof.clear()
    st.info("Observation dates label the period measured, not publication time. ALFRED supplies the historical vintage. Counts cover full histories; the start date changes charts only. A date-level vintage cannot establish availability before a particular intraday trade.")
    rows = []
    for series_id in selected:
        st.subheader(f"{series_id} — {SERIES.get(series_id, 'Additional FRED series')}")
        try:
            current = fetch_today(series_id, today.isoformat())
            known = fetch_asof(series_id, cutoff.isoformat(), today.isoformat())
            summary, revisions = compare(current["values"], known["values"])
            plotted = current["values"].loc[pd.Timestamp(start):]
            if plotted.empty:
                st.warning("No current observations at or after the chart start date.")
            else:
                st.line_chart(plotted.rename(series_id))
            last = summary["Last measured date known then"]
            st.write(f"Last measured date known on {cutoff}: {last.date() if last is not None else 'No observations available'}")
            st.caption(f"Current download: {current['downloaded_utc']} · Vintage download: {known['downloaded_utc']}")
            rows.append({"Series": f"https://fred.stlouisfed.org/series/{series_id}",
                         "Status": "OK", **summary})
            with st.expander("Source downloads and revised observations"):
                st.markdown(f"[Current CSV]({current['url']}) · [Vintage CSV]({known['url']})")
                st.dataframe(revisions, use_container_width=True)
                st.download_button("Download revisions CSV", revisions.to_csv(),
                                   file_name=f"{series_id}_{cutoff}_revisions.csv", key=series_id)
        except (requests.RequestException, ValueError, pd.errors.ParserError) as error:
            st.error(f"{series_id}: {type(error).__name__}: {error}")
            rows.append({"Series": f"https://fred.stlouisfed.org/series/{series_id}", "Status": str(error)})
    if rows:
        table = pd.DataFrame(rows)
        st.subheader("As-of audit")
        st.dataframe(table, hide_index=True, use_container_width=True,
                     column_config={"Series": st.column_config.LinkColumn("Series", display_text=r"/series/(.*)$")})
        st.download_button("Download audit table", table.to_csv(index=False), "asof_audit.csv")


if __name__ == "__main__":
    main()
