@echo off
cd /d "%~dp0"
python -m streamlit run asof_app.py --server.port 8501 --browser.gatherUsageStats false
pause
