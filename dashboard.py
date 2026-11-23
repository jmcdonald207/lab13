"""One Streamlit entry point for the five existing lab applications.

Run from the repository root:
    python -m pip install -r requirements.txt
    python -m streamlit run dashboard.py --server.port 8513

Each lab remains a separate source of truth. Local imports are isolated because
several labs have modules with identical names (portfolio.py, edgar.py).
"""
from pathlib import Path
import runpy
import sys

import streamlit as st

ROOT = Path(__file__).resolve().parent
LOCAL_MODULES = ("portfolio", "prices", "run", "edgar", "panel", "audit")


def run_lab(relative_path):
    script = ROOT / relative_path
    folder = str(script.parent)
    original_path = list(sys.path)
    previous = {name: sys.modules.pop(name, None) for name in LOCAL_MODULES}
    sys.path.insert(0, folder)
    try:
        runpy.run_path(str(script), run_name="__main__")
    finally:
        # Avoid a portfolio/edgar module from one lab leaking into another.
        for name in LOCAL_MODULES:
            sys.modules.pop(name, None)
            if previous[name] is not None:
                sys.modules[name] = previous[name]
        sys.path[:] = original_path


PAGES = [
    ("Project 2 Portfolio Screen", "final version one/app.py"),
    ("Meridian Portfolio Explorer", "lab15/app.py"),
    ("Point-in-Time Rates", "lab 17/asof_app.py"),
    ("Buffett Business Notebook", "lab 18/app.py"),
    ("Same Facts, Different Investors", "lab 19/app.py"),
]


def make_page(path):
    def page():
        run_lab(path)
    return page


navigation = st.navigation(
    [st.Page(make_page(path), title=title, default=(index == 0))
     for index, (title, path) in enumerate(PAGES)],
    position="sidebar",
)
navigation.run()
