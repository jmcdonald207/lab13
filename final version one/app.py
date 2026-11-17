#web browser verion runs at  http://localhost:8501#
"""Run with: python -m streamlit run app.py"""
from copy import deepcopy
from io import BytesIO
import hashlib

import streamlit as st

from portfolio import (SLEEVES, CORRELATIONS, OBJECTIVE_RETURN,
                       estimate_from_csv, search_portfolio)


st.set_page_config(page_title="Meridian portfolio explorer", layout="wide")
st.title("Meridian portfolio explorer")
st.caption("Built with AI help, a learning demonstration, not investment advice.")

objective = st.sidebar.number_input("Expected-return objective (%)", value=OBJECTIVE_RETURN * 100, step=0.1) / 100
reserve_minimum = st.sidebar.number_input("Reserve minimum (%)", min_value=0.0, max_value=100.0, value=3.0, step=1.0) / 100
upload = st.sidebar.file_uploader("Upload prices.csv", type=["csv"])
last_36 = st.sidebar.checkbox("Use only the last 36 months", value=False)

try:
    if upload is None:
        loaded_sleeves, loaded_correlations = deepcopy(SLEEVES), deepcopy(CORRELATIONS)
        current_sleeves, current_correlations = deepcopy(SLEEVES), deepcopy(CORRELATIONS)
        source_key = "meridian"
        st.write("Loaded inputs: Meridian training assumptions.")
    else:
        data = upload.getvalue()
        source_key = hashlib.sha256(data).hexdigest()
        loaded_sleeves, loaded_correlations = estimate_from_csv(BytesIO(data))
        current_sleeves, current_correlations = estimate_from_csv(BytesIO(data), last_36)
        st.write("Loaded inputs: CSV, all months. Current inputs: " +
                 ("up to the last 36 monthly returns." if last_36 else "all months."))

    st.subheader("Current assumptions")
    eligible = []
    for index, sleeve in enumerate(current_sleeves):
        left, right = st.columns(2)
        with left:
            sleeve['expected_return'] = st.number_input(
                f"{sleeve['name']} expected return (%)",
                value=sleeve['expected_return'] * 100, step=0.1,
                key=f"return_{source_key}_{last_36}_{index}") / 100
        with right:
            eligible.append(st.checkbox(
                f"{sleeve['name']} reserve-eligible",
                value=upload is None and index in (0, 1),
                key=f"reserve_{source_key}_{index}"))

    current = search_portfolio(current_sleeves, current_correlations, objective,
                               reserve_minimum, eligible)
    baseline = search_portfolio(loaded_sleeves, loaded_correlations, objective,
                                reserve_minimum, eligible)

    def show_result(result, sleeves):
        if result is None:
            st.write("no mix meets the objective")
            return
        st.table([{"Asset": sleeve['name'], "Weight": f"{weight:.2%}"}
                  for sleeve, weight in zip(sleeves, result['weights'])])
        st.metric("Expected return", f"{result['expected_return']:.2%}")
        st.metric("Volatility", f"{result['volatility']:.2%}")
        st.metric("Reserve-eligible weight", f"{result['reserve_eligible_weight']:.2%}")

    left, right = st.columns(2)
    with left:
        st.subheader("Lowest-risk mix: current inputs")
        show_result(current, current_sleeves)
    with right:
        st.subheader("Lowest-risk mix: inputs as loaded")
        show_result(baseline, loaded_sleeves)
    st.caption("Both answers use the sidebar objective, reserve minimum, and selected reserve eligibility. The loaded answer retains the original expected returns and all CSV months.")
    if current is not None and baseline is not None:
        changes = [abs(a - b) for a, b in zip(current['weights'], baseline['weights'])]
        largest = max(range(len(changes)), key=changes.__getitem__)
        st.metric("Largest weight change (percentage points)",
                  f"{changes[largest] * 100:.2f}",
                  help=f"Largest change: {current_sleeves[largest]['name']}")
    else:
        st.write("Largest weight change: unavailable because a comparison mix is missing.")
except (ValueError, TypeError, KeyError, OverflowError) as error:
    st.error(f"Input error: {error}")
