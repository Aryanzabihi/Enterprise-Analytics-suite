@echo off
echo ========================================
echo    Inventory Intelligence Dashboard
echo ========================================
echo.
echo Starting the Inventory Management System...
echo.
echo Please wait while the application loads...
echo.
echo The dashboard will open in your default browser
echo at: http://localhost:8501
echo.
echo To stop the application, press Ctrl+C in this window
echo.
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher and try again
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo Installing required dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Run the Streamlit application
echo Starting Streamlit application...
streamlit run invt.py

pause
