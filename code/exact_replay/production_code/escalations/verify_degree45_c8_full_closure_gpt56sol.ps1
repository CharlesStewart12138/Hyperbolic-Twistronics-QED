param(
    [string]$BaseDir = ".",
    [string]$OutputName = "GAP_TRANSITIVE_DEGREE45_C8_FULL_CLOSURE_VERIFY_GPT56SOL.txt"
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
    if ($f.Count -lt 4 -or $f[0] -ne $Prefix -or $f[1] -notmatch '^45T([0-9]+)$') {
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
    $rows = @([System.IO.File]::ReadAllLines($path))
    Assert-Equal $rows.Count $ExpectedCount "$Name entry count"
    foreach ($row in $rows) {
        if ($row -notmatch '^([0-9A-F]{64})  (.+)$') { throw "Malformed manifest row in $Name" }
        $want = $Matches[1]; $file = $Matches[2]
        $got = (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $BaseDir $file)).Hash
        Assert-Equal $got $want "$Name hash $file"
    }
    return (Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash
}

function Verify-Replay([string]$Certificate, [string]$Manifest, [int]$Count, [int]$Order) {
    $lines = @([System.IO.File]::ReadAllLines((Join-Path $BaseDir $Certificate)))
    Assert-Equal @($lines | Where-Object { $_ -match '^CERTIFICATE\t' }).Count 1 "$Certificate header"
    Assert-Equal @($lines | Where-Object { $_ -match '^45T' }).Count $Count "$Certificate candidate rows"
    Assert-Equal @($lines | Where-Object { $_ -match "degree=45\torder=$Order\tdistinct=8\tinverse=1\trelator=1\tb3=457\tgenerated=1\tparity=1\twitness_id=[0-9]+\tdepth=8\tword=" }).Count $Count "$Certificate reconstructed gates"
    Assert-Equal @($lines | Where-Object { $_ -eq "CANDIDATES_RECONSTRUCTED`t$Count" }).Count 1 "$Certificate reconstructed count"
    Assert-Equal @($lines | Where-Object { $_ -eq "BASED_REJECTED`t$Count" }).Count 1 "$Certificate rejected count"
    Assert-Equal @($lines | Where-Object { $_ -eq 'BASED_SURVIVORS	0' }).Count 1 "$Certificate survivor count"
    Assert-Equal $lines[-1] 'DONE' "$Certificate terminal marker"
    return Verify-Manifest $Manifest 11
}

$profileLines = @([System.IO.File]::ReadAllLines((Join-Path $BaseDir 'GAP_TRANSITIVE_DEGREE45_AUT_PROFILE_1_10923_GPT56SOL.txt')))
Assert-Equal @($profileLines | Where-Object { $_ -match '^TOTAL\t' }).Count 1 'Aut profile TOTAL count'
Assert-Equal $profileLines[-1] 'DONE' 'Aut profile terminal marker'
$profile = @(
    foreach ($line in $profileLines) {
        if ($line -match '^ENTRY\t') {
            $x = Parse-EntryPairs $line 'ENTRY'
            [pscustomobject]@{ K=$x.K; Order=[int64]$x.ORDER; Classes=[int64]$x.ORDER8_CLASSES; Raw=[int64]$x.RAW_PAIRS }
        }
    }
)
Assert-Equal $profile.Count 521 'full Aut profile entry count'
Assert-Equal (Sum-Property $profile 'Classes') 3662 'full Aut profile classes'
Assert-Equal (Sum-Property $profile 'Raw') 64853010 'full Aut profile raw'
$profileByKey = @{}
foreach ($x in $profile) {
    if ($profileByKey.ContainsKey($x.K)) { throw "Duplicate profile key $($x.K)" }
    Assert-Equal $x.Raw ($x.Order * $x.Classes) "Aut profile raw identity 45T$($x.K)"
    $profileByKey[$x.K] = $x
}
$autManifestHash = Verify-Manifest 'GAP_TRANSITIVE_DEGREE45_AUT_PROFILE_GPT56SOL_MANIFEST.sha256' 14

$cheapLines = @([System.IO.File]::ReadAllLines((Join-Path $BaseDir 'GAP_TRANSITIVE_DEGREE45_ORDER_PARITY_PROFILE_GPT56SOL.txt')))
Assert-Equal @($cheapLines | Where-Object { $_ -match '^TOTAL\t' }).Count 1 'cheap profile TOTAL count'
Assert-Equal $cheapLines[-1] 'DONE' 'cheap profile terminal marker'
$cheap = @(
    foreach ($line in $cheapLines) {
        if ($line -match '^ENTRY\t45T([0-9]+)\tORDER\t([0-9]+)\tPARITY_MAPS\t([0-9]+)$') {
            [pscustomobject]@{ K=[int]$Matches[1]; Order=[int64]$Matches[2]; Parity=[int64]$Matches[3] }
        }
    }
)
Assert-Equal $cheap.Count 590 'cheap order-window count'
$cheapParity = @($cheap | Where-Object { $_.Parity -gt 0 })
Assert-Equal $cheapParity.Count 521 'cheap parity count'
$cheapManifestHash = Verify-Manifest 'GAP_TRANSITIVE_DEGREE45_ORDER_PARITY_PROFILE_GPT56SOL_MANIFEST.sha256' 7

$specs = @(
    [pscustomobject]@{ Name='SHARD1'; File='GAP_TRANSITIVE_DEGREE45_C8_BETA_1_578_GPT56SOL.txt'; Lo=1; Hi=578; Window=332; ParityEntries=292; Classes=2014; Invariant=2014; Beta=443; Raw=16115670; Inverse=514302; InverseOdd=282995; Orbit=236832; Relator=113952; B3=0; Generate=0; ParityGate=0; COrbits=0; Candidates=0; Ms=162752; Manifest='GAP_TRANSITIVE_DEGREE45_C8_SHARD1_GPT56SOL_MANIFEST.sha256'; ManifestCount=9 },
    [pscustomobject]@{ Name='SHARD2'; File='GAP_TRANSITIVE_DEGREE45_C8_BETA_579_708_GPT56SOL.txt'; Lo=579; Hi=708; Window=130; ParityEntries=124; Classes=779; Invariant=779; Beta=213; Raw=16284960; Inverse=341326; InverseOdd=183417; Orbit=157120; Relator=65152; B3=64; Generate=64; ParityGate=64; COrbits=4; Candidates=4; Ms=112965; Manifest='GAP_TRANSITIVE_DEGREE45_C8_SHARD2_GPT56SOL_MANIFEST.sha256'; ManifestCount=20 },
    [pscustomobject]@{ Name='SHARD3'; File='GAP_TRANSITIVE_DEGREE45_C8_BETA_709_782_GPT56SOL.txt'; Lo=709; Hi=782; Window=74; ParityEntries=66; Classes=500; Invariant=500; Beta=222; Raw=16378560; Inverse=295504; InverseOdd=141296; Orbit=122880; Relator=44736; B3=416; Generate=416; ParityGate=416; COrbits=10; Candidates=10; Ms=78873; Manifest='GAP_TRANSITIVE_DEGREE45_C8_SHARD3_GPT56SOL_MANIFEST.sha256'; ManifestCount=20 },
    [pscustomobject]@{ Name='SHARD4'; File='GAP_TRANSITIVE_DEGREE45_C8_BETA_783_10923_GPT56SOL.txt'; Lo=783; Hi=10923; Window=54; ParityEntries=39; Classes=369; Invariant=369; Beta=123; Raw=16073820; Inverse=255388; InverseOdd=152337; Orbit=139504; Relator=56944; B3=64; Generate=0; ParityGate=0; COrbits=0; Candidates=0; Ms=77550; Manifest='GAP_TRANSITIVE_DEGREE45_C8_SHARD4_GPT56SOL_MANIFEST.sha256'; ManifestCount=9 }
)

$verified = [System.Collections.Generic.List[object]]::new()
$allScanKeys = [System.Collections.Generic.List[int]]::new()
foreach ($s in $specs) {
    $lines = @([System.IO.File]::ReadAllLines((Join-Path $BaseDir $s.File)))
    Assert-Equal @($lines | Where-Object { $_ -match '^CERTIFICATE\t' }).Count 1 "$($s.Name) header"
    Assert-Equal @($lines | Where-Object { $_ -match '^TOTAL\t' }).Count 1 "$($s.Name) TOTAL count"
    Assert-Equal @($lines | Where-Object { $_ -eq 'DONE' }).Count 1 "$($s.Name) DONE count"
    Assert-Equal $lines[-1] 'DONE' "$($s.Name) terminal marker"
    Assert-Equal @($lines | Where-Object { $_ -match '^CANDIDATE_NUMERIC\t' }).Count $s.Candidates "$($s.Name) candidate count"
    $total = Parse-Total (@($lines | Where-Object { $_ -match '^TOTAL\t' })[0])
    Assert-Equal $total.RANGE_LO $s.Lo "$($s.Name) range low"
    Assert-Equal $total.RANGE_HI $s.Hi "$($s.Name) range high"
    foreach ($pair in @(
        @('ORDER_WINDOW','Window'),@('PARITY_ENTRIES','ParityEntries'),@('ORDER8_CLASSES','Classes'),
        @('INVARIANT_ALPHA_CLASSES','Invariant'),@('BETA_COMPUTATIONS','Beta'),@('FULL_SEED_PAIRS','Raw'),
        @('INVERSE','Inverse'),@('INVERSE_ODD','InverseOdd'),@('ORBIT8','Orbit'),@('RELATOR','Relator'),
        @('B3','B3'),@('GENERATE','Generate'),@('PARITY','ParityGate'),@('CENTRALIZER_ORBITS','COrbits'),@('MS','Ms')
    )) { Assert-Equal $total.($pair[0]) $s.($pair[1]) "$($s.Name) $($pair[0])" }

    $scanEntries = @(
        foreach ($line in $lines) {
            if ($line -match '^ENTRY\t') { Parse-EntryPairs $line 'ENTRY' }
        }
    )
    Assert-Equal $scanEntries.Count $s.ParityEntries "$($s.Name) ENTRY count"
    Assert-Equal @($lines | Where-Object { $_ -match '^NO_PARITY\t' }).Count ($s.Window-$s.ParityEntries) "$($s.Name) NO_PARITY count"
    Assert-Equal @($lines | Where-Object { $_ -match '^ALPHA\t' }).Count $s.Classes "$($s.Name) ALPHA count"
    foreach ($pair in @(
        @('ORDER8_CLASSES','Classes'),@('INVARIANT_ALPHA_CLASSES','Invariant'),@('DISTINCT_BETA','Beta'),
        @('FULL_SEED_PAIRS','Raw'),@('INVERSE','Inverse'),@('INVERSE_ODD','InverseOdd'),@('ORBIT8','Orbit'),
        @('RELATOR','Relator'),@('B3','B3'),@('GENERATE','Generate'),@('CENTRALIZER_ORBITS','COrbits')
    )) { Assert-Equal (Sum-Property $scanEntries $pair[0]) $s.($pair[1]) "$($s.Name) ENTRY $($pair[0]) sum" }

    $expectedProfile = @($profile | Where-Object { $_.K -ge $s.Lo -and $_.K -le $s.Hi })
    Assert-Equal $expectedProfile.Count $s.ParityEntries "$($s.Name) profile entry count"
    $keyDiff = @(Compare-Object -ReferenceObject @($expectedProfile | ForEach-Object { $_.K }) -DifferenceObject @($scanEntries | ForEach-Object { $_.K }))
    Assert-Equal $keyDiff.Count 0 "$($s.Name) profile key-set difference"
    foreach ($x in $scanEntries) {
        $p = $profileByKey[[int]$x.K]
        Assert-Equal ([int64]$x.ORDER) $p.Order "$($s.Name) profile order 45T$($x.K)"
        Assert-Equal ([int64]$x.ORDER8_CLASSES) $p.Classes "$($s.Name) profile classes 45T$($x.K)"
        Assert-Equal ([int64]$x.FULL_SEED_PAIRS) $p.Raw "$($s.Name) profile raw 45T$($x.K)"
        $allScanKeys.Add([int]$x.K)
    }
    $manifestHash = Verify-Manifest $s.Manifest $s.ManifestCount
    $verified.Add([pscustomobject]@{ Spec=$s; ManifestHash=$manifestHash })
}

Assert-Equal $allScanKeys.Count 521 'combined scan parity-key count'
Assert-Equal @($allScanKeys | Select-Object -Unique).Count 521 'unique scan parity-key count'
Assert-Equal @(Compare-Object -ReferenceObject @($profile | ForEach-Object { $_.K }) -DifferenceObject @($allScanKeys)).Count 0 'combined scan/Aut profile key-set difference'
Assert-Equal @(Compare-Object -ReferenceObject @($cheapParity | ForEach-Object { $_.K }) -DifferenceObject @($allScanKeys)).Count 0 'combined scan/cheap parity key-set difference'

$sumWindow = Sum-Property $specs 'Window'
$sumParity = Sum-Property $specs 'ParityEntries'
$sumClasses = Sum-Property $specs 'Classes'
$sumInvariant = Sum-Property $specs 'Invariant'
$sumBeta = Sum-Property $specs 'Beta'
$sumRaw = Sum-Property $specs 'Raw'
$sumInverse = Sum-Property $specs 'Inverse'
$sumInverseOdd = Sum-Property $specs 'InverseOdd'
$sumOrbit = Sum-Property $specs 'Orbit'
$sumRelator = Sum-Property $specs 'Relator'
$sumB3 = Sum-Property $specs 'B3'
$sumGenerate = Sum-Property $specs 'Generate'
$sumParityGate = Sum-Property $specs 'ParityGate'
$sumCOrbits = Sum-Property $specs 'COrbits'
$sumCandidates = Sum-Property $specs 'Candidates'
$sumMs = Sum-Property $specs 'Ms'
foreach ($pair in @(
    @($sumWindow,590,'window'),@($sumParity,521,'parity entries'),@($sumClasses,3662,'classes'),
    @($sumInvariant,3662,'invariant classes'),@($sumBeta,1001,'beta'),@($sumRaw,64853010,'raw'),
    @($sumInverse,1406520,'inverse'),@($sumInverseOdd,760045,'inverse odd'),@($sumOrbit,656336,'orbit'),
    @($sumRelator,280784,'relator'),@($sumB3,544,'B3'),@($sumGenerate,480,'generate'),
    @($sumParityGate,480,'parity gate'),@($sumCOrbits,14,'centralizer orbits'),@($sumCandidates,14,'candidates'),
    @($sumMs,432140,'shard GAP ms')
)) { Assert-Equal $pair[0] $pair[1] "full $($pair[2])" }

$replay2Hash = Verify-Replay 'GAP_TRANSITIVE_DEGREE45_C8_BASED_REPLAY_579_708_GPT56SOL.txt' 'GAP_TRANSITIVE_DEGREE45_C8_BASED_REPLAY_579_708_GPT56SOL_MANIFEST.sha256' 4 22500
$replay3Hash = Verify-Replay 'GAP_TRANSITIVE_DEGREE45_C8_BASED_REPLAY_709_782_GPT56SOL.txt' 'GAP_TRANSITIVE_DEGREE45_C8_BASED_REPLAY_709_782_GPT56SOL_MANIFEST.sha256' 10 38880

$out = [System.Collections.Generic.List[string]]::new()
$out.Add("CERTIFICATE`tPF-GRP-001-C8-TRANSITIVE-DEGREE45-FULL-CLOSURE-VERIFY")
$out.Add("DEGREE`t45")
$out.Add("DATABASE`t10923")
$out.Add("SCANNED_RANGES`t1-578`t579-708`t709-782`t783-10923")
$out.Add("AUT_PROFILE_MANIFEST_SHA256`t$autManifestHash")
$out.Add("CHEAP_PROFILE_MANIFEST_SHA256`t$cheapManifestHash")
foreach ($v in $verified) {
    $s=$v.Spec
    $out.Add("SHARD`t$($s.Name)`tRANGE`t$($s.Lo)-$($s.Hi)`tORDER_WINDOW`t$($s.Window)`tPARITY_ENTRIES`t$($s.ParityEntries)`tORDER8_CLASSES`t$($s.Classes)`tRAW_PAIRS`t$($s.Raw)`tB3`t$($s.B3)`tCANDIDATES`t$($s.Candidates)`tMANIFEST_SHA256`t$($v.ManifestHash)")
}
$out.Add("TOTAL`tORDER_WINDOW`t$sumWindow`tPARITY_ENTRIES`t$sumParity`tORDER8_CLASSES`t$sumClasses`tINVARIANT_ALPHA_CLASSES`t$sumInvariant`tBETA_COMPUTATIONS`t$sumBeta`tFULL_SEED_PAIRS`t$sumRaw`tINVERSE`t$sumInverse`tINVERSE_ODD`t$sumInverseOdd`tORBIT8`t$sumOrbit`tRELATOR`t$sumRelator`tB3`t$sumB3`tGENERATE`t$sumGenerate`tPARITY`t$sumParityGate`tCENTRALIZER_ORBITS`t$sumCOrbits`tCANDIDATE_NUMERIC`t$sumCandidates`tSHARD_MS`t$sumMs")
$out.Add("PROFILE_KEY_CHECK`tAUT_PARITY_KEYS`t521`tCHEAP_PARITY_KEYS`t521`tSCANNED_PARITY_KEYS`t521`tDUPLICATES`t0`tOMISSIONS`t0`tCLASS_RAW_MISMATCHES`t0")
$out.Add("REPLAY`tCANDIDATES`t14`tDISTINCT`t14`tINVERSE`t14`tRELATOR`t14`tB3_457`t14`tGENERATED`t14`tALL_GENERATORS_ODD_C2`t14`tBASED_REJECTED`t14`tBASED_SURVIVORS`t0")
$out.Add("REPLAY_SHARD2_MANIFEST_SHA256`t$replay2Hash")
$out.Add("REPLAY_SHARD3_MANIFEST_SHA256`t$replay3Hash")
$out.Add("RESULT`tNo degree-45 TransitiveGroups catalogue target in the frozen order/parity scope survives the complete frozen based-tree gate; exact family closure, not a statement about all finite groups.")
$out.Add("DONE")
[System.IO.File]::WriteAllLines((Join-Path $BaseDir $OutputName),$out,[System.Text.UTF8Encoding]::new($false))

Write-Output "PASS window=$sumWindow parity=$sumParity classes=$sumClasses invariant=$sumInvariant beta=$sumBeta raw=$sumRaw inverse=$sumInverse inverseOdd=$sumInverseOdd orbit=$sumOrbit relator=$sumRelator B3=$sumB3 generate=$sumGenerate candidates=$sumCandidates basedRejected=14 survivors=0"
