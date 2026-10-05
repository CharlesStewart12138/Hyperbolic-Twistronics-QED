param(
    [string]$BaseDir = ".",
    [string]$OutputName = "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_32SHARD_PLAN_GPT56SOL.tsv"
)

$ErrorActionPreference = "Stop"

function Assert-Equal($Actual, $Expected, [string]$Label) {
    if ($Actual -ne $Expected) { throw "$Label mismatch: actual=$Actual expected=$Expected" }
}

function Sum-Property($Items, [string]$Property) {
    $v = ($Items | Measure-Object -Property $Property -Sum).Sum
    if ($null -eq $v) { return [int64]0 }
    return [int64]$v
}

function Parse-Pairs([string]$Line, [string]$Prefix) {
    $f=$Line -split "`t"
    if ($f.Count -lt 4 -or $f[0] -ne $Prefix -or $f[1] -notmatch '^24T([0-9]+)$') {
        throw "Malformed $Prefix line: $Line"
    }
    $r=[ordered]@{ K=[int]$Matches[1] }
    for ($i=2; $i -lt $f.Count; $i+=2) {
        if ($i+1 -ge $f.Count) { throw "Odd field count: $Line" }
        $r[$f[$i]]=$f[$i+1]
    }
    return [pscustomobject]$r
}

$solFiles=@(
    'GAP_TRANSITIVE_DEGREE24_SOLVABILITY_1_7860_GPT56SOL.txt',
    'GAP_TRANSITIVE_DEGREE24_SOLVABILITY_7861_10567_GPT56SOL.txt',
    'GAP_TRANSITIVE_DEGREE24_SOLVABILITY_10568_13274_GPT56SOL.txt',
    'GAP_TRANSITIVE_DEGREE24_SOLVABILITY_13275_25000_GPT56SOL.txt'
)
$targets=@(
    foreach ($name in $solFiles) {
        foreach ($line in [System.IO.File]::ReadAllLines((Join-Path $BaseDir $name))) {
            if ($line -match '^ENTRY\t') {
                $x=Parse-Pairs $line 'ENTRY'
                [pscustomobject]@{
                    K=[int]$x.K; Order=[int64]$x.ORDER; Parity=[int64]$x.PARITY_MAPS;
                    Solvable=[int]$x.SOLVABLE
                }
            }
        }
    }
) | Sort-Object K
Assert-Equal $targets.Count 10714 'parity-capable target count'
Assert-Equal @($targets | Group-Object K | Where-Object { $_.Count -ne 1 }).Count 0 'duplicate parity keys'
Assert-Equal @($targets | Where-Object { $_.Parity -le 0 }).Count 0 'nonpositive parity map count'
Assert-Equal @($targets | Where-Object { $_.Solvable -eq 1 }).Count 10537 'solvable target count'
Assert-Equal @($targets | Where-Object { $_.Solvable -eq 0 }).Count 177 'nonsolvable target count'

$parityFiles=@(
    'GAP_TRANSITIVE_DEGREE24_PARITY_1_7860_GPT56SOL.txt',
    'GAP_TRANSITIVE_DEGREE24_PARITY_7861_10567_GPT56SOL.txt',
    'GAP_TRANSITIVE_DEGREE24_PARITY_10568_13274_GPT56SOL.txt',
    'GAP_TRANSITIVE_DEGREE24_PARITY_13275_25000_GPT56SOL.txt'
)
$window=@(
    foreach ($name in $parityFiles) {
        foreach ($line in [System.IO.File]::ReadAllLines((Join-Path $BaseDir $name))) {
            if ($line -match '^ENTRY\t') {
                $x=Parse-Pairs $line 'ENTRY'
                [pscustomobject]@{ K=[int]$x.K; Order=[int64]$x.ORDER; Parity=[int64]$x.PARITY_MAPS }
            }
        }
    }
) | Sort-Object K
Assert-Equal $window.Count 10829 'order-window target count'
Assert-Equal @($window | Where-Object { $_.Parity -gt 0 }).Count 10714 'parity target count from cheap profile'
Assert-Equal @(Compare-Object -ReferenceObject @($window | Where-Object { $_.Parity -gt 0 } | ForEach-Object { $_.K }) -DifferenceObject @($targets | ForEach-Object { $_.K })).Count 0 'cheap/solvability parity key difference'

