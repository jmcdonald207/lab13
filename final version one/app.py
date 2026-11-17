"""Interactive view of the bundled synthetic portfolio demo."""
import streamlit as st

from run import evaluate, report

st.title("Project 2 portfolio screen")
st.caption("Synthetic monthly prices, January 2021 to January 2026")
window = st.selectbox("Estimation window", ("All 60 months", "Last 36 months"))
months = None if window == "All 60 months" else 36
sleeves, _ = evaluate(months)
equity_return = st.number_input("VT expected return (%)",
                                value=round(sleeves[-1]["expected_return"] * 100, 2),
                                step=0.1, key=window)
st.code(report(*evaluate(months, equity_return)), language=None)
