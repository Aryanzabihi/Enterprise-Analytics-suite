@echo off
echo Starting R&D Analytics Dashboard...
echo.
echo Please wait while Streamlit loads...
echo.
streamlit run rd.py --server.port 8502 --server.headless true
pause
