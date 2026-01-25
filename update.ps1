
# One-click Update & Deploy Script

# 1. Setup Environment
$env:Path = "$PSScriptRoot\nodejs;" + $env:Path

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   CREW DASHBOARD - UPDATE & DEPLOY" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# 2. Update Data (Python)
Write-Host "Step 1: Updating Data from CSV files..." -ForegroundColor Yellow
python update_data.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error updating data. Deployment stopped." -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "Step 2: Deploying to Cloudflare..." -ForegroundColor Yellow

# 3. Deploy (Wrangler)
# Using --commit-dirty=true to bypass git check since we are just updating data
npx wrangler pages deploy deploy_static --project-name crew-dashboard --branch main --commit-dirty=true

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ SUCCESS! Dashboard updated." -ForegroundColor Green
    Write-Host "👉 Live URL: https://crew-dashboard.pages.dev" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "❌ Deployment failed." -ForegroundColor Red
}
Write-Host ""
Pause
