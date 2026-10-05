$ErrorActionPreference = 'Stop'
$artifactDir = $PSScriptRoot

$shards = @(
    [pscustomobject]@{ Min = 1;   Max = 620;  Output = 'GAP_TRANSITIVE_DEGREE42_C8_BETA_1_620_V2_GPT56SOL.txt';       Manifest = 'GAP_TRANSITIVE_DEGREE42_C8_SHARD1_GPT56SOL_MANIFEST.sha256' },
    [pscustomobject]@{ Min = 621; Max = 819;  Output = 'GAP_TRANSITIVE_DEGREE42_C8_BETA_621_819_V2_GPT56SOL.txt';     Manifest = 'GAP_TRANSITIVE_DEGREE42_C8_SHARD2_GPT56SOL_MANIFEST.sha256' },
    [pscustomobject]@{ Min = 820; Max = 873;  Output = 'GAP_TRANSITIVE_DEGREE42_C8_BETA_820_873_V2_GPT56SOL.txt';     Manifest = 'GAP_TRANSITIVE_DEGREE42_C8_SHARD3_GPT56SOL_MANIFEST.sha256' },
    [pscustomobject]@{ Min = 874; Max = 9491; Output = 'GAP_TRANSITIVE_DEGREE42_C8_BETA_874_9491_V2_GPT56SOL.txt';   Manifest = 'GAP_TRANSITIVE_DEGREE42_C8_SHARD4_GPT56SOL_MANIFEST.sha256' }
)

$fields = @(
    'ORDER_WINDOW', 'PARITY_ENTRIES', 'ORDER8_CLASSES',
    'INVARIANT_ALPHA_CLASSES', 'BETA_COMPUTATIONS', 'FULL_SEED_PAIRS',
    'INVERSE', 'INVERSE_ODD', 'ORBIT8', 'RELATOR', 'B3', 'GENERATE',
    'PARITY', 'CENTRALIZER_ORBITS'
)
$expected = @{
    ORDER_WINDOW = 714L
    PARITY_ENTRIES = 637L
    ORDER8_CLASSES = 767L
    INVARIANT_ALPHA_CLASSES = 767L
    BETA_COMPUTATIONS = 273L
    FULL_SEED_PAIRS = 11421144L
    INVERSE = 430842L
    INVERSE_ODD = 166335L
    ORBIT8 = 129344L
    RELATOR = 60960L
    B3 = 688L
    GENERATE = 624L
    PARITY = 624L
    CENTRALIZER_ORBITS = 29L
}
$sum = @{}
foreach ($field in $fields) { $sum[$field] = 0L }
$candidateCount = 0

