param(
    [string]$ProfilePath = "GAP_TRANSITIVE_DEGREE42_AUT_PROFILE_1_9491_GPT56SOL.txt",
    [string]$OutputPath = "GAP_TRANSITIVE_DEGREE42_AUT_PROFILE_PARTITION_FORECAST_GPT56SOL.txt"
)

$ErrorActionPreference = "Stop"

$entries = foreach ($line in Get-Content -LiteralPath $ProfilePath) {
    if ($line -notmatch '^ENTRY\t') { continue }
    $f = $line -split "`t"
    if ($f.Count -ne 16 -or $f[1] -notmatch '^42T([0-9]+)$') {
        throw "Malformed ENTRY: $line"
    }
    [pscustomobject]@{
        K       = [int]$Matches[1]
        Classes = [int64]$f[13]
        Raw     = [int64]$f[15]
        CostMs  = [int64]$f[7] + [int64]$f[11]
    }
}

function Measure-Range([int]$Lo, [int]$Hi) {
    $selected = @($entries | Where-Object { $_.K -ge $Lo -and $_.K -le $Hi })
    [pscustomobject]@{
        Range     = "$Lo-$Hi"
        Processed = $selected.Count
        Classes   = [int64](($selected | Measure-Object -Property Classes -Sum).Sum)
        Raw       = [int64](($selected | Measure-Object -Property Raw -Sum).Sum)
        CostMs    = [int64](($selected | Measure-Object -Property CostMs -Sum).Sum)
    }
}

$rawBalanced = @(
    Measure-Range 1 620
    Measure-Range 621 819
    Measure-Range 820 873
    Measure-Range 874 9491
)
$costBalanced = @(
    Measure-Range 1 663
    Measure-Range 664 790
    Measure-Range 791 856
    Measure-Range 857 9491
)

$totalProcessed = [int64](($entries | Measure-Object).Count)
$totalClasses = [int64](($entries | Measure-Object -Property Classes -Sum).Sum)
$totalRaw = [int64](($entries | Measure-Object -Property Raw -Sum).Sum)
$totalCost = [int64](($entries | Measure-Object -Property CostMs -Sum).Sum)
if ($totalProcessed -ne 637 -or $totalClasses -ne 767 -or
    $totalRaw -ne 11421144 -or $totalCost -ne 389233) {
    throw "Profile checksum mismatch"
}

$rawExpected = @(
    @(301,438,2788632,79911),
    @(185,163,3146976,126137),
    @(51,88,2613912,107023),
    @(100,78,2871624,76162)
)
for ($i = 0; $i -lt 4; $i++) {
    $actual = $rawBalanced[$i]
    $expected = $rawExpected[$i]
    if ($actual.Processed -ne $expected[0] -or $actual.Classes -ne $expected[1] -or
        $actual.Raw -ne $expected[2] -or $actual.CostMs -ne $expected[3]) {
        throw "Raw-balanced range checksum mismatch: $($actual.Range)"
    }
}

$raw30 = 127623240.0
$profile30Ms = 469996.0
$full30Ms = 870531.0
$profile42Ms = 424715.0
$ratio = $totalRaw / $raw30
$scaledIncrementMs = ($full30Ms - $profile30Ms) * $ratio
$forecastMs = $profile42Ms + $scaledIncrementMs

$lines = [System.Collections.Generic.List[string]]::new()
$lines.Add("CERTIFICATE_PROFILE`tPF-GRP-001-C8-TRANSITIVE-DEGREE42-PARTITION-FORECAST")
$lines.Add("SOURCE_PROFILE`t$ProfilePath")
foreach ($r in $rawBalanced) {
    $lines.Add("RAW_BALANCED`t$($r.Range)`tPROCESSED`t$($r.Processed)`tORDER8_CLASSES`t$($r.Classes)`tRAW_PAIRS`t$($r.Raw)`tAUT_PLUS_CLASS_MS`t$($r.CostMs)")
}
$lines.Add("RAW_BALANCED_CHECKSUM`tPROCESSED`t$totalProcessed`tORDER8_CLASSES`t$totalClasses`tRAW_PAIRS`t$totalRaw`tAUT_PLUS_CLASS_MS`t$totalCost")
foreach ($r in $costBalanced) {
    $lines.Add("COST_BALANCED_DIAGNOSTIC`t$($r.Range)`tPROCESSED`t$($r.Processed)`tORDER8_CLASSES`t$($r.Classes)`tRAW_PAIRS`t$($r.Raw)`tAUT_PLUS_CLASS_MS`t$($r.CostMs)")
}
$lines.Add("REFERENCE_D30`tRAW_PAIRS`t127623240`tPROFILE_MS`t469996`tFULL_SCAN_MS`t870531")
$lines.Add(("FORECAST`tRAW_RATIO`t{0:F9}`tSCALED_SEED_INCREMENT_MS`t{1:F0}`tFULL_SCAN_TOTAL_MS`t{2:F0}`tFULL_SCAN_MINUTES`t{3:F3}" -f $ratio,$scaledIncrementMs,$forecastMs,($forecastMs / 60000.0)))
$lines.Add("STATUS`tPROFILE_DERIVED_ONLY_NO_SEED_ENUMERATION")
$lines.Add("DONE")
[System.IO.File]::WriteAllLines($OutputPath, $lines, [System.Text.UTF8Encoding]::new($false))
