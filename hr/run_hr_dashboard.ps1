Write-Host "Starting HR Analytics Dashboard..." -ForegroundColor Green
Write-Host ""
Write-Host "This will start the Streamlit HR dashboard in your default browser." -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the dashboard when you're done." -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to continue"
streamlit run hr.py