for ($i = 0; $i -lt $shards.Count; ++$i) {
    $shard = $shards[$i]
    if ($i -eq 0) {
        if ($shard.Min -ne 1) { throw 'first shard does not start at 1' }
    } elseif ($shard.Min -ne $shards[$i - 1].Max + 1) {
        throw "gap or overlap before shard $($i + 1)"
    }
    $path = Join-Path $artifactDir $shard.Output
    $lines = @(Get-Content -LiteralPath $path)
    $wantedHeader = @(
        "CERTIFICATE`tPF-GRP-001-C8-TRANSITIVE-DEGREE42-BETA-RANGE",
        "GAP_VERSION`t4.12.1",
        "DEGREE`t42",
        "DATABASE`t9491",
        "RANGE`t$($shard.Min)`t$($shard.Max)"
    )
    if (@(Compare-Object -ReferenceObject $wantedHeader -DifferenceObject @($lines | Select-Object -First 5)).Count -ne 0) {
        throw "header mismatch in $($shard.Output)"
    }
    $totalLines = @($lines | Where-Object { $_ -match '^TOTAL\t' })
    if ($totalLines.Count -ne 1) { throw "TOTAL count mismatch in $($shard.Output)" }
    if (@($lines | Where-Object { $_ -eq 'DONE' }).Count -ne 1 -or $lines[-1] -ne 'DONE') {
        throw "DONE contract mismatch in $($shard.Output)"
    }
    $total = $totalLines[0]
    if ($total -notmatch "`tRANGE`t$($shard.Min)`t$($shard.Max)(`t|$)") {
        throw "TOTAL range mismatch in $($shard.Output)"
    }
    foreach ($field in $fields) {
        $match = [regex]::Match($total, "(?:^|`t)$field`t([0-9]+)(?:`t|$)")
        if (-not $match.Success) { throw "missing $field in $($shard.Output)" }
        $sum[$field] += [int64]$match.Groups[1].Value
    }
    $candidateCount += @($lines | Where-Object { $_ -match '^CANDIDATE_NUMERIC\t' }).Count

    $manifestPath = Join-Path $artifactDir $shard.Manifest
    foreach ($manifestLine in Get-Content -LiteralPath $manifestPath) {
        if ($manifestLine -notmatch '^([0-9A-F]{64})  (.+)$') {
            throw "malformed manifest line in $($shard.Manifest)"
        }
        $expectedHash = $Matches[1]
        $target = [System.IO.Path]::GetFullPath((Join-Path $artifactDir $Matches[2]))
        $actualHash = (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash
        if ($actualHash -ne $expectedHash) { throw "manifest mismatch: $target" }
    }
}
if ($shards[-1].Max -ne 9491) { throw 'final shard does not end at database size' }
foreach ($field in $fields) {
    if ($sum[$field] -ne $expected[$field]) {
        throw "aggregate mismatch $field expected=$($expected[$field]) actual=$($sum[$field])"
    }
}
if ($candidateCount -ne 29 -or $sum.CENTRALIZER_ORBITS -ne 29) {
    throw 'numeric candidate / centralizer-orbit mismatch'
}

$replays = @(
    [pscustomobject]@{ File = 'GAP_TRANSITIVE_DEGREE42_C8_BASED_REPLAY_621_819_RAW_STDOUT_GPT56SOL.txt'; Count = 8 },
    [pscustomobject]@{ File = 'GAP_TRANSITIVE_DEGREE42_C8_BASED_REPLAY_874_9491_RAW_STDOUT_GPT56SOL.txt'; Count = 21 }
)
$replayed = 0
foreach ($replay in $replays) {
    $lines = @(Get-Content -LiteralPath (Join-Path $artifactDir $replay.File))
    if ($lines[0] -ne "candidates=$($replay.Count)") { throw "candidate count mismatch in $($replay.File)" }
    $results = @($lines | Where-Object { $_ -match '^42T' })
    if ($results.Count -ne $replay.Count) { throw "result count mismatch in $($replay.File)" }
    if (@($results | Where-Object { $_ -notmatch 'distinct=8 inverse=1 relator=1 b3=457 generated=1 parity=1 BASED_FAIL .* depth=8 ' }).Count -ne 0) {
        throw "gate or witness mismatch in $($replay.File)"
    }
    if (@($lines | Where-Object { $_ -match 'BASED_PASS' }).Count -ne 0) {
        throw "based survivor in $($replay.File)"
    }
    $replayed += $results.Count
}
if ($replayed -ne 29) { throw 'replay total mismatch' }

"PASS degree42 ranges=1-9491 shards=4 manifests=4"
"PASS window=$($sum.ORDER_WINDOW) parity_entries=$($sum.PARITY_ENTRIES) classes=$($sum.ORDER8_CLASSES) raw=$($sum.FULL_SEED_PAIRS)"
"PASS inverse=$($sum.INVERSE) inverse_odd=$($sum.INVERSE_ODD) orbit8=$($sum.ORBIT8) relator=$($sum.RELATOR) b3=$($sum.B3) generated=$($sum.GENERATE)"
"PASS centralizer_orbits=$($sum.CENTRALIZER_ORBITS) replayed=$replayed based_survivors=0"
