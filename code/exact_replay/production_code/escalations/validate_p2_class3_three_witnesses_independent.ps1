param(
    [Parameter(Mandatory=$true)][string]$TransitionPath,
    [Parameter(Mandatory=$true)][string]$ClassifierPath,
    [Parameter(Mandatory=$true)][string]$TreePath,
    [Parameter(Mandatory=$true)][string]$RegistryPath,
    [Parameter(Mandatory=$true)][string]$OutputPath
)

$ErrorActionPreference = 'Stop'

function Convert-Bits([string]$bits) {
    if ($bits.Length -ne 25 -or $bits -notmatch '^[01]+$') { throw "invalid 25-bit mask: $bits" }
    [uint32]$value = 0
    for ($i = 0; $i -lt 25; $i++) {
        if ($bits[$i] -eq '1') { $value = $value -bor ([uint32]1 -shl $i) }
    }
    return $value
}

function Get-Parity([uint32]$value) {
    $p = 0
    while ($value -ne 0) { $p = $p -bxor 1; $value = $value -band ($value - 1) }
    return $p
}

$witnessSpecs = @(
    [pscustomobject]@{ Id = 908441; CanonicalId = 'B00908441'; Word = @(0,0,1,4,1,1,4,1) },
    [pscustomobject]@{ Id = 911401; CanonicalId = 'B00911401'; Word = @(0,0,2,5,0,0,1,6) },
    [pscustomobject]@{ Id = 912073; CanonicalId = 'B00912073'; Word = @(0,0,2,5,4,4,1,6) }
)

$table = @{}
$transitionRows = 0
$b3Rows = 0
$b3States = [System.Collections.Generic.List[object]]::new()
Get-Content -LiteralPath $TransitionPath | ForEach-Object {
    if ($_.StartsWith("TRANS`t")) {
        $f = $_ -split "`t"
        if ($f.Count -ne 5) { throw "malformed TRANS row" }
        $key = "$($f[1]),$($f[2])"
        if ($table.ContainsKey($key)) { throw "duplicate TRANS key $key" }
        $table[$key] = @([int]$f[3], (Convert-Bits $f[4]))
        $transitionRows++
    } elseif ($_.StartsWith("B3STATE`t")) {
        $f = $_ -split "`t"
        if ($f.Count -ne 6) { throw "malformed B3STATE row" }
        $b3States.Add([pscustomobject]@{ Base = [int]$f[4]; Layer = (Convert-Bits $f[5]) })
        $b3Rows++
    }
}
if ($transitionRows -ne 65536) { throw "expected 65536 transitions, got $transitionRows" }
if ($b3Rows -ne 457) { throw "expected 457 B3 states, got $b3Rows" }

$witnessStates = @{}
foreach ($spec in $witnessSpecs) {
    $u = 0
    [uint32]$layer = 0
    foreach ($g in $spec.Word) {
        $key = "$u,$g"
        if (-not $table.ContainsKey($key)) { throw "missing transition $key" }
        $entry = $table[$key]
        $u = [int]$entry[0]
        $layer = $layer -bxor [uint32]$entry[1]
    }
    if ($u -ne 0) { throw "witness $($spec.Id) does not return to U2 identity: $u" }
    $witnessStates[$spec.Id] = [pscustomobject]@{ Base = $u; Layer = $layer }
}

