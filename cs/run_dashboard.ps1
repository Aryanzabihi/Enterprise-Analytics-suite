# Customer Service Dashboard Launcher (PowerShell)
# This script launches the refactored Customer Service Dashboard

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Customer Service Dashboard Launcher" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "cs_main.py")) {
    Write-Host "❌ Error: cs_main.py not found in current directory!" -ForegroundColor Red
    Write-Host "Please make sure you're running this script from the 'cs' folder." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Current directory: $(Get-Location)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Expected files:" -ForegroundColor Gray
    Get-ChildItem -Name "*.py" | ForEach-Object { Write-Host "  - $_" -ForegroundColor Gray }
    Write-Host ""
    pause
    exit 1
}

# Check if streamlit is available
try {
    $streamlitVersion = streamlit --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Streamlit found: $streamlitVersion" -ForegroundColor Green
    } else {
        throw "Streamlit not accessible"
    }
} catch {
    Write-Host "❌ Error: Streamlit not found or not accessible!" -ForegroundColor Red
    Write-Host "Please install streamlit: pip install streamlit" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit 1
}

Write-Host ""
Write-Host "🚀 Launching the refactored dashboard..." -ForegroundColor Green
Write-Host "Note: This runs cs_main.py (the new modular version)" -ForegroundColor Yellow
Write-Host "      NOT cs.py (the old monolithic version)" -ForegroundColor Yellow
Write-Host ""

# Launch the dashboard
try {
    streamlit run cs_main.py
} catch {
    Write-Host "❌ Error launching dashboard: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "1. Make sure all dependencies are installed: pip install -r requirements.txt" -ForegroundColor Gray
    Write-Host "2. Check if the test script runs: python test_refactored.py" -ForegroundColor Gray
    Write-Host "3. Verify you're in the correct directory" -ForegroundColor Gray
    Write-Host ""
    pause
}
