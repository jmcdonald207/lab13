# Windows launcher: starts five independent Streamlit servers and tiles five Edge app windows.
# From the repository root:
# powershell -ExecutionPolicy Bypass -File .\open_all_side_by_side.ps1
param([switch]$InstallDependencies)

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
$python = (Get-Command python -ErrorAction Stop).Source

$apps = @(
    @{ Name = "Project 2 Portfolio Screen"; Folder = "final version one"; Script = "app.py"; Port = 8513 },
    @{ Name = "Meridian Portfolio Explorer"; Folder = "lab15"; Script = "app.py"; Port = 8515 },
    @{ Name = "Point-in-Time Rates"; Folder = "lab 17"; Script = "asof_app.py"; Port = 8517 },
    @{ Name = "Buffett Business Notebook"; Folder = "lab 18"; Script = "app.py"; Port = 8518 },
    @{ Name = "Same Facts, Different Investors"; Folder = "lab 19"; Script = "app.py"; Port = 8519 }
)

if ($InstallDependencies) {
    Write-Host "Installing each app's declared dependencies..."
    foreach ($app in $apps) {
        $file = Join-Path (Join-Path $root $app.Folder) "requirements.txt"
        & $python -m pip install -r $file
        if ($LASTEXITCODE -ne 0) { throw "Dependency installation failed: $file" }
    }
}

function Test-LocalPort([int]$Port) {
    $client = New-Object System.Net.Sockets.TcpClient
    try {
        $async = $client.BeginConnect("127.0.0.1", $Port, $null, $null)
        if (-not $async.AsyncWaitHandle.WaitOne(300)) { return $false }
        try { $client.EndConnect($async); return $true } catch { return $false }
    } finally { $client.Close() }
}

foreach ($app in $apps) {
    $folder = Join-Path $root $app.Folder
    if (-not (Test-LocalPort $app.Port)) {
        Write-Host ("Starting {0} on port {1}..." -f $app.Name, $app.Port)
        $args = @("-m", "streamlit", "run", $app.Script, "--server.address", "127.0.0.1",
                  "--server.port", [string]$app.Port, "--server.headless", "true",
                  "--browser.gatherUsageStats", "false")
        Start-Process -FilePath $python -ArgumentList $args -WorkingDirectory $folder | Out-Null
    } else {
        Write-Host ("Port {0} is already in use; opening that address without starting a duplicate server." -f $app.Port)
    }
}

$edgeCandidates = @(
    "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
    "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe",
    "$env:LOCALAPPDATA\Microsoft\Edge\Application\msedge.exe"
)
$edge = $edgeCandidates | Where-Object { $_ -and (Test-Path $_) } | Select-Object -First 1

if (-not $edge) {
    Write-Warning "Microsoft Edge was not found. Opening each page in your default browser; tile windows manually with Windows Snap."
    foreach ($app in $apps) {
        Start-Process ("http://127.0.0.1:{0}" -f $app.Port)
    }
    exit
}

Add-Type -AssemblyName System.Windows.Forms
$area = [System.Windows.Forms.Screen]::PrimaryScreen.WorkingArea
$cols = 3
$rows = 2
$gap = 6
$width = [math]::Floor(($area.Width - ($cols - 1) * $gap) / $cols)
$height = [math]::Floor(($area.Height - ($rows - 1) * $gap) / $rows)

Write-Host "Opening five separate Edge windows in a 3-column, 2-row layout..."
for ($i = 0; $i -lt $apps.Count; $i++) {
    $app = $apps[$i]
    $col = $i % $cols
    $row = [math]::Floor($i / $cols)
    $x = $area.Left + $col * ($width + $gap)
    $y = $area.Top + $row * ($height + $gap)
    $url = "http://127.0.0.1:$($app.Port)"
    # One dedicated browser profile per site ensures distinct, positionable Edge windows.
    $profile = Join-Path $env:TEMP "lab13-tiled-edge-$($app.Port)"
    $edgeArgs = @(
        "--user-data-dir=`"$profile`"",
        "--app=$url",
        "--window-position=$x,$y",
        "--window-size=$width,$height",
        "--no-first-run"
    )
    Start-Process -FilePath $edge -ArgumentList $edgeArgs | Out-Null
}
Write-Host "Five sites requested. Startup may take a few moments; windows are independently scrollable."
Write-Host "FRED live data still needs FRED_API_KEY; SEC downloads require a proper User-Agent."
