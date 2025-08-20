# R&D Analytics Dashboard Launcher
Write-Host "Starting R&D Analytics Dashboard..." -ForegroundColor Green
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Yellow
} catch {
    Write-Host "Error: Python not found. Please ensure Python is installed and in your PATH." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if required packages are installed
Write-Host "Checking required packages..." -ForegroundColor Yellow
try {
    python -c "import streamlit, pandas, plotly" 2>$null
    Write-Host "Required packages found!" -ForegroundColor Green
} catch {
    Write-Host "Installing required packages..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

Write-Host ""
Write-Host "Launching R&D Dashboard..." -ForegroundColor Green
Write-Host "Dashboard will open in your default browser at: http://localhost:8502" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the dashboard" -ForegroundColor Yellow
Write-Host ""

# Launch the dashboard
streamlit run rd.py --server.port 8502 --server.headless true
