# Setup Verification Script
# Run this after completing setup to verify everything is configured correctly

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Chemical Equipment Parameter Visualizer" -ForegroundColor Cyan
Write-Host "Setup Verification Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$allGood = $true

# Check Python
Write-Host "Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python not found" -ForegroundColor Red
    $allGood = $false
}

# Check Node.js
Write-Host "Checking Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "  ✓ Node.js $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Node.js not found" -ForegroundColor Red
    $allGood = $false
}

# Check npm
Write-Host "Checking npm..." -ForegroundColor Yellow
try {
    $npmVersion = npm --version 2>&1
    Write-Host "  ✓ npm $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ npm not found" -ForegroundColor Red
    $allGood = $false
}

Write-Host ""
Write-Host "Checking Project Structure..." -ForegroundColor Yellow

# Check backend
if (Test-Path "backend/manage.py") {
    Write-Host "  ✓ Backend directory exists" -ForegroundColor Green
    
    if (Test-Path "backend/requirements.txt") {
        Write-Host "  ✓ Backend requirements.txt found" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Backend requirements.txt missing" -ForegroundColor Red
        $allGood = $false
    }
    
    if (Test-Path "backend/sample_data.csv") {
        Write-Host "  ✓ Sample data found" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Sample data missing" -ForegroundColor Red
        $allGood = $false
    }
} else {
    Write-Host "  ✗ Backend directory missing" -ForegroundColor Red
    $allGood = $false
}

# Check web frontend
if (Test-Path "web-frontend/package.json") {
    Write-Host "  ✓ Web frontend directory exists" -ForegroundColor Green
    
    if (Test-Path "web-frontend/src/App.js") {
        Write-Host "  ✓ Web frontend source files found" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Web frontend source files missing" -ForegroundColor Red
        $allGood = $false
    }
} else {
    Write-Host "  ✗ Web frontend directory missing" -ForegroundColor Red
    $allGood = $false
}

# Check desktop frontend
if (Test-Path "desktop-frontend/main.py") {
    Write-Host "  ✓ Desktop frontend exists" -ForegroundColor Green
    
    if (Test-Path "desktop-frontend/requirements.txt") {
        Write-Host "  ✓ Desktop requirements.txt found" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Desktop requirements.txt missing" -ForegroundColor Red
        $allGood = $false
    }
} else {
    Write-Host "  ✗ Desktop frontend missing" -ForegroundColor Red
    $allGood = $false
}

Write-Host ""
Write-Host "Checking Documentation..." -ForegroundColor Yellow

$docs = @("README.md", "QUICKSTART.md", "ARCHITECTURE.md", "PROJECT_SUMMARY.md")
foreach ($doc in $docs) {
    if (Test-Path $doc) {
        Write-Host "  ✓ $doc found" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $doc missing" -ForegroundColor Red
        $allGood = $false
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

if ($allGood) {
    Write-Host "✓ All checks passed!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next Steps:" -ForegroundColor Cyan
    Write-Host "1. Setup backend: cd backend && python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt" -ForegroundColor White
    Write-Host "2. Run migrations: python manage.py migrate" -ForegroundColor White
    Write-Host "3. Create superuser: python manage.py createsuperuser" -ForegroundColor White
    Write-Host "4. Start backend: python manage.py runserver" -ForegroundColor White
    Write-Host ""
    Write-Host "5. Setup web frontend: cd web-frontend && npm install" -ForegroundColor White
    Write-Host "6. Start web frontend: npm start" -ForegroundColor White
    Write-Host ""
    Write-Host "7. Setup desktop: cd desktop-frontend && pip install -r requirements.txt" -ForegroundColor White
    Write-Host "8. Run desktop: python main.py" -ForegroundColor White
    Write-Host ""
    Write-Host "See QUICKSTART.md for detailed instructions!" -ForegroundColor Cyan
} else {
    Write-Host "✗ Some checks failed. Please review the errors above." -ForegroundColor Red
    Write-Host "Make sure you're in the project root directory." -ForegroundColor Yellow
}

Write-Host "========================================" -ForegroundColor Cyan
