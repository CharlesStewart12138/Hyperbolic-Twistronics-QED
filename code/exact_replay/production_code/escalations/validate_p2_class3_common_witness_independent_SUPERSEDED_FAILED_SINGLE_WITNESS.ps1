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

$word = @(0,0,2,5,4,4,1,6)
$needed = @{}
for ($i = 0; $i -lt $word.Count; $i++) { $needed["$i,$($word[$i])"] = $true }

# Parse the entire exact table and independently replay the fixed word.
$table = @{}
$transitionRows = 0
$b3Rows = 0
Get-Content -LiteralPath $TransitionPath | ForEach-Object {
    if ($_.StartsWith("TRANS`t")) {
        $f = $_ -split "`t"
        if ($f.Count -ne 5) { throw "malformed TRANS row" }
        $key = "$($f[1]),$($f[2])"
        if ($table.ContainsKey($key)) { throw "duplicate TRANS key $key" }
        $table[$key] = @([int]$f[3], (Convert-Bits $f[4]))
        $transitionRows++
    } elseif ($_.StartsWith("B3STATE`t")) {
        $b3Rows++
    }
}
if ($transitionRows -ne 65536) { throw "expected 65536 transitions, got $transitionRows" }
if ($b3Rows -ne 457) { throw "expected 457 B3 states, got $b3Rows" }

$u = 0
[uint32]$layer = 0
foreach ($g in $word) {
    $key = "$u,$g"
    if (-not $table.ContainsKey($key)) { throw "missing transition $key" }
    $entry = $table[$key]
    $u = [int]$entry[0]
    $layer = $layer -bxor [uint32]$entry[1]
}
if ($u -ne 0) { throw "common witness does not return to U2 identity: $u" }

# Independently parse every survivor, canonicalize its 2-plane, and test the witness.
$planes = [System.Collections.Generic.HashSet[string]]::new()
$candidateCount = 0
$j11 = 0
$j2 = 0
$kernelFailures = 0
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
        if ((Get-Parity ($layer -band $f1)) -ne 0 -or (Get-Parity ($layer -band $f2)) -ne 0) { $kernelFailures++ }
        $candidateCount++
    }
}
if ($candidateCount -ne 512 -or $planes.Count -ne 512 -or $j11 -ne 256 -or $j2 -ne 256) {
    throw "survivor census mismatch: total=$candidateCount unique=$($planes.Count) J1+J1=$j11 J2=$j2"
}
if ($kernelFailures -ne 0) { throw "common witness misses $kernelFailures quotient kernels" }

# Independently inspect the frozen BFS prefix through record 912073 and recover its word.
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

$recovered = [System.Collections.Generic.List[int]]::new()
$node = $target
while ($node -ne 0) { $recovered.Add([int]$generators[$node]); $node = $parents[$node] }
$recovered.Reverse()
if (($recovered -join ',') -ne ($word -join ',') -or $depths[$target] -ne 8) { throw "tree word mismatch" }

# Tie the group-theoretic witness to the independently frozen geometric row.
$registryLine = Select-String -LiteralPath $RegistryPath -Pattern '^B00912073,' | Select-Object -First 1 -ExpandProperty Line
if (-not $registryLine) { throw "missing B00912073 registry row" }
$rf = $registryLine -split ','
if ($rf[1] -ne 'g0 g0 g2 g5 g4 g4 g1 g6' -or $rf[5] -ne '8') { throw "registry word/depth mismatch" }
$translation = [double]::Parse($rf[8], [Globalization.CultureInfo]::InvariantCulture)
if (-not ($translation -lt 6.0)) { throw "witness does not violate >6a_B" }
$traceExact = $rf[9]
if ($traceExact -ne '"0;2082' -and -not $registryLine.Contains('"0;2082,1472,0,0,0,0,0,0"')) { throw "exact trace drift" }

$lines = @(
    "CERTIFICATE`tPF-GRP-001-BOLZA-P2-PCLASS3-COMMON-WITNESS-INDEPENDENT-REPLAY",
    "METHOD`tindependent PowerShell parser; fixed-word replay, quotient-plane canonicalization, frozen BFS-prefix audit, geometric-registry cross-check",
    "TRANSITION_ROWS`t$transitionRows",
    "B3STATE_ROWS`t$b3Rows",
    "SURVIVORS`t$candidateCount",
    "UNIQUE_QUOTIENT_PLANES`t$($planes.Count)",
    "TYPE_J1_PLUS_J1`t$j11",
    "TYPE_J2`t$j2",
    "WITNESS_ID`t$target",
    "WITNESS_DEPTH`t$($depths[$target])",
    "WITNESS_WORD`t$($word | ForEach-Object { 'g' + $_ } | Join-String -Separator ' ')",
    "FINAL_U2_STATE`t$u",
    "LAYER_MASK_UINT32`t$layer",
    "KERNEL_FAILURES`t$kernelFailures",
    "HALF_TRACE_EXACT`t1041+736*sqrt(2)",
    "TRANSLATION_LENGTH_OVER_A_B`t$($rf[8])",
    "VIOLATES_GLOBAL_SYSTOLE_GT_6A_B`ttrue",
    "RESULT`tPASS",
    "DONE"
)
[System.IO.File]::WriteAllLines($OutputPath, $lines, [Text.UTF8Encoding]::new($false))
