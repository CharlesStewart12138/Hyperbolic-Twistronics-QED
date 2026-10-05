param(
    [string]$BaseDir = ".",
    [string]$OutputName = "GAP_TRANSITIVE_DEGREE44_C8_FULL_CLOSURE_VERIFY_GPT56SOL.txt"
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

function Parse-EntryPairs([string]$Line, [string]$Prefix) {
    $f = $Line -split "`t"
    if ($f.Count -lt 4 -or $f[0] -ne $Prefix -or $f[1] -notmatch '^44T([0-9]+)$') {
        throw "Malformed $Prefix line: $Line"
    }
    $record = [ordered]@{ K=[int]$Matches[1] }
    for ($i = 2; $i -lt $f.Count; $i += 2) {
        if ($i + 1 -ge $f.Count) { throw "Odd field count: $Line" }
        $record[$f[$i]] = $f[$i+1]
    }
    return [pscustomobject]$record
}

function Parse-Total([string]$Line) {
    $f = $Line -split "`t"
    if ($f.Count -lt 9 -or $f[0] -ne 'TOTAL' -or $f[1] -ne 'DEGREE' -or
        $f[3] -ne 'DATABASE' -or $f[5] -ne 'RANGE') {
        throw "Malformed TOTAL: $Line"
    }
    $record = [ordered]@{
        DEGREE=[int64]$f[2]; DATABASE=[int64]$f[4]; RANGE_LO=[int]$f[6]; RANGE_HI=[int]$f[7]
    }
    for ($i = 8; $i -lt $f.Count; $i += 2) {
        if ($i + 1 -ge $f.Count) { throw "Odd TOTAL field count: $Line" }
        $record[$f[$i]] = [int64]$f[$i+1]
    }
    return [pscustomobject]$record
}

function Verify-Manifest([string]$Name, [int]$ExpectedCount) {
    $path = Join-Path $BaseDir $Name
    $rows = @(Get-Content -LiteralPath $path)
    Assert-Equal $rows.Count $ExpectedCount "$Name entry count"
    foreach ($row in $rows) {
        if ($row -notmatch '^([0-9A-F]{64})  (.+)$') { throw "Malformed manifest row in $Name" }
        $want = $Matches[1]; $file = $Matches[2]
        $got = (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $BaseDir $file)).Hash
        Assert-Equal $got $want "$Name hash $file"
    }
    return (Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash
}

$profilePath = Join-Path $BaseDir 'GAP_TRANSITIVE_DEGREE44_AUT_PROFILE_FULL_MERGED_V3_GPT56SOL.txt'
$profileLines = @(Get-Content -LiteralPath $profilePath)
$profile = @(
    foreach ($line in $profileLines) {
        if ($line -match '^ENTRY\t') {
            $x = Parse-EntryPairs $line 'ENTRY'
            [pscustomobject]@{
                K=$x.K; Order=[int64]$x.ORDER; Classes=[int64]$x.ORDER8_CLASSES; Raw=[int64]$x.RAW_PAIRS
            }
        }
    }
)
Assert-Equal $profile.Count 203 'full profile entry count'
Assert-Equal (Sum-Property $profile 'Classes') 92 'full profile classes'
Assert-Equal (Sum-Property $profile 'Raw') 1302312 'full profile raw'
$profileByKey = @{}
foreach ($x in $profile) {
    if ($profileByKey.ContainsKey($x.K)) { throw "Duplicate profile key $($x.K)" }
    Assert-Equal $x.Raw ($x.Order * $x.Classes) "profile raw identity T$($x.K)"
    $profileByKey[$x.K] = $x
}

$cheapPath = Join-Path $BaseDir 'GAP_TRANSITIVE_DEGREE44_ORDER_PARITY_PROFILE_GPT56SOL.txt'
$cheap = @(
    foreach ($line in Get-Content -LiteralPath $cheapPath) {
        if ($line -match '^ENTRY\t44T([0-9]+)\tORDER\t([0-9]+)\tPARITY_MAPS\t([0-9]+)$') {
            [pscustomobject]@{ K=[int]$Matches[1]; Order=[int64]$Matches[2]; Parity=[int64]$Matches[3] }
        }
    }
)
Assert-Equal $cheap.Count 227 'cheap order-window count'
Assert-Equal @($cheap | Where-Object { $_.Parity -gt 0 }).Count 203 'cheap parity count'

$specs = @(
    [pscustomobject]@{ Name='SHARD1'; File='GAP_TRANSITIVE_DEGREE44_C8_BETA_1_109_GPT56SOL.txt'; Lo=1; Hi=109; Window=55; Parity=54; Classes=50; Invariant=50; Beta=27; Raw=337832; Inverse=12856; InverseOdd=3584; Orbit=3440; Relator=3440; Ms=16405; Manifest='GAP_TRANSITIVE_DEGREE44_C8_SHARD1_GPT56SOL_MANIFEST.sha256'; ManifestCount=9 },
    [pscustomobject]@{ Name='SHARD2'; File='GAP_TRANSITIVE_DEGREE44_C8_BETA_110_221_GPT56SOL.txt'; Lo=110; Hi=221; Window=112; Parity=91; Classes=22; Invariant=22; Beta=16; Raw=351120; Inverse=18064; InverseOdd=15292; Orbit=14704; Relator=8144; Ms=501918; Manifest='GAP_TRANSITIVE_DEGREE44_C8_SHARD2_GPT56SOL_MANIFEST.sha256'; ManifestCount=9 },
    [pscustomobject]@{ Name='SHARD3'; File='GAP_TRANSITIVE_DEGREE44_C8_BETA_222_226_GPT56SOL.txt'; Lo=222; Hi=226; Window=5; Parity=5; Classes=12; Invariant=12; Beta=3; Raw=359920; Inverse=4472; InverseOdd=1660; Orbit=1520; Relator=720; Ms=2821; Manifest='GAP_TRANSITIVE_DEGREE44_C8_SHARD3_GPT56SOL_MANIFEST.sha256'; ManifestCount=9 },
    [pscustomobject]@{ Name='SHARD4'; File='GAP_TRANSITIVE_DEGREE44_C8_BETA_227_228_GPT56SOL.txt'; Lo=227; Hi=228; Window=2; Parity=2; Classes=8; Invariant=8; Beta=2; Raw=253440; Inverse=3984; InverseOdd=1660; Orbit=1520; Relator=720; Ms=1245; Manifest='GAP_TRANSITIVE_DEGREE44_C8_SHARD4_GPT56SOL_MANIFEST.sha256'; ManifestCount=10 }
)

$verified = [System.Collections.Generic.List[object]]::new()
$allScanKeys = [System.Collections.Generic.List[int]]::new()
foreach ($s in $specs) {
    $path = Join-Path $BaseDir $s.File
    $lines = @(Get-Content -LiteralPath $path)
    Assert-Equal @($lines | Where-Object { $_ -match '^CERTIFICATE\t' }).Count 1 "$($s.Name) certificate header"
    Assert-Equal @($lines | Where-Object { $_ -match '^TOTAL\t' }).Count 1 "$($s.Name) TOTAL count"
    Assert-Equal @($lines | Where-Object { $_ -eq 'DONE' }).Count 1 "$($s.Name) DONE count"
    Assert-Equal @($lines | Where-Object { $_ -match '^CANDIDATE_NUMERIC\t' }).Count 0 "$($s.Name) candidate count"
    $total = Parse-Total (@($lines | Where-Object { $_ -match '^TOTAL\t' })[0])
    Assert-Equal $total.RANGE_LO $s.Lo "$($s.Name) range low"
    Assert-Equal $total.RANGE_HI $s.Hi "$($s.Name) range high"
    foreach ($pair in @(
        @('ORDER_WINDOW','Window'),@('PARITY_ENTRIES','Parity'),@('ORDER8_CLASSES','Classes'),
        @('INVARIANT_ALPHA_CLASSES','Invariant'),@('BETA_COMPUTATIONS','Beta'),
        @('FULL_SEED_PAIRS','Raw'),@('INVERSE','Inverse'),@('INVERSE_ODD','InverseOdd'),
        @('ORBIT8','Orbit'),@('RELATOR','Relator'),@('MS','Ms')
    )) { Assert-Equal $total.($pair[0]) $s.($pair[1]) "$($s.Name) $($pair[0])" }
    Assert-Equal $total.B3 0 "$($s.Name) B3"
    Assert-Equal $total.GENERATE 0 "$($s.Name) generate"
    Assert-Equal $total.PARITY 0 "$($s.Name) parity survivors"
    Assert-Equal $total.CENTRALIZER_ORBITS 0 "$($s.Name) centralizer orbits"

    $scanEntries = @(
        foreach ($line in $lines) {
            if ($line -match '^ENTRY\t') { Parse-EntryPairs $line 'ENTRY' }
        }
    )
    Assert-Equal $scanEntries.Count $s.Parity "$($s.Name) ENTRY count"
    Assert-Equal @($lines | Where-Object { $_ -match '^NO_PARITY\t' }).Count ($s.Window-$s.Parity) "$($s.Name) NO_PARITY count"
    Assert-Equal @($lines | Where-Object { $_ -match '^ALPHA\t' }).Count $s.Classes "$($s.Name) ALPHA count"
    Assert-Equal (Sum-Property $scanEntries 'ORDER8_CLASSES') $s.Classes "$($s.Name) ENTRY class sum"
    Assert-Equal (Sum-Property $scanEntries 'FULL_SEED_PAIRS') $s.Raw "$($s.Name) ENTRY raw sum"
    $expectedProfile = @($profile | Where-Object { $_.K -ge $s.Lo -and $_.K -le $s.Hi })
    $keyDiff = @(Compare-Object -ReferenceObject @($expectedProfile | ForEach-Object { $_.K }) -DifferenceObject @($scanEntries | ForEach-Object { $_.K }))
    Assert-Equal $keyDiff.Count 0 "$($s.Name) profile key-set difference"
    foreach ($x in $scanEntries) {
        $p = $profileByKey[[int]$x.K]
        Assert-Equal ([int64]$x.ORDER) $p.Order "$($s.Name) profile order T$($x.K)"
        Assert-Equal ([int64]$x.ORDER8_CLASSES) $p.Classes "$($s.Name) profile classes T$($x.K)"
        Assert-Equal ([int64]$x.FULL_SEED_PAIRS) $p.Raw "$($s.Name) profile raw T$($x.K)"
        $allScanKeys.Add([int]$x.K)
    }
    $manifestHash = Verify-Manifest $s.Manifest $s.ManifestCount
    $verified.Add([pscustomobject]@{ Spec=$s; Total=$total; ManifestHash=$manifestHash })
}

Assert-Equal $allScanKeys.Count 152 'scanned parity-key count'
Assert-Equal @($allScanKeys | Select-Object -Unique).Count 152 'unique scanned parity-key count'
$scannedProfile = @($profile | Where-Object { $_.K -le 228 })
Assert-Equal $scannedProfile.Count 152 'profile keys through 228'
$scanDiff = @(Compare-Object -ReferenceObject @($scannedProfile | ForEach-Object { $_.K }) -DifferenceObject @($allScanKeys))
Assert-Equal $scanDiff.Count 0 'combined scan/profile key-set difference'

$complementProfile = @($profile | Where-Object { $_.K -ge 229 })
$complementCheap = @($cheap | Where-Object { $_.K -ge 229 })
Assert-Equal $complementProfile.Count 51 'zero-complement parity count'
Assert-Equal $complementCheap.Count 53 'zero-complement order-window count'
Assert-Equal @($complementCheap | Where-Object { $_.Parity -gt 0 }).Count 51 'zero-complement cheap parity count'
Assert-Equal (Sum-Property $complementProfile 'Classes') 0 'zero-complement classes'
Assert-Equal (Sum-Property $complementProfile 'Raw') 0 'zero-complement raw'
$complementKeyDiff = @(Compare-Object -ReferenceObject @($complementCheap | Where-Object { $_.Parity -gt 0 } | ForEach-Object { $_.K }) -DifferenceObject @($complementProfile | ForEach-Object { $_.K }))
Assert-Equal $complementKeyDiff.Count 0 'zero-complement cheap/profile keys'

$sumWindow = [int64](($specs | Measure-Object -Property Window -Sum).Sum) + $complementCheap.Count
$sumParity = [int64](($specs | Measure-Object -Property Parity -Sum).Sum) + $complementProfile.Count
$sumClasses = [int64](($specs | Measure-Object -Property Classes -Sum).Sum)
$sumInvariant = [int64](($specs | Measure-Object -Property Invariant -Sum).Sum)
$sumBeta = [int64](($specs | Measure-Object -Property Beta -Sum).Sum)
$sumRaw = [int64](($specs | Measure-Object -Property Raw -Sum).Sum)
$sumInverse = [int64](($specs | Measure-Object -Property Inverse -Sum).Sum)
$sumInverseOdd = [int64](($specs | Measure-Object -Property InverseOdd -Sum).Sum)
$sumOrbit = [int64](($specs | Measure-Object -Property Orbit -Sum).Sum)
$sumRelator = [int64](($specs | Measure-Object -Property Relator -Sum).Sum)
$sumMs = [int64](($specs | Measure-Object -Property Ms -Sum).Sum)
Assert-Equal $sumWindow 227 'full order-window total'
Assert-Equal $sumParity 203 'full parity total'
Assert-Equal $sumClasses 92 'full class total'
Assert-Equal $sumInvariant 92 'full invariant-class total'
Assert-Equal $sumBeta 48 'full beta total'
Assert-Equal $sumRaw 1302312 'full raw total'
Assert-Equal $sumInverse 39376 'full inverse total'
Assert-Equal $sumInverseOdd 22196 'full inverse-odd total'
Assert-Equal $sumOrbit 21184 'full orbit total'
Assert-Equal $sumRelator 13024 'full relator total'
Assert-Equal $sumMs 522389 'full shard GAP-ms total'

$out = [System.Collections.Generic.List[string]]::new()
$out.Add("CERTIFICATE`tPF-GRP-001-C8-TRANSITIVE-DEGREE44-FULL-CLOSURE-VERIFY")
$out.Add("DEGREE`t44")
$out.Add("DATABASE`t2113")
$out.Add("SCANNED_RANGES`t1-109`t110-221`t222-226`t227-228")
$out.Add("PROFILE_ZERO_COMPLEMENT`t229-2113`tORDER_WINDOW`t53`tPARITY_ENTRIES`t51`tORDER8_CLASSES`t0`tRAW_PAIRS`t0")
foreach ($v in $verified) {
    $s=$v.Spec
    $out.Add("SHARD`t$($s.Name)`tRANGE`t$($s.Lo)-$($s.Hi)`tORDER_WINDOW`t$($s.Window)`tPARITY_ENTRIES`t$($s.Parity)`tORDER8_CLASSES`t$($s.Classes)`tRAW_PAIRS`t$($s.Raw)`tB3`t0`tCANDIDATES`t0`tMANIFEST_SHA256`t$($v.ManifestHash)")
}
$out.Add("TOTAL`tORDER_WINDOW`t$sumWindow`tPARITY_ENTRIES`t$sumParity`tORDER8_CLASSES`t$sumClasses`tINVARIANT_ALPHA_CLASSES`t$sumInvariant`tBETA_COMPUTATIONS`t$sumBeta`tFULL_SEED_PAIRS`t$sumRaw`tINVERSE`t$sumInverse`tINVERSE_ODD`t$sumInverseOdd`tORBIT8`t$sumOrbit`tRELATOR`t$sumRelator`tB3`t0`tGENERATE`t0`tPARITY`t0`tCENTRALIZER_ORBITS`t0`tCANDIDATE_NUMERIC`t0`tSHARD_MS`t$sumMs")
$out.Add("PROFILE_KEY_CHECK`tSCANNED_PARITY_KEYS`t152`tCOMPLEMENT_PARITY_KEYS`t51`tDUPLICATES`t0`tOMISSIONS`t0`tCLASS_RAW_MISMATCHES`t0")
$out.Add("BASED_REPLAY`tVACUOUS_B3_AND_CANDIDATE_ZERO")
$out.Add("RESULT`tNo degree-44 TransitiveGroups catalogue target in the frozen order/parity scope survives B3; exact family closure, not a statement about all finite groups.")
$out.Add("DONE")
[System.IO.File]::WriteAllLines((Join-Path $BaseDir $OutputName),$out,[System.Text.UTF8Encoding]::new($false))

Write-Output "PASS window=$sumWindow parity=$sumParity classes=$sumClasses invariant=$sumInvariant beta=$sumBeta raw=$sumRaw inverse=$sumInverse inverseOdd=$sumInverseOdd orbit=$sumOrbit relator=$sumRelator B3=0 candidates=0 complement=51/0/0"
