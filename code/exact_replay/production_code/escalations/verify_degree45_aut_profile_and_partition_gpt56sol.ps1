param(
    [string]$BaseDir = ".",
    [string]$Profile = "GAP_TRANSITIVE_DEGREE45_AUT_PROFILE_1_10923_GPT56SOL.txt",
    [string]$CheapProfile = "GAP_TRANSITIVE_DEGREE45_ORDER_PARITY_PROFILE_GPT56SOL.txt",
    [string]$PartitionArtifact = "GAP_TRANSITIVE_DEGREE45_AUT_PROFILE_PARTITION_FORECAST_GPT56SOL.tsv"
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

function Parse-Entry([string]$Line) {
    $f = $Line -split "`t"
    if ($f.Count -ne 16 -or $f[1] -notmatch '^45T([0-9]+)$') {
        throw "Malformed Aut-profile ENTRY: $Line"
    }
    if ($f[2] -ne 'ORDER' -or $f[4] -ne 'AUT_ORDER' -or
        $f[6] -ne 'AUT_MS' -or $f[8] -ne 'METHOD' -or
        $f[10] -ne 'CLASS_MS' -or $f[12] -ne 'ORDER8_CLASSES' -or
        $f[14] -ne 'RAW_PAIRS') {
        throw "Aut-profile ENTRY field-label mismatch: $Line"
    }
    [pscustomobject]@{
        K        = [int]$Matches[1]
        Order    = [int64]$f[3]
        AutOrder = [int64]$f[5]
        AutMs    = [int64]$f[7]
        Method   = $f[9]
        ClassMs  = [int64]$f[11]
        Classes  = [int64]$f[13]
        Raw      = [int64]$f[15]
    }
}

$profilePath = Join-Path $BaseDir $Profile
$profileLines = @([System.IO.File]::ReadAllLines($profilePath))
$expectedHeader = @(
    "CERTIFICATE_PROFILE`tPF-GRP-001-C8-TRANSITIVE-AUT-PROFILE",
    "DEGREE`t45",
    "RANGE`t1`t10923",
    "GUARD_MS`t1320000",
    "SCOPE`tExact Aut(G) and exact-order-8 conjugacy classes for every parity-capable order-window target; no seed enumeration."
)
for ($i = 0; $i -lt $expectedHeader.Count; $i++) {
    Assert-Equal $profileLines[$i] $expectedHeader[$i] "profile header line $($i + 1)"
}
Assert-Equal @($profileLines | Where-Object { $_ -match '^CERTIFICATE_PROFILE\t' }).Count 1 'profile header count'
Assert-Equal @($profileLines | Where-Object { $_ -match '^TOTAL\t' }).Count 1 'profile TOTAL count'
Assert-Equal @($profileLines | Where-Object { $_ -eq 'DONE' }).Count 1 'profile DONE count'
Assert-Equal $profileLines[-1] 'DONE' 'profile terminal marker'
Assert-Equal @($profileLines | Where-Object { $_ -match '^TOTAL_PARTIAL\t' -or $_ -eq 'STOPPED_GUARD' }).Count 0 'profile partial/guard markers'

$entries = @(
    foreach ($line in $profileLines) {
        if ($line -match '^ENTRY\t') { Parse-Entry $line }
    }
)
Assert-Equal $entries.Count 521 'Aut-profile ENTRY count'
Assert-Equal @($entries | Group-Object K | Where-Object { $_.Count -ne 1 }).Count 0 'duplicate Aut-profile keys'
for ($i = 1; $i -lt $entries.Count; $i++) {
    if ($entries[$i].K -le $entries[$i - 1].K) { throw "Aut-profile keys not strictly increasing" }
}

$cheapPath = Join-Path $BaseDir $CheapProfile
$cheapLines = @([System.IO.File]::ReadAllLines($cheapPath))
Assert-Equal @($cheapLines | Where-Object { $_ -match '^TOTAL\t' }).Count 1 'cheap-profile TOTAL count'
Assert-Equal @($cheapLines | Where-Object { $_ -eq 'DONE' }).Count 1 'cheap-profile DONE count'
Assert-Equal @($cheapLines | Where-Object { $_ -match '^TOTAL_PARTIAL\t' -or $_ -eq 'STOPPED_GUARD' }).Count 0 'cheap-profile partial/guard markers'
$cheap = @(
    foreach ($line in $cheapLines) {
        if ($line -notmatch '^ENTRY\t45T([0-9]+)\tORDER\t([0-9]+)\tPARITY_MAPS\t([0-9]+)$') { continue }
        $parity = [int64]$Matches[3]
        if ($parity -gt 0) {
            [pscustomobject]@{ K=[int]$Matches[1]; Order=[int64]$Matches[2]; Parity=$parity }
        }
    }
)
Assert-Equal $cheap.Count 521 'cheap-profile parity key count'
$keyDiff = @(Compare-Object -ReferenceObject @($cheap | ForEach-Object { $_.K }) -DifferenceObject @($entries | ForEach-Object { $_.K }))
Assert-Equal $keyDiff.Count 0 'cheap/Aut profile key-set difference'
$cheapByKey = @{}
foreach ($x in $cheap) { $cheapByKey[$x.K] = $x }
foreach ($x in $entries) {
    Assert-Equal $x.Order $cheapByKey[$x.K].Order "cheap/Aut order 45T$($x.K)"
    Assert-Equal $x.Raw ($x.Order * $x.Classes) "raw identity 45T$($x.K)"
}

$totalClasses = Sum-Property $entries 'Classes'
$totalRaw = Sum-Property $entries 'Raw'
$totalAutMs = Sum-Property $entries 'AutMs'
$totalClassMs = Sum-Property $entries 'ClassMs'
$totalCostMs = $totalAutMs + $totalClassMs
$positive = @($entries | Where-Object { $_.Raw -gt 0 })
Assert-Equal $totalClasses 3662 'exact-order-8 class total'
Assert-Equal $totalRaw 64853010 'raw-pair total'
Assert-Equal $totalAutMs 76860 'Aut-ms total'
Assert-Equal $totalClassMs 161291 'class-ms total'
Assert-Equal $totalCostMs 238151 'Aut-plus-class cost'
Assert-Equal $positive.Count 232 'positive-raw ENTRY count'
$expectedTotal = "TOTAL`tDEGREE`t45`tRANGE`t1`t10923`tPROCESSED`t521`tORDER8_CLASSES`t3662`tRAW_PAIRS`t64853010`tAUT_MS`t76860`tCLASS_MS`t161291`tMS`t256803"
Assert-Equal @($profileLines | Where-Object { $_ -match '^TOTAL\t' })[0] $expectedTotal 'profile TOTAL line'

# Exhaust every ordered triple of cuts between the 232 positive-raw entries.
# Objective: minimum maximum shard raw pairs, then minimum spread, then the
# lexicographically first cut-key tuple (the loop order supplies that tie-break).
$prefix = [int64[]]::new($positive.Count + 1)
for ($i = 0; $i -lt $positive.Count; $i++) {
    $prefix[$i + 1] = $prefix[$i] + $positive[$i].Raw
}
$best = $null
for ($i = 0; $i -le $positive.Count - 4; $i++) {
    $r1 = [int64]$prefix[$i + 1]
    for ($j = $i + 1; $j -le $positive.Count - 3; $j++) {
        $r2 = [int64]($prefix[$j + 1] - $prefix[$i + 1])
        for ($k = $j + 1; $k -le $positive.Count - 2; $k++) {
            $r3 = [int64]($prefix[$k + 1] - $prefix[$j + 1])
            $r4 = [int64]($prefix[$positive.Count] - $prefix[$k + 1])
            $maxRaw = [Math]::Max([Math]::Max($r1,$r2),[Math]::Max($r3,$r4))
            $minRaw = [Math]::Min([Math]::Min($r1,$r2),[Math]::Min($r3,$r4))
            $spread = $maxRaw - $minRaw
            if ($null -eq $best -or $maxRaw -lt $best.MaxRaw -or
                ($maxRaw -eq $best.MaxRaw -and $spread -lt $best.Spread)) {
                $best = [pscustomobject]@{
                    Cuts = [int[]]@($positive[$i].K,$positive[$j].K,$positive[$k].K)
                    Raws = [int64[]]@($r1,$r2,$r3,$r4)
                    MaxRaw = [int64]$maxRaw
                    Spread = [int64]$spread
                }
            }
        }
    }
}

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
    Measure-Range 1 $best.Cuts[0]
    Measure-Range ($best.Cuts[0] + 1) $best.Cuts[1]
    Measure-Range ($best.Cuts[1] + 1) $best.Cuts[2]
    Measure-Range ($best.Cuts[2] + 1) 10923
)
Assert-Equal (Sum-Property $ranges 'Processed') 521 'partition processed checksum'
Assert-Equal (Sum-Property $ranges 'Classes') 3662 'partition class checksum'
Assert-Equal (Sum-Property $ranges 'Raw') 64853010 'partition raw checksum'
Assert-Equal (Sum-Property $ranges 'CostMs') 238151 'partition cost checksum'

