param(
    [string]$BaseDir = ".",
    [string]$MergedProfile = "GAP_TRANSITIVE_DEGREE44_AUT_PROFILE_FULL_MERGED_V3_GPT56SOL.txt",
    [string]$PartitionArtifact = "GAP_TRANSITIVE_DEGREE44_AUT_PROFILE_FULL_PARTITION_FORECAST_V3_GPT56SOL.tsv"
)

$ErrorActionPreference = "Stop"

function Assert-Equal($Actual, $Expected, [string]$Label) {
    if ($Actual -ne $Expected) {
        throw "$Label mismatch: actual=$Actual expected=$Expected"
    }
}

function Sum-Property($Items, [string]$Property) {
    $value = ($Items | Measure-Object -Property $Property -Sum).Sum
    if ($null -eq $value) { return [int64]0 }
    return [int64]$value
}

function Parse-LegacyEntry([string]$Line) {
    $f = $Line -split "`t"
    if ($f.Count -ne 16 -or $f[1] -notmatch '^44T([0-9]+)$') {
        throw "Malformed legacy ENTRY: $Line"
    }
    if ($f[2] -ne 'ORDER' -or $f[4] -ne 'AUT_ORDER' -or
        $f[6] -ne 'AUT_MS' -or $f[8] -ne 'METHOD' -or
        $f[10] -ne 'CLASS_MS' -or $f[12] -ne 'ORDER8_CLASSES' -or
        $f[14] -ne 'RAW_PAIRS') {
        throw "Legacy ENTRY field-label mismatch: $Line"
    }
    [pscustomobject]@{
        K       = [int]$Matches[1]
        Order   = [int64]$f[3]
        AutOrder= [int64]$f[5]
        IsoMs   = [int64]0
        AutMs   = [int64]$f[7]
        Method  = $f[9]
        ClassMs = [int64]$f[11]
        Classes = [int64]$f[13]
        Raw     = [int64]$f[15]
        Source  = 'PARTIAL1_NATIVE_DOMAIN'
    }
}

function Parse-V3Entry([string]$Line, [int]$ExpectedKey) {
    $f = $Line -split "`t"
    if ($f.Count -ne 24 -or $f[1] -notmatch '^44T([0-9]+)$') {
        throw "Malformed V3 ENTRY: $Line"
    }
    $key = [int]$Matches[1]
    Assert-Equal $key $ExpectedKey "V3 key"
    if ($f[2] -ne 'ORDER' -or $f[4] -ne 'PC_ORDER' -or
        $f[6] -ne 'PARITY_MAPS_G' -or $f[8] -ne 'PARITY_MAPS_P' -or
        $f[10] -ne 'AUT_ORDER' -or $f[12] -ne 'ISO_MS' -or
        $f[14] -ne 'AUT_MS' -or $f[16] -ne 'METHOD' -or
        $f[18] -ne 'CLASS_MS' -or $f[20] -ne 'ORDER8_CLASSES' -or
        $f[22] -ne 'RAW_PAIRS') {
        throw "V3 ENTRY field-label mismatch: $Line"
    }
    Assert-Equal ([int64]$f[3]) ([int64]$f[5]) "V3 G/P order at T$ExpectedKey"
    Assert-Equal ([int64]$f[7]) ([int64]$f[9]) "V3 parity maps at T$ExpectedKey"
    [pscustomobject]@{
        K       = $key
        Order   = [int64]$f[3]
        AutOrder= [int64]$f[11]
        IsoMs   = [int64]$f[13]
        AutMs   = [int64]$f[15]
        Method  = $f[17]
        ClassMs = [int64]$f[19]
        Classes = [int64]$f[21]
        Raw     = [int64]$f[23]
        Source  = 'V3_PC_DOMAIN'
    }
}

$partialPath = Join-Path $BaseDir 'GAP_TRANSITIVE_DEGREE44_AUT_PROFILE_1_2113_EXTERNAL_GUARD_PARTIAL1_GPT56SOL.txt'
$cheapPath = Join-Path $BaseDir 'GAP_TRANSITIVE_DEGREE44_ORDER_PARITY_PROFILE_GPT56SOL.txt'

$partial = @(
    foreach ($line in Get-Content -LiteralPath $partialPath) {
        if ($line -match '^ENTRY\t') { Parse-LegacyEntry $line }
    }
)
Assert-Equal $partial.Count 194 'partial1 complete ENTRY count'
Assert-Equal $partial[0].K 55 'partial1 first key'
Assert-Equal $partial[-1].K 272 'partial1 last key'

