"""Interactive view of the real adjusted-close portfolio model."""
import streamlit as st

from run import evaluate, report

st.title("Project 2 portfolio screen")
st.caption("Yahoo Finance adjusted closes, October 2021 to October 2026")
window = st.selectbox("Estimation window", ("All 60 months", "Last 36 months"))
months = None if window == "All 60 months" else 36
try:
    sleeves, _ = evaluate(months)
except (OSError, ValueError, KeyError, IndexError, TypeError) as error:
    st.error(f"Could not load adjusted closes: {error}")
    st.stop()
equity_return = st.number_input("VT expected return (%)",
                                value=round(sleeves[-1]["expected_return"] * 100, 2),
                                step=0.1, key=window)
st.code(report(*evaluate(months, equity_return)), language=None)