$planes = [System.Collections.Generic.HashSet[string]]::new()
$candidateCount = 0
$j11 = 0
$j2 = 0
$unrejected = 0
$b3Failures = 0
$witnessHistogram = @{ 908441 = 0; 911401 = 0; 912073 = 0 }
Get-Content -LiteralPath $ClassifierPath | ForEach-Object {
    if ($_.StartsWith("B3_SURVIVOR`t")) {
        $f = $_ -split "`t"
        if ($f.Count -lt 13 -or $f[1] -ne 'DIM' -or $f[2] -ne '2' -or $f[5] -ne 'ORDER' -or $f[6] -ne '32768') {
            throw "malformed B3 survivor row"
        }
        $type = $f[4]
        if ($type -eq 'J1+J1') { $j11++ } elseif ($type -eq 'J2') { $j2++ } else { throw "unexpected type $type" }
        [uint32]$f1 = Convert-Bits $f[8]
        [uint32]$f2 = Convert-Bits $f[10]
        if ($f1 -eq 0 -or $f2 -eq 0 -or $f1 -eq $f2) { throw "dependent quotient functionals" }
        $basis = @($f1,$f2,($f1 -bxor $f2)) | Sort-Object
        if (-not $planes.Add(($basis -join ':'))) { throw "duplicate quotient plane" }
        $b3Images = [System.Collections.Generic.HashSet[string]]::new()
        foreach ($state in $b3States) {
            [void]$b3Images.Add("$($state.Base),$(Get-Parity ($state.Layer -band $f1)),$(Get-Parity ($state.Layer -band $f2))")
        }
        if ($b3Images.Count -ne 457) { $b3Failures++ }
        $rejector = $null
        foreach ($spec in $witnessSpecs) {
            $state = $witnessStates[$spec.Id]
            if ((Get-Parity ($state.Layer -band $f1)) -eq 0 -and (Get-Parity ($state.Layer -band $f2)) -eq 0) {
                $rejector = $spec.Id
                break
            }
        }
        if ($null -eq $rejector) { $unrejected++ } else { $witnessHistogram[$rejector]++ }
        $candidateCount++
    }
}
if ($candidateCount -ne 512 -or $planes.Count -ne 512 -or $j11 -ne 256 -or $j2 -ne 256) {
    throw "survivor census mismatch: total=$candidateCount unique=$($planes.Count) J1+J1=$j11 J2=$j2"
}
if ($b3Failures -ne 0) { throw "$b3Failures survivors fail independent B3=457 reconstruction" }
if ($unrejected -ne 0) { throw "$unrejected survivors are not rejected by the three frozen witnesses" }
if ($witnessHistogram[908441] -ne 192 -or $witnessHistogram[911401] -ne 128 -or $witnessHistogram[912073] -ne 192) {
    throw "witness histogram mismatch: 908441=$($witnessHistogram[908441]) 911401=$($witnessHistogram[911401]) 912073=$($witnessHistogram[912073])"
}

$target = 912073
$stream = [System.IO.File]::OpenRead($TreePath)
try {
    $reader = [System.IO.BinaryReader]::new($stream)
    $magic = [Text.Encoding]::ASCII.GetString($reader.ReadBytes(8))
    $count = $reader.ReadUInt64()
    $width = $reader.ReadUInt32()
    if ($magic -ne 'BOLZAT01' -or $count -ne 23129593 -or $width -ne 8) { throw "tree header mismatch" }
    $parents = [uint32[]]::new($target + 1)
    $generators = [byte[]]::new($target + 1)
    $depths = [byte[]]::new($target + 1)
    [byte]$previousDepth = 0
    for ($i = 0; $i -le $target; $i++) {
        $parents[$i] = $reader.ReadUInt32()
        $generators[$i] = $reader.ReadByte()
        $depths[$i] = $reader.ReadByte()
        [void]$reader.ReadUInt16()
        if ($i -eq 0) {
            if ($parents[$i] -ne 0 -or $depths[$i] -ne 0) { throw "invalid root" }
        } else {
            if ($parents[$i] -ge $i -or $generators[$i] -ge 8 -or $depths[$i] -ne ($depths[$parents[$i]] + 1) -or $depths[$i] -lt $previousDepth) {
                throw "invalid BFS prefix at record $i"
            }
        }
        $previousDepth = $depths[$i]
    }
} finally { $stream.Dispose() }