$tail = @(
    foreach ($key in 273..281) {
        $path = Join-Path $BaseDir "GAP_TRANSITIVE_DEGREE44_AUT_PROFILE_44T${key}_PC_DOMAIN_V3_GPT56SOL.txt"
        $lines = @(Get-Content -LiteralPath $path)
        Assert-Equal (@($lines | Where-Object { $_ -match '^CERTIFICATE_PROFILE\t' }).Count) 1 "T$key header"
        $entryLines = @($lines | Where-Object { $_ -match '^ENTRY\t' })
        Assert-Equal $entryLines.Count 1 "T$key ENTRY"
        Assert-Equal (@($lines | Where-Object { $_ -match '^TOTAL\t' }).Count) 1 "T$key TOTAL"
        Assert-Equal (@($lines | Where-Object { $_ -eq 'DONE' }).Count) 1 "T$key DONE"
        Assert-Equal (@($lines | Where-Object { $_ -match '^TOTAL_PARTIAL\t' -or $_ -eq 'STOPPED_GUARD' }).Count) 0 "T$key partial marker"
        Parse-V3Entry $entryLines[0] $key
    }
)
Assert-Equal $tail.Count 9 'V3 tail ENTRY count'

$entries = @($partial + $tail | Sort-Object K)
Assert-Equal $entries.Count 203 'merged ENTRY count'
$duplicates = @($entries | Group-Object K | Where-Object { $_.Count -ne 1 })
Assert-Equal $duplicates.Count 0 'duplicate merged keys'

$cheap = @(
    foreach ($line in Get-Content -LiteralPath $cheapPath) {
        if ($line -notmatch '^ENTRY\t44T([0-9]+)\tORDER\t([0-9]+)\tPARITY_MAPS\t([0-9]+)$') { continue }
        $parity = [int64]$Matches[3]
        if ($parity -gt 0) {
            [pscustomobject]@{ K=[int]$Matches[1]; Order=[int64]$Matches[2]; Parity=$parity }
        }
    }
)
Assert-Equal $cheap.Count 203 'cheap-profile parity ENTRY count'
$keyDiff = @(Compare-Object -ReferenceObject @($cheap | ForEach-Object { $_.K }) -DifferenceObject @($entries | ForEach-Object { $_.K }))
Assert-Equal $keyDiff.Count 0 'cheap/Aut profile key-set difference'
$cheapByKey = @{}
foreach ($x in $cheap) { $cheapByKey[$x.K] = $x }
foreach ($x in $entries) {
    Assert-Equal $x.Order $cheapByKey[$x.K].Order "cheap/Aut order T$($x.K)"
    if ($cheapByKey[$x.K].Parity -le 0) { throw "Nonpositive parity count at T$($x.K)" }
    Assert-Equal $x.Raw ($x.Order * $x.Classes) "raw identity T$($x.K)"
}

$totalClasses = Sum-Property $entries 'Classes'
$totalRaw = Sum-Property $entries 'Raw'
$totalAutMs = Sum-Property $entries 'AutMs'
$totalClassMs = Sum-Property $entries 'ClassMs'
$tailIsoMs = Sum-Property $tail 'IsoMs'
$totalCostMs = $totalAutMs + $totalClassMs
$positive = @($entries | Where-Object { $_.Raw -gt 0 })
Assert-Equal $totalClasses 92 'full exact-order-8 class total'
Assert-Equal $totalRaw 1302312 'full raw-pair total'
Assert-Equal $totalAutMs 1088635 'full Aut-ms total'
Assert-Equal $totalClassMs 458202 'full class-ms total'
Assert-Equal $tailIsoMs 6 'V3 tail pc-isomorphism ms total'
Assert-Equal $totalCostMs 1546837 'full Aut-plus-class cost'
Assert-Equal $positive.Count 26 'positive-raw ENTRY count'

