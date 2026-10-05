param(
    [string]$PythonExe = "python",
    [switch]$RequireGap
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
$verifier = Join-Path $PSScriptRoot "scripts\verify_environment.py"

& $PythonExe $verifier
if ($LASTEXITCODE -ne 0) {
    throw "Python environment verification failed."
}

$gapCommand = Get-Command gap -ErrorAction SilentlyContinue
if ($null -eq $gapCommand) {
    if ($RequireGap) {
        throw "GAP 4.16.0 is required but no gap executable is available on PATH."
    }
    Write-Output "GAP_STATUS=REQUIRED_NOT_INSTALLED"
    exit 0
}

$gapVersion = & $gapCommand.Source -q -c 'Print(GAPInfo.Version, "\n"); QUIT;'
if ($gapVersion.Trim() -ne "4.16.0") {
    throw "GAP expected 4.16.0, found $($gapVersion.Trim())."
}
Write-Output "GAP_STATUS=PASS VERSION=4.16.0"
