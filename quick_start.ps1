# 定义目录结构
$frontendDir = "frontend"
$backendDir = "backend"

# Get current IPv4 address
Write-Host "Getting IP address..." -ForegroundColor Cyan
$ip = Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Ethernet*", "WLAN*", "Wi-Fi*", "Ethernet*" |
      Where-Object { $_.IPAddress -notlike "127.*" -and $_.IPAddress -notlike "169.254.*" } |
      Select-Object -First 1 -ExpandProperty IPAddress

if (-not $ip) {
    Write-Host "Warning: Using localhost" -ForegroundColor Yellow
    $ip = "localhost"
}
Write-Host "Current IP: $ip" -ForegroundColor Green

# Process .env file in frontend directory
$envFile = Join-Path $frontendDir ".env"
if (Test-Path $envFile) {
    $content = Get-Content $envFile
    $found = $false
    for ($i = 0; $i -lt $content.Count; $i++) {
        if ($content[$i] -match '^VITE_API_BASE_URL\s*=') {
            $content[$i] = $content[$i] -replace '(//)[^:/]+', "`${1}$ip"
            $found = $true
            break
        }
    }
    if (-not $found) {
        $content += "VITE_API_BASE_URL=http://${ip}:8000/cooking/ver3"
    }
    Set-Content $envFile $content -Encoding utf8
    Write-Host "✓ Updated .env file" -ForegroundColor Green
} else {
    if (-not (Test-Path $frontendDir)) {
        Write-Host "Error: frontend directory not found!" -ForegroundColor Red
        exit 1
    }
    Set-Content $envFile "VITE_API_BASE_URL=http://${ip}:8000/cooking/ver3" -Encoding utf8
    Write-Host "✓ Created .env file" -ForegroundColor Green
}

# Check environments
Write-Host "Checking npm and Conda..." -ForegroundColor Cyan
if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Host "Error: npm not found!" -ForegroundColor Red
    exit 1
}
if (-not (Get-Command conda -ErrorAction SilentlyContinue)) {
    Write-Host "Error: conda not found!" -ForegroundColor Red
    exit 1
}

# Get Conda base Python path
$condaBase = & conda info --base 2>$null
if (-not $condaBase) {
    Write-Host "Error: Cannot get Conda base path!" -ForegroundColor Red
    exit 1
}
$condaPython = Join-Path $condaBase "python.exe"
if (-not (Test-Path $condaPython)) {
    Write-Host "Error: Conda Python not found at $condaPython" -ForegroundColor Red
    exit 1
}
Write-Host "Found Conda Python: $condaPython" -ForegroundColor Green

# Start backend in BACKGROUND
Write-Host "Starting backend in background..." -ForegroundColor Cyan
$backendMain = Join-Path $backendDir "main.py"
if (-not (Test-Path $backendMain)) {
    Write-Host "Error: backend/main.py not found!" -ForegroundColor Red
    exit 1
}

# 在后台启动后端进程
$backendProcess = Start-Process -FilePath "python" -ArgumentList "-m backend.main -e prod" -WorkingDirectory "D:\python_project\go_cooking_3" -PassThru -WindowStyle Normal

Write-Host "✓ Backend started (PID: $($backendProcess.Id))" -ForegroundColor Green

# Start frontend dev server
Write-Host "Starting frontend dev server..." -ForegroundColor Cyan
Set-Location $frontendDir
npm run dev

# 脚本结束时清理后端进程
Write-Host "Frontend dev server stopped. Stopping backend..." -ForegroundColor Yellow
Stop-Process -Id $backendProcess.Id -Force