$raw30 = 127623240.0
$profile30Ms = 469996.0
$full30Ms = 870531.0
$seedIncrement30Ms = $full30Ms - $profile30Ms
$ratio = $totalRaw / $raw30
$scaledIncrementMs = $seedIncrement30Ms * $ratio
$forecastMs = $totalCostMs + $scaledIncrementMs

$forecastLines = [System.Collections.Generic.List[string]]::new()
$forecastLines.Add("CERTIFICATE_PROFILE`tPF-GRP-001-C8-TRANSITIVE-DEGREE45-PARTITION-FORECAST")
$forecastLines.Add("SOURCE_PROFILE`t$Profile")
$forecastLines.Add("PARTITION_METHOD`tExhaustive minimization of maximum shard raw pairs over all three cuts between 232 positive-raw entries; tie-break by minimum spread then lexicographic cuts.")
for ($i = 0; $i -lt 4; $i++) {
    $seedInc = $seedIncrement30Ms * $ranges[$i].Raw / $raw30
    $fullEstimate = $ranges[$i].CostMs + $seedInc
    $forecastLines.Add(("RAW_BALANCED`t{0}`tPROCESSED`t{1}`tORDER8_CLASSES`t{2}`tRAW_PAIRS`t{3}`tAUT_PLUS_CLASS_MS`t{4}`tSCALED_SEED_INCREMENT_MS`t{5:F0}`tESTIMATED_FULL_MS`t{6:F0}`tESTIMATED_FULL_MINUTES`t{7:F3}" -f $ranges[$i].Range,$ranges[$i].Processed,$ranges[$i].Classes,$ranges[$i].Raw,$ranges[$i].CostMs,$seedInc,$fullEstimate,($fullEstimate/60000.0)))
}
$forecastLines.Add("RAW_BALANCED_CHECKSUM`tPROCESSED`t521`tORDER8_CLASSES`t$totalClasses`tRAW_PAIRS`t$totalRaw`tAUT_PLUS_CLASS_MS`t$totalCostMs`tMAX_SHARD_RAW`t$($best.MaxRaw)`tRAW_SPREAD`t$($best.Spread)")
$forecastLines.Add("REFERENCE_D30`tRAW_PAIRS`t127623240`tPROFILE_MS`t469996`tFULL_SCAN_MS`t870531`tSEED_INCREMENT_MS`t400535")
$forecastLines.Add(("FORECAST`tRAW_RATIO`t{0:F9}`tSCALED_SEED_INCREMENT_MS`t{1:F0}`tFULL_SCAN_TOTAL_MS`t{2:F0}`tFULL_SCAN_MINUTES`t{3:F3}" -f $ratio,$scaledIncrementMs,$forecastMs,($forecastMs/60000.0)))
$forecastLines.Add("FORECAST_STATUS`tEmpirical scheduling estimate from exact profile-entry costs and sealed degree-30 scaling; not a closure or an inference about unrun seed gates.")
$forecastLines.Add("STATUS`tFULL_AUT_PROFILE_COMPLETE_NO_SEED_ENUMERATION")
$forecastLines.Add("DONE")
[System.IO.File]::WriteAllLines((Join-Path $BaseDir $PartitionArtifact),$forecastLines,[System.Text.UTF8Encoding]::new($false))

Write-Output "PASS entries=521 positive=232 classes=$totalClasses raw=$totalRaw autMs=$totalAutMs classMs=$totalClassMs cuts=$($best.Cuts -join ',') loads=$($best.Raws -join ',') forecastMs=$([Math]::Round($forecastMs))"