# Exhaust all C(26-1,3) ordered positive-entry cut triples.  Objective:
# minimize the maximum shard raw count, then raw spread, then cut tuple.
$prefix = [int64[]]::new($positive.Count + 1)
for ($i = 0; $i -lt $positive.Count; $i++) { $prefix[($i + 1)] = $prefix[$i] + $positive[$i].Raw }
$best = $null
for ($i = 0; $i -le $positive.Count - 4; $i++) {
    for ($j = $i + 1; $j -le $positive.Count - 3; $j++) {
        for ($k = $j + 1; $k -le $positive.Count - 2; $k++) {
            $r1 = [int64]$prefix[($i + 1)]
            $r2 = [int64]($prefix[($j + 1)] - $prefix[($i + 1)])
            $r3 = [int64]($prefix[($k + 1)] - $prefix[($j + 1)])
            $r4 = [int64]($prefix[$positive.Count] - $prefix[($k + 1)])
            $raws = [int64[]]@($r1,$r2,$r3,$r4)
            $maxRaw = [int64](($raws | Measure-Object -Maximum).Maximum)
            $minRaw = [int64](($raws | Measure-Object -Minimum).Minimum)
            $spread = $maxRaw - $minRaw
            $cuts = [int[]]@($positive[$i].K,$positive[$j].K,$positive[$k].K)
            $signature = '{0:D5}-{1:D5}-{2:D5}' -f $cuts[0],$cuts[1],$cuts[2]
            if ($null -eq $best -or $maxRaw -lt $best.MaxRaw -or
                ($maxRaw -eq $best.MaxRaw -and $spread -lt $best.Spread) -or
                ($maxRaw -eq $best.MaxRaw -and $spread -eq $best.Spread -and
                 [string]::CompareOrdinal($signature,$best.Signature) -lt 0)) {
                $best = [pscustomobject]@{ Cuts=$cuts; Raws=$raws; MaxRaw=$maxRaw; Spread=$spread; Signature=$signature }
            }
        }
    }
}
Assert-Equal ($best.Cuts -join ',') '109,221,226' 'minimax cut tuple'
Assert-Equal ($best.Raws -join ',') '337832,351120,359920,253440' 'minimax raw tuple'

function Measure-Range([int]$Lo, [int]$Hi) {
    $selected = @($entries | Where-Object { $_.K -ge $Lo -and $_.K -le $Hi })
    [pscustomobject]@{
        Range = "$Lo-$Hi"
        Processed = $selected.Count
        Classes = Sum-Property $selected 'Classes'
        Raw = Sum-Property $selected 'Raw'
        CostMs = (Sum-Property $selected 'AutMs') + (Sum-Property $selected 'ClassMs')
    }
}
$ranges = @(
    Measure-Range 1 109
    Measure-Range 110 221
    Measure-Range 222 226
    Measure-Range 227 2113
)
$expectedRanges = @(
    @(54,50,337832,13954),
    @(91,22,351120,511536),
    @(5,12,359920,1826),
    @(53,8,253440,1019521)
)
for ($i = 0; $i -lt 4; $i++) {
    Assert-Equal $ranges[$i].Processed $expectedRanges[$i][0] "range $i processed"
    Assert-Equal $ranges[$i].Classes $expectedRanges[$i][1] "range $i classes"
    Assert-Equal $ranges[$i].Raw $expectedRanges[$i][2] "range $i raw"
    Assert-Equal $ranges[$i].CostMs $expectedRanges[$i][3] "range $i cost"
}

$raw30 = 127623240.0
$profile30Ms = 469996.0
$full30Ms = 870531.0
$seedIncrement30Ms = $full30Ms - $profile30Ms
$ratio = $totalRaw / $raw30
$scaledIncrementMs = $seedIncrement30Ms * $ratio
$forecastMs = $totalCostMs + $scaledIncrementMs