$sampleFiles=@(
    'GAP_TRANSITIVE_DEGREE24_AUT_FORECAST_S1_GPT56SOL.txt',
    'GAP_TRANSITIVE_DEGREE24_AUT_FORECAST_S2_GPT56SOL.txt',
    'GAP_TRANSITIVE_DEGREE24_AUT_FORECAST_S3_GPT56SOL.txt',
    'GAP_TRANSITIVE_DEGREE24_AUT_FORECAST_S4_GPT56SOL.txt'
)
$samples=@(
    foreach ($name in $sampleFiles) {
        foreach ($line in [System.IO.File]::ReadAllLines((Join-Path $BaseDir $name))) {
            if ($line -match '^ENTRY\t') {
                $x=Parse-Pairs $line 'ENTRY'
                [pscustomobject]@{
                    K=[int]$x.K; Order=[int64]$x.ORDER;
                    Solvable=if ($x.SOLVABLE -eq 'true') { 1 } else { 0 };
                    AutMs=[int64]$x.AUT_MS; ClassMs=[int64]$x.CLASS_MS;
                    Classes=[int64]$x.ORDER8_CLASSES; Raw=[int64]$x.RAW_PAIRS
                }
            }
        }
    }
)
Assert-Equal $samples.Count 48 'forecast sample count'
$strata=@{}
foreach ($x in $samples) {
    $id="$($x.Order)|$($x.Solvable)"
    if ($strata.ContainsKey($id)) { throw "duplicate sample stratum $id" }
    $strata[$id]=[pscustomobject]@{
        Cost=[int64]($x.AutMs+$x.ClassMs); Classes=$x.Classes; Raw=$x.Raw; SampleKey=$x.K
    }
}
Assert-Equal $strata.Count 48 'sample stratum count'
Assert-Equal @($targets | Group-Object { "$($_.Order)|$($_.Solvable)" }).Count 48 'target stratum count'

$weighted=@(
    foreach ($x in $targets) {
        $id="$($x.Order)|$($x.Solvable)"
        if (-not $strata.ContainsKey($id)) { throw "missing forecast stratum $id" }
        $s=$strata[$id]
        [pscustomobject]@{
            K=$x.K; Order=$x.Order; Solvable=$x.Solvable; PointMs=$s.Cost;
            PointClasses=$s.Classes; PointRaw=$s.Raw
        }
    }
)
$totalPointMs=Sum-Property $weighted 'PointMs'
$totalPointClasses=Sum-Property $weighted 'PointClasses'
$totalPointRaw=Sum-Property $weighted 'PointRaw'
Assert-Equal $totalPointMs 11737831 'point forecast ms'
Assert-Equal $totalPointClasses 967944 'point forecast classes'
Assert-Equal $totalPointRaw 25901774880 'point forecast raw pairs'

$shardCount=32
$prefix=[int64[]]::new($weighted.Count+1)
for ($i=0; $i -lt $weighted.Count; $i++) { $prefix[$i+1]=$prefix[$i]+$weighted[$i].PointMs }
$cutPositions=[System.Collections.Generic.List[int]]::new()
$previous=0
$seek=1
for ($shard=1; $shard -lt $shardCount; $shard++) {
    $target=[double]$totalPointMs*$shard/$shardCount
    $minPosition=$previous+1
    $maxPosition=$weighted.Count-($shardCount-$shard)
    if ($seek -lt $minPosition) { $seek=$minPosition }
    while ($seek -lt $maxPosition -and $prefix[$seek] -lt $target) { $seek++ }
    $candidates=@($seek)
    if ($seek-1 -ge $minPosition) { $candidates+=($seek-1) }
    $bestPosition=$null; $bestDistance=[double]::PositiveInfinity
    foreach ($position in $candidates) {
        if ($position -lt $minPosition -or $position -gt $maxPosition) { continue }
        $distance=[Math]::Abs([double]$prefix[$position]-$target)
        if ($distance -lt $bestDistance -or ($distance -eq $bestDistance -and $position -lt $bestPosition)) {
            $bestPosition=$position; $bestDistance=$distance
        }
    }
    $cutPositions.Add($bestPosition)
    $previous=$bestPosition
    $seek=$bestPosition+1
}

