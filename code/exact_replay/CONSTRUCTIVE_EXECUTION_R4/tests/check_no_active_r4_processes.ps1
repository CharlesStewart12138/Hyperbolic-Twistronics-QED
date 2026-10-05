$ErrorActionPreference = 'Stop'
$patterns = @(
    'scan_candidate_',
    'constructive_execution_r4.*(?:scanner|scan|build_candidate|verify_candidate)',
    'TransitiveGroups',
    'degree.?24.*shard',
    'seed.*shard',
    'gap\.exe'
)
$regex = ($patterns -join '|')
$matches = @(
    Get-CimInstance Win32_Process |
        Where-Object {
            $_.ProcessId -ne $PID -and
            (([string]$_.Name) -match $regex -or ([string]$_.CommandLine) -match $regex)
        } |
        Select-Object ProcessId, Name, CommandLine
)
$payload = [ordered]@{
    schema_version = '1.0'
    classification = if ($matches.Count -eq 0) { 'PASS_NO_ACTIVE_R4_OR_LEGACY_SCAN_PROCESS' } else { 'FAIL_ACTIVE_PROCESS_FOUND' }
    checked_at = (Get-Date).ToString('o')
    active_match_count = $matches.Count
    active_matches = $matches
    note = 'Read-only process inventory; unrelated WSL/EPW workloads are outside scope and were not modified.'
}
$path = Join-Path $PSScriptRoot '..\logs\FINAL_PROCESS_AUDIT.json'
$payload | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $path -Encoding utf8
$payload | ConvertTo-Json -Depth 6
if ($matches.Count -ne 0) { exit 1 }
