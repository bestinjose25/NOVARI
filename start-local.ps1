$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
New-Item -ItemType Directory -Force "$PSScriptRoot\.local-tools" | Out-Null
$nodeCommand = Get-Command node -ErrorAction SilentlyContinue
if ($nodeCommand) { $nodeExe = $nodeCommand.Source } else {
    $nodeExe = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe'
}
if (-not (Test-Path $nodeExe)) { throw 'Node.js is missing. Install Node.js 24 LTS.' }
$pythonExe = Join-Path $PSScriptRoot 'backend\.venv\Scripts\python.exe'
& $pythonExe backend/manage.py migrate --settings=config.settings_local
if ($LASTEXITCODE -ne 0) { throw 'Database setup failed.' }
Start-Process -FilePath $pythonExe -ArgumentList 'manage.py runserver 127.0.0.1:8001 --settings=config.settings_local --noreload' -WorkingDirectory "$PSScriptRoot\backend" -WindowStyle Hidden -RedirectStandardOutput "$PSScriptRoot\.local-tools\backend.log" -RedirectStandardError "$PSScriptRoot\.local-tools\backend-error.log"
Start-Process -FilePath $nodeExe -ArgumentList 'node_modules/vite/bin/vite.js --host 127.0.0.1 --port 5173 --strictPort' -WorkingDirectory "$PSScriptRoot\frontend" -WindowStyle Hidden -RedirectStandardOutput "$PSScriptRoot\.local-tools\frontend.log" -RedirectStandardError "$PSScriptRoot\.local-tools\frontend-error.log"
Write-Host 'Website: http://127.0.0.1:5173'
Write-Host 'Backend: http://127.0.0.1:8001'
