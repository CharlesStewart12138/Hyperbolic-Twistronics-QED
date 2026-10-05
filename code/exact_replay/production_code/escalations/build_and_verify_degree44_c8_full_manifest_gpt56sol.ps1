param(
    [string]$BaseDir = ".",
    [string]$ManifestName = "GAP_TRANSITIVE_DEGREE44_C8_FULL_GPT56SOL_MANIFEST.sha256"
)
$ErrorActionPreference = "Stop"
$files = [System.Collections.Generic.List[string]]::new()
$files.Add('gap_transitive_single_degree_range_c8_exhaustive_beta_gpt56sol.g')
$ranges = @(
    [pscustomobject]@{N=1; Tag='1_109'; Wrapper='gap_run_degree44_c8_beta_1_109_gpt56sol.g'},
    [pscustomobject]@{N=2; Tag='110_221'; Wrapper='gap_run_degree44_c8_beta_110_221_gpt56sol.g'},
    [pscustomobject]@{N=3; Tag='222_226'; Wrapper='gap_run_degree44_c8_beta_222_226_gpt56sol.g'},
    [pscustomobject]@{N=4; Tag='227_228'; Wrapper='gap_run_degree44_c8_beta_227_228_gpt56sol.g'}
)
foreach ($r in $ranges) {
    $files.Add($r.Wrapper)
    $files.Add("GAP_TRANSITIVE_DEGREE44_C8_BETA_$($r.Tag)_GPT56SOL.txt")
    $files.Add("GAP_TRANSITIVE_DEGREE44_C8_SHARD$($r.N)_RUN_STDOUT_GPT56SOL.txt")
    $files.Add("GAP_TRANSITIVE_DEGREE44_C8_SHARD$($r.N)_RUN_STDERR_GPT56SOL.txt")
    $files.Add("GAP_TRANSITIVE_DEGREE44_C8_SHARD$($r.N)_AGGREGATE_GPT56SOL.txt")
    $files.Add("GAP_TRANSITIVE_DEGREE44_C8_SHARD$($r.N)_GPT56SOL_CERTIFICATE.md")
    $files.Add("GAP_TRANSITIVE_DEGREE44_C8_SHARD$($r.N)_GPT56SOL_MANIFEST.sha256")
}
$files.AddRange([string[]]@(
    'GAP_TRANSITIVE_DEGREE44_AUT_PROFILE_FULL_MERGED_V3_GPT56SOL.txt',
    'GAP_TRANSITIVE_DEGREE44_AUT_PROFILE_FULL_AGGREGATE_V3_GPT56SOL.txt',
    'GAP_TRANSITIVE_DEGREE44_AUT_PROFILE_FULL_V3_GPT56SOL_CERTIFICATE.md',
    'GAP_TRANSITIVE_DEGREE44_AUT_PROFILE_FULL_V3_GPT56SOL_MANIFEST.sha256',
    'GAP_TRANSITIVE_DEGREE44_AUT_PROFILE_FULL_PARTITION_FORECAST_V3_GPT56SOL.tsv',
    'GAP_TRANSITIVE_DEGREE44_ORDER_PARITY_PROFILE_GPT56SOL.txt',
    'GAP_TRANSITIVE_DEGREE44_ORDER_PARITY_PROFILE_GPT56SOL_MANIFEST.sha256',
    'verify_degree44_c8_full_closure_gpt56sol.ps1',
    'GAP_TRANSITIVE_DEGREE44_C8_FULL_CLOSURE_VERIFY_GPT56SOL.txt',
    'GAP_TRANSITIVE_DEGREE44_C8_FULL_AGGREGATE_GPT56SOL.txt',
    'GAP_TRANSITIVE_DEGREE44_C8_FULL_GPT56SOL_CERTIFICATE.md',
    'build_and_verify_degree44_c8_full_manifest_gpt56sol.ps1'
))
if ($files.Count -ne 41) { throw "Unexpected evidence count $($files.Count)" }
if (($files | Select-Object -Unique).Count -ne 41) { throw 'Duplicate evidence name' }
if (@($files | Where-Object { $_ -match '(?i)invalid|superseded|incomplete' }).Count -ne 0) { throw 'Noncanonical evidence leak' }
$rows = [System.Collections.Generic.List[string]]::new()
foreach ($name in $files) {
    $path = Join-Path $BaseDir $name
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Missing $name" }
    $rows.Add("$((Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash)  $name")
}
$manifest = Join-Path $BaseDir $ManifestName
[System.IO.File]::WriteAllLines($manifest,$rows,[System.Text.UTF8Encoding]::new($false))
$written = @(Get-Content -LiteralPath $manifest)
if ($written.Count -ne 41) { throw 'Written count mismatch' }
foreach ($row in $written) {
    if ($row -notmatch '^([0-9A-F]{64})  (.+)$') { throw "Malformed row $row" }
    $want=$Matches[1]; $name=$Matches[2]
    $got=(Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $BaseDir $name)).Hash
    if ($got -ne $want) { throw "Hash mismatch $name" }
}
Write-Output "MANIFEST_PASS entries=41 sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $manifest).Hash)"
