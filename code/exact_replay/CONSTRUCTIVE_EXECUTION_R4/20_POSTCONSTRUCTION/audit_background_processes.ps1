$ErrorActionPreference = 'Stop'
$all = @(Get-CimInstance Win32_Process)
$selfId = $PID
$r4Pattern = 'scan_candidate_|CONSTRUCTIVE_EXECUTION_R4.*(?:global.*scan|build_candidate|verify_candidate|replay_mu|MinimalFaithful|enumerate_sl2_9)'
$legacyPattern = 'TransitiveGroups|degree.?24.*shard|seed.*shard|legacy.*enumerat|old.*degree.*scan'
$r4 = @($all | Where-Object { $_.ProcessId -ne $selfId -and ([string]$_.CommandLine) -match $r4Pattern } | Select-Object ProcessId,Name,CommandLine)
$legacy = @($all | Where-Object { $_.ProcessId -ne $selfId -and ([string]$_.CommandLine) -match $legacyPattern } | Select-Object ProcessId,Name,CommandLine)
$gap = @($all | Where-Object { $_.ProcessId -ne $selfId -and ([string]$_.Name) -match '^gap(?:\.exe)?$' } | Select-Object ProcessId,Name,CommandLine)
$payload = [ordered]@{
    schema_version = '1.0'
    classification = if ($r4.Count -eq 0 -and $legacy.Count -eq 0 -and $gap.Count -eq 0) { 'PASS_NO_BACKGROUND_PROJECT_COMPUTE' } else { 'FAIL_BACKGROUND_PROJECT_COMPUTE_FOUND' }
    audited_at = (Get-Date).ToString('o')
    background_R4_process_count = $r4.Count
    background_legacy_enumeration_process_count = $legacy.Count
    background_GAP_process_count = $gap.Count
    R4_processes = $r4
    legacy_processes = $legacy
    GAP_processes = $gap
    note = 'EPW/WSL and unrelated user workloads are outside this audit and were not modified.'
}
$out = Join-Path $PSScriptRoot 'POSTCONSTRUCTION_PROCESS_AUDIT.json'
$payload | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $out -Encoding utf8
$payload | ConvertTo-Json -Depth 8
if ($payload.classification -ne 'PASS_NO_BACKGROUND_PROJECT_COMPUTE') { exit 1 }
