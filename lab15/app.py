"""Run: python -m streamlit run app.py"""
import copy
import hashlib
import io
import importlib

import pandas as pd
import streamlit as st
import portfolio

# Reload on each Streamlit rerun so edits to the engine's inputs take effect.
engine = importlib.reload(portfolio)
st.set_page_config(page_title="Lowest-risk mix", layout="wide")
st.title("Which mix carries the least risk?")
st.caption("Built with AI help, a learning demonstration, not investment advice.")
objective = st.sidebar.number_input("Expected-return objective (%)", value=6.5, step=0.1)
reserve_min = st.sidebar.number_input("Reserve minimum (%)", 0.0, 100.0, 3.0, step=1.0)
upload = st.sidebar.file_uploader("Monthly adjusted-close prices.csv", type=["csv"])
last_36 = st.sidebar.checkbox("Use only the last 36 monthly returns", disabled=upload is None)
st.sidebar.caption("Three to six tickers; date first, oldest month first. Record sources and download dates in your notes.")
try:
    if upload is None:
        baseline_sleeves = copy.deepcopy(engine.SLEEVES)
        baseline_corr = copy.deepcopy(engine.CORRELATIONS)
        current_sleeves, current_corr = copy.deepcopy(baseline_sleeves), baseline_corr
        identity = "Meridian-" + repr(baseline_sleeves)
        st.caption("Meridian: course-authored annual estimates.")
    else:
        data = upload.getvalue()
        identity = hashlib.sha256(data).hexdigest() + str(last_36)
        baseline_sleeves, baseline_corr = engine.estimate_from_csv(io.BytesIO(data))
        current_sleeves, current_corr = engine.estimate_from_csv(io.BytesIO(data), last_36)
        st.caption("Returns are historical arithmetic estimates, not forecasts. Monthly mean × 12; sample standard deviation × √12.")
        prices = pd.read_csv(io.BytesIO(data))
        st.caption(f"{len(prices)} price rows; {len(prices) - 1} monthly returns available. Current window: {'last 36 returns' if last_36 else 'all returns'}.")
        if len(prices) < 60:
            st.warning("Fewer than five years of monthly price observations. Complete the required data history before checkout.")
    st.subheader("Edit annual expected-return estimates")
    eligibility = []
    for i, sleeve in enumerate(current_sleeves):
        left, right = st.columns([3, 2])
        sleeve["expected_return"] = left.number_input(
            sleeve["name"] + " return (%)", value=sleeve["expected_return"] * 100,
            step=0.1, format="%.2f", key=f"return-{identity}-{i}") / 100
        eligibility.append(right.checkbox(
            sleeve["name"] + " is reserve-eligible",
            value=upload is None and i < 2, key=f"reserve-{identity}-{i}"))
    baseline = engine.search(baseline_sleeves, baseline_corr, objective / 100, eligibility, reserve_min / 100)
    current = engine.search(current_sleeves, current_corr, objective / 100, eligibility, reserve_min / 100)

    def show_result(column, title, result):
        with column:
            st.subheader(title)
            if result is None:
                st.info("no mix meets the objective")
                return
            st.dataframe(pd.DataFrame({
                "Asset": [s["name"] for s in current_sleeves],
                "Weight (%)": [f"{w * 100:.2f}" for w in result["weights"]],
            }), hide_index=True, use_container_width=True)
            st.metric("Expected return", f'{result["expected_return"]:.2%}')
            st.metric("Annual volatility", f'{result["volatility"]:.2%}')
            st.metric("Reserve-eligible weight", f'{result["reserve_weight"]:.2%}')

    a, b = st.columns(2)
    show_result(a, "Current inputs", current)
    show_result(b, "As loaded (all months for CSV)", baseline)
    st.caption("Both answers use the objective, reserve minimum and eligibility selected above. Search uses fully invested, long-only weights in 5-point steps.")
    if current is not None and baseline is not None:
        change = max(abs(x - y) for x, y in zip(current["weights"], baseline["weights"])) * 100
        st.metric("Largest weight change", f"{change:.2f} percentage points")
    else:
        st.write("Largest weight change unavailable: both runs must have a feasible mix.")
except (ValueError, TypeError, KeyError, pd.errors.ParserError) as error:
    st.error(str(error))
