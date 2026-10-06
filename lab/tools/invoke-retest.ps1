[CmdletBinding()]
param(
    [ValidatePattern('^[0-9A-Za-z._-]+$')]
    [string]$RunId = (Get-Date -Format 'yyyyMMdd-HHmmss')
)

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$runDir = Join-Path $repoRoot "evidence\retest\$RunId"
$composeFiles = @(
    '-f', (Join-Path $repoRoot 'lab\compose\compose.yaml'),
    '-f', (Join-Path $repoRoot 'lab\compose\compose.verify.yaml')
)

if (Test-Path -LiteralPath $runDir) {
    throw "Run directory already exists: $runDir"
}
New-Item -ItemType Directory -Path $runDir | Out-Null

function Save-CommandOutput {
    param(
        [Parameter(Mandatory)] [string]$Name,
        [Parameter(Mandatory)] [scriptblock]$Command,
        [int[]]$AllowedExitCodes = @(0)
    )

    $path = Join-Path $runDir $Name
    $global:LASTEXITCODE = 0
    & $Command 2>&1 | Out-File -LiteralPath $path -Encoding utf8
    $exitCode = $LASTEXITCODE
    if ($exitCode -notin $AllowedExitCodes) {
        throw "$Name failed with exit code $exitCode. See $path"
    }
    return $exitCode
}

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw 'Docker CLI is not available in PATH.'
}

Push-Location $repoRoot
try {
    [ordered]@{
        os_version = [Environment]::OSVersion.VersionString
        os_architecture = [System.Runtime.InteropServices.RuntimeInformation]::OSArchitecture.ToString()
        powershell_version = $PSVersionTable.PSVersion.ToString()
        timezone = [TimeZoneInfo]::Local.Id
    } | ConvertTo-Json | Out-File (Join-Path $runDir 'host-environment.json') -Encoding utf8
    Save-CommandOutput 'git-commit.txt' { git rev-parse HEAD }
    Save-CommandOutput 'docker-version.txt' { docker version }
    Save-CommandOutput 'compose-version.txt' { docker compose version }
    Save-CommandOutput 'effective-compose.yaml' {
        docker compose @composeFiles --profile verify --profile capture config
    }
    Save-CommandOutput 'services.txt' { docker compose @composeFiles ps }

    $plcId = docker compose @composeFiles ps -q openplc
    $hmiId = docker compose @composeFiles ps -q fuxa
    if (-not $plcId -or -not $hmiId) {
        throw 'Running openplc and fuxa containers are required.'
    }

    $plcNetworksJson = docker inspect --format '{{json .NetworkSettings.Networks}}' $plcId
    $hmiNetworksJson = docker inspect --format '{{json .NetworkSettings.Networks}}' $hmiId
    $plcNetworksJson | Out-File (Join-Path $runDir 'plc-networks.json') -Encoding utf8
    $hmiNetworksJson | Out-File (Join-Path $runDir 'hmi-networks.json') -Encoding utf8

    $plcNetworks = $plcNetworksJson | ConvertFrom-Json
    $controlProperty = $plcNetworks.PSObject.Properties |
        Where-Object { $_.Name -match '(^|_)control$' } |
        Select-Object -First 1
    if (-not $controlProperty -or -not $controlProperty.Value.IPAddress) {
        throw 'Could not identify the PLC address on the control network.'
    }
    $plcIp = $controlProperty.Value.IPAddress

    $plcImage = docker inspect --format '{{.Image}}' $plcId
    $hmiImage = docker inspect --format '{{.Image}}' $hmiId
    $plcImage | Out-File (Join-Path $runDir 'plc-image-id.txt') -Encoding utf8
    $hmiImage | Out-File (Join-Path $runDir 'hmi-image-id.txt') -Encoding utf8
    docker image inspect --format '{{json .RepoDigests}}' $plcImage |
        Out-File (Join-Path $runDir 'plc-digests.json') -Encoding utf8
    docker image inspect --format '{{json .RepoDigests}}' $hmiImage |
        Out-File (Join-Path $runDir 'hmi-digests.json') -Encoding utf8

    Save-CommandOutput 'trusted-read-before.txt' {
        docker compose @composeFiles run --rm --no-deps baseline-probe
    }
    $dnsExit = Save-CommandOutput 'isolated-dns.json' {
        docker compose @composeFiles run --rm --no-deps isolated-tcp-check
    } -AllowedExitCodes @(2)
    $isolatedExit = Save-CommandOutput 'isolated-ip.json' {
        docker compose @composeFiles run --rm --no-deps isolated-tcp-check `
            python /tools/tcp_boundary_check.py --host $plcIp
    } -AllowedExitCodes @(3)
    $trustedExit = Save-CommandOutput 'trusted-ip.json' {
        docker compose @composeFiles run --rm --no-deps trusted-tcp-check `
            python /tools/tcp_boundary_check.py --host $plcIp
    }

    $verdict = [ordered]@{
        run_id = $RunId
        generated_at = (Get-Date).ToString('o')
        plc_control_ip = $plcIp
        isolated_dns_exit = $dnsExit
        isolated_ip_exit = $isolatedExit
        trusted_ip_exit = $trustedExit
        boundary_result = if ($isolatedExit -eq 3 -and $trustedExit -eq 0) { 'PASS' } else { 'FAIL' }
        scope = 'TCP reachability only; no Modbus payload was sent by the boundary checks.'
    }
    $verdict | ConvertTo-Json | Out-File (Join-Path $runDir 'boundary-verdict.json') -Encoding utf8

    Get-FileHash -Algorithm SHA256 -LiteralPath @(
        (Join-Path $repoRoot 'lab\tools\invoke-retest.ps1'),
        (Join-Path $repoRoot 'lab\tools\tcp_boundary_check.py'),
        (Join-Path $repoRoot 'lab\tools\modbus_probe.py'),
        (Join-Path $repoRoot 'lab\compose\compose.yaml'),
        (Join-Path $repoRoot 'lab\compose\compose.verify.yaml')
    ) | Select-Object Path, Hash |
        Export-Csv (Join-Path $runDir 'input-file-hashes.csv') -NoTypeInformation -Encoding utf8

    Get-ChildItem -LiteralPath $runDir -File |
        Get-FileHash -Algorithm SHA256 |
        Select-Object Path, Hash |
        Export-Csv (Join-Path $runDir 'hashes.csv') -NoTypeInformation -Encoding utf8

    Write-Host "Boundary evidence saved to: $runDir"
    Write-Host 'Next: capture the allowed HMI path by following docs/retest-runbook.md section 4.'
}
finally {
    Pop-Location
}