$profileLines = [System.Collections.Generic.List[string]]::new()
$profileLines.Add("CERTIFICATE_PROFILE`tPF-GRP-001-C8-TRANSITIVE-DEGREE44-AUT-FULL-MERGED-V3")
$profileLines.Add("GAP_VERSION`t4.12.1")
$profileLines.Add("DEGREE`t44")
$profileLines.Add("DATABASE`t2113")
$profileLines.Add("ORDER_WINDOW`t227")
$profileLines.Add("PARITY_ENTRIES`t203")
$profileLines.Add("SOURCES`tPARTIAL1_COMPLETE_ENTRIES_44T55_TO_44T272_PLUS_PC_DOMAIN_V3_44T273_TO_44T281")
$profileLines.Add("SCOPE`tExact automorphism-group and exact-order-8 class profile for every parity-capable order-window target; no seed enumeration.")
foreach ($x in $entries) {
    $profileLines.Add("ENTRY`t44T$($x.K)`tORDER`t$($x.Order)`tAUT_ORDER`t$($x.AutOrder)`tAUT_MS`t$($x.AutMs)`tMETHOD`t$($x.Method)`tCLASS_MS`t$($x.ClassMs)`tORDER8_CLASSES`t$($x.Classes)`tRAW_PAIRS`t$($x.Raw)`tSOURCE`t$($x.Source)")
}
$profileLines.Add("TOTAL`tDEGREE`t44`tDATABASE`t2113`tORDER_WINDOW`t227`tPARITY_ENTRIES`t203`tPROCESSED`t203`tORDER8_CLASSES`t$totalClasses`tRAW_PAIRS`t$totalRaw`tAUT_MS`t$totalAutMs`tCLASS_MS`t$totalClassMs`tAUT_PLUS_CLASS_MS`t$totalCostMs`tTAIL_PC_ISO_MS`t$tailIsoMs")
$profileLines.Add("MERGE_CHECK`tPARTIAL1_ENTRIES`t194`tV3_TAIL_ENTRIES`t9`tDUPLICATES`t0`tCHEAP_KEYSET_DIFFERENCE`t0")
$profileLines.Add("SEED_ENUMERATION`tNOT_RUN")
$profileLines.Add("DONE")
[System.IO.File]::WriteAllLines((Join-Path $BaseDir $MergedProfile),$profileLines,[System.Text.UTF8Encoding]::new($false))

$forecastLines = [System.Collections.Generic.List[string]]::new()
$forecastLines.Add("CERTIFICATE_PROFILE`tPF-GRP-001-C8-TRANSITIVE-DEGREE44-FULL-PARTITION-FORECAST-V3")
$forecastLines.Add("SOURCE_PROFILE`t$MergedProfile")
$forecastLines.Add("PARTITION_METHOD`tExhaustive minimization of maximum shard raw pairs over all three cuts between 26 positive-raw entries; tie-break by minimum spread then lexicographic cuts.")
for ($i = 0; $i -lt 4; $i++) {
    $seedInc = $seedIncrement30Ms * $ranges[$i].Raw / $raw30
    $fullEstimate = $ranges[$i].CostMs + $seedInc
    $forecastLines.Add(("RAW_BALANCED`t{0}`tPROCESSED`t{1}`tORDER8_CLASSES`t{2}`tRAW_PAIRS`t{3}`tAUT_PLUS_CLASS_MS`t{4}`tSCALED_SEED_INCREMENT_MS`t{5:F0}`tESTIMATED_FULL_MS`t{6:F0}`tESTIMATED_FULL_MINUTES`t{7:F3}" -f $ranges[$i].Range,$ranges[$i].Processed,$ranges[$i].Classes,$ranges[$i].Raw,$ranges[$i].CostMs,$seedInc,$fullEstimate,($fullEstimate/60000.0)))
}
$forecastLines.Add("RAW_BALANCED_CHECKSUM`tPROCESSED`t203`tORDER8_CLASSES`t$totalClasses`tRAW_PAIRS`t$totalRaw`tAUT_PLUS_CLASS_MS`t$totalCostMs`tMAX_SHARD_RAW`t$($best.MaxRaw)`tRAW_SPREAD`t$($best.Spread)")
$forecastLines.Add("REFERENCE_D30`tRAW_PAIRS`t127623240`tPROFILE_MS`t469996`tFULL_SCAN_MS`t870531`tSEED_INCREMENT_MS`t400535")
$forecastLines.Add(("FORECAST`tRAW_RATIO`t{0:F9}`tSCALED_SEED_INCREMENT_MS`t{1:F0}`tFULL_SCAN_TOTAL_MS`t{2:F0}`tFULL_SCAN_MINUTES`t{3:F3}" -f $ratio,$scaledIncrementMs,$forecastMs,($forecastMs/60000.0)))
$forecastLines.Add("FORECAST_STATUS`tEmpirical scheduling estimate from exact profile-entry costs and sealed degree-30 scaling; not a closure or an inference about unrun seed gates.")
$forecastLines.Add("STATUS`tFULL_AUT_PROFILE_COMPLETE_NO_SEED_ENUMERATION")
$forecastLines.Add("DONE")
[System.IO.File]::WriteAllLines((Join-Path $BaseDir $PartitionArtifact),$forecastLines,[System.Text.UTF8Encoding]::new($false))

Write-Output "PASS entries=203 classes=$totalClasses raw=$totalRaw autMs=$totalAutMs classMs=$totalClassMs tailIsoMs=$tailIsoMs cuts=$($best.Cuts -join ',') forecastMs=$([math]::Round($forecastMs))"
