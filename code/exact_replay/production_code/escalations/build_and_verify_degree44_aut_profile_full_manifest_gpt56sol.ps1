param(
    [string]$BaseDir = ".",
    [string]$ManifestName = "GAP_TRANSITIVE_DEGREE44_AUT_PROFILE_FULL_V3_GPT56SOL_MANIFEST.sha256"
)

$ErrorActionPreference = "Stop"
$files = [System.Collections.Generic.List[string]]::new()

$files.AddRange([string[]]@(
    'gap_transitive_single_degree_order_parity_profile_gpt56sol.g',
    'gap_run_degree44_order_parity_profile_gpt56sol.g',
    'GAP_TRANSITIVE_DEGREE44_ORDER_PARITY_PROFILE_GPT56SOL.txt',
    'GAP_TRANSITIVE_DEGREE44_ORDER_PARITY_PROFILE_RUN_STDOUT_GPT56SOL.txt',
    'GAP_TRANSITIVE_DEGREE44_ORDER_PARITY_PROFILE_RUN_STDERR_GPT56SOL.txt',
    'GAP_TRANSITIVE_DEGREE44_ORDER_PARITY_PROFILE_AGGREGATE_GPT56SOL.txt',
    'GAP_TRANSITIVE_DEGREE44_ORDER_PARITY_PROFILE_GPT56SOL_CERTIFICATE.md',
    'GAP_TRANSITIVE_DEGREE44_ORDER_PARITY_PROFILE_GPT56SOL_MANIFEST.sha256',
    'gap_transitive_single_degree_aut_profile_slice_gpt56sol.g',
    'gap_run_degree44_aut_profile_1_2113_gpt56sol.g',
    'GAP_TRANSITIVE_DEGREE44_AUT_PROFILE_1_2113_EXTERNAL_GUARD_PARTIAL1_GPT56SOL.txt',
    'GAP_TRANSITIVE_DEGREE44_AUT_PROFILE_PARTIAL1_RUN_STDOUT_GPT56SOL.txt',
    'GAP_TRANSITIVE_DEGREE44_AUT_PROFILE_PARTIAL1_RUN_STDERR_GPT56SOL.txt',
    'GAP_TRANSITIVE_DEGREE44_AUT_PROFILE_PARTIAL1_AGGREGATE_GPT56SOL.txt',
    'GAP_TRANSITIVE_DEGREE44_AUT_PROFILE_PARTIAL1_GPT56SOL_CERTIFICATE.md',
    'GAP_TRANSITIVE_DEGREE44_AUT_PROFILE_PARTIAL1_GPT56SOL_MANIFEST.sha256',
    'gap_transitive_single_key_pc_domain_aut_profile_v3_gpt56sol.g'
))

foreach ($key in 273..281) {
    $files.Add("gap_run_degree44_44T${key}_pc_domain_aut_profile_v3_gpt56sol.g")
    $files.Add("GAP_TRANSITIVE_DEGREE44_AUT_PROFILE_44T${key}_PC_DOMAIN_V3_GPT56SOL.txt")
    $files.Add("GAP_TRANSITIVE_DEGREE44_44T${key}_PC_DOMAIN_V3_RUN_STDOUT_GPT56SOL.txt")
    $files.Add("GAP_TRANSITIVE_DEGREE44_44T${key}_PC_DOMAIN_V3_RUN_STDERR_GPT56SOL.txt")
    $files.Add("GAP_TRANSITIVE_DEGREE44_AUT_PROFILE_44T${key}_PC_DOMAIN_V3_AGGREGATE_GPT56SOL.txt")
    $files.Add("GAP_TRANSITIVE_DEGREE44_AUT_PROFILE_44T${key}_PC_DOMAIN_V3_GPT56SOL_CERTIFICATE.md")
    $files.Add("GAP_TRANSITIVE_DEGREE44_AUT_PROFILE_44T${key}_PC_DOMAIN_V3_GPT56SOL_MANIFEST.sha256")
}

$files.AddRange([string[]]@(
    'verify_and_merge_degree44_aut_profile_gpt56sol.ps1',
    'GAP_TRANSITIVE_DEGREE44_AUT_PROFILE_FULL_MERGED_V3_GPT56SOL.txt',
    'GAP_TRANSITIVE_DEGREE44_AUT_PROFILE_FULL_PARTITION_FORECAST_V3_GPT56SOL.tsv',
    'GAP_TRANSITIVE_DEGREE44_AUT_PROFILE_FULL_AGGREGATE_V3_GPT56SOL.txt',
    'GAP_TRANSITIVE_DEGREE44_AUT_PROFILE_FULL_V3_GPT56SOL_CERTIFICATE.md',
    'GAP_TRANSITIVE_DEGREE30_AUT_PROFILE_AGGREGATE_GPT56SOL.txt',
    'GAP_TRANSITIVE_DEGREE30_AUT_FORECAST_GPT56SOL_CERTIFICATE.md',
    'GAP_TRANSITIVE_DEGREE30_AUT_FORECAST_GPT56SOL_MANIFEST.sha256',
    'GAP_TRANSITIVE_DEGREE30_C8_AGGREGATE_GPT56SOL.txt',
    'GAP_TRANSITIVE_DEGREE30_C8_GPT56SOL_CERTIFICATE.md',
    'GAP_TRANSITIVE_DEGREE30_C8_GPT56SOL_MANIFEST.sha256',
    'build_and_verify_degree44_aut_profile_full_manifest_gpt56sol.ps1'
))

if ($files.Count -ne 92) { throw "Unexpected canonical evidence count: $($files.Count)" }
if (($files | Select-Object -Unique).Count -ne $files.Count) { throw "Duplicate manifest filename" }
if (@($files | Where-Object { $_ -match '(?i)invalid|superseded|incomplete' }).Count -ne 0) {
    throw "Invalid/superseded evidence leaked into canonical manifest"
}

$rows = [System.Collections.Generic.List[string]]::new()
foreach ($name in $files) {
    $path = Join-Path $BaseDir $name
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Missing evidence: $name" }
    $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash
    $rows.Add("$hash  $name")
}
$manifestPath = Join-Path $BaseDir $ManifestName
[System.IO.File]::WriteAllLines($manifestPath,$rows,[System.Text.UTF8Encoding]::new($false))

$check = @(Get-Content -LiteralPath $manifestPath)
if ($check.Count -ne 92) { throw "Written manifest count mismatch" }
foreach ($row in $check) {
    if ($row -notmatch '^([0-9A-F]{64})  (.+)$') { throw "Malformed manifest row: $row" }
    $want = $Matches[1]
    $name = $Matches[2]
    $got = (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $BaseDir $name)).Hash
    if ($got -ne $want) { throw "Manifest mismatch: $name" }
}
Write-Output "MANIFEST_PASS entries=92 sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $manifestPath).Hash)"
