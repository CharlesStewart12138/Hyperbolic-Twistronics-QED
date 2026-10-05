param([string]$BaseDir = ".")

$ErrorActionPreference = "Stop"
$outName = "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_1_5962_CHECKPOINT_GPT56SOL.txt"
$stdoutName = "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD01_RUN_STDOUT_GPT56SOL.txt"
$stderrName = "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD01_RUN_STDERR_GPT56SOL.txt"
$verifyName = "GAP_TRANSITIVE_DEGREE24_AUT_PROFILE_SHARD01_VERIFY_GPT56SOL.txt"

function Assert-Eq($Actual, $Expected, [string]$Label) {
    if ($Actual -ne $Expected) { throw "$Label mismatch: actual=$Actual expected=$Expected" }
}
function Parse-Entry([string]$Line, [int]$Index) {
    $f = $Line -split "`t"
    if ($f.Count -ne 20 -or $f[0] -ne 'ENTRY' -or $f[1] -notmatch '^24T([0-9]+)$') {
        throw "malformed ENTRY at line $($Index+1): $Line"
    }
    $k = [int]$Matches[1]
    $h = @{}
    for ($i=2; $i -lt $f.Count; $i+=2) { $h[$f[$i]]=$f[$i+1] }
    foreach ($required in @('ORDER','SOLVABLE_G','PARITY_MAPS','AUT_ORDER','AUT_MS','METHOD','CLASS_MS','ORDER8_CLASSES','RAW_PAIRS')) {
        if (-not $h.ContainsKey($required)) { throw "missing $required at line $($Index+1)" }
    }
    [pscustomobject]@{
        Index=$Index; K=$k; Order=[int64]$h.ORDER; Solvable=$h.SOLVABLE_G;
        Parity=[int64]$h.PARITY_MAPS; AutOrder=[int64]$h.AUT_ORDER;
        AutMs=[int64]$h.AUT_MS; Method=$h.METHOD; ClassMs=[int64]$h.CLASS_MS;
        Classes=[int64]$h.ORDER8_CLASSES; Raw=[int64]$h.RAW_PAIRS
    }
}
function Parse-Pairs([string]$Line, [string]$Prefix) {
    $f=$Line -split "`t"
    if ($f[0] -ne $Prefix -or (($f.Count-1) % 2) -ne 0) { throw "malformed $Prefix line: $Line" }
    $h=@{}
    for($i=1; $i -lt $f.Count; $i+=2) { $h[$f[$i]]=$f[$i+1] }
    return $h
}
function Read-SealedEntryMap([string]$Name, [bool]$HasSolvable) {
    $map=@{}
    foreach($line in [IO.File]::ReadAllLines((Join-Path $BaseDir $Name))) {
        if($line -notmatch '^ENTRY\t24T([0-9]+)\t') { continue }
        $k=[int]$Matches[1]
        $f=$line -split "`t"; $h=@{}
        for($i=2; $i -lt $f.Count; $i+=2) { $h[$f[$i]]=$f[$i+1] }
        $map[$k]=[pscustomobject]@{
            Order=[int64]$h.ORDER; Parity=[int64]$h.PARITY_MAPS;
            Solvable=if($HasSolvable){[int]$h.SOLVABLE}else{$null}
        }
    }
    return $map
}

$path=Join-Path $BaseDir $outName
$lines=[IO.File]::ReadAllLines($path)
if($lines.Count -lt 12){throw 'profile output too short'}
$expectedHeader=@(
    "CERTIFICATE_PROFILE`tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-CHECKPOINT",
    "GAP_VERSION`t4.12.1",
    "DATABASE`t25000",
    "RANGE`t1`t5962",
    "GUARD_MS`t1320000",
    "EXPECTED_ORDER_WINDOW`t810",
    "EXPECTED_PARITY`t798"
)
for($i=0;$i -lt $expectedHeader.Count;$i++){Assert-Eq $lines[$i] $expectedHeader[$i] "header line $($i+1)"}
Assert-Eq @($lines | Where-Object {$_ -match '^TOTAL\t'}).Count 1 'TOTAL count'
Assert-Eq @($lines | Where-Object {$_ -eq 'DONE'}).Count 1 'DONE count'
Assert-Eq $lines[-1] 'DONE' 'terminal marker'
Assert-Eq @($lines | Where-Object {$_ -match '^(TOTAL_PARTIAL|STOPPED_GUARD)'}).Count 0 'guard marker count'