foreach ($spec in $witnessSpecs) {
    $recovered = [System.Collections.Generic.List[int]]::new()
    $node = $spec.Id
    while ($node -ne 0) { $recovered.Add([int]$generators[$node]); $node = $parents[$node] }
    $recovered.Reverse()
    if (($recovered -join ',') -ne ($spec.Word -join ',') -or $depths[$spec.Id] -ne 8) { throw "tree word mismatch at $($spec.Id)" }
}

$registryHeader = Get-Content -LiteralPath $RegistryPath -TotalCount 1
$geometry = @{}
foreach ($spec in $witnessSpecs) {
    $registryLine = Select-String -LiteralPath $RegistryPath -Pattern "^$($spec.CanonicalId)," | Select-Object -First 1 -ExpandProperty Line
    if (-not $registryLine) { throw "missing $($spec.CanonicalId) registry row" }
    $row = @($registryHeader, $registryLine) | ConvertFrom-Csv | Select-Object -First 1
    $expectedWord = $spec.Word | ForEach-Object { 'g' + $_ } | Join-String -Separator ' '
    if ($row.s8_geometric_reduced_word -ne $expectedWord -or [int]$row.geometric_word_length -ne 8) { throw "registry word/depth mismatch at $($spec.Id)" }
    $translation = [double]::Parse($row.translation_length_over_a_B, [Globalization.CultureInfo]::InvariantCulture)
    if (-not ($translation -lt 6.0)) { throw "witness $($spec.Id) does not violate >6a_B" }
    $geometry[$spec.Id] = $row
}

$lines = @(
    "CERTIFICATE`tPF-GRP-001-BOLZA-P2-PCLASS3-THREE-WITNESS-INDEPENDENT-REPLAY",
    "METHOD`tindependent PowerShell parser; three-word replay, all-survivor B3 reconstruction, quotient-plane canonicalization, frozen BFS-prefix audit, geometric-registry cross-check",
    "TRANSITION_ROWS`t$transitionRows",
    "B3STATE_ROWS`t$b3Rows",
    "SURVIVORS`t$candidateCount",
    "UNIQUE_QUOTIENT_PLANES`t$($planes.Count)",
    "TYPE_J1_PLUS_J1`t$j11",
    "TYPE_J2`t$j2",
    "B3_RECONSTRUCTION_FAILURES`t$b3Failures",
    "UNREJECTED_SURVIVORS`t$unrejected",
    "WITNESS_908441_COUNT`t$($witnessHistogram[908441])",
    "WITNESS_908441_WORD`t$($witnessSpecs[0].Word | ForEach-Object { 'g' + $_ } | Join-String -Separator ' ')",
    "WITNESS_908441_HALF_TRACE_EXACT`t1425+1008*sqrt(2)",
    "WITNESS_908441_TRANSLATION_LENGTH_OVER_A_B`t$($geometry[908441].translation_length_over_a_B)",
    "WITNESS_911401_COUNT`t$($witnessHistogram[911401])",
    "WITNESS_911401_WORD`t$($witnessSpecs[1].Word | ForEach-Object { 'g' + $_ } | Join-String -Separator ' ')",
    "WITNESS_911401_ABS_HALF_TRACE_EXACT`t927+656*sqrt(2)",
    "WITNESS_911401_TRANSLATION_LENGTH_OVER_A_B`t$($geometry[911401].translation_length_over_a_B)",
    "WITNESS_912073_COUNT`t$($witnessHistogram[912073])",
    "WITNESS_912073_WORD`t$($witnessSpecs[2].Word | ForEach-Object { 'g' + $_ } | Join-String -Separator ' ')",
    "WITNESS_912073_HALF_TRACE_EXACT`t1041+736*sqrt(2)",
    "WITNESS_912073_TRANSLATION_LENGTH_OVER_A_B`t$($geometry[912073].translation_length_over_a_B)",
    "ALL_WITNESSES_VIOLATE_GLOBAL_SYSTOLE_GT_6A_B`ttrue",
    "RESULT`tPASS",
    "DONE"
)
[System.IO.File]::WriteAllLines($OutputPath, $lines, [Text.UTF8Encoding]::new($false))
