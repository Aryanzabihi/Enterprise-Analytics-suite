# Inventory Intelligence Dashboard Launcher
# PowerShell Script for Windows

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    Inventory Intelligence Dashboard" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Starting the Inventory Management System..." -ForegroundColor Green
Write-Host ""

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python not found"
    }
} catch {
    Write-Host "❌ ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher and try again" -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Blue
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if pip is available
Write-Host "Checking pip availability..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ pip found: $pipVersion" -ForegroundColor Green
    } else {
        throw "pip not found"
    }
} catch {
    Write-Host "❌ ERROR: pip is not available" -ForegroundColor Red
    Write-Host "Please ensure pip is installed with Python" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if requirements are installed
Write-Host "Checking dependencies..." -ForegroundColor Yellow
try {
    $streamlitCheck = pip show streamlit 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Streamlit is already installed" -ForegroundColor Green
    } else {
        Write-Host "Installing required dependencies..." -ForegroundColor Yellow
        Write-Host "This may take a few minutes..." -ForegroundColor Yellow
        
        $installResult = pip install -r requirements.txt 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
        } else {
            Write-Host "❌ ERROR: Failed to install dependencies" -ForegroundColor Red
            Write-Host "Error details: $installResult" -ForegroundColor Red
            Read-Host "Press Enter to exit"
            exit 1
        }
    }
} catch {
    Write-Host "❌ ERROR: Failed to check/install dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Display startup information
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "           Starting Application" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "The dashboard will open in your default browser" -ForegroundColor Green
Write-Host "at: http://localhost:8501" -ForegroundColor Blue
Write-Host ""
Write-Host "To stop the application, press Ctrl+C in this window" -ForegroundColor Yellow
Write-Host ""
Write-Host "Loading..." -ForegroundColor Green
Write-Host ""

# Run the Streamlit application
try {
    streamlit run invt.py
} catch {
    Write-Host "❌ ERROR: Failed to start Streamlit application" -ForegroundColor Red
    Write-Host "Error details: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Application stopped." -ForegroundColor Yellow
Read-Host "Press Enter to exit"