$sol=Read-SealedEntryMap 'GAP_TRANSITIVE_DEGREE24_SOLVABILITY_1_7860_GPT56SOL.txt' $true
$win=Read-SealedEntryMap 'GAP_TRANSITIVE_DEGREE24_PARITY_1_7860_GPT56SOL.txt' $false
$expectedKeys=@($sol.Keys | ForEach-Object {[int]$_} | Where-Object {$_ -ge 1 -and $_ -le 5962} | Sort-Object)
$windowKeys=@($win.Keys | ForEach-Object {[int]$_} | Where-Object {$_ -ge 1 -and $_ -le 5962} | Sort-Object)
Assert-Eq $expectedKeys.Count 798 'sealed expected parity keys'
Assert-Eq $windowKeys.Count 810 'sealed expected window keys'

$entries=@()
for($i=0;$i -lt $lines.Count;$i++){if($lines[$i] -match '^ENTRY\t'){$entries+=Parse-Entry $lines[$i] $i}}
Assert-Eq $entries.Count 798 'ENTRY count'
Assert-Eq @($entries | Group-Object K | Where-Object {$_.Count -ne 1}).Count 0 'duplicate ENTRY keys'
Assert-Eq @(Compare-Object -ReferenceObject $expectedKeys -DifferenceObject @($entries.K)).Count 0 'ENTRY keyset difference'

[int64]$cumClasses=0; [int64]$cumRaw=0; [int64]$cumAutMs=0; [int64]$cumClassMs=0; $previousK=0
foreach($e in $entries){
    if($e.K -le $previousK){throw "non-increasing ENTRY key $($e.K)"}; $previousK=$e.K
    $s=$sol[$e.K]
    Assert-Eq $e.Order $s.Order "24T$($e.K) order"
    Assert-Eq $e.Parity $s.Parity "24T$($e.K) parity maps"
    Assert-Eq $e.Solvable $(if($s.Solvable -eq 1){'true'}else{'false'}) "24T$($e.K) solvability"
    Assert-Eq $e.Raw ($e.Order*$e.Classes) "24T$($e.K) raw identity"
    if($e.Parity -le 0 -or $e.AutOrder -le 0 -or $e.AutMs -lt 0 -or $e.ClassMs -lt 0){throw "invalid numeric field at 24T$($e.K)"}
    if($e.Method -notin @('pc','native')){throw "invalid method at 24T$($e.K)"}
    $cumClasses+=$e.Classes; $cumRaw+=$e.Raw; $cumAutMs+=$e.AutMs; $cumClassMs+=$e.ClassMs
    $next=$lines[$e.Index+1]
    $cp=Parse-Pairs $next 'CHECKPOINT'
    Assert-Eq ([int]$cp.LAST_COMPLETE_K) $e.K "24T$($e.K) checkpoint key"
    Assert-Eq ([int]$cp.PROCESSED) ([array]::IndexOf($entries,$e)+1) "24T$($e.K) checkpoint processed"
    Assert-Eq ([int64]$cp.ORDER8_CLASSES) $cumClasses "24T$($e.K) checkpoint classes"
    Assert-Eq ([int64]$cp.RAW_PAIRS) $cumRaw "24T$($e.K) checkpoint raw"
}

