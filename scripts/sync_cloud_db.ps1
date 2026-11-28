param(
    [string]$OracleIp = "130.61.107.25",
    [string]$SshUser = "ubuntu",
    [string]$KeyPath = "$HOME\.ssh\oracle_career_os.key"
)

$ErrorActionPreference = "Stop"
$BaseDir = Split-Path -Parent $PSScriptRoot
$CloudDb = Join-Path $BaseDir "oracle_cloud\data\career_os_cloud.db"

Write-Host "1/3 Exportiere datenschutzbereinigtes Cloud Knowledge Pack..." -ForegroundColor Cyan
python (Join-Path $PSScriptRoot "export_cloud_knowledge_pack.py")
if ($LASTEXITCODE -ne 0) { throw "Cloud Knowledge Pack Export fehlgeschlagen" }

Write-Host "2/3 Lade career_os_cloud.db nach ${SshUser}@${OracleIp}:/opt/career-os/data/..." -ForegroundColor Cyan
scp -i $KeyPath $CloudDb "${SshUser}@${OracleIp}:/opt/career-os/data/career_os_cloud.db"
if ($LASTEXITCODE -ne 0) { throw "SCP-Upload fehlgeschlagen" }

Write-Host "3/3 Verifiziere Live-Healthcheck..." -ForegroundColor Cyan
$health = Invoke-RestMethod -Uri "https://${OracleIp}.sslip.io/health" -TimeoutSec 10
if (-not $health.ok) { throw "Healthcheck fehlgeschlagen" }
Write-Host ("✅ Cloud DB synchronisiert! Timestamp: " + $health.timestamp) -ForegroundColor Green
