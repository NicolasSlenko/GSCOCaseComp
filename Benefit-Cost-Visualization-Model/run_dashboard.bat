@echo off
REM FOVI Enhanced Dashboard - Standalone Version
REM This version runs on localhost:8502 with comprehensive BCR analysis

echo ================================================
echo Florida Olympic Viability Index - Enhanced
echo Comprehensive BCR Analysis Dashboard
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo Python found!
echo.

REM Check if dependencies are installed
echo Checking dependencies...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
    echo Dependencies installed successfully!
) else (
    echo Dependencies already installed.
)

echo.
echo ================================================
echo Starting Enhanced FOVI Dashboard...
echo ================================================
echo.
echo The dashboard will open in your default browser.
echo URL: http://localhost:8502
echo.
echo Press Ctrl+C to stop the server.
echo.

streamlit run fovi_dashboard_enhanced.py --server.port 8502

pause