$ranges=[System.Collections.Generic.List[object]]::new()
$lo=1; $startPosition=0
for ($i=0; $i -lt $shardCount; $i++) {
    if ($i -lt $shardCount-1) {
        $endPosition=$cutPositions[$i]
        $hi=$weighted[$endPosition-1].K
    } else {
        $endPosition=$weighted.Count
        $hi=25000
    }
    $members=@($weighted[$startPosition..($endPosition-1)])
    $windowCount=@($window | Where-Object { $_.K -ge $lo -and $_.K -le $hi }).Count
    $ranges.Add([pscustomobject]@{
        Number=$i+1; Lo=$lo; Hi=$hi; Window=$windowCount; Parity=$members.Count;
        PointMs=Sum-Property $members 'PointMs';
        PointClasses=Sum-Property $members 'PointClasses';
        PointRaw=Sum-Property $members 'PointRaw'
    })
    $lo=$hi+1; $startPosition=$endPosition
}
Assert-Equal $ranges.Count 32 'range count'
Assert-Equal $ranges[0].Lo 1 'first range low'
Assert-Equal $ranges[-1].Hi 25000 'last range high'
for ($i=1; $i -lt $ranges.Count; $i++) { Assert-Equal $ranges[$i].Lo ($ranges[$i-1].Hi+1) "range continuity $i" }
Assert-Equal (Sum-Property $ranges 'Window') 10829 'range window checksum'
Assert-Equal (Sum-Property $ranges 'Parity') 10714 'range parity checksum'
Assert-Equal (Sum-Property $ranges 'PointMs') 11737831 'range point-ms checksum'
Assert-Equal (Sum-Property $ranges 'PointClasses') 967944 'range point-class checksum'
Assert-Equal (Sum-Property $ranges 'PointRaw') 25901774880 'range point-raw checksum'

$maxPoint=[int64](($ranges | Measure-Object -Property PointMs -Maximum).Maximum)
$minPoint=[int64](($ranges | Measure-Object -Property PointMs -Minimum).Minimum)
$lines=[System.Collections.Generic.List[string]]::new()
$lines.Add("CERTIFICATE_PLAN`tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-PROFILE-32SHARD")
$lines.Add("DATABASE`t25000")
$lines.Add("ORDER_WINDOW`t10829")
$lines.Add("PARITY_KEYS`t10714")
$lines.Add("STRATA`t48")
$lines.Add("POINT_FORECAST_MS`t11737831")
$lines.Add("POINT_FORECAST_CPU_HOURS`t3.260509")
$lines.Add("POINT_CLASSES`t967944")
$lines.Add("POINT_RAW_PAIRS`t25901774880")
$lines.Add("PARTITION_METHOD`t32 cumulative point-cost quantiles over parity keys sorted by catalogue key; each key cost is the sealed median sample AutMs+ClassMs of its exact (order,solvability) stratum; nearest-prefix tie breaks to the earlier key.")
$lines.Add("GUARDS`tINTERNAL_GAP_MS`t1320000`tEXTERNAL_WALL_SECONDS`t1400`tVIRTUAL_MEMORY_BYTES`t51539607552")
$lines.Add("RECOVERY`tEvery completed eligible key emits ENTRY plus CHECKPOINT; every 25 catalogue keys emits SCAN_CHECKPOINT. Internal stop records LAST_COMPLETE_K. External interruption resumes at the last complete key plus one in a new unique segment, never recomputing a sealed Aut ENTRY.")
foreach ($r in $ranges) {
    $lines.Add(("SHARD`t{0}`tRANGE`t{1}`t{2}`tORDER_WINDOW`t{3}`tPARITY_KEYS`t{4}`tPOINT_AUT_CLASS_MS`t{5}`tPOINT_MINUTES`t{6:F3}`tPOINT_CLASSES`t{7}`tPOINT_RAW_PAIRS`t{8}" -f $r.Number,$r.Lo,$r.Hi,$r.Window,$r.Parity,$r.PointMs,($r.PointMs/60000.0),$r.PointClasses,$r.PointRaw))
}
$lines.Add("BALANCE`tSHARDS`t32`tMAX_POINT_MS`t$maxPoint`tMIN_POINT_MS`t$minPoint`tSPREAD_MS`t$($maxPoint-$minPoint)`tMAX_FRACTION_INTERNAL_GUARD`t$('{0:F6}' -f ($maxPoint/1320000.0))")
$lines.Add("CHECKSUM`tRANGES`t32`tFIRST_KEY`t1`tLAST_KEY`t25000`tGAPS`t0`tOVERLAPS`t0`tORDER_WINDOW`t10829`tPARITY_KEYS`t10714`tPOINT_MS`t11737831`tPOINT_CLASSES`t967944`tPOINT_RAW_PAIRS`t25901774880")
$lines.Add("SCOPE`tPlan for exact Aut(G), exact-order-8 conjugacy classes, and raw=Size(G)*class-count only. No seed predicate is included.")
$lines.Add("STATUS`tPLAN_SEALED_NO_AUT_PROFILE_RESULT_YET")
$lines.Add("DONE")
[System.IO.File]::WriteAllLines((Join-Path $BaseDir $OutputName),$lines,[System.Text.UTF8Encoding]::new($false))

$first=$ranges[0]
Write-Output "PASS shards=32 first=$($first.Lo)-$($first.Hi) firstWindow=$($first.Window) firstParity=$($first.Parity) firstPointMs=$($first.PointMs) maxPointMs=$maxPoint totalPointMs=$totalPointMs"