$scanLines=@($lines | Where-Object {$_ -match '^SCAN_CHECKPOINT\t'})
Assert-Eq $scanLines.Count ([math]::Floor(5962/25)) 'SCAN_CHECKPOINT count'
for($j=0;$j -lt $scanLines.Count;$j++){
    $s=Parse-Pairs $scanLines[$j] 'SCAN_CHECKPOINT'; $k=25*($j+1)
    Assert-Eq ([int]$s.LAST_COMPLETE_K) $k "scan checkpoint key $k"
    Assert-Eq ([int]$s.ORDER_WINDOW) @($windowKeys | Where-Object {$_ -le $k}).Count "scan checkpoint window $k"
    Assert-Eq ([int]$s.PROCESSED) @($entries | Where-Object {$_.K -le $k}).Count "scan checkpoint processed $k"
    Assert-Eq ([int64]$s.ORDER8_CLASSES) ([int64](($entries | Where-Object {$_.K -le $k} | Measure-Object Classes -Sum).Sum)) "scan checkpoint classes $k"
    Assert-Eq ([int64]$s.RAW_PAIRS) ([int64](($entries | Where-Object {$_.K -le $k} | Measure-Object Raw -Sum).Sum)) "scan checkpoint raw $k"
}

$totalLine=@($lines | Where-Object {$_ -match '^TOTAL\t'})[0]
$pattern='^TOTAL\tDEGREE\t24\tDATABASE\t25000\tRANGE\t1\t5962\tLAST_COMPLETE_K\t5962\tORDER_WINDOW\t810\tPROCESSED\t798\tORDER8_CLASSES\t([0-9]+)\tRAW_PAIRS\t([0-9]+)\tAUT_MS\t([0-9]+)\tCLASS_MS\t([0-9]+)\tMS\t([0-9]+)$'
if($totalLine -notmatch $pattern){throw "malformed TOTAL: $totalLine"}
Assert-Eq ([int64]$Matches[1]) $cumClasses 'TOTAL classes'
Assert-Eq ([int64]$Matches[2]) $cumRaw 'TOTAL raw'
Assert-Eq ([int64]$Matches[3]) $cumAutMs 'TOTAL AutMs'
Assert-Eq ([int64]$Matches[4]) $cumClassMs 'TOTAL ClassMs'
$totalMs=[int64]$Matches[5]

$stdout=[IO.File]::ReadAllText((Join-Path $BaseDir $stdoutName))
$stderr=[IO.File]::ReadAllText((Join-Path $BaseDir $stderrName))
if($stdout.Trim() -ne "WROTE /mnt/d/work/revise/production_code/escalations/$outName"){throw 'unexpected stdout'}
if($stderr -notmatch 'Exit status: 0' -or $stderr -notmatch 'Maximum resident set size \(kbytes\): ([0-9]+)'){throw 'missing successful runtime telemetry'}
$rssKb=[int64]$Matches[1]
if($rssKb -ge 50331648){throw "RSS exceeded guard: $rssKb"}

$result=@(
    "CERTIFICATE_VERIFY`tPF-GRP-001-C8-TRANSITIVE-DEGREE24-AUT-PROFILE-SHARD01",
    "RANGE`t1`t5962",
    "ORDER_WINDOW`t810",
    "PARITY_KEYS`t798",
    "ENTRY_KEYS_EXACT`tPASS",
    "RAW_IDENTITIES`t798`tPASS",
    "ENTRY_CHECKPOINT_PAIRS`t798`tPASS",
    "SCAN_CHECKPOINTS`t$($scanLines.Count)`tPASS",
    "ORDER8_CLASSES`t$cumClasses",
    "RAW_PAIRS`t$cumRaw",
    "AUT_MS`t$cumAutMs",
    "CLASS_MS`t$cumClassMs",
    "TOTAL_MS`t$totalMs",
    "MAX_RSS_KB`t$rssKb",
    "HEADER_UNIQUE_TOTAL_DONE_NO_GUARD`tPASS",
    "STDOUT_STDERR_TELEMETRY`tPASS",
    "SCOPE`tExact Aut/order-8 profile only; no seed predicates.",
    "VERIFY`tPASS",
    "DONE"
)
[IO.File]::WriteAllLines((Join-Path $BaseDir $verifyName),$result,[Text.UTF8Encoding]::new($false))
Write-Output "PASS entries=798 window=810 classes=$cumClasses raw=$cumRaw autMs=$cumAutMs classMs=$cumClassMs totalMs=$totalMs rssKb=$rssKb scans=$($scanLines.Count)"
